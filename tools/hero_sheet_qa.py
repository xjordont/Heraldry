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

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "build/hero-redesign/review"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_config():
    return json.loads((ROOT / "config/production.json").read_text(encoding="utf-8"))


def signature(page):
    return [(s["text"], round(s["size"], 3), tuple(round(v, 2) for v in s["bbox"]))
            for b in page.get_text("dict", flags=pymupdf.TEXTFLAGS_DICT & ~pymupdf.TEXT_PRESERVE_IMAGES)["blocks"]
            for line in b.get("lines", []) for s in line["spans"] if s["text"].strip()]


def page_check(path, config):
    """The PDF file contract: Letter portrait pages, searchable text at the minimum size or larger,
    essential text inside the safe edge, and every font embedded."""
    page_spec = config["page"]
    width, height = page_spec["width_pt"], page_spec["height_pt"]
    safe = page_spec["essential_edge_safe_inches"] * 72
    minimum = config["format"]["minimum_essential_text_pt"]
    failures, fonts, spans = [], set(), 0

    def fail(code, page, detail):
        if len(failures) < 50:
            failures.append({"code": code, "page": page, "detail": detail})

    with pymupdf.open(path) as doc:
        for n, page in enumerate(doc, 1):
            box = tuple(page.mediabox)
            if page.rotation or any(abs(a - b) > 0.1 for a, b in zip(box, (0, 0, width, height))):
                fail("page_size", n, {"rotation": page.rotation, "mediabox": list(box)})
            for text, size, (x0, y0, x1, y1) in signature(page):
                spans += 1
                if size < minimum - 0.1:
                    fail("small_type", n, {"size_pt": size, "text": text[:80]})
                if min(x0, y0, width - x1, height - y1) < safe - 0.1:
                    fail("unsafe_text", n, {"bbox": [x0, y0, x1, y1], "text": text[:80]})
            for font in page.get_fonts(full=True):
                xref = font[0]
                if xref in fonts:
                    continue
                fonts.add(xref)
                try:
                    embedded = bool(xref and doc.extract_font(xref)[3])
                except Exception:
                    embedded = False
                if not embedded:
                    fail("font_not_embedded", n, {"xref": xref, "font": font[3]})
    if not spans:
        fail("no_searchable_text", None, "the PDF must keep searchable text")
    return {"status": "FAIL" if failures else "PASS", "failures": failures}


def audit_blank(render_review):
    """Review only the blank form, preserving Basic Mode outputs and their review images."""
    review = ROOT / "build/hero-redesign/blank/review"
    review.mkdir(parents=True, exist_ok=True)
    config = load_config()
    files, images, problems = [], [], []
    path = hero_cards.OUT / "hero-sheet.pdf"
    result = page_check(path, config)
    doc = pymupdf.open(path)
    if len(doc) != 2:
        problems.append("blank must have exactly two pages")
    if result["status"] != "PASS":
        problems.append("blank page check failed")
    spans = [s for page in doc for s in signature(page)]
    files.append({"path": str(path.relative_to(ROOT)), "sha256": sha(path), "pages": len(doc),
                  "page_check": result["status"], "failures": result["failures"],
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
    # The prior receipt names each Basic Mode PDF as <stem>-cream.pdf or <stem>-white.pdf; the white set is
    # retired and the cream files are now named <stem>.pdf.
    prior = json.loads((ROOT / "production/qa/hero-sheet-design-review.json").read_text(encoding="utf-8"))
    basic = [p for p in prior["pdfs"] if "hero-sheet-" not in p["path"] and not p["path"].endswith("-white.pdf")]
    for item in basic:
        current = ROOT / item["path"].replace("\\", "/").replace("-cream.pdf", ".pdf")
        if not current.is_file() or sha(current) != item["sha256"]:
            problems.append(f"Basic Mode output changed during blank-only work: {current.relative_to(ROOT)}")
    inputs = [ROOT / p for p in ("typst/heroes/blank-record.typ", "typst/heroes/sheet.typ", "typst/heroes/parts.typ",
                                 "typst/aids/kit.typ", "typst/templates/system.typ", "config/design_tokens.json",
                                 "config/production.json", "tools/hero_sheet_qa.py")]
    inputs += list((ROOT / "fonts/static").glob("*"))
    inputs += [ROOT / "typst/templates/marks/cream/logo.svg"]
    receipt = {"status": "FAIL" if problems else "PASS", "scope": "Blank record only; Basic Mode is deferred",
               "files": files, "review_images": images,
               "design_inputs": {str(p.relative_to(ROOT)): sha(p) for p in sorted(inputs) if p.is_file()},
               "unchanged_basic_pdf_count": len(basic), "unchanged_basic_pdf_hashes": basic,
               "problems": problems,
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
    config = load_config()
    files, problems, art, singles = [], [], [], []
    reviewed = []
    for hr in data["heroes"]:
        selected = selections[hr["art"]]
        ink = ROOT / selected["ink"]["path"]
        valid = selected["status"] == "approved" and sha(ink) == selected["ink"]["sha256"]
        if not valid:
            problems.append(f"{hr['name']}: art is unapproved or changed")
        art.append({"id": hr["art"], "sha256": sha(ink), "approval": selected["status"]})
    pack = pymupdf.open(hero_cards.OUT / "basic-heroes.pdf")
    if len(pack) != 48:
        problems.append("pack must be 48 pages")
    stems = ["hero-sheet"] + [f"hero-{h['name'].lower()}" for h in data["heroes"]]
    for stem in stems + ["basic-heroes"]:
        path = hero_cards.OUT / f"{stem}.pdf"
        result = page_check(path, config)
        doc = pymupdf.open(path)
        entry = {"path": str(path.relative_to(ROOT)), "sha256": sha(path), "pages": len(doc),
                 "page_check": result["status"], "failures": result["failures"]}
        if result["status"] != "PASS":
            problems.append(f"{path.name}: page check failed")
        spans = [s for p in doc for s in signature(p)]
        entry["minimum_type_pt"] = min(s[1] for s in spans)
        entry["minimum_text_inset_pt"] = round(min(min(s[2][0], s[2][1], 612 - s[2][2], 792 - s[2][3]) for s in spans), 2)
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
            if len(doc) == 1:
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
        for start in range(0, len(reviewed), 12):
            canvas = Image.new("RGB", (1500, 2720), "#d8d8d8")
            draw = ImageDraw.Draw(canvas)
            for k, item in enumerate(reviewed[start:start + 12]):
                p = ROOT / item["path"]
                im = Image.open(p).convert("RGB")
                im.thumbnail((480, 635))
                x, y = (k % 3) * 500, (k // 3) * 680
                draw.text((x + 8, y + 5), p.stem, fill="black")
                canvas.paste(im, (x + (500 - im.width) // 2, y + 25))
            canvas.save(REVIEW / f"contact-{start // 12 + 1}.png")
    v = json.loads((ROOT / "source/versions.json").read_text(encoding="utf-8"))
    current = next(r for r in v["revisions"] if r["number"] == v["current"])
    source = ROOT / current["path"]
    bound = list((ROOT / "typst/heroes").glob("*")) + list((ROOT / "fonts/static").glob("*"))
    bound += [ROOT / p for p in ("tools/hero_cards.py", "tools/hero_sheet_qa.py",
                                "typst/aids/kit.typ", "typst/templates/system.typ", "config/design_tokens.json",
                                "config/production.json", "production/art/SELECTIONS.json")]
    receipt = {"status": "FAIL" if problems else "PASS", "source": current["path"], "source_sha256": sha(source),
               "one_sided_heroes": singles, "one_sided_count": len(singles), "two_sided_count": 24 - len(singles),
               "files": files, "art": art, "review_images": reviewed,
               "design_inputs": {str(p.relative_to(ROOT)): sha(p) for p in sorted(bound) if p.is_file()},
               "problems": problems,
               "limits": "Mechanical receipt only. Visual observations are separate; not independent review or accessibility certification."}
    target = ROOT / "build/hero-redesign/qa.json"
    target.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "one_sided": len(singles), "two_sided": 24 - len(singles),
                      "problems": problems, "receipt": str(target)}, indent=2))
    return int(bool(problems))


if __name__ == "__main__":
    sys.exit(main())
