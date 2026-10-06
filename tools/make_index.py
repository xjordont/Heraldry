#!/usr/bin/env python3
"""Build the curated subject index from the manuscript's own structure.

Main entries: every term of C.11 Glossary of Terms and Conditions (the source's
sole alphabetised glossary). Locators, in priority order:
  1. the glossary entry itself (C.11);
  2. sections the entry cites ("See 7.6") — resolved to the numbered heading;
  3. headings whose title names the term (definition sections, max 3);
  4. definitional blocks outside C.11 that open with the term in bold (max 3).
Short-form glossary entries ("Short form of X") become See references.
Named-entry groups (ancestries, classes, Monster entries, scenarios, Powers by
tradition are NOT exhaustively listed) are added as sub-entries from headings.
Locators are tagged on stable block ids; page numbers come from the final layout.
Output: build/index_targets.json, build/index.json, production/mappings/index.json
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from parse_source import plain  # noqa: E402


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main():
    model = json.loads((ROOT / "build/blocks.json").read_text())
    heads = json.loads((ROOT / "production/inventory/headings.json").read_text())
    num2head = {}
    for h in heads:
        m = re.match(r"^((?:\d+|[A-C])(?:\.\d+)+|\d+)\.?\s", h["title"])
        if m:
            num2head.setdefault(m.group(1), h["id"])
    # flatten blocks in source order with chapter id
    flat = []

    def walk(bs, ch, sec):
        for b in bs:
            if b["type"] == "heading":
                sec = b["id"]
            flat.append((b, ch, sec))
            for it in b.get("items", []):
                walk(it["blocks"], ch, sec)
            walk(b.get("blocks", []), ch, sec)
        return sec

    for ch in model["chapters"]:
        if ch["id"] in ("front", "h-table-of-contents"):
            continue
        walk(ch["blocks"], ch["id"], None)

    # ---- glossary
    gloss = []
    in_gloss = False
    for b, ch, sec in flat:
        if b["type"] == "heading":
            if b["level"] <= 3:
                in_gloss = b["title"].startswith("C.11 ")
            continue
        if in_gloss and b["type"] == "para" and b["c"] and b["c"][0]["t"] == "strong":
            term = plain(b["c"][0]["c"]).strip()
            if term.endswith(":"):
                gloss.append((term[:-1].strip(), b))
    targets = {}
    entries = []
    mapping = []

    def tag(bid, key):
        targets.setdefault(bid, [])
        if key not in targets[bid]:
            targets[bid].append(key)

    first_bold = {}
    for b, ch, sec in flat:
        if b["type"] in ("para",) and b["c"] and b["c"][0]["t"] == "strong" and not (sec or "").startswith("h-c11"):
            t = plain(b["c"][0]["c"]).strip().rstrip(":").strip().rstrip(".")
            first_bold.setdefault(t.lower(), []).append(b["id"])

    for term, gb in gloss:
        key = "g-" + slug(term)
        text = plain(gb["c"])
        m = re.match(r"^Short form of (.+?)\.?$", text[len(term) + 1:].strip())
        if m:
            entries.append({"term": term, "keys": [], "see": m.group(1).strip()})
            mapping.append({"term": term, "see": m.group(1).strip(), "source": gb["id"]})
            continue
        locs = [gb["id"]]
        for ref in re.findall(r"\b((?:\d+|[A-C])(?:\.\d+)+)\b", text):
            if ref in num2head and num2head[ref] not in locs:
                locs.append(num2head[ref])
        rx = re.compile(r"(?<![\w-])" + re.escape(term) + r"(?![\w-])", re.I)
        hs = [h["id"] for h in heads if h["level"] in (3, 4) and rx.search(h["title"]) and not h["title"].startswith("C.")]
        for hid in hs[:3]:
            if hid not in locs:
                locs.append(hid)
        for bid in first_bold.get(term.lower(), [])[:3]:
            if bid not in locs:
                locs.append(bid)
        locs = locs[:7]
        for bid in locs:
            tag(bid, key)
        entries.append({"term": term, "keys": [key]})
        mapping.append({"term": term, "key": key, "locators": locs, "basis": "glossary + cited sections + titled sections + definitional bold"})

    # ---- curated section-level concepts (added only when the glossary lacks the term)
    extras = {
        "Weather": ["10.3"], "Secondary Objectives": ["10.2"], "Scenario Scaling": ["10.6"],
        "Solo and Cooperative Play": ["10.5", "11.5"], "Stronghold": ["11.3"], "Legendary Veterans": ["11.4"],
        "Hirelings": ["6.15"], "Backgrounds": ["6.10"], "General Talents": ["6.12"], "Monster AI": ["9.5", "C.8"],
        "Universal Special Abilities": ["9.6"], "Random Monster Generation": ["9.8"], "Weapons": ["7.8", "7.9"],
        "Armour": ["7.10"], "Shields": ["7.12"], "Potions": ["7.13"], "Poisons": ["7.14"], "Scrolls": ["7.15"],
        "Character Creation": ["6.2", "6.3"], "Hero Advancement": ["6.16"], "Campaign Cycle": ["11.2"],
        "Adventure Preparation": ["10.1"], "Learn to Play": ["A"], "Basic Mode": ["B"], "Rules Reference": ["C"],
        "Rules Hierarchy": ["1.6"], "Measurement": ["2.6"], "Line of Sight": ["2.7"], "Terrain": ["2.9"],
        "Reactions": ["4.5", "C.5"], "Attack Sequence": ["5.2", "C.6"], "Monster Phase": ["3.4"], "Party Phase": ["3.3"],
        "Initiative Phase": ["3.2"], "End of Round": ["3.5"], "Timing Rules": ["3.6"],
    }
    have = {e["term"].lower() for e in entries}
    letter_head = {h["title"].split(".")[0].replace("Appendix ", ""): h["id"] for h in heads if h["level"] == 2 and h["title"].startswith("Appendix")}
    for term, refs in extras.items():
        locs = [num2head.get(r) or letter_head.get(r) for r in refs]
        locs = [l for l in locs if l]
        if not locs:
            continue
        key = "x-" + slug(term)
        if term.lower() in have:
            e = next(e for e in entries if e["term"].lower() == term.lower())
            key = (e["keys"] or [key])[0]
            if not e["keys"]:
                continue
        else:
            entries.append({"term": term, "keys": [key]})
        for l in locs:
            tag(l, key)
        mapping.append({"term": term, "key": key, "locators": locs, "basis": "curated section"})

    # ---- named-entry groups from headings
    def group(title, parent_ids, level, strip=r"\s*\[[^\]]*\]$"):
        subs = []
        for h in heads:
            if h["level"] == level and h["parents"] and any(p in parent_ids for p in h["parents"]):
                name = re.sub(strip, "", h["title"]).strip()
                key = "n-" + slug(title) + "-" + slug(name)
                tag(h["id"], key)
                subs.append({"term": name, "keys": [key]})
                mapping.append({"term": f"{title} — {name}", "key": key, "locators": [h["id"]], "basis": "named entry heading"})
        subs.sort(key=lambda s: s["term"].lower())
        return subs

    hid = {h["title"]: h["id"] for h in heads}
    groups = [
        ("Ancestries", ["h-69-ancestries"], 4, r"^$"),
        ("Classes", ["h-613-hero-classes"], 4, r"\s*\[[^\]]*\]$"),
        ("Monsters (Bestiary entries)", ["h-97-the-bestiary"], 5, r"\s*\[[^\]]*\]$"),
        ("Scenarios (Core)", ["h-104-core-scenario-outlines"], 5, r"^$"),
    ]
    for title, parents, lvl, strip in groups:
        subs = group(title, parents, lvl, strip)
        # drop structural headings that are not named entries
        subs = [s for s in subs if not re.match(r"^(Reading a Stat Line|Monster Roles|Entry Structure|Class Archetypes|Universal Class Progression|Resource Restrictions|Automatic Special Abilities)$", s["term"])]
        if subs:
            entries.append({"term": title, "keys": [], "sub": subs})

    # merge duplicate terms, sort
    entries.sort(key=lambda e: re.sub(r"[^a-z0-9 ]", "", e["term"].lower()))
    note = ("Main entries follow the terms of C.11 Glossary of Terms and Conditions. "
            "Locators point to the glossary entry, the sections it cites, and sections that define or apply the term.")
    (ROOT / "build/index.json").write_text(json.dumps({"note": note, "entries": entries}, ensure_ascii=False))
    (ROOT / "build/index_targets.json").write_text(json.dumps(targets, ensure_ascii=False))
    (ROOT / "production/mappings").mkdir(parents=True, exist_ok=True)
    (ROOT / "production/mappings/index.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=0))
    print(f"entries={len(entries)} glossary_terms={len(gloss)} tagged_blocks={len(targets)}")


if __name__ == "__main__":
    main()
