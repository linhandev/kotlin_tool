"""Tests for ``klib`` (run with ``python -m unittest discover klib/tests`` from repo root)."""

import sys
from pathlib import Path

# klib/*.py use flat imports (`import config`, `import manifest`) assuming ``klib/`` is on sys.path.
_klib_dir = Path(__file__).resolve().parent.parent
if str(_klib_dir) not in sys.path:
    sys.path.insert(0, str(_klib_dir))
