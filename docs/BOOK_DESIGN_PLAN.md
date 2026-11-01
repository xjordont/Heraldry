# Book design plan: "Grim Heraldry" (compact design system v5)

Status: compact v5 implements the owner's 2026-10-16 approval of the layout review, explicitly allowing **10.5 pt body**, **9 pt tables**, narrower margins, and more assertive refinement. The owner resumed this implementation on 2026-10-20. This supersedes the earlier 11 pt lock and conservative trial values. `config/design_tokens.json` is the single effective geometry/type/spacing authority; Typst imports it and Python uses `tools/layout_profile.py`. `config/production.json` mirrors public format values and is checked for agreement.

The original v4 reference study and component rationale below remain useful where the v5 profile does not supersede them. Ordinary rules use two columns. Chapter/section opening flavour has an explicit, inset single-column region; wide tables and diagrams retain deliberate spanning roles. Fit-capable complete source units, source order, readable figures, the accepted blank verso, and independent visual review remain mandatory. Physical proof is **NOT TESTED**. Local specimens and measured builds are evidence of their stated scope, not a new release approval.

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
| Margins | inside 45 pt (0.625 in), outside 42 pt (0.5833 in), top/bottom 45 pt (0.625 in); final binding requires physical proof |
| Text frame | 525 × 702 pt; two 254.4 pt columns with a 16.2 pt (0.225 in) gutter |
| Edge safety | essential content and navigation lettering at least 27 pt (0.375 in) from trim; decoration may reach the edge |
| Full-width regions | section titles, chapter openers, wide tables, wide figures, scenario heads |
| Column regions | prose, examples, notes, monster entries, powers, dossiers |

The decorative pennant occupies the outer margin. Its 9 pt keyword sits on the inner face, with actual rotated glyph bounds checked against the 27 pt safe line and the body frame. Initial 36 pt outer and 40.5 pt top margins failed this check; 42 pt outer and 45 pt top margins preserve clearance.

## 3. Type

Four families are used, all under the OFL, with licences in `fonts/licences/`. Each has one job.

| Role | Face | Size / leading | Notes |
|---|---|---|---|
| Rules text | Source Serif 4 | 10.5 pt with 2.9 pt additive leading, about 13.925 pt baseline pitch | Hyphenation discouraged but allowed (en-CA) |
| Flavour, leads, lore | IM FELL English (roman) | 10.5 pt, near-black (84%), 3.3 pt additive leading | Owner 2026-10-12: easier to read than the italic, and plainly a different voice from the rules |
| Chapter title | Grenze Gotisch SemiBold | 50 pt | Centred under the opener art and the chapter's arms |
| Section (x.y) | Grenze Gotisch SemiBold | 21 pt | Number in an engraved black shield; brush rule beneath |
| Subsection (x.y.z) | Source Serif 4 Bold | 13 pt | Lozenge, then a quiet number in Source Sans 3 Bold 9.5 pt, 42% grey (13 pt since the 2026-11-01 audit, so the rank order holds) |
| Minor named heading | Grenze Gotisch SemiBold | 13 pt | One step below the subsection (2026-11-01 audit; was 14.5 pt and read larger than its parent) |
| Entry names | Grenze Gotisch SemiBold | 15.5 to 36 pt | Power 15.5, monster 21, place 28, scenario 32, class 36 |
| Tab keywords | Grenze Gotisch Bold | 9 pt | Reversed, centred, rotated to run along the edge |
| Publication labels and tags | Source Sans 3 Bold | At least 9 pt | Table headers, captions, and essential navigation use the shared size floor; smaller legacy specimen labels are not publication settings |
| Tables | Source Sans 3 | 9 pt with 2.4 pt additive leading, about 11.85 pt baseline pitch | Tabular lining figures |
| Captions | Source Sans 3 | 9 pt | Number and title in the black caption band |
| Running head | Source Sans 3 SemiBold | 9 pt, +0.12 em | |
| Folio | Source Sans 3 Bold | 9 pt | Reversed in an engraved shield |

The essential rules, table, caption, and navigation size floor is 9 pt. Do not shrink individual pages to force fit. Legacy demonstration-only labels are not a licence to reduce the publication components below that floor.

**One treatment for flavour (owner 2026-10-12, revised the same day):** all flavour text is IM FELL roman at the running body size (10.5 pt; see below), justified and hyphenated, with 6 pt of space between paragraphs (no first-line indents). Justification uses Typst `justification-limits` (word space 90–140%, letter spacing −0.5% to +2% of the em) so even the 3.5 in monster columns set without rivers. Section-level flavour (chapter leads, the flavour under a section title, place lore, scenario flavour) is the `lead-block` component: a centred measure 82% of the frame wide, with the text justified inside it. Entry flavour inside a column (monsters, classes, backgrounds) is the `flavour` component: the same face, size, colour and spacing at full column width. Justified was chosen over centred after a side-by-side on the Deepwarden page: centred multi-paragraph lore leaves ragged edges on both sides; justified reads as one quiet block. The specimen renderer can still show the centred variant with `tools/render_template_specimens.py --lead center` for comparison.

**One body size: 10.5 pt (owner approval, 2026-10-16):** running rules, flavour, examples, notes, monster/class entries, and power effects retain their semantic roles at the common body size. Source Serif uses 2.9 pt additive leading, 4.5 pt paragraph spacing, and 2.8 pt list-item spacing. IM FELL retains slightly more open flavour leading. Nominal size and additive leading are distinct from actual baseline pitch; specimens verify the serialized geometry. Table text is 9 pt with 4 pt horizontal and 2.2 pt vertical inset. Example panels use 8 pt horizontal and 6 pt vertical inset. These are shared settings, never content-dependent shrinking.

**Banner tags on titles:** every banner tag that labels a title (monster role, BASTION, HERO CLASS, scenario number) is set by the `entry-title` component: the tag sits on its own line directly above the title, 5 pt above the cap height, always at the title's top-left corner, whether the title is set left or centred (owner 2026-10-12: "The black tags should consistently be aligned to the top left of the text they reference; not centred above it"). The tag never shares a line with the title and never floats against its baseline.

**Blackletter for character, not for reading:** Grenze Gotisch carries titles, names and tab keywords only. It is never set in all capitals, and never used for running text, table cells or numbers.

## 4. Ink, tone and ornament

- **Ink:** black only.
  - Flavour text is 84% black.
  - Labels are 58%; hairlines are 24%.
  - Tints are transparent black: 5% for banding, examples and panels; 9% for the die column.
- **Ornament** is the armoury of section 12: chapter arms, the castle logo, brush rules, engraved shields, corner flourishes, banner tags and the coin. It is medieval heraldry rather than horror props. The skulls of v3 are retired (owner 2026-10-12: "a bit cheesy").
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
- **Index:** three columns. Each initial is reversed in an engraved black block followed by a rule. Entries are sans 9.5 pt (`type_pt.index`) with hanging indents and grey page numbers.
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
  3. The chapter's arms, then the title in 50 pt blackletter, inside the ornate opener frame (corner flourishes, the castle logo at the head).
  4. A flourish.
  5. The source's lead, centred, 12.4 pt IM FELL roman at 82% width.
  6. The first numbered section, starting on the same page in two columns.
- **No running head.** The thumb tab starts here.
- **Art rule:** the chapter's approved scene, ART-CHxx, with each chapter's own subject. Until a chapter's art is approved, the opener drops 1.2 in and the type carries the page (the art-light edition). The page never uses another chapter's art.

### 6.6 Ordinary rules page (specimen 4)

- Section title full width (the shield, the 21 pt title, and the brush span the frame; the two columns start together beneath it, 2026-11-01); prose in two columns.
- Run-in bold labels for definition paragraphs ("Grid Mode:").
- Subsections in serif bold with quiet numbers.
- Lists use a lozenge bullet.
- Examples and notes sit in the column at the point they explain.
- A numbered section starts a fresh page, as DESIGN_REFINEMENT requires.

### 6.7 Worked example and rules note (specimens 4 and 5)

- **Example:**
  - a 5.5% tinted field with a 2.4 pt black left rule and the tag "EXAMPLE";
  - an optional title after a middle dot;
  - 10.5 pt text, from the shared body token.
  - Where an example walks through a figure, its steps are numbered to match the figure labels (TNA lesson: 1.1, 1.2...).
- **Rules note:** the example panel (tinted field, black spine, tag at the top left, 10.5 pt text) with its own tag: "RULES NOTE", "CLARIFICATION" or "DESIGN NOTE" (owner 2026-10-12: "change the ugly in line 'rules note' format to be the same as example format but with a different tag"). It is used only where the manuscript sets a note apart. The book never invents notes.

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

1. **Title:** retain the source heading at its semantic rank. The repeated identity uses 9 pt sans bold. Suppress its duplicate opening text when the immediately preceding source heading already supplies that title, and retain its fixed continuation geometry.
2. **Edges:** retain the hand-inked brush below the last row. The top brush is omitted because it crossed the identity text. There is no outer box around an ordinary lookup table.
3. **Header band:** solid black, reversed 9 pt bold caps. Each label is aligned like its column: centred over centred values, left over left. The band repeats on every continuation page.
4. **Column alignment** is set per column type:
   - **key**: bold, left;
   - **text**: left;
   - **value**: centred (numbers, dice, damage, short codes);
   - **roll**: centred bold on a 9% tinted column.
5. **Rows:** 2.2 pt vertical padding, 9 pt sans, alternate rows banded at 5%, hairlines at 24% between rows. A long text in a row may move to a spanning second line.
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
- **2026-10-29:** 100 approved Monster portraits (and 24 other pieces) had silently dropped out after a pronoun normalisation changed their catalogue specs; they were reviewed, re-bound, and restored. `tools/check_art.py` now fails on an approval bound to an outdated spec, and the composer refuses a stale flavour-block anchor.
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
- **Pagination:** a scenario that fits one page is one page. Later pages repeat its source title with "(continued)" in the running head until the next scenario, climate, or higher-rank section. Long running titles shorten at a word boundary with an ellipsis; essential navigation remains 9 pt. Preserve fit-capable setup/map units.

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

- Each C.x opens under an iron reference band: the code in a paper shield and the title in reversed blackletter. Adopted 2026-11-01: the sections run on rather than each starting a fresh page; a section that opens with a short introduction sets the band and the introduction as one unbreakable, sticky composition (the introduction as a standfirst at the opener's measure) and runs on when the next piece is prose or a unit no taller than half a frame; otherwise it starts a fresh page.
- Reference tables use the approved 9 pt size and measured column/full-width placement, with light banding.
- C.13 retains its source title, "Single-Sheet Rules Summary". The complete current source exceeds one page at the approved size; its title is not permission to omit content or shrink essential text.
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

**Adoption record, 2026-11-01 (design audit, owner approval "Approve everything"):** section heads span the frame; subsection 13 pt and minor 13 pt; the reference band heads Appendix C; bracketed roles and kickers are banner tags; the source's horizontal rules are quiet separators; the first numbered section may share the opener page; Appendix C runs on; tailpieces grow to their gap and sit at the foot; the thumb tab wears a paper halo; the opener label reads "Chapter One"; the version line is serif small caps. Still not adopted (remaining work): the power and item entry grammar (6.13, 6.14), the scenario setup dossier and outcome frame (6.16), the numbered procedure shields (6.9), the gazetteer head (6.11), and the character-entry head (6.12); the book sets those structures as run-in labels and headings. The rationale and evidence are in `reports/Design audit and production plan.md` and `docs/DESIGN_REFINEMENT.md`.

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
  - ragged-right body (superseded the same day: the owner asked whether all body text should be justified, and a side-by-side on the 2.6 and Fighter pages showed justified-within-limits sets evenly and saves lines; body is now justified, and the owner then locked it at 11 pt);
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
| **Chapter arms** | Owner-approved 2026-10-13 ("Approved. Make sure they are big enough to see."), chosen over five Nano Banana 2.1 rounds (`production/art/marks/APPROVED.json`). Flat black ink on a plain field, with bold interior detail and no grey. Each charge is set by `tools/prepare_marks.py` inside one shared double-rimmed heater shield (the Mechanics candidate's rim) and traced to vector SVG in cream and white variants. World/Lore: raven on a crown broken in two. Mechanics: die. Round: hourglass. Actions: three arrows points down. Combat: bearded axe and notched sword. Party: tattered banner. Equipment: great helm. Powers: open hand with an eye. Monsters: horned wyvern's head. Scenarios: ruined arch. Campaign: war pavilion. Learn: key. Basic: lantern. Reference: open book. Index: quill and ink pot | Chapter opener (52 pt, about 0.72 in), contents rows (22 pt), running head (15 pt), armoury sheet (52 pt). Never below 15 pt |
| **Logo / signature mark** | Owner-approved 2026-10-13: a broken heater shield bearing a three-towered castle, cracked through its portcullis gate, with fragments falling away; "the arms of a fallen realm". It replaces the six earlier signature candidates, which are retired | Opener-frame head (30 pt), flourish centre (22 pt), title page, back cover, armoury sheet (92 pt) |
| **Brush rule** | A hand-inked stroke with tapered ends and a slightly uneven edge, drawn the same way every printing | Section titles, table edges, stat bars, entry names, folios |
| **Engraved shield** | A heater shield with a paper inner line, carrying a number | Section numbers, folios, procedure steps, power numbers |
| **Corner flourish** | A fine L with an inner hairline and lozenge finials | Scenario dossiers and outcome frames; chapter-opener frame |
| **Banner tag** | A black strap with a pointed end | EXAMPLE, RULES NOTE, monster roles, scenario number, place kicker |
| **Coin** | Owner-approved 2026-10-13 ("Yes to v2 but take the notch out of the border"): a hammered medieval long-cross penny in heavy black ink, with a bold rim, a beaded border, a solid cross and four pellets in each quarter. It is heavy enough to match bold figures at text size. Generated with Nano Banana 2.1, the notch closed by an image edit, and traced by `tools/prepare_marks.py`. `coin-reversed.svg` (ink in paper colour) serves black header bands. It sits on the baseline beside its figures | Stands for the source's "c" in tables and stat bars |
| **Opener frame** | Thick-and-thin border, corner flourishes, the castle logo at the head, the folio shield at the foot | Chapter openers only |
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
1. Justified within limits: word space 90–140% and letter spacing −0.5% to +2% of the em (Typst `justification-limits`), shared by rules text and flavour, so no line opens rivers. Table cells, captions, stat blocks, sidebars of data and headings stay unjustified. Hyphenation is allowed in the 3.48 in columns but allowed at normal cost (100%; raised from 140% so justified lines in narrow list items stay even); no hyphen in headings, names or table cells. Every list item (a talent, a starting package, a numbered step) is kept whole: it never splits across a column or a page.
2. No widows or orphans: a paragraph never leaves one line alone at the top or foot of a column (widow and orphan costs at the maximum).
3. No runts: a paragraph's last line carries at least two words where possible (runt cost 160%).
4. A paragraph that fits a column never splits across a page turn. When a paragraph must split, it splits within a spread (verso to recto), never recto to verso, wherever the layout engine can achieve that by moving a whole unit.

12a. **Balanced columns.** Wherever a two-column run ends on a page (a section close, lore, a chapter opener's first section), the two columns are balanced to equal depth (`balanced` in `system.typ`), so no column stands half empty beside a full one. Lore and gazetteer text fills the full frame in two balanced columns, never a narrow single measure with a blank margin (owner 2026-10-12: the Deepwarden introduction).

**Units (what reads as one thing stays on one page)**
5. Every heading keeps its first full paragraph, or its first two list items, on the same page and column (sticky headings).
6. Examples, rules notes, procedures, stat profiles, monster, power, class and place entries, short tables and figures with captions are unbreakable keep units.
7. A fit-capable section or subsection moves whole to the next column or page rather than splitting (DESIGN_REFINEMENT). Only over-height units continue, with repeated headers or "(continued)".

**Avoiding page bloat**
8. Every numbered section starts on a fresh page (owner 2026-10-12: "Keep the page breaks so each section starts on a fresh page"). Space left at the end of a short section is never given to the next section; it is handled by rule 9. To keep this from bloating the book, a section is composed to finish cleanly: its two columns are balanced (12a), and its own figures and tables are placed so its last page is as full as the keep rules allow.
9. Space left at a section end is filled in this order (owner 2026-10-30: "fill in the white space with either art, diagrams, further figures"):
   - a source-faithful rules figure for that section (FIG-58 to FIG-77 close twenty short sections of Chapters 1 to 7), sized to the space the section leaves;
   - the section's own spot art, if approved, or its approved tailpiece (`production/art/END_ART_PLAN.json`), set by `endart` below the text only where the next heading already starts a later page, scaled to fit and omitted below 1.6 in tall;
   - a Basic Mode Hero's approved portrait closes their B.4 profile the same way;
   - a relevant example or table from that section, if the source places it there;
   - otherwise intentional white space.

   Never stretch spacing or enlarge type to fill a page.
10. Column balance: two-column runs balance on their last page, but a keep unit is never broken to balance.
11. The compact profile provides a 525 pt by 702 pt usable frame and 254.4 pt columns. Report actual page savings from same-source builds; frame area alone does not predict pagination. Tables use full width whenever their columns would otherwise wrap a header or a short value.

**Measure and rhythm**
12. Use the shared spacing tokens consistently. Actual line pitch includes the font's vertical metrics; additive leading alone does not establish a baseline grid. Inspect facing-column rhythm in rendered pages rather than claiming alignment from a nominal spacing unit.
13. Long prose cells (over about 25 words) in tables move to a spanning second line or a `cards` transformation instead of shrinking type.
14. Type never shrinks below the section 3 minimums to make something fit. Content is never omitted.

**Verification** (each build): the existing reconciliation, the one-page-unit audit and layout QA, plus a widow, orphan and split-paragraph report by stable block ID. Every exception must be reviewed.
