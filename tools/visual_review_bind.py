#!/usr/bin/env python3
"""Bind the all-page visual review of a candidate PDF into production/qa/visual-review.json (standard library only).

Owner decision 2026-10-14: the review of the candidate is done by Codex, unattended. This tool keeps that review honest.
Input: a JSON review record the reviewer wrote after actually viewing every file listed in production/qa/review/manifest.json.
Refuses unless: the candidate is CANDIDATE_READY and matches the manifest's PDF hash; every contact sheet, detail page and the
calibration sheet has an entry with real observations; the image files on disk match the manifest hashes (the reviewer had the
real images, not LFS stubs); a reviewer is named; and no finding is marked major. A major finding means the book is NOT released:
the tool prints it and exits 2.

Review record:
  {"reviewer": "Codex (OpenAI model, image inspection)",
   "sheets":  [{"file": "sheet-01.jpg", "observations": "...", "findings": [{"page": 12, "severity": "minor|major", "text": "..."}]}, ...],
   "details": [{"file": "page-0001.jpg", "observations": "..."}, ...],
   "calibration": {"observations": "..."},
   "summary": "..."}
Severity major = unintended blank page, overlapping or clipped text, missing or wrong art, broken table, content running past the
safe edge, wrong page order, anything a reader would call a defect. Minor = cosmetic notes or accepted layout.

    python tools/visual_review_bind.py bind --review REVIEW.json [--push]
"""
import argparse
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "production/qa/review"
MIN_OBS = 60


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def fail(msg):
    print("REFUSED: " + msg)
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cmd", choices=["bind"])
    ap.add_argument("--review", required=True)
    ap.add_argument("--push", action="store_true")
    a = ap.parse_args()
    man = json.loads((REVIEW / "manifest.json").read_text())
    st = json.loads((ROOT / "production/BUILD_STATUS.json").read_text())
    rv = json.loads(Path(a.review).read_text(encoding="utf-8"))
    cream = next((v for k, v in st.get("pdfs", {}).items() if k.endswith("_inkjet-borderless.pdf")), None)
    if st.get("result") != "CANDIDATE_READY" or not cream or cream["sha256"] != man["pdf_sha256"]:
        fail("BUILD_STATUS.json does not describe a ready candidate of the PDF these review files belong to")
    for item in man["sheets"] + man["details"] + [man["calibration"]]:
        f = REVIEW / item["file"]
        if not f.is_file() or sha(f) != item["sha256"]:
            fail(f"{item['file']} is missing or is a stub (run git lfs pull --include 'production/qa/review/*')")

    def entries(kind, want):
        got = {e.get("file"): e for e in rv.get(kind, [])}
        for item in want:
            e = got.get(item["file"])
            if not e or len(str(e.get("observations", "")).strip()) < MIN_OBS:
                fail(f"no real observations recorded for {item['file']} (at least {MIN_OBS} characters of what was seen)")
        return got
    sheets = entries("sheets", man["sheets"])
    entries("details", man["details"])
    if len(str(rv.get("calibration", {}).get("observations", "")).strip()) < MIN_OBS:
        fail("no real observations recorded for the calibration sheet")
    major, minor = [], []
    for e in sheets.values():
        for f in e.get("findings", []):
            (major if f.get("severity") == "major" else minor).append(f"p{f.get('page')}: {f.get('text')}")
    if major:
        print("REVIEW FAILED: major findings, the book is not released:\n- " + "\n- ".join(major))
        sys.exit(2)
    if not str(rv.get("reviewer", "")).strip():
        fail("the reviewer must be named")
    ledger = {
        "pdf": f"dist/{man['pdf']}", "sha256": man["pdf_sha256"], "pages": man["pages"], "reviewer": rv["reviewer"],
        "reviewed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "all_page_contact_sheets": {"scale": "34 dpi, up to 24 pages per sheet", "sheets": len(man["sheets"]),
                                    "note": "every page of this exact PDF (the candidate build; the release build reproduces it) viewed on contact sheets"},
        "pages_reviewed": list(range(1, man["pages"] + 1)),
        "detailed_pages_viewed_at_100dpi": [d["page"] for d in man["details"]],
        "covers_viewed": True, "calibration_viewed": True,
        "findings_repaired": [], "accepted_layout_notes": minor + ([rv["summary"]] if rv.get("summary") else []),
        "limits": "Contact-sheet review of every page and 100 dpi detail review of the listed pages, by the named reviewer from images; not glyph-level proofreading, not an independent second review, not a physical printer proof.",
        "status": "PASS (all-page contact-sheet review of this exact PDF by an automated vision reviewer; not glyph-level proofreading)",
        "changes_this_run": [f"candidate build {st.get('request_id')} from {st.get('source_commit')}"],
    }
    (ROOT / "production/qa/visual-review.json").write_text(json.dumps(ledger, indent=1) + "\n")
    print(f"bound: {man['pdf']} sha256 {man['pdf_sha256'][:12]}..., {man['pages']} pages, {len(minor)} minor notes")
    if a.push:
        def git(*x):
            return subprocess.run(["git", *x], cwd=ROOT, capture_output=True, text=True)
        git("add", "production/qa/visual-review.json")
        r = git("commit", "-m", f"review: bind the all-page visual review for candidate {st.get('request_id')}")
        if r.returncode:
            fail("commit failed: " + r.stderr.strip())
        for _ in range(4):
            if git("push", "origin", "main").returncode == 0:
                print("ledger commit " + git("rev-parse", "HEAD").stdout.strip())
                return
            git("pull", "--rebase", "origin", "main")
        fail("push failed")


if __name__ == "__main__":
    main()
