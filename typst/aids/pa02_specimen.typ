// SPECIMEN — Player Aid 2, Monster AI (front), v2.
// Wording condensed from RC512 §9.5 (A–F), §3.4 and C.8; not yet semantically reviewed.
#import "/typst/templates/system.typ": *

#let M = 36pt
#set page(width: page-w, height: page-h, margin: (x: M, top: M, bottom: M), fill: paper)
#show: base
#set text(font: sans, size: 10.5pt, hyphenate: false)
#set par(justify: false, leading: 3.4pt, spacing: 5pt)

// ---------------------------------------------------------------- shared aid kit
#let iron-band(arm, code, title, refs) = block(width: 100%, spacing: 0pt, {
  block(width: 100%, fill: ink, inset: (left: 10pt, right: 13pt, y: 8pt), spacing: 0pt,
    grid(columns: (auto, 1fr, auto), column-gutter: 11pt, align: horizon,
      arms(arm, w: 40pt),
      text(font: goth, weight: 700, size: 38pt, fill: paper, title),
      align(right, text(fill: paper, font: sans, weight: 700, size: 9.5pt, tracking: 0.18em)[PLAYER AID #code \ #text(weight: 600, tracking: 0.08em, refs)])))
  v(2pt); line(length: 100%, stroke: 0.7pt + ink)
})

// Step number on an engraved shield.
#let num(n, w: 24pt) = shield(w: w, inner: true, body: text(weight: 800, size: 11pt, fill: paper, str(n)))

// Forged arrow: a tapered shaft swelling toward a barbed broadhead. Horizontal, pointing right.
#let forged-h(len) = box(width: len, height: 16pt, {
  let y = 8pt
  place(polygon(fill: ink,
    (0pt, y - 1.3pt), (len - 15pt, y - 2.9pt), (len - 18pt, y - 8pt), (len, y),
    (len - 18pt, y + 8pt), (len - 15pt, y + 2.9pt), (0pt, y + 1.3pt)))
})
// The same arrow pointing down.
#let forged-v(len) = box(width: 16pt, height: len, {
  let x = 8pt
  place(polygon(fill: ink,
    (x - 1.3pt, 0pt), (x - 2.9pt, len - 15pt), (x - 8pt, len - 18pt), (x, len),
    (x + 8pt, len - 18pt), (x + 2.9pt, len - 15pt), (x + 1.3pt, 0pt)))
})
#let flag(t) = tag(t, size: 8.2pt)

#let yes-arrow = box(width: 62pt, {
  align(center, flag[Yes]); v(-1pt); forged-h(62pt)
})
#let down(label: "No", h: 22pt) = block(above: 2pt, below: 2pt, width: 100%, inset: (left: 98pt),
  grid(columns: (16pt, auto), column-gutter: 6pt, align: horizon, forged-v(h), if label != none { flag(label) }))

// Decision: a drawn-out lozenge plaque with an engraved inner rule.
#let plaque(body, w: 160pt) = context {
  let t = block(width: w - 46pt, align(center, text(weight: 800, size: 11.5pt, body)))
  let h = measure(t).height + 18pt
  let pts(i) = ((h/2 + i, i), (w - h/2 - i, i), (w - 2 * i, h/2), (w - h/2 - i, h - i), (h/2 + i, h - i), (2 * i, h/2))
  box(width: w, height: h, {
    place(polygon(stroke: 1.8pt + ink, fill: tint, ..pts(0pt)))
    place(polygon(stroke: 0.45pt + ink, ..pts(3.2pt)))
    place(center + horizon, t)
  })
}

// Action box with an ENDS banner pinned to its lower-right corner.
#let endbox(body, ends: true) = block(width: 100%, inset: (right: 7pt), {
  block(width: 100%, stroke: 1.3pt + ink, inset: (left: 8pt, right: 10pt, top: 7pt, bottom: if ends { 11pt } else { 7pt }), body)
  if ends { place(bottom + right, dx: 7pt, dy: 7pt, tag[Ends]) }
})
#let rung(n, q, act) = grid(columns: (26pt, 160pt, 62pt, 1fr), column-gutter: 4pt, align: horizon,
  num(n), plaque(q), yes-arrow, endbox(act))

#let aside-head(t, seed: 1) = block(above: 0pt, below: 6pt, sticky: true, {
  text(font: goth, weight: 700, size: 18pt, t); v(-4pt); brush(weight: 2.4pt, seed: seed)
})
#let mini(n, body) = block(above: 4pt, below: 0pt, grid(columns: (17pt, 1fr), column-gutter: 6pt, align: top,
  shield(w: 15pt, body: text(weight: 800, size: 8.4pt, fill: paper, str(n))), body))
#let gap-v = v(13pt)

// ---------------------------------------------------------------- sheet
#iron-band(9, "2", "Monster AI", "§ 9.5 · § 3.4 · C.8")
#v(11pt)

#block(spacing: 0pt, inset: (left: 30pt, right: 7pt), endbox(ends: false)[
  #text(font: goth, weight: 700, size: 15pt)[Each Monster activates] #h(6pt)
  Pick the *Primary Target* (printed Target Priority first). Roll for spent Recharge abilities. Resolve start-of-activation Special Abilities.])
#down(label: none, h: 20pt)
#rung(1, [Any AI Step valid?], [Resolve the *first* valid one, lowest number first. *on d6 N+:* roll 1d6, need N or higher. #h(1fr) #text(size: 9.5pt)[_Says it continues? Go to step 2._]])
#down()
#rung(2, [Engaged?], [Attack the Engaged enemy with the *lowest current HP*. Use Multi-Attack if listed; otherwise melee, or ranged if it has no melee attack.])
#down()
#rung(3, [Enemy visible?], [Move toward the Primary Target; attack if Engaged on arrival. *Ranged:* move to the nearest legal firing position, then attack. *Knocked Out target:* stop within melee distance and attack.])
#down()
#rung(4, [Hidden enemy within 12″ and LOS?], [*Search:* the nearest one's controller makes a DEX Check. On a failure, that enemy is no longer Hidden.])
#down()
#grid(columns: (26pt, 1fr), column-gutter: 4pt, align: horizon, num(5),
  endbox[Move toward the Guard Point, objective, patrol route or scenario destination.])

#v(14pt)
#grid(columns: (1fr, 1fr, 1fr), column-gutter: 18pt,
[
  #aside-head(seed: 1)[Primary Target]
  The *nearest visible enemy* within 12″ and LOS. Hidden and Invisible enemies don't count unless a rule says so. Re-pick if it stops being legal.
  #v(5pt)
  #text(weight: 800, size: 9pt, tracking: 0.14em)[TIES, IN ORDER]
  #mini(1)[Lowest current HP]
  #mini(2)[Last to damage this Monster]
  #mini(3)[Random Determination]
],
[
  #aside-head(seed: 3)[Movement]
  #mini(1)[Shortest legal route]
  #mini(2)[Tied routes: avoid hazards]
  #mini(3)[End at the nearest spot to attack or threaten]
  #v(10pt)
  #aside-head(seed: 7)[Never]
  No AP, NRG or Reactions. Effects that call for a Check apply unless Immune; Terrain Checks always succeed.
],
[
  #aside-head(seed: 5)[Blocked Route]
  Can't reach and attack the Primary Target? Switch to the nearest visible enemy it can. None: move full Speed toward the target (or a firing position) and don't attack.
]
)

// ink vignette at a boundary: lower right corner, standing on the footer rule
#place(bottom + right, dx: M - 10pt, dy: -3pt, image("/assets/art/ink/ART-MON-MINOTAUR.png", width: 118pt))

// footer
#place(bottom + left, dy: 14pt, block(width: 100%, {
  block(spacing: 0pt, line(length: 100%, stroke: 1.6pt + ink)); v(2pt); block(spacing: 0pt, line(length: 100%, stroke: 0.4pt + ink))
  v(5pt)
  grid(columns: (auto, 1fr, auto), column-gutter: 6pt, align: horizon,
    signature(s: 14pt),
    text(size: 9pt, weight: 700, tracking: 0.1em)[HERALDRY SKIRMISH · THE DYING LANDS],
    text(size: 9pt, fill: ink3)[Rules RC512 · front · SPECIMEN])
}))
