// Compact Hero records. Exact profile text comes from the RC-bound extractor.
// Ornament belongs to identity; rules, tables, and pencil fields share a quiet grid.
#import "parts.typ": *
#let DATA = json("/typst/heroes/basic-heroes.json")
#let signed(n) = if n >= 0 { "+" + str(n) } else { "-" + str(-n) }

#let sheet-label(t) = text(font: sans, size: 9pt, weight: 700, t)
#let section(t) = block(above: 6pt, below: 3pt, sticky: true, width: 100%, {
  grid(columns: (auto, 1fr), column-gutter: 7pt, align: horizon,
    sheet-label(t), line(length: 100%, stroke: 0.7pt + ink))
})
#let write-field(t, value: none, h: 27pt, size: 12pt) = block(height: h, width: 100%, spacing: 0pt, {
  place(top + left, sheet-label(t))
  place(bottom + left, line(length: 100%, stroke: 0.5pt + pen))
  if value != none { place(bottom + left, dy: -2pt, dx: 2pt, fit-inked(value, size: size)) }
})
#let record-table(heads, widths, n, row: 20pt, first: ()) = table(
  columns: widths, rows: (16pt,) + (row,) * n, inset: (x: 3pt, y: 0pt),
  align: left + horizon,
  stroke: (x, y) => (bottom: if y == 0 { 0.7pt + ink } else { 0.4pt + pen },
    left: if x > 0 { 0.4pt + pen } else { none }),
  ..heads.map(sheet-label),
  ..range(n).map(r => (text(size: 9pt, first.at(r, default: "")),) + range(heads.len() - 1).map(_ => [])).flatten())
#let lines(n, pitch: 20pt) = block(width: 100%, height: n * pitch, spacing: 0pt,
  fill: tiling(size: (12pt, pitch), place(bottom + left, line(length: 12pt, stroke: 0.4pt + pen))))

#let compact-footer(face) = place(bottom + left, dy: 20pt, block(width: 100%, {
  line(length: 100%, stroke: 0.7pt + ink)
  v(3pt)
  grid(columns: (1fr, auto), text(size: 9pt, weight: 700, "HERALDRY SKIRMISH"),
    text(size: 9pt, "Rules " + rules-rc + " | " + face))
}))
#let record-page(face, body) = page(width: 612pt, height: 792pt,
  margin: (x: 32pt, top: 40pt, bottom: 50pt), fill: paper)[
  #set text(font: sans, size: 9.5pt, fill: ink, lang: "en", region: "CA", hyphenate: false,
    top-edge: 0.8em, bottom-edge: -0.25em)
  #set par(leading: 2.3pt, spacing: 3.2pt, justify: false)
  #set strong(delta: 200)
  #body
  #compact-footer(face)
]

#let compact-title(title, sub, hr: none) = block(width: 100%, spacing: 0pt, below: 8pt, {
  grid(columns: (1fr, 78pt), column-gutter: 14pt,
    {
      text(size: 9pt, weight: 700, tracking: 0.1em, "HERALDRY SKIRMISH / HERO RECORD")
      v(3pt)
      text(font: goth, size: 29pt, weight: 700, title)
      v(3pt)
      text(size: 10pt, sub)
      v(5pt)
      if hr != none {
        text(size: 9pt)[Level #hr.level | #hr.archetype | Casting: #hr.casting | HP/Level: #hr.hp_per_level]
        v(3pt)
        text(size: 9pt)[Senses: #hr.stats.at("Senses", default: "None") | AD: #hr.stats.AD]
      }
    },
    if hr == none { align(right, arms(6, w: 40pt)) } else {
      align(center, image("/assets/art/ink/" + hr.art + ".png", width: 78pt, height: 86pt, fit: "contain"))
    })
})

#let attribute-strip(hr) = {
  let val(k) = if hr == none { none } else { hr.scores.at(k) }
  let init = if hr == none { none } else {
    signed(int(hr.scores.INT.replace("+", "")) + int(hr.scores.SPI.replace("+", "")))
  }
  grid(columns: (1fr, 1fr, 1fr, 1fr, 1.5fr, 1fr, 1fr), column-gutter: 5pt,
    ..("STR", "DEX", "INT", "SPI", "Initiative", "Speed", "Size").enumerate().map(((i, k)) => {
      let value = if i < 4 { val(k) } else if i == 4 { init } else if hr == none { none } else if i == 5 { hr.stats.SPD } else { hr.stats.Sz }
      block(width: 100%, height: 43pt, stroke: 0.6pt + ink, inset: 4pt, {
        sheet-label(k)
        v(3pt)
        if value != none { inked(value, size: 18pt) }
        if i == 4 { h(4pt); text(size: 9pt, "INT + SPI") }
      })
    }))
}
#let resource-strip(hr) = {
  let st(k) = if hr == none { none } else { hr.stats.at(k) }
  grid(columns: (1.45fr, 1fr, 1fr, 1fr), column-gutter: 9pt,
    ..(("HP", st("HP")), ("NRG", st("NRG")), ("Luck", st("Luck")), ("AP", st("AP"))).map(((k, maximum)) => {
      block(height: 42pt, width: 100%, {
        sheet-label(k)
        h(5pt)
        text(size: 9pt)[#if k == "AP" { "Allowance" } else { "Max" }: #if maximum != none { strong(maximum) } else { "______" }]
        v(4pt)
        grid(columns: if k == "HP" { (1fr, 1fr) } else { (1fr,) }, column-gutter: 5pt,
          write-field("Current", h: 23pt), ..if k == "HP" { (write-field("Temp", h: 23pt),) } else { () })
      })
    }))
}

#let profile-sections(hr, filter: "all") = {
  let chunks = ()
  for s in hr.sections.filter(s => if filter == "all" { true } else if filter == "equipment" {
    s.title == "Equipment and Items"
  } else { s.title != "Equipment and Items" }) {
    for (i, it) in s.items.enumerate() {
      chunks.push({
        if i == 0 { section(s.title) }
        block(above: 3.5pt, grid(columns: (5pt, 1fr), column-gutter: 3pt,
          text(size: 9pt, "-"), rich(it.runs)))
      })
      for sub in it.sub {
        chunks.push(block(above: 2.5pt, inset: (left: 8pt),
          grid(columns: (5pt, 1fr), column-gutter: 3pt, text(size: 9pt, "-"), rich(sub))))
      }
    }
  }
  chunks
}
#let senses-rule(hr) = {
  let sense = hr.stats.at("Senses", default: none)
  if sense != none {
    let key = if sense.starts-with("Superior") { "Superior Darkvision" } else { "Darkvision" }
    let r = DATA.reminders.at(key)
    ({ section(r.head); rich(r.runs) },)
  } else { () }
}
#let basic-rules = (
  { section("Basic Mode / Hands and 0 HP"); rich(DATA.notes.hands) },
  block(above: 3.2pt, rich(DATA.notes.knocked_out)),
)
// Choose a real paragraph boundary by measuring both candidate columns. No
// sentence is cut at the column boundary and a section heading keeps its item.
#let rule-columns(chunks) = layout(sz => {
  let w = (sz.width - 16pt) / 2
  let collect(parts) = { for part in parts { block(width: 100%, part) } }
  let best = none
  let best-h = 100000pt
  for i in range(1, chunks.len()) {
    let a = collect(chunks.slice(0, i))
    let b = collect(chunks.slice(i))
    let h = calc.max(measure(block(width: w, a)).height, measure(block(width: w, b)).height)
    if h < best-h { best = (a, b); best-h = h }
  }
  grid(columns: (w, w), column-gutter: 16pt, ..best)
})
#let card-notes = {
  section("Notes")
  grid(columns: (1fr, 1fr, 1fr), column-gutter: 12pt,
    write-field("Active Hand", h: 29pt), write-field("Active Hand", h: 29pt), write-field("Carried Coins", h: 29pt))
  lines(2)
}
#let compact-card(hr) = {
  let all-rules = profile-sections(hr) + senses-rule(hr)
  let gear = profile-sections(hr, filter: "equipment")
  let other = profile-sections(hr, filter: "other") + senses-rule(hr)
  let reverse-head = block(height: 47pt, {
    text(font: goth, size: 26pt, weight: 700, hr.name)
    v(4pt)
    text(size: 9pt, hr.class + " / Profile rules / continued")
  })
  // This first page establishes actual typography and available page size before
  // choosing the layout. The two-side fallback is an explicit content split.
  record-page("Basic Mode", layout(sz => {
    let header = {
      compact-title(hr.name, hr.class + " / " + hr.ancestry + " " + hr.background + " / " + hr.role, hr: hr)
      attribute-strip(hr); v(6pt); resource-strip(hr); v(3pt)
    }
    let one = { header; rule-columns(all-rules + basic-rules); card-notes }
    if measure(block(width: sz.width, one)).height <= sz.height - 5pt {
      one
    } else {
      let best = none
      let best-height = 100000pt
      for split in range(0, other.len() - 1) {
        let front = { header; text(size: 9pt, weight: 700, "RULES CONTINUE ON REVERSE");
          rule-columns(gear + other.slice(0, split) + basic-rules); card-notes }
        let back = { reverse-head; rule-columns(other.slice(split)); section("Notes"); lines(3) }
        let h = calc.max(measure(block(width: sz.width, front)).height, measure(block(width: sz.width, back)).height)
        if h < best-height { best = split; best-height = h }
      }
      assert(best-height <= sz.height - 5pt, message: hr.name + ": full profile cannot fit one duplex sheet")
      header
      text(size: 9pt, weight: 700, "RULES CONTINUE ON REVERSE")
      rule-columns(gear + other.slice(0, best) + basic-rules)
      card-notes
      block(height: 1fr, width: 100%, fill: tiling(size: (12pt, 20pt),
        place(bottom + left, line(length: 12pt, stroke: 0.4pt + pen))))
      [#metadata((name: hr.name, split: best)) <hero-needs-back>]
    }
  }))
  context {
    let matches = query(<hero-needs-back>).filter(it => it.value.name == hr.name)
    if matches.len() > 0 {
      record-page("Basic Mode / reverse", {
        reverse-head
        rule-columns(other.slice(matches.first().value.split))
        section("Notes")
        block(height: 1fr, width: 100%, fill: tiling(size: (12pt, 20pt),
          place(bottom + left, line(length: 12pt, stroke: 0.4pt + pen))))
      })
    }
  }
}
