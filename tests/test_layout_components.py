"""Render compact components and inspect their actual serialized geometry."""
import json
import re
from pathlib import Path
import sys
import tempfile
import unittest

import pymupdf
from pypdf import PdfReader
import typst

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import layout_profile as profile


class CompactComponents(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        scratch = ROOT / "build/checks/layout-v5/components"
        scratch.mkdir(parents=True, exist_ok=True)
        cls.tmp = tempfile.TemporaryDirectory(dir=scratch)
        cls.path = Path(cls.tmp.name) / "components.typ"
        cls.path.write_text('''#import "/typst/heraldry.typ": *
#show: book
#heading(level: 2)[Component proof] <h-proof>
#section-lead[Opening flavour uses a single quiet measure.]
#seg[Rules remain in two columns. A Hero refreshes to *3 AP* at the start of each round.

This second paragraph checks the compact rhythm without removing rules.]
#htable("ALIGN", (260,265), (left,right), ([Name],[Value]), (([First],[1]),([Second],[12]),([Third],[123])), title:[Alignment Ledger])
#statstrip("STRIP",([HP],[AV]),([12],[3]),pre:metadata("strip-pre"))
#statcard("CARD",([HP],[AV]),([12],[3]),pre:metadata("card-pre"))
#figure-block("FIG-PROOF", "/figures/out/FIG-01.svg", [Caption marker proof.], width:150pt)
#pagebreak()
#htable("LONG", (260,265), (left,right), ([Name],[Value]), range(95).map(i=>([Row #i],[#i])),title:[Long Ledger])
#cards("CARDS",range(28).map(i=>(title:[Card #i],fields:(([Cost],[1 AP]),),desc:(([Rules],[This entry retains a complete description and a useful identity across the continuation.]),))),title-label:[Entry Ledger])
#hpos-summary()
''', encoding="utf-8")
        compiler = typst.Compiler(str(cls.path), root=str(ROOT),
                                font_paths=[str(ROOT / "fonts/static")],
                                ignore_system_fonts=True,
                                sys_inputs={"position-identity": "{}"})
        cls.pdf, warnings = compiler.compile_with_warnings()
        if warnings:
            raise AssertionError("Component fixture must converge without warnings: " + str(warnings))
        cls.reader = PdfReader(__import__("io").BytesIO(cls.pdf))
        cls.doc = pymupdf.open(stream=cls.pdf, filetype="pdf")
        key = next(k for k in cls.reader.attachments if k.endswith("heraldry-positions.json"))
        cls.positions = json.loads(cls.reader.attachments[key][0])["positions"]
        furniture = Path(cls.tmp.name) / "furniture.typ"
        furniture.write_text('''#import "/typst/heraldry.typ": *
#import "/typst/templates/system.typ": thumb-tab
#show: book
#set page(background:context thumb-tab(here().page(),calc.odd(here().page())))
#metadata(none) <mainmatter>
#heading(level:1)[Compact Header] <h-furniture>
#for i in range(15) {
  if i>0 { pagebreak() }
  heading(level:2)[Furniture proof]
  [Rules text begins at its safe body frame.]
}
#hpos-summary()
''', encoding="utf-8")
        compiler = typst.Compiler(str(furniture), root=str(ROOT),
                                          font_paths=[str(ROOT / "fonts/static")],
                                          ignore_system_fonts=True)
        cls.furniture_pdf, warnings = compiler.compile_with_warnings()
        if warnings:
            raise AssertionError("Furniture fixture must converge without warnings: " + str(warnings))

    @classmethod
    def tearDownClass(cls):
        cls.doc.close()
        cls.tmp.cleanup()

    def test_effective_profile_and_typst_geometry_agree(self):
        self.assertTrue(profile.validate())
        self.assertEqual((profile.BODY_SIZE_PT, profile.TABLE_SIZE_PT), (10.5, 9))
        self.assertEqual((profile.FRAME_WIDTH_PT, profile.BODY_HEIGHT_PT), (525, 702))
        self.assertAlmostEqual(profile.COLUMN_WIDTH_PT, 254.4)
        spans = [s for b in self.doc[0].get_text("dict")["blocks"]
                 for line in b.get("lines", []) for s in line["spans"]]
        rules = next(s for s in spans if "Rules remain" in s["text"])
        table = next(s for s in spans if s["text"] == "First")
        self.assertEqual(rules["size"], 10.5)
        self.assertEqual(table["size"], 9)

    def test_numeric_right_edges_align_in_serialized_pdf(self):
        words = self.doc[0].get_text("words")
        row_y = {w[4]: w[1] for w in words if w[4] in {"First", "Second", "Third"}}
        right_edges = [next(w[2] for w in words if w[4] == value and abs(w[1] - row_y[label]) < 1)
                       for label, value in (("First", "1"), ("Second", "12"), ("Third", "123"))]
        self.assertLess(max(right_edges) - min(right_edges), 0.02)

    def test_table_identity_has_no_ornamental_strike_through(self):
        spans = [s for b in self.doc[0].get_text("dict")["blocks"]
                 for line in b.get("lines", []) for s in line["spans"]]
        title = pymupdf.Rect(next(s["bbox"] for s in spans if s["text"] == "Alignment Ledger"))
        for drawing in self.doc[0].get_drawings():
            bounds = drawing["rect"]
            if bounds.width > profile.FRAME_WIDTH_PT * 0.9 and bounds.height <= 5:
                self.assertFalse(bounds.intersects(title), "Table identity overlaps a decorative rule")

    def test_table_and_card_continuations_keep_their_names(self):
        texts = [page.extract_text() for page in self.reader.pages]
        long_pages = [t for t in texts if re.search(r'(?m)^Row \d+', t)]
        self.assertGreater(len(long_pages), 1)
        self.assertNotIn("Long Ledger (continued)", long_pages[0])
        for text in long_pages[1:]:
            self.assertIn("Long Ledger (continued)", text)
        self.assertTrue(any("Entry Ledger (continued)" in t for t in texts))
        for row in range(95):
            self.assertEqual(sum(len(re.findall(rf"(?m)^Row {row}(?=\s)", t)) for t in texts), 1)

    def test_stat_and_figure_markers_enclose_real_objects(self):
        markers = self.positions["<tblpos>"]
        for name in ("STRIP", "CARD", "FIG-PROOF"):
            pair = [m for m in markers if m["id"] == name]
            self.assertEqual([m["edge"] for m in pair], ["s", "e"])
            self.assertEqual(pair[0]["page"], pair[1]["page"])
            self.assertGreater(pair[1]["y"], pair[0]["y"])

    def test_essential_furniture_stays_inside_safe_edge(self):
        for page in self.doc:
            spans = [s for b in page.get_text("dict")["blocks"]
                     for line in b.get("lines", []) for s in line["spans"]]
            folio = [s for s in spans if s["text"] == str(page.number + 1) and s["bbox"][1] > 740]
            self.assertEqual(len(folio), 1)
            self.assertLessEqual(folio[0]["bbox"][3], 765)

    def test_no_fixed_prose_height_or_font_shrink(self):
        code = (ROOT / "typst/heraldry.typ").read_text(encoding="utf-8")
        self.assertIn("stacked / 2 + 2 * pitch + head-reserve", code)
        self.assertNotIn('/ 2 + 40pt', code)

    def test_all_rotated_keywords_and_running_heads_clear_safe_frame(self):
        with pymupdf.open(stream=self.furniture_pdf, filetype="pdf") as doc:
            self.assertEqual(len(doc), 15)
            flags = pymupdf.TEXTFLAGS_DICT | pymupdf.TEXT_ACCURATE_BBOXES
            for page in doc:
                # glyph ink: Grenze Gotisch's 1.1 em ascender metric is far taller than its letters
                spans = [s for b in page.get_text("dict", flags=flags)["blocks"]
                         for line in b.get("lines", []) for s in line["spans"] if s["text"].strip()]
                for span in spans:
                    x0, y0, x1, y1 = span["bbox"]
                    self.assertGreaterEqual(min(x0, y0), 27, span["text"])
                    self.assertLessEqual(x1, 585, span["text"])
                    self.assertLessEqual(y1, 765, span["text"])

    def test_navigation_never_shrinks_and_index_decoration_clears_folio(self):
        keywords = ("World", "Mechanics", "Round", "Actions", "Combat", "Party", "Equipment", "Powers",
                    "Monsters", "Scenarios", "Campaign", "Learn", "Basic", "Reference", "Index")
        with pymupdf.open(stream=self.furniture_pdf, filetype="pdf") as doc:
            for page, keyword in zip(doc, keywords):
                spans = [s for b in page.get_text("dict")["blocks"]
                         for line in b.get("lines", []) for s in line["spans"]]
                labels = [s for s in spans if s["text"] == keyword]
                self.assertEqual(len(labels), 1, keyword)
                self.assertEqual(labels[0]["size"], 9, keyword)
            shapes = [d["rect"] for d in doc[-1].get_drawings() if d["type"] == "f"]
            tab_w = profile.MARGIN_OUTSIDE_PT - profile.TOKENS["page"]["thumb_tab_clearance_pt"]
            self.assertGreaterEqual(profile.TOKENS["page"]["thumb_tab_clearance_pt"], 3, "Tabs must clear the text frame")
            tab = next(r for r in shapes if abs(r.width - tab_w) < 0.1 and r.y0 > 680)
            folio = next(r for r in shapes if abs(r.width - 23) < 0.1 and r.y0 > 740)
            self.assertLessEqual(tab.y1, profile.PAGE_HEIGHT_PT - profile.MARGIN_BOTTOM_PT - 12)
            self.assertGreaterEqual(folio.y0 - tab.y1, 12)

    def test_scenario_continuation_header_is_scoped_and_fits_at_nine_points(self):
        source = Path(self.tmp.name) / "scenario-header.typ"
        source.write_text('''#import "/typst/heraldry.typ": *
#show: book
#metadata(none) <mainmatter>
#heading(level:1)[Scenarios]
#heading-scope(2,"10.1 Climate","h-climate")[#heading(level:2)[#"10.1 Climate"] <h-climate>]
#heading-scope(4,"Scenario 1: A deliberately long scenario name with many words that must fit the running header without shrinking essential navigation text","h-scenario")[#heading(level:4)[Scenario 1: A deliberately long scenario name with many words that must fit the running header without shrinking essential navigation text] <h-scenario>]
Opening rules.
#pagebreak()
Continuation rules.
#pagebreak()
#heading-scope(3,"Following section","h-following")[#heading(level:3)[Following section] <h-following>]
Following rules.
#hpos-summary()
#context { pdf.attach("/scenario-scopes.json",bytes(json.encode(query(<scenario-boundary>).map(m=>m.value)))) }
''', encoding="utf-8")
        compiler = typst.Compiler(str(source), root=str(ROOT),
                                  font_paths=[str(ROOT / "fonts/static")], ignore_system_fonts=True)
        pdf, warnings = compiler.compile_with_warnings()
        self.assertFalse(warnings, [str(w) for w in warnings])
        reader = PdfReader(__import__('io').BytesIO(pdf))
        events = json.loads(reader.attachments['scenario-scopes.json'][0])
        self.assertEqual([(e['rank'], e['page']) for e in events], [(2,1), (4,1), (3,3)],
                         'Running headers must not duplicate source boundary metadata')
        with pymupdf.open(stream=pdf, filetype='pdf') as doc:
            self.assertEqual(len(doc), 3)
            self.assertNotIn('(continued)', doc[0].get_text())
            self.assertIn('... (continued)', doc[1].get_text())
            self.assertNotIn('(continued)', doc[2].get_text())
            first = [s for b in doc[0].get_text('dict')['blocks'] for l in b.get('lines', [])
                     for s in l['spans'] if s['bbox'][1] >= profile.MARGIN_TOP_PT]
            self.assertTrue(any(s['text'] == '10.1' and 'SourceSans' in s['font'] for s in first),
                            'Scoped headings must retain their engraved section number')
            spans = [s for b in doc[1].get_text('dict')['blocks'] for l in b.get('lines', [])
                     for s in l['spans'] if s['bbox'][1] < profile.MARGIN_TOP_PT]
            title = next(s for s in spans if '(continued)' in s['text'])
            self.assertEqual(title['size'], 9)
            self.assertGreaterEqual(title['bbox'][0], 42)
            self.assertLessEqual(title['bbox'][2], 570)

    def test_table_identity_geometry_is_independent_of_queried_page(self):
        source = Path(self.tmp.name) / "identity-geometry.typ"
        source.write_text('''#import "/typst/heraldry.typ": *
#show: book
#context {
  let title = [A long ledger identity that wraps with its continuation suffix]
  let heights = (false, true).map(initial => (false, true).map(continued =>
    measure(block(width:100pt, table-identity("PROOF", title,
      initial-title:initial, continued:continued))).height.pt())).flatten()
  pdf.attach("/identity-heights.json",bytes(json.encode(heights)))
}
Geometry proof.
''', encoding="utf-8")
        compiler = typst.Compiler(str(source), root=str(ROOT),
                                  font_paths=[str(ROOT / "fonts/static")], ignore_system_fonts=True)
        pdf, warnings = compiler.compile_with_warnings()
        self.assertFalse(warnings, [str(w) for w in warnings])
        reader = PdfReader(__import__("io").BytesIO(pdf))
        heights = json.loads(reader.attachments['identity-heights.json'][0])
        self.assertGreater(min(heights), 9)
        self.assertLess(max(heights) - min(heights), 0.01)

    def test_suppressed_initial_table_identity_returns_on_continuation(self):
        source = Path(self.tmp.name) / "initial-table-identity.typ"
        source.write_text('''#import "/typst/heraldry.typ": *
#show: book
#heading(level:3)[Adjacent Ledger] <h-adjacent-ledger>
#htable("ADJACENT", (260,265), (left,right), ([Name],[Value]),
  range(95).map(i=>([Row #i],[#i])),title:[Adjacent Ledger],initial-title:false)
#hpos-summary()
''', encoding="utf-8")
        compiler = typst.Compiler(str(source), root=str(ROOT),
                                  font_paths=[str(ROOT / "fonts/static")], ignore_system_fonts=True)
        pdf, warnings = compiler.compile_with_warnings()
        self.assertFalse(warnings, [str(w) for w in warnings])
        reader = PdfReader(__import__("io").BytesIO(pdf))
        texts = [page.extract_text() for page in reader.pages]
        self.assertGreater(len(texts), 1)
        self.assertEqual(texts[0].count("Adjacent Ledger"), 1, "Only the actual source heading belongs on the opening page")
        self.assertTrue(all("Adjacent Ledger (continued)" in text for text in texts[1:]))
        for row in range(95):
            self.assertEqual(sum(len(re.findall(rf"(?m)^Row {row}(?=\s)", text)) for text in texts), 1)

    def test_figure_keep_adds_no_padding_and_survives_partial_column(self):
        source = Path(self.tmp.name) / "figure-keep.typ"
        source.write_text('''#import "/typst/heraldry.typ": *
#show: book
#context {
  let content = [#figure-block("MEASURE", "/figures/out/FIG-01.svg", [Figure caption proof.])]
  [#metadata((
    padded: measure(block(width:col-w,{rect(width:1pt,height:1pt);keepcol(content);rect(width:1pt,height:1pt)})).height.pt(),
    plain: measure(block(width:col-w,{rect(width:1pt,height:1pt);keepfigure(content);rect(width:1pt,height:1pt)})).height.pt(),
  )) <figure-height>]
}
#block(height:580pt)[Partial-page opening]
#seg[#keepfigure[#umark("figure-unit","s")
#figure-block("FIG-KEPT", "/figures/out/FIG-01.svg", [Figure caption proof.])
#umark("figure-unit","e")]]
#hpos-summary()
''', encoding="utf-8")
        compiler = typst.Compiler(str(source), root=str(ROOT),
                                  font_paths=[str(ROOT / "fonts/static")], ignore_system_fonts=True)
        pdf, warnings = compiler.compile_with_warnings()
        self.assertFalse(warnings, [str(w) for w in warnings])
        heights = json.loads(compiler.query("<figure-height>", field="value"))[0]
        # Existing adjacent block margins may already collapse in Typst. The
        # dedicated keep must never add height; it need not claim a fixed saving.
        self.assertLessEqual(heights["plain"], heights["padded"])
        reader = PdfReader(__import__("io").BytesIO(pdf))
        key = next(k for k in reader.attachments if k.endswith("heraldry-positions.json"))
        positions = json.loads(reader.attachments[key][0])["positions"]
        marks = [m for m in positions["<um-pos>"] if m["id"] == "figure-unit"]
        self.assertEqual([m["edge"] for m in marks], ["s", "e"])
        self.assertEqual(marks[0]["page"], marks[1]["page"])
        with pymupdf.open(stream=pdf, filetype="pdf") as doc:
            page = doc[marks[0]["page"] - 1]
            spans = [s for b in page.get_text("dict")["blocks"]
                     for line in b.get("lines", []) for s in line["spans"]]
            caption = next(s for s in spans if s["text"] == "Figure caption proof.")
            self.assertEqual(caption["size"], 9)
            self.assertLessEqual(max(s["bbox"][3] for s in spans), 765)

    def test_partial_column_keeps_converge_without_overflow_or_splits(self):
        source = Path(self.tmp.name) / "partial-keeps.typ"
        cases = [(200, 500), (500, 200), (650, 650), (550, 80), (400, 600)]
        content = ['#import "/typst/heraldry.typ": *\n#show: book\n']
        for number, (lead, height) in enumerate(cases):
            content.append(f'''#pagebreak(weak:true)
#block(height:{lead}pt)[Opening {number}]
#seg[#keepcol[#umark("case-{number}","s") Start {number}
#block(height:{height}pt)[Tall measured block]
End {number} #umark("case-{number}","e")]]
''')
        # This compact, variable-entry run reproduces the old here().y feedback loop.
        content.append('''#pagebreak()
#heading(level:3)[Synthetic opening]
#block(height:90pt)[Opening art]
#seg[#for i in range(45) { keepcol[
#heading(level:4)[Entry #i]
#list([A compact field.], [A longer explanatory field. #("A measured explanatory phrase. " * (1 + calc.rem(i,4)))])
] }]
#heading(level:3)[Following heading] <h-following>
#hpos-summary()
''')
        source.write_text("".join(content), encoding="utf-8")
        compiler = typst.Compiler(str(source), root=str(ROOT),
                                  font_paths=[str(ROOT / "fonts/static")], ignore_system_fonts=True)
        pdf, warnings = compiler.compile_with_warnings()
        self.assertFalse(warnings, [str(w) for w in warnings])
        reader = PdfReader(__import__("io").BytesIO(pdf))
        key = next(k for k in reader.attachments if k.endswith("heraldry-positions.json"))
        positions = json.loads(reader.attachments[key][0])["positions"]["<um-pos>"]
        for number in range(len(cases)):
            marks = [m for m in positions if m["id"] == f"case-{number}"]
            self.assertEqual([m["edge"] for m in marks], ["s", "e"])
            self.assertEqual(marks[0]["page"], marks[1]["page"])
        with pymupdf.open(stream=pdf, filetype="pdf") as doc:
            for page in doc:
                for block in page.get_text("dict")["blocks"]:
                    for line in block.get("lines", []):
                        for span in line["spans"]:
                            self.assertLessEqual(span["bbox"][3], 765, span["text"])

    def test_prose_flows_across_columns_without_loss_or_unsafe_overflow(self):
        source = Path(self.tmp.name) / "flow-prose.typ"
        # Single long paragraph, many short paragraphs, opening/internal headings,
        # and a partial-page start exercise line-level composition and its reserve.
        cases = [
            ('([#("word " * 450)],)', 450, 0),
            ('range(18).map(i => [#("word " * 15)#parbreak()])', 270, 0),
            ('([#heading(level:2)[Opening heading]#("word " * 200)],)', 200, 0),
            ('([#("word " * 120)], [#heading(level:2)[A deliberately long internal heading with several words]#("word " * 300)])', 420, 0),
            ('([#("word " * 300)],)', 300, 250),
            ('([#("word " * 600)],)', 600, 0),
        ]
        content = ['#import "/typst/heraldry.typ": *\n#show: book\n']
        for number, (pieces, _, lead) in enumerate(cases):
            content.append(f'''#pagebreak(weak:true)
''')
            if lead:
                content.append(f'#block(height:{lead}pt)[Partial-page opening]\n')
            content.append(f'#keeppage(id:"flow-{number}", ("p", {pieces}))\n')
        content.append('#hpos-summary()\n')
        source.write_text("".join(content), encoding="utf-8")
        compiler = typst.Compiler(str(source), root=str(ROOT),
                                  font_paths=[str(ROOT / "fonts/static")], ignore_system_fonts=True)
        pdf, warnings = compiler.compile_with_warnings()
        self.assertFalse(warnings, [str(w) for w in warnings])
        reader = PdfReader(__import__("io").BytesIO(pdf))
        key = next(k for k in reader.attachments if k.endswith("heraldry-positions.json"))
        positions = json.loads(reader.attachments[key][0])["positions"]["<um-pos>"]
        for number in range(len(cases)):
            marks = [m for m in positions if m["id"] == f"flow-{number}"]
            self.assertEqual([m["edge"] for m in marks], ["s", "e"])
            self.assertEqual(marks[0]["page"], marks[1]["page"])
        with pymupdf.open(stream=pdf, filetype="pdf") as doc:
            words = [word for page in doc for word in page.get_text("words")]
            self.assertEqual(sum(word[4] == "word" for word in words), sum(c[1] for c in cases))
            self.assertTrue(any(word[4] == "word" and word[0] > 310 for word in doc[0].get_text("words")))
            for page in doc:
                for block in page.get_text("dict")["blocks"]:
                    for line in block.get("lines", []):
                        for span in line["spans"]:
                            self.assertLessEqual(span["bbox"][3], 765, span["text"])

    def test_list_items_balance_as_complete_entries_with_native_height(self):
        source = Path(self.tmp.name) / 'list-fit.typ'
        source.write_text('''#import "/typst/heraldry.typ": *
#show: book
#let items = range(9).map(i => [Item #i. #("A complete explanatory phrase. " * 13)])
#let fragments = items.map(body => list-fragment(body))
#context { pdf.attach("/list-measures.json", bytes(json.encode((
  native: measure(block(width:col-w,list(..items))).height.pt(),
  fragments: measure(block(width:col-w,{for p in fragments {p}})).height.pt(),
)))) }
#keeppage(id:"list-fit",("c",fragments))
#hpos-summary()
''', encoding='utf-8')
        pdf, warnings = typst.Compiler(str(source),root=str(ROOT),font_paths=[str(ROOT/'fonts/static')],ignore_system_fonts=True).compile_with_warnings()
        self.assertFalse(warnings, [str(w) for w in warnings])
        reader = PdfReader(__import__('io').BytesIO(pdf))
        heights = json.loads(reader.attachments['list-measures.json'][0])
        self.assertAlmostEqual(heights['native'], heights['fragments'], delta=3)
        self.assertGreater(heights['native'], profile.BODY_HEIGHT_PT)
        self.assertEqual(len(reader.pages), 1)
        with pymupdf.open(stream=pdf,filetype='pdf') as doc:
            from reconcile import norm
            text=norm(doc[0].get_text())
            self.assertEqual(text.count('A complete explanatory phrase.'),9*13)
            self.assertTrue(any(w[0]>310 and w[4]=='Item' for w in doc[0].get_text('words')))

    def test_full_opening_keeps_table_and_coin_amounts_together(self):
        source = Path(self.tmp.name) / 'opening-table.typ'
        source.write_text('''#import "/typst/heraldry.typ": *
#show: book
#block(height:590pt)[Earlier content]
#full-opening[
#umark("opening","s")
#heading(level:3)[A table opening]
#htable("OPEN",(60,465),(left,left),([Cost],[Rule]),range(8).map(i=>([40c],[A complete rule #i.])),title:[Opening table])
#umark("opening","e")
]
#htable("COIN",(45,480),(left,left),([Cost],[Rule]),(([Cost 3c],[Three.]),([Cost 4c],[Four.]),([Cost 40c],[Forty.])),title:[Coins])
#hpos-summary()
''', encoding='utf-8')
        pdf,warnings=typst.Compiler(str(source),root=str(ROOT),font_paths=[str(ROOT/'fonts/static')],ignore_system_fonts=True).compile_with_warnings()
        self.assertFalse(warnings,[str(w) for w in warnings])
        reader=PdfReader(__import__('io').BytesIO(pdf))
        pos=json.loads(reader.attachments['heraldry-positions.json'][0])['positions']
        marks=[m for m in pos['<um-pos>'] if m['id']=='opening']
        self.assertEqual(len(marks),2)
        self.assertEqual(marks[0]['page'],marks[1]['page'])
        with pymupdf.open(stream=pdf,filetype='pdf') as doc:
            from reconcile import norm
            text=norm(' '.join(p.get_text() for p in doc))
            for value in ('3c','4c','40c'):
                self.assertIn(value,text)


if __name__ == "__main__":
    unittest.main()
