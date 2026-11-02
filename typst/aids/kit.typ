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

// One side of a sheet. `art` is an approved ink file id; it stands on the footer rule at a lower corner.
#let side(arm, code, title, refs, face: "front", art: none, art-w: 130pt, art-at: right, art-dx: 0pt, art-dy: 9pt, body) = page(
  width: page-w, height: page-h, margin: (x: M, top: M, bottom: MB), fill: paper)[
  #set text(font: sans, size: body-pt, hyphenate: false, lang: "en", region: "CA", fill: ink, top-edge: 0.8em, bottom-edge: -0.25em)
  // The book's style lock: straight apostrophes, quotes, and inch marks; never curly quotes or primes.
  #set smartquote(enabled: false)
  // Markup turns "-4" into a Unicode minus; the style lock keeps the manuscript's hyphen-minus.
  #show "\u{2212}": "-"
  #set par(justify: false, leading: 3.4pt, spacing: 5pt)
  #set strong(delta: 200)
  #iron-band(arm, code, title, refs)
  #v(11pt)
  #body
  #if art != none {
    // Inside the text frame: the art's outer edge sits 4pt in from the margin line.
    let dx = if art-at == right { -4pt + art-dx } else { 4pt + art-dx }
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
#let flag(t) = tag(t, size: 8.6pt)
#let yes-arrow(w: 62pt, label: "Yes") = box(width: w, {
  align(center, flag(label)); v(-1pt); forged-h(w)
})
#let down(label: "No", h: 22pt, x: 98pt) = block(above: 2pt, below: 2pt, width: 100%, inset: (left: x),
  grid(columns: (16pt, auto), column-gutter: 6pt, align: horizon, forged-v(h), if label != none { flag(label) }))

// Decision: a drawn-out lozenge plaque with an engraved inner rule.
#let plaque(body, w: 160pt, size: 11.5pt, min-h: 0pt) = context {
  let t = block(width: w - 46pt, align(center, text(weight: 800, size: size, body)))
  let h = calc.max(min-h, measure(t).height + 18pt)
  let pts(i) = ((h/2 + i, i), (w - h/2 - i, i), (w - 2 * i, h/2), (w - h/2 - i, h - i), (h/2 + i, h - i), (2 * i, h/2))
  box(width: w, height: h, {
    place(polygon(stroke: 1.8pt + ink, fill: tint, ..pts(0pt)))
    place(polygon(stroke: 0.45pt + ink, ..pts(3.2pt)))
    place(center + horizon, t)
  })
}

// Action box; `ends` pins an ENDS banner to the lower-right corner.
#let endbox(body, ends: true, tag-text: "Ends", fill: none) = block(width: 100%, inset: (right: if ends { 7pt } else { 0pt }), {
  block(width: 100%, stroke: 1.3pt + ink, fill: fill, inset: (left: 8pt, right: 10pt, top: 7pt, bottom: if ends { 12pt } else { 7pt }), body)
  if ends { place(bottom + right, dx: 7pt, dy: 8pt, tag(tag-text, size: 8.6pt)) }
})
#let rung(n, q, act, w: 160pt, ends: true) = grid(columns: (26pt, w, 62pt, 1fr), column-gutter: 4pt, align: horizon,
  num(n), plaque(q, w: w), yes-arrow(), endbox(act, ends: ends))

// A titled stage box for phase rows and procedures.
#let stage(n, title, body, fill: none, h: auto) = block(width: 100%, height: h, above: 0pt, below: 0pt, stroke: 1.3pt + ink, fill: fill, inset: (x: 8pt, top: 8pt, bottom: 8pt), {
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
  shield(w: 15pt, body: text(weight: 800, size: 9pt, fill: paper, str(n))), body))
#let steps(..items, start: 1) = for (i, s) in items.pos().enumerate() { mini(i + start, s) }
#let dot(body) = block(above: 4pt, below: 0pt, grid(columns: (10pt, 1fr), column-gutter: 3pt, align: top,
  box(baseline: -1.5pt, lozenge(size: 5pt)), body))
#let caps(t) = text(weight: 800, size: 9pt, tracking: 0.14em, upper(t))
#let gap-v = v(12pt)
#let note(body) = block(width: 100%, above: 7pt, below: 8pt, breakable: false, fill: tint, stroke: (left: 2.6pt + ink),
  inset: (x: 8pt, y: 6pt))[#tag("Rules Note", size: 8.6pt) #v(3pt) #body]
#let cost(t) = cost-tag(text(size: 9pt, t))
// A named Town action with its TAP cost tag, then its effect.
#let act(name, tap, body) = block(above: 7pt, below: 0pt, breakable: false, {
  grid(columns: (1fr, auto), column-gutter: 6pt, align: horizon, text(weight: 800, name), cost(tap))
  v(2pt)
  body
})

// Reference table at aid size (the book's ledger table).
#let aid-table(widths, aligns, header, rows, title: none, size: 9.5pt, notes: none) = block(above: 0pt, below: 4pt, {
  if title != none { block(above: 0pt, below: 0pt, sticky: true, text(font: goth, weight: 700, size: 18pt, title)) }
  v(-6pt)
  ref-table(widths, aligns, header, rows, size: size, notes: notes)
})


// ---------------------------------------------------------------- measured flow rows
// Every row measures itself, so the spacing is mechanical: plaque and action box share a top
// line, the shield and YES arrow sit on the plaque's centre line, each NO connector runs from
// the plaque's foot straight down to the next row, and every gap between rows is FLOW-GAP.
#let FLOW-GAP = 18pt
#let FLOW-LEAD = 30pt       // shield column
#let FLOW-ARROW = 52pt      // YES arrow
#let FLOW-W = 150pt         // decision plaque width
#let flag-at(x, y, w, t) = place(dx: x, dy: y, box(width: w, align(center, flag(t))))
#let down-link(cx, y0, len, label) = {
  place(dx: cx - 8pt, dy: y0, forged-v(len))
  if label != none { place(dx: cx + 12pt, dy: y0 + len / 2 - 8pt, flag(label)) }
}

// Opening box of a flow; its connector drops onto the first plaque's centre (`cx`).
#let flow-start(body, cx: FLOW-LEAD + FLOW-W / 2) = layout(size => {
  let b = block(width: size.width - FLOW-LEAD, endbox(ends: false, body))
  let h = measure(b).height
  block(width: size.width, height: h + FLOW-GAP, spacing: 0pt, {
    place(dx: FLOW-LEAD, dy: 0pt, b)
    down-link(cx, h, FLOW-GAP, none)
  })
})

// One decision row: shield n, plaque q, YES arrow, action box. `next` labels the connector to the
// row below (none: last row). `lead` 0pt drops the shield column.
#let flow-row(n, q, act, w: FLOW-W, next: "No", ends: true, tag-text: "Ends", yes: "Yes", lead: FLOW-LEAD) = layout(size => {
  let W = size.width
  let pl = plaque(q, w: w)
  let ax = lead + w + 4pt
  let bx = ax + FLOW-ARROW + 4pt
  let bw = W - bx
  let ab = block(width: bw, endbox(act, ends: ends, tag-text: tag-text))
  let hp = measure(pl).height
  let H = calc.max(hp, measure(ab).height + if ends { 8pt } else { 0pt })
  let total = if next != none { H + FLOW-GAP } else { H }
  block(width: W, height: total, spacing: 0pt, {
    if n != none { place(dx: 0pt, dy: hp / 2 - 14pt, num(n)) }
    place(dx: lead, dy: 0pt, pl)
    place(dx: ax, dy: hp / 2 - 8pt, forged-h(FLOW-ARROW))
    flag-at(ax, hp / 2 - 26pt, FLOW-ARROW, yes)
    place(dx: bx, dy: 0pt, ab)
    if next != none { down-link(lead + w / 2, hp, total - hp, next) }
  })
})

// Closing box of a flow, level with the plaques' left edge.
#let flow-end(n, body, ends: true, tag-text: "Ends", lead: FLOW-LEAD) = layout(size => {
  let b = block(width: size.width - lead, endbox(ends: ends, tag-text: tag-text, body))
  let h = measure(b).height
  block(width: size.width, height: h + if ends { 8pt } else { 0pt }, spacing: 0pt, {
    if n != none { place(dx: 0pt, dy: calc.max(0pt, h / 2 - 18pt), num(n)) }
    place(dx: lead, dy: 0pt, b)
  })
})

// A vertical connector centred on its column, with an optional label, at the standard gap.
#let vlink(label: none, h: FLOW-GAP) = block(width: 100%, height: h, spacing: 0pt, layout(size => {
  down-link(size.width / 2, 0pt, h, label)
}))

// Four stages in a clockwise loop around a centre mark. Stages in the same row share one height.
#let cycle(s1, s2, s3, s4, centre, gap: 34pt, mid: 64pt) = layout(size => {
  let cw = (size.width - gap) / 2
  let mk(s, h) = block(width: cw, align(left + top, stage(s.at(0), s.at(1), s.at(2), h: h)))
  let hh(a, b) = calc.max(measure(mk(a, auto)).height, measure(mk(b, auto)).height)
  let h1 = hh(s1, s2)
  let h2 = hh(s4, s3)
  grid(columns: (cw, gap, cw), rows: (h1, mid, h2), align: center + horizon,
    mk(s1, h1), forged-h(gap), mk(s2, h1),
    forged-v(mid - 12pt, up: true), centre, forged-v(mid - 12pt),
    mk(s4, h2), forged-h(gap, back: true), mk(s3, h2))
})

// A connector at a fixed x (for flows whose boxes span the column), at the standard gap.
#let link-at(cx, label: none) = block(width: 100%, height: FLOW-GAP, spacing: 0pt, down-link(cx, 0pt, FLOW-GAP, label))

// A whole decision flow, laid out at once. `rows` holds (n, question, action) or
// (n, question, action, tag) triples; `start` and `end` are optional boxes (end: (n, body, tag)).
// Each plaque and its action box share one centre line, every gap between rows is `gap`, and
// each connector runs from one plaque straight to the next, with "No" at its midpoint.
#let flow(start: none, rows: (), end: none, w: FLOW-W, lead: FLOW-LEAD, gap: FLOW-GAP, no: "No", min-link: 30pt) = layout(size => {
  let W = size.width
  let ax = lead + w + 4pt
  let bx = ax + FLOW-ARROW + 4pt
  let bw = W - bx
  let cx = lead + w / 2
  let it = ()
  for r in rows {
    let tg = r.at(3, default: "Ends")
    let pl = plaque(r.at(1), w: w)
    let ab = block(width: bw, endbox(r.at(2), tag-text: tg))
    let hp = measure(pl).height
    let hb = measure(ab).height + 8pt
    it.push((n: r.at(0), pl: pl, ab: ab, hp: hp, hb: hb, h: calc.max(hp, hb)))
  }
  let sb = if start != none { block(width: W - lead, endbox(ends: false, start)) } else { none }
  let hs = if sb != none { measure(sb).height } else { 0pt }
  let eb = if end != none { block(width: W - lead, endbox(end.at(1), tag-text: end.at(2, default: "Ends"))) } else { none }
  let he = if eb != none { measure(eb).height + 8pt } else { 0pt }
  // vertical positions
  // Rows sit `gap` apart, but never closer than a connector of `min-link` between plaques.
  let y = if sb != none { hs + gap } else { 0pt }
  let foot = if sb != none { hs } else { none }
  let pos = ()
  for r in it {
    if foot != none { y = calc.max(y, foot + min-link - (r.h - r.hp) / 2) }
    pos.push(y)
    foot = y + (r.h + r.hp) / 2
    y += r.h + gap
  }
  let ye = if foot != none { calc.max(y, foot + min-link) } else { y }
  let total = if eb != none { ye + he } else { y - gap }
  block(width: W, height: total, spacing: 0pt, {
    if sb != none { place(dx: lead, dy: 0pt, sb) }
    let prev = if sb != none { hs } else { none }
    for (i, r) in it.enumerate() {
      let py = pos.at(i) + (r.h - r.hp) / 2
      let by = pos.at(i) + (r.h - r.hb) / 2
      if prev != none { down-link(cx, prev, py - prev, if i == 0 { none } else { no }) }
      if r.n != none { place(dx: 0pt, dy: py + r.hp / 2 - 14pt, num(r.n)) }
      place(dx: lead, dy: py, r.pl)
      place(dx: ax, dy: py + r.hp / 2 - 8pt, forged-h(FLOW-ARROW))
      flag-at(ax, py + r.hp / 2 - 26pt, FLOW-ARROW, "Yes")
      place(dx: bx, dy: by, r.ab)
      prev = py + r.hp
    }
    if eb != none {
      down-link(cx, prev, ye - prev, no)
      if end.at(0) != none { place(dx: 0pt, dy: ye + (he - 8pt) / 2 - 14pt, num(end.at(0))) }
      place(dx: lead, dy: ye, eb)
    }
  })
})
