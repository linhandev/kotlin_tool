import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import klib.disambiguate as disambiguate


class DisambiguateTest(unittest.TestCase):
    def test_try_resolve_gles3_same_package(self) -> None:
        tgt = Path("/fake/klib")
        self.assertEqual(
            disambiguate.gles3(
                "platform.gles3",
                {"platform.gles3": tgt, "platform.other": tgt},
            ),
            "platform.gles3",
        )

    def test_try_resolve_gles3_not_in_candidates(self) -> None:
        tgt = Path("/fake/klib")
        self.assertIsNone(
            disambiguate.gles3(
                "platform.gles3",
                {"platform.other": tgt, "platform.x": tgt},
            )
        )

    def test_try_resolve_gles3_requires_platform_gles3_prefix(self) -> None:
        tgt = Path("/fake/klib")
        self.assertIsNone(
            disambiguate.gles3(
                "platform.foo.gles3.bar",
                {"platform.foo.gles3.bar": tgt, "platform.other": tgt},
            )
        )

    def test_try_resolve_gles3_case_sensitive(self) -> None:
        tgt = Path("/fake/klib")
        self.assertIsNone(
            disambiguate.gles3(
                "Platform.gles3",
                {"Platform.gles3": tgt},
            )
        )

    def test_by_hard_code_returns_target_package(self) -> None:
        self.assertEqual(
            disambiguate.by_hard_code("platform.ohos", "LOG_DEBUG"),
            "platform.PerformanceAnalysisKit.HiLog",
        )

    def test_by_hard_code_unknown(self) -> None:
        self.assertIsNone(disambiguate.by_hard_code("platform.ohos", "NO_SUCH"))

    def test_try_resolve_ambiguous_row_happy_path(self) -> None:
        if not shutil.which("ctags"):
            self.skipTest("ctags not on PATH")
        with tempfile.TemporaryDirectory() as tmp:
            sysroot = Path(tmp)
            inc = sysroot / "usr" / "include"
            inc.mkdir(parents=True)
            a = inc / "a.h"
            b = inc / "b.h"
            a.write_text("#define SHARED 1\n", encoding="utf-8")
            b.write_text("/* no SHARED */\n", encoding="utf-8")

            src_klib = Path(tmp) / "org.example.source"
            (src_klib / "default").mkdir(parents=True)
            (src_klib / "default" / "manifest").write_text(
                "includedHeaders=usr/include/a.h usr/include/b.h\n",
                encoding="utf-8",
            )

            tgt_a = Path(tmp) / "org.jetbrains.pkg.a"
            (tgt_a / "default").mkdir(parents=True)
            (tgt_a / "default" / "manifest").write_text(
                "includedHeaders=usr/include/a.h\n",
                encoding="utf-8",
            )

            tgt_b = Path(tmp) / "org.jetbrains.pkg.b"
            (tgt_b / "default").mkdir(parents=True)
            (tgt_b / "default" / "manifest").write_text(
                "includedHeaders=usr/include/b.h\n",
                encoding="utf-8",
            )

            target_pkg_to_klib = {
                "platform.PkgA": tgt_a.resolve(),
                "platform.PkgB": tgt_b.resolve(),
            }

            with (
                patch.object(disambiguate, "SOURCE_SYSROOT", sysroot),
                patch.object(disambiguate, "SOURCE_KLIBS", Path(tmp)),
                patch.object(disambiguate, "CTAGS_BIN", "ctags"),
            ):
                resolved = disambiguate.by_header(
                    source_klib_fdr=src_klib.name,
                    declaration="SHARED",
                    target_pkg_to_klib=target_pkg_to_klib,
                )
            self.assertEqual(resolved, "platform.PkgA")

    def test_dotted_declaration_skipped(self) -> None:
        r = disambiguate.by_header(
            source_klib_fdr="x",
            declaration="Foo.bar",
            target_pkg_to_klib={},
        )
        self.assertIsNone(r)


if __name__ == "__main__":
    unittest.main()
