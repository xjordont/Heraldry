"""Explicit IDML export preserves source content and refuses misleading completion."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import export_indesign as export
from parse_source import parse
from update_manuscript import anchor_model


class InDesignExport(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.profile = json.loads((ROOT / "config/indesign.json").read_text(encoding="utf-8"))
        self.text = ('# Fixture\n\n**Release Candidate 484 (RC484)**\n\n'
                     '## 1. Rules\n\n[See movement](#11-movement).\n\n'
                     '### 1.1 Movement\n\nMove **6"**, then *rest*. café × 2.\n\n'
                     '| Roll | Result |\n|---|---|\n| 1 | An exact **outcome**. |\n\n'
                     '- First\n  - Nested\n\n> A quoted rule.\n')
        self.blocks = parse(self.text)
        anchor_model(self.blocks)
        self.assets = {"items": [], "fonts": [{"family": "Source Serif 4", "style": "Regular", "fullname": "Source Serif 4", "postscript": "SourceSerif4-Regular"}]}

    def write_idml(self, parts=None, name="test.idml"):
        original, expected = export.make_idml(self.blocks, self.assets, self.profile)
        path = self.folder / name
        export.zip_parts(path, parts or original)
        return path, expected

    def fixture_project(self):
        root = self.folder / "repo"
        for directory in ("source", "config", "tools/indesign", "fonts/static", "fonts/licences", "figures/out"):
            (root / directory).mkdir(parents=True, exist_ok=True)
        (root / "source/Heraldry_RC484.md").write_bytes(self.text.encode("utf-8"))
        (root / "config/indesign.json").write_bytes((ROOT / "config/indesign.json").read_bytes())
        for name in ("source/versions.json", "config/content_anchors.json", "config/figure_dependencies.json"):
            (root / name).write_bytes(b"{}\n")
        (root / "tools/indesign/finish.jsx").write_bytes((ROOT / "tools/indesign/finish.jsx").read_bytes())
        (root / "fonts/static/fixture.ttf").write_bytes(b"Fixture font bytes; parsing tested by asset suite")
        (root / "fonts/licences/OFL.txt").write_bytes(b"Fixture licence bytes")
        (root / "figures/out/FIG-TEST.svg").write_bytes(b'<svg xmlns="http://www.w3.org/2000/svg" width="80" height="40"><text x="0" y="20">Editable label</text></svg>')
        record = {"number": 484, "path": "source/Heraldry_RC484.md", "sha256": export.sha(self.text.encode("utf-8"))}
        figure = {"id": "FIG-TEST", "kind": "figure", "source": "figures/out/FIG-TEST.svg", "anchor": "h-11-movement",
                  "caption": "An editable figure.", "scope": "full", "width_pt": 80, "height_pt": 40,
                  "sha256": export.sha((root / "figures/out/FIG-TEST.svg").read_bytes())}
        assets = {"items": [figure], "fonts": [dict(self.assets["fonts"][0], path="fonts/static/fixture.ttf", sha256=export.sha((root / "fonts/static/fixture.ttf").read_bytes()))],
                  "licences": [{"path": "fonts/licences/OFL.txt", "sha256": export.sha((root / "fonts/licences/OFL.txt").read_bytes())}], "excluded": []}
        project = self.folder / "Owner's $project"
        with patch.object(export, "check", return_value=record), patch.object(export, "gather_assets", return_value=assets):
            manifest = export.export_project(root, project)
        return root, project, manifest

    def test_real_tables_styles_navigation_and_threaded_frames_with_exact_text(self):
        path, expected = self.write_idml()
        result = export.audit_idml(path, expected)
        self.assertEqual(result["structural_status"], "PASS")
        self.assertEqual(result["native_tables"], 1)
        self.assertEqual(result["native_cells"], 4)
        self.assertEqual(result["native_composition"], "NOT TESTED")
        with zipfile.ZipFile(path) as archive:
            self.assertEqual(archive.infolist()[0].filename, "mimetype")
            self.assertEqual(archive.infolist()[0].compress_type, zipfile.ZIP_STORED)
            styles = ET.fromstring(archive.read("Resources/Styles.xml"))
            self.assertTrue(styles.findall("RootParagraphStyleGroup/ParagraphStyle"))
            designmap = ET.fromstring(archive.read("designmap.xml"))
            self.assertEqual(len(designmap.findall("Hyperlink")), 1)
            self.assertEqual(len(designmap.findall("Layer")), 4)

    def test_deterministic_archive_and_input_model_unchanged(self):
        before = deepcopy(self.blocks)
        first, _ = self.write_idml(name="first.idml")
        second, _ = self.write_idml(name="second.idml")
        self.assertEqual(first.read_bytes(), second.read_bytes())
        self.assertEqual(self.blocks, before)

    def test_lost_or_changed_rule_cell_is_detected(self):
        parts, expected = export.make_idml(self.blocks, self.assets, self.profile)
        for name in parts:
            if b"outcome" in parts[name]:
                parts[name] = parts[name].replace(b"outcome", b"altered")
                break
        path = self.folder / "corrupt.idml"
        export.zip_parts(path, parts)
        with self.assertRaisesRegex(ValueError, "text differs"):
            export.audit_idml(path, expected)

    def test_broken_part_reference_and_thread_are_detected(self):
        parts, expected = export.make_idml(self.blocks, self.assets, self.profile)
        part_name = next(n for n in parts if n.startswith("Spreads/Spread_00"))
        broken = dict(parts)
        del broken[part_name]
        path = self.folder / "missing.idml"
        export.zip_parts(path, broken)
        with self.assertRaisesRegex(ValueError, "Missing IDML part"):
            export.audit_idml(path, expected)
        root = ET.fromstring(parts[part_name])
        root.find("Spread/TextFrame").set("NextTextFrame", "n")
        parts[part_name] = export.xml(root)
        path = self.folder / "thread.idml"
        export.zip_parts(path, parts)
        with self.assertRaisesRegex(ValueError, "thread"):
            export.audit_idml(path, expected)

    def test_unresolved_heading_link_refuses_export(self):
        blocks = parse(self.text.replace("#11-movement", "#absent"))
        anchor_model(blocks)
        with self.assertRaisesRegex(ValueError, "Unresolved manuscript link"):
            export.make_idml(blocks, self.assets, self.profile)

    def test_table_boundary_changes_cannot_hide_behind_identical_story_text(self):
        blocks = parse("# Fixture\n\n| A | B |\n|---|---|\n| 1 | 23 |\n")
        anchor_model(blocks)
        parts, expected = export.make_idml(blocks, self.assets, self.profile)
        expected_tables = {"manuscript_00": export.source_tables(blocks)}
        name = "Stories/Story_manuscript_00.xml"
        root = ET.fromstring(parts[name])
        cells = root.findall("Story/ParagraphStyleRange/CharacterStyleRange/Table/Cell")
        cells[2].find(".//Content").text = "12"
        cells[3].find(".//Content").text = "3"
        self.assertEqual(export.text_digest(export.story_text(root.find("Story"))), expected["manuscript_00"])
        parts[name] = export.xml(root)
        path = self.folder / "wrong-cell-boundaries.idml"
        export.zip_parts(path, parts)
        with self.assertRaisesRegex(ValueError, "source positions"):
            export.audit_idml(path, expected, expected_tables)

    def test_invalid_unreadable_or_unbounded_profile_refuses(self):
        changes = (("page", "columns", True), ("page", "inside", 12), ("page", "width", float("nan")),
                   ("type", "body_size", 8), ("type", "table_leading", 0), (None, "maximum_pages", 0))
        for group, key, value in changes:
            p = deepcopy(self.profile)
            (p[group] if group else p)[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                export.validate_profile(p)

    def test_full_project_is_portable_preserves_source_and_binds_finisher(self):
        root, project, manifest = self.fixture_project()
        self.assertEqual((project / "Source/Heraldry_RC484.md").read_bytes(), (root / "source/Heraldry_RC484.md").read_bytes())
        self.assertIn("Finish in InDesign.jsx", manifest["files"])
        self.assertNotIn("NOT TESTED", manifest["export_id"])
        moved = self.folder / "moved package"
        project.rename(moved)
        result = export.verify_project(moved)
        self.assertEqual(result["links"], 1)
        self.assertEqual(result["native_composition"], "NOT TESTED")
        with zipfile.ZipFile(moved / manifest["idml"]) as archive:
            uri = next(e.get("LinkResourceURI") for n in archive.namelist() if n.startswith("Stories/")
                       for e in ET.fromstring(archive.read(n)).iter("Link"))
            self.assertEqual(uri, "file:Links/FIG-TEST.svg")

    def test_changed_link_source_or_script_refuses_verification(self):
        _, project, _ = self.fixture_project()
        for relative in ("Links/FIG-TEST.svg", "Source/Heraldry_RC484.md", "Finish in InDesign.jsx"):
            path = project / relative
            before = path.read_bytes()
            path.write_bytes(before + b"x")
            with self.subTest(relative=relative), self.assertRaisesRegex(ValueError, "changed"):
                export.verify_project(project)
            path.write_bytes(before)

    def test_existing_project_and_authoritative_output_paths_refuse(self):
        root, project, _ = self.fixture_project()
        for destination in (project, root, root / "source/export", root / "production/export"):
            with self.subTest(destination=destination), self.assertRaises(ValueError):
                export.output_location(root, destination)

    def test_structural_export_cannot_claim_native_application_pass(self):
        _, project, _ = self.fixture_project()
        with self.assertRaises(OSError):
            export.verify_project(project, native=True)

    def test_native_report_requires_exact_export_and_roundtrip_content(self):
        _, project, manifest = self.fixture_project()
        native = project / manifest["idml"].replace(".idml", ".indd")
        roundtrip = project / manifest["idml"].replace(".idml", ".composed.idml")
        native.write_bytes(b"Synthetic native test fixture; not an actual InDesign file")
        shutil.copyfile(project / manifest["idml"], roundtrip)
        report = {"status": "PASS", "source_sha256": manifest["manuscript"]["sha256"], "export_id": "wrong"}
        report_path = project / "native-report.json"
        report_path.write_bytes(export.json_bytes(report))
        with self.assertRaisesRegex(ValueError, "No passing native"):
            export.verify_project(project, native=True)
        report.update(export_id=manifest["export_id"], native_bytes=native.stat().st_size, roundtrip_bytes=roundtrip.stat().st_size,
                      missing_fonts=[], missing_links=[], overset_stories=[], overset_cells=[], pages=4)
        report_path.write_bytes(export.json_bytes(report))
        result = export.verify_project(project, native=True)
        self.assertTrue(result["native_composition"].startswith("PASS"))
        # Same-length manual edits must not retain the previous proof.
        native.write_bytes(native.read_bytes().replace(b"Synthetic", b"Altered!!"))
        with self.assertRaisesRegex(ValueError, "changed after verified"):
            export.verify_project(project, native=True)

    def test_native_existing_output_is_preserved_before_launch(self):
        _, project, manifest = self.fixture_project()
        native = project / manifest["idml"].replace(".idml", ".indd")
        native.write_bytes(b"Owner's manual editing")
        with patch.object(export.subprocess, "run") as launch, self.assertRaisesRegex(ValueError, "already exists"):
            export.compose(project)
        launch.assert_not_called()
        self.assertEqual(native.read_bytes(), b"Owner's manual editing")

    def test_native_pass_with_missing_diagnostics_is_rejected(self):
        _, project, manifest = self.fixture_project()
        (project / "native-report.json").write_bytes(export.json_bytes({"status": "PASS",
            "source_sha256": manifest["manuscript"]["sha256"], "export_id": manifest["export_id"]}))
        with self.assertRaisesRegex(ValueError, "incomplete"):
            export.verify_project(project, native=True)

    def test_explicit_front_door_help_does_not_start_indesign(self):
        result = subprocess.run([sys.executable, "tools/dev.py", "indesign", "--help"], cwd=ROOT,
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("export", result.stdout)
        self.assertIn("compose", result.stdout)

    def test_workflow_is_manual_and_not_in_normal_build_targets(self):
        workflow = (ROOT / ".github/workflows/export-indesign.yml").read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", workflow)
        self.assertNotIn("  push:", workflow)
        self.assertNotIn("  schedule:", workflow)
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertNotIn("export_indesign", makefile)


if __name__ == "__main__":
    unittest.main()
