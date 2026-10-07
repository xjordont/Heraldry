#!/usr/bin/env python3
"""Compile content.typ once (fresh process, bounded memory) and optionally dump queries."""
import json, sys, time
from pathlib import Path
import typst
from manuscript import pdf_epoch

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "typst" / "content.typ"
BUILD = ROOT / "build"

out, variant, edition, qfile = sys.argv[1], sys.argv[2], sys.argv[3], (sys.argv[4] if len(sys.argv) > 4 else None)
if not CONTENT.exists():
    raise FileNotFoundError(f"Missing generated Typst source: {CONTENT}. Run the manuscript build pipeline before compiling PDFs.")

out_path = Path(out)
out_path.parent.mkdir(parents=True, exist_ok=True)
if qfile:
    qf = Path(qfile)
    qf.parent.mkdir(parents=True, exist_ok=True)

kw = dict(root=str(ROOT), font_paths=[str(ROOT / "fonts/static")], ignore_system_fonts=True,
          sys_inputs={"substrate": variant, "edition": edition})
t0 = time.time()
c = typst.Compiler(str(CONTENT), **kw) if hasattr(typst, "Compiler") else None
if c is not None:
    c.compile(output=str(out_path), timestamp=pdf_epoch())
    res = {"dt": time.time() - t0}
    if qfile:
        res["pm"] = json.loads(c.query("<pm>", field="value"))
        res["hpos"] = json.loads(c.query("<hpos>", field="value"))[0]
else:
    typst.compile(str(CONTENT), output=str(out_path), timestamp=pdf_epoch(), **kw)
    res = {"dt": time.time() - t0}
    if qfile:
        res["pm"] = json.loads(typst.query(str(CONTENT), "<pm>", field="value", **kw))
        res["hpos"] = json.loads(typst.query(str(CONTENT), "<hpos>", field="value", **kw))[0]
if qfile:
    qf.write_text(json.dumps(res))
print(f"{res['dt']:.1f}")
