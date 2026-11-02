#!/usr/bin/env python3
"""Bind the all-page visual review of a candidate PDF into production/qa/visual-review.json (standard library only).

The candidate needs a look at every review image before release.
Input: a JSON review record written after viewing every file listed in production/qa/review/manifest.json.
Refuses unless: the candidate is CANDIDATE_READY and matches the manifest's PDF hash; every contact sheet, detail page, and cover
has an entry with a note (a short one is fine); the image files on disk match the manifest hashes (real
images, not LFS stubs); a reviewer is named; and no finding is marked major. A major finding means the book is NOT released:
the tool prints it and exits 2.

Review record:
  {"reviewer": "Actual client and model, image inspection",
   "sheets":  [{"file": "sheet-01.jpg", "observations": "...", "findings": [{"page": 12, "severity": "minor|major", "text": "..."}]}, ...],
   "details": [{"file": "page-0001.jpg", "observations": "..."}, ...],
   "covers": [{"file": "cover-front.jpg", "observations": "..."}, {"file": "cover-back.jpg", "observations": "..."}],
   "summary": "..."}
Severity major = unintended blank page, overlapping or clipped text, missing or wrong art, broken table, content running past the
safe edge, wrong page order, anything a reader would call a defect. Minor = cosmetic notes or accepted layout.

    python tools/visual_review_bind.py bind --review REVIEW.json [--push]
"""
import argparse
import datetime
import hashlib
import json
import sys
from pathlib import Path

from git_publish import PublishError, publish_files, require_clean_main

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "production/qa/review"
MIN_OBS = 1  # a short note per image is enough


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def fail(msg):
    print("REFUSED: " + msg)
    sys.exit(2)


def validate_manifest(man):
    """Require the image inventory to account for every claimed PDF page."""
    if not isinstance(man, dict):
        fail("the review manifest must be an object")
    pages = man.get("pages")
    if type(pages) is not int or pages < 1:
        fail("the review manifest needs a positive PDF page count")
    files = set()
    for kind in ("sheets", "details", "covers"):
        items = man.get(kind)
        if not isinstance(items, list) or not items:
            fail(f"the review manifest has no {kind}")
        for item in items:
            if not isinstance(item, dict):
                fail(f"invalid {kind} entry in the review manifest")
    for item in man["sheets"] + man["details"] + man["covers"]:
        name = item.get("file")
        if not isinstance(name, str) or not name or "/" in name or "\\" in name or name in {".", ".."}:
            fail("review image filenames must name files inside the review directory")
        if name in files:
            fail(f"duplicate review manifest image: {name}")
        files.add(name)
        digest = item.get("sha256")
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            fail(f"invalid image hash for {name}")
    covered = set()
    for item in man["sheets"]:
        span = item.get("pages")
        if (not isinstance(span, list) or len(span) != 2 or any(type(p) is not int for p in span)
                or not 1 <= span[0] <= span[1] <= pages):
            fail(f"invalid contact-sheet page range for {item['file']}")
        sheet_pages = set(range(span[0], span[1] + 1))
        if covered & sheet_pages:
            fail(f"overlapping contact-sheet page range for {item['file']}")
        covered.update(sheet_pages)
    if covered != set(range(1, pages + 1)):
        fail("the contact sheets do not cover every PDF page")
    detail_pages = []
    for item in man["details"]:
        page = item.get("page")
        if type(page) is not int or not 1 <= page <= pages or page in detail_pages:
            fail(f"invalid or duplicate detail page for {item['file']}")
        detail_pages.append(page)
    if not {1, pages}.issubset(detail_pages):
        fail("the review manifest needs first-page and last-page detail images")
    roles = [item.get("role") for item in man["covers"]]
    if sorted(roles, key=str) != ["back", "front"]:
        fail("the review manifest needs the front and back cover images")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cmd", choices=["bind"])
    ap.add_argument("--review", required=True)
    ap.add_argument("--push", action="store_true")
    a = ap.parse_args()
    man = json.loads((REVIEW / "manifest.json").read_text(encoding="utf-8"))
    st = json.loads((ROOT / "production/BUILD_STATUS.json").read_text(encoding="utf-8"))
    rv = json.loads(Path(a.review).read_text(encoding="utf-8"))
    validate_manifest(man)
    digital = next((v for k, v in st.get("pdfs", {}).items() if k.endswith("_digital.pdf")), None)
    if st.get("result") != "CANDIDATE_READY" or not digital or digital["sha256"] != man["pdf_sha256"]:
        fail("BUILD_STATUS.json does not describe a ready candidate of the PDF these review files belong to")
    for item in man["sheets"] + man["details"] + man["covers"]:
        f = REVIEW / item["file"]
        if not f.is_file() or sha(f) != item["sha256"]:
            fail(f"{item['file']} is missing or is a stub (run git lfs pull --include 'production/qa/review/*')")

    def entries(kind, want):
        got = {}
        supplied = rv.get(kind, [])
        if not isinstance(supplied, list):
            fail(f"invalid {kind} review entries")
        for e in supplied:
            if not isinstance(e, dict) or not isinstance(e.get("file"), str):
                fail(f"invalid {kind} review entry")
            if e["file"] in got:
                fail(f"duplicate review entry for {e['file']}")
            got[e["file"]] = e
        if set(got) != {item["file"] for item in want}:
            fail(f"the {kind} review entries do not match the manifest")
        for item in want:
            e = got.get(item["file"])
            if not isinstance(e.get("observations"), str) or len(e["observations"].strip()) < MIN_OBS:
                fail(f"no note recorded for {item['file']}")
        return got
    sheets = entries("sheets", man["sheets"])
    details = entries("details", man["details"])
    covers = entries("covers", man["covers"])
    major, minor = [], []
    for name, e in list(sheets.items()) + list(details.items()) + list(covers.items()):
        findings = e.get("findings", [])
        if not isinstance(findings, list):
            fail(f"invalid findings for {name}")
        for f in findings:
            if not isinstance(f, dict) or f.get("severity") not in ("major", "minor"):
                fail(f"unrecognised finding severity for {name}")
            if not isinstance(f.get("text"), str) or not f["text"].strip():
                fail(f"a finding for {name} needs its observed defect or note")
            location = f"p{f['page']}" if "page" in f else name
            (major if f["severity"] == "major" else minor).append(f"{location}: {f['text']}")
    if major:
        print("REVIEW FAILED: major findings, the book is not released:\n- " + "\n- ".join(major))
        sys.exit(2)
    if not isinstance(rv.get("reviewer"), str) or not rv["reviewer"].strip():
        fail("the reviewer must be named")
    ledger = {
        "pdf": f"dist/{man['pdf']}", "sha256": man["pdf_sha256"], "pages": man["pages"], "reviewer": rv["reviewer"],
        "reviewed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "all_page_contact_sheets": {"scale": "34 dpi, up to 24 pages per sheet", "sheets": len(man["sheets"]),
                                    "note": "every page of this exact PDF (the candidate build; the release build reproduces it) viewed on contact sheets"},
        "pages_reviewed": list(range(1, man["pages"] + 1)),
        "detailed_pages_viewed_at_100dpi": [d["page"] for d in man["details"]],
        "covers_viewed": [c["file"] for c in man["covers"]],
        "findings_repaired": [], "accepted_layout_notes": minor + ([rv["summary"]] if rv.get("summary") else []),
        "limits": "Contact-sheet review of every page and 100 dpi detail review of the listed pages, from images; not glyph-level proofreading.",
        "status": "PASS (all-page contact-sheet review of this exact PDF by an automated vision reviewer; not glyph-level proofreading)",
        "changes_this_run": [f"candidate build {st.get('request_id')} from {st.get('source_commit')}"],
    }
    base = None
    if a.push:
        try:
            base = require_clean_main(ROOT)
        except PublishError as exc:
            fail(str(exc))
    (ROOT / "production/qa/visual-review.json").write_text(json.dumps(ledger, indent=1) + "\n", encoding="utf-8")
    print(f"bound: {man['pdf']} sha256 {man['pdf_sha256'][:12]}..., {man['pages']} pages, {len(minor)} minor notes")
    if a.push:
        try:
            commit = publish_files(ROOT, ["production/qa/visual-review.json"],
                                   f"review: bind the all-page visual review for candidate {st.get('request_id')}", base)
        except PublishError as exc:
            fail(str(exc))
        print("ledger commit " + commit)


if __name__ == "__main__":
    main()
