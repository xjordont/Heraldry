#!/usr/bin/env python3
"""Runner helpers for the Heraldry illustration queue (skill v4). Python 3.9+, Pillow only.

  doctor                         environment, repo, queue and reference checks (run first)
  status                         queue state and the single next action
  next [--n 8]                   the next items to generate
  show ID                        one item: references, size, must / do-not-draw lists, verbatim prompt
  check ID IMAGE                 mechanical tripwires for one generated image (not a quality score)
  save ID IMAGE [--attempts N]   check, copy the image unmodified into assets/art/incoming, write the receipt
  refuse ID --reason TEXT        record that the image tool refused an item (no image exists to save)
  sheet [ID ...]                 labelled contact sheet of saved images (default: all saved this session)
  bundle --out FILE.zip          hand-off zip for when git push is impossible

The repository is found by walking up from the current directory (or --repo). The queue,
prompts and receipts format belong to the repo (production/art/gpt/); this script only reads them.
Check thresholds were calibrated on the approved Greythorn render, the three owner style samples
and synthetic defects (wash, frame, crop, tint, grain, blur); see references/QA_CHECKLIST.md."""
import argparse, hashlib, json, os, re, subprocess, sys, tempfile, zipfile
from datetime import datetime, timezone
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageStat
except ImportError:                                           # pragma: no cover
    sys.exit("Pillow is required: pip install pillow")

QUEUE_REL = "production/art/gpt/QUEUE.json"
RECEIPTS_REL = "production/art/gpt/RECEIPTS.jsonl"
SELECTIONS_REL = "production/art/SELECTIONS.json"
INCOMING_REL = "assets/art/incoming"
IMAGE_EXT = {"PNG": ".png", "JPEG": ".jpg", "WEBP": ".webp"}
SIZES = {"1536x1024", "1024x1536", "1024x1024"}
LFS_MAGIC = b"version https://git-lfs"

# Mechanical tripwires. "scene" = vignette register; "figure" = isolated creature, person or still life.
T = {
    "min_long_side": 1000,
    "aspect_tol": 0.05,                                       # the intake warns at the same 5%
    "colour_warn": 0.10, "colour_fail": 0.25,                 # fraction of saturated pixels (art_ink's measure)
    "blank_fail": {"scene": 0.01, "figure": 0.003},           # non-paper fraction
    "sparse_warn": {"scene": 0.12, "figure": 0.02},
    "soft_warn": {"scene": 1500.0, "figure": 400.0},          # Laplacian variance at <=1280 px
    "paper_warn": 240, "paper_fail": 200,                     # 75th-percentile grey of the outer 3% band
    "grain_warn": 4.0,                                        # figure only: std of paper pixels in the band
    "wash_warn": 0.10, "wash_fail": 0.30,                     # figure only: mid-tone fraction
    "edge_warn": {"scene": 0.015, "figure": 0.0005},          # dark fraction of the outer 2% band
    "edge_fail": {"scene": 0.06, "figure": 0.004},
    "margin_warn": 0.02,                                      # figure only: dark fraction of the outer 6% band
}
LAPLACE = ImageFilter.Kernel((3, 3), [0, 1, 0, 1, -4, 1, 0, 1, 0], scale=1, offset=128)


class Fatal(Exception):
    pass


# ------------------------------------------------------------------ repo and queue
def find_repo(start=None):
    p = Path(start or os.getcwd()).resolve()
    for d in [p, *p.parents]:
        if (d / QUEUE_REL).is_file():
            return d
    raise Fatal(f"{QUEUE_REL} not found above {p}: run inside the Heraldry repository clone, or pass --repo")


def jload(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def prompt_text(repo, item):
    f = repo / item["prompt"]
    if not f.is_file():
        raise Fatal(f"prompt file missing: {item['prompt']} (pull main; the queue may have been republished)")
    t = f.read_text(encoding="utf-8")
    return t[:-1] if t.endswith("\n") else t


def prompt_sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def load_queue(repo):
    q = jload(repo / QUEUE_REL)
    if not q:
        raise Fatal("QUEUE.json is unreadable")
    if q.get("schema", 1) < 2:
        raise Fatal("QUEUE.json is schema 1 (no per-item references): git pull main, or ask Claude Code to republish the queue")
    return q


def item_of(q, iid):
    for it in q["items"]:
        if it["id"] == iid:
            return it
    raise Fatal(f"{iid} is not in QUEUE.json (phase {q['phase']}): never generate an ID the queue does not list")


def git(repo, *args):
    try:
        r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=120)
        return r.returncode, r.stdout
    except (OSError, subprocess.SubprocessError):
        return 127, ""


def local_files(repo, iid):
    d = repo / INCOMING_REL
    return sorted(f for f in d.glob(iid + ".*") if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")) if d.is_dir() else []


def git_ok(repo):
    code, out = git(repo, "rev-parse", "--is-inside-work-tree")
    return code == 0 and out.strip() == "true"


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def states(repo, q):
    """pending: no image; redo: image exists but the reviewer rejected it and it is not re-saved;
    saved: image exists and has not been sent (git: uncommitted or unpushed; no git: not yet recorded by the
    intake with the same bytes); pushed: image exists and was sent; refused: the latest receipt is a refusal."""
    sels = jload(repo / SELECTIONS_REL, {})
    have_git = git_ok(repo)
    changed, ahead = set(), set()
    if have_git:
        code, out = git(repo, "status", "--porcelain", "--untracked-files=all", "--", INCOMING_REL)
        changed = {line[3:].strip().strip('"') for line in out.splitlines()} if code == 0 else set()
        code, out = git(repo, "log", "origin/main..HEAD", "--name-only", "--pretty=format:", "--", INCOMING_REL)
        ahead = {line.strip() for line in out.splitlines() if line.strip()} if code == 0 else set()
    refused = {i for i, r in last_receipts(repo).items() if r.get("refused")}
    res = {}
    for it in q["items"]:
        files = local_files(repo, it["id"])
        rels = {f.relative_to(repo).as_posix() for f in files}
        if it["id"] in refused:
            res[it["id"]] = "refused"
        elif not files:
            res[it["id"]] = "pending"
        elif (rels & (changed | ahead)) if have_git else sels.get(it["id"], {}).get("master", {}).get("sha256") != file_sha(files[0]):
            res[it["id"]] = "saved"
        elif sels.get(it["id"], {}).get("status") == "rejected":
            res[it["id"]] = "redo"
        else:
            res[it["id"]] = "pushed"
    return res


def last_receipts(repo):
    """The most recent receipt line per ID (a later save replaces an earlier refusal)."""
    out = {}
    f = repo / RECEIPTS_REL
    for line in f.read_text(encoding="utf-8").splitlines() if f.is_file() else []:
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if isinstance(r, dict) and "id" in r:
            out[r["id"]] = r
    return out


def receipts_unpushed(repo):
    """True when RECEIPTS.jsonl has uncommitted changes or commits that are not on origin/main."""
    code, out = git(repo, "status", "--porcelain", "--untracked-files=all", "--", RECEIPTS_REL)
    if code == 0 and out.strip():
        return True
    code, out = git(repo, "log", "origin/main..HEAD", "--name-only", "--pretty=format:", "--", RECEIPTS_REL)
    return code == 0 and bool(out.strip())


# ------------------------------------------------------------------ image measurements
def _flat_rgb(im):
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        im = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)), im)
    return im.convert("RGB")


def _levels(hist, n):
    def pct(p):
        acc = 0
        for v, c in enumerate(hist):
            acc += c
            if acc >= p * n:
                return v
        return 255
    white, black = max(pct(0.90), 200), min(pct(0.01), 90)
    return black + 10, white - 18                             # same paper / ink levels as tools/art_ink.py


def _bands(w, h, frac):
    bx, by = max(1, int(w * frac)), max(1, int(h * frac))
    return ((0, 0, w, by), (0, h - by, w, h), (0, 0, bx, h), (w - bx, 0, w, h))


def measure(path):
    with Image.open(path) as src:
        fmt = src.format
        src.load()
        im = _flat_rgb(src)
    w, h = im.size
    n = w * h
    g = ImageOps.grayscale(im)
    hist = g.histogram()
    lo, hi = _levels(hist, n)
    cut = (lo + hi) // 2
    dark = g.point([255 if v < cut else 0 for v in range(256)])

    def dark_frac(frac):
        boxes = _bands(w, h, frac)
        cnt = sum(dark.crop(b).histogram()[255] for b in boxes)
        return cnt / sum((b[2] - b[0]) * (b[3] - b[1]) for b in boxes)

    sat = im.convert("HSV").getchannel("S").point([255 if v > 60 else 0 for v in range(256)])
    # paper tone and noise in the outer 3% band, from histograms (no per-pixel loops)
    band_hist = [0] * 256
    for b in _bands(w, h, 0.03):
        for v, c in enumerate(g.crop(b).histogram()):
            band_hist[v] += c
    tot = sum(band_hist)
    acc, p75 = 0, 255
    for v, c in enumerate(band_hist):
        acc += c
        if acc >= 0.75 * tot:
            p75 = v
            break
    bright = [(v, c) for v, c in enumerate(band_hist) if v >= 200 and c]
    bn = sum(c for _, c in bright)
    mean = sum(v * c for v, c in bright) / bn if bn else 0
    grain = (sum(c * (v - mean) ** 2 for v, c in bright) / bn) ** 0.5 if bn else 0
    k = 1280 / max(w, h)
    gs = g.resize((max(1, int(w * k)), max(1, int(h * k))), Image.LANCZOS) if k < 1 else g
    soft = ImageStat.Stat(gs.filter(LAPLACE)).var[0]
    # tools/art_ink.py intake flags, same formulas, so the two never disagree about what the intake will say
    span = max(hi - lo, 1)

    def alpha(v):
        if v >= hi:
            return 0
        if v <= lo:
            return 255
        return int(round(255 * min(1.0, ((hi - v) / span) ** 0.8 * 1.15)))
    bw = g.point([255 if alpha(v) > 128 else 0 for v in range(256)])
    border = 0.0
    for b in ((0, 0, w, 3), (0, h - 3, w, h), (0, 0, 3, h), (w - 3, 0, w, h)):
        border += bw.crop(b).histogram()[255] / max(1, (b[2] - b[0]) * (b[3] - b[1]))
    return {"format": fmt, "px": [w, h],
            "colour": sum(sat.histogram()[255:]) / n,
            "midtone": sum(hist[lo + 25:hi - 25]) / n if hi - lo > 60 else 0.0,
            "intake_border_ink": border / 4,
            "nonpaper": sum(hist[:200]) / n, "sharpness": soft, "paper_tone": p75, "paper_grain": grain,
            "edge2": dark_frac(0.02), "edge6": dark_frac(0.06)}


def evaluate(m, item):
    """Return (fails, warns, infos) for the measurements of one image against its queue item."""
    reg = "scene" if item["register"] == "scene" else "figure"
    fails, warns, infos = [], [], []
    w, h = m["px"]
    ew, eh = (int(x) for x in item["size"].split("x"))
    if m["format"] not in IMAGE_EXT:
        fails.append(f"format {m['format']}: the image must be PNG, JPEG or WEBP")
    if max(w, h) < T["min_long_side"]:
        fails.append(f"only {max(w, h)} px on the long side (minimum {T['min_long_side']}): regenerate at the full size")
    if abs((w / h) - (ew / eh)) / (ew / eh) > T["aspect_tol"]:
        fails.append(f"aspect {w}x{h} is not {ew}x{eh}: regenerate wide 3:2, tall 2:3 or square 1:1 as the queue says")
    c = m["colour"]
    if c > T["colour_fail"]:
        fails.append(f"coloured image ({c:.0%} saturated pixels): pure black ink only")
    elif c > T["colour_warn"]:
        warns.append(f"tinted ink or coloured accents ({c:.0%} saturated pixels): look closely; the book prints black ink only")
    if m["nonpaper"] < T["blank_fail"][reg]:
        fails.append(f"almost no ink ({m['nonpaper']:.1%}): blank or failed generation")
    elif m["nonpaper"] < T["sparse_warn"][reg]:
        warns.append(f"very little ink ({m['nonpaper']:.0%}): the subject may be tiny or faint at print size")
    if m["sharpness"] < T["soft_warn"][reg]:
        warns.append(f"soft or blurry linework (sharpness {m['sharpness']:.0f}): pen lines should be crisp")
    if m["paper_tone"] < T["paper_fail"]:
        fails.append(f"dark or tinted background (paper tone {m['paper_tone']}): flat near-white paper only")
    elif m["paper_tone"] < T["paper_warn"]:
        warns.append(f"paper is not clean white (tone {m['paper_tone']}): stains, a darkened vignette or a grey wash")
    if reg == "figure":
        if m["paper_grain"] > T["grain_warn"]:
            warns.append(f"grain or noise in the margin (sigma {m['paper_grain']:.1f}): the background must be flat")
        if m["midtone"] > T["wash_fail"]:
            fails.append(f"heavy grey wash ({m['midtone']:.0%} mid-tones): shading must be ink marks only")
        elif m["midtone"] > T["wash_warn"]:
            warns.append(f"possible grey wash or soft shading ({m['midtone']:.0%} mid-tones): shading must be ink marks only")
        if m["edge2"] > T["edge_fail"]["figure"]:
            fails.append(f"ink touches the image edge ({m['edge2']:.2%} of the outer band): a limb, weapon, shadow or frame is cropped")
        elif m["edge2"] > T["edge_warn"]["figure"]:
            warns.append(f"stray marks reach the image edge ({m['edge2']:.2%}): check nothing is cropped")
        if m["edge6"] > T["margin_warn"]:
            warns.append(f"the drawing enters the outer 6% margin ({m['edge6']:.1%}): 8% clean margin is requested")
    else:
        if m["edge2"] > T["edge_fail"]["scene"]:
            fails.append(f"ink runs to the image edge ({m['edge2']:.0%} of the outer band): no white vignette, or a frame or box")
        elif m["edge2"] > T["edge_warn"]["scene"]:
            warns.append(f"marks reach the outer 2% of the frame ({m['edge2']:.1%}): check all four edges fade to white")
    flags = [name for name, bad in (("colour", m["colour"] > 0.10), ("gray_wash", m["midtone"] > 0.60),
                                    ("frame_or_box", m["intake_border_ink"] > 0.25)) if bad]
    if flags:
        infos.append("the intake will also flag: " + ", ".join(flags) + " (flags go to the reviewer; they do not reject)")
    return fails, warns, infos


def preview(path, item, outdir):
    with Image.open(path) as src:
        im = _flat_rgb(src)
    width = max(200, int(item["print_w_in"] * 150))
    im = im.resize((width, max(1, round(width * im.height / im.width))), Image.LANCZOS)
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / f"{item['id']}_print_size.png"
    im.save(out)
    return out


def scratch_dir():
    return Path(tempfile.gettempdir()) / "heraldry_art"


# ------------------------------------------------------------------ commands
def cmd_doctor(a, repo):
    q = load_queue(repo)
    blockers, delivery, notes = [], [], []
    if sys.version_info < (3, 9):
        blockers.append("Python 3.9 or newer is required")
    if not git_ok(repo):
        delivery.append("git is not available here")
    else:
        code, branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
        if branch.strip() != "main":
            blockers.append(f"on branch {branch.strip()!r}: work on main only, never create branches")
        if git(repo, "lfs", "version")[0] != 0:
            delivery.append("git-lfs is not installed (PNGs would be committed as ordinary files; the repo stores them with LFS)")
        attrs = (repo / ".gitattributes").read_text() if (repo / ".gitattributes").is_file() else ""
        if "assets/art/incoming/*.png" not in attrs:
            blockers.append(".gitattributes lacks the assets/art/incoming/*.png LFS rule: git pull --rebase origin main")
        rc, out = git(repo, "status", "--porcelain", "--untracked-files=no")
        if rc == 0 and out.strip():
            notes.append("tracked files have uncommitted changes (fine if they are yours from this session)")
    bad_prompts = 0
    for it in q["items"]:
        try:
            if prompt_sha(prompt_text(repo, it)) != it["prompt_sha256"]:
                bad_prompts += 1
        except Fatal:
            bad_prompts += 1
        for r in it["references"]:
            f = repo / r
            if not f.is_file():
                blockers.append(f"reference missing for {it['id']}: {r}")
            elif f.read_bytes()[:len(LFS_MAGIC)] == LFS_MAGIC:
                blockers.append(f"reference is an LFS pointer, not an image: {r} (git lfs pull --include={r})")
    if bad_prompts:
        blockers.append(f"{bad_prompts} prompt files are missing or no longer match the queue hashes: git pull --rebase origin main")
    blockers = list(dict.fromkeys(blockers))
    print(f"queue phase={q['phase']} items={q['count']} schema={q.get('schema')}")
    for n in notes:
        print("note:", n)
    if blockers:
        print("NOT READY:")
        for b in blockers + delivery:
            print(" -", b)
        return 1
    if delivery:
        print("READY TO GENERATE. Delivery by git is blocked: " + "; ".join(delivery)
              + ". Keep generating and saving, then finish each batch with `bundle --out batch.zip` and hand the zip to the owner.")
        return 0
    print("READY")
    return 0


def cmd_status(a, repo):
    q = load_queue(repo)
    st = states(repo, q)
    count = lambda s: sum(1 for v in st.values() if v == s)  # noqa: E731
    refused = [i for i, v in st.items() if v == "refused"]
    print(f"phase={q['phase']} items={q['count']} generated_at={q['generated_at']}")
    print(f"pending={count('pending')} redo={count('redo')} saved-not-pushed={count('saved')} pushed={count('pushed')} refused={len(refused)}")
    if refused:
        print("refused by the image tool (Claude Code owns the prompt): " + ", ".join(refused))
    todo = [i for i, v in st.items() if v in ("redo", "pending")]
    unpushed = count("saved") or receipts_unpushed(repo)
    if count("saved") and not git_ok(repo):
        action = "BUNDLE the saved images (python scripts/heraldry_art.py bundle --out batch.zip) and hand the zip to the owner: git is not available here."
    elif unpushed:
        action = ("COMMIT AND PUSH the saved images and RECEIPTS.jsonl "
                  "(git add assets/art/incoming production/art/gpt/RECEIPTS.jsonl; commit; git pull --rebase origin main; git push origin main).")
    elif todo:
        action = f"GENERATE next: {', '.join(todo[:3])}{' ...' if len(todo) > 3 else ''}  (python scripts/heraldry_art.py next)"
    elif q["phase"] == "anchors":
        action = ("STOP. The anchors are done"
                  + (f" ({len(refused)} refused: {', '.join(refused)})" if refused else "")
                  + ". Tell the owner: ask Claude Code to review the anchors and publish the batch queue. Do not start the batch.")
    else:
        action = ("NOTHING LEFT to generate in this queue"
                  + (f" ({len(refused)} refused: {', '.join(refused)}; tell Claude Code)" if refused else "")
                  + ". git pull origin main and run status again; a new queue means new work.")
    print("NEXT ACTION:", action)
    return 0


def cmd_next(a, repo):
    q = load_queue(repo)
    st = states(repo, q)
    todo = [it for it in q["items"] if st[it["id"]] == "redo"] + [it for it in q["items"] if st[it["id"]] == "pending"]
    for it in todo[:a.n]:
        refs = ", ".join(Path(r).name for r in it["references"])
        print(f"{it['id']}  [{st[it['id']]}] {it['title']} | {it['size']} | {it['register']} | tries<={it['max_attempts']} | refs: {refs}")
    if not todo:
        print("nothing pending")
    return 0


def cmd_show(a, repo):
    q = load_queue(repo)
    it = item_of(q, a.id)
    text = prompt_text(repo, it)
    if prompt_sha(text) != it["prompt_sha256"]:
        raise Fatal(f"{it['prompt']} does not match the queue hash: git pull --rebase origin main, then retry")
    print(f"ID: {it['id']}\nTITLE: {it['title']}\nFAMILY/REGISTER: {it['family']}/{it['register']}")
    print(f"SIZE: {it['size']}   PRINTED WIDTH: {it['print_w_in']} in   ATTEMPTS: at most {it['max_attempts']}")
    print("ATTACH THESE REFERENCES (and no others):")
    for r in it["references"]:
        print("  ", r)
    if it["size_class"]:
        print("SIZE CLASS:", it["size_class"])
    print("MUST BE SHOWN EXACTLY:" + ("" if it["must"] else " (none listed)"))
    for m in it["must"]:
        print("  *", m)
    print("DO NOT DRAW:" + ("" if it["avoid"] else " (none listed)"))
    for x in it["avoid"]:
        print("  *", x)
    print("-----8<----- PROMPT (use verbatim) -----8<-----")
    print(text)
    print("-----8<----- END PROMPT -----8<-----")
    return 0


def run_check(repo, q, iid, image):
    it = item_of(q, iid)
    image = Path(image)
    if not image.is_file():
        raise Fatal(f"{image}: no such file")
    try:
        m = measure(image)
    except Exception as e:                                     # undecodable or truncated image
        raise Fatal(f"{image}: not a readable image ({e})")
    fails, warns, infos = evaluate(m, it)
    pv = preview(image, it, scratch_dir())
    return it, m, fails, warns, infos, pv


def cmd_check(a, repo):
    q = load_queue(repo)
    it, m, fails, warns, infos, pv = run_check(repo, q, a.id, a.image)
    verdict = "FAIL" if fails else "WARN" if warns else "PASS"
    if a.json:
        print(json.dumps({"id": it["id"], "result": verdict, "fails": fails, "warns": warns, "infos": infos,
                          "metrics": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in m.items()},
                          "print_size_preview": str(pv)}, indent=1))
    else:
        print(f"{it['id']}: {m['px'][0]}x{m['px'][1]} {m['format']} (queue size {it['size']})")
        for f in fails:
            print("FAIL", f)
        for w in warns:
            print("WARN", w)
        for i in infos:
            print("info", i)
        print(f"RESULT: {verdict}   print-size preview ({it['print_w_in']} in wide): {pv}")
        print("These are tripwires, not a quality score. Now run the visual checklist in references/QA_CHECKLIST.md.")
    return 1 if fails else 0


def append_receipt(repo, rec):
    f = repo / RECEIPTS_REL
    f.parent.mkdir(parents=True, exist_ok=True)
    prefix = "\n" if f.exists() and f.stat().st_size and not f.read_bytes().endswith(b"\n") else ""
    with f.open("a", encoding="utf-8") as fh:
        fh.write(prefix + json.dumps(rec, ensure_ascii=False) + "\n")


def cmd_save(a, repo):
    q = load_queue(repo)
    it, m, fails, warns, infos, pv = run_check(repo, q, a.id, a.image)
    text = prompt_text(repo, it)
    if prompt_sha(text) != it["prompt_sha256"]:
        raise Fatal(f"{it['prompt']} does not match the queue hash: git pull --rebase origin main, then regenerate from the current prompt")
    state = states(repo, q)[it["id"]]
    if state == "pushed" and not a.redo:
        raise Fatal(f"{it['id']} is already delivered and was not rejected: pass --redo only if the owner or Claude Code asked for a redo")
    if fails and not a.accept_flags:
        for f in fails:
            print("FAIL", f)
        raise Fatal("mechanical failures: regenerate (attempts are limited to "
                    f"{it['max_attempts']}), or pass --accept-flags if this is the best attempt after the last allowed one")
    if a.attempts > it["max_attempts"]:
        warns.append(f"{a.attempts} attempts exceeds the budget of {it['max_attempts']}")
    ext = IMAGE_EXT[m["format"]]
    dest = repo / INCOMING_REL / (it["id"] + ext)
    dest.parent.mkdir(parents=True, exist_ok=True)
    data = Path(a.image).read_bytes()
    dest.write_bytes(data)
    if hashlib.sha256(dest.read_bytes()).hexdigest() != hashlib.sha256(data).hexdigest():
        raise Fatal("copy verification failed")
    for stale in local_files(repo, it["id"]):
        if stale != dest:
            stale.unlink()
            print(f"removed the older {stale.name} (one file per ID)")
    rec = {"id": it["id"], "prompt_sha256": it["prompt_sha256"], "surface": "ChatGPT Work", "model": a.model or "not shown",
           "date_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "variants_tried": a.attempts,
           "notes": a.notes or ""}
    if fails or warns:
        rec["tripwires"] = fails + warns
    append_receipt(repo, rec)
    print(f"saved {dest.relative_to(repo)} ({len(data)} bytes, unmodified) and wrote the receipt")
    if fails:
        print("saved with FAIL tripwires recorded in the receipt: the reviewer will see them")
    print("next: git add " + f"{dest.relative_to(repo)} {RECEIPTS_REL}")
    return 0


def cmd_refuse(a, repo):
    q = load_queue(repo)
    it = item_of(q, a.id)
    append_receipt(repo, {"id": it["id"], "refused": True, "reason": a.reason, "surface": "ChatGPT Work",
                          "date_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d")})
    print(f"recorded the refusal of {it['id']} in {RECEIPTS_REL}: commit it with the next batch and name the item in your report")
    return 0


def cmd_sheet(a, repo):
    q = load_queue(repo)
    st = states(repo, q)
    ids = a.ids or [i for i, v in st.items() if v == "saved"]
    if not ids:
        raise Fatal("no saved images to put on a sheet")
    cell, cols = 360, 4
    items = [item_of(q, i) for i in ids]
    files = []
    for it in items:
        fl = local_files(repo, it["id"])
        if not fl:
            raise Fatal(f"{it['id']}: no saved image")
        files.append(fl[0])
    if a.refs:
        for r in items[0]["references"]:
            files.append(repo / r)
            items.append({"id": "REF " + Path(r).name[:22]})
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, rows * (cell + 22)), "white")
    d = ImageDraw.Draw(sheet)
    for n, (f, it) in enumerate(zip(files, items)):
        with Image.open(f) as src:
            im = _flat_rgb(src)
        im.thumbnail((cell - 8, cell - 8))
        x, y = (n % cols) * cell, (n // cols) * (cell + 22)
        sheet.paste(im, (x + (cell - im.width) // 2, y + 22))
        d.text((x + 6, y + 5), it["id"], fill=(0, 0, 0))
    out = Path(a.out) if a.out else scratch_dir() / "batch_sheet.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=85)
    print(f"contact sheet: {out}  ({len(ids)} images{', plus references' if a.refs else ''})")
    return 0


def cmd_bundle(a, repo):
    q = load_queue(repo)
    st = states(repo, q)
    ids = [i for i, v in st.items() if v == "saved"]
    if not ids:
        raise Fatal("nothing saved to bundle")
    receipts = {}
    for line in (repo / RECEIPTS_REL).read_text(encoding="utf-8").splitlines() if (repo / RECEIPTS_REL).is_file() else []:
        if line.strip():
            r = json.loads(line)
            receipts[r["id"]] = line
    out = Path(a.out)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for i in ids:
            for f in local_files(repo, i):
                z.write(f, f.relative_to(repo).as_posix())
        z.writestr("receipts_append.jsonl", "\n".join(receipts[i] for i in ids if i in receipts) + "\n")
        z.writestr("HANDOFF.txt", "Unzip at the repository root. Append receipts_append.jsonl to production/art/gpt/RECEIPTS.jsonl.\n"
                   "git lfs install; git add assets/art/incoming production/art/gpt/RECEIPTS.jsonl\n"
                   f"git commit -m 'art(gpt): {ids[0]} .. {ids[-1]}'; git pull --rebase origin main; git push origin main\n")
    print(f"bundle: {out} ({len(ids)} images)")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", help="repository root (default: found above the current directory)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor")
    sub.add_parser("status")
    p = sub.add_parser("next")
    p.add_argument("--n", type=int, default=8)
    p = sub.add_parser("show")
    p.add_argument("id")
    p = sub.add_parser("check")
    p.add_argument("id")
    p.add_argument("image")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("save")
    p.add_argument("id")
    p.add_argument("image")
    p.add_argument("--attempts", type=int, default=1)
    p.add_argument("--model", default="")
    p.add_argument("--notes", default="")
    p.add_argument("--accept-flags", action="store_true")
    p.add_argument("--redo", action="store_true")
    p = sub.add_parser("refuse")
    p.add_argument("id")
    p.add_argument("--reason", required=True)
    p = sub.add_parser("sheet")
    p.add_argument("ids", nargs="*")
    p.add_argument("--out")
    p.add_argument("--refs", action="store_true")
    p = sub.add_parser("bundle")
    p.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    try:
        repo = find_repo(a.repo)
        return globals()["cmd_" + a.cmd](a, repo)
    except Fatal as e:
        print("ERROR:", e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
