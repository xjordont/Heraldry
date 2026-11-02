# Humanizer review: proposed patches for RC528

**Not applied.** Three owner requests, 2026-11-02, in a Claude Code session: "humanizer manuscript"; "Use the humanize skill again to ensure nothing is missed that sounds like AI or would trigger AI detection software"; and "Before applying ensure none of the changes create grammar, spelling, or style errors. Also check to ensure the rewritten sections are as well written or better written overall than the text they are proposed to replace by the humanizer." The manuscript changes only through exact replacements the owner approves, promoted once through `tools/revise_manuscript.py` as one new RC. Nothing below has been applied, and no figure, aid, or PDF has been rebuilt.

Prepared 2026-11-02 against `source/Heraldry_RC527.md` (SHA-256 `d28f5ec8ef438b43d278ec59c8faf195204266606bcfad1cbd8258088f48ec55`, 18,552 lines). The 64 patches that survived the quality review are in the JSON twin `editorial/proposals/rc528-humanizer-review.json`, each with status `proposed`; the 76 withdrawn patches are kept there under `withdrawn` as a record and are never applied. Every remaining `find` occurs exactly once in RC527 and still exactly once when the batch is applied in order. No patch adds or removes a line, so block IDs and figure line citations do not move. No patch changes a number or a name; two add a bold game term the book already defines (LEARN-01 **AP**, SCEN-14 **Pressure Clock**). The full candidate passed `python tools/dev.py manuscript prepare` (READY FOR OWNER REVIEW; 83 of 83 content anchors resolve; no blocking finding).

## Quality review

The two humanizer passes produced 140 patches. Before anything is applied, each was checked for errors and for whether it reads at least as well as the text it replaces.

- **Mechanical checks.** Every proposed line was checked for American spellings, unbalanced bold or italic markers, doubled words, stray spaces, and lowercase after a full stop, and every word new to the manuscript was checked by hand. Nothing was found except one style point: the plural 'Fighters' appears nowhere else, because class entries are singular.
- **Author's review.** Each change was reread as a before-and-after pair for grammar, meaning, and quality.
- **Independent blind review.** A separate reviewer was given all 140 pairs (the whole current line and the whole proposed line) under shuffled keys, with the house style but without the patterns, notes, or reasons, and asked to rate each proposal better, equal, or worse as writing for this book, list every error, and say what meaning changed. It rated 14 better, 45 equal, and 81 worse.

The reviews agree on the main finding. Many humanizer edits merge short fragments or cut dry closing lines that are the book's deliberate voice ('Slow. Aware. Dangerous to touch.', 'Sorcery does not study. It bleeds.', 'One is an itch; a swarm is exsanguination.'). Those edits remove a pattern detectors look for, but they make the prose worse, and the owner's bar is that every rewrite reads at least as well as the original.

The rule applied:

1. A patch stays only if neither review rates it worse. 76 patches are withdrawn, including two the blind review rated equal that the author judged worse (LORE-20, PARTY-07), one that shares a paragraph with a better patch (MON-02), and one the final check advised against (MON-08).
2. Where the blind review offered a fix at least as good as the original and the author agreed, the fix replaces the patch (11 patches, marked 'Revised in the quality review' or 'Narrowed').
3. Every error either review flagged in a kept patch is corrected (4 patches, marked 'Corrected').
4. The 16 patches whose wording changed in steps 2 and 3 went back to the independent reviewer for a final check. None was worse than the original. It found one error, the plural 'Pressure Clocks' in SCEN-14 (10.5.7 assigns each scenario one), now singular, and advised keeping the current text for MON-08, which is withdrawn. Of the 15 that remain, 8 are better than the original and 7 equal. For POWER-03 and POWER-05 it noted that restoring 'a cold calculus' and 'pulse with an untamed vitality' would rate better still; those are two of the stock phrases this pass exists to remove, and the current versions meet the bar, so they stay as proposed.

Errors found and fixed in the kept patches: an ambiguous 'they' (POWER-03), a comma splitting a predicate (POWER-04), 'the wild' twice in one sentence (POWER-05), an undefined term where 10.5.7 defines the **Pressure Clock** (SCEN-14), two 'it's with different referents (MON-17), 'strikes ... strike back' (MON-20), and the plural 'Pressure Clocks' where each scenario has one (SCEN-14, found on the final check). The withdrawn patches included the errors the reviews found elsewhere: broken parallelism (LORE-06), a scope change in 'Either way' (LORE-21), a dropped comma (CAMP-03), and the plural class name (PARTY-15).

## AI detection

No edit can promise a particular score from AI-detection software. Detectors are unreliable on short and formulaic text and disagree with one another, and rules text is formulaic by design: rewording 'unless a rule says otherwise' to change the statistics would make the rules less precise. The quality review also means this batch keeps much of the book's stylized voice (fragments, paired closers, and contrasts that carry a fact), which a detector may weigh the same way it weighs generated text. That trade was made deliberately in favour of the writing. Residual counts in the italic lore:

| Pattern in the italic lore | RC527 | All 140 drafted patches | This batch |
| --- | --- | --- | --- |
| 'X is not Y. It is Z.' contrasts | 47 | 19 | 36 |
| 'not just', 'not merely', 'not only' | 1 | 0 | 0 |
| Sentences of three words or fewer | 50 | 19 | 43 |
| 'X given a body' or 'given a shape' | 6 | 2 | 4 |
| 'before the answer lands' or 'comes' | 2 | 1 | 1 |
| 'is their larder' or 'nursery' | 3 | 1 | 1 |
| 'the language of' | 1 | 0 | 1 |

## What the batch still changes

- **The Chapter 8 introduction** (POWER-01 to POWER-07), the one passage that reads as generated throughout: 'transcend the swing of a blade', 'pulse with a terrifying, untamed vitality', 'a terrible intimacy with corruption', and 'living conduits of the world's sickness' go, and every claim stays. The independent review rated four of these seven patches better than the original (POWER-01, POWER-04, POWER-06, and POWER-07) and the other three equal.
- **Stock phrasing in the rules prose:** 'This opening shows why Heraldry Skirmish is not merely a damage race' (LEARN-01), 'is not won only by defeating enemies' (LEARN-02), 'talent ecosystem' (PARTY-13), 'the battlefield itself becomes the enemy' (SCEN-14), 'It is a promise about how the Monster fights' (MON-17), and the item-effect sentences that open 'Additionally' or say 'functions as' (ITEM-07 to ITEM-11).
- **Contrasts and closers that deny nothing a reader believed:** 'The Town Phase is not peace', 'The Vault is not a treasury', 'The Monsters ... are not scattered obstacles', 'magic is not a gift', and the Smuggler, Courier, and Merchant backgrounds.
- **Phrases repeated across entries,** where varying one copy reads at least as well: 'X given a body' (three of eight), 'before the answer lands' (two of three), 'There are always more' (one of three), and 'their larder' and 'their nursery'.

## Counts

| Group | Kept | Withdrawn | Figures affected by kept patches |
| --- | --- | --- | --- |
| Section 1: the world | 11 | 18 | none |
| Section 6: parties, ancestries, backgrounds, and classes | 9 | 8 | FIG-75 |
| Section 7: treasure, item lore, and item wording | 8 | 7 | none |
| Section 8: Powers | 8 | 1 | none |
| Section 9: Monsters | 18 | 21 | none |
| Section 10: objectives, scenarios, and solo play | 4 | 10 | 41 (FIG-13 to FIG-56) |
| Section 11: campaign | 4 | 11 | none |
| Appendix A: Learn to Play | 2 | 0 | FIG-18 |
| **Total** | **64** | **76** | **43** |

63 patches are recommended and 1 optional (ITEM-04). Applied together, they shorten the book by about 221 words.

## Owner choices

1. **Approve everything except the 10.4 scenario patches** (61 patches). 58 of them affect no figure. LEARN-01 and LEARN-02 stale one figure review (FIG-18, which hashes all of Appendix A), and PARTY-08 stales one more (FIG-75, which hashes 6.9 Ancestries).
2. **Also approve the 10.4 scenario patches** (3 patches: SCEN-02, SCEN-09, SCEN-12). `tools/figure_dependencies.py` hashes the whole of **10.4 Core Scenario Outlines** for every scenario map and preparation figure, so any edit inside 10.4, however cosmetic, marks 41 figure reviews stale (FIG-13 to FIG-16 and FIG-20 to FIG-56). The re-review is a confirmation, but it has to be recorded before the next release. With only three small patches left in 10.4, leaving them out is reasonable.
3. **Optional patch.** ITEM-04 is a small merge the reviews rated equal.

## Dependency impact

- **Figures.** 2 figures (FIG-18, FIG-75) without the 10.4 patches, 43 with them.
- **Content anchors.** All 83 resolve on the full candidate; none needs a new prefix. The back cover's quoted facts are unchanged.
- **Player-aid sheets.** `tools/aids_fidelity.py` will report changed sections for pa02 (MON-13, MON-35); pa08 (CAMP-06, CAMP-13); pa09 (CAMP-06, CAMP-13); pa10 (SCEN-14). No sheet quotes the patched wording, so re-recording after a diff is a confirmation and the sheets do not need rebuilding.
- **Hero cards, back cover, How to Use, and cover lead.** Unaffected.
- **Art catalog.** `production/art/SPOT_CATALOG.json` and `production/art/ILLUSTRATION_LIST.md` quote the flavour text above each illustration, and 25 patches change quoted paragraphs. Regenerate both at promotion (`python tools/dev.py agent run art-catalog`, then `tools/art_list.py`). Approved art is unaffected.
- **Build.** Nothing was built. The last released PDFs (RC527-build-41) are unchanged.

## Withdrawn patches

Withdrawn because a review rated them worse than the original (the reason is the reviewer's, shortened), or for the reason given. Their find and replace text stays in the JSON twin under `withdrawn`.

| Patch | Where | Reason |
| --- | --- | --- |
| LORE-01 | 1.1, third paragraph | The paragraph now opens abruptly and the closing line loses its setup |
| LORE-02 | 1.2, second paragraph | The image and the closing 'They know... They know...' pair carry the voice |
| LORE-03 | 1.2, third paragraph | The three 'Some rise' sentences build to the closing image; the colon list with elided verbs is tidier but flatter |
| LORE-04 | 1.2, fourth paragraph | The 'waits there' litany is the rhythm of the passage; the merge is smooth but flatter |
| LORE-06 | 1.3.1, last paragraph | The three fragments 'Slow. Aware. Dangerous to touch.' are the point of the line |
| LORE-07 | 1.3.2, opening paragraph | Drops the opening thesis 'Beyond the walls, land has become allegiance.', which frames why survivors use older names |
| LORE-08 | 1.3.2, The Greenmark | The two-sentence turn is the dry closing line |
| LORE-09 | 1.3.2, closing paragraph | Drops 'These six are the world now.', the summary line that closes the climate survey. Calling the six 'climates' is consistent with the at-a-glance box |
| LORE-13 | 1.3.3, Saltspire | The separate 'It also makes it hated.' is the sting |
| LORE-14 | 1.3.4, Arcane Spells | The aphorism is the better line |
| LORE-17 | 1.3.6, third paragraph | The three fragments are the punchline. The same fragments recur verbatim later in the campaign chapter; vary that repeat instead, see CAMP-02 |
| PARTY-01 | 6, opening paragraph | Loses 'not the heroes sung about in warm halls', a strong image that sets up the rest of the paragraph |
| ITEM-01 | 7.17.3, The Hollow Crown | Changes the referent: CURRENT contrasts the crown with the tomb that has never been found, while PROPOSED says 'finding them' (the sovereign). It also turns the hedged 'the... |
| ITEM-03 | 7.17.3, The Three-Strike Staff | The three short declaratives are the payoff |
| ITEM-05 | 7.17.3, Karnessa's Binding | Loses the 'It is cold. It is always cold.' escalation |
| ITEM-06 | 7.17.3, The Bell's Tongue | The two separate 'It has always' sentences make the closing beat |
| POWER-09 | 8.5, Tier 1 Sorceries introduction | 'Is learned' implies study, the opposite of CURRENT's 'does not study'. It also breaks the echo of the Psion line ('do not study their power; they survive it') |
| MON-02 | 9, introduction | Shares its paragraph with MON-01; the independent review advised applying only one, so the paragraph keeps one contrast |
| MON-05 | 9.7, Swamp Goblin | Drops 'a nuisance one at a time'. 'Dangerous' is flatter than 'a hazard' |
| MON-06 | 9.7, Stirge | This is the strongest use of the one-versus-many formula; trim the others instead |
| MON-08 | 9.7, Skeleton Warrior | The final check found the revised 'Others stand ranked in the dark' weaker than 'There are always more' and advised keeping the current text, since MON-07 already removes one... |
| MON-10 | 9.7, Desert Naga | The two short sentences are the dry close; 'but' spells the irony out |
| MON-12 | 9.7, White Court Executioner | The merged version loses the turn, and 'only' becomes vaguer |
| MON-14 | 9.7, The Ancient Void Dragon | Loses 'neither burns nor freezes', the contrast with the fire and frost dragons |
| MON-15 | 9.7, Captain Veyr of the Forsaken | The fragment 'Only the oath.' is the closer |
| MON-16 | 9.7, The Antlered Warden of the Tithe | Loses 'does not come to bargain' (they do not negotiate) |
| SCEN-01 | 10.2, Ashlands Secondary Objectives, the Reliquary | Colon misuse: the colon makes 'one of Mordain Kest's bindings...' read as the explanation of the warmth, which it is not |
| SCEN-03 | 10.4, Greenmark Scenario 2, Scenario-Specific Monster: Antlered Warden | The triple 'They do not... They do not... They maintain' is the closing rhythm |
| SCEN-04 | 10.4, Ashlands Scenario 6, The Iron-Vein Vault | The fragment 'Until now.' is the hook |
| SCEN-05 | 10.4, Ashlands Scenario 6, The Iron-Vein Vault | Drops the closing 'The vault does not care about either contract.' |
| SCEN-06 | 10.4, Ashlands Scenario 5, The Reliquary of Broken Saints | Drops 'are not confused', the dry note that these dead guard on purpose |
| SCEN-07 | 10.4, Pale City Scenario 2, The Alchemist's Frozen Laboratory | Drops 'Some things in that laboratory were never meant to thaw.', the only hint that something there is dangerous |
| SCEN-08 | 10.4, Sun-Drowned Scenario 1, The Oasis Raiders | Drops the closing line that resolves the liberation/seizure pair |
| SCEN-10 | 10.4, Mire Scenario 1, Scenario-Specific Monster: Salttide's Shade | The three 'They watch' sentences build |
| CAMP-01 | 11, first paragraph | The fragments are the ledger rhythm |
| CAMP-03 | 11, seventh paragraph | The six-item colon list is heavy; the fragment litany reads better |
| CAMP-04 | 11.1, first lore paragraph | Drops 'not a castle in the noble sense' |
| CAMP-05 | 11.1, third lore paragraph | Drops 'That is not mercy. It is weight.' and 'more than adventurers with blades and debts'. 'Take on the weight of answering for' is wordier |
| CAMP-07 | 11.3, The Armoury | Drops 'does not look safe' (prepared is not the same as safe) |
| LORE-20 | 1.1, first paragraph | Rated equal by the independent review but worse by the author ('treasure and glory and hoping' is clumsier than the original) |
| LORE-21 | 1.1, fourth paragraph | Unclear reference: 'Either way' now points back to solo versus cooperative play, so competitive play drops out of the summary. 'With the constant risk' is loosely attached |
| LORE-22 | 1.2, first paragraph | The two parallel sentences make the closing antithesis |
| LORE-23 | 1.2, fifth paragraph | Drops 'feared' |
| LORE-24 | 1.2, last paragraph | 'Renewed one Skirmish at a time' (rolled over) becomes 'comes due again every Skirmish' (payment demanded), a different metaphor |
| LORE-26 | 1.3.4, Divine Prayers | The paired 'Both...' sentences are the closer |
| LORE-29 | 1.3.7, after the omens | Register clash: 'rule of play' is rules language inside italic lore; the sentence ends on its weakest phrase |
| PARTY-06 | 6, second paragraph | Shares its line with PARTY-02, the stronger edit of that line |
| PARTY-07 | 6.9, Dwarf | Rated equal by the independent review but worse by the author ('Hardship hardened' echoes) |
| PARTY-09 | 6.9, Drakeblood | Drops 'the old language of'; 'is fallen' (a state) becomes 'has fallen' (an event) |
| PARTY-11 | 6.10, Apprentice | Loses 'marks that never quite fade' |
| PARTY-15 | 6.13, Fighter | Breaks the house rule that class entries use the singular ('A Fighter ...'). It also breaks the series opener used across class entries ('A Fighter is forged', 'A Rogue is... |
| PARTY-16 | 6.13, Ranger | Style: breaks the parallel 'A [Class] is [participle]' opener used across the class entries |
| PARTY-17 | 6.13, Wizard | Style: breaks the parallel class-entry opener; the long second sentence repeats 'the Wizard' |
| ITEM-13 | 7.17.3, The Hollow Crown's Writ | Loses the dry 'less reassuringly' |
| ITEM-14 | 7.17.3, Kest's Iron Reliquary | The full stop after 'This one is warm.' is the beat before the reveal |
| ITEM-15 | 7.17.3, Ysolde Vane's Marginalia | The separate 'They are always in blood.' is the sting |
| MON-18 | 9.7, Monster Roles, Minion | Loses the 'tide' image |
| MON-19 | 9.7, Monster Roles, Soldier | Repetition: 'hold a line' echoes 'line-holder' in the same entry |
| MON-23 | 9.7, Monster Roles, Controller | Loses 'the weight of their arm' and 'the shape of the fight' |
| MON-27 | 9.7, Avatar of the Old Growth | Unclear pronoun: in 'a body it can act through', 'it' can be the will or the forest |
| MON-28 | 9.7, The Voice Beneath the Bells | Style: breaks the paired construction ('given a child's shape and a drowned chapel's patience') into an unbalanced 'in ..., with ...' |
| MON-29 | 9.7, Avatar of the Old Growth | The separate 'The Greenmark does not forgive.' is the closer |
| MON-30 | 9.7, Forsaken Knight | Drops 'Their honour has curdled into compulsion.' |
| MON-31 | 9.7, White Court Sentinel | Drops 'only' (they do nothing but endure) |
| MON-33 | 9.7, Tomb Guardian | The two sentences make the closing beat |
| MON-36 | 9.7, Lizardfolk Hunter | Drops the second-person closer 'By the time they move, you are already in the water.' |
| SCEN-11 | 10.4, Undermarches Scenario 2, The Chasm Crossing | Merges away the separate 'It does not ask what the things want.' |
| SCEN-13 | 10.4, Mire Scenario 5, Salttide's Reckoning | Drops the sensory detail 'The water smells of brine, this far from any sea.' |
| CAMP-08 | 11, fourth paragraph | Merges away the separate 'Clean things do not last long beyond the gates.' |
| CAMP-10 | 11.1, Triumph | The 'It means' anaphora and the closing pair 'That is enough to matter. It is not enough to last.' are the passage |
| CAMP-11 | 11.3, The Apothecary | The repeated 'leave' builds the line |
| CAMP-12 | 11.3, The Stronghold Chapel | Loses the 'Its... Its... Its...' triple |
| CAMP-14 | 11.3, The War Room | Folds the staccato close into a colon list |
| CAMP-15 | 11.3, The Undercroft | Merges the 'Each year' pair |
| MON-38 | 9.7, Green Dragon | Awkward usage: in 'prefer manipulation to rampage', 'rampage' reads oddly as an uncountable noun |
| MON-39 | 9.7, Possessed Corpse | 'They only reach' becomes 'the body only reaches'. This settles the referent but flattens the closer |

## Left alone

- **Procedural rules wording.** Repeated formulas such as 'unless a rule says otherwise' are deliberate rules language.
- **Headings and bold labels.** House style; they carry anchors, cross-references, and the index.
- **The book's lore voice.** Fragments, paired closers, anaphora, and contrasts that carry a fact, as the quality review found.
- **Repeated content.** The 1.3.6 climate list returns in the Chapter 11 introduction, and Chapter 8's tradition paragraphs repeat 1.3.4; that is a structure question, not a writing error.

## Findings

Kept patches only, grouped by section, in manuscript order. Line numbers refer to `source/Heraldry_RC527.md`. 'Current' is the whole line as it stands; 'Proposed' is that line with only this patch applied.

## Section 1: the world

### LORE-25: 1.3, The Dying Lands at a Glance

**§25 writing about the document. Recommended. Independent review: equal.** 'The sections below tell the story' describes the page; the pointer to the rules stays.

*Line 205, under "1.3 The Dying Lands".* Dependencies: none.

**Current**

> **The Dying Lands at a Glance.** One ruined continent, six climates: the overgrown **Greenmark**, the ash-choked **Ashlands**, the lightless **Undermarches**, the frozen **Pale City**, the sun-scorched **Sun-Drowned**, and **The Mire**, poisoned and drowning beneath its own waters. Six **Bastions** hold what remains of mortal civilization. Everything between them is contested ground, and adventurers are the few who are paid to cross it. The sections below tell the story. The rules begin at **1.4**.

**Proposed**

> **The Dying Lands at a Glance.** One ruined continent, six climates: the overgrown **Greenmark**, the ash-choked **Ashlands**, the lightless **Undermarches**, the frozen **Pale City**, the sun-scorched **Sun-Drowned**, and **The Mire**, poisoned and drowning beneath its own waters. Six **Bastions** hold what remains of mortal civilization. Everything between them is contested ground, and adventurers are the few who are paid to cross it. The rules begin at **1.4**.

### LORE-05: 1.3, third paragraph

**§1 contrast. Recommended. Independent review: equal.** The negative half denies a claim nobody made; the rest of the sentence already says the crowns and borders stopped being useful.

*Line 209, under "1.3 The Dying Lands".* Dependencies: none.

**Current**

> *The lands where Heraldry Skirmish is fought are not a kingdom. They are a continent in the oldest sense: a single body of land held together by mountains, rivers, roads, ruins, and grief long after its crowns and borders stopped being useful.*

**Proposed**

> *The lands where Heraldry Skirmish is fought are a continent in the oldest sense: a single body of land held together by mountains, rivers, roads, ruins, and grief long after its crowns and borders stopped being useful.*

### LORE-10: 1.3.3, fourth paragraph

**§7 repeated openings. Recommended. Independent review of the revised wording: equal.** Seven short sentences, four opening 'They', become three; every item stays. The closing 'No Bastion... No Bastion...' pair is kept as written. (Revised in the quality review: the first draft also merged that pair, which the independent review rated worse.)

*Line 267, under "1.3.3 The Six Bastions".* Dependencies: none.

**Current**

> *The Bastions themselves are not allies. They send envoys. They trade iron, salt, grain, oil, bodies, medicine, and lies. They exchange prisoners when it is useful. They accept refugees when plague at the gate would be worse than charity. Their treaties are thin things. Tired clerks write them. Hungry captains break them. No Bastion can afford open war with another. No Bastion trusts that fact to last.*

**Proposed**

> *The Bastions themselves are not allies. They send envoys and trade iron, salt, grain, oil, bodies, medicine, and lies. They exchange prisoners when it is useful and accept refugees when plague at the gate would be worse than charity. Their treaties are thin things, written by tired clerks and broken by hungry captains. No Bastion can afford open war with another. No Bastion trusts that fact to last.*

### LORE-11: 1.3.3, fifth paragraph

**§1 contrast. Recommended. Independent review of the revised wording: better.** Adds the 'but' the list needs. (Revised in the quality review: the first draft also rewrote 'The Bastions are not safe. They are safer.', which both reviews rated worse; that pair stays.)

*Line 269, under "1.3.3 The Six Bastions".* Dependencies: none.

**Current**

> *The Bastions are not safe. They are safer. Their walls keep out the worst of the dark, not hunger, fever, debt, politics, superstition, or the quiet passengers hidden among refugees and trade goods. Every gate has a price. Every chapel keeps lists. Every guild counts favours. Every watch-fire burns lower than the captains admit.*

**Proposed**

> *The Bastions are not safe. They are safer. Their walls keep out the worst of the dark, but not hunger, fever, debt, politics, superstition, or the quiet passengers hidden among refugees and trade goods. Every gate has a price. Every chapel keeps lists. Every guild counts favours. Every watch-fire burns lower than the captains admit.*

### LORE-12: 1.3.3, last paragraph before Greythorn

**§1 contrast. Recommended. Independent review: equal.** 'Part of the war' already says it is not peace.

*Line 275, under "1.3.3 The Six Bastions".* Dependencies: none.

**Current**

> *For most people, the Bastion is the end of the world made habitable by walls. For adventurers, it is where wounds are priced, contracts are stamped, dead companions are replaced, and the next mistake is made official. The **Town Phase** is not peace. It is the part of the war fought with ledgers, knives, prayers, and closed doors.*

**Proposed**

> *For most people, the Bastion is the end of the world made habitable by walls. For adventurers, it is where wounds are priced, contracts are stamped, dead companions are replaced, and the next mistake is made official. The **Town Phase** is the part of the war fought with ledgers, knives, prayers, and closed doors.*

### LORE-15: 1.3.5, opening paragraph

**§1 contrast. Recommended. Independent review: equal.** The negative half denies a claim nobody made. Chapter 9 opens with the same move (MON-01).

*Line 343, under "1.3.5 Monstrous Threats".* Dependencies: art catalog quote.

**Current**

> *The **Monsters** of the Dying Lands are not scattered obstacles. They hold the world now. They keep roads closed, fields empty, shrines silent, and old borders meaningless. A village may vanish because of hunger, tax, fever, or weather. Outside the walls, those causes often have claws, banners, laws, or names.*

**Proposed**

> *The **Monsters** of the Dying Lands hold the world now. They keep roads closed, fields empty, shrines silent, and old borders meaningless. A village may vanish because of hunger, tax, fever, or weather. Outside the walls, those causes often have claws, banners, laws, or names.*

### LORE-27: 1.3.5, Goblinoids

**§7 repeated openings. Recommended. Independent review of the revised wording: better.** Three 'Some' openings in a row; the third becomes 'A few'. (Narrowed in the quality review: the first draft also merged the first two sentences.)

*Line 347, under "1.3.5 Monstrous Threats".* Dependencies: none.

**Current**

> ***Goblinoids, kobolds, gnolls, and orcs** raid wherever they can find a foothold. Goblin clans and web-wrights haunt the Greenmark roads. Gnoll war-bands ride the Sun-Drowned surface under banners cured stiff by heat. Orcs test borderlands for weak gates, poor watch, and winter hunger. Kobolds vanish into drains, old mines, and foundation cracks. Some serve stolen banners from older kingdoms. Some serve nothing. Some Bandit Captains of the forest roads are no longer mortal enough for that title to comfort anyone.*

**Proposed**

> ***Goblinoids, kobolds, gnolls, and orcs** raid wherever they can find a foothold. Goblin clans and web-wrights haunt the Greenmark roads. Gnoll war-bands ride the Sun-Drowned surface under banners cured stiff by heat. Orcs test borderlands for weak gates, poor watch, and winter hunger. Kobolds vanish into drains, old mines, and foundation cracks. Some serve stolen banners from older kingdoms. Some serve nothing. A few Bandit Captains of the forest roads are no longer mortal enough for that title to comfort anyone.*

### LORE-16: 1.3.5, the old peoples

**§7 repeated openings. Recommended. Independent review: equal.** Four 'Some' sentences in a row; the three one-word ones merge.

*Line 351, under "1.3.5 Monstrous Threats".* Dependencies: none.

**Current**

> ***The old peoples and border powers** have not vanished. Were-creatures, satyr cohorts, dryad ambassadors, deep elves, nagas, necromancers, lizardfolk temple-guards, and stranger courts hold places the Bastions still mark as lost. Some bargain. Some tithe. Some raid. Some remember treaties humanity has forgotten and punish the breach with perfect sincerity. In the Sun-Drowned, the tomb-cities of the priest-kings are administered by **necromancers** who have outlasted their own deaths: judges, clerks, and tax-collectors preserved in linen, oil, and old authority. They do not acknowledge the Fall. They acknowledge overdue accounts.*

**Proposed**

> ***The old peoples and border powers** have not vanished. Were-creatures, satyr cohorts, dryad ambassadors, deep elves, nagas, necromancers, lizardfolk temple-guards, and stranger courts hold places the Bastions still mark as lost. Some bargain, some tithe, and some raid. Some remember treaties humanity has forgotten and punish the breach with perfect sincerity. In the Sun-Drowned, the tomb-cities of the priest-kings are administered by **necromancers** who have outlasted their own deaths: judges, clerks, and tax-collectors preserved in linen, oil, and old authority. They do not acknowledge the Fall. They acknowledge overdue accounts.*

### LORE-18: 1.3.6, last paragraph

**§2 fragments. Recommended. Independent review: equal.** Three fragments become the end of the sentence they illustrate.

*Line 375, under "1.3.6 Adventurers and the Road".* Dependencies: none.

**Current**

> *Those who survive begin to build something larger than a purse. A keep on a hill. A reclaimed manor. A forge, a chapel, a vault, and a wall thick enough to last one hard winter. Few parties live long enough to raise such a place. Fewer reach **Triumph**, the old Bastion word for planting a banner in ground that has stayed clean for a generation. Every party leaving the gate tells itself this is the road ahead. Most roads end before that.*

**Proposed**

> *Those who survive begin to build something larger than a purse: a keep on a hill or a reclaimed manor, with a forge, a chapel, a vault, and a wall thick enough to last one hard winter. Few parties live long enough to raise such a place. Fewer reach **Triumph**, the old Bastion word for planting a banner in ground that has stayed clean for a generation. Every party leaving the gate tells itself this is the road ahead. Most roads end before that.*

### LORE-28: 1.3.7, opening line

**§2 fragments. Recommended. Independent review: equal.** Two-beat closer joined.

*Line 379, under "1.3.7 Legends and Echoes".* Dependencies: art catalog quote.

**Current**

> *The Dying Lands remember. They do not remember kindly.*

**Proposed**

> *The Dying Lands remember, and not kindly.*

### LORE-19: 1.3.7, last paragraph

**§1 contrast. Recommended. Independent review: better.** Split 'does not need X. It needs only Y.' stated directly.

*Line 403, under "1.3.7 Legends and Echoes".* Dependencies: none.

**Current**

> *The lore of the Dying Lands provides names, scars, and old quarrels for expeditions, rival parties, patrons, **Monsters**, relics, and campaign goals. A scenario does not need to explain the whole world. It needs only enough history to make the blood on the ground feel older than the fight.*

**Proposed**

> *The lore of the Dying Lands provides names, scars, and old quarrels for expeditions, rival parties, patrons, **Monsters**, relics, and campaign goals. A scenario needs only enough history to make the blood on the ground feel older than the fight.*

## Section 6: parties, ancestries, backgrounds, and classes

### PARTY-02: 6, second paragraph

**§7 repeated openings. Recommended. Independent review: better.** Three parallel sentences become one.

*Line 2000, under "6. Your Adventuring Party".* Dependencies: none.

**Current**

> *A Bastion blesses these parties when it must. It pays them when it can. It denies them when the work turns shameful. Most **Expeditions** begin with a writ: a council mark, chapel order, guild contract, noble warrant, salvage-right, grave-tax exemption, or debt bond. The paper grants legal cause to enter forbidden ground and take what can be carried out. Rival parties may hold different writs for the same ruin. Each seal may be valid under some law, oath, or patronage. The Dying Lands do not care. A contract only matters if someone lives long enough to collect.*

**Proposed**

> *A Bastion blesses these parties when it must, pays them when it can, and denies them when the work turns shameful. Most **Expeditions** begin with a writ: a council mark, chapel order, guild contract, noble warrant, salvage-right, grave-tax exemption, or debt bond. The paper grants legal cause to enter forbidden ground and take what can be carried out. Rival parties may hold different writs for the same ruin. Each seal may be valid under some law, oath, or patronage. The Dying Lands do not care. A contract only matters if someone lives long enough to collect.*

### PARTY-08: 6.9, Deep Elf

**§7 repeated template. Recommended. Independent review: better.** 'They are X and Y, and far more/harder...' closes three ancestry entries (Halfling, Deep Elf, and the Gnome's near copy); this varies one.

*Line 2343, under "Deep Elf".* Dependencies: figures FIG-75; art catalog quote.

**Current**

> *Deep elves are a crueller branch of the elder blood, raised on night, venom, and treachery taught as a fine art. They are graceful and dangerous, and far more at ease beneath the dark than beneath the sun.*

**Proposed**

> *Deep elves are a crueller branch of the elder blood, raised on night, venom, and treachery taught as a fine art. Graceful and dangerous, they are more at home in the dark than under the sun.*

### PARTY-03: 6.10, Smuggler background

**§1 contrast. Recommended. Independent review: equal.** 'Not a flourish. It is...' denies a claim nobody made.

*Line 2454, under "Smuggler".* Dependencies: art catalog quote.

**Current**

> *A smuggler lives by false bottoms, whispered routes, and the craft of keeping valuable things out of dangerous hands. Stealth is not a flourish to them. It is the trade that buys supper.*

**Proposed**

> *A smuggler lives by false bottoms, whispered routes, and the craft of keeping valuable things out of dangerous hands. To them, stealth is the trade that buys supper.*

### PARTY-04: 6.10, Courier background

**§1 contrast. Recommended. Independent review: equal.** Same move as PARTY-03.

*Line 2462, under "Courier".* Dependencies: art catalog quote.

**Current**

> *A courier carried news, coin, or secrets across broken roads and worse weather, for patrons who paid for speed and asked no questions. Speed was never a convenience. It was the difference between arriving and being found later.*

**Proposed**

> *A courier carried news, coin, or secrets across broken roads and worse weather, for patrons who paid for speed and asked no questions. Speed was the difference between arriving and being found later.*

### PARTY-10: 6.10, Scholar

**§12 'matters', stock 'where others see'. Recommended. Independent review of the revised wording: better.** 'Lived among books, diagrams, and arguments, and the stubborn belief' yokes a belief to things one lives among. (Narrowed in the quality review: the second sentence stays as written.)

*Line 2494, under "Scholar".* Dependencies: art catalog quote.

**Current**

> *A scholar lived among books, diagrams, and arguments, and the stubborn belief that knowledge matters even in a dying world. Where others see only rubble, they read the record of how it came to fall.*

**Proposed**

> *A scholar lived among books, diagrams, and arguments, stubbornly sure that knowledge matters even in a dying world. Where others see only rubble, they read the record of how it came to fall.*

### PARTY-12: 6.10, Believer

**§7 repeated template. Recommended. Independent review: equal.** Ten of the twenty background entries turn on 'learned' or 'taught'; this varies one where the sentence allows it.

*Line 2518, under "Believer".* Dependencies: art catalog quote.

**Current**

> *A believer kept faith in a world that rewards it rarely, and learned that courage spreads as readily as panic. People stand straighter when they believe something is still watching from above.*

**Proposed**

> *A believer kept faith in a world that rewards it rarely, and found that courage spreads as readily as panic. People stand straighter when they believe something is still watching from above.*

### PARTY-05: 6.10, Merchant background

**§1 contrast. Recommended. Independent review: equal.** 'Never only X. It is Y.' stated directly.

*Line 2550, under "Merchant".* Dependencies: art catalog quote.

**Current**

> *A merchant learned value, leverage, and the quiet power of knowing what desperate people will pay. Coin is never only money to them. It is movement, influence, and another season behind the walls.*

**Proposed**

> *A merchant learned value, leverage, and the quiet power of knowing what desperate people will pay. To them, coin means movement, influence, and another season behind the walls.*

### PARTY-14: 6.12, Recommended First Party box

**§1 restated contrast. Recommended. Independent review: equal.** The box is headed 'Recommended First Party'; the closing line restates it.

*Line 2669, under "SPI General Talents".* Dependencies: none.

**Current**

> > **Recommended First Party:** For your first full-rules party, build a **Human Fighter (Soldier)**, an **Elf Ranger (Scout)**, a **Dwarf Cleric (Soldier)**, and a **Halfling Rogue (Smuggler)**, each using **Starting Package A**. This party provides front-line pressure and protection, ranged offence and control, healing and support, and mobility and objective utility. This is a recommendation, not a requirement.

**Proposed**

> > **Recommended First Party:** For your first full-rules party, build a **Human Fighter (Soldier)**, an **Elf Ranger (Scout)**, a **Dwarf Cleric (Soldier)**, and a **Halfling Rogue (Smuggler)**, each using **Starting Package A**. This party provides front-line pressure and protection, ranged offence and control, healing and support, and mobility and objective utility.

### PARTY-13: 6.13, introduction

**§12 jargon. Recommended. Independent review: better.** 'Talent ecosystem' is product jargon; 'defines a distinct' is padding.

*Line 2673, under "6.13 Hero Classes".* Dependencies: none.

**Current**

> Each class defines a distinct battlefield role, resource model, and talent ecosystem. Class talents are mechanically explicit and use the standard timing, action, and reaction rules of **Heraldry Skirmish**.

**Proposed**

> Each class has its own battlefield role, resources, and talents. Class talents are mechanically explicit and use the standard timing, action, and reaction rules of **Heraldry Skirmish**.

## Section 7: treasure, item lore, and item wording

### ITEM-12: 7.6, second paragraph

**§3 saying, §7 repeated openings. Recommended. Independent review of the revised wording: equal.** Joins one pair of 'may' sentences. (Revised in the quality review: the first draft also cut the closing line 'Wealth is leverage, temptation, and tomorrow's trouble made bright enough to carry home', which stays.)

*Line 3441, under "7.6 Treasure Tables".* Dependencies: none.

**Current**

> *Adventurers return to the ruins because coin keeps breath in the body. It buys bread, lamp oil, splints, armour, apothecary work, chapel rites, hired blades, and one more season behind a wall. A relic may ransom a village. It may also ruin one. A saint's ring may pay a healer. A king's cup may wake the court buried with it. Wealth is leverage, temptation, and tomorrow's trouble made bright enough to carry home.*

**Proposed**

> *Adventurers return to the ruins because coin keeps breath in the body. It buys bread, lamp oil, splints, armour, apothecary work, chapel rites, hired blades, and one more season behind a wall. A relic may ransom a village or ruin one. A saint's ring may pay a healer. A king's cup may wake the court buried with it. Wealth is leverage, temptation, and tomorrow's trouble made bright enough to carry home.*

### ITEM-07: 7.17.3, Kest's Iron Reliquary effect

**§12 'additionally'. Recommended. Independent review: better.** Wording only; the effect is unchanged.

*Line 4923, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> **Effect:** Once per adventure, when you are adjacent to an enemy and spend **[1 AP]**, you may open the reliquary and release the bound spirit within. That enemy suffers **2d8 necrotic damage**, then must pass a **SPI Check** against **12**. **Failure:** They become **Frightened** until the end of their next activation. After use, the reliquary is empty until the next adventure, when it is found to contain something again. It is always warm. Additionally, while you wear Kest's Iron Reliquary you may spend **[1 AP]** to end **Cursed** on yourself or one ally within **2"**.

**Proposed**

> **Effect:** Once per adventure, when you are adjacent to an enemy and spend **[1 AP]**, you may open the reliquary and release the bound spirit within. That enemy suffers **2d8 necrotic damage**, then must pass a **SPI Check** against **12**. **Failure:** They become **Frightened** until the end of their next activation. After use, the reliquary is empty until the next adventure, when it is found to contain something again. It is always warm. While you wear Kest's Iron Reliquary, you may also spend **[1 AP]** to end **Cursed** on yourself or one ally within **2"**.

### ITEM-08: 7.17.3, Saint Cael's Burning Seal effect

**§12 'additionally'. Recommended. Independent review: equal.** Wording only; the effect is unchanged.

*Line 4953, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> **Effect:** This weapon deals **holy** damage. While wielding Saint Cael's Burning Seal, once per adventure when you are within **2"** of a scenario-marked threshold, bridge, ford, gate, or archway and you apply **AV** or use **Parry** against an **Undead** or **Fiend**, you may treat each **AD** die or retained **Parry** base die as its maximum natural result instead of rolling it. Roll any exploding **Parry** bonus dice and resolve **Riposte** normally. Additionally, **Undead** and **Fiends** that attack you while you are within **2"** of such a threshold suffer **1d6 holy damage** after their attack resolves. While wielding Saint Cael's Burning Seal you may spend **[1 AP]** to end **Cursed** on yourself or one ally within **2"**.

**Proposed**

> **Effect:** This weapon deals **holy** damage. While wielding Saint Cael's Burning Seal, once per adventure when you are within **2"** of a scenario-marked threshold, bridge, ford, gate, or archway and you apply **AV** or use **Parry** against an **Undead** or **Fiend**, you may treat each **AD** die or retained **Parry** base die as its maximum natural result instead of rolling it. Roll any exploding **Parry** bonus dice and resolve **Riposte** normally. **Undead** and **Fiends** that attack you while you are within **2"** of such a threshold also suffer **1d6 holy damage** after their attack resolves. While wielding Saint Cael's Burning Seal you may spend **[1 AP]** to end **Cursed** on yourself or one ally within **2"**.

### ITEM-04: 7.17.3, Salttide's Counting Stone

**§2 fragments. Optional. Independent review: equal.** Optional. Merges two of the three closing fragments; the dry last line stays.

*Line 5052, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> *The stone Edrava Salttide used to count ships that should have paid their toll. Sailors still see them at low winter tide, counting. The stone counts everything now. It remembers every debt. It is very patient.*

**Proposed**

> *The stone Edrava Salttide used to count ships that should have paid their toll. Sailors still see them at low winter tide, counting. The stone counts everything now and remembers every debt. It is very patient.*

### ITEM-02: 7.17.3, Old Wode's Iron-Shod Staff

**§2 fragments. Recommended. Independent review: equal.** A one-phrase fragment ('Three times.') folds into the sentence it belongs to.

*Line 5076, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> *An iron-shod walking staff that has been struck against standing stones. Three times. The strikes are still there. Three dents in the iron cap, each one slightly warmer than the rest of the metal.*

**Proposed**

> *An iron-shod walking staff that has been struck three times against standing stones. The strikes are still there: three dents in the iron cap, each one slightly warmer than the rest of the metal.*

### ITEM-09: 7.17.3, Karnessa's Iron Seal effect

**§12 'additionally'. Recommended. Independent review: equal.** Wording only; the effect is unchanged.

*Line 5124, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> **Effect:** Once per adventure, when a Summon you control would be reduced to **0 HP**, you may spend **[0 AP]** to press Karnessa's Seal against them. This is a **Reaction**; declare it before that source's damage dice and commit its once-per-adventure use under **4.5**. That Summon is instead set to **1 HP**. Additionally, while wearing this Seal, you gain **+1** on **SPI Checks** made to resist the effects of **Undead** and **Fiend** Special Abilities.

**Proposed**

> **Effect:** Once per adventure, when a Summon you control would be reduced to **0 HP**, you may spend **[0 AP]** to press Karnessa's Seal against them. This is a **Reaction**; declare it before that source's damage dice and commit its once-per-adventure use under **4.5**. That Summon is instead set to **1 HP**. While wearing this Seal, you also gain **+1** on **SPI Checks** made to resist the effects of **Undead** and **Fiend** Special Abilities.

### ITEM-10: 7.17.3, Bell-Shard Charm effect

**§12 'additionally', §18 'functions as'. Recommended. Independent review: better.** 'Functions as' where 'is' says the same thing. (The Monster abilities that 'function as' another ability keep that wording, because there it means 'use the rules of'.)

*Line 5160, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> **Effect:** This item functions as an early warning system. When any **Undead** Monster becomes **Awake** within **12"** of you, the Charm chimes. You immediately become aware of that Monster's approximate location and that their Wake-Up condition has been met. You may then take a **[0 AP Reaction]**, even outside your activation, to make an **INT Check** against **12**. This Check does not require the Monster to be **Hidden** or in your **LOS**. On a success, the Monster loses **Hidden**, if applicable, and you know their exact position until the end of the round. Additionally, you gain **+1** on **SPI Checks** made to resist **Frightened** from **Undead** sources.

**Proposed**

> **Effect:** This item is an early warning system. When any **Undead** Monster becomes **Awake** within **12"** of you, the Charm chimes. You immediately become aware of that Monster's approximate location and that their Wake-Up condition has been met. You may then take a **[0 AP Reaction]**, even outside your activation, to make an **INT Check** against **12**. This Check does not require the Monster to be **Hidden** or in your **LOS**. On a success, the Monster loses **Hidden**, if applicable, and you know their exact position until the end of the round. Additionally, you gain **+1** on **SPI Checks** made to resist **Frightened** from **Undead** sources.

### ITEM-11: 7.17.3, Bell-Shard Charm effect

**§12 'additionally'. Recommended. Independent review: equal.** Wording only; the effect is unchanged.

*Line 5160, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> **Effect:** This item functions as an early warning system. When any **Undead** Monster becomes **Awake** within **12"** of you, the Charm chimes. You immediately become aware of that Monster's approximate location and that their Wake-Up condition has been met. You may then take a **[0 AP Reaction]**, even outside your activation, to make an **INT Check** against **12**. This Check does not require the Monster to be **Hidden** or in your **LOS**. On a success, the Monster loses **Hidden**, if applicable, and you know their exact position until the end of the round. Additionally, you gain **+1** on **SPI Checks** made to resist **Frightened** from **Undead** sources.

**Proposed**

> **Effect:** This item functions as an early warning system. When any **Undead** Monster becomes **Awake** within **12"** of you, the Charm chimes. You immediately become aware of that Monster's approximate location and that their Wake-Up condition has been met. You may then take a **[0 AP Reaction]**, even outside your activation, to make an **INT Check** against **12**. This Check does not require the Monster to be **Hidden** or in your **LOS**. On a success, the Monster loses **Hidden**, if applicable, and you know their exact position until the end of the round. You also gain **+1** on **SPI Checks** made to resist **Frightened** from **Undead** sources.

## Section 8: Powers

### POWER-01: 8, first paragraph

**§1 contrast, §12 words. Recommended. Independent review: better.** The Chapter 8 introduction is the most machine-sounding passage in the book. This paragraph drops the 'not a gift' contrast, 'transcend', 'the comforting heft of', and the participle chain, and keeps every claim.

*Line 5206, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *In the Dying Lands, magic is not a gift; it is a symptom of a broken world. To cast a spell is to reach into the cracks of reality and pull something volatile through, a transaction that always leaves a stain. The common folk know better than to trust it, having learned to fear its touch through generations of curses, twisted omens, and localized catastrophe. Sensible people cling to the safety of timber walls and the comforting heft of cold iron. But the desperate, the greedy, and the doomed recognize that surviving the ruins often requires bargaining with forces that transcend the swing of a blade.*

**Proposed**

> *In the Dying Lands, magic is a symptom of a broken world. To cast a spell is to reach into the cracks of reality and pull something volatile through, and the transaction always leaves a stain. Generations of curses, twisted omens, and local catastrophes have taught the common folk to fear its touch. Sensible people keep to timber walls and cold iron. The desperate, the greedy, and the doomed know that surviving the ruins often means bargaining with forces no blade can reach.*

### POWER-02: 8, second paragraph

**§16 sales word. Recommended. Independent review: equal.** 'Profoundly' is decoration.

*Line 5208, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Though the empires that once codified magic are ash, the Five Traditions survived the Fall, each scarred, perilous, and profoundly changed.*

**Proposed**

> *Though the empires that once codified magic are ash, the Five Traditions survived the Fall, each scarred, perilous, and much changed.*

### POWER-03: 8, Arcane Spells paragraph

**§1 contrast, §12 words, §15 riders. Recommended. Independent review of the revised wording: equal.** Drops 'less X than they are Y', 'cold calculus', 'sheer utility', and 'invariably'. (Corrected in the quality review: 'because they are useful' could be read as the Bastions.)

*Line 5210, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Arcane Spells are the hollow inheritance of the old world. Wizards are less miracle-workers than they are magical scavengers, piecing together forbidden principles from half-burned grimoires and the silent, dust-choked observatories where their predecessors still sit slumped in death. Their craft is a cold calculus of arcane formulae and unstable geometry. While Bastions tolerate them for their sheer utility, wizards are rarely loved, and are invariably blamed the moment a working leaks or the dead begin to walk.*

**Proposed**

> *Arcane Spells are the hollow inheritance of the old world. Wizards are scavengers, piecing together forbidden principles from half-burned grimoires and from silent, dust-choked observatories where their predecessors still sit slumped in death. Their craft runs on arcane formulae and unstable geometry. The Bastions tolerate wizards for their usefulness, rarely love them, and blame them the moment a working leaks or the dead begin to walk.*

### POWER-04: 8, Divine Prayers paragraph

**§6 triads, §9 qualifiers. Recommended. Independent review of the revised wording: better.** Plainer wording. 'An insult no scripture will name' and 'not yet worthy' match the wording 1.3.1 and 1.3.4 already use for the same two doctrines. (Corrected in the quality review: no comma splitting the predicate, and no triad.)

*Line 5212, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Divine Prayers are whispered into a largely empty sky. The old saints remain in the chapel rolls, but they answer fitfully, if they answer at all. A priest capable of calling down a true working is a rarity, famous enough to command reverence and terrifying enough to be feared. The faithful fracture over the silence: some preach that the gods retreated in disgust at an unnameable insult, while others insist mortal souls simply lack the worthiness to be heard. Regardless of the doctrine, divine magic is a desperate plea for a miracle, fuelled by fanatical devotion and answered only in blood and light.*

**Proposed**

> *Divine Prayers are whispered into a largely empty sky. The old saints remain in the chapel rolls, but they answer fitfully, if at all. A priest who can call down a true working is rare, feared as much as revered. The faithful split over the silence: some preach that the gods withdrew in disgust at an insult no scripture will name, and others that mortal souls are not yet worthy to be heard. Whatever the doctrine, a prayer is a desperate plea for a miracle, fuelled by fanatical devotion and answered only in blood and light.*

### POWER-05: 8, Druidic Rituals paragraph

**§16 sales language, §18 'act as'. Recommended. Independent review of the revised wording: equal.** Drops 'pulse with a terrifying, untamed vitality' and 'act as'. The 'do not mourn' contrast stays, because it marks the difference from the other traditions. (Corrected in the quality review: the first draft said 'the wild' twice in one long sentence.)

*Line 5214, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Druidic Rituals pulse with a terrifying, untamed vitality. Unlike the crumbling arcane or the silent divine, the magic of the wild has only grown more ferocious since the Fall. Druids commune with the encroaching forests, the choking bogs, and the violent storms. Their oldest circles do not mourn the dying world; instead, they teach that the earth is merely shedding mortal civilization like dead skin, and they act as the ruthless midwives to this violent rebirth.*

**Proposed**

> *Druidic Rituals draw on the wild. While arcane learning crumbles and the gods stay silent, the wild has only grown more ferocious since the Fall. Druids commune with the encroaching forests, the choking bogs, and the violent storms. Their oldest circles do not mourn the dying world. They teach that the earth is shedding mortal civilization like dead skin, and they attend that violent rebirth like ruthless midwives.*

### POWER-06: 8, Sorceries paragraph

**§18 'represent', §12 words. Recommended. Independent review: better.** 'Represent' becomes 'are'; drops 'terrible intimacy', 'raw, unrefined', 'paying for their output', and 'living conduits'.

*Line 5216, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Sorceries represent the most volatile and treacherous path to power, demanding a terrible intimacy with corruption. Some sorcerers are twisted by exposure to blighted ruin-sites, while others suffer from ancestral wounds reopening generations later, or strike infernal pacts in their darkest, most desperate hours. They wield raw, unrefined destruction, paying for their output in their own blood. Hanged in the streets of Sablekeep and treated with extreme caution everywhere else, sorcerers are living conduits of the world's sickness.*

**Proposed**

> *Sorceries are the most volatile and treacherous path to power, and the closest to corruption. Some sorcerers are twisted by exposure to blighted ruin-sites. Others carry ancestral wounds that reopen generations later, or strike infernal pacts in their most desperate hours. They wield raw destruction and pay for it in their own blood. Sablekeep hangs them in the streets, and everywhere else treats them with extreme caution. The world's sickness runs through every one of them.*

### POWER-07: 8, Psychic Abilities paragraph

**§1 contrast, §6 triad. Recommended. Independent review of the revised wording: better.** Parallel 'by ... by ... by' list, 'sheer proximity' made plain, and a clear subject for the last sentence. (Revised in the quality review: the first draft cut 'Psions do not study their power; they survive it' and 'strangest', which both stay.)

*Line 5218, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Psychic Abilities remain the rarest, strangest, and least understood of the traditions. Psions do not study their power; they survive it. Their minds are cracked open by the long, suffocating pressure of sunken crypts, exposure to thought-eater nests, or sheer proximity to the alien things sleeping beneath the Undermarches. They emerge from the dark hearing the jagged thoughts of everyone around them. They are rarely hunted with the same religious fervour as sorcerers, but they are never trusted, for no one welcomes a person who can weaponize a memory or peel back the privacy of a skull.*

**Proposed**

> *Psychic Abilities remain the rarest, strangest, and least understood of the traditions. Psions do not study their power; they survive it. Their minds are cracked open by the long, suffocating pressure of sunken crypts, by exposure to thought-eater nests, or by nearness to the alien things sleeping beneath the Undermarches. They emerge from the dark hearing the jagged thoughts of everyone around them. Psions are rarely hunted with the religious fervour reserved for sorcerers, but they are never trusted, because no one welcomes a person who can weaponize a memory or peel back the privacy of a skull.*

### POWER-08: 8.4, Tier 3 Divine Prayers introduction

**§1 contrast. Recommended. Independent review: equal.** 'Not asked but demanded' stated directly.

*Line 6207, under "Tier 3 Divine Prayers (d20)".* Dependencies: art catalog quote.

**Current**

> *At this height a prayer is not asked but demanded, and something always answers. Whether it is the god prayed to is a question the devout do not raise aloud.*

**Proposed**

> *At this height a prayer is a demand, and something always answers. Whether it is the god prayed to is a question the devout do not raise aloud.*

## Section 9: Monsters

### MON-01: 9, introduction

**§1 contrast. Recommended. Independent review: better.** Same move as LORE-15.

*Line 7552, under "9. Monsters".* Dependencies: none.

**Current**

> *Beyond the Bastions, the world is no longer governed by mortal law. Roads, courts, borders, shrines, and markets have been replaced by hunger, territory, instinct, old commands, and powers that survived the Fall better than humankind did. The creatures encountered in the Dying Lands are not interruptions to an expedition; they are the present owners of the world. Some are beasts made clever by scarcity, some are the dead still obeying ruined offices, some are mortals remade by pact, curse, rot, or worship, and some are older than the kingdoms whose bones they now inhabit. Each climate teaches its inhabitants a different form of cruelty, and each has produced creatures that use that cruelty as law. To enter the wilds is not to wander into empty land. It is to trespass.*

**Proposed**

> *Beyond the Bastions, the world is no longer governed by mortal law. Roads, courts, borders, shrines, and markets have been replaced by hunger, territory, instinct, old commands, and powers that survived the Fall better than humankind did. The creatures encountered in the Dying Lands are the present owners of the world. Some are beasts made clever by scarcity, some are the dead still obeying ruined offices, some are mortals remade by pact, curse, rot, or worship, and some are older than the kingdoms whose bones they now inhabit. Each climate teaches its inhabitants a different form of cruelty, and each has produced creatures that use that cruelty as law. To enter the wilds is not to wander into empty land. It is to trespass.*

### MON-17: 9.7, Monster Roles

**§3 saying. Recommended. Independent review of the revised wording: better.** 'It is a promise about...' dresses up a plain function. (Revised in the quality review: the first draft's 'what kind of fight it has woken up' had two 'it's with different referents.)

*Line 7805, under "Monster Roles".* Dependencies: none.

**Current**

> Every Monster fills a Role on the battlefield, named in brackets after their name. A Role is an encounter-building label and has no mechanical effect unless a rule explicitly says otherwise. It is a promise about how the Monster fights, so that a single glance tells a party what kind of trouble has woken up.

**Proposed**

> Every Monster fills a Role on the battlefield, named in brackets after their name. A Role is an encounter-building label and has no mechanical effect unless a rule explicitly says otherwise. It tells a party at a glance what kind of trouble has woken up.

### MON-20: 9.7, Monster Roles, Skirmisher

**repeated phrase. Recommended. Independent review of the revised wording: equal.** 'Before the answer lands' or 'comes' appears three times (also the Giant Bat and the Frost Wyvern, MON-21). (Revised in the quality review to avoid 'strikes ... strike back'.)

*Line 7809, under "Monster Roles".* Dependencies: none.

**Current**

> - **Skirmisher:** A darting, circling threat that strikes and slips away before the answer lands. A Skirmisher trades armour for speed and is deadliest in a pack that never holds still.

**Proposed**

> - **Skirmisher:** A darting, circling threat that hits and slips away before anyone can strike back. A Skirmisher trades armour for speed and is deadliest in a pack that never holds still.

### MON-22: 9.7, Monster Roles, Cannon

**stock closer. Recommended. Independent review of the revised wording: better.** 'Or pay the price' is a stock phrase.

*Line 7810, under "Monster Roles".* Dependencies: none.

**Current**

> - **Cannon:** A fragile engine of sudden violence. A Cannon can fell a hero in a single dreadful moment, then shatter the instant a blade reaches them. Strike them first or pay the price.

**Proposed**

> - **Cannon:** A fragile engine of sudden violence. A Cannon can fell a hero in a single dreadful moment, then shatter the instant a blade reaches them. Strike them first.

### MON-24: 9.7, Monster Roles, Elite

**'X given a body' template. Recommended. Independent review: equal.** 'X given a body' or 'given a shape' appears eight times in the book; this and MON-25 and MON-26 vary three. Also drops the doubled 'focused, concerted'.

*Line 7813, under "Monster Roles".* Dependencies: none.

**Current**

> - **Elite:** A small war given a single body. An Elite duels a seasoned hero as an equal and shrugs off scattered blows; only focused, concerted effort will bring one down. Their kind are rare and terrible, and seldom seen in numbers.

**Proposed**

> - **Elite:** A whole battle in one body. An Elite duels a seasoned hero as an equal and shrugs off scattered blows; only a concentrated attack will bring one down. Elites are rare and terrible, and seldom seen in numbers.

### MON-03: 9.7, Wererat

**§2 repeated closer. Recommended. Independent review: equal.** 'One is X; a swarm is Y' closes seven Monster entries. This and MON-04 trim two; the Goblin, Dire Wolf, Ratkin Warrior, Swamp Goblin, and Stirge keep theirs.

*Line 8301, under "Wererat [Skirmisher]".* Dependencies: art catalog quote.

**Current**

> *Where the Ashlands meet the old sewers and undercrofts, the wererat thrives, a hunched, plague-grey shapeshifter scurrying between man and rat-thing. They bite, then skitter back into the dark, leaving filth-fever in every wound. Mundane blades barely mark them. One wererat is a nuisance; a nest of them is an outbreak.*

**Proposed**

> *Where the Ashlands meet the old sewers and undercrofts, the wererat thrives, a hunched, plague-grey shapeshifter scurrying between man and rat-thing. They bite, then skitter back into the dark, leaving filth-fever in every wound. Mundane blades barely mark them. A nest of them is an outbreak.*

### MON-04: 9.7, Kobold

**§2 repeated closer. Recommended. Independent review: equal.** See MON-03.

*Line 8604, under "Kobold [Minion]".* Dependencies: art catalog quote.

**Current**

> *Knee-high reptilian scavengers with dull scales and dingy picks, kobolds are the Undermarches' scuttling vermin-folk. One alone is nothing; a chittering mob of them, dragging traps and loosing slings from the dark, is a real danger. They know every tunnel and trust not one. Where a single kobold shows themselves, a whole warren is watching.*

**Proposed**

> *Knee-high reptilian scavengers with dull scales and dingy picks, kobolds are the Undermarches' scuttling vermin-folk. A chittering mob of them, dragging traps and loosing slings from the dark, is a real danger. They know every tunnel and trust not one. Where a single kobold shows themselves, a whole warren is watching.*

### MON-07: 9.7, Frozen Skeleton

**§2 repeated closer. Recommended. Independent review: equal.** 'There are always more' closes three undead Minion entries. The Undead Warrior keeps it; this entry already calls them 'countless'.

*Line 8992, under "Frozen Skeleton [Minion]".* Dependencies: art catalog quote.

**Current**

> *Rimed in blue frost, a sword welded to their hand by ice, a frozen skeleton is one of the Pale City's countless dead, still standing the post they were given. They guard avenues that have not seen a living census in centuries. The cold preserves them whole; they will hold that post when the last warm thing in the world goes out. There are always more under the snow.*

**Proposed**

> *Rimed in blue frost, a sword welded to their hand by ice, a frozen skeleton is one of the Pale City's countless dead, still standing the post they were given. They guard avenues that have not seen a living census in centuries. The cold preserves them whole; they will hold that post when the last warm thing in the world goes out.*

### MON-26: 9.7, Ice Wraith

**'X given a body' template. Recommended. Independent review: equal.** See MON-24.

*Line 9169, under "Ice Wraith [Cannon]".* Dependencies: art catalog quote.

**Current**

> *A knife of frozen malice given a drifting, translucent shape, the ice wraith is the spirit of someone who froze to death in the Pale City and never forgave it. Their touch saps warmth and thickens the blood to sludge. Steel passes clean through; only magic bites. They haunt the coldest avenues, hungry for the heat of anything still living.*

**Proposed**

> *A knife of frozen malice in a drifting, translucent shape, the ice wraith is the spirit of someone who froze to death in the Pale City and never forgave it. Their touch saps warmth and thickens the blood to sludge. Steel passes clean through; only magic bites. They haunt the coldest avenues, hungry for the heat of anything still living.*

### MON-21: 9.7, Frost Wyvern

**repeated phrase. Recommended. Independent review of the revised wording: equal.** See MON-20. (Revised in the quality review: the first draft's 'again' lost the timing.)

*Line 9286, under "Frost Wyvern [Elite]".* Dependencies: art catalog quote.

**Current**

> *A lesser cousin of the great dragons, the frost wyvern is a winged reptile the colour of dirty ice, a venom-and-frost sting whipping at the end of their tail. They stoop from the white sky to harry and poison, then climb out of reach before the answer comes. They are cunning rather than wise. The Pale City's frozen peaks are crowded with their roosts.*

**Proposed**

> *A lesser cousin of the great dragons, the frost wyvern is a winged reptile the colour of dirty ice, a venom-and-frost sting whipping at the end of their tail. They stoop from the white sky to harry and poison, then climb out of reach before a blade or bolt can follow. They are cunning rather than wise. The Pale City's frozen peaks are crowded with their roosts.*

### MON-25: 9.7, White Dragon

**'X given a body' template. Recommended. Independent review: equal.** See MON-24.

*Line 9348, under "White Dragon [Elite]".* Dependencies: art catalog quote.

**Current**

> *Visath's feral get, the white dragon is an ice-crusted wyrm whose breath flash-freezes whatever it touches. Less cunning than their kin but no less lethal, they are pure predatory cold given wings and an appetite. They nest in the lesser spires and suffer the White Court about them as courtiers. When they descend, the city's eternal winter only deepens.*

**Proposed**

> *Visath's feral get, the white dragon is an ice-crusted wyrm whose breath flash-freezes whatever it touches. Less cunning than their kin but no less lethal, they are predatory cold with wings and an appetite. They nest in the lesser spires and suffer the White Court about them as courtiers. When they descend, the city's eternal winter only deepens.*

### MON-32: 9.7, Imp

**stock closer. Recommended. Independent review: equal.** 'A herald of worse to come' is stock.

*Line 9391, under "Imp [Skirmisher]".* Dependencies: art catalog quote.

**Current**

> *Knee-high and bat-winged, a barbed venomous tail lashing behind them, the imp flits about the Sun-Drowned tombs as the spiteful servant of darker things. They dart in to sting and wheel away cackling, untroubled by the desert's heat or their own infernal fire. Alone they are more nuisance than threat. They are also a herald of worse to come.*

**Proposed**

> *Knee-high and bat-winged, a barbed venomous tail lashing behind them, the imp flits about the Sun-Drowned tombs as the spiteful servant of darker things. They dart in to sting and wheel away cackling, untroubled by the desert's heat or their own infernal fire. Alone they are more nuisance than threat, but worse usually follows them.*

### MON-11: 9.7, Fire Elemental

**§2 closer. Recommended. Independent review: equal.** Restates the first sentence ('scorches whatever strikes them').

*Line 9570, under "Fire Elemental [Cannon]".* Dependencies: art catalog quote.

**Current**

> *A roaring man-shape of living flame, white-hot at the core and shedding embers at the edges, the fire elemental sets alight everything they touch and scorches whatever strikes them. Water and ice are their only checks; the desert sun is their cradle. They draw a trail of cinders across the tomb-floors. To lay hands on them is to burn.*

**Proposed**

> *A roaring man-shape of living flame, white-hot at the core and shedding embers at the edges, the fire elemental sets alight everything they touch and scorches whatever strikes them. Water and ice are their only checks; the desert sun is their cradle. They draw a trail of cinders across the tomb-floors.*

### MON-09: 9.7, Giant Skeleton

**§2 closer. Recommended. Independent review: equal.** 'They guard it still' closes five guardian entries; this one adds nothing to the carving detail before it.

*Line 9587, under "Giant Skeleton [Brute]".* Dependencies: art catalog quote.

**Current**

> *A looming framework of fused bone twice a man's height, the giant skeleton is what remains of something that was never entirely natural and is far less so now. They move with grinding deliberation, sweeping aside anything in their path with fists like falling masonry. Tomb-city carvings show their kind kneeling before the priest-kings; none show them standing. Whatever they were raised to guard, they guard it still.*

**Proposed**

> *A looming framework of fused bone twice a man's height, the giant skeleton is what remains of something that was never entirely natural and is far less so now. They move with grinding deliberation, sweeping aside anything in their path with fists like falling masonry. Tomb-city carvings show their kind kneeling before the priest-kings; none show them standing.*

### MON-34: 9.7, Manticore

**repeated closer. Recommended. Independent review: equal.** 'The X is their larder / barracks / nursery / hunting ground' closes seven entries, two with 'larder'. This and MON-35 trim two; the Elder Vrymk keeps 'larder'.

*Line 9687, under "Manticore [Elite]".* Dependencies: art catalog quote.

**Current**

> *A monstrous fusion of lion's body, bat's wings, and a man's leering face, the manticore flicks volleys of iron spikes from their lashing tail. They wait where the dune-road narrows and rain barbs on whatever they have trapped. They savour a meal that begged first. The Sun-Drowned's loneliest trails are their larder.*

**Proposed**

> *A monstrous fusion of lion's body, bat's wings, and a man's leering face, the manticore flicks volleys of iron spikes from their lashing tail. They wait where the dune-road narrows and rain barbs on whatever they have trapped. They savour a meal that begged first.*

### MON-37: 9.7, Swamp Hag

**repeated phrase. Recommended. Independent review: equal.** The Night Hag has the same 'They bargain, they lie, and they...' triad; this keeps all three claims in a different shape.

*Line 10009, under "Swamp Hag [Controller]".* Dependencies: art catalog quote.

**Current**

> *A warty, weed-haired crone, the swamp hag poles their way through The Mire cursing all they meet, slipping half into the spirit-world when cornered. Their stench chokes out hope. They bargain, they lie, and they feed on misery. The loneliest hut in the mire is theirs, and it is never empty for long.*

**Proposed**

> *A warty, weed-haired crone, the swamp hag poles their way through The Mire cursing all they meet, slipping half into the spirit-world when cornered. Their stench chokes out hope. They feed on misery, and every bargain they offer is a lie. The loneliest hut in the mire is theirs, and it is never empty for long.*

### MON-35: 9.7, The Broodmother Prime

**repeated closer. Recommended. Independent review: equal.** See MON-34; the first sentence already calls them the mother of every giant spider.

*Line 10274, under "The Broodmother Prime [Boss]".* Dependencies: player aid pa02; art catalog quote.

**Current**

> *In the deepest dark of the Undermarches squats the mother of every giant spider that plagues the deep, a bloated horror the size of a cottage, egg-sacs trailing from them that twitch with the unborn. They flood the field with their brood and bind the survivors in webs for later. Their venom stops a heart in a single beat. The deep, in the end, is their nursery.*

**Proposed**

> *In the deepest dark of the Undermarches squats the mother of every giant spider that plagues the deep, a bloated horror the size of a cottage, egg-sacs trailing from them that twitch with the unborn. They flood the field with their brood and bind the survivors in webs for later. Their venom stops a heart in a single beat.*

### MON-13: 9.7, Visath the White

**§1 contrast. Recommended. Independent review: better.** 'Does not merely X; it Y.' The ice survives in the same sentence.

*Line 10463, under "Visath the White [Boss]".* Dependencies: player aid pa02; art catalog quote.

**Current**

> *Visath is the Pale City's eternal winter wearing the body of a wyrm, a glacier with wings and a will. Their breath does not merely freeze; it stops time in the flesh, leaving victims locked mid-scream in the ice. They rule from the highest spire and suffer no warmth anywhere in their domain. Where they fly, the snow falls harder, as though the sky itself bows.*

**Proposed**

> *Visath is the Pale City's eternal winter wearing the body of a wyrm, a glacier with wings and a will. Their breath stops time in the flesh, leaving victims locked mid-scream in the ice. They rule from the highest spire and suffer no warmth anywhere in their domain. Where they fly, the snow falls harder, as though the sky itself bows.*

## Section 10: objectives, scenarios, and solo play

### SCEN-02: 10.4, Greenmark Scenario 2, Scenario-Specific Monster: Antlered Warden

**§1 contrast, §7 repeated openings. Recommended. Independent review: equal.** Keeps the correction (a reader may well expect Old Wode here) without the verbless opener.

*Line 12115, under "Scenario 2: The Whispering Grove".* Dependencies: figures FIG-13 to FIG-56 (41).

**Current**

> *Not Old Wode themselves. Old Wode does not stir for small intrusions. The Antlered Warden is the agreement's enforcement arm: a figure woven from the grove's oldest growth, robed in bark and grey moss, with antlers that have more branches than any natural animal. They do not speak. They do not negotiate. They maintain the terms.*

**Proposed**

> *This is not Old Wode, who does not stir for small intrusions. The Antlered Warden is the agreement's enforcement arm: a figure woven from the grove's oldest growth, robed in bark and grey moss, with antlers that have more branches than any natural animal. They do not speak. They do not negotiate. They maintain the terms.*

### SCEN-12: 10.4, Pale City Scenario 5, The Ice Wyrm's Hoard

**§2 closer. Recommended. Independent review: better.** Restates the sentence before it, and repeats the 'kind of listener' closer the Sandwyrm also uses (SCEN-09).

*Line 13665, under "Scenario 5: The Ice Wyrm's Hoard".* Dependencies: figures FIG-13 to FIG-56 (41); art catalog quote.

**Current**

> *The old stories put jewels and gold in a frozen cavern beneath the north road out of Hearthhold, and a wyrm coiled on top of them whose breath can stop a heart inside its own armour. Hearthhold needs the gold more than it fears the breath, which is the kind of arithmetic only the poorest Bastion does out loud. The second part of the story has never discouraged the first kind of listener.*

**Proposed**

> *The old stories put jewels and gold in a frozen cavern beneath the north road out of Hearthhold, and a wyrm coiled on top of them whose breath can stop a heart inside its own armour. Hearthhold needs the gold more than it fears the breath, which is the kind of arithmetic only the poorest Bastion does out loud.*

### SCEN-09: 10.4, Sun-Drowned Scenario 4, The Sandwyrm's Lair

**§2 closer. Recommended. Independent review: equal.** Restates the warning/inventory contrast the two sentences before it already make.

*Line 14019, under "Scenario 4: The Sandwyrm's Lair".* Dependencies: figures FIG-13 to FIG-56 (41); art catalog quote.

**Current**

> *Nomad legends speak of a vast shape beneath the dunes south of the passes, and a gullet lined with the treasure of everything they have swallowed. The nomads tell it as a warning. Saltspire's patrons hear it as an inventory and pay accordingly. The dunes do not distinguish between the two kinds of listener.*

**Proposed**

> *Nomad legends speak of a vast shape beneath the dunes south of the passes, and a gullet lined with the treasure of everything they have swallowed. The nomads tell it as a warning. Saltspire's patrons hear it as an inventory and pay accordingly.*

### SCEN-14: 10.5, introduction

**stock phrase. Recommended. Independent review of the revised wording: better.** 'The battlefield itself becomes the enemy' is stock. The replacement names what replaces the rival party, using the defined term from 10.5.7, which assigns each scenario one mandatory **Pressure Clock**. (Corrected in the quality review: 'pressure rules' is not a defined term.)

*Line 14699, under "10.5 Solo and Cooperative Play".* Dependencies: player aid pa10.

**Current**

> Heraldry Skirmish may be played as a **solo** or **cooperative** game. In these modes, there is no rival adventuring party. Instead, the battlefield itself becomes the enemy. Solo and cooperative play use the normal core rules unless this section says otherwise.

**Proposed**

> Heraldry Skirmish may be played as a **solo** or **cooperative** game. In these modes, there is no rival adventuring party; the scenario's Monsters, hazards, and **Pressure Clock** take its place. Solo and cooperative play use the normal core rules unless this section says otherwise.

## Section 11: campaign

### CAMP-02: 11, third paragraph

**§2 fragments. Recommended. Independent review: equal.** The same 'Small enough to hide. Strong enough to fight. Cheap enough to lose.' row opens 1.3.6, which keeps it as written; this varies the verbatim repeat.

*Line 15025, under "11. Campaign Play".* Dependencies: none.

**Current**

> *Councils, chapels, guilds, and discreet nobles use smaller tools. They hire parties. Small enough to hide. Strong enough to fight. Cheap enough to lose. Each contract begins as ink on a table inside the walls. It ends in mud, ash, snow, salt, or blood.*

**Proposed**

> *Councils, chapels, guilds, and discreet nobles use a smaller tool. They hire parties small enough to hide, strong enough to fight, and cheap enough to lose. Each contract begins as ink on a table inside the walls. It ends in mud, ash, snow, salt, or blood.*

### CAMP-09: 11, fifth paragraph

**§7 repeated openings, §2 closer. Recommended. Independent review of the revised wording: equal.** 'They rarely mention' twice in a row. (Revised in the quality review: the closing 'The Bastions know. The contracts are drafted accordingly.' stays as written.)

*Line 15029, under "11. Campaign Play".* Dependencies: none.

**Current**

> *Each adventure begins with a promise written by someone who expects not to bleed. A patron may ask the party to recover medicine from a ruined apothecary, extract a relic from a sealed crypt, escort a message through The Mire, burn out a sorcerer's tower, slay a named **Monster**, or confirm that another party failed. The written terms rarely mention the rival company hired under another seal. They rarely mention the last expedition whose bones still lie within sight of the objective. The Bastions know. The contracts are drafted accordingly.*

**Proposed**

> *Each adventure begins with a promise written by someone who expects not to bleed. A patron may ask the party to recover medicine from a ruined apothecary, extract a relic from a sealed crypt, escort a message through The Mire, burn out a sorcerer's tower, slay a named **Monster**, or confirm that another party failed. The written terms rarely mention the rival company hired under another seal, or the last expedition whose bones still lie within sight of the objective. The Bastions know. The contracts are drafted accordingly.*

### CAMP-06: 11.3, The Vault

**§1 contrast. Recommended. Independent review: equal.** The negative half denies a claim nobody made.

*Line 15668, under "The Vault".* Dependencies: player aid pa08, pa09; art catalog quote.

**Current**

> *The Vault is not a treasury. It is a sealed confession of greed, iron-bound and watched by clerks who sleep in shifts. They count each coin as if the dead might come back to collect.*

**Proposed**

> *The Vault is a sealed confession of greed, iron-bound and watched by clerks who sleep in shifts. They count each coin as if the dead might come back to collect.*

### CAMP-13: 11.3, The Stronghold Chapel

**§1 contrast. Recommended. Independent review: better.** Split 'does not X. It Y.' as one sentence.

*Line 15730, under "The Stronghold Chapel".* Dependencies: player aid pa08, pa09.

**Current**

> *The Chapel does not promise salvation. It gives the desperate a place to kneel before they return to the roads that nearly killed them.*

**Proposed**

> *The Chapel promises no salvation, only a place for the desperate to kneel before they return to the roads that nearly killed them.*

## Appendix A: Learn to Play

### LEARN-02: A.10, opening paragraph

**§1 contrast, §12 'matter'. Recommended. Independent review: equal.** 'Is not won only by X' followed by its restatement.

*Line 16397, under "A.10 Objectives, Extraction, and Scoring".* Dependencies: figures FIG-18.

**Current**

> Heraldry Skirmish is not won only by defeating enemies. Positioning and objective play matter more than trading damage.

**Proposed**

> Positioning and objective play decide more games than trading damage does.

### LEARN-01: A.11, closing paragraph

**§1 contrast, §2 'this shows'. Recommended. Independent review: equal.** 'This shows why X is not merely Y' is the strongest tell in the rules text. The replacement states what the two rounds showed; the rest of the paragraph is unchanged.

*Line 16544, under "Round 2".* Dependencies: figures FIG-18.

**Current**

> This opening shows why Heraldry Skirmish is not merely a damage race. Edric seized the objective quickly, but spending all **3 AP** left them unable to **Dodge**, **Block**, or **Parry**. Varek punished the exposed carrier, the Dire Wolves punished the centre scrum, and Mara earned coins only by taking a flank objective while the main fight collapsed.

**Proposed**

> Both rounds turned on **AP** and objectives more than on damage. Edric seized the objective quickly, but spending all **3 AP** left them unable to **Dodge**, **Block**, or **Parry**. Varek punished the exposed carrier, the Dire Wolves punished the centre scrum, and Mara earned coins only by taking a flank objective while the main fight collapsed.
