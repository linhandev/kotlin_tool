"""
Collect ``.kt`` paths under ``root`` that include ``/<sourceSet>/`` in the normalized path.

Git work trees: uses ``git ls-files`` (ignore-aware). Otherwise ``rglob("*.kt")``.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterable


def collect(
    root: Path | str,
    source_set_names: Iterable[str],
) -> list[Path]:
    """
    Sorted unique ``.kt`` files under ``root`` whose path (relative to ``root`` when
    possible) contains ``/<name>/`` for some ``name`` in ``source_set_names``.
    Uses Git listing when ``root`` is in a work tree; else scans all ``.kt`` files.
    """
    root_p = Path(root)
    if not root_p.is_dir():
        raise NotADirectoryError(f"not a directory: {root_p}")

    names = frozenset(n.strip() for n in source_set_names if n and n.strip())
    if not names:
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
        if not any(f"/{n}/" in norm_path(p) for n in names):
            continue
        rp = p.resolve()
        if rp in seen:
            continue
        seen.add(rp)
        result.append(p)

    return sorted(result, key=norm_path)
