import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import pymupdf  # noqa: E402
import layout_flow as lf  # noqa: E402


def text_line(x0, y0, x1, y1, text="A line of body text"):
    return {"dir": (1.0, 0.0), "bbox": (x0, y0, x1, y1), "spans": [{"text": text, "size": 10}]}


def rule(y, x0=45, x1=567, width=0.5):
    return {"rect": pymupdf.Rect(x0, y, x1, y), "width": width}


class RuleStrikes(unittest.TestCase):
    page = {"blocks": [{"lines": [text_line(45, 300, 300, 314.4)]}]}

    def test_a_hairline_through_the_letters_is_found(self):
        self.assertEqual(len(lf.rule_strikes(self.page, [rule(307)])), 1)

    def test_a_hairline_resting_on_the_letter_tops_is_found(self):
        # candidate 24, C.3: the band rule at 103.1 over a line boxed 100.6 to 115.0
        self.assertEqual(len(lf.rule_strikes(self.page, [rule(302.9)])), 1)

    def test_a_hairline_in_the_gap_above_is_not(self):
        self.assertEqual(lf.rule_strikes(self.page, [rule(301.5)]), [])

    def test_a_hairline_in_the_gap_below_is_not(self):
        self.assertEqual(lf.rule_strikes(self.page, [rule(318)]), [])

    def test_a_figure_stroke_with_its_label_on_it_is_not_tested(self):
        # FIG-11, FIG-18 and the Chapter 11 cycle set labels on their own heavier lines by design
        self.assertEqual(lf.rule_strikes(self.page, [rule(307, width=1.25)]), [])

    def test_a_short_rule_is_not_a_composition_rule(self):
        self.assertEqual(lf.rule_strikes(self.page, [rule(307, x0=100, x1=200)]), [])


class ColumnFeet(unittest.TestCase):
    def test_a_spanning_element_counts_for_both_columns(self):
        boxes = [(pymupdf.Rect(45, 100, 290, 400), "text"), (pymupdf.Rect(45, 450, 567, 500), "image"),
                 (pymupdf.Rect(320, 100, 567, 200), "text")]
        self.assertEqual(lf.column_feet(boxes), {"left": 500, "right": 500})

    def test_columns_end_where_their_own_content_ends(self):
        boxes = [(pymupdf.Rect(45, 100, 290, 600), "text"), (pymupdf.Rect(320, 100, 567, 250), "text")]
        self.assertEqual(lf.column_feet(boxes), {"left": 600, "right": 250})


class Classify(unittest.TestCase):
    def test_a_short_column_is_classed_by_what_follows_it(self):
        self.assertEqual(lf.classify(10, {11}, False, False), "section_end")       # heading at the next page top
        self.assertEqual(lf.classify(10, set(), False, True), "section_end")       # a chapter's last page
        self.assertEqual(lf.classify(10, set(), True, False), "keep_gap")          # a whole figure or table next
        self.assertEqual(lf.classify(10, set(), False, False), "interior")         # the text simply continues

    def test_a_kept_block_is_the_first_wide_non_text_element(self):
        figure_first = [(pymupdf.Rect(45, 60, 567, 400), "image"), (pymupdf.Rect(45, 420, 290, 434), "text")]
        text_first = [(pymupdf.Rect(45, 60, 290, 74), "text"), (pymupdf.Rect(45, 200, 567, 400), "image")]
        self.assertTrue(lf.opens_with_kept_block(figure_first))
        self.assertFalse(lf.opens_with_kept_block(text_first))


class SectionStarts(unittest.TestCase):
    def test_a_numbered_section_off_a_page_or_column_top_is_listed(self):
        doc = pymupdf.open()
        for _ in range(5):
            doc.new_page()
        go = lambda x, y: {"kind": pymupdf.LINK_GOTO, "to": pymupdf.Point(x, y)}
        doc.set_toc([[1, "Chapter", 1, go(45, 50)], [2, "1.1 Shares the opener", 1, go(45, 480)],
                     [2, "1.2 Page top", 2, go(45, 50)], [2, "1.3 Right column top", 3, go(320, 50)],
                     [2, "1.4 Mid column", 4, go(45, 400)], [3, "1.4.1 Subsection", 5, go(45, 400)]])
        self.assertEqual([s["heading"] for s in lf.analyse(doc)["mid_column_section_starts"]], ["1.4 Mid column"])


class ClassifyFromTheBuildRecord(unittest.TestCase):
    def doc(self, positions):
        import json
        doc = pymupdf.open()
        for _ in range(3):
            doc.new_page()
        doc.embfile_add("heraldry-positions.json", json.dumps({"positions": positions}).encode())
        return doc

    def test_what_tops_the_next_column_names_the_gap(self):
        top = lf.TOP
        starts = lf.column_starts(self.doc({
            "<hpos>": [[{"page": 2, "x": 45, "y": top, "level": 2}, {"page": 3, "x": 320, "y": top, "level": 3}]],
            "<tblpos>": [{"id": "FIG-9", "edge": "s", "page": 3, "x": 45, "y": top}],
            "<pm>": [{"seg": 1, "piece": 4, "edge": "s", "page": 2, "x": 320, "y": top}]}))
        self.assertEqual(starts, {(2, "left"): "section", (2, "right"): "piece", (3, "left"): "figure", (3, "right"): "heading"})
        self.assertEqual(lf.classify_by_record(1, "right", starts, False), ("section_end", None))
        self.assertEqual(lf.classify_by_record(2, "left", starts, False), ("keep_gap", "piece"))    # beside it first
        self.assertEqual(lf.classify_by_record(2, "right", starts, False), ("keep_gap", "figure"))
        self.assertEqual(lf.classify_by_record(3, "right", starts, False), ("interior", None))

    def test_without_the_record_the_page_geometry_is_used(self):
        self.assertIsNone(lf.column_starts(pymupdf.open()))


if __name__ == "__main__":
    unittest.main()
