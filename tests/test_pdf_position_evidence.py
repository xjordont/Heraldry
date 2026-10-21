"""Real serialized-PDF regressions: a hash of a later query is not evidence."""
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

import pypdf
import typst

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from pdf_positions import compilation_identity, read_positions, validate_sidecar, ATTACHMENT
from keep_audit import analyze_units


FIXTURE = '''#set page(width: 300pt, height: 300pt, margin: 30pt)
= C.5 Reactions Summary <h-c5>
#context [#metadata((id: "UNIT1", edge: "s", page: here().page())) <um-pos>]
First section's complete text. See #link(<tbl-T327>)[reaction table].
#context [#metadata((id: "UNIT1", edge: "e", page: here().page())) <um-pos>]
#pagebreak()
= C.6 Critical Hits <h-c6>
#metadata("T327") <tbl-T327>
#context [#metadata((id: "T327", edge: "s", page: here().page())) <tblpos>]
#table(columns: (1fr, 1fr), [Reaction], [Cost], [Brace], [0 AP])
#context [#metadata((id: "T327", edge: "e", page: here().page())) <tblpos>]
#context {
  let headings = query(heading).map(h => (id: str(h.label), page: h.location().page()))
  pdf.attach("/heraldry-positions.json", bytes(json.encode((
    schema: 1, identity: json(bytes(sys.inputs.at("position-identity"))),
    positions: ("<pm>": (), "<tblpos>": query(<tblpos>).map(m => m.value),
      "<ixpos>": (), "<hpos>": (headings,), "<um-pos>": query(<um-pos>).map(m => m.value)),
  ))), mime-type: "application/json")
}
'''


class ExactPdfPositions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for name in ("typst", "source", "config"):
            (self.root / name).mkdir()
        (self.root / "source/versions.json").write_text(json.dumps({"revisions": [{"number": 999}]}))
        self.content = self.root / "typst/content.typ"
        self.content.write_text(FIXTURE, encoding="utf-8")
        self.style = self.root / "config/design_tokens.json"
        self.style.write_text('{"body": 10.5}')
        self.pdf = self.root / "fixture.pdf"
        identity = compilation_identity(self.root)
        typst.compile(str(self.content), output=str(self.pdf), timestamp=identity["timestamp"],
                      root=str(self.root), ignore_system_fonts=True,
                      sys_inputs={"position-identity": json.dumps(identity)})

    def tearDown(self):
        self.tmp.cleanup()

    def test_export_attachment_matches_actual_pages_and_named_destinations(self):
        positions = read_positions(self.pdf, root=self.root)
        self.assertEqual(positions["binding"]["pdf_pages"], 2)
        anchors = positions["binding"]["serialized_anchors"]
        self.assertGreaterEqual(anchors["checked"], 2)
        self.assertFalse(anchors["missing"] or anchors["mismatches"])
        self.assertEqual(positions["<hpos>"][0][0]["page"], 1)
        self.assertEqual(positions["<tblpos>"][0]["page"], 2)
        self.assertEqual(validate_sidecar(positions, self.pdf, root=self.root), positions)

    def test_new_style_or_asset_input_invalidates_old_position_evidence(self):
        self.style.write_text('{"body": 10}')
        with self.assertRaisesRegex(ValueError, "current source/style/font/asset"):
            read_positions(self.pdf, root=self.root)

    def test_new_generated_content_invalidates_old_position_evidence(self):
        self.content.write_text(FIXTURE + "\nChanged rules text.")
        with self.assertRaisesRegex(ValueError, "current source/style/font/asset"):
            read_positions(self.pdf, root=self.root)

    def test_wrong_variant_cannot_reuse_print_positions(self):
        with self.assertRaisesRegex(ValueError, "variant/edition"):
            read_positions(self.pdf, root=self.root, variant="white")

    def test_a_later_query_with_matching_pdf_hash_is_rejected(self):
        positions = read_positions(self.pdf, root=self.root)
        positions["<um-pos>"][0]["page"] = 2
        with self.assertRaisesRegex(ValueError, "differs from the exact PDF"):
            validate_sidecar(positions, self.pdf, root=self.root)

    def test_attachment_heading_shift_is_detected_by_serialized_destination(self):
        reader = pypdf.PdfReader(self.pdf)
        payload = json.loads(reader.attachments[ATTACHMENT][0])
        payload["positions"]["<hpos>"][0][0]["page"] = 2
        writer = pypdf.PdfWriter()
        writer.clone_document_from_reader(reader)
        writer.root_object["/Names"].get_object().pop("/EmbeddedFiles", None)
        writer.add_attachment(ATTACHMENT, json.dumps(payload).encode())
        bad = self.root / "changed-attachment.pdf"
        writer.write(bad)
        with self.assertRaisesRegex(ValueError, "anchors disagree"):
            read_positions(bad, root=self.root)

    def test_legacy_hash_only_query_cannot_validate_pdf_without_attachment(self):
        writer = pypdf.PdfWriter()
        writer.add_blank_page(width=300, height=300)
        bad = self.root / "legacy.pdf"
        writer.write(bad)
        with self.assertRaisesRegex(ValueError, "exactly one serialized"):
            read_positions(bad, root=self.root)


class IndependentKeepCoverage(unittest.TestCase):
    def inventory(self):
        return {"frame_fit_pt": 100, "expected_unit_ids": ["UNIT"],
                "source_unit_manifest": [{"id": "UNIT", "kind": "section"}],
                "units": [{"id": "UNIT", "kind": "section", "class": "page", "h1": 10, "h2": 10}]}

    def positions(self, start=1, end=1):
        return {"<um-pos>": [{"id": "UNIT", "edge": "s", "page": start},
                              {"id": "UNIT", "edge": "e", "page": end}]}

    def test_source_unit_missing_from_both_measurement_and_markers_cannot_pass(self):
        u = self.inventory()
        u["units"] = []
        result = analyze_units(u, {"<um-pos>": []}, 2)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["missing_coverage"], ["UNIT"])
        self.assertEqual(result["source_coverage_errors"][0]["measured_count"], 0)

    def test_duplicate_unit_and_missing_measurement_fail_closed(self):
        u = self.inventory()
        u["units"] *= 2
        u["units"][0]["h2"] = None
        result = analyze_units(u, self.positions(), 2)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(result["source_coverage_errors"])
        self.assertTrue(result["measurement_errors"])

    def test_fit_capable_split_fails_and_overheight_is_explained(self):
        u = self.inventory()
        result = analyze_units(u, self.positions(end=2), 2)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(len(result["avoidable_splits"]), 1)
        u["units"][0].update(h1=150, h2=140)
        result = analyze_units(u, self.positions(end=2), 2)
        self.assertEqual(result["status"], "PASS")
        self.assertIn("child units audited separately", result["over_height"][0]["reason"])

    def test_off_pdf_page_and_missing_source_manifest_fail(self):
        u = self.inventory()
        del u["source_unit_manifest"]
        result = analyze_units(u, self.positions(end=3), 2)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(result["malformed_markers"])
        self.assertTrue(result["source_coverage_errors"])


if __name__ == "__main__":
    unittest.main()
