#!/usr/bin/env python3
"""Runner helpers for the Heraldry illustration queue (skill v6). Python 3.9+, Pillow only.

  doctor                         environment, repo, queue and reference checks (run first)
  status [--end]                 queue state and the single next action (--end: session end, push anything unsent)
  next [--n 8]                   the next items to generate
  show ID                        one item: references, size, must / do-not-draw lists, verbatim prompt
  check ID IMAGE                 mechanical tripwires for one generated image; counts it as an attempt
  save ID IMAGE --must ... --avoid-clear   check, copy the image unmodified into assets/art/incoming, write the receipt
  refuse ID --reason TEXT        record that the image tool refused an item (no image exists to save)
  sheet [ID ...] [--refs]        labelled contact sheet (default: every saved image not yet pushed; name IDs for others)
  bundle [--out FILE.zip] [--evidence FILE ...]   review hand-off zip when git push is impossible (default: the scratch folder)

The repository is found by walking up from the current directory (or --repo). The queue,
prompts and receipts format belong to the repo (production/art/gpt/); this script only reads them.
An offline Work input package (WORK_PACKAGE.json at its root, no .git) works the same way, with git
never used: images and receipts are saved inside it and delivered only by `bundle`.
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
PACKAGE_REL = "WORK_PACKAGE.json"
IMAGE_EXT = {"PNG": ".png", "JPEG": ".jpg", "WEBP": ".webp"}
SIZES = {"1536x1024", "1024x1536", "1024x1024"}
LFS_MAGIC = b"version https://git-lfs"
HELPER_IN_REPO = "production/art/skill/heraldry-classic-ink-art/scripts/heraldry_art.py"
_REPO = None                 # set by main(): lets messages name the repo's own copy of this helper
BATCH_PUSH_AT = 5            # status asks for a push once this many saved images are unsent
ROUND_ENDS = ("redo", "pushed", "pending", "refused")
STATE_WORDS = {"pending": "pending (nothing delivered yet)", "redo": "redo (the reviewer sent this image back)",
               "saved": "saved here, not pushed yet", "pushed": "delivered (pushed); awaiting or past review",
               "refused": "refused by the image tool (recorded)"}
# statements that admit the must-show item is absent or could not be checked: that is a hard fail, not a pass
ADMISSION = re.compile(r"(?<![a-z])(?:could ?n[o']t|couldn't|cannot|can't|can not|unable|not (?:drawn|shown|visible|present|depicted|verifiable|verified)"
                       r"|missing|absent|fails?|failed|wrong|incorrect|zero)(?![a-z])|(?<![\d.])0 [a-z]", re.I)
LOOKALIKE_MAX = 16           # of 256 difference bits: closer than this is warned as a re-encoded or resized copy

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
    raise Fatal(f"{QUEUE_REL} not found above {p}: cd into the Heraldry repository clone and run the repo's own copy of the helper "
                f"({HELPER_IN_REPO}), or pass --repo")


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
    """True only for a Git checkout rooted at repo. A folder unzipped inside some other checkout is not one."""
    if not (Path(repo) / ".git").exists():
        return False
    code, out = git(repo, "rev-parse", "--is-inside-work-tree")
    return code == 0 and out.strip() == "true"


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def local_sha(path):
    """sha256 of a delivered image. An LFS pointer file carries the real image's sha256 as its oid."""
    data = Path(path).read_bytes()
    if data[:len(LFS_MAGIC)] == LFS_MAGIC:
        m = re.search(rb"oid sha256:([0-9a-f]{64})", data)
        return m.group(1).decode() if m else None
    return hashlib.sha256(data).hexdigest()


def incoming_changes(repo):
    """(have_git, changed, ahead): paths under assets/art/incoming that are uncommitted, or committed but not on origin/main."""
    if not git_ok(repo):
        return False, set(), set()
    code, out = git(repo, "status", "--porcelain", "--untracked-files=all", "--", INCOMING_REL)
    changed = {line[3:].strip().strip('"') for line in out.splitlines()} if code == 0 else set()
    code, out = git(repo, "log", "origin/main..HEAD", "--name-only", "--pretty=format:", "--", INCOMING_REL)
    ahead = {line.strip() for line in out.splitlines() if line.strip()} if code == 0 else set()
    return True, changed, ahead


def states(repo, q):
    """pending: no image; redo: image exists but the reviewer rejected it and it is not re-saved;
    saved: image exists and has not been sent (git: uncommitted or unpushed; no git: not yet recorded by the
    intake with the same bytes); pushed: image exists and was sent; refused: the latest receipt is a refusal."""
    sels = jload(repo / SELECTIONS_REL, {})
    have_git, changed, ahead = incoming_changes(repo)
    refused = {i for i, r in last_receipts(repo).items() if r.get("refused")}
    res = {}
    for it in q["items"]:
        files = local_files(repo, it["id"])
        rels = {f.relative_to(repo).as_posix() for f in files}
        if it["id"] in refused:
            res[it["id"]] = "refused"
        elif not files:
            res[it["id"]] = "pending"
        elif (rels & (changed | ahead)) if have_git else sels.get(it["id"], {}).get("master", {}).get("sha256") != local_sha(files[0]):
            res[it["id"]] = "saved"
        elif sels.get(it["id"], {}).get("status") == "rejected" and still_the_rejected_image(sels[it["id"]], files[0]):
            res[it["id"]] = "redo"
        else:
            res[it["id"]] = "pushed"
    return res


def still_the_rejected_image(sel, file):
    """A rejected item stays 'redo' only while the local file is still the image that was rejected. Once a different
    image has been pushed it is awaiting the intake, whatever SELECTIONS.json still says."""
    sha = (sel.get("master") or {}).get("sha256")
    return not sha or local_sha(file) in (None, sha)


def package_info(repo):
    """The offline Work input package manifest, or None in a Git checkout."""
    if (Path(repo) / ".git").exists():
        return None
    return jload(Path(repo) / PACKAGE_REL)


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
    if (w, h) != (ew, eh):
        fails.append(f"native dimensions {w}x{h} do not exactly match queue {ew}x{eh}: reviewer exception needed after attempt budget")
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


def preview(path, item, outdir, attempt=1, rnd=1):
    with Image.open(path) as src:
        im = _flat_rgb(src)
    width = max(200, int(item["print_w_in"] * 150))
    im = im.resize((width, max(1, round(width * im.height / im.width))), Image.LANCZOS)
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / f"{item['id']}_r{rnd}_attempt{attempt}_print_size.png"
    im.save(out)
    return out


def helper():
    """A runnable command prefix for messages. Always the repo's own copy when there is one, so an installed copy
    never sends the operator to itself."""
    target = (_REPO / HELPER_IN_REPO) if _REPO and (_REPO / HELPER_IN_REPO).is_file() else Path(__file__)
    try:
        rel = os.path.relpath(target)
    except ValueError:
        rel = str(target)
    return f"python {rel}"


def copy_notice(repo):
    """One line when this running file is not the repo's copy of the helper."""
    mine, theirs = Path(__file__).resolve(), (repo / HELPER_IN_REPO).resolve()
    if not theirs.is_file() or mine == theirs:
        return None
    if mine.read_bytes() == theirs.read_bytes():
        return "helper: this is a copy of the repo's helper (identical); prefer the repo's own copy"
    return f"WARNING: this helper differs from the repo's copy. Stop and run the repo's copy instead: {helper()} <command>"


def scratch_dir(repo):
    """Per-repository scratch folder in the system temp directory (previews, sheets, bundles, attempt counts).
    HERALDRY_SCRATCH overrides the base folder; the owner sets it for tests and isolated sessions."""
    base = Path(os.environ.get("HERALDRY_SCRATCH") or tempfile.gettempdir()) / "heraldry_art"
    return base / hashlib.sha1(str(Path(repo).resolve()).encode()).hexdigest()[:8]


def _attempt_entry(data, iid):
    e = data.get(iid)
    if isinstance(e, list):                       # tolerate an older file format
        e = {"images": e, "closed": False}
    e = dict(e or {"images": [], "closed": False})
    e.setdefault("round", 1)
    return e


def attempts_of(repo, iid):
    """Distinct images checked in the item's current round."""
    return _attempt_entry(jload(scratch_dir(repo) / "attempts.json", {}), iid)["images"]


def attempts_used(repo, iid, state):
    e = _attempt_entry(jload(scratch_dir(repo) / "attempts.json", {}), iid)
    return 0 if e["closed"] and state in ROUND_ENDS else len(e["images"])


def record_attempt(repo, iid, digest, state):
    """Count one distinct generated image for this item and return (count, round number) for the current round.
    A round ends when a saved image has been delivered, sent back or refused. Until then, for example in a
    drift-review redo before the push, the count carries on, so the budget really covers every generation."""
    f = scratch_dir(repo) / "attempts.json"
    data = jload(f, {})
    e = _attempt_entry(data, iid)
    if e["closed"] and state in ROUND_ENDS:
        e = {"images": [], "closed": False, "round": e["round"] + 1}
    e["closed"] = False
    if digest not in e["images"]:
        e["images"].append(digest)
    data[iid] = e
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(data))
    return len(e["images"]), e["round"]


def close_attempts(repo, iid):
    f = scratch_dir(repo) / "attempts.json"
    data = jload(f, {})
    e = _attempt_entry(data, iid)
    e["closed"] = True
    data[iid] = e
    f.write_text(json.dumps(data))


def _pool(repo, item):
    """Other delivered images and the item's own references: what a new generation must not be a copy of."""
    inc = repo / INCOMING_REL
    pool = [f for f in inc.glob("*") if f.is_file() and f.stem != item["id"]] if inc.is_dir() else []
    return pool + [repo / r for r in item["references"]]


def _is_pointer(f):
    with f.open("rb") as fh:
        return fh.read(len(LFS_MAGIC)) == LFS_MAGIC


def duplicate_of(repo, item, image, digest):
    """Path of another delivered image or one of the item's references with exactly these bytes, if any."""
    size = Path(image).stat().st_size
    for f in _pool(repo, item):
        try:
            if f.stat().st_size == size and file_sha(f) == digest:
                return f.relative_to(repo).as_posix()
        except OSError:
            continue
    return None


def _dhash(path, n=16):
    """Difference hash: stable under re-encoding and resizing, different for different pictures."""
    try:
        with Image.open(path) as src:
            g = ImageOps.grayscale(_flat_rgb(src)).resize((n + 1, n), Image.LANCZOS)
    except Exception:
        return None
    px = g.tobytes()
    bits = 0
    for y in range(n):
        for x in range(n):
            bits = (bits << 1) | (1 if px[y * (n + 1) + x] > px[y * (n + 1) + x + 1] else 0)
    return bits


def look_alike(repo, item, image):
    """(difference, path) of the closest other image if it is almost the same picture, else None."""
    mine = _dhash(image)
    if mine is None:
        return None
    best = None
    for f in _pool(repo, item):
        try:
            if _is_pointer(f):
                continue
        except OSError:
            continue
        other = _dhash(f)
        if other is None:
            continue
        d = bin(mine ^ other).count("1")
        if d <= LOOKALIKE_MAX and (best is None or d < best[0]):
            best = (d, f.relative_to(repo).as_posix())
    return best


# ------------------------------------------------------------------ commands
def cmd_doctor(a, repo):
    q = load_queue(repo)
    blockers, delivery, notes = [], [], []
    if sys.version_info < (3, 9):
        blockers.append("Python 3.9 or newer is required")
    pkg = package_info(repo)
    if pkg:
        src = pkg.get("source", {})
        notes.append(f"offline Work input package from {src.get('repository')} commit {src.get('commit')}: git is not used and nothing is pushed "
                     "from here. Verify it with work_preflight.py --offline-package; deliver with `bundle`")
        delivery.append("this is an offline Work input package (no Git checkout, no remote credentials)")
    elif not git_ok(repo):
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
    fixable = []
    bad_prompts = 0
    pointers = []
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
            elif f.read_bytes()[:len(LFS_MAGIC)] == LFS_MAGIC and r not in pointers:
                pointers.append(r)
    if pointers:
        fixable.append(f"{len(pointers)} reference image(s) are LFS pointers, not images. Fetch only these, then run doctor again: "
                       f"git lfs pull --include=\"{','.join(pointers)}\"")
    if bad_prompts:
        blockers.append(f"{bad_prompts} prompt files are missing or no longer match the queue hashes: git pull --rebase origin main")
    blockers = list(dict.fromkeys(blockers))
    print(f"queue phase={q['phase']} items={q['count']} schema={q.get('schema')}")
    scratch_dir(repo).mkdir(parents=True, exist_ok=True)
    print(f"scratch folder (previews, sheets, attempt counts; keep every attempt's image here until the item is saved): {scratch_dir(repo)}")
    note = copy_notice(repo)
    if note:
        print(note)
    for n in notes:
        print("note:", n)
    if blockers:
        print("NOT READY:")
        for b in blockers + fixable + delivery:
            print(" -", b)
        return 1
    if fixable:
        print("NOT READY YET (one step):")
        for b in fixable:
            print(" -", b)
        return 1
    if delivery:
        print("READY TO GENERATE. Delivery by git is blocked: " + "; ".join(delivery)
              + f". Keep generating and saving, then finish each batch with `{helper()} bundle` and hand the zip to the owner.")
        return 0
    print("READY")
    return 0


def cmd_status(a, repo):
    q = load_queue(repo)
    st = states(repo, q)
    count = lambda s: sum(1 for v in st.values() if v == s)  # noqa: E731
    refused = [i for i, v in st.items() if v == "refused"]
    saved = [it["id"] for it in q["items"] if st[it["id"]] == "saved"]
    print(f"phase={q['phase']} items={q['count']} generated_at={q['generated_at']}")
    print(f"pending={count('pending')} redo={count('redo')} saved-not-pushed={len(saved)} pushed={count('pushed')} refused={len(refused)}")
    if refused:
        print("refused by the image tool (Claude Code owns the prompt): " + ", ".join(refused))
    sels = jload(repo / SELECTIONS_REL, {})
    for i, v in st.items():
        if v == "redo":
            print(f"redo {i}: " + (sels.get(i, {}).get("rejected_reason") or "no reason recorded; ask the owner if it is not obvious"))
    note = copy_notice(repo)
    if note and note.startswith("WARNING"):
        print(note)
    todo = [i for i, v in st.items() if v in ("redo", "pending")]
    unsent = bool(saved) or receipts_unpushed(repo)
    due = len(saved) >= BATCH_PUSH_AT or (unsent and (not todo or a.end))
    # what a push would sweep up: files that are not queue items, and images saved without a matching receipt
    have_git, changed, ahead = incoming_changes(repo)
    queue_ids = {it["id"] for it in q["items"]}
    stray = sorted(p for p in (changed | ahead) if Path(p).stem not in queue_ids)
    receipts = last_receipts(repo)
    byid = {it["id"]: it for it in q["items"]}
    no_receipt = [i for i in saved if not (receipts.get(i) and not receipts[i].get("refused")
                                           and receipts[i].get("prompt_sha256") == byid[i]["prompt_sha256"])]
    for p in stray:
        print("WARNING: not a queue item, but changed under assets/art/incoming:", p)
    for i in no_receipt:
        print(f"WARNING: {i} has an image but no matching receipt, so it was not saved with `save`")
    if stray:
        action = ("STOP. The files above are not queue items. Remove them (git restore --staged --worktree, or delete) unless the owner "
                  "put them there, then run status again.")
    elif no_receipt:
        action = (f"STOP. {', '.join(no_receipt)} have no receipt from `save` (placed by hand?). Delete the file, or run `save` on the image "
                  "you generated.")
    elif due and not git_ok(repo) and saved and all_bundled(repo, saved) and not todo:
        b = jload(scratch_dir(repo) / "bundled.json", {})
        action = (f"STOP. Every saved image is in the review bundle {b.get('bundle')} (sha256 {b.get('bundle_sha256')}). Hand that zip over as a "
                  "downloadable file and say plainly that nothing was pushed to GitHub. "
                  + ("The anchors are done: wait for Claude Code's independent review and a new queue. Do not start the batch."
                     if q["phase"] == "anchors" else "Wait for the review and a new queue."))
    elif due and not git_ok(repo):
        action = (f"DRIFT REVIEW, THEN BUNDLE: `{helper()} sheet --refs`, then the style audit, then `{helper()} bundle --evidence SHEET "
                  "--evidence STYLE_JSON [--evidence SMOKE_JSON]` and hand the zip to the owner: git is not available here.")
    elif due:
        action = ("DRIFT REVIEW, THEN GUARDED DELIVERY. First `" + helper() + " sheet --refs`; "
                  "then `python production/art/skill/heraldry-classic-ink-art/scripts/delivery_guard.py audit --repo .` "
                  "and, only if it passes, `python production/art/skill/heraldry-classic-ink-art/scripts/delivery_guard.py ship --execute --repo .`. "
                  "On any LFS/auth/conflict failure STOP and use `" + helper() + " bundle`. Never force-push or auto-rebase receipts.")
    elif todo:
        note = (f" ({len(saved)} saved and not sent yet: send at {BATCH_PUSH_AT}, or run `status --end` at session end)" if unsent else "")
        action = f"GENERATE next: {', '.join(todo[:3])}{' ...' if len(todo) > 3 else ''}  (`{helper()} next`){note}"
    elif q["phase"] == "anchors":
        action = ("STOP. The anchors are done"
                  + (f" ({len(refused)} refused: {', '.join(refused)}; Claude Code decides what a refused anchor means for the batch)" if refused else "")
                  + ". Tell the owner: ask Claude Code to review the anchors and publish the batch queue. Do not start the batch.")
    else:
        action = ("NOTHING LEFT to generate in this queue"
                  + (f" ({len(refused)} refused: {', '.join(refused)}; tell Claude Code)" if refused else "")
                  + ". git pull origin main and run status again; a new queue means new work.")
    if a.end and not due and not stray and not no_receipt:
        action = "SESSION END: nothing is unsent. Write your report. Next session: " + action
    print("NEXT ACTION:", action)
    return 0


def all_bundled(repo, ids):
    """True when the last bundle holds exactly the current bytes of every one of these saved images."""
    done = jload(scratch_dir(repo) / "bundled.json", {}).get("images", {})
    for i in ids:
        files = local_files(repo, i)
        if not files or done.get(i) != file_sha(files[0]):
            return False
    return True


def cmd_next(a, repo):
    q = load_queue(repo)
    st = states(repo, q)
    todo = [it for it in q["items"] if st[it["id"]] == "redo"] + [it for it in q["items"] if st[it["id"]] == "pending"]
    for it in todo[:a.n]:
        refs = ", ".join(Path(r).name for r in it["references"])
        print(f"{it['id']}  [{st[it['id']]}] {it['title']} | {it['size']} | {it['register']} | tries<={it['max_attempts']} | refs: {refs}")
        if st[it["id"]] == "redo":
            print("    redo reason: " + (jload(repo / SELECTIONS_REL, {}).get(it["id"], {}).get("rejected_reason") or "none recorded"))
    if not todo:
        print("nothing pending")
    return 0


def cmd_show(a, repo):
    q = load_queue(repo)
    it = item_of(q, a.id)
    text = prompt_text(repo, it)
    if prompt_sha(text) != it["prompt_sha256"]:
        raise Fatal(f"{it['prompt']} does not match the queue hash: git pull --rebase origin main, then retry")
    state = states(repo, q)[it["id"]]
    used = attempts_used(repo, it["id"], state)
    print(f"ID: {it['id']}\nTITLE: {it['title']}\nFAMILY/REGISTER: {it['family']}/{it['register']}")
    w, h = (int(x) for x in it["size"].split("x"))
    shape = "wide 3:2" if w > h else "tall 2:3" if h > w else "square 1:1"
    print(f"IMAGE SIZE: {it['size']} pixels ({shape})   PRINTED WIDTH: {it['print_w_in']} in   ATTEMPTS: at most {it['max_attempts']} (used so far: {used})")
    print("STATE:", STATE_WORDS[state])
    if state == "redo":
        why = jload(repo / SELECTIONS_REL, {}).get(it["id"], {}).get("rejected_reason")
        print("REDO: the reviewer sent this image back. Reason: " + (why or "none recorded") + "\n      A fresh attempt budget applies; "
              "base your correction sentence on the reason.")
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
    digest = file_sha(image)
    n, rnd = record_attempt(repo, it["id"], digest, states(repo, q)[it["id"]])
    if n > it["max_attempts"]:
        fails.append(f"attempt budget used up ({n} images checked, budget {it['max_attempts']}): do not generate again; "
                     "save the best earlier attempt with --accept-flags")
    dup = duplicate_of(repo, it, image, digest)
    if dup:
        fails.append(f"byte-identical to {dup}: not a new generation of this item")
    else:
        sim = look_alike(repo, it, image)
        if sim:
            warns.append(f"looks almost identical to {sim[1]} (difference {sim[0]} of 256): the same picture re-encoded or resized? Look before saving")
    if last_receipts(repo).get(it["id"], {}).get("refused"):
        infos.append("this ID is recorded as refused; a successful save replaces the refusal")
    return it, m, fails, warns, infos, preview(image, it, scratch_dir(repo), n, rnd), n, dup


def cmd_check(a, repo):
    q = load_queue(repo)
    it, m, fails, warns, infos, pv, n, dup = run_check(repo, q, a.id, a.image)
    verdict = "FAIL" if fails else "WARN" if warns else "PASS"
    if a.json:
        print(json.dumps({"id": it["id"], "result": verdict, "attempt": n, "max_attempts": it["max_attempts"], "fails": fails, "warns": warns,
                          "infos": infos, "must": it["must"], "avoid": it["avoid"],
                          "metrics": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in m.items()},
                          "print_size_preview": str(pv)}, indent=1))
    else:
        print(f"{it['id']}: {m['px'][0]}x{m['px'][1]} {m['format']} (queue size {it['size']})   attempt {n} of {it['max_attempts']}")
        for f in fails:
            print("FAIL", f)
        for w in warns:
            print("WARN", w)
        for i in infos:
            print("info", i)
        print(f"RESULT: {verdict}   print-size preview ({it['print_w_in']} in wide): {pv}")
        print("The tripwires cannot see what follows. LOOK at the image and the preview:")
        for x in it["must"]:
            print("  MUST BE SHOWN (count or find it):", x)
        for x in it["avoid"]:
            print("  DO NOT DRAW (confirm it is absent):", x)
        print("  and the other hard fails: lettering, colour or grey wash, frame or crop, reference bleed, anatomy, scale, legibility "
              "(references/QA_CHECKLIST.md)")
    return 1 if fails else 0


def append_receipt(repo, rec):
    f = repo / RECEIPTS_REL
    f.parent.mkdir(parents=True, exist_ok=True)
    prefix = "\n" if f.exists() and f.stat().st_size and not f.read_bytes().endswith(b"\n") else ""
    with f.open("a", encoding="utf-8") as fh:
        fh.write(prefix + json.dumps(rec, ensure_ascii=False) + "\n")


def cmd_save(a, repo):
    # v6: a standalone visual QA report binds the prompt, native image and attached references.
    # The report lives OUTSIDE the checkout; only its summary is appended to the receipt.
    from fidelity_gate import verify_record, CRITERIA
    if not a.qa_file:
        raise Fatal("v6 requires --qa-file PATH. Create it with scripts/fidelity_gate.py, inspect the original + print-size preview, and complete the checks.")
    qa_path = Path(a.qa_file).resolve()
    if not qa_path.is_file() or repo.resolve() in qa_path.parents:
        raise Fatal("--qa-file must be an existing JSON report OUTSIDE the repository clone")
    try:
        qa = json.loads(qa_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise Fatal(f"cannot read QA report: {e}")
    q = load_queue(repo)
    it, m, fails, warns, infos, pv, n, dup = run_check(repo, q, a.id, a.image)
    errors = verify_record(qa, a.image, it, require_pass=not a.accept_flags)
    if errors:
        raise Fatal("visual QA record failed: " + "; ".join(errors))
    text = prompt_text(repo, it)
    if prompt_sha(text) != it["prompt_sha256"]:
        raise Fatal(f"{it['prompt']} does not match the queue hash: git pull --rebase origin main, then regenerate from the current prompt")
    if dup:
        raise Fatal(f"this image is a byte copy of {dup}: never save a copy. If every attempt is a copy, record "
                    f"`{helper()} refuse {it['id']} --reason \"the tool keeps returning a copy of {dup}\"` and move on")
    state = states(repo, q)[it["id"]]
    if state == "pushed" and not a.redo:
        raise Fatal(f"{it['id']} is already delivered and was not rejected: pass --redo only if the owner or Claude Code asked for a redo")
    if fails and not a.accept_flags:
        for f in fails:
            print("FAIL", f)
        raise Fatal("mechanical failures: regenerate (the budget is "
                    f"{it['max_attempts']} attempts), or pass --accept-flags with --notes if this is the best attempt after the last allowed one")
    if a.accept_flags:
        if n < it["max_attempts"]:
            raise Fatal(f"--accept-flags is only for the last allowed attempt: you have checked {n} of {it['max_attempts']} images. "
                        "Regenerate (references/REPAIR.md). If the tool will not let you, stop and report instead")
        if not a.notes:
            raise Fatal("--accept-flags needs --notes saying what is still wrong")
    else:
        missing = []
        if it["must"]:
            if len(a.must) != len(it["must"]):
                missing.append(f"exactly one --must \"<what you counted or found>\" per MUST line ({len(it['must'])}): " + "; ".join(it["must"]))
            elif any(len(s.strip()) < 10 for s in a.must):
                missing.append("each --must needs a real statement of 10 or more characters, such as \"counted 8 legs, 4 a side\"")
            else:
                for s in a.must:
                    if ADMISSION.search(s):
                        raise Fatal(f"the statement \"{s}\" says the item is missing, not drawn, wrong or could not be checked. That is a hard fail, "
                                    "not a pass: retry (references/REPAIR.md). Only at the last allowed attempt may you save it, with --accept-flags "
                                    "and --notes. If you meant the opposite, say it positively, for example \"all 8 legs present, 4 a side\"")
        elif a.must:
            raise Fatal("this item has no MUST lines: omit --must")
        if it["avoid"] and not a.avoid_clear:
            missing.append("--avoid-clear, meaning you looked and none of the DO NOT DRAW items is present")
        if missing:
            raise Fatal("look at the image, then state your checks. Missing: " + " | ".join(missing))
    attempts = max(a.attempts or 0, n)
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
           "date_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "variants_tried": attempts,
           "notes": a.notes or ""}
    if a.must:
        rec["must_checked"] = a.must
    if a.avoid_clear:
        rec["avoid_clear"] = True
    if a.redo or state == "redo":
        rec["redo"] = True
    if a.accept_flags:
        rec["accepted_flags"] = True
        rec["accepted_at_attempt"] = n
    rec["qa_schema"] = 1
    # The external scratch report may not survive a Work session. Keep the full
    # visual evidence with the in-repo receipt so Claude Code can audit it later.
    rec["qa_review"] = qa["checks"]
    rec["qa_register"] = qa.get("register_compared", "")
    rec["qa_print_size_reviewed"] = qa.get("visual_review_at_print_size", False)
    rec["qa_unresolved"] = qa.get("unresolved_issues", [])
    rec["qa_report_sha256"] = hashlib.sha256(qa_path.read_bytes()).hexdigest()
    rec["qa_failed_criteria"] = [name for name in CRITERIA if not qa["checks"][name]["pass"]]
    rec["reference_shas"] = [r["sha256"] for r in qa.get("references_used", [])]
    rec["native_sha256"] = hashlib.sha256(data).hexdigest()
    if fails or warns:
        rec["tripwires"] = fails + warns
    append_receipt(repo, rec)
    close_attempts(repo, it["id"])
    # Keep the exact QA report beside the attempt counts: `bundle` ships it as review evidence.
    qa_copy = scratch_dir(repo) / "qa" / f"{it['id']}.qa.json"
    qa_copy.parent.mkdir(parents=True, exist_ok=True)
    qa_copy.write_bytes(qa_path.read_bytes())
    print(f"saved {dest.relative_to(repo)} ({len(data)} bytes, unmodified) after {attempts} attempt(s); receipt written")
    if fails:
        print("saved with FAIL tripwires recorded in the receipt: the reviewer will see them")
    print(f"next: run `{helper()} status` for the next action")
    return 0


def cmd_refuse(a, repo):
    q = load_queue(repo)
    it = item_of(q, a.id)
    reason = (a.reason or "").strip()
    if len(reason) < 10:
        raise Fatal("--reason needs a real sentence of 10 or more characters: what the tool said, or what happened if it said nothing")
    if states(repo, q)[it["id"]] == "pushed":
        raise Fatal(f"{it['id']} is already delivered and is not a redo, so there is nothing to refuse. "
                    "If a redo was refused it shows as redo in status; otherwise leave it alone")
    append_receipt(repo, {"id": it["id"], "refused": True, "reason": reason, "surface": "ChatGPT Work",
                          "date_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d")})
    print(f"recorded the refusal of {it['id']} in {RECEIPTS_REL}: commit it with the next batch and name the item in your report")
    return 0


def cmd_sheet(a, repo):
    q = load_queue(repo)
    st = states(repo, q)
    ids = a.ids or [i for i, v in st.items() if v == "saved"]
    if not ids:
        raise Fatal(f"no saved, unpushed images. Name the IDs to put on a sheet: {helper()} sheet ID ID ... [--refs]")
    cell, cols = 360, 4
    items = [item_of(q, i) for i in ids]
    files, labels = [], []
    for it in items:
        fl = local_files(repo, it["id"])
        if not fl:
            raise Fatal(f"{it['id']}: no saved image")
        files.append(fl[0])
        labels.append(it["id"])
    if a.refs:
        seen = []
        for it in items:
            for r in it["references"]:
                if r not in seen:
                    seen.append(r)
        for r in seen[:6]:
            files.append(repo / r)
            labels.append("REF " + Path(r).name[:24])
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, rows * (cell + 22)), "white")
    d = ImageDraw.Draw(sheet)
    for n, (f, label) in enumerate(zip(files, labels)):
        with Image.open(f) as src:
            im = _flat_rgb(src)
        im.thumbnail((cell - 8, cell - 8))
        x, y = (n % cols) * cell, (n // cols) * (cell + 22)
        sheet.paste(im, (x + (cell - im.width) // 2, y + 22))
        d.text((x + 6, y + 5), label, fill=(0, 0, 0))
    out = Path(a.out) if a.out else scratch_dir(repo) / "batch_sheet.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=85)
    print(f"contact sheet: {out}  ({len(ids)} images{', plus the references of every item on it' if a.refs else ''})")
    return 0


def cmd_bundle(a, repo):
    from delivery_guard import Error as GuardError, check_receipt
    q = load_queue(repo)
    st = states(repo, q)
    ids = [i for i, v in st.items() if v == "saved"]
    refused = [i for i, v in st.items() if v == "refused"]
    if not ids and not refused:
        raise Fatal("nothing unsent to bundle: every saved image has already been pushed, and nothing was refused")
    name = f"batch_{ids[0]}__{ids[-1]}.zip" if ids else "batch_refusals.zip"
    out = Path(a.out) if a.out else scratch_dir(repo) / name
    if repo.resolve() in out.resolve().parents:
        raise Fatal("write the bundle outside the repository clone (the skill changes no other repo file); omit --out for the scratch folder")
    receipts = last_receipts(repo)
    byid = {it["id"]: it for it in q["items"]}
    files, items = {}, []
    for i in ids:
        f = local_files(repo, i)[0]
        rec = receipts.get(i)
        try:                                   # the same byte, prompt, reference and QA gate as a guarded push
            check_receipt(byid[i], f, rec)
        except GuardError as e:
            raise Fatal(f"not bundled: {e}")
        qa = scratch_dir(repo) / "qa" / f"{i}.qa.json"
        if not qa.is_file() or file_sha(qa) != rec.get("qa_report_sha256"):
            raise Fatal(f"not bundled: the QA report saved with {i} is missing from {qa.parent} or changed since `save`. "
                        "Re-create it for the same image and save again")
        rel = f.relative_to(repo).as_posix()
        files[rel] = f.read_bytes()
        files[f"review_evidence/qa/{i}.qa.json"] = qa.read_bytes()
        with Image.open(f) as im:
            px = [im.width, im.height]
        items.append({"id": i, "file": rel, "sha256": file_sha(f), "bytes": f.stat().st_size, "px": px, "queue_size": byid[i]["size"],
                      "prompt_sha256": rec["prompt_sha256"], "reference_shas": rec["reference_shas"],
                      "receipt_sha256": hashlib.sha256(json.dumps(rec, ensure_ascii=False).encode()).hexdigest(),
                      "qa_report": f"review_evidence/qa/{i}.qa.json", "qa_report_sha256": rec["qa_report_sha256"],
                      "qa_failed_criteria": rec.get("qa_failed_criteria", []), "accepted_flags": bool(rec.get("accepted_flags")),
                      "variants_tried": rec.get("variants_tried")})
    for e in a.evidence:
        ef = Path(e)
        if not ef.is_file():
            raise Fatal(f"--evidence {e}: no such file")
        files[f"review_evidence/{ef.name}"] = ef.read_bytes()
    lines = [json.dumps(receipts[i], ensure_ascii=False) for i in ids + refused if i in receipts]
    files["receipts_append.jsonl"] = ("\n".join(lines) + "\n").encode()
    pkg = package_info(repo)
    if pkg:
        source = {"kind": "offline_package", **{k: pkg.get("source", {}).get(k) for k in ("repository", "branch", "commit")},
                  "package_manifest_sha256": file_sha(repo / PACKAGE_REL)}
    else:
        code, head = git(repo, "rev-parse", "HEAD")
        source = {"kind": "git_checkout" if git_ok(repo) else "folder", "commit": head.strip() if code == 0 else None}
    span = ids[0] + " .. " + ids[-1] if ids else "refusals"
    files["HANDOFF.txt"] = ("Heraldry ChatGPT Work review bundle. NOTHING IN IT WAS PUSHED TO GITHUB, AND NOTHING IN IT IS APPROVED.\n"
                            "Claude Code reviews it independently: python3 tools/art_work_package.py verify-bundle THIS.zip\n"
                            "Only after that review: copy assets/art/incoming/<ID>.* into the clone, append receipts_append.jsonl to\n"
                            "production/art/gpt/RECEIPTS.jsonl, keep review_evidence/ outside the repository, then\n"
                            "git lfs install; git add assets/art/incoming production/art/gpt/RECEIPTS.jsonl; git lfs ls-files\n"
                            f"git commit -m 'art(gpt): {span}'; git pull --rebase origin main; git push origin main\n").encode()
    manifest = {"schema": 1, "kind": "heraldry-work-review-bundle", "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "source": source, "queue": {"phase": q["phase"], "sha256": file_sha(repo / QUEUE_REL), "ids": [it["id"] for it in q["items"]]},
                "delivery": "bundle", "pushed_to_github": False, "approval": "NOT APPROVED: independent Claude Code / owner review required",
                "items": items, "refusals": refused,
                "files": {k: {"sha256": hashlib.sha256(v).hexdigest(), "bytes": len(v)} for k, v in sorted(files.items())}}
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for k in sorted(files):
            z.writestr(k, files[k])
        z.writestr("BUNDLE_MANIFEST.json", json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    digest = file_sha(out)
    (scratch_dir(repo) / "bundled.json").write_text(json.dumps({"bundle": str(out), "bundle_sha256": digest,
                                                                 "images": {it["id"]: it["sha256"] for it in items}}))
    print(f"bundle: {out} ({len(ids)} images, {len(refused)} refusals, {len(a.evidence)} extra evidence files)  sha256 {digest}")
    print("Nothing was pushed. Hand this zip over as a downloadable file for independent review; it is not approved artwork.")
    if git_ok(repo):
        print("note: git is available here. Push instead of handing over a bundle, unless a push has failed.")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", help="repository root (default: found above the current directory)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor", help="environment, repo, queue and reference checks")
    p = sub.add_parser("status", help="queue state and the single next action")
    p.add_argument("--end", action="store_true", help="session end: ask for a push of anything unsent, even below the batch size")
    p = sub.add_parser("next", help="the next items to generate (8 unless --n N)")
    p.add_argument("--n", type=int, default=8)
    p = sub.add_parser("show", help="one item: references, size, must and do-not-draw lists, verbatim prompt")
    p.add_argument("id")
    p = sub.add_parser("check", help="mechanical tripwires for one generated image; counts it as an attempt")
    p.add_argument("id")
    p.add_argument("image")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("save", help="check, copy the image unmodified into assets/art/incoming, write the receipt")
    p.add_argument("id")
    p.add_argument("image")
    p.add_argument("--attempts", type=int, default=0,
                   help="total generations made for this item, the saved one included. The helper counts the images you checked; "
                        "this can only raise that count, for images you generated but did not check")
    p.add_argument("--model", default="")
    p.add_argument("--qa-file", help="v6 mandatory visual QA JSON outside the clone")
    p.add_argument("--notes", default="")
    p.add_argument("--must", action="append", default=[],
                   help="what you counted or found, exactly one per MUST BE SHOWN line, in order (repeat the flag)")
    p.add_argument("--avoid-clear", action="store_true", help="you looked and none of the DO NOT DRAW items is present")
    p.add_argument("--accept-flags", action="store_true",
                   help="save the best attempt despite FAIL tripwires or an uncorrected hard fail; only at the last allowed attempt; needs --notes")
    p.add_argument("--redo", action="store_true", help="replace an image that was already delivered (only when the owner asked)")
    p = sub.add_parser("refuse", help="record that the image tool refused an item")
    p.add_argument("id")
    p.add_argument("--reason", required=True)
    p = sub.add_parser("sheet", help="labelled contact sheet of saved images")
    p.add_argument("ids", nargs="*")
    p.add_argument("--out")
    p.add_argument("--refs", action="store_true", help="add the references of every item on the sheet, for style comparison")
    p = sub.add_parser("bundle", help="review hand-off zip (images, receipts, QA reports, manifest) for when git push is impossible")
    p.add_argument("--out", help="default: the scratch folder; must be outside the repository clone")
    p.add_argument("--evidence", action="append", default=[],
                   help="extra review evidence to include under review_evidence/: the contact sheet, style audit JSON, smoke record (repeat)")
    a = ap.parse_args(argv)
    global _REPO
    try:
        repo = find_repo(a.repo)
        _REPO = repo
        return globals()["cmd_" + a.cmd](a, repo)
    except Fatal as e:
        print("ERROR:", e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
