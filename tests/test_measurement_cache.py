"""Whole-export caching must retain the serialized-PDF measurement evidence."""
import hashlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pypdf
import typst

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import measure_units
from keep_audit import validate_measurement_binding
from pdf_positions import compilation_identity


SOURCE = '''#set page(width: 200pt, height: 200pt, margin: 20pt)
#let munit(id, body) = context {
  let h = measure(block(width: 120pt, body)).height.pt()
  [#metadata((id: id, h1: h, h2: h)) <um>]
}
#munit("one", [Readable rules.])
#munit("two", [More rules.])
#context {
  pdf.attach("/heraldry-unit-measurements.json", bytes(json.encode(query(<um>).map(m => m.value))), mime-type: "application/json")
}
'''


class WholeMeasurementCache(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for folder in ("typst", "source", "config", "build"):
            (self.root / folder).mkdir()
        (self.root / "source/versions.json").write_text('{"revisions":[{"number":999}]}', encoding="utf-8")
        self.manuscript = self.root / "source/current.md"
        self.manuscript.write_text("Current manuscript.", encoding="utf-8")
        self.style = self.root / "config/design_tokens.json"
        self.style.write_text('{"body":10.5}', encoding="utf-8")
        self.source = self.root / "typst/measure.typ"
        self.source.write_text(SOURCE, encoding="utf-8")

    def measure(self, **kwargs):
        return measure_units.measure(self.source, self.root, **kwargs)

    def entry(self, evidence):
        return Path(evidence["cache"]["path"])

    def read_envelope(self, evidence):
        return json.loads((self.entry(evidence) / "evidence.json").read_bytes())

    def write_envelope(self, evidence, envelope):
        (self.entry(evidence) / "evidence.json").write_text(json.dumps(envelope), encoding="utf-8")

    def test_real_pdf_hit_reextracts_without_compiling_and_retains_binding(self):
        rows, fresh = self.measure()
        self.assertEqual(fresh["cache"]["status"], "miss")
        self.assertTrue(fresh["cache"]["stored"])
        entry = self.entry(fresh)
        self.assertEqual(hashlib.sha256((entry / "measurement.pdf").read_bytes()).hexdigest(), fresh["measurement_pdf_sha256"])
        self.assertNotIn("rows", self.read_envelope(fresh))
        with patch.object(measure_units.typst, "Compiler", side_effect=AssertionError("cache hit compiled")), \
             patch.object(measure_units, "measurement_rows", wraps=measure_units.measurement_rows) as extract:
            cached_rows, hit = self.measure()
        extract.assert_called_once()
        self.assertEqual(rows, cached_rows)
        self.assertEqual(hit["cache"]["status"], "hit")
        self.assertEqual(hit["compile_seconds"], 0)
        self.assertEqual(hit["cached_compile_seconds"], self.read_envelope(fresh)["evidence"]["seconds"])
        for key in ("origin", "identity", "measurement_pdf_sha256", "measurements_sha256", "units", "warnings"):
            self.assertEqual(fresh[key], hit[key])
        (self.root / "build/unit_measure.json").write_text(json.dumps(cached_rows), encoding="utf-8")
        (self.root / "build/unit_measure.binding.json").write_text(json.dumps(hit), encoding="utf-8")
        units = {"expected_unit_ids": list(rows), "units": [{"id": k, **v} for k, v in rows.items()]}
        self.assertEqual(validate_measurement_binding(units, {"identity": compilation_identity(self.root, content=self.source)}, self.root), hit)

    def test_changed_manuscript_style_and_generated_source_each_compile_again(self):
        _, before = self.measure()
        for path, suffix in ((self.manuscript, "\nNew manuscript paragraph."),
                             (self.style, "\n "), (self.source, "\n// Generated source changed.\n")):
            with self.subTest(path=path.name):
                path.write_text(path.read_text(encoding="utf-8") + suffix, encoding="utf-8")
                with patch.object(measure_units.typst, "Compiler", wraps=typst.Compiler) as compiler:
                    _, after = self.measure()
                self.assertEqual(compiler.call_count, 1)
                self.assertEqual(after["cache"]["status"], "miss")
                self.assertNotEqual(before["cache"]["key"], after["cache"]["key"])
                self.assertNotEqual(before["identity"], after["identity"])
                before = after

    def test_cache_survives_removing_only_build_outputs(self):
        _, fresh = self.measure()
        shutil.rmtree(self.root / "build")
        self.assertTrue(self.entry(fresh).exists())
        with patch.object(measure_units.typst, "Compiler", side_effect=AssertionError("clean destroyed cache")):
            _, hit = self.measure()
        self.assertEqual(hit["cache"]["status"], "hit")

    def test_bypass_compiles_and_neither_reads_nor_writes_cache(self):
        _, fresh = self.measure()
        entry = self.entry(fresh)
        original = {p.name: p.read_bytes() for p in entry.iterdir()}
        with patch.object(measure_units, "load_cache", side_effect=AssertionError("bypass read cache")), \
             patch.object(measure_units, "save_cache", side_effect=AssertionError("bypass wrote cache")), \
             patch.object(measure_units.typst, "Compiler", wraps=typst.Compiler) as compiler:
            _, bypass = self.measure(use_cache=False)
        self.assertEqual(compiler.call_count, 1)
        self.assertEqual(bypass["cache"]["status"], "bypass")
        self.assertFalse(bypass["cache"]["stored"])
        self.assertEqual(original, {p.name: p.read_bytes() for p in entry.iterdir()})

    def test_damaged_pdf_or_envelope_is_rejected_then_recompiled(self):
        _, fresh = self.measure()
        entry = self.entry(fresh)
        corruptions = ("pdf bytes", "missing pdf", "invalid json", "identity", "key", "warnings", "digest")
        for damage in corruptions:
            with self.subTest(damage=damage):
                envelope = self.read_envelope(fresh)
                if damage == "pdf bytes":
                    (entry / "measurement.pdf").write_bytes(b"damaged PDF")
                elif damage == "missing pdf":
                    (entry / "measurement.pdf").unlink()
                elif damage == "invalid json":
                    (entry / "evidence.json").write_text("{", encoding="utf-8")
                else:
                    if damage == "identity": envelope["evidence"]["identity"]["input_sha256"] = "changed"
                    if damage == "key": envelope["key"] = "wrong"
                    if damage == "warnings": envelope["evidence"]["warnings"] = ["document did not converge"]
                    if damage == "digest": envelope["evidence"]["measurements_sha256"] = "wrong"
                    self.write_envelope(fresh, envelope)
                with patch.object(measure_units.typst, "Compiler", wraps=typst.Compiler) as compiler:
                    _, repaired = self.measure()
                self.assertEqual(compiler.call_count, 1)
                self.assertEqual(repaired["cache"]["status"], "miss")
                self.assertIn("rejected entry", repaired["cache"]["reason"])
                self.assertTrue(repaired["cache"]["stored"])

    def test_changed_attachment_with_rehashed_pdf_cannot_reuse_cached_heights(self):
        rows, fresh = self.measure()
        entry = self.entry(fresh)
        reader = pypdf.PdfReader(io.BytesIO((entry / "measurement.pdf").read_bytes()))
        payload = json.loads(reader.attachments[measure_units.ATTACHMENT][0])
        payload[0]["h1"] += 100
        writer = pypdf.PdfWriter()
        writer.clone_document_from_reader(reader)
        writer.root_object["/Names"].get_object().pop("/EmbeddedFiles", None)
        writer.add_attachment(measure_units.ATTACHMENT, json.dumps(payload).encode())
        buffer = io.BytesIO()
        writer.write(buffer)
        changed_pdf = buffer.getvalue()
        (entry / "measurement.pdf").write_bytes(changed_pdf)
        envelope = self.read_envelope(fresh)
        envelope["evidence"]["measurement_pdf_sha256"] = hashlib.sha256(changed_pdf).hexdigest()
        self.write_envelope(fresh, envelope)
        with patch.object(measure_units.typst, "Compiler", wraps=typst.Compiler) as compiler:
            repaired_rows, repaired = self.measure()
        self.assertEqual(compiler.call_count, 1)
        self.assertEqual(rows, repaired_rows)
        self.assertIn("attachment differs", repaired["cache"]["reason"])

    def test_nonconvergence_failure_and_other_warnings_never_write_entries(self):
        _, original = self.measure(use_cache=False)
        compiler = typst.Compiler(str(self.source), root=str(self.root), ignore_system_fonts=True)
        pdf, warnings = compiler.compile_with_warnings(timestamp=original["identity"]["timestamp"])
        self.assertFalse(warnings)
        for warning in ("document did not converge after five attempts", "font fallback warning"):
            with self.subTest(warning=warning), patch.object(measure_units.typst, "Compiler") as fake:
                fake.return_value.compile_with_warnings.return_value = (pdf, [warning])
                if "converge" in warning:
                    with self.assertRaisesRegex(ValueError, "did not converge"):
                        self.measure()
                else:
                    _, evidence = self.measure()
                    self.assertFalse(evidence["cache"]["stored"])
                    self.assertEqual(evidence["cache"]["write_skipped"], "compiler warnings")
                self.assertFalse((self.root / measure_units.CACHE_DIRECTORY).exists())

    def test_inputs_changing_during_hit_fail_instead_of_returning_stale_rows(self):
        self.measure()
        original = measure_units.load_cache
        def concurrent_change(*args):
            result = original(*args)
            self.manuscript.write_text("Inputs changed while reading cache.", encoding="utf-8")
            return result
        with patch.object(measure_units, "load_cache", side_effect=concurrent_change), \
             patch.object(measure_units.typst, "Compiler", side_effect=AssertionError("stale hit compiled")):
            with self.assertRaisesRegex(ValueError, "changed during"):
                self.measure()

    def test_cache_write_failure_preserves_valid_compile_evidence(self):
        with patch.object(measure_units, "save_cache", side_effect=PermissionError("cache read-only")):
            rows, evidence = self.measure()
        self.assertEqual(set(rows), {"one", "two"})
        self.assertFalse(evidence["cache"]["stored"])
        self.assertIn("read-only", evidence["cache"]["write_error"])
        self.assertFalse(evidence["warnings"])


if __name__ == "__main__":
    unittest.main()
