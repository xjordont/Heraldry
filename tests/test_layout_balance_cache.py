"""Persisted balance hints never replace measurement or layout recomputation."""
import copy
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import layout_balance_cache as hints


class LayoutBalanceHints(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.key = "a" * 64
        self.pdf_bytes = b"fixture measurement export bytes; only the hash is used by the hint module"
        self.binding = {
            "origin": "measurement-pdf-attachment", "warnings": [], "units": 2,
            "identity": {"schema": 1, "content_sha256": "b" * 64,
                         "input_sha256": "c" * 64, "variant": "cream", "edition": "print",
                         "compiler": "0.15.0", "timestamp": 1792105845},
            "measurement_pdf_sha256": hashlib.sha256(self.pdf_bytes).hexdigest(),
            "measurements_sha256": "d" * 64,
            "cache": {"status": "miss", "key": self.key, "stored": True},
        }
        self.entry = self.root / hints.CACHE_DIRECTORY / self.key
        self.entry.mkdir(parents=True)
        (self.entry / "measurement.pdf").write_bytes(self.pdf_bytes)
        self.measurement_envelope = {"schema": 1, "key": self.key,
                                     "evidence": copy.deepcopy(self.binding)}
        self.write_measurement()
        self.balance = {"0": ["v2:" + "1" * 64, 0],
                        "1": ["v2:" + "2" * 64, 21], "7": ["v2:" + "3" * 64, 0]}
        self.target = self.entry / "balance.json"

    def write_measurement(self):
        (self.entry / "evidence.json").write_text(json.dumps(self.measurement_envelope), encoding="utf-8")

    def save(self, balance=None, **kwargs):
        return hints.save_hint(self.root, self.binding, self.balance if balance is None else balance, **kwargs)

    def payload(self):
        return json.loads(self.target.read_bytes())

    def write_hint(self, payload, *, rehash=True):
        if rehash:
            payload.pop("hint_sha256", None)
            payload["hint_sha256"] = hashlib.sha256(hints._canonical(payload)).hexdigest()
        self.target.write_text(json.dumps(payload), encoding="utf-8")

    def test_roundtrip_is_only_a_plan_with_observable_hit_status(self):
        status = self.save()
        self.assertEqual(status["status"], "stored")
        diagnostics = []
        # A subsequent measurement-cache hit may have different runtime metrics.
        binding = copy.deepcopy(self.binding)
        binding["cache"].update(status="hit", stored=False)
        binding.update(seconds=0.1, compile_seconds=0.0)
        with self.assertLogs(hints.LOG, level="INFO") as logs:
            loaded = hints.load_hint(self.root, binding, diagnostics=diagnostics)
        self.assertEqual(loaded, self.balance)
        self.assertEqual(diagnostics[0]["status"], "hit")
        self.assertIn("recomputation required", diagnostics[0]["reason"])
        self.assertIn("hit", logs.output[0])
        self.assertEqual(set(self.payload()), {"schema", "key", "converged", "identity",
            "measurement_pdf_sha256", "measurements_sha256", "balance", "hint_sha256"})
        self.assertEqual(set(self.entry.iterdir()), {self.target, self.entry / "measurement.pdf", self.entry / "evidence.json"})

    def test_survives_build_deletion_and_same_key_transfer_to_another_checkout(self):
        self.save()
        (self.root / "build").mkdir()
        (self.root / "build/balance.json").write_text("ephemeral")
        shutil.rmtree(self.root / "build")
        self.assertEqual(hints.load_hint(self.root, self.binding), self.balance)
        other = self.root / "other-checkout"
        shutil.copytree(self.root / ".cache", other / ".cache")
        self.assertEqual(hints.load_hint(other, self.binding), self.balance)

    def test_missing_entry_is_a_nonfatal_diagnosed_miss(self):
        diagnostics = []
        self.assertEqual(hints.load_hint(self.root, self.binding, diagnostics=diagnostics), {})
        self.assertEqual(diagnostics[0]["status"], "miss")
        self.assertTrue(diagnostics[0]["reason"])
        (self.entry / "evidence.json").unlink()
        self.assertEqual(self.save()["status"], "skipped")
        self.assertFalse(self.target.exists())

    def test_full_identity_drift_is_never_rebound_to_a_previous_hint(self):
        self.save()
        for key, changed in (("content_sha256", "1" * 64), ("input_sha256", "2" * 64),
                             ("compiler", "0.16.0"), ("timestamp", 1),
                             ("variant", "white"), ("edition", "digital")):
            with self.subTest(key=key):
                binding = copy.deepcopy(self.binding)
                binding["identity"][key] = changed
                self.assertEqual(hints.load_hint(self.root, binding), {})
                self.assertEqual(hints.save_hint(self.root, binding, self.balance)["status"], "skipped")
        # Even if measurement evidence matches a new identity under the same key,
        # the old hint must match that full identity as well.
        self.binding["identity"]["input_sha256"] = "3" * 64
        self.measurement_envelope["evidence"] = copy.deepcopy(self.binding)
        self.write_measurement()
        self.assertEqual(hints.load_hint(self.root, self.binding), {})

    def test_warning_failure_and_bypass_cannot_overwrite_good_hint(self):
        self.save()
        original = self.target.read_bytes()
        for kwargs in ({"converged": False}, {"warnings": ["document did not converge"]},
                       {"warnings": ["font fallback"]}):
            with self.subTest(kwargs=kwargs):
                self.assertEqual(self.save(**kwargs)["status"], "skipped")
                self.assertEqual(original, self.target.read_bytes())
        for change in ({"warnings": ["document did not converge"]}, {"cache": {"status": "bypass", "key": self.key}}):
            binding = copy.deepcopy(self.binding)
            binding.update(change)
            self.assertEqual(hints.load_hint(self.root, binding), {})
            self.assertEqual(hints.save_hint(self.root, binding, self.balance)["status"], "skipped")
            self.assertEqual(original, self.target.read_bytes())

    def test_invalid_cache_keys_and_partial_identity_miss_without_external_io(self):
        self.save()
        for key in ("../outside", "a" * 63, "A" * 64, None, True):
            with self.subTest(key=key), patch.object(Path, "read_bytes", side_effect=AssertionError("invalid key performed cache IO")):
                binding = copy.deepcopy(self.binding)
                binding["cache"]["key"] = key
                self.assertEqual(hints.load_hint(self.root, binding), {})
                self.assertEqual(hints.save_hint(self.root, binding, self.balance)["status"], "skipped")
        for key in self.binding["identity"]:
            binding = copy.deepcopy(self.binding)
            del binding["identity"][key]
            self.assertEqual(hints.load_hint(self.root, binding), {})

    def test_invalid_balance_structure_is_rejected_even_with_correct_digest(self):
        signature = "v2:" + "1" * 64
        invalid = ([], {"x": [signature, 0]}, {"-1": [signature, 0]},
                   {"01": [signature, 0]}, {"0": [signature, True]},
                   {"0": [signature, -1]}, {"0": [signature, 1.0]},
                   {"0": ["", 1]}, {"0": ["fake-hash", 1]},
                   {"0": ["B00600:5", 0]}, {"0": [signature, 1, 2]},
                   {"0": ["v2:" + "A" * 64, 0]}, {"0": ["v2:" + "1" * 63, 0]},
                   {"0": ["v1:" + "1" * 64, 0]}, {"0": [12, 1]}, {"0": None})
        self.save()
        original = self.payload()
        for balance in invalid:
            with self.subTest(balance=balance):
                self.assertEqual(hints.save_hint(self.root, self.binding, balance)["status"], "skipped")
                payload = copy.deepcopy(original)
                payload["balance"] = balance
                self.write_hint(payload)
                self.assertEqual(hints.load_hint(self.root, self.binding), {})

    def test_corrupted_envelope_schema_or_digest_is_a_safe_miss(self):
        self.save()
        original = self.payload()
        for field, value in (("schema", 2), ("schema", True), ("key", "e" * 64),
                             ("converged", False), ("measurement_pdf_sha256", "f" * 64),
                             ("measurements_sha256", "f" * 64), ("identity", {})):
            with self.subTest(field=field):
                payload = copy.deepcopy(original)
                payload[field] = value
                self.write_hint(payload)
                self.assertEqual(hints.load_hint(self.root, self.binding), {})
        self.write_hint(original)
        payload = self.payload()
        payload["balance"]["1"][1] = 10
        self.write_hint(payload, rehash=False)
        self.assertEqual(hints.load_hint(self.root, self.binding), {})
        self.target.write_text("{", encoding="utf-8")
        self.assertEqual(hints.load_hint(self.root, self.binding), {})

    def test_damaged_measurement_pdf_or_evidence_cannot_supply_hint(self):
        self.save()
        original = self.target.read_bytes()
        (self.entry / "measurement.pdf").write_bytes(b"damaged")
        self.assertEqual(hints.load_hint(self.root, self.binding), {})
        self.assertEqual(self.save()["status"], "skipped")
        self.assertEqual(original, self.target.read_bytes())
        (self.entry / "measurement.pdf").write_bytes(self.pdf_bytes)
        self.measurement_envelope["evidence"]["measurements_sha256"] = "0" * 64
        self.write_measurement()
        self.assertEqual(hints.load_hint(self.root, self.binding), {})

    def test_nonfatal_read_and_atomic_write_errors_are_diagnosed(self):
        self.save()
        original = self.target.read_bytes()
        diagnostics = []
        with patch.object(Path, "read_bytes", side_effect=PermissionError("read denied")):
            self.assertEqual(hints.load_hint(self.root, self.binding, diagnostics=diagnostics), {})
        self.assertIn("read denied", diagnostics[0]["reason"])
        with patch.object(Path, "replace", side_effect=PermissionError("write denied")):
            result = self.save()
        self.assertEqual(result["status"], "error")
        self.assertIn("write denied", result["reason"])
        self.assertEqual(original, self.target.read_bytes())
        self.assertFalse(list(self.entry.glob(".balance-*")))


if __name__ == "__main__":
    unittest.main()
