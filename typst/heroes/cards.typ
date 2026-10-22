// The 24 Basic Mode hero cards (Appendix B.4): the hero sheet's front, filled in, and a back that prints
// every remaining profile rule verbatim from typst/heroes/basic-heroes.json (tools/hero_cards.py).
// sys.inputs.hero: one Hero's name, or "all" for the full set in roster order.
#import "hero.typ": *

#let rules-head(t) = block(above: 9pt, below: 3pt, sticky: true, {
  grid(columns: (auto, 1fr), column-gutter: 6pt, align: horizon,
    text(font: goth, weight: 700, size: 13.5pt, t),
    box(width: 100%, height: 4pt, align(horizon, line(length: 100%, stroke: 0.5pt + ink))))
})

#let back-rules(hr) = leaf(hr.name, hr.class + " · " + hr.role, face: "back", arm: 13, title-size: 26pt)[
  #set text(size: 10pt)
  #let body = {
    for s in hr.sections.filter(s => s.title != "Equipment and Items") {
      rules-head(s.title)
      for it in s.items { rule-item(it) }
    }
    let senses = hr.stats.at("Senses", default: none)
    if senses != none {
      let key = if senses.starts-with("Superior") { "Superior Darkvision" } else { "Darkvision" }
      let r = DATA.reminders.at(key)
      rules-head(r.head)
      block(above: 5pt, rich(r.runs))
    }
  }
  #plate(title: "Rules", inset: (x: 12pt, top: 13pt, bottom: 10pt), balanced-pair(body))
  #v(BAND)
  #block(height: 1fr, plate(title: "Notes", h: "fill")[#ruled(h: 1fr)])
]

#let pick = sys.inputs.at("hero", default: "all")
#for hr in DATA.heroes.filter(x => pick == "all" or x.name == pick) {
  front(hr)
  back-rules(hr)
}
