"""Bind a build and its QA result to the exact current inputs and PDF bytes."""
import json
from pathlib import Path
from manuscript import ROOT, active, sha256, version, check as check_source

INPUTS = ["config", "source", "editorial/patches.json", "editorial/how_to_use.json", "editorial/history", "tools", "typst", "fonts", "figures/src", "figures/out",
          "figures/manifest.json", "figures/placements.json", "assets", "production/art/SELECTIONS.json", "production/art/SPOT_CATALOG.json",
          "Makefile", "requirements.lock", "docs/PRINT_INSTRUCTIONS_TEMPLATE.md"]
# generated raw masters are bound by SHA256 in production/art/SELECTIONS.json; builds use only the ink derivatives
EXCLUDE = {"__pycache__", "test", "private", "masters", "style"}
SUFFIXES = ["digital", "inkjet-borderless", "inkjet-borderless-white", "covers-front-back", "covers-front-back-white", "inkjet-calibration"]


def inputs(root=ROOT):
    paths = set()
    for name in INPUTS:
        p = root / name
        paths.update(p.rglob("*") if p.is_dir() else [p])
    return {p.relative_to(root).as_posix(): sha256(p) for p in sorted(paths)
            if p.is_file() and not (EXCLUDE & set(p.parts))
            and p.name != "content.typ" and not p.name.startswith(".env")}


def pdfs(root=ROOT):
    return {f"dist/Heraldry_{version(root)}_{s}.pdf": sha256(root / f"dist/Heraldry_{version(root)}_{s}.pdf") for s in SUFFIXES}


def current(root=ROOT):
    authority = check_source(root)
    model = json.loads((root / "build/blocks.json").read_text())
    if model["sha256"] != authority["sha256"] or model["source"] != authority["path"]:
        raise ValueError("Parsed model is stale for the active manuscript")
    generated = {name: sha256(root / name) for name in ("build/blocks.json", "build/index.json", "typst/content.typ")}
    return {"manuscript": authority, "inputs": inputs(root), "generated": generated, "pdfs": pdfs(root)}


def check(root=ROOT):
    expected = json.loads((root / "production/build-provenance.json").read_text())
    actual = current(root)
    if actual != expected:
        raise ValueError("Build inputs or PDF bytes differ from build-provenance.json; rebuild before verifying")
    return actual


if __name__ == "__main__":
    (ROOT / "production/build-provenance.json").write_text(json.dumps(current(), indent=2) + "\n")
