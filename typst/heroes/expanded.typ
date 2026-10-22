// Expanded Hero record. One visual grammar; one populated front and back per Hero.
#import "parts.typ": *
#let DATA = json("/typst/heroes/basic-heroes.json")
#let rule-ink = luma(35%)
#let label-fill = rgb(0, 0, 0, 7%)
#let small(t, size: 9pt, fill: ink) = text(font: sans, weight: 650, size: size, fill: fill, tracking: 0.025em, t)
#let signed(n) = if n >= 0 { "+" + str(n) } else { "-" + str(-n) }
#let get(hr, key) = if hr == none { none } else { hr.at(key) }

// The label is a band in the field itself, sharing its border with the writing area.
#let cell(label, value: none, h: 32pt, size: 13pt, display: false, wrap: false) = block(
  width: 100%, height: h, spacing: 0pt, stroke: 0.55pt + rule-ink, fill: paper, {
    place(block(width: 100%, height: 13pt, fill: label-fill, inset: (left: 5pt, top: 1.5pt), small(label)))
    if value != none {
      place(dx: 5pt, dy: 15pt, block(width: 100% - 10pt,
        if wrap { text(size: size, value) } else if display { text(font: goth, size: size, weight: 700, value) }
        else { fit-inked(value, size: size, room: 0pt) }))
    }
  })

#let panel(title, body, h: auto, pad: 7pt) = layout(sz => {
  let title-h = 19pt
  let natural = measure(block(width: sz.width - 2 * pad, body)).height + title-h + 2 * pad
  let H = if h == auto { natural } else if h == "fill" { sz.height } else { h }
  assert(natural <= H + 1pt, message: title + ": panel content exceeds its frame")
  block(width: 100%, height: H, spacing: 0pt, breakable: false, stroke: 0.8pt + ink, {
    place(block(width: 100%, height: title-h, fill: ink,
      inset: (left: 8pt, top: 3pt), small(upper(title), size: 9.5pt, fill: paper)))
    place(dx: pad, dy: title-h + pad, block(width: sz.width - 2 * pad, height: H - title-h - 2 * pad, body))
  })
})

#let ruled-area(h: 1fr, pitch: 20pt) = block(width: 100%, height: h,
  fill: tiling(size: (10pt, pitch), place(bottom + left,
    line(length: 10pt, stroke: 0.4pt + rule-ink))))

#let record-table(heads, widths, n, row: 23pt, first: ()) = table(
  columns: widths, rows: (16pt,) + (row,) * n, inset: (x: 4pt, y: 0pt),
  align: left + horizon, stroke: 0.45pt + rule-ink,
  fill: (_, y) => if y == 0 { label-fill } else { none },
  ..heads.map(t => small(t)),
  ..range(n).map(r => (text(size: 9pt, first.at(r, default: "")),) + range(heads.len() - 1).map(_ => [])).flatten())

#let page-footer(face) = place(bottom + left, dy: 22pt, block(width: 100%, {
  line(length: 100%, stroke: 0.7pt + ink)
  v(3pt)
  grid(columns: (1fr, auto), small("HERALDRY SKIRMISH"), text(size: 9pt, rules-rc + " | " + face))
}))
#let record-page(face, body) = page(width: 612pt, height: 792pt,
  margin: (x: 36pt, top: 36pt, bottom: 52pt), fill: paper)[
  #set text(font: sans, size: 10pt, fill: ink, lang: "en", region: "CA", hyphenate: false,
    top-edge: 0.8em, bottom-edge: -0.25em)
  #set par(leading: 2pt, spacing: 3pt, justify: false)
  #set strong(delta: 200)
  #body
  #page-footer(face)
]

#let identity(hr) = {
  let st(k) = if hr == none { none } else { hr.stats.at(k, default: "None") }
  block(height: 128pt, width: 100%, stroke: 1pt + ink, {
    place(block(width: 100%, height: 20pt, fill: ink, inset: (x: 7pt, top: 3pt),
      grid(columns: (1fr, auto), small("HERALDRY SKIRMISH", size: 10pt, fill: paper),
        small(if hr == none { "HERO RECORD / FRONT" } else { "BASIC MODE / FRONT" }, fill: paper))))
    place(dy: 20pt, grid(columns: (1fr, 108pt), column-gutter: 0pt,
      stack(dir: ttb, spacing: 0pt,
        grid(columns: (1fr, 135pt), column-gutter: 0pt,
          cell("Name", value: get(hr, "name"), h: 44pt, size: 26pt, display: true),
          cell("Role", value: get(hr, "role"), h: 44pt, size: 10pt, wrap: true)),
        grid(columns: (1fr, 1fr, 1fr), column-gutter: 0pt,
          cell("Class", value: get(hr, "class")), cell("Ancestry", value: get(hr, "ancestry")),
          cell("Background", value: get(hr, "background"))),
        grid(columns: (37pt, 71pt, 69pt, 71pt, 1fr), column-gutter: 0pt,
          cell("Level", value: get(hr, "level")), cell("Archetype", value: get(hr, "archetype"), size: 11pt),
          cell("Casting", value: get(hr, "casting")), cell("HP/Level", value: get(hr, "hp_per_level")),
          cell("Senses", value: st("Senses"), size: 10pt))),
      block(width: 108pt, height: 108pt, stroke: 0.55pt + rule-ink, {
        place(top + center, dy: 3pt, arch-path(102pt, 103pt, stroke: 0.65pt + rule-ink))
        if hr != none {
          place(center + bottom, dy: -3pt, image("/assets/art/ink/" + hr.art + ".png", width: 87pt, height: 98pt, fit: "contain"))
        } else {
          place(center + horizon, arms(6, w: 37pt))
          place(center + bottom, dy: -8pt, small("PORTRAIT / ARMS"))
        }
      })))
  })
}

#let statistic(label, value: none, chief: false, sub: none) = layout(sz => {
  let H = 54pt
  block(width: 100%, height: H, {
    if chief {
      place(polygon(stroke: 0.9pt + ink, (0pt, 0pt), (sz.width, 0pt), (sz.width, H - 10pt),
        (sz.width / 2, H), (0pt, H - 10pt)))
    } else { place(rect(width: 100%, height: H, stroke: 0.7pt + rule-ink)) }
    place(block(width: 100%, height: 16pt, fill: if chief { ink } else { label-fill },
      inset: (top: 2pt), align(center, small(label, size: 10pt, fill: if chief { paper } else { ink }))))
    if value != none { place(top + center, dy: 21pt, inked(value, size: 22pt)) }
    if sub != none { place(bottom + center, dy: -2pt, text(size: 9pt, sub)) }
  })
})
#let statistics(hr) = {
  let init = if hr == none { none } else { signed(int(hr.scores.INT.replace("+", "")) + int(hr.scores.SPI.replace("+", ""))) }
  grid(columns: (60pt, 60pt, 60pt, 60pt, 110pt, 80pt, 74pt), column-gutter: 6pt,
    ..("STR", "DEX", "INT", "SPI").map(k => statistic(k, chief: true, value: if hr == none { none } else { hr.scores.at(k) })),
    statistic("Initiative", value: init, sub: "INT + SPI"),
    statistic("Speed", value: if hr == none { none } else { hr.stats.SPD }),
    statistic("Size", value: if hr == none { none } else { hr.stats.Sz }))
}
#let pool(label, maximum: none, temp: false, ap: false) = block(height: 52pt, width: 100%, stroke: 0.7pt + ink,
  stack(dir: ttb, spacing: 0pt,
  block(width: 100%, height: 16pt, fill: ink, inset: (left: 5pt, top: 2pt), small(label, size: 10pt, fill: paper)),
  grid(columns: if temp { (1fr, 1fr, 1fr) } else { (1fr, 1fr) }, column-gutter: 0pt,
    cell("Current", h: 36pt), cell(if ap { "Allowance" } else { "Max" }, value: maximum, h: 36pt, size: 16pt),
    ..if temp { (cell("Temp", h: 36pt),) } else { () })))
#let resources(hr) = grid(columns: (1.45fr, 1fr, 1fr, 1fr), column-gutter: 6pt,
  pool("HIT POINTS", maximum: if hr == none { none } else { hr.stats.HP }, temp: true),
  pool("ENERGY / NRG", maximum: if hr == none { none } else { hr.stats.NRG }),
  pool("LUCK", maximum: if hr == none { none } else { hr.stats.Luck }),
  pool("ACTION POINTS", maximum: if hr == none { none } else { hr.stats.AP }, ap: true))

#let paragraph-item(it) = {
  block(above: 3pt, grid(columns: (5pt, 1fr), column-gutter: 3pt, text(size: 10pt, "-"), rich(it.runs)))
  for sub in it.sub {
    block(above: 2pt, inset: (left: 8pt), grid(columns: (5pt, 1fr), column-gutter: 3pt, text(size: 10pt, "-"), rich(sub)))
  }
}
// Very long form-rule paragraphs may cross columns at a sentence boundary.
// Slice the existing text runs, retaining every character and emphasis run.
#let sentence-parts(rs) = {
  let flat = rs.map(r => r.at(0)).join("")
  if flat.len() < 900 { (rs,) } else {
    let sentences = flat.split(". ")
    let best = none
    let distance = flat.len()
    let count = 0
    for sentence in sentences.slice(0, sentences.len() - 1) {
      count += sentence.len() + 2
      let d = calc.abs(count - flat.len() / 2)
      if d < distance { distance = d; best = count }
    }
    if best == none { (rs,) } else {
      let a = (); let b = (); let offset = 0
      for r in rs {
        let txt = r.at(0)
        let n = calc.min(txt.len(), calc.max(0, best - offset))
        if n > 0 { a.push((txt.slice(0, n), r.at(1))) }
        if n < txt.len() { b.push((txt.slice(n), r.at(1))) }
        offset += txt.len()
      }
      (a, b)
    }
  }
}
#let chunks(hr, titles, headings: false) = {
  let out = ()
  for s in hr.sections.filter(s => titles.contains(s.title)) {
    for (i, it) in s.items.enumerate() {
      out.push({
        if headings and i == 0 {
          block(above: 4pt, below: 3pt, width: 100%, fill: label-fill, inset: 4pt,
            small(s.title, size: 10pt))
        }
        block(above: 3pt, grid(columns: (5pt, 1fr), column-gutter: 3pt,
          text(size: 10pt, "-"), rich(it.runs)))
      })
      for sub in it.sub {
        for (part-index, part) in sentence-parts(sub).enumerate() {
          out.push(block(above: 2pt, inset: (left: 8pt), grid(columns: (5pt, 1fr), column-gutter: 3pt,
            text(size: 10pt, if part-index == 0 { "-" } else { "" }), rich(part))))
        }
      }
    }
  }
  out
}
#let balanced(body) = layout(sz => {
  let w = (sz.width - 14pt) / 2
  let combine(parts) = { for part in parts { block(width: 100%, part) } }
  let best = (combine(body), [])
  let best-h = measure(block(width: w, best.at(0))).height
  for i in range(1, body.len()) {
    let a = combine(body.slice(0, i))
    let b = combine(body.slice(i))
    let H = calc.max(measure(block(width: w, a)).height, measure(block(width: w, b)).height)
    if H < best-h { best = (a, b); best-h = H }
  }
  grid(columns: (w, w), column-gutter: 14pt, ..best)
})
#let sense-body(hr) = {
  let s = hr.stats.at("Senses", default: none)
  if s != none {
    let r = DATA.reminders.at(if s.starts-with("Superior") { "Superior Darkvision" } else { "Darkvision" })
    ({ block(above: 4pt, below: 3pt, fill: label-fill, inset: 4pt, width: 100%, small(r.head, size: 10pt)); rich(r.runs) },)
  } else { () }
}
#let reverse-heading(title, hr: none) = block(width: 100%, height: 44pt, stroke: 1pt + ink, {
  place(block(width: 100%, height: 44pt, fill: ink, inset: (left: 9pt, top: 5pt),
    grid(columns: (1fr, 180pt), align: horizon,
      text(font: goth, weight: 700, size: 25pt, fill: paper, title),
      block(inset: 1pt, cell("Hero / Reverse", value: get(hr, "name"), h: 32pt, size: 13pt)))))
})

#let basic-card(hr) = {
  record-page("Basic Mode / front", {
    identity(hr); v(8pt); statistics(hr); v(8pt); resources(hr); v(8pt)
    panel("Equipment and Items", {
      text(size: 9pt)[*Armour Dice:* #hr.stats.AD]
      balanced(chunks(hr, ("Equipment and Items",)))
    })
    v(8pt)
    panel("Basic Mode", grid(columns: (1fr, 1fr), column-gutter: 14pt,
      rich(DATA.notes.hands), rich(DATA.notes.knocked_out)))
    v(8pt)
    grid(columns: (1fr, 1fr, 1fr), column-gutter: 0pt,
      cell("Active Hand", h: 36pt), cell("Active Hand", h: 36pt), cell("Carried Coins", h: 36pt))
    v(8pt)
    block(height: 1fr, panel("Carried Items and Changes", h: "fill", ruled-area()))
  })
  record-page("Basic Mode / reverse", {
    reverse-heading("Talents and Powers", hr: hr)
    v(8pt)
    panel("Abilities and Rules", balanced(chunks(hr, ("Ancestry Traits", "Background Rule", "Talents, Powers, and Special Rules", "Weapon Trait Rules"), headings: true) + sense-body(hr)))
    v(8pt)
    block(height: 1fr, panel("Notes", h: "fill", ruled-area()))
  })
}
