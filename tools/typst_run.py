#!/usr/bin/env python3
"""Compile once in a bounded process; extract positions from that PDF export."""
import hashlib, json, sys, time
from pathlib import Path
import typst
from manuscript import pdf_epoch
from pdf_positions import compilation_identity, read_positions

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
    qf.unlink(missing_ok=True)

identity = compilation_identity(ROOT, variant, edition)
kw = dict(root=str(ROOT), font_paths=[str(ROOT / "fonts/static")], ignore_system_fonts=True,
          sys_inputs={"substrate": variant, "edition": edition,
                      "position-identity": json.dumps(identity, sort_keys=True, separators=(",", ":"))})
t0 = time.time()
c = typst.Compiler(str(CONTENT), **kw)
_, warnings = c.compile_with_warnings(output=str(out_path), timestamp=pdf_epoch())
res = {"dt": time.time() - t0}
diagnostics = [str(w) for w in warnings]
if any("converg" in d.lower() or "introspection" in d.lower() for d in diagnostics):
    raise ValueError("Typst position introspection did not converge: " + "\n".join(diagnostics))
for diagnostic in diagnostics:
    print(diagnostic, file=sys.stderr)
positions = read_positions(out_path, variant=variant, edition=edition)
out_path.with_suffix(".positions.json").write_text(json.dumps(positions, ensure_ascii=False), encoding="utf-8")
if qfile:
    # Keep the existing balancing wrapper API while replacing every relayout
    # query with the attachment emitted inside this exact PDF serialization.
    res["pm"], res["hpos"] = positions["<pm>"], positions["<hpos>"][0]
    res["positions"] = positions
    res["pdf_sha256"] = hashlib.sha256(out_path.read_bytes()).hexdigest()
    res["content_sha256"] = hashlib.sha256(CONTENT.read_bytes()).hexdigest()
    res["substrate"] = variant
    res["edition"] = edition
    qf.write_text(json.dumps(res))
print(f"{res['dt']:.1f}")
