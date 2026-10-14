// Front and back cover sheets (portrait US Letter, borderless background).
// Design v4: the castle logo, the opener-frame border and live type (owner-approved marks 2026-10-13).
#import "heraldry.typ": *

#let cover-page(body) = page(width: page-w, height: page-h, fill: substrate, margin: 0pt, header: none, footer: none, numbering: none, body)

#let front-cover-classic(title, subtitle, version) = cover-page[
  // thin inset frame at a safe distance (decorative, inside the 0.375 in safe edge)
  #frame-border(true)
  #place(top + center, dy: 0.95in)[
    #set align(center)
    #set par(leading: 8pt)
    #text(font: serif, weight: 700, size: 36pt, tracking: 0.12em, hyphenate: false, title.at(0))
    #v(4pt)
    #text(font: serif, weight: 600, size: 16pt, tracking: 0.32em, title.at(1))
    #v(6pt)
    #flourish(len: 110pt)
  ]
  // cover art from build/cover.json: generated ink art when selected, else ART-COVER-001 at native 300 ppi; title stays live type
  #let cart = json("../build/cover.json").art
  #place(center + horizon, dy: 0.45in, image(cart.path, width: cart.w_in * 1in, height: cart.h_in * 1in))
  #place(bottom + center, dy: -1.0in)[
    #set align(center)
    #block(width: 5.2in)[#set text(font: fell, size: 14pt); #show emph: it => it.body; #subtitle]
    #v(14pt)
    #text(font: sans, size: 11pt, weight: 600, tracking: 0.12em, version)
  ]
]

#let front-cover(title, subtitle, version) = if json("../build/cover.json").art.at("full_page", default: false) {
  // owner-supplied cover picture with its own lettering (2026-10-14): the whole front cover, inside the safe edge
  let cart = json("../build/cover.json").art
  cover-page[#place(center + horizon, image(cart.path, width: cart.w_in * 1in, height: cart.h_in * 1in))]
} else [#front-cover-classic(title, subtitle, version)]

#let back-cover(copy, version) = cover-page[
  #frame-border(false)
  #place(top + center, dy: 1.25in, block(width: 5.4in)[
    #set align(center)
    #flourish(len: 70pt)
    #v(16pt)
    #set par(leading: 5pt, justify: false)
    #set text(font: fell, size: 13pt)
    #show emph: it => it.body
    #copy.lead
    #v(18pt)
    #brush(weight: 1.8pt, seed: 21)
    #v(14pt)
    #set text(font: serif, size: 11pt)
    #set par(leading: 4pt, spacing: 9pt)
    #for p in copy.facts [#p #parbreak()]
  ])
  #place(bottom + center, dy: -1.05in)[
    #set align(center)
    #signature(s: 70pt)
    #v(10pt)
    #text(font: sans, size: 10pt, weight: 600, tracking: 0.12em, version)
  ]
]
