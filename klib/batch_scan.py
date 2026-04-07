#!/usr/bin/env python3
"""
Batch OH import migration **dry-run scan** across Git checkouts under a CI mirror root.

For each immediate child directory that is a Git work tree (under ``--ci-root``):

1. ``git fetch --all --prune``.
2. ``git reset --hard HEAD`` then ``git clean -fdx`` (tree matches HEAD; no untracked/ignored cruft).
3. For each branch on ``origin`` (except ``origin/HEAD``): ``checkout -f -B``, ``reset --hard``
   to ``origin/<branch>``, then ``git clean -fdx`` again so the tree matches that remote tip.
4. Run ``migrate.py --dry-run --all-kt`` and save combined stdout/stderr per branch.

Restores the original branch (or detached SHA) after each repository.

**Destructive:** local branches and working trees are rewritten to match ``origin``; untracked
and ignored files are removed.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import subprocess
import sys
from pathlib import Path
from subprocess import CompletedProcess

try:
    from tqdm import tqdm
except ImportError:  # pragma: no cover
    tqdm = None  # type: ignore[misc, assignment]

DEFAULT_CI_ROOT = Path("/Users/ohoskt/git/ci")
SOURCE_COMPILER_VERSION = "2.0.21-KBA-014"
TARGET_COMPILER_VERSION = "2.2.21-EZ.0.2.0-05"
REMOTE = "origin"

MIGRATE_NOTHING_TO_DO = "Migration complete (nothing to do)."

_PREFIX_LINES_CHANGED = "Lines changed:"
_PREFIX_WILDCARD = "Wildcard imports (warnings):"
_PREFIX_FQ_MISS = "FQ imports not updated (missing/ambiguous):"

_SAFE_FILENAME_CHARS = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._+@-"
)


def _klib_dir() -> Path:
    return Path(__file__).resolve().parent


def _run_git(
    repo: Path,
    *args: str,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        capture_output=True,
        text=True,
        errors="replace",
    )


def _is_git_worktree(path: Path) -> bool:
    git = path / ".git"
    return git.is_dir() or git.is_file()


def _discover_projects(ci_root: Path) -> list[Path]:
    if not ci_root.is_dir():
        raise NotADirectoryError(f"CI root is not a directory: {ci_root}")
    out: list[Path] = []
    for child in sorted(ci_root.iterdir(), key=lambda p: p.name.lower()):
        if not child.is_dir():
            continue
        if child.name.startswith("."):
            continue
        if _is_git_worktree(child):
            out.append(child)
    return out


def _remote_branches(repo: Path, remote: str) -> list[str]:
    p = _run_git(repo, "branch", "-r", check=False)
    if p.returncode != 0:
        return []
    prefix = f"{remote}/"
    seen: set[str] = set()
    for line in p.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith(f"{remote}/HEAD"):
            continue
        if line.startswith(prefix):
            seen.add(line[len(prefix) :])
    return sorted(seen)


def _safe_branch_filename(branch: str) -> str:
    s = branch.replace("/", "__")
    s = "".join(c if c in _SAFE_FILENAME_CHARS else "_" for c in s)
    return s or "branch"


def _unsigned_int_after_prefix(stripped_line: str, prefix: str) -> int | None:
    if not stripped_line.startswith(prefix):
        return None
    tail = stripped_line[len(prefix) :].strip()
    return int(tail) if tail.isdigit() else None


def _read_head_state(repo: Path) -> tuple[str, str]:
    """Return (abbrev_ref, full_sha). abbrev_ref is ``HEAD`` when detached."""
    ar = _run_git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    sha = _run_git(repo, "rev-parse", "HEAD").stdout.strip()
    return ar, sha


def _restore_head(repo: Path, abbrev_ref: str, sha: str) -> None:
    if abbrev_ref != "HEAD":
        _run_git(repo, "checkout", "-f", abbrev_ref, check=False)
    else:
        _run_git(repo, "checkout", "-f", sha, check=False)


def _reset_hard_and_clean(repo: Path) -> CompletedProcess[str]:
    """``git reset --hard HEAD`` then ``git clean -fdx``."""
    r = _run_git(repo, "reset", "--hard", "HEAD", check=False)
    if r.returncode != 0:
        return r
    return _run_git(repo, "clean", "-fdx", check=False)


def _migration_report_hints(log_text: str) -> str:
    """Short hint from migrate stderr (counts / completion line) for summary reasons."""
    hints: list[str] = []
    lines_changed = 0
    wildcard_n = 0
    fq_n = 0
    for raw in log_text.splitlines():
        line = raw.strip()
        v = _unsigned_int_after_prefix(line, _PREFIX_LINES_CHANGED)
        if v is not None:
            lines_changed = v
            continue
        v = _unsigned_int_after_prefix(line, _PREFIX_WILDCARD)
        if v is not None:
            wildcard_n = v
            continue
        v = _unsigned_int_after_prefix(line, _PREFIX_FQ_MISS)
        if v is not None:
            fq_n = v
            continue
    if lines_changed > 0:
        hints.append(f"lines_changed={lines_changed}")
    if wildcard_n > 0:
        hints.append(f"wildcard_warnings={wildcard_n}")
    if fq_n > 0:
        hints.append(f"fq_not_updated={fq_n}")
    if "Migration complete." in log_text and "nothing to do" not in log_text:
        if not hints:
            hints.append("migration_complete_with_edits")
    return "; ".join(hints)


def _row_needs_action(row: dict[str, str], report_dir: Path) -> tuple[bool, str]:
    """
    ``False`` only when sync + migrate succeeded and the log contains
    ``Migration complete (nothing to do).`` (see :func:`migrate.report`).
    """
    note = (row.get("note") or "").strip()
    branch = (row.get("branch") or "").strip()
    sync_ok = row.get("sync_ok") == "1"
    migrate_exit = (row.get("migrate_exit") or "").strip()
    log_rel = (row.get("log") or "").strip()

    if not branch:
        return True, note or "project_level"
    if not sync_ok:
        return True, note or "git_sync_failed"
    if migrate_exit != "0":
        return True, note or f"migrate_exit_{migrate_exit or 'missing'}"

    log_path = report_dir / log_rel
    try:
        text = log_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return True, f"log_read_error:{exc}"

    if MIGRATE_NOTHING_TO_DO in text:
        return False, ""
    hints = _migration_report_hints(text)
    return True, hints or "not_nothing_to_do"


def _write_action_summary(rows: list[dict[str, str]], report_dir: Path) -> tuple[Path, int]:
    action_rows: list[tuple[str, str, str]] = []
    for row in rows:
        need, reason = _row_needs_action(row, report_dir)
        if need:
            action_rows.append((row.get("project", ""), row.get("branch", ""), reason))

    tsv_path = report_dir / "action-required.tsv"
    txt_path = report_dir / "action-required.txt"
    with tsv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["project", "branch", "reason"])
        for proj, br, reason in action_rows:
            w.writerow([proj, br, reason])

    lines = [
        "# Branches and projects that are not clean (migrate did not print "
        f'"{MIGRATE_NOTHING_TO_DO}") or tooling failed.',
        f"# Total: {len(action_rows)}",
        "",
    ]
    for proj, br, reason in action_rows:
        b = br or "(project)"
        lines.append(f"{proj}\t{b}\t{reason}")
    txt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return tsv_path, len(action_rows)


def _sync_branch_to_remote(repo: Path, remote: str, branch: str) -> CompletedProcess[str]:
    ref = f"{remote}/{branch}"
    p1 = _run_git(repo, "checkout", "-f", "-B", branch, ref, check=False)
    if p1.returncode != 0:
        return p1
    p2 = _run_git(repo, "reset", "--hard", ref, check=False)
    if p2.returncode != 0:
        return p2
    return _run_git(repo, "clean", "-fdx", check=False)


def main() -> None:
    klib = _klib_dir()
    migrate_py = klib / "migrate.py"

    ap = argparse.ArgumentParser(
        description=(
            "Sync each repo to origin (fetch, reset, clean), dry-run migrate every branch "
            "with --all-kt; write reports under ./ci-migrate-scan-reports/<timestamp>/."
        )
    )
    ap.add_argument(
        "--ci-root",
        type=Path,
        default=DEFAULT_CI_ROOT,
        help=f"Parent of one Git checkout per child directory (default: {DEFAULT_CI_ROOT})",
    )
    args = ap.parse_args()

    if not migrate_py.is_file():
        print(f"error: migrate.py not found next to this script: {migrate_py}", file=sys.stderr)
        sys.exit(2)

    ts = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    report_dir = (Path.cwd() / "ci-migrate-scan-reports" / ts).resolve()
    report_dir.mkdir(parents=True, exist_ok=True)

    projects = _discover_projects(args.ci_root.resolve())
    index_path = report_dir / "index.tsv"
    rows: list[dict[str, str]] = []

    progress = None
    if tqdm is not None:
        progress = tqdm(
            total=len(projects),
            desc="Projects",
            unit="repo",
            file=sys.stderr,
            dynamic_ncols=True,
        )
    else:
        print(
            "warning: tqdm not installed; pip install -r klib/requirements.txt for a progress bar",
            file=sys.stderr,
        )

    for proj in projects:
        try:
            abbrev0, sha0 = _read_head_state(proj)
            if progress is not None:
                progress.set_postfix(project=proj.name, branch="…", refresh=False)

            fp = _run_git(proj, "fetch", "--all", "--prune", check=False)
            if fp.returncode != 0:
                rows.append(
                    {
                        "project": proj.name,
                        "branch": "",
                        "sync_ok": "0",
                        "migrate_exit": "",
                        "log": "",
                        "note": f"fetch_failed: {fp.stderr.strip() or fp.stdout.strip()}",
                    }
                )
                print(f"[{proj.name}] fetch failed ({fp.returncode})", file=sys.stderr)
                _restore_head(proj, abbrev0, sha0)
                continue

            pr = _reset_hard_and_clean(proj)
            if pr.returncode != 0:
                detail = (pr.stderr or pr.stdout or "").strip()
                rows.append(
                    {
                        "project": proj.name,
                        "branch": "",
                        "sync_ok": "0",
                        "migrate_exit": "",
                        "log": "",
                        "note": f"reset_clean_failed: {detail}",
                    }
                )
                print(f"[{proj.name}] reset/clean failed ({pr.returncode})", file=sys.stderr)
                _restore_head(proj, abbrev0, sha0)
                continue

            branches = _remote_branches(proj, REMOTE)
            if not branches:
                rows.append(
                    {
                        "project": proj.name,
                        "branch": "",
                        "sync_ok": "",
                        "migrate_exit": "",
                        "log": "",
                        "note": "no_remote_branches",
                    }
                )
                print(f"[{proj.name}] no remote branches on {REMOTE}", file=sys.stderr)
                _restore_head(proj, abbrev0, sha0)
                continue

            proj_log_dir = report_dir / _safe_branch_filename(proj.name)
            proj_log_dir.mkdir(parents=True, exist_ok=True)

            for branch in branches:
                if progress is not None:
                    progress.set_postfix(project=proj.name, branch=branch, refresh=True)
                sp = _sync_branch_to_remote(proj, REMOTE, branch)
                sync_ok = sp.returncode == 0
                note = ""
                if not sync_ok:
                    note = f"sync_failed: {(sp.stderr or sp.stdout or '').strip()}"

                log_path = proj_log_dir / f"{_safe_branch_filename(branch)}.log"
                migrate_exit = ""
                if sync_ok:
                    cmd = [
                        sys.executable,
                        str(migrate_py),
                        "--project",
                        str(proj),
                        "--source-version",
                        SOURCE_COMPILER_VERSION,
                        "--target-version",
                        TARGET_COMPILER_VERSION,
                        "--dry-run",
                        "--all-kt",
                    ]
                    mp = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        errors="replace",
                    )
                    migrate_exit = str(mp.returncode)
                    parts: list[str] = []
                    if mp.stdout:
                        parts.append(mp.stdout)
                    if mp.stderr:
                        parts.append(mp.stderr)
                    log_path.write_text("\n".join(parts), encoding="utf-8")
                    if mp.returncode != 0:
                        note = "migrate_nonzero_exit"
                else:
                    log_path.write_text(note + "\n", encoding="utf-8")

                rows.append(
                    {
                        "project": proj.name,
                        "branch": branch,
                        "sync_ok": "1" if sync_ok else "0",
                        "migrate_exit": migrate_exit,
                        "log": str(log_path.relative_to(report_dir)),
                        "note": note,
                    }
                )

            _restore_head(proj, abbrev0, sha0)
        finally:
            if progress is not None:
                progress.update(1)

    if progress is not None:
        progress.close()

    fieldnames = ["project", "branch", "sync_ok", "migrate_exit", "log", "note"]
    with index_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})

    summary_tsv, action_count = _write_action_summary(rows, report_dir)

    print(f"Wrote {index_path}", file=sys.stderr)
    print(f"Wrote {summary_tsv} ({action_count} row(s) need action)", file=sys.stderr)
    print(f"Reports under {report_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
