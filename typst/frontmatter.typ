// Front and back matter: title page, how-to-use, generated contents, index.
#import "heraldry.typ": *
#import "cover.typ": front-cover, back-cover
#let edition = sys.inputs.at("edition", default: "interior")

#let how-to-use = json("../editorial/how_to_use.json")
#let index-data = if sys.inputs.at("index", default: "on") == "on" { json("../build/index.json") } else { (entries: ()) }

#let title-page(title, subtitle, version) = page(header: none, footer: none, margin: (x: 0.9in, y: 0.9in))[
  #metadata("title") <frontmatter-start>
  #v(0.55in)
  #align(center)[
    #signature(s: 1.7in)
    #v(22pt)
    #set par(leading: 10pt, justify: false)
    #text(font: serif, weight: 700, size: 34pt, tracking: 0.12em, hyphenate: false, title.at(0))
    #v(6pt)
    #text(font: serif, weight: 600, size: 15pt, tracking: 0.32em, title.at(1))
    #v(14pt)
    #flourish(len: 96pt)
    #v(16pt)
    #block(width: 80%)[#set par(leading: 5pt, justify: false); #set text(font: fell, size: 13pt); #show emph: it => it.body; #subtitle]
    #v(0.7in)
    // Author credit (owner, 2026-10-29), set as the book's byline in the title's face.
    #text(font: serif, weight: 600, size: 17pt, tracking: 0.16em, upper(publication.verified_publication_metadata.author_credit))
    #v(1fr)
  ]
  // Imprint at the foot: the Escutcheon Press device (owner, 2026-10-30) over the manuscript version.
  #place(bottom + center, dy: -0.35in)[
    #set align(center)
    #publisher-logo(0.95in)
    #v(8pt)
    // The version line in the title's own face, small caps, so the page keeps one voice (D-10).
    #text(font: serif, size: tokens.type_pt.imprint * 1pt, weight: 600, tracking: 0.1em, smallcaps(all: true, version))
  ]
]

// Contents: each chapter row carries its arms; sections beneath with dotted leaders.
#let toc-tab(loc) = {
  let os = query(<chapter-opener>).filter(m => m.location().page() == loc.page())
  if os.len() == 0 { none } else { opener-tab(os.first().value) }
}
#let toc-page() = {
  pagebreak(weak: true)
  block(width: 100%, below: 10pt)[
    #align(center)[
      #v(0.1in)
      #text(font: goth, weight: 600, size: 34pt)[Contents]
      #v(-6pt)
      #flourish(len: 70pt)
    ]
  ]
  set text(size: 10pt)
  set par(justify: false)
  show outline.entry.where(level: 1): it => {
    v(11pt, weak: true)
    block(sticky: true, below: 4pt)[
      #let n = toc-tab(it.element.location())
      #link(it.element.location())[#grid(columns: (22pt, 1fr, auto), column-gutter: 7pt, align: horizon,
        if n != none { arms(n, w: 20pt) } else { [] },
        text(font: goth, weight: 600, size: tokens.type_pt.toc_chapter * 1pt, it.element.body),
        text(font: sans, weight: 700, size: 10pt, it.page()))]
      #v(-3pt)
      #line(length: 100%, stroke: 0.6pt + ink)
    ]
  }
  // The page number has its own right gutter: a long title wraps short of it with a hanging indent, the
  // leader runs to the end of the title's last line, and the number sits level with that line, so neither
  // the number nor a lone leader dot falls to a line of its own (rulebook-layout review, 2026-11-06: 2.6).
  show outline.entry.where(level: 2): it => {
    block(above: 3pt, below: 0pt, inset: (left: 29pt))[
      #set text(size: tokens.type_pt.toc_entry * 1pt)
      #link(it.element.location())[#grid(columns: (1fr, 16pt), column-gutter: 2pt, align: (left, right + bottom),
        par(hanging-indent: 12pt)[#text(hyphenate: false, it.element.body) #box(width: 1fr, repeat(text(fill: ink3)[.#h(3pt)]))],
        text(font: sans, size: tokens.type_pt.toc_entry * 1pt, it.page()))]
    ]
  }
  columns(2, gutter: gap, outline(title: none, depth: 2, indent: 0pt))
}

#let version-text = json("../build/cover.json").version
// Edition text names the current manuscript, so the colophon and How to Use never go stale.
#let rc-code = version-text.find(regex("RC\d+"))
#let pub-meta = publication.verified_publication_metadata
#let edition-text(p) = p.replace("{{VERSION}}", version-text).replace("{{RC}}", if rc-code == none { version-text } else { rc-code }).replace("{{AUTHOR}}", pub-meta.author_credit).replace("{{PUBLISHER}}", pub-meta.publisher).replace("{{YEAR}}", str(pub-meta.copyright_year)).replace("{{HOLDER}}", pub-meta.copyright_holder)
#let frontmatter(title: ("HERALDRY SKIRMISH", "THE DYING LANDS"), subtitle: [], version: []) = {
  if edition == "digital" {
    front-cover(title, emph(subtitle), version)
    page(header: none, footer: none, numbering: none)[]   // inside front cover (keeps recto/verso parity)
  }
  set page(numbering: "i")
  counter(page).update(1)
  title-page(title, subtitle, version)
  // verso of title: production/edition notice (verified information only)
  page(header: none)[
    #v(1fr)
    #set text(font: sans, size: 9pt, fill: ink)
    #set par(leading: 3pt, spacing: 6pt)
    // The publisher's device heads the imprint (owner, 2026-10-30).
    #publisher-logo(1.3in)
    #v(14pt)
    #block(width: 70%)[
      #for p in how-to-use.colophon [#edition-text(p) #parbreak()]
    ]
  ]
  // How to use this book
  pagebreak(weak: true)
  align(center)[#v(0.1in) #text(font: goth, weight: 600, size: 34pt, how-to-use.title) #v(-6pt) #flourish(len: 70pt) #v(10pt)]
  columns(2, gutter: gap)[
    #for s in how-to-use.sections [
      #heading(level: 4, outlined: false, bookmarked: false, s.heading)
      #for p in s.paras [#edition-text(p) #parbreak()]
    ]
  ]
  toc-page()
}

#let mainmatter() = {
  pagebreak(to: "odd", weak: true)
  [#metadata("main") <mainmatter>]
}

#let index-page() = {
  if index-data.entries.len() == 0 { return }
  pagebreak(weak: true)
  block(width: 100%, below: 14pt)[
    #metadata("index") <chapter-opener>
    #v(0.1in)
    #align(center)[
      #arms(15, w: 40pt)
      #v(-2pt)
      #heading(level: 1, outlined: true, bookmarked: true, "Index") <index>
      #v(-6pt)
      #flourish(len: 70pt)
      #v(8pt)
      #block(width: 80%)[#set text(font: fell, size: 11pt); #set par(justify: false); #index-data.note]
    ]
  ]
  set text(font: sans, size: tokens.type_pt.index * 1pt)
  set par(leading: 2.4pt, spacing: 2pt, hanging-indent: 10pt, justify: false)
  let pages-for(key) = {
    let hits = query(label("ix-" + key)).map(h => h.location())
    for hid in index-data.at("heads", default: (:)).at(key, default: ()) {
      let q = query(label(hid))
      if q.len() > 0 { hits.push(q.first().location()) }
    }
    let ps = hits.map(l => (n: counter(page).at(l).first(), loc: l))
    let seen = ()
    let out = ()
    for p in ps.sorted(key: p => p.n) {
      if p.n not in seen { seen.push(p.n); out.push(link(p.loc, str(p.n))) }
    }
    out.join(", ")
  }
  // Index items in reading order: letter heads ("h"), main entries ("e"), and sub-entries ("s").
  let items = ()
  let letter = ""
  for e in index-data.entries {
    let l = e.at("letter", default: upper(e.term.first()))
    if l != letter {
      letter = l
      items.push((kind: "h", above: 10pt, below: 4pt, inset: 0pt, body: grid(columns: (auto, 1fr), column-gutter: 5pt, align: horizon,
        box(fill: ink, inset: (x: 4pt, y: 2.5pt), text(font: goth, weight: 600, size: tokens.type_pt.index_letter * 1pt, fill: paper, l)), line(length: 100%, stroke: 0.4pt + ink3))))
    }
    items.push((kind: "e", above: 2.5pt, below: 0pt, inset: 0pt, body: [
      #text(weight: 600, e.term)#if e.keys.len() > 0 [, #context e.keys.map(k => pages-for(k)).join(", ")]#if e.at("see", default: none) != none [. #emph[See] #e.see]#if e.at("also", default: none) != none [. #emph[See also] #e.also]
    ]))
    for s in e.at("sub", default: ()) {
      items.push((kind: "s", above: 1.5pt, below: 0pt, inset: 9pt, body: [
        #s.term, #context s.keys.map(k => pages-for(k)).join(", ")
      ]))
    }
  }
  let ix-gap = 14pt
  let ix-col = (frame-w - 2 * ix-gap) / 3
  let piece(i, it) = block(above: it.above, below: it.below, inset: (left: it.inset),
    sticky: it.kind == "h", breakable: false, [#metadata(i) <ix-item>#it.body])
  // The last index page is balanced: its items are split into three whole-entry columns of near-equal
  // height. A column never starts with a sub-entry or ends with a letter head. Pages before the last
  // fill normally, so the split points depend only on where the previous layout pass began that page.
  context {
    let marks = query(<ix-item>)
    let breaks = ()
    if marks.len() == items.len() and items.len() > 0 {
      let last = marks.last().location().page()
      let s = marks.position(m => m.location().page() == last)
      let n = items.len()
      if n - s >= 6 {
        let h = items.map(it => measure(block(width: ix-col, inset: (left: it.inset), breakable: false, it.body)).height)
        let gap-before(j) = calc.max(items.at(j - 1).below, items.at(j).above)
        // pre.at(j): stacked height of items s..j-1 as one run, including the gaps between them
        let pre = (0pt,)
        for j in range(s, n) { pre.push(pre.last() + h.at(j) + if j > s { gap-before(j) } else { 0pt }) }
        let run(a, b) = pre.at(b - s) - pre.at(a - s) - if a > s { gap-before(a) } else { 0pt }
        let ok(j) = items.at(j).kind != "s" and items.at(j - 1).kind != "h"
        let avail = body-bottom - marks.at(s).location().position().y - 2pt
        let best = (pre.last(), none, none)
        for k1 in range(s + 1, n - 1) {
          if not ok(k1) { continue }
          let a = run(s, k1)
          if a >= best.at(0) { break }
          for k2 in range(k1 + 1, n) {
            if not ok(k2) { continue }
            let m = calc.max(a, run(k1, k2), run(k2, n))
            if m < best.at(0) { best = (m, k1, k2) }
            if run(k1, k2) >= best.at(0) { break }
          }
        }
        if best.at(1) != none and best.at(0) <= avail { breaks = (best.at(1), best.at(2)) }
      }
    }
    columns(3, gutter: ix-gap, {
      for (i, it) in items.enumerate() {
        if i in breaks { colbreak() }
        piece(i, it)
      }
    })
  }
}

#let backmatter() = {
  index-page()
  if edition == "digital" {
    let cd = json("../build/cover.json")
    back-cover((lead: emph(cd.lead), facts: cd.facts), version-text)
  }
}
