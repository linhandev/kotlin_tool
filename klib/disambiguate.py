#!/usr/bin/env python3
"""
Ambiguous mapping rows: infer defining header from source ``includedHeaders`` + ctags,
then pick the target klib whose manifest lists that path. Skips declarations containing ``.``.
"""
from __future__ import annotations

import json
import manifest
import shutil
import subprocess
import sys
from pathlib import Path

from config import (
    CTAGS_BIN,
    HARDCODED_SOURCE_FQNAME_TO_TARGET_FQNAME,
    SOURCE_KLIBS,
    SOURCE_SYSROOT,
)

# ``frozenset(manifest.headers(kd))`` by resolved target klib directory; stable for a given folder.
_headers_by_target_klib_fdr: dict[Path, frozenset[str]] = {}
# One resolved header path -> all ctags JSON tag dicts for that file only.
_ctags_by_header_path: dict[str, list[dict]] = {}


def by_hard_code(source_package: str, declaration: str) -> str | None:
    """
    If ``(source_package + '.' + declaration).strip()`` is in ``HARDCODED_SOURCE_FQNAME_TO_TARGET_FQNAME``,
    return the target Kotlin **package** (parent of the last segment of the target fqname).
    Otherwise None.
    """
    key = f"{source_package}.{declaration}".strip()
    tgt_fq = HARDCODED_SOURCE_FQNAME_TO_TARGET_FQNAME.get(key)
    if tgt_fq is None:
        return None
    return tgt_fq.rsplit(".", 1)[0]


def _tags_for_header_file(header_path: Path) -> list[dict]:
    """Return ctags JSON tags for a single header, with cache."""
    key = str(header_path.resolve())
    if key in _ctags_by_header_path:
        return _ctags_by_header_path[key]
    cmd = [CTAGS_BIN, "--output-format=json", "-o", "-", key]
    tags: list[dict] = []
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError as e:
        print(f"warning: ctags could not run ({e})", file=sys.stderr)
        proc = None
    if proc is None or proc.returncode != 0:
        if proc and (proc.stderr or "").strip():
            print(
                f"warning: ctags exit {proc.returncode}: {proc.stderr.strip()}",
                file=sys.stderr,
            )
        _ctags_by_header_path[key] = []
        return []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("_type") == "tag":
            tags.append(obj)
    _ctags_by_header_path[key] = tags
    return tags


def gles3(
    source_package: str,
    target_pkg_to_klib: dict[str, Path],
) -> str | None:
    """
    If ``source_package`` starts with ``platform.gles3`` (case-sensitive) and that exact
    package name is among the target candidates, return it so the row maps 1:1 by name.
    Otherwise return None (caller keeps ``ambiguous`` or tries other resolvers).
    """
    if not source_package.startswith("platform.gles3"):
        return None
    if source_package in target_pkg_to_klib:
        return source_package
    return None


def by_header(
    source_klib_fdr: str,
    declaration: str,
    target_pkg_to_klib: dict[str, Path],
) -> str | None:
    """Return the Kotlin **package** name if exactly one target matches; else None."""
    if (
        not declaration
        or "." in declaration
        or not shutil.which(CTAGS_BIN)
        or SOURCE_SYSROOT is None
        or not SOURCE_SYSROOT.is_dir()
    ):
        return None

    sysroot = SOURCE_SYSROOT
    paths = manifest.header_paths(
        (SOURCE_KLIBS / source_klib_fdr).resolve(), sysroot
    )
    if not paths:
        return None

    root = sysroot.resolve()
    defining: set[str] = set()
    for hp in paths:
        for tag in _tags_for_header_file(hp):
            if tag.get("name") != declaration:
                continue
            path_str = tag.get("path")
            if not path_str:
                continue
            try:
                rel = Path(path_str).resolve().relative_to(root)
            except ValueError:
                continue
            defining.add(rel.as_posix())
    if len(defining) != 1:
        return None
    (header,) = tuple(defining)

    matching: list[str] = []
    for pkg, kd in sorted(target_pkg_to_klib.items(), key=lambda x: (x[0], str(x[1]))):
        cached = _headers_by_target_klib_fdr.get(kd)
        if cached is None:
            cached = frozenset(manifest.headers(kd))
            _headers_by_target_klib_fdr[kd] = cached
        if header in cached:
            matching.append(pkg)

    if len(matching) != 1:
        return None
    return matching[0]

