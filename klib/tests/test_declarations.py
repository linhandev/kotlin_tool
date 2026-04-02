import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from klib.declarations import collect_from_klib, collect_from_klibs


class DeclarationsTest(unittest.TestCase):
    @patch("klib.declarations.subprocess.check_output")
    def test_collect_from_klib(self, mock_check: MagicMock) -> None:
        lines = [
            "klib dump-metadata-signatures /path/to/lib",
            # Synthetic OHOS-style
            "platform.ohos/ANYMARK|{}ANYMARK[100]",
            "platform.ohos/ANYMARK.<get-ANYMARK>|<get-ANYMARK>(){}[100]",
            "platform.ohos/SomeType.member|{}member[100]",
            "platform.ohos/SomeType.<init>|<init>(){}[100]",
            "platform.ohos/SomeEnum.ENTRY_ALPHA|{}ENTRY_ALPHA[100]",
            "platform.ohos/napi_typedarray_type.napi_int16_array|null[100]",
            "platform.ohos/napi_typedarray_type.napi_int32_array|null[100]",
            "platform.ohos/SomeType.Companion|null[100]",
            "platform.ohos/ZZZ_CONST|{}ZZZ_CONST[100]",
            "platform.ohos/ANYMARK|{}ANYMARK[100]",
            # Real zlib: const + getter pair; only non-accessor line is kept
            "platform.zlib/ZLIB_VERNUM|{}ZLIB_VERNUM[100]",
            "platform.zlib/ZLIB_VERNUM.<get-ZLIB_VERNUM>|<get-ZLIB_VERNUM>(){}[100]",
            # Real iconv: signature contains "|" inside generic text (after first "|")
            "platform.iconv/iconv|iconv(kotlinx.cinterop.CPointer<out|kotlinx.cinterop.CPointed>?){}[100]",
            "platform.iconv/iconv_tVar|null[100]",
            # Real OHOS: nested property setter (skip)
            "platform.ohos/ARKUI_TextPickerCascadeRangeContent.children.<set-children>|<set-children>(kotlinx.cinterop.CPointer<platform.ohos.ARKUI_TextPickerRangeContent>?){}[100]",
            "noise without slash",
            "",
        ]
        mock_check.return_value = "\n".join(lines)

        declarations = collect_from_klib(Path("/klib/bin"), Path("/some/klib/dir"))

        self.assertEqual(
            declarations,
            [
                ("platform.iconv", "iconv"),
                ("platform.iconv", "iconv_tVar"),
                ("platform.ohos", "ANYMARK"),
                ("platform.ohos", "SomeEnum.ENTRY_ALPHA"),
                ("platform.ohos", "SomeType.Companion"),
                ("platform.ohos", "SomeType.member"),
                ("platform.ohos", "ZZZ_CONST"),
                ("platform.ohos", "napi_typedarray_type.napi_int16_array"),
                ("platform.ohos", "napi_typedarray_type.napi_int32_array"),
                ("platform.zlib", "ZLIB_VERNUM"),
            ],
        )
        mock_check.assert_called_once_with(
            ["/klib/bin", "dump-metadata-signatures", "/some/klib/dir"],
            text=True,
        )

    @patch("klib.declarations.subprocess.check_output")
    def test_collect_from_klibs_matches_sequential_merge(self, mock_check: MagicMock) -> None:
        """Parallel ``collect_from_klibs`` must equal merging ``collect_from_klib`` per dir."""

        def fake_output(cmd: list[str], text: bool = True) -> str:
            kd = Path(cmd[2]).name
            return f"platform.{kd}/DECL_{kd}|{{}}[1]\n"

        mock_check.side_effect = fake_output

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("k1", "k2", "k3"):
                (root / name).mkdir()

            parallel = collect_from_klibs(Path("/bin/klib"), root)

            mock_check.reset_mock()
            mock_check.side_effect = fake_output
            sequential: list[tuple[str, str, str]] = []
            for kd in sorted(p for p in root.iterdir() if p.is_dir()):
                for pkg, decl in collect_from_klib(Path("/bin/klib"), kd):
                    sequential.append((kd.name, pkg, decl))
            sequential.sort()

        self.assertEqual(
            parallel,
            [
                ("k1", "platform.k1", "DECL_k1"),
                ("k2", "platform.k2", "DECL_k2"),
                ("k3", "platform.k3", "DECL_k3"),
            ],
        )
        self.assertEqual(parallel, sequential)

    def test_collect_from_klibs_empty_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(collect_from_klibs(Path("/bin/klib"), Path(tmp)), [])


if __name__ == "__main__":
    unittest.main()
