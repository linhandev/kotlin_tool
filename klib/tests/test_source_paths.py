import subprocess
import tempfile
import unittest
from pathlib import Path

from klib.source_paths import collect


class SourcePathsTest(unittest.TestCase):
    def test_non_git_filters_by_source_set_and_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src" / "commonMain" / "kotlin").mkdir(parents=True)
            (root / "src" / "commonMain" / "kotlin" / "A.kt").write_text("x", encoding="utf-8")
            (root / "src" / "jvmMain" / "kotlin").mkdir(parents=True)
            (root / "src" / "jvmMain" / "kotlin" / "B.kt").write_text("y", encoding="utf-8")
            (root / "other").mkdir(parents=True)
            (root / "other" / "C.kt").write_text("z", encoding="utf-8")

            paths = collect(root, ["commonMain"])
            rels = sorted(p.relative_to(root).as_posix() for p in paths)
            self.assertEqual(rels, ["src/commonMain/kotlin/A.kt"])

            paths_both = collect(root, ["commonMain", "jvmMain"])
            rels_b = sorted(p.relative_to(root).as_posix() for p in paths_both)
            self.assertEqual(
                rels_b,
                ["src/commonMain/kotlin/A.kt", "src/jvmMain/kotlin/B.kt"],
            )

    def test_empty_source_set_names_returns_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src" / "commonMain").mkdir(parents=True)
            (root / "src" / "commonMain" / "x.kt").write_text("", encoding="utf-8")
            self.assertEqual(collect(root, []), [])
            self.assertEqual(collect(root, ["", "  "]), [])

    def test_git_respects_gitignore(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
            (root / "src" / "commonMain").mkdir(parents=True)
            (root / "src" / "commonMain" / "keep.kt").write_text("", encoding="utf-8")
            (root / "src" / "commonMain" / "ignored.kt").write_text("", encoding="utf-8")
            (root / ".gitignore").write_text("ignored.kt\n", encoding="utf-8")
            subprocess.run(["git", "add", ".gitignore", "src/commonMain/keep.kt"], cwd=root, check=True)

            paths = collect(root, ["commonMain"])
            rels = [p.relative_to(root).as_posix() for p in paths]
            self.assertEqual(rels, ["src/commonMain/keep.kt"])

    def test_git_includes_untracked_non_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
            (root / "src" / "commonMain").mkdir(parents=True)
            (root / "src" / "commonMain" / "new.kt").write_text("", encoding="utf-8")

            paths = collect(root, ["commonMain"])
            rels = [p.relative_to(root).as_posix() for p in paths]
            self.assertEqual(rels, ["src/commonMain/new.kt"])

    def test_not_a_directory_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "f"
            f.write_text("x", encoding="utf-8")
            with self.assertRaises(NotADirectoryError):
                collect(f, ["commonMain"])


if __name__ == "__main__":
    unittest.main()
