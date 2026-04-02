import tempfile
import unittest
from pathlib import Path

from klib.mapping import get_compiler_version


class MappingTest(unittest.TestCase):
    def test_get_compiler_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plat = root / "p" / "klib" / "platform" / "ohos_arm64"
            plat.mkdir(parents=True)
            konan = root / "p" / "konan" / "konan.properties"
            konan.parent.mkdir(parents=True, exist_ok=True)
            konan.write_text(
                "# c\ncompilerVersion=1.2.3-test\nother=x\n",
                encoding="utf-8",
            )
            self.assertEqual(get_compiler_version(plat), "1.2.3-test")


if __name__ == "__main__":
    unittest.main()
