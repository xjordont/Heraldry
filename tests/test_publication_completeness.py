"""Owner instruction 2026-10-29: imprint metadata, current player aids, style-lock typography, 300 ppi art."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


class Imprint(unittest.TestCase):
    def test_owner_metadata_is_recorded(self):
        meta = json.loads((ROOT / "config/production.json").read_text())["verified_publication_metadata"]
        self.assertEqual(meta["author_credit"], "Jordon")
        self.assertEqual(meta["publisher"], "Escutcheon Press")
        self.assertIsNone(meta["isbn"])
        self.assertTrue(meta["version"].startswith("Release Candidate "))

    def test_colophon_has_no_stale_edition_text_or_illustration_credit(self):
        colophon = " ".join(json.loads((ROOT / "editorial/how_to_use.json").read_text())["colophon"])
        for stale in ("RC484", "Art-light", "Cinzel", "illustrat", "ISBN", "Rules diagrams"):
            self.assertNotIn(stale, colophon)
        for token in ("{{AUTHOR}}", "{{PUBLISHER}}", "{{VERSION}}"):
            self.assertIn(token, colophon)

    def test_back_cover_blurb_is_not_the_chapter_one_lead(self):
        blurb = json.loads((ROOT / "editorial/back_cover.json").read_text())["blurb"]
        source = (ROOT / "source/Heraldry_RC522.md").read_text(encoding="utf-8")
        self.assertNotIn(blurb, source)
        for banned in ("—", "’", "“", "…"):
            self.assertNotIn(banned, blurb)

    def test_publisher_logo_prints_sharp_where_it_is_placed(self):
        from PIL import Image
        logo = ROOT / "assets/art/brand/escutcheon-press-logo.png"
        self.assertTrue((ROOT / "assets/art/brand/escutcheon-press-logo-source.jpg").is_file())
        with Image.open(logo) as image:
            self.assertEqual(image.mode, "LA")             # ink plus transparency: the paper shows through
            width, height = image.size
        widest = 1.3                                        # inches wide, the colophon placement
        self.assertGreaterEqual(width / widest, 300)
        self.assertGreater(height, width)                   # the shield and banner stand upright
        self.assertIn("publisher-logo(w)", (ROOT / "typst/heraldry.typ").read_text())
        front = (ROOT / "typst/frontmatter.typ").read_text()
        self.assertEqual(front.count("publisher-logo("), 2)    # the title page and the colophon
        self.assertIn("publisher-logo(", (ROOT / "typst/cover.typ").read_text())
        self.assertIn("`assets/art/brand/`", (ROOT / "docs/LARGE_FILES.md").read_text())   # plain Git, not LFS


class ArtResolution(unittest.TestCase):
    def test_low_resolution_placement_fails(self):
        import check_art_ppi
        doc = pymupdf.open()
        page = doc.new_page(width=612, height=792)
        pix = pymupdf.Pixmap(pymupdf.csGRAY, pymupdf.IRect(0, 0, 300, 300), False)
        pix.clear_with(128)
        page.insert_image(pymupdf.Rect(36, 36, 36 + 144, 36 + 144), pixmap=pix)    # 300 px over 2 in
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "low.pdf"
            doc.save(path)
            ppi, where = check_art_ppi.lowest(str(path))
            self.assertAlmostEqual(ppi, 150, delta=1)
            result = subprocess.run([sys.executable, str(ROOT / "tools/check_art_ppi.py"), str(path)], capture_output=True)
            self.assertEqual(result.returncode, 1)


class PlayerAids(unittest.TestCase):
    def test_every_sheet_is_current_with_the_active_manuscript(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/aids_fidelity.py")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_sheets_follow_the_style_lock(self):
        kit = (ROOT / "typst/aids/kit.typ").read_text()
        self.assertIn("smartquote(enabled: false)", kit)
        for sheet in sorted((ROOT / "typst/aids").glob("pa*.typ")):
            text = sheet.read_text(encoding="utf-8")
            for banned in ("″", "−", "—", "’", "True Death", "Bleeding Out"):
                self.assertNotIn(banned, text, sheet.name)


class OpenerSpread(unittest.TestCase):
    def test_composer_marks_the_end_of_the_opening_flavour(self):
        from build_book import Book
        book = Book.__new__(Book)
        calls = []
        book.chapter_items = lambda blocks: blocks
        book.build_tree = lambda items: {"children": items}
        book.collect_units = lambda c, acc: None
        book.request_measure = lambda u: None
        book.extra_units = {}
        book.out = []
        def emit_x(c, cur, after):
            book.out.append(c["id"])
            return cur, False
        book.emit_x = emit_x
        book.flush = lambda cur: None
        book.emit_chapter_body([{"id": "lead", "kind": "f"}, {"id": "more", "kind": "f"},
                                {"id": "h", "head": {}, "kind": "c"}])
        self.assertEqual(book.out, ["lead", "more", "#intro-end(solo: \"auto\")\n", "h"])

    def test_opener_with_a_fresh_first_section_is_marked_solo(self):
        from build_book import Book
        book = Book.__new__(Book)
        book.chapter_items = lambda blocks: blocks
        book.build_tree = lambda items: {"children": items}
        book.collect_units = lambda c, acc: None
        book.request_measure = lambda u: None
        book.extra_units = {}
        book.out = []
        def emit_x(c, cur, after):
            if "head" in c:
                book.out.append("#pagebreak(weak: true)\n")
            book.out.append(c["id"])
            return cur, False
        book.emit_x = emit_x
        book.flush = lambda cur: None
        book.emit_chapter_body([{"id": "lead", "kind": "f"}, {"id": "h", "head": {}, "kind": "c"}])
        self.assertEqual(book.out, ["lead", "#intro-end(solo: true)\n", "#pagebreak(weak: true)\n", "h"])
        book.out = []
        book.emit_chapter_body([{"id": "lead", "kind": "f"}, {"id": "p", "kind": "c"}])
        self.assertEqual(book.out, ["lead", "#intro-end()\n", "p"])


if __name__ == "__main__":
    unittest.main()


class SectionEndFill(unittest.TestCase):
    """Owner 2026-10-30: fill the white space a section's last page leaves with art, diagrams, and figures."""

    def test_figures_print_in_book_order_and_relabel_their_references(self):
        from build_book import number_figures
        text = ('#figure-block("FIG-08", "../figures/out/FIG-08.svg", [#"A (see 2.7)."], width: 100%)\n'
                '#figure-block("FIG-20", "../figures/out/FIG-20.svg", [#"Key (see 10.4)."], width: 100%)\n'
                '#figure-block("FIG-07", "../figures/out/FIG-07.svg", [#"key: FIG-20 (see 2.8)."], width: 100%)\n')
        out = number_figures(text)
        self.assertIn('shown: "FIG-01"', out.splitlines()[0])
        self.assertIn('[#"key: FIG-02 (see 2.8)."], shown: "FIG-03"', out.splitlines()[2])
        self.assertIn('#figure-block("FIG-07", "../figures/out/FIG-07.svg"', out)   # registry id and file unchanged

    def test_end_figures_are_registered_with_anchors(self):
        sys.path.insert(0, str(ROOT / "figures/src"))
        import figdata
        anchors = json.loads((ROOT / "config/content_anchors.json").read_text())
        for n in range(58, 78):
            fid = f"FIG-{n}"
            self.assertIn(fid, figdata.META)
            self.assertIn(fid, anchors)
            self.assertTrue((ROOT / "figures/out" / f"{fid}.svg").is_file())

    def test_tailpieces_are_catalogued_and_briefed(self):
        cat = json.loads((ROOT / "production/art/SPOT_CATALOG.json").read_text())["entries"]
        ends = [e for e in cat if e.get("end_art")]
        self.assertEqual(len(ends), len(json.loads((ROOT / "production/art/END_ART_PLAN.json").read_text())["entries"]))
        for e in ends:
            self.assertIn("brief", e)
            self.assertIn("No lettering, numbers, dice, game tokens, or rulebook pages", e["brief"]["avoid"])

    def test_end_art_never_moves_text(self):
        source = (ROOT / "typst/heraldry.typ").read_text()
        self.assertIn("#let endart(", source)
        self.assertIn("next.first().location().page() == at.page()", source)   # only where the next heading starts a later page


class OptionalTailpieces(unittest.TestCase):
    def test_pending_tailpieces_do_not_block_a_build_request(self):
        import build_request
        problems = " ".join(build_request.problems())
        self.assertNotIn("required items", problems)
