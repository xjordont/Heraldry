// HERALDRY SKIRMISH — book design system v3 ("Grim Heraldry").
// Page templates and components for every page type in the book; the plan and rationale are in
// docs/BOOK_DESIGN_PLAN.md, the reference evidence in docs/design/REFERENCE_STUDY.md.
// Self-contained: specimens use it today, and the book build adopts it component by component
// (names and signatures follow typst/heraldry.typ where the two overlap).
//
// Direction (owner 2026-10-12): ornate and grim, but clarity and ease of use first. Ornament lives
// at boundaries (bands, rules, corners, tabs); reading text and table cells stay plain and open.

// ================================================================ tokens
#let substrate-name = sys.inputs.at("substrate", default: "cream")
#let paper = if substrate-name == "white" { rgb("#FFFFFF") } else { rgb("#FCFAF5") }
#let ink = rgb(0, 0, 0)
#let ink2 = luma(22%)                 // secondary text, still reads as black on inkjet
#let ink3 = luma(45%)                 // furniture labels and secondary caption parts
#let hair = rgb(0, 0, 0, 26%)         // hairlines between rows and column guides
#let tint = rgb(0, 0, 0, 6%)          // banding, example and panel fields (transparent)
#let tint2 = rgb(0, 0, 0, 11%)        // key column of ledgers

#let serif = "Source Serif 4"         // reading text
#let sans = "Source Sans 3"           // data, labels, navigation
#let goth = "Grenze Gotisch"          // display blackletter: titles and names (never all caps)
#let fell = "IM FELL English"         // flavour italic and leads

#let page-w = 612pt
#let page-h = 792pt
#let m-in = 0.875in                   // binding side
#let m-out = 0.62in
#let m-top = 0.82in
#let m-bot = 0.82in
#let gap = 0.25in
#let frame-w = page-w - m-in - m-out
#let col-w = (frame-w - gap) / 2
#let edge-safe = 0.375in

#let body-size = 10.25pt
#let body-lead = 3.35pt               // line pitch about 13.4pt

// ================================================================ the armoury (original vector marks)
// Rivet: an iron stud with a struck highlight. `on-black` draws a paper stud on a black band.
#let rivet(d: 4.4pt, on-black: false) = box(width: d, height: d, baseline: 15%, {
  place(circle(radius: d / 2, fill: if on-black { paper } else { ink }))
  place(dx: d * 0.22, dy: d * 0.2, circle(radius: d * 0.14, fill: if on-black { ink } else { paper }))
})

#let lozenge(size: 6pt, fill: ink) = box(width: size, height: size, baseline: 0.05em,
  polygon(fill: fill, (size / 2, 0pt), (size, size / 2), (size / 2, size), (0pt, size / 2)))

// Skull: cranium, jaw, sockets, nasal cavity and teeth. A grim mark kept to openers, terminals of
// major tables and the cover; never a running bullet.
#let skull(s: 10pt, fill: ink) = box(width: s, height: s * 1.08, baseline: 18%, {
  let g = if fill == ink { paper } else { ink }
  place(dx: 0pt, dy: 0pt, ellipse(width: s, height: s * 0.82, fill: fill))
  place(dx: s * 0.22, dy: s * 0.62, rect(width: s * 0.56, height: s * 0.44, radius: s * 0.08, fill: fill))
  place(dx: s * 0.16, dy: s * 0.34, ellipse(width: s * 0.27, height: s * 0.24, fill: g))
  place(dx: s * 0.57, dy: s * 0.34, ellipse(width: s * 0.27, height: s * 0.24, fill: g))
  place(polygon(fill: g, (s * 0.5, s * 0.58), (s * 0.43, s * 0.7), (s * 0.57, s * 0.7)))
  for i in range(3) { place(dx: s * (0.36 + i * 0.14), dy: s * 0.82, rect(width: s * 0.04, height: s * 0.2, fill: g)) }
})

// Heater shield, w wide; the body sits centred in the upper part.
#let shield(w: 14pt, fill: ink, stroke: none, inner: false, body: none) = box(width: w, height: w * 1.18, baseline: 20%, {
  let h = w * 1.18
  let outline(w, h, dx, dy, fill, stroke) = place(dx: dx, dy: dy, curve(fill: fill, stroke: stroke,
    curve.move((0pt, 0pt)), curve.line((w, 0pt)), curve.line((w, h * 0.42)),
    curve.cubic((w, h * 0.78), (w * 0.62, h * 0.9), (w * 0.5, h)),
    curve.cubic((w * 0.38, h * 0.9), (0pt, h * 0.78), (0pt, h * 0.42)), curve.close()))
  outline(w, h, 0pt, 0pt, fill, stroke)
  if inner { let k = w * 0.1; outline(w - 2 * k, h - 2.3 * k, k, k, none, (0.45pt + paper)) }
  if body != none { place(center + top, dy: h * 0.15, box(width: w, align(center, body))) }
})

// Thorn rule: a briar stem with alternating hooked thorns, filling the available width.
#let thorn-rule(weight: 1.1pt, every: 7.5pt, hook: 2.6pt) = layout(size => {
  let w = size.width
  let n = calc.max(1, int(w / every))
  let y0 = hook + 0.5pt
  box(width: w, height: 2 * y0 + weight, {
    place(dy: y0, line(length: w, stroke: weight + ink))
    for i in range(n) {
      let x = (i + 0.5) * w / n
      let up = calc.even(i)
      let base = y0 + weight / 2
      let tip = if up { y0 - hook } else { y0 + weight + hook }
      place(polygon(fill: ink, (x - 1.3pt, base), (x + 1.3pt, base), (x + 1.9pt, tip)))
    }
  })
})

// Iron rule: a heavy bar ending in rivets, with an optional centrepiece (skull, shield...).
#let iron-rule(weight: 1.6pt, piece: none) = block(width: 100%, above: 0pt, below: 0pt,
  grid(columns: if piece != none { (auto, 1fr, auto, 1fr, auto) } else { (auto, 1fr, auto) },
    column-gutter: 3pt, align: horizon,
    rivet(d: 4.6pt), line(length: 100%, stroke: weight + ink),
    ..if piece != none { (piece, line(length: 100%, stroke: weight + ink)) },
    rivet(d: 4.6pt)))

// Iron band: a black strap with an engraved inner line and a rivet at each end. Holds headings
// such as reference heads, caption bars and section labels; text inside is reversed.
#let band(body, inset: (x: 13pt, y: 4.2pt), width: 100%) = block(width: width, fill: ink, inset: 1.8pt, spacing: 0pt,
  block(width: 100%, stroke: 0.45pt + paper, inset: inset, spacing: 0pt, {
    place(left + horizon, dx: -9.5pt, rivet(d: 3.6pt, on-black: true))
    place(right + horizon, dx: 9.5pt, rivet(d: 3.6pt, on-black: true))
    body
  }))

// Banner tag: a short black strap with a pointed (or swallowtail) right end.
#let tag(body, size: 7pt, swallow: false) = box(baseline: 22%, {
  let t = text(font: sans, weight: 700, size: size, tracking: 0.16em, fill: paper, upper(body))
  context {
    let m = measure(t)
    let h = m.height + 6pt
    let w = m.width + 14pt
    box(width: w, height: h, {
      place(polygon(fill: ink, (0pt, 0pt), (w - 5pt, 0pt), (w, h / 2), (w - 5pt, h), (0pt, h),
        ..if swallow { () } else { () }))
      if swallow { place(polygon(fill: paper, (w - 5pt, 0pt), (w + 0.5pt, 0pt), (w - 1.5pt, h / 2), (w + 0.5pt, h), (w - 5pt, h))) }
      place(left + horizon, dx: 5pt, t)
    })
  }
})

// Iron corner plate: an L-bracket of forged strap with a riveted boss and a thorn spike pointing
// inward. `corner` is one of "tl", "tr", "bl", "br".
#let corner-iron(corner, s: 16pt, t: 2.4pt) = box(width: s, height: s, {
  let fx = if corner.ends-with("r") { (x) => s - x } else { (x) => x }
  let fy = if corner.starts-with("b") { (y) => s - y } else { (y) => y }
  let p(x, y) = (fx(x), fy(y))
  place(polygon(fill: ink, p(0pt, 0pt), p(s, 0pt), p(s - t * 0.9, t), p(t, t), p(t, s - t * 0.9), p(0pt, s)))
  place(polygon(fill: ink, p(0pt, 0pt), p(s * 0.42, 0pt), p(s * 0.42, s * 0.42), p(0pt, s * 0.42)))
  place(polygon(fill: ink, p(s * 0.34, s * 0.42), p(s * 0.42, s * 0.34), p(s * 0.7, s * 0.7)))
  let c = p(s * 0.21, s * 0.21)
  place(dx: c.at(0) - 1.5pt, dy: c.at(1) - 1.5pt, circle(radius: 1.5pt, fill: paper))
})

// Iron-cornered panel: a block with corner plates; optional tint field.
#let ironclad(body, fill: none, inset: (x: 11pt, y: 10pt), s: 14pt) = block(width: 100%, breakable: false, fill: fill, {
  block(width: 100%, inset: inset, spacing: 0pt, body)
  place(top + left, corner-iron("tl", s: s))
  place(top + right, corner-iron("tr", s: s))
  place(bottom + left, corner-iron("bl", s: s))
  place(bottom + right, corner-iron("br", s: s))
})

// Flourish for openers: thorns, rivet, skull, rivet, thorns.
#let flourish(len: 70pt, piece: none) = box(baseline: 30%,
  grid(columns: (len, auto, auto, auto, len), column-gutter: 4pt, align: horizon,
    thorn-rule(weight: 1pt), rivet(d: 4pt), if piece != none { piece } else { skull(s: 11pt) }, rivet(d: 4pt), thorn-rule(weight: 1pt)))

// Label with a thorn rule running to the margin: the entry-anatomy separator.
#let label-rule(body, size: 7.4pt) = block(above: 7.5pt, below: 3.5pt, sticky: true, width: 100%,
  grid(columns: (auto, 1fr), column-gutter: 5pt, align: horizon,
    text(font: sans, weight: 700, size: size, tracking: 0.14em, upper(body)),
    line(length: 100%, stroke: 0.5pt + ink)))

// Drop capital: a black block with an engraved inner line and the blackletter initial reversed,
// three lines deep (vendored droplet 0.3.1, MIT, typst/vendor/).
#import "../vendor/droplet-0.3.1/src/lib.typ": dropcap as _dropcap
#let dropcap(body, lines: 3) = _dropcap(height: lines, gap: 5pt, hanging-indent: 0pt,
  transform: letter => box(fill: ink, inset: 1.6pt, box(stroke: 0.45pt + paper, inset: (x: 4pt, top: 3pt, bottom: 4pt),
    text(font: goth, weight: 600, fill: paper, letter))), body)

// ================================================================ running furniture
// Chapter tabs: tall black pennants hanging from the outer edge, one fixed slot per part, carrying
// the part's keyword rotated along the edge (owner 2026-10-12). Navigation only: the running head
// names the chapter too, so a tab trimmed by overscan loses nothing.
#let tab-keys = ("World", "Mechanics", "Round", "Actions", "Combat", "Party", "Equipment", "Powers",
  "Monsters", "Scenarios", "Campaign", "Learn", "Basic", "Reference", "Index")
#let thumb-tab(n, recto) = {
  let top0 = 0.42in
  let slot-h = (page-h - 2 * top0) / tab-keys.len()
  let y = top0 + slot-h * (n - 1)
  let w = 0.4in
  let h = slot-h - 3pt
  let k = 5pt                                   // pointed inner end
  let pts = if recto { ((w, 0pt), (k, 0pt), (0pt, k), (0pt, h - k), (k, h), (w, h)) }
            else { ((0pt, 0pt), (w - k, 0pt), (w, k), (w, h - k), (w - k, h), (0pt, h)) }
  let inner = if recto { ((w, 2pt), (k + 0.8pt, 2pt), (2pt, k + 0.8pt), (2pt, h - k - 0.8pt), (k + 0.8pt, h - 2pt), (w, h - 2pt)) }
              else { ((0pt, 2pt), (w - k - 0.8pt, 2pt), (w - 2pt, k + 0.8pt), (w - 2pt, h - k - 0.8pt), (w - k - 0.8pt, h - 2pt), (0pt, h - 2pt)) }
  let word = text(font: sans, weight: 700, size: 6.9pt, tracking: 0.05em, fill: paper, upper(tab-keys.at(n - 1)))
  place(top + left, dx: if recto { page-w - w } else { 0pt }, dy: y, box(width: w, height: h, {
    place(polygon(fill: ink, ..pts))
    place(polygon(fill: none, stroke: 0.45pt + paper, ..inner))
    // keyword reads top-to-bottom on the right edge, bottom-to-top on the left; sits 0.17in in
    place(horizon + left, dx: if recto { 0.07in } else { w - 0.07in - 9pt },
      box(width: 9pt, height: h, align(center + horizon,
        rotate(if recto { 90deg } else { -90deg }, reflow: true, box(width: h - 2pt, align(center, word))))))
  }))
}

#let running-head(left-text, right-text, recto) = {
  set text(font: sans, size: 7.4pt, weight: 600, tracking: 0.16em, fill: ink2)
  block(width: 100%, below: 0pt, {
    if recto [#h(1fr)#upper(right-text)#h(6pt)#rivet(d: 4pt)] else [#rivet(d: 4pt)#h(6pt)#upper(left-text)#h(1fr)]
    v(1pt)
    thorn-rule(weight: 0.8pt, every: 9pt, hook: 2pt)
  })
}

#let folio(n, recto) = {
  let sh = shield(w: 20pt, inner: true, body: text(font: sans, size: 7.8pt, weight: 700, fill: paper, number-type: "lining", str(n)))
  let rule = box(width: 46pt, baseline: -7pt, thorn-rule(weight: 0.7pt, every: 8pt, hook: 1.8pt))
  if recto { align(right)[#rule#h(4pt)#sh] } else { align(left)[#sh#h(4pt)#rule] }
}

// Opener frame: a double-ruled border with iron corners and a skull at the head; openers only.
#let opener-frame(recto, n: none) = {
  let x0 = 0.45in
  let y0 = 0.45in
  let w = page-w - 2 * x0
  let h = page-h - 2 * y0
  place(top + left, dx: x0, dy: y0, box(width: w, height: h, {
    place(rect(width: w, height: h, stroke: 1.6pt + ink))
    place(dx: 4pt, dy: 4pt, rect(width: w - 8pt, height: h - 8pt, stroke: 0.5pt + ink))
    place(top + left, dx: -3pt, dy: -3pt, corner-iron("tl", s: 30pt, t: 3.6pt))
    place(top + right, dx: 3pt, dy: -3pt, corner-iron("tr", s: 30pt, t: 3.6pt))
    place(bottom + left, dx: -3pt, dy: 3pt, corner-iron("bl", s: 30pt, t: 3.6pt))
    place(bottom + right, dx: 3pt, dy: 3pt, corner-iron("br", s: 30pt, t: 3.6pt))
    place(top + center, dy: -7pt, box(fill: paper, inset: (x: 5pt), skull(s: 13pt)))
    place(bottom + center, dy: 13pt, box(fill: paper, inset: (x: 5pt), grid(columns: 3, column-gutter: 4pt, align: horizon, rivet(d: 4pt),
      if n != none { shield(w: 20pt, inner: true, body: text(font: sans, size: 7.8pt, weight: 700, fill: paper, str(n))) } else { lozenge(size: 7pt) },
      rivet(d: 4pt))))
  }))
}

// A page shell for specimens: furniture comes from explicit arguments (the book derives it).
#let shell(n, chapter: "", section: "", tab: none, furniture: true, folio-on: true, frame: false, body) = {
  let recto = calc.odd(n)
  set page(width: page-w, height: page-h, fill: paper,
    margin: if recto { (left: m-in, right: m-out, top: m-top, bottom: m-bot) }
            else { (left: m-out, right: m-in, top: m-top, bottom: m-bot) },
    header: if furniture { running-head(chapter, section, recto) },
    header-ascent: 16pt,
    footer: if folio-on and not frame { folio(n, recto) },
    footer-descent: 16pt,
    background: {
      if frame { opener-frame(recto, n: if folio-on { n }) }
      if tab != none { thumb-tab(tab, recto) }
    },
  )
  body
}

// ================================================================ base text
#let base(body) = {
  set text(font: serif, size: body-size, lang: "en", region: "CA", fill: ink, hyphenate: true,
    top-edge: 0.8em, bottom-edge: -0.25em, number-type: "lining")
  set par(leading: body-lead, spacing: 6.5pt, justify: false, first-line-indent: 0pt)
  set strong(delta: 200)
  set list(marker: (box(baseline: -1.2pt, lozenge(size: 4.4pt)), [–]), indent: 1pt, body-indent: 6pt, spacing: 4.5pt)
  set enum(indent: 1pt, body-indent: 6pt, spacing: 4.5pt, numbering: n => text(font: sans, weight: 700, size: 9pt)[#n.])
  body
}

// ================================================================ headings
// Numbered section (x.y): number on a black shield, blackletter title, briar rule beneath.
#let section(num, title) = block(above: 4pt, below: 11pt, sticky: true, width: 100%, breakable: false)[
  #set par(justify: false)
  #grid(columns: (auto, 1fr), column-gutter: 9pt, align: horizon,
    shield(w: 25pt, inner: true, body: text(font: sans, weight: 700, size: if num.len() > 3 { 7.6pt } else { 9pt }, fill: paper, num)),
    text(font: goth, weight: 600, size: 24pt, hyphenate: false, title))
  #v(1pt)
  #thorn-rule(weight: 1.3pt, every: 8pt, hook: 3pt)
]

// Subsection (x.y.z): serif bold with a quiet sans number and a rivet.
#let subsection(num, title) = block(above: 13pt, below: 5pt, sticky: true)[
  #set par(justify: false)
  #rivet(d: 4.4pt)#h(5pt)#if num != none [#text(font: sans, weight: 700, size: 9.5pt, fill: ink3, num)#h(5pt)]#text(font: serif, weight: 700, size: 12.5pt, title)
]

// Minor named heading inside a subsection.
#let minor(title) = block(above: 10pt, below: 3pt, sticky: true, text(font: goth, weight: 500, size: 14pt, title))

// Run-in label for definition-style paragraphs ("Primary Objective:" etc.).
#let runin(label, body) = par[#text(weight: 700, label)#h(0.3em)#body]

// ================================================================ text components
#let flavour(body, size: 11.2pt) = block(above: 3pt, below: 8pt, {
  set par(justify: false, leading: 3.6pt)
  text(font: fell, style: "italic", size: size, fill: ink2, body)
})

// Worked example: tinted field on an iron spine (riveted top and bottom), banner tag.
#let example(title: none, body) = block(width: 100%, above: 10pt, below: 11pt, breakable: true,
  fill: tint, stroke: (left: 3pt + ink), inset: (left: 11pt, right: 9pt, top: 7pt, bottom: 9pt))[
  #place(top + left, dx: -11pt - 3.7pt, dy: -7pt - 2pt, rivet(d: 4.4pt))
  #place(bottom + left, dx: -11pt - 3.7pt, dy: 9pt + 2pt, rivet(d: 4.4pt))
  #tag([Example#if title != none [ #h(2pt)·#h(2pt) #title]])
  #v(3pt)
  #set text(size: 9.8pt)
  #set par(leading: 3.1pt)
  #body
]

// Rules note: iron-cornered panel with a centred band tag.
#let note-box(tag-text: "Rules Note", body) = block(width: 100%, above: 13pt, below: 12pt, breakable: false)[
  #ironclad(inset: (x: 12pt, top: 14pt, bottom: 10pt), s: 13pt)[#set text(size: 9.8pt); #set par(leading: 3.1pt); #body]
  #place(top + center, dy: -6pt, box(fill: paper, inset: (x: 3pt), tag(tag-text)))
]

// Procedure: numbered steps on black shields down an iron spine.
#let procedure(title: none, steps) = block(width: 100%, above: 9pt, below: 10pt, breakable: true)[
  #if title != none { label-rule(title) }
  #for (i, s) in steps.enumerate() {
    block(above: 5pt, below: 5pt, breakable: false,
      grid(columns: (17pt, 1fr), column-gutter: 6pt,
        shield(w: 15pt, body: text(font: sans, weight: 700, size: 8pt, fill: paper, str(i + 1))),
        s))
  }
]

// ================================================================ tables: the ledger
// Built for reading first. Every table has: a blackletter title on a shield and rule; a black
// header band with rivets; generous rows with light banding; faint column guides; a bold key
// column; and an iron closing rule (skull centrepiece on titled tables). Roll results sit in black
// shields. Long text in a row can move to a spanning second line (`notes`).
#let table-title(body) = block(below: 5pt, sticky: true, width: 100%,
  grid(columns: (auto, auto, 1fr), column-gutter: 6pt, align: horizon,
    shield(w: 11pt), text(font: goth, weight: 600, size: 15pt, body), thorn-rule(weight: 0.9pt, every: 8pt, hook: 2.2pt)))

#let ref-table(widths, aligns, header, rows, title: none, roll: false, band: true, key: true, notes: none, size: 9.3pt) = {
  set text(font: sans, size: size, number-type: "lining", number-width: "tabular", hyphenate: false)
  set par(leading: 2.7pt, spacing: 4pt, justify: false)
  let n = header.len()
  let ix = 5.5pt
  let iy = 4.1pt
  let cells = ()
  let r = 0
  for (i, row) in rows.enumerate() {
    cells += row.enumerate().map(((x, c)) => table.cell(
      if roll and x == 0 { shield(w: 15pt, body: text(weight: 700, size: 8.2pt, fill: paper, c)) }
      else if key and x == (if roll { 1 } else { 0 }) { text(weight: 700, c) } else { c }))
    if notes != none and notes.at(i, default: none) != none {
      cells.push(table.cell(colspan: n, inset: (left: 16pt, right: 6pt, top: 0pt, bottom: 4.5pt),
        text(size: size - 0.6pt, fill: ink2, notes.at(i))))
    }
  }
  let head = header.enumerate().map(((i, h)) => table.cell({
    if i == 0 { place(left + horizon, dx: -9pt, rivet(d: 3.4pt, on-black: true)) }
    if i == n - 1 { place(right + horizon, dx: 9pt, rivet(d: 3.4pt, on-black: true)) }
    text(weight: 700, size: 7.8pt, tracking: 0.1em, fill: paper, upper(h))
  }))
  block(width: 100%, above: 10pt, below: 12pt, breakable: true)[
    #if title != none { table-title(title) }
    #table(
      columns: widths,
      align: (x, y) => aligns.at(x, default: left) + horizon,
      inset: (x, y) => (x: ix, y: iy) + if y == 0 { (left: if x == 0 { ix + 7pt } else { ix }, right: if x == n - 1 { ix + 7pt } else { ix }) } else { (:) },
      fill: (x, y) => if y == 0 { ink } else if roll and x == 0 { tint2 } else if band and calc.even(y) { tint } else { none },
      stroke: (x, y) => (
        bottom: if y == 0 { none } else { 0.3pt + hair },
        left: if y > 0 and x > 0 { 0.3pt + hair } else if y > 0 and x == 0 { 0.8pt + ink } else { none },
        right: if y > 0 and x == n - 1 { 0.8pt + ink } else { none },
      ),
      table.header(repeat: true, ..head),
      ..cells,
    )
    #v(-2pt)
    #iron-rule(weight: 1.8pt, piece: if title != none { skull(s: 9pt) } else { lozenge(size: 6pt) })
  ]
}

// ================================================================ figures and art
// The caption is welded to the figure: an iron band carries the number and title, the caption
// sits directly beneath, closed by an iron rule.
#let figure-block(id, title, file, caption, width: 100%) = block(width: 100%, above: 10pt, below: 12pt, breakable: false)[
  #align(center, image(file, width: width))
  #v(4pt)
  #band(inset: (x: 13pt, y: 3.2pt), text(font: sans, size: 7.8pt, weight: 700, tracking: 0.1em, fill: paper)[#id #h(4pt)#lozenge(size: 4pt, fill: paper)#h(4pt) #upper(title)])
  #block(width: 100%, inset: (x: 6pt, top: 4.5pt, bottom: 5pt), spacing: 0pt, {
    set text(font: sans, size: 8.6pt)
    set par(leading: 2.5pt, justify: false)
    caption
  })
  #line(length: 100%, stroke: 0.6pt + ink)
]

// Spot art: open-edged ink vignette; the art carries its own white fade, so no frame or rule.
#let spot(file, width: 100%) = block(width: 100%, above: 6pt, below: 8pt, breakable: false,
  align(center, image(file, width: width)))

// ================================================================ profiles and entries
#let role-tag(role) = tag(role, size: 6.6pt)
#let cost-tag(body) = box(fill: ink, inset: (x: 4pt, top: 2.4pt, bottom: 1.8pt), baseline: 0.15em,
  text(font: sans, weight: 700, size: 7.2pt, tracking: 0.08em, fill: paper, body))

// Stat bar: black label row riveted at each end, values beneath in large sans, iron close.
#let stat-strip(header, values, size: 12pt) = block(width: 100%, above: 7pt, below: 6pt, breakable: false, {
  set text(font: sans, number-type: "lining", number-width: "tabular")
  set par(justify: false)
  block(width: 100%, spacing: 0pt, {
    grid(columns: (1fr,) * header.len(), column-gutter: 0pt, row-gutter: 0pt,
      ..header.map(h => block(width: 100%, fill: ink, inset: (y: 3pt), align(center,
        text(size: 6.8pt, weight: 700, tracking: 0.14em, fill: paper, h)))),
      ..values.enumerate().map(((i, v)) => block(width: 100%, inset: (x: 2pt, top: 3.8pt, bottom: 4pt),
        stroke: if i > 0 { (left: 0.4pt + hair) } else { none },
        align(center, text(size: size, weight: 600, v)))))
    place(top + left, dx: 3pt, dy: 3.5pt, rivet(d: 3.2pt, on-black: true))
    place(top + right, dx: -3pt, dy: 3.5pt, rivet(d: 3.2pt, on-black: true))
  })
  iron-rule(weight: 1.6pt)
})

// Formula profile (scenario-scaled monsters): black label column, values in prose.
#let stat-card(header, values) = block(width: 100%, above: 7pt, below: 7pt, breakable: false, {
  set text(font: sans, size: 9pt, number-type: "lining")
  set par(justify: false, leading: 2.5pt)
  table(columns: (auto, 1fr), inset: (x: 6pt, y: 3.4pt), stroke: (x, y) => (bottom: 0.3pt + hair, right: if x == 1 { 0.8pt + ink } else { none }),
    fill: (x, y) => if x == 0 { ink } else if calc.odd(y) { tint } else { none },
    ..header.zip(values).map(((h, v)) => (text(weight: 700, size: 7.4pt, tracking: 0.1em, fill: paper, h), v)).flatten())
  v(-2pt)
  iron-rule(weight: 1.6pt)
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
  // fixed portrait box: every entry's name sits on the same line across a page
  #if art != none { block(width: 100%, height: 2.5in, spacing: 0pt, align(center + bottom, image(art, height: 100%, width: art-width, fit: "contain"))); v(2pt) }
  #block(below: 2pt, sticky: true)[
    #set par(justify: false)
    #text(font: goth, weight: 600, size: 21pt, name)#h(7pt)#role-tag(role)
  ]
  #thorn-rule(weight: 0.8pt, every: 8pt, hook: 2pt)
  #flavour(flavour-text, size: 10.6pt)
  #stat-strip(header, values)
  #anatomy(sections)
]

// Class / ancestry / background entry: a tall portrait in the outer column beside the entry head.
#let character-entry(name, kicker, tag-text, art: none, flavour-text, facts, body) = block(width: 100%, breakable: true, above: 0pt)[
  #grid(columns: (1fr, 2.15in), column-gutter: gap, align: top,
    [
      #text(font: sans, weight: 700, size: 8pt, tracking: 0.3em, upper(kicker))
      #v(-6pt)
      #text(font: goth, weight: 600, size: 36pt, name)#h(8pt)#role-tag(tag-text)
      #v(-4pt)
      #thorn-rule(weight: 1.3pt, every: 8pt, hook: 3pt)
      #v(4pt)
      #flavour(flavour-text)
      #block(above: 6pt, width: 100%, {
        set text(font: sans, size: 9pt)
        set par(justify: false, leading: 2.5pt)
        table(columns: (auto, 1fr), inset: (x: 6pt, y: 3.4pt), stroke: (x, y) => (bottom: 0.3pt + hair),
          fill: (x, y) => if x == 0 { ink } else if calc.odd(y) { tint } else { none },
          ..facts.map(((k, v)) => (text(weight: 700, size: 7.4pt, tracking: 0.1em, fill: paper, upper(k)), v)).flatten())
        v(-2pt)
        iron-rule(weight: 1.6pt)
      })
    ],
    if art != none { image(art, width: 100%) })
  #body
]

// Power entry: shield numeral, blackletter name, cost tag, italic field strip, then effect.
#let power(n, name, cost, fields, effect) = block(width: 100%, breakable: false, above: 8pt, below: 8pt)[
  #set par(justify: false)
  #grid(columns: (15pt, 1fr), column-gutter: 5pt, align: horizon,
    shield(w: 14pt, body: text(font: sans, weight: 700, size: 7.6pt, fill: paper, str(n))),
    [#text(font: goth, weight: 600, size: 15.5pt, name)#h(6pt)#cost-tag(cost)])
  #v(1pt)
  #block(inset: (left: 20pt), {
    text(font: sans, size: 8.4pt, style: "italic", fill: ink2, fields.map(((k, v)) => [#text(weight: 700, style: "normal")[#k] #v]).join(h(4pt) + sym.dot.c + h(4pt)))
    v(2pt)
    set text(size: 9.8pt)
    effect
  })
]

#let tier-head(title) = block(above: 12pt, below: 6pt, sticky: true, width: 100%, band(inset: (x: 13pt, y: 3.4pt),
  text(font: goth, weight: 600, size: 13pt, fill: paper, title)))

// ================================================================ chapter opener
// Framed page (opener-frame in the shell): art at the head, "Chapter One" between briars, the
// blackletter title, the skull flourish and the italic lead; rules resume on the same page with a
// drop capital. With no art yet, the type alone carries the page (owner 2026-10-12).
#let chapter-opener(word, title, art: none, lead: none) = block(width: 100%, breakable: false, above: 0pt, below: 14pt)[
  #if art != none {
    v(-0.12in)
    align(center, image(art, width: 96%))
    v(-6pt)
  } else { v(1.2in) }
  #align(center)[
    #grid(columns: (60pt, auto, 60pt), column-gutter: 8pt, align: horizon,
      thorn-rule(weight: 0.9pt, every: 8pt, hook: 2.2pt),
      text(font: sans, weight: 700, size: 8.5pt, tracking: 0.42em, upper[Chapter #word]),
      thorn-rule(weight: 0.9pt, every: 8pt, hook: 2.2pt))
    #v(-4pt)
    #text(font: goth, weight: 600, size: 50pt, hyphenate: false, title)
    #v(-8pt)
    #flourish(len: 80pt)
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
#let scenario-head(num, title, flavour-text, art: none) = block(width: 100%, below: 8pt, breakable: false)[
  #grid(columns: if art != none { (1fr, 1.7in) } else { (1fr,) }, column-gutter: 12pt, align: bottom,
    [
      #tag([Scenario #h(2pt) #num], size: 7.6pt)
      #v(-2pt)
      #text(font: goth, weight: 600, size: 32pt, hyphenate: false, title)
      #v(0pt)
      #block(width: 84%, flavour(flavour-text, size: 11pt))
    ],
    ..if art != none { (image(art, width: 100%),) })
  #thorn-rule(weight: 1.3pt, every: 8pt, hook: 3pt)
]

// Setup dossier: the source's labelled setup fields in an iron-cornered tinted panel.
#let dossier(fields) = block(width: 100%, above: 10pt, breakable: false, ironclad(fill: tint, inset: (x: 12pt, y: 11pt))[
  #set text(size: 9.2pt)
  #set par(leading: 2.8pt, justify: false, spacing: 5pt)
  #for (k, v) in fields { block(below: 5.5pt, [#text(font: sans, weight: 700, size: 7.2pt, tracking: 0.12em, upper(k))\ #v]) }
])

// Closing frame for the victory and tiebreak fields of a scenario.
#let outcome(fields) = block(width: 100%, above: 10pt, breakable: false, ironclad(inset: (x: 12pt, y: 10pt))[
  #set text(size: 9.6pt)
  #set par(justify: false, leading: 2.9pt)
  #for (k, v) in fields { block(below: 4pt, [#text(weight: 700, k) #v]) }
])

// ================================================================ quick reference (Appendix C)
#let qref-head(code, title) = block(width: 100%, above: 0pt, below: 7pt,
  band(inset: (x: 14pt, y: 5pt), text(fill: paper)[
    #box(baseline: 30%, shield(w: 15pt, fill: paper, body: text(font: sans, weight: 700, size: 6.8pt, fill: ink, code)))#h(9pt)#text(font: goth, weight: 600, size: 18pt, title)#h(1fr)#text(font: sans, weight: 700, size: 7pt, tracking: 0.2em)[RULES REFERENCE]]))

// ================================================================ contents and index
#let toc-chapter(num, title, page) = block(above: 9pt, below: 3pt, breakable: false, width: 100%)[
  #grid(columns: (22pt, 1fr, auto), column-gutter: 6pt, align: horizon,
    shield(w: 18pt, inner: true, body: text(font: sans, weight: 700, size: 8.4pt, fill: paper, num)),
    text(font: goth, weight: 600, size: 16pt, title),
    text(font: sans, weight: 700, size: 10pt, str(page)))
  #v(-3pt)
  #thorn-rule(weight: 0.9pt, every: 8pt, hook: 2pt)
]
#let toc-line(num, title, page) = block(above: 2.6pt, below: 2.6pt, {
  set text(font: serif, size: 9.4pt)
  grid(columns: (22pt, 1fr, auto), column-gutter: 6pt,
    text(font: sans, size: 8.4pt, weight: 600, fill: ink3, num),
    box(width: 100%)[#title #box(width: 1fr, repeat(gap: 2.4pt)[#text(fill: ink3)[.]])],
    text(font: sans, size: 8.8pt, str(page)))
})

#let index-letter(l) = block(above: 9pt, below: 3pt, sticky: true,
  grid(columns: (auto, 1fr), column-gutter: 6pt, align: horizon,
    box(fill: ink, inset: 1.4pt, box(stroke: 0.45pt + paper, inset: (x: 4pt, top: 1pt, bottom: 3pt), text(font: goth, weight: 600, size: 18pt, fill: paper, l))),
    thorn-rule(weight: 0.8pt, every: 8pt, hook: 2pt)))
#let index-entry(term, pages, sub: false) = block(above: 1.4pt, below: 1.4pt, {
  set text(font: sans, size: 8.6pt)
  set par(hanging-indent: 10pt, justify: false, leading: 2.3pt)
  if sub { h(8pt) }
  [#term#h(4pt)#text(fill: ink2, pages)]
})

// ================================================================ gazetteer (places of the world)
#let gazetteer(name, kicker, art: none, body) = block(width: 100%, breakable: false, above: 0pt, below: 16pt)[
  #if art != none { align(center, image(art, width: 100%)); v(-2pt) }
  #grid(columns: (auto, auto, 1fr), column-gutter: 9pt, align: horizon,
    text(font: goth, weight: 600, size: 28pt, name), role-tag(kicker), [])
  #v(-3pt)
  #thorn-rule(weight: 1.2pt, every: 8pt, hook: 2.8pt)
  #v(4pt)
  #block(width: 78%, {
    set text(style: "italic", size: 10.5pt)
    set par(leading: 3.6pt, spacing: 7pt)
    body
  })
]
