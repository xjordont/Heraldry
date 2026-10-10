#!/usr/bin/env python3
"""Automated pen-and-ink illustration pipeline (owner decision 2026-10-08).

  plan             prompts, counts and cost estimate; no network
  anchors          generate the style-anchor set (existing masters used only as inspiration)
  approve-anchors  orchestrator records its visual approval of the proposed anchors
  batch            generate every catalog entry not yet selected, with the approved anchors
                   attached as style references; an automated judge picks the best candidate
  ink              re-run deterministic ink preparation for every selection
  sheet            contact sheets of selected ink art per family

Reads GEMINI_API_KEY from the environment and never prints it. Stops at the budget cap
in config/art_style.json (estimated from token usage). Resumable: selections are written
after each entry; with --commit-every the run commits progress to the current branch."""
import argparse, base64, hashlib, io, json, os, subprocess, sys, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from art_ink import prep  # noqa: E402

CFG = json.loads((ROOT / "config/art_style.json").read_text())
CATALOG = ROOT / "production/art/SPOT_CATALOG.json"
SELECTIONS = ROOT / "production/art/SELECTIONS.json"
ANCHORS = ROOT / "production/art/ANCHORS.json"
LEDGER = ROOT / "production/art/GENERATION_LEDGER.jsonl"
CAND = ROOT / "build/art/candidates"
MASTERS = ROOT / "assets/art/masters"
INK = ROOT / "assets/art/ink"
API = "https://generativelanguage.googleapis.com/v1beta"


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load(p, default):
    return json.loads(p.read_text()) if p.exists() else default


def save(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def sha(b):
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------------------ prompts
def prompt_for(e, with_refs):
    fam = CFG["families"][e["family"]]
    parts = [CFG["style"]]
    if with_refs:
        parts.append(CFG["reference_instruction"])
    parts.append(f"FORMAT: {fam['framing']} Aspect ratio {fam['aspect']}.")
    if e["family"] in ("cover", "chapter"):
        parts.append(f"SUBJECT: {e['subject']}. COMPOSITION: {e['composition']}.")
    else:
        where = " / ".join(e.get("context", []))
        if e["family"] in ("monster", "boss"):
            f = e.get("facts", {})
            size = CFG["size_words"].get(f.get("size_code") or "", "")
            parts.append(f"SUBJECT: the creature called \"{e['title']}\" ({where}). {('Size: ' + size + '.') if size else ''} "
                         "Depict it faithfully from this description, inventing nothing that contradicts it:")
        else:
            parts.append(f"SUBJECT: \"{e['title']}\" ({where}). Depict this faithfully, inventing nothing that contradicts it:")
        parts.append("\"" + e["flavour"] + "\"")
        if e.get("direction"):
            parts.append("IMAGE: " + e["direction"])
    parts.append(CFG["exclusions"])
    return "\n\n".join(parts)


# ------------------------------------------------------------------ API
_key = None


def key():
    """Bare API key from the secret. Tolerates surrounding whitespace/quotes, a NAME=value line
    or a JSON object holding the key; never prints any part of it."""
    global _key
    if _key:
        return _key
    raw = os.environ.get("GEMINI_API_KEY", "")
    if not raw.strip():
        raise SystemExit("GEMINI_API_KEY is not set (add it as a repository secret)")
    import re
    found = re.findall(r"AIza[0-9A-Za-z_\-]{30,}", raw)
    if found:
        _key = found[0]
    elif '"private_key"' in raw or '"type": "service_account"' in raw:
        raise SystemExit("GEMINI_API_KEY holds a service-account JSON; store a Gemini API key from Google AI Studio instead")
    else:
        _key = raw.strip().split("=", 1)[-1].strip().strip("'\"")
    return _key


def call(method, path, body=None, timeout=300):
    data = None if body is None else json.dumps(body).encode()
    for attempt in range(6):
        req = urllib.request.Request(f"{API}/{path}", data=data, method=method,
                                     headers={"x-goog-api-key": key(), "content-type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as ex:
            msg = ex.read().decode(errors="replace")[:400]
            if ex.code == 429 and ("free_tier" in msg or "PerDay" in msg):
                raise SystemExit("Gemini quota exhausted (free tier or daily limit): enable billing on the key's "
                                 "Google Cloud project, then rerun. " + msg[:300])
            if ex.code in (429, 500, 502, 503, 504) and attempt < 5:
                time.sleep(min(90, 5 * 2 ** attempt))
                continue
            raise RuntimeError(f"HTTP {ex.code}: {msg}") from None
        except (urllib.error.URLError, TimeoutError):
            if attempt < 5:
                time.sleep(min(90, 5 * 2 ** attempt))
                continue
            raise


_models = {}


def resolve(kind):
    if kind in _models:
        return _models[kind]
    names, tok = [], ""
    while True:
        r = call("GET", "models?pageSize=1000" + (f"&pageToken={tok}" if tok else ""))
        names += [m["name"].split("/", 1)[1] for m in r.get("models", []) if "generateContent" in m.get("supportedGenerationMethods", [])]
        tok = r.get("nextPageToken")
        if not tok:
            break
    for pref in CFG[f"{kind}_model_preference"]:
        if pref in names:
            _models[kind] = pref
            return pref
    if kind == "image":
        cands = [n for n in names if "image" in n and "flash" in n]
    else:
        cands = [n for n in names if "flash" in n and "image" not in n and "tts" not in n and "live" not in n]
    if not cands:
        raise SystemExit(f"No {kind} model available; models seen: {names[:40]}")
    _models[kind] = sorted(cands)[-1]
    return _models[kind]


def b64img(path_or_im, max_px=768):
    im = Image.open(path_or_im) if not isinstance(path_or_im, Image.Image) else path_or_im
    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im.convert("RGBA"), mask=im.convert("RGBA").getchannel("A"))
        im = bg
    im = im.convert("RGB")
    im.thumbnail((max_px, max_px))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=88)
    return {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(buf.getvalue()).decode()}}


def ledger(rec):
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(json.dumps(rec) + "\n")


def spent():
    if not LEDGER.exists():
        return 0.0
    return sum(json.loads(l).get("usd_est", 0) for l in LEDGER.read_text().splitlines() if l.strip())


def usd(usage, kind):
    p = CFG["price_per_mtok_usd"]
    i, o = usage.get("promptTokenCount", 0), usage.get("candidatesTokenCount", 0)
    if kind == "image":
        return (i * p["image_in"] + o * p["image_out"]) / 1e6 if o else 0.11
    return (i * p["judge_in"] + (o + usage.get("thoughtsTokenCount", 0)) * p["judge_out"]) / 1e6


def generate_one(e, prompt, refs, out):
    fam = CFG["families"][e["family"]]
    model = resolve("image")
    parts = [b64img(r) for r in refs] + [{"text": prompt}]
    cfg = {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": fam["aspect"], "imageSize": fam["size"]}}
    try:
        r = call("POST", f"models/{model}:generateContent", {"contents": [{"role": "user", "parts": parts}], "generationConfig": cfg})
    except RuntimeError as ex:
        if "imageSize" not in str(ex) and "image_size" not in str(ex):
            raise
        cfg["imageConfig"].pop("imageSize")
        r = call("POST", f"models/{model}:generateContent", {"contents": [{"role": "user", "parts": parts}], "generationConfig": cfg})
    u = r.get("usageMetadata", {})
    cost = usd(u, "image")
    img = None
    for c in r.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            d = p.get("inlineData") or p.get("inline_data")
            if d and d.get("data"):
                img = base64.b64decode(d["data"])
    reason = (r.get("candidates") or [{}])[0].get("finishReason")
    ledger({"t": now(), "kind": "image", "id": e["id"], "model": model, "usage": u, "usd_est": round(cost, 5),
            "ok": img is not None, "finish": reason, "prompt_sha256": sha(prompt.encode())})
    if img is None:
        return None
    out.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(io.BytesIO(img))
    im.save(out)  # PNG container; pixels unchanged
    return out


JUDGE = """You are the art director for a black-and-white pen-and-ink fantasy rulebook. Every illustration must look drawn by the same illustrator as the REFERENCE images.
Score each CANDIDATE from 0 to 10 on:
- style_match: line weight, hatching technique, contrast and finish match the references; pure black ink on white, no grey wash or colour.
- subject_fidelity: depicts the described subject accurately (anatomy, number of limbs/heads, equipment, setting) and contradicts nothing in the text.
- craft: coherent anatomy, hands, weapons, architecture and perspective; readable silhouette at small size.
List defects such as: text or lettering, signature, frame or box border, colour, grey wash, photographic look, extra limbs, malformed hands, cropped subject, busy background.
overall = a 0-10 judgement for print, heavily penalising any text, frame, colour or anatomical error.
Return JSON: {"candidates":[{"index":1,"style_match":0,"subject_fidelity":0,"craft":0,"defects":[],"overall":0}],"best":1}

SUBJECT DESCRIPTION:
"""


def judge(e, prompt_subject, cand_paths, refs):
    model = resolve("judge")
    parts = []
    for i, r in enumerate(refs[:4], 1):
        parts += [{"text": f"REFERENCE {i}:"}, b64img(r, 640)]
    for i, c in enumerate(cand_paths, 1):
        parts += [{"text": f"CANDIDATE {i}:"}, b64img(c, 768)]
    parts.append({"text": JUDGE + prompt_subject})
    r = call("POST", f"models/{model}:generateContent", {"contents": [{"role": "user", "parts": parts}],
                                                          "generationConfig": {"responseMimeType": "application/json", "temperature": 0}})
    u = r.get("usageMetadata", {})
    txt = "".join(p.get("text", "") for c in r.get("candidates", []) for p in c.get("content", {}).get("parts", []))
    ledger({"t": now(), "kind": "judge", "id": e["id"], "model": model, "usage": u, "usd_est": round(usd(u, "judge"), 5)})
    try:
        j = json.loads(txt)
        scores = {int(c["index"]): c for c in j["candidates"]}
        best = max(scores, key=lambda k: (scores[k].get("overall", 0), scores[k].get("style_match", 0)))
        return best, scores, model
    except (ValueError, KeyError, TypeError):
        return 1, {}, model


def subject_text(e):
    if e["family"] in ("cover", "chapter"):
        return f"{e['subject']}. {e['composition']}"
    return f"{e['title']} ({e['family']}): {e['flavour']}"


# ------------------------------------------------------------------ selection
def select(e, prompt, src, best, scores, judge_model, rnd, status):
    sels = load(SELECTIONS, {})
    master = MASTERS / f"{e['id']}.png"
    master.parent.mkdir(parents=True, exist_ok=True)
    data = src.read_bytes()
    master.write_bytes(data)
    ink = INK / f"{e['id']}.png"
    info = prep(master, ink)
    im = Image.open(master)
    sels[e["id"]] = {"family": e["family"], "title": e["title"], "heading_id": e.get("heading_id"), "replaces": e.get("replaces"),
                     "spec_sha256": e["spec_sha256"], "prompt_sha256": sha(prompt.encode()), "prompt": prompt,
                     "model": resolve("image"), "judge_model": judge_model, "round": rnd, "candidate": src.name,
                     "judge": scores.get(best, {}), "status": status, "generated_at": now(),
                     "master": {"path": str(master.relative_to(ROOT)), "sha256": sha(data), "px": list(im.size)},
                     "ink": {"path": info["dst"], "sha256": sha(ink.read_bytes()), "px": info["ink_px"], "flags": info["flags"],
                             "max_print_w_in_300ppi": info["max_print_w_in_300ppi"]},
                     "provenance": "Generated with the Google Gemini API image model named above; automated judge selection; not hand-drawn."}
    save(SELECTIONS, sels)


def run_entry(e, refs, n, rounds, status_ok):
    with_refs = bool(refs)
    prompt = prompt_for(e, with_refs)
    best_any = None
    for rnd in range(1, rounds + 1):
        if spent() >= CFG["budget_usd"]:
            return "budget"
        outs = [CAND / e["id"] / f"r{rnd}c{k}.png" for k in range(1, n + 1)]
        with ThreadPoolExecutor(max_workers=n) as ex:
            got = [p for p in ex.map(lambda o: generate_one(e, prompt, refs, o), outs) if p]
        if not got:
            continue
        best, scores, jm = judge(e, subject_text(e), got, refs) if len(got) > 1 or refs else (1, {}, None)
        best = min(max(best, 1), len(got))
        sc = scores.get(best, {})
        bad_flags = prep(got[best - 1], CAND / e["id"] / "ink-check.png")["flags"]
        ok = sc.get("overall", 0) >= CFG["judge_pass_score"] and not bad_flags
        if best_any is None or sc.get("overall", 0) > best_any[0]:
            best_any = (sc.get("overall", 0), got[best - 1], best, scores, jm, rnd)
        if ok:
            select(e, prompt, got[best - 1], best, scores, jm, rnd, status_ok)
            return "selected"
    if best_any:
        _, path, best, scores, jm, rnd = best_any
        select(e, prompt, path, best, scores, jm, rnd, "low-score-needs-review")
        return "low-score"
    return "failed"


def commit(msg):
    subprocess.run(["git", "add", "assets/art/masters", "assets/art/ink", "production/art"], cwd=ROOT, check=True)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode == 0:
        return
    subprocess.run(["git", "commit", "-qm", msg], cwd=ROOT, check=True)
    for k in range(5):
        subprocess.run(["git", "pull", "--rebase", "-q", "origin", "main"], cwd=ROOT)
        if subprocess.run(["git", "push", "-q", "origin", "HEAD:main"], cwd=ROOT).returncode == 0:
            return
        time.sleep(2 ** (k + 1))
    raise SystemExit("push failed")


def entries():
    return load(CATALOG, {})["entries"]


def pending(sel_status=None):
    sels = load(SELECTIONS, {})
    out = []
    for e in entries():
        s = sels.get(e["id"])
        if s and s["spec_sha256"] == e["spec_sha256"] and s["status"] != "rejected":
            continue
        out.append(e)
    return out


def anchor_refs():
    a = load(ANCHORS, {})
    if a.get("status") != "approved":
        raise SystemExit("Anchors are not approved; run the anchors phase and review it first")
    # approved anchors first (the judge compares against the first four), then the owner's style samples
    return [ROOT / p for p in a["references"]] + [ROOT / p for p in CFG["style_refs"]]


# ------------------------------------------------------------------ commands
def cmd_plan(a):
    pend = pending()
    fams = {}
    for e in pend:
        fams[e["family"]] = fams.get(e["family"], 0) + 1
    p = CFG["price_per_mtok_usd"]
    tok = {"1K": 1120, "2K": 1680}
    est = sum(CFG["candidates_per_entry"] * tok[CFG["families"][e["family"]]["size"]] * p["image_out"] / 1e6 + 0.004 for e in pend)
    print(json.dumps({"pending": len(pend), "by_family": fams, "spent_usd_est": round(spent(), 2), "budget_usd": CFG["budget_usd"],
                      "first_round_usd_est": round(est, 2), "worst_case_usd_est": round(est * CFG["max_rounds"], 2)}, indent=1))
    if a.ids:
        for e in entries():
            if e["id"] in a.ids:
                print("\n--- " + e["id"] + "\n" + prompt_for(e, True))


def cmd_anchors(a):
    # owner-supplied style samples define the hand; the old ChatGPT masters are no longer references
    insp = [ROOT / p for p in CFG["style_refs"]]
    ids = CFG["anchor_ids"]
    for e in entries():
        if e["id"] in ids:
            print(e["id"], run_entry(e, insp, CFG["anchor_candidates"], 1, "anchor-proposed"), flush=True)
    sels = load(SELECTIONS, {})
    save(ANCHORS, {"status": "proposed", "proposed_at": now(), "anchor_ids": ids,
                   "references": [sels[i]["master"]["path"] for i in ids if i in sels],
                   "inspiration": [str(p.relative_to(ROOT)) for p in insp]})
    sheet(ids, ROOT / "build/art/sheets/anchors.png")
    if a.commit_every:
        commit("art: proposed style anchors")


def cmd_approve(a):
    an = load(ANCHORS, {})
    keep = a.ids or an["anchor_ids"]
    sels = load(SELECTIONS, {})
    an.update(status="approved", approved_at=now(), approved_by=a.by, anchor_ids=keep,
              references=[sels[i]["master"]["path"] for i in keep])
    for i in keep:
        sels[i]["status"] = "anchor-approved"
    for i in set(an.get("anchor_ids", [])) - set(keep):
        sels.pop(i, None)
    save(SELECTIONS, sels)
    save(ANCHORS, an)


def cmd_batch(a):
    refs = anchor_refs()
    t0 = time.time()
    todo = [e for e in pending() if (not a.family or e["family"] in a.family) and (not a.ids or e["id"] in a.ids)]
    done = 0
    for e in todo[:a.limit or None]:
        if a.max_minutes and time.time() - t0 > a.max_minutes * 60:
            print("time limit reached", flush=True)
            break
        r = run_entry(e, refs, CFG["candidates_per_entry"], CFG["max_rounds"], "auto-selected")
        print(e["id"], r, f"spent≈${spent():.2f}", flush=True)
        if r == "budget":
            print("budget cap reached", flush=True)
            break
        done += 1
        if a.commit_every and done % a.commit_every == 0:
            commit(f"art: generated {done} illustrations (batch in progress)")
    if a.commit_every:
        commit(f"art: generated {done} illustrations")


def cmd_ink(a):
    sels = load(SELECTIONS, {})
    for i, s in sels.items():
        info = prep(ROOT / s["master"]["path"], INK / f"{i}.png")
        s["ink"].update(sha256=sha((INK / f"{i}.png").read_bytes()), px=info["ink_px"], flags=info["flags"],
                        max_print_w_in_300ppi=info["max_print_w_in_300ppi"])
    save(SELECTIONS, sels)


def sheet(ids, out, cell=360, cols=6):
    sels = load(SELECTIONS, {})
    ids = [i for i in ids if i in sels]
    if not ids:
        return
    rows = (len(ids) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * cell, rows * cell), (252, 250, 245))
    for k, i in enumerate(ids):
        im = Image.open(ROOT / sels[i]["ink"]["path"])
        im.thumbnail((cell - 16, cell - 16))
        x, y = (k % cols) * cell + (cell - im.width) // 2, (k // cols) * cell + (cell - im.height) // 2
        canvas.paste((0, 0, 0), (x, y, x + im.width, y + im.height), mask=im.getchannel("A"))
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)


def cmd_sheet(a):
    sels = load(SELECTIONS, {})
    fams = sorted({s["family"] for s in sels.values()})
    for f in fams:
        ids = [i for i, s in sels.items() if s["family"] == f]
        for k in range(0, len(ids), 36):
            sheet(ids[k:k + 36], ROOT / f"build/art/sheets/{f}-{k // 36 + 1}.png")
    print("\n".join(str(p.relative_to(ROOT)) for p in sorted((ROOT / "build/art/sheets").glob("*.png"))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["plan", "anchors", "approve-anchors", "batch", "ink", "sheet"])
    ap.add_argument("--ids", nargs="*")
    ap.add_argument("--family", nargs="*")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-minutes", type=float, default=0)
    ap.add_argument("--commit-every", type=int, default=0)
    ap.add_argument("--by", default="orchestrator visual review")
    a = ap.parse_args()
    {"plan": cmd_plan, "anchors": cmd_anchors, "approve-anchors": cmd_approve, "batch": cmd_batch,
     "ink": cmd_ink, "sheet": cmd_sheet}[a.cmd](a)


if __name__ == "__main__":
    main()
