#!/usr/bin/env python3
"""Regenerate all HERALDRY SKIRMISH RC484 rules diagrams: python3 figures/src/make_figures.py
Writes figures/out/FIG-NN.svg, figures/manifest.json and figures/placements.json.
Optional: pass figure ids (e.g. FIG-01 FIG-05) to build a subset only (SVG only)."""
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "..", "out")

MODULES = ["fig_seq", "fig_spatial", "fig_monster", "fig_scen", "fig_misc"]


def registry():
    reg = {}
    for m in MODULES:
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError as e:
            if e.name == m:
                continue
            raise
        for name in dir(mod):
            if name.startswith("fig") and name[3:].isdigit():
                reg["FIG-%02d" % int(name[3:])] = getattr(mod, name)
    return reg


def build(only=None):
    os.makedirs(OUT, exist_ok=True)
    reg = registry()
    done = []
    for fid in sorted(reg):
        if only and fid not in only:
            continue
        svg, h = reg[fid]()
        import figdata
        meta = figdata.META.get(fid, {})
        text = svg.render(h, title=meta.get("title", fid), desc=meta.get("purpose"))
        with open(os.path.join(OUT, fid + ".svg"), "w", encoding="utf-8") as f:
            f.write(text)
        done.append((fid, svg.w, round(h, 1)))
    return done


if __name__ == "__main__":
    only = sys.argv[1:] or None
    done = build(only)
    for d in done:
        print("wrote %s  %spt x %spt" % d)
    if not only:
        try:
            import figdata
            figdata.write_all()
            print("wrote manifest.json, placements.json")
        except ModuleNotFoundError as e:
            if e.name != "figdata":
                raise
