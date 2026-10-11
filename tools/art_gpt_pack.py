#!/usr/bin/env python3
"""ChatGPT Work handoff pack: one ready-to-paste prompt file per pending illustration plus an
ordered queue (production/art/gpt/QUEUE.json and QUEUE.md). The anchors phase runs first; the
batch phase requires approved anchors. Prompts come from art_generate.prompt_for (owner prompts
override). Regenerate after any catalog, brief or style change.

Queue schema 2: every item carries its register, its own short list of reference images
(config gpt_reference_sets, at most max_refs), its printed width, its attempt budget and the
brief's must / avoid lists, so the runner never has to parse prompt text or attach every anchor.
There is deliberately no queue-level list of references: only an item's own list is ever attached."""
import argparse, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import art_generate as g  # noqa: E402

GPT = ROOT / "production/art/gpt"
SCHEMA = 2
SIZES = {"3:2": "1536x1024", "2:3": "1024x1536", "1:1": "1024x1024"}
ORDER = ["bastion", "climate", "monster", "class", "ancestry", "boss", "scenario", "world", "campaign",
         "tradition", "background", "item", "chapter", "cover"]
IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp")


def received(sels=None):
    sels = g.load(g.SELECTIONS, {}) if sels is None else sels
    return {k for k, v in sels.items() if v.get("route") == "gpt" and v.get("status") in ("received", "approved", "anchor-approved")}


def ref_set(e):
    """(name, candidates) for an entry: kind_sets (by ID) over family_sets (by family) over the register set."""
    cfg = g.CFG["gpt_reference_sets"]
    for kind, spec in cfg.get("kind_sets", {}).items():
        if e["id"] in spec["ids"]:
            return f"{e['family']}:{kind}", spec["refs"]
    if e["family"] in cfg.get("family_sets", {}):
        return e["family"], cfg["family_sets"][e["family"]]
    reg = cfg["register_of_family"][e["family"]]
    return reg, cfg["sets"][reg]


def check_kinds(ents):
    """Every queued monster belongs to exactly one kind, and every kinded ID is a real monster."""
    kinds = g.CFG["gpt_reference_sets"].get("kind_sets", {})
    seen = {}
    for kind, spec in kinds.items():
        for i in spec["ids"]:
            if i in seen:
                raise SystemExit(f"{i} is in kind_sets {seen[i]} and {kind}")
            if i not in ents or ents[i]["family"] != "monster":
                raise SystemExit(f"kind_sets {kind}: {i} is not a monster entry")
            seen[i] = kind
    if kinds:
        missing = sorted(i for i, e in ents.items() if e["family"] == "monster" and i not in seen)
        if missing:
            raise SystemExit("monsters without a kind in kind_sets: " + ", ".join(missing))


def references_for(e, sels, root=ROOT):
    """Up to max_refs reference images for this entry's family (family_sets) or else its register: repo paths
    always (they must exist), anchor IDs once approved. Never the entry itself."""
    cfg = g.CFG["gpt_reference_sets"]
    out = []
    for cand in ref_set(e)[1]:
        if cand.lower().endswith(IMAGE_SUFFIXES):
            if not (root / cand).is_file():
                raise SystemExit(f"reference image missing: {cand}")
            out.append(cand)
        elif cand != e["id"]:
            s = sels.get(cand, {})
            if s.get("route") == "gpt" and s.get("status") in ("approved", "anchor-approved"):
                out.append(s["master"]["path"])
        if len(out) >= cfg["max_refs"]:
            break
    return out


def item_for(e, prompt, sels, root=ROOT):
    fam = g.CFG["families"][e["family"]]
    b = e.get("brief") or {}
    att = g.CFG["gpt_max_attempts"]
    size_code = (e.get("facts") or {}).get("size_code") or ""
    return {"id": e["id"], "family": e["family"], "register": g.CFG["gpt_reference_sets"]["register_of_family"][e["family"]],
            "ref_set": ref_set(e)[0],
            "title": e["title"], "prompt": f"production/art/gpt/prompts/{e['id']}.txt",
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(), "size": SIZES.get(fam["aspect"], "1536x1024"),
            "print_w_in": fam["print_w_in"], "references": references_for(e, sels, root),
            "max_attempts": att.get(e["family"], att["default"]),
            "size_class": g.CFG["size_words"].get(size_code, "") if e["family"] in ("monster", "boss") else "",
            "must": list(b.get("must", [])), "avoid": [x.rstrip(".") + "." for x in b.get("avoid", [])],
            "save_as": f"assets/art/incoming/{e['id']}.png"}


def build_queue(phase, ents, sels, anchors, root=ROOT):
    """Returns (queue dict, {id: prompt text}) without touching disk."""
    done = received(sels)
    if phase == "anchors":
        ids = [i for i in g.CFG["gpt_anchor_ids"] if i not in done]
    else:
        if not (anchors.get("route") == "gpt" and anchors.get("status") == "approved"):
            raise SystemExit("GPT anchors are not approved yet")
        check_kinds(ents)
        lead = [i for i in g.CFG.get("gpt_lead_ids", []) if i in ents and i not in done]
        ids = lead + sorted((i for i in ents if i not in done and i not in lead), key=lambda i: (ORDER.index(ents[i]["family"]), i))
    prompts, items = {}, []
    for i in ids:
        prompts[i] = g.prompt_for(ents[i], True)
        items.append(item_for(ents[i], prompts[i], sels, root))
    return {"schema": SCHEMA, "phase": phase, "generated_at": g.now(), "max_references": g.CFG["gpt_reference_sets"]["max_refs"],
            "push_every": g.CFG.get("gpt_push_every", 5), "review_every": g.CFG.get("gpt_review_every", 10),
            "count": len(items), "items": items}, prompts


def queue_markdown(q):
    sets = []
    for it in q["items"]:
        if tuple(it["references"]) not in sets:
            sets.append(tuple(it["references"]))
    letter = lambda t: chr(65 + sets.index(t))  # noqa: E731
    md = [f"# ChatGPT Work queue: {q['phase']} ({q['count']} images)", "",
          "Follow `production/art/gpt/INSTRUCTIONS.md`. Attach each item's own references (its set below), never the whole list.", "",
          "| Set | Reference images |", "|---|---|"]
    md += [f"| {letter(t)} | " + "<br>".join(f"`{r}`" for r in t) + " |" for t in sets]
    md += ["", "| # | ID | Subject | Size | Set | Tries | Prompt |", "|---|---|---|---|---|---|---|"]
    md += [f"| {n} | `{x['id']}` | {x['title']} | {x['size']} | {letter(tuple(x['references']))} | {x['max_attempts']} | `{x['prompt']}` |"
           for n, x in enumerate(q["items"], 1)]
    return "\n".join(md) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["anchors", "batch"], default=None)
    a = ap.parse_args()
    anchors = g.load(g.ANCHORS, {})
    gpt_anchor_ok = anchors.get("route") == "gpt" and anchors.get("status") == "approved"
    phase = a.phase or ("batch" if gpt_anchor_ok else "anchors")
    ents = {e["id"]: e for e in g.entries()}
    q, prompts = build_queue(phase, ents, g.load(g.SELECTIONS, {}), anchors)
    (GPT / "prompts").mkdir(parents=True, exist_ok=True)
    for old in (GPT / "prompts").glob("*.txt"):
        old.unlink()
    for i, p in prompts.items():
        (GPT / "prompts" / f"{i}.txt").write_text(p + "\n")
    g.save(GPT / "QUEUE.json", q)
    (GPT / "QUEUE.md").write_text(queue_markdown(q))
    print(json.dumps({"phase": phase, "count": q["count"]}))


if __name__ == "__main__":
    main()
