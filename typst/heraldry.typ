// HERALDRY SKIRMISH — publication design system, v4 "Grim Heraldry" (owner-approved 2026-10-12/13).
// The look comes from templates/system.typ (the approved specimens); this file adapts it to the
// generated book: furniture derived from the document, the component signatures the generator
// emits, and the pagination machinery (pm, bal, keeppage, munit, tmark), which is unchanged.
// content.typ is generated from the protected manuscript.

#import "templates/system.typ" as v4
// Re-bound (not imported) so files that import this module with * see them too.
#let paper = v4.paper
#let ink = v4.ink
#let ink2 = v4.ink2
#let ink3 = v4.ink3
#let hair = v4.hair
#let tint = v4.tint
#let tint2 = v4.tint2
#let serif = v4.serif
#let sans = v4.sans
#let goth = v4.goth
#let fell = v4.fell
#let page-w = v4.page-w
#let page-h = v4.page-h
#let m-in = v4.m-in
#let m-out = v4.m-out
#let m-top = v4.m-top
#let m-bot = v4.m-bot
#let gap = v4.gap
#let frame-w = v4.frame-w
#let col-w = v4.col-w
#let body-size = v4.body-size
#let body-lead = v4.body-lead
#let brush = v4.brush
#let shield = v4.shield
#let arms = v4.arms
#let signature = v4.signature
#let coin = v4.coin
#let lozenge = v4.lozenge
#let tag = v4.tag
#let flourish = v4.flourish
#let corner = v4.corner
#let tab-keys = v4.tab-keys

#let frame-border = v4.opener-frame
#let lead-block = v4.lead-block
#let publication = json("../config/production.json")
#let tokens = json("../config/design_tokens.json")
#let substrate-name = v4.substrate-name
#let substrate = paper
#let body-bottom = page-h - m-bot

// Names kept for the front matter, covers and calibration sheet.
#let display = goth
#let rule-ink = ink3
#let band = tint
#let ring(size: 7pt, stroke: 0.7pt) = lozenge(size: size * 0.8)
#let taper(len: 60pt, weight: 1.6pt, dir: 1) = box(width: len, brush(weight: weight, seed: if dir == 1 { 1 } else { 2 }))
#let motif(len: 54pt) = flourish(len: len)

// ---------------------------------------------------------------- inline helpers
#let nb(s) = s   // placeholder (no-break handled in generator via U+00A0)
// Capitals on source text are small caps (smallcaps(all: true)), never upper(): the text layer keeps
// the source's letters, so reconciliation still matches. The coin mark replaces the source's "c" in tables; the letter stays in the text layer, invisibly,
// so reconciliation still finds every source cell (a typographic mapping, not a text change).
// The source letters stay under the coin as transparent glyphs stretched to its width, so the text
// layer reads exactly as the source ("16c", "Cost (c)") with no gap (a typographic mapping).
#let under-coin(src, s, fill) = context {
  let cw = measure(text(src)).width
  let target = measure(coin(s: s)).width
  if cw >= target {
    // wider source ("(c)"): keep the glyphs at full size and centre the coin over them
    box(width: cw, { place(center + bottom, dy: 0.1em, coin(s: s, fill: fill)); text(fill: rgb(0, 0, 0, 0%), src) })
  } else {
    box(width: target, {
      place(left + bottom, dy: 0.1em, coin(s: s, fill: fill))
      scale(x: target / cw * 100%, origin: left, reflow: true, text(fill: rgb(0, 0, 0, 0%), src))
    })
  }
}
#let coin-text(body, s: 0.82em, fill: ink) = {
  show regex("\(c\)"): it => under-coin("(c)", s, fill)
  show regex("(\d)c\b"): it => [#it.text.slice(0, -1)#h(0.8pt)#under-coin("c", s, fill)]
  body
}

// IM FELL has no bold: a strong run inside flavour is set in Source Serif bold italic (an italic
// face, so the flavour's emphasis run stays unbroken for reconciliation).
#let fell-body(body) = { show emph: it => it.body; show strong: it => text(font: serif, weight: 700, style: "italic", size: 0.93em, it.body); body }

// ---------------------------------------------------------------- chapter index (tabs and arms)
// Tab slot of a chapter opener: 1-11 for the numbered chapters, 12-14 for Appendices A-C, 15 Index.
#let tab-of(num) = {
  if num == none { return none }
  let s = if type(num) == str { num } else if num.has("text") { num.text } else { "" }
  let m = s.match(regex("^(\d+)\.$"))
  if m != none { return int(m.captures.at(0)) }
  let a = s.match(regex("^Appendix ([A-C])\.$"))
  if a != none { return 12 + "ABC".position(a.captures.at(0)) }
  none
}
#let opener-tab(v) = if type(v) == dictionary { v.tab } else if v == "index" { 15 } else { none }
#let words = ("One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven")

// ---------------------------------------------------------------- running furniture
#let chapter-pages = state("chapter-pages", ())
#let furniture-font = (font: sans, size: 7.4pt, fill: ink2, tracking: 0.16em)

#let current-heading(level) = {
  // Heading active at top of page; if a heading of that level starts on this page use it.
  let here-page = here().page()
  let on-page = query(heading.where(level: level)).filter(h => h.location().page() == here-page)
  if on-page.len() > 0 { return on-page.first() }
  let before = query(selector(heading.where(level: level)).before(here()))
  if before.len() > 0 { before.last() } else { none }
}
#let in-main(p) = {
  let fm = query(<mainmatter>)
  fm.len() > 0 and fm.first().location().page() <= p
}
#let opener-on(p) = query(<chapter-opener>).filter(m => m.location().page() == p)
#let current-tab(p) = {
  let os = query(<chapter-opener>).filter(m => m.location().page() <= p)
  if os.len() == 0 { none } else { opener-tab(os.last().value) }
}

#let header-content = context {
  let p = here().page()
  if opener-on(p).len() > 0 or not in-main(p) { return }
  let ch = current-heading(1)
  let sec = current-heading(2)
  let recto = calc.odd(p)
  let label = if not recto {
    if ch != none { ch.body }
  } else {
    if sec != none and (ch == none or sec.location().page() >= ch.location().page()) { sec.body } else if ch != none { ch.body }
  }
  let tab = current-tab(p)
  set text(font: sans, size: 9pt, weight: 600, tracking: 0.12em, fill: ink2)
  // the arms overlay the line (no added height), so the head stays clear of the 0.375 in edge
  let a = if tab != none { box(width: 15pt, height: 7pt, place(dy: -6pt, arms(tab, w: 15pt))) } else { lozenge(size: 4.4pt) }
  block(width: 100%, below: 0pt, {
    if recto [#h(1fr)#smallcaps(all: true, label)#h(6pt)#a] else [#a#h(6pt)#smallcaps(all: true, label)#h(1fr)]
    v(-1pt)
    line(length: 100%, stroke: 1.1pt + ink)
    v(-5.4pt)
    line(length: 100%, stroke: 0.35pt + ink)
  })
}

#let footer-content = context {
  let p = here().page()
  let fm = query(<frontmatter-start>)
  if fm.len() > 0 and p == fm.first().location().page() { return }
  if opener-on(p).filter(m => type(m.value) == dictionary).len() > 0 { return }   // the opener frame carries the folio
  let n = counter(page).display()
  let recto = calc.odd(p)
  let sh = shield(w: 23pt, inner: true, body: text(font: sans, size: 9pt, weight: 700, fill: paper, number-type: "lining", n))
  let b = box(width: 40pt, baseline: -6pt, brush(weight: 1.2pt, seed: p))
  if recto { align(right)[#b#h(5pt)#sh] } else { align(left)[#sh#h(5pt)#b] }
}

#let background-content = context {
  let p = here().page()
  let recto = calc.odd(p)
  let os = opener-on(p).filter(m => type(m.value) == dictionary)
  if os.len() > 0 {
    v4.opener-frame(recto, n: if in-main(p) { counter(page).display() })
  }
  if in-main(p) {
    let t = current-tab(p)
    if t != none { v4.thumb-tab(t, recto) }
  }
}

// ---------------------------------------------------------------- headings
#let section-rule = brush(weight: 2.2pt, seed: 4)
#let split-num(body) = {
  let s = if body.has("text") { body.text } else { none }
  if s == none { return (none, body) }
  let m = s.match(regex("^((?:\d+|[A-C])(?:\.\d+)+)\s+(.+)$"))
  if m == none { (none, body) } else { (m.captures.at(0), m.captures.at(1)) }
}

#let book(body) = {
  set document(title: publication.verified_publication_metadata.title + " — " + publication.verified_publication_metadata.version)
  set page(
    width: page-w, height: page-h,
    fill: substrate,
    margin: (inside: m-in, outside: m-out, top: m-top, bottom: m-bot),
    binding: left,
    header: header-content, header-ascent: 3pt,
    footer: footer-content, footer-descent: 7pt,
    background: background-content,
  )
  set text(font: serif, size: body-size, lang: "en", region: "CA", fill: ink,
    top-edge: 0.8em, bottom-edge: -0.25em, hyphenate: true, number-type: "lining",
    costs: (hyphenation: 100%, runt: 160%, widow: 1000%, orphan: 1000%))
  set par(leading: body-lead, spacing: 6.5pt, justify: true, first-line-indent: 0pt,
    justification-limits: (spacing: (min: 90%, max: 140%), tracking: (min: -0.005em, max: 0.02em)))
  set strong(delta: 200)
  set list(marker: (box(baseline: -1.2pt, lozenge(size: 4.4pt)), [–], [·]), indent: 1pt, body-indent: 6pt, spacing: 4.5pt)
  set enum(indent: 1pt, body-indent: 6pt, spacing: 4.5pt, numbering: n => text(font: sans, weight: 700, size: 9pt)[#n.])
  show list.item: it => block(breakable: false, it)
  show enum.item: it => block(breakable: false, it)
  set table(stroke: none)
  set heading(numbering: none)
  show heading: set text(hyphenate: false)
  show heading: set par(justify: false)

  // chapter title (H2 in the manuscript → level 1): set inside the opener
  show heading.where(level: 1): it => block(text(font: goth, weight: 600, size: 50pt, hyphenate: false, it.body))
  // numbered section: the number in an engraved shield, blackletter title, brush rule beneath
  show heading.where(level: 2): it => {
    let (num, title) = split-num(it.body)
    block(above: 16pt, below: 10pt, sticky: true, breakable: false, width: 100%)[
      #if num != none {
        grid(columns: (auto, 1fr), column-gutter: 9pt, align: horizon,
          shield(w: if num.len() > 3 { 30pt } else { 25pt }, inner: true, body: text(font: sans, weight: 700, size: 9pt, fill: paper, num)),
          text(font: goth, weight: 600, size: 21pt, top-edge: "cap-height", bottom-edge: "baseline", title))
      } else { text(font: goth, weight: 600, size: 21pt, title) }
      #v(5pt)
      #section-rule
    ]
  }
  // subsection: lozenge, quiet number, bold serif
  show heading.where(level: 3): it => {
    let (num, title) = split-num(it.body)
    block(above: 13pt, below: 5pt, sticky: true, breakable: false)[
      #set par(leading: 2.5pt)
      #lozenge(size: 5.5pt)#h(5pt)#if num != none [#text(font: sans, weight: 700, size: 9.5pt, fill: ink3, num)#h(5pt)]#text(font: serif, weight: 700, size: 12.5pt, title)
    ]
  }
  // minor named heading: blackletter
  show heading.where(level: 4): it => block(above: 11pt, below: 4pt, sticky: true, breakable: false,
    text(font: goth, weight: 600, size: 14.5pt, it.body))
  show link: it => it
  body
}

// ---------------------------------------------------------------- chapter opener
#let chapter-opener(num, title, anchor, lead: none, art: none) = {
  pagebreak(weak: true)
  let t = tab-of(num)
  block(width: 100%, above: 0pt, below: 14pt, breakable: false)[
    #metadata((anchor: anchor, tab: t)) <chapter-opener>
    #if art != none {
      let (file, w, h) = art
      align(center, image(file, width: calc.min(w, frame-w * 0.84)))   // never above native 300 ppi size
      v(-8pt)
    } else { v(0.9in) }
    #align(center)[
      #if t != none { arms(t, w: 52pt) }
      #v(-2pt)
      #if num != none {
        let s = if num.has("text") { num.text } else { "" }
        let m = s.match(regex("^(\d+)\.$"))
        text(font: sans, weight: 700, size: 10pt,
          smallcaps(all: true, if m != none { "Chapter " + s } else { s }))
        v(-6pt)
      }
      #heading(level: 1, outlined: true, bookmarked: true, title) #label(anchor)
      #v(-6pt)
      #flourish(len: 90pt)
    ]
    #if lead != none { v4.lead-block(fell-body(lead), width: 82%) }
  ]
}

// ---------------------------------------------------------------- segments
#let seg-gap = gap
#let pm(seg, piece, edge) = context [#metadata((seg: seg, piece: piece, edge: edge, page: here().page(), y: here().position().y.pt(), x: here().position().x.pt())) <pm>]

#let pmx(..args) = none
#let tmark(id, edge) = context [#metadata((id: id, edge: edge, page: here().page(), folio: counter(page).display())) <tblpos>]
#let ixm(k) = [#metadata(k) #label("ix-" + k)#context [#metadata((k: k, page: here().page(), folio: counter(page).display())) <ixpos>]]
// One summary of every labelled heading's position (balancing + index audit).
#let hpos-summary() = context [#metadata(query(heading).filter(h => h.has("label")).map(h => (
  id: str(h.label), page: h.location().page(), y: h.location().position().y.pt(), x: h.location().position().x.pt(),
  folio: counter(page).at(h.location()).first()))) <hpos>]
#let seg(body) = columns(2, gutter: gap, body)

// Balanced tail: pieces are top-level blocks that sat on one page in the previous pass.
// Height = min over split points k of max(stack(0..k), stack(k..n)): a guaranteed fit,
// after which Typst's own column flow balances further at line level.
// ---------------------------------------------------------------- keep units (one-page rule)
// Usable frame height of an empty page; units no taller than this must stay on one physical page.
#let frame-h = body-bottom - m-top
#let umark(id, edge) = context [#metadata((id: id, edge: edge, page: here().page(), y: here().position().y.pt())) <um-pos>]
// Column-fit unit: unbreakable inside the two-column flow.
#let keepcol(body) = {
  let b = block(breakable: false, width: 100%, above: 6pt, below: 6pt, body)
  // Typst force-places an unbreakable block into an empty column that is too short, so check
  // the remaining space here and again after one column break (at the new position).
  let fits() = measure(block(width: col-w, b)).height + 6pt <= body-bottom - here().position().y
  context {
    if not fits() { colbreak() }
    context {
      if not fits() { colbreak() }
      b
    }
  }
}
// Height of pieces laid out as a balanced two-column run (same search as `bal`).
#let bal-split(ps) = {
  // best split index k: minimises the taller of the two stacks
  let n = ps.len()
  let stack(a, b) = measure(block(width: col-w, { for p in ps.slice(a, b) { p } })).height
  let best = (stack(0, n), n)
  let lo = 1
  let hi = n - 1
  while lo <= hi {
    let k = calc.div-euclid(lo + hi, 2)
    let a = stack(0, k)
    let b = stack(k, n)
    if calc.max(a, b) < best.at(0) { best = (calc.max(a, b), k) }
    if a < b { lo = k + 1 } else { hi = k - 1 }
  }
  best
}
#let bal-height(ps) = bal-split(ps).at(0) + 4pt
// Balanced two-column run built from whole pieces: no flow, so it can never overflow.
#let balcols(ps) = context {
  let (h, k) = bal-split(ps)
  block(width: 100%, above: 0pt, below: 8pt, breakable: false,
    grid(columns: (col-w, col-w), column-gutter: gap,
      { for p in ps.slice(0, k) { p } }, { for p in ps.slice(k) { p } }))
}
#let bal(..pieces) = context {
  let ps = pieces.pos()
  let avail = body-bottom - here().position().y
  if ps.len() < 2 { columns(2, gutter: gap, { for p in ps { p } }); return }
  let (h, k) = bal-split(ps)
  if h + 6pt > avail {
    columns(2, gutter: gap, { for p in ps { p } })
  } else {
    block(width: 100%, above: 0pt, below: 8pt, breakable: false,
      grid(columns: (col-w, col-w), column-gutter: gap,
        { for p in ps.slice(0, k) { p } }, { for p in ps.slice(k) { p } }))
  }
}

#let full(body) = block(width: 100%, above: 8pt, below: 10pt, body)
// Prose-only run: real flowing columns at half the stacked height plus three lines of slack.
#let flow-height(ps) = measure(block(width: col-w, { for p in ps { p } })).height / 2 + 40pt
// A run holding only position markers (no visible content) takes no space, so it can never push an
// empty page before a section break.
#let flowcols(ps) = context {
  if measure(block(width: col-w, { for p in ps { p } })).height < 1pt { for p in ps { p } }
  else { block(width: 100%, height: flow-height(ps), above: 0pt, below: 8pt, breakable: false,
    columns(2, gutter: gap, { for p in ps { p } })) }
}
// Page-fit unit: one unbreakable composition (balanced column runs and full-width parts).
#let keeppage(id: none, ..parts) = block(breakable: false, width: 100%, above: 0pt, below: 10pt, {
  if id != none { umark(id, "s") }
  for (kind, body) in parts.pos() {
    if kind == "c" { balcols(body) } else if kind == "p" { flowcols(body) } else { block(width: 100%, above: 6pt, below: 8pt, body) }
  }
  if id != none { umark(id, "e") }
})
// Measurement record for the build's classification pass.
#let munit(id, parts) = context {
  let cols = parts.filter(p => p.at(0) != "f")
  let h1 = if cols.len() == parts.len() {
    measure(block(width: col-w, { for (_, ps) in parts { for p in ps { p } } })).height.pt()
  } else { 1e9 }
  let h2 = parts.map(((kind, body)) => if kind == "c" { bal-height(body).pt() + 8 } else if kind == "p" { flow-height(body).pt() + 8 } else {
    measure(block(width: frame-w, body)).height.pt() + 14 }).sum()
  [#metadata((id: id, h1: h1, h2: h2)) <um>]
}


// ---------------------------------------------------------------- body components
// A short paragraph directly after a heading is kept whole (no 1-line orphan under a heading).
#let keep(body) = block(breakable: false, above: 6pt, below: 6pt, body)
// Glossary entry: hanging indent so each bold term stands at the margin.
#let gloss(body) = block(above: 5pt, below: 5pt, par(hanging-indent: 9pt, justify: false, body))
// A paragraph that is only a bold label acts as a minor heading: keep it with what follows.
#let runin(body) = block(sticky: true, above: 6pt, below: 6pt, body)
// Flavour: IM FELL roman at the running size, justified (the source marks it with emphasis).
#let flavour(body) = block(above: 5pt, below: 9pt, v4.flavour-set(fell-body(body)))
// generated pen-and-ink spot art (transparent ink, so the page substrate shows through)
#let spotart(path, w) = block(width: 100%, above: 4pt, below: 2pt, breakable: false, align(center, image(path, width: w)))

// Worked example and rules note: one panel (tinted field, black spine). The source's own label
// ("Example:", "Recommended First Party:") leads in bold, so no word is added or repeated.
#let panel(body) = block(width: 100%, above: 10pt, below: 11pt, breakable: true,
  fill: tint, stroke: (left: 2.6pt + ink), inset: (left: 11pt, right: 9pt, top: 8pt, bottom: 9pt))[
  #set par(justify: true)
  #body
]
#let example(body, pre: none) = panel({
  show regex("^Example( [^:]{0,40})?:"): it => strong(it)
  body
})
#let note-box(body) = panel(body)

#let hr-ornament(pre: none) = align(center, block(above: 10pt, below: 10pt)[#pre#flourish(len: 40pt)])

// ---------------------------------------------------------------- tables: the ledger
#let tcell(body, header: false) = {
  if header { text(font: sans, weight: 700, size: 9.3pt, fill: paper, body) } else { body }
}
#let head-cell(h) = text(font: sans, weight: 700, size: 9.3pt, fill: paper,
  coin-text(smallcaps(all: true, h), s: 1.05em, fill: paper))

#let htable(id, widths, aligns, header, rows, kind: "table", title: none, pre: none) = {
  set text(font: sans, size: 9.3pt, top-edge: 0.8em, bottom-edge: -0.25em, number-type: "lining", number-width: "tabular", hyphenate: false)
  set par(leading: 2.7pt, spacing: 4pt, justify: false)
  set strong(delta: 200)
  let al(x) = { let a = aligns.at(x); if a == left { left } else { center } }
  set table.cell(breakable: false)   // keep ordinary rows intact
  block(width: 100%, above: 10pt, below: 12pt, breakable: true)[
    #pre#metadata(id) #label("tbl-" + id)#tmark(id, "s")
    // the opening (rule, header band and about two rows) never splits from the heading above it
    #block(breakable: false, height: 64pt, above: 0pt, below: 0pt, brush(weight: 2.2pt, seed: 3))
    #v(-64pt + 2.2pt - 2.2pt)
    #coin-text(table(
      columns: widths.map(w => w * 1pt),
      align: (x, y) => al(x) + horizon,
      inset: (x: 5pt, y: 4pt),
      fill: (x, y) => if y == 0 { ink } else if calc.even(y) { tint } else { none },
      stroke: (x, y) => (bottom: if y == 0 { none } else { 0.35pt + hair }),
      table.header(repeat: true, ..header.enumerate().map(((x, h)) => table.cell(align: al(x) + horizon, head-cell(h)))),
      ..rows.map(r => r.enumerate().map(((x, c)) => if x == 0 and aligns.at(0) == left { strong(c) } else { c })).flatten(),
    ))
    #v(-1pt)
    #brush(weight: 2.2pt, seed: 5)
    #tmark(id, "e")
  ]
}

// Monster stat strip: black header band, large centred values, a brush beneath.
#let statstrip(id, header, values, pre: none) = {
  set text(font: sans, number-type: "lining", number-width: "tabular", hyphenate: false)
  block(width: 100%, above: 7pt, below: 8pt, breakable: false)[
    #pre#pre#metadata(id) #label("tbl-" + id)#tmark(id, "s")#tmark(id, "e")
    #coin-text(table(
      columns: (1fr,) * header.len(),
      align: center + horizon,
      inset: (x, y) => (x: 2pt, y: if y == 0 { 3pt } else { 4.5pt }),
      fill: (x, y) => if y == 0 { ink } else { none },
      stroke: (x, y) => (left: if y == 1 and x > 0 { 0.35pt + hair } else { none }),
      table.header(..header.map(h => text(weight: 700, size: 9pt, fill: paper, smallcaps(all: true, h)))),
      ..values.map(v => text(weight: 600, size: 12pt, v)),
    ), s: 0.8em)
    #v(-2pt)
    #brush(weight: 2pt, seed: 7)
  ]
}

// Labelled key/value profile (stat tables whose cells hold formulas): reversed key column.
#let statcard(id, header, values, pre: none) = {
  set text(font: sans, size: 9.3pt, top-edge: 0.8em, bottom-edge: -0.25em, number-type: "lining")
  set par(justify: false)
  block(width: 100%, above: 7pt, below: 8pt, breakable: false)[
    #pre#pre#metadata(id) #label("tbl-" + id)#tmark(id, "s")#tmark(id, "e")
    #coin-text(table(
      columns: (auto, 1fr),
      inset: (x: 6pt, y: 3.6pt),
      fill: (x, y) => if x == 0 { ink } else if calc.odd(y) { tint } else { none },
      stroke: (x, y) => (bottom: if x == 1 { 0.35pt + hair } else { none }),
      ..header.zip(values).map(((h, v)) => (text(weight: 700, size: 9pt, fill: paper, smallcaps(all: true, h)), v)).flatten(),
    ))
    #v(-1pt)
    #brush(weight: 2pt, seed: 9)
  ]
}

// Prose-heavy many-column tables: one labelled entry per source row.
#let cards(id, entries, title-label: none, pre: none) = {
  block(width: 100%, above: 8pt, below: 10pt, breakable: true)[
    #pre#metadata(id) #label("tbl-" + id)#tmark(id, "s")
    #block(breakable: false, height: 54pt, above: 0pt, below: 0pt, brush(weight: 2.2pt, seed: 11))
    #v(-54pt + 2.2pt)
    #coin-text(for e in entries {
      block(width: 100%, above: 0pt, below: 0pt, breakable: true, inset: (top: 5pt, bottom: 6pt),
        stroke: (bottom: 0.35pt + hair))[
        #set par(leading: 2.8pt, spacing: 3pt, justify: false)
        #block(sticky: true, below: 3pt)[
          #set text(font: sans, size: 10pt)
          #e.title
        ]
        #if e.fields.len() > 0 {
          set text(font: sans, size: 9.3pt, number-type: "lining")
          block(below: 3pt, e.fields.map(((k, v)) => box[#text(weight: 700, size: 9.3pt, fill: ink3, smallcaps(all: true, k))#h(3pt)#v]).join(h(9pt, weak: true)))
        }
        #for (k, v) in e.desc {
          block(below: 2pt)[#text(font: sans, size: 9.3pt, weight: 700, fill: ink3, smallcaps(all: true, k)) #h(2pt) #text(size: 10pt, v)]
        }
      ]
    })
    #brush(weight: 2.2pt, seed: 13)
    #tmark(id, "e")
  ]
}

// ---------------------------------------------------------------- figures
// Caption welded to the figure: a black band with the number, the caption beneath, a rule.
#let figure-block(id, file, caption, width: 100%, anchor: none, pre: none) = block(width: 100%, above: 10pt, below: 12pt, breakable: false)[
  #pre#metadata(id) #label("fig-" + id)#tmark(id, "s")
  #align(center, image(file, width: width))
  #v(4pt)
  #block(width: 100%, fill: ink, inset: (x: 7pt, y: 3.6pt), spacing: 0pt,
    text(font: sans, size: 9pt, weight: 700, fill: paper)[#id])
  #block(width: 100%, inset: (x: 6pt, top: 4.5pt, bottom: 5pt), spacing: 0pt, {
    set text(font: sans, size: 9pt, fill: ink)
    set par(leading: 2.5pt, justify: false)
    caption
  })
  #line(length: 100%, stroke: 0.6pt + ink)
]
