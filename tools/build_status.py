#!/usr/bin/env python3
"""Write production/BUILD_STATUS.json after a candidate build (called by build-candidate.yml; also unit-tested).

A candidate is READY when the build succeeded and the only mandatory check that fails is the hash-bound
all-page visual review (visual_review_currency): that review is a human/Claude inspection of the exact PDF, so an
unattended run can never satisfy it. Any other failed check, or a failed step, makes the result FAILED.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def evaluate(status, failed_step):
    """(result, failed_checks, note) from verify's STATUS.json content and the name of a failed step, if any."""
    if failed_step:
        return "FAILED", [], f"step failed: {failed_step}"
    failed = list((status or {}).get("mandatory_failed", ["verify did not run"]))
    if failed == ["visual_review_currency"]:
        return "CANDIDATE_READY", failed, "all automated checks pass; the all-page visual review of this exact PDF is still pending"
    if not failed:
        return "CANDIDATE_READY", failed, "all automated checks pass and the visual ledger already matches this PDF"
    return "FAILED", failed, "mandatory checks failed: " + ", ".join(failed)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--request-id", required=True)
    ap.add_argument("--failed-step", default="")
    ap.add_argument("--source-commit", default="")
    ap.add_argument("--run-url", default="")
    ap.add_argument("--release-url", default="")
    a = ap.parse_args()
    sp = ROOT / "production/qa/STATUS.json"
    status = json.loads(sp.read_text()) if sp.is_file() else None
    result, failed, note = evaluate(status, a.failed_step)
    pdfs = {p.name: {"bytes": p.stat().st_size, "sha256": sha(p)} for p in sorted((ROOT / "dist").glob("Heraldry_*.pdf"))} if (ROOT / "dist").is_dir() else {}
    out = {"request_id": a.request_id, "result": result, "note": note, "failed_checks": failed, "source_commit": a.source_commit,
           "run_url": a.run_url, "release_url": a.release_url, "pdfs": pdfs,
           "physical_print": "NOT TESTED", "next": "Claude Code reproduces this build, reviews every page and binds the visual ledger; pushing production/qa/visual-review.json then releases." if result == "CANDIDATE_READY" else "Fix the failure; do not release."}
    (ROOT / "production/BUILD_STATUS.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: out[k] for k in ("request_id", "result", "note")}))


if __name__ == "__main__":
    main()
