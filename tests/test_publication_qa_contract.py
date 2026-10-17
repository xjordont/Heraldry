"""Regress publication position authority and nonsemantic layout fixes."""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import query_typst
from qa_contract import MANDATORY_CHECKS


class CompileBoundQuery(unittest.TestCase):
    def test_query_uses_exact_pdf_and_typst_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "build").mkdir()
            (root / "typst").mkdir()
            (root / "dist").mkdir()
            source = root / "typst/content.typ"
            pdf = root / "dist/Heraldry_RC999_inkjet-borderless.pdf"
            source.write_text("Typst fixture", encoding="utf-8")
            pdf.write_bytes(b"PDF fixture bytes")
            payload = {"substrate": "cream", "edition": "print",
                       "content_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                       "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
                       "positions": {k: [] for k in query_typst.SELECTORS}}
            (root / "build/query.json").write_text(json.dumps(payload), encoding="utf-8")
            with patch.object(query_typst, "version", return_value="RC999"):
                self.assertEqual(query_typst.compiled_positions(root), payload["positions"])
                pdf.write_bytes(b"different PDF")
                with self.assertRaisesRegex(ValueError, "Stale PDF"):
                    query_typst.compiled_positions(root)
                pdf.write_bytes(b"PDF fixture bytes")
                source.write_text("different source", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "Stale Typst"):
                    query_typst.compiled_positions(root)

    def test_page_map_is_mandatory(self):
        self.assertIn("page_map_accuracy", MANDATORY_CHECKS)


class LayoutSourceContract(unittest.TestCase):
    def test_right_alignment_is_preserved(self):
        code = (ROOT / "typst/heraldry.typ").read_text(encoding="utf-8")
        self.assertIn("if a == right { right }", code)

    def test_stat_markers_do_not_repeat_source_or_close_before_table(self):
        code = (ROOT / "typst/heraldry.typ").read_text(encoding="utf-8")
        self.assertNotIn("#pre#pre", code)
        for title, next_title in (("#let statstrip(", "#let statcard("),
                                  ("#let statcard(", "#let cards(")):
            block = code.split(title, 1)[1].split(next_title, 1)[0]
            self.assertEqual(block.count('#tmark(id, "s")'), 1)
            self.assertEqual(block.count('#tmark(id, "e")'), 1)
            self.assertLess(block.index('#coin-text(table('), block.index('#tmark(id, "e")'))

    def test_figure_has_true_end_marker(self):
        code = (ROOT / "typst/heraldry.typ").read_text(encoding="utf-8")
        block = code.split("#let figure-block(", 1)[1]
        self.assertEqual(block.count('#tmark(id, "s")'), 1)
        self.assertEqual(block.count('#tmark(id, "e")'), 1)
        self.assertLess(block.index("#line(length: 100%"), block.index('#tmark(id, "e")'))


if __name__ == "__main__":
    unittest.main()
