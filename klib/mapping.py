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
then ``disambiguate.by_hard_code`` as a fallback. Output CSV lists ``target_package`` (Kotlin package names only).

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


def generate_mapping() -> list[tuple[str, str, str, str]]:
    """
    Build source→target rows by declaration path (``config``: ``KLIB``, ``SOURCE_KLIBS``,
    ``TARGET_KLIBS``).

    Each row is ``(source_package, declaration, status, target_package)`` —
    one row per source klib that exports that source fqname, represented by ``source_package``
    and ``declaration`` as in the dump; a given declaration path appears at most once per klib.
    ``target_package`` is the Kotlin package name (or sorted ``|``-joined names when ambiguous).
    Ambiguous or missing rows may resolve by ``gles3``, then ``by_header`` (ctags), then ``by_hard_code``.
    """
    source_records = declarations.collect_from_klibs(
        KLIB, SOURCE_KLIBS, progress_desc="source klibs"
    )

    target_records = declarations.collect_from_klibs(
        KLIB, TARGET_KLIBS, progress_desc="target klibs"
    )
    target_klib_by_declaration: dict[str, dict[str, Path]] = defaultdict(dict)
    for klib_name, pkg, declaration in target_records:
        kd = (TARGET_KLIBS / klib_name).resolve()
        target_klib_by_declaration[declaration][pkg] = kd

    can_disambiguate = (
        SOURCE_SYSROOT is not None
        and SOURCE_SYSROOT.is_dir()
        and shutil.which(CTAGS_BIN)
    )

    rows: list[tuple[str, str, str, str]] = []
    for klib, pkg, declaration in source_records:
        pkg_to_klib = target_klib_by_declaration.get(declaration, {})
        pkgs_sorted = sorted(pkg_to_klib.keys())
        n = len(pkgs_sorted)
        if n == 0:
            status, tgt = "missing", ""
        elif n == 1:
            status, tgt = "mapped", pkgs_sorted[0]
        else:
            status, tgt = "ambiguous", "|".join(pkgs_sorted)
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
        rows.append((pkg, declaration, status, tgt))

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
            ["source_package", "declaration", "status", "target_package"]
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
