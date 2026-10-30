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
        self.assertEqual(book.out, ["lead", "more", "#intro-end()\n", "h"])


if __name__ == "__main__":
    unittest.main()
