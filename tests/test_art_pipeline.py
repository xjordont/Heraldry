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

    def test_reject_keeps_the_reviewers_reason_until_the_entry_is_approved(self):
        import art_generate as g, art_intake
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as d:
            sel = Path(d) / "SELECTIONS.json"
            sel.write_text(json.dumps({"x": {"status": "received"}}))
            with patch.object(g, "SELECTIONS", sel):
                art_intake.set_status(["x"], "rejected", "six legs, not eight")
                self.assertEqual(json.loads(sel.read_text())["x"]["rejected_reason"], "six legs, not eight")
                art_intake.set_status(["x"], "rejected")
                self.assertNotIn("rejected_reason", json.loads(sel.read_text())["x"])
                art_intake.set_status(["x"], "rejected", "again")
                art_intake.set_status(["x"], "approved")
                self.assertNotIn("rejected_reason", json.loads(sel.read_text())["x"])

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

    def _reference_root(self):
        """A temporary repo root holding stand-in reference images, so the tests also pass in a release
        package, which does not ship the owner's style samples."""
        import art_generate as g
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        for sets in g.CFG["gpt_reference_sets"]["sets"].values():
            for cand in sets:
                if "/" in cand:
                    (root / cand).parent.mkdir(parents=True, exist_ok=True)
                    (root / cand).write_bytes(b"stand-in")
        return root

    def _batch_queue(self):
        import art_gpt_pack as pack, art_generate as g
        ents = {e["id"]: e for e in g.entries()}
        sels = dict(g.load(g.SELECTIONS, {}))
        for i in g.CFG["gpt_anchor_ids"]:
            sels[i] = {"route": "gpt", "status": "anchor-approved", "master": {"path": f"assets/art/incoming/{i}.png"}}
        anchors = {"route": "gpt", "status": "approved"}
        return pack, g, ents, pack.build_queue("batch", ents, sels, anchors, root=self._reference_root())

    def test_gpt_queue_references_are_short_and_register_specific(self):
        pack, g, ents, (q, prompts) = self._batch_queue()
        cfg = g.CFG["gpt_reference_sets"]
        scene_only = {c for c in cfg["sets"]["scene"]} | {"assets/art/incoming/ART-BAS-GREYTHORN.png"}
        figure_only = {"assets/art/style/STYLE-REF-03-figure-spotblack.jpg"} | {
            f"assets/art/incoming/{i}.png" for s in ("creature", "person") for i in cfg["sets"][s] if "/" not in i}
        self.assertEqual(q["schema"], 2)
        self.assertEqual(q["count"], len(ents) - len(g.CFG["gpt_anchor_ids"]))
        for it in q["items"]:
            refs = it["references"]
            self.assertTrue(1 <= len(refs) <= cfg["max_refs"], it["id"])
            self.assertEqual(len(refs), len(set(refs)), it["id"])
            self.assertNotIn(f"assets/art/incoming/{it['id']}.png", refs, "an entry never references itself")
            if it["register"] == "scene":
                self.assertFalse(set(refs) & {r for r in figure_only if "STYLE-REF-03" in r or "MON-" in r or "CLA-" in r or "ANC-" in r}, it["id"])
            else:
                self.assertFalse(set(refs) & {"assets/art/style/STYLE-REF-01-scene-hatching.jpg", "assets/art/style/STYLE-REF-02-panorama-line.jpg",
                                              "assets/art/incoming/ART-BAS-GREYTHORN.jpg", "assets/art/incoming/ART-CLI-THE-GREENMARK.png"}, it["id"])
            self.assertIn(it["size"], ("1536x1024", "1024x1536", "1024x1024"))
            self.assertEqual(it["print_w_in"], g.CFG["families"][it["family"]]["print_w_in"])
        self.assertEqual({it["max_attempts"] for it in q["items"] if it["family"] in ("cover", "chapter")}, {5})
        self.assertEqual({it["max_attempts"] for it in q["items"] if it["family"] == "monster"}, {3})

    def test_gpt_queue_must_and_avoid_lists_appear_in_the_prompt_text(self):
        pack, g, ents, (q, prompts) = self._batch_queue()
        seen_must = 0
        for it in q["items"]:
            text = prompts[it["id"]]
            for m in it["must"]:
                seen_must += 1
                self.assertIn("* " + m, text, it["id"])
            for a in it["avoid"]:
                self.assertIn("* " + a, text, it["id"])
            if it["family"] in ("monster", "boss"):
                self.assertEqual(bool(it["size_class"]), True, it["id"])
                self.assertIn("Size: " + it["size_class"], text, it["id"])
        self.assertGreater(seen_must, 20)
        md = pack.queue_markdown(q)
        self.assertIn("| Set | Reference images |", md)

    def test_gpt_anchor_queue_excludes_received_owner_anchor_and_lists_references(self):
        import art_gpt_pack as pack, art_generate as g
        ents = {e["id"]: e for e in g.entries()}
        sels = {"ART-BAS-GREYTHORN": {"route": "gpt", "status": "received"}}
        q, prompts = pack.build_queue("anchors", ents, sels, {}, root=self._reference_root())
        ids = [it["id"] for it in q["items"]]
        self.assertNotIn("ART-BAS-GREYTHORN", ids)
        self.assertEqual(len(ids), len(g.CFG["gpt_anchor_ids"]) - 1)
        for it in q["items"]:
            self.assertTrue(it["references"], it["id"])
        with self.assertRaises(SystemExit):
            pack.build_queue("batch", ents, sels, {})


if __name__ == "__main__":
    unittest.main()
