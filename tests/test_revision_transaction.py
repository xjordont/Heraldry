"""Manuscript promotion is stale-safe and rolls back interrupted writes."""
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import revise_manuscript
from manuscript import check


class RevisionTransaction(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.original = "# Test manuscript\n\n**Release Candidate 484 (RC484)**\n\nOwner text: café.\n"
        source = self.root / "source/Heraldry_RC484.md"
        source.parent.mkdir()
        source.write_bytes(self.original.encode("utf-8"))
        self.base_sha = hashlib.sha256(source.read_bytes()).hexdigest()
        self.authority = patch("manuscript.ORIGINAL_SHA", self.base_sha)
        self.authority.start()
        self.addCleanup(self.authority.stop)
        self.config_path = self.root / "config/production.json"
        self.registry_path = self.root / "source/versions.json"
        self.write_json(self.config_path, {
            "source": "source/Heraldry_RC484.md",
            "verified_publication_metadata": {"version": "Release Candidate 484 (RC484)"},
        })
        self.write_json(self.registry_path, {"current": 484, "revisions": [{
            "number": 484, "path": "source/Heraldry_RC484.md", "sha256": self.base_sha,
            "bytes": len(source.read_bytes()), "reason": "Synthetic fixture only",
        }]})
        self.write_json(self.root / "editorial/patches.json", {"patches": []})
        self.proposal = self.root / "proposal.json"
        self.batch = {"base_sha256": self.base_sha, "patches": [{
            "id": "TEST-01", "status": "approved", "find": "Owner text: café.",
            "replace": "Owner text: café, updated.", "expected_count": 1,
        }]}
        self.write_json(self.proposal, self.batch)

    @staticmethod
    def write_json(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        # Deliberately use CRLF metadata so rollback must preserve bytes, not reserialize.
        path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + "\n").replace("\n", "\r\n").encode("utf-8"))

    def snapshot(self):
        return {path.relative_to(self.root).as_posix(): path.read_bytes()
                for path in self.root.rglob("*") if path.is_file()}

    def revise(self):
        return revise_manuscript.revise(self.root, self.proposal, "Fixture update", "Synthetic owner decision")

    def assert_original(self, expected):
        self.assertEqual(self.snapshot(), expected)
        self.assertEqual(check(self.root)["number"], 484)

    def test_success_archives_exact_batch_and_uses_utf8_lf_metadata(self):
        original_source = (self.root / "source/Heraldry_RC484.md").read_bytes()
        evidence = self.proposal.read_bytes()
        result = self.revise()
        self.assertEqual(result, check(self.root))
        self.assertEqual(result["number"], 485)
        self.assertEqual((self.root / result["patch_file"]).read_bytes(), evidence)
        self.assertEqual((self.root / "source/Heraldry_RC484.md").read_bytes(), original_source)
        self.assertIn("café, updated.", (self.root / result["path"]).read_text(encoding="utf-8"))
        for path in (self.config_path, self.registry_path):
            self.assertNotIn(b"\r", path.read_bytes())
            self.assertTrue(path.read_bytes().endswith(b"\n"))
        self.assertFalse(list(self.root.rglob("*.tmp")))
        self.assertFalse((self.root / "source/.revision.lock").exists())

    def test_historical_batches_without_base_hash_still_work(self):
        del self.batch["base_sha256"]
        self.batch["patches"][0]["status"] = "applied"
        self.write_json(self.proposal, self.batch)
        self.assertEqual(self.revise()["number"], 485)

    def test_stale_hash_is_rejected_before_writes(self):
        self.batch["base_sha256"] = "0" * 64
        self.write_json(self.proposal, self.batch)
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "base_sha256"):
            self.revise()
        self.assert_original(before)

    def test_boolean_match_count_is_not_an_integer_count(self):
        self.batch["patches"][0]["expected_count"] = True
        self.write_json(self.proposal, self.batch)
        before = self.snapshot()
        with self.assertRaises(ValueError):
            self.revise()
        self.assert_original(before)

    def test_imported_candidate_hash_is_enforced_before_writes(self):
        self.batch["import"] = {"candidate_sha256": "0" * 64}
        self.write_json(self.proposal, self.batch)
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "reviewed manuscript hash"):
            self.revise()
        self.assert_original(before)

    def test_invalid_original_state_prevents_promotion(self):
        value = json.loads(self.config_path.read_bytes())
        value["source"] = "source/Heraldry_RC999.md"
        self.write_json(self.config_path, value)
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "configuration differs"):
            self.revise()
        self.assertEqual(self.snapshot(), before)

    def test_metadata_replace_failures_restore_all_original_bytes(self):
        real_replace = os.replace
        for failed_name in ("production.json", "versions.json"):
            with self.subTest(failed_name=failed_name):
                before = self.snapshot()
                failed = False

                def fail_once(source, destination):
                    nonlocal failed
                    if Path(destination).name == failed_name and not failed:
                        failed = True
                        raise OSError("Simulated metadata write failure")
                    return real_replace(source, destination)

                with patch("revise_manuscript.os.replace", side_effect=fail_once):
                    with self.assertRaisesRegex(OSError, "Simulated metadata"):
                        self.revise()
                self.assertTrue(failed)
                self.assert_original(before)

    def test_evidence_publish_failure_removes_new_snapshot(self):
        real_link = os.link
        before = self.snapshot()

        def fail_evidence(source, destination):
            if Path(destination).name == "RC485.json":
                raise OSError("Simulated evidence write failure")
            return real_link(source, destination)

        with patch("revise_manuscript.os.link", side_effect=fail_evidence):
            with self.assertRaisesRegex(OSError, "Simulated evidence"):
                self.revise()
        self.assert_original(before)

    def test_final_validation_failure_rolls_back_entire_revision(self):
        real_check = revise_manuscript.check
        before = self.snapshot()

        def fail_after_publication(root):
            result = real_check(root)
            if result["number"] == 485:
                raise ValueError("Simulated final validation failure")
            return result

        with patch("revise_manuscript.check", side_effect=fail_after_publication):
            with self.assertRaisesRegex(ValueError, "Simulated final"):
                self.revise()
        self.assert_original(before)

    def test_staging_failure_leaves_no_transaction_files(self):
        real_stage = revise_manuscript._stage_bytes
        before = self.snapshot()

        def fail_staging(path, data):
            if path == self.registry_path:
                raise OSError("Simulated staging failure")
            return real_stage(path, data)

        with patch("revise_manuscript._stage_bytes", side_effect=fail_staging):
            with self.assertRaisesRegex(OSError, "Simulated staging"):
                self.revise()
        self.assert_original(before)

    def test_failed_rollback_retains_lock_and_recovery_bytes(self):
        real_replace = os.replace
        config_bytes = self.config_path.read_bytes()

        def fail_metadata(source, destination):
            if Path(destination) == self.registry_path:
                raise OSError("Simulated registry publish failure")
            if Path(destination) == self.config_path and Path(source).read_bytes() == config_bytes:
                raise OSError("Simulated rollback failure")
            return real_replace(source, destination)

        with patch("revise_manuscript.os.replace", side_effect=fail_metadata):
            with self.assertRaisesRegex(revise_manuscript.RevisionRecoveryError, "lock and recovery files retained"):
                self.revise()
        self.assertTrue((self.root / "source/.revision.lock").is_file())
        self.assertTrue(any(p.read_bytes() == config_bytes for p in self.root.rglob("*.tmp")))
        with self.assertRaisesRegex(ValueError, "interrupted transaction"):
            self.revise()

    def test_preexisting_snapshot_and_evidence_are_never_overwritten(self):
        for relative in ("source/Heraldry_RC485.md", "editorial/history/RC485.json"):
            with self.subTest(relative=relative):
                path = self.root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"Existing owner data")
                before = self.snapshot()
                with self.assertRaisesRegex(ValueError, "never overwrite"):
                    self.revise()
                self.assert_original(before)
                path.unlink()

    def test_existing_lock_is_preserved_and_refuses_concurrent_revision(self):
        lock = self.root / "source/.revision.lock"
        lock.write_bytes(b"Another owner transaction\n")
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "Another revision"):
            self.revise()
        self.assert_original(before)


if __name__ == "__main__":
    unittest.main()
