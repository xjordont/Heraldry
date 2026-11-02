# Hero sheet research and redesign audit

**Current direction:** Keep the consistent expanded, two-sided format, and finish the blank record before adapting Basic Mode Heroes. The latest blank uses the main book's type, signature, shields, lozenges, and brush rules with open writing fields. It removes grey inner cells, nested frames, redundant ancestry/background rules, reminders, the advancement lookup, and the Party Leader checkbox. Equipment and carried possessions share one Inventory. The preceding framed Basic Mode design remains unchanged pending the blank's refinement. See `docs/HERO_SHEETS.md` for current outputs; earlier implementation results below are historical evidence, not owner approval.

Owner request, 2026-10-22: scrutinize the existing Hero sheets, research comparable games before further design, and improve their beauty, readability, density, and organization within one US Letter sheet per Hero, preferably one side. Active rules authority: RC513. This is a graphic and information design pass, not permission to change rules.

## Evidence and method

Actual sheets were inspected as page images before redesign. PDF page numbers below are one-based viewer pages, not inferred printed folios. Private reference pages and their renders stay out of publication packages. The comparison is a design assessment by the author, not a player study.

| Source inspected | Actual sheet | Useful principle | Limit and Heraldry application |
| --- | --- | --- | --- |
| Mordheim, archived roster named Official Roster Sheet, Broheim, PDF pages 1 and 2 | Henchmen and Heroes; repeated compact profiles, black statistic headers, equipment, skills, injuries, and experience tracks | Repeat the same field order; keep a combatant's information together; concentrate illustration at the boundary | The archive's Heroes page explicitly credits Honza Skypala's modification to six Heroes. It is not an unmodified original Games Workshop master. Tiny tracking boxes and narrow stat columns are poor models for frequently erased resources. Adopt grouping, not its typography or art. |
| Lasting Tales, owner-supplied core PDF, pages 255, 258, 259, and 260 | Filled Hero example, filled spellcaster example, blank character record, and blank spellcaster record | Identity at top; characteristic rail; distinct maximum and current resources; weapons beside defence; substantial skills and inventory areas | The specialized spell page acknowledges real content capacity. Its coloured ribbons and textured substrate are not required for Heraldry. Adapt the hierarchy to black ink, a flat substrate, and canonical Heraldry attributes. |
| Five Leagues from the Borderlands, third edition, verified repository reference, pages 230 and 231 | Landscape campaign tracking and six-character warband roster | Separate party/campaign records from personal records; compact repeated fields; shared equipment recorded once | Six short profiles are not evidence that one rules-heavy Hero can fit at the same density. Use the landscape example to assess page shape and party scope, not to import its statistics or communal-resource mechanics. |
| Frostgrave, second edition, Osprey downloadable Wizard Sheet, pages 1, 2, and 3; owner-supplied book pages 216-218 | Wizard and apprentice; spells by school; repeated soldier profiles | Stable stat order; current Health next to Health; distinct sheets for different information types; minimal framing | Its Wizard Sheet is a three-page download, not a one-page all-information solution. Its large campaign boxes should not displace Heraldry's Hero-specific Powers and abilities. |
| Mythras Classic Fantasy Imperative, verified repository reference, pages 154-156 | Character, combat/equipment, and spell record | Numeric tables use aligned columns and restrained alternating rules; spells have parameters and description space | High field count produces very small visual targets. Do not copy its dense skill taxonomy, inventory limits, or tiny type. Adopt alignment and dedicated effect space. |

Deth Wizards pages 107-108 were also inspected. They are textured Notes pages, not character sheets, and provide no evidence for claims about its character-sheet design. TNA Ultimate's end matter was checked for relevant sheets; it was not used as a character-sheet authority.

Public sources: [Mordheim archived roster](https://broheim.net/downloads/resources/Official%20Roster%20Sheet.pdf), [Lasting Tales publisher](https://www.blacklistgamesllc.com/lastingtales), [Frostgrave second edition sheet](https://www.ospreypublishing.com/media/0pqjvqot/frostgrave_wizard_sheet-1.pdf). Local Five Leagues and Mythras originals are identified and hash-bound in `references/sample_pdfs.json`.

The [GOV.UK text-input guidance](https://design-system.service.gov.uk/components/text-input/) supports explicit, associated labels and appropriately sized inputs. [W3C contrast guidance](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum/) provides a useful 4.5:1 screen-text benchmark. Applying these principles to a pencil sheet is a design inference; neither source certifies this sheet or replaces player testing.

## Close audit of the existing draft

Baseline: `typst/heroes/parts.typ`, `hero.typ`, `sheet.typ`, and `cards.typ`, rendered from current RC513 data before modification. Blank front/back, Crowwick, and the longest profile, Mossgrave, were inspected. Baseline renders are retained locally under `build/hero-redesign/baseline/`.

1. **Hierarchy:** almost every panel has the same black ribbon, double border, notched corners, and four jewels. Armour, incidental inventory, and major resource tracking compete at the same visual weight. Reserve the strongest shapes for identity and primary statistics.
2. **Density:** the blank identity block is 140 pt high, before its surrounding title, gaps, scores, or resources. The blank portrait consumes 124 x 140 pt. Recover this area for Powers, talents, and equipment.
3. **Redundant decoration:** 1.5 pt outer and 0.5 pt inner borders repeat around all panels. A 13 pt inter-panel band protects protruding ribbons. Use flush headings, shared rules, and a regular baseline instead.
4. **Score scanning:** four large shields and an unrelated Initiative roundel create a dispersed scan path. Retain a restrained heraldic accent while arranging the four attributes in one stable row.
5. **Changing values:** oversized double-ring maximums sit beside under-defined current-value space. Current HP, NRG, and Luck deserve explicit, bounded write-in areas; maximums can be smaller.
6. **AP:** a single roundel does not distinguish allowance from what is available now. Label the two values separately without changing the refresh rule.
7. **Abbreviations:** SPD and Sz are economical but can be expanded in headings when space permits; preserve source abbreviations in verbatim profiles. Initiative needs its INT + SPI cue.
8. **Armour:** separate Chest and Shield rows and their AD/AV labels are useful and must survive. Keep the shield restriction beside the armour, rather than implying that all listed armour values apply together.
9. **Weapons:** preserve hands, damage type, range, traits, and Primary/Off-Hand assignment. Do not reduce a weapon to a name and damage die to gain space.
10. **Equipment split:** equipped-slot records are on the reverse while weapon/armour and carried records are on the front. Bring equipped and carried records together on the compact sheet.
11. **Campaign versus combat:** the ten-column advancement reference dominates the reverse. It is a useful lookup aid, but not a changing Hero statistic. Keep an optional expanded sheet for its complete reference rather than requiring it on the compact operational record.
12. **Talents and Powers:** the blank front cannot record any. A one-side Hero record must expose both, with cost and effect space, not merely a list of names.
13. **Writing capacity:** the old blank front's carried panel has few useful lines despite the page's large dimensions. Measure usable rows and field widths; avoid judging blank area by appearance alone.
14. **Art currency:** the baseline generator selects approved class art. The owner has since selected all 24 V1 Hero portraits. Use the approved individual portrait, preserve its aspect ratio, and keep it away from rules and handwriting.
15. **Art proportion:** the large decorative arch adds another frame grammar. A modest open portrait can identify the Hero without taking a full column of rules space.
16. **Rule flow:** Mossgrave's back begins its second column mid-sentence. Prefer a deliberately structured front/back division for profiles that cannot fit one side; preserve sequence inside a continuing long entry.
17. **Notes:** the baseline Notes box can be little more than a line or two. Guarantee meaningful ruled space in a proposed layout rather than filling a residual sliver.
18. **Type:** blackletter works for the main identity and sparse major headings. Sans serif is clearer for numerical parameters, table labels, and repeated rules headings. Keep all essential text at least 9 pt.
19. **Ink:** cream is already flat and restrained, which should remain; use no faux parchment or additional background texture.
20. **Production:** the baseline enforces exactly two pages even where one might fit. Page count must follow measured content capacity, capped at two sides per Hero, with content auditing independent of page count.
21. **Semantic safety:** manuscript prose contains conventions newer than the imported brief. The redesign follows RC513, including current armour treatment and Druidic Rituals. It must not introduce Brace, outdated default TAP, or new conditions.
22. **Edge safety:** a previous minimum text inset of 28.3 pt leaves little headroom above the 27 pt minimum. Use a regular 32 pt working inset and verify actual text bounds, not just frame coordinates.

## Page-shape decision

US Letter portrait and landscape have equal area. With a 32 pt working inset, portrait offers 548 x 728 pt; landscape offers 728 x 548 pt. A two-column portrait rules region yields approximately 265 pt columns, while three landscape columns yield approximately 231 pt columns before additional furniture. Wider landscape tables benefit a roster; shorter landscape columns can create more continuations in long abilities. These are geometric comparisons, not claims of a tested landscape prototype.

Use portrait as the primary format because it supports the existing book identity, longer rules columns, and a narrow table footprint when four Heroes are in play. Do not rotate content merely to disguise excess page count. A one-page blank operational record can offer fewer writing rows than the expanded two-side reference; preserve both honestly.

## Implementation requirements

- One-sided blank sheet: identity, ancestry, background, class, level, archetype, Senses, casting score, HP per Level, Initiative, STR/DEX/INT/SPI, HP/current/maximum/temporary, NRG/current/maximum, Luck/current/maximum, AP, Speed, Size, Chest and Shield parameters, Wounds, injuries, weapons, equipped slots, carried items, coins, Powers, talents, special abilities, adventures, Permanent Special Items, and Fate.
- Keep the complete previous advancement reference as an expanded alternative. The compact sheet references progression rather than reproducing the ten-level gains and price table; this removes duplicate reference material, not a Hero rule.
- Pre-generated Heroes: attempt one side at a stable readable size. Use an intentional two-side layout where full text and writing room exceed capacity. Never truncate, summarize, or hide a profile rule to pass a page target.
- Use actual approved V1 portraits. No borrowed reference art or new generated illustration.
- Keep costs in their complete bracketed form, headings attached to content, and separate equipped state from ownership.
- Maintain exact extraction of all B.4 words, sub-items, values, and shared Basic Mode reminders. Check every rendered profile, including the densest Hero.
- Inspect all final pages, plus individual dense pages at readable resolution. Check typography, margin safety, font embedding, and source hashes.

## Verification limits

The final receipt records measured results and actual page observations after implementation. Compilation and text coverage do not establish independent semantic review, tagged-PDF accessibility, or handwriting comfort. The current task is a sheet redesign, not a full-book build or release.

## First implemented outcome - rejected by the owner

The redesigned blank operational record fits one portrait Letter side. Its optional expanded reverse retains the complete advancement lookup and increases the total capacity to 7 Powers and 15 abilities. The compact blank has 3 weapon rows, 4 Power rows, and 4 ability rows; those are finite writing capacities, not game limits.

At the final edge-safe geometry, 8 Basic Mode Heroes fit one side and 16 use two. All 24 retain every extracted B.4 rule, sub-item, value, and applicable sense reminder, plus the full shared Hands and Basic Mode 0 HP rules. Two-sided profiles always keep equipment and those shared rules on the front. The measured fit changes page count rather than shrinking text or cutting wording. All 24 now use the owner's approved V1 individual portraits.

The 48-page combined packs insert blank backs after the 8 compact Heroes. This prevents a new Hero from landing on the reverse of another Hero's sheet. Individually, the compact files contain one page without a blank back.

The redesigned PDFs passed Letter geometry, type-size, text-inset, font-embedding, searchable-text, and source-coverage checks. Minimum type is 9 pt; profile prose is 9.5 pt; the smallest actual glyph bounding-box inset is 28.65 pt. The 86 individual page images were inspected in eight contact sheets, with eight full-page detail inspections covering both blank sides, compact characters, long form rules, long weapon rules, and dense equipment. This is author review, not an independent review.

The permanent observation record is `production/qa/hero-sheet-design-review.json`; local exact-file evidence and all-page Poppler renders are under `build/hero-redesign/`. Reproduction directions are in [HERO_SHEETS.md](HERO_SHEETS.md).
