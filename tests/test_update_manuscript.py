"""Owner-supplied Markdown updates stay exact, reviewable, and separate from builds."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from manuscript import ROOT, ORIGINAL_SHA, check
from update_manuscript import analyse, apply_review, exact_patches, normalise, prepare
import update_manuscript
from git_publish import PublishError


class ManuscriptUpdates(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.root = self.directory / "repo"
        self.text = ('# Fixture manuscript\n\n**Release Candidate 484 (RC484)**\n\n'
                     '## 1. Rules\n\n### 1.1 Speed\n\nMove 6".\n\n'
                     '### 1.2 Rest\n\nRest here.\n')
        self.source = self.root / "source/Heraldry_RC484.md"
        self.source.parent.mkdir(parents=True)
        self.source.write_bytes(self.text.encode("utf-8"))
        self.base_sha = hashlib.sha256(self.source.read_bytes()).hexdigest()
        authority = patch("manuscript.ORIGINAL_SHA", self.base_sha)
        authority.start()
        self.addCleanup(authority.stop)
        self.write_json("source/versions.json", {"current": 484, "revisions": [{
            "number": 484, "path": "source/Heraldry_RC484.md", "sha256": self.base_sha,
            "bytes": self.source.stat().st_size}]})
        self.write_json("config/production.json", {"source": "source/Heraldry_RC484.md",
            "verified_publication_metadata": {"version": "Release Candidate 484 (RC484)"}})
        self.write_json("editorial/patches.json", {"patches": []})
        self.write_json("config/content_anchors.json", {"speed": {
            "section": "h-11-speed", "type": "para", "prefix": 'Move 6".'}})
        self.write_json("config/figure_dependencies.json", {"FIG-01": ["1.1"], "FIG-02": ["1.2"]})
        self.incoming = self.directory / "Owner update.md"
        self.proposed = self.text.replace("Rest here.", "Rest here, then finish. café × 2.")
        self.incoming.write_bytes(self.proposed.encode("utf-8"))
        self.bundle = self.directory / "review bundle"

    def write_json(self, relative, value):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((json.dumps(value, ensure_ascii=False) + "\n").encode("utf-8"))

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def prepare(self):
        return prepare(self.root, self.incoming, self.bundle)

    def apply(self, **kwargs):
        return apply_review(self.root, self.bundle, "Owner update", "Fixture owner instruction", **kwargs)

    def test_prepare_does_not_change_repository_or_approve_patches(self):
        before = self.snapshot()
        path, report = self.prepare()
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(path, self.bundle)
        self.assertEqual(report["impact"]["affected_figures"], ["FIG-02"])
        self.assertEqual(report["impact"]["blockers"], [])
        batch = json.loads((path / "proposed-patches.json").read_text(encoding="utf-8"))
        self.assertTrue(all(p["status"] == "proposed" for p in batch["patches"]))
        self.assertIn("Rest here, then finish.", (path / "changes.diff").read_text(encoding="utf-8"))
        with self.assertRaises(FileExistsError):
            self.prepare()

    def test_approved_import_archives_exact_changes_and_promotes_once(self):
        before = self.source.read_bytes()
        self.prepare()
        record = self.apply(approve=True)
        self.assertEqual(record, check(self.root))
        self.assertEqual(record["number"], 485)
        self.assertEqual(self.source.read_bytes(), before)
        expected = self.proposed.replace("484 (RC484)", "485 (RC485)").encode("utf-8")
        self.assertEqual((self.root / record["path"]).read_bytes(), expected)
        self.assertEqual((self.root / record["patch_file"]).read_bytes(), (self.bundle / "approved-patches.json").read_bytes())
        after = self.snapshot()
        with self.assertRaisesRegex(ValueError, "stale"):
            self.apply(approve=True)
        self.assertEqual(self.snapshot(), after)

    def test_bom_crlf_and_next_marker_are_explicit_normalisations(self):
        raw = b"\xef\xbb\xbf" + self.proposed.replace("484 (RC484)", "485 (RC485)").replace("\n", "\r\n").encode("utf-8")
        self.incoming.write_bytes(raw)
        _, report = self.prepare()
        self.assertEqual(report["normalisations"], {"incoming_rc": 485, "utf8_bom_removed": True, "line_endings_normalised": True})
        self.apply(approve=True)
        self.assertEqual((self.bundle / "incoming.md").read_bytes(), raw)
        self.assertNotIn(b"\r", (self.root / "source/Heraldry_RC485.md").read_bytes())

    def test_noop_and_marker_only_update_create_no_bundle_or_revision(self):
        before = self.snapshot()
        for text in (self.text, self.text.replace("484 (RC484)", "485 (RC485)")):
            self.incoming.write_bytes(text.encode("utf-8"))
            with self.assertRaisesRegex(ValueError, "No manuscript text changes"):
                self.prepare()
            self.assertFalse(self.bundle.exists())
        self.assertEqual(self.snapshot(), before)

    def test_invalid_version_markers_refuse(self):
        for text in (self.proposed.replace("484 (RC484)", "483 (RC483)"),
                     self.proposed.replace("484 (RC484)", "490 (RC490)"),
                     self.proposed.replace("484 (RC484)", "484 (RC485)"),
                     self.proposed + "\n**Release Candidate 484 (RC484)**\n",
                     self.proposed.replace("**Release Candidate 484 (RC484)**", "")):
            with self.subTest(text=text[:70]), self.assertRaises(ValueError):
                normalise(text.encode("utf-8"), 484)

    def test_approval_and_owner_reference_are_required(self):
        self.prepare()
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "--approve"):
            self.apply()
        for reason, authorization in (("", "Owner"), ("Update", " ")):
            with self.assertRaises(ValueError):
                apply_review(self.root, self.bundle, reason, authorization, approve=True)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.bundle / "approved-patches.json").exists())

    def test_changed_bundle_files_refuse_before_promotion(self):
        self.prepare()
        before = self.snapshot()
        for name in ("incoming.md", "candidate.md", "proposed-patches.json", "changes.diff"):
            with self.subTest(name=name):
                path = self.bundle / name
                original = path.read_bytes()
                path.write_bytes(original + b" ")
                with self.assertRaisesRegex(ValueError, "Review bundle changed"):
                    self.apply(approve=True)
                self.assertEqual(self.snapshot(), before)
                path.write_bytes(original)

    def test_changed_config_requires_fresh_review(self):
        self.prepare()
        self.write_json("config/content_anchors.json", {})
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "configuration changed"):
            self.apply(approve=True)
        self.assertEqual(self.snapshot(), before)

    def test_companion_bindings_can_target_new_manuscript_text_in_same_commit(self):
        text = self.proposed.replace('Move 6".', 'Walk 6".').replace("### 1.2 Rest", "### 1.3 Rest")
        self.incoming.write_bytes(text.encode("utf-8"))
        self.write_json("config/content_anchors.json", {"speed": {
            "section": "h-11-speed", "type": "para", "prefix": 'Walk 6".'}})
        self.write_json("config/figure_dependencies.json", {"FIG-01": ["1.1"], "FIG-02": ["1.3"]})
        _, report = self.prepare()
        self.assertEqual(report["impact"]["blockers"], [])
        self.assertEqual(report["impact"]["affected_figures"], ["FIG-01", "FIG-02"])
        self.assertEqual(self.apply(approve=True)["number"], 485)

    def test_cli_enforces_current_main_before_any_promotion(self):
        self.prepare()
        before = self.snapshot()
        with patch.object(update_manuscript, "ROOT", self.root), \
                patch.object(update_manuscript, "require_current_main", side_effect=PublishError("Fixture dirty main")) as guard, \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(update_manuscript.main(["apply", "--review-dir", str(self.bundle), "--approve",
                             "--reason", "Fixture update", "--authorization", "Fixture owner"]), 1)
        guard.assert_called_once_with(self.root, allowed_changes=update_manuscript.CONFIGS)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.bundle / "approved-patches.json").exists())

    def test_broken_anchors_missing_sections_and_unsupported_markdown_block_apply(self):
        cases = (self.proposed.replace('Move 6".', 'Walk 6".'),
                 self.proposed.replace("### 1.2 Rest", "### 1.3 Rest"),
                 self.proposed + "\n```python\nprint('unsupported')\n```\n")
        for i, text in enumerate(cases):
            with self.subTest(case=i):
                self.incoming.write_bytes(text.encode("utf-8"))
                path, report = prepare(self.root, self.incoming, self.directory / f"blocked-{i}")
                self.assertTrue(report["impact"]["blockers"])
                before = self.snapshot()
                with self.assertRaisesRegex(ValueError, "blocked"):
                    apply_review(self.root, path, "Update", "Owner", approve=True)
                self.assertEqual(self.snapshot(), before)

    def test_line_shifts_are_reported_and_no_newline_diff_is_readable(self):
        proposed = self.proposed + "\nExtra paragraph without final newline"
        report, _, _, diff = analyse(self.root, proposed.encode("utf-8"))
        self.assertTrue(report["impact"]["line_numbers_shift"])
        self.assertIn(b"\n\\ No newline at end of file\n", diff)

    def test_review_directory_cannot_write_into_authoritative_tracks(self):
        for location in (self.root, self.root / "source/review", self.root / "production/review"):
            with self.subTest(location=location), self.assertRaisesRegex(ValueError, "Review bundles belong"):
                prepare(self.root, self.incoming, location)
        with self.assertRaisesRegex(ValueError, "Markdown"):
            prepare(self.root, self.directory / "incoming.docx", self.bundle)

    def test_real_current_manuscript_analysis_preserves_all_live_bindings(self):
        with patch("manuscript.ORIGINAL_SHA", ORIGINAL_SHA):
            source = ROOT / f"source/Heraldry_RC{check(ROOT)['number']}.md"
            original = source.read_bytes()
            # Isolated in-memory input only; never modify or promote the real manuscript.
            incoming = original.replace(b"A competitive GM-less", b"A fixture competitive GM-less", 1)
            report, batch, _, _ = analyse(ROOT, incoming)
        self.assertEqual(report["impact"]["blockers"], [])
        self.assertEqual(report["impact"]["affected_figures"], [])
        self.assertGreater(report["impact"]["anchors_resolved"], 50)
        self.assertEqual(len(batch["patches"]), 1)
        self.assertEqual(source.read_bytes(), original)


class PatchGeneration(unittest.TestCase):
    def test_random_repeated_passages_insertions_deletions_and_simultaneous_title_edits(self):
        rng = random.Random(492)
        marker = "**Release Candidate 492 (RC492)**"
        for iteration in range(120):
            old = [rng.choice(("Repeat.\n", "Other.\n", "\n")) for _ in range(24)]
            new = old[:]
            for _ in range(4):
                n = rng.randrange(len(new) + 1)
                new[n:n + rng.randrange(3)] = [rng.choice(("Repeat.\n", "Changed.\n", "\n")) for _ in range(rng.randrange(3))]
            original = "# Title\n\n" + marker + "\n\n" + "".join(old)
            proposed = "# New title\n\n" + marker + "\n\n" + "".join(new)
            rebuilt = original
            patches = exact_patches(original, proposed, marker)
            for p in patches:
                self.assertEqual(rebuilt.count(p["find"]), 1, iteration)
                self.assertNotIn("Release Candidate", p["find"])
                rebuilt = rebuilt.replace(p["find"], p["replace"])
            self.assertEqual(rebuilt, proposed, iteration)

    def test_developer_front_door_delegates_help_without_building(self):
        result = subprocess.run([sys.executable, "tools/dev.py", "manuscript", "--help"], cwd=ROOT,
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("prepare", result.stdout)
        self.assertIn("apply", result.stdout)


if __name__ == "__main__":
    unittest.main()
