#!/usr/bin/env python3
"""Measure every keep unit (sections, scenarios, tables, lists, examples, figures) in a fresh process.
Writes build/unit_measure.json {id: {h1, h2}} in pt: h1 = single-column height, h2 = one-page composition height."""
import json, time
from pathlib import Path
import typst

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "typst/measure.typ"
t0 = time.time()
res = json.loads(typst.query(str(src), "<um>", field="value", root=str(ROOT), font_paths=[str(ROOT / "fonts/static")],
                             ignore_system_fonts=True, sys_inputs={"substrate": "cream", "edition": "print", "index": "off"}))
out = {r["id"]: {"h1": round(r["h1"], 1), "h2": round(r["h2"], 1)} for r in res}
(ROOT / "build/unit_measure.json").write_text(json.dumps(out))
print(f"{len(out)} units measured in {time.time() - t0:.1f}s")
