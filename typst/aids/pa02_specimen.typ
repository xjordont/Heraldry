// SPECIMEN — Player Aid 2, Monster AI (front). Wording abridged from RC512 §9.5 / C.8; not yet fidelity-reviewed.
#import "/typst/templates/system.typ": *

#let M = 36pt
#set page(width: page-w, height: page-h, margin: (x: M, top: M, bottom: M), fill: paper)
#show: base
#set text(font: sans, size: 9.5pt, hyphenate: false)
#set par(justify: false, leading: 3pt, spacing: 4pt)

// ---------- aid components (proposed shared kit) ----------
#let iron-band(arm, code, title, refs) = block(width: 100%, spacing: 0pt, {
  block(width: 100%, fill: ink, inset: (left: 10pt, right: 12pt, y: 7pt), spacing: 0pt,
    grid(columns: (auto, 1fr, auto), column-gutter: 10pt, align: horizon,
      arms(arm, w: 34pt),
      text(font: goth, weight: 600, size: 30pt, fill: paper, title),
      align(right, text(fill: paper, font: sans, weight: 700, size: 9pt, tracking: 0.18em)[PLAYER AID #code \ #text(weight: 600, tracking: 0.08em, refs)])))
  v(1.5pt); line(length: 100%, stroke: 0.6pt + ink)
})
#let num(n, w: 17pt) = shield(w: w, inner: true, body: text(weight: 700, size: 8.6pt, fill: paper, str(n)))
#let ends = tag[Ends]
#let proc(body, w: 100%) = block(width: w, stroke: 0.8pt + ink, inset: (x: 7pt, y: 6pt), body)
#let plaque(body, w: 128pt) = context {
  let t = block(width: w - 22pt, align(center, text(weight: 700, size: 10pt, body)))
  let h = measure(t).height + 12pt
  box(width: w, height: h, {
    place(polygon(stroke: 1.1pt + ink, fill: tint, (h/2, 0pt), (w - h/2, 0pt), (w, h/2), (w - h/2, h), (h/2, h), (0pt, h/2)))
    place(center + horizon, t)
  })
}
#let harrow(label) = box(width: 34pt, {
  align(center, text(size: 7.6pt, weight: 700, tracking: 0.14em, label))
  v(-2pt)
  box(width: 34pt, height: 6pt, {
    place(dy: 3pt, line(length: 28pt, stroke: 1pt + ink))
    place(polygon(fill: ink, (27pt, 0pt), (34pt, 3pt), (27pt, 6pt)))
  })
})
#let varrow(label) = block(spacing: 0pt, width: 100%, inset: (left: 70pt), box(height: 20pt, {
  place(dx: 0pt, line(start: (0pt, 0pt), end: (0pt, 14pt), stroke: 1pt + ink))
  place(polygon(fill: ink, (-3pt, 13pt), (3pt, 13pt), (0pt, 20pt)))
  place(dx: 7pt, dy: 4pt, text(size: 7.6pt, weight: 700, tracking: 0.14em, label))
}))
#let endbox(body) = block(width: 100%, inset: (right: 6pt), {
  block(width: 100%, stroke: 0.8pt + ink, inset: (left: 7pt, right: 10pt, top: 6pt, bottom: 9pt), body)
  place(bottom + right, dx: 6pt, dy: 6pt, ends)
})
#let rung(n, q, act) = grid(columns: (20pt, 128pt, 36pt, 1fr), column-gutter: 3pt, align: horizon,
  num(n), plaque(q), harrow[YES], endbox(act))
#let aside-head(t) = block(above: 0pt, below: 5pt, sticky: true, {
  text(font: goth, weight: 600, size: 16pt, t); v(-3pt); brush(weight: 1.8pt, seed: 2)
})
#let mini(n, body) = grid(columns: (15pt, 1fr), column-gutter: 5pt, align: top,
  shield(w: 13pt, body: text(weight: 700, size: 7.4pt, fill: paper, str(n))), body)

// ---------- sheet ----------
#iron-band(9, "2", "Monster AI", "§ 9.5 · § 3.4 · C.8")
#v(7pt)
#align(center, block(width: 78%, text(font: fell, size: 11pt, fill: ink2)[Monsters must act neutrally, quickly, and reproducibly.]))
#v(6pt)

#grid(columns: (338pt, 1fr), column-gutter: 16pt,
[
  #block(spacing: 0pt, inset: (left: 23pt), proc(w: 300pt)[
    #text(weight: 700, size: 10.5pt)[When a Monster activates] \
    Determine the *Primary Target*, applying any printed *Target Priority* first. Resolve start-of-activation Special Abilities. Monsters spend no AP.])
  #varrow[THEN]
  #rung(1, [Has an AI Step whose trigger is met?], [Resolve the *first valid* AI Step, in ascending order. *on d6 N+*: roll 1d6, need N or higher.])
  #varrow[NO]
  #rung(2, [Engaged?], [Attack the Engaged enemy; if several, the one with the *lowest current HP*. Use Multi-Attack if listed.])
  #varrow[NO]
  #rung(3, [Any visible enemy?], [Move toward the Primary Target; attack if Engaged on arrival. *Ranged:* move to the nearest legal firing position and attack.])
  #varrow[NO]
  #rung(4, [Hidden enemy within 12″ and LOS?], [*Search:* the nearest one's controller makes a DEX Check. On a failure, that enemy loses Hidden.])
  #varrow[NO]
  #grid(columns: (20pt, 1fr), column-gutter: 3pt, align: horizon, num(5),
    endbox[*No visible target:* move toward the Guard Point, objective, patrol route or scenario destination.])
  #v(10pt)
  #panel("Rules Note")[The first valid instruction ends the activation unless a rule says the Monster continues. Re-determine the Primary Target if they cease to be legal.]
],
[
  #aside-head[Primary Target]
  The *nearest visible enemy*: within 12″ perception and LOS. Hidden and Invisible enemies are not visible unless a rule says so.
  #v(5pt)
  #text(weight: 700, size: 8.6pt, tracking: 0.12em)[TIES, IN ORDER]
  #v(2pt)
  #mini(1)[Lowest current HP]
  #mini(2)[Most recent attacker (last to damage this Monster)]
  #mini(3)[Random Determination]
  #v(12pt)
  #aside-head[Movement]
  #mini(1)[Shortest legal route]
  #mini(2)[Among equal routes, avoid Dangerous Terrain and hazards]
  #mini(3)[End in the nearest legal position to attack or threaten the target]
  #v(12pt)
  #aside-head[Blocked Route]
  Cannot reach and attack the Primary Target this activation? Switch to the nearest visible enemy it *can* reach and attack. If none, move full Speed toward the Primary Target and do not attack.
  #v(12pt)
  #aside-head[Never]
  No AP, Reactions, NRG or Checks. A Monster automatically succeeds on every Terrain Check.
]
)

// ink vignette at a boundary: lower right, may reach the trim
#place(bottom + right, dx: M - 10pt, dy: -2pt, image("/assets/art/ink/ART-MON-MINOTAUR.png", width: 178pt))

// footer
#place(bottom + left, dy: 14pt, block(width: 100%, {
  block(spacing: 0pt, line(length: 100%, stroke: 1.4pt + ink)); v(2pt); block(spacing: 0pt, line(length: 100%, stroke: 0.4pt + ink))
  v(5pt)
  grid(columns: (auto, 1fr, auto), column-gutter: 6pt, align: horizon,
    signature(s: 13pt),
    text(size: 9pt, weight: 600, tracking: 0.1em)[HERALDRY SKIRMISH · THE DYING LANDS],
    text(size: 9pt, fill: ink3)[Rules RC512 · front · SPECIMEN])
}))
