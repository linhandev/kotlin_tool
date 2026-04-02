import tempfile
import unittest
from pathlib import Path

from klib.manifest import header_paths, headers, _is_header_path


class ManifestTest(unittest.TestCase):
    def test_headers_included_headers_after_other_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "k"
            (root / "default").mkdir(parents=True)
            (root / "default" / "manifest").write_text(
                "abi_version=2\nincludedHeaders=usr/include/a.h token\n",
                encoding="utf-8",
            )
            self.assertEqual(headers(root), ["usr/include/a.h", "token"])

    def test_header_paths_resolves_existing_files_under_sysroot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "k"
            (root / "default").mkdir(parents=True)
            (root / "default" / "manifest").write_text(
                "includedHeaders=usr/include/a.h missing.h\n",
                encoding="utf-8",
            )
            sysroot = Path(tmp) / "sys"
            inc = sysroot / "usr" / "include"
            inc.mkdir(parents=True)
            h = inc / "a.h"
            h.write_text("/* */\n", encoding="utf-8")
            self.assertEqual(header_paths(root, sysroot), [h.resolve()])

    def test_headers_multiple_included_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "k"
            (root / "default").mkdir(parents=True)
            (root / "default" / "manifest").write_text(
                "includedHeaders=usr/include/a.h usr/include/b.h\n",
                encoding="utf-8",
            )
            self.assertEqual(headers(root), ["usr/include/a.h", "usr/include/b.h"])

    def test_is_header_path_token(self) -> None:
        self.assertFalse(_is_header_path("a" * 64))
        self.assertTrue(_is_header_path("a" * 62 + ".h"))
        self.assertTrue(_is_header_path("usr/include/x.h"))
        self.assertTrue(_is_header_path("single.h"))

    def test_headers_filters_snapshot_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "k"
            (root / "default").mkdir(parents=True)
            (root / "default" / "manifest").write_text(
                "includedHeaders="
                + "usr/include/ok.h "
                + "a" * 64
                + "\n",
                encoding="utf-8",
            )
            self.assertEqual(headers(root), ["usr/include/ok.h"])


if __name__ == "__main__":
    unittest.main()
