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
#let table-size = v4.table-size
#let table-lead = v4.table-lead
#let table-x = v4.table-x
#let table-y = v4.table-y
#let space-token = v4.space-token
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

// Names kept for the front matter and covers.
#let display = goth
#let band = tint
#let motif(len: 54pt) = flourish(len: len)

// ---------------------------------------------------------------- inline helpers
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
  show regex("\b\d[\d,]*c\b"): it => box[#it.text.slice(0, -1)#h(0.8pt)#under-coin("c", s, fill)]
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

// A scenario identity remains active until another heading of its rank or higher.
// Running furniture cannot alter the body flow or introduce a manuscript label.
#let heading-scope(rank, title, anchor, body) = {
  // Keep metadata outside the source heading body, which is also reused by
  // numbered-title styling and running furniture. Resolve the real heading
  // anchor: this zero-height wrapper can otherwise remain on the prior page.
  if rank <= 4 { context {
    let targets = query(label(anchor))
    if targets.len() > 0 { [#metadata((rank: rank,
      title: if title.match(regex("^Scenario \d+:")) != none { title } else { none },
      page: targets.first().location().page())) <scenario-boundary>] }
  } }
  body
}
#let ongoing-scenario(p) = {
  let events = query(<scenario-boundary>).filter(m => m.value.page <= p)
  let candidates = events.filter(m => m.value.title != none and m.value.page < p)
  if candidates.len() == 0 { return none }
  let scenario = candidates.last()
  let later = events.slice(events.position(m => m.location() == scenario.location()) + 1)
  if later.any(m => m.value.rank <= scenario.value.rank) { return none }
  let chapter = current-heading(1)
  if chapter != none and chapter.location().page() > scenario.value.page { return none }
  scenario
}
#let scenario-continuation-title(scenario) = {
  let words = scenario.value.title.split(" ")
  let title = scenario.value.title + " (continued)"
  let width = frame-w - 21pt
  let extent(s) = measure(text(font: sans, size: tokens.type_pt.navigation * 1pt,
    weight: 600, tracking: 0.12em, smallcaps(all: true, s))).width
  while extent(title) > width and words.len() > 2 {
    let _ = words.pop()
    title = words.join(" ") + "... (continued)"
  }
  title
}

#let header-content = context {
  let p = here().page()
  if opener-on(p).len() > 0 or not in-main(p) { return }
  let ch = current-heading(1)
  let sec = current-heading(2)
  let recto = calc.odd(p)
  let ordinary-label = if not recto {
    if ch != none { ch.body }
  } else {
    if sec != none and (ch == none or sec.location().page() >= ch.location().page()) { sec.body } else if ch != none { ch.body }
  }
  let scenario = ongoing-scenario(p)
  let label = if scenario != none { scenario-continuation-title(scenario) } else { ordinary-label }
  let tab = current-tab(p)
  set text(font: sans, size: tokens.type_pt.navigation * 1pt, weight: 600, tracking: 0.12em, fill: ink2)
  // The arms overlay the line (no added height), standing on the rule level with the label. Their own 17 pt frame
  // matters: an image laid out in the 7 pt box fills it with fit "cover" and is cropped to a 7 pt band.
  let a = if tab != none { box(width: 15pt, height: 7pt, place(dy: 4pt, box(height: 17pt, arms(tab, w: 15pt)))) } else { lozenge(size: 4.4pt) }
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
  let sh = shield(w: 23pt, inner: true, body: text(font: sans, size: tokens.type_pt.navigation * 1pt, weight: 700, fill: paper, number-type: "lining", n))
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
// Bracketed role or kicker closing an entry heading ("[Elite]", "[2/5 Complexity]", "[Intro]"): set as the
// banner tag of the design system (D-06 step 2). The brackets stay in the text layer as transparent
// glyphs inside the tag and the role is small caps, so the extracted heading still reads exactly as
// the source; nothing is added to or removed from the manuscript's words.
#let role-tag(s) = box(baseline: 22%, {
  let inner = s.slice(1, s.len() - 1)
  let size = tokens.type_pt.tag * 1pt
  let hidden(c) = text(font: sans, weight: 700, size: size, fill: rgb(0, 0, 0, 0%), c)
  let t = [#hidden("[")#text(font: sans, weight: 700, size: size, tracking: 0.1em, fill: paper, smallcaps(all: true, inner))#hidden("]")]
  context {
    let m = measure(t)
    let h = m.height + 5pt
    let w = m.width + 9pt
    box(width: w, height: h, {
      place(polygon(fill: ink, (0pt, 0pt), (w - 4.5pt, 0pt), (w, h / 2), (w - 4.5pt, h), (0pt, h)))
      place(left + horizon, dx: 2.5pt, t)
    })
  }
})
#let role-pattern = regex("\[[^\]]+\]$")
// The reference appendix sets its section heads as the iron reference band (docs/DESIGN.md 6.19).
#let reference-band(num) = tokens.layout.reference_band_chapters.len() > 0 and num.match(regex("^C\.\d+$")) != none
// A numbered section head spans the frame (D-01): the composer emits it in the outer flow ahead of its
// columns, sticky to them, so a head never ends a page on its own.
#let section-head(body) = block(width: 100%, above: 0pt, below: 0pt, sticky: true, breakable: false, body)
// A run-on section head (D-02 c) relies on `sticky` to travel with its columns; the composer decides
// fresh pages and opener sharing from measured heights, never from a position read during layout,
// because such reads lag one layout iteration and chained with the opener centring and the tailpiece
// probes they exceeded Typst's five iterations (first local build, 2026-11-01).

#let book(body) = {
  let meta = publication.verified_publication_metadata
  set document(title: meta.title + ", " + meta.version, author: meta.author_credit,
    keywords: ("Heraldry Skirmish", "tabletop miniature skirmish", "rulebook", meta.publisher))
  set smartquote(enabled: false)   // style lock: straight quotes and inch marks
  set page(
    width: page-w, height: page-h,
    fill: substrate,
    margin: (inside: m-in, outside: m-out, top: m-top, bottom: m-bot),
    binding: left,
    header: header-content, header-ascent: 3pt,
    footer: footer-content, footer-descent: 2pt,
    background: background-content,
  )
  set text(font: serif, size: body-size, lang: "en", region: "CA", fill: ink,
    top-edge: 0.8em, bottom-edge: -0.25em, hyphenate: true, overhang: false, number-type: "lining",
    costs: (hyphenation: 100%, runt: 160%, widow: 1000%, orphan: 1000%))
  set par(leading: body-lead, spacing: v4.par-space, justify: true, first-line-indent: 0pt,
    justification-limits: (spacing: (min: 85%, max: 140%), tracking: (min: -0.02em, max: 0.02em)))
  set strong(delta: 200)
  set list(marker: (box(baseline: -1.2pt, lozenge(size: 4.4pt)), [–], [·]), indent: 1pt, body-indent: 6pt, spacing: v4.list-space)
  set enum(indent: 1pt, body-indent: 6pt, spacing: v4.list-space, numbering: n => text(font: sans, weight: 700, size: 9pt)[#n.])
  show list.item: it => block(breakable: false, it)
  show enum.item: it => block(breakable: false, it)
  set table(stroke: none)
  set heading(numbering: none)
  show heading: set text(hyphenate: false)
  show heading: set par(justify: false)

  // chapter title (H2 in the manuscript → level 1): set inside the opener
  show heading.where(level: 1): it => block(text(font: goth, weight: 600, size: tokens.type_pt.chapter * 1pt, hyphenate: false, it.body))
  // numbered section: the number in an engraved shield, blackletter title, brush rule beneath
  show heading.where(level: 2): it => {
    let (num, title) = split-num(it.body)
    block(above: space-token.section_before * 1pt, below: space-token.section_after * 1pt, sticky: true, breakable: false, width: 100%)[
      #if num != none and reference-band(num) {
        // Appendix C: the code in a paper shield, the title reversed, and the RULES REFERENCE label
        // (D-06 step 1); a fine rule closes the band.
        block(width: 100%, fill: ink, inset: (x: 10pt, y: 6pt), spacing: 0pt,
          grid(columns: (auto, 1fr, auto), column-gutter: 9pt, align: horizon,
            shield(w: if num.len() > 3 { 30pt } else { 25pt }, fill: paper, body: text(font: sans, weight: 700, size: 9pt, fill: ink, num)),
            text(font: goth, weight: 600, size: tokens.type_pt.reference_band * 1pt, fill: paper, title),
            text(font: sans, weight: 700, size: tokens.type_pt.navigation * 1pt, tracking: 0.12em, fill: paper, smallcaps(all: true, "Rules Reference"))))
        v(1.5pt)
        line(length: 100%, stroke: tokens.line_pt.reference_band_rule * 1pt + ink)
      } else if num != none {
        grid(columns: (auto, 1fr), column-gutter: 9pt, align: horizon,
          shield(w: if num.len() > 3 { 30pt } else { 25pt }, inner: true, body: text(font: sans, weight: 700, size: 9pt, fill: paper, num)),
          text(font: goth, weight: 600, size: tokens.type_pt.section * 1pt, top-edge: "cap-height", bottom-edge: "baseline", title))
      } else { text(font: goth, weight: 600, size: tokens.type_pt.section * 1pt, title) }
      #if num == none or not reference-band(num) {
        v(5pt)
        section-rule
      }
    ]
  }
  // subsection: lozenge, quiet number, bold serif
  show heading.where(level: 3): it => {
    let (num, title) = split-num(it.body)
    show role-pattern: m => role-tag(m.text)
    block(above: space-token.subsection_before * 1pt, below: space-token.subsection_after * 1pt, sticky: true, breakable: false)[
      #set par(leading: 2.5pt)
      #lozenge(size: 5.5pt)#h(5pt)#if num != none [#text(font: sans, weight: 700, size: tokens.type_pt.subsection_number * 1pt, fill: ink3, num)#h(5pt)]#text(font: serif, weight: 700, size: tokens.type_pt.subsection * 1pt, title)
    ]
  }
  // minor named heading: blackletter, one step below the subsection in size (D-04)
  show heading.where(level: 4): it => {
    show role-pattern: m => role-tag(m.text)
    block(above: space-token.minor_before * 1pt, below: space-token.minor_after * 1pt, sticky: true, breakable: false,
      text(font: goth, weight: 600, size: tokens.type_pt.minor * 1pt, it.body))
  }
  show link: it => it
  body
}

// ---------------------------------------------------------------- chapter opener
// Marks the end of a chapter's opening flavour (emitted by the composer after the last opening block).
// A zero-height block keeps the mark where the flavour ends; a bare metadata tag would travel with the
// next block onto the next page and report an overflow that did not happen.
// `solo`: true when the composer found that the first section after the introduction starts a fresh
// page; "auto" when the first section follows directly and may or may not fit beside the opener.
// A solo opener page holds nothing but the opener and its introduction.
#let solo-intro(end) = {
  let s = if type(end.value) == dictionary { end.value.at("solo", default: false) } else { false }
  if s == "auto" {
    let hs = query(selector(heading).after(end.location()))
    hs.len() > 0 and hs.first().location().page() > end.location().page()
  } else { s == true }
}
#let intro-end(solo: false) = {
  block(height: 0pt, above: 0pt, below: 0pt, sticky: false)[#metadata((solo: solo)) <intro-end>]
  context {
    let os = query(selector(<chapter-opener>).before(here()))
    let ends = query(selector(<intro-end>).before(here()))
    if os.len() > 0 and type(os.last().value) == dictionary and ends.len() > 0 {
      let o = os.last()
      // On an opener spread the introduction page is centred, like the display page it faces.
      if o.value.at("spread", default: false) { v(1fr) }
      // A solo opener page is set as a composed chapter title page: the art, title, and introduction
      // sit at the optical centre of the frame instead of leaving the lower half empty.
      // The mark's own page decides: this context yields only spacing, so its location tag travels
      // to the next block, which on a solo page is already on the following page.
      else if solo-intro(ends.last()) and o.location().page() == ends.last().location().page() { v(1.4fr) }
    }
  }
}
// The opener's display (art, arms, label, title, flourish). `title-element` is the real level-1
// heading in the book; the composer measures the same display with a plain title of the same size to
// decide whether the first section shares the opener page (D-02 b).
#let opener-display(num, title, art: none, title-element: none) = {
  let t = tab-of(num)
  if art != none {
    let (file, w, h) = art
    align(center, image(file, width: calc.min(w, frame-w * 0.84)))   // never above native 300 ppi size
    v(-8pt)
  } else { v(0.9in) }
  align(center)[
    #if t != none { arms(t, w: 52pt) }
    #v(-2pt)
    #if num != none {
      let s = if num.has("text") { num.text } else { "" }
      let m = s.match(regex("^(\d+)\.$"))
      // "Chapter One" (D-09). The source's own number token ("1.") stays in the text layer as
      // transparent glyphs in a zero-width box on the same line, so the extracted heading still
      // reads "1. The World of Heraldry" for reconciliation.
      let shown = if m != none { "Chapter " + words.at(int(m.captures.at(0)) - 1) } else { s.trim(".", at: end) }
      let keep = if m != none { s } else { "." }
      text(font: sans, weight: 700, size: 10pt)[#smallcaps(all: true, shown)#box(width: 0pt, text(fill: rgb(0, 0, 0, 0%))[ #keep])]
      v(-6pt)
    }
    #if title-element != none { title-element } else { block(text(font: goth, weight: 600, size: tokens.type_pt.chapter * 1pt, hyphenate: false, title)) }
    #v(-6pt)
    #flourish(len: 90pt)
  ]
}
// Measurable opener: the display and the lead, as the book sets them, without page breaks or marks.
#let opener-body(num, title, art: none, lead: none) = {
  opener-display(num, title, art: art)
  if lead != none { v4.lead-block(fell-body(lead), width: 82%) }
}
#let chapter-opener(num, title, anchor, lead: none, art: none) = {
  pagebreak(weak: true)
  let t = tab-of(num)
  let display = opener-display(num, title, art: art, title-element: [#heading(level: 1, outlined: true, bookmarked: true, title) #label(anchor)])
  // An introduction too long to share the opener page would end on a mostly empty page before the
  // first section's fresh page. Such a chapter opens as a spread instead: a display page with the art
  // and title, centred, then the whole introduction on the facing page (design review 2026-10-29).
  context {
    let ends = query(selector(<intro-end>).after(here()))
    let spread = ends.len() > 0 and ends.first().location().page() > here().page()
    if spread {
      block(width: 100%, height: body-bottom - m-top - 1pt, above: 0pt, below: 0pt, breakable: false, {
        [#metadata((anchor: anchor, tab: t, spread: true)) <chapter-opener>]
        v(1fr)
        display
        v(1.3fr)
      })
      pagebreak()
      v(1fr)
      if lead != none { v4.lead-block(fell-body(lead), width: 82%) }
    } else {
      if ends.len() > 0 and solo-intro(ends.first()) { v(1fr) }
      block(width: 100%, above: 0pt, below: 14pt, breakable: false, {
        [#metadata((anchor: anchor, tab: t)) <chapter-opener>]
        display
        if lead != none { v4.lead-block(fell-body(lead), width: 82%) }
      })
    }
  }
}

// ---------------------------------------------------------------- segments
#let pm(seg, piece, edge) = context [#metadata((seg: seg, piece: piece, edge: edge, page: here().page(), y: here().position().y.pt(), x: here().position().x.pt())) <pm>]

#let pmx(..args) = none
#let tmark(id, edge) = context [#metadata((id: id, edge: edge, page: here().page(), folio: counter(page).display(), x: here().position().x.pt(), y: here().position().y.pt())) <tblpos>]
#let ixm(k) = [#metadata(k) #label("ix-" + k)#context [#metadata((k: k, page: here().page(), folio: counter(page).display())) <ixpos>]]
// One summary of every labelled heading's position (balancing + index audit).
#let hpos-summary() = context {
  [#metadata(query(heading).filter(h => h.has("label")).map(h => (
    id: str(h.label), page: h.location().page(), y: h.location().position().y.pt(), x: h.location().position().x.pt(),
    level: h.level, outlined: h.outlined, bookmarked: h.bookmarked,
    folio: counter(page).at(h.location()).first()))) <hpos>]
  // Serialized with the very PDF whose layout these positions describe.
  pdf.attach("/heraldry-positions.json", bytes(json.encode((
    schema: 1, identity: json(bytes(sys.inputs.at("position-identity", default: "{}"))),
    positions: (
      "<pm>": query(<pm>).map(x => x.value),
      "<tblpos>": query(<tblpos>).map(x => x.value),
      "<ixpos>": query(<ixpos>).map(x => x.value),
      "<hpos>": query(<hpos>).map(x => x.value),
      "<um-pos>": query(<um-pos>).map(x => x.value),
    ),
  ))), mime-type: "application/json", relationship: "supplement")
}
// Stacked column bands (all-page review 2026-11-06): where a two-column band starts directly beneath another
// on the same page, a full-width hairline in the gap between them marks the boundary, so the columns read band
// by band. Both hooks sit inside the band's own block and are placed, so they take no height and move nothing.
#let band-top = place(top + left, context {
  let prev = query(selector(<band-end>).before(here()))
  if prev.len() > 0 {
    let e = prev.last().location().position()
    let p = here().position()
    let gap = p.y - e.y
    // A fixed band's end marker sits at the foot of its block, below the block's own slack: where the next
    // band abuts it, the rule goes in that slack. A natural flow's marker sits on its last line, so its rule
    // needs the gap `band-gap` leaves; with none (the flow ends in the left column) the next band continues
    // that column and takes no rule (all-page review of candidate 19, pp. 218, 402, 419, 485, 490).
    let fixed = prev.last().value == "fixed"
    let dy = if gap > 1pt and (fixed or gap >= 4pt) { -gap / 2 } else if fixed { -6.5pt } else { none }
    if e.page == p.page and gap >= 0pt and gap < 14pt and dy != none {
      place(dy: dy, line(length: 100%, stroke: 0.5pt + v4.hair))
    }
  }
})
#let band-end = place(bottom + left, [#metadata("fixed") <band-end>])
#let flow-end = place[#metadata("flow") <band-end>]
// `seg-last` records where a natural flow's text ends: in which column, and on which page.
#let seg(body) = block(width: 100%, breakable: true, {
  band-top; columns(2, gutter: gap, { body; [#metadata("seg") <seg-last>] }); flow-end
})
// After a natural flow. When its last lines stand in the right column of the page that follows on, whatever
// comes next is a second band beneath both columns: it starts the band gap lower (as after a fixed band), so
// a hairline has room between them. Otherwise the next band continues the left column directly and nothing
// is added. Weak spacing, so it merges with a heading's own space and vanishes at the top of a page.
#let band-gap = context {
  let ends = query(selector(<seg-last>).before(here()))
  if ends.len() > 0 {
    let e = ends.last().location().position()
    let p = here().position()
    if e.page == p.page and e.x > p.x + col-w / 2 { v(8pt, weak: true) }
  }
}

// Balanced tail: pieces are top-level blocks that sat on one page in the previous pass.
// Height = min over split points k of max(stack(0..k), stack(k..n)): a guaranteed fit,
// after which Typst's own column flow balances further at line level.
// ---------------------------------------------------------------- keep units (one-page rule)
#let umark(id, edge) = context [#metadata((id: id, edge: edge, page: here().page(), y: here().position().y.pt())) <um-pos>]
// Column-fit unit: unbreakable inside the two-column flow.
#let keepcol(body, padded: true) = layout(size => {
  let padding = if padded { 6pt } else { 0pt }
  let b = block(breakable: false, width: 100%, above: padding, below: padding, body)
  // The current layout region supplies its remaining height directly. A position query here
  // would observe the break it causes, creating a self-referential pagination fixed point.
  if measure(block(width: col-w, b)).height > size.height { colbreak() }
  b
})
// Figure components already own their outer spacing; the keep adds no second inset.
#let keepfigure(body) = keepcol(body, padded: false)
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
  block(width: 100%, above: 0pt, below: 8pt, breakable: false, {
    band-top
    grid(columns: (col-w, col-w), column-gutter: gap,
      { for p in ps.slice(0, k) { p } }, { for p in ps.slice(k) { p } })
    band-end
  })
}
#let bal(..pieces) = context {
  let ps = pieces.pos()
  let avail = body-bottom - here().position().y
  // A tail that cannot be balanced flows as a natural band, with the band hooks (candidate 19, p. 490).
  if ps.len() < 2 { seg({ for p in ps { p } }); return }
  let (h, k) = bal-split(ps)
  if h + 6pt > avail {
    seg({ for p in ps { p } })
  } else {
    block(width: 100%, above: 0pt, below: 8pt, breakable: false, {
      band-top
      grid(columns: (col-w, col-w), column-gutter: gap,
        { for p in ps.slice(0, k) { p } }, { for p in ps.slice(k) { p } })
      band-end
    })
  }
}

// A heading whose first table cannot share a column with it starts only where both columns of the
// current page can hold the pair, so the table may continue into the second column but never onto
// another page (`need`: measured height plus the repeated header and an undividable row group).
#let split-start(need) = context {
  if 2 * (body-bottom - here().position().y) < need { pagebreak(weak: true) }
}
// Escutcheon Press, the publisher's device (owner-supplied 2026-10-30; ink prepared by tools/brand_ink.py).
#let publisher-logo(w) = image("/assets/art/brand/escutcheon-press-logo.png", width: w, alt: "Escutcheon Press")
#let full(body) = block(width: 100%, above: 6pt, below: 8pt, body)
// `sticky`: a run-on opening never ends a page alone; when the columns after it cannot start on the
// page, the opening moves with them (design audit 2026-11-01). Ordinary openings (a head with its
// leading full-width table or figure) keep their place: moving them cost four pages in a local proof.
#let full-opening(body, sticky: false) = context {
  let height = measure(block(width: frame-w, body)).height
  block(width: 100%, above: 6pt, below: 8pt, sticky: sticky,
    breakable: height > body-bottom - m-top - 12pt, body)
}
// Prose balances at line boundaries, preserving its complete physical-page keep.
// Paragraph line boxes use the same explicit 0.8em/-0.25em edges as book().
#let prose-headings(body) = {
  if type(body) != content { return () }
  if body.func() == heading { return (body,) }
  if body.has("children") { return body.children.map(prose-headings).flatten() }
  if body.has("body") { return prose-headings(body.body) }
  ()
}
#let flow-height(ps) = {
  let stacked = measure(block(width: col-w, { for p in ps { p } })).height
  if stacked < 1pt { return 0pt }
  let pitch = body-size * 1.05 + body-lead
  // Internal sticky headings can move across the split with their opening lines.
  // The opening heading already starts in the left column and needs no extra reserve.
  let internal = ps.slice(calc.min(1, ps.len())).map(prose-headings).flatten()
  let head-reserve = if internal.len() == 0 { 0pt } else {
    internal.map(h => measure(block(width: col-w, h)).height).fold(0pt, calc.max)
  }
  stacked / 2 + 2 * pitch + head-reserve
}
#let flowcols(ps) = context {
  let height = flow-height(ps)
  if height < 1pt { for p in ps { p } }
  else { block(width: 100%, height: height, above: 0pt, below: 8pt, breakable: false, {
    band-top
    columns(2, gutter: gap, { for p in ps { p } })
    band-end
  }) }
}
#let flowtail(ps) = layout(size => {
  if flow-height(ps) <= size.height { flowcols(ps) }
  else { seg({ for p in ps { p } }) }
})
// Complete list items are legal column split points, with the native markers and indents.
#let list-fragment(number: none, body) = block(above: 0pt, below: v4.list-space, breakable: false, {
  show list: set block(above: 0pt, below: 0pt)
  show enum: set block(above: 0pt, below: 0pt)
  if number == none { list(body) } else { enum(start: number, body) }
})
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
#let flavour(body) = block(above: 4pt, below: 7pt, v4.flavour-set(fell-body(body)))
// Semantic opening only: generator emits this outside the ordinary two-column run.
#let section-lead(body, width: 82%) = v4.lead-block(fell-body(body), width: width)
// Short plain chapter introduction (one to three paragraphs before the first section): rules
// prose in the body face at the opener's 82% measure, instead of a few lines in two columns.
#let chapter-intro(body) = block(width: 100%, above: space-token.lead_above * 1pt, below: space-token.lead_below * 1pt + 4pt,
  align(center, block(width: 82%, align(left, body))))
// generated pen-and-ink spot art (transparent ink, so the page substrate shows through)
#let spotart(path, w) = block(width: 100%, above: 4pt, below: 2pt, breakable: false, align(center, image(path, width: w)))
// End-of-unit art (owner 2026-10-30: fill section-end white space with art). Placed only where a
// unit's last page is left empty because the next heading starts a later page, so it never moves
// text. `aspect` is height / width; the art prints at `w` or smaller to fit, but never below
// `min-h` (a wide, short piece whose full size is under `min-h` prints at full size), and is
// omitted when even that does not fit. A zero-height probe keeps the measuring
// point on this page (a context that yields nothing would report the following page).
// `max-w` (D-02 f): a tailpiece may grow past its family width to the gap it closes, up to its 300 ppi
// maximum and the design cap the composer passes. When the gap is generous the piece sits at the foot of
// the frame, so the page reads as text, air, tailpiece (D-02 g); a small gap keeps the piece under the text.
#let endart(id, path, w, aspect, max-w: none, min-h: tokens.art.tailpiece_min_height_in * 1in, gap: space-token.tailpiece_gap * 1pt) = {
  block(height: 0pt, above: 0pt, below: 0pt, sticky: false)[#metadata(id) <endart-probe>]
  context {
    let probe = query(selector(<endart-probe>).before(here())).last()
    let at = probe.location()
    let next = query(selector(heading).after(at))
    if next.len() > 0 and next.first().location().page() == at.page() { return }
    let avail = body-bottom - at.position().y - gap - 6pt
    let wmax = if max-w == none { w } else { calc.max(w, max-w) }
    let wfit = calc.min(wmax, avail / aspect)
    let h = calc.min(wfit * aspect, avail)
    if h >= calc.min(min-h, w * aspect) {
      let spare = avail - h
      if spare > tokens.art.tailpiece_foot_spare_pt * 1pt { v(1fr) } else { v(gap) }
      block(width: 100%, above: 0pt, below: 0pt, breakable: false,
        align(center, [#image(path, height: h, alt: id)#metadata((id: id, page: at.page(), h: h.pt())) <endart>]))
    }
  }
}

// Worked example and rules note: one panel (tinted field, black spine). The source's own label
// ("Example:", "Recommended First Party:") leads in bold, so no word is added or repeated.
#let panel(body) = block(width: 100%, above: space-token.panel_above * 1pt, below: space-token.panel_below * 1pt, breakable: true,
  fill: tint, stroke: (left: 2.6pt + ink), inset: (x: space-token.panel_horizontal_padding * 1pt, y: space-token.panel_vertical_padding * 1pt))[
  #set par(justify: true)
  #body
]
#let example(body, pre: none) = panel({
  show regex("^Example( [^:]{0,40})?:"): it => strong(it)
  body
})
#let note-box(body) = panel(body)

// The source's horizontal rules: a quiet separator (a short hairline with a lozenge) instead of the
// castle flourish, which stays at chapter and front-matter boundaries; an ordinary page then carries at
// most the ornament budget of two marks (design audit 2026-11-01, D-03).
#let hr-ornament(pre: none) = block(width: 100%, above: space-token.separator_above * 1pt, below: space-token.separator_below * 1pt,
  align(center, box(width: tokens.ornament.separator_width_fraction * 100%, {
    pre
    grid(columns: (1fr, auto, 1fr), column-gutter: 5pt, align: horizon,
      line(length: 100%, stroke: tokens.line_pt.separator * 1pt + ink),
      lozenge(size: tokens.ornament.separator_lozenge_pt * 1pt),
      line(length: 100%, stroke: tokens.line_pt.separator * 1pt + ink))
  })))

// ---------------------------------------------------------------- tables: the ledger
#let head-cell(h) = text(font: sans, weight: 700, size: table-size, fill: paper,
  coin-text(smallcaps(all: true, h), s: 1.05em, fill: paper))

// Native repeated headers retain the real table's identity on each continuation.
#let table-identity(id, title, continued: none, initial-title: true) = context {
  let starts = query(label("tbl-" + id))
  let is-continuation = if continued != none { continued } else { starts.len() > 0 and here().page() > starts.first().location().page() }
  // Repeated headers must have identical geometry before their page is known.
  // Removing the first identity row changes table placement, which changes the
  // queried start page and can oscillate indefinitely. Hidden text keeps the
  // measured continuation geometry while suppressing a duplicate opening title.
  let identity = text(font: sans, weight: 700, size: table-size, fill: ink,
    [#if title != none { title } else { id }#if is-continuation [ (continued)] else { hide[ (continued)] }])
  if initial-title or is-continuation { identity } else { hide(identity) }
}

// Rows that never stand alone at a break: the first and last few rows of a long table travel
// together, carried by an invisible zero-width column whose unbreakable cells span them (Typst
// keeps every row a breakable: false cell spans in one region). A short table is one group.
#let row-groups(n) = if n <= 5 { ((0, n),) } else { ((0, 3), (n - 3, n)) }
#let grouped-rows(rows, n-cols, groups) = {
  let out = ()
  for (y, r) in rows.enumerate() {
    let g = groups.find(((a, b)) => a <= y and y < b)
    let extra = if g == none { (table.cell(inset: 0pt)[],) }
      else if g.at(0) == y { (table.cell(rowspan: g.at(1) - g.at(0), breakable: false, inset: 0pt)[],) }
      else { () }
    out += r + extra
  }
  out
}

#let htable(id, widths, aligns, header, rows, kind: "table", title: none, initial-title: true, pre: none) = {
  set text(font: sans, size: table-size, top-edge: 0.8em, bottom-edge: -0.25em, number-type: "lining", number-width: "tabular", hyphenate: false)
  set par(leading: table-lead, spacing: 4pt, justify: false)
  set strong(delta: 200)
  let n-cols = header.len()
  let al(x) = { if x >= n-cols { return left }; let a = aligns.at(x); if a == left { left } else if a == right { right } else { center } }
  let identity = table.cell(colspan: n-cols + 1, fill: none, inset: (x: 0pt, top: 0pt, bottom: 3pt), align: left, table-identity(id, title, initial-title: initial-title))
  let columns = widths.map(w => w * 1pt) + (0pt,)
  let body = rows.map(r => r.enumerate().map(((x, c)) => if x == 0 and aligns.at(0) == left { strong(c) } else { c }))
  let head-row = header.enumerate().map(((x, h)) => table.cell(fill: ink, align: al(x) + horizon, head-cell(h))) + (table.cell(inset: 0pt)[],)
  set table.cell(breakable: false)   // keep ordinary rows intact
  block(width: 100%, above: space-token.table_above * 1pt, below: space-token.table_below * 1pt + 4pt, breakable: true)[
    #pre#metadata(id) #label("tbl-" + id)#tmark(id, "s")
    // The opening (heading, header band and its first row group) never splits from the heading
    // above it; the reserve measures them at the actual profile. When the table's own title is
    // hidden because it repeats that heading, the table rises by the hidden row so that no blank
    // line separates heading and header. The geometry never depends on the queried page.
    #context {
      let groups = row-groups(body.len())
      let opening = groups.first()
      let probe = coin-text(table(
        columns: columns,
        inset: (x: table-x, y: table-y),
        table.header(identity, ..head-row),
        ..grouped-rows(body.slice(0, opening.at(1)), n-cols, ((0, opening.at(1)),)),
      ))
      let lift = if initial-title { 0pt } else {
        calc.max(0pt, measure(block(width: widths.sum() * 1pt, table-identity(id, title, initial-title: false))).height + 3pt - 4pt)
      }
      let reserve = measure(probe).height + 2.2pt - lift
      v(-lift)
      block(breakable: false, height: reserve, above: 0pt, below: 0pt, none)
      v(-reserve)
    }
    #coin-text(table(
      columns: columns,
      align: (x, y) => al(x) + horizon,
      inset: (x: table-x, y: table-y),
      fill: (x, y) => if y < 2 or x >= n-cols { none } else if calc.even(y) { tint } else { none },
      stroke: (x, y) => (bottom: if y < 2 or x >= n-cols { none } else { 0.35pt + hair }),
      table.header(repeat: true, identity, ..head-row),
      ..grouped-rows(body, n-cols, row-groups(body.len())),
    ))
    // The closing brush takes no height, so it can never fall alone onto the next page.
    #block(height: 0pt, above: 0pt, below: 0pt, sticky: false)[#v(-1pt)#brush(weight: 2.2pt, seed: 5)]
    #tmark(id, "e")
  ]
}

// Monster stat strip: black header band, large centred values, a brush beneath.
#let statstrip(id, header, values, pre: none) = {
  set text(font: sans, number-type: "lining", number-width: "tabular", hyphenate: false)
  block(width: 100%, above: 7pt, below: 8pt, breakable: false)[
    #pre#metadata(id) #label("tbl-" + id)#tmark(id, "s")
    #coin-text(table(
      columns: (1fr,) * header.len(),
      align: center + horizon,
      inset: (x, y) => (x: 2pt, y: if y == 0 { 3pt } else { 4.5pt }),
      fill: (x, y) => if y == 0 { ink } else { none },
      stroke: (x, y) => (left: if y == 1 and x > 0 { 0.35pt + hair } else { none }),
      table.header(..header.map(h => text(weight: 700, size: table-size, fill: paper, smallcaps(all: true, h)))),
      ..values.map(v => text(weight: 600, size: tokens.type_pt.stat_value * 1pt, v)),
    ), s: 0.8em)
    #v(-2pt)
    #brush(weight: 2pt, seed: 7)
    #tmark(id, "e")
  ]
}

// Labelled key/value profile (stat tables whose cells hold formulas): reversed key column.
#let statcard(id, header, values, pre: none) = {
  set text(font: sans, size: table-size, top-edge: 0.8em, bottom-edge: -0.25em, number-type: "lining")
  set par(justify: false)
  block(width: 100%, above: 7pt, below: 8pt, breakable: false)[
    #pre#metadata(id) #label("tbl-" + id)#tmark(id, "s")
    #coin-text(table(
      columns: (auto, 1fr),
      inset: (x: 6pt, y: 3.6pt),
      fill: (x, y) => if x == 0 { ink } else if calc.odd(y) { tint } else { none },
      stroke: (x, y) => (bottom: if x == 1 { 0.35pt + hair } else { none }),
      ..header.zip(values).map(((h, v)) => (text(weight: 700, size: table-size, fill: paper, smallcaps(all: true, h)), v)).flatten(),
    ))
    #v(-1pt)
    #brush(weight: 2pt, seed: 9)
    #tmark(id, "e")
  ]
}

// Prose-heavy many-column tables: one labelled entry per source row.
#let cards(id, entries, title-label: none, initial-title: true, pre: none) = layout(size => {
  let entry(e) = block(width: 100%, above: 0pt, below: 0pt, inset: (top: 4pt, bottom: 5pt),
    stroke: (bottom: 0.35pt + hair))[
    #set par(leading: body-lead, spacing: 3pt, justify: false)
    #block(sticky: true, below: 3pt)[#text(font: sans, size: body-size, e.title)]
    #if e.fields.len() > 0 {
      set text(font: sans, size: table-size, number-type: "lining")
      block(below: 3pt, e.fields.map(((k, v)) => box[#text(weight: 700, size: table-size, fill: ink3, smallcaps(all: true, k))#h(3pt)#v]).join(h(9pt, weak: true)))
    }
    #for (k, v) in e.desc {
      block(below: 2pt)[#text(font: sans, size: table-size, weight: 700, fill: ink3, smallcaps(all: true, k)) #h(2pt) #text(size: body-size, v)]
    }
  ]
  let continuation-height = measure(block(width: size.width, table-identity(id, title-label, continued: true))).height + 3pt
  // As in the ledger (6.10): when the heading above names the table, its identity line is hidden on the
  // opening page and the entries rise by that line, so no blank line separates heading and first entry.
  let lift = if initial-title { 0pt } else {
    measure(block(width: size.width, table-identity(id, title-label, initial-title: false))).height + 3pt
  }
  block(width: 100%, above: space-token.table_above * 1pt, below: space-token.table_below * 1pt + 4pt, breakable: true)[
    #pre#metadata(id) #label("tbl-" + id)#tmark(id, "s")
    #v(-lift)
    #coin-text(table(columns: (1fr,), inset: 0pt, stroke: none,
      table.header(repeat: true, table.cell(inset: (bottom: 3pt), table-identity(id, title-label, initial-title: initial-title))),
      ..entries.map(e => table.cell(
        // A genuinely over-height entry may continue; fit-capable entries remain intact.
        breakable: measure(block(width: size.width, entry(e))).height > page-h - m-top - m-bot - continuation-height, entry(e))),
    ))
    #block(height: 0pt, above: 0pt, below: 0pt)[#brush(weight: 2.2pt, seed: 13)]
    #tmark(id, "e")
  ]
})

// ---------------------------------------------------------------- figures
// Caption welded to the figure: a black band with the number, the caption beneath, a rule.
// `shown`: the printed number in book order (the composer numbers figures as they appear); `id` stays
// the figure's registry id for its file, marks, and review.
#let figure-block(id, file, caption, width: 100%, anchor: none, pre: none, shown: none) = block(width: 100%, above: 10pt, below: 12pt, breakable: false)[
  #pre#metadata(id) #label("fig-" + id)#tmark(id, "s")
  #align(center, image(file, width: width))
  #v(4pt)
  #block(width: 100%, fill: ink, inset: (x: 7pt, y: 3.6pt), spacing: 0pt,
    text(font: sans, size: tokens.type_pt.caption * 1pt, weight: 700, fill: paper)[#if shown != none { shown } else { id }])
  #block(width: 100%, inset: (x: 6pt, top: 4.5pt, bottom: 5pt), spacing: 0pt, {
    set text(font: sans, size: tokens.type_pt.caption * 1pt, fill: ink)
    set par(leading: 2.5pt, justify: false)
    caption
  })
  #line(length: 100%, stroke: 0.6pt + ink)
  #tmark(id, "e")
]
