"""
Exercises ``import_path_fqname_and_span`` for IDEA-style, compiling-import lines.

**Not covered** (would need Kotlin PSI or a full lexer): multiline ``import``,
backtick / quoted names, comments *inside* the dotted path, BOM-prefixed lines,
``import`` followed only by ``\\v``/``\\f`` (we only accept space/tab after
``import``), string literals on the import line, K2-only edge cases.
"""
from __future__ import annotations

import unittest

import migrate


class ImportPathFqnameAndSpanTest(unittest.TestCase):
    def _assert_span(
        self,
        line: str,
        *,
        expect: tuple[str, str] | None,
        msg: str = "",
    ) -> None:
        """
        If ``expect`` is ``None``, result must be ``None``.
        Else ``expect`` is ``(fqname, exact_slice_text)`` where ``exact_slice_text``
        must equal ``line[start:end]``.
        """
        got = migrate.import_path_fqname_and_span(line)
        if expect is None:
            self.assertIsNone(got, msg or repr(line))
            return
        exp_fq, exp_slice = expect
        self.assertIsNotNone(got, msg or repr(line))
        assert got is not None
        fq, s, e = got
        self.assertEqual(fq, exp_fq, msg)
        self.assertEqual(line[s:e], exp_slice, msg)
        self.assertEqual("".join(line[s:e].split()), exp_fq, msg)

    def test_none_not_import_or_empty_path(self) -> None:
        for line in (
            "",
            "\n",
            " // import foo.Bar\n",
            "not import\n",
            "important\n",
            "Import foo.Bar\n",
            "import\n",
            "import \n",
            "import  \n",
            "import\t\n",
            "importfoo.Bar\n",  # keyword must be followed by whitespace
        ):
            self._assert_span(line, expect=None)

    def test_none_wildcard_or_invalid_path(self) -> None:
        for line in (
            "import foo.*\n",
            "import foo.* // wild\n",
            "import foo..bar\n",
            "import .foo\n",
            "import foo.\n",
        ):
            self._assert_span(line, expect=None)

    def test_simple_and_indent(self) -> None:
        self._assert_span(
            "import a.b.C\n",
            expect=("a.b.C", "a.b.C"),
        )
        self._assert_span(
            "  import  a.b.C  \n",
            expect=("a.b.C", "a.b.C"),
        )
        self._assert_span(
            "\timport\tx.y.Z\n",
            expect=("x.y.Z", "x.y.Z"),
        )

    def test_single_segment(self) -> None:
        self._assert_span("import Foo\n", expect=("Foo", "Foo"))

    def test_crlf_and_cr_only(self) -> None:
        self._assert_span(
            "import pkg.Type\r\n",
            expect=("pkg.Type", "pkg.Type"),
        )
        self._assert_span(
            "import pkg.Type\r",
            expect=("pkg.Type", "pkg.Type"),
        )

    def test_semicolon(self) -> None:
        self._assert_span(
            "import a.b.C;\n",
            expect=("a.b.C", "a.b.C"),
        )
        self._assert_span(
            "import a.b.C; \n",
            expect=("a.b.C", "a.b.C"),
        )
        self._assert_span(
            "import a.b.C;;\n",
            expect=("a.b.C", "a.b.C"),
        )

    def test_line_comment(self) -> None:
        self._assert_span(
            "import a.b.C // one\n",
            expect=("a.b.C", "a.b.C"),
        )
        self._assert_span(
            "import  a.b.C  // spaces\n",
            expect=("a.b.C", "a.b.C"),
        )

    def test_block_comment_start_after_path(self) -> None:
        self._assert_span(
            "import a.b.C /* tail */\n",
            expect=("a.b.C", "a.b.C"),
        )
        self._assert_span(
            "import a.b.C/*no space*/\n",
            expect=("a.b.C", "a.b.C"),
        )

    def test_as_alias(self) -> None:
        self._assert_span(
            "import a.b.C as Z\n",
            expect=("a.b.C", "a.b.C"),
        )
        self._assert_span(
            "import  a.b.C  as  Alias  \n",
            expect=("a.b.C", "a.b.C"),
        )

    def test_as_with_line_comment(self) -> None:
        self._assert_span(
            "import a.b.C as Z // note\n",
            expect=("a.b.C", "a.b.C"),
        )
        self._assert_span(
            "import platform.ohos.FOO as Alias // keep\n",
            expect=("platform.ohos.FOO", "platform.ohos.FOO"),
        )

    def test_as_with_block_comment_after_alias(self) -> None:
        self._assert_span(
            "import a.b.C as Z /* c */\n",
            expect=("a.b.C", "a.b.C"),
        )

    def test_slash_slash_in_comment_not_in_path(self) -> None:
        """``//`` only in comment tail — path still parsed."""
        self._assert_span(
            "import a.b.C // https://example.com\n",
            expect=("a.b.C", "a.b.C"),
        )

    def test_replace_roundtrip(self) -> None:
        """Slice replacement preserves suffix (as, ``//``, newline style)."""
        cases = (
            ("import old.path.Here\n", "import new.pkg.Here\n"),
            ("import old.path.Here as A\n", "import new.pkg.Here as A\n"),
            ("import old.path.Here as A // x\n", "import new.pkg.Here as A // x\n"),
            ("import  old.path.Here  ;  // c\n", "import  new.pkg.Here  ;  // c\n"),
            ("\timport\told.path.Here\r\n", "\timport\tnew.pkg.Here\r\n"),
        )
        new_path = "new.pkg.Here"
        for line, want in cases:
            with self.subTest(line=repr(line)):
                got = migrate.import_path_fqname_and_span(line)
                self.assertIsNotNone(got)
                assert got is not None
                _, s, e = got
                out = line[:s] + new_path + line[e:]
                self.assertEqual(out, want)

    def test_platform_style_long_path(self) -> None:
        self._assert_span(
            "import platform.ohos.data.rdb.RdbPredicates\n",
            expect=("platform.ohos.data.rdb.RdbPredicates", "platform.ohos.data.rdb.RdbPredicates"),
        )

    def test_semicolon_touching_slash_slash(self) -> None:
        self._assert_span(
            "import a.b.C;//c\n",
            expect=("a.b.C", "a.b.C"),
        )
        self._assert_span(
            "import a.b as Z;//c\n",
            expect=("a.b", "a.b"),
        )

    def test_semicolon_before_line_comment_with_spaces(self) -> None:
        self._assert_span(
            "import a.b.C; // c\n",
            expect=("a.b.C", "a.b.C"),
        )
        self._assert_span(
            "import a.b as Z; // c\n",
            expect=("a.b", "a.b"),
        )

    def test_trailing_semicolon_after_alias(self) -> None:
        self._assert_span(
            "import a.b.C as Z;\n",
            expect=("a.b.C", "a.b.C"),
        )

    def test_unicode_identifier_segments(self) -> None:
        """Python ``isalnum`` on Unicode letters matches our segment check."""
        self._assert_span(
            "import naïve.Example\n",
            expect=("naïve.Example", "naïve.Example"),
        )

    def test_none_backtick_qualified_name(self) -> None:
        """Backtick segments are valid Kotlin but not ``_dotted_import_path``."""
        self._assert_span(
            "import `foo bar`.Baz\n",
            expect=None,
        )

    def test_none_bom_before_import(self) -> None:
        """UTF-8 BOM breaks ``import`` at column 0 (no strip)."""
        self._assert_span("\ufeffimport foo.Bar\n", expect=None)

    def test_none_vertical_tab_after_import(self) -> None:
        """Only space/tab accepted after ``import`` (not ``\\v``)."""
        self._assert_span("import\vfoo.Bar\n", expect=None)


class WildcardImportDetectionTest(unittest.TestCase):
    """``is_mapping_scoped_wildcard_import`` stays aligned with ``import`` + ws rules."""

    def test_tab_after_import(self) -> None:
        pkgs = frozenset({"platform.ohos"})
        self.assertTrue(
            migrate.is_mapping_scoped_wildcard_import(
                "\timport\tplatform.ohos.*\n",
                pkgs,
            )
        )

    def test_wildcard_with_line_comment(self) -> None:
        pkgs = frozenset({"platform.ohos"})
        self.assertTrue(
            migrate.is_mapping_scoped_wildcard_import(
                "import platform.ohos.* // star\n",
                pkgs,
            )
        )


class ImportPathSpanIntegrationTest(unittest.TestCase):
    """``process_line`` / ``migrate_project`` with span-based replace."""

    def test_slice_replace_matches_manual(self) -> None:
        line = "  import  p.a.T  as  X  // n\n"
        got = migrate.import_path_fqname_and_span(line)
        self.assertIsNotNone(got)
        assert got is not None
        _, s, e = got
        self.assertEqual(line[:s] + "NEW" + line[e:], "  import  NEW  as  X  // n\n")


if __name__ == "__main__":
    unittest.main()
