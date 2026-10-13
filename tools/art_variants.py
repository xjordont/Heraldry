#!/usr/bin/env python3
"""Generate extra candidate versions of catalogued illustrations with the Gemini image API (Nano Banana 2.1).

Owner instruction 2026-10-13: "rebuild all 20 background art pieces through nano banana 2.1 then we will
compare all versions made of each background illustration side by side and select the best".

This is a comparison route, not a production route: it uses the entry's current prompt and the same
reference set the Codex queue uses, writes raw native PNGs to assets/art/variants/<ID>/nb-<n>.png, and
NEVER touches production/art/SELECTIONS.json, assets/art/incoming or any approval. A chosen version is
placed afterwards through a separate, reviewed step. Spend shares the cap in config/art_style.json and
the ledger production/art/GENERATION_LEDGER.jsonl (kind "variant"). The key is read from the environment
by art_generate.py and is never printed.

    python3 tools/art_variants.py prompts --family background        # print the assembled prompts (no API call)
    python3 tools/art_variants.py refs --family background           # comma-separated reference paths to fetch (LFS)
    python3 tools/art_variants.py run --family background --n 3      # generate (needs GEMINI_API_KEY)
"""
import argparse
import base64
import io
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
OUT = ROOT / "assets/art/variants"
SIZE = "2K"          # largest the model offers; 1K would fall below the 1,572,864-pixel target


def targets(g, a):
    ents = {e["id"]: e for e in g.entries()}
    ids = a.ids or [i for i, e in ents.items() if not a.family or e["family"] == a.family]
    bad = [i for i in ids if i not in ents]
    if bad:
        raise SystemExit(f"unknown IDs: {bad}")
    return [ents[i] for i in sorted(ids)]


def one(g, pack, e, n, model):
    from PIL import Image
    fam = g.CFG["families"][e["family"]]
    prompt = g.prompt_for(e, True)
    refs = [ROOT / r for r in pack.references_for(e, {}, guided=False)]
    parts = [g.b64img(r) for r in refs] + [{"text": prompt}]
    cfg = {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": fam["aspect"], "imageSize": SIZE}}
    body = {"contents": [{"role": "user", "parts": parts}], "generationConfig": cfg}
    try:
        r = g.call("POST", f"models/{model}:generateContent", body)
    except RuntimeError as ex:
        if "imageSize" not in str(ex) and "image_size" not in str(ex):
            raise
        cfg["imageConfig"].pop("imageSize")
        r = g.call("POST", f"models/{model}:generateContent", body)
    u = r.get("usageMetadata", {})
    img = None
    for c in r.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            d = p.get("inlineData") or p.get("inline_data")
            if d and d.get("data"):
                img = base64.b64decode(d["data"])
    g.ledger({"t": g.now(), "kind": "variant", "id": e["id"], "variant": n, "model": model, "usage": u,
              "usd_est": round(g.usd(u, "image"), 5), "ok": img is not None, "size": SIZE,
              "prompt_sha256": g.sha(prompt.encode()), "refs": len(refs)})
    if img is None:
        print(f"{e['id']} nb-{n}: no image ({(r.get('candidates') or [{}])[0].get('finishReason')})")
        return None
    dest = OUT / e["id"] / f"nb-{n}.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    Image.open(io.BytesIO(img)).save(dest)
    print(f"{e['id']} nb-{n}: saved")
    return dest


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cmd", choices=("prompts", "refs", "run"))
    ap.add_argument("--family", default="")
    ap.add_argument("--ids", nargs="*", default=[])
    ap.add_argument("--n", type=int, default=3, help="versions per illustration")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    import art_generate as g
    import art_gpt_pack as pack
    ents = targets(g, a)
    if a.cmd == "prompts":
        for e in ents:
            print(f"=== {e['id']}\n{g.prompt_for(e, True)}\n")
        return
    if a.cmd == "refs":
        print(",".join(sorted({r for e in ents for r in pack.references_for(e, {}, guided=False)})))
        return
    model = g.resolve("image")
    print(f"image model: {model}; budget used so far ${g.spent():.2f} of ${g.CFG['budget_usd']:.2f}")
    jobs = [(e, n) for e in ents for n in range(1, a.n + 1) if not (OUT / e["id"] / f"nb-{n}.png").exists()]
    est = len(jobs) * 0.25
    if g.spent() + est > g.CFG["budget_usd"]:
        raise SystemExit(f"{len(jobs)} images could exceed the cap (about ${est:.2f} more); stopping")
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        done = [f.result() for f in [ex.submit(one, g, pack, e, n, model) for e, n in jobs]]
    print(f"{sum(1 for d in done if d)} of {len(jobs)} images written to {OUT.relative_to(ROOT)}; spent so far ${g.spent():.2f}")


if __name__ == "__main__":
    main()
