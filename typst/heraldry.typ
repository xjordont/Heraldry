// HERALDRY SKIRMISH — publication design system (frozen after specimen review).
// All layout lives here; content.typ is generated from the protected manuscript.

#let tokens = json("../config/design_tokens.json")
#let substrate-name = sys.inputs.at("substrate", default: "cream")
#let substrate = if substrate-name == "white" { rgb("#FFFFFF") } else { rgb(tokens.substrate.warm_cream_hex) }
#let ink = rgb(0, 0, 0)
#let ink2 = luma(20%)          // secondary text gray 0.2 (still >= 80% black)
#let rule-ink = luma(35%)
#let band = rgb(0, 0, 0, 6%)   // transparent band works on cream and white
#let serif = "Source Serif 4"
#let sans = "Source Sans 3"
#let display = "Cinzel"

#let page-w = 612pt
#let page-h = 792pt
#let m-in = 0.875in
#let m-out = 0.625in
#let m-top = 0.65in
#let m-bot = 0.7in
#let gap = 0.25in
#let frame-w = page-w - m-in - m-out
#let col-w = (frame-w - gap) / 2
#let body-bottom = page-h - m-bot

// ---------------------------------------------------------------- ornament
// One original motif: a broken ring with a short tapered rule.
#let ring(size: 7pt, stroke: 0.7pt) = box(width: size, height: size, baseline: 0.1em,
  curve(stroke: stroke + ink,
    curve.move((size * 0.5, 0pt)),
    curve.cubic((size * 0.95, 0pt), (size, size * 0.4), (size, size * 0.5)),
    curve.cubic((size, size * 0.95), (size * 0.6, size), (size * 0.5, size)),
    curve.move((size * 0.18, size * 0.88)),
    curve.cubic((0pt, size * 0.7), (0pt, size * 0.3), (size * 0.22, size * 0.1)),
  ))
#let taper(len: 60pt, weight: 1.6pt, dir: 1) = box(width: len, height: weight,
  polygon(fill: ink, ..(if dir == 1 {
    ((0pt, weight / 2), (len, 0pt), (len, weight))
  } else {
    ((0pt, 0pt), (len, weight / 2), (0pt, weight))
  })))
#let motif(len: 54pt) = box(baseline: -0.15em)[#taper(len: len, dir: -1)#h(4pt)#ring()#h(4pt)#taper(len: len)]

// ---------------------------------------------------------------- inline helpers
#let nb(s) = s   // placeholder (no-break handled in generator via U+00A0)

// ---------------------------------------------------------------- running furniture
#let chapter-pages = state("chapter-pages", ())
#let furniture-font = (font: sans, size: 9pt, fill: ink2, tracking: 0.04em)

#let current-heading(level) = {
  // Heading active at top of page; if a heading of that level starts on this page use it.
  let here-page = here().page()
  let on-page = query(heading.where(level: level)).filter(h => h.location().page() == here-page)
  if on-page.len() > 0 { return on-page.first() }
  let before = query(selector(heading.where(level: level)).before(here()))
  if before.len() > 0 { before.last() } else { none }
}

#let header-content = context {
  let p = here().page()
  let openers = query(<chapter-opener>).filter(m => m.location().page() == p)
  if openers.len() > 0 { return }
  let fm = query(<mainmatter>)
  if fm.len() == 0 or fm.first().location().page() > p { return }
  let ch = current-heading(1)
  let sec = current-heading(2)
  let left = calc.even(p)
  set text(..furniture-font)
  let label = if left {
    if ch != none { upper(ch.body) }
  } else {
    if sec != none and (ch == none or sec.location().page() >= ch.location().page()) { sec.body } else if ch != none { upper(ch.body) }
  }
  block(width: 100%, below: 0pt)[
    #if left [#label #h(1fr) #ring(size: 6pt, stroke: 0.55pt)] else [#ring(size: 6pt, stroke: 0.55pt) #h(1fr) #label]
    #v(-6pt)
    #line(length: 100%, stroke: 0.4pt + rule-ink)
  ]
}

#let footer-content = context {
  let p = here().page()
  let fm = query(<frontmatter-start>)
  if fm.len() > 0 and p == fm.first().location().page() { return }
  set text(font: sans, size: 9pt, fill: ink, number-type: "lining")
  let n = counter(page).display()
  if calc.even(p) { align(left, n) } else { align(right, n) }
}

// ---------------------------------------------------------------- headings
#let section-rule = line(length: 100%, stroke: 0.6pt + ink)

#let book(body) = {
  set document(title: "HERALDRY SKIRMISH: THE DYING LANDS — Release Candidate 484 (RC484)")
  set page(
    width: page-w, height: page-h,
    fill: substrate,
    margin: (inside: m-in, outside: m-out, top: m-top, bottom: m-bot),
    binding: left,
    header: header-content, header-ascent: 8pt,
    footer: footer-content, footer-descent: 12pt,
  )
  set text(font: serif, size: 10.5pt, lang: "en", region: "CA", fill: ink,
    top-edge: 0.8em, bottom-edge: -0.25em, hyphenate: true, number-type: "lining")
  set par(leading: 2.95pt, spacing: 6pt, justify: false)
  set strong(delta: 200)
  set list(marker: ([•], [–], [·]), indent: 2pt, body-indent: 5pt, spacing: 4pt)
  set enum(indent: 2pt, body-indent: 5pt, spacing: 4pt)
  set table(stroke: none)
  set heading(numbering: none)

  // chapter title (H2 in the manuscript → level 1)
  show heading.where(level: 1): it => block(text(font: display, weight: 600, size: 28pt, hyphenate: false, it.body))
  show heading.where(level: 2): it => block(above: 16pt, below: 7pt, sticky: true, breakable: false, width: 100%)[
    #line(length: 100%, stroke: 0.6pt + ink)
    #v(-2pt)
    #set par(leading: 3pt)
    #text(font: display, weight: 600, size: 14.5pt, top-edge: 0.8em, bottom-edge: -0.25em, it.body)
  ]
  show heading.where(level: 3): it => block(above: 12pt, below: 5pt, sticky: true, breakable: false)[
    #set par(leading: 2.5pt)
    #text(font: serif, weight: 600, size: 12.5pt, it.body)
  ]
  show heading.where(level: 4): it => block(above: 10pt, below: 4pt, sticky: true, breakable: false)[
    #set par(leading: 2.5pt)
    #text(font: serif, weight: 700, size: 11pt, it.body)
  ]
  show link: it => it
  body
}

// ---------------------------------------------------------------- chapter opener
#let chapter-opener(num, title, anchor, lead: none, art: none) = {
  pagebreak(weak: true)
  block(width: 100%, above: 0pt, below: 18pt, breakable: false)[
    #metadata(anchor) <chapter-opener>
    #if art != none {
      align(center, image(art, width: 100%, height: 3.6in, fit: "contain"))
      v(6pt)
    } else { v(0.35in) }
    #align(center)[
      #motif(len: 80pt)
      #v(10pt)
      #if num != none [
        #text(font: display, size: 13pt, weight: 600, fill: ink2, num)
        #v(2pt)
      ]
      #set par(leading: 6pt)
      #heading(level: 1, outlined: true, bookmarked: true, title) #label(anchor)
      #v(8pt)
      #line(length: 36%, stroke: 0.6pt + ink)
    ]
    #if lead != none {
      v(10pt)
      align(center, block(width: 78%)[
        #set par(justify: false, leading: 3.4pt)
        #set text(size: 10.5pt, fill: ink)
        #lead
      ])
    }
  ]
}

// ---------------------------------------------------------------- segments
#let seg-gap = gap
#let pm(seg, piece, edge) = context [#metadata((seg: seg, piece: piece, edge: edge, page: here().page(), y: here().position().y.pt(), x: here().position().x.pt())) <pm>]

#let pmx(..args) = none
#let tmark(id, edge) = context [#metadata((id: id, edge: edge, page: here().page(), folio: counter(page).display())) <tblpos>]
#let ixm(k) = [#metadata(k) #label("ix-" + k)#context [#metadata((k: k, page: here().page(), folio: counter(page).display())) <ixpos>]]
#let seg(body) = columns(2, gutter: gap, body)

// Balanced tail: pieces are top-level blocks that sat on one page in the previous pass.
// Height = min over split points k of max(stack(0..k), stack(k..n)): a guaranteed fit,
// after which Typst's own column flow balances further at line level.
#let bal(..pieces) = context {
  let ps = pieces.pos()
  let n = ps.len()
  let stack(a, b) = measure(block(width: col-w, { for p in ps.slice(a, b) { p } })).height
  // prefix height grows and suffix height shrinks with k: binary search the crossing.
  let lo = 1
  let hi = n - 1
  let best = stack(0, n)
  while lo <= hi {
    let k = calc.div-euclid(lo + hi, 2)
    let a = stack(0, k)
    let b = stack(k, n)
    best = calc.min(best, calc.max(a, b))
    if a < b { lo = k + 1 } else { hi = k - 1 }
  }
  let avail = body-bottom - here().position().y
  if best + 14pt > avail {
    columns(2, gutter: gap, { for p in ps { p } })
  } else {
    block(width: 100%, height: best + 14pt, above: 0pt, below: 8pt, columns(2, gutter: gap, { for p in ps { p } }))
  }
}

#let full(body) = block(width: 100%, above: 8pt, below: 10pt, body)

// ---------------------------------------------------------------- body components
// Flavour text: the source marks it with emphasis, so the italic comes from #emph.
#let flavour(body) = block(above: 4pt, below: 8pt, body)

#let example(body) = block(width: 100%, above: 8pt, below: 10pt, breakable: true,
  stroke: (left: 1pt + ink), inset: (left: 8pt, top: 2pt, bottom: 2pt, right: 0pt))[
  #set text(size: 10pt)
  #set par(leading: 2.9pt)
  #body
]

#let note-box(body) = block(width: 100%, above: 8pt, below: 10pt, breakable: true,
  stroke: (left: 1pt + ink, top: 0.4pt + rule-ink, bottom: 0.4pt + rule-ink), inset: (left: 8pt, top: 5pt, bottom: 5pt, right: 4pt))[#body]

#let hr-ornament() = align(center, block(above: 10pt, below: 10pt, motif(len: 30pt)))

// ---------------------------------------------------------------- tables
#let tcell(body, header: false) = {
  if header { text(font: sans, weight: 600, size: 9.5pt, body) } else { body }
}

#let htable(id, widths, aligns, header, rows, kind: "table", title: none) = {
  set text(font: sans, size: 9.5pt, top-edge: 0.8em, bottom-edge: -0.25em, number-type: "lining", number-width: "tabular", hyphenate: false)
  set par(leading: 2.6pt, spacing: 4pt)
  set strong(delta: 200)
  let n = widths.len()
  let fills = (x, y) => if y > 0 and calc.even(y) { band } else { none }
  set table.cell(breakable: false)   // keep ordinary rows intact
  block(width: 100%, above: 8pt, below: 10pt, breakable: true)[
    #metadata(id) #label("tbl-" + id)#tmark(id, "s")
    #table(
      columns: widths.map(w => w * 1pt),
      align: (x, y) => aligns.at(x) + top,
      inset: (x: 4pt, y: 3pt),
      fill: fills,
      stroke: (x, y) => (
        top: if y == 0 { 0.75pt + ink } else { none },
        bottom: if y == 0 { 0.75pt + ink } else { 0.3pt + rgb(0,0,0,22%) },
      ),
      table.header(repeat: true, ..header.map(h => table.cell(text(weight: 600, h)))),
      ..rows.flatten(),
    )
    #tmark(id, "e")
  ]
}

// Monster stat strip: compact six-field profile.
#let statstrip(id, header, values) = {
  set text(font: sans, size: 9.5pt, top-edge: 0.8em, bottom-edge: -0.25em, number-type: "lining", number-width: "tabular")
  block(width: 100%, above: 6pt, below: 8pt, breakable: false)[
    #metadata(id) #label("tbl-" + id)#tmark(id, "s")#tmark(id, "e")
    #table(
      columns: (1fr,) * header.len(),
      align: center + horizon,
      inset: (x: 2pt, y: 3pt),
      stroke: (x, y) => (top: if y == 0 { 0.75pt + ink } else { none }, bottom: if y == 0 { 0.4pt + rule-ink } else { 0.75pt + ink }),
      fill: (x, y) => if y == 0 { band } else { none },
      table.header(..header.map(h => text(weight: 700, size: 9pt, tracking: 0.05em, h))),
      ..values,
    )
  ]
}

// Labelled key/value profile (stat tables whose cells hold formulas).
#let statcard(id, header, values) = {
  set text(font: sans, size: 9.5pt, top-edge: 0.8em, bottom-edge: -0.25em, number-type: "lining")
  block(width: 100%, above: 6pt, below: 8pt, breakable: false)[
    #metadata(id) #label("tbl-" + id)#tmark(id, "s")#tmark(id, "e")
    #table(
      columns: (auto, 1fr),
      inset: (x: 4pt, y: 2.6pt),
      stroke: (x, y) => (top: if y == 0 { 0.75pt + ink } else { 0.3pt + rgb(0,0,0,22%) }, bottom: if y == header.len() - 1 { 0.75pt + ink } else { none }),
      fill: (x, y) => if x == 0 { band } else { none },
      ..header.zip(values).map(((h, v)) => (text(weight: 700, h), v)).flatten(),
    )
  ]
}

// Prose-heavy many-column tables: one labelled entry per source row.
// `lead` = key fields shown in the entry title line, `fields` = (label, value) pairs, `desc` = (label, value) prose fields.
#let cards(id, entries, title-label: none) = {
  block(width: 100%, above: 6pt, below: 8pt, breakable: true)[
    #metadata(id) #label("tbl-" + id)#tmark(id, "s")
    #for e in entries {
      block(width: 100%, above: 0pt, below: 0pt, breakable: true, inset: (top: 5pt, bottom: 6pt),
        stroke: (top: 0.3pt + rgb(0,0,0,30%)))[
        #set par(leading: 2.8pt, spacing: 3pt)
        #block(sticky: true, below: 3pt)[
          #set text(font: sans, size: 10pt)
          #e.title
        ]
        #if e.fields.len() > 0 {
          set text(font: sans, size: 9.5pt, number-type: "lining")
          block(below: 3pt, e.fields.map(((k, v)) => box[#text(weight: 600, fill: ink2, k)#h(3pt)#v]).join(h(9pt, weak: true)))
        }
        #for (k, v) in e.desc {
          block(below: 2pt)[#text(font: sans, size: 9.5pt, weight: 600, fill: ink2, k) #h(2pt) #text(size: 10pt, v)]
        }
      ]
    }
    #line(length: 100%, stroke: 0.6pt + ink)
    #tmark(id, "e")
  ]
}

// ---------------------------------------------------------------- figures
#let figure-block(id, file, caption, width: 100%, anchor: none) = block(width: 100%, above: 10pt, below: 12pt, breakable: false)[
  #metadata(id) #label("fig-" + id)#tmark(id, "s")
  #align(center, image(file, width: width))
  #v(4pt)
  #set text(font: sans, size: 9pt, fill: ink)
  #set par(leading: 2.4pt)
  #text(weight: 700, id + ".") #caption
]
