// Hero-sheet kit, second design. Every panel is an engraved plate: a heavy outer rule, a fine inner
// rule, concave notched corners with a lozenge jewel, and a swallowtail ribbon title. Scores stand
// in heater shields with a black chief, fixed values sit in double-ringed roundels, and the portrait
// stands in a pointed gothic arch. Built on the book's Grim Heraldry marks, type, and ink.
#import "/typst/aids/kit.typ": *

#let PITCH = 18pt                       // writing-line pitch: room for a pencil hand
#let pen = rgb(0, 0, 0, 32%)            // writing lines: visible, quieter than printed rules
#let OUT = 1.5pt                        // plate outer rule
#let INN = 0.5pt                        // plate inner rule
#let GAP = 2.8pt                        // between the two rules
#let R = 7pt                            // corner notch radius

#let lbl(t, fill: ink, size: 9pt, tracking: 0.12em, weight: 700) = text(font: sans, size: size, weight: weight,
  tracking: tracking, fill: fill, upper(t))
// Printed values on the hero cards: the book's serif with lining figures and a true minus sign.
#let inked(t, size: 15pt) = text(font: serif, weight: 600, size: size, number-type: "lining",
  if type(t) == str and t.starts-with("-") { "−" + t.slice(1) } else { t })
// A printed value that steps down in half points (never below 9pt) until it fits its line.
#let fit-inked(t, size: 15pt, min: 9pt, room: 6pt) = layout(sz => {
  let s = size
  while s > min and measure(inked(t, size: s)).width > sz.width - room { s -= 0.5pt }
  inked(t, size: s)
})
#let rubric(t) = text(font: fell, style: "italic", size: 10pt, fill: ink2, t)
#let rich(rs) = for r in rs { if r.at(1) { strong(r.at(0)) } else { r.at(0) } }

// ---------------------------------------------------------------- shapes
// Rectangle with concave quarter-circle notches centred on its outer corners; `d` insets the path
// and keeps it parallel to the outer one.
#let notched(w, h, r: R, d: 0pt, stroke: none, fill: none) = {
  let k = 0.5523
  let q = r + d
  let e = calc.sqrt(calc.max(0.0, (q / 1pt) * (q / 1pt) - (d / 1pt) * (d / 1pt))) * 1pt
  let s = (e - d) * k
  curve(stroke: stroke, fill: fill,
    curve.move((e, d)), curve.line((w - e, d)),
    curve.cubic((w - e, d + s), (w - d - s, e), (w - d, e)), curve.line((w - d, h - e)),
    curve.cubic((w - d - s, h - e), (w - e, h - d - s), (w - e, h - d)), curve.line((e, h - d)),
    curve.cubic((e, h - d - s), (d + s, h - e), (d, h - e)), curve.line((d, e)),
    curve.cubic((d + s, e), (e, d + s), (e, d)), curve.close())
}

#let jewel(s: 5pt) = polygon(fill: ink, (s / 2, 0pt), (s, s / 2), (s / 2, s), (0pt, s / 2))

// Swallowtail ribbon: a black band whose forked tails fold behind it.
#let ribbon(t, size: 12.5pt) = context {
  let tx = text(font: goth, weight: 700, size: size, fill: paper, t)
  let m = measure(tx)
  let h = size + 4.5pt
  let w = m.width + 20pt
  let tail = 10pt
  let drop = 3.2pt
  let fork = 4.5pt
  box(width: w + 2 * tail, height: h + drop, baseline: 30%, {
    place(polygon(fill: ink, (0pt, drop), (tail + 3pt, drop), (tail + 3pt, h + drop), (0pt, h + drop), (fork, drop + h / 2)))
    let rx = w + 2 * tail
    place(polygon(fill: ink, (rx, drop), (rx - tail - 3pt, drop), (rx - tail - 3pt, h + drop), (rx, h + drop), (rx - fork, drop + h / 2)))
    place(dx: tail, rect(width: w, height: h, fill: ink, stroke: 0.9pt + paper))
    place(dx: tail, box(width: w, height: h, align(center + horizon, tx)))
  })
}

// ---------------------------------------------------------------- the plate
// `h`: auto (fits its body), a length, or "fill" (takes the height its container gives it).
#let plate(body, title: none, h: auto, inset: (x: 10pt, top: 12pt, bottom: 9pt), fill: none) = layout(size => {
  let w = size.width
  let ins = if title == none { inset + (top: inset.at("bottom", default: 9pt) + 1pt) } else { inset }
  let H = if h == auto { measure(block(width: w, inset: ins, body)).height } else if h == "fill" { size.height } else { h }
  block(width: w, height: H, spacing: 0pt, breakable: false, {
    place(notched(w, H, stroke: OUT + ink, fill: fill))
    place(notched(w, H, d: GAP, stroke: INN + ink))
    for (x, y) in ((0pt, 0pt), (w, 0pt), (0pt, H), (w, H)) { place(dx: x - 2.6pt, dy: y - 2.6pt, jewel(s: 5.2pt)) }
    place(block(width: w, height: H, inset: ins, body))
    if title != none { place(top + center, dy: -8pt, ribbon(title)) }
  })
})

// A labelled write-in line, the label set small beneath the line.
#let field(label, value: none, h: 27pt, size: 14pt) = block(width: 100%, height: h, spacing: 0pt, {
  place(bottom + left, lbl(label, size: 9pt, weight: 600, fill: ink2))
  place(dy: h - 12pt, line(length: 100%, stroke: 0.6pt + ink))
  if value != none { place(dy: h - 14pt - size * 0.75, dx: 2pt, box(width: 100% - 2pt, fit-inked(value, size: size))) }
})

// Ruled writing space; `h` may be a length or 1fr.
#let ruled(h: auto, pitch: PITCH) = block(width: 100%, height: h, spacing: 0pt,
  fill: tiling(size: (12pt, pitch), place(bottom + left, line(length: 12pt, stroke: 0.5pt + pen))))

// Double-ringed roundel with a label beneath.
#let roundel(label, value: none, d: 44pt, size: 20pt, sub: none) = box(width: 100%, align(center, {
  box(width: d, height: d, {
    place(circle(radius: d / 2, stroke: OUT + ink))
    place(dx: GAP, dy: GAP, circle(radius: d / 2 - GAP, stroke: INN + ink))
    if value != none { place(center + horizon, dy: 1pt, inked(value, size: size)) }
  })
  v(2pt, weak: false)
  lbl(label)
  if sub != none { linebreak(); text(size: 9pt, fill: ink3, sub) }
}))

// Ability score: heater shield, the abbreviation reversed out of a black chief.
#let score(abbr, name, value: none, w: 52pt) = box(width: 100%, align(center, {
  let h = w * 1.18
  box(width: w, height: h, {
    shield-curve(w, h, stroke: 1.8pt + ink)
    place(rect(width: w, height: h * 0.26, fill: ink))
    let k = w * 0.075
    shield-curve(w - 2 * k, h - 2.3 * k, dx: k, dy: k, stroke: 0.45pt + ink)
    place(top + center, dy: h * 0.035, text(font: goth, weight: 700, size: 13pt, fill: paper, abbr))
    if value != none { place(top + center, dy: h * 0.36, inked(value, size: 24pt)) }
  })
  v(1pt)
  lbl(name, size: 9pt, weight: 600, fill: ink2)
}))

#let check(on: false, s: 10pt) = box(width: s, height: s, baseline: 1.5pt, stroke: 1.1pt + ink,
  if on { place(center + horizon, jewel(s: s * 0.62)) })
#let ticks(n, s: 10pt, on: 0, gap: 3pt) = box(for i in range(n) { check(on: i < on, s: s); if i < n - 1 { h(gap) } })
// Wound mark: an outlined lozenge to fill in.
#let wound(s: 18pt) = box(width: s, height: s, baseline: 25%, {
  place(polygon(stroke: (if s < 14pt { 1.1pt } else { 1.5pt }) + ink, (s / 2, 0pt), (s, s / 2), (s / 2, s), (0pt, s / 2)))
  let i = 3pt
  if s >= 14pt { place(polygon(stroke: 0.45pt + ink, (s / 2, i), (s - i, s / 2), (s / 2, s - i), (i, s / 2))) }
})

// Pointed gothic arch (two arcs meeting at an apex over a rectangle), outer and inner rule.
#let arch-path(w, h, d: 0pt, stroke: none, fill: none) = {
  let s = w * 0.62            // springing line below the top
  let a = (w / 2, d)
  curve(stroke: stroke, fill: fill,
    curve.move((d, h - d)), curve.line((d, s)),
    curve.cubic((d, s - (s - d) * 0.55), (w / 2 - (w / 2 - d) * 0.42, d + (s - d) * 0.12), a),
    curve.cubic((w / 2 + (w / 2 - d) * 0.42, d + (s - d) * 0.12), (w - d, s - (s - d) * 0.55), (w - d, s)),
    curve.line((w - d, h - d)), curve.close())
}
#let arch-frame(w, h, body: none) = box(width: w, height: h, {
  place(arch-path(w, h, stroke: OUT + ink))
  place(arch-path(w, h, d: GAP, stroke: INN + ink))
  for (x, y) in ((0pt, h), (w, h)) { place(dx: x - 2.6pt, dy: y - 2.6pt, jewel(s: 5.2pt)) }
  place(dx: w / 2 - 2.6pt, dy: -2.6pt, jewel(s: 5.2pt))
  if body != none { place(center + bottom, dy: -GAP - 3pt, body) }
})

// Two plates side by side at one shared height (the taller body sets it).
#let twin(a, b, cols: (1fr, 150pt), gutter: 14pt, inset: (x: 10pt, top: 12pt, bottom: 9pt)) = layout(size => {
  let wa = if cols.at(0) == 1fr { size.width - gutter - cols.at(1) } else { cols.at(0) }
  let wb = size.width - gutter - wa
  let h = calc.max(measure(block(width: wa, inset: inset, a.at(1))).height,
    measure(block(width: wb, inset: inset, b.at(1))).height)
  grid(columns: (wa, wb), column-gutter: gutter,
    plate(title: a.at(0), h: h, inset: inset, a.at(1)), plate(title: b.at(0), h: h, inset: inset, b.at(1)))
})

// ---------------------------------------------------------------- the page
// Title block: arms, the sheet's title in blackletter, a kicker line, and a brush rule.
#let title-block(title, kicker, arm: 6, size: 30pt) = block(width: 100%, spacing: 0pt, {
  grid(columns: (auto, 1fr, auto), column-gutter: 10pt, align: horizon,
    arms(arm, w: 30pt),
    text(font: goth, weight: 700, size: size, title),
    align(right, text(font: sans, weight: 700, size: 9pt, tracking: 0.16em, fill: ink2, upper(kicker))))
  v(-3pt)
  brush(weight: 2.6pt, seed: 4)
})

#let leaf(title, kicker, face: "front", arm: 6, title-size: 30pt, body) = page(
  width: page-w, height: page-h, margin: (x: M, top: M, bottom: MB), fill: paper)[
  #set text(font: sans, size: 10pt, hyphenate: false, lang: "en", region: "CA", fill: ink, top-edge: 0.8em, bottom-edge: -0.25em)
  #set par(justify: false, leading: 3.2pt, spacing: 5pt)
  #set strong(delta: 200)
  #title-block(title, kicker, arm: arm, size: title-size)
  #v(14pt)
  #body
  #footer(face)
]

// Two columns of equal depth: measure the text at column width, then give the pair half of it plus a line.
#let balanced-pair(body, gutter: 18pt) = layout(size => {
  let w = (size.width - gutter) / 2
  let h = measure(block(width: w, body)).height
  block(width: 100%, height: h / 2 + 16pt, columns(2, gutter: gutter, body))
})

// Rules entry from the extracted profile. A leading "Name [cost]:" run prints the name in bold and
// its bracketed cost, word for word, in a black cost tag; every other run prints as extracted.
#let cost-pill(t) = box(fill: ink, inset: (x: 3pt, top: 1.2pt, bottom: 1pt), outset: (y: 0.6pt), baseline: 0.1em,
  text(font: sans, weight: 700, size: 9pt, fill: paper, t))
#let rule-item(it, size: auto) = block(above: 5pt, below: 0pt, {
  set text(size: size) if size != auto
  let runs = it.runs
  let head = none
  let first = runs.at(0)
  if first.at(1) {
    let m = first.at(0).match(regex("^(.*?) \[([^\]]+)\]:$"))
    if m != none { head = (m.captures.at(0), m.captures.at(1)); runs = runs.slice(1) }
  }
  grid(columns: (8pt, 1fr), column-gutter: 3pt, align: top, box(baseline: -1.5pt, lozenge(size: 4.6pt)),
    if head != none [*#head.at(0)* #cost-pill(head.at(1))#strong(":")#rich(runs)] else { rich(runs) })
  for s in it.sub {
    block(above: 3pt, below: 0pt, inset: (left: 12pt),
      grid(columns: (8pt, 1fr), column-gutter: 2pt, align: top, text(weight: 800, "–"), rich(s)))
  }
})
