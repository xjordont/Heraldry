#!/usr/bin/env python3
"""Release verification gate. Runs every deterministic check on the final files in dist/
and writes production/qa/*.json plus production/qa/STATUS.json. Exits non-zero when a
mandatory check fails, so a failed build cannot be labelled an unconditional release."""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "production/qa"
DIST = ROOT / "dist"
PY = sys.executable


def run(args, report=None):
    r = subprocess.run([PY] + args, cwd=ROOT, capture_output=True, text=True)
    status = "PASS" if r.returncode == 0 else "FAIL"
    if report and Path(report).exists():
        try:
            status = json.loads(Path(report).read_text()).get("status", status)
        except Exception:
            pass
    return status, (r.stdout + r.stderr)[-600:]


def tquery(sel):
    import typst
    return json.loads(typst.query(str(ROOT / "typst/content.typ"), sel, field="value", root=str(ROOT),
                                  font_paths=[str(ROOT / "fonts/static")], ignore_system_fonts=True,
                                  sys_inputs={"substrate": "cream", "edition": "print"}))


def main():
    QA.mkdir(parents=True, exist_ok=True)
    cream = DIST / "Heraldry_RC484_inkjet-borderless.pdf"
    white = DIST / "Heraldry_RC484_inkjet-borderless-white.pdf"
    digital = DIST / "Heraldry_RC484_digital.pdf"
    st = {}
    st["source_preflight"], _ = run(["tools/preflight.py", "--report", "production/preflight.json"])
    pf = json.loads((ROOT / "production/preflight.json").read_text())
    src_ok = next(c for c in pf["checks"] if c["check"] == "source_integrity")["status"]
    st["source_integrity"] = src_ok
    st["reconciliation"], _ = run(["tools/reconcile.py", str(cream), "--report", str(QA / "reconciliation.json")], QA / "reconciliation.json")
    st["reconciliation_digital"], _ = run(["tools/reconcile.py", str(digital), "--skip-covers", "--report", str(QA / "reconciliation-digital.json")], QA / "reconciliation-digital.json")
    lay, _ = run(["tools/layout_qa.py", str(cream), "--report", str(QA / "layout.json")])
    lj = json.loads((QA / "layout.json").read_text())
    st["layout_detectors"] = "PASS" if not lj["counts"] else "FAIL"
    st["inkjet_checker_cream"], _ = run(["tools/verify_inkjet_pdf.py", str(cream), "--report", str(QA / "inkjet-preflight.json")], QA / "inkjet-preflight.json")
    st["inkjet_checker_white"], _ = run(["tools/verify_inkjet_pdf.py", str(white), "--report", str(QA / "inkjet-preflight-white.json")], QA / "inkjet-preflight-white.json")
    st["print_supplementary"], _ = run(["tools/print_checks.py", "--cream", str(cream), "--white", str(white), "--report", str(QA / "print-checks.json")], QA / "print-checks.json")
    st["xref_audit"], _ = run(["tools/xref_audit.py"])
    xr = json.loads((QA / "xref-audit.json").read_text())
    st["xref_audit"] = "PASS" if not xr["unresolved"] and not xr["duplicate_heading_numbers"] else "FAIL"

    # ---- all-table audit: source id → output pages → representation → reconciliation
    rec = json.loads((QA / "reconciliation.json").read_text())
    bad_tables = {t["id"] for t in rec["table_cells_missing"]}
    inv = json.loads((ROOT / "production/inventory/tables.json").read_text())
    reps = {t["id"]: t for t in json.loads((ROOT / "production/mappings/tables.json").read_text())}
    pos = {}
    allpos = tquery("<tblpos>")
    for m in allpos:
        pos.setdefault(m["id"], []).append(m)
    starts = {}
    for m in allpos:
        if m["edge"] == "s":
            starts[m["id"]] = starts.get(m["id"], 0) + 1
    dup = {k: v for k, v in starts.items() if v != 1}
    st["no_duplicate_tables_figures"] = "PASS" if not dup else "FAIL"
    rows = []
    for t in inv:
        ps = pos.get(t["id"], [])
        folios = sorted({m["folio"] for m in ps}, key=lambda f: int(f) if f.isdigit() else 0)
        pages = sorted({m["page"] for m in ps})
        r = reps.get(t["id"], {})
        rows.append({"id": t["id"], "src_lines": t["src"], "heading": t["heading_title"], "columns": t["columns"],
                     "rows": t["rows"], "cells": t["cells"], "cell_sha256": t["cell_sha256"],
                     "representation": r.get("rep"), "scope": r.get("scope"), "family": r.get("family"),
                     "field_map": r.get("field_map"), "pdf_pages": [pages[0], pages[-1]] if pages else None,
                     "folios": [folios[0], folios[-1]] if folios else None,
                     "multipage": len(pages) > 1 and pages[0] != pages[-1],
                     "reconciliation": "FAIL" if t["id"] in bad_tables or not pages else "PASS"})
    ta = {"tables": len(rows), "pass": sum(r["reconciliation"] == "PASS" for r in rows),
          "multipage": [r["id"] for r in rows if r["multipage"]], "rows": rows,
          "note": "Cell-level check: every normalised source cell appears in the PDF text layer within the table's local window (tools/reconcile.py). Repeated headers and card field labels are layout duplication, not source data."}
    ta["status"] = "PASS" if ta["pass"] == ta["tables"] else "FAIL"
    (QA / "table-audit.json").write_text(json.dumps(ta, indent=1, ensure_ascii=False))
    st["table_audit"] = ta["status"]

    # ---- index audit
    idx = json.loads((ROOT / "build/index.json").read_text())
    loc = {}
    for m in tquery("<ixpos>"):
        loc.setdefault(m["k"], set()).add(m["folio"])
    hpos = {h["id"]: h for h in tquery("<hpos>")[0]}
    for k, hids in idx.get("heads", {}).items():
        for hid in hids:
            if hid in hpos:
                loc.setdefault(k, set()).add(str(hpos[hid]["folio"]))
    keys = [k for e in idx["entries"] for k in e.get("keys", [])] + [k for e in idx["entries"] for s in e.get("sub", []) for k in s["keys"]]
    missing = [k for k in keys if k not in loc]
    see_bad = [e["term"] for e in idx["entries"] if e.get("see") and e["see"].lower() not in {x["term"].lower() for x in idx["entries"]}]
    ia = {"entries": len(idx["entries"]), "locator_keys": len(keys), "keys_without_page": missing, "see_targets_missing": see_bad,
          "term_pages": {k: sorted(v, key=lambda f: int(f) if f.isdigit() else 0) for k, v in loc.items()}}
    ia["status"] = "PASS" if not missing and not see_bad else "FAIL"
    (QA / "index-audit.json").write_text(json.dumps(ia, indent=1, ensure_ascii=False))
    st["index_audit"] = ia["status"]

    # ---- figures
    man = ROOT / "figures/manifest.json"
    if man.exists():
        figs = json.loads(man.read_text())
        figs = figs["figures"] if isinstance(figs, dict) else figs
        placed = {m["id"]: m for m in tquery("<tblpos>") if str(m["id"]).startswith("FIG")}
        fa = [{"id": f["id"], "placed": f["id"] in placed, "folio": placed.get(f["id"], {}).get("folio"),
               "semantic_status": f.get("status")} for f in figs]
        st["figures_placed"] = "PASS" if all(x["placed"] for x in fa) else "FAIL"
        (QA / "figure-audit.json").write_text(json.dumps(fa, indent=1))
    else:
        st["figures_placed"] = "NOT TESTED"
    # figure semantic review must be current (hash-bound to the SVG and caption) and free of open majors
    st["figure_semantic_review"], _ = run(["tools/figure_review_gate.py", "--report", str(QA / "figure-review-gate.json")], QA / "figure-review-gate.json")

    declared = [x["id"] for x in json.loads((ROOT / "editorial/patches.json").read_text())["patches"] if x.get("status") == "applied"]
    applied = json.loads((ROOT / "build/blocks.json").read_text()).get("patches_applied", [])
    st["editorial_patches"] = "PASS" if declared == applied else "FAIL"

    mandatory = ["editorial_patches", "source_preflight", "source_integrity", "reconciliation", "reconciliation_digital", "layout_detectors", "inkjet_checker_cream",
                 "inkjet_checker_white", "print_supplementary", "no_duplicate_tables_figures", "xref_audit", "table_audit", "index_audit", "figures_placed",
                 "figure_semantic_review"]
    failed = [k for k in mandatory if st.get(k) != "PASS"]
    out = {"checks": st, "mandatory_failed": failed, "release_gate": "PASS" if not failed else "FAIL",
           "not_covered_here": ["all-page visual inspection (production/qa/visual-review.json)",
                                "diagram semantic correctness beyond the hash-bound review record (production/qa/figure-semantic-review.json)",
                                "physical inkjet proof: NOT TESTED"]}
    (QA / "STATUS.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
