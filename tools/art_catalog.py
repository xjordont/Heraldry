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
    for e in entries:
        e["spec_sha256"] = hashlib.sha256(json.dumps({k: e.get(k) for k in ("family", "title", "subject", "composition", "flavour", "facts", "context")}, sort_keys=True).encode()).hexdigest()
    counts = {}
    for e in entries:
        counts[e["family"]] = counts.get(e["family"], 0) + 1
    OUT.write_text(json.dumps({"source_sha256": model["sha256"], "counts": counts, "total": len(entries), "entries": entries}, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({"total": len(entries), "counts": counts}))


if __name__ == "__main__":
    main()
