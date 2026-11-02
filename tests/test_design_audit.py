"""Design audit implementation (owner approval 2026-11-01): composition policy, text-layer mappings, tooling."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

import pymupdf
import typst

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_book import Book, SECTION_HEADS_FULL, OPENER_SHARE_FREE, RUN_ON_CHAPTERS  # noqa: E402
from layout_diagnostics import page_diagnostics  # noqa: E402

TOKENS = json.loads((ROOT / "config/design_tokens.json").read_text(encoding="utf-8"))


def compile_fixture(source, substrate="cream"):
    # Typst refuses a file outside its root, and a fresh CI checkout has no build/ yet.
    (ROOT / "build").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=ROOT / "build") as tmp:
        path = Path(tmp) / "fixture.typ"
        path.write_text(source, encoding="utf-8")
        compiler = typst.Compiler(str(path), root=str(ROOT), font_paths=[str(ROOT / "fonts/static")],
                                  ignore_system_fonts=True, sys_inputs={"substrate": substrate, "edition": "print"})
        pdf, warnings = compiler.compile_with_warnings()
        return pdf, [str(w) for w in warnings]


def spans(page):
    return [s for b in page.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"] if s["text"].strip()]


class CompositionPolicy(unittest.TestCase):
    def test_tokens_record_the_approved_policy(self):
        layout = TOKENS["layout"]
        self.assertTrue(layout["section_heads_full_width"])
        self.assertEqual(layout["opener_share_free_fraction"], 0.35)
        self.assertIn("h-appendix-c-rules-reference", layout["run_on_chapters"])
        self.assertEqual((TOKENS["type_pt"]["subsection"], TOKENS["type_pt"]["minor"]), (13, 13))
        self.assertGreaterEqual(TOKENS["type_pt"]["tag"], TOKENS["type_pt"]["minimum_essential"])
        self.assertTrue(SECTION_HEADS_FULL)
        self.assertEqual(OPENER_SHARE_FREE, 0.35)
        self.assertIn("h-appendix-c-rules-reference", RUN_ON_CHAPTERS)

    def test_section_head_is_a_full_width_part_and_subsections_stay_in_columns(self):
        book = Book.__new__(Book)
        book.measurable = lambda x: False
        book.log_unit = lambda *_: None
        section = {"level": 3, "id": "h-21", "head": {"id": "h-21", "b": {"level": 3}, "s": "#heading(level: 2)[2.1 Core Terms]"},
                   "children": [{"id": "p1", "kind": "c", "typ": "para", "s": "A paragraph.\n\n", "b": {}}]}
        parts = book.flat_parts(section)
        self.assertEqual(parts[0][0], "f")
        self.assertIn("2.1 Core Terms", parts[0][1][0])
        self.assertEqual(parts[1][0], "c")
        subsection = {"level": 4, "id": "h-211", "head": {"id": "h-211", "b": {"level": 4}, "s": "#heading(level: 3)[2.1.1 A target]"},
                      "children": [{"id": "p2", "kind": "c", "typ": "para", "s": "Text.\n\n", "b": {}}]}
        self.assertEqual(book.flat_parts(subsection)[0][0], "c")

    def test_reference_appendix_sections_run_on(self):
        book = Book.__new__(Book)
        self.assertTrue(book.is_fresh({"level": 3, "title": "2.1 Core Terms"}))
        book.run_on = True
        self.assertFalse(book.is_fresh({"level": 3, "title": "C.2 Core Terms and Abbreviations"}))
        self.assertTrue(book.is_fresh({"level": 5, "title": "Scenario 1: Hunt the Wild Beast [Intro]"}))

    def test_first_section_shares_the_opener_page_only_from_measured_room(self):
        book = Book.__new__(Book)
        book.out, book.block_map = [], []
        book.flush = lambda _: None
        book.record = lambda *_: None
        book.log_unit = lambda *_: None
        book.end_art = {}
        book.run_on = False
        first = {"level": 3, "id": "h-11"}
        # No measurement: never share. Enough room and a page-fit section that fits: share.
        book.measures = {}
        self.assertFalse(book.opener_shares("opener:h-1", first))
        book.measures = {"opener:h-1": {"h1": 1e9, "h2": 300.0}, "h-11": {"h1": 500.0, "h2": 320.0}}
        self.assertTrue(book.opener_shares("opener:h-1", first))
        book.measures["h-11"]["h2"] = 420.0                 # the section no longer fits beside the opener
        self.assertFalse(book.opener_shares("opener:h-1", first))
        book.measures["opener:h-1"]["h2"] = 480.0           # the opener leaves less than 35% of the frame
        book.measures["h-11"]["h2"] = 100.0
        self.assertFalse(book.opener_shares("opener:h-1", first))
        book.run_on = True                                   # run-on chapters never need the rule
        book.measures["opener:h-1"]["h2"] = 100.0
        self.assertFalse(book.opener_shares("opener:h-1", first))
        # The emitted break follows the decision; the section head is a full-width block either way.
        book.run_on = False
        head = {"id": "h-11", "b": {"level": 3, "src": [1, 1], "title": "1.1 What is Heraldry Skirmish?"}, "s": "#heading(level: 2)[1.1 What is Heraldry Skirmish?]"}
        node = {"level": 3, "id": "h-11", "head": head, "children": [], "title": "1.1 What is Heraldry Skirmish?"}
        for share, expected in ((True, False), (False, True)):
            book.out, book.first_section_pending, book.share_opener, book.flow_next_flush = [], True, share, False
            book.emit_x(node, [], False)
            out = "".join(book.out)
            self.assertEqual("#pagebreak(weak: true)" in out, expected)
            self.assertEqual(book.flow_next_flush, share)      # a shared first section opens in natural flow
            # the head spans the frame: a page-fit unit carries it as its first full-width part,
            # an over-height section emits it in the outer flow
            self.assertTrue("#section-head[" in out or '("f", [#heading(level: 2)' in out, out)
            self.assertFalse(book.first_section_pending)

    def test_table_identity_is_hidden_behind_a_short_run_in_label(self):
        book = Book.__new__(Book)
        book.block_map, book.table_titles = [], {"T1": "The Mire Random Monster Table"}
        book.table = lambda b, initial_title=True, force_column=False: (f"#htable(initial-title: {str(initial_title).lower()})", "column")
        book.para = lambda b, role=None: "#runin[APL 1–2 (d10)]\n"
        book.render = lambda b: "#heading[The Mire Random Monster Table]\n" if b["type"] == "heading" else book.para(b)
        book.figs_for = lambda b: []
        book.tags = lambda bid: ""
        book.contained = lambda b, s: s
        items = book.chapter_items([
            {"id": "h", "type": "heading", "title": "The Mire Random Monster Table", "level": 4},
            {"id": "lab", "type": "para", "src": [1, 1], "c": [{"t": "strong", "c": [{"t": "text", "v": "APL 1–2 (d10)"}]}]},
            {"id": "T1", "type": "table", "src": [1, 2], "header": [], "rows": [], "align": []},
        ])
        self.assertIn("initial-title: false", items[-1]["s"])


    def test_run_on_section_opens_as_a_sticky_band_and_standfirst_when_its_first_piece_can_follow(self):
        book = Book.__new__(Book)
        book.block_map, book.end_art = [], {}
        book.flush = lambda _: None
        book.record = lambda *_: None
        book.log_unit = lambda *_: None
        book.run_on, book.first_section_pending, book.share_opener = True, False, False
        head = {"id": "h-c11", "b": {"level": 3, "src": [1, 1], "title": "C.11 Glossary"}, "s": "#heading(level: 2)[C.11 Glossary]"}
        intro = {"id": "p1", "kind": "c", "typ": "para", "s": "#keep[Short introduction.]\n", "b": {"src": [2, 2], "c": [{"t": "text", "v": "Short introduction."}]}}
        table = {"id": "T1", "kind": "c", "typ": "table", "s": "#htable(...)\n", "b": {"src": [3, 4]}}
        prose = {"id": "p2", "kind": "c", "typ": "para", "s": "Flowing prose.\n\n", "b": {"src": [5, 5]}}
        def emit(children, measures):
            book.measures = measures
            book.out = []
            book.emit_x({"level": 3, "id": "h-c11", "head": head, "children": list(children), "title": "C.11 Glossary"}, [], False)
            return "".join(book.out)
        out = emit([intro, table], {"T1": {"h1": 200.0, "h2": 200.0}})      # a short unit follows: runs on
        self.assertIn("#full-opening(sticky: true)[", out)
        self.assertIn("#chapter-intro[Short introduction.]", out)
        self.assertNotIn("#pagebreak", out)
        out = emit([intro, prose], {})                                      # prose follows: runs on
        self.assertNotIn("#pagebreak", out)
        self.assertIn("#full-opening(sticky: true)[", out)
        out = emit([intro, table], {"T1": {"h1": 500.0, "h2": 500.0}})      # a tall unit follows: fresh page, same opening
        self.assertIn("#pagebreak(weak: true)", out)
        self.assertIn("#full-opening(sticky: true)[", out)
        out = emit([table], {"T1": {"h1": 200.0, "h2": 200.0}})             # no introduction: fresh page, band only
        self.assertIn("#pagebreak(weak: true)", out)
        self.assertIn("#section-head[", out)
        self.assertNotIn("#full-opening", out)
        book.run_on = False                                                  # an ordinary chapter keeps the sticky head in the flow
        out = emit([intro, table], {"T1": {"h1": 200.0, "h2": 200.0}})
        self.assertIn("#section-head[", out)
        self.assertNotIn("#full-opening", out)

    def test_shared_opener_segment_ignores_the_balance_plan_once(self):
        book = Book.__new__(Book)
        book.out, book.block_map, book.seg_count, book.seg_sigs = [], [], 0, {}
        book.piece_heads, book.bare_heads = {}, set()
        pieces = [({"type": "para", "id": f"p{i}", "src": [i, i]}, f"Paragraph {i}.\n\n") for i in range(4)]
        from build_book import segment_signature
        plan = {"0": [segment_signature(pieces), 2], "1": [segment_signature(pieces), 2]}
        book.balance, book.flow_next_flush = plan, True
        book.flush(list(pieces))
        self.assertTrue(book.out[-1].startswith("#seg["))          # the plan is set aside for this segment
        self.assertFalse(book.flow_next_flush)
        book.flush(list(pieces))
        self.assertTrue(book.out[-1].startswith("#flowtail(") or "#flowtail(" in book.out[-1])   # later segments balance again

    def test_marker_only_tail_is_emitted_raw_so_it_cannot_open_a_blank_page(self):
        book = Book.__new__(Book)
        book.out, book.block_map, book.seg_count, book.seg_sigs, book.balance = [], [], 0, {}, {}
        book.piece_heads, book.bare_heads = {}, set()
        marker = ({"type": "marker", "id": "h-x:end", "src": [1, 2]}, '#umark("h-x", "e")')
        book.flush([marker])
        self.assertEqual(book.out, ['#umark("h-x", "e")\n'])
        self.assertEqual(book.seg_count, 0)
        book.out = []
        book.flush([({"type": "para", "id": "p", "src": [1, 1]}, "Text.\n\n"), marker])
        self.assertTrue(book.out[0].startswith("#seg["))


class TextLayerMappings(unittest.TestCase):
    def test_role_tag_and_chapter_label_keep_the_source_text(self):
        pdf, warnings = compile_fixture('''#import "/typst/heraldry.typ": *
#show: book
#chapter-opener([#"1."], [#"The World of Heraldry"], "h-1", lead: none, art: none)
#intro-end(solo: true)
#heading(level: 3)[Berserker [2/5 Complexity]] <h-b>
Text.
#heading(level: 4)[Frost Giant [Elite]] <h-fg>
Text.
''')
        self.assertFalse(warnings, warnings)
        with pymupdf.open(stream=pdf, filetype="pdf") as doc:
            text = " ".join(page.get_text() for page in doc).replace("\n", " ")
            for expected in ("Chapter One", "1. The World of Heraldry", "Berserker [2/5 Complexity]", "Frost Giant [Elite]"):
                self.assertIn(expected, text)
            sizes = [s["size"] for page in doc for s in spans(page)]
            self.assertGreaterEqual(min(sizes), 9)                 # transparent glyphs never fall below the floor
            tags = [s for page in doc for s in spans(page) if s["text"] in ("Elite", "2/5 Complexity")]
            self.assertEqual(len(tags), 2)
            self.assertTrue(all("SourceSans" in s["font"] for s in tags))

    def test_source_rules_set_as_quiet_separators_without_the_castle_mark(self):
        pdf, warnings = compile_fixture('''#import "/typst/heraldry.typ": *
#show: book
#seg[
  #lorem(20)
  #hr-ornament()
  #lorem(20)
  #hr-ornament()
  #lorem(20)
  #hr-ornament()
  #lorem(20)
]
''')
        self.assertFalse(warnings, warnings)
        with pymupdf.open(stream=pdf, filetype="pdf") as doc:
            page = doc[0]
            self.assertEqual([im for im in page.get_image_info() if im["bbox"][1] > 45], [])   # no castle mark in the body
            rules = [d for d in page.get_drawings() if d["type"] == "s" and 30 < d["rect"].width < 70 and d["rect"].y0 > 45]
            self.assertGreaterEqual(len(rules), 6)                 # two short hairlines per separator

    def test_reference_band_heads_the_appendix_sections(self):
        pdf, warnings = compile_fixture('''#import "/typst/heraldry.typ": *
#show: book
#section-head[#heading(level: 2)[C.3 Conditions Summary] <h-c3>]
#seg[#lorem(30)]
''')
        self.assertFalse(warnings, warnings)
        with pymupdf.open(stream=pdf, filetype="pdf") as doc:
            page = doc[0]
            text = page.get_text()
            self.assertIn("C.3 Conditions Summary", text.replace("\n", " "))
            self.assertIn("RulesReference", text.replace(" ", "").replace("\n", ""))   # tracked label; extraction may space letters
            band = [d for d in page.get_drawings() if d["type"] == "f" and d["rect"].width > 500 and 20 < d["rect"].height < 50]
            self.assertEqual(len(band), 1)

    def test_tailpiece_grows_to_the_gap_and_sits_at_the_foot(self):
        art = ROOT / "assets/art/ink/ART-END-TERRAIN.png"
        if not art.is_file() or art.read_bytes()[:7] == b"version":
            self.skipTest("tailpiece ink needs Git LFS bytes")
        from PIL import Image
        with Image.open(art) as image:
            aspect = image.size[1] / image.size[0]
        pdf, warnings = compile_fixture(f'''#import "/typst/heraldry.typ": *
#show: book
#seg[#lorem(40)]
#endart("ART-END-TERRAIN", "/assets/art/ink/ART-END-TERRAIN.png", 237.6pt, {aspect:.4f}, max-w: 331.2pt)
#pagebreak()
#heading(level: 2)[2.10 Luck Points] <h-next>
''')
        self.assertFalse(warnings, warnings)
        with pymupdf.open(stream=pdf, filetype="pdf") as doc:
            images = doc[0].get_image_info()
            self.assertEqual(len(images), 1)
            box = pymupdf.Rect(images[0]["bbox"])
            self.assertAlmostEqual(box.width, 331.2, delta=1.5)          # grew to the cap, not the family width
            self.assertGreater(box.y1, 792 - 45 - 12)                    # anchored at the foot of the frame
            self.assertLessEqual(box.y1, 792 - 45 + 0.5)


class Tooling(unittest.TestCase):
    def test_keep_audit_sets_opener_probes_aside_but_keeps_source_coverage_strict(self):
        import keep_audit
        rows = {"B00010": {"h1": 1, "h2": 1}, "opener:h-1": {"h1": 1e9, "h2": 300}}
        self.assertEqual(keep_audit.composition_probes(rows), ["opener:h-1"])
        self.assertEqual(set(rows) - set(keep_audit.composition_probes(rows)), {"B00010"})

    def test_density_metric_ignores_the_thumb_tab(self):
        with pymupdf.open() as doc:
            page = doc.new_page(width=612, height=792)
            page.insert_text((60, 100), "Rules text", fontsize=10.5)
            shape = page.new_shape()
            shape.draw_rect(pymupdf.Rect(573, 400, 612, 460))        # a pennant in the outer strip
            shape.finish(fill=(0, 0, 0))
            shape.commit()
            result = page_diagnostics(page, 1, top=45, bottom=747, tab=30.24)
        self.assertGreater(result["bottom_empty_band_pt"], 600)
        self.assertTrue(result["sparse"])

    def test_digital_compact_downsamples_and_keeps_navigation(self):
        import digital_compact
        with tempfile.TemporaryDirectory() as tmp:
            src, dst = Path(tmp) / "digital.pdf", Path(tmp) / "compact.pdf"
            with pymupdf.open() as doc:
                page = doc.new_page(width=612, height=792)
                pix = pymupdf.Pixmap(pymupdf.csGRAY, pymupdf.IRect(0, 0, 1200, 800), False)
                pix.clear_with(200)
                page.insert_image(pymupdf.Rect(100, 100, 388, 292), pixmap=pix)   # 4 in wide: 300 ppi
                page.insert_text((72, 600), "Linked text", fontsize=10)
                page.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(72, 590, 200, 605), "uri": "https://example.invalid"})
                doc.new_page(width=612, height=792)
                doc.set_toc([[1, "Chapter", 1], [1, "Next", 2]])
                doc.save(src)
            with contextlib.redirect_stdout(io.StringIO()):
                report = digital_compact.compact(src, dst, ppi=150)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["images_downsampled"], 1)
            self.assertLessEqual(report["after"]["lowest_ppi"], 160)
            self.assertEqual(report["after"]["toc"], 2)
            self.assertEqual(report["after"]["links"], 1)
            self.assertLess(report["after"]["bytes"], report["before"]["bytes"])


if __name__ == "__main__":
    unittest.main()
