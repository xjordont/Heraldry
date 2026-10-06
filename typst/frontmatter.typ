// Front and back matter: title page, how-to-use, generated contents, index.
#import "heraldry.typ": *
#import "cover.typ": front-cover, back-cover
#let edition = sys.inputs.at("edition", default: "print")

#let how-to-use = json("../editorial/how_to_use.json")
#let index-data = if sys.inputs.at("index", default: "on") == "on" { json("../build/index.json") } else { (entries: ()) }

#let title-page(title, subtitle, version) = page(header: none, footer: none, margin: (x: 0.9in, y: 0.9in))[
  #metadata("title") <frontmatter-start>
  #v(1.3in)
  #align(center)[
    #motif(len: 110pt)
    #v(26pt)
    #set par(leading: 10pt)
    #text(font: display, weight: 700, size: 40pt, tracking: 0.03em, hyphenate: false, title.at(0))
    #v(4pt)
    #text(font: display, weight: 600, size: 20pt, tracking: 0.12em, title.at(1))
    #v(22pt)
    #line(length: 40%, stroke: 0.7pt + ink)
    #v(18pt)
    #block(width: 80%)[#set par(leading: 5pt); #set text(size: 12pt, style: "italic"); #subtitle]
    #v(1fr)
  ]
  #place(bottom + center, dy: -0.4in)[
    #set text(font: sans, size: 10pt, tracking: 0.1em)
    #version
  ]
]

#let toc-page() = {
  pagebreak(weak: true)
  block(width: 100%)[
    #align(center)[
      #v(0.2in)
      #motif(len: 60pt)
      #v(6pt)
      #text(font: display, weight: 600, size: 22pt)[Contents]
      #v(4pt)
    ]
  ]
  set text(size: 10pt)
  show outline.entry.where(level: 1): it => {
    v(9pt, weak: true)
    block(sticky: true)[
      #set text(font: display, weight: 600, size: 11pt)
      #link(it.element.location())[#it.element.body #box(width: 1fr, repeat(text(fill: rule-ink)[.#h(3pt)])) #text(font: sans, weight: 600, size: 10pt, it.page())]
    ]
  }
  show outline.entry.where(level: 2): it => {
    block(above: 3pt, below: 0pt, inset: (left: 10pt))[
      #set text(size: 9.5pt)
      #link(it.element.location())[#it.element.body #box(width: 1fr, repeat(text(fill: rule-ink)[.#h(3pt)])) #text(font: sans, size: 9.5pt, it.page())]
    ]
  }
  columns(2, gutter: gap, outline(title: none, depth: 2, indent: 0pt))
}

#let version-text = json("../build/cover.json").version
#let frontmatter(title: ("HERALDRY SKIRMISH", "THE DYING LANDS"), subtitle: [], version: []) = {
  if edition == "digital" {
    front-cover(title, emph(subtitle), version)
    page(header: none, footer: none, numbering: none)[]   // inside front cover (keeps recto/verso parity)
  }
  set page(numbering: "i")
  counter(page).update(1)
  title-page(title, subtitle, version)
  // verso of title: production/edition notice (verified information only)
  page(header: none)[
    #v(1fr)
    #set text(font: sans, size: 9pt, fill: ink)
    #set par(leading: 3pt, spacing: 6pt)
    #block(width: 70%)[
      #for p in how-to-use.colophon [#p #parbreak()]
    ]
  ]
  // How to use this book
  pagebreak(weak: true)
  align(center)[#v(0.2in) #motif(len: 60pt) #v(6pt) #text(font: display, weight: 600, size: 22pt, how-to-use.title) #v(10pt)]
  columns(2, gutter: gap)[
    #for s in how-to-use.sections [
      #heading(level: 4, outlined: false, bookmarked: false, s.heading)
      #for p in s.paras [#p #parbreak()]
    ]
  ]
  toc-page()
}

#let mainmatter() = {
  pagebreak(to: "odd", weak: true)
  [#metadata("main") <mainmatter>]
}

#let index-page() = {
  if index-data.entries.len() == 0 { return }
  pagebreak(weak: true)
  block(width: 100%, below: 14pt)[
    #metadata("index") <chapter-opener>
    #v(0.35in)
    #align(center)[
      #motif(len: 80pt)
      #v(10pt)
      #heading(level: 1, outlined: true, bookmarked: true, "Index") <index>
      #v(8pt)
      #line(length: 36%, stroke: 0.6pt + ink)
      #v(8pt)
      #block(width: 80%)[#set text(size: 9.5pt, style: "italic"); #index-data.note]
    ]
  ]
  set text(font: sans, size: 9.5pt)
  set par(leading: 2.4pt, spacing: 2pt, hanging-indent: 10pt)
  let pages-for(key) = {
    let hits = query(label("ix-" + key)).map(h => h.location())
    for hid in index-data.at("heads", default: (:)).at(key, default: ()) {
      let q = query(label(hid))
      if q.len() > 0 { hits.push(q.first().location()) }
    }
    let ps = hits.map(l => (n: counter(page).at(l).first(), loc: l))
    let seen = ()
    let out = ()
    for p in ps.sorted(key: p => p.n) {
      if p.n not in seen { seen.push(p.n); out.push(link(p.loc, str(p.n))) }
    }
    out.join(", ")
  }
  columns(3, gutter: 14pt)[
    #let letter = ""
    #for e in index-data.entries {
      let l = upper(e.term.first())
      if l != letter {
        letter = l
        block(above: 9pt, below: 4pt, sticky: true, text(font: display, weight: 700, size: 11pt, l))
      }
      block(above: 2.5pt, below: 0pt, breakable: false)[
        #text(weight: 600, e.term)#if e.keys.len() > 0 [, #context e.keys.map(k => pages-for(k)).join(", ")]#if e.at("see", default: none) != none [. #emph[See] #e.see]#if e.at("also", default: none) != none [. #emph[See also] #e.also]
      ]
      for s in e.at("sub", default: ()) {
        block(above: 1.5pt, below: 0pt, inset: (left: 9pt), breakable: false)[
          #s.term, #context s.keys.map(k => pages-for(k)).join(", ")
        ]
      }
    }
  ]
}

#let backmatter() = {
  index-page()
  if edition == "digital" {
    let cd = json("../build/cover.json")
    back-cover((lead: emph(cd.lead), facts: cd.facts), version-text)
  }
}
