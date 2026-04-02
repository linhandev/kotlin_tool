#!/usr/bin/env python3
"""
Parse Kotlin/Native cinterop ``default/manifest`` files.

``includedHeaders`` is a single line of space-separated tokens: mostly paths like
``usr/include/foo.h``, sometimes trailing 64-character snapshot tokens (no ``.``).
Those hashes are not filesystem paths and are ignored for header resolution.
"""
from __future__ import annotations

from pathlib import Path


def _is_header_path(token: str) -> bool:
    t = token.strip()
    return t and not (len(t) == 64 and "." not in t)


def headers(klib_dir: Path) -> list[str]:
    """Load ``default/manifest`` under ``klib_dir`` and return path-like header strings (no hashes)."""
    manifest_path = klib_dir / "default" / "manifest"
    if not manifest_path.is_file():
        return []
    text = manifest_path.read_text(encoding="utf-8", errors="replace")
    raw = ""
    for line_raw in text.splitlines():
        line = line_raw.strip()
        if line.startswith("includedHeaders="):
            raw = line.split("=", 1)[1].strip()
            break
    parts = raw.split() if raw.strip() else []
    return [t for t in parts if _is_header_path(t)]


def header_paths(klib_dir: Path, sysroot: Path) -> list[Path]:
    """Resolve ``headers(klib_dir)`` tokens under ``sysroot``; return paths that exist as files."""
    out: list[Path] = []
    for header in headers(klib_dir):
        p = (sysroot / header).resolve()
        if p.is_file():
            out.append(p)
    return out
