#!/usr/bin/env python3
"""
Scan a klib folder (or platform root) with ``klib dump-metadata-signatures`` and print
declaration counts. Set ``KLIB_FOLDER_TO_SCAN`` below (default: ``SOURCE_KLIBS`` from ``config``).

    python scan.py
"""
from __future__ import annotations

import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from tqdm import tqdm

from config import KLIB, SOURCE_COMPILER_VERSION, SOURCE_KLIBS
from declarations import parse_dump_metadata_line

KLIB_FOLDER_TO_SCAN = SOURCE_KLIBS


def scan_platform(klib_bin: Path, folder: Path) -> tuple[int, int, int]:
    """
    Returns ``(unique (package, declaration) pairs, duplicate lines within dumps,
    declaration strings appearing in more than one package)``.
    If ``folder`` is a platform root (children are klib artifacts with ``default/``),
    runs one dump per child; otherwise one dump on ``folder``.
    """
    if not folder.is_dir():
        return (0, 0, 0)
    if (folder / "default").is_dir():
        targets = [folder]
    else:
        children = sorted(p for p in folder.iterdir() if p.is_dir())
        if children and all((c / "default").is_dir() for c in children):
            targets = children
        else:
            targets = [folder]

    global_seen: set[tuple[str, str]] = set()
    duplicate_lines = 0
    for kd in tqdm(
        targets,
        desc="klib dump",
        unit="klib",
        file=sys.stderr,
    ):
        lines = subprocess.check_output(
            [str(klib_bin), "dump-metadata-signatures", str(kd)],
            text=True,
        ).splitlines()
        local_seen: set[tuple[str, str]] = set()
        for line in lines:
            pair = parse_dump_metadata_line(line)
            if pair is None:
                continue
            if pair in local_seen:
                duplicate_lines += 1
            else:
                local_seen.add(pair)
            global_seen.add(pair)

    by_decl: dict[str, set[str]] = defaultdict(set)
    for pkg, decl in global_seen:
        by_decl[decl].add(pkg)
    multi_pkg = sum(1 for pkgs in by_decl.values() if len(pkgs) > 1)
    return (len(global_seen), duplicate_lines, multi_pkg)


def main() -> None:
    if not KLIB.is_file():
        print(f"error: klib binary not found: {KLIB}", file=sys.stderr)
        sys.exit(1)
    if not KLIB_FOLDER_TO_SCAN.is_dir():
        print(f"error: not a directory: {KLIB_FOLDER_TO_SCAN}", file=sys.stderr)
        sys.exit(1)

    n, dup, multi = scan_platform(KLIB, KLIB_FOLDER_TO_SCAN)
    print(f"SOURCE_COMPILER_VERSION={SOURCE_COMPILER_VERSION}")
    print(f"KLIB={KLIB}")
    print(f"KLIB_FOLDER_TO_SCAN={KLIB_FOLDER_TO_SCAN}")
    print(f"unique_declaration_pairs={n}")
    print(f"duplicate_lines_in_dump={dup}")
    print(f"declarations_in_multiple_packages={multi}")


if __name__ == "__main__":
    main()
