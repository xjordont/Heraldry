"""Isolated publication-asset collection; no book build or live approvals."""
from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from indesign_assets import gather_assets, copy_assets


class InDesignAssets(unittest.TestCase):
    def setUp(self):
        from PIL import Image
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repo"
        self.root.mkdir()
        self.output = Path(self.temporary.name) / "output"
        raster = BytesIO()
        Image.new("RGBA", (600, 400), "white").save(raster, format="PNG")
        self.raster = raster.getvalue()
        self.model = [{"id": "h-1-rules", "type": "heading", "level": 2,
                       "c": [{"t": "text", "v": "1. Rules"}]},
                      {"id": "h-example", "type": "heading", "level": 3,
                       "c": [{"t": "text", "v": "Example"}]},
                      {"id": "B00099", "type": "para", "c": [{"t": "em", "c": [{"t": "text", "v": "Old flavour."}]}]},
                      {"id": "B00101", "type": "para", "c": [{"t": "text", "v": "Resolve the rules."}]}]
        catalog = [{"id": "ART-COVER-002", "family": "cover", "spec_sha256": "cover-spec"},
                   {"id": "ART-CH01-002", "family": "chapter", "spec_sha256": "chapter-spec"},
                   {"id": "ART-EXAMPLE", "family": "world", "spec_sha256": "spot-spec", "heading_id": "h-example",
                    "flavour_block": "B00001"}]
        self.write_json("production/art/SPOT_CATALOG.json", {"entries": catalog})
        selections = {}
        for entry in catalog:
            aid = entry["id"]
            selections[aid] = dict(entry, status="approved", ink={"path": f"assets/art/ink/{aid}.png",
                                                               "sha256": sha256(self.raster).hexdigest(), "px": [600, 400]})
            if entry["family"] != "cover":
                self.write(f"assets/art/ink/{aid}.png", self.raster)
        self.write_json("production/art/SELECTIONS.json", selections)
        self.write_json("config/art_style.json", {"families": {"chapter": {"print_w_in": 4.5}, "world": {"print_w_in": 3.3}},
                                                  "art_width_overrides": {"ART-EXAMPLE": 1.5}})
        self.write_json("figures/manifest.json", [{"id": "FIG-01", "file": "figures/out/FIG-01.svg",
                                                  "size_pt": {"width": 504, "height": 200}, "caption": "Exact figure caption.", "scope": "full"}])
        self.write_json("config/content_anchors.json", {"FIG-01": {"section": "h-example", "type": "para", "prefix": "Resolve the rules."}})
        self.write("figures/out/FIG-01.svg", b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 504 200"><path d="M0 0L2 2"/></svg>')
        self.write("assets/art/cover/front.png", self.raster)
        self.write_json("production/art/marks/APPROVED.json", {"arms": {"1": "approved-arm.png"}, "logo": "approved-logo.png", "coin": "approved-coin.png"})
        for name in ("arms-01", "coin", "coin-reversed", "logo"):
            self.write(f"typst/templates/marks/cream/{name}.svg", b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120"><path d="M0 0L2 2"/></svg>')
        self.make_font()
        self.write("fonts/licences/OFL-test.txt", b"Synthetic test font licence.")

    def write(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def write_json(self, relative, value):
        return self.write(relative, json.dumps(value).encode("utf-8"))

    def mutate(self, relative, update):
        path = self.root / relative
        value = json.loads(path.read_text(encoding="utf-8"))
        update(value)
        self.write_json(relative, value)

    def make_font(self):
        from fontTools.fontBuilder import FontBuilder
        from fontTools.pens.ttGlyphPen import TTGlyphPen
        builder = FontBuilder(1000, isTTF=True)
        builder.setupGlyphOrder([".notdef", "A"])
        builder.setupCharacterMap({65: "A"})
        builder.setupGlyf({name: TTGlyphPen(None).glyph() for name in (".notdef", "A")})
        builder.setupHorizontalMetrics({name: (500, 0) for name in (".notdef", "A")})
        builder.setupHorizontalHeader(ascent=800, descent=-200)
        builder.setupNameTable({"familyName": "Heraldry Test", "styleName": "Regular", "uniqueFontIdentifier": "HeraldryTest-Regular",
                                "fullName": "Heraldry Test Regular", "psName": "HeraldryTest-Regular", "version": "Version 1.0"})
        builder.setupOS2(sTypoAscender=800, sTypoDescender=-200, usWinAscent=800, usWinDescent=200)
        builder.setupPost()
        path = self.root / "fonts/static/Test-Regular.ttf"
        path.parent.mkdir(parents=True)
        builder.save(path)

    def gather(self):
        return gather_assets(self.root, self.model)

    def test_current_heading_and_flavour_anchor_replace_old_line_id(self):
        assets = self.gather()
        lookup = {item["id"]: item for item in assets["items"]}
        self.assertEqual(lookup["ART-EXAMPLE"]["anchor"], "B00099")
        self.assertEqual(lookup["ART-CH01-002"]["anchor"], "h-1-rules")
        self.assertEqual(lookup["FIG-01"]["anchor"], "B00101")
        self.assertEqual(lookup["ART-EXAMPLE"]["width_pt"], 108)
        self.assertEqual(lookup["ART-CH01-002"]["width_pt"], 144)
        self.assertEqual(len(assets["items"]), 8)
        self.assertEqual(assets["excluded"][0]["id"], "ART-COVER-002")
        self.assertNotIn("ART-COVER-002", lookup)

    def test_font_metadata_and_exact_bytes_packaged(self):
        gathered = self.gather()
        self.assertEqual(gathered["fonts"][0]["family"], "Heraldry Test")
        self.assertEqual(gathered["fonts"][0]["postscript"], "HeraldryTest-Regular")
        self.assertFalse(gathered["fonts"][0]["variable"])
        copied = copy_assets(self.root, self.output, gathered)
        self.assertNotIn("package_path", gathered["items"][0])
        for key in ("items", "fonts", "licences"):
            for record in copied[key]:
                data = (self.output / record["package_path"]).read_bytes()
                self.assertEqual(sha256(data).hexdigest(), record["sha256"])
        self.assertEqual(len(list(self.output.rglob("*.*"))), 10)

    def test_selection_requires_explicit_approval_and_current_spec(self):
        for field, value, message in (("status", "auto-selected", "explicit approval"), ("spec_sha256", "stale", "specification is stale")):
            with self.subTest(field=field):
                original = (self.root / "production/art/SELECTIONS.json").read_bytes()
                self.mutate("production/art/SELECTIONS.json", lambda data: data["ART-EXAMPLE"].update({field: value}))
                with self.assertRaisesRegex(ValueError, message):
                    self.gather()
                self.write("production/art/SELECTIONS.json", original)

    def test_missing_selection_refuses_incomplete_export(self):
        self.mutate("production/art/SELECTIONS.json", lambda data: data.pop("ART-EXAMPLE"))
        with self.assertRaisesRegex(ValueError, "Every catalog item"):
            self.gather()

    def test_changed_derivative_and_lfs_pointer_refuse(self):
        path = "assets/art/ink/ART-EXAMPLE.png"
        for data, message in ((b"changed", "hash mismatch"), (b"version https://git-lfs.github.com/spec/v1\noid sha256:a\nsize 1\n", "unfetched Git LFS")):
            with self.subTest(message=message):
                self.write(path, data)
                with self.assertRaisesRegex(ValueError, message):
                    self.gather()

    def test_missing_file_refuses(self):
        (self.root / "assets/art/cover/front.png").unlink()
        with self.assertRaisesRegex(ValueError, "Missing publication asset"):
            self.gather()

    def test_wrong_approved_pixel_dimensions_refuse(self):
        self.mutate("production/art/SELECTIONS.json", lambda data: data["ART-EXAMPLE"]["ink"].update(px=[100, 100]))
        with self.assertRaisesRegex(ValueError, "dimensions disagree"):
            self.gather()

    def test_unresolved_art_and_figure_anchors_refuse(self):
        original = deepcopy(self.model)
        for index in (1, 3):
            with self.subTest(index=index):
                self.model = deepcopy(original)
                self.model[index]["c"] = [{"t": "text", "v": "Changed."}]
                if index == 1:
                    self.model[index]["id"] = "h-changed"
                with self.assertRaises(ValueError):
                    self.gather()

    def test_private_or_escaping_source_is_never_packaged(self):
        for path in ("../outside.png", "references/private/pdfs/test.pdf"):
            with self.subTest(path=path):
                self.mutate("production/art/SELECTIONS.json", lambda data: data["ART-EXAMPLE"]["ink"].update(path=path))
                if path.startswith("references"):
                    self.write(path, self.raster)
                with self.assertRaises(ValueError):
                    self.gather()

    def test_svg_external_resource_and_xml_declarations_refuse(self):
        for data in (b'<svg viewBox="0 0 10 10"><image href="https://example.test/private.png"/></svg>',
                     b'<svg viewBox="0 0 10 10"><path fill="url(file://private.svg)" d="M0 0"/></svg>',
                     b'<svg viewBox="0 0 10 10"><script>alert(1)</script></svg>',
                     b'<!DOCTYPE svg><svg viewBox="0 0 10 10"/>'):
            with self.subTest(data=data):
                self.write("figures/out/FIG-01.svg", data)
                with self.assertRaises(ValueError):
                    self.gather()

    def test_duplicate_metadata_key_is_not_silently_dropped(self):
        self.write("production/art/SELECTIONS.json", b'{"duplicate": {}, "duplicate": {}}')
        with self.assertRaisesRegex(ValueError, "Duplicate metadata key"):
            self.gather()

    def test_duplicate_manifest_ids_and_missing_binding_refuse(self):
        self.mutate("figures/manifest.json", lambda data: data.append(deepcopy(data[0])))
        with self.assertRaisesRegex(ValueError, "Duplicate figure"):
            self.gather()
        self.mutate("figures/manifest.json", lambda data: data.pop())
        self.write_json("config/content_anchors.json", {})
        with self.assertRaisesRegex(ValueError, "persistent content anchor"):
            self.gather()

    def test_existing_output_is_never_overwritten(self):
        assets = self.gather()
        self.output.mkdir()
        (self.output / "keep.txt").write_bytes(b"Keep this")
        with self.assertRaisesRegex(ValueError, "already exists"):
            copy_assets(self.root, self.output, assets)
        self.assertEqual((self.output / "keep.txt").read_bytes(), b"Keep this")

    def test_stale_collected_bytes_refuse_before_output_created(self):
        assets = self.gather()
        self.write("figures/out/FIG-01.svg", b"changed")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            copy_assets(self.root, self.output, assets)
        self.assertFalse(self.output.exists())

    def test_filename_collision_refuses_before_output_created(self):
        assets = self.gather()
        duplicate = deepcopy(assets["items"][-1])
        duplicate["id"] = "SECOND-PLACEMENT"
        assets["items"].append(duplicate)
        with self.assertRaisesRegex(ValueError, "filename collision"):
            copy_assets(self.root, self.output, assets)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
