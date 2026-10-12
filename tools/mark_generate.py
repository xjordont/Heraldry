#!/usr/bin/env python3
"""Generate candidate images for the heraldic marks (logo and chapter arms) with the Gemini image API.

Owner instruction 2026-10-12 (production/art/marks/PROMPTS.json). Runs only in the manual
'Generate heraldic marks' workflow, which holds GEMINI_API_KEY as a secret; the key is never printed.
Shares tools/art_generate.py's key handling, model resolution, budget cap and cost ledger.
Candidates go to assets/art/marks/candidates/<ID>-v<n>.png (round 1) or <ID>-r<round>-v<n>.png; nothing is placed until approved.

    python3 tools/mark_generate.py prompts            # print the assembled prompts (no API call)
    python3 tools/mark_generate.py run [--ids ...]    # generate the variants and commit them
"""
import argparse
import base64
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
SPEC = ROOT / "production/art/marks/PROMPTS.json"
OUT = ROOT / "assets/art/marks/candidates"


def prompts(spec):
    out = {}
    for it in spec["items"]:
        parts = [it["subject"], spec["style"]]
        if it["kind"] == "arms":
            parts.append(spec["series"])
        out[it["id"]] = "\n\n".join(parts)
    return out


def run(ids):
    import art_generate as g
    from PIL import Image
    spec = json.loads(SPEC.read_text())
    texts = prompts(spec)
    items = [it for it in spec["items"] if not ids or it["id"] in ids]
    model = g.resolve("image")
    print(f"image model: {model}; budget used so far ${g.spent():.2f} of ${g.CFG['budget_usd']:.2f}")
    OUT.mkdir(parents=True, exist_ok=True)
    made = 0
    rnd = spec.get("round", 1)
    tag = f"-r{rnd}" if rnd > 1 else ""
    for it in items:
        for v in range(1, it["variants"] + 1):
            if g.spent() >= g.CFG["budget_usd"]:
                print("budget cap reached; stopping")
                return made
            cfg = {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": it["aspect"], "imageSize": it["size"]}}
            body = {"contents": [{"role": "user", "parts": [{"text": texts[it["id"]]}]}], "generationConfig": cfg}
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
            g.ledger({"t": g.now(), "kind": "mark", "id": it["id"], "round": rnd, "variant": v, "model": model, "usage": u,
                      "usd_est": round(g.usd(u, "image"), 5), "ok": img is not None,
                      "prompt_sha256": g.sha(texts[it["id"]].encode())})
            if img is None:
                print(f"{it['id']} v{v}: no image ({(r.get('candidates') or [{}])[0].get('finishReason')})")
                continue
            Image.open(io.BytesIO(img)).save(OUT / f"{it['id']}{tag}-v{v}.png")
            made += 1
            print(f"{it['id']} v{v}: saved")
    return made


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cmd", choices=("prompts", "run"))
    ap.add_argument("--ids", nargs="*", default=[])
    a = ap.parse_args()
    spec = json.loads(SPEC.read_text())
    if a.cmd == "prompts":
        for k, t in prompts(spec).items():
            if not a.ids or k in a.ids:
                print(f"=== {k}\n{t}\n")
        return
    n = run(set(a.ids))
    print(f"{n} candidates written to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
