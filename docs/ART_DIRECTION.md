# Heraldry illustration direction

This document governs atmospheric illustration and art planning. `docs/PROJECT_CONTRACT.md` governs source fidelity, asset QA, and placement. The manuscript, not this brief, supplies setting facts.

## Gritty old-school direction (owner, 2026-10-11, later; current)

The owner asked to "redo the art inspiration a bit to move our current art benchmarks and inspiration to be closer to the more old school black and white gritty style artworks" and supplied eleven examples. This supersedes the "economy of line" wording below; the hand-inked rules (human marks, no AI polish, no stipple fields, only owner samples as references) still hold.

- **Target:** gritty old-school black-and-white ink, as in late-1970s and 1980s rulebook and module art. That means:
  - bold, rough brush contours of uneven weight;
  - heavy solid-black shadow shapes;
  - scratchy hatching and dry-brush drag where form turns;
  - the bite of a woodcut;
  - high contrast, with few in-between textures;
  - visible human imperfection (broken lines, dry-brush streaks, an occasional ink fleck).
- **Still forbidden:** grey wash or grey ink tone, stipple fields, uniform machine texture, clean vector-like line, digital polish and airbrush. The book uses pure black ink.
- **References, mapping v7** (owner instruction 2026-10-11: reanalyse every reference and map it optimally). Files are in `assets/art/style/`, recorded in `STYLE_REFS.json`, and never placed or packaged. Each item gets at most 5 (owner 2026-10-12 asked for up to six; the Codex image tool accepts at most five, so the cap is 5 and 64 armour sheet left the item set), chosen in `gpt_reference_sets` in this order of precedence: `kind_sets` (monsters, by ID), then `family_sets`, then the register `sets`. Every set draws on the gritty core. Clean-line pieces appear only where their subject has no gritty match (36 insect anatomy, 20 armoury, 15 weapons, 02 city).

  | Images | References |
  |---|---|
  | Monsters: undead (30) | 04 skeleton king, 03 skeleton warrior, 52 crowned lich, 51 bandaged mummy |
  | Monsters: beasts (12) | 18 bear, 22 wolf pack (owner-approved scenery risk), 70 chimera, 74 winged reptile |
  | Monsters: vermin and aberrations (17) | 36 crab insectoid, 35 grub beast, 72 mantis insectoid, 71 tree creature |
  | Monsters: humanoids and beastfolk (39) | 38 gnoll, 32 goat-folk spearman, 50 flame-sword elf, 66 troll pair |
  | Monsters: dragons, demons, elementals, constructs (22) | 16 dragon-man, 68 coiled dragon, 73 manticore, 69 hydra |
  | Bosses | 10 undead crowd, 05 cave creature, 49 swordsman on a mountain pass, 60 skeletal standard-bearer |
  | Classes and ancestries | 06 hooded archer, 41 Callot beggar, 54 dwarf warrior, 57 armoured swordswoman, 61 herbalist |
  | Backgrounds | 19 pack, rope and lantern; 34 gear sheet; 25 bracers; 39 poison flask |
  | Items | 15 sword and mace, 40 rag-wrapped scythe, 27 carved scroll case (pseudo-writing risk), 33 bone cross, plus extras 56 weapons sheet and 64 armour sheet  |
  | Spell tiers | 29 holy fire, 26 summoning, 63 wizard casting flame, 28 wizard vs fiend |
  | Stronghold rooms | 20 armoury, 37 dungeon pits, 43 Piranesi drawbridge, 23 dungeon arches |
  | Climates | 44 Haden vignette, 13 cave river, 17 swamp hut, 47 barrow on the moor |
  | Scenarios | 09 skeleton melee, 21 party on a forest path, 31 dungeon melee, 67 sewer ghoul ambush, 07 dry-brush duel |
  | World sections | 30 forest path, 58 flight from collapsing ruins, 55 siege wall-climb, 44 |
  | Bastions | 11 city approach, 02 city panorama, 45 cathedral facade, 53 frost harbour city |
  | Chapters | 46 round tower, 65 ship and dead tree, 59 harbour wharf, 43 |
  | Cover | 11 city approach, 47 barrow, 46 round tower, 65 ship on the coast |

- **Public-domain additions** (Claude sourced these on owner instruction to fill the gaps, from the Art Institute of Chicago's CC0 images; each scan was levelled to black on white and its plate number or signature painted out):
  - 41 and 42: Callot beggars. Isolated full-length figures with bold swelling line.
  - 43: Piranesi, *The Drawbridge*. Colossal architecture and heavy etched blacks.
  - 44: Haden, *Challow Farm*. A landscape vignette that dissolves into paper.
- **Bank promoted** (owner, 2026-10-12: "promote them if there is room ... include risky"): one banked image joined each set it fits best, shown in the table above. The owner accepted these risks:
  - 12 and 17 carry grey tone, 23 screen tone, and 30 and 31 stipple fields: the generator may copy the tone, which the checks still reject.
  - 32, 35 and 39 are small; 24 is cleaner than the core.
- **Owner samples 45 to 52** (2026-10-12): see the table. 52 lich and 51 mummy replace 38 gnoll in the undead set (38 stays in beasts and humanoids). The owner removed 22 wolf pack the same day, then restored it to beasts.
- **Owner samples 54 to 67** (2026-10-12): placed as in the table, replacing shared images toward four unique per set. Caveats: grey tone in 55, 58, 59 and 62; a dark backdrop behind the 62 figure; a monogram on 65.
- **Review 2026-10-12** (owner: review every reference and category): 54 and 57 replace 08 and 42 in classes and ancestries (period costume and a beggar are poor adventurer models); 63 replaces 28 in spell tiers (28 stays in magical); 46 and 65 replace 29 and 43 on the cover (establishing scenes with sky); 47 replaces 07 in climates (no figures in a terrain set). Vermin and magical keep 18 and 16 as their weakest members: the only alternatives (05, 26) are scenes, which must not reach isolated figures.
- **Creature samples 68 to 74** (2026-10-12): beasts, vermin and magical monsters now use only images of their own kind; 16, 18 and 38 each belong to one set. Caveats: 71 has grey-looking dense hatching; 70 and 73 are composite or human-faced creatures that must not be copied onto other subjects.
- **Second review 2026-10-12:** 50 replaces 62 in humanoids (no backdrop behind isolated figures); 69 hydra replaces 28 in magical (no human figure in a creature set); 28 replaces 12 in spell tiers (no grey screen tone).
- **Promoted to six-per-set limit 2026-10-12:** 61 herbalist (classes and ancestries) and 07 dry-brush duel (scenarios).
- **Still on file, not attached:** 62 ratman (dark backdrop), 12 wizard storm (screen tone), 08 fencers and 42 Callot beggar on crutches (period costume); 48 bearded warrior (no slot, and its black box background could teach a frame); 14 (signed still life); 24 flanged mace (the cleanest still life, replaced in items by the owner's choice of 40, 27 and 33).
- **Still open:** no gritty desert, ash-waste or snow landscape example exists in the public domain at usable quality. Those climates rely on their prompts plus the general landscape references 44, 13 and 07.
- **Mood only:** three ink-wash examples (`STYLE-INSPIRATION-wash-*`) are never attached, because the book's art is pure black ink with no grey tone.
- **Cut and superseded:** the owner cut STYLE-REF-01 (it remains in git history) and replaced it with STYLE-REF-11, an owner exception to the rule against machine-made references.
- **Prompts:** `prompt_v2` (intro, `style_scene`, `style_figure`, `style_still`, `final_*` and `reference`) carries this wording. The v7 audit replaced 32 brief details that asked for dense stipple with ink flecks, dry-brush or hatching, and gave still lifes their own equipment-art style line. The queue was republished.
- **Approved art:** the owner cleared every earlier approval on 2026-10-12; everything approved since was made under this direction.

## Hand-inked direction (owner, 2026-10-11)

The owner judged the first ChatGPT Work calibration images "too hyper detailed, AI-like, low-resolution". The target is "a notch more hand drawn and authentic human art-like". The examples are the owner's three samples (STYLE-REF-01, -02 and -03, below) plus a Dying Lands map kept as line inspiration (`assets/art/style/STYLE-INSPIRATION-map-dying-lands.png`; it carries lettering, so it is never attached). Consequences:

- Prompts (`prompt_v2` in `config/art_style.json`) ask for confident hand-inked line with dip pen and brush, economy of line, selective hatching, generous open paper and detail only at the focus. They no longer ask for "exceptionally detailed", "intricate crosshatching" or stippling, wording that drove the hyper-detailed look.
- Only the owner's samples are attached as references. Generated images, even approved ones, are never style references, so model output cannot compound its own drift.
- Resolution: the queue size is the minimum at a fixed aspect, and Work requests the largest size offered.
- Model: GPT Image 2.5 Sunburst if ChatGPT Work offers it; the model shown is recorded in each receipt.
- The five calibration anchors of 2026-10-11 were set back to redo under this direction. Greythorn, the owner's own render from the owner's verbatim prompt, stays approved but is no longer a style reference.

## Shared style (owner-defined 2026-10-08)

The operative wording is `style` in `config/art_style.json`. It was derived from three owner samples, kept in `assets/art/style/` and never packaged:
- a hatched town scene, which sets the hatching, skies and scene density;
- a line-only panorama, which sets detail with lots of white paper;
- a skeleton warrior, which sets figures: bold contour, spot blacks, isolated on white.

It also draws on classic black-and-white RPG interior art (bold woodcut-like contours, dense hatching) and Dark Souls' "withered beauty" (decayed grandeur, gothic ruin at overwhelming scale, quiet dread).

The illustrator works in two registers with one hand:
- **Figures:** monsters, ancestries, classes, backgrounds, traditions and items, isolated on white.
- **Scenes:** cover, chapters, world sections, climates, bastions, scenarios and campaign rooms. These are vignettes that thin into white paper.

Counter-example: the original ART-CH01-001 master's dense, near-photographic darkness muddies at spot size and is not the target. Mood comes from subject, decay and solid black shapes, not from grey tone.

The paragraphs below remain as background.

Rough black-and-white medieval fantasy pen-and-ink illustration. Expressive, slightly irregular nib lines, convincing economical contour drawing, dense but purposeful crosshatching, dry-brush accents, subtle stippling, strong silhouettes, open paper-white negative space, selective pools of black. The appearance of accomplished hand-drawn ink rather than photorealism or a polished digital render. Severe, weathered, grounded, inhabited, and materially coherent. Distress belongs in the depicted world and drawing marks; keep the image substrate clean.

Keep one coherent visual identity across figures, architecture, creatures, equipment, and landscape. Anatomically plausible bodies and believable medieval construction. Subjects must match the active manuscript lore and rules. Interpret miniature-agnostic as freedom from branded sculpt ranges; do not add an imaginary proprietary miniature line.

Exclude colour accents, glossy 3D, photographic lighting, airbrushed smooth gradients, anime/cartoon style, decorative pseudo-writing, visible text, logos, signatures, watermarks, faint square grids, repeated tiling artefacts, and named-artist imitation. Do not label generated images as human-made.

## Diagram distinction

Rules diagrams use crisp editable vector geometry, clean typography, consistent patterned terrain, clear base/party symbols, arrows, dimensions, and legible legends. Their subject matter may carry the medieval identity, but their geometry and wording must be exact. They are not drawn by an atmospheric image generator.

## Finish criteria for the light cream page

Follow VISUAL_QA.md. Keep foreground ink separate from the page substrate. Transparent spot art or a clean matte matching the actual cream is preferred; preserve native masters and avoid a bright rectangular paper patch or fringe. Use controlled asymmetry and specific source-supported equipment/architecture rather than generic skulls, hooded warriors, ornate weapons, smoke and spires repeated across chapters. Choose one clear focal subject and readable silhouette for each small vignette; cut incidental hatch before it turns into muddy grey at placed size.

Review hands, joints, armour closures, weapon grips, material transitions, masonry, scale and setting facts in enlarged crops, then inspect the placed size. A beautiful texture cannot rescue incoherent construction. The dark-fantasy character must survive the light cream page without blanket grain or a heavy frame. This is a visible-quality contract, not a promise to hide generated provenance or an instruction to misrepresent authorship.

## Artwork route

Art is generated through the owner's ChatGPT plan (Codex is the current route), through the queue and intake in `docs/ART_AUTOMATION.md`, with `config/art_style.json` (`prompt_v2`) and the per-entry briefs as the operative art direction. Whoever generates an image may review and approve it after looking at its native resolution, ink edges, setting fidelity, and final-size quality.
