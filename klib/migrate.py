#!/usr/bin/env python3
"""
Migrate Kotlin ``import`` lines from source-version platform FQ names to target-version
FQ names using a mapping CSV (see ``mapping.py``). Only OH source-set ``.kt`` files
(``collect()`` + ``config``, or all ``.kt`` files with ``--all-kt``).

**Import parsing scope (intentionally minimal)**

This tool is meant to be driven by an LLM or human on normal code; **exotic** syntax
is out of scope here.

- **Handled:** one line per ``import``; path is the substring after ``import`` (plus
  space/tab) **up to the first** of ``//``, ``/*``, or `` as `` (whichever is
  earliest); trailing ``;`` on the path side is stripped; internal whitespace in
  that region is collapsed for the mapping lookup key; replacement uses the
  non-whitespace span in the source line.
- **Skipped / not handled:** import paths containing **backticks** (skipped so we
  do not corrupt names); comments inside the path that confuse the cut points;
  multiline imports; BOM; non-space/tab after ``import`` — use an editor or
  **LLM** to normalize those lines before/after migration.
"""
from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from config import (
    MIGRATING_PROJECT,
    SOURCE_SET_NAMES,
    TARGET_COMPILER_VERSION,
)


def collect(
    root: Path | str,
    source_set_names: Iterable[str],
    *,
    filter_source_sets: bool = True,
) -> list[Path]:
    """
    Sorted unique ``.kt`` files under ``root``.

    When ``filter_source_sets`` is True (default), only paths that contain
    ``/<name>/`` for some non-empty ``name`` in ``source_set_names`` are kept; if
    that set is empty after stripping, returns no files.

    When ``filter_source_sets`` is False, every ``.kt`` file under ``root`` (Git-
    listed or rglob) is included; ``source_set_names`` is ignored for filtering.

    Git work trees: uses ``git ls-files`` (ignore-aware). Otherwise ``rglob("*.kt")``.
    """
    root_p = Path(root)
    if not root_p.is_dir():
        raise NotADirectoryError(f"not a directory: {root_p}")

    names = frozenset(n.strip() for n in source_set_names if n and n.strip())
    if filter_source_sets and not names:
        return []

    def norm_path(path: Path) -> str:
        try:
            rel = path.resolve().relative_to(root_p.resolve())
        except ValueError:
            rel = path.resolve()
        return rel.as_posix()

    def inside_git_work_tree() -> bool:
        r = subprocess.run(
            ["git", "-C", str(root_p), "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            check=False,
        )
        return r.returncode == 0 and r.stdout.strip() == "true"

    def git_ls_files() -> list[Path]:
        proc = subprocess.run(
            ["git", "-C", str(root_p), "ls-files", "-z", "-c", "-o", "--exclude-standard"],
            capture_output=True,
            check=True,
        )
        if not proc.stdout:
            return []
        out: list[Path] = []
        for rel in proc.stdout.split(b"\0"):
            if rel:
                out.append(root_p / rel.decode("utf-8", errors="surrogateescape"))
        return out

    if inside_git_work_tree():
        candidates = git_ls_files()
    else:
        candidates = [p for p in root_p.rglob("*.kt") if p.is_file()]

    seen: set[Path] = set()
    result: list[Path] = []
    for p in candidates:
        if not p.is_file() or p.suffix != ".kt":
            continue
        if filter_source_sets and not any(f"/{n}/" in norm_path(p) for n in names):
            continue
        rp = p.resolve()
        if rp in seen:
            continue
        seen.add(rp)
        result.append(p)

    return sorted(result, key=norm_path)


def _simple_tail(declaration: str) -> str:
    """Tail key aligned with :func:`mapping.simple_tail` (``::`` only; dotted paths stay whole)."""
    if "::" in declaration:
        return declaration.split("::")[-1]
    return declaration


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

def _strip_trailing_semicolons(s: str) -> str:
    s = s.rstrip()
    while s.endswith(";"):
        s = s[:-1].rstrip()
    return s


def _import_path_region(tail: str) -> str:
    """Substring after ``import`` + whitespace, up to the first ``//``, ``/*``, or `` as ``."""
    cut = len(tail)
    for marker in ("//", "/*", " as "):
        if marker in tail:
            cut = min(cut, tail.index(marker))
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
    Return ``(fqname, start, end)`` for the **basic** path slice (see module docstring).
    **Wildcard** ``.*`` paths return ``None`` (handled elsewhere). Empty path
    returns ``None``.
    """
    li = len(line) - len(line.lstrip())
    p0 = _import_path_start_index(line, li)
    if p0 is None:
        return None
    tail = line[p0:]
    tail = tail.split("\n", 1)[0].rstrip("\r")
    region = _import_path_region(tail)
    region = _strip_trailing_semicolons(region)
    if not region.strip():
        return None
    i0 = len(region) - len(region.lstrip())
    i1 = len(region.rstrip())
    slice_text = region[i0:i1]
    if "`" in slice_text:
        return None
    fqname = "".join(slice_text.split())
    if not fqname or fqname.endswith(".*"):
        return None
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
    region = _import_path_region(tail)
    region = _strip_trailing_semicolons(region)
    compact = "".join(region.split())
    if not compact.endswith(".*"):
        return False
    prefix = compact[:-2]
    return prefix in source_pkgs


@dataclass
class MigrationStats:
    lines_changed: int = 0
    fq_replaced: int = 0
    typealias_lines_added: int = 0
    changed_line_refs: list[str] = field(default_factory=list)  # file://path:line per changed line
    wildcard_hits: list[tuple[str, str]] = field(default_factory=list)  # (file://url, reason)
    fq_not_changed: list[tuple[str, str]] = field(default_factory=list)  # (file://url, reason)


def load_mapping_csv(path: Path) -> tuple[dict[str, tuple[str, str, str, str]], frozenset[str]]:
    """
    Return ``(mappings, source_packages)`` where
    ``mappings[source_fqname] = (status, target_package, source_declaration, target_declaration)``.
    ``target_declaration`` is empty when the import path is ``target_package`` + ``.`` + ``declaration``;
    when set (nested ``::`` name on target), the import line uses a backtick-quoted nested name
    after ``target_package.`` and a ``typealias`` is inserted after the last import.
    ``source_fqname`` is ``source_package`` + ``.`` + ``declaration``.
    Duplicate ``source_fqname`` rows are rejected (assert).
    """
    mappings: dict[str, tuple[str, str, str, str]] = {}
    packages: set[str] = set()
    with path.open(encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            sp = row["source_package"].strip()
            decl = row["declaration"].strip()
            st = row["status"].strip()
            tp = row["target_package"].strip()
            td = (row.get("target_declaration") or "").strip()
            fqname = f"{sp}.{decl}"
            assert fqname not in mappings, f"duplicate source fqname in mapping CSV: {fqname!r}"
            mappings[fqname] = (st, tp, decl, td)
            packages.add(sp)
    return mappings, frozenset(packages)


def lookup_mapped_import(
    import_path: str,
    mappings: dict[str, tuple[str, str, str, str]],
) -> tuple[str, str, str, str] | None:
    """
    If ``import_path`` equals a source fqname key in ``mappings``, return
    ``(declaration, status, target_package, target_declaration)``; else None.
    """
    row = mappings.get(import_path)
    if row is None:
        return None
    st, target_pkg, decl, tgt_decl = row
    return (decl, st, target_pkg, tgt_decl)


def file_ref(path: Path, lineno: int) -> str:
    return f"file://{path.resolve().as_posix()}:{lineno}"


def process_line(
    line: str,
    lineno: int,
    path: Path,
    mappings: dict[str, tuple[str, str, str, str]],
    source_pkgs: frozenset[str],
    stats: MigrationStats,
    typealias_keys: set[tuple[str, str]] | None = None,
) -> str | None:
    """
    Return replacement line (with newline) if the line should change; ``None`` if unchanged.
    When ``typealias_keys`` is set and the row uses ``target_declaration``, records
    ``(simple_tail(source declaration), target_declaration)`` for insertion after the last import.
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

    decl, status, target_pkg, target_decl = hit
    if status == "mapped":
        if target_decl:
            new_path = f"{target_pkg}.`{target_decl}`"
        else:
            new_path = f"{target_pkg}.{decl}"
        new_line = line[:start] + new_path + line[end:]
        if new_line != line:
            if target_decl and typealias_keys is not None:
                typealias_keys.add((_simple_tail(decl), target_decl))
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


def _last_import_line_index(lines: list[str]) -> int | None:
    """Index of the last line that starts an ``import`` statement, or ``None``."""
    last: int | None = None
    for i, line in enumerate(lines):
        li = len(line) - len(line.lstrip())
        if _import_path_start_index(line, li) is not None:
            last = i
    return last


def _typealias_lines(keys: set[tuple[str, str]]) -> list[str]:
    """Sorted ``typealias`` lines for stable output."""
    out: list[str] = []
    for alias, rhs in sorted(keys, key=lambda t: (t[0], t[1])):
        out.append(f"typealias {alias} = `{rhs}`\n")
    return out


def migrate_project(
    project: Path,
    mapping_csv: Path,
    *,
    write: bool,
    filter_source_sets: bool = True,
) -> MigrationStats:
    mappings, source_pkgs = load_mapping_csv(mapping_csv)

    kt_files = collect(
        project, SOURCE_SET_NAMES, filter_source_sets=filter_source_sets
    )
    stats = MigrationStats()
    # Same ``(alias, rhs)`` must not be emitted in multiple ``package`` compilation units; skip
    # duplicates after the first file (same pattern as duplicate imports across demo samples).
    typealias_seen_project: set[tuple[str, str]] = set()

    for kt in kt_files:
        text = kt.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines(keepends=True)
        out: list[str] = []
        typealias_keys: set[tuple[str, str]] = set()
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
                typealias_keys=typealias_keys,
            )
            if new_line is not None:
                out.append(new_line)
                stats.lines_changed += 1
                stats.changed_line_refs.append(file_ref(kt, lineno))
            else:
                out.append(line)

        if typealias_keys:
            to_add = typealias_keys - typealias_seen_project
            typealias_seen_project |= typealias_keys
            if to_add:
                alias_lines = _typealias_lines(to_add)
                li = _last_import_line_index(out)
                if li is not None:
                    out = out[: li + 1] + alias_lines + out[li + 1 :]
                    stats.typealias_lines_added += len(alias_lines)
                    stats.lines_changed += len(alias_lines)
                    for j in range(len(alias_lines)):
                        stats.changed_line_refs.append(file_ref(kt, li + 2 + j))

        if write and "".join(out) != text:
            kt.write_text("".join(out), encoding="utf-8")

    return stats


def report(stats: MigrationStats) -> None:
    print("--- Migration report ---", file=sys.stderr)
    print(f"Lines changed: {stats.lines_changed}", file=sys.stderr)
    for ref in stats.changed_line_refs:
        print(f"  {ref}", file=sys.stderr)
    print(f"FQ imports rewritten: {stats.fq_replaced}", file=sys.stderr)
    print(f"Typealias lines added: {stats.typealias_lines_added}", file=sys.stderr)
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
        default="2.0.21-KBA-014",
        help=(
            "Source Kotlin/Native compilerVersion (default: 2.0.21-KBA-014, KBA-014)"
        ),
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
    ap.add_argument(
        "--all-kt",
        action="store_true",
        help=(
            "Do not restrict to OH source-set directories (config.SOURCE_SET_NAMES); "
            "consider every .kt file under --project."
        ),
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
    stats = migrate_project(
        args.project,
        mapping_csv,
        write=not args.dry_run,
        filter_source_sets=not args.all_kt,
    )
    report(stats)
    if not args.dry_run:
        print(f"wrote changes where applicable under {args.project.resolve()}", file=sys.stderr)


if __name__ == "__main__":
    main()
