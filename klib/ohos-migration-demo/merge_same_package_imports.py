#!/usr/bin/env python3
"""Merge same-package Kotlin imports to star imports in this demo only (./src/**/*.kt).

  import platform.ohos.napi_env
  import platform.ohos.napi_value
  ->  import platform.ohos.*

Run: ./merge_same_package_imports.py  (no args; skips lines with `as`)
"""

import sys
from pathlib import Path


def _parse_import(line: str):
    """Return (indent, pkg, is_star, simple_name_or_none, alias) or None."""
    raw = line.rstrip("\n\r")
    stripped = raw.lstrip(" \t")
    if not stripped.startswith("import"):
        return None
    # import keyword + whitespace + rest
    i = len("import")
    if i >= len(stripped) or stripped[i] not in " \t":
        return None
    rest = stripped[i:].lstrip(" \t")
    rest = rest.split("//", 1)[0].strip()
    if not rest:
        return None
    alias = None
    if " as " in rest:
        target, alias_rest = rest.split(" as ", 1)
        target = target.strip()
        alias = alias_rest.strip().split(None, 1)[0] if alias_rest.strip() else None
    else:
        target = rest
    segs = target.split(".")
    if len(segs) < 2:
        return None
    indent = raw[: len(raw) - len(stripped)]
    if segs[-1] == "*":
        pkg = ".".join(segs[:-1])
        return (indent, pkg, True, None, alias) if pkg else None
    pkg = ".".join(segs[:-1])
    return (indent, pkg, False, segs[-1], alias) if pkg else None


def transform_source(text: str):
    lines = text.splitlines()
    nl = "\r\n" if "\r\n" in text else "\n"
    parsed = []
    for i, line in enumerate(lines):
        p = _parse_import(line)
        if p:
            parsed.append((i, p))
    if not parsed:
        return text, False

    by_pkg = {}
    for i, (indent, pkg, is_star, simple, alias) in parsed:
        by_pkg.setdefault(pkg, []).append((i, indent, None if is_star else simple, alias))

    remove = set()
    replace = {}

    for pkg, entries in by_pkg.items():
        has_alias = any(e[3] for e in entries)
        stars = [e for e in entries if e[2] is None]
        singles = [e for e in entries if e[2] is not None]

        if stars:
            ind = stars[0][1]
            for idx, _, _, al in singles:
                if al is None:
                    remove.add(idx)
            for idx, _, _, _ in stars[1:]:
                remove.add(idx)
            replace[stars[0][0]] = f"{ind}import {pkg}.*"
            continue
        if has_alias or len(singles) < 2:
            continue
        singles.sort(key=lambda e: e[0])
        replace[singles[0][0]] = f"{singles[0][1]}import {pkg}.*"
        for idx, _, _, _ in singles[1:]:
            remove.add(idx)

    if not remove and not replace:
        return text, False

    out = []
    for i, line in enumerate(lines):
        if i in remove:
            continue
        out.append(replace[i] if i in replace else line)
    new_text = nl.join(out)
    if text.endswith("\n") and not new_text.endswith("\n"):
        new_text += nl
    return new_text, new_text != text


def main() -> int:
    if len(sys.argv) > 1:
        print("No arguments — only rewrites Kotlin under this demo's src/.", file=sys.stderr)
        return 2

    src = Path(__file__).resolve().parent / "src"
    if not src.is_dir():
        print(f"Missing {src}", file=sys.stderr)
        return 1

    files = sorted(src.rglob("*.kt"))
    if not files:
        print(f"No .kt files under {src}", file=sys.stderr)
        return 1

    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except OSError as e:
            print(f"{f}: {e}", file=sys.stderr)
            return 1
        new_text, changed = transform_source(text)
        if changed:
            f.write_text(new_text, encoding="utf-8", newline="")
            print(f"updated: {f}")
        else:
            print(f"unchanged: {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
