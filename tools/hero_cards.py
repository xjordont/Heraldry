#!/usr/bin/env python3
"""Extract the 24 Basic Mode Hero profiles (Appendix B.4) for the hero cards, and render the sheets.

`extract` parses B.4 of the current manuscript into typst/heroes/basic-heroes.json without
rewording anything: every rule line is kept as text runs (plain or bold). `check` (the default)
re-extracts and proves two things: the JSON matches the current manuscript, and rebuilding the
Markdown from the JSON reproduces every profile line for line. `render` compiles the blank hero
sheet, the party ledger, and the 24 hero cards to ignored build/heroes/.

usage: python tools/hero_cards.py [check|extract|render] [--paper cream|white|both] [--png] [--only NAME ...]
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "typst" / "heroes" / "basic-heroes.json"
SRC = ROOT / "typst" / "heroes"
OUT = ROOT / "build" / "heroes"

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


def card_problems(pdf_path, hero, reminders, notes=None):
    """Printed-output audit for one hero card: every rule item, sub-item, reminder, and printed statistic
    appears in the PDF text, and no text runs into the ruled notes space on either side."""
    import pymupdf
    # Whitespace, a true minus, and square brackets are presentation: costs print in black tags without them.
    norm = lambda t: re.sub(r"[\s\[\]]+", "", t).replace("\u2212", "-")
    doc = pymupdf.open(str(pdf_path))
    if doc.page_count != 2:
        return [f"{doc.page_count} pages"]
    text = norm("".join(p.get_text() for p in doc))
    items = [it for s in hero["sections"] for it in s["items"]]
    need = ["".join(t for t, _ in it["runs"]) for it in items]
    need += ["".join(t for t, _ in sub) for it in items for sub in it["sub"]]
    senses = hero["stats"].get("Senses")
    if senses:
        key = "Superior Darkvision" if senses.startswith("Superior") else "Darkvision"
        need.append("".join(t for t, _ in reminders[key]["runs"]))
    need += list(hero["stats"].values()) + list(hero["scores"].values())
    need += [hero["name"], hero["class"], hero["ancestry"], hero["background"]]
    if notes:
        need += ["".join(t for t, _ in rs) for rs in notes.values()]
    problems = [f"missing: {n[:70]}" for n in need if norm(n) not in text]
    front = norm(doc[0].get_text())
    front_required = ["".join(t for t, _ in it["runs"])
                      for s in hero["sections"] if s["title"] == "Equipment and Items" for it in s["items"]]
    if notes:
        front_required += ["".join(t for t, _ in rs) for rs in notes.values()]
    problems += [f"missing on front: {n[:70]}" for n in front_required if norm(n) not in front]
    for page in doc:
        spans = [s for b in page.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"] if s["text"].strip()]
        foot = [s for s in spans if "HERALDRY SKIRMISH" in s["text"]]
        if not foot:
            problems.append(f"page {page.number + 1}: footer not found")
            continue
        footer = max(foot, key=lambda s: s["bbox"][1])
        rule = footer["bbox"][1] - 8
        low = [s["text"] for s in spans if s["bbox"][3] > rule and s not in foot and s["bbox"][1] < footer["bbox"][1] - 2]
        if low:
            problems.append(f"page {page.number + 1}: text reaches the footer rule: {low[0][:50]}")
        if page.number == doc.page_count - 1:
            head = [s for s in spans if s["text"].strip().casefold() == "notes"]
            if len(head) != 1:
                problems.append("page 2: Notes heading not found")
                continue
            intruders = [s["text"] for s in spans if s["bbox"][1] > head[0]["bbox"][3] and s["bbox"][3] < rule]
            if intruders:
                problems.append(f"page 2: text inside the notes space: {intruders[0][:50]}")
    return problems


def render(paper, png, only):
    import typst
    from pypdf import PdfReader
    OUT.mkdir(parents=True, exist_ok=True)
    kw = dict(root=str(ROOT), font_paths=[str(ROOT / "fonts/static")], ignore_system_fonts=True)
    data = json.loads(DATA.read_text(encoding="utf-8"))
    names = [h["name"] for h in data["heroes"]]
    jobs = [("hero-sheet", {}, (2,)), ("party-ledger", {}, (2,))]
    jobs += [(f"hero-{n.lower()}", {"hero": n}, (2,)) for n in names]
    jobs += [("basic-heroes", {"hero": "all"}, (48,))]
    bad = 0
    for stem, extra, want in jobs:
        if only and stem not in only and extra.get("hero") not in only:
            continue
        src = SRC / ("ledger.typ" if stem == "party-ledger" else "sheet.typ" if stem == "hero-sheet" else "cards.typ")
        c = typst.Compiler(str(src), sys_inputs={"substrate": paper, **extra}, **kw)
        out = OUT / f"{stem}-{paper}"
        for old in OUT.glob(f"{out.name}-*.png"):
            old.unlink()
        _, warnings = c.compile_with_warnings(output=str(out) + ".pdf")
        for w in warnings:
            print(f"WARN {stem}: {str(w)[:300]}")
        if png and stem != "basic-heroes":
            c.compile(output=str(out) + "-{p}.png", format="png", ppi=110)
        pages = len(PdfReader(str(out) + ".pdf").pages)
        status = "ok" if pages in want and not warnings else "FAIL"
        bad += status == "FAIL"
        print(f"{status} {out.relative_to(ROOT)}.pdf ({pages} pages, want {want})")
        if extra.get("hero", "all") != "all":
            hero = next(h for h in data["heroes"] if h["name"] == extra["hero"])
            for p in card_problems(str(out) + ".pdf", hero, data["reminders"], data["notes"]):
                bad += 1
                print(f"FAIL {stem}: {p}")
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("action", nargs="?", choices=["check", "extract", "render"], default="check")
    ap.add_argument("--paper", choices=["cream", "white", "both"], default="cream")
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    if a.action == "render":
        papers = ["cream", "white"] if a.paper == "both" else [a.paper]
        sys.exit(1 if sum(render(p, a.png, a.only) for p in papers) else 0)
    rc, sha, lines = current_source()
    doc = build_doc(rc, sha, lines)
    text = dumps(doc)
    if a.action == "extract":
        DATA.write_text(text, encoding="utf-8", newline="\n")
        print(f"extracted {len(doc['heroes'])} Heroes from RC{rc}; every profile rebuilds line for line")
        return
    if not DATA.exists() or DATA.read_text(encoding="utf-8") != text:
        sys.exit(f"STALE {DATA.relative_to(ROOT)}: run `python tools/hero_cards.py extract` and review the hero cards")
    print(f"PASS: {len(doc['heroes'])} hero cards match B.4 of RC{rc}, and every profile rebuilds line for line")


if __name__ == "__main__":
    main()
