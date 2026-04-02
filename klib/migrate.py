#!/usr/bin/env python3
"""
Migrate Kotlin ``import`` lines from source-version platform FQ names to target-version
FQ names using a mapping CSV (see ``mapping.py``). Only OH source-set ``.kt`` files
(``source_paths.collect`` + ``config``).

Imports are assumed **compiling Kotlin** and **IDEA “Optimize Imports”**-style layout:
one statement per line, no comments inside the dotted path, optional ``//`` / ``/*``
only after the path (or after ``as``).
"""
from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass, field
from pathlib import Path

import source_paths

from config import (
    MIGRATING_PROJECT,
    SOURCE_COMPILER_VERSION,
    SOURCE_SET_NAMES,
    TARGET_COMPILER_VERSION,
)


def resolve_mapping_csv(
    source_compiler_version: str, target_compiler_version: str,
) -> Path | None:
    """
    Look for ``mapping-{source}-to-{target}.csv`` under ``klib/mappings/`` first
    (same as ``mapping.py`` output), then next to this script (``klib/``).
    """
    klib_dir = Path(__file__).resolve().parent
    name = f"mapping-{source_compiler_version}-to-{target_compiler_version}.csv"
    for p in (klib_dir / "mappings" / name, klib_dir / name):
        if p.is_file():
            return p
    return None

def _dotted_import_path(s: str) -> bool:
    """Non-empty dot-separated segments of letters, digits, or underscores."""
    if not s:
        return False
    return all(
        seg and all(c.isalnum() or c == "_" for c in seg) for seg in s.split(".")
    )


def _strip_trailing_semicolons(s: str) -> str:
    s = s.rstrip()
    while s.endswith(";"):
        s = s[:-1].rstrip()
    return s


def _import_tail_before_comments(tail: str) -> str:
    """Drop ``//`` line comment and ``/*`` block start (IDEA-style: path before these)."""
    cut = len(tail)
    if "//" in tail:
        cut = min(cut, tail.index("//"))
    if "/*" in tail:
        cut = min(cut, tail.index("/*"))
    return tail[:cut]


def _import_path_start_index(line: str, li: int) -> int | None:
    """
    If ``line[li:]`` is ``import`` plus at least one space/tab, return the index of
    the first import-path character (Kotlin allows ``import\\tfoo``).
    """
    if not line[li:].startswith("import"):
        return None
    j = li + len("import")
    if j >= len(line) or line[j] not in " \t":
        return None
    while j < len(line) and line[j] in " \t":
        j += 1
    return j


def import_path_fqname_and_span(line: str) -> tuple[str, int, int] | None:
    """
    For a single physical line, return ``(fqname, start, end)`` where ``line[start:end]``
    is the import path text to replace, and ``fqname`` is that span with whitespace
    collapsed (mapping lookup key). Wildcard ``path.*`` is not returned (handled
    elsewhere). Returns ``None`` if not a simple FQ import line.
    """
    li = len(line) - len(line.lstrip())
    p0 = _import_path_start_index(line, li)
    if p0 is None:
        return None
    tail = line[p0:]
    tail = tail.split("\n", 1)[0].rstrip("\r")
    code = _import_tail_before_comments(tail)
    if " as " in code:
        left, _, _ = code.partition(" as ")
    else:
        left = code
    left = _strip_trailing_semicolons(left)
    if not left.strip():
        return None
    i0 = len(left) - len(left.lstrip())
    path_text = left.lstrip()
    path_text = _strip_trailing_semicolons(path_text)
    if not path_text or path_text.endswith(".*"):
        return None
    if not _dotted_import_path(path_text):
        return None
    fqname = "".join(path_text.split())
    i1 = i0 + len(path_text)
    start = p0 + i0
    end = p0 + i1
    return fqname, start, end


def is_mapping_scoped_wildcard_import(line: str, source_pkgs: frozenset[str]) -> bool:
    """
    ``True`` only for ``import <source_package>.*`` where ``source_package`` is a
    CSV ``source_package`` (not arbitrary ``import foo.bar.*``).
    """
    li = len(line) - len(line.lstrip())
    p0 = _import_path_start_index(line, li)
    if p0 is None:
        return False
    tail = line[p0:]
    tail = tail.split("\n", 1)[0].rstrip("\r")
    if " as " in tail:
        return False
    code = _import_tail_before_comments(tail)
    compact = "".join(code.split())
    if not compact.endswith(".*"):
        return False
    prefix = compact[:-2]
    return prefix in source_pkgs


@dataclass
class MigrationStats:
    lines_changed: int = 0
    fq_replaced: int = 0
    wildcard_hits: list[tuple[str, str]] = field(default_factory=list)  # (file://url, reason)
    fq_not_changed: list[tuple[str, str]] = field(default_factory=list)  # (file://url, reason)


def load_mapping_csv(path: Path) -> tuple[dict[str, tuple[str, str, str]], frozenset[str]]:
    """
    Return ``(mappings, source_packages)`` where
    ``mappings[source_fqname] = (status, target_package, declaration)``.
    ``source_fqname`` is ``source_package`` + ``.`` + ``declaration``.
    Duplicate ``source_fqname`` rows are rejected (assert).
    """
    mappings: dict[str, tuple[str, str, str]] = {}
    packages: set[str] = set()
    with path.open(encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            sp = row["source_package"].strip()
            decl = row["declaration"].strip()
            st = row["status"].strip()
            tp = row["target_package"].strip()
            fqname = f"{sp}.{decl}"
            assert fqname not in mappings, f"duplicate source fqname in mapping CSV: {fqname!r}"
            mappings[fqname] = (st, tp, decl)
            packages.add(sp)
    return mappings, frozenset(packages)


def lookup_mapped_import(
    import_path: str,
    mappings: dict[str, tuple[str, str, str]],
) -> tuple[str, str, str] | None:
    """
    If ``import_path`` equals a source fqname key in ``mappings``, return
    ``(declaration, status, target_package)``; else None.
    """
    row = mappings.get(import_path)
    if row is None:
        return None
    st, target_pkg, decl = row
    return (decl, st, target_pkg)


def file_ref(path: Path, lineno: int) -> str:
    return f"file://{path.resolve().as_posix()}:{lineno}"


def process_line(
    line: str,
    lineno: int,
    path: Path,
    mappings: dict[str, tuple[str, str, str]],
    source_pkgs: frozenset[str],
    stats: MigrationStats,
) -> str | None:
    """
    Return replacement line (with newline) if the line should change; ``None`` if unchanged.
    """
    if is_mapping_scoped_wildcard_import(line, source_pkgs):
        stats.wildcard_hits.append(
            (file_ref(path, lineno), "Can't process wildcard import")
        )
        return None

    span = import_path_fqname_and_span(line)
    if span is None:
        return None
    import_path, start, end = span

    hit = lookup_mapped_import(import_path, mappings)
    if hit is None:
        return None

    decl, status, target_pkg = hit
    if status == "mapped":
        new_path = f"{target_pkg}.{decl}"
        new_line = line[:start] + new_path + line[end:]
        if new_line != line:
            stats.fq_replaced += 1
            return new_line
        return None

    if status == "ambiguous":
        stats.fq_not_changed.append(
            (
                file_ref(path, lineno),
                f"Multiple packages provide {decl} on target version",
            )
        )
    else:
        stats.fq_not_changed.append(
            (
                file_ref(path, lineno),
                f"{decl} not available on target version",
            )
        )
    return None


def migrate_project(
    project: Path,
    mapping_csv: Path,
    *,
    write: bool,
) -> MigrationStats:
    mappings, source_pkgs = load_mapping_csv(mapping_csv)

    kt_files = source_paths.collect(project, SOURCE_SET_NAMES)
    stats = MigrationStats()

    for kt in kt_files:
        text = kt.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines(keepends=True)
        out: list[str] = []
        for lineno, line in enumerate(lines, start=1):
            # Kotlin ``import`` is lowercase; skip non-import lines (``import`` + ws + path).
            li = len(line) - len(line.lstrip())
            if _import_path_start_index(line, li) is None:
                out.append(line)
                continue
            new_line = process_line(
                line,
                lineno,
                kt,
                mappings,
                source_pkgs,
                stats,
            )
            if new_line is not None:
                out.append(new_line)
                stats.lines_changed += 1
            else:
                out.append(line)

        if write and "".join(out) != text:
            kt.write_text("".join(out), encoding="utf-8")

    return stats


def report(stats: MigrationStats) -> None:
    print("--- Migration report ---", file=sys.stderr)
    print(f"Lines changed: {stats.lines_changed}", file=sys.stderr)
    print(f"FQ imports rewritten: {stats.fq_replaced}", file=sys.stderr)
    print(f"Wildcard imports (warnings): {len(stats.wildcard_hits)}", file=sys.stderr)
    for url, reason in stats.wildcard_hits:
        print(f"  {url} — {reason}", file=sys.stderr)

    print(
        f"FQ imports not updated (missing/ambiguous): {len(stats.fq_not_changed)}",
        file=sys.stderr,
    )
    for url, reason in stats.fq_not_changed:
        print(f"  {url} — {reason}", file=sys.stderr)

    if not stats.wildcard_hits and not stats.fq_not_changed:
        if stats.lines_changed == 0:
            print("Migration complete (nothing to do).", file=sys.stderr)
        else:
            print("Migration complete.", file=sys.stderr)


def main() -> None:
    ap = argparse.ArgumentParser(
        description=(
            "Migrate platform imports using mapping CSV derived from source/target "
            "compiler versions: looks for mapping-{src}-to-{tgt}.csv under klib/mappings/, "
            "then under klib/ next to this script."
        )
    )
    ap.add_argument(
        "--project",
        type=Path,
        default=MIGRATING_PROJECT,
        help="Kotlin project root (default: config.MIGRATING_PROJECT)",
    )
    ap.add_argument(
        "--source-version",
        metavar="VER",
        default=SOURCE_COMPILER_VERSION,
        help=f"Source Kotlin/Native compilerVersion (default: {SOURCE_COMPILER_VERSION})",
    )
    ap.add_argument(
        "--target-version",
        metavar="VER",
        default=TARGET_COMPILER_VERSION,
        help=f"Target Kotlin/Native compilerVersion (default: {TARGET_COMPILER_VERSION})",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Report only; do not modify .kt files (default is to apply changes).",
    )
    args = ap.parse_args()

    mapping_csv = resolve_mapping_csv(args.source_version, args.target_version)
    if mapping_csv is None:
        klib_dir = Path(__file__).resolve().parent
        name = f"mapping-{args.source_version}-to-{args.target_version}.csv"
        print("error: mapping CSV not found. Tried:", file=sys.stderr)
        print(f"  {klib_dir / 'mappings' / name}", file=sys.stderr)
        print(f"  {klib_dir / name}", file=sys.stderr)
        print(
            "  (run mapping.py to generate under klib/mappings/, or place the file next to migrate.py)",
            file=sys.stderr,
        )
        sys.exit(1)
    if not args.project.is_dir():
        print(f"error: project not a directory: {args.project}", file=sys.stderr)
        sys.exit(1)

    print(f"Using mapping: {mapping_csv.resolve()}", file=sys.stderr)
    if args.dry_run:
        print("Dry run: no files will be modified.", file=sys.stderr)
    stats = migrate_project(args.project, mapping_csv, write=not args.dry_run)
    report(stats)
    if not args.dry_run:
        print(f"wrote changes where applicable under {args.project.resolve()}", file=sys.stderr)


if __name__ == "__main__":
    main()
