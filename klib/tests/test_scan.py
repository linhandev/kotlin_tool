import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from klib.scan import scan_platform


class ScanTest(unittest.TestCase):
    @patch("klib.scan.subprocess.check_output")
    def test_scan_platform_single_klib(self, mock_check: MagicMock) -> None:
        lines = [
            "klib dump-metadata-signatures /path/to/lib",
            "platform.ohos/ANYMARK|{}ANYMARK[100]",
            "platform.ohos/ANYMARK|{}ANYMARK[100]",
            "platform.ohos/SomeType.member|{}member[100]",
            "platform.a/SHARED_DECL|{}[1]",
            "platform.b/SHARED_DECL|{}[1]",
        ]
        mock_check.return_value = "\n".join(lines)

        with tempfile.TemporaryDirectory() as tmp:
            kdir = Path(tmp) / "leaf"
            kdir.mkdir()
            (kdir / "default").mkdir()

            n, dup, multi = scan_platform(Path("/klib/bin"), kdir)

        self.assertEqual(n, 4)
        self.assertEqual(dup, 1)
        self.assertEqual(multi, 1)


if __name__ == "__main__":
    unittest.main()
