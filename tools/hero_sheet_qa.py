#!/usr/bin/env python3
"""Audit the rendered Hero set; optionally make Poppler review images. No book build or release."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pymupdf
from PIL import Image, ImageDraw

import hero_cards
from verify_inkjet_pdf import inspect

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "build/hero-redesign/review"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def signature(page):
    return [(s["text"], round(s["size"], 3), tuple(round(v, 2) for v in s["bbox"]))
            for b in page.get_text("dict", flags=pymupdf.TEXTFLAGS_DICT & ~pymupdf.TEXT_PRESERVE_IMAGES)["blocks"]
            for line in b.get("lines", []) for s in line["spans"] if s["text"].strip()]


def audit_blank(render_review):
    """Review only the blank form, preserving Basic Mode outputs and their review images."""
    review = ROOT / "build/hero-redesign/blank/review"
    review.mkdir(parents=True, exist_ok=True)
    config = json.loads((ROOT / "config/production.json").read_text(encoding="utf-8"))
    files, images, problems = [], [], []
    cream_signatures = None
    for paper in ("cream", "white"):
        path = hero_cards.OUT / f"hero-sheet-{paper}.pdf"
        result = inspect(path, config)
        doc = pymupdf.open(path)
        if len(doc) != 2:
            problems.append(f"{paper}: blank must have exactly two pages")
        if result["status"] != "PASS":
            problems.append(f"{paper}: print preflight failed")
        sig = [signature(page) for page in doc]
        if paper == "cream":
            cream_signatures = sig
        elif sig != cream_signatures:
            problems.append("Blank cream/white text or geometry differs")
        spans = [s for page in sig for s in page]
        files.append({"path": str(path.relative_to(ROOT)), "sha256": sha(path), "pages": len(doc),
                      "print_preflight": result["status"], "failures": result["failure_examples_first_50"],
                      "minimum_type_pt": min(s[1] for s in spans),
                      "minimum_text_inset_pt": round(min(min(s[2][0], s[2][1], 612 - s[2][2], 792 - s[2][3])
                                                         for s in spans), 2)})
        if render_review:
            executable = shutil.which("pdftoppm")
            if not executable:
                raise RuntimeError("Poppler pdftoppm is required for the review render")
            prefix = review / path.stem
            subprocess.run([executable, "-scale-to", "1500", "-png", str(path), str(prefix)],
                           check=True, capture_output=True)
            for image_path in sorted(review.glob(prefix.name + "-*.png")):
                images.append({"path": str(image_path.relative_to(ROOT)), "sha256": sha(image_path)})
    prior = json.loads((ROOT / "production/qa/hero-sheet-design-review.json").read_text(encoding="utf-8"))
    basic = [p for p in prior["pdfs"] if "hero-sheet-" not in p["path"]]
    for item in basic:
        if sha(ROOT / item["path"]) != item["sha256"]:
            problems.append(f"Basic Mode output changed during blank-only work: {item['path']}")
    inputs = [ROOT / p for p in ("typst/heroes/blank-record.typ", "typst/heroes/sheet.typ", "typst/heroes/parts.typ",
                                 "typst/aids/kit.typ", "typst/templates/system.typ", "config/design_tokens.json",
                                 "config/production.json", "tools/hero_sheet_qa.py", "tools/verify_inkjet_pdf.py")]
    inputs += list((ROOT / "fonts/static").glob("*"))
    inputs += [ROOT / f"typst/templates/marks/{p}/logo.svg" for p in ("cream", "white")]
    receipt = {"status": "FAIL" if problems else "PASS", "scope": "Blank record only; Basic Mode is deferred",
               "files": files, "review_images": images,
               "design_inputs": {str(p.relative_to(ROOT)): sha(p) for p in sorted(inputs) if p.is_file()},
               "unchanged_basic_pdf_count": len(basic), "unchanged_basic_pdf_hashes": basic,
               "problems": problems, "physical_print": "NOT TESTED",
               "limits": "Mechanical receipt only; author visual observations and owner aesthetic review are separate."}
    target = ROOT / "build/hero-redesign/blank/qa.json"
    target.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": receipt["status"], "files": len(files), "unchanged_basic_pdf_count": len(basic),
                      "problems": problems, "receipt": str(target)}, indent=2))
    return int(bool(problems))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--render-review", action="store_true")
    ap.add_argument("--only-blank", action="store_true", help="Audit the blank record without rebuilding Basic Mode Heroes")
    a = ap.parse_args()
    if a.only_blank:
        return audit_blank(a.render_review)
    REVIEW.mkdir(parents=True, exist_ok=True)
    data = json.loads(hero_cards.DATA.read_text(encoding="utf-8"))
    selections = json.loads((ROOT / "production/art/SELECTIONS.json").read_text(encoding="utf-8"))
    config = json.loads((ROOT / "config/production.json").read_text(encoding="utf-8"))
    files, problems, art, singles = [], [], [], []
    reviewed = []
    for hr in data["heroes"]:
        selected = selections[hr["art"]]
        ink = ROOT / selected["ink"]["path"]
        valid = selected["status"] == "approved" and sha(ink) == selected["ink"]["sha256"]
        if not valid:
            problems.append(f"{hr['name']}: art is unapproved or changed")
        art.append({"id": hr["art"], "sha256": sha(ink), "approval": selected["status"]})
    for paper in ("cream", "white"):
        pack = pymupdf.open(hero_cards.OUT / f"basic-heroes-{paper}.pdf")
        if len(pack) != 48:
            problems.append(f"{paper}: print pack must be 48 pages")
        stems = ["hero-sheet"] + [f"hero-{h['name'].lower()}" for h in data["heroes"]]
        for stem in stems + ["basic-heroes"]:
            path = hero_cards.OUT / f"{stem}-{paper}.pdf"
            result = inspect(path, config)
            doc = pymupdf.open(path)
            entry = {"path": str(path.relative_to(ROOT)), "sha256": sha(path), "pages": len(doc),
                     "print_preflight": result["status"], "failures": result["failure_examples_first_50"]}
            if result["status"] != "PASS":
                problems.append(f"{path.name}: print preflight failed")
            spans = [s for p in doc for s in signature(p)]
            entry["minimum_type_pt"] = min(s[1] for s in spans)
            entry["minimum_text_inset_pt"] = round(min(min(s[2][0], s[2][1], 612 - s[2][2], 792 - s[2][3]) for s in spans), 2)
            if paper == "white":
                cream = pymupdf.open(hero_cards.OUT / f"{stem}-cream.pdf")
                if len(cream) != len(doc) or any(signature(x) != signature(y) for x, y in zip(cream, doc)):
                    problems.append(f"{stem}: cream/white text or geometry differs")
            if stem.startswith("hero-") and not stem.startswith("hero-sheet"):
                hr = next(h for h in data["heroes"] if stem == "hero-" + h["name"].lower())
                errs = hero_cards.card_problems(path, hr, data["reminders"], data["notes"])
                problems.extend(f"{path.name}: {e}" for e in errs)
                entry["profile_coverage"] = "FAIL" if errs else "PASS"
                index = data["heroes"].index(hr)
                if len(pack) == 48:
                    if signature(pack[index * 2]) != signature(doc[0]):
                        problems.append(f"{hr['name']}: pack front differs")
                    if len(doc) != 2:
                        problems.append(f"{hr['name']}: every Hero must have exactly two populated sides")
                    elif signature(pack[index * 2 + 1]) != signature(doc[1]):
                        problems.append(f"{hr['name']}: pack reverse differs")
                if paper == "cream" and len(doc) == 1:
                    singles.append(hr["name"])
            files.append(entry)
            if a.render_review and stem != "basic-heroes":
                executable = shutil.which("pdftoppm")
                if not executable:
                    raise RuntimeError("Poppler pdftoppm is required for the review render")
                prefix = REVIEW / path.stem
                subprocess.run([executable, "-scale-to", "1100", "-png", str(path), str(prefix)], check=True,
                               capture_output=True)
                for image_path in sorted(REVIEW.glob(prefix.name + "-*.png")):
                    reviewed.append({"path": str(image_path.relative_to(ROOT)), "sha256": sha(image_path)})
    if a.render_review:
        for paper in ("cream", "white"):
            pages = [r for r in reviewed if f"-{paper}-" in r["path"]]
            for start in range(0, len(pages), 12):
                canvas = Image.new("RGB", (1500, 2720), "#d8d8d8")
                draw = ImageDraw.Draw(canvas)
                for k, item in enumerate(pages[start:start + 12]):
                    p = ROOT / item["path"]
                    im = Image.open(p).convert("RGB")
                    im.thumbnail((480, 635))
                    x, y = (k % 3) * 500, (k // 3) * 680
                    draw.text((x + 8, y + 5), p.stem, fill="black")
                    canvas.paste(im, (x + (500 - im.width) // 2, y + 25))
                canvas.save(REVIEW / f"contact-{paper}-{start // 12 + 1}.png")
    v = json.loads((ROOT / "source/versions.json").read_text(encoding="utf-8"))
    current = next(r for r in v["revisions"] if r["number"] == v["current"])
    source = ROOT / current["path"]
    bound = list((ROOT / "typst/heroes").glob("*")) + list((ROOT / "fonts/static").glob("*"))
    bound += [ROOT / p for p in ("tools/hero_cards.py", "tools/hero_sheet_qa.py", "tools/verify_inkjet_pdf.py",
                                "typst/aids/kit.typ", "typst/templates/system.typ", "config/design_tokens.json",
                                "config/production.json", "production/art/SELECTIONS.json")]
    receipt = {"status": "FAIL" if problems else "PASS", "source": current["path"], "source_sha256": sha(source),
               "one_sided_heroes": singles, "one_sided_count": len(singles), "two_sided_count": 24 - len(singles),
               "files": files, "art": art, "review_images": reviewed,
               "design_inputs": {str(p.relative_to(ROOT)): sha(p) for p in sorted(bound) if p.is_file()},
               "problems": problems, "physical_print": "NOT TESTED",
               "limits": "Mechanical receipt only. Visual observations are separate; not independent review or accessibility certification."}
    target = ROOT / "build/hero-redesign/qa.json"
    target.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "one_sided": len(singles), "two_sided": 24 - len(singles),
                      "problems": problems, "receipt": str(target)}, indent=2))
    return int(bool(problems))


if __name__ == "__main__":
    sys.exit(main())
