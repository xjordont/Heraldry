#!/usr/bin/env python3
"""Intake for ChatGPT Work artwork.

  scan               ink-prepare every new image in assets/art/incoming/ named <catalog id>.png|.jpg|.webp,
                     record it in SELECTIONS.json as status 'received' (route gpt) and write a review sheet
  approve --ids ...  orchestrator approval after visual review ('approved'; anchors: 'anchor-approved')
  approve-anchors    mark the received GPT anchors approved and make them the batch references
  reject --ids ...   reject (the entry returns to the queue)

Only 'approved'/'anchor-approved' art is placed in the book (tools/build_book.py)."""
import argparse, hashlib, json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import art_generate as g  # noqa: E402
from art_ink import prep  # noqa: E402

INCOMING = ROOT / "assets/art/incoming"
RECEIPTS = ROOT / "production/art/gpt/RECEIPTS.jsonl"
REVIEW = ROOT / "production/art/review"


def receipts():
    out = {}
    if RECEIPTS.exists():
        for line in RECEIPTS.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                out[r["id"]] = r
    return out


def scan(a):
    ents = {e["id"]: e for e in g.entries()}
    sels = g.load(g.SELECTIONS, {})
    rec = receipts()
    queue = {x["id"]: x for x in g.load(ROOT / "production/art/gpt/QUEUE.json", {"items": []})["items"]}
    new = []
    for f in sorted(INCOMING.iterdir()):
        if f.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp") or f.stem not in ents:
            continue
        data = f.read_bytes()
        if data[:7] == b"version":   # Git LFS pointer, not the image
            raise SystemExit(f"{f}: LFS pointer; run git lfs pull first")
        h = hashlib.sha256(data).hexdigest()
        s = sels.get(f.stem)
        if s and s.get("master", {}).get("sha256") == h:
            continue
        e = ents[f.stem]
        ink = g.INK / f"{f.stem}.png"
        info = prep(f, ink)
        im = Image.open(f)
        r = rec.get(f.stem, {})
        sels[f.stem] = {"family": e["family"], "title": e["title"], "heading_id": e.get("heading_id"), "route": "gpt",
                        "spec_sha256": e["spec_sha256"], "prompt_sha256": r.get("prompt_sha256") or queue.get(f.stem, {}).get("prompt_sha256"),
                        "status": "received", "received_at": g.now(),
                        "surface": r.get("surface", "ChatGPT Work image generation"), "model": r.get("model", "not recorded"),
                        "notes": r.get("notes", ""),
                        "master": {"path": str(f.relative_to(ROOT)), "sha256": h, "px": list(im.size)},
                        "ink": {"path": info["dst"], "sha256": hashlib.sha256(ink.read_bytes()).hexdigest(), "px": info["ink_px"],
                                "flags": info["flags"], "max_print_w_in_300ppi": info["max_print_w_in_300ppi"]},
                        "provenance": "AI-generated in ChatGPT Work from the recorded prompt; not hand-drawn."}
        new.append(f.stem)
    g.save(g.SELECTIONS, sels)
    if new:
        REVIEW.mkdir(parents=True, exist_ok=True)
        stamp = g.now()[:19].replace(":", "")
        for k in range(0, len(new), 24):
            g.sheet(new[k:k + 24], REVIEW / f"intake-{stamp}-{k // 24 + 1}.png", cell=420, cols=6)
            p = REVIEW / f"intake-{stamp}-{k // 24 + 1}.png"
            Image.open(p).convert("RGB").save(p.with_suffix(".jpg"), quality=82)
            p.unlink()
    print(json.dumps({"received": new}))


def set_status(ids, status):
    sels = g.load(g.SELECTIONS, {})
    for i in ids:
        if i not in sels:
            raise SystemExit(f"{i}: not received")
        sels[i]["status"] = status
        sels[i][status + "_at"] = g.now()
    g.save(g.SELECTIONS, sels)


def approve_anchors(a):
    ids = g.CFG["gpt_anchor_ids"]
    sels = g.load(g.SELECTIONS, {})
    missing = [i for i in ids if sels.get(i, {}).get("route") != "gpt"]
    if missing:
        raise SystemExit(f"GPT anchors not received: {missing}")
    set_status(ids, "anchor-approved")
    g.save(g.ANCHORS, {"route": "gpt", "status": "approved", "approved_at": g.now(), "approved_by": a.by,
                       "anchor_ids": ids, "references": [sels[i]["master"]["path"] for i in ids]})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["scan", "approve", "approve-anchors", "reject"])
    ap.add_argument("--ids", nargs="*", default=[])
    ap.add_argument("--by", default="orchestrator visual review")
    a = ap.parse_args()
    if a.cmd == "scan":
        scan(a)
    elif a.cmd == "approve":
        set_status(a.ids, "approved")
    elif a.cmd == "reject":
        set_status(a.ids, "rejected")
    else:
        approve_anchors(a)


if __name__ == "__main__":
    main()
