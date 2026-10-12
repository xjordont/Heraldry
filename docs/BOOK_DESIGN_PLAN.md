# Book design plan: "Ink and Iron" (design system v2)

Status: owner-requested design pass (2026-10-12). The templates are implemented as Typst components in `typst/templates/system.typ` and shown on fourteen specimen pages in `typst/templates/specimens.typ`. These are set with real RC492 text, approved art and the real vector figures, and rendered to PNG by `tools/render_template_specimens.py`. No book PDF was produced.

The current book build (`typst/heraldry.typ`) is unchanged until the owner asks for a build. Then it adopts this system as described in section 10.

The evidence is in `docs/design/REFERENCE_STUDY.md`: all ten reference books were mapped page by page, and about 90 pages were inspected closely.

This plan supersedes the visual identity sections of `DESIGN_SPEC.md` (display face, heading styles, furniture, component styling). The pagination contract in `DESIGN_REFINEMENT.md` stays in force without change. That contract covers fresh-page starts, mandatory one-page keeps and continuation rules.

## 1. The idea

The book should read as a rulebook printed from woodcut-era type and drawn in iron-gall ink, but laid out with modern information design. Every page should be easy to read.

- **Mood** comes from three sources:
  - the display face, IM FELL, a revival of the 17th-century Fell types with real press texture;
  - the gritty ink art;
  - solid black accents: number blocks, header bars and thumb tabs.
- **Legibility** comes from three sources:
  - a quiet, very readable serif for all rules;
  - a clear sans for every number and label;
  - generous, consistent spacing.
- **Nothing decorates the reading field.** Text is never set on a texture. There is no paper grain and no perimeter frame, and no colour carries meaning. Ornament is one small original family used at boundaries only.

The ordinary rules page is the product. The cover and chapter openers set the mood, but the book succeeds or fails on its 500 working pages.

## 2. Page and grid

| Element | Value |
|---|---|
| Trim | US Letter portrait, 612 × 792 pt, borderless inkjet; cream `#FCFAF5` and a white companion with identical pagination |
| Margins | inside (binding) 0.875 in, outside 0.6 in, top 0.8 in, bottom 0.8 in |
| Text frame | 7.025 × 9.4 in; two columns of 3.39 in with a 0.25 in gutter |
| Edge safety | essential content at least 0.375 in from every edge (thumb tabs are navigation, not essential) |
| Full-width regions | section titles, chapter openers, wide tables, wide figures, scenario heads |
| Column regions | prose, examples, notes, monster entries, powers, dossiers |

The 0.8 in top margin leaves room for the running head and its double rule, which Mythras showed is the one piece of furniture worth its space.

## 3. Type

Three families are used, all under the OFL, with licences in `fonts/licences/`.

| Role | Face | Size / leading | Notes |
|---|---|---|---|
| Body | Source Serif 4 | 10.25 / 13.4 pt, ragged right | Hyphenation on (en-CA). Ragged right avoids the rivers that justification opens in 3.4 in columns |
| Chapter title | IM FELL English SC | 44 pt | Centred under the opener art |
| Section (x.y) | IM FELL English SC | 21 pt | Black number block in Source Sans 3 Bold 10 pt reversed, then a thick-and-thin rule |
| Subsection (x.y.z) | Source Serif 4 Bold | 12.5 pt | Quiet number in Source Sans 3 Bold 9.5 pt, 45% grey |
| Minor named heading | IM FELL English SC | 12.5 pt | For named rules and talent tiers |
| Entry names | IM FELL English SC | 14 to 30 pt | Monster 17 pt, power 14 pt, class 30 pt, place 22 pt, scenario 28 pt |
| Flavour and leads | IM FELL English Italic | 10.6 to 13 pt | Short passages only. Long lore uses Source Serif 4 Italic |
| Labels and tags | Source Sans 3 Bold | 7 to 7.6 pt caps, +0.12 to 0.16 em tracking | Entry anatomy, dossier fields, example tags |
| Tables | Source Sans 3 | 9.2 pt (8.8 pt in Appendix C) / about 12 pt | Tabular lining figures. Header caps 7.6 pt reversed |
| Captions | Source Sans 3 | 8.6 pt | Number and title in the black caption bar |
| Running head | Source Sans 3 SemiBold | 7.4 pt caps, +0.16 em | |
| Folio | IM FELL English SC | 11 pt | Old-style figures, with a short taper toward the gutter |

The minimum essential size is 8.6 pt for captions and 8.8 pt for dense reference tables. The DESIGN_SPEC floor of 9 pt for running text still applies to body copy.

Cinzel is retired. It is common in fantasy games and lacks the press texture of the art. IM FELL's old-style figures are kept out of anything that must be read as a number (thumb tabs, tables, stat bars). Those use Source Sans 3.

## 4. Ink, tone and ornament

- **Ink:** black only.
  - Secondary text is 22% grey.
  - Furniture labels and quiet numbers are 45% grey.
  - Hairlines are 28% black.
  - Tints are transparent black: 5.5% for example fields, dossiers and table banding; 9% for the roll column.
  - Transparent tints sit correctly on both the cream and white substrates.
- **Solid black** marks structure, never decoration:
  - section number blocks;
  - table header bars;
  - stat bars;
  - figure caption bars;
  - cost tags;
  - thumb tabs;
  - the Appendix C reference heads.

  Each is small, so an ordinary page carries well under 3% solid black.
- **Ornament family** (original):
  - the lozenge and the voided lozenge (a heraldic mascle);
  - tapered rules;
  - the thick-and-thin double rule.

  The double rule closes the running head, every section title, scenario and character heads, and the gazetteer. The flourish (taper, mascle, taper) appears only on chapter openers, title, contents, index and back cover. An ordinary page carries no more than two ornaments.
- **Not used:**
  - texture, stains, burned edges or parchment;
  - frames around pages;
  - drop shadows or gradients;
  - icons that would need a legend;
  - colour.

## 5. Navigation

- **Running heads:**
  - The verso carries the chapter name, flush to the outside edge.
  - The recto carries the current section, flush to the outside edge.
  - A lozenge marks the outer end.
  - A thick-and-thin rule sits beneath.
  - Heads are suppressed on chapter openers, scenario openers, the title page, contents and full-art pages.
- **Folios:** at the outer bottom corner, with a taper toward the gutter.
- **Thumb tabs:** black tabs bleed off the outer edge. There are 14 fixed slots: chapters 1 to 11, and appendices A, B and C, labelled "A", "B" and "C". The index uses the last slot, labelled "Ix". The closed book shows a stepped index. The chapter number is reversed in Source Sans 3 Bold, centred about 0.27 in from the trim. Tabs are navigation only: the running head always names the chapter, so a trimmed tab loses nothing.
- **Contents:** two columns. Each chapter row has a display numeral and title over a rule, with its page. Each section line has a sans number, a serif title and dot leaders to the page. The contents is two levels deep; deeper levels live in the PDF bookmarks.
- **Index:** three columns, large display initials over a rule, sans 8.6 pt entries with hanging indents and grey page numbers.
- **Digital:** linked contents and index, PDF bookmarks, and clickable cross references ("see 10.6.4"). These are built from the existing anchors.

## 6. Page-type catalogue

Each template lists its components, its pagination rule (in addition to DESIGN_REFINEMENT), its art rule and the specimen page that shows it. Reference lessons are in `docs/design/REFERENCE_STUDY.md`.

### 6.1 Cover, front and back (existing `typst/cover.typ`)

- **Front:** keeps its current construction and gains the IM FELL wordmark of the title page.
- **Back cover (specimen 14):**
  - a flourish;
  - a short italic line from the manuscript's opening;
  - a single creature vignette;
  - the wordmark and strapline at the foot.

  This follows the Black Death City back-cover lesson: one image and one line, nothing busy.

### 6.2 Title page (specimen 1)

- Strapline in sans caps.
- "Heraldry" in 62 pt display, with "Skirmish" in 27 pt tracked display beneath.
- A flourish, then the cover art (ART-COVER-002) at full frame width.
- An italic line, and the release line at the foot.
- No running furniture.

### 6.3 Credits and colophon (verso of the title)

- Sans 8.5 pt in a single column, set low on the page.
- Contents: credits, licences for the three typefaces, the art provenance statement (the intake records each image as "AI-generated in Codex from the recorded prompt; not hand-drawn"), the manuscript release and the print notes.
- No ornament beyond one lozenge.

### 6.4 Contents (specimen 2)

As in section 5. The contents takes two pages, facing if possible.

### 6.5 Chapter opener (specimen 3; 11 chapters and 3 appendices)

- **Order on the page:**
  1. Chapter art at full frame width from the top of the frame, rising 0.3 in into the top margin. It is a 3:2 wide scene and takes about 45% of the page.
  2. "CHAPTER ONE" in tracked sans caps.
  3. The title in 44 pt display.
  4. A flourish.
  5. The source's italic lead, centred, 13 pt display italic at 80% width.
  6. The first numbered section, starting on the same page in two columns.
- **No running head.** The thumb tab starts here.
- **Art rule:** the chapter's approved scene, ART-CHxx, with each chapter's own subject. Until a chapter's art is approved, the opener drops 1.2 in and the type carries the page (the art-light edition). The page never uses another chapter's art.

### 6.6 Ordinary rules page (specimen 4)

- Section title full width; prose in two columns.
- Run-in bold labels for definition paragraphs ("Grid Mode:").
- Subsections in serif bold with quiet numbers.
- Lists use a lozenge bullet.
- Examples and notes sit in the column at the point they explain.
- A numbered section starts a fresh page, as DESIGN_REFINEMENT requires.

### 6.7 Worked example and rules note (specimens 4 and 5)

- **Example:**
  - a 5.5% tinted field with a 2.4 pt black left rule and the tag "EXAMPLE";
  - an optional title after a middle dot;
  - 9.8 pt text.
  - Where an example walks through a figure, its steps are numbered to match the figure labels (TNA lesson: 1.1, 1.2...).
- **Rules note:** an open box between a 1 pt rule and a 0.45 pt rule, with a centred tag ("RULES NOTE", "CLARIFICATION" or "DESIGN NOTE") between mascles. It is used only where the manuscript sets a note apart. The book never invents notes.

### 6.8 Rules with a figure (specimen 5)

- The figure is full width or column width, by its native size.
- A black caption bar is welded beneath it with the figure number and title in reversed caps (TES lesson). The caption sits directly under the bar and is closed by a hairline.
- The figure, bar and caption form one unbreakable unit, and the unit stays with the rule it illustrates.
- FIG-20, the shared key, appears once at the start of 10.4, and every map caption ends "key: FIG-20" as now.

### 6.9 Procedure (specimen 5)

- Numbered steps hang 16 pt display numerals at the left of the column.
- A label-rule titles the procedure.
- Steps are set exactly as the source lists them. The specimen uses invented step text only to show the component, and says so on the page.

### 6.10 Tables (specimen 6)

There is one grammar for all 332 tables:

- black header bar with reversed 7.6 pt caps;
- hairline rows;
- a closing 1.3 pt rule;
- repeated headers on continuation.

| Family | Treatment |
|---|---|
| Roll / lookup (1d6, d66 ...) | Narrow centred die column tinted 9%; result name bold; wide effect column. No banding (the tinted column guides the eye) |
| Equipment / numeric | Name left; numbers right-aligned in tabular figures; traits last; light 5.5% banding for long tables. Long text in a row moves to a spanning second line (Five Leagues lesson) |
| Prose-heavy (5+ columns of sentences) | Full width; or the existing `cards` transformation where width cannot be found |
| Reference summaries (Appendix C) | 8.8 pt, banded, full width under a black reference head |

A table title, when the source gives one, is set in 12.5 pt display above the bar.

Short tables are mandatory keeps. Long tables continue with the repeated header bar and "(continued)" in the title line.

### 6.11 Gazetteer: places of the world (specimen 11)

- Used for the Bastions and Climates in 1.3, and the strongholds in 11.3 where the source is lore prose.
- Wide 3:2 art at full frame width.
- The place name in 22 pt display with a tracked sans kicker ("BASTION", "CLIMATE").
- A double rule.
- The lore in Source Serif 4 Italic, as the source sets it, at 10.5 pt in a 78% measure.
- Two places per page where both fit. A place never splits.

### 6.12 Hero class, ancestry and background (specimen 7)

- **Head, full width:** a kicker (HERO CLASS, ANCESTRY or BACKGROUND), the name in 30 pt display and a role tag ("1/5 Complexity"), then a double rule.
- **Beside the head:** the italic flavour, then a fact table of the source's labelled fields in source order.
- **Outer column:** a 2:3 portrait, 2.15 in wide.
- **Below:** the talent tiers in two columns, with label-rules and display minor heads.
- **Pagination:**
  - classes (12): each class starts a fresh page;
  - ancestries (11) and backgrounds (20): each is a keep unit and packs two per page.

### 6.13 Equipment entries (7.11 to 7.17)

- Item entries use the power-entry grammar (6.14) without the numeral.
- Tables follow 6.10.
- Still-life art (ART-ITE-*) sits at the foot of a table page in leftover space, never displacing a keep unit.

### 6.14 Powers (specimen 8; five traditions)

- **Tier head:** display title with a rule running to the margin.
- **Each power:**
  - a display numeral and name;
  - the source's cost in a black cost tag;
  - one italic sans field line (Range · Target · ...), from the Mythras lesson;
  - the effect paragraph.
- Each power is a keep unit, set in two columns.
- **Tradition identity:** the tradition's name in the running head and its art (ART-TRA-*) on its first page. No icon taxonomy is added.

### 6.15 Bestiary (specimen 9; 120 monsters and 15 bosses)

- **One monster per column; every bestiary page shows two complete creatures.**
- **Each entry:**
  - a fixed 2.55 in portrait box, so the names align across the page;
  - the name in 17 pt display with a role tag ([Elite], [Brute]...);
  - the italic flavour;
  - the black stat bar (HP · AV · SPD · LVL · CV · Sz) with values in 11.5 pt sans;
  - the source's AI Steps, Attacks and Special Abilities under label-rules, in source order.
- **Long entries:** an entry that cannot fit a column takes the full width of a page, with the portrait in the outer column.
- **Climate groups:** each climate group (Greenmark, Ashlands...) opens with its group heading and the group's random table where the source places it.
- **Bosses:** use the same entry at full width, with a larger portrait.
- **Missing art:** the portrait box collapses, and the entry still owns its column.
- **Effect:** this replaces today's half-empty bestiary pages with full ones.

### 6.16 Scenario (specimen 10; 36 core scenarios and the two tutorial scenarios)

Every named scenario starts a fresh page.

- **Head, full width:**
  - "SCENARIO PALE CITY 2" in tracked caps;
  - the 28 pt display title;
  - the flavour in display italic at 82% measure;
  - optional scenario art (ART-SCE-*) at the right of the head;
  - a double rule.
- **Left column:** the setup dossier, a 5.5% tinted panel under a 1.5 pt rule. It holds the source's labelled setup fields in source order with their exact labels (Primary Objective, Final Random Monster Groups, Awake Groups, Minion Swarm, Objective Scaling, Pressure Clock, Party Deployment ...). The remaining setup prose follows below it.
- **Right column:**
  - the deployment map with its caption bar;
  - the scenario-specific monster, shown as a formula stat card (black label column) because its values are formulas;
  - its AI Steps and abilities as in the bestiary.
- **Special Rules and Victory Conditions** follow in two columns. Victory Conditions and Tiebreaker close in the ruled outcome frame.
- **No invented labels.** The book adds no phase labels the source lacks; Black Death City's "Before / During / After" is a lesson in grouping, not in labels.
- **Pagination:** a scenario that fits one page is one page. A longer one continues with "Scenario Pale City 2, continued" in the running head and never splits its setup from its map.

### 6.17 Campaign play (Chapter 11)

- The campaign cycle uses FIG-17 as a full-width figure, with the cycle steps as a procedure.
- The stronghold buildings in 11.3 use power-style keep entries.
- The Bastions use the gazetteer (6.11).
- Campaign records are not invented. If the manuscript defines a record or roster sheet, it is set as a heavy-box form (Hametsu character-sheet lesson) on its own page.

### 6.18 Learn to Play and Basic Mode (Appendices A and B)

- Same templates, one notch friendlier:
  - procedures for setup;
  - examples for the guided opening;
  - the scenario template for "The Broken Courier" and "The Courier's Strongbox".
- The two-round sample opening (A.11) uses examples numbered to match FIG-18.
- Basic Mode profiles use the stat bar.

### 6.19 Rules reference (Appendix C; specimen 12)

- Each C.x opens under a black reference head: the code in sans and the title in display reversed.
- Tables are full width at 8.8 pt and banded.
- C.13 (the single-sheet summary) is designed as one self-contained page that can be printed alone.
- C.11 (the glossary) uses index-style hanging entries in two columns.

### 6.20 Index (specimen 13)

As in section 5. The index is generated from the existing tagged terms (`ixm`).

## 7. Art integration

| Page type | Art | Size and placement |
|---|---|---|
| Title, back cover | ART-COVER, one creature vignette | Full frame width / 34% width |
| Chapter opener | ART-CHxx (wide) | Full frame width, top, about 45% of the page |
| Gazetteer | ART-BAS-*, ART-CLI-*, ART-WOR-* (wide) | Full frame width above the name |
| Hero entries | ART-CLA-*, ART-ANC-*, ART-BAC-* | 2:3 portrait 2.15 in in the outer column; backgrounds 1:1 at 1.6 in |
| Bestiary | ART-MON-* (square) | Fixed 2.55 in portrait box at the top of the column |
| Scenario | ART-SCE-* | 1.7 in at the right of the scenario head |
| Powers, items, campaign | ART-TRA-*, ART-ITE-*, ART-CAM-* | First page of the section, or the foot of a table page in leftover space |

These rules apply to every placement:

- The art carries its own white vignette, so there are no frames, rules or boxes around art.
- Text never runs over art.
- No art is wrapped around irregular contours in rules pages; that is a lesson from Deth Wizards' uneven lines.
- Art never displaces or splits a keep unit. It moves instead.
- Art is placed from `assets/art/ink/` (the intake's ink-prepared files) only after approval.
- When art is missing, the slot collapses cleanly (the art-light edition).

## 8. Pagination and composition

DESIGN_REFINEMENT's policy stands. This plan adds these rules:

1. Bestiary entries are column keep units, so two complete creatures sit on every page.
2. Scenario setup and its map share the opening spread column pair.
3. Character entries: classes start fresh pages; ancestries and backgrounds pack two per page.
4. Gazetteer places pack two per page.
5. A wide table or figure is placed full width at a column boundary. It never interrupts a column mid-sentence.
6. Leftover space at the end of a section can take a relevant spot illustration from the same section. It is never filled with unrelated prose or art.

## 9. Print production

- **Ink coverage:** solid black is limited to small structural marks. Large black slabs are used only in the art.
- **Hairlines:** none is thinner than 0.3 pt; the 28% grey hairlines hold on inkjet.
- **Tints:** transparent black works on cream and white alike; check banding on the physical proof.
- **Thumb tabs:** they bleed 0.42 in. At the 1.03 overscan test, the number stays fully visible; a tab trimmed by borderless overscan still reads.
- **Specimens:** `tools/render_template_specimens.py --substrate white` renders the white companion for comparison.
- Physical printing remains NOT TESTED until real sheets are examined.

## 10. Adoption into the book build (on the owner's build request)

The generator (`tools/build_book.py`) already emits semantic component calls (`chapter-opener`, `htable`, `statstrip`, `statcard`, `cards`, `example`, `note-box`, `figure-block`, `spotart`, `flavour`). Adoption is mostly a reskin of those components, plus a few new wrappers that group entries the generator already recognizes.

1. **Tokens and furniture:**
   - Add IM FELL to the font set (done: `fonts/static/IMFe*.ttf`, `fonts/licences/OFL-imfell.txt`).
   - Port the geometry, running heads, folios and thumb tabs into `heraldry.typ`.
   - Record the v2 tokens in `config/design_tokens.json`.
2. **Reskin existing components** with the v2 versions from `system.typ`. Signatures are kept, and the pagination machinery (`pm`, `bal`, `keeppage`, `munit`, `tmark`) is untouched:
   - `chapter-opener`;
   - section headings (level 2);
   - `htable` (black header grammar, roll and spanning-row options);
   - `statstrip` (stat bar);
   - `statcard`;
   - `example`;
   - `note-box`;
   - `figure-block` (caption bar).
3. **New wrappers in the generator.** The source structures are already detected for keeps; the wrappers change presentation only:
   - `monster` entry grouping and portrait lookup by ART ID;
   - `character-entry`;
   - `power` entry parsing of "Name **[cost]**" lines;
   - `gazetteer`;
   - scenario dossier grouping of the labelled setup fields;
   - the contents and index renderers.
4. **Gates** (all existing):
   - reconciliation (every word and cell);
   - the mandatory one-page-unit audit;
   - layout QA;
   - visual review of every page type at readable size, and the cream/white pair;
   - specimen pages are re-rendered at each step.
5. **Release:** `make clean all verify package` and the visual ledger, as BUILD.md describes.

## 11. Decisions recorded and open questions

- **Recorded (Claude Code, 2026-10-12, within the owner's request for a design plan):**
  - display face IM FELL replaces Cinzel;
  - ragged-right body;
  - black-bar table headers;
  - one monster per column;
  - thumb tabs;
  - caption bars.
- **Open for the owner:**
  1. Thumb tabs bleed and use ink. They can be removed without other changes if you prefer a cleaner edge.
  2. The 1.2 in typographic drop for chapters whose art is not yet approved. The alternative is to hold the layout until all chapter art exists.
  3. Whether C.13 should also be produced as a separate one-page play aid.
