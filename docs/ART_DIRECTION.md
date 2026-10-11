# Heraldry illustration direction

This document governs atmospheric illustration and art planning. MASTER_PROMPT.md governs source fidelity, asset QA, and placement. The manuscript, not this brief, supplies setting facts.

## Hand-inked direction (owner, 2026-10-11)

The owner judged the first ChatGPT Work calibration images "too hyper detailed, AI-like, low-resolution". The target is "a notch more hand drawn and authentic human art-like". The examples are the owner's three samples (STYLE-REF-01, -02 and -03, below) plus a Dying Lands map kept as line inspiration (`assets/art/style/STYLE-INSPIRATION-map-dying-lands.png`; it carries lettering, so it is never attached). Consequences:

- Prompts (`prompt_v2` in `config/art_style.json`) ask for confident hand-inked line with dip pen and brush, economy of line, selective hatching, generous open paper and detail only at the focus. They no longer ask for "exceptionally detailed", "intricate crosshatching" or stippling, wording that drove the hyper-detailed look.
- Only the owner's samples are attached as references. Generated images, even approved ones, are never style references, so model output cannot compound its own drift.
- Resolution: the queue size is the minimum at a fixed aspect, and Work requests the largest size offered.
- Model: GPT Image 2.5 Sunburst if ChatGPT Work offers it; the model shown is recorded in each receipt.
- The five calibration anchors of 2026-10-11 were set back to redo under this direction. Greythorn, the owner's own render from the owner's verbatim prompt, stays approved but is no longer a style reference.

## Shared style (owner-defined 2026-10-08)

The operative wording is `style` in `config/art_style.json`. It was derived from three owner samples, kept privately in `assets/art/style/` and never packaged:
- a hatched town scene, which sets the hatching, skies and scene density;
- a line-only panorama, which sets detail with lots of white paper;
- a skeleton warrior, which sets figures: bold contour, spot blacks, isolated on white.

It also draws on classic black-and-white RPG interior art (bold woodcut-like contours, dense hatching) and Dark Souls' "withered beauty" (decayed grandeur, gothic ruin at overwhelming scale, quiet dread).

The illustrator works in two registers with one hand:
- **Figures:** monsters, ancestries, classes, backgrounds, traditions and items, isolated on white.
- **Scenes:** cover, chapters, world sections, climates, bastions, scenarios and campaign rooms. These are vignettes that thin into white paper.

Counter-example: the original ART-CH01-001 master's dense, near-photographic darkness muddies at spot size and is not the target. Mood comes from subject, decay and solid black shapes, not from grey tone.

The paragraphs below remain as background.

Rough black-and-white medieval fantasy pen-and-ink illustration. Expressive, slightly irregular nib lines, convincing economical contour drawing, dense but purposeful crosshatching, dry-brush accents, subtle stippling, strong silhouettes, open paper-white negative space, selective pools of black. The appearance of accomplished hand-drawn ink rather than photorealism or a polished digital render. Severe, weathered, grounded, inhabited, and materially coherent. Distress belongs in the depicted world and drawing marks; keep the image substrate clean enough for print.

Keep one coherent visual identity across figures, architecture, creatures, equipment, and landscape. Anatomically plausible bodies and believable medieval construction. Subjects must match the active manuscript lore and rules. Interpret miniature-agnostic as freedom from branded sculpt ranges; do not add an imaginary proprietary miniature line.

Exclude colour accents, glossy 3D, photographic lighting, airbrushed smooth gradients, anime/cartoon style, decorative pseudo-writing, visible text, logos, signatures, watermarks, faint square grids, repeated tiling artefacts, and named-artist imitation. Do not label generated images as human-made.

## Reusable ChatGPT/image-service prompt

Replace the braces with one asset's specification, and attach the approved style-anchor image where reference images are supported:

```text
Create an original illustration for HERALDRY SKIRMISH: THE DYING LANDS,
a dark medieval fantasy tabletop skirmish rulebook.

SUBJECT: {source-supported subject and exact lore details}
SCENE: {specific setting, figures, equipment, action, and focal point}
COMPOSITION: {aspect ratio, camera/viewpoint, intended crop, negative-space locations}
PRINT PLACEMENT: {intended physical size and required native pixel dimensions}

Use rough black-and-white pen-and-ink drawing: expressive irregular nib lines,
controlled crosshatching, dry-brush accents, occasional stippling, readable silhouettes,
deliberate paper-white negative space, and selective dense black shapes.
It should have the visual character of a skilled medieval fantasy ink illustrator's
hand-drawn work, without photographic rendering or glossy digital airbrushing.
Keep architecture, anatomy, clothing, weapons, and material details coherent.
Match the attached approved reference's line character, contrast, and degree of finish
when a reference is supplied.

No embedded lettering, title, label, signature, logo, watermark, colour, faint grid,
decorative pseudo-script, tiling, or parchment texture behind the entire image.
Leave the specified negative space useful for separately typeset book elements.
Follow the requested dimensions where supported; do not claim an unsupported resolution.
```

## Production plan

1. Plan a source-specific cover scene and one representative chapter image as the style test. The approved anchor is an internal quality gate; the autonomous agent need not request approval.
2. Prioritise the cover hero image and 11 chapter-opening images. Read each actual chapter and derive its subject, not merely its title. Optional climate, creature, item, and landscape vignettes follow after the required suite.
3. Number assets with stable IDs, for example `ART-COVER-001` and `ART-CH01-001`. Use the same IDs in the manifest and filenames. Preserve native originals and separate final grayscale/crop derivatives.
4. When a generated image has limited native resolution, place it smaller or use a supported high-resolution route and inspect the result. Changing a DPI tag or resampling does not create authentic fine detail.
5. Assess style consistency using a contact sheet and assess final crops at print size. Check setting accuracy, visual artefacts, muddy blacks, hatching survival, and space for titles.

Do not hand-generate 12 polished atmospheric illustrations with procedural silhouette code and claim the image-generator route succeeded. When no art service/assets are configured, create polished original vector ornaments, finish the art-light edition, and deliver detailed ready-to-run prompts and insertion instructions for the missing suite.

## Diagram distinction

Rules diagrams use crisp editable vector geometry, clean typography, consistent patterned terrain, clear base/party symbols, arrows, dimensions, and legible legends. Their subject matter may carry the medieval identity, but their geometry and wording must be exact. They are not drawn by an atmospheric image generator.

## Finish criteria for the light borderless edition

Follow VISUAL_QA.md. Keep foreground ink separate from the page substrate. Transparent spot art or a clean matte matching the actual cream is preferred; preserve native masters and avoid a bright rectangular paper patch or fringe. Use controlled asymmetry and specific source-supported equipment/architecture rather than generic skulls, hooded warriors, ornate weapons, smoke and spires repeated across chapters. Choose one clear focal subject and readable silhouette for each small vignette; cut incidental hatch before it turns into muddy grey at print size.

Review hands, joints, armour closures, weapon grips, material transitions, masonry, scale and setting facts in enlarged crops, then inspect the placed size. A beautiful texture cannot rescue incoherent construction. The dark-fantasy character must survive a paper-white background without blanket grain or a heavy frame. This is a visible-quality contract, not a promise to hide generated provenance or an instruction to misrepresent authorship.


## Current reference calibration and artwork route

Use the ten owner-selected references in REFERENCE_ANALYSIS.md for abstract silhouette, ink and composition lessons. Since the owner decision of 2026-10-10, all artwork is generated in ChatGPT Work through the queue and intake route in ART_AUTOMATION.md, with `config/art_style.json` (prompt_v2) and the per-entry briefs as the operative art direction. Claude approves the style anchors and reviews native resolution, ink edges, setting fidelity and final-size quality.
