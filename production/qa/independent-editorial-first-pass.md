# RC492 bounded editorial source proof

Date: 2026-10-15. Reviewer: Codex, a fresh delegated review context in the same OpenAI model family as the integrating agent. This is a second source-review pass, not an independent human copyedit, a full-book certification, or a full-detail proof of the delivered PDF.

Disposition update, 2026-10-15: **ALL TEN CORRECTIONS APPROVED AND APPLIED IN RC493** under the owner instruction "Approve all as proposed." The original bounded review below concerns RC492; its coverage does not become a complete RC493 proof. The exact approved evidence is `editorial/history/RC493.json`; reconstruction and unchanged prior files are verified in `production/qa/rc493-editorial-verification.json`. No PDF was built or reviewed. Physical proof: **NOT TESTED**.

## Source and scope

- Reviewed source baseline: `source/Heraldry_RC492.md`, confirmed by the registry at review time; current authority is RC493.
- SHA-256: `a5ca7e72ad05a0cd69bb0bdca8238c10a635cf18345ae719c047c42fd3a8552a`.
- Checkout when review began: clean `main`, commit `1a890818694fd03f6f2d44e6508e787b6879280c`, matching local `origin/main`.
- Governing files read: `AGENTS.md`, `CLAUDE.md`, `production/STATE.md`, `docs/WORKFLOW.md`, and `docs/BUILD_AUTOMATION.md`. Append-only historical state entries do not replace the active registry or current source.

The following complete named sections were read in source, rather than reviewed only through search hits:

| Section | Source lines, inclusive |
| --- | --- |
| 1.1 What is Heraldry Skirmish?, including reading routes | 165-188 |
| 4.5 Reactions and 4.6 Illegal Actions | 1418-1449 |
| Combat opening and 5.1-5.5, including the complete Attack Sequence, mitigation rules, and Reactions | 1450-1688 |
| 8.2 Casting Powers, including the Universal Casting Sequence, defaults, and backlash tables | 5225-5418 |
| 9.1 Monster Stat Profile | 7513-7544 |
| 9.5 Universal Monster AI Principles, including all seven labelled subsections | 7592-7673 |
| 10.5 Solo and Cooperative Play, all subsections | 14649-14806 |
| 11.2.4 Phase 4: Town Phase, all locations | 15405-15480 |
| Appendix A, A.1-A.12, including both worked rounds | 16070-16506 |
| Appendix B opening, B.1-B.3 | 16507-16574 |
| C.12 Play Examples and C.13 Single-Sheet Rules Summary | 17779-17953 |

This is **1,517 lines** of defined coverage. Additional targeted checks read 2.7.3 (698-747), the equipment header and relevant weapon rows (3598-3615), the Arcane Bolt cost/range entry (5480-5483), and the Advanced Ogre rule and surrounding variant instructions (17096-17123). These targeted checks do not establish complete coverage of their parent chapters.

Method: contextual source reading; comparison of teaching/reference text to the current main rule; arithmetic inspection using only the example's existing printed rolls; exact proposed-match checks; and a scoped typography/pronoun search. No playtest was run and no new dice result is claimed.

## Findings and proposed corrections

Severity describes the observed source issue within this scope. It is not a new release-gate result. All ten exact changes were subsequently owner-approved, promoted once through the revision engine, and archived in `editorial/history/RC493.json`. The proposed language below records the original recommendation and is superseded by that explicit approval; no further approval is required for this applied batch.

### E01 - Tutorial Dire Wolf instructions can resolve two attacks

**Priority: high. Owner decision required.** A.9, lines 16321-16328, is written as an ordered procedure. Step 1 tells an already Engaged Dire Wolf to attack. Step 3 then unconditionally tells it to move, and step 4 tells it to attack if it ends Engaged. Step 1 does not end the activation or direct the reader to skip later steps. The full AI script at 7628-7636 uses the first valid instruction; the tutorial's more specific procedure does not repeat that control flow.

The conservative proposed alignment is one Bite per activation, with Pack Tactics applied before base damage is rolled and Takedown checked after damage. **PUB-E01 replaces the original six-step block at 16323-16328 as one exact proposed replacement.** The initially Engaged branch selects its existing-priority target, skips movement, and joins the same single attack/rider sequence as the unengaged branch. It does not add a target priority, change the Bite profile, or alter the surrounding prohibition on Dire Wolf AP or Reactions. No NRG system, new dice, or rolled results are introduced.

Exact proposed replacement:

```markdown
1. If the Dire Wolf is **Engaged**, select an **Engaged** non-**Knocked Out** Hero as its target. If more than one **Engaged** Hero is legal, choose the Hero carrying the **Dispatch Satchel**, then the Hero with lower current **HP**, then use **Random Determination** among the tied Heroes. Skip steps 2–3 and proceed to step 4.
2. If the Dire Wolf is not **Engaged**, choose its **Primary Target** using the learn-to-play target priority below.
3. The Dire Wolf moves up to **8"** toward its **Primary Target** by the shortest legal route.
4. If the Dire Wolf is **Engaged** with a Hero, declare one **Bite** attack. Otherwise, end its activation.
5. Before rolling the **Bite** attack's base damage dice, apply **Pack Tactics** if at least one other Dire Wolf is within the attack's melee distance of the target. Resolve the **Bite** attack using the **Attack Sequence** in **5.2**.
6. If **Bite** deals damage, the target makes a **STR Check**. On a failure, the target becomes **Prone**. The Dire Wolf's activation then ends.
```

The owner decision is explicit: confirm that the tutorial uses one Bite per activation, with no movement when initially Engaged, and resolves that attack and its riders in the same timing order as the current main Attack Sequence. The proposal makes that conservative interpretation concrete; it is not an approved rule change.

Acceptance: trace the procedure with an initially Engaged Dire Wolf and with an unengaged Dire Wolf, with Pack Tactics eligible and ineligible, and with damaging and fully mitigated Bites. Each trace resolves at most one Bite. The Engaged branch skips only steps 2-3. The unengaged branch retains movement up to 8 inches by the shortest legal route. Determine Pack Tactics before rolling the Bite's base damage dice; the existing Bite profile supplies its dice and piercing damage. Resolve Takedown's STR Check and Prone result only when Bite deals damage, then end the activation. Preserve the satchel-carrier, HP, random, and existing Primary Target priorities. These are review acceptance cases, not claimed playtest or dice results.

### E02 - C.13 Monster AI reference omits Search

**Priority: medium. Main-rule alignment; owner review required.** C.13 lines 17932-17938 proceed from moving toward a visible Primary Target to moving toward a Guard Point. They omit the full script's Search instruction at 7633. A reader using the table reference can therefore skip a legal Search and move away instead.

Proposed exact correction: insert the full canonical Search instruction from 9.5 before the final destination instruction and renumber the latter. The draft copies the existing targeting, DEX Check, failure, and activation-end procedure. It does not grant Monsters a Check or a player-chosen search target.

Acceptance: with no visible enemy and a Hidden enemy within 12 inches and LOS, the reference leads to the controller's DEX Check and ends the Monster's activation, matching 9.5. With no legal Search, the destination instruction remains available.

### E03 - Main Parry example uses the wrong ability for a Shortsword

**Priority: medium. Example correction; owner review required.** The 5.5.3 example at 1675 adds DEX +1 to a mundane Shortsword Parry. The weapon row at 3609 lists Light and Parrying, not Finesse. The normal modifier under 5.1 and 5.5.3 is therefore STR. C.12's Shortsword/STR example at 17791 is consistent and should be retained.

Changing only DEX +1 to STR +1 would introduce another problem: the Shortsword requires STR 2. The proposed exact example correction uses STR +2 and updates its total and Riposte from 9 to 10. It retains the printed base 6 and exploding 2. This is an illustrative-profile decision, so it remains a proposal.

Acceptance: 6 + 2 + 2 = 10; the Guard meets the Shortsword's STR requirement, the Parry succeeds against 7 incoming damage, and the Riposte is 10 before normal AV. No equipment trait is changed.

### E04 - Block example teaches a late declaration

**Priority: medium. Teaching timing; owner review required.** A.8's Block example at 16309 narrates the Bite damage and automatic armour roll before Edric spends AP to Block. Both the main Attack Sequence (1516) and A.8's sequence (16280) place the defender's modifying Reaction declaration before damage is rolled. The current narration can teach the reader to choose Block after seeing damage and armour.

The proposed exact replacement declares and pays for Block before the printed Bite damage, then resolves the same armour and shield dice. Its existing 7 damage, armour 5, shield 3, total AV 8, and 0 final damage are unchanged.

Acceptance: declaration precedes damage generation; mitigation still resolves after the final damage roll. Compare the revised example to 5.2 and A.8, rather than changing those main procedures to accommodate the example.

### E05 - Mara's Reaction comparison uses an unavailable option

**Priority: low. Teaching copy correction.** At 16455, Mara chooses Reflex Attack, and the example says Mara cannot also Block the shot because of the one-Reaction limit. Mara's fixed profile at 16131-16139 has no shield, so Block was unavailable regardless of that limit. Dodge is the legal alternative that demonstrates the intended choice.

Proposed exact correction: `Mara cannot also **Block** the shot.` becomes `Mara cannot also **Dodge** the shot.` All actions, AP, dice, damage, and state totals remain unchanged.

Acceptance: both compared Reactions are otherwise available to Mara against that ranged attack; the chosen Reflex Attack still uses the single response permitted by 4.5.

### E06 - Combatant pronouns and a definition need contextual copyediting

**Priority: low. Meaning-preserving copy corrections.** Line 187 defines a Summon as a combatant `that their creating rule identifies`. The grammatical correction is `that its creating rule identifies`. Other clear singular combatant uses occur at 1456 and throughout the Monster AI script, including 7628 and 7631-7634. These conflict with the supplied it/its/itself style instruction.

The draft contains bounded exact repairs for the definition, the Engaged definition, and the AI introductory paragraph as reviewable examples. It does **not** perform a blanket replacement or claim complete pronoun correction. The scoped search found 135 candidate lines containing they/their/them/themselves; these are not 135 confirmed defects. Human players, multiple Monsters, and plural combatants can legitimately use those words. For example, Marta at 14686 and Elspeth at 17783 refer to human players and should not be changed on this basis.

Acceptance: inspect each antecedent and agreement; preserve plural and human uses. A subsequent approved copyedit must check the rest of the manuscript separately.

### E07 - Basic Mode component list omits the Ogre variant's extra markers

**Priority: low. Reference completeness.** B.3 lists the optional Ogre model at 16553 but only 3 Satchels and 3 Monster Entry markers at 16555-16556. B.1 already notes the fourth Satchel, and Advanced Ogre at 17102 requires both a fourth entry marker and a fourth Satchel.

Proposed exact correction: append `or **4** for the **Advanced Ogre** variant` to both component-list items. This repeats an existing requirement; it does not add a new marker or change the variant.

Acceptance: the materials list supplies every marker required by Advanced Ogre, while default setup still uses 3 of each.

## Other checked observations

- Existing reading routes distinguish tutorial, Basic Mode, standard play, campaign, and lookup. The scoped reading does not support adding another general introduction before reader tests.
- The printed AP/HP arithmetic in A.11 was checked against its stated rolls and resource ledger; no additional arithmetic correction was found. Physical routes, base placement, and LOS in that example were not independently reconstructed on a board or diagram.
- The Arcane Bolt cost and its critical-cast example agree on 2 AP and 1 NRG. No change is proposed there.
- Scoped typography scanning found no smart quotes, em dashes, typographic ellipses, non-breaking spaces, section signs, or prime measurement marks. The detected en dashes were numeric ranges. This does not certify the remaining source or PDF glyphs.
- Current canon was preserved. Live source uses 4 TAP and Druidic Rituals. It also uses automatic Chest AD rather than Brace and states Monsters never make Checks; Monster AI tie-breaks use lowest HP, Most Recent Attacker, then random. These differ from the supplied standing brief. A separate authority trace is required; this report does not normalize either source or brief.
- C.13's generic non-area shared-damage reminder must be read with 8.2's more specific Power target default. No new roll rule is proposed in this pass.

## Next editorial stage and acceptance

1. Completed: the owner approved all ten replacements and the one-Bite tutorial interpretation. The revision engine created RC493 once, with the original RC492 hash, actual authorisation, and exact patch archive retained. Prior snapshots remain unchanged.
2. Commission or arrange a complete human copyedit against the authoritative current source, using an agreed terminology/style sheet and an issue log. This pass is supporting evidence, not completion of that task. No person was contacted.
3. After a separately requested publication build, proof the actual delivered PDF at readable detail: all pages, tables, captions, running matter, cross-references, links/bookmarks, final line breaks, and glyphs. Review altered examples and all affected downstream pagination. A source pass cannot approve those surfaces.
4. Run reader tasks without designer assistance and record observed rule-lookup errors, including Reaction timing, an already Engaged tutorial wolf, and Monster Search. No user-test result is claimed here.
5. Examine actual printed sheets and binding before replacing NOT TESTED with a physical-proof result.

The approved batch is applied in RC493. This source review and approval do not supersede the hash-bound visual record for the released RC492 PDF or complete the remaining human, final-format, accessibility, or physical checks.
