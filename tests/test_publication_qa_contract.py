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
from tables import PT, LEAD, PAD, VPAD


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

    def test_effective_layout_profile_matches_renderer(self):
        prod = json.loads((ROOT / "config/production.json").read_text(encoding="utf-8"))
        tokens = json.loads((ROOT / "config/design_tokens.json").read_text(encoding="utf-8"))
        v4 = (ROOT / "typst/templates/system.typ").read_text(encoding="utf-8")
        book = (ROOT / "typst/heraldry.typ").read_text(encoding="utf-8")
        fmt = prod["format"]
        self.assertIn("#let m-in = 0.75in", v4)
        self.assertIn("#let m-out = 0.55in", v4)
        self.assertIn("#let m-top = 0.68in", v4)
        self.assertIn("#let gap = 0.24in", v4)
        self.assertIn("#let body-size = 11pt", v4)
        self.assertEqual([fmt["inside_margin_inches"], fmt["outside_margin_inches"],
                          fmt["top_margin_inches"], fmt["column_gap_inches"]],
                         [0.75, 0.55, 0.68, 0.24])
        self.assertEqual((fmt["body_font_size_pt"], fmt["table_font_size_pt"]), (11, 9.3))
        self.assertEqual((tokens["type_pt"]["body"], tokens["type_pt"]["chapter"],
                          tokens["fonts"]["max_families"]), (11, 50, 4))
        self.assertIn("#let table-size = 9.3pt", book)
        self.assertIn("#let table-lead = 2.7pt", book)
        self.assertEqual((PT, LEAD, PAD, VPAD), (9.3, 12, 5.0, 4.0))
        self.assertEqual((tokens["spacing_pt"]["table_horizontal_padding"],
                          tokens["spacing_pt"]["table_vertical_padding"]), (PAD, VPAD))


if __name__ == "__main__":
    unittest.main()
