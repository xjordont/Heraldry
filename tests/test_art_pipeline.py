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
        self.assertIn(g.CFG["exclusions"], p)

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
