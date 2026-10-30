#!/usr/bin/env python3
"""Deterministic illustration catalog: every heading whose first block is flavour text,
plus the cover and chapter openers. Writes production/art/SPOT_CATALOG.json.
Text is copied verbatim from build/blocks.json (the current manuscript); nothing is paraphrased."""
import hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_book import is_flavour  # noqa: E402

OUT = ROOT / "production/art/SPOT_CATALOG.json"


def text(nodes):
    s = ""
    for n in nodes:
        s += n["v"] if n.get("t") == "text" else ("\n" if n.get("t") in ("softbreak", "hardbreak") else text(n.get("c", [])))
    return s


def slug(s):
    return re.sub(r"[^A-Z0-9]+", "-", s.upper()).strip("-")[:40]


def family(chapter, parents, title):
    num = chapter.split(".")[0]
    p = " / ".join(parents)
    if num == "1":
        return "climate" if "Climates" in p else "bastion" if "Bastions" in p else "world"
    if num == "6":
        return "ancestry" if "6.9" in p else "background" if "6.10" in p else "class" if "6.13" in p else "world"
    return {"7": "item", "8": "tradition", "9": "monster", "10": "scenario", "11": "campaign"}.get(num, "scenario" if chapter.startswith("Appendix A") else None)


def table_cell(blk, col):
    hdr = [text(c).strip() for c in blk["header"]]
    if col in hdr and blk["rows"]:
        return text(blk["rows"][0][hdr.index(col)]).strip()
    return None


def hero_entries(model):
    """Basic Mode Hero profiles (Appendix B.4): one entry per level-4 heading, with the class, ancestry,
    background, size and equipment names read verbatim from the profile. Profiles have no flavour block."""
    out = []
    for ch in model["chapters"]:
        blocks, inside, cur = ch["blocks"], False, None
        for b in blocks:
            if b["type"] == "heading" and int(b["level"]) <= 3:
                inside = b["title"].startswith("B.4 ")
            if not inside:
                continue
            if b["type"] == "heading" and int(b["level"]) == 4:
                cur = {"id": "ART-HER-" + slug(b["title"]), "family": "hero", "heading_id": b["id"], "title": b["title"],
                       "context": [ch["title"], "B.4 Basic Mode Hero Profiles"], "facts": {}, "src_lines": b["src"]}
                out.append(cur)
            elif cur is not None and b["type"] == "para":
                t = text(b["c"])
                m = re.match(r"Class: (.+?) \| Ancestry and Background: (.+?) \| Level:", t)
                if m:
                    ancestry, _, background = m.group(2).rpartition(" ")
                    cur["facts"].update(cls=m.group(1), ancestry=ancestry, background=background)
                m = re.search(r"Sz: (\w+)", t)
                if m:
                    cur["facts"]["size_code"] = m.group(1)
                if t.strip() == "Equipment and Items":
                    cur["_eq"] = True
            elif cur is not None and cur.get("_eq") and b["type"] == "list":
                cur["facts"]["equipment"] = [text(i["blocks"][0]["c"]).split(":")[0].split(" [")[0].strip() for i in b["items"]]
                cur.pop("_eq")
    return out


def end_art_entries(model):
    """Section-end tailpieces (owner 2026-10-30: fill the white space a section's last page leaves
    with art). `production/art/END_ART_PLAN.json` names each section, family, and subject; the brief
    in `production/art/briefs/end_art.json` gives the art direction. The book sets an approved
    tailpiece below the section's text only where the page would otherwise stay empty."""
    plan = ROOT / "production/art/END_ART_PLAN.json"
    if not plan.exists():
        return []
    heads = {b["id"]: (ch["title"], b) for ch in model["chapters"] for b in ch["blocks"] if b["type"] == "heading"}
    out = []
    for p in json.loads(plan.read_text())["entries"]:
        if p["heading_id"] not in heads:
            raise SystemExit(f"{p['id']}: heading {p['heading_id']} is not in the active manuscript")
        chapter, head = heads[p["heading_id"]]
        out.append({"id": p["id"], "family": p["family"], "heading_id": p["heading_id"], "end_art": True,
                    "title": p["title"], "context": [chapter, head["title"]], "facts": {}, "src_lines": head["src"]})
    return out


PLAN = ROOT / "production/art/SUBJECT_PLAN.json"
OWNER = ROOT / "production/art/OWNER_PROMPTS.json"


def audit(entries):
    """Uniqueness gate: every entry needs a distinct visual subject. Entries whose names share a
    core noun (e.g. Goblin ancestry vs Goblin monster, a dragon vs a named dragon boss) must be
    separated by family framing or explicit direction; chapter subjects must not repeat an entry."""
    subj = {}
    for e in entries:
        key = (e.get("subject") or "") + "|" + (e.get("direction") or "") + "|" + (e.get("flavour") or "") + "|" + json.dumps(e.get("brief", {}).get("composition", ""))
        if key in subj:
            raise SystemExit(f"duplicate visual subject: {e['id']} and {subj[key]}")
        subj[key] = e["id"]
    core = lambda t: re.sub(r"^(scenario \d+: |the |tier \d )", "", t.lower()).split(" [")[0]
    names = {}
    for e in entries:
        names.setdefault(core(e["title"]), []).append(e)
    for n, es in names.items():
        fams = [x["family"] for x in es]
        if len(es) > 1 and len(set(fams)) < len(fams) and not all("direction" in x for x in es):
            raise SystemExit(f"same name and family: {[x['id'] for x in es]}")
        if len(es) > 1 and sum("direction" not in x for x in es) > 1:
            raise SystemExit(f"name collision without direction: {[x['id'] for x in es]}")


def main():
    model = json.loads((ROOT / "build/blocks.json").read_text())
    man = json.loads((ROOT / "production/art/ART_MANIFEST.json").read_text())["assets"]
    entries = []
    for a in man:
        fam = "cover" if a["asset_id"] == "ART-COVER-001" else "chapter"
        entries.append({"id": a["asset_id"].replace("-001", "-002"), "family": fam, "heading_id": None,
                        "title": a["asset_id"], "subject": a["subject"], "composition": a.get("composition", ""),
                        "lore_refs": a.get("source_lore_refs", []), "replaces": a["asset_id"]})
    seen = set()
    for ch in model["chapters"]:
        blocks = ch["blocks"]
        stack = []
        for i, b in enumerate(blocks):
            if b["type"] != "heading":
                continue
            lvl = int(b["level"])
            stack = [s for s in stack if s[0] < lvl] + [(lvl, b["title"])]
            if lvl <= 2 or i + 1 >= len(blocks) or not is_flavour(blocks[i + 1]):
                continue
            fam = family(ch["title"], [t for _, t in stack[:-1]], b["title"])
            if fam is None:
                continue
            facts = {}
            if fam == "monster":
                m = re.search(r"\[([^\]]+)\]", b["title"])
                facts["role"] = m.group(1) if m else None
                for nb in blocks[i + 2:i + 4]:
                    if nb["type"] == "table":
                        facts["size_code"] = table_cell(nb, "Sz")
                        break
            name = re.sub(r"\s*\[[^\]]*\]\s*$", "", b["title"]).strip()
            base = f"ART-{fam[:3].upper()}-{slug(name)}"
            aid, k = base, 2
            while aid in seen:
                aid, k = f"{base}-{k}", k + 1
            seen.add(aid)
            entries.append({"id": aid, "family": fam, "heading_id": b["id"], "flavour_block": blocks[i + 1]["id"],
                            "title": name, "context": [t for _, t in stack[:-1]][-2:],
                            "flavour": text(blocks[i + 1]["c"]).strip(), "facts": facts,
                            "src_lines": b["src"]})
    entries += hero_entries(model)
    entries += end_art_entries(model)
    # orchestrator art direction: fresh chapter subjects, boss family, per-entry unique subjects
    plan = json.loads(PLAN.read_text()) if PLAN.exists() else {"chapters": {}, "direction": {}}
    for e in entries:
        if e["id"] in plan["chapters"]:
            e.update(plan["chapters"][e["id"]])
        if e["family"] == "monster" and e.get("context") and e["context"][-1] == "Bosses":
            e["family"] = "boss"
        if plan["direction"].get(e["id"]):
            e["direction"] = plan["direction"][e["id"]]
    # per-entry briefs (orchestrator/worker art direction from the manuscript) and owner prompts
    briefs = {}
    for f in sorted((ROOT / "production/art/briefs").glob("*.json")):
        briefs.update({k: v for k, v in json.loads(f.read_text()).items() if not k.startswith("_")})
    owner = json.loads(OWNER.read_text()) if OWNER.exists() else {}
    for e in entries:
        if e["id"] in briefs:
            e["brief"] = briefs[e["id"]]
        if e["id"] in owner:
            e["owner_prompt_sha256"] = hashlib.sha256(owner[e["id"]].encode()).hexdigest()
    for e in entries:
        keys = ("family", "title", "subject", "composition", "flavour", "facts", "context") + tuple(k for k in ("direction", "brief", "owner_prompt_sha256") if k in e)
        e["spec_sha256"] = hashlib.sha256(json.dumps({k: e.get(k) for k in keys}, sort_keys=True).encode()).hexdigest()
    unbriefed = [e["id"] for e in entries if e["family"] == "hero" and "brief" not in e]
    if unbriefed:
        raise SystemExit(f"Hero entries without a brief in production/art/briefs/heroes.json: {unbriefed}")
    unbriefed = [e["id"] for e in entries if e.get("end_art") and "brief" not in e]
    if unbriefed:
        raise SystemExit(f"Tailpieces without a brief in production/art/briefs/end_art.json: {unbriefed}")
    audit(entries)
    counts = {}
    for e in entries:
        counts[e["family"]] = counts.get(e["family"], 0) + 1
    OUT.write_text(json.dumps({"source_sha256": model["sha256"], "counts": counts, "total": len(entries), "entries": entries}, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({"total": len(entries), "counts": counts}))


if __name__ == "__main__":
    main()
