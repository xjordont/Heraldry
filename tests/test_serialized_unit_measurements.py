"""Measurement queries must not hide an unconverged Typst compilation."""
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pypdf

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


class SerializedMeasurements(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "source").mkdir()
        (self.root / "typst").mkdir()
        (self.root / "source/versions.json").write_text('{"revisions": [{"number": 999}]}')
        self.source = self.root / "typst/measure.typ"
        self.source.write_text(SOURCE, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_actual_compile_serializes_unique_measurements_without_query(self):
        rows, binding = measure_units.measure(self.source, self.root)
        self.assertEqual(set(rows), {"one", "two"})
        self.assertGreater(rows["one"]["h1"], 0)
        self.assertEqual(binding["origin"], "measurement-pdf-attachment")
        self.assertFalse(binding["warnings"])

    def pdf(self, rows):
        writer = pypdf.PdfWriter()
        writer.add_blank_page(width=200, height=200)
        writer.add_attachment(measure_units.ATTACHMENT, json.dumps(rows).encode())
        out = io.BytesIO()
        writer.write(out)
        return out.getvalue()

    def test_missing_duplicate_and_nonfinite_measurements_are_rejected(self):
        good = {"id": "one", "h1": 10, "h2": 12}
        for rows, wanted in (([good], ["one", "two"]), ([good, good], ["one"]),
                             ([good | {"h2": float("nan")}], ["one"])):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                measure_units.measurement_rows(self.pdf(rows), wanted)

    def test_nonconvergence_warning_is_not_suppressed_as_a_success(self):
        with patch.object(measure_units.typst, "Compiler") as compiler:
            compiler.return_value.compile_with_warnings.return_value = (b"unusable", ["document did not converge within five attempts"])
            with self.assertRaisesRegex(ValueError, "did not converge"):
                measure_units.measure(self.source, self.root)
            self.assertFalse(compiler.return_value.query.called)

    def test_changed_inputs_during_compile_do_not_publish_measurements(self):
        with patch.object(measure_units, "compilation_identity", side_effect=[{"id": "before"}, {"id": "after"}]), \
             patch.object(measure_units.typst, "Compiler") as compiler:
            compiler.return_value.compile_with_warnings.return_value = (b"unusable", [])
            with self.assertRaisesRegex(ValueError, "changed during"):
                measure_units.measure(self.source, self.root)

    def binding_fixture(self):
        (self.root / "build").mkdir()
        (self.root / "typst/content.typ").write_text("Current generated book")
        rows, binding = measure_units.measure(self.source, self.root)
        (self.root / "build/unit_measure.json").write_text(json.dumps(rows))
        (self.root / "build/unit_measure.binding.json").write_text(json.dumps(binding))
        units = {"expected_unit_ids": list(rows),
                 "units": [{"id": key, **value} for key, value in rows.items()]}
        return units, {"identity": compilation_identity(self.root)}

    def test_final_pdf_and_measurement_have_identical_full_input_identity(self):
        units, final_binding = self.binding_fixture()
        self.assertEqual(validate_measurement_binding(units, final_binding, self.root)["units"], 2)

    def test_changed_height_cannot_turn_an_avoidable_split_into_overheight(self):
        units, final_binding = self.binding_fixture()
        units["units"][0]["h2"] = 1000000
        with self.assertRaisesRegex(ValueError, "audit heights differ"):
            validate_measurement_binding(units, final_binding, self.root)

    def test_stale_measurement_file_or_input_identity_is_rejected(self):
        units, final_binding = self.binding_fixture()
        path = self.root / "build/unit_measure.json"
        original = path.read_bytes()
        rows = json.loads(original)
        rows["one"]["h1"] = 99999
        path.write_text(json.dumps(rows))
        with self.assertRaisesRegex(ValueError, "heights differ from serialized"):
            validate_measurement_binding(units, final_binding, self.root)
        path.write_bytes(original)
        final_binding["identity"]["input_sha256"] = "wrong fingerprint"
        with self.assertRaisesRegex(ValueError, "final PDF inputs"):
            validate_measurement_binding(units, final_binding, self.root)


if __name__ == "__main__":
    unittest.main()
