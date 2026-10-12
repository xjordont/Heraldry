# Book design plan: "Grim Heraldry" (design system v4)

Status: owner-requested design pass (2026-10-12), rebuilt as v3 at the owner's direction: "add much more character and rebuild the whole graphic design moving in a more ornate grim dark direction while focusing on clarity and ease of use. Ensure the tables are not only beautiful but also very easy to read." The templates are implemented as Typst components in `typst/templates/system.typ` and shown on fourteen specimen pages in `typst/templates/specimens.typ`. These are set with real RC492 text, approved art and the real vector figures, and rendered to PNG by `tools/render_template_specimens.py`. No book PDF was produced.

The current book build (`typst/heraldry.typ`) is unchanged until the owner asks for a build. Then it adopts this system as described in section 10.

The evidence is in `docs/design/REFERENCE_STUDY.md`: all ten reference books were mapped page by page, and about 90 pages were inspected closely.

This plan supersedes the visual identity sections of `DESIGN_SPEC.md` (display face, heading styles, furniture, component styling). The pagination contract in `DESIGN_REFINEMENT.md` stays in force without change. That contract covers fresh-page starts, mandatory one-page keeps and continuation rules.

## 1. The idea

The book should read as a rulebook printed from woodcut-era type and drawn in iron-gall ink, but laid out with modern information design. Every page should be easy to read.

- **Mood** comes from three sources:
  - the display face, Grenze Gotisch, a readable modern blackletter, with IM FELL italic for flavour;
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
| Margins | inside (binding) 0.75 in, outside 0.55 in, top 0.68 in, bottom 0.7 in (owner 2026-10-12: narrower) |
| Text frame | 7.2 × 9.62 in; two columns of 3.48 in with a 0.24 in gutter (about 6% more text per page than v3) |
| Edge safety | essential content at least 0.375 in from every edge (thumb tabs are navigation, not essential) |
| Full-width regions | section titles, chapter openers, wide tables, wide figures, scenario heads |
| Column regions | prose, examples, notes, monster entries, powers, dossiers |

The outer margin carries the 0.32 in thumb tabs with 0.23 in clear space before the text.

## 3. Type

Four families are used, all under the OFL, with licences in `fonts/licences/`. Each has one job.

| Role | Face | Size / leading | Notes |
|---|---|---|---|
| Rules text | Source Serif 4 | 10.25 / 13.3 pt, ragged right | Hyphenation discouraged but allowed (en-CA) |
| Flavour, leads, lore | IM FELL English (roman) | 10.2 to 12.4 pt, near-black (84%), leading about 14.5 pt | Owner 2026-10-12: easier to read than the italic, and plainly a different voice from the rules |
| Chapter title | Grenze Gotisch SemiBold | 50 pt | Centred under the opener art and the chapter's arms |
| Section (x.y) | Grenze Gotisch SemiBold | 24 pt | Number in an engraved black shield; brush rule beneath |
| Subsection (x.y.z) | Source Serif 4 Bold | 12.5 pt | Lozenge, then a quiet number in Source Sans 3 Bold 9.5 pt, 42% grey |
| Minor named heading, table titles | Grenze Gotisch SemiBold | 14 to 15.5 pt | |
| Entry names | Grenze Gotisch SemiBold | 15.5 to 36 pt | Power 15.5, monster 21, place 28, scenario 32, class 36 |
| Tab keywords | Grenze Gotisch Bold | up to 12 pt, auto-fitted | Reversed, centred, rotated to run along the edge |
| Labels and tags | Source Sans 3 Bold | 6.6 to 7.8 pt caps, +0.09 to 0.16 em tracking | Entry anatomy, dossier fields, banner tags, table headers |
| Tables | Source Sans 3 | 9.3 pt (8.8 pt in Appendix C) / about 12 pt | Tabular lining figures |
| Captions | Source Sans 3 | 8.6 pt | Number and title in the black caption band |
| Running head | Source Sans 3 SemiBold | 7.4 pt caps, +0.16 em | |
| Folio | Source Sans 3 Bold | 7.6 pt | Reversed in an engraved shield |

The minimum essential size is 8.6 pt for captions and 8.8 pt for dense reference tables. The DESIGN_SPEC floor of 9 pt for running text still applies to body copy.

**Blackletter for character, not for reading:** Grenze Gotisch carries titles, names and tab keywords only. It is never set in all capitals, and never used for running text, table cells or numbers.

## 4. Ink, tone and ornament

- **Ink:** black only.
  - Flavour text is 84% black.
  - Labels are 58%; hairlines are 24%.
  - Tints are transparent black: 5% for banding, examples and panels; 9% for the die column.
- **Ornament** is the armoury of section 12: chapter arms, the broken crown, brush rules, engraved shields, corner flourishes, banner tags and the coin. It is medieval heraldry rather than horror props. The skulls of v3 are retired (owner 2026-10-12: "a bit cheesy").
- **Ornament lives only at boundaries:**
  - running heads and folios;
  - titles;
  - table edges;
  - panel corners;
  - tabs;
  - chapter-opener frames.

  Nothing ornamental sits inside the reading field, a table cell or behind art.
- **Rules are calm:** one brush stroke under a section title; a thick-and-thin pair under the running head; brush strokes only at the top and bottom of a table. The v3 thorn rules are retired (owner 2026-10-12: "some of the rule lines are crowded").
- **Not used:**
  - parchment texture, stains or burned edges;
  - drop shadows or gradients;
  - icons that would need a legend;
  - colour.

## 5. Navigation

- **Running heads:**
  - The verso carries the chapter name; the recto carries the current section.
  - Each sits at the outer end beside the chapter's arms, over a thick-and-thin rule.
  - Heads are suppressed on chapter openers, scenario openers, the title page and contents.
- **Folios:** the page number reversed in an engraved shield at the outer bottom corner, with a short brush stroke toward the gutter. On framed opener pages the shield sits in the frame's bottom centre.
- **Thumb tabs (owner 2026-10-12):**
  - Tall black pennants hang from the outer edge, 0.32 in wide, each with an engraved inner line and bevelled inner corners.
  - Each carries its part's keyword in bold blackletter, reversed and centred. The keyword is auto-fitted up to 12 pt and rotated to run along the edge: top to bottom on the right edge, bottom to top on the left.
  - There are 15 fixed slots, so the closed book shows a stepped index:

  | Slot | Part | Keyword |
  |---|---|---|
  | 1 | The World of Heraldry | World |
  | 2 | Core Mechanics | Mechanics |
  | 3 | The Game Round | Round |
  | 4 | Actions and Movement | Actions |
  | 5 | Combat | Combat |
  | 6 | Your Adventuring Party | Party |
  | 7 | Equipment and Items | Equipment |
  | 8 | Powers and Traditions | Powers |
  | 9 | Monsters | Monsters |
  | 10 | Scenarios | Scenarios |
  | 11 | Campaign Play | Campaign |
  | 12 | Appendix A. Learn to Play | Learn |
  | 13 | Appendix B. Basic Mode | Basic |
  | 14 | Appendix C. Rules Reference | Reference |
  | 15 | Index | Index |

  Tabs are navigation only. The running head always names the chapter, so a tab trimmed by overscan loses nothing.
- **Contents:** two columns. Each chapter row has the chapter's arms, its number, the title in blackletter and its page, over a rule. Each section line has a sans number, a serif title and dot leaders to the page. The contents is two levels deep; deeper levels live in the PDF bookmarks.
- **Index:** three columns. Each initial is reversed in an engraved black block followed by a rule. Entries are sans 8.6 pt with hanging indents and grey page numbers.
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
- "Heraldry" in 72 pt blackletter, with "Skirmish" in 30 pt blackletter beneath.
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
  1. Chapter art at full frame width from the top of the frame, within the opener frame. It is a 3:2 wide scene and takes about 45% of the page.
  2. "CHAPTER ONE" in tracked sans caps.
  3. The chapter's arms, then the title in 50 pt blackletter, inside the ornate opener frame (corner flourishes, the broken crown at the head).
  4. A flourish.
  5. The source's lead, centred, 12.4 pt IM FELL roman at 82% width.
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
- **Rules note:** a panel held by four corner irons, with a centred banner tag ("RULES NOTE", "CLARIFICATION" or "DESIGN NOTE"). It is used only where the manuscript sets a note apart. The book never invents notes.

### 6.8 Rules with a figure (specimen 5)

- The figure is full width or column width, by its native size.
- A black caption bar is welded beneath it with the figure number and title in reversed caps (TES lesson). The caption sits directly under the bar and is closed by a hairline.
- The figure, bar and caption form one unbreakable unit, and the unit stays with the rule it illustrates.
- FIG-20, the shared key, appears once at the start of 10.4, and every map caption ends "key: FIG-20" as now.

### 6.9 Procedure (specimen 5)

- Numbered steps hang black shields carrying the step number at the left of the column.
- A label-rule titles the procedure.
- Steps are set exactly as the source lists them. The specimen uses invented step text only to show the component, and says so on the page.

### 6.10 Tables: the ledger (specimen 6)

Owner 2026-10-12: "The tables look amateur. We should be centring values in cells ... changing (c) to a symbol for a coin." There is one grammar for all 332 tables, built on the Deth Wizards (page 22) and Black Death City (page 66) lessons: centred values, calm rules and no boxes.

1. **Title**, when the source gives one: blackletter 15.5 pt directly above the table. They never separate.
2. **Edges:** a hand-inked brush stroke above the header and another below the last row. There are no vertical rules and no side frame.
3. **Header band:** solid black, reversed 7.6 pt bold caps. Each label is aligned like its column: centred over centred values, left over left. The band repeats on every continuation page.
4. **Column alignment** is set per column type:
   - **key**: bold, left;
   - **text**: left;
   - **value**: centred (numbers, dice, damage, short codes);
   - **roll**: centred bold on a 9% tinted column.
5. **Rows:** 4.2 pt vertical padding, 9.3 pt sans, alternate rows banded at 5%, hairlines at 24% between rows. A long text in a row may move to a spanning second line.
6. **The coin:** the source's "c" for coins is set as the coin mark.
   - In a header, "Cost (c)" becomes "COST" followed by a paper coin.
   - In a value, "36c" becomes "36" followed by the coin.
   - The mapping is purely typographic and recorded for reconciliation: coin mark = "c".

| Family | Treatment |
|---|---|
| Roll / lookup (1d6, d66 ...) | Roll column, bold key, wide effect column |
| Equipment / numeric | Bold key, centred values, traits left and last |
| Prose-heavy (5+ columns of sentences) | Full width, or the existing `cards` transformation where width cannot be found |
| Reference summaries (Appendix C) | 8.8 pt, full width under the black reference head |

Short tables are mandatory keeps. Long tables continue with the repeated header band and "(continued)" in the title line.

### 6.11 Gazetteer: places of the world (specimen 11)

- Used for the Bastions and Climates in 1.3, and the strongholds in 11.3 where the source is lore prose.
- Wide 3:2 art at full frame width.
- The place name in 28 pt blackletter with a banner tag kicker ("BASTION", "CLIMATE").
- A brush rule.
- The lore in Source Serif 4 Italic, as the source sets it, at 10.5 pt in a 78% measure.
- Two places per page where both fit. A place never splits.

### 6.12 Hero class, ancestry and background (specimen 7)

- **Head, full width:** a kicker (HERO CLASS, ANCESTRY or BACKGROUND), the name in 36 pt blackletter and a banner tag ("1/5 Complexity"), then a brush rule.
- **Beside the head:** the italic flavour, then a fact table of the source's labelled fields in source order.
- **Outer column:** a 2:3 portrait, 2.15 in wide.
- **Below:** the talent tiers in two columns, with label-rules and blackletter minor heads.
- **Pagination:**
  - classes (12): each class starts a fresh page;
  - ancestries (11) and backgrounds (20): each is a keep unit and packs two per page.

### 6.13 Equipment entries (7.11 to 7.17)

- Item entries use the power-entry grammar (6.14) without the numeral.
- Tables follow 6.10.
- Still-life art (ART-ITE-*) sits at the foot of a table page in leftover space, never displacing a keep unit.

### 6.14 Powers (specimen 8; five traditions)

- **Tier head:** the title in blackletter, reversed in an iron band.
- **Each power:**
  - a shield numeral and the name in blackletter;
  - the source's cost in a black cost tag;
  - one italic sans field line (Range · Target · ...), from the Mythras lesson;
  - the effect paragraph.
- Each power is a keep unit, set in two columns.
- **Tradition identity:** the tradition's name in the running head and its art (ART-TRA-*) on its first page. No icon taxonomy is added.

### 6.15 Bestiary (specimen 9; 120 monsters and 15 bosses)

- **One monster per column; every bestiary page shows two complete creatures.**
- **Each entry:**
  - a fixed 2.55 in portrait box, so the names align across the page;
  - the name in 21 pt blackletter with a banner role tag ([Elite], [Brute]...);
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
  - the 32 pt blackletter title, under a banner tag carrying the scenario number;
  - the flavour in display italic at 82% measure;
  - optional scenario art (ART-SCE-*) at the right of the head;
  - a brush rule.
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

- Each C.x opens under an iron reference band: the code in a paper shield and the title in reversed blackletter.
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
- **Thumb tabs:** they bleed 0.5 in. At the 1.03 overscan test, the number stays fully visible; a tab trimmed by borderless overscan still reads.
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

## 11. Decisions recorded

- **Claude Code, 2026-10-12, within the owner's request for a design plan:**
  - display faces: Grenze Gotisch (titles and names) and IM FELL italic (flavour) replace Cinzel;
  - ragged-right body;
  - black-bar table headers;
  - one monster per column;
  - caption bars.
- **Owner, 2026-10-12:**
  1. Keep the thumb tabs, "or something more artful that serves the same purpose"; then (later the same day) "the pennants should have the name of the chapter in a word for easy reference ... written 90 degrees to run along the page edge; use a keyword for the chapter for long chapter names": section 5.
  2. Chapters whose art is not yet approved use the typographic opener (a 1.2 in drop, type alone), so layout never waits for art.
  3. C.13, the single-sheet rules summary, is also produced as a separate one-page play aid. It is built from the same source and template as the C.13 page, as its own file, whenever the book is built; no PDF is produced before a build is requested.
  4. "Add some more flavour than the plain layout ... better graphic design to the tables and elsewhere", then "add much more character and rebuild the whole graphic design moving in a more ornate grim dark direction while focusing on clarity and ease of uses. Ensure the tables are not only beautiful but also very easy to read": sections 3, 4, 6.10 and 12 (design system v3).
  5. v4 (later 2026-10-12): bolder, centred blackletter tab keywords; ledger tables with centred values and the coin mark for "c"; skulls replaced by chapter arms and the broken crown; calmer rules; narrower margins; IM FELL roman for flavour; the typesetting policy of section 13.

## 12. The armoury: grim medieval heraldry (v4)

The owner directed on 2026-10-12: "take it further ... more decorations, symbols, ornaments but keep it tasteful without distracting from the text or art ... the skulls are a bit cheesy ... design something better grim dark medieval heraldry that's not so on the nose ... some of the rule lines are crowded." Every mark is an original vector drawn in `typst/templates/system.typ` and shown on specimen 15, "The Armoury".

| Mark | Form | Where |
|---|---|---|
| **Chapter arms** | Each of the 15 parts bears its own coat of arms: a classic heraldic ordinary in black on paper. World per pale, Mechanics fess, Round bend, Actions chevron, Combat saltire, Party cross, Equipment pale, Powers pile, Monsters per saltire, Scenarios chief, Campaign bordure, Learn quarterly, Basic per bend, Reference per fess, Index a lozenge | Chapter opener (26 pt), running head (8.5 pt), contents rows (15 pt) |
| **Broken crown** | Five points, the fourth snapped to a jagged stump: a dead dynasty, "kings are buried" | Signature mark: opener-frame head, flourishes, title page, back cover |
| **Brush rule** | A hand-inked stroke with tapered ends and a slightly uneven edge, drawn the same way every printing | Section titles, table edges, stat bars, entry names, folios |
| **Engraved shield** | A heater shield with a paper inner line, carrying a number | Section numbers, folios, procedure steps, power numbers |
| **Corner flourish** | A fine L with an inner hairline and lozenge finials | Rules notes, scenario dossiers and outcome frames; chapter-opener frame |
| **Banner tag** | A black strap with a pointed end | EXAMPLE, RULES NOTE, monster roles, scenario number, place kicker |
| **Coin** | A struck disc with a ring and a lozenge stamp | Stands for the source's "c" in tables and stat bars |
| **Opener frame** | Thick-and-thin border, corner flourishes, the broken crown at the head, the folio shield at the foot | Chapter openers only |
| **Drop capital** | Blackletter initial reversed in an engraved black block | First paragraph after a chapter opener (vendored droplet 0.3.1, MIT) |

**Restraint rules:**
1. Nothing ornamental inside text, table cells or art.
2. At most one ornamental mark per heading or table edge.
3. Rules are one brush stroke or one thick-and-thin pair, never stacked.
4. Every reversed label is at least 6.6 pt bold, on solid black.
5. Black areas stay small and structural.

## 13. Typesetting and layout policy

Owner 2026-10-12: "We should be very careful of how we set up policy and procedure for typesetting and text layout to be easy to read, avoid page bloat, and avoid having to read sections/paragraphs across pages." These rules bind the build, alongside the mandatory one-page keep contract in DESIGN_REFINEMENT.md.

**Paragraphs**
1. Ragged right, so word spacing never stretches. Hyphenation is allowed in the 3.48 in columns but discouraged (cost 140%); no hyphen in headings, names or table cells.
2. No widows or orphans: a paragraph never leaves one line alone at the top or foot of a column (widow and orphan costs at the maximum).
3. No runts: a paragraph's last line carries at least two words where possible (runt cost 160%).
4. A paragraph that fits a column never splits across a page turn. When a paragraph must split, it splits within a spread (verso to recto), never recto to verso, wherever the layout engine can achieve that by moving a whole unit.

**Units (what reads as one thing stays on one page)**
5. Every heading keeps its first full paragraph, or its first two list items, on the same page and column (sticky headings).
6. Examples, rules notes, procedures, stat profiles, monster, power, class and place entries, short tables and figures with captions are unbreakable keep units.
7. A fit-capable section or subsection moves whole to the next column or page rather than splitting (DESIGN_REFINEMENT). Only over-height units continue, with repeated headers or "(continued)".

**Avoiding page bloat**
8. Numbered sections start on a fresh page only where the policy requires it (DESIGN_REFINEMENT). A short section that ends early leaves its remaining space to the next same-chapter keep unit that fits it whole, before any page break is forced. This is never unrelated content and never a split unit.
9. Space left at a section end is filled in this order:
   - the section's own spot art, if approved;
   - a relevant example or table from that section, if the source places it there;
   - otherwise intentional white space.

   Never stretch spacing or enlarge type to fill a page.
10. Column balance: two-column runs balance on their last page, but a keep unit is never broken to balance.
11. The narrower v4 margins give about 6% more text per page. Tables use full width whenever their columns would otherwise wrap a header or a short value.

**Measure and rhythm**
12. All vertical spacing is a multiple of the 3.3 pt half-line, so text in facing columns lines up.
13. Long prose cells (over about 25 words) in tables move to a spanning second line or a `cards` transformation instead of shrinking type.
14. Type never shrinks below the section 3 minimums to make something fit. Content is never omitted.

**Verification** (each build): the existing reconciliation, the one-page-unit audit and layout QA, plus a widow, orphan and split-paragraph report by stable block ID. Every exception must be reviewed.
