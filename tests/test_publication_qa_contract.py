"""Regress publication position authority and nonsemantic layout fixes."""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import query_typst
import verify
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
            with patch.object(query_typst, "version", return_value="RC999"), \
                 patch.object(query_typst, 'validate_sidecar', return_value=payload['positions']) as validate:
                self.assertEqual(query_typst.compiled_positions(root), payload["positions"])
                validate.assert_called_once_with(payload['positions'], pdf, root=root)
                pdf.write_bytes(b"different PDF")
                with self.assertRaisesRegex(ValueError, "Stale PDF"):
                    query_typst.compiled_positions(root)
                pdf.write_bytes(b"PDF fixture bytes")
                source.write_text("different source", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "Stale Typst"):
                    query_typst.compiled_positions(root)

    def test_page_map_is_mandatory(self):
        self.assertIn("page_map_accuracy", MANDATORY_CHECKS)


class LayoutReportGate(unittest.TestCase):
    def clean_report(self):
        return {"pdf": "fixture.pdf", "pages": 2, "counts": {}, "flags": [], "flagged_pages": []}

    def run_detector(self, payload, *, exit_code=0, stale=None):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "layout.json"
            if stale is not None:
                report.write_text(json.dumps(stale))
            def process(args, **kwargs):
                # A previous PASS must have been removed before the new process.
                self.assertFalse(report.exists())
                self.assertIn("--report", args)
                if payload is not None:
                    report.write_text(payload if isinstance(payload, str) else json.dumps(payload))
                return SimpleNamespace(returncode=exit_code, stdout="", stderr="")
            with patch.object(verify.subprocess, "run", side_effect=process):
                return verify.layout_check("fixture.pdf", report)[0]

    def test_clean_counts_and_complete_report_pass(self):
        self.assertEqual(self.run_detector(self.clean_report()), "PASS")

    def test_missing_or_malformed_report_cannot_pass_successful_exit(self):
        for payload in (None, "{not json", {}, [], {"counts": {}}, self.clean_report() | {"counts": None},
                        self.clean_report() | {"counts": []}, self.clean_report() | {"pages": 0}):
            with self.subTest(payload=payload):
                self.assertEqual(self.run_detector(payload), "FAIL")

    def test_stale_pass_does_not_mask_missing_current_report(self):
        self.assertEqual(self.run_detector(None, stale=self.clean_report()), "FAIL")

    def test_real_flags_and_contradictory_counts_remain_failures(self):
        for code in ("near_empty", "stranded_heading", "text_overlap", "unsafe_edge", "small_type"):
            payload = self.clean_report() | {"counts": {code: 1},
                "flags": [{"page": 1, "code": code}], "flagged_pages": [1]}
            with self.subTest(code=code):
                self.assertEqual(self.run_detector(payload), "FAIL")
        for change in ({"flags": [{"page": 1, "code": "near_empty"}]}, {"flagged_pages": [1]}, {"status": "FAIL"}):
            self.assertEqual(self.run_detector(self.clean_report() | change), "FAIL")

    def test_nonzero_detector_exit_cannot_be_overruled_by_clean_report(self):
        self.assertEqual(self.run_detector(self.clean_report(), exit_code=1), "FAIL")


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
        self.assertIn('json("../../config/design_tokens.json")', v4)
        self.assertIn('#let body-size = type-token.body * 1pt', v4)
        from layout_profile import validate, MARGIN_INSIDE_PT, MARGIN_OUTSIDE_PT, MARGIN_TOP_PT, COLUMN_GAP_PT
        self.assertTrue(validate())
        for key, value in (('inside_margin_inches', MARGIN_INSIDE_PT), ('outside_margin_inches', MARGIN_OUTSIDE_PT),
                           ('top_margin_inches', MARGIN_TOP_PT), ('column_gap_inches', COLUMN_GAP_PT)):
            self.assertAlmostEqual(fmt[key], value / 72)
        self.assertEqual((fmt["body_font_size_pt"], fmt["table_font_size_pt"]), (10.5, 9))
        self.assertEqual((tokens["type_pt"]["body"], tokens["type_pt"]["chapter"],
                          tokens["fonts"]["max_families"]), (10.5, 50, 4))
        self.assertIn("#let table-size = v4.table-size", book)
        self.assertIn("#let table-lead = v4.table-lead", book)
        self.assertEqual((PT, PAD, VPAD), (9, 4.0, 2.2))
        self.assertAlmostEqual(LEAD, PT * 1.05 + tokens['type_pt']['table_leading_additive'])
        self.assertEqual((tokens["spacing_pt"]["table_horizontal_padding"],
                          tokens["spacing_pt"]["table_vertical_padding"]), (PAD, VPAD))


if __name__ == "__main__":
    unittest.main()
