// Player-aid kit: the shared sheet anatomy and diagram grammar of docs/PLAYER_AIDS.md,
// built on the book's Grim Heraldry components. Each sheet file imports this kit.
#import "/typst/templates/system.typ": *

#let M = 36pt
#let MB = 64pt          // bottom margin: the footer lives here, its text 30pt from the trim
#let rules-rc = {
  let v = json("/source/versions.json")
  "RC" + str(v.current)
}
#let body-pt = 10.5pt

// ---------------------------------------------------------------- page furniture
#let iron-band(arm, code, title, refs) = block(width: 100%, spacing: 0pt, {
  block(width: 100%, fill: ink, inset: (left: 10pt, right: 13pt, y: 8pt), spacing: 0pt,
    grid(columns: (auto, 1fr, auto), column-gutter: 11pt, align: horizon,
      arms(arm, w: 40pt),
      text(font: goth, weight: 700, size: 38pt, fill: paper, title),
      align(right, text(fill: paper, font: sans, weight: 700, size: 9.5pt, tracking: 0.18em)[PLAYER AID #code \ #text(weight: 600, tracking: 0.08em, refs)])))
  v(2pt); line(length: 100%, stroke: 0.7pt + ink)
})

#let footer(face) = place(bottom + left, dy: MB - 30pt, block(width: 100%, {
  block(spacing: 0pt, line(length: 100%, stroke: 1.6pt + ink)); v(2pt); block(spacing: 0pt, line(length: 100%, stroke: 0.4pt + ink))
  v(5pt)
  grid(columns: (auto, 1fr, auto), column-gutter: 6pt, align: horizon,
    signature(s: 14pt),
    text(size: 9pt, weight: 700, tracking: 0.1em)[HERALDRY SKIRMISH · THE DYING LANDS],
    text(size: 9pt, fill: ink3)[Rules #rules-rc · #face])
}))

// One printed side. `art` is an approved ink file id; it stands on the footer rule at a lower corner.
#let side(arm, code, title, refs, face: "front", art: none, art-w: 130pt, art-at: right, art-dx: 0pt, art-dy: 9pt, body) = page(
  width: page-w, height: page-h, margin: (x: M, top: M, bottom: MB), fill: paper)[
  #set text(font: sans, size: body-pt, hyphenate: false, lang: "en", region: "CA", fill: ink, top-edge: 0.8em, bottom-edge: -0.25em)
  #set par(justify: false, leading: 3.4pt, spacing: 5pt)
  #set strong(delta: 200)
  #iron-band(arm, code, title, refs)
  #v(11pt)
  #body
  #if art != none {
    let dx = if art-at == right { M - 10pt + art-dx } else { -M + 10pt + art-dx }
    place(bottom + art-at, dx: dx, dy: art-dy, image("/assets/art/ink/" + art + ".png", width: art-w))
  }
  #footer(face)
]

// ---------------------------------------------------------------- flow grammar
#let num(n, w: 24pt) = shield(w: w, inner: true, body: text(weight: 800, size: if w < 20pt { 8.6pt } else { 11pt }, fill: paper, str(n)))

// Forged arrow: a tapered shaft swelling into a barbed broadhead.
#let forged-h(len, back: false) = box(width: len, height: 16pt, {
  let y = 8pt
  let pts = ((0pt, y - 1.3pt), (len - 15pt, y - 2.9pt), (len - 18pt, y - 8pt), (len, y),
    (len - 18pt, y + 8pt), (len - 15pt, y + 2.9pt), (0pt, y + 1.3pt))
  place(polygon(fill: ink, ..if back { pts.map(((x, yy)) => (len - x, yy)) } else { pts }))
})
#let forged-v(len, up: false) = box(width: 16pt, height: len, {
  let x = 8pt
  let pts = ((x - 1.3pt, 0pt), (x - 2.9pt, len - 15pt), (x - 8pt, len - 18pt), (x, len),
    (x + 8pt, len - 18pt), (x + 2.9pt, len - 15pt), (x + 1.3pt, 0pt))
  place(polygon(fill: ink, ..if up { pts.map(((xx, y)) => (xx, len - y)) } else { pts }))
})
#let flag(t) = tag(t, size: 8.2pt)
#let yes-arrow(w: 62pt, label: "Yes") = box(width: w, {
  align(center, flag(label)); v(-1pt); forged-h(w)
})
#let down(label: "No", h: 22pt, x: 98pt) = block(above: 2pt, below: 2pt, width: 100%, inset: (left: x),
  grid(columns: (16pt, auto), column-gutter: 6pt, align: horizon, forged-v(h), if label != none { flag(label) }))

// Decision: a drawn-out lozenge plaque with an engraved inner rule.
#let plaque(body, w: 160pt, size: 11.5pt) = context {
  let t = block(width: w - 46pt, align(center, text(weight: 800, size: size, body)))
  let h = measure(t).height + 18pt
  let pts(i) = ((h/2 + i, i), (w - h/2 - i, i), (w - 2 * i, h/2), (w - h/2 - i, h - i), (h/2 + i, h - i), (2 * i, h/2))
  box(width: w, height: h, {
    place(polygon(stroke: 1.8pt + ink, fill: tint, ..pts(0pt)))
    place(polygon(stroke: 0.45pt + ink, ..pts(3.2pt)))
    place(center + horizon, t)
  })
}

// Action box; `ends` pins an ENDS banner to the lower-right corner.
#let endbox(body, ends: true, tag-text: "Ends", fill: none) = block(width: 100%, inset: (right: if ends { 7pt } else { 0pt }), {
  block(width: 100%, stroke: 1.3pt + ink, fill: fill, inset: (left: 8pt, right: 10pt, top: 7pt, bottom: if ends { 11pt } else { 7pt }), body)
  if ends { place(bottom + right, dx: 7pt, dy: 7pt, tag(tag-text)) }
})
#let rung(n, q, act, w: 160pt, ends: true) = grid(columns: (26pt, w, 62pt, 1fr), column-gutter: 4pt, align: horizon,
  num(n), plaque(q, w: w), yes-arrow(), endbox(act, ends: ends))

// A titled stage box for phase rows and procedures.
#let stage(n, title, body, fill: none, h: auto) = block(width: 100%, height: h, stroke: 1.3pt + ink, fill: fill, inset: (x: 8pt, top: 8pt, bottom: 8pt), {
  grid(columns: (auto, 1fr), column-gutter: 7pt, align: horizon,
    num(n, w: 20pt), text(font: goth, weight: 700, size: 16pt, title))
  v(5pt)
  body
})
// Stages in a row joined by forged arrows.
#let stage-row(..items, gap: 24pt, h: auto) = {
  let it = items.pos()
  let cols = ()
  let cells = ()
  for (i, s) in it.enumerate() {
    cols.push(1fr)
    cells.push(s)
    if i < it.len() - 1 { cols.push(gap); cells.push(align(horizon, forged-h(gap))) }
  }
  grid(columns: cols, align: (x, y) => if calc.odd(x) { horizon } else { top }, ..cells)
}
// A return arrow under a row: "repeat" path back to the first stage.
#let return-arrow(label) = block(above: 6pt, below: 4pt, width: 100%, {
  grid(columns: (auto, 1fr), column-gutter: 8pt, align: horizon,
    box(width: 70pt, forged-h(70pt, back: true)),
    text(weight: 700, size: 10pt)[#label])
})

// ---------------------------------------------------------------- reference panels
#let aside-head(t, seed: 1, size: 18pt) = block(above: 0pt, below: 6pt, sticky: true, {
  text(font: goth, weight: 700, size: size, t); v(-4pt); brush(weight: 2.4pt, seed: seed)
})
#let mini(n, body) = block(above: 4pt, below: 0pt, grid(columns: (17pt, 1fr), column-gutter: 6pt, align: top,
  shield(w: 15pt, body: text(weight: 800, size: 8.4pt, fill: paper, str(n))), body))
#let steps(..items, start: 1) = for (i, s) in items.pos().enumerate() { mini(i + start, s) }
#let dot(body) = block(above: 4pt, below: 0pt, grid(columns: (10pt, 1fr), column-gutter: 3pt, align: top,
  box(baseline: -1.5pt, lozenge(size: 5pt)), body))
#let caps(t) = text(weight: 800, size: 9pt, tracking: 0.14em, upper(t))
#let gap-v = v(12pt)
#let note(body) = panel("Rules Note", body)
#let cost(t) = cost-tag(text(size: 8.6pt, t))

// Reference table at aid size (the book's ledger table).
#let aid-table(widths, aligns, header, rows, title: none, size: 9.5pt, notes: none) = block(above: 0pt, below: 4pt, {
  if title != none { block(above: 0pt, below: 0pt, sticky: true, text(font: goth, weight: 700, size: 18pt, title)) }
  v(-6pt)
  ref-table(widths, aligns, header, rows, size: size, notes: notes)
})

