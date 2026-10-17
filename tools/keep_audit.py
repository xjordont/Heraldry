#!/usr/bin/env python3
"""Mandatory one-page keep audit (docs/DESIGN_REFINEMENT.md).

Every measured unit (section/subsection/scenario, table, list, example, figure) whose rendered
height fits an empty usable page (single column or balanced two-column/full-width composition)
must start and end on the same physical page. Over-height units are recorded with their measured
size. Missing position coverage or any avoidable split is a hard FAIL."""
import argparse, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--positions", required=True, help="JSON from tools/query_typst.py")
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--report", required=True)
    a = ap.parse_args()
    u = json.loads((ROOT / "build/units.json").read_text())
    fit = u["frame_fit_pt"]
    content = hashlib.sha256((ROOT / "typst/content.typ").read_bytes()).hexdigest()
    if u.get("content_sha256") != content:
        raise SystemExit("units.json does not describe the current typst/content.typ; rebuild")
    # A dict assignment used to discard duplicate/malformed start/end markers.
    # That could conceal an actual split or a duplicated unit in a passing report.
    markers = {}
    for m in json.loads(Path(a.positions).read_text())["<um-pos>"]:
        markers.setdefault(m["id"], []).append(m)
    pos, marker_errors = {}, []
    expected = {x["id"] for x in u["units"]}
    for uid, found in markers.items():
        starts = [m for m in found if m.get("edge") == "s"]
        ends = [m for m in found if m.get("edge") == "e"]
        if uid not in expected or len(starts) != 1 or len(ends) != 1 or len(found) != 2:
            marker_errors.append({"id": uid, "starts": len(starts), "ends": len(ends),
                                  "records": len(found), "unexpected": uid not in expected})
            continue
        p1, p2 = starts[0].get("page"), ends[0].get("page")
        if not isinstance(p1, int) or not isinstance(p2, int) or p1 < 1 or p2 < p1:
            marker_errors.append({"id": uid, "start": p1, "end": p2, "invalid_page_order": True})
            continue
        pos[uid] = {"s": p1, "e": p2}
    rows, fails, missing, over = [], [], [], []
    for x in u["units"]:
        h1, h2 = x.get("h1"), x.get("h2")
        fits = h1 is not None and (h1 <= fit or h2 <= fit)
        p = pos.get(x["id"], {})
        if "s" not in p or "e" not in p:
            missing.append(x["id"])
            continue
        pages = list(range(p["s"], p["e"] + 1))
        row = {"id": x["id"], "kind": x["kind"], "class": x["class"], "h1_pt": h1, "h2_pt": h2,
               "fit_capable": fits, "pages": pages}
        rows.append(row)
        if fits and len(pages) > 1:
            fails.append(row)
        if not fits:
            over.append({"id": x["id"], "kind": x["kind"], "h2_pt": h2, "pages": pages,
                         "reason": "taller than one empty usable page at its approved width; continues with intact child units"})
    rep = {"content_sha256": content, "pdf": a.pdf, "pdf_sha256": hashlib.sha256(Path(a.pdf).read_bytes()).hexdigest(),
           "frame_fit_pt": fit, "units": len(u["units"]), "audited": len(rows), "fit_capable": sum(r["fit_capable"] for r in rows),
           "avoidable_splits": fails, "missing_coverage": missing, "malformed_markers": marker_errors,
           "over_height": over,
           "status": "PASS" if not fails and not missing and not marker_errors else "FAIL", "rows": rows}
    Path(a.report).write_text(json.dumps(rep, indent=1))
    print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in rep.items() if k != "rows"}))
    raise SystemExit(0 if rep["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
