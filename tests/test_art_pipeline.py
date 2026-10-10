import json, sys, tempfile, unittest
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


class ArtPipeline(unittest.TestCase):
    def test_catalog_entries_are_unique_and_styled(self):
        cat = json.loads((ROOT / "production/art/SPOT_CATALOG.json").read_text())
        cfg = json.loads((ROOT / "config/art_style.json").read_text())
        ids = [e["id"] for e in cat["entries"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(cat["total"], len(ids))
        for e in cat["entries"]:
            self.assertIn(e["family"], cfg["families"])
        for a in cfg["anchor_ids"]:
            self.assertIn(a, ids)

    def test_prompt_quotes_flavour_verbatim(self):
        import art_generate as g
        e = next(x for x in g.entries() if x["family"] == "monster")
        p = g.prompt_for(e, True)
        self.assertIn('"' + e["flavour"] + '"', p)
        self.assertIn("FINAL VISUAL REQUIREMENTS", p)
        self.assertTrue(p.startswith(e["title"].upper()))

    def test_publication_uses_only_approved_art_selections(self):
        from unittest.mock import patch
        import build_book as book
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "production/art").mkdir(parents=True)
            Image.new("LA", (600, 400)).save(root / "ink.png")
            entries = [{"id": "a", "spec_sha256": "same", "flavour_block": "flavour"}]
            (root / "production/art/SPOT_CATALOG.json").write_text(json.dumps({"entries": entries}))
            style, selections = root / "style.json", root / "selections.json"
            style.write_text(json.dumps({"families": {"monster": {"print_w_in": 2}}}))
            for status in ("anchor-proposed", "low-score-needs-review", "rejected", "anchor-approved", "auto-selected"):
                with self.subTest(status=status):
                    selections.write_text(json.dumps({"a": {"family": "monster", "status": status,
                        "spec_sha256": "same", "ink": {"path": "ink.png"}}}))
                    with patch.multiple(book, ROOT=root, ART_SEL=selections, ART_STYLE=style):
                        by_block, by_id = book.load_spot_art()
                    approved = status in {"anchor-approved", "auto-selected"}
                    self.assertEqual(bool(by_id), approved)
                    self.assertEqual(bool(by_block), approved)

    def test_ink_prep_makes_transparent_black(self):
        from art_ink import prep
        with tempfile.TemporaryDirectory() as d:
            src, dst = Path(d) / "a.png", Path(d) / "b.png"
            im = Image.new("RGB", (400, 300), (250, 248, 240))
            ImageDraw.Draw(im).ellipse((100, 80, 300, 220), outline=(10, 10, 10), width=8)
            im.save(src)
            info = prep(src, dst)
            out = Image.open(dst)
            self.assertEqual(out.mode, "LA")
            self.assertEqual(out.getpixel((0, 0))[1], 0)
            self.assertEqual(info["flags"], [])
            self.assertLessEqual(out.size[0], 400)


if __name__ == "__main__":
    unittest.main()
