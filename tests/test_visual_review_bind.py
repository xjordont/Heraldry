"""A review cannot release a defect or invent missing page coverage."""
import contextlib
import copy
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import visual_review_bind as bind


class VisualReviewBinding(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.images = self.root / "production/qa/review"
        self.images.mkdir(parents=True)
        self.ledger = self.root / "production/qa/visual-review.json"
        self.review_path = self.root / "review.json"

        def image(name, **fields):
            data = ("fixture image: " + name).encode("utf-8")
            (self.images / name).write_bytes(data)
            return {"file": name, "sha256": hashlib.sha256(data).hexdigest(), **fields}

        self.manifest = {
            "pdf": "Heraldry_fixture_inkjet-borderless.pdf", "pdf_sha256": "a" * 64, "pages": 3,
            "sheets": [image("sheet-01.jpg", pages=[1, 2]), image("sheet-02.jpg", pages=[3, 3])],
            "details": [image("page-0001.jpg", page=1), image("page-0003.jpg", page=3)],
            "covers": [image("cover-front.jpg", role="front"), image("cover-back.jpg", role="back")],
            "calibration": image("calibration.jpg"),
        }
        observation = "The full image was inspected for clipping, missing content, and overlapping text."
        self.review = {"reviewer": "Fixture reviewer", "calibration": {"observations": observation}}
        for kind in ("sheets", "details", "covers"):
            self.review[kind] = [{"file": image["file"], "observations": observation}
                                 for image in self.manifest[kind]]
        status = {"result": "CANDIDATE_READY", "request_id": "fixture",
                  "pdfs": {self.manifest["pdf"]: {"sha256": self.manifest["pdf_sha256"]}}}
        (self.root / "production/BUILD_STATUS.json").write_text(json.dumps(status), encoding="utf-8")

    def invoke(self, review=None, manifest=None):
        self.review_path.write_text(json.dumps(review if review is not None else self.review), encoding="utf-8")
        (self.images / "manifest.json").write_text(
            json.dumps(manifest if manifest is not None else self.manifest), encoding="utf-8")
        with patch.object(bind, "ROOT", self.root), patch.object(bind, "REVIEW", self.images), \
                patch.object(sys, "argv", ["visual_review_bind.py", "bind", "--review", str(self.review_path)]), \
                contextlib.redirect_stdout(io.StringIO()):
            bind.main()

    def assert_refused(self, review=None, manifest=None):
        before = self.ledger.read_bytes() if self.ledger.exists() else None
        with self.assertRaises(SystemExit) as caught:
            self.invoke(review, manifest)
        self.assertEqual(caught.exception.code, 2)
        self.assertEqual(self.ledger.read_bytes() if self.ledger.exists() else None, before)

    def review_entry(self, review, kind):
        return review[kind] if kind == "calibration" else review[kind][0]

    def test_blocks_major_findings_from_every_image_kind_without_writing_ledger(self):
        for kind in ("sheets", "details", "covers", "calibration"):
            with self.subTest(kind=kind):
                review = copy.deepcopy(self.review)
                self.review_entry(review, kind)["findings"] = [
                    {"severity": "major", "text": "Text overlaps an illustration."}]
                self.assert_refused(review=review)

    def test_keeps_minor_notes_from_every_image_kind_and_records_real_coverage(self):
        notes = []
        for kind in ("sheets", "details", "covers", "calibration"):
            text = f"Accepted cosmetic note for {kind}."
            notes.append(text)
            self.review_entry(self.review, kind)["findings"] = [{"severity": "minor", "text": text}]
        self.invoke()
        ledger = json.loads(self.ledger.read_text(encoding="utf-8"))
        self.assertTrue(ledger["status"].startswith("PASS"))
        self.assertEqual(ledger["pages_reviewed"], [1, 2, 3])
        self.assertEqual(ledger["detailed_pages_viewed_at_100dpi"], [1, 3])
        self.assertEqual(len(ledger["accepted_layout_notes"]), 4)
        for note in notes:
            self.assertTrue(any(note in recorded for recorded in ledger["accepted_layout_notes"]))

    def test_unknown_finding_severity_cannot_be_treated_as_minor(self):
        for kind in ("sheets", "details", "covers", "calibration"):
            for severity in ("critical", "MAJOR", None, []):
                with self.subTest(kind=kind, severity=severity):
                    review = copy.deepcopy(self.review)
                    self.review_entry(review, kind)["findings"] = [
                        {"severity": severity, "text": "A finding requiring explicit classification."}]
                    self.assert_refused(review=review)

    def test_contact_sheets_must_cover_every_page_once(self):
        changes = [[], [self.manifest["sheets"][0]],
                   [dict(self.manifest["sheets"][0], pages=[1, 3]), self.manifest["sheets"][1]],
                   [dict(self.manifest["sheets"][0], pages=[0, 2]), self.manifest["sheets"][1]],
                   [dict(self.manifest["sheets"][0], pages=[1, 4])],
                   [dict(self.manifest["sheets"][0], pages=[1, "2"])]]
        for sheets in changes:
            with self.subTest(sheets=sheets):
                manifest = copy.deepcopy(self.manifest)
                manifest["sheets"] = sheets
                self.assert_refused(manifest=manifest)

    def test_required_detail_and_cover_images_cannot_be_omitted(self):
        for kind, items in (("details", []), ("details", self.manifest["details"][:1]),
                            ("covers", []), ("covers", self.manifest["covers"][:1])):
            with self.subTest(kind=kind, count=len(items)):
                manifest = copy.deepcopy(self.manifest)
                manifest[kind] = items
                self.assert_refused(manifest=manifest)

    def test_duplicate_review_cannot_overwrite_a_major_finding(self):
        self.review["sheets"][0]["findings"] = [{"severity": "major", "text": "A broken table."}]
        clean_duplicate = copy.deepcopy(self.review["sheets"][0])
        clean_duplicate.pop("findings")
        self.review["sheets"].append(clean_duplicate)
        self.assert_refused()

    def test_missing_review_or_wrong_image_bytes_preserves_existing_ledger(self):
        self.ledger.write_bytes(b"previous reviewed ledger")
        review = copy.deepcopy(self.review)
        review["details"].pop()
        self.assert_refused(review=review)
        (self.images / self.manifest["sheets"][0]["file"]).write_bytes(b"unreviewed replacement")
        self.assert_refused()


if __name__ == "__main__":
    unittest.main()
