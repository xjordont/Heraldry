#!/usr/bin/env python3
"""Generate typst/content.typ from build/blocks.json and run the balancing build loop.

Text is emitted only as Typst string literals (#"..."), so Typst never applies
smart quotes, shorthands or markup interpretation to manuscript characters.
Layout-only transformations (no-break spaces in dice/AP units, soft line breaks
rendered as line breaks, table representations) are recorded in
production/mappings/.
"""
from __future__ import annotations
import argparse, json, re, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tables import classify, cell_plain, COL_W, FULL_W  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
MAP = ROOT / "production/mappings"

DIE_HEADERS = re.compile(r"^(\d*d\d+|d\d+|\d+d\d+ roll|Roll|\d+d\d+)$", re.I)
NOBREAK = [
    re.compile(r"\b\d*d\d+(?: [+−-] (?:APL/\d|\d+))+"),      # 1d6 + 2, 1d8 + APL/2
    re.compile(r"\[\d+ AP\]"),                                # [1 AP]
    re.compile(r"\b\d+ AP\b"),                               # 2 AP
    re.compile(r"\b(?:STR|DEX|INT|SPI) [+−-]?\d+\b"),        # STR +1
    re.compile(r"\bAPL \d+(?:–\d+|\+)?"),                    # APL 1–3
    re.compile(r"\bRound \d+\b"),
]
NBSP = " "


def nobreak(s: str) -> str:
    for rx in NOBREAK:
        s = rx.sub(lambda m: m.group(0).replace(" ", NBSP), s)
    return s


def lit(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


class Emitter:
    def __init__(self, anchors: set[str]):
        self.anchors = anchors
        self.links = []

    def inl(self, nodes, soft_break=True) -> str:
        out = []
        prev = None
        for n in nodes:
            t = n["t"]
            if t == "soft" and prev == "br":
                prev = t
                continue   # "<br>" + source newline is one line break, not two
            prev = t
            if t == "text":
                if n["v"]:
                    out.append("#" + lit(nobreak(n["v"])))
            elif t == "code":
                out.append("#raw(" + lit(n["v"]) + ")")
            elif t == "soft":
                out.append("#linebreak()" if soft_break else "#\" \"")
            elif t == "br":
                out.append("#linebreak()")
            elif t == "strong":
                out.append("#strong[" + self.inl(n["c"], soft_break) + "]")
            elif t == "em":
                out.append("#emph[" + self.inl(n["c"], soft_break) + "]")
            elif t == "link":
                href = n.get("href") or ""
                if href.startswith("#") and href[1:] in self.anchors:
                    self.links.append(href[1:])
                    out.append(f"#link(label({lit('h-' + href[1:])}))[" + self.inl(n["c"], soft_break) + "]")
                else:
                    raise SystemExit(f"Unresolved link {href!r}")
            else:
                raise SystemExit(f"unknown inline {t}")
        return "".join(out)


def is_flavour(b) -> bool:
    if b["type"] != "para":
        return False
    nodes = [n for n in b["c"] if not (n["t"] == "text" and not n["v"].strip())]
    return bool(nodes) and all(n["t"] == "em" for n in nodes) and not first_text(b).startswith("Example")


def first_text(b) -> str:
    nodes = b.get("c", [])
    s = ""
    def walk(ns):
        nonlocal s
        for n in ns:
            if len(s) > 40:
                return
            if n["t"] == "text":
                s += n["v"]
            elif "c" in n:
                walk(n["c"])
    walk(nodes)
    return s.strip()


def inject(s: str, mark: str) -> str:
    """Put a zero-size marker INSIDE a rendered block so that no stray inline content
    sits between a heading and the block it must keep with."""
    for f in ("#example[", "#flavour[", "#note-box[", "#runin["):
        if s.startswith(f):
            return f + mark + s[len(f):]
    for f in ("#htable(", "#statstrip(", "#statcard(", "#cards(", "#figure-block("):
        if s.startswith(f):
            return f + f"pre: [{mark}], " + s[len(f):]
    if s.startswith("#hr-ornament()"):
        return f"#hr-ornament(pre: [{mark}])" + s[len("#hr-ornament()"):]
    if s.startswith("#list([") or s.startswith("#enum("):
        i = s.index("[")
        return s[:i + 1] + mark + s[i + 1:]
    return mark + s


def is_caption(b) -> bool:
    """A paragraph consisting solely of one short bold run (e.g. **APL 1–2 (d10)**)."""
    if b["type"] != "para":
        return False
    nodes = [n for n in b["c"] if not (n["t"] == "text" and not n["v"].strip())]
    return len(nodes) == 1 and nodes[0]["t"] == "strong" and len(first_text(b)) <= 60


def is_example(b) -> bool:
    if b["type"] != "para" or not b["c"]:
        return False
    ft = first_text(b)
    first = next((n for n in b["c"] if not (n["t"] == "text" and not n["v"])), None)
    if first and first["t"] == "em" and ft.startswith("Example"):
        return True
    if first and first["t"] == "strong" and re.match(r"^[\w ,'-]*Example:", ft):
        return True
    return False


class Book:
    def __init__(self, model, balance):
        self.model = model
        self.balance = balance  # seg index -> tail start piece
        anchors = set()
        for ch in model["chapters"]:
            self._anchors(ch["blocks"], anchors)
        self.em = Emitter(anchors)
        self.seg_count = 0
        self.seg_sigs = {}
        self.placed_figs = set()
        self.piece_heads = {}
        self.table_map = []
        self.block_map = []   # (block id, src span, representation, segment)
        self.out = []
        self.fig_slots = json.loads((ROOT / "figures/placements.json").read_text()) if (ROOT / "figures/placements.json").exists() else {}
        self.index_targets = json.loads((BUILD / "index_targets.json").read_text()) if (BUILD / "index_targets.json").exists() else {}
        self.tclass = self._classify_all()

    def _classify_all(self):
        """Classify every table, then unify families (same header signature within the
        same H3 section) so that sibling tables share one representation and widths."""
        from tables import measure_table, allocate, est_height
        tabs = []
        def walk(bs, sec):
            for b in bs:
                if b["type"] == "heading" and b["level"] <= 3:
                    sec = b["id"]
                if b["type"] == "table":
                    tabs.append((b, sec))
                for it in b.get("items", []):
                    walk(it["blocks"], sec)
                walk(b.get("blocks", []), sec)
            return sec
        sec = None
        for ch in self.model["chapters"]:
            sec = walk(ch["blocks"], sec)
        res, fam = {}, {}
        for b, sec in tabs:
            c = classify(b, None)
            res[b["id"]] = c
            fam.setdefault((sec, tuple(c["header"])), []).append(b)
        self.families = {}
        for key, members in fam.items():
            if len(members) < 2:
                continue
            cs = [res[m["id"]] for m in members]
            for m in members:
                self.families[m["id"]] = members[0]["id"]
            if any(c["rep"] in ("cards", "stat", "statcard") for c in cs) or len({c["rep"] for c in cs}) > 1:
                continue
            scope = "full" if any(c["scope"] == "full" for c in cs) else "column"
            mins = [max(x) for x in zip(*[measure_table(m)[0] for m in members])]
            maxs = [max(x) for x in zip(*[measure_table(m)[1] for m in members])]
            w, _ = allocate(mins, maxs, FULL_W if scope == "full" else COL_W)
            if w is None:
                continue
            for m, c in zip(members, cs):
                c["scope"] = scope
                c["widths"] = [round(x, 2) for x in w]
                c["max_pt"] = [round(x, 1) for x in maxs]
                c["family"] = members[0]["id"]
        return res

    def _anchors(self, bs, acc):
        for b in bs:
            if b["type"] == "heading":
                acc.add(b["anchor"])
            for it in b.get("items", []):
                self._anchors(it["blocks"], acc)
            self._anchors(b.get("blocks", []), acc)

    # ------------------------------------------------------------- blocks
    def heading(self, b):
        lvl = b["level"] - 1
        body = self.em.inl(b["c"])
        bm = "true" if lvl <= 3 else "false"
        ol = "true" if lvl <= 2 else "false"
        return f"#heading(level: {lvl}, outlined: {ol}, bookmarked: {bm})[{body}] #label({lit(b['id'])})"

    def para(self, b, role=None):
        body = self.em.inl(b["c"])
        tag = self.tags(b["id"])
        if role == "example" or is_example(b):
            return f"#example[{tag}{body}]"
        if is_flavour(b):
            return f"#flavour[{tag}{body}]"
        if is_caption(b):
            return f"#runin[{tag}{body}]\n"
        return f"{tag}{body}\n\n"

    def block_inline(self, b):
        """Render a block inside a list item / quote."""
        t = b["type"]
        if t == "para":
            return self.tags(b["id"]) + self.em.inl(b["c"])
        if t == "list":
            return self.lst(b)
        if t == "table":
            return self.table(b, force_column=True)
        if t == "quote":
            return self.quote(b)
        if t == "heading":
            raise SystemExit(f"heading inside container {b['id']}")
        if t == "hr":
            return "#hr-ornament()"
        raise SystemExit(t)

    def tags(self, bid):
        if bid.startswith("h-"):
            return ""   # headings are index targets through their own label (see make_index heads)
        return "".join(f"#ixm({lit(k)})" for k in self.index_targets.get(bid, []))

    def lst(self, b):
        items = []
        for it in b["items"]:
            parts = [self.block_inline(x) for x in it["blocks"]]
            items.append("[" + "#parbreak()".join(parts) + "]")
        if b["ordered"]:
            return f"#enum(start: {b['start']}, " + ", ".join(items) + ")\n"
        return "#list(" + ", ".join(items) + ")\n"

    def quote(self, b):
        inner = "#parbreak()".join(self.block_inline(x) for x in b["blocks"])
        return f"#note-box[{inner}]"

    def table(self, b, force_column=False):
        c = self.tclass[b["id"]]
        hdr = [self.em.inl(h) for h in b["header"]]
        rows = [[self.em.inl(cell) for cell in r] for r in b["rows"]]
        rep = c["rep"]
        mapping = {"id": b["id"], "src": b["src"], "rep": rep, "scope": c["scope"], "columns": c["columns"],
                   "rows": c["rows"], "header": c["header"]}
        if rep == "stat" or (c["header"][:6] == ["HP", "AV", "SPD", "LVL", "CV", "Sz"]):
            if len(b["rows"]) == 1 and c["scope"] == "column" and rep == "stat":
                mapping["rep"] = "statstrip"
                s = f"#statstrip({lit(b['id'])}, ({', '.join('[' + h + ']' for h in hdr)},), ({', '.join('[' + v + ']' for v in rows[0])},))"
            elif len(b["rows"]) == 1:
                mapping["rep"] = "statcard"
                mapping["scope"] = "column"
                c["scope"] = "column"
                mapping["field_map"] = {h: f"row1.{h}" for h in c["header"]}
                s = f"#statcard({lit(b['id'])}, ({', '.join('[' + h + ']' for h in hdr)},), ({', '.join('[' + v + ']' for v in rows[0])},))"
            else:
                s = self._plain_table(b, c, hdr, rows)
        elif rep == "cards":
            s = self._cards(b, c, hdr, rows, mapping)
        else:
            s = self._plain_table(b, c, hdr, rows)
        mapping["scope"] = c["scope"]
        if "family" in c:
            mapping["family"] = c["family"]
        self.table_map.append(mapping)
        return s, c["scope"]

    def _aligns(self, b, c):
        al = []
        for i, a in enumerate(b["align"]):
            col = [cell_plain(r[i]).strip() for r in b["rows"]]
            if a in ("right", "center"):
                al.append("center" if DIE_HEADERS.match(c["header"][i]) else a)
            elif DIE_HEADERS.match(c["header"][i]) or all(re.fullmatch(r"[\d–\-+×\"c/ .%]{1,7}", x or "-") for x in col):
                al.append("center")
            else:
                al.append("left")
        return al

    def _plain_table(self, b, c, hdr, rows):
        total = COL_W if c["scope"] == "column" else FULL_W
        w = list(c["widths"])
        slack = total - sum(w)
        if slack > 0:
            # give spare width to the column with the most text
            i = max(range(len(w)), key=lambda k: c["max_pt"][k])
            w[i] += slack
        aligns = self._aligns(b, c)
        hs = ", ".join("[" + h + "]" for h in hdr)
        rs = ", ".join("(" + ", ".join("[" + v + "]" for v in r) + ",)" for r in rows)
        ws = ", ".join(f"{x:.2f}" for x in w)
        als = ", ".join(aligns)
        return f"#htable({lit(b['id'])}, ({ws},), ({als},), ({hs},), ({rs},))"

    def _cards(self, b, c, hdr, rows, mapping):
        heads = c["header"]
        desc = set(c["desc_cols"])
        die = DIE_HEADERS.match(heads[0]) is not None
        name_col = 1 if die else 0
        entries = []
        fmap = {}
        for r in rows:
            title_parts = []
            if die:
                title_parts.append(f"#text(weight: 700, fill: ink2)[{r[0]}]#h(6pt)")
            title_parts.append(f"#strong[{r[name_col]}]")
            fields = [f"([{hdr[i]}], [{r[i]}])" for i in range(len(heads)) if i not in desc and i != name_col and not (die and i == 0)]
            descs = [f"([{hdr[i]}:], [{r[i]}])" for i in sorted(desc)]
            entries.append(f"(title: [{''.join(title_parts)}], fields: ({', '.join(fields)}{',' if fields else ''}), desc: ({', '.join(descs)}{',' if descs else ''}))")
        for i, h in enumerate(heads):
            fmap[h] = "entry.title.roll" if (die and i == 0) else "entry.title.name" if i == name_col else ("entry.desc" if i in desc else "entry.field")
        mapping["field_map"] = fmap
        return f"#cards({lit(b['id'])}, ({', '.join(entries)},))"

    # ------------------------------------------------------------- chapters
    def emit(self):
        o = self.out
        o.append('#import "heraldry.typ": *\n#import "frontmatter.typ": *\n#show: book\n')
        chapters = self.model["chapters"]
        fr = chapters[0]["blocks"]
        assert fr[0]["type"] == "heading" and fr[0]["level"] == 1
        t1, _, t2 = fr[0]["title"].partition(": ")
        o.append(f"#frontmatter(title: ({lit(t1)}, {lit(t2)}), subtitle: [{self.em.inl(fr[1]['c'])}], version: [{self.em.inl(fr[2]['c'])}])\n")
        for ch in chapters:
            if ch["id"] == "front":
                self.front = ch
                for b in ch["blocks"]:
                    self.block_map.append((b["id"], b["src"], "front-matter-title-page", None))
                continue
            if ch["id"] == "h-table-of-contents":
                for b in ch["blocks"]:
                    self.block_map.append((b["id"], b["src"], "replaced-by-generated-toc", None))
                continue
            self.chapter(ch)
        o.append("#backmatter()\n#hpos-summary()\n")
        want = {f["id"] for v in self.fig_slots.values() for f in v}
        if want - self.placed_figs:
            raise SystemExit(f"figures not placed (unknown insert_after ids): {sorted(want - self.placed_figs)}")
        return "".join(o)

    def chapter(self, ch):
        blocks = ch["blocks"]
        h = blocks[0]
        title = h["title"]
        m = re.match(r"^((?:Appendix [A-Z]\.)|(?:\d+\.))\s+(.*)$", title)
        num, rest = (m.group(1), m.group(2)) if m else (None, title)
        # Title must be rendered from the source inline nodes: split on the first text node.
        lead = None
        i = 1
        if len(blocks) > 1 and is_flavour(blocks[1]):
            lead = self.em.inl(blocks[1]["c"])
            self.block_map.append((blocks[1]["id"], blocks[1]["src"], "chapter-lead", None))
            i = 2
        first = ch is self.model["chapters"][2] if len(self.model["chapters"]) > 2 else False
        if num and num.startswith("1.") and title.startswith("1. "):
            self.out.append("#mainmatter()\n#set page(numbering: \"1\")\n#counter(page).update(1)\n")
        self.block_map.append((h["id"], h["src"], "chapter-opener", None))
        numlit = f"[#{lit(num)}]" if num else "none"
        art = "none"
        if num and num.rstrip(".").isdigit():
            f = ROOT / f"assets/art/incoming/ART-CH{int(num.rstrip('.')):02d}-001.png"
            if f.exists():
                art = lit("../" + str(f.relative_to(ROOT)))
        self.out.append(f"#chapter-opener({numlit}, [#{lit(rest)}], {lit(h['id'])}, lead: {('[' + lead + ']') if lead else 'none'}, art: {art})\n")
        self.out.append(self.tags(h["id"]) + "\n")
        # group remaining blocks into segments
        cur = []
        rest_blocks = blocks[i:]
        for k, b in enumerate(rest_blocks):
            nxt = rest_blocks[k + 1] if k + 1 < len(rest_blocks) else None
            if b["type"] == "hr" and (nxt is None):
                self.block_map.append((b["id"], b["src"], "hr-absorbed-by-chapter-break", None))
                continue
            if b["type"] == "table":
                s, scope = self.table(b)
                if scope == "full":
                    # carry immediately preceding heading(s) with the full-width table
                    carry = []
                    while cur and (cur[-1][0]["type"] == "heading" or is_caption(cur[-1][0])):
                        carry.insert(0, cur.pop())
                    self.flush(cur)
                    cur = []
                    body = "".join(x[1] for x in carry) + s
                    body = body.replace("#pm(", "#pmx(")
                    for x in carry:
                        self.block_map.append((x[0]["id"], x[0]["src"], "full-width-caption", None))
                    self.block_map.append((b["id"], b["src"], "table-full", None))
                    self.out.append(f"#full[{body}]\n")
                    continue
                cur.append((b, s + "\n"))
                continue
            cur.append((b, self.render(b)))
            for fig in self.figs_for(b):
                if fig.get("scope") == "full":
                    self.flush(cur)
                    cur = []
                    self.block_map.append((fig["id"], b["src"], "figure-full", None))
                    self.out.append(f"#full[{self.figure(fig, full=True)}]\n")
                else:
                    cur.append(({"type": "figure", "id": fig["id"], "src": b["src"]}, self.figure(fig)))
        self.flush(cur)

    def figs_for(self, b):
        ids = []
        def walk(x):
            ids.append(x["id"])
            for it in x.get("items", []):
                for y in it["blocks"]:
                    walk(y)
            for y in x.get("blocks", []):
                walk(y)
        walk(b)
        out = []
        for i in dict.fromkeys(ids):   # a list and its first item paragraph can share an id
            out.extend(self.fig_slots.get(i, []))
            self.placed_figs.update(f["id"] for f in self.fig_slots.get(i, []))
        return out

    def figure(self, fig, full=False):
        w = fig.get("width", "100%")
        cap = fig["caption"]
        return f"#figure-block({lit(fig['id'])}, {lit('../figures/out/' + fig['id'] + '.svg')}, [#{lit(cap)}], width: {w})\n"

    def render(self, b):
        t = b["type"]
        if t == "heading":
            return self.heading(b) + "\n"
        if t == "para":
            return self.para(b)
        if t == "list":
            return self.lst(b)
        if t == "quote":
            return self.quote(b) + "\n"
        if t == "hr":
            return "#hr-ornament()\n"
        raise SystemExit(t)

    def flush(self, pieces):
        if not pieces:
            return
        sid = self.seg_count
        self.seg_count += 1
        sig = f"{pieces[0][0]['id']}:{len(pieces)}"
        self.seg_sigs[str(sid)] = sig
        entry = self.balance.get(str(sid))
        tail = entry[1] if entry and entry[0] == sig and len(pieces) - entry[1] <= 60 else None
        parts = []
        for j, (b, s) in enumerate(pieces):
            self.block_map.append((b["id"], b["src"], "column", sid))
            if b["type"] == "heading":
                self.piece_heads[f"{sid}:{j}"] = b["id"]
                parts.append(s)
            else:
                parts.append(inject(s, f"#pm({sid}, {j}, \"s\")"))
        end = f"#place(pm({sid}, {len(pieces)}, \"e\"))"
        if tail is None or tail >= len(pieces):
            self.out.append("#seg[" + "".join(parts) + end + "]\n")
        else:
            if tail > 0:
                self.out.append("#seg[" + "".join(parts[:tail]) + "]\n")
            tp = []
            carry = ""
            for j in range(tail, len(parts)):
                if f"{sid}:{j}" in self.piece_heads and j < len(parts) - 1:
                    carry += parts[j]      # keep headings in the same balancing unit as what follows
                    continue
                tp.append(carry + parts[j])
                carry = ""
            if carry:
                tp.append(carry)
            tp[-1] = tp[-1] + end
            self.out.append("#bal(" + ", ".join("[" + x + "]" for x in tp) + ")\n")


def compile_book(variant="cream", out=None, query=True, edition="print"):
    import subprocess
    out = out or BUILD / f"book-{variant}.pdf"
    qf = BUILD / "query.json"
    args = [sys.executable, str(ROOT / "tools/typst_run.py"), str(out), variant, edition] + ([str(qf)] if query else [])
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-3000:])
    dt = float(r.stdout.strip().splitlines()[-1])
    if query:
        q = json.loads(qf.read_text())
        return out, dt, (q["pm"], q["hpos"])
    return out, dt, None


def typst_query(sel):
    import typst
    return json.loads(typst.query(str(ROOT / "typst/content.typ"), sel, field="value", root=str(ROOT),
                                  font_paths=[str(ROOT / "fonts/static")], ignore_system_fonts=True,
                                  sys_inputs={"substrate": "cream", "edition": "print"}))


TOP_Y = 0.65 * 72
BODY_BOTTOM = 792 - 0.7 * 72


def compute_balance(pm, prev, sigs, heads=None, hpos=None):
    """Decide, per segment, from which piece the tail on its last page should be balanced."""
    segs = {}
    for m in pm:
        segs.setdefault(m["seg"], []).append(m)
    hp = {h["id"]: h for h in (hpos or [])}
    for key, hid in (heads or {}).items():
        sid, j = map(int, key.split(":"))
        if hid in hp:
            h = hp[hid]
            segs.setdefault(sid, []).append({"seg": sid, "piece": j, "edge": "s", "page": h["page"], "y": h["y"], "x": h["x"]})
    res = {}
    for sid, ms in segs.items():
        starts = sorted([m for m in ms if m["edge"] == "s"], key=lambda m: m["piece"])
        end = [m for m in ms if m["edge"] == "e"][0]
        L = end["page"]
        pt = prev.get(str(sid))
        pt = pt[1] if pt and pt[0] == sigs.get(str(sid)) else None
        if pt is not None and pt < len(starts) and starts[pt]["page"] == L:
            res[str(sid)] = [sigs[str(sid)], pt]   # hysteresis: previous tail still sits on the last page
            continue
        on_last = [m for m in starts if m["page"] == L]
        if not on_last:
            continue  # only the tail of a straddling piece is on the last page; leave natural
        t = on_last[0]["piece"]
        if t > 0:
            prevp = starts[t - 1]
            first = on_last[0]
            at_top = abs(first["y"] - TOP_Y) < 20 and first["x"] < 300
            if not at_top:
                # previous piece straddles onto the last page; include it if little is left on the previous page
                if BODY_BOTTOM - prevp["y"] < 160 or prevp["page"] == L:
                    t = t - 1
                else:
                    continue
        res[str(sid)] = [sigs[str(sid)], t]
    # never leave a heading as the last piece before the balanced tail
    for k, (sig, t) in list(res.items()):
        while t > 0 and f"{k}:{t-1}" in (heads or {}):
            t -= 1
        res[k] = [sig, t]
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="cream")
    ap.add_argument("--passes", type=int, default=5)
    ap.add_argument("--no-balance", action="store_true")
    ap.add_argument("--variants-only", action="store_true", help="compile white + digital from the current content.typ")
    a = ap.parse_args()
    if a.variants_only:
        for v, ed, name in (("white", "print", "book-white.pdf"), ("cream", "digital", "book-digital.pdf")):
            out, dt, _ = compile_book(v, BUILD / name, query=False, edition=ed)
            print(f"{name}: {dt:.1f}s")
        return
    model = json.loads((BUILD / "blocks.json").read_text())
    balance = {}
    bal_file = BUILD / "balance.json"
    if bal_file.exists() and not a.no_balance:
        balance = json.loads(bal_file.read_text())
    flips = {}
    for p in range(a.passes):
        book = Book(model, balance)
        (ROOT / "typst/content.typ").write_text(book.emit())
        out, dt, (pm, hpos) = compile_book(a.variant)
        new = compute_balance(pm, balance, book.seg_sigs, book.piece_heads, hpos) if not a.no_balance else {}
        print(f"pass {p+1}: {dt:.1f}s, segments={book.seg_count}, balanced={len(new)}, changed={sum(1 for k in set(new)|set(balance) if new.get(k)!=balance.get(k))}")
        if new == balance or a.no_balance:
            break
        # damping: a segment that has already changed twice keeps its current value
        for k in set(new) | set(balance):
            if new.get(k) != balance.get(k):
                flips[k] = flips.get(k, 0) + 1
                if flips[k] > 2:
                    if k in balance:
                        new[k] = balance[k]
                    else:
                        new.pop(k, None)
        for k, (sig, t) in list(new.items()):
            while t > 0 and f"{k}:{t-1}" in book.piece_heads:
                t -= 1
            new[k] = [sig, t]
        if p == a.passes - 1 or new == balance:
            break   # keep balance.json consistent with the PDF just compiled
        balance = new
        bal_file.write_text(json.dumps(balance))
    MAP.mkdir(parents=True, exist_ok=True)
    (MAP / "tables.json").write_text(json.dumps(book.table_map, ensure_ascii=False, indent=0))
    (MAP / "blocks.json").write_text(json.dumps(book.block_map, ensure_ascii=False))
    print("links:", len(book.em.links), "->", out)


if __name__ == "__main__":
    main()
