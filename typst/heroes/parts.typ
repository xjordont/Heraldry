// Hero-sheet parts: pencil fields, strapped boxes, score shields, and ruled writing space, built on
// the player-aid kit so the hero sheet, the party ledger, and the hero cards share the book's look.
#import "/typst/aids/kit.typ": *

#let PITCH = 20pt                       // writing-line pitch: about 7 mm, room for a pencil hand
#let pen = rgb(0, 0, 0, 34%)            // writing lines: visible, quieter than printed rules
#let lbl(t, fill: ink, tracking: 0.12em) = text(font: sans, size: 9pt, weight: 800, tracking: tracking, fill: fill, upper(t))
// Printed values on the hero cards: the book's serif with lining figures and a true minus sign.
#let inked(t, size: 15pt) = text(font: serif, weight: 600, size: size, number-type: "lining",
  if type(t) == str and t.starts-with("-") { "−" + t.slice(1) } else { t })
#let hint(t) = text(font: sans, size: 9pt, fill: ink3, t)
#let strap(t) = box(fill: ink, inset: (x: 4.5pt, top: 2.6pt, bottom: 2.2pt), lbl(t, fill: paper, tracking: 0.08em))
#let rich(rs) = for r in rs { if r.at(1) { strong(r.at(0)) } else { r.at(0) } }

// A printed value that steps down in half points (never below 9pt) until it fits its line.
#let fit-inked(t, size: 15pt, min: 9pt, room: 6pt) = layout(sz => {
  let s = size
  while s > min and measure(inked(t, size: s)).width > sz.width - room { s -= 0.5pt }
  inked(t, size: s)
})

// Ruled writing space; `h` may be a length or 1fr.
#let ruled(h: auto, pitch: PITCH) = block(width: 100%, height: h, spacing: 0pt,
  fill: tiling(size: (12pt, pitch), place(bottom + left, line(length: 12pt, stroke: 0.55pt + pen))))

#let sheet-head(t, seed: 1, size: 14.5pt, right: none) = block(above: 0pt, below: 4pt, sticky: true, {
  grid(columns: (1fr, auto), align: bottom, text(font: goth, weight: 700, size: size, t), if right != none { hint(right) })
  v(-5pt); brush(weight: 2pt, seed: seed)
})

// A labelled write-in line; `value` prints in the scribe's hand.
#let field(label, value: none, h: 30pt, size: 15pt, note: none) = block(width: 100%, height: h, spacing: 0pt, {
  place(top + left, lbl(label))
  if note != none { place(top + right, hint(note)) }
  place(bottom + left, line(length: 100%, stroke: 0.9pt + ink))
  if value != none { place(bottom + left, dx: 3pt, dy: -3pt, fit-inked(value, size: size)) }
})

// A ruled box with a black strap across its top edge.
#let cell(label, value: none, h: 48pt, size: 20pt, sub: none, fill: none, stroke: 1.4pt, body: none) = block(width: 100%, height: h, spacing: 0pt, {
  place(dy: 7pt, rect(width: 100%, height: h - 7pt, stroke: stroke + ink, fill: fill))
  place(top + center, strap(label))
  if value != none { place(center + horizon, dy: if sub != none { 1pt } else { 4pt }, inked(value, size: size)) }
  if sub != none { place(bottom + center, dy: -3pt, hint(sub)) }
  if body != none { place(center + horizon, dy: 4pt, body) }
})

// A resource that changes in play: a wide pencil area for the current value, a tinted column for the maximum.
#let pool(label, max: none, h: 58pt, mw: 46pt, extra: none) = block(width: 100%, height: h, spacing: 0pt, layout(size => {
  let w = size.width
  place(dy: 7pt, rect(width: w, height: h - 7pt, stroke: 1.4pt + ink))
  place(dx: w - mw, dy: 7pt, rect(width: mw, height: h - 7pt, fill: tint, stroke: (left: 0.9pt + ink)))
  place(top + left, dx: 8pt, strap(label))
  place(dx: 6pt, dy: h - 14pt, hint("Current"))
  place(dx: w - mw, dy: 11pt, box(width: mw, align(center, hint("Max"))))
  if max != none { place(dx: w - mw, dy: 26pt, box(width: mw, align(center, inked(max, size: 20pt)))) }
  if extra != none { place(dx: w - mw - 50pt, dy: 7pt, extra) }
}))

// Ability score: an outlined heater shield with an engraved inner line, the abbreviation strapped on top.
#let score(abbr, name, value: none, w: 50pt) = box(width: 100%, align(center, {
  let h = w * 1.18
  box(width: w, height: h + 8pt, {
    place(dy: 8pt, box(width: w, height: h, {
      shield-curve(w, h, stroke: 1.8pt + ink)
      let k = w * 0.08
      shield-curve(w - 2 * k, h - 2.3 * k, dx: k, dy: k, stroke: 0.45pt + ink)
    }))
    place(top + center, strap(abbr))
    if value != none { place(top + center, dy: 8pt + h * 0.24, inked(value, size: 24pt)) }
  })
}))

#let check(on: false, s: 10pt) = box(width: s, height: s, baseline: 1.5pt, stroke: 1.1pt + ink,
  if on { place(center + horizon, polygon(fill: ink, (s * 0.35, 0pt), (s * 0.7, s * 0.35), (s * 0.35, s * 0.7), (0pt, s * 0.35))) })
#let ticks(n, s: 10pt, on: 0) = box(for i in range(n) { check(on: i < on, s: s); if i < n - 1 { h(3pt) } })

// One printed hero leaf: iron band with the party arms, the body, the series footer.
#let hero-band(title, kicker, sub, arm: 6, size: 34pt) = block(width: 100%, spacing: 0pt, {
  block(width: 100%, fill: ink, inset: (left: 10pt, right: 13pt, y: if size < 30pt { 5pt } else { 7pt }), spacing: 0pt,
    grid(columns: (auto, 1fr, auto), column-gutter: 11pt, align: horizon,
      arms(arm, w: if size < 30pt { 26pt } else { 36pt }),
      text(font: goth, weight: 700, size: size, fill: paper, title),
      align(right, text(fill: paper, font: sans, weight: 700, size: 9.5pt, tracking: 0.18em)[#upper(kicker) \ #text(weight: 600, tracking: 0.08em, sub)])))
  v(2pt); line(length: 100%, stroke: 0.7pt + ink)
})

#let leaf(title, kicker, sub, face: "front", arm: 6, title-size: 34pt, body) = page(
  width: page-w, height: page-h, margin: (x: M, top: M, bottom: MB), fill: paper)[
  #set text(font: sans, size: 10pt, hyphenate: false, lang: "en", region: "CA", fill: ink, top-edge: 0.8em, bottom-edge: -0.25em)
  #set par(justify: false, leading: 3.2pt, spacing: 5pt)
  #set strong(delta: 200)
  #hero-band(title, kicker, sub, arm: arm, size: title-size)
  #v(9pt)
  #body
  #footer(face)
]

// Two columns of equal depth: measure the text at column width, then give the pair half of it plus a line.
#let balanced-pair(body, gutter: 18pt) = layout(size => {
  let w = (size.width - gutter) / 2
  let h = measure(block(width: w, body)).height
  block(width: 100%, height: h / 2 + 16pt, columns(2, gutter: gutter, body))
})

// Rules entry from the extracted profile: bold name, verbatim text, indented sub-entries.
#let rule-item(it, size: auto) = block(above: 4pt, below: 0pt, {
  set text(size: size) if size != auto
  grid(columns: (8pt, 1fr), column-gutter: 3pt, align: top, box(baseline: -1.5pt, lozenge(size: 4.6pt)), rich(it.runs))
  for s in it.sub {
    block(above: 3pt, below: 0pt, inset: (left: 14pt),
      grid(columns: (8pt, 1fr), column-gutter: 2pt, align: top, text(weight: 800, "–"), rich(s)))
  }
})
