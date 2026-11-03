#!/usr/bin/env python3
"""Screen-optimised digital edition (design audit 2026-11-01, P-03).

The verified digital PDF carries every raster at 300 ppi or more for print parity, which makes it
large. This tool writes a companion file for screens: the same pages, text, bookmarks, links and
attachments, with every placed raster downsampled to the target resolution at its placed size.
The print and verified digital PDFs are untouched; the companion is a convenience copy and is not
a print file (tools/check_art_ppi.py skips it by name).

    python tools/digital_compact.py IN.pdf OUT.pdf [--ppi 150] [--report production/qa/digital-compact.json]
"""
import argparse
import io
import json
from pathlib import Path

import pymupdf
from PIL import Image


def pixmap_image(doc, xref):
    """The image behind an xref as a PIL image with its soft mask applied (ink on transparency)."""
    pix = pymupdf.Pixmap(doc, xref)
    smask = doc.xref_get_key(xref, "SMask")
    if smask[0] == "xref":
        mask = pymupdf.Pixmap(doc, int(smask[1].split()[0]))
        if mask.width == pix.width and mask.height == pix.height:
            pix = pymupdf.Pixmap(pix, mask)
    if pix.n - pix.alpha not in (1, 3):
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    mode = {(1, 0): "L", (1, 1): "LA", (3, 0): "RGB", (3, 1): "RGBA"}[(pix.n - pix.alpha, pix.alpha)]
    return Image.frombytes(mode, (pix.width, pix.height), pix.samples)


def compact(src, dst, ppi=150):
    doc = pymupdf.open(str(src))
    before = {"pages": len(doc), "toc": len(doc.get_toc()), "links": sum(len(p.get_links()) for p in doc),
              "attachments": doc.embfile_count(), "bytes": Path(src).stat().st_size}
    # Smallest placement of every image xref across the book decides its new size; the first page that shows an
    # image is where it is replaced (one scan of the book, not one per image).
    placed, first_page = {}, {}
    for page in doc:
        for info in page.get_image_info(xrefs=True):
            xref = info.get("xref")
            if not xref:
                continue
            first_page.setdefault(xref, page.number)
            x0, y0, x1, y1 = info["bbox"]
            if x1 - x0 < 2 or y1 - y0 < 2:
                continue
            w_in = (x1 - x0) / 72
            placed[xref] = max(placed.get(xref, 0), w_in)
    changed, kept = [], 0
    for xref, w_in in placed.items():
        image = doc.extract_image(xref)
        wpx, hpx = image["width"], image["height"]
        current = wpx / w_in
        if current <= ppi * 1.05:
            kept += 1
            continue
        scale = ppi / current
        new_size = (max(1, round(wpx * scale)), max(1, round(hpx * scale)))
        pil = pixmap_image(doc, xref).resize(new_size, Image.LANCZOS)
        buffer = io.BytesIO()
        pil.save(buffer, format="PNG", optimize=True)
        doc[first_page[xref]].replace_image(xref, stream=buffer.getvalue())
        changed.append({"xref": xref, "pixels": [wpx, hpx], "new_pixels": list(new_size), "placed_in": round(w_in, 3)})
    # garbage=2 drops the replaced image streams and compacts the xref table; garbage=3/4 also hunt for duplicate
    # objects, which took over two minutes for 0.4% of the size. no_new_id keeps the file ID, so the same digital PDF
    # always yields the same companion (candidate and release match byte for byte).
    doc.save(str(dst), garbage=2, deflate=True, deflate_images=True, deflate_fonts=True, no_new_id=True)
    doc.close()
    with pymupdf.open(str(dst)) as out:
        after = {"pages": len(out), "toc": len(out.get_toc()), "links": sum(len(p.get_links()) for p in out),
                 "attachments": out.embfile_count(), "bytes": Path(dst).stat().st_size,
                 "lowest_ppi": None}
        worst = None
        for page in out:
            for info in page.get_image_info():
                x0, y0, x1, y1 = info["bbox"]
                if x1 - x0 < 2:
                    continue
                value = info["width"] / ((x1 - x0) / 72)
                worst = value if worst is None else min(worst, value)
        after["lowest_ppi"] = round(worst, 1) if worst is not None else None
    for key in ("pages", "toc", "links", "attachments"):
        if before[key] != after[key]:
            raise SystemExit(f"digital compact: {key} changed ({before[key]} -> {after[key]}); refusing to deliver")
    return {"source": str(src), "output": str(dst), "target_ppi": ppi, "before": before, "after": after,
            "images_downsampled": len(changed), "images_kept": kept, "images": changed[:400],
            "note": "Screen companion of the verified digital edition: same pages, text, bookmarks, links and attachments; rasters "
                    "downsampled to the target resolution at their placed size. Not a print file.", "status": "PASS"}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("source")
    ap.add_argument("output")
    ap.add_argument("--ppi", type=float, default=150)
    ap.add_argument("--report")
    a = ap.parse_args()
    report = compact(a.source, a.output, a.ppi)
    if a.report:
        Path(a.report).write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("images_downsampled", "images_kept")} |
                     {"bytes": [report["before"]["bytes"], report["after"]["bytes"]], "lowest_ppi": report["after"]["lowest_ppi"]}))


if __name__ == "__main__":
    main()
