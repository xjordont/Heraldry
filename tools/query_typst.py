#!/usr/bin/env python3
"""Run all QA location queries once in a disposable compiler process."""
import json
import typst
from manuscript import ROOT

if __name__ == "__main__":
    compiler = typst.Compiler(str(ROOT / "typst/content.typ"), root=str(ROOT),
        font_paths=[str(ROOT / "fonts/static")], ignore_system_fonts=True,
        sys_inputs={"substrate": "cream", "edition": "print"})
    print(json.dumps({s: json.loads(compiler.query(s, field="value"))
                      for s in ("<tblpos>", "<ixpos>", "<hpos>", "<um-pos>")}))
