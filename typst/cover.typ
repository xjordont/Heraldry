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
    #text(font: serif, size: 11pt, weight: 600, tracking: 0.1em, smallcaps(all: true, version))
  ]
]

#let front-cover(title, subtitle, version) = if json("../build/cover.json").art.at("full_page", default: false) {
  // owner-supplied cover picture with its own lettering (2026-10-14): the whole front cover, inside the safe edge
  let cart = json("../build/cover.json").art
  cover-page[#place(center + horizon, image(cart.path, width: cart.w_in * 1in, height: cart.h_in * 1in))]
} else [#front-cover-classic(title, subtitle, version)]

#let back-cover(copy, version) = cover-page[
  #frame-border(false)
  // Numeric ranges ("4–8 rounds") never break after the dash; the text is unchanged.
  #show regex("\d+–\d+"): it => box(it)
  #let bart = json("../build/cover.json").at("back_art", default: none)
  // With the party scene, the frame's crest already heads the page; a second crest flourish
  // directly beneath it would repeat the motif, so the blurb opens the composition instead.
  #place(top + center, dy: if bart != none { 1.3in } else { 1.25in }, block(width: 5.4in)[
    #set align(center)
    #if bart == none {
      flourish(len: 70pt)
      v(14pt)
    }
    #set par(leading: 5pt, justify: false)
    #set text(font: fell, size: 13pt)
    #show emph: it => it.body
    // Measure chosen so the blurb ends on a full last line (no runt).
    #block(width: 5.2in, copy.lead)
    #if bart != none {
      // the approved ink party scene carries the eye from the lead to the game facts
      v(16pt)
      image(bart.path, width: bart.w_in * 1in, height: bart.h_in * 1in)
      v(16pt)
    } else {
      v(18pt)
      brush(weight: 1.8pt, seed: 21)
      v(14pt)
    }
    // Game facts: ragged left in a narrower measure under a short brush, so they read as a note while
    // the centred blurb above keeps its voice (D-10).
    #block(width: 1.4in, brush(weight: 1.5pt, seed: 23))
    #v(10pt)
    #block(width: 4.8in, align(left, {
      set text(font: serif, size: 11pt)
      set par(leading: 4pt, spacing: 9pt, justify: false)
      for p in copy.facts [#p #parbreak()]
    }))
  ])
  #let pub = json("../build/cover.json").at("publisher", default: none)
  #place(bottom + center, dy: if bart != none { -0.75in } else { -1.05in })[
    #set align(center)
    // The Escutcheon Press device (owner, 2026-10-30) replaces the book's castle mark here: the frame
    // already carries the castle at its head, and the foot of a back cover is the publisher's place.
    #if pub != none { publisher-logo(1.15in) } else { signature(s: 70pt) }
    #v(8pt)
    #text(font: serif, size: 10pt, weight: 600, tracking: 0.1em, smallcaps(all: true, version))
  ]
]
