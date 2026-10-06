#!/usr/bin/env python3
"""Cover data (verbatim manuscript text), cover sheets, calibration sheet."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from parse_source import plain  # noqa: E402


def cover_data():
    m = json.loads((ROOT / "build/blocks.json").read_text())
    blocks = {}

    def walk(bs):
        for b in bs:
            blocks[b["id"]] = b
            for it in b.get("items", []):
                walk(it["blocks"])
            walk(b.get("blocks", []))
    for ch in m["chapters"]:
        walk(ch["blocks"])
    fr = m["chapters"][0]["blocks"]
    t1, _, t2 = fr[0]["title"].partition(": ")
    lead = plain(blocks["B00163"]["c"])
    # verbatim sentences from 1.1 (B00169, B00173, B00175)
    facts = []
    for bid, take in (("B00169", None), ("B00173", 1), ("B00175", None)):
        txt = plain(blocks[bid]["c"])
        facts.append(txt if take is None else txt.split(". ")[0] + ".")
    data = {"title": [t1, t2], "subtitle": plain(fr[1]["c"]), "version": plain(fr[2]["c"]),
            "lead": lead, "facts": facts, "source_blocks": ["h-heraldry-skirmish-the-dying-lands", "B00003", "B00005", "B00163", "B00169", "B00173", "B00175"]}
    (ROOT / "build/cover.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
    return data


def compile_doc(src, out, variant):
    import typst
    typst.compile(str(src), output=str(out), root=str(ROOT), font_paths=[str(ROOT / "fonts/static")],
                  ignore_system_fonts=True, sys_inputs={"substrate": variant})


def main():
    d = cover_data()
    print(json.dumps({k: d[k] for k in ("title", "version")}))
    out = ROOT / "build"
    for v in ("cream", "white"):
        compile_doc(ROOT / "typst/covers-main.typ", out / f"covers-{v}.pdf", v)
    compile_doc(ROOT / "typst/calibration.typ", out / "calibration.pdf", "cream")
    print("covers + calibration built")


if __name__ == "__main__":
    main()
