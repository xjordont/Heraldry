"""Regression tests for the 2026-10-29 design-review repairs (layout only; no manuscript text)."""
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

import pymupdf
from pypdf import PdfReader
import typst

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import tables  # noqa: E402
from build_book import Book, RANGE, nobreak  # noqa: E402


def cell(text):
    return [{"t": "text", "v": text}]


POTIONS = {
    "header": [cell("d20"), cell("Item"), cell("Cost (c)"), cell("Effect")],
    "rows": [[cell(str(i)), cell(name), cell("24"), cell(effect)] for i, (name, effect) in enumerate([
        ("Potion of Protection from Arrows", "Gain +4 AV against ranged weapon attacks until the end of the round. "
         "You are Resistant to damage from ranged weapon attacks and harmful ranged Powers."),
        ("Potion of Superior Blindsight", "Until the end of the round, within 18\" you ignore Blinded and may draw LOS "
         "through Cover Terrain."),
        ("Oil of Greater Arcane Vestment", "Armour gains +4 AV until the end of the round."),
        ("Potion of Cloud Giant's Strength", "Gain +6 STR for attacks and Checks until the end of the round."),
    ], 1)],
}


def compile_fixture(source):
    (ROOT / "build").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=ROOT / "build") as folder:
        path = Path(folder) / "fixture.typ"
        path.write_text(source, encoding="utf-8")
        compiler = typst.Compiler(str(path), root=str(ROOT), font_paths=[str(ROOT / "fonts/static")],
                                  ignore_system_fonts=True, sys_inputs={"position-identity": "{}"})
        pdf, warnings = compiler.compile_with_warnings()
    if warnings:
        raise AssertionError("fixture warnings: " + str(warnings))
    return pdf


class TableWidths(unittest.TestCase):
    def test_word_wrapping_matches_whole_word_breaks(self):
        segments = tables.cell_segments(cell("Potion of Protection from Arrows"))
        self.assertEqual(tables.wrapped_lines(segments, 70 - 2 * tables.PAD), 3)
        self.assertEqual(tables.wrapped_lines(segments, 400), 1)

    def test_cell_aware_allocation_is_never_taller_than_proportional(self):
        mins, maxs, _ = tables.measure_table(POTIONS)
        old, _ = tables.allocate(mins, maxs, tables.FULL_W)
        new, _ = tables.allocate(mins, maxs, tables.FULL_W, [POTIONS])
        self.assertAlmostEqual(sum(new), tables.FULL_W, places=1)
        self.assertLessEqual(tables.est_height(POTIONS, new)[0], tables.est_height(POTIONS, old)[0])
        for minimum, width in zip(mins, new):
            self.assertGreaterEqual(width, minimum)

    def test_cost_label_and_ranges_never_break(self):
        self.assertIn("Cost (c)", nobreak("Cost (c)"))
        self.assertEqual([m.group(0) for m in RANGE.finditer("lasts 60–90 minutes (4–8 rounds)")], ["60–90", "4–8"])
        mins, _, _ = tables.measure_table(POTIONS)
        whole = tables.seg_width("Cost (c)", False, False, header=True)
        self.assertGreaterEqual(mins[2], whole - 0.01)


class RunInGlue(unittest.TestCase):
    def test_label_merged_with_its_list_does_not_glue_the_next_piece(self):
        book = Book.__new__(Book)
        book.logged_units, book.unit_log, book.measures = set(), [], {}
        node = {"id": "n", "head": {"s": "HEAD"}, "children": [
            {"typ": "para", "s": "#runin[A]", "kind": "c", "id": "a", "b": {}},
            {"typ": "list", "s": "#runin[B]#keep[x]", "kind": "c", "id": "b", "b": {}},
            {"typ": "list", "s": "#runin[C]#keep[y]", "kind": "c", "id": "c", "b": {}},
        ]}
        parts = book.flat_parts(node)
        self.assertEqual(parts, [("c", ["HEAD#runin[A]#runin[B]#keep[x]", "#runin[C]#keep[y]"])])


class BalanceTails(unittest.TestCase):
    def emit(self, pieces, tail):
        from build_book import segment_signature
        book = Book.__new__(Book)
        book.seg_count, book.seg_sigs = 0, {}
        book.balance = {"0": [segment_signature(pieces), tail]}
        book.block_map, book.piece_heads, book.bare_heads, book.out = [], {}, set(), []
        book.flush(pieces)
        return book, "".join(book.out)

    def test_complete_heading_units_stay_separate_tail_pieces(self):
        head = lambda i: {"id": f"h{i}", "type": "heading", "src": [i, i]}
        pieces = [({"id": "p", "type": "para", "src": [0, 0]}, "Intro."),
                  (head(1), "#keepcol[#heading[One] Body one.]\n"),
                  (head(2), "#keepcol[#heading[Two] Body two.]\n"),
                  (head(3), "#keepcol[#heading[Three] Body three.]\n")]
        book, out = self.emit(pieces, 2)
        self.assertEqual(book.bare_heads, set())
        self.assertIn("#bal([#keepcol[#heading[Two]", out)
        self.assertIn("], [#keepcol[#heading[Three]", out)

    def test_bare_heading_still_travels_with_its_next_piece(self):
        pieces = [({"id": "p", "type": "para", "src": [0, 0]}, "Intro."),
                  ({"id": "h", "type": "heading", "src": [1, 1]}, "#heading[Bare]"),
                  ({"id": "q", "type": "para", "src": [2, 2]}, "#keepcol[Body.]"),
                  ({"id": "r", "type": "para", "src": [3, 3]}, "#keepcol[More.]")]
        book, out = self.emit(pieces, 1)
        self.assertEqual(book.bare_heads, {"0:1"})
        self.assertIn("#bal([#heading[Bare]#keepcol[#pm(0, 2, \"s\")Body.]], [#keepcol[", out)

    def test_bare_runin_label_travels_with_its_next_piece(self):
        # candidate 20261102T174706Z, p. 446: "AI Steps" closed the flowing run, its content opened the tail
        pieces = [({"id": "p", "type": "para", "src": [0, 0]}, "Intro."),
                  ({"id": "l", "type": "para", "src": [1, 1]}, "#runin[#strong[AI Steps]]\n"),
                  ({"id": "q", "type": "para", "src": [2, 2]}, "#keepcol[Target Priority.]"),
                  ({"id": "r", "type": "para", "src": [3, 3]}, "#keepcol[More.]")]
        book, out = self.emit(pieces, 1)
        self.assertEqual(book.bare_heads, {"0:1"})
        first_piece = out.split("#bal([", 1)[1].split("], [", 1)[0]
        self.assertIn("AI Steps", first_piece)
        self.assertIn("Target Priority.", first_piece)

    def test_label_merged_with_its_list_stays_a_whole_piece(self):
        pieces = [({"id": "p", "type": "para", "src": [0, 0]}, "Intro."),
                  ({"id": "a", "type": "list", "src": [1, 1]}, "#runin[#strong[Attacks]]\n#list([Bite.])"),
                  ({"id": "q", "type": "para", "src": [2, 2]}, "#keepcol[Body.]")]
        book, _ = self.emit(pieces, 1)
        self.assertEqual(book.bare_heads, set())

    def test_single_whole_unit_tail_stays_in_the_segment_flow(self):
        head = lambda i: {"id": f"h{i}", "type": "heading", "src": [i, i]}
        pieces = [(head(1), "#keepcol[#heading[One] Body one.]\n"),
                  (head(2), "#keepcol[#heading[Two] Body two.]\n")]
        _, out = self.emit(pieces, 1)
        self.assertNotIn("#bal(", out)
        self.assertEqual(out.count("#seg["), 1)
        self.assertIn("Body two.]\n#place(pm(0, 2, \"e\"))]", out)
        # the parent's zero-size end marker does not count as a second piece
        marked = pieces + [({"id": "n:end", "type": "marker", "src": [3, 3]}, '#umark("n", "e")')]
        _, out = self.emit(marked, 1)
        self.assertNotIn("#bal(", out)
        self.assertEqual(out.count("#seg["), 1)

    def test_short_balanced_last_page_pulls_back_the_previous_piece(self):
        from build_book import compute_balance, BODY_BOTTOM
        pm = [{"seg": 1, "piece": 0, "edge": "s", "page": 1, "x": 42, "y": 45},
              {"seg": 1, "piece": 1, "edge": "s", "page": 1, "x": 316, "y": BODY_BOTTOM - 150},
              {"seg": 1, "piece": 2, "edge": "s", "page": 2, "x": 42, "y": 45},
              {"seg": 1, "piece": 3, "edge": "s", "page": 2, "x": 316, "y": 45},
              {"seg": 1, "piece": 4, "edge": "e", "page": 2, "x": 316, "y": 75}]
        sig = "v2:" + "a" * 64
        self.assertEqual(compute_balance(pm, {"1": [sig, 2]}, {"1": sig}), {"1": [sig, 1]})
        # a balanced tail of normal length keeps its start
        pm[-1]["y"] = 400
        self.assertEqual(compute_balance(pm, {"1": [sig, 2]}, {"1": sig}), {"1": [sig, 2]})

    def test_table_too_tall_to_share_a_column_with_its_heading_splits_under_it(self):
        book = Book.__new__(Book)
        table = {"id": "T", "kind": "c", "typ": "table"}
        book.measures = {"T": {"h1": 686.0}}
        self.assertTrue(book.splits_under_heading([table]))
        book.measures = {"T": {"h1": 600.0}}
        self.assertFalse(book.splits_under_heading([table]))
        book.measures = {"T": {"h1": 720.0}}
        self.assertFalse(book.splits_under_heading([table]))

    def test_refining_tail_is_not_mistaken_for_oscillation(self):
        from build_book import stabilize_balance
        flips, excluded, plan = {}, set(), {}
        for tail in (6, 5, 4):
            proposed = {"9": ["sig", tail]}
            self.assertEqual(stabilize_balance(proposed, plan, flips, excluded), proposed)
            plan = proposed
        self.assertEqual(excluded, set())
        self.assertEqual(stabilize_balance({"9": ["sig", 5]}, plan, flips, excluded), {})
        self.assertEqual(excluded, {"9"})

    def test_walk_back_skips_only_bare_headings(self):
        from build_book import compute_balance
        pm = [{"seg": 1, "piece": 0, "edge": "s", "page": 1, "x": 42, "y": 45},
              {"seg": 1, "piece": 3, "edge": "e", "page": 2, "x": 42, "y": 500}]
        hpos = [{"id": "a", "page": 1, "x": 315, "y": 45}, {"id": "b", "page": 2, "x": 42, "y": 45}]
        heads = {"1:1": "a", "1:2": "b"}
        self.assertEqual(compute_balance(pm, {}, {"1": "sig"}, heads, hpos, set()), {"1": ["sig", 2]})
        self.assertEqual(compute_balance(pm, {}, {"1": "sig"}, heads, hpos, {"1:1"}), {"1": ["sig", 1]})


class ProfileOpenings(unittest.TestCase):
    def test_identification_lines_are_recognised(self):
        from build_book import is_statline
        line = lambda text: {"typ": "para", "kind": "c", "b": {"type": "para", "c": [{"t": "text", "v": text}]}}
        self.assertTrue(is_statline(line("HP: 13 | AD: d2 (Chest) | SPD: 5\" | AP: 3")))
        self.assertFalse(is_statline(line("A plain sentence without fields.")))
        self.assertFalse(is_statline({"head": {}, "typ": "para", "kind": "c"}))


class TypstComponents(unittest.TestCase):
    def rows(self, n):
        return ", ".join(f'([{i}], [Row {i}])' for i in range(n))

    def test_long_table_keeps_three_rows_at_each_break(self):
        for filler in (560, 600, 640, 120, 200):
            pdf = compile_fixture(f'''#import "/typst/heraldry.typ": *
#show: book
#block(height: {filler}pt)
#htable("ROWS", (60, 465), (left, left), ([N], [Label]), ({self.rows(52)},), title: [Ledger])
''')
            with pymupdf.open(stream=pdf, filetype="pdf") as doc:
                counts = [sum(1 for w in page.get_text("words") if w[4] == "Row") for page in doc]
            counts = [c for c in counts if c]
            self.assertEqual(sum(counts), 52)
            self.assertTrue(all(c >= 3 for c in counts), (filler, counts))

    def test_hidden_duplicate_title_leaves_no_blank_line(self):
        pdf = compile_fixture('''#import "/typst/heraldry.typ": *
#show: book
#heading(level: 3)[Tier 3 Potions] <h-t3>
#htable("T3", (60, 465), (left, left), ([N], [Row]), (([1], [One]), ([2], [Two])), title: [Tier 3 Potions], initial-title: false)
''')
        with pymupdf.open(stream=pdf, filetype="pdf") as doc:
            page = doc[0]
            heading = next(s for b in page.get_text("dict")["blocks"] for l in b.get("lines", [])
                           for s in l["spans"] if s["text"] == "Tier 3 Potions")
            band = min(d["rect"].y0 for d in page.get_drawings()
                       if d["type"] == "f" and d["rect"].width > 50 and 5 < d["rect"].height < 30)
        self.assertLessEqual(band - heading["bbox"][3], 10)   # was about 17 pt with the hidden row
        self.assertGreaterEqual(band - heading["bbox"][3], 2)

    def test_card_table_hides_a_title_its_heading_already_names(self):
        def gap(initial):
            pdf = compile_fixture(f'''#import "/typst/heraldry.typ": *
#show: book
#heading(level: 3)[Tier 3 Potions] <h-t3>
#cards("T3", ((title: [#strong[Elixir]], fields: (([Cost], [5]),), desc: (([Rule:], [Heal 1.]),)),), title-label: [Tier 3 Potions], initial-title: {initial})
''')
            with pymupdf.open(stream=pdf, filetype="pdf") as doc:
                page = doc[0]
                spans = [s for b in page.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"]]
                titles = [s for s in spans if s["text"] == "Tier 3 Potions"]
                entry = next(s for s in spans if s["text"] == "Elixir")
            return len(titles), entry["bbox"][1] - titles[0]["bbox"][3]
        shown, shown_gap = gap("true")
        hidden, hidden_gap = gap("false")
        self.assertEqual((shown, hidden), (2, 1))           # heading and identity line, then the heading alone
        self.assertLess(hidden_gap, shown_gap - 8)          # the entries rise by the hidden line
        self.assertGreaterEqual(hidden_gap, 2)


if __name__ == "__main__":
    unittest.main()
