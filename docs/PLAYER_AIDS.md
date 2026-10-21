# Player aids: design and art direction

Status: direction proposed 2026-10-21 and Route A chosen the same day (section 10). All ten sheets, PA-1 to PA-10, were composed on 2026-10-21 from RC513 (section 12). Their wording was checked against the source by the author, not yet by an independent review. Built PDFs are not committed. Physical print is **NOT TESTED**.

The player aids are a companion series of printable reference sheets for the table. They are not part of the manuscript, and they do not advance the RC number. Adding them, or a pointer to them, inside the book's appendices is a manuscript change that needs its own owner decision.

## 1. The idea: field orders of a fallen realm

Each sheet should look like an order posted in a war camp by the herald of a broken kingdom. It carries an iron header band, the realm's arms, numbered steps on engraved shields, and one ink drawing of the threat it describes. The mood comes from black ink, blackletter and heraldry. Clarity comes from modern information design: one diagram language, one type system and generous space.

The sheets are the book's design system turned outward, not a new style. A player should recognise a sheet as Heraldry from across the table, and find the answer on it within five seconds.

## 2. Inherit, do not invent

Everything below comes from the book's "Grim Heraldry" system (`docs/BOOK_DESIGN_PLAN.md`, `config/design_tokens.json`, `typst/templates/system.typ`). Where this document is silent, the book's rules apply.

- **Marks:** the owner-approved armoury only (BOOK_DESIGN_PLAN section 12): chapter arms, the broken-castle logo, the engraved shield, the brush rule, the banner tag, the corner flourish, the lozenge and the coin. No new emblems, skulls, occult glyphs or clip-art icons.
- **Type:** the book's four families. Grenze Gotisch for titles and panel heads only, never in all capitals and never for running text or numbers. Source Sans 3 for all diagram text, labels and numbers. Source Serif 4 for any longer rules note. No flavour face: the sheets carry no flavour or editorial lines (owner, 2026-10-21).
- **Ink:** black only, with the book's transparent tints: 5% for panels and decision fills, 9% for die columns, 24% for hairlines, 42% and 58% for quiet labels. Colour never carries meaning, so every sheet must read when photocopied in greyscale.
- **Paper:** cream `#FCFAF5` and a white companion, identical in layout.
- **Not used:** parchment texture, stains, burned edges, gradients, drop shadows, glows, coloured highlights, or icons that need a legend.

## 3. Sheet anatomy

US Letter portrait, 612 × 792 pt. The sheets are unbound, so the margins are symmetric.

| Zone | Specification |
|---|---|
| Margins | 36 pt (0.5 in) top and sides; 64 pt at the foot, which holds the footer. Essential content, footer text included, stays at least 27 pt (0.375 in) inside the trim (measured: 30.6 pt). Only art and decoration may reach the edge |
| Iron header band | Full frame width, about 48 pt tall, solid black. Left: the chapter's arms at 34 pt. Centre-left: the sheet title in Grenze Gotisch SemiBold 30 pt, reversed. Right: "PLAYER AID n" and the § references in Source Sans 3 Bold 9 pt, tracked, reversed. Under the band: a 1.5 pt gap, then a 0.6 pt rule (the book's thick-and-thin) |
| Body | Two zones. The main diagram takes about 62% of the width on the left. Reference panels (tie-breakers, priorities, short tables) take the right column. A sheet whose subject is one table uses the full width |
| Art | One approved ink vignette per side at most, at a boundary (lower or upper outer corner), standing on the footer rule or bleeding off the outer edge. No more than about 18% of the page area. Never behind or under text |
| Footer | In the bottom margin, its text 30 pt from the trim: a thick-and-thin rule (1.6 pt, 2 pt gap, 0.4 pt). Left: the castle logo at 13 pt and "HERALDRY SKIRMISH · THE DYING LANDS". Right: "Rules RC<n> · front/back" in 42% grey |

Each sheet is double-sided where it needs to be. The front carries the procedure players reach for most. The back carries the supporting lookups (for example wake-up triggers and Group order behind the Monster AI script). A one-sided sheet leaves its back blank rather than padding it.

## 4. Type scale

| Role | Face and size |
|---|---|
| Sheet title | Grenze Gotisch Bold 38 pt, reversed in the iron band, beside the arms at 40 pt |
| Panel heading | Grenze Gotisch Bold 18 pt with a 2.4 pt brush rule beneath |
| Decision text | Source Sans 3 ExtraBold 11.5 pt, centred |
| Step and panel text | Source Sans 3 10.5 pt, key terms in Bold |
| Small caps labels (YES, NO, THEN, TIES IN ORDER) | Source Sans 3 Bold 7.6 to 8.6 pt, tracked +0.12 to +0.16 em. These are wayfinding labels, not essential text |
| Rules note | Source Sans 3 or Source Serif 4, at least 9.5 pt, in the book's tinted panel with the RULES NOTE banner tag |
| Minimum for essential text | 9 pt, as in the book |

No hyphenation anywhere on a sheet. Text is set ragged right. Never shrink type to fit; move content to the back or split the sheet.

## 5. Diagram grammar

One shape language across every sheet, so a player learns it once. Every distinction is made by shape and line, never by colour.

| Meaning | Shape |
|---|---|
| Numbered step | A black engraved shield carrying the step number (the book's procedure shield), at the left of the step |
| Action or process | A rectangle with a 0.8 pt black rule and no fill |
| Decision | A six-sided plaque (a lozenge drawn out sideways) with a 1.1 pt rule and 5% fill. Its question ends in "?" |
| Yes or a taken branch | A forged arrow to the right, about 62 pt long: a tapered shaft swelling from 2.6 to 5.8 pt into a barbed broadhead, with a black YES banner tag above it |
| No or fall-through | The same forged arrow pointing down, with a black NO banner tag beside it |
| Optional or conditional path | A short italic note inside the box it leaves ("Says it continues? Go to step 2."), or a dashed arrow where a drawn route is clearer |
| Ends (activation, step or phase) | A black banner tag reading ENDS, pinned to the lower-right corner of the box |
| Dice roll | A box with a double rule, the die named in a black cost tag ("d20", "1d6") |
| AP or Coin cost | A black cost tag ("1 AP"), and the coin mark for "c" |
| Rules note or exception | The book's panel: 5% tint, a 2.6 pt left rule and a RULES NOTE banner tag |
| Grouped lookup | A panel with corner flourishes (the book's dossier frame), at most one per side |
| Cross-reference | "§ 9.5" in Source Sans 3, 42% grey |

Flow runs top to bottom and left to right. The main spine stays in one column, with branches leaving to the right, so a finger can trace it. Arrowheads are solid triangles. Lines never cross. Shared geometry (zones, markers, terrain, dimension lines) reuses the figure glyphs explained by FIG-20, so the sheets and the book's diagrams agree.

## 6. Ink, tone and art

- **Ink style:** gritty old-school black-and-white ink, as in `docs/ART_DIRECTION.md`: bold brush contours, solid black shadow shapes, scratchy hatching and dry-brush, high contrast. No grey wash or stipple.
- **Art source:** approved illustrations only (`production/art/SELECTIONS.json` status `approved`, ink files in `assets/art/ink/`). The vignette shows the sheet's subject: the threat for Monster AI, a melee for combat, the war camp or road for the campaign, a town building for the Town Phase. No art is generated for the sheets without an owner instruction, and the paid image API is not used.
- **Black areas stay small and structural:** the header band, the step shields, tags and the art's own shadows. No large black panels. They waste inkjet ink and cockle the paper.
- **Ornament restraint:** at most two ornamental marks per side outside the header and footer (for example one corner-flourished panel and one brush-ruled heading group). Nothing ornamental inside a diagram box or a table cell.

## 7. The series

| Code | Sheet | Arms | Front | Back |
|---|---|---|---|---|
| PA-1 | The Round | 3 Round (hourglass) | The four phases as a loop around the arms; activating, eligibility, solo and co-op PvE Initiative | Actions table, Checks, Advantage, timing and simultaneous effects, Luck |
| PA-2 | Monster AI | 9 Monsters (wyvern) | The Standard Monster AI Script as a flowchart; Primary Target, ties, movement, Blocked Route, Never | The Monster Phase, wake-up triggers, setup and Guard Points, allegiance, Bosses, areas, AP changes |
| PA-3 | Combat | 5 Combat (axe and sword) | The attack sequence; the dice, Critical riders, Mitigation Order | Reactions table; reacting, damage and AV, attacks, attack modifiers |
| PA-4 | The Fallen | 6 Party (tattered banner) | 0 HP to Wounds, death or the Injuries Roll, as a flow; hit while down, Knocked Out, others at 0 HP, death marker | The Injuries Table (d20); the Chapel's healing |
| PA-5 | Conditions | 14 Reference (open book) | Stacking, recovery immunity, conditions A to I | Conditions K to Z, Heard the Song, negative conditions |
| PA-6 | Movement | 4 Actions (arrows) | Movement types; moving, costs, Climb, Jump and Falling | Engagement and Reach, Reflex Attack, sizes, forced movement, Push and Trip |
| PA-7 | Sight and Ground | 2 Mechanics (die) | LOS, concealment, Cover, Hidden, light and darkness | Terrain types and tags, elevation, areas of effect |
| PA-8 | The Campaign | 11 Campaign (pavilion) | The campaign cycle as a loop; start-of-adventure order, Monster CV, the Three Fates, Triumph, limits | The Expedition Event Table, Journey Home, keeping a record |
| PA-9 | The Town | 11 Campaign | Town Phase checklist; the Grand Hall, the Chapel, the Arcane Spire | The Training Grounds, the Ironworks, the Guild of Keys, Hirelings, Stronghold costs |
| PA-10 | Setup | 10 Scenarios (ruined arch) | The twelve preparation steps, Setup Roll-off, Random Direction compass | Climate and Core Scenario roll table |

Later sheets (Journey tables by Climate, Weather, hero creation and advancement, trackers and record sheets) use the same anatomy. A record sheet uses the book's heavy-box form.

## 8. Words

- Wording is the most concise reading that keeps every meaning: every condition, exception, number and tie-break survives, but connective prose does not.
- Every word on a sheet comes from the current manuscript, resolved through `source/versions.json`. Wording may be abridged and reordered, but never reinterpreted, and no rule, number, exception or condition may be added or dropped.
- Each sheet keeps a fidelity record: the sections it draws on, the manuscript RC and the sha256 of each section's text. A new RC that changes one of those sections marks the sheet stale until it is reviewed again.
- Every sheet passes a semantic review against its sections before release, as for the book's figures. A hash is never a substitute for that review.
- Capitalised game terms keep the manuscript's capitalisation. Canadian spelling, as in the manuscript.

## 9. Print

- Borderless US Letter, actual size, as in `docs/INKJET_PRINT.md`. A sheet must survive a non-borderless printer: nothing essential sits in the outer 27 pt.
- Recommended stock: matte card (65 to 110 lb cover) or heavy matte paper. Sheet protectors with a dry-erase marker suit the trackers.
- Every sheet is checked as a greyscale print and at 1.03 overscan, like the book.

## 10. Production route

Owner decision 2026-10-21, after the trial below: "Canva was inferior. Let's keep the design here within our workflow." The sheets are made with Route A. Route B stays documented only as the record of the trial.

The direction is the same on either route. The difference is how faithfully and cheaply it can be reproduced.

**Route A, the book's Typst kit (recommended).** The sheets are composed from the components in `system.typ`, with the exact approved marks, the seeded brush rule and the bundled fonts. The text can be bound to the manuscript and its hashes, and every sheet rebuilds when the rules change. The specimen in section 12 was made this way. The PDFs can still be imported into Canva for light editing or sharing.

**Route B, Canva.** Canva is a comfortable editing surface, but it cannot read the repository or check text against the manuscript. Before the first sheet:

1. Export an asset kit: the arms, logo and coin SVGs from `typst/templates/marks/cream/` and `white/`, plus SVG renders of the brush rule, engraved shields 1 to 12, the six-sided plaque, the ENDS and RULES NOTE tags, arrowheads and corner flourishes. The brush rule and shields exist only as Typst code today.
2. Load the four font families. All are OFL; uploading custom fonts to Canva needs a paid Canva plan.
3. Build one master Letter template with guides at 27 pt (safe) and 36 pt (margin), the header band, footer and colour swatches: `#000000`, `#FCFAF5`, `#FFFFFF`, with tints made as black at 5%, 9%, 24%, 42% and 58% opacity.
4. Lock the master and duplicate it for each sheet. Do not use Canva's generated layouts, generated images or stock graphics, because they would break both the style and the art rules.
5. Export "PDF Print" at Letter size. Keep the wording ledger (section 8) outside Canva, and re-check every sheet by hand after a rules revision.

The Canva account currently shows one brand kit; whether it is the Heraldry kit has not been checked.

### Route trial, 2026-10-21

The owner asked to try both routes on PA-2 Monster AI (front) and compare. Both used the same approved Minotaur ink, the Monsters arms, the logo and the same abridged wording. The Canva design is "Monster AI player aid flyer" in the owner's Canva account, generated by Canva from a written brief and then corrected through the connector.

- **Wording:** Canva's generator changed the supplied text in six places even though the brief said to use it exactly: "reproducibly" became "Reproducing"; "§" became "$"; "it can reach" became "to an reach"; "on arrival" became "or arrival"; and two punctuation changes altered how a step reads. All six were corrected by hand. Route A sets the text exactly as written.
- **Art:** Canva added its own AI-generated dragon in the art slot, which breaks the approved-art rule. It was replaced with the approved Minotaur. The page background is also a Canva image, not the flat cream.
- **Type:** Canva chose its own blackletter and sans and set almost all text bold. The connector cannot set a font family, so the book's four faces can only be applied by hand in the Canva editor, after uploading them (paid plan).
- **Shapes:** Canva drew every box, plaque, arrow and tag as a picture fill, so they cannot be restyled as one family. Two decision plaques let their text run into the plaque's edge. Route A draws them as vectors from shared components.
- **Feel:** Canva's larger, bolder type reads from farther away. Route A is closer to the book and fits more on the side.

## 11. Acceptance checklist (every side)

- The iron band, title, arms, § references, footer and RC stamp are present and placed as in section 3.
- Every shape follows the grammar in section 5; no colour, no new symbol.
- Nothing essential lies within 27 pt of the trim; type is at least 9 pt for essential text; nothing is hyphenated.
- The flow can be traced with a finger without a crossing line.
- At most one vignette, approved, not behind text, about 18% of the area or less.
- The wording matches the manuscript sections in the fidelity record, reviewed against the current RC.
- It reads correctly as a greyscale print and as a cream and a white print.

## 12. The sheets

Each sheet is `typst/aids/paNN.typ`, built on the shared kit `typst/aids/kit.typ`. The rules RC printed in each footer is read from `source/versions.json`.

- Render: `python tools/render_aids.py --paper both [--png]` writes each sheet and a combined 20-page set for cream and white paper to `build/aids/`, and fails any sheet that is not exactly two pages. Outputs are never committed.
- Fidelity: `python tools/aids_fidelity.py` compares each sheet's source sections with those recorded in `production/aids/fidelity.json` and lists the stale sheets after a manuscript revision. After re-reviewing a sheet's wording, run `record` with an honest `--reviewer` note. A hash only shows what was reviewed; it is not a review.
- Art used (all approved inks): Minotaur, Fighter, Berserker, Ghoul, Night Hag, Ranger, Assassin, the Road, Hearthhold and Greenmark, at most one per side.
- Rulebook figures were tried and left out: below 504 pt wide their labels fall under the 9 pt minimum, and no side has room at full width.
- The true-scale area templates planned for PA-7 are not included: a 6″ cone does not fit beside the rules on one side. They would need a sheet of their own.
