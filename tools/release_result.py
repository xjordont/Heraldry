#!/usr/bin/env python3
"""Write production/RELEASE_RESULT.json after the release workflow ran for a visual-ledger push (called by rebuild-delivery.yml)."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger-commit", required=True)
    ap.add_argument("--failed-step", default="")
    ap.add_argument("--run-url", default="")
    a = ap.parse_args()
    rel = ROOT / "dist/RELEASE.json"
    r = json.loads(rel.read_text()) if rel.is_file() else {}
    ok = not a.failed_step and r.get("source_commit") == a.ledger_commit
    out = {"ledger_commit": a.ledger_commit, "result": "RELEASED" if ok else "FAILED",
           "note": "released and verified" if ok else (f"step failed: {a.failed_step}" if a.failed_step else "no release was published for this commit"),
           "release_url": r.get("url", "") if ok else "", "tag": r.get("tag", "") if ok else "", "run_url": a.run_url,
           "physical_print": "NOT TESTED"}
    (ROOT / "production/RELEASE_RESULT.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: out[k] for k in ("result", "note")}))


if __name__ == "__main__":
    main()
