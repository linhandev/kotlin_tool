import tempfile
import unittest
from pathlib import Path

import migrate


class MigrateTest(unittest.TestCase):
    def test_load_mapping_and_replace_mapped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mapping = root / "m.csv"
            mapping.write_text(
                "source_package,declaration,status,target_package,target_declaration\n"
                "platform.ohos,FOO,mapped,platform.target,\n",
                encoding="utf-8",
            )
            (root / "src" / "ohosMain" / "kotlin").mkdir(parents=True)
            kt = root / "src" / "ohosMain" / "kotlin" / "T.kt"
            kt.write_text("import platform.ohos.FOO\n", encoding="utf-8")

            stats = migrate.migrate_project(root, mapping, write=False)
            self.assertEqual(stats.fq_replaced, 1)
            self.assertEqual(stats.lines_changed, 1)
            self.assertEqual(stats.wildcard_hits, [])
            self.assertEqual(stats.fq_not_changed, [])

            stats_w = migrate.migrate_project(root, mapping, write=True)
            self.assertEqual(kt.read_text(encoding="utf-8"), "import platform.target.FOO\n")

    def test_replace_preserves_as_and_line_comment(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mapping = root / "m.csv"
            mapping.write_text(
                "source_package,declaration,status,target_package,target_declaration\n"
                "platform.ohos,FOO,mapped,platform.target,\n",
                encoding="utf-8",
            )
            (root / "src" / "ohosMain" / "kotlin").mkdir(parents=True)
            kt = root / "src" / "ohosMain" / "kotlin" / "T.kt"
            kt.write_text(
                "import platform.ohos.FOO as Alias // keep\n",
                encoding="utf-8",
            )
            migrate.migrate_project(root, mapping, write=True)
            self.assertEqual(
                kt.read_text(encoding="utf-8"),
                "import platform.target.FOO as Alias // keep\n",
            )

    def test_import_path_fqname_and_span(self) -> None:
        fq, s, e = migrate.import_path_fqname_and_span(
            "  import  platform.ohos.FOO  as  X  // c\n"
        )
        self.assertEqual(fq, "platform.ohos.FOO")
        self.assertEqual("  import  platform.ohos.FOO  as  X  // c\n"[s:e], "platform.ohos.FOO")

    def test_wildcard_warning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mapping = root / "m.csv"
            mapping.write_text(
                "source_package,declaration,status,target_package,target_declaration\n"
                "platform.ohos,FOO,mapped,platform.target,\n",
                encoding="utf-8",
            )
            (root / "src" / "ohosMain" / "kotlin").mkdir(parents=True)
            kt = root / "src" / "ohosMain" / "kotlin" / "T.kt"
            kt.write_text("import platform.ohos.*\n", encoding="utf-8")

            stats = migrate.migrate_project(root, mapping, write=False)
            self.assertEqual(len(stats.wildcard_hits), 1)
            self.assertIn("Can't process wildcard import", stats.wildcard_hits[0][1])

    def test_wildcard_other_package_not_flagged(self) -> None:
        """Only ``import <mapping source_package>.*`` is a wildcard hit, not ``import foo.*``."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mapping = root / "m.csv"
            mapping.write_text(
                "source_package,declaration,status,target_package,target_declaration\n"
                "platform.ohos,FOO,mapped,platform.target,\n",
                encoding="utf-8",
            )
            (root / "src" / "ohosMain" / "kotlin").mkdir(parents=True)
            kt = root / "src" / "ohosMain" / "kotlin" / "T.kt"
            kt.write_text("import java.util.*\n", encoding="utf-8")

            stats = migrate.migrate_project(root, mapping, write=False)
            self.assertEqual(stats.wildcard_hits, [])

    def test_missing_and_ambiguous_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mapping = root / "m.csv"
            mapping.write_text(
                "source_package,declaration,status,target_package,target_declaration\n"
                "platform.ohos,GONE,missing,,\n"
                "platform.devices,X,ambiguous,a|b,\n",
                encoding="utf-8",
            )
            (root / "src" / "ohosMain" / "kotlin").mkdir(parents=True)
            kt = root / "src" / "ohosMain" / "kotlin" / "T.kt"
            kt.write_text(
                "import platform.ohos.GONE\nimport platform.devices.X\n",
                encoding="utf-8",
            )

            stats = migrate.migrate_project(root, mapping, write=False)
            self.assertEqual(len(stats.fq_not_changed), 2)
            reasons = {r[1] for r in stats.fq_not_changed}
            self.assertTrue(any("not available" in r for r in reasons))
            self.assertTrue(any("Multiple packages" in r for r in reasons))

    def test_duplicate_source_fqname_asserts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mapping = root / "m.csv"
            mapping.write_text(
                "source_package,declaration,status,target_package,target_declaration\n"
                "platform.ohos,FOO,mapped,platform.a,\n"
                "platform.ohos,FOO,mapped,platform.b,\n",
                encoding="utf-8",
            )
            with self.assertRaises(AssertionError) as ctx:
                migrate.load_mapping_csv(mapping)
            self.assertIn("duplicate source fqname", str(ctx.exception))

    def test_nested_target_declaration_import_and_typealias(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mapping = root / "m.csv"
            mapping.write_text(
                "source_package,declaration,status,target_package,target_declaration\n"
                "platform.framework,Rdb_KeyData,mapped,platform.ArkData.RDB,"
                "Rdb_KeyInfo::Rdb_KeyData\n",
                encoding="utf-8",
            )
            (root / "src" / "ohosMain" / "kotlin").mkdir(parents=True)
            kt = root / "src" / "ohosMain" / "kotlin" / "T.kt"
            kt.write_text(
                "import platform.framework.Rdb_KeyData\n\nfun f(x: Rdb_KeyData?) {}\n",
                encoding="utf-8",
            )
            stats = migrate.migrate_project(root, mapping, write=True)
            self.assertEqual(stats.typealias_lines_added, 1)
            text = kt.read_text(encoding="utf-8")
            self.assertIn(
                "import platform.ArkData.RDB.`Rdb_KeyInfo::Rdb_KeyData`",
                text,
            )
            self.assertIn("typealias Rdb_KeyData = `Rdb_KeyInfo::Rdb_KeyData`", text)

    def test_mapping_csv_without_target_declaration_column(self) -> None:
        """Older CSVs without the column behave like empty ``target_declaration``."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mapping = root / "m.csv"
            mapping.write_text(
                "source_package,declaration,status,target_package\n"
                "platform.ohos,FOO,mapped,platform.target\n",
                encoding="utf-8",
            )
            (root / "src" / "ohosMain" / "kotlin").mkdir(parents=True)
            kt = root / "src" / "ohosMain" / "kotlin" / "T.kt"
            kt.write_text("import platform.ohos.FOO\n", encoding="utf-8")
            migrate.migrate_project(root, mapping, write=True)
            self.assertEqual(kt.read_text(encoding="utf-8"), "import platform.target.FOO\n")


if __name__ == "__main__":
    unittest.main()
