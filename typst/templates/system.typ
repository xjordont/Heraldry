// HERALDRY SKIRMISH — book design system v2 ("ink and iron").
// Page templates and components for every page type in the book; the plan and rationale are in
// docs/BOOK_DESIGN_PLAN.md, the reference evidence in docs/design/REFERENCE_STUDY.md.
// Self-contained: specimens use it today, and the book build adopts it component by component
// (names and signatures follow typst/heraldry.typ where the two overlap).

// ================================================================ tokens
#let substrate-name = sys.inputs.at("substrate", default: "cream")
#let paper = if substrate-name == "white" { rgb("#FFFFFF") } else { rgb("#FCFAF5") }
#let ink = rgb(0, 0, 0)
#let ink2 = luma(22%)                 // secondary text, still reads as black on inkjet
#let ink3 = luma(45%)                 // furniture labels and secondary caption parts
#let hair = rgb(0, 0, 0, 28%)         // hairlines between rows and entries
#let tint = rgb(0, 0, 0, 5.5%)        // example and panel fields (transparent: cream and white)
#let tint2 = rgb(0, 0, 0, 9%)         // the roll column of lookup tables

#let serif = "Source Serif 4"         // reading text
#let sans = "Source Sans 3"           // data, labels, navigation
#let fell = "IM FELL English"         // display roman and italic (flavour text, leads)
#let fellsc = "IM FELL English SC"    // display small caps (titles, entry names)

#let page-w = 612pt
#let page-h = 792pt
#let m-in = 0.875in                   // binding side
#let m-out = 0.6in
#let m-top = 0.8in
#let m-bot = 0.8in
#let gap = 0.25in
#let frame-w = page-w - m-in - m-out
#let col-w = (frame-w - gap) / 2
#let edge-safe = 0.375in

#let body-size = 10.25pt
#let body-lead = 3.35pt               // line pitch about 13.4pt

// ================================================================ ornament
// One original family: the lozenge and the voided lozenge (heraldic "mascle"), tapered rules, and
// the thick-and-thin double rule that closes running heads, section titles and tables.
#let lozenge(size: 6pt, fill: ink) = box(width: size, height: size, baseline: 0.05em,
  polygon(fill: fill, (size / 2, 0pt), (size, size / 2), (size / 2, size), (0pt, size / 2)))
#let mascle(size: 7pt, ground: none) = box(width: size, height: size, baseline: 0.08em, {
  let g = if ground == none { paper } else { ground }
  place(polygon(fill: ink, (size / 2, 0pt), (size, size / 2), (size / 2, size), (0pt, size / 2)))
  place(dx: size * 0.3, dy: size * 0.3, polygon(fill: g,
    (size * 0.2, 0pt), (size * 0.4, size * 0.2), (size * 0.2, size * 0.4), (0pt, size * 0.2)))
})
#let taper(len: 60pt, weight: 1.4pt, dir: 1) = box(width: len, height: weight,
  polygon(fill: ink, ..(if dir == 1 { ((0pt, 0pt), (len, weight / 2), (0pt, weight)) }
                         else { ((0pt, weight / 2), (len, 0pt), (len, weight)) })))
#let flourish(len: 50pt) = box(baseline: -0.1em)[#taper(len: len, dir: -1)#h(5pt)#mascle()#h(5pt)#taper(len: len)]
#let double-rule(heavy: 1.5pt, light: 0.45pt, spread: 1.6pt, flip: false) = block(width: 100%, spacing: 0pt, {
  line(length: 100%, stroke: (if flip { light } else { heavy }) + ink)
  v(spread)
  line(length: 100%, stroke: (if flip { heavy } else { light }) + ink)
})

// Small caps label with a hairline running to the margin: the entry-anatomy separator.
#let label-rule(body, size: 7.4pt) = block(above: 7pt, below: 3.5pt, sticky: true, width: 100%,
  grid(columns: (auto, 1fr), column-gutter: 5pt, align: horizon,
    text(font: sans, weight: 700, size: size, tracking: 0.14em, upper(body)),
    line(length: 100%, stroke: 0.4pt + hair)))

// ================================================================ running furniture
// Chapter thumb tabs bleed off the outer edge in a fixed slot per part, so the closed book shows an
// index. They are navigation only: the running head names the chapter too. Numbers sit 0.22in in.
#let tab-slots = 14
#let thumb-tab(n, recto, label: none) = {
  let slot-h = (page-h - 2 * 1.15in) / tab-slots
  let y = 1.15in + slot-h * (n - 1)
  let w = 0.42in
  let x = if recto { page-w - w } else { 0pt }
  place(top + left, dx: x, dy: y,
    block(width: w, height: slot-h - 4pt, fill: ink,
      inset: if recto { (right: 0.12in) } else { (left: 0.12in) },
      align(center + horizon, text(font: sans, weight: 700, size: 10pt, fill: paper,
        if label != none { label } else { str(n) }))))
}

#let running-head(left-text, right-text, recto, mark: none) = {
  set text(font: sans, size: 7.4pt, weight: 600, tracking: 0.16em, fill: ink2)
  let m = if mark != none { mark } else { lozenge(size: 4.2pt) }
  block(width: 100%, below: 0pt, {
    if recto [#h(1fr)#upper(right-text)#h(6pt)#m] else [#m#h(6pt)#upper(left-text)#h(1fr)]
    v(3pt)
    double-rule(heavy: 0.9pt, light: 0.3pt, spread: 1.3pt)
  })
}

#let folio(n, recto) = {
  set text(font: fellsc, size: 11pt, fill: ink)
  if recto { align(right)[#taper(len: 22pt, weight: 0.9pt, dir: -1)#h(5pt)#str(n)] }
  else { align(left)[#str(n)#h(5pt)#taper(len: 22pt, weight: 0.9pt)] }
}

// A page shell for specimens: furniture comes from explicit arguments (the book derives it).
#let shell(n, chapter: "", section: "", tab: none, tab-label: none, furniture: true, folio-on: true, body) = {
  let recto = calc.odd(n)
  set page(width: page-w, height: page-h, fill: paper,
    margin: if recto { (left: m-in, right: m-out, top: m-top, bottom: m-bot) }
            else { (left: m-out, right: m-in, top: m-top, bottom: m-bot) },
    header: if furniture { running-head(chapter, section, recto) },
    header-ascent: 16pt,
    footer: if furniture or folio-on { if folio-on { folio(n, recto) } },
    footer-descent: 18pt,
    background: if tab != none { thumb-tab(tab, recto, label: tab-label) },
  )
  body
}

// ================================================================ base text
#let base(body) = {
  set text(font: serif, size: body-size, lang: "en", region: "CA", fill: ink, hyphenate: true,
    top-edge: 0.8em, bottom-edge: -0.25em, number-type: "lining")
  set par(leading: body-lead, spacing: 6.5pt, justify: false, first-line-indent: 0pt)
  set strong(delta: 200)
  set list(marker: (box(baseline: -1.2pt, lozenge(size: 4.2pt)), [–]), indent: 1pt, body-indent: 6pt, spacing: 4.5pt)
  set enum(indent: 1pt, body-indent: 6pt, spacing: 4.5pt, numbering: n => text(font: sans, weight: 700, size: 9pt)[#n.])
  body
}

// ================================================================ headings
// Numbered section (x.y): starts a fresh page in the book (or the chapter opener page); black
// number block, display small caps, thick-and-thin rule. Full width above the columns.
#let section(num, title) = block(above: 4pt, below: 11pt, sticky: true, width: 100%, breakable: false)[
  #set par(justify: false)
  #grid(columns: (auto, 1fr), column-gutter: 9pt, align: bottom,
    box(fill: ink, inset: (x: 5pt, top: 4.5pt, bottom: 3.5pt),
      text(font: sans, weight: 700, size: 10pt, fill: paper, tracking: 0.04em, num)),
    text(font: fellsc, size: 21pt, hyphenate: false, title))
  #v(4pt)
  #double-rule()
]

// Subsection (x.y.z): serif bold with a quiet sans number.
#let subsection(num, title) = block(above: 13pt, below: 5pt, sticky: true)[
  #set par(justify: false)
  #if num != none [#text(font: sans, weight: 700, size: 9.5pt, fill: ink3, num)#h(6pt)]#text(font: serif, weight: 700, size: 12.5pt, title)
]

// Minor named heading inside a subsection.
#let minor(title) = block(above: 10pt, below: 3pt, sticky: true, text(font: fellsc, size: 12.5pt, title))

// Run-in label for definition-style paragraphs ("Primary Objective:" etc.).
#let runin(label, body) = par[#text(weight: 700, label)#h(0.3em)#body]

// ================================================================ text components
#let flavour(body, size: 11.2pt) = block(above: 3pt, below: 8pt, {
  set par(justify: false, leading: 3.6pt)
  text(font: fell, style: "italic", size: size, fill: ink2, body)
})

// Worked example: tinted field, heavy left rule, small caps tag. Numbered steps (1.1, 1.2...) match
// the labels in the figure they explain.
#let example(title: none, body) = block(width: 100%, above: 9pt, below: 11pt, breakable: true,
  fill: tint, stroke: (left: 2.4pt + ink), inset: (left: 10pt, right: 9pt, top: 7pt, bottom: 8pt))[
  #text(font: sans, weight: 700, size: 7.4pt, tracking: 0.16em)[EXAMPLE#if title != none [ #h(3pt)·#h(3pt) #upper(title)]]
  #v(2pt)
  #set text(size: 9.8pt)
  #set par(leading: 3.1pt)
  #body
]

// Rules note / clarification: open box between rules, centred tag in the top rule.
#let note-box(tag: "Rules Note", body) = block(width: 100%, above: 12pt, below: 12pt, breakable: false)[
  #grid(columns: (1fr, auto, 1fr), column-gutter: 6pt, align: horizon,
    line(length: 100%, stroke: 1pt + ink),
    text(font: sans, weight: 700, size: 7.4pt, tracking: 0.16em)[#mascle(size: 6pt)#h(4pt)#upper(tag)#h(4pt)#mascle(size: 6pt)],
    line(length: 100%, stroke: 1pt + ink))
  #block(inset: (x: 4pt, top: 3pt, bottom: 6pt))[#set text(size: 9.8pt); #set par(leading: 3.1pt); #body]
  #line(length: 100%, stroke: 0.45pt + ink)
]

// Procedure: numbered steps with large display numerals hanging at the left.
#let procedure(title: none, steps) = block(width: 100%, above: 9pt, below: 10pt, breakable: true)[
  #if title != none { label-rule(title) }
  #for (i, s) in steps.enumerate() {
    block(above: 5pt, below: 5pt, breakable: false,
      grid(columns: (16pt, 1fr), column-gutter: 5pt,
        align(right, text(font: fellsc, size: 16pt, top-edge: "cap-height", str(i + 1))),
        s))
  }
]

// ================================================================ tables
// Reference table: black header bar with reversed small caps, hairline rows, closing heavy rule.
// `band` adds light banding for long tables; `roll` tints the first (die) column; `notes` gives
// a row a spanning second line for long text (the Traits line of an equipment row, say).
#let ref-table(widths, aligns, header, rows, title: none, roll: false, band: false, notes: none, size: 9.2pt) = {
  set text(font: sans, size: size, number-type: "lining", number-width: "tabular", hyphenate: false)
  set par(leading: 2.6pt, spacing: 4pt, justify: false)
  let n = header.len()
  let cells = ()
  for (i, r) in rows.enumerate() {
    cells += r.map(c => table.cell(c))
    if notes != none and notes.at(i, default: none) != none {
      cells.push(table.cell(colspan: n, inset: (left: 14pt, right: 5pt, top: 0pt, bottom: 4pt),
        text(size: size - 0.6pt, fill: ink2, notes.at(i))))
    }
  }
  block(width: 100%, above: 9pt, below: 11pt, breakable: true)[
    #if title != none { block(below: 4pt, sticky: true, text(font: fellsc, size: 12.5pt, title)) }
    #table(
      columns: widths,
      align: (x, y) => aligns.at(x, default: left) + horizon,
      inset: (x: 5pt, y: 3.4pt),
      fill: (x, y) => if y == 0 { ink } else if roll and x == 0 { tint2 } else if band and calc.even(y) { tint } else { none },
      stroke: (x, y) => (bottom: if y == 0 { none } else { 0.3pt + hair }),
      table.header(repeat: true, ..header.map(h => text(weight: 700, size: 7.6pt, tracking: 0.12em, fill: paper, upper(h)))),
      ..cells,
    )
    #v(-4.5pt)
    #line(length: 100%, stroke: 1.3pt + ink)
  ]
}

// ================================================================ figures and art
// The caption is welded to the figure: a black bar carries the figure number and title, and the
// caption sits directly beneath, so legend and drawing never separate.
#let figure-block(id, title, file, caption, width: 100%) = block(width: 100%, above: 10pt, below: 12pt, breakable: false)[
  #align(center, image(file, width: width))
  #v(4pt)
  #block(width: 100%, fill: ink, inset: (x: 6pt, y: 3.6pt), spacing: 0pt,
    text(font: sans, size: 7.8pt, weight: 700, tracking: 0.1em, fill: paper)[#id #h(5pt) #upper(title)])
  #block(width: 100%, inset: (x: 6pt, top: 4pt, bottom: 5pt), stroke: (bottom: 0.45pt + ink), spacing: 0pt, {
    set text(font: sans, size: 8.6pt)
    set par(leading: 2.5pt, justify: false)
    caption
  })
]

// Spot art: open-edged ink vignette; the art carries its own white fade, so no frame or rule.
#let spot(file, width: 100%) = block(width: 100%, above: 6pt, below: 8pt, breakable: false,
  align(center, image(file, width: width)))

// ================================================================ profiles and entries
#let role-tag(role) = box(stroke: 0.6pt + ink, inset: (x: 3.5pt, top: 2.2pt, bottom: 1.6pt), baseline: 0.15em,
  text(font: sans, weight: 700, size: 7pt, tracking: 0.14em, upper(role)))
#let cost-tag(body) = box(fill: ink, inset: (x: 4pt, top: 2.4pt, bottom: 1.8pt), baseline: 0.15em,
  text(font: sans, weight: 700, size: 7.2pt, tracking: 0.08em, fill: paper, body))

// Stat bar: black label row with reversed caps, values beneath, heavy rule. Used by monsters,
// scenario monsters and Basic Mode profiles alike.
#let stat-strip(header, values, size: 11.5pt) = block(width: 100%, above: 7pt, below: 6pt, breakable: false, {
  set text(font: sans, number-type: "lining", number-width: "tabular")
  set par(justify: false)
  grid(columns: (1fr,) * header.len(), column-gutter: 0pt, row-gutter: 0pt,
    ..header.map(h => block(width: 100%, fill: ink, inset: (y: 2.6pt), align(center,
      text(size: 6.8pt, weight: 700, tracking: 0.14em, fill: paper, h)))),
    ..values.enumerate().map(((i, v)) => block(width: 100%, inset: (x: 2pt, top: 3.6pt, bottom: 3.8pt),
      stroke: if i > 0 { (left: 0.4pt + hair) } else { none },
      align(center, text(size: size, weight: 600, v)))))
  v(-1pt)
  line(length: 100%, stroke: 1.3pt + ink)
})

// Formula profile (scenario-scaled monsters): label column tinted, values in prose.
#let stat-card(header, values) = block(width: 100%, above: 7pt, below: 7pt, breakable: false, {
  set text(font: sans, size: 9pt, number-type: "lining")
  set par(justify: false, leading: 2.5pt)
  line(length: 100%, stroke: 1.3pt + ink)
  v(-1pt)
  table(columns: (auto, 1fr), inset: (x: 5pt, y: 2.8pt), stroke: (x, y) => (bottom: 0.3pt + hair),
    fill: (x, y) => if x == 0 { ink } else { none },
    ..header.zip(values).map(((h, v)) => (text(weight: 700, size: 7.4pt, tracking: 0.1em, fill: paper, h), v)).flatten())
  v(-2pt)
  line(length: 100%, stroke: 1.3pt + ink)
})

#let anatomy(sections, size: 9.8pt) = for (label, items) in sections {
  label-rule(label)
  set text(size: size)
  set par(leading: 3pt, justify: false)
  for it in items { block(above: 3pt, below: 3pt, par(hanging-indent: 8pt, it)) }
}

// Monster entry = portrait, name + role, flavour, stat bar, labelled anatomy. One keep unit; the
// bestiary sets one entry per column so every page is two complete creatures.
#let monster(name, role, art: none, art-width: 80%, flavour-text, header, values, sections) = block(width: 100%, breakable: false, above: 0pt, below: 14pt)[
  // fixed portrait box: every entry's name sits on the same line across a spread
  #if art != none { block(width: 100%, height: 2.55in, spacing: 0pt, align(center + bottom, image(art, height: 100%, width: art-width, fit: "contain"))); v(2pt) }
  #block(below: 3pt, sticky: true)[
    #set par(justify: false)
    #text(font: fellsc, size: 17pt, name)#h(6pt)#role-tag(role)
  ]
  #flavour(flavour-text, size: 10.6pt)
  #stat-strip(header, values)
  #anatomy(sections)
]

// Class / ancestry / background entry: a tall portrait in the outer column beside the entry head.
#let character-entry(name, tag, art: none, flavour-text, facts, body) = block(width: 100%, breakable: true, above: 0pt)[
  #grid(columns: (1fr, 2.15in), column-gutter: gap, align: top,
    [
      #text(font: sans, weight: 700, size: 8pt, tracking: 0.3em)[HERO CLASS]
      #v(-4pt)
      #text(font: fellsc, size: 30pt, name)#h(8pt)#role-tag(tag)
      #v(-2pt)
      #double-rule()
      #v(4pt)
      #flavour(flavour-text)
      #block(above: 6pt, width: 100%, {
        set text(font: sans, size: 9pt)
        set par(justify: false, leading: 2.5pt)
        table(columns: (auto, 1fr), inset: (x: 5pt, y: 3pt), stroke: (x, y) => (bottom: 0.3pt + hair, top: if y == 0 { 1.3pt + ink } else { none }),
          ..facts.map(((k, v)) => (text(weight: 700, size: 7.6pt, tracking: 0.12em, upper(k)), v)).flatten())
        v(-4pt)
        line(length: 100%, stroke: 1.3pt + ink)
      })
    ],
    if art != none { image(art, width: 100%) })
  #body
]

// Power entry: number and name in display, cost tag, a one-line italic field strip, then effect.
#let power(n, name, cost, fields, effect) = block(width: 100%, breakable: false, above: 8pt, below: 8pt)[
  #set par(justify: false)
  #grid(columns: (14pt, 1fr), column-gutter: 4pt, align: bottom,
    text(font: fellsc, size: 15pt, str(n)), [#text(font: fellsc, size: 14pt, name)#h(6pt)#cost-tag(cost)])
  #v(1pt)
  #block(inset: (left: 18pt), {
    text(font: sans, size: 8.4pt, style: "italic", fill: ink2, fields.map(((k, v)) => [#text(weight: 700, style: "normal")[#k] #v]).join(h(4pt) + sym.dot.c + h(4pt)))
    v(2pt)
    set text(size: 9.8pt)
    effect
  })
]

#let tier-head(title) = block(above: 12pt, below: 6pt, sticky: true, width: 100%, {
  set par(justify: false)
  grid(columns: (auto, 1fr), column-gutter: 7pt, align: horizon,
    text(font: fellsc, size: 13.5pt, title), line(length: 100%, stroke: 0.6pt + ink))
})

// ================================================================ chapter opener
// Art from the top of the frame, chapter word, display title, flourish, italic lead; rules resume
// on the same page. With no art yet, the type alone carries the page (art-light edition).
#let chapter-opener(word, title, art: none, lead: none) = block(width: 100%, breakable: false, above: 0pt, below: 14pt)[
  #if art != none {
    v(-0.3in)
    align(center, image(art, width: 100%))
    v(-4pt)
  } else { v(1.2in) }
  #align(center)[
    #text(font: sans, weight: 700, size: 8.5pt, tracking: 0.42em, upper[Chapter #word])
    #v(-2pt)
    #text(font: fellsc, size: 44pt, hyphenate: false, title)
    #v(-10pt)
    #flourish(len: 70pt)
  ]
  #if lead != none {
    v(6pt)
    align(center, block(width: 80%, {
      set par(justify: false, leading: 4pt)
      set text(font: fell, style: "italic", size: 13pt, fill: ink2)
      lead
    }))
  }
]

// ================================================================ scenario
// Opening: scenario number and display title over a double rule, flavour, then the setup dossier
// (the canonical fields, exactly as labelled in the source) beside the deployment map.
#let scenario-head(num, title, flavour-text, art: none) = block(width: 100%, below: 8pt, breakable: false)[
  #grid(columns: if art != none { (1fr, 1.7in) } else { (1fr,) }, column-gutter: 12pt, align: bottom,
    [
      #text(font: sans, weight: 700, size: 8.5pt, tracking: 0.4em)[SCENARIO #h(2pt) #upper(num)]
      #v(-3pt)
      #text(font: fellsc, size: 28pt, hyphenate: false, title)
      #v(2pt)
      #block(width: 82%, flavour(flavour-text, size: 11pt))
    ],
    ..if art != none { (image(art, width: 100%),) })
  #double-rule()
]

#let dossier(fields) = block(width: 100%, fill: tint, inset: (x: 9pt, y: 8pt), breakable: false,
  stroke: (top: 1.5pt + ink, bottom: 0.45pt + ink))[
  #set text(size: 9.2pt)
  #set par(leading: 2.8pt, justify: false, spacing: 5pt)
  #for (k, v) in fields { block(below: 5pt, [#text(font: sans, weight: 700, size: 7.2pt, tracking: 0.12em, upper(k))\ #v]) }
]

// Closing frame for the victory and tiebreak fields of a scenario.
#let outcome(fields) = block(width: 100%, above: 10pt, breakable: false, inset: (x: 8pt, y: 7pt),
  stroke: (top: 1.5pt + ink, bottom: 1.5pt + ink, left: 0.45pt + ink, right: 0.45pt + ink))[
  #set text(size: 9.6pt)
  #set par(justify: false, leading: 2.9pt)
  #for (k, v) in fields { block(below: 4pt, [#text(weight: 700, k) #v]) }
]

// ================================================================ quick reference (Appendix C)
#let qref-head(code, title) = block(width: 100%, above: 0pt, below: 6pt, fill: ink, inset: (x: 7pt, y: 5pt),
  text(fill: paper)[#text(font: sans, weight: 700, size: 9pt, tracking: 0.1em, code)#h(8pt)#text(font: fellsc, size: 15pt, title)])

// ================================================================ contents and index
#let toc-chapter(num, title, page) = block(above: 9pt, below: 3pt, breakable: false, width: 100%)[
  #grid(columns: (22pt, 1fr, auto), column-gutter: 6pt, align: bottom,
    text(font: fellsc, size: 18pt, num), text(font: fellsc, size: 14pt, title),
    text(font: fellsc, size: 12pt, str(page)))
  #v(-3pt)
  #line(length: 100%, stroke: 0.8pt + ink)
]
#let toc-line(num, title, page) = block(above: 2.6pt, below: 2.6pt, {
  set text(font: serif, size: 9.4pt)
  grid(columns: (22pt, 1fr, auto), column-gutter: 6pt,
    text(font: sans, size: 8.4pt, weight: 600, fill: ink3, num),
    box(width: 100%)[#title #box(width: 1fr, repeat(gap: 2.4pt)[#text(fill: ink3)[.]])],
    text(font: sans, size: 8.8pt, str(page)))
})

#let index-letter(l) = block(above: 9pt, below: 3pt, sticky: true,
  grid(columns: (auto, 1fr), column-gutter: 5pt, align: horizon,
    text(font: fellsc, size: 22pt, l), line(length: 100%, stroke: 0.5pt + ink)))
#let index-entry(term, pages, sub: false) = block(above: 1.4pt, below: 1.4pt, {
  set text(font: sans, size: 8.6pt)
  set par(hanging-indent: 10pt, justify: false, leading: 2.3pt)
  if sub { h(8pt) }
  [#term#h(4pt)#text(fill: ink2, pages)]
})

// ================================================================ gazetteer (places of the world)
// Wide art, display name over a short rule, lore in the reading italic. Two places per page; a
// place never splits. Lore keeps the source's italic; display italic is reserved for short flavour.
#let gazetteer(name, kicker, art: none, body) = block(width: 100%, breakable: false, above: 0pt, below: 16pt)[
  #if art != none { align(center, image(art, width: 100%)); v(-2pt) }
  #grid(columns: (auto, 1fr), column-gutter: 9pt, align: horizon,
    text(font: fellsc, size: 22pt, name),
    text(font: sans, weight: 700, size: 7.4pt, tracking: 0.24em, fill: ink3, upper(kicker)))
  #v(-1pt)
  #double-rule(heavy: 1.1pt)
  #v(3pt)
  #block(width: 78%, {
    set text(style: "italic", size: 10.5pt)
    set par(leading: 3.6pt, spacing: 7pt)
    body
  })
]
