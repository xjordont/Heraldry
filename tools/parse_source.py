#!/usr/bin/env python3
"""Parse the active versioned manuscript into a lossless semantic block model.

Output: build/blocks.json (document model consumed by the Typst templates) and
production/inventory/*.json (heading, table, construct and source-span inventories).

The source text is never rewritten: every inline text node is the exact substring
markdown-it produced from the protected source; the source hash is checked first.
Unsupported Markdown constructs raise instead of being dropped.
"""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
from manuscript import source_path, check
SRC = source_path()


def slugify(text: str) -> str:
    """GitHub-style anchor slug (matches the manuscript's manual TOC links)."""
    s = text.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s, flags=re.UNICODE)
    return s.replace(" ", "-")


class Unsupported(Exception):
    pass


def inline(children):
    """Convert markdown-it inline tokens into nested nodes."""
    out, stack = [], []
    cur = out
    for t in children:
        if t.type == "text":
            if t.content:
                cur.append({"t": "text", "v": t.content})
        elif t.type in ("strong_open", "em_open", "link_open"):
            node = {"t": {"strong_open": "strong", "em_open": "em", "link_open": "link"}[t.type], "c": []}
            if t.type == "link_open":
                node["href"] = t.attrs.get("href")
            cur.append(node)
            stack.append(cur)
            cur = node["c"]
        elif t.type in ("strong_close", "em_close", "link_close"):
            cur = stack.pop()
        elif t.type == "softbreak":
            cur.append({"t": "soft"})
        elif t.type == "hardbreak":
            cur.append({"t": "br"})
        elif t.type == "html_inline":
            if re.fullmatch(r"<br\s*/?>", t.content.strip(), re.I):
                cur.append({"t": "br", "html": True})
            else:
                raise Unsupported(f"inline html {t.content!r}")
        elif t.type == "code_inline":
            cur.append({"t": "code", "v": t.content})
        else:
            raise Unsupported(f"inline token {t.type}")
    if stack:
        raise Unsupported("unbalanced inline tokens")
    # merge adjacent text nodes
    merged = []
    for n in out:
        if merged and n["t"] == "text" and merged[-1]["t"] == "text":
            merged[-1]["v"] += n["v"]
        else:
            merged.append(n)
    return merged


def plain(nodes) -> str:
    s = []
    for n in nodes:
        if n["t"] in ("text", "code"):
            s.append(n["v"])
        elif n["t"] == "soft":
            s.append(" ")
        elif n["t"] == "br":
            s.append("\n")
        else:
            s.append(plain(n["c"]))
    return "".join(s)


def parse(text: str):
    md = MarkdownIt("commonmark", {"html": True}).enable("table")
    toks = md.parse(text)
    pos = 0

    def block_seq(end_types=()):
        nonlocal pos
        blocks = []
        while pos < len(toks):
            t = toks[pos]
            if t.type in end_types:
                return blocks
            if t.type == "heading_open":
                lvl = int(t.tag[1])
                inl = toks[pos + 1]
                blocks.append({"type": "heading", "level": lvl, "lines": t.map, "c": inline(inl.children)})
                pos += 3
            elif t.type == "paragraph_open":
                inl = toks[pos + 1]
                blocks.append({"type": "para", "lines": t.map, "c": inline(inl.children)})
                pos += 3
            elif t.type in ("bullet_list_open", "ordered_list_open"):
                ordered = t.type == "ordered_list_open"
                start = int(t.attrs.get("start", 1)) if ordered else None
                lines = t.map
                close = t.type.replace("open", "close")
                pos += 1
                items = []
                while toks[pos].type != close:
                    it = toks[pos]
                    assert it.type == "list_item_open", it.type
                    pos += 1
                    body = block_seq(("list_item_close",))
                    pos += 1
                    items.append({"lines": it.map, "info": it.info, "blocks": body})
                pos += 1
                b = {"type": "list", "ordered": ordered, "lines": lines, "items": items,
                     "tight": all(True for _ in items)}
                if ordered:
                    b["start"] = start
                blocks.append(b)
            elif t.type == "table_open":
                lines = t.map
                pos += 1
                header, rows, aligns = [], [], []
                section = None
                while toks[pos].type != "table_close":
                    tt = toks[pos]
                    if tt.type == "thead_open":
                        section = header
                    elif tt.type == "tbody_open":
                        section = rows
                    elif tt.type == "tr_open":
                        row = []
                        pos += 1
                        while toks[pos].type != "tr_close":
                            c = toks[pos]
                            if c.type in ("th_open", "td_open"):
                                style = c.attrs.get("style") or ""
                                al = re.search(r"text-align:(\w+)", style)
                                if section is header:
                                    aligns.append(al.group(1) if al else None)
                                row.append(inline(toks[pos + 1].children))
                                pos += 3
                            else:
                                raise Unsupported(f"table token {c.type}")
                        section.append(row)
                    pos += 1
                pos += 1
                blocks.append({"type": "table", "lines": lines, "header": header[0], "rows": rows, "align": aligns})
            elif t.type == "blockquote_open":
                lines = t.map
                pos += 1
                body = block_seq(("blockquote_close",))
                pos += 1
                blocks.append({"type": "quote", "lines": lines, "blocks": body})
            elif t.type == "hr":
                blocks.append({"type": "hr", "lines": t.map})
                pos += 1
            elif t.type == "html_block":
                raise Unsupported(f"html block at line {t.map}: {t.content[:80]!r}")
            elif t.type in ("fence", "code_block"):
                raise Unsupported(f"code block at {t.map}")
            else:
                raise Unsupported(f"block token {t.type} at {t.map}")
        return blocks

    return block_seq()


def main():
    authority = check()
    raw = SRC.read_bytes()
    sha = authority["sha256"]
    text = raw.decode("utf-8")
    pub = text
    applied = []  # text patches belong to immutable manuscript revisions
    blocks = parse(pub)

    # ---- assign stable ids, chapters, anchors --------------------------------
    slugs = {}
    seq = {"heading": 0, "para": 0, "list": 0, "table": 0, "quote": 0, "hr": 0}
    path = []  # heading stack of (level, id)
    headings, tables = [], []

    def walk(bs, top=True, ctx=None):
        for b in bs:
            seq[b["type"]] += 1
            ln = b["lines"][0] + 1
            b["src"] = [b["lines"][0] + 1, b["lines"][1]]  # 1-based inclusive line span
            del b["lines"]
            if b["type"] == "heading":
                title = plain(b["c"])
                s = slugify(title)
                n = slugs.get(s, 0)
                slugs[s] = n + 1
                anchor = s if n == 0 else f"{s}-{n}"
                b["id"] = "h-" + anchor
                b["anchor"] = anchor
                b["title"] = title
                while path and path[-1][0] >= b["level"]:
                    path.pop()
                path.append((b["level"], b["id"], title))
                headings.append({"id": b["id"], "anchor": anchor, "level": b["level"], "title": title,
                                 "line": ln, "parents": [p[1] for p in path[:-1]]})
            elif b["type"] == "table":
                tid = f"T{len(tables)+1:03d}"
                b["id"] = tid
                ncols = len(b["header"])
                cells = [[plain(c) for c in b["header"]]] + [[plain(c) for c in r] for r in b["rows"]]
                tables.append({"id": tid, "src": b["src"], "heading": path[-1][1] if path else None,
                               "heading_title": path[-1][2] if path else None,
                               "context": [p[2] for p in path], "columns": ncols,
                               "rows": len(b["rows"]), "header": cells[0], "align": b["align"],
                               "cells": sum(len(r) for r in cells),
                               "max_cell_chars": max((len(c) for r in cells for c in r), default=0),
                               "col_max_chars": [max(len(r[i]) if i < len(r) else 0 for r in cells) for i in range(ncols)],
                               "col_avg_chars": [round(sum(len(r[i]) if i < len(r) else 0 for r in cells[1:]) / max(1, len(cells) - 1), 1) for i in range(ncols)],
                               "row_lengths_ok": all(len(r) == ncols for r in b["rows"]),
                               "cell_sha256": hashlib.sha256(json.dumps(cells, ensure_ascii=False).encode()).hexdigest()})
                b["context"] = [p[1] for p in path]
            else:
                b["id"] = f"B{ln:05d}"
            if b["type"] == "list":
                for it in b["items"]:
                    it["src"] = [it["lines"][0] + 1, it["lines"][1]]
                    del it["lines"]
                    walk(it["blocks"], False)
            if b["type"] == "quote":
                walk(b["blocks"], False)

    walk(blocks)

    # ---- chapters: split at H2 -----------------------------------------------
    chapters = []
    cur = {"id": "front", "title": None, "blocks": []}
    for b in blocks:
        if b["type"] == "heading" and b["level"] == 2:
            chapters.append(cur)
            cur = {"id": b["id"], "title": b["title"], "blocks": []}
        cur["blocks"].append(b)
    chapters.append(cur)

    out = ROOT / "build"
    out.mkdir(exist_ok=True)
    model = {"source": str(SRC.relative_to(ROOT)), "sha256": sha, "patches_applied": applied, "chapters": chapters}
    (out / "blocks.json").write_text(json.dumps(model, ensure_ascii=False))

    inv = ROOT / "production/inventory"
    inv.mkdir(parents=True, exist_ok=True)
    (inv / "headings.json").write_text(json.dumps(headings, ensure_ascii=False, indent=0))
    (inv / "tables.json").write_text(json.dumps(tables, ensure_ascii=False, indent=0))

    # construct counts
    counts = {}

    def count(bs):
        for b in bs:
            counts[b["type"]] = counts.get(b["type"], 0) + 1
            if b["type"] == "list":
                counts["list_item"] = counts.get("list_item", 0) + len(b["items"])
                for it in b["items"]:
                    count(it["blocks"])
            if b["type"] == "quote":
                count(b["blocks"])
            for key in ("c",):
                if key in b:
                    inl_count(b[key])
            if b["type"] == "table":
                for r in [b["header"]] + b["rows"]:
                    for c in r:
                        inl_count(c)

    def inl_count(nodes):
        for n in nodes:
            k = "inline_" + n["t"]
            counts[k] = counts.get(k, 0) + 1
            if "c" in n:
                inl_count(n["c"])

    count(blocks)
    hl = {}
    for h in headings:
        hl[h["level"]] = hl.get(h["level"], 0) + 1
    summary = {"sha256": sha, "bytes": len(raw), "lines": len(text.split("\n")),
               "words_whitespace": len(text.split()), "headings_by_level": hl, "headings": len(headings),
               "tables": len(tables), "max_table_columns": max(t["columns"] for t in tables),
               "tables_ragged_rows": [t["id"] for t in tables if not t["row_lengths_ok"]],
               "constructs": counts, "chapters": [{"id": c["id"], "title": c["title"], "blocks": len(c["blocks"])} for c in chapters],
               "patches_applied": applied,
               "duplicate_heading_slugs": {k: v for k, v in slugs.items() if v > 1}}
    (inv / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(json.dumps({k: summary[k] for k in ("headings", "headings_by_level", "tables", "max_table_columns", "constructs", "tables_ragged_rows")}, indent=None))


if __name__ == "__main__":
    main()
