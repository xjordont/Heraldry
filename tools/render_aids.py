#!/usr/bin/env python3
"""Render the player-aid sheets (typst/aids/paNN.typ) to build/aids/.

Writes one PDF per sheet and paper (cream, white), a combined PDF per paper, and,
with --png, page previews. Outputs are build products and are never committed.

usage: python tools/render_aids.py [--paper cream|white|both] [--png] [--only pa02 ...]
"""
import argparse
from pathlib import Path

import json
import sys

import typst
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "typst" / "aids"
OUT = ROOT / "build" / "aids"


def compile_one(src, paper, png):
    kw = dict(root=str(ROOT), font_paths=[str(ROOT / "fonts/static")], ignore_system_fonts=True,
              sys_inputs={"substrate": paper})
    c = typst.Compiler(str(src), **kw)
    stem = OUT / f"{src.stem}-{paper}"
    for old in OUT.glob(f"{stem.name}-*.png"):
        old.unlink()
    _, warnings = c.compile_with_warnings(output=str(stem) + ".pdf")
    for w in warnings:
        print(f"WARN {src.name}: {str(w)[:300]}")
        FAILURES.append(f"{src.name}: compiler warning")
    if png:
        c.compile(output=str(stem) + "-{p}.png", format="png", ppi=110)
    pdf = stem.with_suffix(".pdf")
    pages = len(PdfReader(str(pdf)).pages)
    if src.parent == SRC and pages != 2:
        print(f"FAIL {src.name}: {pages} pages; every sheet must be exactly one front and one back")
        FAILURES.append(f"{src.name}: {pages} pages")
    stamp(pdf, "Player Aids" if src.parent != SRC else f"Player Aid {int(src.stem[2:])}")
    return pdf


def stamp(pdf, subject):
    """Document metadata matching the book's imprint (owner, 2026-10-29)."""
    meta = json.loads((ROOT / "config/production.json").read_text(encoding="utf-8"))["verified_publication_metadata"]
    writer = PdfWriter(clone_from=str(pdf))
    writer.add_metadata({"/Title": f"{meta['title']}, {subject}, {meta['version']}",
                         "/Author": meta.get("author_credit") or "", "/Subject": subject})
    writer.write(str(pdf))


FAILURES = []


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--paper", choices=["cream", "white", "both"], default="cream")
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    sheets = sorted(p for p in SRC.glob("pa[0-9][0-9].typ") if not a.only or p.stem in a.only)
    papers = ["cream", "white"] if a.paper == "both" else [a.paper]
    for paper in papers:
        for s in sheets:
            print("ok", compile_one(s, paper, a.png).relative_to(ROOT))
        if not a.only:
            combined = OUT / "all.typ"
            combined.write_text("".join(f'#include "/typst/aids/{s.name}"\n' for s in sheets), encoding="utf-8")
            print("ok", compile_one(combined, paper, False).relative_to(ROOT))
    if FAILURES:
        sys.exit("FAIL: " + "; ".join(FAILURES))


if __name__ == "__main__":
    main()
