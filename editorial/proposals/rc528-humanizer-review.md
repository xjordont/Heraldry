# Humanizer review: proposed patches for RC528

**Not applied.** Two owner requests, 2026-11-02, in a Claude Code session: "humanizer manuscript", then "Use the humanize skill again to ensure nothing is missed that sounds like AI or would trigger AI detection software." This is the proposal those requests produce under the project contract: the manuscript changes only through exact replacements the owner approves, promoted once through `tools/revise_manuscript.py` as one new RC. Nothing below has been applied, and no figure, aid, or PDF has been rebuilt.

Prepared 2026-11-02 against `source/Heraldry_RC527.md` (SHA-256 `d28f5ec8ef438b43d278ec59c8faf195204266606bcfad1cbd8258088f48ec55`, 18,552 lines). The 140 patches (78 from the first pass, 62 from the second) are in the JSON twin `editorial/proposals/rc528-humanizer-review.json`, each with status `proposed` and its pass number. Every `find` occurs exactly once in RC527 and still exactly once when the batch is applied in order. No patch adds or removes a line, so block IDs and figure line citations do not move. No patch changes a number, a name, or a bold term (LEARN-01 adds a bold **AP**, as the book writes it elsewhere). The full candidate passed `python tools/dev.py manuscript prepare` (READY FOR OWNER REVIEW; 83 of 83 content anchors resolve; no blocking finding).

## Method

Both passes follow the humanizer skill (patterns from Wikipedia's "Signs of AI writing"). Section numbers like §1 refer to its pattern list: §1 is 'not X but Y' contrasts, §2 one-line closers and rows of fragments, §3 sayings that sound deep, §6 forced triads, §7 repeated sentence openings and templates, §12 stock AI words, §16 sales language, §18 'serves as' and 'represents' in place of 'is', and §25 text that describes the document instead of its subject.

- **First pass.** Every italic lore paragraph (about 22,700 words), all of Section 1, and the Appendix A walkthrough, read in full; the whole manuscript swept mechanically for dashes, contrast formulas, stock vocabulary, and staged phrasing.
- **Second pass.** Every non-italic paragraph and list item with descriptive rather than procedural content (691 passages, about 23,000 words, selected as any line of 90 or more characters with no digits and at most one rules keyword), read in full. This found the Monster Roles definitions, the class introduction, and the solo-play introduction. A wider sweep (transitions such as 'Furthermore' and 'Moreover', corporate words such as 'ensure' and 'leverage', intensifiers, 'to X is to Y', 'neither X nor Y', repeated phrases across entries) and a stricter re-read of the lore followed, at the document scale as well as the sentence scale: templates repeated across entries, phrases that recur in different chapters, and the first pass's own replacements. The re-read also found the one lore paragraph outside Section 1 that the first pass's extraction had skipped (the 11.1 Triumph paragraph, which opens in bold italics), and one forced triad the first pass had itself introduced (POWER-04, now corrected).

The voice is the book's own: terse, grim, and fond of a dry last line. The rewrites keep that. Fiction may invent, but these patches add nothing to the canon: every replacement keeps the facts of the text it replaces, and where a line is cut, the line was a restatement.

## AI detection

No edit can promise a particular score from AI-detection software. Detectors are unreliable on short and formulaic text and disagree with one another, and rules text is formulaic by design: 'unless a rule says otherwise' is correct rulebook English, and rewriting it to vary the statistics would make the rules less precise. This batch therefore removes what both detectors and careful readers key on (stock contrasts, rows of fragments, templated closers, phrases repeated across entries, and stock vocabulary) and leaves the procedural rules wording alone. The residual counts in the italic lore, before and after the whole batch:

| Pattern in the italic lore | RC527 | With all patches |
| --- | --- | --- |
| 'X is not Y. It is Z.' contrasts | 47 | 19 |
| 'not just', 'not merely', 'not only' | 1 | 0 |
| Sentences of three words or fewer | 50 | 19 |
| 'X given a body' or 'given a shape' | 6 | 2 |
| 'before the answer lands' or 'comes' | 2 | 1 |
| 'is their larder' or 'nursery' | 3 | 1 |
| 'the language of' | 1 | 0 |
| Lore sentences | 1698 | 1562 |

The remaining contrasts are kept on purpose: the negative half corrects something a reader would plausibly assume ("The Bastions themselves are not allies", "Parties do not hunt the five", "The gates do not ask what a refugee is"), or the line is a joke that carries a fact ("They do not count coin. They count the heavy, bright things their last few meals were carrying"). The remaining short sentences are ordinary topic sentences and dry asides ("Priests preach withdrawal.", "You have checked.", "Probably."). Varied sentence length is a human trait, so they stay.

## Verdict

The rules text is clean. The manuscript has no em dashes, all 370 en dashes sit in number ranges such as 1–3, there are no 'Furthermore' or 'Moreover' transitions, and the stock AI vocabulary is almost absent. The contrast hits in the rules ('not a Total Miss but before mitigation') are real rule distinctions. The rules-text patches are few: the Appendix A teaching lines (LEARN-01, LEARN-02), the solo-play introduction (SCEN-14), the class introduction (PARTY-13), the Recommended First Party box (PARTY-14), the Monster Roles definitions (MON-17 to MON-24), and five item-effect sentences, four opening 'Additionally' and one using 'functions as' (ITEM-07 to ITEM-11).

The tells are in the lore: 'Not X. It is Y.' contrasts, rows of fragments, closers repeated across entries ('One is X; a swarm is Y' ends seven Monster entries), templated openings (seven class entries open 'A [Class] is forged / bred / built / schooled / formed / bound / handed'), and phrases used in several chapters ('X given a body' appears eight times). The Chapter 8 introduction (POWER-01 to POWER-07) reads as generated throughout and is rewritten in full, keeping each claim.

## Counts

| Group | First pass | Second pass | Figures affected |
| --- | --- | --- | --- |
| Section 1: the world | 19 | 10 | none |
| Section 6: parties, ancestries, backgrounds, and classes | 5 | 12 | FIG-75 |
| Section 7: treasure, item lore, and item wording | 11 | 4 | none |
| Section 8: Powers | 9 | 0 | none |
| Section 9: Monsters | 16 | 23 | none |
| Section 10: objectives, scenarios, and solo play | 10 | 4 | 41 (FIG-13 to FIG-56) |
| Section 11: campaign | 7 | 8 | none |
| Appendix A: Learn to Play | 1 | 1 | FIG-18 |
| **Total** | **78** | **62** | **43** |

137 patches are recommended and 3 optional (ITEM-04, MON-14, PARTY-01). Applied together, they shorten the book by about 395 words.

## Owner choices

Approving a group means approving its patch IDs. The groups differ mainly in what they cost downstream:

1. **Approve everything except the 10.4 scenario patches** (128 patches). 123 of them affect no figure. LEARN-01 and LEARN-02 stale one figure review (FIG-18, which hashes all of Appendix A), and PARTY-07 to PARTY-09 stale one more (FIG-75, which hashes 6.9 Ancestries).
2. **Also approve the 10.4 scenario patches** (12 patches: SCEN-02, SCEN-03, SCEN-04, SCEN-05, SCEN-06, SCEN-07, SCEN-08, SCEN-09, SCEN-10, SCEN-11, SCEN-12, SCEN-13). `tools/figure_dependencies.py` hashes the whole of **10.4 Core Scenario Outlines** for every scenario map and preparation figure, so any edit inside 10.4, however cosmetic, marks 41 figure reviews stale (FIG-13 to FIG-16 and FIG-20 to FIG-56). None of these patches touches what a figure draws, so the re-review is a confirmation, but it has to be recorded before the next release. SCEN-01 (10.2) and SCEN-14 (10.5) affect no figure.
3. **Two earlier owner-approved phrases.** LORE-02 removes 'not soft clerks with ledgers' and LORE-17 restructures 'Small enough to hide. Strong enough to fight. Cheap enough to lose.'; RC523 polished both. Decline either to keep the current wording.
4. **The game's pitch.** LORE-20 and LORE-21 vary the triads in the 1.1 introduction, the first prose a new reader sees. The back cover's quoted facts are unaffected. Decline them if you prefer the current pitch.
5. **Optional patches.** PARTY-01 ("not the heroes sung about in warm halls") arguably corrects a real genre expectation; ITEM-04 is a small merge; MON-14 removes the Void Dragon's 'neither burns nor freezes' contrast with the other dragons.

## Dependency impact

- **Figures.** See the owner choices above: 2 figures (FIG-18, FIG-75) without the 10.4 patches, 43 with them.
- **Content anchors.** All 83 resolve on the full candidate; none needs a new prefix. The back cover's quoted facts come from 1.1 paragraphs whose quoted sentences are unchanged.
- **Player-aid sheets.** `tools/aids_fidelity.py` will report changed sections for pa02 (MON-13, MON-14, MON-15, MON-16, MON-27, MON-28, MON-29, MON-35); pa08 (CAMP-06, CAMP-07, CAMP-11, CAMP-12, CAMP-13, CAMP-14, CAMP-15); pa09 (CAMP-06, CAMP-07, CAMP-11, CAMP-12, CAMP-13, CAMP-14, CAMP-15); pa10 (SCEN-14). The changes are lore paragraphs (and, for pa10, the 10.5 introduction) inside sections a sheet condenses; no sheet quotes the patched wording, so re-recording after a diff is a confirmation and the sheets do not need rebuilding.
- **Hero cards, back cover, How to Use, and cover lead.** Unaffected: B.4 is untouched, and no string in `editorial/back_cover.json`, `editorial/how_to_use.json`, or the 'cover-lead' anchor changes.
- **Art catalog.** `production/art/SPOT_CATALOG.json` and `production/art/ILLUSTRATION_LIST.md` quote the flavour text above each illustration, and 62 patches change quoted paragraphs. Regenerate both at promotion (`python tools/dev.py agent run art-catalog`, then `tools/art_list.py`) as after the earlier lore revisions. Approved art is unaffected.
- **Specimen.** `typst/templates/specimens.typ` quotes the Frozen Laboratory introduction as sample text; SCEN-07 would leave it one sentence longer than the book. It is a type specimen, not book content, so updating it is optional.
- **Build.** Nothing was built. The last released PDFs (RC527-build-41) are unchanged.

## Left alone

- **Procedural rules wording.** Repeated formulas such as 'unless a rule says otherwise' and the condition-expiry sentences are deliberate rules language; varying them would cost precision.
- **Headings and bold labels.** Title-case headings and bold run-in labels are the book's house style and carry anchors, cross-references, and the index (§19 and §20 do not apply).
- **Monster entry openings.** Most Bestiary entries open with an appositive ('Knee-high and bat-winged, the imp...'). That is a template, but it is the house form for all 135 entries and each one carries specific physical detail.
- **Deliberate motifs.** The frogs falling silent before The Mire's predators, the warm relics of Mordain Kest, the 'only magic answers' immunity reminders that mirror the stat blocks, and the Greythorn line 'Its chapel is small. Its arcane spire is smaller. Its training yard is the largest in the world.'
- **Repeated content.** Two passages restate earlier ones closely: the 'Columns need wagons...' climate list in 1.3.6 returns in the Chapter 11 introduction, and Chapter 8's tradition paragraphs repeat 1.3.4. That is a structure question, not a writing tell, so no patch cuts either; say if you want one.

## Findings

Grouped by section, in manuscript order within each group. Line numbers refer to `source/Heraldry_RC527.md`. 'Current' is the whole line as it stands; 'Proposed' is that line with only this patch applied (where two patches share a line, each is shown alone).

## Section 1: the world

### LORE-20: 1.1, first paragraph

**§6 forced triads. Recommended. Second pass.** Three triads in two sentences. This varies the last one; the first two stay, and nothing is dropped.

*Line 167, under "1.1 What is Heraldry Skirmish?".* Dependencies: none.

**Current**

> **Heraldry Skirmish** is a competitive GM-less PvPvE fantasy tabletop miniatures game of desperate expeditions, brutal clashes, and hard-won survival. Most battles pit two rival adventuring parties against one another as they race through monster-haunted ruins, damned wilderness, and blood-soaked strongholds in search of treasure, glory, and escape.

**Proposed**

> **Heraldry Skirmish** is a competitive GM-less PvPvE fantasy tabletop miniatures game of desperate expeditions, brutal clashes, and hard-won survival. Most battles pit two rival adventuring parties against one another as they race through monster-haunted ruins, damned wilderness, and blood-soaked strongholds, chasing treasure and glory and hoping to get out alive.

### LORE-01: 1.1, third paragraph

**§2 closers. Recommended. First pass.** The opener announces what the next sentence shows, and 'Even victory is rarely clean' restates the closing sentence. Both go; the three facts and the closing line stay.

*Line 171, under "1.1 What is Heraldry Skirmish?".* Dependencies: none.

**Current**

> The battlefield is never passive. Neutral Monsters stalk the field, hazards punish hesitation, and scenarios place pressure on both sides from the first activation to the last. Even victory is rarely clean. The party that leaves the field richest is often the one that bled for every coin.

**Proposed**

> Neutral Monsters stalk the field, hazards punish hesitation, and scenarios place pressure on both sides from the first activation to the last. The party that leaves the field richest is often the one that bled for every coin.

### LORE-21: 1.1, fourth paragraph

**§6 forced triad. Recommended. Second pass.** A promotional triad. The back cover quotes only this paragraph's first sentence (cover-fact-2), which is unchanged.

*Line 173, under "1.1 What is Heraldry Skirmish?".* Dependencies: none.

**Current**

> Heraldry Skirmish supports **solo** and **cooperative** play. In those games, **1–4 players** control **1–4 allied Heroes** against scenarios strengthened by additional Monsters, harsher threats, and fixed PvE pressure in place of a rival party. Whether played competitively or cooperatively, Heraldry is built around dangerous choices, concise tactical rules, and the constant risk that boldness will be rewarded before it is punished.

**Proposed**

> Heraldry Skirmish supports **solo** and **cooperative** play. In those games, **1–4 players** control **1–4 allied Heroes** against scenarios strengthened by additional Monsters, harsher threats, and fixed PvE pressure in place of a rival party. Either way, the tactical rules stay concise and the choices stay dangerous, with the constant risk that boldness will be rewarded before it is punished.

### LORE-22: 1.2, first paragraph

**§7 repeated openings. Recommended. Second pass.** A balanced 'Their X. Their Y.' pair becomes one sentence.

*Line 191, under "1.2 The Grim World".* Dependencies: art catalog quote.

**Current**

> *The world of **Heraldry Skirmish** is a realm of old faiths, broken kingdoms, hungry roads, and cold bargains. Kings, princes, bishops, and warlords still raise banners over land they can barely hold. They fight over relics, tolls, doctrine, trade roads, salt, iron, and pride. Their victories are measured in burnt farms and new taxes. Their defeats are carried by peasants who never chose a side.*

**Proposed**

> *The world of **Heraldry Skirmish** is a realm of old faiths, broken kingdoms, hungry roads, and cold bargains. Kings, princes, bishops, and warlords still raise banners over land they can barely hold. They fight over relics, tolls, doctrine, trade roads, salt, iron, and pride. Their victories are measured in burnt farms and new taxes, and their defeats are carried by peasants who never chose a side.*

### LORE-02: 1.2, second paragraph

**§1 contrast, §7 repeated openings. Recommended. First pass.** Nobody claimed merchants were soft clerks; the list of what they do makes the point. The two 'They know which' sentences merge. RC523 polished the 'soft clerks' phrase, so decline this patch if you want to keep it.

*Line 193, under "1.2 The Grim World".* Dependencies: none.

**Current**

> *Most people live close to a gate. A palisade, a bell, a chapel lamp, and a few armed neighbours are the shape of civilization now. Beyond them lie drowned fields, plague roads, ruined shrines, black forests, dead bridges, and the shattered works of older realms. Merchants who travel between holdings are not soft clerks with ledgers. They bargain, lie, fight, navigate, and plan funerals with equal care. They know which inns change names too often. They know which milestones bleed in rain.*

**Proposed**

> *Most people live close to a gate. A palisade, a bell, a chapel lamp, and a few armed neighbours are the shape of civilization now. Beyond them lie drowned fields, plague roads, ruined shrines, black forests, dead bridges, and the shattered works of older realms. Merchants who travel between holdings bargain, lie, fight, navigate, and plan funerals with equal care. They know which inns change names too often and which milestones bleed in rain.*

### LORE-03: 1.2, third paragraph

**§6 forced triad, §7 repeated openings. Recommended. First pass.** Three fragments with the same opening become one sentence; all three kinds of dead stay.

*Line 195, under "1.2 The Grim World".* Dependencies: none.

**Current**

> *The countryside has teeth. Bandits prey on the weak and call it tax. Beasts prowl where the ploughs stopped. Goblin raiders descend on lonely roads and isolated farms. Orcs, gnolls, and kobolds test the borderlands for weakness and plunder. Haunted crypts and mass graves fill with the failures of earlier expeditions. The dead do not always stay down. Some rise hungry. Some rise bitter. Some rise with orders still clenched behind their teeth.*

**Proposed**

> *The countryside has teeth. Bandits prey on the weak and call it tax. Beasts prowl where the ploughs stopped. Goblin raiders descend on lonely roads and isolated farms. Orcs, gnolls, and kobolds test the borderlands for weakness and plunder. Haunted crypts and mass graves fill with the failures of earlier expeditions. The dead do not always stay down: some rise hungry, some bitter, and some with orders still clenched behind their teeth.*

### LORE-04: 1.2, fourth paragraph

**§7 repeated openings. Recommended. First pass.** 'X waits there' three times in a row.

*Line 197, under "1.2 The Grim World".* Dependencies: none.

**Current**

> *Beneath ruined towers, sunken monasteries, and collapsed fortresses lie the vaults of fallen empires. Coin waits there. Relics wait there. Forbidden lore waits there too, written in dust, iron, blood, and languages that make candles gutter. Dragons still brood in the deep places of the earth and on the high forgotten peaks. Their hoards could ransom kingdoms. Their wrath could end them.*

**Proposed**

> *Beneath ruined towers, sunken monasteries, and collapsed fortresses lie the vaults of fallen empires. Coin and relics wait there, and so does forbidden lore, written in dust, iron, blood, and languages that make candles gutter. Dragons still brood in the deep places of the earth and on the high forgotten peaks. Their hoards could ransom kingdoms. Their wrath could end them.*

### LORE-23: 1.2, fifth paragraph

**§6 forced triad. Recommended. Second pass.** 'Feared' and 'never trusted' overlap, and the rest of the paragraph shows the fear.

*Line 199, under "1.2 The Grim World".* Dependencies: none.

**Current**

> *Magic is real, feared, and never trusted. It is too common to dismiss and too dangerous to treat as ordinary. Curses, omens, failed workings, and old catastrophes have taught peasants to spit before speaking of it. Wizards dig power from broken observatories, dust-choked books, and stolen manuscripts. Sorcerers pay in blood for gifts they rarely understand. Priests beg miracles from distant powers that answer by silence as often as grace. Druids bargain with roots, rivers, storms, and things that remember the world before walls. Psions return from forbidden disciplines with minds cracked open and something still echoing inside.*

**Proposed**

> *Magic is real and never trusted, too common to dismiss and too dangerous to treat as ordinary. Curses, omens, failed workings, and old catastrophes have taught peasants to spit before speaking of it. Wizards dig power from broken observatories, dust-choked books, and stolen manuscripts. Sorcerers pay in blood for gifts they rarely understand. Priests beg miracles from distant powers that answer by silence as often as grace. Druids bargain with roots, rivers, storms, and things that remember the world before walls. Psions return from forbidden disciplines with minds cracked open and something still echoing inside.*

### LORE-24: 1.2, last paragraph

**§3 saying, §2 closer. Recommended. Second pass.** Two aphorisms as a closing pair; joined, with the debt image kept.

*Line 201, under "1.2 The Grim World".* Dependencies: none.

**Current**

> *Sensible people cling to hearth, habit, and walls. Your **Heroes** do not. They take writs from patrons who will not bleed for their own promises. They cross causeways where relief columns vanished, ford rivers that carry bones in flood season, and pry gold from rooms that should have stayed shut. In Heraldry, glory is a rumour told after the bodies are counted. Survival is a debt renewed one Skirmish at a time.*

**Proposed**

> *Sensible people cling to hearth, habit, and walls. Your **Heroes** do not. They take writs from patrons who will not bleed for their own promises. They cross causeways where relief columns vanished, ford rivers that carry bones in flood season, and pry gold from rooms that should have stayed shut. In Heraldry, glory is a rumour told after the bodies are counted, and survival is a debt that comes due again every Skirmish.*

### LORE-25: 1.3, The Dying Lands at a Glance

**§25 writing about the document. Recommended. Second pass.** 'The sections below tell the story' describes the page; the pointer to the rules stays.

*Line 205, under "1.3 The Dying Lands".* Dependencies: none.

**Current**

> **The Dying Lands at a Glance.** One ruined continent, six climates: the overgrown **Greenmark**, the ash-choked **Ashlands**, the lightless **Undermarches**, the frozen **Pale City**, the sun-scorched **Sun-Drowned**, and **The Mire**, poisoned and drowning beneath its own waters. Six **Bastions** hold what remains of mortal civilization. Everything between them is contested ground, and adventurers are the few who are paid to cross it. The sections below tell the story. The rules begin at **1.4**.

**Proposed**

> **The Dying Lands at a Glance.** One ruined continent, six climates: the overgrown **Greenmark**, the ash-choked **Ashlands**, the lightless **Undermarches**, the frozen **Pale City**, the sun-scorched **Sun-Drowned**, and **The Mire**, poisoned and drowning beneath its own waters. Six **Bastions** hold what remains of mortal civilization. Everything between them is contested ground, and adventurers are the few who are paid to cross it. The rules begin at **1.4**.

### LORE-05: 1.3, third paragraph

**§1 contrast. Recommended. First pass.** The negative half denies a claim nobody made; the rest of the sentence already says the crowns and borders stopped being useful.

*Line 209, under "1.3 The Dying Lands".* Dependencies: none.

**Current**

> *The lands where Heraldry Skirmish is fought are not a kingdom. They are a continent in the oldest sense: a single body of land held together by mountains, rivers, roads, ruins, and grief long after its crowns and borders stopped being useful.*

**Proposed**

> *The lands where Heraldry Skirmish is fought are a continent in the oldest sense: a single body of land held together by mountains, rivers, roads, ruins, and grief long after its crowns and borders stopped being useful.*

### LORE-06: 1.3.1, last paragraph

**§1 contrast, §2 fragments. Recommended. First pass.** A 'not X, it is Y' opener followed by a row of one-word fragments. The image and all three qualities stay.

*Line 227, under "1.3.1 The Fall".* Dependencies: none.

**Current**

> *The world is not dying gently. It dies like a wounded animal under a hedge. Slow. Aware. Dangerous to touch.*

**Proposed**

> *The world is dying the way a wounded animal dies under a hedge: slowly, aware of it, and dangerous to touch.*

### LORE-07: 1.3.2, opening paragraph

**§3 saying. Recommended. First pass.** An aphorism with no claim the paragraph goes on to support; the paragraph is about names and labels.

*Line 231, under "1.3.2 The Six Climates of Ruin".* Dependencies: art catalog quote.

**Current**

> *Beyond the walls, land has become allegiance. Expedition ledgers still say forest, city, cavern, ice, desert, and swamp. Survivors know better. They use older names. The shape of the world is plain enough to anyone who has walked it. The broken mountains run down its spine. The dead empire and its ruined cities sprawl across the eastern heart. The great forest spreads west to the coast, the ice locks the north, the dunes burn in the south beyond the mountain passes, and the swamps drown the south-east where the rivers give out at the sea. The old imperial roads still join all of it, straight and patient, running out from the Ashlands to every climate that survived. A dry label cannot warn a traveller that a road has memory, a court still sits without lungs, or a pool of black water may be listening.*

**Proposed**

> *Expedition ledgers still say forest, city, cavern, ice, desert, and swamp. Survivors know better. They use older names. The shape of the world is plain enough to anyone who has walked it. The broken mountains run down its spine. The dead empire and its ruined cities sprawl across the eastern heart. The great forest spreads west to the coast, the ice locks the north, the dunes burn in the south beyond the mountain passes, and the swamps drown the south-east where the rivers give out at the sea. The old imperial roads still join all of it, straight and patient, running out from the Ashlands to every climate that survived. A dry label cannot warn a traveller that a road has memory, a court still sits without lungs, or a pool of black water may be listening.*

### LORE-08: 1.3.2, The Greenmark

**§1 contrast. Recommended. First pass.** Split 'not X. It is Y.' closer stated directly.

*Line 235, under "The Greenmark".* Dependencies: art catalog quote.

**Current**

> *The Greenmark is the great temperate forest of the surviving world. It is larger than the maps. Roots take a road within a season and make the milestones useless. Travellers report trees shifting at the edge of sight, upright hounds between trunks, and grove-circles where moss stays warm after snow. Foresters cut warning signs into bark for those who know how to read them. The most common sign means turn back even if the voice ahead is your own. The forest is no wilderness. It is a country that does not recognize human law.*

**Proposed**

> *The Greenmark is the great temperate forest of the surviving world. It is larger than the maps. Roots take a road within a season and make the milestones useless. Travellers report trees shifting at the edge of sight, upright hounds between trunks, and grove-circles where moss stays warm after snow. Foresters cut warning signs into bark for those who know how to read them. The most common sign means turn back even if the voice ahead is your own. The forest is a country of its own, and it does not recognize human law.*

### LORE-09: 1.3.2, closing paragraph

**§2 closer. Recommended. First pass.** 'These six are the world now' restates the section; the two Bastion sentences share a subject and merge.

*Line 257, under "The Mire".* Dependencies: none.

**Current**

> *These six are the world now. The Bastions are what mortal civilization built against them. They are also what mortal civilization hides inside.*

**Proposed**

> *The Bastions are what mortal civilization built against these six climates, and what it hides inside.*

### LORE-10: 1.3.3, fourth paragraph

**§7 repeated openings. Recommended. First pass.** Nine short sentences, four opening 'They' and two 'No Bastion', become four. Every item stays.

*Line 267, under "1.3.3 The Six Bastions".* Dependencies: none.

**Current**

> *The Bastions themselves are not allies. They send envoys. They trade iron, salt, grain, oil, bodies, medicine, and lies. They exchange prisoners when it is useful. They accept refugees when plague at the gate would be worse than charity. Their treaties are thin things. Tired clerks write them. Hungry captains break them. No Bastion can afford open war with another. No Bastion trusts that fact to last.*

**Proposed**

> *The Bastions themselves are not allies. They send envoys and trade iron, salt, grain, oil, bodies, medicine, and lies. They exchange prisoners when it is useful and accept refugees when plague at the gate would be worse than charity. Their treaties are thin things, written by tired clerks and broken by hungry captains. No Bastion can afford open war with another, and none trusts that fact to last.*

### LORE-11: 1.3.3, fifth paragraph

**§1 contrast. Recommended. First pass.** 'Not safe. They are safer.' is the staged form; the plain comparison says the same thing. 'but' repairs the list that follows.

*Line 269, under "1.3.3 The Six Bastions".* Dependencies: none.

**Current**

> *The Bastions are not safe. They are safer. Their walls keep out the worst of the dark, not hunger, fever, debt, politics, superstition, or the quiet passengers hidden among refugees and trade goods. Every gate has a price. Every chapel keeps lists. Every guild counts favours. Every watch-fire burns lower than the captains admit.*

**Proposed**

> *The Bastions are only safer than the country around them. Their walls keep out the worst of the dark, but not hunger, fever, debt, politics, superstition, or the quiet passengers hidden among refugees and trade goods. Every gate has a price. Every chapel keeps lists. Every guild counts favours. Every watch-fire burns lower than the captains admit.*

### LORE-12: 1.3.3, last paragraph before Greythorn

**§1 contrast. Recommended. First pass.** 'Part of the war' already says it is not peace.

*Line 275, under "1.3.3 The Six Bastions".* Dependencies: none.

**Current**

> *For most people, the Bastion is the end of the world made habitable by walls. For adventurers, it is where wounds are priced, contracts are stamped, dead companions are replaced, and the next mistake is made official. The **Town Phase** is not peace. It is the part of the war fought with ledgers, knives, prayers, and closed doors.*

**Proposed**

> *For most people, the Bastion is the end of the world made habitable by walls. For adventurers, it is where wounds are priced, contracts are stamped, dead companions are replaced, and the next mistake is made official. The **Town Phase** is the part of the war fought with ledgers, knives, prayers, and closed doors.*

### LORE-13: 1.3.3, Saltspire

**§2 fragments. Recommended. First pass.** Two follow-up fragments merge into the sentence they explain.

*Line 311, under "Saltspire".* Dependencies: art catalog quote.

**Current**

> ***Saltspire** is a tower-city built around a deep, sacred well at the centre of an oasis ringed by salt-pans and the bones of older cities. It has the only reliable water for a hundred miles. This makes it wealthy. It also makes it hated.*

**Proposed**

> ***Saltspire** is a tower-city built around a deep, sacred well at the centre of an oasis ringed by salt-pans and the bones of older cities. It has the only reliable water for a hundred miles, which makes it wealthy and hated.*

### LORE-14: 1.3.4, Arcane Spells

**§3 saying. Recommended. First pass.** 'Tolerance is not trust' is an aphorism standing in for the plain claim.

*Line 329, under "1.3.4 Magic in the Dying Lands".* Dependencies: none.

**Current**

> ***Arcane Spells** are the inheritance of the broken empires. Wizards seek ruined libraries, half-burned grimoires, observatories with cracked lenses, and silent towers where their predecessors are still slumped over their work. Most Bastions tolerate wizards because they are useful. Tolerance is not trust. Sablekeep requires registration. Greythorn pays enough to keep them polite. Deepwarden watches their shadows on tunnel walls. They are blamed whenever blame needs a shape.*

**Proposed**

> ***Arcane Spells** are the inheritance of the broken empires. Wizards seek ruined libraries, half-burned grimoires, observatories with cracked lenses, and silent towers where their predecessors are still slumped over their work. Most Bastions tolerate wizards because they are useful. No Bastion trusts them. Sablekeep requires registration. Greythorn pays enough to keep them polite. Deepwarden watches their shadows on tunnel walls. They are blamed whenever blame needs a shape.*

### LORE-26: 1.3.4, Divine Prayers

**§7 repeated openings. Recommended. Second pass.** Paired 'Both' fragments.

*Line 331, under "1.3.4 Magic in the Dying Lands".* Dependencies: none.

**Current**

> ***Divine Prayers** answer fitfully. The old saints remain in chapel rolls, and a few still seem to listen. Most do not. Priests who can call down a working become famous. Fame makes them useful, feared, and watched. Some teach that prayers fail because the gods withdrew. Others teach that prayers fail because the faithful are not yet worthy. Both teachings recruit. Both can get people killed.*

**Proposed**

> ***Divine Prayers** answer fitfully. The old saints remain in chapel rolls, and a few still seem to listen. Most do not. Priests who can call down a working become famous. Fame makes them useful, feared, and watched. Some teach that prayers fail because the gods withdrew. Others teach that prayers fail because the faithful are not yet worthy. Both teachings recruit, and both can get people killed.*

### LORE-15: 1.3.5, opening paragraph

**§1 contrast. Recommended. First pass.** The negative half denies a claim nobody made. Chapter 9 opens with the same move (MON-01).

*Line 343, under "1.3.5 Monstrous Threats".* Dependencies: art catalog quote.

**Current**

> *The **Monsters** of the Dying Lands are not scattered obstacles. They hold the world now. They keep roads closed, fields empty, shrines silent, and old borders meaningless. A village may vanish because of hunger, tax, fever, or weather. Outside the walls, those causes often have claws, banners, laws, or names.*

**Proposed**

> *The **Monsters** of the Dying Lands hold the world now. They keep roads closed, fields empty, shrines silent, and old borders meaningless. A village may vanish because of hunger, tax, fever, or weather. Outside the walls, those causes often have claws, banners, laws, or names.*

### LORE-27: 1.3.5, Goblinoids

**§7 repeated openings. Recommended. Second pass.** Three 'Some' openings in a row.

*Line 347, under "1.3.5 Monstrous Threats".* Dependencies: none.

**Current**

> ***Goblinoids, kobolds, gnolls, and orcs** raid wherever they can find a foothold. Goblin clans and web-wrights haunt the Greenmark roads. Gnoll war-bands ride the Sun-Drowned surface under banners cured stiff by heat. Orcs test borderlands for weak gates, poor watch, and winter hunger. Kobolds vanish into drains, old mines, and foundation cracks. Some serve stolen banners from older kingdoms. Some serve nothing. Some Bandit Captains of the forest roads are no longer mortal enough for that title to comfort anyone.*

**Proposed**

> ***Goblinoids, kobolds, gnolls, and orcs** raid wherever they can find a foothold. Goblin clans and web-wrights haunt the Greenmark roads. Gnoll war-bands ride the Sun-Drowned surface under banners cured stiff by heat. Orcs test borderlands for weak gates, poor watch, and winter hunger. Kobolds vanish into drains, old mines, and foundation cracks. Some serve stolen banners from older kingdoms, and some serve nothing. A few Bandit Captains of the forest roads are no longer mortal enough for that title to comfort anyone.*

### LORE-16: 1.3.5, the old peoples

**§7 repeated openings. Recommended. First pass.** Four 'Some' sentences in a row; the three one-word ones merge.

*Line 351, under "1.3.5 Monstrous Threats".* Dependencies: none.

**Current**

> ***The old peoples and border powers** have not vanished. Were-creatures, satyr cohorts, dryad ambassadors, deep elves, nagas, necromancers, lizardfolk temple-guards, and stranger courts hold places the Bastions still mark as lost. Some bargain. Some tithe. Some raid. Some remember treaties humanity has forgotten and punish the breach with perfect sincerity. In the Sun-Drowned, the tomb-cities of the priest-kings are administered by **necromancers** who have outlasted their own deaths: judges, clerks, and tax-collectors preserved in linen, oil, and old authority. They do not acknowledge the Fall. They acknowledge overdue accounts.*

**Proposed**

> ***The old peoples and border powers** have not vanished. Were-creatures, satyr cohorts, dryad ambassadors, deep elves, nagas, necromancers, lizardfolk temple-guards, and stranger courts hold places the Bastions still mark as lost. Some bargain, some tithe, and some raid. Some remember treaties humanity has forgotten and punish the breach with perfect sincerity. In the Sun-Drowned, the tomb-cities of the priest-kings are administered by **necromancers** who have outlasted their own deaths: judges, clerks, and tax-collectors preserved in linen, oil, and old authority. They do not acknowledge the Fall. They acknowledge overdue accounts.*

### LORE-17: 1.3.6, third paragraph

**§2 fragments. Recommended. First pass.** A row of fragments becomes one sentence; the three qualities stay. The same row appears again in Chapter 11 (CAMP-02). RC523 reworded 'Strong enough to fight'; that wording is kept.

*Line 367, under "1.3.6 Adventurers and the Road".* Dependencies: none.

**Current**

> *What works is a party of four. Small enough to hide. Strong enough to fight. Cheap enough to lose.*

**Proposed**

> *What works is a party of four: small enough to hide, strong enough to fight, and cheap enough to lose.*

### LORE-18: 1.3.6, last paragraph

**§2 fragments. Recommended. First pass.** Three fragments become the end of the sentence they illustrate.

*Line 375, under "1.3.6 Adventurers and the Road".* Dependencies: none.

**Current**

> *Those who survive begin to build something larger than a purse. A keep on a hill. A reclaimed manor. A forge, a chapel, a vault, and a wall thick enough to last one hard winter. Few parties live long enough to raise such a place. Fewer reach **Triumph**, the old Bastion word for planting a banner in ground that has stayed clean for a generation. Every party leaving the gate tells itself this is the road ahead. Most roads end before that.*

**Proposed**

> *Those who survive begin to build something larger than a purse: a keep on a hill or a reclaimed manor, with a forge, a chapel, a vault, and a wall thick enough to last one hard winter. Few parties live long enough to raise such a place. Fewer reach **Triumph**, the old Bastion word for planting a banner in ground that has stayed clean for a generation. Every party leaving the gate tells itself this is the road ahead. Most roads end before that.*

### LORE-28: 1.3.7, opening line

**§2 fragments. Recommended. Second pass.** Two-beat closer joined.

*Line 379, under "1.3.7 Legends and Echoes".* Dependencies: art catalog quote.

**Current**

> *The Dying Lands remember. They do not remember kindly.*

**Proposed**

> *The Dying Lands remember, and not kindly.*

### LORE-29: 1.3.7, after the omens

**§1 contrast, §2 closer. Recommended. Second pass.** The first pass kept this because a rulebook reader may wonder whether omens are rules. The stricter pass keeps that information but drops the staged 'not X. They are Y.' form.

*Line 401, under "1.3.7 Legends and Echoes".* Dependencies: none.

**Current**

> *These are not rules. They are warnings.*

**Proposed**

> *The omens are warnings only; none of them is a rule of play.*

### LORE-19: 1.3.7, last paragraph

**§1 contrast. Recommended. First pass.** Split 'does not need X. It needs only Y.' stated directly.

*Line 403, under "1.3.7 Legends and Echoes".* Dependencies: none.

**Current**

> *The lore of the Dying Lands provides names, scars, and old quarrels for expeditions, rival parties, patrons, **Monsters**, relics, and campaign goals. A scenario does not need to explain the whole world. It needs only enough history to make the blood on the ground feel older than the fight.*

**Proposed**

> *The lore of the Dying Lands provides names, scars, and old quarrels for expeditions, rival parties, patrons, **Monsters**, relics, and campaign goals. A scenario needs only enough history to make the blood on the ground feel older than the fight.*

## Section 6: parties, ancestries, backgrounds, and classes

### PARTY-01: 6, opening paragraph

**§1 contrast. Optional. First pass.** Optional. The negative half does push against a genre expectation, so keep it if that is the point; the next sentences make the same point with specifics.

*Line 1998, under "6. Your Adventuring Party".* Dependencies: none.

**Current**

> *Adventuring parties are not the heroes sung about in warm halls. They are the people the Bastions can send when soldiers would die too loudly. Debtors march with seals burned into their papers. Condemned prisoners carry pardons that become valid only if they return. Chapel agents, guild cutters, ruined heirs, oath-bound hirelings, and free companies with no banner worth saluting all leave by the same gates.*

**Proposed**

> *Adventuring parties are the people the Bastions can send when soldiers would die too loudly. Debtors march with seals burned into their papers. Condemned prisoners carry pardons that become valid only if they return. Chapel agents, guild cutters, ruined heirs, oath-bound hirelings, and free companies with no banner worth saluting all leave by the same gates.*

### PARTY-02: 6, second paragraph

**§7 repeated openings. Recommended. First pass.** Three parallel sentences become one.

*Line 2000, under "6. Your Adventuring Party".* Dependencies: none.

**Current**

> *A Bastion blesses these parties when it must. It pays them when it can. It denies them when the work turns shameful. Most **Expeditions** begin with a writ: a council mark, chapel order, guild contract, noble warrant, salvage-right, grave-tax exemption, or debt bond. The paper grants legal cause to enter forbidden ground and take what can be carried out. Rival parties may hold different writs for the same ruin. Each seal may be valid under some law, oath, or patronage. The Dying Lands do not care. A contract only matters if someone lives long enough to collect.*

**Proposed**

> *A Bastion blesses these parties when it must, pays them when it can, and denies them when the work turns shameful. Most **Expeditions** begin with a writ: a council mark, chapel order, guild contract, noble warrant, salvage-right, grave-tax exemption, or debt bond. The paper grants legal cause to enter forbidden ground and take what can be carried out. Rival parties may hold different writs for the same ruin. Each seal may be valid under some law, oath, or patronage. The Dying Lands do not care. A contract only matters if someone lives long enough to collect.*

### PARTY-06: 6, second paragraph

**§2 closer. Recommended. Second pass.** Two closers in a row joined.

*Line 2000, under "6. Your Adventuring Party".* Dependencies: none.

**Current**

> *A Bastion blesses these parties when it must. It pays them when it can. It denies them when the work turns shameful. Most **Expeditions** begin with a writ: a council mark, chapel order, guild contract, noble warrant, salvage-right, grave-tax exemption, or debt bond. The paper grants legal cause to enter forbidden ground and take what can be carried out. Rival parties may hold different writs for the same ruin. Each seal may be valid under some law, oath, or patronage. The Dying Lands do not care. A contract only matters if someone lives long enough to collect.*

**Proposed**

> *A Bastion blesses these parties when it must. It pays them when it can. It denies them when the work turns shameful. Most **Expeditions** begin with a writ: a council mark, chapel order, guild contract, noble warrant, salvage-right, grave-tax exemption, or debt bond. The paper grants legal cause to enter forbidden ground and take what can be carried out. Rival parties may hold different writs for the same ruin. Each seal may be valid under some law, oath, or patronage. The Dying Lands do not care, and a contract only matters if someone lives long enough to collect.*

### PARTY-07: 6.9, Dwarf

**§1 'not so much X as Y'. Recommended. Second pass.** Same claim without the contrast frame.

*Line 2246, under "Dwarf".* Dependencies: figures FIG-75; art catalog quote.

**Current**

> *Dwarves are cut from sealed stone halls, old grudges, and craft traditions older than most fallen kingdoms. Hardship did not sour them so much as harden them, and little in this world meets one of them head-on and walks away whole.*

**Proposed**

> *Dwarves are cut from sealed stone halls, old grudges, and craft traditions older than most fallen kingdoms. Hardship hardened them more than it soured them, and little in this world meets one of them head-on and walks away whole.*

### PARTY-08: 6.9, Deep Elf

**§7 repeated template. Recommended. Second pass.** 'They are X and Y, and far more/harder...' closes three ancestry entries (Halfling, Deep Elf, and the Gnome's near copy); this varies one.

*Line 2343, under "Deep Elf".* Dependencies: figures FIG-75; art catalog quote.

**Current**

> *Deep elves are a crueller branch of the elder blood, raised on night, venom, and treachery taught as a fine art. They are graceful and dangerous, and far more at ease beneath the dark than beneath the sun.*

**Proposed**

> *Deep elves are a crueller branch of the elder blood, raised on night, venom, and treachery taught as a fine art. Graceful and dangerous, they are more at home in the dark than under the sun.*

### PARTY-09: 6.9, Drakeblood

**§3 'the language of'. Recommended. Second pass.** 'The language of' is a stock phrase.

*Line 2378, under "Drakeblood".* Dependencies: figures FIG-75; art catalog quote.

**Current**

> *The drakeblood carry the remnant of an older majesty in the blood, as blessing, burden, or half-remembered debt. The world is fallen, but power still answers them in the old language of flame, storm, and scale.*

**Proposed**

> *The drakeblood carry the remnant of an older majesty in the blood, as blessing, burden, or half-remembered debt. The world has fallen, but power still answers them through flame, storm, and scale.*

### PARTY-03: 6.10, Smuggler background

**§1 contrast. Recommended. First pass.** 'Not a flourish. It is...' denies a claim nobody made.

*Line 2454, under "Smuggler".* Dependencies: art catalog quote.

**Current**

> *A smuggler lives by false bottoms, whispered routes, and the craft of keeping valuable things out of dangerous hands. Stealth is not a flourish to them. It is the trade that buys supper.*

**Proposed**

> *A smuggler lives by false bottoms, whispered routes, and the craft of keeping valuable things out of dangerous hands. To them, stealth is the trade that buys supper.*

### PARTY-04: 6.10, Courier background

**§1 contrast. Recommended. First pass.** Same move as PARTY-03.

*Line 2462, under "Courier".* Dependencies: art catalog quote.

**Current**

> *A courier carried news, coin, or secrets across broken roads and worse weather, for patrons who paid for speed and asked no questions. Speed was never a convenience. It was the difference between arriving and being found later.*

**Proposed**

> *A courier carried news, coin, or secrets across broken roads and worse weather, for patrons who paid for speed and asked no questions. Speed was the difference between arriving and being found later.*

### PARTY-10: 6.10, Scholar

**§12 'matters', stock 'where others see'. Recommended. Second pass.** 'Where others see only X, they Y' is a stock frame.

*Line 2494, under "Scholar".* Dependencies: art catalog quote.

**Current**

> *A scholar lived among books, diagrams, and arguments, and the stubborn belief that knowledge matters even in a dying world. Where others see only rubble, they read the record of how it came to fall.*

**Proposed**

> *A scholar lived among books, diagrams, and arguments, stubbornly sure that knowledge is worth keeping even in a dying world. In the rubble, they read the record of how it came to fall.*

### PARTY-11: 6.10, Apprentice

**§2 repeated closer. Recommended. Second pass.** 'Leaves marks' closes both the Apprentice and the Noble.

*Line 2502, under "Apprentice".* Dependencies: art catalog quote.

**Current**

> *An apprentice served beneath someone wiser, crueller, or more dangerous than themselves, and took what scraps of the craft they could. Even unfinished training leaves marks that never quite fade.*

**Proposed**

> *An apprentice served beneath someone wiser, crueller, or more dangerous than themselves, and took what scraps of the craft they could. Even unfinished, the training has stayed with them.*

### PARTY-12: 6.10, Believer

**§7 repeated template. Recommended. Second pass.** Ten of the twenty background entries turn on 'learned' or 'taught'; this varies one where the sentence allows it.

*Line 2518, under "Believer".* Dependencies: art catalog quote.

**Current**

> *A believer kept faith in a world that rewards it rarely, and learned that courage spreads as readily as panic. People stand straighter when they believe something is still watching from above.*

**Proposed**

> *A believer kept faith in a world that rewards it rarely, and found that courage spreads as readily as panic. People stand straighter when they believe something is still watching from above.*

### PARTY-05: 6.10, Merchant background

**§1 contrast. Recommended. First pass.** 'Never only X. It is Y.' stated directly.

*Line 2550, under "Merchant".* Dependencies: art catalog quote.

**Current**

> *A merchant learned value, leverage, and the quiet power of knowing what desperate people will pay. Coin is never only money to them. It is movement, influence, and another season behind the walls.*

**Proposed**

> *A merchant learned value, leverage, and the quiet power of knowing what desperate people will pay. To them, coin means movement, influence, and another season behind the walls.*

### PARTY-14: 6.12, Recommended First Party box

**§1 restated contrast. Recommended. Second pass.** The box is headed 'Recommended First Party'; the closing line restates it.

*Line 2669, under "SPI General Talents".* Dependencies: none.

**Current**

> > **Recommended First Party:** For your first full-rules party, build a **Human Fighter (Soldier)**, an **Elf Ranger (Scout)**, a **Dwarf Cleric (Soldier)**, and a **Halfling Rogue (Smuggler)**, each using **Starting Package A**. This party provides front-line pressure and protection, ranged offence and control, healing and support, and mobility and objective utility. This is a recommendation, not a requirement.

**Proposed**

> > **Recommended First Party:** For your first full-rules party, build a **Human Fighter (Soldier)**, an **Elf Ranger (Scout)**, a **Dwarf Cleric (Soldier)**, and a **Halfling Rogue (Smuggler)**, each using **Starting Package A**. This party provides front-line pressure and protection, ranged offence and control, healing and support, and mobility and objective utility.

### PARTY-13: 6.13, introduction

**§12 jargon. Recommended. Second pass.** 'Talent ecosystem' is product jargon; 'defines a distinct' is padding.

*Line 2673, under "6.13 Hero Classes".* Dependencies: none.

**Current**

> Each class defines a distinct battlefield role, resource model, and talent ecosystem. Class talents are mechanically explicit and use the standard timing, action, and reaction rules of **Heraldry Skirmish**.

**Proposed**

> Each class has its own battlefield role, resources, and talents. Class talents are mechanically explicit and use the standard timing, action, and reaction rules of **Heraldry Skirmish**.

### PARTY-15: 6.13, Fighter

**§7 repeated template. Recommended. Second pass.** Seven class entries open 'A [Class] is forged / bred / built / schooled / formed / bound / handed'. This varies three (PARTY-15 to PARTY-17); also drops 'the only thing that matters'.

*Line 2746, under "Fighter [1/5 Complexity]".* Dependencies: art catalog quote.

**Current**

> *A Fighter is forged in places where hesitation gets people killed. Drill, repetition, and hard lessons carve in the instinct to hold ground when holding it is the only thing that matters. They have watched lines collapse, and they know to the heartbeat how long one can stand before it does.*

**Proposed**

> *Fighters come from places where hesitation gets people killed. Drill, repetition, and hard lessons carve in the instinct to hold ground when nothing else will do. They have watched lines collapse, and they know to the heartbeat how long one can stand before it does.*

### PARTY-16: 6.13, Ranger

**§7 repeated template. Recommended. Second pass.** See PARTY-15.

*Line 2894, under "Ranger [3/5 Complexity]".* Dependencies: art catalog quote.

**Current**

> *A Ranger is schooled by ground that kills the careless. Tracks, wind, and distance tell them what others miss entirely. They learn to act before danger closes the gap, and to strike from where the enemy cannot answer.*

**Proposed**

> *A Ranger trains on ground that kills the careless. Tracks, wind, and distance tell them what others miss entirely. They learn to act before danger closes the gap, and to strike from where the enemy cannot answer.*

### PARTY-17: 6.13, Wizard

**§7 repeated template. Recommended. Second pass.** See PARTY-15; also joins the passive closing sentence to the one before.

*Line 3008, under "Wizard [4/5 Complexity]".* Dependencies: art catalog quote.

**Current**

> *A Wizard is formed through study that most would not endure. Fragments of knowledge, careful notes, and repeated failure shape their craft. Power is taken apart, understood, and rebuilt with precision.*

**Proposed**

> *A Wizard has endured study that most would not. Fragments of knowledge, careful notes, and repeated failure shape the craft, and the Wizard takes power apart, understands it, and rebuilds it with precision.*

## Section 7: treasure, item lore, and item wording

### ITEM-12: 7.6, second paragraph

**§3 saying, §7 repeated openings. Recommended. Second pass.** Four 'may' sentences, then an aphorism with a triad as the closer.

*Line 3441, under "7.6 Treasure Tables".* Dependencies: none.

**Current**

> *Adventurers return to the ruins because coin keeps breath in the body. It buys bread, lamp oil, splints, armour, apothecary work, chapel rites, hired blades, and one more season behind a wall. A relic may ransom a village. It may also ruin one. A saint's ring may pay a healer. A king's cup may wake the court buried with it. Wealth is leverage, temptation, and tomorrow's trouble made bright enough to carry home.*

**Proposed**

> *Adventurers return to the ruins because coin keeps breath in the body. It buys bread, lamp oil, splints, armour, apothecary work, chapel rites, hired blades, and one more season behind a wall. A relic may ransom a village or ruin one. A saint's ring may pay a healer, and a king's cup may wake the court buried with it.*

### ITEM-13: 7.17.3, The Hollow Crown's Writ

**repeated phrase. Recommended. Second pass.** 'Others, less reassuringly, no longer do' already closes the Hollow Crown legend in 1.3.7.

*Line 4896, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> *A sealed document written in a language no living scholar reads fluently, bearing a seal that has no face. Some Ashland constructs still answer to it. Others, less reassuringly, do not.*

**Proposed**

> *A sealed document written in a language no living scholar reads fluently, bearing a seal that has no face. Some Ashland constructs still answer to it, though not all of them.*

### ITEM-01: 7.17.3, The Hollow Crown

**§2 closer. Recommended. First pass.** 'The distinction matters' is the stock closer. The rewrite keeps the contrast, which here carries the point, and keeps the warning that it will matter later.

*Line 4906, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> *The crown of the last sovereign of the fallen empires. No personal name survives. The statues that wore it have no faces. Their tomb has never been found. You have found their crown. This is not the same thing, and the distinction matters, but perhaps not yet.*

**Proposed**

> *The crown of the last sovereign of the fallen empires. No personal name survives. The statues that wore it have no faces. Their tomb has never been found. You have found their crown, which is not the same as finding them. In time, the difference will matter.*

### ITEM-14: 7.17.3, Kest's Iron Reliquary

**repeated phrase. Recommended. Second pass.** 'This one is warm.' stands alone in two entries; this one joins its sentence.

*Line 4921, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> *Mordain Kest was a warlord-exorcist who bound Monsters into iron reliquaries and forced ghosts to testify in court. Their reliquaries still surface in Ashland ruins, usually warm to the touch and never empty. This one is warm. Something pushes against the inside of the latch when you hold it in the dark.*

**Proposed**

> *Mordain Kest was a warlord-exorcist who bound Monsters into iron reliquaries and forced ghosts to testify in court. Their reliquaries still surface in Ashland ruins, usually warm to the touch and never empty. This one is warm, and something pushes against the inside of the latch when you hold it in the dark.*

### ITEM-07: 7.17.3, Kest's Iron Reliquary effect

**§12 'additionally'. Recommended. First pass.** Wording only; the effect is unchanged.

*Line 4923, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> **Effect:** Once per adventure, when you are adjacent to an enemy and spend **[1 AP]**, you may open the reliquary and release the bound spirit within. That enemy suffers **2d8 necrotic damage**, then must pass a **SPI Check** against **12**. **Failure:** They become **Frightened** until the end of their next activation. After use, the reliquary is empty until the next adventure, when it is found to contain something again. It is always warm. Additionally, while you wear Kest's Iron Reliquary you may spend **[1 AP]** to end **Cursed** on yourself or one ally within **2"**.

**Proposed**

> **Effect:** Once per adventure, when you are adjacent to an enemy and spend **[1 AP]**, you may open the reliquary and release the bound spirit within. That enemy suffers **2d8 necrotic damage**, then must pass a **SPI Check** against **12**. **Failure:** They become **Frightened** until the end of their next activation. After use, the reliquary is empty until the next adventure, when it is found to contain something again. It is always warm. While you wear Kest's Iron Reliquary, you may also spend **[1 AP]** to end **Cursed** on yourself or one ally within **2"**.

### ITEM-08: 7.17.3, Saint Cael's Burning Seal effect

**§12 'additionally'. Recommended. First pass.** Wording only; the effect is unchanged.

*Line 4953, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> **Effect:** This weapon deals **holy** damage. While wielding Saint Cael's Burning Seal, once per adventure when you are within **2"** of a scenario-marked threshold, bridge, ford, gate, or archway and you apply **AV** or use **Parry** against an **Undead** or **Fiend**, you may treat each **AD** die or retained **Parry** base die as its maximum natural result instead of rolling it. Roll any exploding **Parry** bonus dice and resolve **Riposte** normally. Additionally, **Undead** and **Fiends** that attack you while you are within **2"** of such a threshold suffer **1d6 holy damage** after their attack resolves. While wielding Saint Cael's Burning Seal you may spend **[1 AP]** to end **Cursed** on yourself or one ally within **2"**.

**Proposed**

> **Effect:** This weapon deals **holy** damage. While wielding Saint Cael's Burning Seal, once per adventure when you are within **2"** of a scenario-marked threshold, bridge, ford, gate, or archway and you apply **AV** or use **Parry** against an **Undead** or **Fiend**, you may treat each **AD** die or retained **Parry** base die as its maximum natural result instead of rolling it. Roll any exploding **Parry** bonus dice and resolve **Riposte** normally. **Undead** and **Fiends** that attack you while you are within **2"** of such a threshold also suffer **1d6 holy damage** after their attack resolves. While wielding Saint Cael's Burning Seal you may spend **[1 AP]** to end **Cursed** on yourself or one ally within **2"**.

### ITEM-15: 7.17.3, Ysolde Vane's Marginalia

**§2 fragments. Recommended. Second pass.** Two 'always' closers joined.

*Line 4975, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> *Handwriting that matches no living scribe appears in the margins of scrolls that have been near this document. The notes are always useful. They are always in blood.*

**Proposed**

> *Handwriting that matches no living scribe appears in the margins of scrolls that have been near this document. The notes are always useful, and always written in blood.*

### ITEM-04: 7.17.3, Salttide's Counting Stone

**§2 fragments. Optional. First pass.** Optional. Merges two of the three closing fragments; the dry last line stays.

*Line 5052, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> *The stone Edrava Salttide used to count ships that should have paid their toll. Sailors still see them at low winter tide, counting. The stone counts everything now. It remembers every debt. It is very patient.*

**Proposed**

> *The stone Edrava Salttide used to count ships that should have paid their toll. Sailors still see them at low winter tide, counting. The stone counts everything now and remembers every debt. It is very patient.*

### ITEM-02: 7.17.3, Old Wode's Iron-Shod Staff

**§2 fragments. Recommended. First pass.** A one-phrase fragment ('Three times.') folds into the sentence it belongs to.

*Line 5076, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> *An iron-shod walking staff that has been struck against standing stones. Three times. The strikes are still there. Three dents in the iron cap, each one slightly warmer than the rest of the metal.*

**Proposed**

> *An iron-shod walking staff that has been struck three times against standing stones. The strikes are still there: three dents in the iron cap, each one slightly warmer than the rest of the metal.*

### ITEM-03: 7.17.3, The Three-Strike Staff

**§2 fragments. Recommended. First pass.** Three fragments in a row.

*Line 5099, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> *Old Wode of the Antlered Path struck the standing stones three times at the end of the first post-Fall winter and returned with the agreement under which the Greenmark accepts Greythorn's autumn tithe. The agreement has never been written down. The forest has never broken it. This is the staff. The dents are there. The iron cap is still warm.*

**Proposed**

> *Old Wode of the Antlered Path struck the standing stones three times at the end of the first post-Fall winter and returned with the agreement under which the Greenmark accepts Greythorn's autumn tithe. The agreement has never been written down. The forest has never broken it. This is the staff, dents and all, and the iron cap is still warm.*

### ITEM-09: 7.17.3, Karnessa's Iron Seal effect

**§12 'additionally'. Recommended. First pass.** Wording only; the effect is unchanged.

*Line 5124, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> **Effect:** Once per adventure, when a Summon you control would be reduced to **0 HP**, you may spend **[0 AP]** to press Karnessa's Seal against them. This is a **Reaction**; declare it before that source's damage dice and commit its once-per-adventure use under **4.5**. That Summon is instead set to **1 HP**. Additionally, while wearing this Seal, you gain **+1** on **SPI Checks** made to resist the effects of **Undead** and **Fiend** Special Abilities.

**Proposed**

> **Effect:** Once per adventure, when a Summon you control would be reduced to **0 HP**, you may spend **[0 AP]** to press Karnessa's Seal against them. This is a **Reaction**; declare it before that source's damage dice and commit its once-per-adventure use under **4.5**. That Summon is instead set to **1 HP**. While wearing this Seal, you also gain **+1** on **SPI Checks** made to resist the effects of **Undead** and **Fiend** Special Abilities.

### ITEM-05: 7.17.3, Karnessa's Binding

**§2 repeated closer. Recommended. First pass.** 'It is X. It is always X.' is used as the closer on several relics (also ITEM-06 and SCEN-01); this keeps the fact once.

*Line 5144, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> *The thing that leaked through the vault walls when Karnessa Iron-Vein sealed it is not described in any surviving record. The seal held. That is what the records say. The records say it with the tone of people who are very grateful and do not intend to investigate further. Karnessa's Binding is the principle of that seal made portable. It is cold. It is always cold.*

**Proposed**

> *The thing that leaked through the vault walls when Karnessa Iron-Vein sealed it is not described in any surviving record. The seal held. That is what the records say. The records say it with the tone of people who are very grateful and do not intend to investigate further. Karnessa's Binding is the principle of that seal made portable, and it is always cold.*

### ITEM-10: 7.17.3, Bell-Shard Charm effect

**§12 'additionally', §18 'functions as'. Recommended. First pass.** 'Functions as' where 'is' says the same thing. (The Monster abilities that 'function as' another ability keep that wording, because there it means 'use the rules of'.)

*Line 5160, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> **Effect:** This item functions as an early warning system. When any **Undead** Monster becomes **Awake** within **12"** of you, the Charm chimes. You immediately become aware of that Monster's approximate location and that their Wake-Up condition has been met. You may then take a **[0 AP Reaction]**, even outside your activation, to make an **INT Check** against **12**. This Check does not require the Monster to be **Hidden** or in your **LOS**. On a success, the Monster loses **Hidden**, if applicable, and you know their exact position until the end of the round. Additionally, you gain **+1** on **SPI Checks** made to resist **Frightened** from **Undead** sources.

**Proposed**

> **Effect:** This item is an early warning system. When any **Undead** Monster becomes **Awake** within **12"** of you, the Charm chimes. You immediately become aware of that Monster's approximate location and that their Wake-Up condition has been met. You may then take a **[0 AP Reaction]**, even outside your activation, to make an **INT Check** against **12**. This Check does not require the Monster to be **Hidden** or in your **LOS**. On a success, the Monster loses **Hidden**, if applicable, and you know their exact position until the end of the round. Additionally, you gain **+1** on **SPI Checks** made to resist **Frightened** from **Undead** sources.

### ITEM-11: 7.17.3, Bell-Shard Charm effect

**§12 'additionally'. Recommended. First pass.** Wording only; the effect is unchanged.

*Line 5160, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> **Effect:** This item functions as an early warning system. When any **Undead** Monster becomes **Awake** within **12"** of you, the Charm chimes. You immediately become aware of that Monster's approximate location and that their Wake-Up condition has been met. You may then take a **[0 AP Reaction]**, even outside your activation, to make an **INT Check** against **12**. This Check does not require the Monster to be **Hidden** or in your **LOS**. On a success, the Monster loses **Hidden**, if applicable, and you know their exact position until the end of the round. Additionally, you gain **+1** on **SPI Checks** made to resist **Frightened** from **Undead** sources.

**Proposed**

> **Effect:** This item functions as an early warning system. When any **Undead** Monster becomes **Awake** within **12"** of you, the Charm chimes. You immediately become aware of that Monster's approximate location and that their Wake-Up condition has been met. You may then take a **[0 AP Reaction]**, even outside your activation, to make an **INT Check** against **12**. This Check does not require the Monster to be **Hidden** or in your **LOS**. On a success, the Monster loses **Hidden**, if applicable, and you know their exact position until the end of the round. You also gain **+1** on **SPI Checks** made to resist **Frightened** from **Undead** sources.

### ITEM-06: 7.17.3, The Bell's Tongue

**§2 repeated closer. Recommended. First pass.** Same closer as ITEM-05; two fragments merge.

*Line 5193, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> *No surviving record describes this item clearly. The accounts that come closest describe a clapper removed from a very old bell, cold as iron left in a winter river, that rings without being struck. The Voice Beneath the Bells is mentioned in all six Bastions' folk songs. No grave has ever been found. The Bell's Tongue has no provenance. It has always existed. It has always been cold.*

**Proposed**

> *No surviving record describes this item clearly. The accounts that come closest describe a clapper removed from a very old bell, cold as iron left in a winter river, that rings without being struck. The Voice Beneath the Bells is mentioned in all six Bastions' folk songs. No grave has ever been found. The Bell's Tongue has no provenance. It has always existed, and it has always been cold.*

## Section 8: Powers

### POWER-01: 8, first paragraph

**§1 contrast, §12 words. Recommended. First pass.** The Chapter 8 introduction is the most machine-sounding passage in the book. This paragraph drops the 'not a gift' contrast, 'transcend', 'the comforting heft of', and the participle chain, and keeps every claim.

*Line 5206, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *In the Dying Lands, magic is not a gift; it is a symptom of a broken world. To cast a spell is to reach into the cracks of reality and pull something volatile through, a transaction that always leaves a stain. The common folk know better than to trust it, having learned to fear its touch through generations of curses, twisted omens, and localized catastrophe. Sensible people cling to the safety of timber walls and the comforting heft of cold iron. But the desperate, the greedy, and the doomed recognize that surviving the ruins often requires bargaining with forces that transcend the swing of a blade.*

**Proposed**

> *In the Dying Lands, magic is a symptom of a broken world. To cast a spell is to reach into the cracks of reality and pull something volatile through, and the transaction always leaves a stain. Generations of curses, twisted omens, and local catastrophes have taught the common folk to fear its touch. Sensible people keep to timber walls and cold iron. The desperate, the greedy, and the doomed know that surviving the ruins often means bargaining with forces no blade can reach.*

### POWER-02: 8, second paragraph

**§16 sales word. Recommended. First pass.** 'Profoundly' is decoration.

*Line 5208, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Though the empires that once codified magic are ash, the Five Traditions survived the Fall, each scarred, perilous, and profoundly changed.*

**Proposed**

> *Though the empires that once codified magic are ash, the Five Traditions survived the Fall, each scarred, perilous, and much changed.*

### POWER-03: 8, Arcane Spells paragraph

**§1 contrast, §12 words, §15 riders. Recommended. First pass.** Drops 'less X than they are Y', 'cold calculus', 'sheer utility', and 'invariably'. Same claims, plainer verbs.

*Line 5210, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Arcane Spells are the hollow inheritance of the old world. Wizards are less miracle-workers than they are magical scavengers, piecing together forbidden principles from half-burned grimoires and the silent, dust-choked observatories where their predecessors still sit slumped in death. Their craft is a cold calculus of arcane formulae and unstable geometry. While Bastions tolerate them for their sheer utility, wizards are rarely loved, and are invariably blamed the moment a working leaks or the dead begin to walk.*

**Proposed**

> *Arcane Spells are the hollow inheritance of the old world. Wizards are scavengers, piecing together forbidden principles from half-burned grimoires and from silent, dust-choked observatories where their predecessors still sit slumped in death. Their craft runs on arcane formulae and unstable geometry. The Bastions tolerate wizards because they are useful, rarely love them, and blame them the moment a working leaks or the dead begin to walk.*

### POWER-04: 8, Divine Prayers paragraph

**§6 triads, §9 qualifiers. Recommended. First pass.** Plainer wording. 'An insult no scripture will name' and 'not yet worthy' match the wording 1.3.1 and 1.3.4 already use for the same two doctrines.

*Line 5212, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Divine Prayers are whispered into a largely empty sky. The old saints remain in the chapel rolls, but they answer fitfully, if they answer at all. A priest capable of calling down a true working is a rarity, famous enough to command reverence and terrifying enough to be feared. The faithful fracture over the silence: some preach that the gods retreated in disgust at an unnameable insult, while others insist mortal souls simply lack the worthiness to be heard. Regardless of the doctrine, divine magic is a desperate plea for a miracle, fuelled by fanatical devotion and answered only in blood and light.*

**Proposed**

> *Divine Prayers are whispered into a largely empty sky. The old saints remain in the chapel rolls, but they answer fitfully, if at all. A priest who can call down a true working is rare, and is feared as much as revered. The faithful split over the silence: some preach that the gods withdrew in disgust at an insult no scripture will name, and others that mortal souls are not yet worthy to be heard. Whatever the doctrine, a prayer is a desperate plea for a miracle, fuelled by fanatical devotion and answered only in blood and light.*

### POWER-05: 8, Druidic Rituals paragraph

**§16 sales language, §18 'act as'. Recommended. First pass.** Drops 'pulse with a terrifying, untamed vitality' and 'act as'. The 'do not mourn' contrast stays, because it marks the difference from the other traditions.

*Line 5214, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Druidic Rituals pulse with a terrifying, untamed vitality. Unlike the crumbling arcane or the silent divine, the magic of the wild has only grown more ferocious since the Fall. Druids commune with the encroaching forests, the choking bogs, and the violent storms. Their oldest circles do not mourn the dying world; instead, they teach that the earth is merely shedding mortal civilization like dead skin, and they act as the ruthless midwives to this violent rebirth.*

**Proposed**

> *Druidic Rituals draw on the wild, and while arcane learning crumbles and the gods stay silent, the wild has only grown more ferocious since the Fall. Druids commune with the encroaching forests, the choking bogs, and the violent storms. Their oldest circles do not mourn the dying world. They teach that the earth is shedding mortal civilization like dead skin, and they attend that violent rebirth like ruthless midwives.*

### POWER-06: 8, Sorceries paragraph

**§18 'represent', §12 words. Recommended. First pass.** 'Represent' becomes 'are'; drops 'terrible intimacy', 'raw, unrefined', 'paying for their output', and 'living conduits'.

*Line 5216, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Sorceries represent the most volatile and treacherous path to power, demanding a terrible intimacy with corruption. Some sorcerers are twisted by exposure to blighted ruin-sites, while others suffer from ancestral wounds reopening generations later, or strike infernal pacts in their darkest, most desperate hours. They wield raw, unrefined destruction, paying for their output in their own blood. Hanged in the streets of Sablekeep and treated with extreme caution everywhere else, sorcerers are living conduits of the world's sickness.*

**Proposed**

> *Sorceries are the most volatile and treacherous path to power, and the closest to corruption. Some sorcerers are twisted by exposure to blighted ruin-sites. Others carry ancestral wounds that reopen generations later, or strike infernal pacts in their most desperate hours. They wield raw destruction and pay for it in their own blood. Sablekeep hangs them in the streets, and everywhere else treats them with extreme caution. The world's sickness runs through every one of them.*

### POWER-07: 8, Psychic Abilities paragraph

**§1 contrast, §6 triad. Recommended. First pass.** Drops the 'do not study; they survive' contrast (the Psion class text already says 'not so much chosen as survived') and the padded triad.

*Line 5218, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Psychic Abilities remain the rarest, strangest, and least understood of the traditions. Psions do not study their power; they survive it. Their minds are cracked open by the long, suffocating pressure of sunken crypts, exposure to thought-eater nests, or sheer proximity to the alien things sleeping beneath the Undermarches. They emerge from the dark hearing the jagged thoughts of everyone around them. They are rarely hunted with the same religious fervour as sorcerers, but they are never trusted, for no one welcomes a person who can weaponize a memory or peel back the privacy of a skull.*

**Proposed**

> *Psychic Abilities remain the rarest and least understood of the traditions. A psion's mind is cracked open by the long, suffocating pressure of sunken crypts, by exposure to thought-eater nests, or by nearness to the alien things sleeping beneath the Undermarches, and it comes out of the dark hearing the jagged thoughts of everyone nearby. Psions are rarely hunted with the religious fervour reserved for sorcerers, but they are never trusted, because no one welcomes a person who can weaponize a memory or peel back the privacy of a skull.*

### POWER-08: 8.4, Tier 3 Divine Prayers introduction

**§1 contrast. Recommended. First pass.** 'Not asked but demanded' stated directly.

*Line 6207, under "Tier 3 Divine Prayers (d20)".* Dependencies: art catalog quote.

**Current**

> *At this height a prayer is not asked but demanded, and something always answers. Whether it is the god prayed to is a question the devout do not raise aloud.*

**Proposed**

> *At this height a prayer is a demand, and something always answers. Whether it is the god prayed to is a question the devout do not raise aloud.*

### POWER-09: 8.5, Tier 1 Sorceries introduction

**§1 contrast. Recommended. First pass.** Split 'does not X. It Y.' stated directly.

*Line 6359, under "Tier 1 Sorceries (d20)".* Dependencies: art catalog quote.

**Current**

> *Sorcery does not study. It bleeds. These first workings cost little blood and never fail, which is how they teach the unwary to want more.*

**Proposed**

> *Sorcery is learned by bleeding. These first workings cost little blood and never fail, which is how they teach the unwary to want more.*

## Section 9: Monsters

### MON-01: 9, introduction

**§1 contrast. Recommended. First pass.** Same move as LORE-15.

*Line 7552, under "9. Monsters".* Dependencies: none.

**Current**

> *Beyond the Bastions, the world is no longer governed by mortal law. Roads, courts, borders, shrines, and markets have been replaced by hunger, territory, instinct, old commands, and powers that survived the Fall better than humankind did. The creatures encountered in the Dying Lands are not interruptions to an expedition; they are the present owners of the world. Some are beasts made clever by scarcity, some are the dead still obeying ruined offices, some are mortals remade by pact, curse, rot, or worship, and some are older than the kingdoms whose bones they now inhabit. Each climate teaches its inhabitants a different form of cruelty, and each has produced creatures that use that cruelty as law. To enter the wilds is not to wander into empty land. It is to trespass.*

**Proposed**

> *Beyond the Bastions, the world is no longer governed by mortal law. Roads, courts, borders, shrines, and markets have been replaced by hunger, territory, instinct, old commands, and powers that survived the Fall better than humankind did. The creatures encountered in the Dying Lands are the present owners of the world. Some are beasts made clever by scarcity, some are the dead still obeying ruined offices, some are mortals remade by pact, curse, rot, or worship, and some are older than the kingdoms whose bones they now inhabit. Each climate teaches its inhabitants a different form of cruelty, and each has produced creatures that use that cruelty as law. To enter the wilds is not to wander into empty land. It is to trespass.*

### MON-02: 9, introduction

**§1 contrast, §2 closer. Recommended. First pass.** Split 'not X. It is Y.' closer.

*Line 7552, under "9. Monsters".* Dependencies: none.

**Current**

> *Beyond the Bastions, the world is no longer governed by mortal law. Roads, courts, borders, shrines, and markets have been replaced by hunger, territory, instinct, old commands, and powers that survived the Fall better than humankind did. The creatures encountered in the Dying Lands are not interruptions to an expedition; they are the present owners of the world. Some are beasts made clever by scarcity, some are the dead still obeying ruined offices, some are mortals remade by pact, curse, rot, or worship, and some are older than the kingdoms whose bones they now inhabit. Each climate teaches its inhabitants a different form of cruelty, and each has produced creatures that use that cruelty as law. To enter the wilds is not to wander into empty land. It is to trespass.*

**Proposed**

> *Beyond the Bastions, the world is no longer governed by mortal law. Roads, courts, borders, shrines, and markets have been replaced by hunger, territory, instinct, old commands, and powers that survived the Fall better than humankind did. The creatures encountered in the Dying Lands are not interruptions to an expedition; they are the present owners of the world. Some are beasts made clever by scarcity, some are the dead still obeying ruined offices, some are mortals remade by pact, curse, rot, or worship, and some are older than the kingdoms whose bones they now inhabit. Each climate teaches its inhabitants a different form of cruelty, and each has produced creatures that use that cruelty as law. To enter the wilds is to trespass.*

### MON-17: 9.7, Monster Roles

**§3 saying. Recommended. Second pass.** 'It is a promise about...' dresses up a plain function.

*Line 7805, under "Monster Roles".* Dependencies: none.

**Current**

> Every Monster fills a Role on the battlefield, named in brackets after their name. A Role is an encounter-building label and has no mechanical effect unless a rule explicitly says otherwise. It is a promise about how the Monster fights, so that a single glance tells a party what kind of trouble has woken up.

**Proposed**

> Every Monster fills a Role on the battlefield, named in brackets after their name. A Role is an encounter-building label and has no mechanical effect unless a rule explicitly says otherwise. It tells a party at a glance what kind of fight it has woken up.

### MON-18: 9.7, Monster Roles, Minion

**stock metaphor. Recommended. Second pass.** 'A tide' also describes goblins two pages later.

*Line 7807, under "Monster Roles".* Dependencies: none.

**Current**

> - **Minion:** The rank and file of the dark places. A Minion falls to a single clean blow, but they never come alone, and a tide of them can pull down a hero who treats them lightly.

**Proposed**

> - **Minion:** The rank and file of the dark places. A Minion falls to a single clean blow, but they never come alone, and enough of them can pull down a hero who treats them lightly.

### MON-19: 9.7, Monster Roles, Soldier

**§1 'neither X nor Y'. Recommended. Second pass.** 'Neither glass nor wall' states the same thing as two metaphors.

*Line 7808, under "Monster Roles".* Dependencies: none.

**Current**

> - **Soldier:** The dependable line-holder, trading blow for blow. A Soldier is the honest yardstick of a fair fight, neither glass nor wall.

**Proposed**

> - **Soldier:** The dependable line-holder, trading blow for blow. A Soldier is the yardstick of a fair fight: sturdy enough to hold a line, but not hard to bring down.

### MON-20: 9.7, Monster Roles, Skirmisher

**repeated phrase. Recommended. Second pass.** 'Before the answer lands' or 'comes' appears three times (also the Giant Bat and the Frost Wyvern, MON-21).

*Line 7809, under "Monster Roles".* Dependencies: none.

**Current**

> - **Skirmisher:** A darting, circling threat that strikes and slips away before the answer lands. A Skirmisher trades armour for speed and is deadliest in a pack that never holds still.

**Proposed**

> - **Skirmisher:** A darting, circling threat that strikes and slips away before anyone can strike back. A Skirmisher trades armour for speed and is deadliest in a pack that never holds still.

### MON-22: 9.7, Monster Roles, Cannon

**stock closer. Recommended. Second pass.** 'Or pay the price' is a stock phrase.

*Line 7810, under "Monster Roles".* Dependencies: none.

**Current**

> - **Cannon:** A fragile engine of sudden violence. A Cannon can fell a hero in a single dreadful moment, then shatter the instant a blade reaches them. Strike them first or pay the price.

**Proposed**

> - **Cannon:** A fragile engine of sudden violence. A Cannon can fell a hero in a single dreadful moment, then shatter the instant a blade reaches them, so strike them first.

### MON-23: 9.7, Monster Roles, Controller

**§1 'rather than', §3 saying. Recommended. Second pass.** 'The shape of the fight' is an abstract-noun saying; 'the weight of their arm' becomes plain.

*Line 7812, under "Monster Roles".* Dependencies: none.

**Current**

> - **Controller:** A bender of the battlefield, ruling through fear, venom, snare, and summoned horror rather than the weight of their arm. Their danger is the shape of the fight they force upon you.

**Proposed**

> - **Controller:** A Monster that bends the battlefield, fighting with fear, venom, snares, and summoned horrors more than with their own strength. They are dangerous because of the fight they force on you.

### MON-24: 9.7, Monster Roles, Elite

**'X given a body' template. Recommended. Second pass.** 'X given a body' or 'given a shape' appears eight times in the book; this pass varies five (MON-24 to MON-28). Also drops the doubled 'focused, concerted'.

*Line 7813, under "Monster Roles".* Dependencies: none.

**Current**

> - **Elite:** A small war given a single body. An Elite duels a seasoned hero as an equal and shrugs off scattered blows; only focused, concerted effort will bring one down. Their kind are rare and terrible, and seldom seen in numbers.

**Proposed**

> - **Elite:** A whole battle in one body. An Elite duels a seasoned hero as an equal and shrugs off scattered blows; only a concentrated attack will bring one down. Elites are rare and terrible, and seldom seen in numbers.

### MON-38: 9.7, Green Dragon

**§1 contrast. Recommended. Second pass.** 'They do not X; they Y' stated as a preference.

*Line 8188, under "Green Dragon [Elite]".* Dependencies: art catalog quote.

**Current**

> *Lesser kin to Maelthorn and the Greenmark's most practised liar, the green dragon is a serpentine tyrant the colour of deep moss, spine-crested, their breath a rolling, corrosive poison. They do not rampage; they manipulate, ruling a swathe of forest through fear and bargain. Lesser things bring them tribute in exchange for being spared a while longer.*

**Proposed**

> *Lesser kin to Maelthorn and the Greenmark's most practised liar, the green dragon is a serpentine tyrant the colour of deep moss, spine-crested, their breath a rolling, corrosive poison. They prefer manipulation to rampage, ruling a swathe of forest through fear and bargain. Lesser things bring them tribute in exchange for being spared a while longer.*

### MON-39: 9.7, Possessed Corpse

**§2 fragments. Recommended. Second pass.** A two-word closing fragment joined to its sentence.

*Line 8264, under "Possessed Corpse [Minion]".* Dependencies: art catalog quote.

**Current**

> *Not all the Ashlands' dead rose by design. A possessed corpse is a body worn by something that crept in from the dark between worlds, lurching on borrowed legs toward a wrong, jerking purpose. Their grip does not tire, and they burst in a reek of corruption when they finally fall. Whatever rides them does not speak. They only reach.*

**Proposed**

> *Not all the Ashlands' dead rose by design. A possessed corpse is a body worn by something that crept in from the dark between worlds, lurching on borrowed legs toward a wrong, jerking purpose. Their grip does not tire, and they burst in a reek of corruption when they finally fall. Whatever rides them does not speak, and the body only reaches.*

### MON-03: 9.7, Wererat

**§2 repeated closer. Recommended. First pass.** 'One is X; many are Y' closes seven Monster entries. This keeps the Goblin, Dire Wolf, and Ratkin Warrior versions and trims four (MON-03 to MON-06).

*Line 8301, under "Wererat [Skirmisher]".* Dependencies: art catalog quote.

**Current**

> *Where the Ashlands meet the old sewers and undercrofts, the wererat thrives, a hunched, plague-grey shapeshifter scurrying between man and rat-thing. They bite, then skitter back into the dark, leaving filth-fever in every wound. Mundane blades barely mark them. One wererat is a nuisance; a nest of them is an outbreak.*

**Proposed**

> *Where the Ashlands meet the old sewers and undercrofts, the wererat thrives, a hunched, plague-grey shapeshifter scurrying between man and rat-thing. They bite, then skitter back into the dark, leaving filth-fever in every wound. Mundane blades barely mark them. A nest of them is an outbreak.*

### MON-30: 9.7, Forsaken Knight

**§2 closer. Recommended. Second pass.** The closer restates the sentence before it.

*Line 8480, under "Forsaken Knight [Soldier]".* Dependencies: art catalog quote.

**Current**

> *Dead chivalry in spectral plate, the forsaken knight advances through the ash with a flamberge wreathed in grave-light. They parry with a lifetime's drill written into bone and cannot be slowed or turned aside. Bound by an oath they can no longer recall, they follow Veyr's banner into every fight. Their honour has curdled into compulsion.*

**Proposed**

> *Dead chivalry in spectral plate, the forsaken knight advances through the ash with a flamberge wreathed in grave-light. They parry with a lifetime's drill written into bone and cannot be slowed or turned aside. Bound by an oath they can no longer recall, they follow Veyr's banner into every fight.*

### MON-04: 9.7, Kobold

**§2 repeated closer. Recommended. First pass.** See MON-03.

*Line 8604, under "Kobold [Minion]".* Dependencies: art catalog quote.

**Current**

> *Knee-high reptilian scavengers with dull scales and dingy picks, kobolds are the Undermarches' scuttling vermin-folk. One alone is nothing; a chittering mob of them, dragging traps and loosing slings from the dark, is a real danger. They know every tunnel and trust not one. Where a single kobold shows themselves, a whole warren is watching.*

**Proposed**

> *Knee-high reptilian scavengers with dull scales and dingy picks, kobolds are the Undermarches' scuttling vermin-folk. A chittering mob of them, dragging traps and loosing slings from the dark, is a real danger. They know every tunnel and trust not one. Where a single kobold shows themselves, a whole warren is watching.*

### MON-07: 9.7, Frozen Skeleton

**§2 repeated closer. Recommended. First pass.** 'There are always more' closes three undead Minion entries. The Undead Warrior keeps it; this entry already calls them 'countless'.

*Line 8992, under "Frozen Skeleton [Minion]".* Dependencies: art catalog quote.

**Current**

> *Rimed in blue frost, a sword welded to their hand by ice, a frozen skeleton is one of the Pale City's countless dead, still standing the post they were given. They guard avenues that have not seen a living census in centuries. The cold preserves them whole; they will hold that post when the last warm thing in the world goes out. There are always more under the snow.*

**Proposed**

> *Rimed in blue frost, a sword welded to their hand by ice, a frozen skeleton is one of the Pale City's countless dead, still standing the post they were given. They guard avenues that have not seen a living census in centuries. The cold preserves them whole; they will hold that post when the last warm thing in the world goes out.*

### MON-26: 9.7, Ice Wraith

**'X given a body' template. Recommended. Second pass.** See MON-24.

*Line 9169, under "Ice Wraith [Cannon]".* Dependencies: art catalog quote.

**Current**

> *A knife of frozen malice given a drifting, translucent shape, the ice wraith is the spirit of someone who froze to death in the Pale City and never forgave it. Their touch saps warmth and thickens the blood to sludge. Steel passes clean through; only magic bites. They haunt the coldest avenues, hungry for the heat of anything still living.*

**Proposed**

> *A knife of frozen malice in a drifting, translucent shape, the ice wraith is the spirit of someone who froze to death in the Pale City and never forgave it. Their touch saps warmth and thickens the blood to sludge. Steel passes clean through; only magic bites. They haunt the coldest avenues, hungry for the heat of anything still living.*

### MON-31: 9.7, White Court Sentinel

**§2 repeated closer. Recommended. Second pass.** 'They do not pursue. They only X.' also closes the Undead Sentinel, which keeps it.

*Line 9188, under "White Court Sentinel [Brute]".* Dependencies: art catalog quote.

**Current**

> *A greatshield-bearing corpse-knight, the White Court sentinel is the dead nobility's bodyguard, planting themselves before their lords and refusing to give ground. They lend their frozen resolve to the soldiers around them and weather blows that would shatter a lesser guardian. They will not pursue and will not break. They only endure, as the court endures.*

**Proposed**

> *A greatshield-bearing corpse-knight, the White Court sentinel is the dead nobility's bodyguard, planting themselves before their lords and refusing to give ground. They lend their frozen resolve to the soldiers around them and weather blows that would shatter a lesser guardian. They will not pursue and will not break; they endure, as the court endures.*

### MON-12: 9.7, White Court Executioner

**§1 contrast. Recommended. First pass.** Split 'did not X. It only Y.' stated directly.

*Line 9265, under "White Court Executioner [Elite]".* Dependencies: art catalog quote.

**Current**

> *The White Court executioner carries out sentences the living court passed centuries ago, a towering headsman whose frost-rimed axe seeks the weakest throat on the field. They stride past the hale to reach the wounded and end them with grim efficiency. The court's justice did not die with the court. It only grew patient.*

**Proposed**

> *The White Court executioner carries out sentences the living court passed centuries ago, a towering headsman whose frost-rimed axe seeks the weakest throat on the field. They stride past the hale to reach the wounded and end them with grim efficiency. The court's justice outlived the court and only grew patient.*

### MON-21: 9.7, Frost Wyvern

**repeated phrase. Recommended. Second pass.** See MON-20.

*Line 9286, under "Frost Wyvern [Elite]".* Dependencies: art catalog quote.

**Current**

> *A lesser cousin of the great dragons, the frost wyvern is a winged reptile the colour of dirty ice, a venom-and-frost sting whipping at the end of their tail. They stoop from the white sky to harry and poison, then climb out of reach before the answer comes. They are cunning rather than wise. The Pale City's frozen peaks are crowded with their roosts.*

**Proposed**

> *A lesser cousin of the great dragons, the frost wyvern is a winged reptile the colour of dirty ice, a venom-and-frost sting whipping at the end of their tail. They stoop from the white sky to harry and poison, then climb out of reach again. They are cunning rather than wise. The Pale City's frozen peaks are crowded with their roosts.*

### MON-25: 9.7, White Dragon

**'X given a body' template. Recommended. Second pass.** See MON-24.

*Line 9348, under "White Dragon [Elite]".* Dependencies: art catalog quote.

**Current**

> *Visath's feral get, the white dragon is an ice-crusted wyrm whose breath flash-freezes whatever it touches. Less cunning than their kin but no less lethal, they are pure predatory cold given wings and an appetite. They nest in the lesser spires and suffer the White Court about them as courtiers. When they descend, the city's eternal winter only deepens.*

**Proposed**

> *Visath's feral get, the white dragon is an ice-crusted wyrm whose breath flash-freezes whatever it touches. Less cunning than their kin but no less lethal, they are predatory cold with wings and an appetite. They nest in the lesser spires and suffer the White Court about them as courtiers. When they descend, the city's eternal winter only deepens.*

### MON-32: 9.7, Imp

**stock closer. Recommended. Second pass.** 'A herald of worse to come' is stock.

*Line 9391, under "Imp [Skirmisher]".* Dependencies: art catalog quote.

**Current**

> *Knee-high and bat-winged, a barbed venomous tail lashing behind them, the imp flits about the Sun-Drowned tombs as the spiteful servant of darker things. They dart in to sting and wheel away cackling, untroubled by the desert's heat or their own infernal fire. Alone they are more nuisance than threat. They are also a herald of worse to come.*

**Proposed**

> *Knee-high and bat-winged, a barbed venomous tail lashing behind them, the imp flits about the Sun-Drowned tombs as the spiteful servant of darker things. They dart in to sting and wheel away cackling, untroubled by the desert's heat or their own infernal fire. Alone they are more nuisance than threat, but worse usually follows them.*

### MON-08: 9.7, Skeleton Warrior

**§2 repeated closer. Recommended. First pass.** See MON-07.

*Line 9408, under "Skeleton Warrior [Minion]".* Dependencies: art catalog quote.

**Current**

> *A skeleton warrior stands at the post they were set in the year of their death, a sun-bleached frame in the corroded bronze of a priest-king's guard. They still hold the weapon they carried in life, waiting on an order that has not come in centuries. When intruders breach the sealed courts the order arrives at last, and the bones remember their drill. There are always more, ranked in the dark behind them.*

**Proposed**

> *A skeleton warrior stands at the post they were set in the year of their death, a sun-bleached frame in the corroded bronze of a priest-king's guard. They still hold the weapon they carried in life, waiting on an order that has not come in centuries. When intruders breach the sealed courts the order arrives at last, and the bones remember their drill, rank on rank of them in the dark.*

### MON-10: 9.7, Desert Naga

**§2 fragments. Recommended. First pass.** Two fragments become one sentence; the ambiguity of 'answer' is kept.

*Line 9552, under "Desert Naga [Controller]".* Dependencies: art catalog quote.

**Current**

> *A great serpent with an almost-human face and the patient cunning of something very old, the desert naga coils among the tomb-pillars. They spit venom from a distance and crush what comes close, hexing the strong into an unnatural sleep. The priest-kings kept them as guardians and oracles. They guard still. They no longer answer.*

**Proposed**

> *A great serpent with an almost-human face and the patient cunning of something very old, the desert naga coils among the tomb-pillars. They spit venom from a distance and crush what comes close, hexing the strong into an unnatural sleep. The priest-kings kept them as guardians and oracles. They still guard, but they no longer answer.*

### MON-11: 9.7, Fire Elemental

**§2 closer. Recommended. First pass.** Restates the first sentence ('scorches whatever strikes them').

*Line 9570, under "Fire Elemental [Cannon]".* Dependencies: art catalog quote.

**Current**

> *A roaring man-shape of living flame, white-hot at the core and shedding embers at the edges, the fire elemental sets alight everything they touch and scorches whatever strikes them. Water and ice are their only checks; the desert sun is their cradle. They draw a trail of cinders across the tomb-floors. To lay hands on them is to burn.*

**Proposed**

> *A roaring man-shape of living flame, white-hot at the core and shedding embers at the edges, the fire elemental sets alight everything they touch and scorches whatever strikes them. Water and ice are their only checks; the desert sun is their cradle. They draw a trail of cinders across the tomb-floors.*

### MON-09: 9.7, Giant Skeleton

**§2 closer. Recommended. First pass.** 'They guard it still' closes five guardian entries; this one adds nothing to the carving detail before it.

*Line 9587, under "Giant Skeleton [Brute]".* Dependencies: art catalog quote.

**Current**

> *A looming framework of fused bone twice a man's height, the giant skeleton is what remains of something that was never entirely natural and is far less so now. They move with grinding deliberation, sweeping aside anything in their path with fists like falling masonry. Tomb-city carvings show their kind kneeling before the priest-kings; none show them standing. Whatever they were raised to guard, they guard it still.*

**Proposed**

> *A looming framework of fused bone twice a man's height, the giant skeleton is what remains of something that was never entirely natural and is far less so now. They move with grinding deliberation, sweeping aside anything in their path with fists like falling masonry. Tomb-city carvings show their kind kneeling before the priest-kings; none show them standing.*

### MON-33: 9.7, Tomb Guardian

**§2 fragments. Recommended. Second pass.** Paired closer joined.

*Line 9644, under "Tomb Guardian [Soldier]".* Dependencies: art catalog quote.

**Current**

> *A faceless construct of gilded stone and ritual, the tomb guardian was built to defend the priest-kings' seals and is tireless in that one duty. They plant themselves at a threshold and cannot be hurried or frightened. They have held one doorway for a thousand years. They will hold it for a thousand more.*

**Proposed**

> *A faceless construct of gilded stone and ritual, the tomb guardian was built to defend the priest-kings' seals and is tireless in that one duty. They plant themselves at a threshold and cannot be hurried or frightened. They have held one doorway for a thousand years and will hold it for a thousand more.*

### MON-34: 9.7, Manticore

**repeated closer. Recommended. Second pass.** 'The X is their larder / barracks / nursery / hunting ground' closes seven entries, two with 'larder'. This and MON-35 trim two; the Elder Vrymk keeps 'larder'.

*Line 9687, under "Manticore [Elite]".* Dependencies: art catalog quote.

**Current**

> *A monstrous fusion of lion's body, bat's wings, and a man's leering face, the manticore flicks volleys of iron spikes from their lashing tail. They wait where the dune-road narrows and rain barbs on whatever they have trapped. They savour a meal that begged first. The Sun-Drowned's loneliest trails are their larder.*

**Proposed**

> *A monstrous fusion of lion's body, bat's wings, and a man's leering face, the manticore flicks volleys of iron spikes from their lashing tail. They wait where the dune-road narrows and rain barbs on whatever they have trapped. They savour a meal that begged first.*

### MON-05: 9.7, Swamp Goblin

**§2 repeated closer. Recommended. First pass.** See MON-03; also removes a verbless fragment.

*Line 9775, under "Swamp Goblin [Minion]".* Dependencies: art catalog quote.

**Current**

> *Slime-streaked cousins of their forest kin, swamp goblins paddle The Mire's channels and blow poisoned darts from the reeds. They melt into the cover and strike from wherever the water hides them. A nuisance one at a time, a hazard in a swarm. They strip the drowned for trinkets and teeth.*

**Proposed**

> *Slime-streaked cousins of their forest kin, swamp goblins paddle The Mire's channels and blow poisoned darts from the reeds. They melt into the cover and strike from wherever the water hides them, and in a swarm they are dangerous. They strip the drowned for trinkets and teeth.*

### MON-06: 9.7, Stirge

**§2 repeated closer. Recommended. First pass.** See MON-03.

*Line 9814, under "Stirge [Minion]".* Dependencies: art catalog quote.

**Current**

> *A bloated mosquito-thing the size of a cat, the stirge carries a needle proboscis and a belly that swells red with stolen blood. They dart in, latch on, and drain until they are pried loose. The Mire's dusk air hums with them. One is an itch; a swarm is exsanguination.*

**Proposed**

> *A bloated mosquito-thing the size of a cat, the stirge carries a needle proboscis and a belly that swells red with stolen blood. They dart in, latch on, and drain until they are pried loose. The Mire's dusk air hums with them, and a swarm can drain a body dry.*

### MON-36: 9.7, Lizardfolk Hunter

**repeated closer. Recommended. Second pass.** 'By the time X, you are already Y' closes several entries, and the first sentence already drags prey into the water.

*Line 9869, under "Lizardfolk Hunter [Cannon]".* Dependencies: art catalog quote.

**Current**

> *A barbed harpoon in their claws, the lizardfolk hunter stalks The Mire's margins, dragging prey off the walkways and into the water where every advantage is their own. They strike from cover and the reeds, unseen until the line snaps taut. Patient and silent, they wait out the careless. By the time they move, you are already in the water.*

**Proposed**

> *A barbed harpoon in their claws, the lizardfolk hunter stalks The Mire's margins, dragging prey off the walkways and into the water where every advantage is their own. They strike from cover and the reeds, unseen until the line snaps taut. Patient and silent, they wait out the careless.*

### MON-37: 9.7, Swamp Hag

**repeated phrase. Recommended. Second pass.** The Night Hag has the same 'They bargain, they lie, and they...' triad; this keeps all three claims in a different shape.

*Line 10009, under "Swamp Hag [Controller]".* Dependencies: art catalog quote.

**Current**

> *A warty, weed-haired crone, the swamp hag poles their way through The Mire cursing all they meet, slipping half into the spirit-world when cornered. Their stench chokes out hope. They bargain, they lie, and they feed on misery. The loneliest hut in the mire is theirs, and it is never empty for long.*

**Proposed**

> *A warty, weed-haired crone, the swamp hag poles their way through The Mire cursing all they meet, slipping half into the spirit-world when cornered. Their stench chokes out hope. They feed on misery, and every bargain they offer is a lie. The loneliest hut in the mire is theirs, and it is never empty for long.*

### MON-14: 9.7, The Ancient Void Dragon

**§1 contrast. Optional. First pass.** Optional. 'Neither X nor Y but Z.' If the contrast with the fire and frost dragons is wanted, decline.

*Line 10183, under "The Ancient Void Dragon [Boss]".* Dependencies: player aid pa02; art catalog quote.

**Current**

> *Older than the Fall and perhaps its cause, the Ancient Void Dragon is a wound in the shape of a wyrm, their scales drinking the light from the air around them. Their breath neither burns nor freezes but unmakes, peeling away substance until nothing is left. Stars seem to dim where they pass. The wise do not speak their name, and the dead do not speak at all.*

**Proposed**

> *Older than the Fall and perhaps its cause, the Ancient Void Dragon is a wound in the shape of a wyrm, their scales drinking the light from the air around them. Their breath unmakes, peeling away substance until nothing is left. Stars seem to dim where they pass. The wise do not speak their name, and the dead do not speak at all.*

### MON-27: 9.7, Avatar of the Old Growth

**'X given a body' template. Recommended. Second pass.** See MON-24; the Dryad Grovewarden keeps 'the will of an old tree given a shape'.

*Line 10251, under "Avatar of the Old Growth [Boss]".* Dependencies: player aid pa02; art catalog quote.

**Current**

> *A towering shape of ancient trunk and grasping root, bark-skinned and crowned with a tangle of antlered branches, the Avatar of the Old Growth is the will of the deep forest given a body to act through. They call the lesser green things to their side and drown intruders in living wood. To kill them is to wound the Greenmark itself. The Greenmark does not forgive.*

**Proposed**

> *A towering shape of ancient trunk and grasping root, bark-skinned and crowned with a tangle of antlered branches, the Avatar of the Old Growth is the deep forest's will in a body it can act through. They call the lesser green things to their side and drown intruders in living wood. To kill them is to wound the Greenmark itself. The Greenmark does not forgive.*

### MON-29: 9.7, Avatar of the Old Growth

**§2 closer, 'to X is to Y'. Recommended. Second pass.** 'To X is to Y' plus a one-line closer.

*Line 10251, under "Avatar of the Old Growth [Boss]".* Dependencies: player aid pa02; art catalog quote.

**Current**

> *A towering shape of ancient trunk and grasping root, bark-skinned and crowned with a tangle of antlered branches, the Avatar of the Old Growth is the will of the deep forest given a body to act through. They call the lesser green things to their side and drown intruders in living wood. To kill them is to wound the Greenmark itself. The Greenmark does not forgive.*

**Proposed**

> *A towering shape of ancient trunk and grasping root, bark-skinned and crowned with a tangle of antlered branches, the Avatar of the Old Growth is the will of the deep forest given a body to act through. They call the lesser green things to their side and drown intruders in living wood. Killing them wounds the Greenmark itself, and the Greenmark does not forgive.*

### MON-35: 9.7, The Broodmother Prime

**repeated closer. Recommended. Second pass.** See MON-34; the first sentence already calls them the mother of every giant spider.

*Line 10274, under "The Broodmother Prime [Boss]".* Dependencies: player aid pa02; art catalog quote.

**Current**

> *In the deepest dark of the Undermarches squats the mother of every giant spider that plagues the deep, a bloated horror the size of a cottage, egg-sacs trailing from them that twitch with the unborn. They flood the field with their brood and bind the survivors in webs for later. Their venom stops a heart in a single beat. The deep, in the end, is their nursery.*

**Proposed**

> *In the deepest dark of the Undermarches squats the mother of every giant spider that plagues the deep, a bloated horror the size of a cottage, egg-sacs trailing from them that twitch with the unborn. They flood the field with their brood and bind the survivors in webs for later. Their venom stops a heart in a single beat.*

### MON-15: 9.7, Captain Veyr of the Forsaken

**§2 fragments. Recommended. First pass.** A one-phrase fragment joins its sentence.

*Line 10298, under "Captain Veyr of the Forsaken [Boss]".* Dependencies: player aid pa02; art catalog quote.

**Current**

> *Veyr was the empire's greatest captain, who swore their company would never break and held them to it past death itself. Now they lead the Forsaken in spectral plate, a duelist whose paired blades have not slowed since the empire fell. They rally their dead soldiers with a voice like a closing tomb. They no longer recall the war they are still fighting. Only the oath.*

**Proposed**

> *Veyr was the empire's greatest captain, who swore their company would never break and held them to it past death itself. Now they lead the Forsaken in spectral plate, a duelist whose paired blades have not slowed since the empire fell. They rally their dead soldiers with a voice like a closing tomb. They no longer recall the war they are still fighting, only the oath.*

### MON-16: 9.7, The Antlered Warden of the Tithe

**§1 contrast. Recommended. First pass.** Split 'does not come to X. They come to Y.' stated directly.

*Line 10364, under "The Antlered Warden of the Tithe [Boss]".* Dependencies: player aid pa02; art catalog quote.

**Current**

> *The antlered figure admitted to Greythorn's west gate each winter does not come to bargain when the tithe goes unpaid. They come to collect. A towering shape of bone-antler and living wood, they drag the indebted into their reach and call the wild court to witness. The forest has never broken the agreement, and it does not forgive those who do.*

**Proposed**

> *When the tithe goes unpaid, the antlered figure admitted to Greythorn's west gate each winter comes to collect. A towering shape of bone-antler and living wood, they drag the indebted into their reach and call the wild court to witness. The forest has never broken the agreement, and it does not forgive those who do.*

### MON-28: 9.7, The Voice Beneath the Bells

**'X given a body' template. Recommended. Second pass.** See MON-24.

*Line 10388, under "The Voice Beneath the Bells [Boss]".* Dependencies: player aid pa02; art catalog quote.

**Current**

> *Survivors describe a small figure at the edge of the torchlight, singing in a tongue that sounds like an old lullaby heard through water. Then the torch goes out. The Voice Beneath the Bells is grief given a child's shape and a drowned chapel's patience, and their song hollows out everyone who hears it. The bells they wait beneath have not rung in a very long time.*

**Proposed**

> *Survivors describe a small figure at the edge of the torchlight, singing in a tongue that sounds like an old lullaby heard through water. Then the torch goes out. The Voice Beneath the Bells is grief in a child's shape, with a drowned chapel's patience, and their song hollows out everyone who hears it. The bells they wait beneath have not rung in a very long time.*

### MON-13: 9.7, Visath the White

**§1 contrast. Recommended. First pass.** 'Does not merely X; it Y.' The ice survives in the same sentence.

*Line 10463, under "Visath the White [Boss]".* Dependencies: player aid pa02; art catalog quote.

**Current**

> *Visath is the Pale City's eternal winter wearing the body of a wyrm, a glacier with wings and a will. Their breath does not merely freeze; it stops time in the flesh, leaving victims locked mid-scream in the ice. They rule from the highest spire and suffer no warmth anywhere in their domain. Where they fly, the snow falls harder, as though the sky itself bows.*

**Proposed**

> *Visath is the Pale City's eternal winter wearing the body of a wyrm, a glacier with wings and a will. Their breath stops time in the flesh, leaving victims locked mid-scream in the ice. They rule from the highest spire and suffer no warmth anywhere in their domain. Where they fly, the snow falls harder, as though the sky itself bows.*

## Section 10: objectives, scenarios, and solo play

### SCEN-01: 10.2, Ashlands Secondary Objectives, the Reliquary

**§2 repeated closer. Recommended. First pass.** Same closer as ITEM-05; also gives the verbless second sentence a verb by joining it to the first.

*Line 11320, under "Climate 2: Ashlands Secondary Objectives (1d20)".* Dependencies: none.

**Current**

> *The Reliquary is warm to the touch. It is always warm. One of Mordain Kest's bindings, never recovered, surfacing again. Heroes who carry it report hearing a voice that does not belong to them.*

**Proposed**

> *The Reliquary is always warm to the touch: one of Mordain Kest's bindings, never recovered, surfacing again. Heroes who carry it report hearing a voice that does not belong to them.*

### SCEN-02: 10.4, Greenmark Scenario 2, Scenario-Specific Monster: Antlered Warden

**§1 contrast, §7 repeated openings. Recommended. First pass.** Keeps the correction (a reader may well expect Old Wode here) without the verbless opener.

*Line 12115, under "Scenario 2: The Whispering Grove".* Dependencies: figures FIG-13 to FIG-56 (41).

**Current**

> *Not Old Wode themselves. Old Wode does not stir for small intrusions. The Antlered Warden is the agreement's enforcement arm: a figure woven from the grove's oldest growth, robed in bark and grey moss, with antlers that have more branches than any natural animal. They do not speak. They do not negotiate. They maintain the terms.*

**Proposed**

> *This is not Old Wode, who does not stir for small intrusions. The Antlered Warden is the agreement's enforcement arm: a figure woven from the grove's oldest growth, robed in bark and grey moss, with antlers that have more branches than any natural animal. They do not speak. They do not negotiate. They maintain the terms.*

### SCEN-03: 10.4, Greenmark Scenario 2, Scenario-Specific Monster: Antlered Warden

**§7 repeated openings. Recommended. First pass.** Two parallel negatives merge.

*Line 12115, under "Scenario 2: The Whispering Grove".* Dependencies: figures FIG-13 to FIG-56 (41).

**Current**

> *Not Old Wode themselves. Old Wode does not stir for small intrusions. The Antlered Warden is the agreement's enforcement arm: a figure woven from the grove's oldest growth, robed in bark and grey moss, with antlers that have more branches than any natural animal. They do not speak. They do not negotiate. They maintain the terms.*

**Proposed**

> *Not Old Wode themselves. Old Wode does not stir for small intrusions. The Antlered Warden is the agreement's enforcement arm: a figure woven from the grove's oldest growth, robed in bark and grey moss, with antlers that have more branches than any natural animal. They do not speak or negotiate. They maintain the terms.*

### SCEN-06: 10.4, Ashlands Scenario 5, The Reliquary of Broken Saints

**§1 contrast. Recommended. First pass.** The negative half denies a claim nobody made.

*Line 12753, under "Scenario 5: The Reliquary of Broken Saints".* Dependencies: figures FIG-13 to FIG-56 (41); art catalog quote.

**Current**

> *Broken statues and smashed reliquaries fill the hall, and sanctified bone and silver remain in the wreckage, too holy to abandon and too valuable to leave. Sablekeep needs the relics to keep its braziers lit and its authority legal, and will pay to register every fragment. The dead here are not confused. They swore to guard these relics, and death has not released them from the oath.*

**Proposed**

> *Broken statues and smashed reliquaries fill the hall, and sanctified bone and silver remain in the wreckage, too holy to abandon and too valuable to leave. Sablekeep needs the relics to keep its braziers lit and its authority legal, and will pay to register every fragment. The dead here swore to guard these relics, and death has not released them from the oath.*

### SCEN-04: 10.4, Ashlands Scenario 6, The Iron-Vein Vault

**§2 fragments, §2 closer. Recommended. First pass.** A one-phrase fragment ('Until now.') joins its sentence.

*Line 12827, under "Scenario 6: The Iron-Vein Vault".* Dependencies: figures FIG-13 to FIG-56 (41); art catalog quote.

**Current**

> *The vault has been sealed for two generations. Karnessa Iron-Vein pressed their blood into the iron door when something inside began to leak through the walls, and the seal has held. Until now. Tremors along the imperial roads have cracked the outer binding, and something below is pushing. Sablekeep sends one party to reinforce the seal before whatever waits finishes their work; a rival patron sends another to open the vault and price what was sealed there. The vault does not care about either contract.*

**Proposed**

> *The vault has been sealed for two generations. Karnessa Iron-Vein pressed their blood into the iron door when something inside began to leak through the walls, and until now the seal has held. Tremors along the imperial roads have cracked the outer binding, and something below is pushing. Sablekeep sends one party to reinforce the seal before whatever waits finishes their work; a rival patron sends another to open the vault and price what was sealed there. The vault does not care about either contract.*

### SCEN-05: 10.4, Ashlands Scenario 6, The Iron-Vein Vault

**§2 closer. Recommended. First pass.** Most scenario introductions end on a wry one-line closer. This one, and SCEN-07 to SCEN-09, restate the sentence before them; the rest add a fact and stay.

*Line 12827, under "Scenario 6: The Iron-Vein Vault".* Dependencies: figures FIG-13 to FIG-56 (41); art catalog quote.

**Current**

> *The vault has been sealed for two generations. Karnessa Iron-Vein pressed their blood into the iron door when something inside began to leak through the walls, and the seal has held. Until now. Tremors along the imperial roads have cracked the outer binding, and something below is pushing. Sablekeep sends one party to reinforce the seal before whatever waits finishes their work; a rival patron sends another to open the vault and price what was sealed there. The vault does not care about either contract.*

**Proposed**

> *The vault has been sealed for two generations. Karnessa Iron-Vein pressed their blood into the iron door when something inside began to leak through the walls, and the seal has held. Until now. Tremors along the imperial roads have cracked the outer binding, and something below is pushing. Sablekeep sends one party to reinforce the seal before whatever waits finishes their work; a rival patron sends another to open the vault and price what was sealed there.*

### SCEN-11: 10.4, Undermarches Scenario 2, The Chasm Crossing

**§2 fragments. Recommended. Second pass.** Paired closer joined.

*Line 12994, under "Scenario 2: The Chasm Crossing".* Dependencies: figures FIG-13 to FIG-56 (41); art catalog quote.

**Current**

> *A chasm splits the caverns like a wound in the world, crossed only by narrow ledges in broken pieces. A Survey Map must reach the Lantern Council before Deepwarden's rivals can claim the new diggings. Things cling to the dark stone below the ledges and wait for a hand to shake. The Council wants the map. It does not ask what the things want.*

**Proposed**

> *A chasm splits the caverns like a wound in the world, crossed only by narrow ledges in broken pieces. A Survey Map must reach the Lantern Council before Deepwarden's rivals can claim the new diggings. Things cling to the dark stone below the ledges and wait for a hand to shake. The Council wants the map and does not ask what the things want.*

### SCEN-07: 10.4, Pale City Scenario 2, The Alchemist's Frozen Laboratory

**§2 closer. Recommended. First pass.** A stock closer; the guardians in the sentence before already carry the threat.

*Line 13466, under "Scenario 2: The Alchemist's Frozen Laboratory".* Dependencies: figures FIG-13 to FIG-56 (41); art catalog quote.

**Current**

> *In the ice-locked Silent District, north along the road out of Hearthhold, an alchemist's laboratory remains sealed under frost. The formula inside might be worth a village, and Hearthhold burns through everything it owns just to stay warm. The cold has preserved the benches, the bottles, the last mistakes, and the guardians left to watch them. Some things in that laboratory were never meant to thaw.*

**Proposed**

> *In the ice-locked Silent District, north along the road out of Hearthhold, an alchemist's laboratory remains sealed under frost. The formula inside might be worth a village, and Hearthhold burns through everything it owns just to stay warm. The cold has preserved the benches, the bottles, the last mistakes, and the guardians left to watch them.*

### SCEN-12: 10.4, Pale City Scenario 5, The Ice Wyrm's Hoard

**§2 closer. Recommended. Second pass.** Restates the sentence before it, and repeats the 'kind of listener' closer cut from the Sandwyrm (SCEN-09).

*Line 13665, under "Scenario 5: The Ice Wyrm's Hoard".* Dependencies: figures FIG-13 to FIG-56 (41); art catalog quote.

**Current**

> *The old stories put jewels and gold in a frozen cavern beneath the north road out of Hearthhold, and a wyrm coiled on top of them whose breath can stop a heart inside its own armour. Hearthhold needs the gold more than it fears the breath, which is the kind of arithmetic only the poorest Bastion does out loud. The second part of the story has never discouraged the first kind of listener.*

**Proposed**

> *The old stories put jewels and gold in a frozen cavern beneath the north road out of Hearthhold, and a wyrm coiled on top of them whose breath can stop a heart inside its own armour. Hearthhold needs the gold more than it fears the breath, which is the kind of arithmetic only the poorest Bastion does out loud.*

### SCEN-08: 10.4, Sun-Drowned Scenario 1, The Oasis Raiders

**§2 closer. Recommended. First pass.** Restates the two-contract point.

*Line 13819, under "Scenario 1: The Oasis Raiders [Intro]".* Dependencies: figures FIG-13 to FIG-56 (41); art catalog quote.

**Current**

> *A vital oasis south of the mountain passes has changed hands again, and raiders hold the wells, the shade, and the people too slow to flee. Saltspire sells water as sovereignty, and an oasis it does not control is a debt it cannot collect. One contract from the Well-Keepers says liberation. A rival contract says seizure. The water will not ask which seal is righteous.*

**Proposed**

> *A vital oasis south of the mountain passes has changed hands again, and raiders hold the wells, the shade, and the people too slow to flee. Saltspire sells water as sovereignty, and an oasis it does not control is a debt it cannot collect. One contract from the Well-Keepers says liberation. A rival contract says seizure.*

### SCEN-09: 10.4, Sun-Drowned Scenario 4, The Sandwyrm's Lair

**§2 closer. Recommended. First pass.** Restates the warning/inventory contrast the two sentences before it already make.

*Line 14019, under "Scenario 4: The Sandwyrm's Lair".* Dependencies: figures FIG-13 to FIG-56 (41); art catalog quote.

**Current**

> *Nomad legends speak of a vast shape beneath the dunes south of the passes, and a gullet lined with the treasure of everything they have swallowed. The nomads tell it as a warning. Saltspire's patrons hear it as an inventory and pay accordingly. The dunes do not distinguish between the two kinds of listener.*

**Proposed**

> *Nomad legends speak of a vast shape beneath the dunes south of the passes, and a gullet lined with the treasure of everything they have swallowed. The nomads tell it as a warning. Saltspire's patrons hear it as an inventory and pay accordingly.*

### SCEN-10: 10.4, Mire Scenario 1, Scenario-Specific Monster: Salttide's Shade

**§7 repeated openings. Recommended. First pass.** 'They watch' three times in a row.

*Line 14271, under "Scenario 1: The Reliquary of Edrava Salttide [Intro]".* Dependencies: figures FIG-13 to FIG-56 (41).

**Current**

> *Edrava Salttide has not finished counting. The Mire preserved them, and it is patient. The Shade does not speak. They watch the reliquary. They watch the water. They watch every hand that reaches for what belongs to them.*

**Proposed**

> *Edrava Salttide has not finished counting. The Mire preserved them, and it is patient. The Shade does not speak. They watch the reliquary, the water, and every hand that reaches for what belongs to them.*

### SCEN-13: 10.4, Mire Scenario 5, Salttide's Reckoning

**repeated closer. Recommended. Second pass.** Mire Scenario 1 already ends 'The water smells of salt. There is no ocean for eighty miles.'

*Line 14547, under "Scenario 5: Salttide's Reckoning".* Dependencies: figures FIG-13 to FIG-56 (41); art catalog quote.

**Current**

> *A curse lies over the sacred island like oil on water. Edrava Salttide has made a ritual of the place, the same ritual they once used to curse the harbours that refused their ships, now turned on the living who entered The Mire without paying the toll. The reeds bend toward the island. The water smells of brine, this far from any sea. Reedmarch sent one party to break the working, and let a rival sell the other a contract whose small print it has not read.*

**Proposed**

> *A curse lies over the sacred island like oil on water. Edrava Salttide has made a ritual of the place, the same ritual they once used to curse the harbours that refused their ships, now turned on the living who entered The Mire without paying the toll. The reeds bend toward the island. Reedmarch sent one party to break the working, and let a rival sell the other a contract whose small print it has not read.*

### SCEN-14: 10.5, introduction

**stock phrase. Recommended. Second pass.** 'The battlefield itself becomes the enemy' is stock. The replacement names what 1.1 and 10.5.6 say replaces the rival party.

*Line 14699, under "10.5 Solo and Cooperative Play".* Dependencies: player aid pa10.

**Current**

> Heraldry Skirmish may be played as a **solo** or **cooperative** game. In these modes, there is no rival adventuring party. Instead, the battlefield itself becomes the enemy. Solo and cooperative play use the normal core rules unless this section says otherwise.

**Proposed**

> Heraldry Skirmish may be played as a **solo** or **cooperative** game. In these modes, there is no rival adventuring party; the scenario's Monsters, hazards, and pressure rules take its place. Solo and cooperative play use the normal core rules unless this section says otherwise.

## Section 11: campaign

### CAMP-01: 11, first paragraph

**§2 fragments. Recommended. First pass.** A row of fragments becomes the end of the sentence it illustrates.

*Line 15021, under "11. Campaign Play".* Dependencies: none.

**Current**

> *In the Dying Lands, a single **Skirmish** is a transaction. Blood for coin. Risk for salvage. A name crossed off a roster so another name can eat for a week. A campaign is the longer ledger. It records what the party won, what it spent, who carried the chest, who did not stand up, and which debts waited at the gate.*

**Proposed**

> *In the Dying Lands, a single **Skirmish** is a transaction: blood for coin, risk for salvage, and a name crossed off a roster so another name can eat for a week. A campaign is the longer ledger. It records what the party won, what it spent, who carried the chest, who did not stand up, and which debts waited at the gate.*

### CAMP-02: 11, third paragraph

**§2 fragments. Recommended. First pass.** Same fragment row as LORE-17, fixed the same way.

*Line 15025, under "11. Campaign Play".* Dependencies: none.

**Current**

> *Councils, chapels, guilds, and discreet nobles use smaller tools. They hire parties. Small enough to hide. Strong enough to fight. Cheap enough to lose. Each contract begins as ink on a table inside the walls. It ends in mud, ash, snow, salt, or blood.*

**Proposed**

> *Councils, chapels, guilds, and discreet nobles use a smaller tool. They hire parties small enough to hide, strong enough to fight, and cheap enough to lose. Each contract begins as ink on a table inside the walls. It ends in mud, ash, snow, salt, or blood.*

### CAMP-08: 11, fourth paragraph

**§2 closer. Recommended. Second pass.** Paired closer joined.

*Line 15027, under "11. Campaign Play".* Dependencies: none.

**Current**

> *A campaign follows that cycle of contracts, scars, salvage, and attrition. It is played as a sequence of **Expeditions**, **Skirmishes**, **Aftermaths**, and **Town Phases**. The party earns coin, recovers equipment, recruits replacements, improves its **Heroes**, and spends its winnings in pursuit of a final **Stronghold**. Nothing about the process is clean. Clean things do not last long beyond the gates.*

**Proposed**

> *A campaign follows that cycle of contracts, scars, salvage, and attrition. It is played as a sequence of **Expeditions**, **Skirmishes**, **Aftermaths**, and **Town Phases**. The party earns coin, recovers equipment, recruits replacements, improves its **Heroes**, and spends its winnings in pursuit of a final **Stronghold**. Nothing about the process is clean, and clean things do not last long beyond the gates.*

### CAMP-09: 11, fifth paragraph

**§7 repeated openings, §2 closer. Recommended. Second pass.** 'They rarely mention' twice, then two short closers.

*Line 15029, under "11. Campaign Play".* Dependencies: none.

**Current**

> *Each adventure begins with a promise written by someone who expects not to bleed. A patron may ask the party to recover medicine from a ruined apothecary, extract a relic from a sealed crypt, escort a message through The Mire, burn out a sorcerer's tower, slay a named **Monster**, or confirm that another party failed. The written terms rarely mention the rival company hired under another seal. They rarely mention the last expedition whose bones still lie within sight of the objective. The Bastions know. The contracts are drafted accordingly.*

**Proposed**

> *Each adventure begins with a promise written by someone who expects not to bleed. A patron may ask the party to recover medicine from a ruined apothecary, extract a relic from a sealed crypt, escort a message through The Mire, burn out a sorcerer's tower, slay a named **Monster**, or confirm that another party failed. The written terms rarely mention the rival company hired under another seal, or the last expedition whose bones still lie within sight of the objective. The Bastions know, and draft the contracts accordingly.*

### CAMP-03: 11, seventh paragraph

**§2 fragments. Recommended. First pass.** Six fragments become one list; every item and every bold term stays.

*Line 15033, under "11. Campaign Play".* Dependencies: none.

**Current**

> *Between **Skirmishes**, survival is counted in smaller measures. A blade recovered from a corpse. A shield hammered flat and bound with wire. A **Hireling** paid before they desert. A **Hero** carried back breathing, though not whole. A name scratched from the **Roster**. A debt moved from one column to another. The **Treasury** grows by contract pay, salvage, theft, and **Monster** blood. **Storage** fills with gear stripped from the dead and saved for the living. The **Bench** waits behind the walls, healing, drinking, praying, or pretending not to hear the next contract read aloud.*

**Proposed**

> *Between **Skirmishes**, survival is counted in smaller measures: a blade recovered from a corpse, a shield hammered flat and bound with wire, a **Hireling** paid before they desert, a **Hero** carried back breathing though not whole, a name scratched from the **Roster**, and a debt moved from one column to another. The **Treasury** grows by contract pay, salvage, theft, and **Monster** blood. **Storage** fills with gear stripped from the dead and saved for the living. The **Bench** waits behind the walls, healing, drinking, praying, or pretending not to hear the next contract read aloud.*

### CAMP-04: 11.1, first lore paragraph

**§1 contrast, §7 repeated openings. Recommended. First pass.** 'Not a castle in the noble sense' is then explained twice; the two explanations carry it.

*Line 15041, under "11.1 Campaign Overview".* Dependencies: art catalog quote.

**Current**

> *A **Stronghold** is not a castle in the noble sense. No ancient bloodline sanctifies it. No bard remembers its founding. It is a claim driven into a dying world with coin, fear, salvage, and stubborn labour. Its stones come from ruined shrines, abandoned watch-keeps, broken bridges, and walls that failed other people first. Its gates are paid for with burial gold, bounty coin, chapel debt, and the last wages of the dead.*

**Proposed**

> *A **Stronghold** has no ancient bloodline to sanctify it and no bard to remember its founding. It is a claim driven into a dying world with coin, fear, salvage, and stubborn labour. Its stones come from ruined shrines, abandoned watch-keeps, broken bridges, and walls that failed other people first. Its gates are paid for with burial gold, bounty coin, chapel debt, and the last wages of the dead.*

### CAMP-05: 11.1, third lore paragraph

**§1 contrast, §2 fragments. Recommended. First pass.** Two staged contrasts in a row ('not mercy. It is weight.' and 'more than X. It becomes Y.'). The weight and the list of what the party becomes stay.

*Line 15045, under "11.1 Campaign Overview".* Dependencies: none.

**Current**

> *To build a Stronghold is to stop running long enough to answer for other people. That is not mercy. It is weight. A party becomes more than adventurers with blades and debts. It becomes a name in ledgers, a mark on maps, a rumour at gates, and a provocation beyond the watch-fire. Its enemies no longer need to hunt it across the Dying Lands. They know where to come.*

**Proposed**

> *To build a Stronghold is to stop running long enough to take on the weight of answering for other people. The party becomes a name in ledgers, a mark on maps, a rumour at gates, and a provocation beyond the watch-fire. Its enemies no longer need to hunt it across the Dying Lands. They know where to come.*

### CAMP-10: 11.1, Triumph

**§7 repeated openings, §2 closer. Recommended. Second pass.** 'It means' three times, then two closing fragments. The opening 'does not mean the world is saved' stays, because a reader may well expect Triumph to mean exactly that.

*Line 15047, under "11.1 Campaign Overview".* Dependencies: none.

**Current**

> ***Triumph** does not mean the world is saved. It means people can sleep behind a door they helped bar. It means a few more fires stay lit when the weather turns. It means a few more children hear the training yard before they hear claws on wood. The dark has been pushed back by the width of a wall. That is enough to matter. It is not enough to last.*

**Proposed**

> ***Triumph** does not mean the world is saved. It means people can sleep behind a door they helped bar, a few more fires stay lit when the weather turns, and a few more children hear the training yard before they hear claws on wood. The dark has been pushed back by the width of a wall, which is enough to matter and not enough to last.*

### CAMP-06: 11.3, The Vault

**§1 contrast. Recommended. First pass.** The negative half denies a claim nobody made.

*Line 15668, under "The Vault".* Dependencies: player aid pa08, pa09; art catalog quote.

**Current**

> *The Vault is not a treasury. It is a sealed confession of greed, iron-bound and watched by clerks who sleep in shifts. They count each coin as if the dead might come back to collect.*

**Proposed**

> *The Vault is a sealed confession of greed, iron-bound and watched by clerks who sleep in shifts. They count each coin as if the dead might come back to collect.*

### CAMP-07: 11.3, The Armoury

**§1 contrast, §2 closer. Recommended. First pass.** Split 'does not look X. It looks Y.' stated directly.

*Line 15690, under "The Armoury".* Dependencies: player aid pa08, pa09.

**Current**

> *A party with an Armoury does not look safe. It looks prepared. In the Dying Lands, that is close enough to hope.*

**Proposed**

> *A party with an Armoury looks prepared, and in the Dying Lands that is close enough to hope.*

### CAMP-11: 11.3, The Apothecary

**§7 repeated openings. Recommended. Second pass.** 'Leave' three times in three sentences.

*Line 15700, under "The Apothecary".* Dependencies: player aid pa08, pa09.

**Current**

> *No one leaves untouched. The fortunate leave with scars closed. The unlucky leave with something inside them quieted rather than cured.*

**Proposed**

> *No one leaves untouched: the fortunate go with their scars closed, and the unlucky with something inside them quieted rather than cured.*

### CAMP-12: 11.3, The Stronghold Chapel

**§7 repeated openings. Recommended. Second pass.** 'Its' three times in a row.

*Line 15728, under "The Stronghold Chapel".* Dependencies: player aid pa08, pa09; art catalog quote.

**Current**

> *The Chapel is small, cold, and crowded with votive offerings from those who survived by inches. Its saints are chipped. Its relics are suspect. Its candles burn low even when no wind enters.*

**Proposed**

> *The Chapel is small, cold, and crowded with votive offerings from those who survived by inches. Its saints are chipped and its relics suspect, and its candles burn low even when no wind enters.*

### CAMP-13: 11.3, The Stronghold Chapel

**§1 contrast. Recommended. Second pass.** Split 'does not X. It Y.' as one sentence.

*Line 15730, under "The Stronghold Chapel".* Dependencies: player aid pa08, pa09.

**Current**

> *The Chapel does not promise salvation. It gives the desperate a place to kneel before they return to the roads that nearly killed them.*

**Proposed**

> *The Chapel promises no salvation, only a place for the desperate to kneel before they return to the roads that nearly killed them.*

### CAMP-14: 11.3, The War Room

**§2 fragments. Recommended. Second pass.** A row of fragments.

*Line 15740, under "The War Room".* Dependencies: player aid pa08, pa09.

**Current**

> *A party with a War Room becomes visible. Petitioners arrive. Rivals take note. Every whispered bargain begins to sound like law.*

**Proposed**

> *A party with a War Room becomes visible: petitioners arrive, rivals take note, and every whispered bargain begins to sound like law.*

### CAMP-15: 11.3, The Undercroft

**§7 repeated openings. Recommended. Second pass.** Paired 'Each year' sentences joined.

*Line 15760, under "The Undercroft".* Dependencies: player aid pa08, pa09.

**Current**

> *No one admits how deep it goes. Each year another blocked stair is uncovered. Each year the party decides not to ask who carved it.*

**Proposed**

> *No one admits how deep it goes. Each year another blocked stair is uncovered, and each year the party decides not to ask who carved it.*

## Appendix A: Learn to Play

### LEARN-02: A.10, opening paragraph

**§1 contrast, §12 'matter'. Recommended. Second pass.** 'Is not won only by X' followed by its restatement.

*Line 16397, under "A.10 Objectives, Extraction, and Scoring".* Dependencies: figures FIG-18.

**Current**

> Heraldry Skirmish is not won only by defeating enemies. Positioning and objective play matter more than trading damage.

**Proposed**

> Positioning and objective play decide more games than trading damage does.

### LEARN-01: A.11, closing paragraph

**§1 contrast, §2 'this shows'. Recommended. First pass.** 'This shows why X is not merely Y' is the strongest tell in the rules text. The replacement states what the two rounds showed; the rest of the paragraph is unchanged.

*Line 16544, under "Round 2".* Dependencies: figures FIG-18.

**Current**

> This opening shows why Heraldry Skirmish is not merely a damage race. Edric seized the objective quickly, but spending all **3 AP** left them unable to **Dodge**, **Block**, or **Parry**. Varek punished the exposed carrier, the Dire Wolves punished the centre scrum, and Mara earned coins only by taking a flank objective while the main fight collapsed.

**Proposed**

> Both rounds turned on **AP** and objectives more than on damage. Edric seized the objective quickly, but spending all **3 AP** left them unable to **Dodge**, **Block**, or **Parry**. Varek punished the exposed carrier, the Dire Wolves punished the centre scrum, and Mara earned coins only by taking a flank objective while the main fight collapsed.
