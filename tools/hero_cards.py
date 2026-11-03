#!/usr/bin/env python3
"""Extract the 24 Basic Mode Hero profiles (Appendix B.4) into typst/heroes/basic-heroes.json.

`extract` parses B.4 of the current manuscript into the JSON without rewording anything: every rule line is
kept as text runs (plain or bold). `check` (the default) re-extracts and proves two things: the JSON matches the
current manuscript, and rebuilding the Markdown from the JSON reproduces every profile line for line. The
illustrated Hero record (assets/hero-record/sheet.py) builds the released Hero PDFs from this JSON.

usage: python tools/hero_cards.py [check|extract]
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "typst" / "heroes" / "basic-heroes.json"

SECTIONS = ["Ancestry Traits", "Background Rule", "Equipment and Items",
            "Talents, Powers, and Special Rules", "Weapon Trait Rules"]
STAT_KEYS = ["HP", "AD", "SPD", "Sz", "AP", "Luck", "NRG", "Coins", "Senses"]
SCORES = ["STR", "DEX", "INT", "SPI"]


def current_source():
    v = json.loads((ROOT / "source/versions.json").read_text(encoding="utf-8"))
    rev = next(r for r in v["revisions"] if r["number"] == v["current"])
    return v["current"], rev["sha256"], (ROOT / rev["path"]).read_text(encoding="utf-8").split("\n")


def runs(md):
    """Split inline Markdown into [text, bold] runs. Only **bold** occurs in B.4 profiles."""
    if "*" in md.replace("**", ""):
        raise ValueError(f"unexpected emphasis markup: {md[:80]}")
    parts = md.split("**")
    if len(parts) % 2 == 0:
        raise ValueError(f"unbalanced bold: {md[:80]}")
    return [[p, i % 2 == 1] for i, p in enumerate(parts) if p]


def unruns(rs):
    return "".join(f"**{t}**" if b else t for t, b in rs)


def pipe_fields(line):
    out = {}
    for cell in line.split(" | "):
        m = re.fullmatch(r"\*\*([^*]+):\*\* (.+)", cell)
        if not m:
            raise ValueError(f"bad field cell: {cell!r}")
        out[m.group(1)] = m.group(2)
    return out


def b4_bounds(lines):
    a = lines.index("### B.4 Basic Mode Hero Profiles")
    b = next(i for i in range(a + 1, len(lines)) if lines[i].startswith("### "))
    return a, b


def class_facts(lines):
    """Archetype, HP per level, and Primary Casting Score from each 6.13 class entry."""
    facts = {}
    for i, line in enumerate(lines):
        m = re.match(r"^#### (\w+) \[\d/5 Complexity\]$", line)
        if not m:
            continue
        block = lines[i:i + 14]
        get = lambda k: next(l.split(":** ", 1)[1] for l in block if l.startswith(f"**{k}:**"))
        facts[m.group(1)] = {"archetype": get("Archetype"), "hp_per_level": get("Max HP Gained per Level"),
                             "casting": get("Primary Casting Score")}
    return facts


def reminders(lines, a):
    out = {}
    for line in lines[a:a + 60]:
        m = re.match(r"^\*\*((?:Superior )?Darkvision) \((\d+)\"\) Reminder:\*\* (.+)$", line)
        if m:
            out[m.group(1)] = {"head": f"{m.group(1)} ({m.group(2)}\") Reminder", "runs": runs(m.group(3))}
    return out


def parse_items(body):
    """Bullet list -> [{runs, sub:[runs...]}]. Two-space indented bullets are sub-items."""
    items = []
    for line in body:
        if not line:
            continue
        if line.startswith("- "):
            items.append({"runs": runs(line[2:]), "sub": []})
        elif line.startswith("  - "):
            items[-1]["sub"].append(runs(line[4:]))
        else:
            raise ValueError(f"unexpected line in list: {line[:80]!r}")
    return items


def parse_hero(block, roster, facts):
    name = block[0][5:]
    ident = pipe_fields(block[2])
    stats = pipe_fields(block[4])
    scores = pipe_fields(block[6])
    if block[1] or block[3] or block[5] or block[7]:
        raise ValueError(f"{name}: unexpected profile header layout")
    if set(stats) - set(STAT_KEYS) or list(scores) != SCORES:
        raise ValueError(f"{name}: unexpected stat keys")
    secs, cur = {}, None
    for line in block[8:]:
        m = re.fullmatch(r"\*\*([^*]+)\*\*", line)
        if m and m.group(1) in SECTIONS:
            cur = m.group(1)
            secs[cur] = []
        elif cur is None:
            if line:
                raise ValueError(f"{name}: text before first section: {line[:60]!r}")
        else:
            secs[cur].append(line)
    r = roster[name]
    if ident["Class"] != r["class"] or ident["Ancestry and Background"] != f"{r['ancestry']} {r['background']}":
        raise ValueError(f"{name}: identity line disagrees with the roster table")
    f = facts[r["class"]]
    return {
        "name": name, "class": r["class"], "ancestry": r["ancestry"], "background": r["background"],
        "role": r["role"], "level": ident["Level"], "archetype": f["archetype"],
        "hp_per_level": f["hp_per_level"], "casting": f["casting"],
        "stats": stats, "scores": scores,
        "sections": [{"title": t, "items": parse_items(secs[t])} for t in SECTIONS if t in secs],
        "art": "ART-HER-" + name.upper(),
    }


def unparse_hero(h):
    """Rebuild the profile Markdown exactly as B.4 prints it, from the JSON."""
    out = [f"#### {h['name']}", "",
           f"**Class:** {h['class']} | **Ancestry and Background:** {h['ancestry']} {h['background']} | **Level:** {h['level']}", "",
           " | ".join(f"**{k}:** {v}" for k, v in h["stats"].items()), "",
           " | ".join(f"**{k}:** {v}" for k, v in h["scores"].items()), ""]
    for s in h["sections"]:
        out += [f"**{s['title']}**", ""]
        for it in s["items"]:
            out.append("- " + unruns(it["runs"]))
            out += ["  - " + unruns(sr) for sr in it["sub"]]
        out.append("")
    return out


def extract(lines):
    a, b = b4_bounds(lines)
    roster = {}
    for line in lines[a:b]:
        m = re.fullmatch(r"\| \*\*(\w+)\*\* \| (\w+) \| ([\w ]+) \| (\w+) \| (.+) \|", line)
        if m:
            roster[m.group(1)] = dict(zip(["class", "ancestry", "background", "role"], m.groups()[1:]))
    starts = [i for i in range(a, b) if lines[i].startswith("#### ")] + [b]
    facts = class_facts(lines)
    heroes, blocks = [], []
    for s, e in zip(starts, starts[1:]):
        blk = lines[s:e]
        heroes.append(parse_hero(blk, roster, facts))
        blocks.append(blk)
    if len(heroes) != 24 or [h["name"] for h in heroes] != list(roster):
        raise ValueError("expected the 24 roster Heroes in roster order")
    for h, blk in zip(heroes, blocks):
        rebuilt = unparse_hero(h)
        if rebuilt != blk[:len(rebuilt)] or any(blk[len(rebuilt):]):
            raise ValueError(f"{h['name']}: JSON does not rebuild the source profile line for line")
    intro = lines[a:starts[0]]
    hands = next(l for l in intro if l.startswith("Before deployment, choose each Hero's active Hands"))
    ko = next(l for l in lines[lines.index("## Appendix B. Basic Mode"):a] if l.startswith("When a Hero reaches **0 HP** in Basic Mode"))
    return heroes, reminders(lines, a), {"hands": runs(hands), "knocked_out": runs(ko)}


def build_doc(rc, sha, lines):
    """The card data. It holds only what the cards print, so a revision that leaves B.4, the Basic Mode
    0 HP rule, and the class entries alone leaves it unchanged."""
    heroes, rem, notes = extract(lines)
    a, b = b4_bounds(lines)
    return {"b4_sha256": hashlib.sha256("\n".join(lines[a:b]).encode("utf-8")).hexdigest(),
            "reminders": rem, "notes": notes, "heroes": heroes}


def dumps(doc):
    """Indented JSON with each [text, bold] run on one line, so a reworded rule shows as a one-line diff."""
    text = json.dumps(doc, indent=1, ensure_ascii=False) + "\n"
    return re.sub(r'\[\n\s*("(?:[^"\\]|\\.)*"),\n\s*(true|false)\n\s*\]', r"[\1, \2]", text)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("action", nargs="?", choices=["check", "extract"], default="check")
    a = ap.parse_args()
    rc, sha, lines = current_source()
    doc = build_doc(rc, sha, lines)
    text = dumps(doc)
    if a.action == "extract":
        DATA.write_text(text, encoding="utf-8", newline="\n")
        print(f"extracted {len(doc['heroes'])} Heroes from RC{rc}; every profile rebuilds line for line")
        return
    if not DATA.exists() or DATA.read_text(encoding="utf-8") != text:
        sys.exit(f"STALE {DATA.relative_to(ROOT)}: run `python tools/hero_cards.py extract` and review the Hero record")
    print(f"PASS: {len(doc['heroes'])} Hero profiles match B.4 of RC{rc}, and every profile rebuilds line for line")


if __name__ == "__main__":
    main()
