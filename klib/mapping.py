#!/usr/bin/env python3
"""
Map source-klib fqnames to target-klib fqnames by declaration path.

For each declaration string ``d`` (the part after ``pkg/`` in dump lines), target may
contain zero, one, or many fqnames. Status: ``mapped`` (1→1), ``ambiguous`` (1→many),
``missing`` (1→0).

Ambiguous rows may be resolved when ``config.SOURCE_SYSROOT`` and Universal Ctags are
available: Phase A uses this row’s source klib ``includedHeaders`` + ctags to infer a
single defining header; Phase B selects the target whose manifest (pre-read per klib)
lists that path (see ``disambiguate.by_header``). Rule-based steps: ``disambiguate.gles3``,
then ``disambiguate.by_hard_code`` as a fallback. Output CSV lists ``target_package`` and optional
``target_declaration`` for nested cinterop names (``::``).

Paths and ``klib`` binary come from ``config`` (not ``.env``). Writes
``mapping-{source compilerVersion}-to-{target compilerVersion}.csv`` under ``mappings/``
(versions from each prebuilt’s ``konan/konan.properties``).
"""
from __future__ import annotations

import csv
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from typing import Callable

import declarations
import disambiguate

from config import (
    CTAGS_BIN,
    KLIB,
    SOURCE_KLIBS,
    SOURCE_SYSROOT,
    TARGET_KLIBS,
)


def get_compiler_version(klibs_platform_dir: Path) -> str:
    """``compilerVersion`` from ``…/konan/konan.properties`` (prebuilt root = three parents above platform leaf)."""
    path = klibs_platform_dir.resolve().parent.parent.parent / "konan" / "konan.properties"
    if not path.is_file():
        raise FileNotFoundError(f"konan.properties not found: {path}")
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            if key.strip() == "compilerVersion":
                return value.strip()
    raise KeyError(f"compilerVersion not found in {path}")


def simple_tail(declaration: str) -> str:
    """
    Tail key for fallback matching when there is no exact target declaration.

    Splits only on ``::`` (Kotlin/Native nested metadata). Dotted paths like ``Foo.Bar`` stay
    **whole** so they do not collapse onto a generic last segment (e.g. ``Companion``).
    """
    if "::" in declaration:
        return declaration.split("::")[-1]
    return declaration


def build_target_simple_tail_index(
    target_records: list[tuple[str, str, str]],
    *,
    tail_fn: Callable[[str], str] = simple_tail,
) -> dict[str, list[tuple[str, str, Path]]]:
    """
    Map tail key -> list of ``(package, full_declaration, klib_dir)`` for each target
    occurrence (used when source declaration string has no exact target match).
    """
    index: dict[str, list[tuple[str, str, Path]]] = defaultdict(list)
    for klib_name, pkg, declaration in target_records:
        kd = (TARGET_KLIBS / klib_name).resolve()
        index[tail_fn(declaration)].append((pkg, declaration, kd))
    return dict(index)


def generate_mapping(
    *,
    tail_fn: Callable[[str], str] = simple_tail,
    source_records: list[tuple[str, str, str]] | None = None,
    target_records: list[tuple[str, str, str]] | None = None,
) -> list[tuple[str, str, str, str, str]]:
    """
    Build source→target rows by declaration path (``config``: ``KLIB``, ``SOURCE_KLIBS``,
    ``TARGET_KLIBS``).

    Each row is ``(source_package, declaration, status, target_package, target_declaration)`` —
    one row per source klib that exports that source fqname, represented by ``source_package``
    and ``declaration`` as in the dump; a given declaration path appears at most once per klib.
    ``target_package`` is the Kotlin package name (or sorted ``|``-joined names when ambiguous).
    ``target_declaration`` is empty when the target uses the same dotted path as today; when the
    target klib exposes a nested name (``::``), it holds the **full** target declaration string
    (e.g. ``Rdb_KeyInfo::Rdb_KeyData``) for ``migrate.py`` to emit backticks + typealias.
    Ambiguous or missing rows may resolve by ``gles3``, then ``by_header`` (ctags), then ``by_hard_code``.
    """
    if source_records is None:
        source_records = declarations.collect_from_klibs(
            KLIB, SOURCE_KLIBS, progress_desc="source klibs"
        )

    if target_records is None:
        target_records = declarations.collect_from_klibs(
            KLIB, TARGET_KLIBS, progress_desc="target klibs"
        )
    target_klib_by_declaration: dict[str, dict[str, Path]] = defaultdict(dict)
    for klib_name, pkg, declaration in target_records:
        kd = (TARGET_KLIBS / klib_name).resolve()
        target_klib_by_declaration[declaration][pkg] = kd

    target_by_simple_tail = build_target_simple_tail_index(
        target_records, tail_fn=tail_fn
    )

    can_disambiguate = (
        SOURCE_SYSROOT is not None
        and SOURCE_SYSROOT.is_dir()
        and shutil.which(CTAGS_BIN)
    )

    rows: list[tuple[str, str, str, str, str]] = []
    for klib, pkg, declaration in source_records:
        pkg_to_klib = dict(target_klib_by_declaration.get(declaration, {}))
        tgt_decl_by_pkg: dict[str, str] = {}
        forced_ambiguous = False

        if not pkg_to_klib:
            tail = tail_fn(declaration)
            triples = target_by_simple_tail.get(tail, [])
            by_pkg: dict[str, list[tuple[str, Path]]] = defaultdict(list)
            for tgt_pkg, tgt_decl, kd in triples:
                by_pkg[tgt_pkg].append((tgt_decl, kd))

            pkg_to_klib = {}
            conflict_same_pkg = False
            for tgt_pkg, pairs in by_pkg.items():
                decls = {p[0] for p in pairs}
                if len(decls) > 1:
                    conflict_same_pkg = True
                    break
                pkg_to_klib[tgt_pkg] = pairs[0][1]
                tgt_decl_by_pkg[tgt_pkg] = pairs[0][0]

            if conflict_same_pkg:
                forced_ambiguous = True
                pkg_to_klib = {t[0]: t[2] for t in triples}
                tgt_decl_by_pkg = {}

        pkgs_sorted = sorted(pkg_to_klib.keys())
        n = len(pkgs_sorted)
        if forced_ambiguous:
            status, tgt, tgt_decl = "ambiguous", "|".join(pkgs_sorted), ""
        elif n == 0:
            status, tgt, tgt_decl = "missing", "", ""
        elif n == 1:
            status, tgt = "mapped", pkgs_sorted[0]
            tgt_decl = tgt_decl_by_pkg.get(tgt, "")
        else:
            status, tgt = "ambiguous", "|".join(pkgs_sorted)
            tgt_decl = ""
            resolved = disambiguate.gles3(pkg, pkg_to_klib)
            if resolved is None and can_disambiguate:
                resolved = disambiguate.by_header(
                    source_klib_fdr=klib,
                    declaration=declaration,
                    target_pkg_to_klib=pkg_to_klib,
                )
            if resolved is None:
                resolved = disambiguate.by_hard_code(pkg, declaration)
            if resolved is not None:
                status, tgt = "mapped", resolved
                tgt_decl = tgt_decl_by_pkg.get(resolved, "")
        rows.append((pkg, declaration, status, tgt, tgt_decl))

    return rows


def main() -> None:
    if not KLIB.is_file():
        print(f"error: klib binary not found: {KLIB}", file=sys.stderr)
        sys.exit(1)
    try:
        source_ver = get_compiler_version(SOURCE_KLIBS)
        target_ver = get_compiler_version(TARGET_KLIBS)
    except (OSError, KeyError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

    rows = generate_mapping()
    out_path = Path("mappings") / Path(f"mapping-{source_ver}-to-{target_ver}.csv")
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "source_package",
                "declaration",
                "status",
                "target_package",
                "target_declaration",
            ]
        )
        w.writerows(rows)

    n_source = len(rows)
    mapped = sum(1 for r in rows if r[2] == "mapped")
    ambiguous = sum(1 for r in rows if r[2] == "ambiguous")
    missing = sum(1 for r in rows if r[2] == "missing")
    print(
        f"wrote {out_path.resolve()}  "
        f"source_rows={n_source} mapped={mapped} ambiguous={ambiguous} missing={missing}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
