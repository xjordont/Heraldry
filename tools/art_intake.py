#!/usr/bin/env python3
"""Intake for ChatGPT Work artwork.

  scan               ink-prepare every new image in assets/art/incoming/ named <catalog id>.png|.jpg|.webp and
                     record it in SELECTIONS.json as status 'received' (route gpt)
  approve --ids ...  orchestrator approval after visual review ('approved'; anchors: 'anchor-approved')
  approve-anchors    mark the received GPT anchors approved and make them the batch references
  reject --ids ... [--reason TEXT]   reject (the entry returns to the queue; the reason is shown to the operator as a redo)
  pending [--sheet]  received images awaiting review, flagged ones first; --sheet also writes contact sheets of them
                     to build/art/review/ (not committed; fetches their LFS ink files first). The reviewer opens flagged
                     ones at full size and reviews the rest from the sheets

Only 'approved'/'anchor-approved' art is placed in the book (tools/build_book.py)."""
import argparse, hashlib, json, re, subprocess, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import art_prompts as g  # noqa: E402
from art_ink import prep  # noqa: E402

INCOMING = ROOT / "assets/art/incoming"
RECEIPTS = ROOT / "production/art/gpt/RECEIPTS.jsonl"
REVIEW = ROOT / "build/art/review"      # local review sheets; never committed (one image per push would bloat history)
IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".webp")


def receipts():
    out = {}
    if RECEIPTS.exists():
        for line in RECEIPTS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                out[r["id"]] = r
    return out


def pointer_oid(data):
    m = re.search(rb"oid sha256:([0-9a-f]{64})", data[:300])
    return m.group(1).decode() if m else None


def needs_pull():
    """Incoming images that are LFS pointers and not yet recorded with the same bytes. A pointer's oid is the
    image's SHA-256, so the intake fetches only new images instead of the whole growing set every run."""
    sels = g.load(g.SELECTIONS, {})
    ents = {e["id"] for e in g.entries()}          # same filter as scan: legacy masters are never recorded, so never fetch them
    out = []
    for f in sorted(INCOMING.iterdir()):
        if f.suffix.lower() not in IMAGE_SUFFIXES or f.stem not in ents:
            continue
        with f.open("rb") as fh:
            data = fh.read(300)
        if data[:7] == b"version" and (sels.get(f.stem) or {}).get("master", {}).get("sha256") != pointer_oid(data):
            out.append(f.relative_to(ROOT).as_posix())
    return out


def scan(a):
    ents = {e["id"]: e for e in g.entries()}
    sels = g.load(g.SELECTIONS, {})
    rec = receipts()
    queue = {x["id"]: x for x in g.load(ROOT / "production/art/gpt/QUEUE.json", {"items": []})["items"]}
    new = []
    for f in sorted(INCOMING.iterdir()):
        if f.suffix.lower() not in IMAGE_SUFFIXES or f.stem not in ents:
            continue
        data = f.read_bytes()
        if data[:7] == b"version":   # Git LFS pointer, not the image
            oid = pointer_oid(data)
            if oid and (sels.get(f.stem) or {}).get("master", {}).get("sha256") == oid:
                continue             # already received with these exact bytes: no download needed
            raise SystemExit(f"{f}: LFS pointer of a new image; fetch it first (tools/art_intake.py needs-pull)")
        h = hashlib.sha256(data).hexdigest()
        s = sels.get(f.stem)
        if s and s.get("master", {}).get("sha256") == h:
            continue
        e = ents[f.stem]
        warn = []
        qsha = queue.get(f.stem, {}).get("prompt_sha256")
        if rec.get(f.stem, {}).get("prompt_sha256") and qsha and rec[f.stem]["prompt_sha256"] != qsha:
            warn.append("receipt prompt hash differs from the queued prompt")
        aw, ah = (int(x) for x in g.CFG["families"][e["family"]]["aspect"].split(":"))
        with Image.open(f) as _im:
            if abs(_im.width / _im.height - aw / ah) > 0.05 * aw / ah:
                warn.append(f"aspect {_im.width}x{_im.height} differs from {aw}:{ah}")
        ink = g.INK / f"{f.stem}.png"
        info = prep(f, ink)
        im = Image.open(f)
        r = rec.get(f.stem, {})
        made_in = r.get("surface") or "ChatGPT image generation"
        sels[f.stem] = {"family": e["family"], "title": e["title"], "heading_id": e.get("heading_id"), "route": "gpt",
                        "spec_sha256": e["spec_sha256"], "prompt_sha256": r.get("prompt_sha256") or queue.get(f.stem, {}).get("prompt_sha256"),
                        "status": "received", "received_at": g.now(),
                        "surface": made_in, "model": r.get("model", "not recorded"),
                        "notes": r.get("notes", ""), "intake_warnings": warn,
                        "master": {"path": str(f.relative_to(ROOT)), "sha256": h, "px": list(im.size)},
                        "ink": {"path": info["dst"], "sha256": hashlib.sha256(ink.read_bytes()).hexdigest(), "px": info["ink_px"],
                                "flags": info["flags"], "max_print_w_in_300ppi": info["max_print_w_in_300ppi"]},
                        "provenance": f"AI-generated in {made_in} from the recorded prompt; not hand-drawn."}
        new.append(f.stem)
    g.save(g.SELECTIONS, sels)
    print(json.dumps({"received": new}))


def review_sheets(ids):
    """Contact sheets (24 per sheet) of received images, in build/art/review/. Ink files still held as LFS
    pointers are fetched first, and only those."""
    sels = g.load(g.SELECTIONS, {})
    ptr = []
    for i in ids:
        p = sels[i]["ink"]["path"]
        with (ROOT / p).open("rb") as fh:
            if fh.read(7) == b"version":
                ptr.append(p)
    if ptr:
        subprocess.run(["git", "-C", str(ROOT), "lfs", "pull", "--include", ",".join(ptr), "--exclude", ""], check=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    for old in REVIEW.glob("pending-*.jpg"):
        old.unlink()
    out = []
    for k in range(0, len(ids), 24):
        p = REVIEW / f"pending-{k // 24 + 1}.png"
        g.sheet(ids[k:k + 24], p, cell=420, cols=6)
        Image.open(p).convert("RGB").save(p.with_suffix(".jpg"), quality=82)
        p.unlink()
        out.append(p.with_suffix(".jpg").relative_to(ROOT).as_posix())
    return out


def set_status(ids, status, reason=None):
    sels = g.load(g.SELECTIONS, {})
    for i in ids:
        if i not in sels:
            raise SystemExit(f"{i}: not received")
        sels[i]["status"] = status
        sels[i][status + "_at"] = g.now()
        if status == "rejected":
            if reason:
                sels[i]["rejected_reason"] = reason
            else:
                sels[i].pop("rejected_reason", None)
        else:
            sels[i].pop("rejected_reason", None)
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


def pending(a):
    """Compact review list: one line per received image, flagged first. Keeps the reviewer's token use low."""
    sels = g.load(g.SELECTIONS, {})
    rec = receipts()
    rows = []
    for i, v in sels.items():
        if v.get("route") != "gpt" or v.get("status") != "received":
            continue
        r = rec.get(i, {})
        flags = []
        if r.get("accepted_flags"):
            flags.append("ACCEPTED-FLAGS")
        if r.get("qa_failed_criteria"):
            flags.append("failed:" + ",".join(r["qa_failed_criteria"]))
        if r.get("qa_unresolved"):
            flags.append(f"{len(r['qa_unresolved'])} unresolved")
        if r.get("tripwires"):
            flags.append(f"{len(r['tripwires'])} tripwires")
        if v.get("intake_warnings") or (v.get("ink") or {}).get("flags"):
            flags.append("intake:" + ",".join((v.get("intake_warnings") or []) + ((v.get("ink") or {}).get("flags") or [])))
        rows.append((0 if flags else 1, v.get("family", ""), i, r.get("variants_tried"), "; ".join(flags) or "clean"))
    rows.sort()
    for _, fam, i, n, f in rows:
        print(f"{i}\t{fam}\tattempts={n}\t{f}")
    print(f"{len(rows)} received awaiting review ({sum(1 for r in rows if r[0] == 0)} flagged).")
    if a.sheet and rows:
        print("Sheets, in the order above: " + ", ".join(review_sheets([r[2] for r in rows])))
    elif rows:
        print("Contact sheets: tools/art_intake.py pending --sheet")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["scan", "approve", "approve-anchors", "reject", "pending", "needs-pull"])
    ap.add_argument("--ids", nargs="*", default=[])
    ap.add_argument("--by", default="orchestrator visual review")
    ap.add_argument("--reason", default=None, help="with reject: why, in a sentence the operator can turn into a correction")
    ap.add_argument("--sheet", action="store_true", help="with pending: also write contact sheets to build/art/review/")
    a = ap.parse_args()
    if a.cmd == "scan":
        scan(a)
    elif a.cmd == "approve":
        set_status(a.ids, "approved")
    elif a.cmd == "reject":
        set_status(a.ids, "rejected", a.reason)
    elif a.cmd == "pending":
        pending(a)
    elif a.cmd == "needs-pull":
        print(",".join(needs_pull()))
    else:
        approve_anchors(a)


if __name__ == "__main__":
    main()
