#!/usr/bin/env python3
"""Write production/BUILD_STATUS.json after a candidate build (called by build-candidate.yml; also unit-tested).

A candidate is READY when the build succeeded and the only mandatory check that fails is the hash-bound
all-page visual review (visual_review_currency): that review is a named reviewer image inspection of the exact PDF, so an
unattended run can never satisfy it. Any other failed check, or a failed step, makes the result FAILED.
"""
import argparse
import hashlib
import json
from pathlib import Path
from qa_contract import MANDATORY_CHECKS

ROOT = Path(__file__).resolve().parents[1]


def evaluate(status, failed_step):
    """(result, failed_checks, note) from verify's STATUS.json content and the name of a failed step, if any."""
    if failed_step:
        return "FAILED", [], f"step failed: {failed_step}"
    if not isinstance(status, dict) or not isinstance(status.get("checks"), dict):
        return "FAILED", ["verification_report"], "verification report is missing or incomplete"
    checks = status["checks"]
    if any(checks.get(name) not in ("PASS", "FAIL", "NOT TESTED") for name in MANDATORY_CHECKS):
        return "FAILED", ["verification_report"], "verification report lacks recognised results for every mandatory check"
    failed = [name for name in MANDATORY_CHECKS if checks[name] != "PASS"]
    declared = status.get("mandatory_failed")
    if (not isinstance(declared, list) or any(not isinstance(name, str) for name in declared)
            or len(declared) != len(set(declared)) or set(declared) != set(failed)
            or status.get("release_gate") != ("FAIL" if failed else "PASS")):
        return "FAILED", ["verification_report"], "verification report summary disagrees with its check results"
    if failed == ["visual_review_currency"]:
        return "CANDIDATE_READY", failed, "all automated checks pass; the all-page visual review of this exact PDF is still pending"
    if not failed:
        return "CANDIDATE_READY", failed, "all automated checks pass and the visual ledger already matches this PDF"
    return "FAILED", failed, "mandatory checks failed: " + ", ".join(failed)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--request-id")
    ap.add_argument("--check-candidate", action="store_true", help="classify fresh verification without writing any ledger")
    ap.add_argument("--failed-step", default="")
    ap.add_argument("--source-commit", default="")
    ap.add_argument("--run-url", default="")
    ap.add_argument("--release-url", default="")
    a = ap.parse_args()
    sp = ROOT / "production/qa/STATUS.json"
    try:
        status = json.loads(sp.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        status = None
    result, failed, note = evaluate(status, a.failed_step)
    if a.check_candidate:
        print(json.dumps({"result": result, "failed_checks": failed, "note": note}))
        return 0 if result == "CANDIDATE_READY" else 2
    if not a.request_id:
        ap.error("--request-id is required unless --check-candidate is used")
    pdfs = {p.name: {"bytes": p.stat().st_size, "sha256": sha(p)} for p in sorted((ROOT / "dist").glob("Heraldry_*.pdf"))} if (ROOT / "dist").is_dir() else {}
    out = {"request_id": a.request_id, "result": result, "note": note, "failed_checks": failed, "source_commit": a.source_commit,
           "run_url": a.run_url, "release_url": a.release_url, "pdfs": pdfs,
           "physical_print": "NOT TESTED", "next": "The assigned reviewer inspects every review image and binds the exact PDF; pushing production/qa/visual-review.json starts release." if result == "CANDIDATE_READY" else "Fix the failure; do not release."}
    (ROOT / "production/BUILD_STATUS.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("request_id", "result", "note")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
