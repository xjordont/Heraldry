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
        rs = g.CFG["gpt_reference_sets"]
        for sets in list(rs["sets"].values()) + list(rs.get("family_sets", {}).values()) + [k["refs"] for k in rs.get("kind_sets", {}).values()]:
            for cand in sets:
                if "/" in cand:
                    (root / cand).parent.mkdir(parents=True, exist_ok=True)
                    (root / cand).write_bytes(b"stand-in")
        return root

    def _batch_queue(self):
        import art_gpt_pack as pack, art_generate as g
        ents = {e["id"]: e for e in g.entries()}
        # The full queue as it stood before any approvals: the live selections are all "approved" once the
        # illustrations are complete, which would leave the queue (and so this check) empty.
        sels = {}
        for i in g.CFG["gpt_anchor_ids"]:
            sels[i] = {"route": "gpt", "status": "anchor-approved", "master": {"path": f"assets/art/incoming/{i}.png"}}
        anchors = {"route": "gpt", "status": "approved"}
        return pack, g, ents, pack.build_queue("batch", ents, sels, anchors, root=self._reference_root())

    def test_gpt_queue_references_are_short_and_register_specific(self):
        pack, g, ents, (q, prompts) = self._batch_queue()
        cfg = g.CFG["gpt_reference_sets"]
        style = "assets/art/style/"
        # scenery-carrying references never reach an isolated figure or still life (one owner-approved exception,
        # 2026-10-12: STYLE-REF-22, the wolf pack in a forest, in the beast set)
        scenic = {style + n for n in ("STYLE-REF-02-panorama-line.jpg", "STYLE-REF-07-drybrush-duel.jpg", "STYLE-REF-09-skeleton-melee-ink.jpg",
                                      "STYLE-REF-10-undead-crowd-ink.jpg", "STYLE-REF-11-city-approach-ink.png", "STYLE-REF-13-cave-river-pen.jpg",
                                      "STYLE-REF-21-adventuring-party-forest.jpg", "STYLE-REF-43-piranesi-drawbridge.jpg",
                                      "STYLE-REF-44-haden-vignette-farm.jpg",
                                      "STYLE-REF-46-round-tower-riders.jpg", "STYLE-REF-47-barrow-dolmen-moor.jpg",
                                      "STYLE-REF-49-swordsman-mountain-pass.jpg", "STYLE-REF-53-frost-harbour-city.png",
                                      "STYLE-REF-55-siege-wall-climb.jpg", "STYLE-REF-58-waterfall-ruins-flight.jpg",
                                      "STYLE-REF-59-harbour-wharf-etching.jpg", "STYLE-REF-60-skeleton-standard-bearer.jpg",
                                      "STYLE-REF-65-ship-dead-tree-coast.jpg", "STYLE-REF-67-ghoul-sewer-ambush.jpg")}
        city = style + "STYLE-REF-11-city-approach-ink.png"
        self.assertEqual(q["schema"], 2)
        # received images await review and are not re-queued; rejected ones are (as redos)
        done = set(g.CFG["gpt_anchor_ids"])        # the queue here is built with no selections beyond the anchors
        self.assertEqual(q["count"], len([i for i in ents if i not in done]), "every entry neither approved nor awaiting review is queued")
        lead = [i for i in g.CFG["gpt_lead_ids"] if i in {x["id"] for x in q["items"]}]
        self.assertEqual([x["id"] for x in q["items"][:len(lead)]], lead, "the mixed lead goes first")
        self.assertEqual(len({x["ref_set"] for x in q["items"][:len(lead)]}), len(lead), "one lead item per reference set")
        for it in q["items"]:
            refs = it["references"]
            self.assertTrue(1 <= len(refs) <= cfg["max_refs"], it["id"])
            self.assertEqual(len(refs), len(set(refs)), it["id"])
            self.assertNotIn(f"assets/art/incoming/{it['id']}.png", refs, "an entry never references itself")
            self.assertNotIn(style + "STYLE-REF-01-scene-hatching.jpg", refs, "cut by the owner 2026-10-11")
            self.assertFalse([r for r in refs if "/incoming/" in r], "generated images are never references")
            self.assertEqual(city in refs, it["family"] in ("bastion", "cover"), it["id"])
            if it["register"] != "scene":
                self.assertFalse(set(refs) & scenic, it["id"])
            if it["family"] == "monster":
                self.assertTrue(it["ref_set"].startswith("monster:"), it["id"])
            self.assertIn(it["size"], ("1536x1024", "1024x1536", "1024x1024"))
            self.assertEqual(it["print_w_in"], g.CFG["families"][it["family"]]["print_w_in"])
        self.assertEqual({it["max_attempts"] for it in q["items"]}, {1})       # one generation per item (owner 2026-10-12)

    def test_every_monster_has_exactly_one_kind(self):
        import copy
        pack, g, ents, _ = self._batch_queue()
        pack.check_kinds(ents)                                   # the live config covers every monster once
        saved = copy.deepcopy(g.CFG["gpt_reference_sets"]["kind_sets"])
        try:
            g.CFG["gpt_reference_sets"]["kind_sets"]["beast"]["ids"].remove("ART-MON-DIRE-WOLF")
            with self.assertRaisesRegex(SystemExit, "without a kind"):
                pack.check_kinds(ents)
            g.CFG["gpt_reference_sets"]["kind_sets"]["beast"]["ids"] += ["ART-MON-DIRE-WOLF", "ART-MON-ORC"]
            with self.assertRaisesRegex(SystemExit, "is in kind_sets"):
                pack.check_kinds(ents)
        finally:
            g.CFG["gpt_reference_sets"]["kind_sets"] = saved

    def test_gpt_queue_must_and_avoid_lists_appear_in_the_prompt_text(self):
        pack, g, ents, (q, prompts) = self._batch_queue()
        for it in q["items"]:
            text = prompts[it["id"]]
            self.assertEqual(it["must"], list((ents[it["id"]].get("brief") or {}).get("must", [])), it["id"])
            for m in it["must"]:
                self.assertIn("* " + m, text, it["id"])
            for a in it["avoid"]:
                self.assertIn("* " + a, text, it["id"])
            if it["family"] in ("monster", "boss"):
                self.assertEqual(bool(it["size_class"]), True, it["id"])
                self.assertIn("Size: " + it["size_class"], text, it["id"])
        # the catalogue, not the shrinking queue: approvals remove items from the queue as production goes on
        self.assertGreater(sum(len((e.get("brief") or {}).get("must", [])) for e in ents.values()), 20)
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
