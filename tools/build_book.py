#!/usr/bin/env python3
"""Generate typst/content.typ from build/blocks.json and run the balancing build loop.

Text is emitted only as Typst string literals (#"..."), so Typst never applies
smart quotes, shorthands or markup interpretation to manuscript characters.
Layout-only transformations (no-break spaces in dice/AP units, soft line breaks
rendered as line breaks, table representations) are recorded in
production/mappings/.
"""
from __future__ import annotations
import argparse, hashlib, json, math, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tables import classify, cell_plain, COL_W, FULL_W  # noqa: E402
from layout_profile import (MARGIN_TOP_PT, MARGIN_BOTTOM_PT, PAGE_HEIGHT_PT, PAGE_WIDTH_PT,
    BODY_HEIGHT_PT, profile_dict)
from layout_balance_cache import load_hint, save_hint

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


FIG_CALL = re.compile(r'#figure-block\((?P<pre>pre: \[#umark\("FIG-\d+", "s"\)\], )?"(?P<id>FIG-\d+)", (?P<path>"[^"]+"), \[#"(?P<cap>(?:[^"\\]|\\.)*)"\]')


def number_figures(text):
    """Figures print in book order: FIG-01 is the first figure a reader meets. The figure's
    registry id (its file, manifest record, review, and position marks) is unchanged; only the
    printed label and the caption references follow book order (owner 2026-10-30 polish)."""
    order = list(dict.fromkeys(m.group("id") for m in FIG_CALL.finditer(text)))
    shown = {fid: f"FIG-{i:02d}" for i, fid in enumerate(order, 1)}
    relabel = lambda s: re.sub(r"FIG-\d+", lambda m: shown.get(m.group(0), m.group(0)), s)
    (BUILD / "figure_labels.json").write_text(json.dumps(shown, indent=1) + "\n")
    # A drawing that names another figure (the setup diagrams' "key: FIG-20") gets a relabelled copy.
    copies = BUILD / "figures"
    copies.mkdir(parents=True, exist_ok=True)
    def path_for(fid, path):
        svg = (ROOT / "figures/out" / f"{fid}.svg").read_text(encoding="utf-8")
        new = relabel(svg)
        if new == svg:
            return path
        (copies / f"{fid}.svg").write_text(new, encoding="utf-8", newline="\n")
        return lit(f"../build/figures/{fid}.svg")
    return FIG_CALL.sub(lambda m: f'#figure-block({m.group("pre") or ""}"{m.group("id")}", {path_for(m.group("id"), m.group("path"))}, '
                                  f'[#"{relabel(m.group("cap"))}"], shown: "{shown[m.group("id")]}"', text)


def load_end_art(art_ids):
    """Art set at the end of a unit, in white space its last page would otherwise leave empty
    (owner 2026-10-30). Basic Mode Hero portraits close their profiles; catalogue tailpieces
    (`end_art`, from production/art/END_ART_PLAN.json) close their sections once approved.
    Returns {heading id: (art id, path, width pt, aspect, maximum width pt)}. A tailpiece may grow past
    its family width to the gap it closes, up to its 300 ppi maximum and the design cap (D-02 f); Hero
    portraits keep their family width."""
    from PIL import Image
    cat = json.loads((ROOT / "production/art/SPOT_CATALOG.json").read_text())["entries"]
    cap = float(json.loads((ROOT / "config/design_tokens.json").read_text()).get("art", {}).get("tailpiece_max_width_in", 0)) * 72
    wanted = {e["heading_id"]: (e["id"], bool(e.get("end_art"))) for e in cat
              if (e.get("family") == "hero" or e.get("end_art")) and e.get("heading_id")}
    out = {}
    for head, (aid, tailpiece) in wanted.items():
        if aid not in art_ids:
            continue                   # not approved yet: the space stays white
        rel, w_in = art_ids[aid]
        with Image.open(ROOT / rel[3:]) as image:
            wpx, hpx = image.size
        aspect = hpx / wpx
        w = w_in * 72
        wmax = max(w, min(wpx / 300 * 72, cap)) if tailpiece and cap > 0 else w
        out[head] = (aid, rel, w, aspect, wmax)
    return out


FLOAT_FIGS = set(json.loads((ROOT / "config/design_tokens.json").read_text()).get("layout", {}).get("float_figures", []))
TABLE_SCOPE_POLICIES = json.loads((ROOT / "config/design_tokens.json").read_text()).get('layout', {}).get('table_scope_policies', {})
# Composition policy (owner approval 2026-11-01): numbered section heads span the frame, the first section
# may share the chapter-opener page, reference appendices run on, and short tails pull back.
LAYOUT_TOKENS = json.loads((ROOT / "config/design_tokens.json").read_text()).get("layout", {})
SECTION_HEADS_FULL = bool(LAYOUT_TOKENS.get("section_heads_full_width", False))
RUN_ON_CHAPTERS = set(LAYOUT_TOKENS.get("run_on_chapters", []))
OPENER_SHARE_FREE = float(LAYOUT_TOKENS.get("opener_share_free_fraction", 0))

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
    re.compile(r"\b\w+ \(c\)"),                            # Cost (c): the coin stays with its label
]
# A numeric range never breaks after its en dash ("4–8 rounds"); boxed in layout only, so the
# text layer keeps the source characters exactly.
RANGE = re.compile(r"\d+(?:\.\d+)?–\d+(?:\.\d+)?")
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


def semantic_heading(title):
    """Ignore section numbering, preserving the confirmed heading words exactly."""
    return re.sub(r'^(?:Appendix [A-Z]\.\s+|(?:\d+(?:\.\d+)*|[A-Z](?:\.\d+)+)\.?\s+)',
                  '', ' '.join(title.split()))


class TableScopePolicyError(ValueError):
    def __init__(self, message, diagnostics):
        super().__init__(message)
        self.diagnostics = diagnostics


def resolve_table_scope_policies(tables, policies):
    """Resolve reviewed width preferences by full heading path and header cells.

    Cell hashes describe the reviewed specimen; they never supply cached heights.
    A removed/renamed target is unused, while duplicate semantic targets fail.
    """
    resolved, diagnostics, errors = {}, [], []
    for name, policy in policies.items():
        selector = policy['selector']
        path = [semantic_heading(t) for t in selector['heading_path']]
        matches = [b for b, actual_path in tables
                   if [semantic_heading(t) for t in actual_path] == path
                   and [cell_plain(c) for c in b['header']] == selector['headers']]
        record = {'policy': name, 'selector': selector,
                  'reviewed_content_sha256': policy['reviewed_content_sha256']}
        if not matches:
            diagnostics.append(record | {'status': 'missing', 'table_id': None,
                'message': 'No semantic target; width preference unused. Check removed or renamed headings/headers.'})
            continue
        if len(matches) != 1:
            ids = [b['id'] for b in matches]
            diagnostics.append(record | {'status': 'ambiguous', 'table_ids': ids})
            errors.append(f'{name}: ambiguous semantic table selector matches {", ".join(ids)}')
            continue
        table = matches[0]
        current_hash = table_content_sha256(table)
        status = 'matched' if current_hash == policy['reviewed_content_sha256'] else 'content_changed'
        record |= {'status': status, 'table_id': table['id'], 'content_sha256': current_hash,
                   'measurement': 'Fresh allocation and normal rendered measurement required; no reviewed height reused.'}
        diagnostics.append(record)
        if table['id'] in resolved:
            errors.append(f'{table["id"]}: multiple width policies resolve to the same table')
        else:
            resolved[table['id']] = policy | {'audit': record}
    if errors:
        raise TableScopePolicyError('; '.join(errors), diagnostics)
    return resolved, diagnostics


def apply_table_scope_override(table, classification, policy):
    """Reallocate current cells at the reviewed preferred width; never reuse heights."""
    from tables import allocate, measure_table
    if policy.get('scope') != 'full' or classification.get('rep') != 'table':
        raise ValueError('Unsupported table scope override: ' + table['id'])
    mins, maxs, _ = measure_table(table)
    widths, _ = allocate(mins, maxs, FULL_W, [table])
    if widths is None:
        raise ValueError('Reviewed table no longer fits full width: ' + table['id'])
    return classification | {'scope':'full', 'widths':[round(x,2) for x in widths],
        'max_pt':[round(x,1) for x in maxs], 'scope_reason':policy['reason'],
        'scope_policy': policy['audit']}


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
                    v = nobreak(n["v"])
                    at = 0
                    for m in RANGE.finditer(v):
                        if m.start() > at:
                            out.append("#" + lit(v[at:m.start()]))
                        out.append("#box[#" + lit(m.group(0)) + "]")
                        at = m.end()
                    if at < len(v):
                        out.append("#" + lit(v[at:]))
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


# A column unit made only of headings, paragraphs, run-in labels, list items, and examples may be split
# between those pieces inside a balanced run, which always sits on one page: the one-page keep rule asks for
# one page, not one column ("A column limit is not proof that a unit cannot fit", PROJECT_CONTRACT). Units with
# tables, figures, art, stat blocks, cards, nested whole units, or power-style numbered entries stay whole.
SPLIT_BLOCKERS = ("#htable(", "#statstrip(", "#statcard(", "#cards(", "#figure-block(", "#keepfigure[", "#keepcol[",
                  "#spotart(", "#endart(", "image(", "#keep[#enum(", "#keep[#list(", "#keeppage(", "#full")


def splittable(pieces):
    return len(pieces) > 1 and not any(b in p for p in pieces for b in SPLIT_BLOCKERS)


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
    if s.startswith("#list-fragment(") and ")[" in s:
        i = s.index(")[") + 2
        return s[:i] + mark + s[i:]
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
    def __init__(self, model, balance, figfit=None):
        self.model = model
        self.figfit = dict(figfit or {})     # figure id -> width scale that lets it fit where it starts
        self.expansions = {}                 # a column unit's string -> its pieces, for use inside a balanced run
        self.full_figs = set()               # full-width figures set alone in the outer flow (#full or a float)
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
        self.piece_heads = {}   # heading-led pieces: start positions come from the heading query
        self.bare_heads = set()  # pieces that are only a heading and must travel with the next piece
        self.table_map = []
        self.block_map = []   # (block id, src span, representation, segment)
        self.out = []
        self.fig_slots = json.loads((ROOT / "figures/placements.json").read_text()) if (ROOT / "figures/placements.json").exists() else {}
        self.index_targets = json.loads((BUILD / "index_targets.json").read_text()) if (BUILD / "index_targets.json").exists() else {}
        self.tclass = self._classify_all()
        self.spot_art, self.art_ids = load_spot_art()
        self._check_art_anchors()
        self.end_art = load_end_art(self.art_ids)

    def _check_art_anchors(self):
        """Spot art attaches by flavour-block id. After a manuscript revision renumbers blocks, a stale
        catalogue would hang an illustration above another entry's flavour; refuse instead."""
        if not self.spot_art:
            return
        catalogue = json.loads((ROOT / "production/art/SPOT_CATALOG.json").read_text())["entries"]
        expected = {e["flavour_block"]: e["heading_id"] for e in catalogue if e.get("flavour_block")}
        follows = {}
        def walk(blocks):
            for i, b in enumerate(blocks):
                if b["type"] == "heading" and i + 1 < len(blocks):
                    follows[blocks[i + 1]["id"]] = b["id"]
                for item in b.get("items", []):
                    walk(item["blocks"])
                walk(b.get("blocks", []))
        for chapter in self.model["chapters"]:
            walk(chapter["blocks"])
        wrong = sorted(block for block in self.spot_art if follows.get(block) != expected.get(block))
        if wrong:
            raise SystemExit(f"Art catalogue is stale for {len(wrong)} flavour blocks (first: {wrong[:5]}); "
                             "run tools/art_catalog.py and review any changed specs")

    def _classify_all(self):
        """Classify every table, then unify families (same header signature within the
        same H3 section) so that sibling tables share one representation and widths."""
        from tables import measure_table, allocate
        tabs, contexts = [], []
        def walk(bs, sec, path):
            path = list(path)
            for b in bs:
                if b["type"] == "heading" and b["level"] <= 3:
                    sec = b["id"]
                if b["type"] == "heading":
                    path = [(level, title) for level, title in path if level < b['level']]
                    path.append((b['level'], b['title']))
                if b["type"] == "table":
                    tabs.append((b, sec))
                    contexts.append((b, [title for _, title in path]))
                    self.table_titles[b["id"]] = path[-1][1] if path else b['id']
                for it in b.get("items", []):
                    walk(it["blocks"], sec, path)
                walk(b.get("blocks", []), sec, path)
            return sec
        sec = None
        for ch in self.model["chapters"]:
            sec = walk(ch["blocks"], sec, [])
        res, fam = {}, {}
        policies, self.table_scope_diagnostics = resolve_table_scope_policies(contexts, TABLE_SCOPE_POLICIES)
        for b, sec in tabs:
            c = classify(b, None)
            if b['id'] in policies:
                c = apply_table_scope_override(b, c, policies[b['id']])
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
            w, _ = allocate(mins, maxs, FULL_W if scope == "full" else COL_W, members)
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
            mapping['scope_policy'] = c['scope_policy']
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
            s = self._cards(b, c, hdr, rows, mapping, initial_title=initial_title)
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

    def _cards(self, b, c, hdr, rows, mapping, initial_title=True):
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
        hidden = "" if initial_title else ", initial-title: false"
        return f"#cards({lit(b['id'])}, ({', '.join(entries)},), title-label: [#{lit(self.table_titles.get(b['id'], b['id']))}]{hidden})"

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
        return number_figures("".join(o))

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
        self.run_on = ch["id"] in RUN_ON_CHAPTERS          # D-02 c: sections of this chapter run on
        self.first_section_pending = True                   # D-02 b: the first section may share the opener page
        self.share_opener = False
        self.opener_id = h["id"]
        self.opener_src = f"#opener-body({numlit}, [#{lit(rest)}], art: {art}, lead: {('[' + lead + ']') if lead else 'none'})"
        self.emit_chapter_body(blocks[i:])

    # ------------------------------------------------------------- keep-unit layout
    def chapter_items(self, rest_blocks):
        """Flatten a chapter into rendered items: dict(b, s, kind 'c'|'f', id, typ)."""
        items = []
        # Further chapter-intro paragraphs continue in the full-width page flow.
        # Packing them into the unbreakable title/art opener can overflow a page.
        introduction = bool(rest_blocks and is_flavour(rest_blocks[0]))
        # A short plain introduction before the first section reads as one standfirst at the
        # opener's measure rather than a few loosely justified lines in two columns.
        intro = []
        for b in rest_blocks:
            if b["type"] == "para" and is_flavour(b) and not intro:
                continue
            if b["type"] == "para" and not (is_flavour(b) or is_example(b) or is_caption(b)):
                intro.append(b)
                continue
            if b["type"] != "heading":
                intro = []
            break
        if not (1 <= len(intro) <= 3 and sum(len(first_text_full(b)) for b in intro) <= 700):
            intro = []
        intro_ids = {b["id"] for b in intro}
        for k, b in enumerate(rest_blocks):
            if b["id"] in intro_ids:
                if b is intro[0]:
                    body = "#parbreak()".join(self.para(x).rstrip("\n") for x in intro)
                    items.append(dict(b=b, s=f"#chapter-intro[{body}]\n", kind="f", id=b["id"], typ="para"))
                else:
                    self.block_map.append((b["id"], b["src"], "chapter-intro", None))
                continue
            nxt = rest_blocks[k + 1] if k + 1 < len(rest_blocks) else None
            if b["type"] == "hr" and nxt is None:
                self.block_map.append((b["id"], b["src"], "hr-absorbed-by-chapter-break", None))
                continue
            if b["type"] == "table":
                introduction = False
                # The visible heading names the table, so the identity line is hidden on the opening page;
                # a short run-in label between them ("APL 1–2 (d10)") does not change that (D-08).
                named_by = items[-1]['b'] if items and items[-1]['typ'] == 'heading' else (
                    items[-2]['b'] if len(items) >= 2 and items[-2]['typ'] == 'heading'
                    and items[-1]['s'].startswith('#runin[') and items[-1]['kind'] == 'c' else None)
                duplicate_title = bool(named_by and self.table_titles.get(b['id']) == named_by.get('title'))
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
            if (b["type"] == "para" and r.endswith("\n\n") and nxt is not None and is_flavour(nxt)
                    and items and items[-1]["s"].startswith("#runin[") and items[-1]["kind"] == "c"
                    and items[-1]["typ"] == "para" and len(first_text_full(b)) < 300):
                # An item's label and name line ("Tier 2 Special Item", then "Old Wode's Tithe-Bundle | Cost: 20c
                # | ...") head its entry: one run-in block, so they never end a column or page without the
                # flavour that follows (all-page review of candidate 19, p. 209).
                lab = items.pop()
                self.block_map.append((lab["id"], lab["b"]["src"], "label-with-entry-head", None))
                r = lab["s"].rstrip()[:-1] + "#parbreak()" + r.rstrip() + "]\n"
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
                if outer and SECTION_HEADS_FULL and n["head"].get("b", {}).get("level") == 3:
                    parts.append(("f", [prefix + n["head"]["s"]]))   # the section head spans the frame (D-01)
                    glue[0] = False
                else:
                    add("c", prefix + n["head"]["s"], True)
                for c in n["children"]:
                    walk(c)
            else:
                if n['typ'] == 'list' and n['s'].startswith(('#list(', '#enum(')):
                    for index, fragment in enumerate(self.list_fragments(n['b'])):
                        add(n['kind'], (prefix if index == 0 else '') + fragment)
                else:
                    # Only a bare run-in label glues to what follows. A label already merged with its
                    # list or table is a complete piece; gluing it chained every later piece of a
                    # profile into one unbreakable block (design review 2026-10-29, PDF p. 531).
                    add(n["kind"], inject(n["s"], prefix) if prefix else n["s"],
                        n["s"].startswith("#runin[") and n["typ"] == "para")
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
        intro_open = True
        mark = None
        # The opener and its introduction are measured as one full-width run (the measurement pass
        # records them like any unit), so the sharing decision is deterministic (D-02 b).
        intro_items = [c for c in root["children"] if "head" not in c and c["kind"] == "f"]
        leading = []
        for c in root["children"]:
            if "head" in c or c["kind"] != "f":
                break
            leading.append(c)
        opener_key = f"opener:{getattr(self, 'opener_id', 'none')}"
        if hasattr(self, "opener_src") and opener_key not in self.requested_units:
            self.requested_units.add(opener_key)
            parts = [("f", [self.opener_src + "".join(c["s"] for c in leading)])]
            self.measure_requests.append(f"#munit({lit(opener_key)}, ({self.parts_typst(parts)},))\n")
        for c in root["children"]:
            if intro_open and ("head" in c or c["kind"] != "f"):
                # End of the chapter's opening flavour: the opener uses this mark to see whether its
                # introduction fits beside the art or needs an opener spread.
                mark = len(self.out)
                if "head" in c:
                    # "auto": the opener centres itself when the first section does not land on its page
                    # after all (Typst's balanced grid may still move it), so a shared opener never
                    # prints top-aligned above an empty half page (candidate 20261101T183315Z, p. 75).
                    self.share_opener = self.opener_shares(opener_key, c)
                    self.out.append('#intro-end(solo: "auto")\n')
                else:
                    self.out.append("#intro-end()\n")
                intro_open = False
            cur, prev_heading_only = self.emit_x(c, cur, prev_heading_only)
        self.flush(cur)
        if intro_open:
            mark = len(self.out)
            self.out.append("#intro-end()\n")
        if mark is not None and (mark + 1 == len(self.out) or self.out[mark + 1].startswith("#pagebreak")):
            # Nothing but the opener shares its page: the first section starts a fresh page.
            self.out[mark] = "#intro-end(solo: true)\n"

    def first_piece_fits(self, piece):
        """True when the first column piece after a run-on opening is prose, or a measured unit no
        taller than half a frame (a subsection counts by its column height)."""
        if piece is None:
            return True
        if "head" in piece or self.measurable(piece):
            m = getattr(self, "measures", {}).get(piece["id"])
            return bool(m) and m["h1"] <= FRAME_FIT / 2
        return piece.get("kind") == "c"

    def opener_shares(self, opener_key, first):
        """True when the first numbered section starts on the chapter-opener page (owner approval
        2026-11-01, D-02 b): the measured opener and introduction leave more than the token fraction of
        the frame free, and a page-fit first section fits in that free space. Decided from the
        measurement pass, so it never depends on a position read during layout."""
        if OPENER_SHARE_FREE <= 0 or not SECTION_HEADS_FULL or getattr(self, "run_on", False):
            return False
        measures = getattr(self, "measures", {})
        opener = measures.get(opener_key)
        if not opener or first.get("level") != 3:
            return False
        free = FRAME_FIT - opener["h2"]
        if free < OPENER_SHARE_FREE * FRAME_H:
            return False
        section = measures.get(first["id"])
        if section and section["h2"] <= FRAME_FIT:
            return section["h2"] <= free       # a page-fit unit must fit beside the opener, or it moves whole
        return True

    def request_measure(self, u):
        if u['id'] not in self.requested_units:
            self.requested_units.add(u['id'])
            self.measure_requests.append(f"#munit({lit(u['id'])}, ({self.parts_typst(self.flat_parts(u))},))\n")

    def is_fresh(self, n):
        if n["level"] == 3 and getattr(self, "run_on", False):
            return False        # a reference appendix packs its sections (owner approval 2026-11-01, D-02 c)
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
        section = x["level"] == 3 and SECTION_HEADS_FULL
        if fresh and not after_heading:
            self.flush(cur)
            cur = []
            if x["level"] == 3 and getattr(self, "first_section_pending", False) and getattr(self, "share_opener", False):
                # The first section shares the opener page (D-02 b). Its first column segment flows
                # naturally instead of as a balanced grid: the grid's fixed height is decided from a
                # position that lags one layout iteration, and the fixed point it reached put the whole
                # section on the next page even though the flow fits (candidate 20261101T183315Z, p. 75).
                self.flow_next_flush = True
            else:
                self.out.append("#pagebreak(weak: true)\n")
            after_heading = True
        if x["level"] == 3:
            self.first_section_pending = False
        cls = self.unit_class(x, fresh)
        if cls == "col" and section:
            cls = "page"               # a column-fit section keeps its full-width head (D-01): a page unit
        if cls == "over" and not after_heading and x["children"] and is_statline(x["children"][0]):
            # An entry profile taller than a page (a Basic Mode Hero) starts a fresh page. Begun mid-page, its
            # whole-unit subsections could not fit the short column beside it, which stayed empty while they
            # moved to the next page (all-page review 2026-11-06, Ashborn).
            self.flush(cur)
            cur = []
            self.out.append("#pagebreak(weak: true)\n")
            after_heading = True
        self.log_unit(x, cls)
        if cls == "col":
            self.record(x, "keep-col")
            unit_parts = self.flat_parts(x, marked=True)
            pieces = [s for _, ss in unit_parts for s in ss]
            body = "".join(pieces)
            whole = f"#keepcol[#umark({lit(x['id'])}, \"s\"){body}#umark({lit(x['id'])}, \"e\")]\n"
            cur.append((x["head"]["b"], whole))
            if all(k == "c" for k, _ in unit_parts) and splittable(pieces):
                self.__dict__.setdefault("expansions", {})[whole] = ([inject(pieces[0], f"#umark({lit(x['id'])}, \"s\")")] + pieces[1:-1]
                                          + [pieces[-1] + f"#umark({lit(x['id'])}, \"e\")"])
            if x["id"] in getattr(self, "end_art", {}):
                # a one-column unit closes with its end art too (it was skipped here before)
                self.flush(cur)
                self.emit_end_art(x)
                return [], False
            return cur, False
        if cls == "page":
            self.record(x, "keep-page")
            self.flush(cur)
            self.out.append(f"#keeppage(id: {lit(x['id'])}, {self.parts_typst(self.flat_parts(x, marked=True))})\n")
            self.emit_end_art(x)
            return [], False
        # over-height: heading sticks to its content; children keep their own units
        self.block_map.append((x["head"]["id"], x["head"]["b"]["src"], "full" if section else "column", None))
        head = f"#umark({lit(x['id'])}, \"s\")" + x["head"]["s"]
        kids = x["children"]
        if section:
            # The numbered section head spans the frame (D-01): it is emitted in the outer flow ahead of
            # its columns, sticky to them; a leading full-width element still travels with it below.
            self.flush(cur)
            cur = []
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
        elif section and getattr(self, "run_on", False) and not after_heading:
            # A run-on section (D-02 c). With a short introduction, the head and the introduction open
            # as one unbreakable full-width composition, the introduction set as a standfirst at the
            # opener's measure; the opening is sticky, so when the first column piece cannot start on
            # the page the whole opening moves with it and never strands at a page foot. The section
            # runs on only when that first piece is prose or a unit no taller than half a frame, which
            # always fits beside a fresh-page opening; a taller first unit, or an opening without an
            # introduction, starts a fresh page (local build 2026-11-01, pp. 596 and 602).
            self.flush(cur)
            cur = []
            intro = (kids and "head" not in kids[0] and kids[0]["kind"] == "c" and kids[0]["typ"] == "para"
                     and kids[0]["s"].startswith("#keep[") and len(first_text_full(kids[0]["b"])) <= STANDFIRST_CHARS)
            follower = kids[1] if intro and len(kids) > 1 else (kids[0] if kids else None)
            runs_on = intro and self.first_piece_fits(follower)
            if not runs_on:
                self.out.append("#pagebreak(weak: true)\n")
            if intro:
                first = kids[0]
                standfirst = "#chapter-intro[" + first["s"].strip()[len("#keep["):-1] + "]"
                self.out.append(f"#full-opening(sticky: true)[{head}{standfirst}]\n".replace("#pm(", "#pmx("))
                self.record(first, "full")
                kids = kids[1:]
            else:
                self.out.append(f"#section-head[{head}]\n".replace("#pm(", "#pmx("))
            after = False
        elif section:
            self.out.append(f"#section-head[{head}]\n".replace("#pm(", "#pmx("))
            after = False
            n = self.lead_run(kids)
            if n:
                # The introduction closes its own run, which the tail rule balances on the opening page; the
                # first subsection, too tall for a column under the section head, starts the next page as it
                # would anyway (candidate 23, p. 12: 1.3 The Dying Lands in one column beside an empty one).
                for c in kids[:n]:
                    cur, after = self.emit_x(c, cur, after)
                self.flush(cur)
                cur = []
                self.out.append("#pagebreak(weak: true)\n")
                self.__dict__.setdefault("lead_runs", []).append(x["id"])
                kids = kids[n:]
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
                elif is_statline(kids[0]):
                    # A long profile's identification lines ("Class: ... | Level: 1", "HP: ... | AP: 3")
                    # and its first subsection stay with its name, so the entry never opens at a column
                    # foot with only its name and stats (design review 2026-10-29, B.4 profiles).
                    j = 1
                    while j < len(kids) and is_statline(kids[j]):
                        lead.append(kids[j])
                        j += 1
                    if (j < len(kids) and "head" not in kids[j] and kids[j]["kind"] == "c"
                            and kids[j]["typ"] == "list" and small(kids[j])):
                        lead.append(kids[j])
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
            elif self.splits_under_heading(kids):
                # The first table fits a column but not beside its heading. Kept whole, Typst's sticky
                # heading skipped a column and left the heading alone on its page (design review
                # 2026-10-29, Climate 5 journey table). Start the pair where both columns of one page
                # hold it, and let the table continue into the second column under its header.
                self.flush(cur)
                cur = []
                need = self.measures[x["id"]]["h1"] + SPLIT_RESERVE
                self.out.append(f"#split-start({need:.1f}pt)\n")
                cur.append((x["head"]["b"], head))
                cur = self.emit_leaf(kids[0], cur, split=True)
                kids = kids[1:]
                after = False
            else:
                cur.append((x["head"]["b"], head))
                after = after_heading
        for c in kids:
            cur, after = self.emit_x(c, cur, after)
        cur.append(({"type": "marker", "id": x["id"] + ":end", "src": x["head"]["b"]["src"]},
                    f"#umark({lit(x['id'])}, \"e\")"))
        if x["id"] in getattr(self, "end_art", {}):
            self.flush(cur)
            self.emit_end_art(x)
            return [], False
        return cur, False

    def emit_end_art(self, x):
        if x["id"] in getattr(self, "end_art", {}):
            aid, rel, w, aspect, wmax = self.end_art[x["id"]]
            self.out.append(f"#endart({lit(aid)}, {lit(rel)}, {w:.1f}pt, {aspect:.4f}, max-w: {wmax:.1f}pt)\n")

    def lead_run(self, kids):
        """Number of prose paragraphs opening a numbered section that close their own balanced run: a short
        introduction followed by a whole column unit that cannot split and is too tall for a column under the
        section head, so it can only start the next page. 0 when the section opens any other way."""
        n = 0
        while n < len(kids) and "head" not in kids[n] and kids[n]["kind"] == "c" and kids[n]["typ"] == "para":
            n += 1
        if not n or n == len(kids) or "head" not in kids[n]:
            return 0
        if sum(len(first_text_full(k["b"])) for k in kids[:n]) > LEAD_RUN_CHARS:
            return 0
        follower = kids[n]
        m = self.measures.get(follower["id"])
        if not m or self.unit_class(follower, False) != "col" or m["h1"] <= FRAME_H - SECTION_HEAD_PT:
            return 0
        parts = self.flat_parts(follower)      # unmarked: a marked walk logs the unit's contents
        if all(k == "c" for k, _ in parts) and splittable([s for _, ss in parts for s in ss]):
            return 0
        return n

    def splits_under_heading(self, kids):
        """True when a node's first child is a fit-capable table too tall to share a column with the heading."""
        if not kids or "head" in kids[0] or kids[0]["kind"] != "c" or kids[0]["typ"] != "table":
            return False
        m = self.measures.get(kids[0]["id"])
        return bool(m) and m["h1"] <= FRAME_FIT < m["h1"] + HEADING_ALLOWANCE

    def emit_leaf(self, x, cur, split=False):
        mid = x["id"]
        if x["kind"] == "f":
            self.flush(cur)
            m = self.measures.get(mid)
            self.record(x, "full")
            tracked = self.measurable(x)
            body = (f"#umark({lit(mid)}, \"s\"){x['s']}#umark({lit(mid)}, \"e\")"
                    if tracked else x['s'])
            if x.get("typ") == "figure":
                self.full_figs.add(mid)
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
            head = None
            if (cur and cur[-1][0].get("type") == "heading" and not is_unit_piece(cur[-1][1])
                    and self.measures.get(mid, {}).get("h2", 1e9) + HEADING_ALLOWANCE <= FRAME_FIT):
                # A bare heading never ends the segment before the page unit it introduces: it opens that
                # unit, glued to its first piece, so it cannot strand at a column foot while the unit moves
                # to the next page (all-page review 2026-11-06, "Preparation Steps").
                head = cur.pop()
            self.flush(cur)
            self.record(x, "keep-page")
            parts = self.flat_parts(x)
            if head is not None:
                self.block_map.append((head[0]["id"], head[0]["src"], "keep-page", None))
                if parts and parts[0][0] == "c":
                    parts[0][1][0] = head[1].rstrip("\n") + "\n" + parts[0][1][0]
                else:
                    parts.insert(0, ("c", [head[1]]))
            self.out.append(f"#keeppage(id: {lit(mid)}, {self.parts_typst(parts)})\n")
            return []
        s = x["s"].rstrip("\n")
        body = f"#umark({lit(mid)}, \"s\"){s}#umark({lit(mid)}, \"e\")"
        wrapper = '#keepfigure' if x['typ'] == 'figure' else '#keepcol'
        piece = (f"{wrapper}[{body}]" if cls == "col" and not split else body) + "\n"
        cur.append((x["b"], piece))
        if cls == "col" and not split and x["typ"] == "list" and s.startswith(("#list(", "#enum(")):
            frags = list(self.list_fragments(x["b"]))
            if splittable(frags):
                self.__dict__.setdefault("expansions", {})[piece] = ([inject(frags[0], f"#umark({lit(mid)}, \"s\")")] + frags[1:-1]
                                          + [frags[-1] + f"#umark({lit(mid)}, \"e\")"])
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
        if fig["id"] in self.figfit and w == "100%":
            # Figure fit (rulebook-layout skill 1.6): a full-width figure that would leave the page above it
            # largely bare is set just small enough to close it, never below FIG_FIT_FLOOR of its width.
            w = f"{self.figfit[fig['id']] * 100:.1f}%"
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
        if all(b.get("type") == "marker" for b, _ in pieces):
            # Only zero-size end markers remain (the unit ended in a full-width element). Any block
            # wrapper (columns, flowtail, even a zero-height block) placed after an element that fills
            # the page lands on a fresh page and keeps it, leaving a blank page before the next fresh
            # start; raw markers attach to the page they follow (local build 2026-11-01, pages 24, 53).
            for b, s in pieces:
                self.block_map.append((b["id"], b["src"], "column", None))
            self.out.append("".join(s for _, s in pieces) + "\n")
            return
        sid = self.seg_count
        self.seg_count += 1
        sig = segment_signature(pieces)
        self.seg_sigs[str(sid)] = sig
        entry = self.balance.get(str(sid))
        tail = entry[1] if valid_balance_entry(entry, sig) and entry[1] < len(pieces) and len(pieces) - entry[1] <= 60 else None
        if getattr(self, "flow_next_flush", False):
            tail = None                    # the segment that opens a shared opener page: natural flow
            self.flow_next_flush = False
        parts = []
        for j, (b, s) in enumerate(pieces):
            self.block_map.append((b["id"], b["src"], "column", sid))
            if b["type"] == "heading":
                self.piece_heads[f"{sid}:{j}"] = b["id"]
                # A complete column unit that opens with its heading (an ancestry, a Monster, an item)
                # is a whole piece. Only a bare heading glues to what follows; treating whole units as
                # bare merged every unit of a tail into one piece and walked the tail back to the
                # segment start, stranding short section openers (design review 2026-10-29, PDF p. 101).
                if not is_unit_piece(s):
                    self.bare_heads.add(f"{sid}:{j}")
                parts.append(s)
            else:
                parts.append(inject(s, f"#pm({sid}, {j}, \"s\")"))
                if b.get("type") == "para" and s.lstrip().startswith("#runin["):
                    # A bare bold run-in label ("AI Steps", "Special Rules:") introduces what follows, like a
                    # bare heading: the balance split may not fall right after it, and in a balanced tail it
                    # travels with the next piece. Otherwise it could close the flowing run while its content
                    # opened the balanced tail, stranded at a column foot (candidate 20261102T174706Z, p. 446).
                    self.bare_heads.add(f"{sid}:{j}")
        end = f"#place(pm({sid}, {len(pieces)}, \"e\"))"
        tp = []
        if tail is not None and tail < len(pieces):
            carry = ""
            for j in range(tail, len(parts)):
                if f"{sid}:{j}" in self.bare_heads and j < len(parts) - 1:
                    carry += parts[j]
                    continue
                if pieces[j][0].get("type") == "marker" and tp and not carry:
                    tp[-1] += parts[j]           # a zero-size end marker is never a balancing piece
                    continue
                sub = getattr(self, "expansions", {}).get(pieces[j][1])
                if sub:
                    # inside the balanced run the unit may split between its pieces; it stays on one page
                    tp.append(carry + inject(sub[0], f"#pm({sid}, {j}, \"s\")"))
                    tp.extend(sub[1:])
                else:
                    tp.append(carry + parts[j])
                carry = ""
            if carry:
                tp.append(carry)
        if len(tp) == 1 and is_rigid(tp[0]):
            # One whole unit cannot be balanced against anything. As a separate run it would start a new
            # column region below the segment's last column and could not use the empty column beside it
            # (design review 2026-10-29: Drakeblood fell to its own page beside an empty column).
            tp = []
        if not tp:
            self.out.append("#seg[" + "".join(parts) + end + "]\n#band-gap\n")
        else:
            if tail > 0:
                self.out.append("#seg[" + "".join(parts[:tail]) + "]\n#band-gap\n")
            tp[-1] = tp[-1] + end
            if all(not is_rigid(piece) for piece in tp):
                # Zero-size terminal markers do not turn a prose tail into a
                # whole-piece grid with an empty right column.
                self.out.append("#flowtail((" + ', '.join('[' + piece + ']' for piece in tp) + ",))\n")
            else:
                self.out.append("#bal(" + ", ".join("[" + x + "]" for x in tp) + ")\n")


def compile_book(variant="cream", out=None, query=True, edition="interior"):
    import subprocess
    out = out or BUILD / f"book-{variant}.pdf"
    qf = BUILD / "query.json"
    args = [sys.executable, str(ROOT / "tools/typst_run.py"), str(out), variant, edition] + ([str(qf)] if query else [])
    compile_book.last_warnings = []
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-3000:])
    compile_book.last_warnings = r.stderr.strip().splitlines()
    if compile_book.last_warnings:
        print(r.stderr.rstrip(), file=sys.stderr)
    dt = float(r.stdout.strip().splitlines()[-1])
    if query:
        q = json.loads(qf.read_text())
        return out, dt, (q["pm"], q["hpos"])
    return out, dt, None


STRADDLE_MAX = 250
MAX_TAIL_CHANGES = 5                     # within the cream build's 8 passes
TINY_TAIL_PT = float(LAYOUT_TOKENS.get("tiny_tail_pt", 180))   # D-02 d: a shorter last page pulls back
STANDFIRST_CHARS = 800                   # a run-on section's introduction set as a standfirst (about eight lines)
# Room a table split under its heading needs beyond its measured height: the repeated header in the
# second column and the row group that cannot divide at the column break.
SPLIT_RESERVE = 120
HEADING_ALLOWANCE = 24                   # a run-in section heading and its spacing (measured 21.2 pt at level 4)
SECTION_HEAD_PT = 54                     # a full-width numbered section head: its columns start 54 pt down (1.3, p. 12)
LEAD_RUN_CHARS = 2400                    # a section introduction short enough to balance on its opening page
TOP_Y = MARGIN_TOP_PT
FRAME_H = BODY_HEIGHT_PT
FRAME_FIT = FRAME_H - 12                 # measured component overhead and a documented boundary tolerance
BODY_BOTTOM = PAGE_HEIGHT_PT - MARGIN_BOTTOM_PT


def is_statline(k):
    """A short identification line of an entry: plain paragraph with "Label: value | Label: value" fields."""
    if "head" in k or k.get("typ") != "para" or k.get("kind") != "c":
        return False
    text = first_text_full(k["b"])
    return len(text) < 300 and " | " in text


def is_unit_piece(s):
    """True when a rendered piece is a complete keep unit rather than a bare heading."""
    return s.lstrip().startswith(("#keepcol[", "#keepfigure["))


def compute_balance(pm, prev, sigs, heads=None, hpos=None, bare=None, feet=None):
    """feet: optional callable, page -> {"left": y, "right": y} column feet measured from this pass's PDF
    (pages as the pm marks count them). It lets a tiny last page flow back into the page before it."""
    bare = set(heads or {}) if bare is None else bare
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
        pt = pt[1] if valid_balance_entry(pt, sigs.get(str(sid))) else None
        byp = {m["piece"]: m for m in starts}
        on_last = [m for m in starts if m["page"] == L]
        # A short last page (about a dozen lines in one column, or half that in a tail already balanced
        # over two) pulls back the piece that starts near the foot of the previous page; the run then
        # either fits that page or gives the last page a fuller close (design review 2026-10-29,
        # Scenario 1 tail). A natural run that merely spills into the second column is not short.
        balanced = pt is not None and pt in byp and byp[pt]["page"] == L
        # A piece straddles onto the last page only from the foot of the previous page's right column. One
        # starting at the foot of the left column continues in the right column beside it, and pulling back
        # one from near the top of a short column region (a run that opens below a full-width figure) empties
        # most of that column: the run then flows naturally (all-page review of candidate 19, p. 435).
        def straddles(m):
            first = byp.get(0)
            opens_here = first is not None and first is not m and first["page"] == m["page"] and first.get("x", 0) < PAGE_WIDTH_PT / 2
            top = first["y"] if opens_here else TOP_Y
            room = BODY_BOTTOM - m["y"]
            return (m["page"] == L - 1 and m.get("x", 0) >= PAGE_WIDTH_PT / 2 and room < STRADDLE_MAX
                    and room < 0.75 * (BODY_BOTTOM - top))
        in_first = end.get('x', 0) < PAGE_WIDTH_PT / 2
        tiny_tail = len(on_last) <= 5 and ((in_first and end['y'] < TOP_Y + TINY_TAIL_PT)
                                           or (balanced and not in_first and end['y'] < TOP_Y + TINY_TAIL_PT / 2))
        if (feet is not None and tiny_tail and on_last and on_last[0]["y"] < TOP_Y + 20
                and on_last[0].get("x", 0) < PAGE_WIDTH_PT / 2 and fits_back(feet, L)):
            # A tiny last page that opens with its own piece (nothing straddles onto it) flows back into the
            # right column of the page before when that column has room. A planned tail can never flow back,
            # so the plan kept the content on a page of its own (candidate 22, p. 392: Objective 20 alone,
            # under about 300 pt free). With no plan the run flows naturally, and the next pass balances it.
            continue
        first = byp.get(0)
        if (feet is not None and first is not None and first["page"] == L - 1 and first.get("x", 0) < PAGE_WIDTH_PT / 2
                and first["y"] < TOP_Y + 120 and run_fits_one_page(feet, L, first["y"])):
            # A short run that opens near the top of a page, whose unit was carried whole to the next page
            # (7.14 Poisons: the head and two lines, then 7.14.1 alone overleaf), is balanced from its first
            # piece on that first page when the whole of it fits there in two columns. Its units may split
            # between their pieces inside the balanced run, which stays on one page.
            res[str(sid)] = [sigs[str(sid)], 0]
            continue
        if pt is not None and pt in byp and byp[pt]["page"] == L and not tiny_tail:
            res[str(sid)] = [sigs[str(sid)], pt]
            continue
        if not on_last:
            lastp = starts[-1] if starts else None
            if lastp and straddles(lastp):
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
            if tiny_tail and straddles(prevp):
                t = prevp['piece']
            elif not at_top:
                if straddles(prevp) or prevp["page"] == L:
                    t = prevp["piece"]
                else:
                    continue
        res[str(sid)] = [sigs[str(sid)], t]
    for k, (sig, t) in list(res.items()):
        while t > 0 and f"{k}:{t-1}" in bare:
            t -= 1
        res[k] = [sig, t]
    return res


FIG_FIT_FLOOR = 0.80                     # rulebook-layout skill: a fitted figure keeps at least 80% of its width
FIG_FIT_SPACE = 14                       # the figure block's own space above it in the outer flow


MIN_TYPE_PT = float(json.loads((ROOT / "config/design_tokens.json").read_text())["type_pt"]["minimum_essential"])


def figure_geometry(fid):
    """(aspect, smallest scale) of a full-width figure: its drawn height over width, and the scale at which
    its smallest text reaches the minimum essential type size. Figures are drawn at 9 pt on a 504 pt
    measure and set at 525 pt, so they may shrink only to about 96%: below that, their labels fall under
    the type floor that layout_qa enforces. A figure whose type sizes cannot be read is not scaled."""
    svg = (ROOT / "figures/out" / f"{fid}.svg").read_text(encoding="utf-8")
    m = re.search(r'viewBox="[\d.]+ [\d.]+ ([\d.]+) ([\d.]+)"', svg[:600])
    if not m:
        return None, None
    width, height = float(m.group(1)), float(m.group(2))
    sizes = [float(x) for x in re.findall(r'font-size="([\d.]+)', svg)]
    type_floor = (MIN_TYPE_PT * width / (FULL_W * min(sizes))) if sizes else 1.0
    return height / width, max(FIG_FIT_FLOOR, type_floor)


def page_feet(pdf):
    """Column feet of a compiled pass, measured on demand, page by page (1-based, as the pm marks count).
    Without a readable PDF every page reads as unmeasured, which leaves the plan as it would be without."""
    cache, state = {}, {}
    def feet(page):
        if "doc" not in state:
            try:
                import pymupdf
                state["doc"] = pymupdf.open(str(pdf))
            except Exception:
                state["doc"] = None
        doc = state["doc"]
        if page not in cache:
            import layout_flow
            cache[page] = layout_flow.page_measures(doc[page - 1])["feet"] if doc is not None and 1 <= page <= len(doc) else {}
        return cache[page]
    return feet


def compute_figfit(pdf, positions, previous, candidates, excluded):
    """Figure fit (rulebook-layout skill 1.6 and 3.2, pass 1). A full-width figure carried whole to the top
    of a page leaves the page before it short. When the space left there holds the figure at FIG_FIT_FLOOR
    of its width or more, propose that scale; the figure stays where it was anchored, in its own section.
    A figure whose applied scale still left it on the next page keeps its full width (excluded)."""
    import pymupdf
    import layout_flow
    tbl = positions.get("<tblpos>", [])
    spans = {}
    for t in tbl:
        if t["id"] in candidates:
            spans.setdefault(t["id"], {})[t["edge"]] = t
    out = dict(previous)
    doc = None
    for fid, e in spans.items():
        if fid in excluded or "s" not in e or "e" not in e or e["s"]["page"] != e["e"]["page"]:
            continue
        top = e["s"]["y"] < TOP_Y + 4
        if not top:
            continue                       # it already shares a page with what precedes it
        if fid in previous:
            out.pop(fid, None)             # scaled, yet still carried over: the scale did not help
            excluded.add(fid)
            continue
        page = e["s"]["page"] - 1          # 1-based page before the figure
        if page < 1:
            continue
        doc = doc or pymupdf.open(str(pdf))
        boxes = layout_flow.body_boxes(doc[page - 1])
        if not boxes:
            continue
        end = max(b[0].y1 for b in boxes)
        room = BODY_BOTTOM - end - FIG_FIT_SPACE
        aspect, floor = figure_geometry(fid)
        if aspect is None:
            continue
        height = e["e"]["y"] - e["s"]["y"]
        image = aspect * FULL_W            # the drawing at full width; the caption below it does not scale
        caption = height - image
        need = (room - caption - 2) / image
        if floor <= need < 1:
            out[fid] = round(math.floor(need * 200) / 200, 3)
        # Too short at the floor: no proposal this pass. It is not excluded, because an early pass reads an
        # unbalanced layout; only a scale that was applied and still failed excludes the figure (a clean build,
        # as in CI, otherwise excluded FIG-14 and FIG-16 in its first pass).
    if doc is not None:
        doc.close()
    return out


def fits_back(feet, last):
    """True when the content of page `last`, set in one column, fits the free right column of the page before."""
    here, before = feet(last) or {}, feet(last - 1) or {}
    need = sum(here[s] - TOP_Y for s in ("left", "right") if here.get(s))
    free = BODY_BOTTOM - (before.get("right") or TOP_Y)
    return 0 < need and need + 12 <= free


def run_fits_one_page(feet, last, y0):
    """True when a run's content on the page before `last` (from y0 down) and on `last` would fit, balanced,
    in the two columns of that page below y0."""
    before, here = feet(last - 1) or {}, feet(last) or {}
    need = sum(before[s] - y0 for s in ("left", "right") if before.get(s) and before[s] > y0)
    need += sum(here[s] - TOP_Y for s in ("left", "right") if here.get(s))
    return 0 < need and need + 30 <= 2 * (BODY_BOTTOM - y0)


def stabilize_balance(proposed, previous, flips, excluded):
    """Use natural column flow for an oscillating tail, rather than freezing a proposal.

    Exclusions are explicit planner policy. The final emitted balance must equal
    a fresh proposal filtered by that policy; keeping a previous alternating
    variant alone is not convergence.
    """
    result = dict(proposed)
    for key in set(result) | set(previous):
        if result.get(key) != previous.get(key) and key not in excluded:
            # A tail that returns to a plan it already had is oscillating. A tail that keeps moving to
            # new plans is refining (a short last page pulls back one piece per pass) and may continue
            # up to a bounded number of changes (design review 2026-10-29, Scenario 2 tail).
            state = flips.setdefault(key, {'changes': 0, 'seen': [repr(previous.get(key))]})
            state['changes'] += 1
            value = repr(result.get(key))
            if value in state['seen'] or state['changes'] > MAX_TAIL_CHANGES:
                excluded.add(key)
            state['seen'].append(value)
    for key in excluded:
        result.pop(key, None)
    return result


def segment_signature(pieces):
    """Bind balance hints to rendered text/structure and the full layout profile."""
    value = {'pieces': [[b['id'], rendered] for b, rendered in pieces], 'profile': profile_dict()}
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return 'v2:' + hashlib.sha256(data).hexdigest()


def valid_balance_entry(entry, signature=None):
    return (isinstance(entry, (list, tuple)) and len(entry) == 2
            and isinstance(entry[0], str) and re.fullmatch(r'v2:[0-9a-f]{64}', entry[0]) is not None
            and (signature is None or entry[0] == signature)
            and type(entry[1]) is int and entry[1] >= 0)


def filtered_balance_plan(balance, signatures=None):
    if not isinstance(balance, dict):
        return {}
    return {key: list(value) for key, value in balance.items()
            if isinstance(key, str) and re.fullmatch(r'0|[1-9][0-9]*', key) is not None
            and valid_balance_entry(value)
            and (signatures is None or value[0] == signatures.get(key))}


def save_converged_balance(path, balance, signatures, converged):
    """Cache only the actually emitted plan and its current segment signatures."""
    if not converged:
        return False
    current = filtered_balance_plan(balance, signatures)
    path.write_text(json.dumps(current), encoding='utf-8', newline='\n')
    return True


def report_table_scope_policies(diagnostics):
    (MAP / 'table_scope_policies.json').write_text(
        json.dumps({'policies': diagnostics}, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8', newline='\n')
    for record in diagnostics:
        if record['status'] != 'matched':
            print(f"WARNING table width policy {record['policy']}: {record['status']}"
                  + (f" ({record['table_id']})" if record.get('table_id') else ''))


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
    ap.add_argument("--no-measurement-cache", action="store_true",
                    help="bypass measurement reuse and persisted balance hints")
    ap.add_argument("--variants-only", action="store_true", help="compile the digital edition from the current content.typ")
    ap.add_argument("--allow-nonconverged", action="store_true", help="diagnostic output only; final publication requires convergence")
    a = ap.parse_args()
    if a.variants_only:
        for v, ed, name in (("cream", "digital", "book-digital.pdf"),):
            out, dt, _ = compile_book(v, BUILD / name, query=False, edition=ed)
            print(f"{name}: {dt:.1f}s")
        return
    model = json.loads((BUILD / "blocks.json").read_text())
    balance = {}
    bal_file = BUILD / "balance.json"
    local_balance_exists = bal_file.exists()
    balance_cache_diagnostics = []
    if local_balance_exists and not a.no_balance:
        try:
            candidate = json.loads(bal_file.read_text())
            balance = filtered_balance_plan(candidate)
            balance_cache_diagnostics.append({'status': 'local', 'segments': len(balance),
                'discarded': len(candidate) - len(balance) if isinstance(candidate, dict) else 1})
        except (OSError, ValueError) as error:
            balance_cache_diagnostics.append({'status': 'invalid-local', 'reason': str(error)})
            print('WARNING ignoring unreadable balance plan: ' + str(error), file=sys.stderr)
    # measurement pass: classify keep units from their real rendered heights
    import subprocess
    try:
        probe = Book(model, balance)
    except TableScopePolicyError as error:
        report_table_scope_policies(error.diagnostics)
        raise
    report_table_scope_policies(probe.table_scope_diagnostics)
    probe.emit()
    (ROOT / "typst/measure.typ").write_text(
        '#import "heraldry.typ": *\n#show: book\n' + "".join(probe.measure_requests)
        + '\n#context { pdf.attach("/heraldry-unit-measurements.json", '
        'bytes(json.encode(query(<um>).map(m => m.value))), '
        'mime-type: "application/json", relationship: "supplement") }\n', encoding="utf-8", newline="\n")
    measure_args = [sys.executable, str(ROOT / "tools/measure_units.py")]
    if a.no_measurement_cache:
        measure_args.append('--no-cache')
    r = subprocess.run(measure_args, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-3000:])
    print(r.stdout.strip())
    binding_file = BUILD / 'unit_measure.binding.json'
    try:
        measurement_binding = json.loads(binding_file.read_text())
    except (OSError, ValueError):
        measurement_binding = {}
    if a.no_measurement_cache or a.no_balance:
        balance_cache_diagnostics.append({'status': 'disabled', 'reason': 'cache bypass or balancing disabled'})
    elif not local_balance_exists:
        balance = load_hint(ROOT, measurement_binding, diagnostics=balance_cache_diagnostics)
    else:
        balance_cache_diagnostics.append({'status': 'skipped-load', 'reason': 'local balance file present'})
    flips, pass_log, excluded = {}, [], set()
    fit_file = BUILD / "figfit.json"
    figfit = {} if a.no_balance or not fit_file.exists() else json.loads(fit_file.read_text())
    fit_excluded = set()
    converged = False
    compile_warnings = []
    for p in range(a.passes):
        book = Book(model, balance, figfit)
        (ROOT / "typst/content.typ").write_text(book.emit(), encoding="utf-8", newline="\n")
        out, dt, (pm, hpos) = compile_book(a.variant)
        query_file = BUILD / "query.json"
        positions = json.loads(query_file.read_text()).get("positions", {}) if query_file.exists() else {}
        new_fit = (compute_figfit(out, positions, figfit, book.full_figs, fit_excluded)
                   if positions and not a.no_balance else figfit)
        fit_changed = new_fit != figfit
        figfit = new_fit
        fit_file.write_text(json.dumps(figfit, indent=1, sort_keys=True))
        warnings = getattr(compile_book, 'last_warnings', [])
        warnings = list(warnings) if isinstance(warnings, (list, tuple)) else []
        compile_warnings.extend(warnings)
        new = (compute_balance(pm, balance, book.seg_sigs, book.piece_heads, hpos, book.bare_heads, feet=page_feet(out))
               if not a.no_balance else {})
        raw_changes = sum(1 for k in set(new) | set(balance) if new.get(k) != balance.get(k))
        new = stabilize_balance(new, balance, flips, excluded)
        changes = sum(1 for k in set(new) | set(balance) if new.get(k) != balance.get(k))
        pass_log.append({'pass': p + 1, 'compile_seconds': dt, 'segments': book.seg_count,
                         'balanced': len(new), 'changes': changes, 'raw_changes': raw_changes,
                         'warnings': warnings,
                         'natural_flow_segments': sorted(excluded)})
        print(f"pass {p+1}: {dt:.1f}s, segments={book.seg_count}, balanced={len(new)}, changed={sum(1 for k in set(new)|set(balance) if new.get(k)!=balance.get(k))}, fitted figures={len(figfit)}{' (changed)' if fit_changed else ''}")
        if (new == balance or a.no_balance) and not fit_changed:
            converged = True
            break
        for k, (sig, t) in list(new.items()):
            while t > 0 and f"{k}:{t-1}" in book.bare_heads:
                t -= 1
            new[k] = [sig, t]
        if p == a.passes - 1 or (new == balance and not fit_changed):
            converged = new == balance and not fit_changed
            break
        balance = new
        bal_file.write_text(json.dumps(balance))
    save_converged_balance(bal_file, balance, book.seg_sigs, converged)
    final_balance = filtered_balance_plan(balance, book.seg_sigs)
    if not a.no_measurement_cache and not a.no_balance:
        balance_cache_diagnostics.append(save_hint(ROOT, measurement_binding, final_balance,
            converged=converged, warnings=compile_warnings))
    MAP.mkdir(parents=True, exist_ok=True)
    (MAP / "tables.json").write_text(json.dumps(book.table_map, ensure_ascii=False, indent=0), encoding="utf-8", newline="\n")
    (MAP / "blocks.json").write_text(json.dumps(book.block_map, ensure_ascii=False), encoding="utf-8", newline="\n")
    import hashlib
    from source_units import source_unit_manifest
    manifest = source_unit_manifest(model, book.fig_slots)
    (BUILD / "units.json").write_text(json.dumps({"frame_fit_pt": FRAME_FIT, "units": book.unit_log,
        "balanced_leads": book.__dict__.get("lead_runs", []),
        "expected_unit_ids": [u['id'] for u in manifest], 'source_unit_manifest': manifest,
        "content_sha256": hashlib.sha256((ROOT / "typst/content.typ").read_bytes()).hexdigest()}))
    (BUILD / 'layout-build.json').write_text(json.dumps({'profile': profile_dict(), 'passes': pass_log,
        'converged': converged, 'natural_flow_segments': sorted(excluded),
        'balance_cache': balance_cache_diagnostics, 'warnings': compile_warnings,
        'table_scope_policies': book.table_scope_diagnostics,
        'seconds': round(time.perf_counter() - started, 3),
        'source_sha256': model['sha256'], 'content_sha256': hashlib.sha256((ROOT / 'typst/content.typ').read_bytes()).hexdigest()}, indent=2))
    if not converged and not a.allow_nonconverged:
        raise SystemExit('Layout balancing did not converge; diagnostic PDF preserved but cannot be published')
    print("links:", len(book.em.links), "->", out)


if __name__ == "__main__":
    main()
