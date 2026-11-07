"""Whitespace measurements are triage; complete-unit keeps can require space."""
import sys
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from layout_diagnostics import interval_summary, page_diagnostics
import layout_qa


class DensityDiagnostics(unittest.TestCase):
    def test_front_contents_heading_is_not_a_stranded_rules_heading(self):
        with tempfile.TemporaryDirectory() as tmp:
            pdf, report = Path(tmp)/'outlined.pdf', Path(tmp)/'report.json'
            font = Path(__file__).resolve().parents[1]/'fonts/static/SourceSerif4-Bold.ttf'
            with pymupdf.open() as doc:
                for _ in range(2):
                    page=doc.new_page(width=612,height=792)
                    page.insert_font(fontname='SourceSerif4-Bold',fontfile=str(font))
                    page.insert_text((45,720),'Heading',fontname='SourceSerif4-Bold',fontsize=13)
                doc.set_toc([[1,'First rules chapter',2]])
                doc.save(pdf)
            with patch.object(sys,'argv',['layout_qa.py',str(pdf),'--report',str(report)]), contextlib.redirect_stdout(io.StringIO()):
                layout_qa.main()
            flags=json.loads(report.read_text())['flags']
            self.assertEqual([f['page'] for f in flags if f['code']=='stranded_heading'],[2])

    def test_layout_report_prints_after_closing_windows_pdf_handle(self):
        with tempfile.TemporaryDirectory() as tmp:
            pdf, report = Path(tmp) / "fixture.pdf", Path(tmp) / "report.json"
            with pymupdf.open() as doc:
                page = doc.new_page(width=612, height=792)
                page.insert_text((45, 100), "Readable rules", fontsize=10.5)
                doc.save(pdf)
            output = io.StringIO()
            with patch.object(sys, "argv", ["layout_qa.py", str(pdf), "--report", str(report)]), \
                 contextlib.redirect_stdout(output):
                layout_qa.main()
            self.assertEqual(json.loads(output.getvalue())["pages"], 1)
            self.assertEqual(len(json.loads(report.read_text())["density_triage"]), 1)
            pdf.unlink()  # Windows fails this if the native document is still open.

    def test_intervals_are_clipped_and_overlaps_counted_once(self):
        result = interval_summary([(-10, 10), (5, 15), (50, 70), (110, 120)], 0, 100)
        self.assertEqual(result["vertical_union_fraction"], 0.35)
        self.assertEqual(result["largest_empty_band_pt"], 35)
        self.assertEqual(result["bottom_empty_band_pt"], 30)

    def test_blank_verso_remains_context_for_review_not_automatic_failure(self):
        with pymupdf.open() as doc:
            page = doc.new_page(width=612, height=792)
            result = page_diagnostics(page, 6, top=40.5, bottom=751.5, tab=30)
        self.assertEqual(result["body_lines"], 0)
        self.assertEqual(result["vertical_union_fraction"], 0)
        self.assertNotIn("status", result)
        self.assertIn("review context", result["interpretation"])

    def test_body_short_paragraph_and_column_imbalance_are_recorded(self):
        with pymupdf.open() as doc:
            page = doc.new_page(width=612, height=792)
            page.insert_text((45, 100), "Victory Conditions", fontsize=10.5)
            page.insert_text((45, 120), "Resolve the scenario's victory procedure.", fontsize=10.5)
            result = page_diagnostics(page, 1, top=40.5, bottom=751.5, tab=30)
        self.assertGreater(result["bottom_empty_band_pt"], 600)
        self.assertEqual(result["column_lines"]["right"], 0)
        self.assertTrue(result["short_text_blocks"])


class HeadAlone(unittest.TestCase):
    def test_a_page_holding_only_its_section_head_is_flagged(self):
        heads = ["6.7 Human Trinket Table"]
        self.assertTrue(layout_qa.head_alone(["6.7", "Human Trinket Table"], heads))
        self.assertFalse(layout_qa.head_alone(["6.7", "Human Trinket Table", "If a Hero randomly generates",
                                               "Human ancestry, roll 1d10 on the table below."], heads))
        self.assertFalse(layout_qa.head_alone(["Any text"], []))      # no outline heading on the page


if __name__ == "__main__":
    unittest.main()
