#!/usr/bin/env python3
"""Generate typst/content.typ from build/blocks.json and run the balancing build loop.

Text is emitted only as Typst string literals (#"..."), so Typst never applies
smart quotes, shorthands or markup interpretation to manuscript characters.
Layout-only transformations (no-break spaces in dice/AP units, soft line breaks
rendered as line breaks, table representations) are recorded in
production/mappings/.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tables import classify, cell_plain, COL_W, FULL_W  # noqa: E402
from layout_profile import (MARGIN_TOP_PT, MARGIN_BOTTOM_PT, PAGE_HEIGHT_PT, PAGE_WIDTH_PT,
    BODY_HEIGHT_PT, profile_dict)

ROOT = Path(__file__).resolve().parents[1]
ART_SEL = ROOT / "production/art/SELECTIONS.json"
ART_STYLE = ROOT / "config/art_style.json"


def load_spot_art():
    """Selected generated ink art keyed by catalog flavour block / asset id: (relpath, width_in).
    Width = family print width, never above native 300 ppi."""
    if not ART_SEL.exists():
        return {}, {}
    style = json.loads(ART_STYLE.read_text())
    fams = style["families"]
    overrides = {k: v for k, v in style.get("art_width_overrides", {}).items() if not k.startswith("_")}
    cat = {e["id"]: e for e in json.loads((ROOT / "production/art/SPOT_CATALOG.json").read_text())["entries"]}
    by_block, by_id = {}, {}
    for aid, s in json.loads(ART_SEL.read_text()).items():
        f = ROOT / s["ink"]["path"]
        if aid not in cat or s.get("status") not in {"anchor-approved", "auto-selected", "approved"} or not f.exists() or s["spec_sha256"] != cat[aid]["spec_sha256"]:
            continue
        from PIL import Image
        with Image.open(f) as image:
            wpx = image.size[0]
        w = min(fams[s["family"]]["print_w_in"], wpx / 300, overrides.get(aid, 99))
        rec = ("../" + s["ink"]["path"], w)
        by_id[aid] = rec
        if cat[aid].get("flavour_block"):
            by_block[cat[aid]["flavour_block"]] = rec
    return by_block, by_id


FLOAT_FIGS = set(json.loads((ROOT / "config/design_tokens.json").read_text()).get("layout", {}).get("float_figures", []))
TABLE_SCOPE_OVERRIDES = json.loads((ROOT / "config/design_tokens.json").read_text()).get('layout', {}).get('table_scope_overrides', {})
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


def table_content_sha256(table):
    values = [[cell_plain(cell) for cell in table['header']],
              [[cell_plain(cell) for cell in row] for row in table['rows']]]
    return hashlib.sha256(json.dumps(values, ensure_ascii=False, separators=(',', ':')).encode('utf-8')).hexdigest()


def apply_table_scope_override(table, classification, policy):
    """Apply a measured width decision only to the exact reviewed cell contents."""
    from tables import allocate, measure_table
    if policy.get('scope') != 'full' or classification.get('rep') != 'table':
        raise ValueError('Unsupported table scope override: ' + table['id'])
    if policy.get('content_sha256') != table_content_sha256(table):
        raise ValueError('Table content changed; review its width override: ' + table['id'])
    mins, maxs, _ = measure_table(table)
    widths, _ = allocate(mins, maxs, FULL_W)
    if widths is None:
        raise ValueError('Reviewed table no longer fits full width: ' + table['id'])
    return classification | {'scope':'full', 'widths':[round(x,2) for x in widths],
                              'max_pt':[round(x,1) for x in maxs], 'scope_reason':policy['reason']}


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


RIGID = ("#htable(", "#statstrip(", "#statcard(", "#cards(", "#keepcol[", "#keepfigure[", "#figure-block(", "#list(", "#enum(",
         "#list-fragment(", "#example[", "#keep[", "#runin[", "#note-box[", "#gloss[", "#flavour[")


def is_rigid(s: str) -> bool:
    """True if a piece contains anything that cannot flow line-by-line between columns."""
    return any(r in s for r in RIGID)


def inject(s: str, mark: str) -> str:
    """Put a zero-size marker INSIDE a rendered block so that no stray inline content
    sits between a heading and the block it must keep with."""
    for f in ("#example[", "#flavour[", "#note-box[", "#runin[", "#keep[", "#gloss[", "#keepcol[", "#keepfigure["):
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


def first_text_full(b) -> str:
    from parse_source import plain
    return plain(b.get("c", []))


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
        # Scope continuation events to chapters containing actual numbered scenarios.
        # Scanning every heading body in every running header triples compile time.
        def headings(blocks):
            for block in blocks:
                if block['type'] == 'heading':
                    yield block
                for item in block.get('items', []):
                    yield from headings(item['blocks'])
                yield from headings(block.get('blocks', []))
        self.scenario_scope_ids = set()
        for chapter in model['chapters']:
            chapter_heads = list(headings(chapter['blocks']))
            if any(re.match(r'^Scenario \d+:', h['title']) for h in chapter_heads):
                self.scenario_scope_ids.update(h['id'] for h in chapter_heads)
        self.balance = balance  # seg index -> tail start piece
        anchors = set()
        for ch in model["chapters"]:
            self._anchors(ch["blocks"], anchors)
        self.em = Emitter(anchors)
        self.seg_count = 0
        self.seg_sigs = {}
        self.placed_figs = set()
        self.in_glossary = False
        self.measure_requests = []
        self.unit_log = []
        self.logged_units = set()
        self.extra_units = {}
        self.requested_units = set()
        self.table_titles = {}
        mf = BUILD / "unit_measure.json"
        self.measures = json.loads(mf.read_text()) if mf.exists() else {}
        self.piece_heads = {}
        self.table_map = []
        self.block_map = []   # (block id, src span, representation, segment)
        self.out = []
        self.fig_slots = json.loads((ROOT / "figures/placements.json").read_text()) if (ROOT / "figures/placements.json").exists() else {}
        self.index_targets = json.loads((BUILD / "index_targets.json").read_text()) if (BUILD / "index_targets.json").exists() else {}
        self.tclass = self._classify_all()
        self.spot_art, self.art_ids = load_spot_art()

    def _classify_all(self):
        """Classify every table, then unify families (same header signature within the
        same H3 section) so that sibling tables share one representation and widths."""
        from tables import measure_table, allocate
        tabs = []
        def walk(bs, sec):
            for b in bs:
                if b["type"] == "heading" and b["level"] <= 3:
                    sec = b["id"]
                if b["type"] == "heading":
                    self._current_table_title = b["title"]
                if b["type"] == "table":
                    tabs.append((b, sec))
                    self.table_titles[b["id"]] = getattr(self, '_current_table_title', b["id"])
                for it in b.get("items", []):
                    walk(it["blocks"], sec)
                walk(b.get("blocks", []), sec)
            return sec
        sec = None
        for ch in self.model["chapters"]:
            sec = walk(ch["blocks"], sec)
        res, fam = {}, {}
        unknown_overrides = set(TABLE_SCOPE_OVERRIDES) - {b['id'] for b, _ in tabs}
        if unknown_overrides:
            raise ValueError('Unknown reviewed table width IDs: ' + ', '.join(sorted(unknown_overrides)))
        for b, sec in tabs:
            c = classify(b, None)
            if b['id'] in TABLE_SCOPE_OVERRIDES:
                c = apply_table_scope_override(b, c, TABLE_SCOPE_OVERRIDES[b['id']])
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

    def heading(self, b):
        lvl = b["level"] - 1
        body = self.em.inl(b["c"])
        bm = "true" if lvl <= 3 else "false"
        ol = "true" if lvl <= 2 else "false"
        rendered = f"#heading(level: {lvl}, outlined: {ol}, bookmarked: {bm})[{body}] #label({lit(b['id'])})"
        if b['id'] in getattr(self, 'scenario_scope_ids', set()):
            rendered = f"#heading-scope({lvl}, {lit(b['title'])}, {lit(b['id'])})[{rendered}]"
        return rendered

    def para(self, b, role=None):
        body = self.em.inl(b["c"])
        tag = self.tags(b["id"])
        if role == "example" or is_example(b):
            return f"#example[{tag}{body}]"
        if is_flavour(b):
            art = self.spot_art.get(b["id"])
            pre = f"#spotart({lit(art[0])}, {art[1]:.3f}in)" if art else ""
            if role == 'section-lead':
                return f"{pre}#section-lead[{tag}{body}]"
            return f"{pre}#flavour[{tag}{body}]"
        if is_caption(b):
            return f"#runin[{tag}{body}]\n"
        if self.in_glossary and b["c"] and b["c"][0]["t"] == "strong" and first_text({"c": b["c"][0]["c"]}).rstrip().endswith(":"):
            return f"#gloss[{tag}{body}]\n"
        return f"{tag}{body}\n\n"

    def block_inline(self, b):
        t = b["type"]
        if t == "para":
            return self.tags(b["id"]) + self.em.inl(b["c"])
        if t == "list":
            return self.contained(b, self.lst(b))
        if t == "table":
            return self.contained(b, self.table(b, force_column=True)[0])
        if t == "quote":
            return self.contained(b, self.quote(b))
        if t == "heading":
            raise SystemExit(f"heading inside container {b['id']}")
        if t == "hr":
            return "#hr-ornament()"
        raise SystemExit(t)

    def contained(self, b, text):
        """Track a nested or joined source unit instead of losing it from the audit."""
        self.extra_units[b['id']] = dict(b=b, s=text, kind='c', id=b['id'], typ=b['type'])
        self.log_unit(self.extra_units[b['id']], 'contained')
        return f"#umark({lit(b['id'])}, \"s\"){text}#umark({lit(b['id'])}, \"e\")"

    def log_unit(self, x, mode):
        if x['id'] not in self.logged_units:
            self.logged_units.add(x['id'])
            self.unit_log.append({'id': x['id'], 'kind': 'section' if 'head' in x else x['typ'],
                                  'class': mode, **self.measures.get(x['id'], {})})

    def tags(self, bid):
        if bid.startswith("h-"):
            return ""
        return "".join(f"#ixm({lit(k)})" for k in self.index_targets.get(bid, []))

    def lst(self, b):
        items = []
        for it in b["items"]:
            parts = [self.block_inline(x) for x in it["blocks"]]
            items.append("[" + "#parbreak()".join(parts) + "]")
        if b["ordered"]:
            return f"#enum(start: {b['start']}, " + ", ".join(items) + ")\n"
        return "#list(" + ", ".join(items) + ")\n"

    def list_fragments(self, block):
        """Offer complete source items as legal two-column split points."""
        for index, item in enumerate(block['items']):
            body = '#parbreak()'.join(self.block_inline(child) for child in item['blocks'])
            number = str(block['start'] + index) if block['ordered'] else 'none'
            yield f'#list-fragment(number: {number})[{body}]'

    def quote(self, b):
        inner = "#parbreak()".join(self.block_inline(x) for x in b["blocks"])
        return f"#note-box[{inner}]"

    def table(self, b, force_column=False, initial_title=True):
        c = self.tclass[b["id"]]
        hdr = [self.em.inl(h) for h in b["header"]]
        rows = [[self.em.inl(cell) for cell in r] for r in b["rows"]]
        rep = c["rep"]
        mapping = {"id": b["id"], "src": b["src"], "rep": rep, "scope": c["scope"], "columns": c["columns"],
                   "rows": c["rows"], "header": c["header"]}
        if c.get('scope_reason'):
            mapping['scope_reason'] = c['scope_reason']
        if rep == "stat" or (c["header"][:6] == ["HP", "AV", "SPD", "LVL", "CV", "Sz"]):
            short = all(len(cell_plain(v)) <= 12 for v in b["rows"][0]) if b["rows"] else False
            if len(b["rows"]) == 1 and c["scope"] == "column" and rep == "stat" and short:
                mapping["rep"] = "statstrip"
                s = f"#statstrip({lit(b['id'])}, ({', '.join('[' + h + ']' for h in hdr)},), ({', '.join('[' + v + ']' for v in rows[0])},))"
            elif len(b["rows"]) == 1:
                mapping["rep"] = "statcard"
                mapping["scope"] = "column"
                c["scope"] = "column"
                mapping["field_map"] = {h: f"row1.{h}" for h in c["header"]}
                s = f"#statcard({lit(b['id'])}, ({', '.join('[' + h + ']' for h in hdr)},), ({', '.join('[' + v + ']' for v in rows[0])},))"
            else:
                s = self._plain_table(b, c, hdr, rows, initial_title=initial_title)
        elif rep == "cards":
            s = self._cards(b, c, hdr, rows, mapping)
        else:
            s = self._plain_table(b, c, hdr, rows, initial_title=initial_title)
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

    def _plain_table(self, b, c, hdr, rows, initial_title=True):
        total = COL_W if c["scope"] == "column" else FULL_W
        w = list(c["widths"])
        slack = total - sum(w)
        if slack > 0:
            i = max(range(len(w)), key=lambda k: c["max_pt"][k])
            w[i] += slack
        aligns = self._aligns(b, c)
        hs = ", ".join("[" + h + "]" for h in hdr)
        rs = ", ".join("(" + ", ".join("[" + v + "]" for v in r) + ",)" for r in rows)
        ws = ", ".join(f"{x:.2f}" for x in w)
        als = ", ".join(aligns)
        return f"#htable({lit(b['id'])}, ({ws},), ({als},), ({hs},), ({rs},), title: [#{lit(self.table_titles.get(b['id'], b['id']))}], initial-title: {str(initial_title).lower()})"

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
        return f"#cards({lit(b['id'])}, ({', '.join(entries)},), title-label: [#{lit(self.table_titles.get(b['id'], b['id']))}])"

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
        lead = None
        i = 1
        if len(blocks) > 1 and is_flavour(blocks[1]):
            lead = self.em.inl(blocks[1]["c"])
            self.block_map.append((blocks[1]["id"], blocks[1]["src"], "chapter-lead", None))
            i = 2
        if num and num.startswith("1.") and title.startswith("1. "):
            self.out.append("#mainmatter()\n#set page(numbering: \"1\")\n#counter(page).update(1)\n")
        self.block_map.append((h["id"], h["src"], "chapter-opener", None))
        numlit = f"[#{lit(num)}]" if num else "none"
        art = "none"
        if num and num.rstrip(".").isdigit():
            gen = self.art_ids.get(f"ART-CH{int(num.rstrip('.')):02d}-002")
            f = ROOT / gen[0][3:] if gen else ROOT / f"assets/art/incoming/ART-CH{int(num.rstrip('.')):02d}-001.png"
            if gen:
                from PIL import Image
                wpx, hpx = Image.open(f).size
                w = gen[1]
                art = f"({lit(gen[0])}, {w:.3f}in, {w * hpx / wpx:.3f}in)"
            elif f.exists():
                from PIL import Image
                wpx, hpx = Image.open(f).size
                # place at native 300 ppi (never upscaled): width = px / 300 in
                art = f"({lit('../' + str(f.relative_to(ROOT)))}, {wpx / 300:.3f}in, {hpx / 300:.3f}in)"
        self.out.append(f"#chapter-opener({numlit}, [#{lit(rest)}], {lit(h['id'])}, lead: {('[' + lead + ']') if lead else 'none'}, art: {art})\n")
        self.out.append(self.tags(h["id"]) + "\n")
        self.emit_chapter_body(blocks[i:])

    # ------------------------------------------------------------- keep-unit layout
    def chapter_items(self, rest_blocks):
        """Flatten a chapter into rendered items: dict(b, s, kind 'c'|'f', id, typ)."""
        items = []
        # Further chapter-intro paragraphs continue in the full-width page flow.
        # Packing them into the unbreakable title/art opener can overflow a page.
        introduction = bool(rest_blocks and is_flavour(rest_blocks[0]))
        for k, b in enumerate(rest_blocks):
            nxt = rest_blocks[k + 1] if k + 1 < len(rest_blocks) else None
            if b["type"] == "hr" and nxt is None:
                self.block_map.append((b["id"], b["src"], "hr-absorbed-by-chapter-break", None))
                continue
            if b["type"] == "table":
                introduction = False
                duplicate_title = bool(items and items[-1]['typ'] == 'heading' and
                    self.table_titles.get(b['id']) == items[-1]['b'].get('title'))
                s, scope = self.table(b, initial_title=not duplicate_title)
                if items and items[-1]["s"].startswith("#runin[") and items[-1]["kind"] == "c":
                    lab = items.pop()
                    self.block_map.append((lab["id"], lab["b"]["src"], "label-with-table", None))
                    s = lab["s"] + s
                items.append(dict(b=b, s=s + "\n", kind="f" if scope == "full" else "c", id=b["id"], typ="table"))
                continue
            # Opening flavour belongs to chapters, numbered sections and named scenarios.
            # Individual monster/power/gear entry flavour remains within its ordinary column.
            opening = b['type'] == 'para' and is_flavour(b) and introduction
            introduction = opening or (b['type'] == 'heading' and
                (b['level'] <= 3 or bool(re.match(r'^Scenario \d+: ', b.get('title', '')))))
            r = self.para(b, role='section-lead') if opening else self.render(b)
            if (b["type"] == "para" and items and items[-1]["typ"] == "heading" and r.endswith("\n\n")
                    and len(first_text_full(b)) < 300 and not r.startswith(("#example[", "#flavour[", "#runin["))):
                r = f"#keep[{r.rstrip()}]\n"
            typ = b["type"]
            if typ == "para" and r.startswith("#example["):
                typ = "example"
            if (typ == "list" and not b["ordered"] and items and items[-1]["typ"] == "list" and items[-1]["kind"] == "c"
                    and items[-1]["b"].get("ordered") and len(items[-1]["b"]["items"]) == 1 and items[-1]["s"].startswith("#enum(")):
                # an entry's numbered title ("2. Heaven's Spear [3 AP, 10 NRG]") never splits from its Range/Area/Effect lines
                title = items.pop()
                self.block_map.append((title["id"], title["b"]["src"], "title-with-list", None))
                r = f"#keep[{self.contained(title['b'], title['s'].rstrip())}{r.rstrip()}]\n"
            if typ in ("list", "quote") and items and items[-1]["s"].startswith("#runin[") and items[-1]["kind"] == "c":
                # a bold run-in label ("Attacks", "Adept Assassin Talents") travels with the list it introduces
                lab = items.pop()
                self.block_map.append((lab["id"], lab["b"]["src"], "label-with-list", None))
                r = lab["s"] + r
            items.append(dict(b=b, s=r, kind="f" if opening else "c", id=b["id"], typ=typ))
            for fig in self.figs_for(b):
                full = fig.get("scope") == "full"
                items.append(dict(b={"type": "figure", "id": fig["id"], "src": b["src"]}, s=self.figure(fig, full=full),
                                  kind="f" if full else "c", id=fig["id"], typ="figure",
                                  float=fig["id"] in FLOAT_FIGS))
        return items

    @staticmethod
    def build_tree(items):
        root = {"level": 2, "children": [], "id": None}
        stack = [root]
        for it in items:
            if it["typ"] == "heading":
                lvl = it["b"]["level"]
                while stack[-1]["level"] >= lvl:
                    stack.pop()
                node = {"level": lvl, "head": it, "children": [], "id": it["id"], "title": it["b"]["title"]}
                stack[-1]["children"].append(node)
                stack.append(node)
            else:
                stack[-1]["children"].append(it)
        return root

    def flat_parts(self, x, marked=False):
        """[(kind, [strings])] runs for measuring/placing a whole unit on one page."""
        parts = []
        glue = [False]
        def add(kind, s, is_head=False):
            if kind == "c" and parts and parts[-1][0] == "c":
                if glue[0]:
                    parts[-1][1][-1] += s        # a heading never ends a balancing piece
                else:
                    parts[-1][1].append(s)
            else:
                parts.append((kind, [s]))
            glue[0] = is_head and kind == "c"
        def walk(n, outer=False):
            tracked = marked and not outer and self.measurable(n)
            prefix = f"#umark({lit(n['id'])}, \"s\")" if tracked else ''
            if "head" in n:
                add("c", prefix + n["head"]["s"], True)
                for c in n["children"]:
                    walk(c)
            else:
                if n['typ'] == 'list' and n['s'].startswith(('#list(', '#enum(')):
                    for index, fragment in enumerate(self.list_fragments(n['b'])):
                        add(n['kind'], (prefix if index == 0 else '') + fragment)
                else:
                    add(n["kind"], inject(n["s"], prefix) if prefix else n["s"], n["s"].startswith("#runin["))
            if tracked:
                self.log_unit(n, 'contained')
                parts[-1][1][-1] += f"#umark({lit(n['id'])}, \"e\")"
        walk(x, outer=True)
        return parts

    @staticmethod
    def parts_typst(parts, strip=False):
        out = []
        for kind, ss in parts:
            if kind == "c":
                # prose-only runs may flow between columns; runs with rigid pieces use the whole-piece grid
                k = "c" if any(is_rigid(x) for x in ss) else "p"
                out.append(f"(\"{k}\", ({', '.join('[' + x + ']' for x in ss)},))")
            else:
                out.append(f"(\"f\", [{''.join(ss)}])")
        return ", ".join(out)

    def measurable(self, x):
        return ("head" in x) or x["typ"] in ("list", "table", "example", "quote", "figure")

    def collect_units(self, x, acc):
        if "head" in x:
            acc.append(x)
            for c in x["children"]:
                self.collect_units(c, acc)
        elif self.measurable(x):
            acc.append(x)

    def unit_class(self, x, fresh):
        m = self.measures.get(x["id"])
        if not m:
            return "over"
        if fresh and m["h2"] <= FRAME_FIT:
            return "page"
        if m["h1"] <= FRAME_FIT:
            return "col"
        if m["h2"] <= FRAME_FIT:
            return "page"
        return "over"

    def emit_chapter_body(self, rest_blocks):
        items = self.chapter_items(rest_blocks)
        root = self.build_tree(items)
        units = []
        for c in root["children"]:
            self.collect_units(c, units)
        for u in units:
            self.request_measure(u)
        for u in list(self.extra_units.values()):
            self.request_measure(u)
        cur = []
        prev_heading_only = True     # chapter opener counts as the start of the opening composition
        for c in root["children"]:
            cur, prev_heading_only = self.emit_x(c, cur, prev_heading_only)
        self.flush(cur)

    def request_measure(self, u):
        if u['id'] not in self.requested_units:
            self.requested_units.add(u['id'])
            self.measure_requests.append(f"#munit({lit(u['id'])}, ({self.parts_typst(self.flat_parts(u))},))\n")

    def is_fresh(self, n):
        return n["level"] == 3 or bool(re.match(r"^(?:Scenario \d+: |Climate \d+: .* Scenarios$)", n.get("title", "")))

    def record(self, x, mode):
        def walk(n):
            if "head" in n:
                self.block_map.append((n["head"]["id"], n["head"]["b"]["src"], mode, None))
                for c in n["children"]:
                    walk(c)
            else:
                self.block_map.append((n["id"], n["b"]["src"], mode, None))
        walk(x)

    def emit_x(self, x, cur, after_heading):
        """Emit item/node x. `after_heading`: nothing but headings since the last fresh-page start.
        Returns (cur, after_heading)."""
        if "head" not in x:
            return self.emit_leaf(x, cur), False
        fresh = self.is_fresh(x)
        if fresh and not after_heading:
            self.flush(cur)
            cur = []
            self.out.append("#pagebreak(weak: true)\n")
            after_heading = True
        cls = self.unit_class(x, fresh)
        self.log_unit(x, cls)
        if cls == "col":
            self.record(x, "keep-col")
            body = "".join(s for _, ss in self.flat_parts(x, marked=True) for s in ss)
            cur.append((x["head"]["b"], f"#keepcol[#umark({lit(x['id'])}, \"s\"){body}#umark({lit(x['id'])}, \"e\")]\n"))
            return cur, False
        if cls == "page":
            self.record(x, "keep-page")
            self.flush(cur)
            self.out.append(f"#keeppage(id: {lit(x['id'])}, {self.parts_typst(self.flat_parts(x, marked=True))})\n")
            return [], False
        # over-height: heading sticks to its content; children keep their own units
        self.block_map.append((x["head"]["id"], x["head"]["b"]["src"], "column", None))
        head = f"#umark({lit(x['id'])}, \"s\")" + x["head"]["s"]
        kids = x["children"]
        if kids and "head" not in kids[0] and kids[0]["kind"] == "f":
            # heading travels with a leading full-width element
            self.flush(cur)
            cur = []
            first = kids[0]
            piece = first['s']
            if self.measurable(first):
                self.log_unit(first, 'full')
                piece = f"#umark({lit(first['id'])}, \"s\"){piece}#umark({lit(first['id'])}, \"e\")"
            self.out.append(f"#full-opening[{head}{piece}]\n".replace("#pm(", "#pmx("))
            self.record(kids[0], "full")
            kids = kids[1:]
            after = False
        else:
            # opening group: heading + first leaf (+ the list/table a short lead-in introduces) move as one
            lead = []
            def small(k):
                if self.measurable(k):
                    return self.measures.get(k["id"], {}).get("h1", 1e9) <= FRAME_FIT / 2
                return k["typ"] in ("para", "heading") and len(first_text_full(k["b"])) < 1200
            if kids and "head" not in kids[0] and kids[0]["kind"] == "c" and small(kids[0]):
                lead.append(kids[0])
                intro_text = first_text_full(kids[0]['b']).rstrip()
                if (kids[0]["typ"] == "para" and len(intro_text) <= 300 and
                        (intro_text.endswith(":") or len(intro_text.split()) <= 4)
                        and len(kids) > 1 and "head" not in kids[1] and kids[1]["kind"] == "c"
                        and small(kids[1])):
                    lead.append(kids[1])
            if lead:
                for l in lead:
                    self.record(l, "keep-with-heading")
                body = head
                for l in lead:
                    if self.measurable(l):
                        self.log_unit(l, 'keep-with-heading')
                        body += f"#umark({lit(l['id'])}, \"s\"){l['s']}#umark({lit(l['id'])}, \"e\")"
                    else:
                        body += l['s']
                cur.append((x["head"]["b"], f"#keepcol[{body.rstrip()}]\n"))
                kids = kids[len(lead):]
                after = False
            else:
                cur.append((x["head"]["b"], head))
                after = after_heading
        for c in kids:
            cur, after = self.emit_x(c, cur, after)
        cur.append(({"type": "marker", "id": x["id"] + ":end", "src": x["head"]["b"]["src"]},
                    f"#umark({lit(x['id'])}, \"e\")"))
        return cur, False

    def emit_leaf(self, x, cur):
        mid = x["id"]
        if x["kind"] == "f":
            self.flush(cur)
            m = self.measures.get(mid)
            self.record(x, "full")
            tracked = self.measurable(x)
            body = (f"#umark({lit(mid)}, \"s\"){x['s']}#umark({lit(mid)}, \"e\")"
                    if tracked else x['s'])
            if x.get("float"):
                self.out.append(f"#place(auto, float: true, clearance: 12pt)[{body}]\n")
            else:
                brk = "false" if (m and m["h2"] <= FRAME_FIT) else "true"
                self.out.append(f"#full[#block(breakable: {brk}, width: 100%)[{body}]]\n")
            if tracked:
                self.log_unit(x, 'full')
            return []
        if not self.measurable(x):
            cur.append((x["b"], x["s"]))
            return cur
        cls = self.unit_class(x, False)
        self.log_unit(x, cls)
        if cls == "page":
            self.flush(cur)
            self.record(x, "keep-page")
            self.out.append(f"#keeppage(id: {lit(mid)}, {self.parts_typst(self.flat_parts(x))})\n")
            return []
        s = x["s"].rstrip("\n")
        body = f"#umark({lit(mid)}, \"s\"){s}#umark({lit(mid)}, \"e\")"
        wrapper = '#keepfigure' if x['typ'] == 'figure' else '#keepcol'
        cur.append((x["b"], (f"{wrapper}[{body}]" if cls == "col" else body) + "\n"))
        return cur

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
        for i in dict.fromkeys(ids):
            out.extend(self.fig_slots.get(i, []))
            self.placed_figs.update(f["id"] for f in self.fig_slots.get(i, []))
        return out

    def figure(self, fig, full=False):
        w = fig.get("width", "100%")
        cap = fig["caption"]
        return f"#figure-block({lit(fig['id'])}, {lit('../figures/out/' + fig['id'] + '.svg')}, [#{lit(cap)}], width: {w})\n"

    def render(self, b):
        if b["type"] == "heading" and b["level"] <= 3:
            self.in_glossary = b["title"].startswith("C.11 ")
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
                    carry += parts[j]
                    continue
                tp.append(carry + parts[j])
                carry = ""
            if carry:
                tp.append(carry)
            tp[-1] = tp[-1] + end
            if all(not is_rigid(piece) for piece in tp):
                # Zero-size terminal markers do not turn a prose tail into a
                # whole-piece grid with an empty right column.
                self.out.append("#flowtail((" + ', '.join('[' + piece + ']' for piece in tp) + ",))\n")
            else:
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


STRADDLE_MAX = 250
TOP_Y = MARGIN_TOP_PT
FRAME_H = BODY_HEIGHT_PT
FRAME_FIT = FRAME_H - 12                 # measured component overhead and a documented boundary tolerance
BODY_BOTTOM = PAGE_HEIGHT_PT - MARGIN_BOTTOM_PT


def compute_balance(pm, prev, sigs, heads=None, hpos=None):
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
        byp = {m["piece"]: m for m in starts}
        on_last = [m for m in starts if m["page"] == L]
        tiny_tail = (end.get('x', 0) < PAGE_WIDTH_PT / 2 and end['y'] < TOP_Y + 90 and len(on_last) <= 5)
        if pt is not None and pt in byp and byp[pt]["page"] == L and not tiny_tail:
            res[str(sid)] = [sigs[str(sid)], pt]
            continue
        if not on_last:
            lastp = starts[-1] if starts else None
            if lastp and lastp["page"] == L - 1 and BODY_BOTTOM - lastp["y"] < STRADDLE_MAX:
                res[str(sid)] = [sigs[str(sid)], lastp["piece"]]
            continue
        t = on_last[0]["piece"]
        if t > 0:
            prevs = [m for m in starts if m["piece"] < t]
            if not prevs:
                res[str(sid)] = [sigs[str(sid)], t]
                continue
            prevp = prevs[-1]
            first = on_last[0]
            at_top = abs(first["y"] - TOP_Y) < 20 and first["x"] < 300
            if tiny_tail and prevp['page'] == L - 1 and BODY_BOTTOM - prevp['y'] < STRADDLE_MAX:
                t = prevp['piece']
            elif not at_top:
                if BODY_BOTTOM - prevp["y"] < STRADDLE_MAX or prevp["page"] == L:
                    t = prevp["piece"]
                else:
                    continue
        res[str(sid)] = [sigs[str(sid)], t]
    for k, (sig, t) in list(res.items()):
        while t > 0 and f"{k}:{t-1}" in (heads or {}):
            t -= 1
        res[k] = [sig, t]
    return res


def stabilize_balance(proposed, previous, flips, excluded):
    """Use natural column flow for an oscillating tail, rather than freezing a proposal.

    Exclusions are explicit planner policy. The final emitted balance must equal
    a fresh proposal filtered by that policy; keeping a previous alternating
    variant alone is not convergence.
    """
    result = dict(proposed)
    for key in set(result) | set(previous):
        if result.get(key) != previous.get(key) and key not in excluded:
            flips[key] = flips.get(key, 0) + 1
            if flips[key] > 2:
                excluded.add(key)
    for key in excluded:
        result.pop(key, None)
    return result


def main():
    import time
    started = time.perf_counter()
    BUILD.mkdir(parents=True, exist_ok=True)
    MAP.mkdir(parents=True, exist_ok=True)
    if not (BUILD / "blocks.json").exists():
        raise FileNotFoundError("Missing build/blocks.json; generate the parsed manuscript before building the book.")
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="cream")
    ap.add_argument("--passes", type=int, default=5)
    ap.add_argument("--no-balance", action="store_true")
    ap.add_argument("--variants-only", action="store_true", help="compile white + digital from the current content.typ")
    ap.add_argument("--allow-nonconverged", action="store_true", help="diagnostic output only; final publication requires convergence")
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
    # measurement pass: classify keep units from their real rendered heights
    import subprocess
    probe = Book(model, balance)
    probe.emit()
    (ROOT / "typst/measure.typ").write_text(
        '#import "heraldry.typ": *\n#show: book\n' + "".join(probe.measure_requests)
        + '\n#context { pdf.attach("/heraldry-unit-measurements.json", '
        'bytes(json.encode(query(<um>).map(m => m.value))), '
        'mime-type: "application/json", relationship: "supplement") }\n', encoding="utf-8", newline="\n")
    r = subprocess.run([sys.executable, str(ROOT / "tools/measure_units.py")], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-3000:])
    print(r.stdout.strip())
    flips, pass_log, excluded = {}, [], set()
    converged = False
    for p in range(a.passes):
        book = Book(model, balance)
        (ROOT / "typst/content.typ").write_text(book.emit(), encoding="utf-8", newline="\n")
        out, dt, (pm, hpos) = compile_book(a.variant)
        new = compute_balance(pm, balance, book.seg_sigs, book.piece_heads, hpos) if not a.no_balance else {}
        raw_changes = sum(1 for k in set(new) | set(balance) if new.get(k) != balance.get(k))
        new = stabilize_balance(new, balance, flips, excluded)
        changes = sum(1 for k in set(new) | set(balance) if new.get(k) != balance.get(k))
        pass_log.append({'pass': p + 1, 'compile_seconds': dt, 'segments': book.seg_count,
                         'balanced': len(new), 'changes': changes, 'raw_changes': raw_changes,
                         'natural_flow_segments': sorted(excluded)})
        print(f"pass {p+1}: {dt:.1f}s, segments={book.seg_count}, balanced={len(new)}, changed={sum(1 for k in set(new)|set(balance) if new.get(k)!=balance.get(k))}")
        if new == balance or a.no_balance:
            converged = True
            break
        for k, (sig, t) in list(new.items()):
            while t > 0 and f"{k}:{t-1}" in book.piece_heads:
                t -= 1
            new[k] = [sig, t]
        if p == a.passes - 1 or new == balance:
            converged = new == balance
            break
        balance = new
        bal_file.write_text(json.dumps(balance))
    MAP.mkdir(parents=True, exist_ok=True)
    (MAP / "tables.json").write_text(json.dumps(book.table_map, ensure_ascii=False, indent=0), encoding="utf-8", newline="\n")
    (MAP / "blocks.json").write_text(json.dumps(book.block_map, ensure_ascii=False), encoding="utf-8", newline="\n")
    import hashlib
    from source_units import source_unit_manifest
    manifest = source_unit_manifest(model, book.fig_slots)
    (BUILD / "units.json").write_text(json.dumps({"frame_fit_pt": FRAME_FIT, "units": book.unit_log,
        "expected_unit_ids": [u['id'] for u in manifest], 'source_unit_manifest': manifest,
        "content_sha256": hashlib.sha256((ROOT / "typst/content.typ").read_bytes()).hexdigest()}))
    (BUILD / 'layout-build.json').write_text(json.dumps({'profile': profile_dict(), 'passes': pass_log,
        'converged': converged, 'natural_flow_segments': sorted(excluded),
        'seconds': round(time.perf_counter() - started, 3),
        'source_sha256': model['sha256'], 'content_sha256': hashlib.sha256((ROOT / 'typst/content.typ').read_bytes()).hexdigest()}, indent=2))
    if not converged and not a.allow_nonconverged:
        raise SystemExit('Layout balancing did not converge; diagnostic PDF preserved but cannot be published')
    print("links:", len(book.em.links), "->", out)


if __name__ == "__main__":
    main()
