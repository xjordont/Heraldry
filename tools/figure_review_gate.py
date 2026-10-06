#!/usr/bin/env python3
"""Figure semantic-review currency gate.

Inputs
  figures/manifest.json            list, or {"figures": [...]}; each item has "id"
  figures/out/<id>.svg             current figure artwork
  figures/placements.json          {anchor: [{"id", "caption", ...}, ...]}; caption per figure id
  production/qa/figure-semantic-review.json   reviewer record (schema below)

Review schema (reviewers write this file):
  {"reviewer": str, "reviewed_at": str,
   "figures": [{"id": "FIG-01",
                "svg_sha256": hex           # sha256 of figures/out/<id>.svg bytes
                "caption_sha256": hex       # sha256 of the UTF-8 caption string in placements.json
                "verdict": "PASS" | "PASS_WITH_NOTES" | "FAIL",
                "findings": [{"severity": "critical"|"major"|"minor",
                              "status": "open"|"resolved"|"accepted",
                              "issue": str, ...}]}]}
  Use `--print-hashes` to obtain the current hashes to record.

FAIL when: a manifest figure has no review entry; a recorded hash differs from the current
file (stale) or is missing; verdict is FAIL (or not a recognised verdict); any critical or
major finding has status other than "resolved". Open minor findings are reported only.
Report: production/qa/figure-review-gate.json. Exit code 0 on PASS, 1 on FAIL.
"""
import argparse, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERDICTS = {"PASS", "PASS_WITH_NOTES", "FAIL"}


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _manifest_ids(root):
    m = json.loads((root / "figures/manifest.json").read_text())
    m = m["figures"] if isinstance(m, dict) else m
    return [f["id"] for f in m]


def current_hashes(root=ROOT):
    root = Path(root)
    caps = {}
    pl = json.loads((root / "figures/placements.json").read_text())
    for anchor, items in pl.items():
        for it in (items if isinstance(items, list) else [items]):
            if isinstance(it, dict) and "id" in it:
                caps[it["id"]] = it.get("caption", "")
    out = {}
    for fid in _manifest_ids(root):
        svg = root / "figures/out" / f"{fid}.svg"
        out[fid] = {"svg_sha256": _sha(svg.read_bytes()) if svg.exists() else None,
                    "caption_sha256": _sha(caps[fid].encode("utf-8")) if fid in caps else None}
    return out


def run_gate(root=ROOT, review_path=None, report_path=None):
    root = Path(root)
    review_path = Path(review_path or root / "production/qa/figure-semantic-review.json")
    report_path = Path(report_path or root / "production/qa/figure-review-gate.json")
    cur = current_hashes(root)
    reviews = {}
    reviewer = reviewed_at = None
    problems = []
    if review_path.exists():
        rv = json.loads(review_path.read_text())
        reviewer, reviewed_at = rv.get("reviewer"), rv.get("reviewed_at")
        for e in rv.get("figures", []):
            reviews[e.get("id")] = e
    else:
        problems.append(f"review file missing: {review_path}")
    rows = []
    for fid, c in cur.items():
        e = reviews.get(fid)
        row = {"id": fid, "current": c, "reviewed": None, "reviewed_present": e is not None,
               "stale": False, "stale_reasons": [], "verdict": None, "open_majors": [], "open_minors": [], "fail_reasons": []}
        if c["svg_sha256"] is None:
            row["fail_reasons"].append("svg file missing")
        if c["caption_sha256"] is None:
            row["fail_reasons"].append("no caption in placements.json")
        if e is None:
            row["fail_reasons"].append("no review entry")
        else:
            row["reviewed"] = {"svg_sha256": e.get("svg_sha256"), "caption_sha256": e.get("caption_sha256")}
            row["verdict"] = e.get("verdict")
            for k in ("svg_sha256", "caption_sha256"):
                if e.get(k) != c[k]:
                    row["stale"] = True
                    row["stale_reasons"].append(f"{k} " + ("missing from review" if not e.get(k) else "differs from current"))
            if row["stale"]:
                row["fail_reasons"].append("STALE review")
            if e.get("verdict") not in VERDICTS:
                row["fail_reasons"].append(f"unrecognised verdict {e.get('verdict')!r}")
            elif e["verdict"] == "FAIL":
                row["fail_reasons"].append("verdict FAIL")
            for f in e.get("findings", []):
                sev, stt = f.get("severity"), f.get("status")
                if sev in ("critical", "major") and stt != "resolved":
                    row["open_majors"].append({"severity": sev, "status": stt, "issue": f.get("issue")})
                elif sev == "minor" and stt == "open":
                    row["open_minors"].append(f.get("issue"))
                elif sev not in ("critical", "major", "minor"):
                    row["fail_reasons"].append(f"finding with unrecognised severity {sev!r}")
            if row["open_majors"]:
                row["fail_reasons"].append(f"{len(row['open_majors'])} unresolved critical/major finding(s)")
        row["status"] = "FAIL" if row["fail_reasons"] else "PASS"
        rows.append(row)
    extra = sorted(set(reviews) - set(cur))
    status = "PASS" if not problems and all(r["status"] == "PASS" for r in rows) else "FAIL"
    rep = {"status": status, "reviewer": reviewer, "reviewed_at": reviewed_at, "figures_total": len(rows),
           "figures_pass": sum(r["status"] == "PASS" for r in rows),
           "stale": [r["id"] for r in rows if r["stale"]],
           "missing_review": [r["id"] for r in rows if not r["reviewed_present"]],
           "open_majors": {r["id"]: r["open_majors"] for r in rows if r["open_majors"]},
           "open_minor_count": sum(len(r["open_minors"]) for r in rows),
           "review_entries_for_unknown_figures": extra, "problems": problems, "figures": rows}
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(rep, indent=1, ensure_ascii=False))
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--print-hashes", action="store_true", help="print current {id: {svg_sha256, caption_sha256}} and exit")
    ap.add_argument("--review"), ap.add_argument("--report")
    a = ap.parse_args()
    if a.print_hashes:
        print(json.dumps(current_hashes(), indent=1))
        return 0
    rep = run_gate(review_path=a.review, report_path=a.report)
    print(json.dumps({k: rep[k] for k in ("status", "figures_total", "figures_pass", "stale", "missing_review", "open_majors", "open_minor_count")}, indent=1))
    return 0 if rep["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
