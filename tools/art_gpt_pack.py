#!/usr/bin/env python3
"""ChatGPT Work handoff pack: one ready-to-paste prompt file per pending illustration plus an
ordered queue (production/art/gpt/QUEUE.json and QUEUE.md). The anchors phase runs first; the
batch phase requires approved anchors. Prompts come from art_generate.prompt_for (owner prompts
override). Regenerate after any catalog, brief or style change."""
import argparse, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import art_generate as g  # noqa: E402

GPT = ROOT / "production/art/gpt"
SIZES = {"3:2": "1536x1024", "2:3": "1024x1536", "1:1": "1024x1024"}
ORDER = ["bastion", "climate", "monster", "class", "ancestry", "boss", "scenario", "world", "campaign",
         "tradition", "background", "item", "chapter", "cover"]


def received():
    sels = g.load(g.SELECTIONS, {})
    return {k for k, v in sels.items() if v.get("route") == "gpt" and v.get("status") in ("received", "approved", "anchor-approved")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["anchors", "batch"], default=None)
    a = ap.parse_args()
    anchors = g.load(g.ANCHORS, {})
    gpt_anchor_ok = anchors.get("route") == "gpt" and anchors.get("status") == "approved"
    phase = a.phase or ("batch" if gpt_anchor_ok else "anchors")
    done = received()
    ents = {e["id"]: e for e in g.entries()}
    if phase == "anchors":
        ids = [i for i in g.CFG["gpt_anchor_ids"] if i not in done]
        refs = g.CFG["style_refs"]
    else:
        if not gpt_anchor_ok:
            raise SystemExit("GPT anchors are not approved yet")
        ids = sorted((i for i in ents if i not in done),
                     key=lambda i: (ORDER.index(ents[i]["family"]), i))
        refs = anchors["references"]
    (GPT / "prompts").mkdir(parents=True, exist_ok=True)
    for old in (GPT / "prompts").glob("*.txt"):
        old.unlink()
    items = []
    for i in ids:
        e = ents[i]
        p = g.prompt_for(e, True)
        f = GPT / "prompts" / f"{i}.txt"
        f.write_text(p + "\n")
        aspect = g.CFG["families"][e["family"]]["aspect"]
        items.append({"id": i, "family": e["family"], "title": e["title"], "prompt": str(f.relative_to(ROOT)),
                      "prompt_sha256": hashlib.sha256(p.encode()).hexdigest(), "size": SIZES.get(aspect, "1536x1024"),
                      "save_as": f"assets/art/incoming/{i}.png"})
    q = {"phase": phase, "generated_at": g.now(), "references": refs, "count": len(items), "items": items}
    g.save(GPT / "QUEUE.json", q)
    md = [f"# ChatGPT Work queue: {phase} ({len(items)} images)", "",
          "Follow `production/art/gpt/INSTRUCTIONS.md`. Attach these reference images to every generation:", ""]
    md += [f"- `{r}`" for r in refs] + ["", "| # | ID | Subject | Size | Prompt |", "|---|---|---|---|---|"]
    md += [f"| {n} | `{x['id']}` | {x['title']} | {x['size']} | `{x['prompt']}` |" for n, x in enumerate(items, 1)]
    (GPT / "QUEUE.md").write_text("\n".join(md) + "\n")
    print(json.dumps({"phase": phase, "count": len(items)}))


if __name__ == "__main__":
    main()
