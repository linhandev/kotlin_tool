#!/usr/bin/env python3
"""
Parse ``klib dump-metadata-signatures`` lines into ``(package, declaration)`` pairs.
Skips synthetic ``.<get-…>``, ``.<set-…>``, ``.<init>`` paths.

Walks all klibs under ``KLIB_DIR`` and writes ``declarations.csv``: each declaration
path, how many Kotlin packages define it, and those packages separated by ``|``.

Depends on ``tqdm`` for parallel scans with a progress bar (``pip install -r klib/requirements.txt``).
"""
from __future__ import annotations

import csv
import os
import subprocess
import sys
from collections import defaultdict
from functools import partial
from pathlib import Path

from tqdm.contrib.concurrent import thread_map

from config import KLIB as KLIB_BIN
from config import TARGET_KLIBS as KLIB_DIR


def parse_dump_metadata_line(line: str) -> tuple[str, str] | None:
    """
    Parse one line from ``klib dump-metadata-signatures`` output, or return ``None``
    if skipped (header, noise, or synthetic accessor/initializer path).
    """
    line = line.strip()
    if not line or line.startswith("klib ") or "/" not in line or "|" not in line:
        return None
    pkg, rest = line.split("/", 1)
    declaration = rest.split("|", 1)[0].strip()
    if not declaration:
        return None
    if ".<get-" in declaration or ".<set-" in declaration or ".<init>" in declaration:
        return None
    return (pkg, declaration)


def collect_from_klib(klib_bin: Path, klib_dir: Path) -> list[tuple[str, str]]:
    """Run ``dump-metadata-signatures`` on one klib dir; return sorted ``(package, declaration)`` pairs."""
    lines = subprocess.check_output(
        [str(klib_bin), "dump-metadata-signatures", str(klib_dir)],
        text=True,
    ).splitlines()
    out: set[tuple[str, str]] = set()
    for line in lines:
        pair = parse_dump_metadata_line(line)
        if pair is not None:
            out.add(pair)
    return sorted(out)


def collect_from_klibs(
    klib_bin: Path,
    klib_root: Path,
    *,
    progress_desc: str = "klib dump",
) -> list[tuple[str, str, str]]:
    """
    Scan every immediate child klib under ``klib_root`` (one ``dump-metadata-signatures`` each).

    Returns sorted flat rows ``(klib_folder_name, package, declaration)`` — one entry per
    klib that contributes that pair (e.g. klib dir ``org.jetbrains…platform.uv``).
    """
    if not klib_root.is_dir():
        raise NotADirectoryError(f"not a directory: {klib_root}")
    klib_dirs = sorted(p for p in klib_root.iterdir() if p.is_dir())
    if not klib_dirs:
        return []

    n = len(klib_dirs)
    # at least 4, at most 2x cpu cores, but never more than number of klibs
    max_workers = min(n, max(4, (os.cpu_count() or 1) * 2))
    worker = partial(collect_from_klib, klib_bin)
    results = thread_map(
        worker,
        klib_dirs,
        max_workers=max_workers,
        desc=progress_desc,
        unit="klib",
        disable=False,
    )
    rows: list[tuple[str, str, str]] = []
    for kd, pairs in zip(klib_dirs, results):
        klib_dir_name = kd.name
        for pkg, decl in pairs:
            rows.append((klib_dir_name, pkg, decl))
    rows.sort()
    return rows


def main() -> None:
    if not KLIB_DIR.is_dir():
        print(f"error: not a directory: {KLIB_DIR}", file=sys.stderr)
        sys.exit(1)
    klib_dirs = sorted(p for p in KLIB_DIR.iterdir() if p.is_dir())
    records = collect_from_klibs(KLIB_BIN, KLIB_DIR)
    declaration_packages: dict[str, set[str]] = defaultdict(set)
    for _klib, pkg, declaration in records:
        declaration_packages[declaration].add(pkg)

    multi = sum(1 for pkgs in declaration_packages.values() if len(pkgs) > 1)
    out_path = Path("declarations.csv")
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["declaration", "package_count", "packages"])
        for declaration in sorted(declaration_packages.keys()):
            pkgs = sorted(declaration_packages[declaration])
            w.writerow([declaration, len(pkgs), "|".join(pkgs)])

    print(
        f"wrote {out_path.resolve()}  klib_dirs={len(klib_dirs)} "
        f"unique_declarations={len(declaration_packages)} "
        f"declarations_in_more_than_one_package={multi}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
