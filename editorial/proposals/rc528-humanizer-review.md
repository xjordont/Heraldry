# Humanizer review: proposed patches for RC528

**Not applied.** Owner request, 2026-11-02, in a Claude Code session: "humanizer manuscript". This is the proposal that request produces under the project contract: the manuscript changes only through exact replacements the owner approves, promoted once through `tools/revise_manuscript.py` as one new RC. Nothing below has been applied, and no figure, aid, or PDF has been rebuilt.

Prepared 2026-11-02 against `source/Heraldry_RC527.md` (SHA-256 `d28f5ec8ef438b43d278ec59c8faf195204266606bcfad1cbd8258088f48ec55`, 18,552 lines). The patches are in the JSON twin `editorial/proposals/rc528-humanizer-review.json`, each with status `proposed`. Every `find` occurs exactly once in RC527 and still exactly once when the batch is applied in order. No patch adds or removes a line, so block IDs and figure line citations do not move. No patch changes a number, a name, or a bold term (LEARN-01 adds a bold **AP**, as the book writes it elsewhere). The full candidate passed `python tools/dev.py manuscript prepare` (READY FOR OWNER REVIEW; 83 of 83 content anchors resolve; no blocking finding).

## Method

The pass follows the humanizer skill (patterns from Wikipedia's "Signs of AI writing"). Section numbers like §1 refer to its pattern list: §1 is 'not X but Y' contrasts, §2 one-line closers and rows of fragments, §3 sayings that sound deep, §6 forced triads, §7 repeated sentence openings, §12 stock AI words, §16 sales language, and §18 'serves as' and 'represents' in place of 'is'. I read every italic lore passage (406 paragraphs, about 22,700 words), all of Section 1, and the Appendix A walkthrough, then swept the whole manuscript mechanically for dashes, the contrast formulas, the stock vocabulary, and staged phrasing.

The voice is the book's own: terse, grim, and fond of a dry last line. The rewrites keep that. Fiction may invent, but these patches add nothing to the canon: every replacement keeps the facts of the text it replaces, and where a line is cut, the line was a restatement. Rhythm the author plainly chose (the lists of what the Bastions trade, the 'Every gate has a price' series, the paired sentences in the Bastion entries) stays.

## Verdict

The rules text is clean. The manuscript has no em dashes, and all 370 en dashes sit in number ranges such as 1–3. The stock AI vocabulary is almost absent: no 'delve', 'tapestry', 'testament', 'pivotal', or 'showcase', and only four rules sentences open with 'Additionally'. The contrast hits in the rules ('not a Total Miss but before mitigation') are real rule distinctions. A sweep for 'this means', 'this shows', 'matters', and similar staging found one real instance (LEARN-01).

The tells are in the lore, and three account for most of them:

- **'Not X. It is Y.'** (§1), 30 patches. The negative half denies something no reader thought ("The forest is no wilderness", "The Town Phase is not peace", "The Vault is not a treasury") so that the positive half sounds larger. Where the negative half does correct a real expectation, it stays, for example "The gates do not ask what a refugee is" and the Druids who "do not mourn the dying world".
- **Fragment rows and stock closers** (§2), 36 patches: "Slow. Aware. Dangerous to touch.", "Small enough to hide. Strong enough to fight. Cheap enough to lose." (printed twice), and the closers repeated across entries: 'One is X; a swarm is Y' ends seven Monster entries, 'There are always more' three, and 'It is always warm' or 'always cold' four relics.
- **Repeated openings** (§7), 10 patches: "They send envoys. They trade... They exchange... They accept...", "Some rise hungry. Some rise bitter. Some rise...", "They watch the reliquary. They watch the water. They watch...".

The Chapter 8 introduction (POWER-01 to POWER-07) is the one passage that reads as generated throughout: 'transcend the swing of a blade', 'a cold calculus', 'pulse with a terrifying, untamed vitality', 'a terrible intimacy with corruption', and 'living conduits of the world's sickness'. Those seven paragraphs are rewritten in full, keeping each claim.

## Counts

| Group | Patches | Figures affected |
| --- | --- | --- |
| Section 1: the world | 19 | none |
| Section 6: parties and backgrounds | 5 | none |
| Section 7: item lore and item wording | 11 | none |
| Section 8: Powers | 9 | none |
| Section 9: Monsters | 16 | none |
| Section 10: objective and scenario lore | 10 | 41 (FIG-13 to FIG-56) |
| Section 11: campaign | 7 | none |
| Appendix A: Learn to Play | 1 | FIG-18 |
| **Total** | **78** | **42** |

75 patches are recommended and 3 optional (ITEM-04, MON-14, PARTY-01). Applied together, they shorten the book by about 285 words.

## Owner choices

Approving a group means approving its patch IDs. The groups differ mainly in what they cost downstream:

1. **Approve everything except the scenario group** (69 patches). 68 of them affect no figure; LEARN-01 stales one figure review (FIG-18, which hashes all of Appendix A). This is the low-cost option.
2. **Also approve the scenario group** (SCEN-02 to SCEN-10, 9 patches). `tools/figure_dependencies.py` hashes the whole of **10.4 Core Scenario Outlines** for every scenario map and preparation figure, so any edit inside 10.4, however cosmetic, marks 41 figure reviews stale (FIG-13 to FIG-16 and FIG-20 to FIG-56). None of these patches touches what a figure draws, so the re-review is a confirmation, but it has to be recorded before the next release. SCEN-01 sits in 10.2 and affects no figure.
3. **Two earlier owner-approved phrases.** LORE-02 removes 'not soft clerks with ledgers' and LORE-17 restructures 'Small enough to hide. Strong enough to fight. Cheap enough to lose.'; RC523 polished both. Decline either to keep the current wording.
4. **Optional patches.** PARTY-01 ("not the heroes sung about in warm halls") arguably corrects a real genre expectation; ITEM-04 is a small merge; MON-14 removes the Void Dragon's 'neither burns nor freezes' contrast with the other dragons.

## Dependency impact

- **Figures.** See the owner choices above: 1 figure (FIG-18) without the scenario group, 42 with it.
- **Content anchors.** All 83 resolve on the full candidate; none needs a new prefix.
- **Player-aid sheets.** `tools/aids_fidelity.py` will report changed sections for pa02 (the Bosses section: MON-13 to MON-16) and pa08 and pa09 (11.3: CAMP-06 and CAMP-07). No sheet quotes the patched lore, so re-recording after a diff is a confirmation; the sheets do not need rebuilding.
- **Hero cards, back cover, How to Use, and cover lead.** Unaffected: B.4 is untouched, and no string in `editorial/back_cover.json`, `editorial/how_to_use.json`, or the 'cover-lead' anchor changes.
- **Art catalog.** `production/art/SPOT_CATALOG.json` and `production/art/ILLUSTRATION_LIST.md` quote the flavour text above each illustration, and 31 patches change quoted paragraphs. Regenerate both at promotion (`python tools/dev.py agent run art-catalog`, then `tools/art_list.py`) as after the earlier lore revisions. Approved art is unaffected.
- **Specimen.** `typst/templates/specimens.typ` quotes the Frozen Laboratory introduction as sample text; SCEN-07 would leave it one sentence longer than the book. It is a type specimen, not book content, so updating it is optional.
- **Build.** Nothing was built. The last released PDFs (RC527-build-41) are unchanged.

## Left alone

- **Headings and bold labels.** Title-case headings and bold run-in labels are the book's house style and carry anchors, cross-references, and the index (§19 and §20 do not apply).
- **Monster entry openings.** Most Bestiary entries open with an appositive ('Knee-high and bat-winged, the imp...'). That is a template, but it is the house form for all 135 entries and each one carries specific physical detail.
- **Deliberate echoes.** The two hags share 'They bargain, they lie...'; the salt smell in two Mire scenarios; the 'only magic answers' immunity reminders, which mirror the stat blocks.
- **Repeated content.** Two passages restate earlier ones closely: the 'Columns need wagons...' climate list in 1.3.6 returns in the Chapter 11 introduction, and Chapter 8's tradition paragraphs repeat 1.3.4. That is a structure question, not a writing tell, so no patch cuts either; say if you want one.
- **Rules text.** Apart from LEARN-01 and the four 'Additionally' sentences, no rules wording changes.

## Findings

Grouped by section, in manuscript order within each group. Line numbers refer to `source/Heraldry_RC527.md`. 'Current' is the whole line as it stands; 'Proposed' is that line with only this patch applied.

## Section 1: the world

### LORE-01: 1.1, third paragraph

**§2 closers. Recommended.** The opener announces what the next sentence shows, and 'Even victory is rarely clean' restates the closing sentence. Both go; the three facts and the closing line stay.

*Line 171, under "1.1 What is Heraldry Skirmish?".* Dependencies: none.

**Current**

> The battlefield is never passive. Neutral Monsters stalk the field, hazards punish hesitation, and scenarios place pressure on both sides from the first activation to the last. Even victory is rarely clean. The party that leaves the field richest is often the one that bled for every coin.

**Proposed**

> Neutral Monsters stalk the field, hazards punish hesitation, and scenarios place pressure on both sides from the first activation to the last. The party that leaves the field richest is often the one that bled for every coin.

### LORE-02: 1.2, second paragraph

**§1 contrast, §7 repeated openings. Recommended.** Nobody claimed merchants were soft clerks; the list of what they do makes the point. The two 'They know which' sentences merge. RC523 polished the 'soft clerks' phrase, so decline this patch if you want to keep it.

*Line 193, under "1.2 The Grim World".* Dependencies: none.

**Current**

> *Most people live close to a gate. A palisade, a bell, a chapel lamp, and a few armed neighbours are the shape of civilization now. Beyond them lie drowned fields, plague roads, ruined shrines, black forests, dead bridges, and the shattered works of older realms. Merchants who travel between holdings are not soft clerks with ledgers. They bargain, lie, fight, navigate, and plan funerals with equal care. They know which inns change names too often. They know which milestones bleed in rain.*

**Proposed**

> *Most people live close to a gate. A palisade, a bell, a chapel lamp, and a few armed neighbours are the shape of civilization now. Beyond them lie drowned fields, plague roads, ruined shrines, black forests, dead bridges, and the shattered works of older realms. Merchants who travel between holdings bargain, lie, fight, navigate, and plan funerals with equal care. They know which inns change names too often and which milestones bleed in rain.*

### LORE-03: 1.2, third paragraph

**§6 forced triad, §7 repeated openings. Recommended.** Three fragments with the same opening become one sentence; all three kinds of dead stay.

*Line 195, under "1.2 The Grim World".* Dependencies: none.

**Current**

> *The countryside has teeth. Bandits prey on the weak and call it tax. Beasts prowl where the ploughs stopped. Goblin raiders descend on lonely roads and isolated farms. Orcs, gnolls, and kobolds test the borderlands for weakness and plunder. Haunted crypts and mass graves fill with the failures of earlier expeditions. The dead do not always stay down. Some rise hungry. Some rise bitter. Some rise with orders still clenched behind their teeth.*

**Proposed**

> *The countryside has teeth. Bandits prey on the weak and call it tax. Beasts prowl where the ploughs stopped. Goblin raiders descend on lonely roads and isolated farms. Orcs, gnolls, and kobolds test the borderlands for weakness and plunder. Haunted crypts and mass graves fill with the failures of earlier expeditions. The dead do not always stay down: some rise hungry, some bitter, and some with orders still clenched behind their teeth.*

### LORE-04: 1.2, fourth paragraph

**§7 repeated openings. Recommended.** 'X waits there' three times in a row.

*Line 197, under "1.2 The Grim World".* Dependencies: none.

**Current**

> *Beneath ruined towers, sunken monasteries, and collapsed fortresses lie the vaults of fallen empires. Coin waits there. Relics wait there. Forbidden lore waits there too, written in dust, iron, blood, and languages that make candles gutter. Dragons still brood in the deep places of the earth and on the high forgotten peaks. Their hoards could ransom kingdoms. Their wrath could end them.*

**Proposed**

> *Beneath ruined towers, sunken monasteries, and collapsed fortresses lie the vaults of fallen empires. Coin and relics wait there, and so does forbidden lore, written in dust, iron, blood, and languages that make candles gutter. Dragons still brood in the deep places of the earth and on the high forgotten peaks. Their hoards could ransom kingdoms. Their wrath could end them.*

### LORE-05: 1.3, third paragraph

**§1 contrast. Recommended.** The negative half denies a claim nobody made; the rest of the sentence already says the crowns and borders stopped being useful.

*Line 209, under "1.3 The Dying Lands".* Dependencies: none.

**Current**

> *The lands where Heraldry Skirmish is fought are not a kingdom. They are a continent in the oldest sense: a single body of land held together by mountains, rivers, roads, ruins, and grief long after its crowns and borders stopped being useful.*

**Proposed**

> *The lands where Heraldry Skirmish is fought are a continent in the oldest sense: a single body of land held together by mountains, rivers, roads, ruins, and grief long after its crowns and borders stopped being useful.*

### LORE-06: 1.3.1, last paragraph

**§1 contrast, §2 fragments. Recommended.** A 'not X, it is Y' opener followed by a row of one-word fragments. The image and all three qualities stay.

*Line 227, under "1.3.1 The Fall".* Dependencies: none.

**Current**

> *The world is not dying gently. It dies like a wounded animal under a hedge. Slow. Aware. Dangerous to touch.*

**Proposed**

> *The world is dying the way a wounded animal dies under a hedge: slowly, aware of it, and dangerous to touch.*

### LORE-07: 1.3.2, opening paragraph

**§3 saying. Recommended.** An aphorism with no claim the paragraph goes on to support; the paragraph is about names and labels.

*Line 231, under "1.3.2 The Six Climates of Ruin".* Dependencies: none.

**Current**

> *Beyond the walls, land has become allegiance. Expedition ledgers still say forest, city, cavern, ice, desert, and swamp. Survivors know better. They use older names. The shape of the world is plain enough to anyone who has walked it. The broken mountains run down its spine. The dead empire and its ruined cities sprawl across the eastern heart. The great forest spreads west to the coast, the ice locks the north, the dunes burn in the south beyond the mountain passes, and the swamps drown the south-east where the rivers give out at the sea. The old imperial roads still join all of it, straight and patient, running out from the Ashlands to every climate that survived. A dry label cannot warn a traveller that a road has memory, a court still sits without lungs, or a pool of black water may be listening.*

**Proposed**

> *Expedition ledgers still say forest, city, cavern, ice, desert, and swamp. Survivors know better. They use older names. The shape of the world is plain enough to anyone who has walked it. The broken mountains run down its spine. The dead empire and its ruined cities sprawl across the eastern heart. The great forest spreads west to the coast, the ice locks the north, the dunes burn in the south beyond the mountain passes, and the swamps drown the south-east where the rivers give out at the sea. The old imperial roads still join all of it, straight and patient, running out from the Ashlands to every climate that survived. A dry label cannot warn a traveller that a road has memory, a court still sits without lungs, or a pool of black water may be listening.*

### LORE-08: 1.3.2, The Greenmark

**§1 contrast. Recommended.** Split 'not X. It is Y.' closer stated directly.

*Line 235, under "The Greenmark".* Dependencies: none.

**Current**

> *The Greenmark is the great temperate forest of the surviving world. It is larger than the maps. Roots take a road within a season and make the milestones useless. Travellers report trees shifting at the edge of sight, upright hounds between trunks, and grove-circles where moss stays warm after snow. Foresters cut warning signs into bark for those who know how to read them. The most common sign means turn back even if the voice ahead is your own. The forest is no wilderness. It is a country that does not recognize human law.*

**Proposed**

> *The Greenmark is the great temperate forest of the surviving world. It is larger than the maps. Roots take a road within a season and make the milestones useless. Travellers report trees shifting at the edge of sight, upright hounds between trunks, and grove-circles where moss stays warm after snow. Foresters cut warning signs into bark for those who know how to read them. The most common sign means turn back even if the voice ahead is your own. The forest is a country of its own, and it does not recognize human law.*

### LORE-09: 1.3.2, closing paragraph

**§2 closer. Recommended.** 'These six are the world now' restates the section; the two Bastion sentences share a subject and merge.

*Line 257, under "The Mire".* Dependencies: none.

**Current**

> *These six are the world now. The Bastions are what mortal civilization built against them. They are also what mortal civilization hides inside.*

**Proposed**

> *The Bastions are what mortal civilization built against these six climates, and what it hides inside.*

### LORE-10: 1.3.3, fourth paragraph

**§7 repeated openings. Recommended.** Nine short sentences, four opening 'They' and two 'No Bastion', become four. Every item stays.

*Line 267, under "1.3.3 The Six Bastions".* Dependencies: none.

**Current**

> *The Bastions themselves are not allies. They send envoys. They trade iron, salt, grain, oil, bodies, medicine, and lies. They exchange prisoners when it is useful. They accept refugees when plague at the gate would be worse than charity. Their treaties are thin things. Tired clerks write them. Hungry captains break them. No Bastion can afford open war with another. No Bastion trusts that fact to last.*

**Proposed**

> *The Bastions themselves are not allies. They send envoys and trade iron, salt, grain, oil, bodies, medicine, and lies. They exchange prisoners when it is useful and accept refugees when plague at the gate would be worse than charity. Their treaties are thin things, written by tired clerks and broken by hungry captains. No Bastion can afford open war with another, and none trusts that fact to last.*

### LORE-11: 1.3.3, fifth paragraph

**§1 contrast. Recommended.** 'Not safe. They are safer.' is the staged form; the plain comparison says the same thing. 'but' repairs the list that follows.

*Line 269, under "1.3.3 The Six Bastions".* Dependencies: none.

**Current**

> *The Bastions are not safe. They are safer. Their walls keep out the worst of the dark, not hunger, fever, debt, politics, superstition, or the quiet passengers hidden among refugees and trade goods. Every gate has a price. Every chapel keeps lists. Every guild counts favours. Every watch-fire burns lower than the captains admit.*

**Proposed**

> *The Bastions are only safer than the country around them. Their walls keep out the worst of the dark, but not hunger, fever, debt, politics, superstition, or the quiet passengers hidden among refugees and trade goods. Every gate has a price. Every chapel keeps lists. Every guild counts favours. Every watch-fire burns lower than the captains admit.*

### LORE-12: 1.3.3, last paragraph before Greythorn

**§1 contrast. Recommended.** 'Part of the war' already says it is not peace.

*Line 275, under "1.3.3 The Six Bastions".* Dependencies: none.

**Current**

> *For most people, the Bastion is the end of the world made habitable by walls. For adventurers, it is where wounds are priced, contracts are stamped, dead companions are replaced, and the next mistake is made official. The **Town Phase** is not peace. It is the part of the war fought with ledgers, knives, prayers, and closed doors.*

**Proposed**

> *For most people, the Bastion is the end of the world made habitable by walls. For adventurers, it is where wounds are priced, contracts are stamped, dead companions are replaced, and the next mistake is made official. The **Town Phase** is the part of the war fought with ledgers, knives, prayers, and closed doors.*

### LORE-13: 1.3.3, Saltspire

**§2 fragments. Recommended.** Two follow-up fragments merge into the sentence they explain.

*Line 311, under "Saltspire".* Dependencies: none.

**Current**

> ***Saltspire** is a tower-city built around a deep, sacred well at the centre of an oasis ringed by salt-pans and the bones of older cities. It has the only reliable water for a hundred miles. This makes it wealthy. It also makes it hated.*

**Proposed**

> ***Saltspire** is a tower-city built around a deep, sacred well at the centre of an oasis ringed by salt-pans and the bones of older cities. It has the only reliable water for a hundred miles, which makes it wealthy and hated.*

### LORE-14: 1.3.4, Arcane Spells

**§3 saying. Recommended.** 'Tolerance is not trust' is an aphorism standing in for the plain claim.

*Line 329, under "1.3.4 Magic in the Dying Lands".* Dependencies: none.

**Current**

> ***Arcane Spells** are the inheritance of the broken empires. Wizards seek ruined libraries, half-burned grimoires, observatories with cracked lenses, and silent towers where their predecessors are still slumped over their work. Most Bastions tolerate wizards because they are useful. Tolerance is not trust. Sablekeep requires registration. Greythorn pays enough to keep them polite. Deepwarden watches their shadows on tunnel walls. They are blamed whenever blame needs a shape.*

**Proposed**

> ***Arcane Spells** are the inheritance of the broken empires. Wizards seek ruined libraries, half-burned grimoires, observatories with cracked lenses, and silent towers where their predecessors are still slumped over their work. Most Bastions tolerate wizards because they are useful. No Bastion trusts them. Sablekeep requires registration. Greythorn pays enough to keep them polite. Deepwarden watches their shadows on tunnel walls. They are blamed whenever blame needs a shape.*

### LORE-15: 1.3.5, opening paragraph

**§1 contrast. Recommended.** The negative half denies a claim nobody made. Chapter 9 opens with the same move (MON-01).

*Line 343, under "1.3.5 Monstrous Threats".* Dependencies: none.

**Current**

> *The **Monsters** of the Dying Lands are not scattered obstacles. They hold the world now. They keep roads closed, fields empty, shrines silent, and old borders meaningless. A village may vanish because of hunger, tax, fever, or weather. Outside the walls, those causes often have claws, banners, laws, or names.*

**Proposed**

> *The **Monsters** of the Dying Lands hold the world now. They keep roads closed, fields empty, shrines silent, and old borders meaningless. A village may vanish because of hunger, tax, fever, or weather. Outside the walls, those causes often have claws, banners, laws, or names.*

### LORE-16: 1.3.5, the old peoples

**§7 repeated openings. Recommended.** Four 'Some' sentences in a row; the three one-word ones merge.

*Line 351, under "1.3.5 Monstrous Threats".* Dependencies: none.

**Current**

> ***The old peoples and border powers** have not vanished. Were-creatures, satyr cohorts, dryad ambassadors, deep elves, nagas, necromancers, lizardfolk temple-guards, and stranger courts hold places the Bastions still mark as lost. Some bargain. Some tithe. Some raid. Some remember treaties humanity has forgotten and punish the breach with perfect sincerity. In the Sun-Drowned, the tomb-cities of the priest-kings are administered by **necromancers** who have outlasted their own deaths: judges, clerks, and tax-collectors preserved in linen, oil, and old authority. They do not acknowledge the Fall. They acknowledge overdue accounts.*

**Proposed**

> ***The old peoples and border powers** have not vanished. Were-creatures, satyr cohorts, dryad ambassadors, deep elves, nagas, necromancers, lizardfolk temple-guards, and stranger courts hold places the Bastions still mark as lost. Some bargain, some tithe, and some raid. Some remember treaties humanity has forgotten and punish the breach with perfect sincerity. In the Sun-Drowned, the tomb-cities of the priest-kings are administered by **necromancers** who have outlasted their own deaths: judges, clerks, and tax-collectors preserved in linen, oil, and old authority. They do not acknowledge the Fall. They acknowledge overdue accounts.*

### LORE-17: 1.3.6, third paragraph

**§2 fragments. Recommended.** A row of fragments becomes one sentence; the three qualities stay. The same row appears again in Chapter 11 (CAMP-02). RC523 reworded 'Strong enough to fight'; that wording is kept.

*Line 367, under "1.3.6 Adventurers and the Road".* Dependencies: none.

**Current**

> *What works is a party of four. Small enough to hide. Strong enough to fight. Cheap enough to lose.*

**Proposed**

> *What works is a party of four: small enough to hide, strong enough to fight, and cheap enough to lose.*

### LORE-18: 1.3.6, last paragraph

**§2 fragments. Recommended.** Three fragments become the end of the sentence they illustrate.

*Line 375, under "1.3.6 Adventurers and the Road".* Dependencies: none.

**Current**

> *Those who survive begin to build something larger than a purse. A keep on a hill. A reclaimed manor. A forge, a chapel, a vault, and a wall thick enough to last one hard winter. Few parties live long enough to raise such a place. Fewer reach **Triumph**, the old Bastion word for planting a banner in ground that has stayed clean for a generation. Every party leaving the gate tells itself this is the road ahead. Most roads end before that.*

**Proposed**

> *Those who survive begin to build something larger than a purse: a keep on a hill or a reclaimed manor, with a forge, a chapel, a vault, and a wall thick enough to last one hard winter. Few parties live long enough to raise such a place. Fewer reach **Triumph**, the old Bastion word for planting a banner in ground that has stayed clean for a generation. Every party leaving the gate tells itself this is the road ahead. Most roads end before that.*

### LORE-19: 1.3.7, last paragraph

**§1 contrast. Recommended.** Split 'does not need X. It needs only Y.' stated directly.

*Line 403, under "1.3.7 Legends and Echoes".* Dependencies: none.

**Current**

> *The lore of the Dying Lands provides names, scars, and old quarrels for expeditions, rival parties, patrons, **Monsters**, relics, and campaign goals. A scenario does not need to explain the whole world. It needs only enough history to make the blood on the ground feel older than the fight.*

**Proposed**

> *The lore of the Dying Lands provides names, scars, and old quarrels for expeditions, rival parties, patrons, **Monsters**, relics, and campaign goals. A scenario needs only enough history to make the blood on the ground feel older than the fight.*

## Section 6: parties and backgrounds

### PARTY-01: 6, opening paragraph

**§1 contrast. Optional.** Optional. The negative half does push against a genre expectation, so keep it if that is the point; the next sentences make the same point with specifics.

*Line 1998, under "6. Your Adventuring Party".* Dependencies: none.

**Current**

> *Adventuring parties are not the heroes sung about in warm halls. They are the people the Bastions can send when soldiers would die too loudly. Debtors march with seals burned into their papers. Condemned prisoners carry pardons that become valid only if they return. Chapel agents, guild cutters, ruined heirs, oath-bound hirelings, and free companies with no banner worth saluting all leave by the same gates.*

**Proposed**

> *Adventuring parties are the people the Bastions can send when soldiers would die too loudly. Debtors march with seals burned into their papers. Condemned prisoners carry pardons that become valid only if they return. Chapel agents, guild cutters, ruined heirs, oath-bound hirelings, and free companies with no banner worth saluting all leave by the same gates.*

### PARTY-02: 6, second paragraph

**§7 repeated openings. Recommended.** Three parallel sentences become one.

*Line 2000, under "6. Your Adventuring Party".* Dependencies: none.

**Current**

> *A Bastion blesses these parties when it must. It pays them when it can. It denies them when the work turns shameful. Most **Expeditions** begin with a writ: a council mark, chapel order, guild contract, noble warrant, salvage-right, grave-tax exemption, or debt bond. The paper grants legal cause to enter forbidden ground and take what can be carried out. Rival parties may hold different writs for the same ruin. Each seal may be valid under some law, oath, or patronage. The Dying Lands do not care. A contract only matters if someone lives long enough to collect.*

**Proposed**

> *A Bastion blesses these parties when it must, pays them when it can, and denies them when the work turns shameful. Most **Expeditions** begin with a writ: a council mark, chapel order, guild contract, noble warrant, salvage-right, grave-tax exemption, or debt bond. The paper grants legal cause to enter forbidden ground and take what can be carried out. Rival parties may hold different writs for the same ruin. Each seal may be valid under some law, oath, or patronage. The Dying Lands do not care. A contract only matters if someone lives long enough to collect.*

### PARTY-03: 6.10, Smuggler background

**§1 contrast. Recommended.** 'Not a flourish. It is...' denies a claim nobody made.

*Line 2454, under "Smuggler".* Dependencies: none.

**Current**

> *A smuggler lives by false bottoms, whispered routes, and the craft of keeping valuable things out of dangerous hands. Stealth is not a flourish to them. It is the trade that buys supper.*

**Proposed**

> *A smuggler lives by false bottoms, whispered routes, and the craft of keeping valuable things out of dangerous hands. To them, stealth is the trade that buys supper.*

### PARTY-04: 6.10, Courier background

**§1 contrast. Recommended.** Same move as PARTY-03.

*Line 2462, under "Courier".* Dependencies: none.

**Current**

> *A courier carried news, coin, or secrets across broken roads and worse weather, for patrons who paid for speed and asked no questions. Speed was never a convenience. It was the difference between arriving and being found later.*

**Proposed**

> *A courier carried news, coin, or secrets across broken roads and worse weather, for patrons who paid for speed and asked no questions. Speed was the difference between arriving and being found later.*

### PARTY-05: 6.10, Merchant background

**§1 contrast. Recommended.** 'Never only X. It is Y.' stated directly.

*Line 2550, under "Merchant".* Dependencies: none.

**Current**

> *A merchant learned value, leverage, and the quiet power of knowing what desperate people will pay. Coin is never only money to them. It is movement, influence, and another season behind the walls.*

**Proposed**

> *A merchant learned value, leverage, and the quiet power of knowing what desperate people will pay. To them, coin means movement, influence, and another season behind the walls.*

## Section 7: item lore and item wording

### ITEM-01: 7.17.3, The Hollow Crown

**§2 closer. Recommended.** 'The distinction matters' is the stock closer. The rewrite keeps the contrast, which here carries the point, and keeps the warning that it will matter later.

*Line 4906, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> *The crown of the last sovereign of the fallen empires. No personal name survives. The statues that wore it have no faces. Their tomb has never been found. You have found their crown. This is not the same thing, and the distinction matters, but perhaps not yet.*

**Proposed**

> *The crown of the last sovereign of the fallen empires. No personal name survives. The statues that wore it have no faces. Their tomb has never been found. You have found their crown, which is not the same as finding them. In time, the difference will matter.*

### ITEM-07: 7.17.3, Kest's Iron Reliquary effect

**§12 'additionally'. Recommended.** Wording only; the effect is unchanged.

*Line 4923, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> **Effect:** Once per adventure, when you are adjacent to an enemy and spend **[1 AP]**, you may open the reliquary and release the bound spirit within. That enemy suffers **2d8 necrotic damage**, then must pass a **SPI Check** against **12**. **Failure:** They become **Frightened** until the end of their next activation. After use, the reliquary is empty until the next adventure, when it is found to contain something again. It is always warm. Additionally, while you wear Kest's Iron Reliquary you may spend **[1 AP]** to end **Cursed** on yourself or one ally within **2"**.

**Proposed**

> **Effect:** Once per adventure, when you are adjacent to an enemy and spend **[1 AP]**, you may open the reliquary and release the bound spirit within. That enemy suffers **2d8 necrotic damage**, then must pass a **SPI Check** against **12**. **Failure:** They become **Frightened** until the end of their next activation. After use, the reliquary is empty until the next adventure, when it is found to contain something again. It is always warm. While you wear Kest's Iron Reliquary, you may also spend **[1 AP]** to end **Cursed** on yourself or one ally within **2"**.

### ITEM-08: 7.17.3, Saint Cael's Burning Seal effect

**§12 'additionally'. Recommended.** Wording only; the effect is unchanged.

*Line 4953, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> **Effect:** This weapon deals **holy** damage. While wielding Saint Cael's Burning Seal, once per adventure when you are within **2"** of a scenario-marked threshold, bridge, ford, gate, or archway and you apply **AV** or use **Parry** against an **Undead** or **Fiend**, you may treat each **AD** die or retained **Parry** base die as its maximum natural result instead of rolling it. Roll any exploding **Parry** bonus dice and resolve **Riposte** normally. Additionally, **Undead** and **Fiends** that attack you while you are within **2"** of such a threshold suffer **1d6 holy damage** after their attack resolves. While wielding Saint Cael's Burning Seal you may spend **[1 AP]** to end **Cursed** on yourself or one ally within **2"**.

**Proposed**

> **Effect:** This weapon deals **holy** damage. While wielding Saint Cael's Burning Seal, once per adventure when you are within **2"** of a scenario-marked threshold, bridge, ford, gate, or archway and you apply **AV** or use **Parry** against an **Undead** or **Fiend**, you may treat each **AD** die or retained **Parry** base die as its maximum natural result instead of rolling it. Roll any exploding **Parry** bonus dice and resolve **Riposte** normally. **Undead** and **Fiends** that attack you while you are within **2"** of such a threshold also suffer **1d6 holy damage** after their attack resolves. While wielding Saint Cael's Burning Seal you may spend **[1 AP]** to end **Cursed** on yourself or one ally within **2"**.

### ITEM-04: 7.17.3, Salttide's Counting Stone

**§2 fragments. Optional.** Optional. Merges two of the three closing fragments; the dry last line stays.

*Line 5052, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> *The stone Edrava Salttide used to count ships that should have paid their toll. Sailors still see them at low winter tide, counting. The stone counts everything now. It remembers every debt. It is very patient.*

**Proposed**

> *The stone Edrava Salttide used to count ships that should have paid their toll. Sailors still see them at low winter tide, counting. The stone counts everything now and remembers every debt. It is very patient.*

### ITEM-02: 7.17.3, Old Wode's Iron-Shod Staff

**§2 fragments. Recommended.** A one-phrase fragment ('Three times.') folds into the sentence it belongs to.

*Line 5076, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> *An iron-shod walking staff that has been struck against standing stones. Three times. The strikes are still there. Three dents in the iron cap, each one slightly warmer than the rest of the metal.*

**Proposed**

> *An iron-shod walking staff that has been struck three times against standing stones. The strikes are still there: three dents in the iron cap, each one slightly warmer than the rest of the metal.*

### ITEM-03: 7.17.3, The Three-Strike Staff

**§2 fragments. Recommended.** Three fragments in a row.

*Line 5099, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> *Old Wode of the Antlered Path struck the standing stones three times at the end of the first post-Fall winter and returned with the agreement under which the Greenmark accepts Greythorn's autumn tithe. The agreement has never been written down. The forest has never broken it. This is the staff. The dents are there. The iron cap is still warm.*

**Proposed**

> *Old Wode of the Antlered Path struck the standing stones three times at the end of the first post-Fall winter and returned with the agreement under which the Greenmark accepts Greythorn's autumn tithe. The agreement has never been written down. The forest has never broken it. This is the staff, dents and all, and the iron cap is still warm.*

### ITEM-09: 7.17.3, Karnessa's Iron Seal effect

**§12 'additionally'. Recommended.** Wording only; the effect is unchanged.

*Line 5124, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> **Effect:** Once per adventure, when a Summon you control would be reduced to **0 HP**, you may spend **[0 AP]** to press Karnessa's Seal against them. This is a **Reaction**; declare it before that source's damage dice and commit its once-per-adventure use under **4.5**. That Summon is instead set to **1 HP**. Additionally, while wearing this Seal, you gain **+1** on **SPI Checks** made to resist the effects of **Undead** and **Fiend** Special Abilities.

**Proposed**

> **Effect:** Once per adventure, when a Summon you control would be reduced to **0 HP**, you may spend **[0 AP]** to press Karnessa's Seal against them. This is a **Reaction**; declare it before that source's damage dice and commit its once-per-adventure use under **4.5**. That Summon is instead set to **1 HP**. While wearing this Seal, you also gain **+1** on **SPI Checks** made to resist the effects of **Undead** and **Fiend** Special Abilities.

### ITEM-05: 7.17.3, Karnessa's Binding

**§2 repeated closer. Recommended.** 'It is X. It is always X.' is used as the closer on several relics (also ITEM-06 and SCEN-01); this keeps the fact once.

*Line 5144, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> *The thing that leaked through the vault walls when Karnessa Iron-Vein sealed it is not described in any surviving record. The seal held. That is what the records say. The records say it with the tone of people who are very grateful and do not intend to investigate further. Karnessa's Binding is the principle of that seal made portable. It is cold. It is always cold.*

**Proposed**

> *The thing that leaked through the vault walls when Karnessa Iron-Vein sealed it is not described in any surviving record. The seal held. That is what the records say. The records say it with the tone of people who are very grateful and do not intend to investigate further. Karnessa's Binding is the principle of that seal made portable, and it is always cold.*

### ITEM-10: 7.17.3, Bell-Shard Charm effect

**§12 'additionally', §18 'functions as'. Recommended.** 'Functions as' where 'is' says the same thing. (The Monster abilities that 'function as' another ability keep that wording, because there it means 'use the rules of'.)

*Line 5160, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> **Effect:** This item functions as an early warning system. When any **Undead** Monster becomes **Awake** within **12"** of you, the Charm chimes. You immediately become aware of that Monster's approximate location and that their Wake-Up condition has been met. You may then take a **[0 AP Reaction]**, even outside your activation, to make an **INT Check** against **12**. This Check does not require the Monster to be **Hidden** or in your **LOS**. On a success, the Monster loses **Hidden**, if applicable, and you know their exact position until the end of the round. Additionally, you gain **+1** on **SPI Checks** made to resist **Frightened** from **Undead** sources.

**Proposed**

> **Effect:** This item is an early warning system. When any **Undead** Monster becomes **Awake** within **12"** of you, the Charm chimes. You immediately become aware of that Monster's approximate location and that their Wake-Up condition has been met. You may then take a **[0 AP Reaction]**, even outside your activation, to make an **INT Check** against **12**. This Check does not require the Monster to be **Hidden** or in your **LOS**. On a success, the Monster loses **Hidden**, if applicable, and you know their exact position until the end of the round. Additionally, you gain **+1** on **SPI Checks** made to resist **Frightened** from **Undead** sources.

### ITEM-11: 7.17.3, Bell-Shard Charm effect

**§12 'additionally'. Recommended.** Wording only; the effect is unchanged.

*Line 5160, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> **Effect:** This item functions as an early warning system. When any **Undead** Monster becomes **Awake** within **12"** of you, the Charm chimes. You immediately become aware of that Monster's approximate location and that their Wake-Up condition has been met. You may then take a **[0 AP Reaction]**, even outside your activation, to make an **INT Check** against **12**. This Check does not require the Monster to be **Hidden** or in your **LOS**. On a success, the Monster loses **Hidden**, if applicable, and you know their exact position until the end of the round. Additionally, you gain **+1** on **SPI Checks** made to resist **Frightened** from **Undead** sources.

**Proposed**

> **Effect:** This item functions as an early warning system. When any **Undead** Monster becomes **Awake** within **12"** of you, the Charm chimes. You immediately become aware of that Monster's approximate location and that their Wake-Up condition has been met. You may then take a **[0 AP Reaction]**, even outside your activation, to make an **INT Check** against **12**. This Check does not require the Monster to be **Hidden** or in your **LOS**. On a success, the Monster loses **Hidden**, if applicable, and you know their exact position until the end of the round. You also gain **+1** on **SPI Checks** made to resist **Frightened** from **Undead** sources.

### ITEM-06: 7.17.3, The Bell's Tongue

**§2 repeated closer. Recommended.** Same closer as ITEM-05; two fragments merge.

*Line 5193, under "7.17.3 Named Special Items and Artifacts".* Dependencies: none.

**Current**

> *No surviving record describes this item clearly. The accounts that come closest describe a clapper removed from a very old bell, cold as iron left in a winter river, that rings without being struck. The Voice Beneath the Bells is mentioned in all six Bastions' folk songs. No grave has ever been found. The Bell's Tongue has no provenance. It has always existed. It has always been cold.*

**Proposed**

> *No surviving record describes this item clearly. The accounts that come closest describe a clapper removed from a very old bell, cold as iron left in a winter river, that rings without being struck. The Voice Beneath the Bells is mentioned in all six Bastions' folk songs. No grave has ever been found. The Bell's Tongue has no provenance. It has always existed, and it has always been cold.*

## Section 8: Powers

### POWER-01: 8, first paragraph

**§1 contrast, §12 words. Recommended.** The Chapter 8 introduction is the most machine-sounding passage in the book. This paragraph drops the 'not a gift' contrast, 'transcend', 'the comforting heft of', and the participle chain, and keeps every claim.

*Line 5206, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *In the Dying Lands, magic is not a gift; it is a symptom of a broken world. To cast a spell is to reach into the cracks of reality and pull something volatile through, a transaction that always leaves a stain. The common folk know better than to trust it, having learned to fear its touch through generations of curses, twisted omens, and localized catastrophe. Sensible people cling to the safety of timber walls and the comforting heft of cold iron. But the desperate, the greedy, and the doomed recognize that surviving the ruins often requires bargaining with forces that transcend the swing of a blade.*

**Proposed**

> *In the Dying Lands, magic is a symptom of a broken world. To cast a spell is to reach into the cracks of reality and pull something volatile through, and the transaction always leaves a stain. Generations of curses, twisted omens, and local catastrophes have taught the common folk to fear its touch. Sensible people keep to timber walls and cold iron. The desperate, the greedy, and the doomed know that surviving the ruins often means bargaining with forces no blade can reach.*

### POWER-02: 8, second paragraph

**§16 sales word. Recommended.** 'Profoundly' is decoration.

*Line 5208, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Though the empires that once codified magic are ash, the Five Traditions survived the Fall, each scarred, perilous, and profoundly changed.*

**Proposed**

> *Though the empires that once codified magic are ash, the Five Traditions survived the Fall, each scarred, perilous, and much changed.*

### POWER-03: 8, Arcane Spells paragraph

**§1 contrast, §12 words, §15 riders. Recommended.** Drops 'less X than they are Y', 'cold calculus', 'sheer utility', and 'invariably'. Same claims, plainer verbs.

*Line 5210, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Arcane Spells are the hollow inheritance of the old world. Wizards are less miracle-workers than they are magical scavengers, piecing together forbidden principles from half-burned grimoires and the silent, dust-choked observatories where their predecessors still sit slumped in death. Their craft is a cold calculus of arcane formulae and unstable geometry. While Bastions tolerate them for their sheer utility, wizards are rarely loved, and are invariably blamed the moment a working leaks or the dead begin to walk.*

**Proposed**

> *Arcane Spells are the hollow inheritance of the old world. Wizards are scavengers, piecing together forbidden principles from half-burned grimoires and from silent, dust-choked observatories where their predecessors still sit slumped in death. Their craft runs on arcane formulae and unstable geometry. The Bastions tolerate wizards because they are useful, rarely love them, and blame them the moment a working leaks or the dead begin to walk.*

### POWER-04: 8, Divine Prayers paragraph

**§6 triads, §9 qualifiers. Recommended.** Plainer wording. 'An insult no scripture will name' and 'not yet worthy' match the wording 1.3.1 and 1.3.4 already use for the same two doctrines.

*Line 5212, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Divine Prayers are whispered into a largely empty sky. The old saints remain in the chapel rolls, but they answer fitfully, if they answer at all. A priest capable of calling down a true working is a rarity, famous enough to command reverence and terrifying enough to be feared. The faithful fracture over the silence: some preach that the gods retreated in disgust at an unnameable insult, while others insist mortal souls simply lack the worthiness to be heard. Regardless of the doctrine, divine magic is a desperate plea for a miracle, fuelled by fanatical devotion and answered only in blood and light.*

**Proposed**

> *Divine Prayers are whispered into a largely empty sky. The old saints remain in the chapel rolls, but they answer fitfully, if at all. A priest who can call down a true working is rare, revered, and feared. The faithful split over the silence: some preach that the gods withdrew in disgust at an insult no scripture will name, and others that mortal souls are not yet worthy to be heard. Whatever the doctrine, a prayer is a desperate plea for a miracle, fuelled by fanatical devotion and answered only in blood and light.*

### POWER-05: 8, Druidic Rituals paragraph

**§16 sales language, §18 'act as'. Recommended.** Drops 'pulse with a terrifying, untamed vitality' and 'act as'. The 'do not mourn' contrast stays, because it marks the difference from the other traditions.

*Line 5214, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Druidic Rituals pulse with a terrifying, untamed vitality. Unlike the crumbling arcane or the silent divine, the magic of the wild has only grown more ferocious since the Fall. Druids commune with the encroaching forests, the choking bogs, and the violent storms. Their oldest circles do not mourn the dying world; instead, they teach that the earth is merely shedding mortal civilization like dead skin, and they act as the ruthless midwives to this violent rebirth.*

**Proposed**

> *Druidic Rituals draw on the wild, and while arcane learning crumbles and the gods stay silent, the wild has only grown more ferocious since the Fall. Druids commune with the encroaching forests, the choking bogs, and the violent storms. Their oldest circles do not mourn the dying world. They teach that the earth is shedding mortal civilization like dead skin, and they attend that violent rebirth like ruthless midwives.*

### POWER-06: 8, Sorceries paragraph

**§18 'represent', §12 words. Recommended.** 'Represent' becomes 'are'; drops 'terrible intimacy', 'raw, unrefined', 'paying for their output', and 'living conduits'.

*Line 5216, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Sorceries represent the most volatile and treacherous path to power, demanding a terrible intimacy with corruption. Some sorcerers are twisted by exposure to blighted ruin-sites, while others suffer from ancestral wounds reopening generations later, or strike infernal pacts in their darkest, most desperate hours. They wield raw, unrefined destruction, paying for their output in their own blood. Hanged in the streets of Sablekeep and treated with extreme caution everywhere else, sorcerers are living conduits of the world's sickness.*

**Proposed**

> *Sorceries are the most volatile and treacherous path to power, and the closest to corruption. Some sorcerers are twisted by exposure to blighted ruin-sites. Others carry ancestral wounds that reopen generations later, or strike infernal pacts in their most desperate hours. They wield raw destruction and pay for it in their own blood. Sablekeep hangs them in the streets, and everywhere else treats them with extreme caution. The world's sickness runs through every one of them.*

### POWER-07: 8, Psychic Abilities paragraph

**§1 contrast, §6 triad. Recommended.** Drops the 'do not study; they survive' contrast (the Psion class text already says 'not so much chosen as survived') and the padded triad.

*Line 5218, under "8. Powers and Traditions".* Dependencies: none.

**Current**

> *Psychic Abilities remain the rarest, strangest, and least understood of the traditions. Psions do not study their power; they survive it. Their minds are cracked open by the long, suffocating pressure of sunken crypts, exposure to thought-eater nests, or sheer proximity to the alien things sleeping beneath the Undermarches. They emerge from the dark hearing the jagged thoughts of everyone around them. They are rarely hunted with the same religious fervour as sorcerers, but they are never trusted, for no one welcomes a person who can weaponize a memory or peel back the privacy of a skull.*

**Proposed**

> *Psychic Abilities remain the rarest and least understood of the traditions. A psion's mind is cracked open by the long, suffocating pressure of sunken crypts, by exposure to thought-eater nests, or by nearness to the alien things sleeping beneath the Undermarches, and it comes out of the dark hearing the jagged thoughts of everyone nearby. Psions are rarely hunted with the religious fervour reserved for sorcerers, but they are never trusted, because no one welcomes a person who can weaponize a memory or peel back the privacy of a skull.*

### POWER-08: 8.4, Tier 3 Divine Prayers introduction

**§1 contrast. Recommended.** 'Not asked but demanded' stated directly.

*Line 6207, under "Tier 3 Divine Prayers (d20)".* Dependencies: none.

**Current**

> *At this height a prayer is not asked but demanded, and something always answers. Whether it is the god prayed to is a question the devout do not raise aloud.*

**Proposed**

> *At this height a prayer is a demand, and something always answers. Whether it is the god prayed to is a question the devout do not raise aloud.*

### POWER-09: 8.5, Tier 1 Sorceries introduction

**§1 contrast. Recommended.** Split 'does not X. It Y.' stated directly.

*Line 6359, under "Tier 1 Sorceries (d20)".* Dependencies: none.

**Current**

> *Sorcery does not study. It bleeds. These first workings cost little blood and never fail, which is how they teach the unwary to want more.*

**Proposed**

> *Sorcery is learned by bleeding. These first workings cost little blood and never fail, which is how they teach the unwary to want more.*

## Section 9: Monsters

### MON-01: 9, introduction

**§1 contrast. Recommended.** Same move as LORE-15.

*Line 7552, under "9. Monsters".* Dependencies: none.

**Current**

> *Beyond the Bastions, the world is no longer governed by mortal law. Roads, courts, borders, shrines, and markets have been replaced by hunger, territory, instinct, old commands, and powers that survived the Fall better than humankind did. The creatures encountered in the Dying Lands are not interruptions to an expedition; they are the present owners of the world. Some are beasts made clever by scarcity, some are the dead still obeying ruined offices, some are mortals remade by pact, curse, rot, or worship, and some are older than the kingdoms whose bones they now inhabit. Each climate teaches its inhabitants a different form of cruelty, and each has produced creatures that use that cruelty as law. To enter the wilds is not to wander into empty land. It is to trespass.*

**Proposed**

> *Beyond the Bastions, the world is no longer governed by mortal law. Roads, courts, borders, shrines, and markets have been replaced by hunger, territory, instinct, old commands, and powers that survived the Fall better than humankind did. The creatures encountered in the Dying Lands are the present owners of the world. Some are beasts made clever by scarcity, some are the dead still obeying ruined offices, some are mortals remade by pact, curse, rot, or worship, and some are older than the kingdoms whose bones they now inhabit. Each climate teaches its inhabitants a different form of cruelty, and each has produced creatures that use that cruelty as law. To enter the wilds is not to wander into empty land. It is to trespass.*

### MON-02: 9, introduction

**§1 contrast, §2 closer. Recommended.** Split 'not X. It is Y.' closer.

*Line 7552, under "9. Monsters".* Dependencies: none.

**Current**

> *Beyond the Bastions, the world is no longer governed by mortal law. Roads, courts, borders, shrines, and markets have been replaced by hunger, territory, instinct, old commands, and powers that survived the Fall better than humankind did. The creatures encountered in the Dying Lands are not interruptions to an expedition; they are the present owners of the world. Some are beasts made clever by scarcity, some are the dead still obeying ruined offices, some are mortals remade by pact, curse, rot, or worship, and some are older than the kingdoms whose bones they now inhabit. Each climate teaches its inhabitants a different form of cruelty, and each has produced creatures that use that cruelty as law. To enter the wilds is not to wander into empty land. It is to trespass.*

**Proposed**

> *Beyond the Bastions, the world is no longer governed by mortal law. Roads, courts, borders, shrines, and markets have been replaced by hunger, territory, instinct, old commands, and powers that survived the Fall better than humankind did. The creatures encountered in the Dying Lands are not interruptions to an expedition; they are the present owners of the world. Some are beasts made clever by scarcity, some are the dead still obeying ruined offices, some are mortals remade by pact, curse, rot, or worship, and some are older than the kingdoms whose bones they now inhabit. Each climate teaches its inhabitants a different form of cruelty, and each has produced creatures that use that cruelty as law. To enter the wilds is to trespass.*

### MON-03: 9.7, Wererat

**§2 repeated closer. Recommended.** 'One is X; many are Y' closes seven Monster entries. This keeps the Goblin, Dire Wolf, and Ratkin Warrior versions and trims four (MON-03 to MON-06).

*Line 8301, under "Wererat [Skirmisher]".* Dependencies: none.

**Current**

> *Where the Ashlands meet the old sewers and undercrofts, the wererat thrives, a hunched, plague-grey shapeshifter scurrying between man and rat-thing. They bite, then skitter back into the dark, leaving filth-fever in every wound. Mundane blades barely mark them. One wererat is a nuisance; a nest of them is an outbreak.*

**Proposed**

> *Where the Ashlands meet the old sewers and undercrofts, the wererat thrives, a hunched, plague-grey shapeshifter scurrying between man and rat-thing. They bite, then skitter back into the dark, leaving filth-fever in every wound. Mundane blades barely mark them. A nest of them is an outbreak.*

### MON-04: 9.7, Kobold

**§2 repeated closer. Recommended.** See MON-03.

*Line 8604, under "Kobold [Minion]".* Dependencies: none.

**Current**

> *Knee-high reptilian scavengers with dull scales and dingy picks, kobolds are the Undermarches' scuttling vermin-folk. One alone is nothing; a chittering mob of them, dragging traps and loosing slings from the dark, is a real danger. They know every tunnel and trust not one. Where a single kobold shows themselves, a whole warren is watching.*

**Proposed**

> *Knee-high reptilian scavengers with dull scales and dingy picks, kobolds are the Undermarches' scuttling vermin-folk. A chittering mob of them, dragging traps and loosing slings from the dark, is a real danger. They know every tunnel and trust not one. Where a single kobold shows themselves, a whole warren is watching.*

### MON-07: 9.7, Frozen Skeleton

**§2 repeated closer. Recommended.** 'There are always more' closes three undead Minion entries. The Undead Warrior keeps it; this entry already calls them 'countless'.

*Line 8992, under "Frozen Skeleton [Minion]".* Dependencies: none.

**Current**

> *Rimed in blue frost, a sword welded to their hand by ice, a frozen skeleton is one of the Pale City's countless dead, still standing the post they were given. They guard avenues that have not seen a living census in centuries. The cold preserves them whole; they will hold that post when the last warm thing in the world goes out. There are always more under the snow.*

**Proposed**

> *Rimed in blue frost, a sword welded to their hand by ice, a frozen skeleton is one of the Pale City's countless dead, still standing the post they were given. They guard avenues that have not seen a living census in centuries. The cold preserves them whole; they will hold that post when the last warm thing in the world goes out.*

### MON-12: 9.7, White Court Executioner

**§1 contrast. Recommended.** Split 'did not X. It only Y.' stated directly.

*Line 9265, under "White Court Executioner [Elite]".* Dependencies: none.

**Current**

> *The White Court executioner carries out sentences the living court passed centuries ago, a towering headsman whose frost-rimed axe seeks the weakest throat on the field. They stride past the hale to reach the wounded and end them with grim efficiency. The court's justice did not die with the court. It only grew patient.*

**Proposed**

> *The White Court executioner carries out sentences the living court passed centuries ago, a towering headsman whose frost-rimed axe seeks the weakest throat on the field. They stride past the hale to reach the wounded and end them with grim efficiency. The court's justice outlived the court and only grew patient.*

### MON-08: 9.7, Skeleton Warrior

**§2 repeated closer. Recommended.** See MON-07.

*Line 9408, under "Skeleton Warrior [Minion]".* Dependencies: none.

**Current**

> *A skeleton warrior stands at the post they were set in the year of their death, a sun-bleached frame in the corroded bronze of a priest-king's guard. They still hold the weapon they carried in life, waiting on an order that has not come in centuries. When intruders breach the sealed courts the order arrives at last, and the bones remember their drill. There are always more, ranked in the dark behind them.*

**Proposed**

> *A skeleton warrior stands at the post they were set in the year of their death, a sun-bleached frame in the corroded bronze of a priest-king's guard. They still hold the weapon they carried in life, waiting on an order that has not come in centuries. When intruders breach the sealed courts the order arrives at last, and the bones remember their drill, rank on rank of them in the dark.*

### MON-10: 9.7, Desert Naga

**§2 fragments. Recommended.** Two fragments become one sentence; the ambiguity of 'answer' is kept.

*Line 9552, under "Desert Naga [Controller]".* Dependencies: none.

**Current**

> *A great serpent with an almost-human face and the patient cunning of something very old, the desert naga coils among the tomb-pillars. They spit venom from a distance and crush what comes close, hexing the strong into an unnatural sleep. The priest-kings kept them as guardians and oracles. They guard still. They no longer answer.*

**Proposed**

> *A great serpent with an almost-human face and the patient cunning of something very old, the desert naga coils among the tomb-pillars. They spit venom from a distance and crush what comes close, hexing the strong into an unnatural sleep. The priest-kings kept them as guardians and oracles. They still guard, but they no longer answer.*

### MON-11: 9.7, Fire Elemental

**§2 closer. Recommended.** Restates the first sentence ('scorches whatever strikes them').

*Line 9570, under "Fire Elemental [Cannon]".* Dependencies: none.

**Current**

> *A roaring man-shape of living flame, white-hot at the core and shedding embers at the edges, the fire elemental sets alight everything they touch and scorches whatever strikes them. Water and ice are their only checks; the desert sun is their cradle. They draw a trail of cinders across the tomb-floors. To lay hands on them is to burn.*

**Proposed**

> *A roaring man-shape of living flame, white-hot at the core and shedding embers at the edges, the fire elemental sets alight everything they touch and scorches whatever strikes them. Water and ice are their only checks; the desert sun is their cradle. They draw a trail of cinders across the tomb-floors.*

### MON-09: 9.7, Giant Skeleton

**§2 closer. Recommended.** 'They guard it still' closes five guardian entries; this one adds nothing to the carving detail before it.

*Line 9587, under "Giant Skeleton [Brute]".* Dependencies: none.

**Current**

> *A looming framework of fused bone twice a man's height, the giant skeleton is what remains of something that was never entirely natural and is far less so now. They move with grinding deliberation, sweeping aside anything in their path with fists like falling masonry. Tomb-city carvings show their kind kneeling before the priest-kings; none show them standing. Whatever they were raised to guard, they guard it still.*

**Proposed**

> *A looming framework of fused bone twice a man's height, the giant skeleton is what remains of something that was never entirely natural and is far less so now. They move with grinding deliberation, sweeping aside anything in their path with fists like falling masonry. Tomb-city carvings show their kind kneeling before the priest-kings; none show them standing.*

### MON-05: 9.7, Swamp Goblin

**§2 repeated closer. Recommended.** See MON-03; also removes a verbless fragment.

*Line 9775, under "Swamp Goblin [Minion]".* Dependencies: none.

**Current**

> *Slime-streaked cousins of their forest kin, swamp goblins paddle The Mire's channels and blow poisoned darts from the reeds. They melt into the cover and strike from wherever the water hides them. A nuisance one at a time, a hazard in a swarm. They strip the drowned for trinkets and teeth.*

**Proposed**

> *Slime-streaked cousins of their forest kin, swamp goblins paddle The Mire's channels and blow poisoned darts from the reeds. They melt into the cover and strike from wherever the water hides them, and in a swarm they are dangerous. They strip the drowned for trinkets and teeth.*

### MON-06: 9.7, Stirge

**§2 repeated closer. Recommended.** See MON-03.

*Line 9814, under "Stirge [Minion]".* Dependencies: none.

**Current**

> *A bloated mosquito-thing the size of a cat, the stirge carries a needle proboscis and a belly that swells red with stolen blood. They dart in, latch on, and drain until they are pried loose. The Mire's dusk air hums with them. One is an itch; a swarm is exsanguination.*

**Proposed**

> *A bloated mosquito-thing the size of a cat, the stirge carries a needle proboscis and a belly that swells red with stolen blood. They dart in, latch on, and drain until they are pried loose. The Mire's dusk air hums with them, and a swarm can drain a body dry.*

### MON-14: 9.7, The Ancient Void Dragon

**§1 contrast. Optional.** Optional. 'Neither X nor Y but Z.' If the contrast with the fire and frost dragons is wanted, decline.

*Line 10183, under "The Ancient Void Dragon [Boss]".* Dependencies: player aid pa02.

**Current**

> *Older than the Fall and perhaps its cause, the Ancient Void Dragon is a wound in the shape of a wyrm, their scales drinking the light from the air around them. Their breath neither burns nor freezes but unmakes, peeling away substance until nothing is left. Stars seem to dim where they pass. The wise do not speak their name, and the dead do not speak at all.*

**Proposed**

> *Older than the Fall and perhaps its cause, the Ancient Void Dragon is a wound in the shape of a wyrm, their scales drinking the light from the air around them. Their breath unmakes, peeling away substance until nothing is left. Stars seem to dim where they pass. The wise do not speak their name, and the dead do not speak at all.*

### MON-15: 9.7, Captain Veyr of the Forsaken

**§2 fragments. Recommended.** A one-phrase fragment joins its sentence.

*Line 10298, under "Captain Veyr of the Forsaken [Boss]".* Dependencies: player aid pa02.

**Current**

> *Veyr was the empire's greatest captain, who swore their company would never break and held them to it past death itself. Now they lead the Forsaken in spectral plate, a duelist whose paired blades have not slowed since the empire fell. They rally their dead soldiers with a voice like a closing tomb. They no longer recall the war they are still fighting. Only the oath.*

**Proposed**

> *Veyr was the empire's greatest captain, who swore their company would never break and held them to it past death itself. Now they lead the Forsaken in spectral plate, a duelist whose paired blades have not slowed since the empire fell. They rally their dead soldiers with a voice like a closing tomb. They no longer recall the war they are still fighting, only the oath.*

### MON-16: 9.7, The Antlered Warden of the Tithe

**§1 contrast. Recommended.** Split 'does not come to X. They come to Y.' stated directly.

*Line 10364, under "The Antlered Warden of the Tithe [Boss]".* Dependencies: player aid pa02.

**Current**

> *The antlered figure admitted to Greythorn's west gate each winter does not come to bargain when the tithe goes unpaid. They come to collect. A towering shape of bone-antler and living wood, they drag the indebted into their reach and call the wild court to witness. The forest has never broken the agreement, and it does not forgive those who do.*

**Proposed**

> *When the tithe goes unpaid, the antlered figure admitted to Greythorn's west gate each winter comes to collect. A towering shape of bone-antler and living wood, they drag the indebted into their reach and call the wild court to witness. The forest has never broken the agreement, and it does not forgive those who do.*

### MON-13: 9.7, Visath the White

**§1 contrast. Recommended.** 'Does not merely X; it Y.' The ice survives in the same sentence.

*Line 10463, under "Visath the White [Boss]".* Dependencies: player aid pa02.

**Current**

> *Visath is the Pale City's eternal winter wearing the body of a wyrm, a glacier with wings and a will. Their breath does not merely freeze; it stops time in the flesh, leaving victims locked mid-scream in the ice. They rule from the highest spire and suffer no warmth anywhere in their domain. Where they fly, the snow falls harder, as though the sky itself bows.*

**Proposed**

> *Visath is the Pale City's eternal winter wearing the body of a wyrm, a glacier with wings and a will. Their breath stops time in the flesh, leaving victims locked mid-scream in the ice. They rule from the highest spire and suffer no warmth anywhere in their domain. Where they fly, the snow falls harder, as though the sky itself bows.*

## Section 10: objective and scenario lore

### SCEN-01: 10.2, Ashlands Secondary Objectives, the Reliquary

**§2 repeated closer. Recommended.** Same closer as ITEM-05; also gives the verbless second sentence a verb by joining it to the first.

*Line 11320, under "Climate 2: Ashlands Secondary Objectives (1d20)".* Dependencies: none.

**Current**

> *The Reliquary is warm to the touch. It is always warm. One of Mordain Kest's bindings, never recovered, surfacing again. Heroes who carry it report hearing a voice that does not belong to them.*

**Proposed**

> *The Reliquary is always warm to the touch: one of Mordain Kest's bindings, never recovered, surfacing again. Heroes who carry it report hearing a voice that does not belong to them.*

### SCEN-02: 10.4, Greenmark Scenario 2, Scenario-Specific Monster: Antlered Warden

**§1 contrast, §7 repeated openings. Recommended.** Keeps the correction (a reader may well expect Old Wode here) without the verbless opener.

*Line 12115, under "Scenario 2: The Whispering Grove".* Dependencies: figures FIG-13 to FIG-56 (41).

**Current**

> *Not Old Wode themselves. Old Wode does not stir for small intrusions. The Antlered Warden is the agreement's enforcement arm: a figure woven from the grove's oldest growth, robed in bark and grey moss, with antlers that have more branches than any natural animal. They do not speak. They do not negotiate. They maintain the terms.*

**Proposed**

> *This is not Old Wode, who does not stir for small intrusions. The Antlered Warden is the agreement's enforcement arm: a figure woven from the grove's oldest growth, robed in bark and grey moss, with antlers that have more branches than any natural animal. They do not speak. They do not negotiate. They maintain the terms.*

### SCEN-03: 10.4, Greenmark Scenario 2, Scenario-Specific Monster: Antlered Warden

**§7 repeated openings. Recommended.** Two parallel negatives merge.

*Line 12115, under "Scenario 2: The Whispering Grove".* Dependencies: figures FIG-13 to FIG-56 (41).

**Current**

> *Not Old Wode themselves. Old Wode does not stir for small intrusions. The Antlered Warden is the agreement's enforcement arm: a figure woven from the grove's oldest growth, robed in bark and grey moss, with antlers that have more branches than any natural animal. They do not speak. They do not negotiate. They maintain the terms.*

**Proposed**

> *Not Old Wode themselves. Old Wode does not stir for small intrusions. The Antlered Warden is the agreement's enforcement arm: a figure woven from the grove's oldest growth, robed in bark and grey moss, with antlers that have more branches than any natural animal. They do not speak or negotiate. They maintain the terms.*

### SCEN-06: 10.4, Ashlands Scenario 5, The Reliquary of Broken Saints

**§1 contrast. Recommended.** The negative half denies a claim nobody made.

*Line 12753, under "Scenario 5: The Reliquary of Broken Saints".* Dependencies: figures FIG-13 to FIG-56 (41).

**Current**

> *Broken statues and smashed reliquaries fill the hall, and sanctified bone and silver remain in the wreckage, too holy to abandon and too valuable to leave. Sablekeep needs the relics to keep its braziers lit and its authority legal, and will pay to register every fragment. The dead here are not confused. They swore to guard these relics, and death has not released them from the oath.*

**Proposed**

> *Broken statues and smashed reliquaries fill the hall, and sanctified bone and silver remain in the wreckage, too holy to abandon and too valuable to leave. Sablekeep needs the relics to keep its braziers lit and its authority legal, and will pay to register every fragment. The dead here swore to guard these relics, and death has not released them from the oath.*

### SCEN-04: 10.4, Ashlands Scenario 6, The Iron-Vein Vault

**§2 fragments, §2 closer. Recommended.** A one-phrase fragment ('Until now.') joins its sentence.

*Line 12827, under "Scenario 6: The Iron-Vein Vault".* Dependencies: figures FIG-13 to FIG-56 (41).

**Current**

> *The vault has been sealed for two generations. Karnessa Iron-Vein pressed their blood into the iron door when something inside began to leak through the walls, and the seal has held. Until now. Tremors along the imperial roads have cracked the outer binding, and something below is pushing. Sablekeep sends one party to reinforce the seal before whatever waits finishes their work; a rival patron sends another to open the vault and price what was sealed there. The vault does not care about either contract.*

**Proposed**

> *The vault has been sealed for two generations. Karnessa Iron-Vein pressed their blood into the iron door when something inside began to leak through the walls, and until now the seal has held. Tremors along the imperial roads have cracked the outer binding, and something below is pushing. Sablekeep sends one party to reinforce the seal before whatever waits finishes their work; a rival patron sends another to open the vault and price what was sealed there. The vault does not care about either contract.*

### SCEN-05: 10.4, Ashlands Scenario 6, The Iron-Vein Vault

**§2 closer. Recommended.** Most scenario introductions end on a wry one-line closer. This one, and SCEN-07 to SCEN-09, restate the sentence before them; the rest add a fact and stay.

*Line 12827, under "Scenario 6: The Iron-Vein Vault".* Dependencies: figures FIG-13 to FIG-56 (41).

**Current**

> *The vault has been sealed for two generations. Karnessa Iron-Vein pressed their blood into the iron door when something inside began to leak through the walls, and the seal has held. Until now. Tremors along the imperial roads have cracked the outer binding, and something below is pushing. Sablekeep sends one party to reinforce the seal before whatever waits finishes their work; a rival patron sends another to open the vault and price what was sealed there. The vault does not care about either contract.*

**Proposed**

> *The vault has been sealed for two generations. Karnessa Iron-Vein pressed their blood into the iron door when something inside began to leak through the walls, and the seal has held. Until now. Tremors along the imperial roads have cracked the outer binding, and something below is pushing. Sablekeep sends one party to reinforce the seal before whatever waits finishes their work; a rival patron sends another to open the vault and price what was sealed there.*

### SCEN-07: 10.4, Pale City Scenario 2, The Alchemist's Frozen Laboratory

**§2 closer. Recommended.** A stock closer; the guardians in the sentence before already carry the threat.

*Line 13466, under "Scenario 2: The Alchemist's Frozen Laboratory".* Dependencies: figures FIG-13 to FIG-56 (41).

**Current**

> *In the ice-locked Silent District, north along the road out of Hearthhold, an alchemist's laboratory remains sealed under frost. The formula inside might be worth a village, and Hearthhold burns through everything it owns just to stay warm. The cold has preserved the benches, the bottles, the last mistakes, and the guardians left to watch them. Some things in that laboratory were never meant to thaw.*

**Proposed**

> *In the ice-locked Silent District, north along the road out of Hearthhold, an alchemist's laboratory remains sealed under frost. The formula inside might be worth a village, and Hearthhold burns through everything it owns just to stay warm. The cold has preserved the benches, the bottles, the last mistakes, and the guardians left to watch them.*

### SCEN-08: 10.4, Sun-Drowned Scenario 1, The Oasis Raiders

**§2 closer. Recommended.** Restates the two-contract point.

*Line 13819, under "Scenario 1: The Oasis Raiders [Intro]".* Dependencies: figures FIG-13 to FIG-56 (41).

**Current**

> *A vital oasis south of the mountain passes has changed hands again, and raiders hold the wells, the shade, and the people too slow to flee. Saltspire sells water as sovereignty, and an oasis it does not control is a debt it cannot collect. One contract from the Well-Keepers says liberation. A rival contract says seizure. The water will not ask which seal is righteous.*

**Proposed**

> *A vital oasis south of the mountain passes has changed hands again, and raiders hold the wells, the shade, and the people too slow to flee. Saltspire sells water as sovereignty, and an oasis it does not control is a debt it cannot collect. One contract from the Well-Keepers says liberation. A rival contract says seizure.*

### SCEN-09: 10.4, Sun-Drowned Scenario 4, The Sandwyrm's Lair

**§2 closer. Recommended.** Restates the warning/inventory contrast the two sentences before it already make.

*Line 14019, under "Scenario 4: The Sandwyrm's Lair".* Dependencies: figures FIG-13 to FIG-56 (41).

**Current**

> *Nomad legends speak of a vast shape beneath the dunes south of the passes, and a gullet lined with the treasure of everything they have swallowed. The nomads tell it as a warning. Saltspire's patrons hear it as an inventory and pay accordingly. The dunes do not distinguish between the two kinds of listener.*

**Proposed**

> *Nomad legends speak of a vast shape beneath the dunes south of the passes, and a gullet lined with the treasure of everything they have swallowed. The nomads tell it as a warning. Saltspire's patrons hear it as an inventory and pay accordingly.*

### SCEN-10: 10.4, Mire Scenario 1, Scenario-Specific Monster: Salttide's Shade

**§7 repeated openings. Recommended.** 'They watch' three times in a row.

*Line 14271, under "Scenario 1: The Reliquary of Edrava Salttide [Intro]".* Dependencies: figures FIG-13 to FIG-56 (41).

**Current**

> *Edrava Salttide has not finished counting. The Mire preserved them, and it is patient. The Shade does not speak. They watch the reliquary. They watch the water. They watch every hand that reaches for what belongs to them.*

**Proposed**

> *Edrava Salttide has not finished counting. The Mire preserved them, and it is patient. The Shade does not speak. They watch the reliquary, the water, and every hand that reaches for what belongs to them.*

## Section 11: campaign

### CAMP-01: 11, first paragraph

**§2 fragments. Recommended.** A row of fragments becomes the end of the sentence it illustrates.

*Line 15021, under "11. Campaign Play".* Dependencies: none.

**Current**

> *In the Dying Lands, a single **Skirmish** is a transaction. Blood for coin. Risk for salvage. A name crossed off a roster so another name can eat for a week. A campaign is the longer ledger. It records what the party won, what it spent, who carried the chest, who did not stand up, and which debts waited at the gate.*

**Proposed**

> *In the Dying Lands, a single **Skirmish** is a transaction: blood for coin, risk for salvage, and a name crossed off a roster so another name can eat for a week. A campaign is the longer ledger. It records what the party won, what it spent, who carried the chest, who did not stand up, and which debts waited at the gate.*

### CAMP-02: 11, third paragraph

**§2 fragments. Recommended.** Same fragment row as LORE-17, fixed the same way.

*Line 15025, under "11. Campaign Play".* Dependencies: none.

**Current**

> *Councils, chapels, guilds, and discreet nobles use smaller tools. They hire parties. Small enough to hide. Strong enough to fight. Cheap enough to lose. Each contract begins as ink on a table inside the walls. It ends in mud, ash, snow, salt, or blood.*

**Proposed**

> *Councils, chapels, guilds, and discreet nobles use a smaller tool. They hire parties small enough to hide, strong enough to fight, and cheap enough to lose. Each contract begins as ink on a table inside the walls. It ends in mud, ash, snow, salt, or blood.*

### CAMP-03: 11, seventh paragraph

**§2 fragments. Recommended.** Six fragments become one list; every item and every bold term stays.

*Line 15033, under "11. Campaign Play".* Dependencies: none.

**Current**

> *Between **Skirmishes**, survival is counted in smaller measures. A blade recovered from a corpse. A shield hammered flat and bound with wire. A **Hireling** paid before they desert. A **Hero** carried back breathing, though not whole. A name scratched from the **Roster**. A debt moved from one column to another. The **Treasury** grows by contract pay, salvage, theft, and **Monster** blood. **Storage** fills with gear stripped from the dead and saved for the living. The **Bench** waits behind the walls, healing, drinking, praying, or pretending not to hear the next contract read aloud.*

**Proposed**

> *Between **Skirmishes**, survival is counted in smaller measures: a blade recovered from a corpse, a shield hammered flat and bound with wire, a **Hireling** paid before they desert, a **Hero** carried back breathing though not whole, a name scratched from the **Roster**, and a debt moved from one column to another. The **Treasury** grows by contract pay, salvage, theft, and **Monster** blood. **Storage** fills with gear stripped from the dead and saved for the living. The **Bench** waits behind the walls, healing, drinking, praying, or pretending not to hear the next contract read aloud.*

### CAMP-04: 11.1, first lore paragraph

**§1 contrast, §7 repeated openings. Recommended.** 'Not a castle in the noble sense' is then explained twice; the two explanations carry it.

*Line 15041, under "11.1 Campaign Overview".* Dependencies: none.

**Current**

> *A **Stronghold** is not a castle in the noble sense. No ancient bloodline sanctifies it. No bard remembers its founding. It is a claim driven into a dying world with coin, fear, salvage, and stubborn labour. Its stones come from ruined shrines, abandoned watch-keeps, broken bridges, and walls that failed other people first. Its gates are paid for with burial gold, bounty coin, chapel debt, and the last wages of the dead.*

**Proposed**

> *A **Stronghold** has no ancient bloodline to sanctify it and no bard to remember its founding. It is a claim driven into a dying world with coin, fear, salvage, and stubborn labour. Its stones come from ruined shrines, abandoned watch-keeps, broken bridges, and walls that failed other people first. Its gates are paid for with burial gold, bounty coin, chapel debt, and the last wages of the dead.*

### CAMP-05: 11.1, third lore paragraph

**§1 contrast, §2 fragments. Recommended.** Two staged contrasts in a row ('not mercy. It is weight.' and 'more than X. It becomes Y.'). The weight and the list of what the party becomes stay.

*Line 15045, under "11.1 Campaign Overview".* Dependencies: none.

**Current**

> *To build a Stronghold is to stop running long enough to answer for other people. That is not mercy. It is weight. A party becomes more than adventurers with blades and debts. It becomes a name in ledgers, a mark on maps, a rumour at gates, and a provocation beyond the watch-fire. Its enemies no longer need to hunt it across the Dying Lands. They know where to come.*

**Proposed**

> *To build a Stronghold is to stop running long enough to take on the weight of answering for other people. The party becomes a name in ledgers, a mark on maps, a rumour at gates, and a provocation beyond the watch-fire. Its enemies no longer need to hunt it across the Dying Lands. They know where to come.*

### CAMP-06: 11.3, The Vault

**§1 contrast. Recommended.** The negative half denies a claim nobody made.

*Line 15668, under "The Vault".* Dependencies: player aid pa08, pa09.

**Current**

> *The Vault is not a treasury. It is a sealed confession of greed, iron-bound and watched by clerks who sleep in shifts. They count each coin as if the dead might come back to collect.*

**Proposed**

> *The Vault is a sealed confession of greed, iron-bound and watched by clerks who sleep in shifts. They count each coin as if the dead might come back to collect.*

### CAMP-07: 11.3, The Armoury

**§1 contrast, §2 closer. Recommended.** Split 'does not look X. It looks Y.' stated directly.

*Line 15690, under "The Armoury".* Dependencies: player aid pa08, pa09.

**Current**

> *A party with an Armoury does not look safe. It looks prepared. In the Dying Lands, that is close enough to hope.*

**Proposed**

> *A party with an Armoury looks prepared, and in the Dying Lands that is close enough to hope.*

## Appendix A: Learn to Play

### LEARN-01: A.11, closing paragraph

**§1 contrast, §2 'this shows'. Recommended.** 'This shows why X is not merely Y' is the strongest tell in the rules text. The replacement states what the two rounds showed; the rest of the paragraph is unchanged.

*Line 16544, under "Round 2".* Dependencies: figures FIG-18.

**Current**

> This opening shows why Heraldry Skirmish is not merely a damage race. Edric seized the objective quickly, but spending all **3 AP** left them unable to **Dodge**, **Block**, or **Parry**. Varek punished the exposed carrier, the Dire Wolves punished the centre scrum, and Mara earned coins only by taking a flank objective while the main fight collapsed.

**Proposed**

> Both rounds turned on **AP** and objectives more than on damage. Edric seized the objective quickly, but spending all **3 AP** left them unable to **Dodge**, **Block**, or **Parry**. Varek punished the exposed carrier, the Dire Wolves punished the centre scrum, and Mara earned coins only by taking a flank objective while the main fight collapsed.
