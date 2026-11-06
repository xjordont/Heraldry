# Book design: "Grim Heraldry" (compact design system v5)

This is the book's one current design document. It replaces `DESIGN_SPEC.md`, `BOOK_DESIGN_PLAN.md`, and `DESIGN_REFINEMENT.md` (merged 2026-11-03 with the owner's approval). Sections 1 to 13 keep their `BOOK_DESIGN_PLAN.md` numbers, which Typst comments cite. The dated record (owner wording, superseded values, adoption and specimen steps, and old inspection logs) is in `docs/history/DESIGN_HISTORY.md`, which also maps old citations here.

**Authority.** `config/design_tokens.json` is the single effective authority for geometry, type, spacing, ink, rules, ornament, tailpieces, and composition settings; Typst reads it, and Python reads it through `tools/layout_profile.py`; no other file repeats its values. Where this document disagrees with the tokens or the Typst source, they are right. The manuscript governs mechanics and terminology; `docs/PROJECT_CONTRACT.md` governs source fidelity, format, tables, figures, and verification; `docs/ART_DIRECTION.md` governs illustration; `docs/VISUAL_QA.md` is the review rubric. The one-page keep rule is stated once, in `docs/PROJECT_CONTRACT.md` ("Pagination: the one-page keep rule"); 8.4 adds how the composer applies it.

**Status.** The v5 profile implements the owner's approvals of 2026-10-16 (10.5 pt body, 9 pt tables, narrower margins) and 2026-11-01 (the design audit). The book is digital only (2026-11-02). Section 10 says which templates the book sets.

## 1. The idea

The book is an original dark medieval fantasy reference book. It should read as a rulebook printed from woodcut-era type and drawn in iron-gall ink, laid out with modern information design, on a light, quiet reading field. Every page should be easy to read.

- **Mood** comes from the display face (Grenze Gotisch, a readable modern blackletter) with IM FELL English for flavour, from the ink art, and from small solid-black accents: number shields, header bands, and thumb tabs.
- **Legibility** comes from a quiet, very readable serif for all rules, a clear sans for every number and label, and generous, consistent spacing.
- **Nothing decorates the reading field.** Text is never set on a texture. There is no paper grain, no perimeter frame on ordinary pages, and no colour that carries meaning. Ornament is one small original family (section 12), used at boundaries only.
- **Darkness comes from the subjects**, the ink silhouettes, and restrained heraldry; the page stays light. Atmosphere follows specific manuscript subjects and convincing ink drawing.

The ordinary rules page is the product: the covers and openers set the mood, but the book succeeds or fails on its working pages. Avoid a generic shield badge on every entry, random flourishes, skulls, imitation occult lettering, dashboard cards, drop shadows, gradients, and busy symmetrical frames. Body ink stays strong; ornament stays subordinate.

The design draws on the owner's ten reference books (lessons in `docs/history/REFERENCE_STUDY.md` and `docs/history/design-decisions.md`, cited here by book and page). They are visual inspiration only: never clone a page, take or trace their art, logos, borders, emblems, or icons, import their mechanics, or cite them as an authority in the editorial patch ledger. Record a newly adopted lesson (book and page, principle, implementation, and the page that shows it) in the section of this document it changes, and note it in `production/STATE.md`.

## 2. Page and grid

| Element | Value |
|---|---|
| Page | US Letter portrait, 612 × 792 pt (8.5 × 11 in); single pages with facing-page furniture; cream `#FCFAF5` to every edge |
| Margins | inside 45 pt (0.625 in), outside 42 pt (0.5833 in), top and bottom 45 pt (0.625 in) |
| Text frame | 525 × 702 pt; two 254.4 pt columns with a 16.2 pt (0.225 in) gap |
| Edge safety | essential content and navigation lettering at least 27 pt (0.375 in) from every page edge; decoration may reach the edge |
| Full-width regions | section heads, chapter openers, opening flavour, wide tables, wide figures, scenario heads |
| Column regions | prose, examples, notes, monster entries, powers, dossiers |

- Portrait pages only: no landscape fallback and no imposed spreads.
- The page colour is an opaque page background, independent of the margins; a background that reaches the edge does not remove the text margins. Never put a white rectangle behind a paragraph or table.
- Ordinary rules and reference entries use two columns. Opening chapter and section flavour uses an inset single-column region (the lead block, section 3); substantive scenario and procedure prose follows the two-column grammar. A wide table or diagram may take one continuous full-width region; avoid repeated full-width islands between tiny two-column fragments (8.5).
- Measured furniture safety takes priority over the smallest margin: the thumb-tab keyword's rotated glyph outlines are checked against the 27 pt safe line and the body frame, and the 42 pt outside and 45 pt top and bottom margins preserve that clearance.
- Chapter titles may take more space; running navigation stays quiet. There is no navigation rail or sidebar column in the text frame; the thumb tabs live in the outer margin.

## 3. Type

Four families, all under the OFL, with licences in `fonts/licences/`; each has one job. Bundle the approved files and licences, and check embedding and glyph coverage.

| Role | Face | Size and spacing | Notes |
|---|---|---|---|
| Rules text | Source Serif 4 | 10.5 pt; 2.9 pt additive leading (about 13.925 pt pitch); 4.5 pt between paragraphs, 2.8 pt between list items | Justified within limits (13, rule 1); hyphenation allowed (en-CA) |
| Flavour, leads, lore | IM FELL English roman | 10.5 pt, 84% black; 3.3 pt additive leading; 6 pt between paragraphs | Easier to read than the italic, and plainly a different voice (2026-10-12) |
| Chapter title | Grenze Gotisch SemiBold | 50 pt | Centred under the opener art and the chapter's arms |
| Section (x.y) | Grenze Gotisch SemiBold | 21 pt | Number reversed in an engraved shield; brush rule beneath |
| Subsection (x.y.z) | Source Serif 4 Bold | 13 pt | Lozenge, then a quiet number in Source Sans 3 Bold 9.5 pt at the furniture grey |
| Minor named heading | Grenze Gotisch SemiBold | 13 pt | One step below the subsection (2026-11-01) |
| Reference band title | Grenze Gotisch SemiBold | 19 pt | Reversed (6.19) |
| Entry names | Grenze Gotisch SemiBold | 15.5 to 36 pt | Power 15.5, monster 21, place 30, scenario 32, class 36 (entry-head templates) |
| Tab keywords | Grenze Gotisch Bold | 9 pt | Reversed, centred, rotated along the edge |
| Labels, tags, captions | Source Sans 3 Bold (captions regular) | 9 pt | Labels and tags in small capitals on the source's letters |
| Tables | Source Sans 3 | 9 pt; 2.4 pt additive leading (about 11.85 pt pitch) | Tabular lining figures |
| Stat-bar values | Source Sans 3 SemiBold | 12 pt | |
| Running head; folio | Source Sans 3 SemiBold; Bold | 9 pt | Head tracked +0.12 em in small capitals; folio reversed in a shield |

**Size floor.** Essential rules, table, caption, label, and navigation text is never below 9 pt (`type_pt.minimum_essential`), and pages are never shrunk to force a fit. The smaller labels on the specimen sheets (6.6 to 8.4 pt) are legacy demonstration settings, not publication settings.

**One body size (owner, 2026-10-16).** Rules, flavour, examples, notes, entries, and power effects keep their semantic roles at the one body size, with shared insets, never content-dependent shrinking. Nominal size and additive leading are not the actual baseline pitch, which includes the font's vertical metrics; specimens verify the serialised geometry.

**One treatment for flavour (owner, 2026-10-12).** All flavour is IM FELL roman at the body size, justified and hyphenated within the limits of 13, rule 1, with no first-line indents. A bold run inside it is set in Source Serif 4 Bold Italic, because IM FELL has no bold. Section-level flavour (chapter leads, the flavour under a section title, place lore, and scenario flavour) is the `lead-block`: centred, 82% of the frame wide, justified inside. Entry flavour in a column (monsters, classes, and backgrounds) is the `flavour` component: the same setting at full column width.

**Banner tags.** In the book (2026-11-01), a bracketed role or kicker closing a heading ("[Elite]", "[2/5 Complexity]", "[Intro]") is set as a banner tag at the end of the heading, with the brackets kept as transparent glyphs and the role in small capitals. In the `entry-title` component of the entry-head templates, the tag stands on its own line directly above the title, 5 pt above the cap height, at the title's top-left corner whether the title is set left or centred, never centred above it (owner, 2026-10-12).

**Blackletter for character, not for reading.** Grenze Gotisch carries chapter, section, and minor headings, titles, names, and tab keywords only. It is never set in all capitals, and never used for running text, table cells, or numbers. Subsections stay in the serif.

**Typography lock.** Preserve semantic bold and the manuscript's own characters: straight quotes and apostrophes (smart quotes are off in every Typst document), numeric-range en dashes, ×, and −. The player aids and Hero records use the manuscript's hyphen-minus for negatives and empty cells. Capitals on source text are small capitals, never `upper()`, so the text layer keeps the source's letters.

## 4. Ink, tone, and ornament

- **Ink** is black only. Rules text is 100%; flavour and running heads 84% (`ink.secondary_text_gray`); quiet numbers and labels 58% (`ink.furniture_gray`, rendered as 42% luma). Hairlines are transparent black at 24%. Tints are transparent black over the cream: 5% for banding, examples, and panels, and 9% for the die column of roll tables.
- **Ornament** is the armoury of section 12: medieval heraldry rather than horror props. The skulls of v3 are retired (2026-10-12).
- **Ornament lives only at boundaries:** running heads and folios, titles, table edges, panel corners, tabs, chapter-opener frames, and the quiet separator. Nothing ornamental sits inside the reading field, a table cell, or behind art. An ordinary page carries at most two marks (`ornament.maximum_marks_per_ordinary_page`). Use the same line vocabulary throughout. Skip an ornament where it weakens alignment or reading flow; marks have no rules meaning.
- **Rules are calm:** one brush stroke under a section title; a thick-and-thin pair (1.1 pt and 0.35 pt) under the running head; a brush under the last row of a table. The source's horizontal rules are the quiet separator: a short 0.6 pt hairline pair, 40% of the measure, around a 4 pt lozenge, with 10 pt above and below. The castle flourish is reserved for chapter and front-matter boundaries. The v3 thorn rules are retired (2026-10-12).
- **Not used:** parchment texture, stains, burned edges, grain, repeated texture, or watermarks; a distressed body font or a dark ordinary-page background; drop shadows or gradients; icons that would need a legend; colour; a box or card around every paragraph.

## 5. Navigation

- **Running heads:** the verso carries the chapter name; the recto carries the current section or, on a scenario's later pages, its source title with "(continued)", shortened at a word boundary with an ellipsis so it fits at 9 pt. Each sits at the outer end beside the chapter's arms (15 pt), over the thick-and-thin rule. Heads are suppressed on chapter openers, the index opener, and the front matter (title page, colophon, How to Use, and contents).
- **Folios:** the page number reversed in an engraved shield (23 pt wide) at the outer bottom corner, with a short brush stroke toward the gutter. On framed opener pages the shield sits in the frame's bottom centre. The title page and covers carry none.
- **Thumb tabs (owner 2026-10-12):** tall black pennants on the outer edge of every main-matter page, running from the page edge to 3 pt short of the text frame (so 39 pt wide), with an engraved inner line, bevelled inner corners, and a 3 pt paper halo so the opener frame never runs into them. The part's keyword is Grenze Gotisch Bold 9 pt, reversed, centred, and rotated to run along the edge: top to bottom on the right edge, bottom to top on the left. Its glyph ink sits between the 27 pt safe line and the tab's inner line, measured by glyph outlines (Grenze Gotisch's ascender metric is far taller than its letters). Fifteen fixed slots run from 0.4 in below the top edge to just above the folio, so the page edges show a stepped index. Tabs are navigation only; the running head always names the chapter.

  | Slot | Part | Keyword | Slot | Part | Keyword |
  |---|---|---|---|---|---|
  | 1 | The World of Heraldry | World | 9 | Monsters | Monsters |
  | 2 | Core Mechanics | Mechanics | 10 | Scenarios | Scenarios |
  | 3 | The Game Round | Round | 11 | Campaign Play | Campaign |
  | 4 | Actions and Movement | Actions | 12 | Appendix A. Learn to Play | Learn |
  | 5 | Combat | Combat | 13 | Appendix B. Basic Mode | Basic |
  | 6 | Your Adventuring Party | Party | 14 | Appendix C. Rules Reference | Reference |
  | 7 | Equipment and Items | Equipment | 15 | Index | Index |
  | 8 | Powers and Traditions | Powers | | | |

- **Contents:** two columns under a blackletter title and flourish. Each chapter row has the chapter's arms (20 pt), the title in 14 pt blackletter, and its page in sans bold, over a rule. Each section line has its number and title in Source Serif 4 9.5 pt and dot leaders to its page. Two levels deep; deeper levels live in the PDF bookmarks.
- **Index:** three columns. Each letter head is a 13 pt blackletter initial reversed in a black block, followed by a rule. Entries are Source Sans 3 9.5 pt, the term in semibold, with hanging indents. The last page is balanced into three whole-entry columns of near-equal height; a column never starts with a sub-entry or ends with a letter head.
- **Digital:** linked contents and index, PDF bookmarks, and clickable cross-references ("see 10.6.4"), built from the existing anchors, with reliable page references once pagination settles. Alphabetical entry pages have clear group headings and hanging indents.

## 6. Page-type catalogue

Each template gives its components, its pagination rule (in addition to section 8), its art rule, and its specimen page in `typst/templates/specimens.typ` (PNG only, never a book PDF: `python3 tools/render_template_specimens.py --sheet`). The specimens use RC492 excerpts and some components the book has not adopted; section 10 says what the book sets today.

**Entry anatomy, for every kind of entry.** Use recurring templates, not a unique box for every named ability. An entry runs: a stable title, the source's metadata or stat strip, the description, then the abilities or procedure. Fields stay in source order, except for a documented, mechanically neutral layout mapping. Never invent metadata, abilities, resources, or labels. Separate neighbouring entries with spacing and a fine rule, not a box. Short entries stay together; long entries continue with a repeated identifying name.

### 6.1 Cover, front and back (`typst/cover.typ`)

- **Front:** the owner-supplied cover picture with its own lettering (2026-10-14), fitted inside the 0.375 in safe edge. Without it, the classic cover: the opener frame, a live serif title, a flourish, the cover art at no more than native 300 ppi, the subtitle in IM FELL, and the version in serif small capitals. Cover lettering is live type, never drawn by an image model.
- **Back:** the opener frame; the edition blurb (`editorial/back_cover.json`) in IM FELL, in a 5.2 in measure chosen so it ends on a full line; the approved ART-COVER-002 party scene, with no crest flourish under the frame's own crest; three verbatim game facts from 1.1, ragged left in a 4.8 in measure under a short brush; and at the foot the Escutcheon Press device (1.15 in) over the version line in serif small capitals.
- Both covers are pages of the digital PDF and carry no running head, folio, page-background frame, or thumb tab (2026-11-02). Specimen 13 shows an earlier back cover.

### 6.2 Title page (specimen 1 shows an earlier design)

The castle logo at the head; the title in tracked Source Serif 4 Bold capitals (34 pt) over its second line; a flourish; the manuscript's subtitle in IM FELL; the author's byline in tracked serif capitals. At the foot, the Escutcheon Press device (0.95 in) over the version line in serif small capitals (`type_pt.imprint`). No running furniture and no folio.

### 6.3 Colophon (verso of the title) and How to Use

Source Sans 3 9 pt in one column, set low, headed by the Escutcheon Press device (1.3 in). The text (`editorial/how_to_use.json`) gives the title, version, author and publisher, copyright, edition statement, the four typefaces and their licence, and the page format. No ISBN, no illustration credit (owner, 2026-10-29), and no ornament beyond the device. How to Use follows in two columns. Both name the current manuscript automatically.

### 6.4 Contents (specimen 2)

As in section 5, on two pages, facing if possible. The main matter then starts on a recto, after the accepted blank verso.

### 6.5 Chapter opener (specimen 3; 11 chapters and 3 appendices)

1. The chapter's approved 3:2 scene, centred at the top of the frame inside the opener frame, at the chapter family's print width (`config/art_style.json`), never wider than 84% of the frame or its native 300 ppi size. The composition target is at most two fifths of the page (`art.chapter_opening_target_max_area_fraction`).
2. The chapter's arms (52 pt).
3. The label "Chapter One" ("Appendix A" for an appendix) in Source Sans 3 Bold 10 pt small capitals, with the source's "1." kept on the line as transparent glyphs.
4. The title in 50 pt blackletter, inside the ornate opener frame (corner flourishes, the castle logo at the head).
5. A flourish.
6. The source's lead as the lead block (IM FELL 10.5 pt, justified, 82% measure). A short plain introduction (one to three paragraphs, at most 700 characters, before the first section) is one standfirst at the same measure in the body face.
7. The first numbered section, on the same page in two columns when the measured opener and introduction leave more than 35% of the frame free (`layout.opener_share_free_fraction`; the illustrated openers leave 36 to 42%), otherwise on the next page.

- **Composition:** a shared opener is top-aligned, and the section's first column segment flows naturally rather than as a balanced grid. An opener page holding only the opener and its introduction is optically centred, with slightly more space below than above. A chapter whose introduction cannot share its opener page opens as a spread: a centred display page (art, arms, label, and title), then the whole introduction, centred, on the next page (Chapters 8 and 11). Sharing is decided from the measurement pass, never from a position read during layout.
- **No running head.** The opener frame carries the folio, and the thumb tab starts here.
- **Art rule:** the chapter's own approved scene (ART-CHxx), its subject drawn from the chapter's current source lore (`production/art/ART_MANIFEST.json`), asymmetrical with useful negative space; never another chapter's art or a generic figure repeated across chapters. Until a chapter's art is approved, the opener drops 0.9 in and the type carries the page (the art-light opener), so layout never waits for art.

### 6.6 Ordinary rules page (specimen 4)

- The section head spans the frame: shield, 21 pt title, and brush run across the 525 pt frame, and the two columns start together beneath it. The composer emits it as the first part of a page-fit unit, or in the outer flow ahead of its columns and sticky to them, so it never ends a page alone.
- Prose in two columns, with a consistent spacing rhythm and few horizontal rules; keep the source's emphasis rather than making all text heavier. Section, subsection, and run-in treatments read clearly different.
- Run-in bold labels lead definition paragraphs ("Grid Mode:"); a paragraph that is only a bold label acts as a minor heading and keeps with what follows.
- Lists use a lozenge bullet; numbered lists use Source Sans 3 Bold 9 pt numerals.
- Examples and notes sit in the column at the point they explain. Page starts follow 8.1.

### 6.7 Worked example and rules note (specimens 4 and 5)

- **Example:** a panel with a 5% tinted field, a 2.6 pt black left spine, 8 pt by 6 pt inset, and 10.5 pt text. The source's own label ("Example:") leads in bold, so no word is added. It attaches to the rule or procedure it explains. Where an example walks through a figure, its steps are numbered to match the figure labels (TNA lesson: 1.1, 1.2, and so on). No dark sidebar and no permanent narrow third column (Hametsu lesson).
- **Rules note:** the same panel, used only where the manuscript sets a note apart. The book never invents notes.
- **Specimen design, not adopted:** a banner tag at the panel's top left: "EXAMPLE" with an optional title after a middle dot, or "RULES NOTE", "CLARIFICATION", or "DESIGN NOTE" (owner, 2026-10-12).

### 6.8 Rules with a figure (specimen 5)

- The figure is full width or column width, by its native size. A black caption band is welded beneath it, carrying the printed figure number reversed in Source Sans 3 Bold 9 pt (TES lesson); the 9 pt caption sits directly under the band, closed by a 0.6 pt rule. The specimen band also carries the title in reversed capitals; the book's carries the number only.
- Figure, band, and caption form one unbreakable unit that stays with the rule it illustrates.
- Figures print in book order (FIG-01 is the first a reader meets). Registry ids (files, manifests, and reviews) do not change; caption references follow the printed numbers.
- The shared key (registry FIG-20) appears once at the start of 10.4, and every map caption cites it. When it is taller than the space left, it floats to the next page top (`layout.float_figures`).
- **Rules graphics** are editable vectors drawn with code or vector tools, never an image model: a clean field, consistent base symbols, patterned terrain, solid and dashed lines, numbered callouts, readable legends, and typeset labels legible at the placed size. Allegiance and geometry are distinguished redundantly, never by colour or tone alone. Use metric-perfect dimensions only when the source supports them and the drawing is to scale; otherwise label it schematic. Where rules differ, explain Tabletop first and Grid second. Draw AI and phase diagrams only from source-supported branches, one decision topic per figure, with compact multi-panel spatial diagrams for local edge cases and no single giant flowchart. Verify every caption and worked arithmetic against the manuscript.

### 6.9 Procedure (specimen 5)

Numbered steps hang black shields carrying the step number at the left of the column, under a label-rule title. Steps are set exactly as the source lists them; the specimen's invented step text only shows the component, and says so.

### 6.10 Tables: the ledger (specimen 6)

One grammar (owner, 2026-10-12) serves all 332 tables, built on the Deth Wizards (page 22) and Black Death City (page 66) lessons: centred values, calm rules, and no boxes. Every table has the black header band; the body stays light.

1. **Title:** the source heading keeps its semantic rank. The repeated identity line is 9 pt sans bold. Its duplicate opening text is suppressed when the preceding heading already names the table, including across a short run-in label such as "APL 1–2 (d10)", leaving no blank line, and its fixed continuation geometry is kept. The same holds for a table set as entries (`cards`).
2. **Edges:** a hand-inked 2.2 pt brush below the last row, taking no height so it can never fall alone onto the next page. No top brush (it crossed the identity text), no outer box, and no vertical rule unless a matrix needs one.
3. **Header band:** solid black, reversed 9 pt bold small capitals, each label aligned like its column, repeated on every continuation page.
4. **Columns:** key bold and left; text left; values (numbers, dice, damage, short codes) centred; roll centred bold on the 9% tinted column.
5. **Rows:** 9 pt sans, 4 pt by 2.2 pt padding, alternate rows banded at 5%, 0.35 pt hairlines at 24% between rows. Labels and rules must still work without the banding. Ordinary rows never split, and an over-height row is handled explicitly; a long text may move to a spanning second line. No hyphenation in cells, and a numeric range never breaks after its en dash.
6. **The coin:** the source's "c" is set as the coin mark: "Cost (c)" becomes "COST" and a paper coin, on one line; "36c" becomes "36" and the coin. The mapping is purely typographic and recorded for reconciliation (coin mark = "c"); the source letters stay under the coin as transparent glyphs.
7. **Widths:** family-specific widths and alignment, strong header separation, and a generous descriptive column. Widths are measured from the actual cells and go where they remove the most wrapped lines; reviewed scope decisions (`layout.table_scope_policies`) keep their proportional rule. Use full width whenever columns would otherwise wrap a header or a short value; full-width tables take priority over narrow prose columns. Never make long skinny columns to keep a spreadsheet silhouette.
8. **Overflow,** in this order: adjust width and padding; place full width; continue at natural row groups; transform faithfully into entries (`cards`); then keyed portrait continuation panels. Preserve every cell, and repeat unique row keys when column groups continue.
9. **Changed representation:** a table set in another form needs a machine-readable source-cell-to-output-field mapping. Preserve notes, ranges, row keys, and source relationships.

| Family | Treatment |
|---|---|
| Roll or lookup (1d6, d66, and so on) | Narrow centred roll column, bold key, wide left-aligned effect; no decorative full grid |
| Equipment and numeric | Bold key, centred values, traits left and last |
| Prose-heavy (5 or more columns of sentences) | Full width, or the `cards` transformation where width cannot be found |
| Scenario and scaling | Exact canonical field labels, readable groups, full width where needed |
| Reference summaries (Appendix C) | 9 pt, full width under the reference band; compact hierarchy and explicit continuations |

Short tables are mandatory keeps. Long tables continue with the repeated header band and "(continued)" in the identity line, by the row groups of 8.2.

### 6.11 Gazetteer: places of the world (specimen 10b)

For the Bastions and Climates in 1.3, and the strongholds in 11.3 where the source is lore prose: wide 3:2 art above; the place name in 30 pt blackletter with a banner tag kicker ("BASTION", "CLIMATE"); a brush rule; the lore as flavour (IM FELL roman 10.5 pt) in a lead block, or, when too long for one, in two balanced full-frame columns (13, rule 12a). Two places per page where both fit; a place never splits.

### 6.12 Hero class, ancestry, and background (specimen 7)

- **Head, full width:** a kicker (HERO CLASS, ANCESTRY, or BACKGROUND), the name in 36 pt blackletter, a banner tag ("1/5 Complexity"), and a brush rule. Beside it, the flavour, then a fact table of the source's labelled fields in source order. In the outer column, a 2:3 portrait 2.15 in wide (backgrounds 1:1 at 1.6 in). Below, the talent tiers in two columns, with label-rules and blackletter minor heads.
- **Pagination:** each of the 12 classes starts a fresh page; ancestries (11) and backgrounds (20) are keep units that pack two per page.

### 6.13 Equipment entries (7.11 to 7.17)

Item entries use the power-entry grammar (6.14) without the numeral. Tables follow 6.10. Still-life art (ART-ITE-*) sits at the foot of a table page in leftover space, never displacing a keep unit.

### 6.14 Powers (specimen 8; five traditions)

- **Tier head:** the title in blackletter, reversed in an iron band with lozenge terminals.
- **Each power:** a shield numeral and the name in blackletter; the source's cost in a black cost tag; one italic sans field line (Range · Target · ...), from the Mythras lesson; the effect. Each power is a keep unit, set in two columns.
- **Tradition identity:** the tradition's name in the running head and its art (ART-TRA-*) on its first page. The five traditions are told apart by their canonical text labels; no icon taxonomy is added.

### 6.15 Bestiary (specimen 9; 120 monsters and 15 bosses)

- **One monster per column; every bestiary page shows two complete creatures.**
- **Each entry:** the approved portrait (ART-MON-*); the name with its role as a banner tag ([Elite], [Brute], and so on); the flavour; the black stat bar (HP · AV · SPD · LVL · CV · Sz) with 12 pt values and a brush close; the source's AI Steps, Attacks, and Special Abilities in source order, with no invented abilities or resources.
- **Portrait:** in the book, centred above the entry's flavour at the monster family width (section 7). The specimen sets it in a fixed 2.5 in box at the top of the column so names align across the page.
- An entry too long for a column takes the full width of a page, with the portrait in the outer column. Bosses use the same entry at full width with a larger portrait. Each climate group (Greenmark, Ashlands, and so on) opens with its heading and its random table where the source places it. With no art, the portrait collapses and the entry still owns its column.

### 6.16 Scenario (specimen 10; 36 core scenarios and the two tutorial scenarios)

Every named scenario starts a fresh page, with a clear title and its source flavour.

- **Head, full width:** "SCENARIO PALE CITY 2" in tracked capitals; the 32 pt blackletter title under a banner tag carrying the scenario number; the flavour as a lead block; optional scenario art (ART-SCE-*); a brush rule.
- **Left column:** the setup dossier, a 5% tinted panel with corner flourishes, holding the source's labelled setup fields in source order with their exact labels (Primary Objective, Final Random Monster Groups, Awake Groups, Minion Swarm, Objective Scaling, Pressure Clock, Party Deployment, and so on), followed by the remaining setup prose.
- **Right column:** the deployment map with its caption band, beside or directly after its setup; the scenario-specific monster as a formula stat card (black label column), because its values are formulas; its AI Steps and abilities as in the bestiary.
- **Then** Special Rules and Victory Conditions in two columns under the source's exact headings, followed by scoring and any source-provided aftermath. Victory Conditions and Tiebreaker close in the ruled outcome frame.
- **No invented labels.** The book adds no phase labels the source lacks; Black Death City's "Before / During / After" is a lesson in grouping, not in labels. Repeatable spacing makes setup, timing, special rules, and scoring easy to find.
- **Pagination:** a scenario that fits one page is one page. Later pages repeat its source title with "(continued)" in the running head until the next scenario, climate, or higher-rank section. Fit-capable setup and map units, and other fit-capable child units, stay intact. A multi-page scenario is acceptable; a split opening with detached deployment instructions is not, and rules are never omitted to force one page.

### 6.17 Campaign play (Chapter 11)

The campaign cycle uses FIG-17 as a full-width figure, with the cycle steps as a procedure. The stronghold buildings in 11.3 use power-style keep entries, or light cards where the source structure supports them, fully reconciled. The Bastions use the gazetteer (6.11). Campaign records are not invented: if the manuscript defines a record or roster sheet, it is set as a heavy-box form (Hametsu character-sheet lesson) on its own page.

### 6.18 Learn to Play and Basic Mode (Appendices A and B)

- The same templates, one notch friendlier: procedures for setup, examples for the guided opening, and the scenario template for "The Broken Courier" and "The Courier's Strongbox". The two-round sample opening (A.11) uses examples numbered to match FIG-18.
- Basic Mode profiles use the stat bar. A run-in label merged with its list does not glue the following piece, so profile subsections balance as separate pieces. A long profile keeps its name, identification lines ("Class: ... | Level: 1"), and first subsection together, so it never opens at a column foot with only its name and stats. Each Hero's approved portrait closes their B.4 profile (13, rule 9) at the Hero family width.

### 6.19 Rules reference (Appendix C; specimen 11)

- Each C.x opens under the iron reference band: a black band with the code in a paper shield, the title in reversed 19 pt blackletter, and "RULES REFERENCE" in 9 pt small capitals, closed by a 0.5 pt rule.
- **The sections run on (owner, 2026-11-01)** instead of each starting a fresh page (`layout.run_on_chapters`). A fit-capable section is still one unbreakable page unit and moves whole when it does not fit. An over-height section that opens with a short introduction (at most 800 characters) opens as one unbreakable, sticky full-width composition: the band with the introduction as a standfirst at the opener's measure (`full-opening`). It runs on only when the piece after the introduction is prose or a measured unit no taller than half a frame, which always fits under a fresh-page opening; being sticky, it moves with its columns when they cannot start on the page, so it never strands at a page foot. A taller first unit, or a section opening with a table or list, starts a fresh page, with the same opening when it has an introduction. Ordinary section openings elsewhere are not sticky in this way.
- Reference tables use the approved 9 pt size and measured column or full-width placement, with light banding. C.11 (the glossary) uses index-style hanging entries in two columns.
- C.13 keeps its source title, "Single-Sheet Rules Summary". The complete current source exceeds one page at the approved size; the title is not permission to omit content or shrink essential text. C.13 is also produced as a separate one-page play aid (owner, 2026-10-12), built from the same source and template as its own file whenever the book is built; no PDF is made before a build is requested.

### 6.20 Index (specimen 12)

As in section 5, generated from the tagged terms (`ixm`). Its opener carries the Index arms (40 pt), the title, a flourish, and the index note in IM FELL.

## 7. Art integration

| Page type | Art | Placement in the book |
|---|---|---|
| Covers | Owner's front cover; ART-COVER-002 | 6.1 |
| Chapter opener | ART-CHxx (3:2) | Centred at the top of the frame (6.5) |
| World, Climates, Bastions | ART-WOR-*, ART-CLI-*, ART-BAS-* (3:2) | Centred above the place's flavour |
| Hero entries | ART-CLA-*, ART-ANC-* (2:3), ART-BAC-* (1:1) | Centred above the entry's flavour |
| Bestiary | ART-MON-* (1:1); bosses larger | Centred above the entry's flavour, in its column |
| Scenario | ART-SCE-* | With the scenario head, above its flavour |
| Powers, items, campaign | ART-TRA-*, ART-ITE-*, ART-CAM-* | First page of the section, or the foot of a table page in leftover space |
| Section ends | Approved tailpieces (`production/art/END_ART_PLAN.json`); Basic Mode Hero portraits | Below the section's last text (13, rule 9) |

Each family's print width is in `config/art_style.json`, and no art prints above its native 300 ppi size. The entry-head templates (specimens 7, 9, 10, and 10b) place art differently; adopting them changes this table.

- The art carries its own vignette, transparent or matted to the cream: no frames, rules, or boxes around art, and no white rectangles, bright halos, doubled paper texture, or muddy hatch blocks. Test hatching at the placed size.
- Text never runs over art, and no illustration sits under rules text. Placements are rectangular or open, with clean negative space; no art is wrapped around irregular contours on rules pages (a lesson from Deth Wizards' uneven lines).
- Art attaches to a relevant entry or chapter transition. It never hides or fills a pagination defect, and it never displaces or splits a keep unit: it moves instead.
- Spot art on an ordinary page normally takes at most a quarter of the page, and chapter art at most two fifths (`art` tokens); there are no full-page art interludes by default.
- Only approved art is placed, from `assets/art/ink/` (the intake's ink-prepared files). `tools/check_art.py` fails on an approval bound to an outdated catalogue spec, and the composer refuses a stale flavour-block anchor. Every placed raster is at least 300 ppi at its placed size; `tools/check_art_ppi.py` gates each release PDF (the compact companion is exempt by name).
- Missing art collapses its slot cleanly (the art-light edition), which never claims missing illustrations are complete and never fills a gap with generic silhouettes, clip art, or placeholders. Deployment and rules figures stay precise editable vectors.
- **Tailpieces** grow to the gap they close, up to their 300 ppi maximum and a 4.6 in cap (`art.tailpiece_max_width_in`), and sit at the foot of the frame when more than 60 pt would otherwise be left beneath them; below 1.6 in tall they are omitted. A tailpiece needs a full-width band at the foot of its section's last page; without one it is omitted rather than moving text. Hero portraits keep their family width.

## 8. Pagination and composition

The aim is coherent sections, with breaks before significant new headings. The policy lives in the renderer and style metadata, never in inserted blank lines or manuscript changes. The one-page keep rule is in `docs/PROJECT_CONTRACT.md` ("Pagination: the one-page keep rule"); 8.4 adds how it is applied, and section 13 gives the paragraph rules.

### 8.1 Page starts

| Content | Default |
|---|---|
| Chapter or appendix | Fresh page, with no forced blank verso. The one accepted blank verso is before Chapter 1, so the main matter starts on a recto. |
| Numbered section (manuscript H3, Typst level 2) | Fresh page, except that the first section may share the chapter-opener page (6.5) and Appendix C runs on (6.19), both approved 2026-11-01. A redundant break at a page top is suppressed. |
| Named scenario, including one represented by a bold-only paragraph | Fresh page through a stable semantic scenario target, regardless of Markdown depth |
| Hero class | Fresh page (6.12) |
| Nested subsection or minor heading | No forced page; it keeps its opening content, and a short complete subsection moves whole to the next column or page when it fits there |

Do not force every minor heading onto a fresh page: it would fragment the reference material and inflate the page count.

### 8.2 Keeps and continuations

| Content | Default |
|---|---|
| Heading followed by prose | At least three body lines, or the whole short opening paragraph |
| Heading followed by a list or procedure | Two complete short items, or the first substantive step if steps are long; a step label is never stranded |
| Short table or stat profile | Caption, header, rows, and necessary note together, when the measured unit fits an empty destination column or page |
| Long table | Splits at row or logical group boundaries, repeating its headers and identifying continuation label. The first three and last three rows travel together, carried by an invisible zero-width spanning cell, so a table of five rows or fewer never splits. |
| Table that fits a column but not beside its heading | Starts only where both columns of one page can hold the pair, then continues under its repeated header into the second column |
| Figure | Graphic, legend, and caption together; a deployment figure stays with its own setup, never an unrelated later scenario |
| Over-height unit | Continues by a documented path, with repeated table headers or an identifying continuation and its smaller fit-capable units intact |

Keep definitions, procedures, exceptions, and interpretive table notes together where practical. Body paragraphs keep their natural flow under the widow and orphan rules of section 13.

### 8.3 Page-type composition

1. Bestiary entries are column keep units, so two complete creatures sit on every page.
2. Scenario setup and its map share the opening spread column pair.
3. Character entries: classes start fresh pages; ancestries and backgrounds pack two per page.
4. Gazetteer places pack two per page.
5. A wide table or figure is placed full width at a column boundary. It never interrupts a column mid-sentence.
6. Leftover space at the end of a section can take a relevant spot illustration from the same section. It is never filled with unrelated prose or art.

### 8.4 The one-page keep: how it is applied

The rule, with its measurement and its audit, is stated in `docs/PROJECT_CONTRACT.md` ("Pagination: the one-page keep rule"). The composer and the keep audit apply it with these details:

- Height estimates from character counts may help choose table widths; they never decide pagination.
- Test both facing-page positions.
- For a table, measure the actual Typst content at the selected width, including the header, cell inset, wrapper spacing, caption, and necessary note. Use an unbreakable wrapper only when that complete unit fits an empty frame, and breakable rows or entries only for genuinely over-height content with a faithful, documented representation. Never hide overflow by clipping. Repeated headers count in reconciliation's permitted repetition.
- The audit (`tools/keep_audit.py`, in the mandatory verification gate) records each unit by its stable source ID, with its frame width and height beside the measured height, fit class, and actual pages that the contract requires. Inspect boundary cases and actual pages, not only the metadata.

### 8.5 Composition mechanics

- In two-column material a page break happens in the outer page flow, after the prior segment is flushed; a break inside a nested columns block is not a fresh page.
- The page policy runs before the balancer, whose split candidates respect semantic keep groups. A short subsection is measured as one unit at its destination width, may take an approved full-width placement when a column is too narrow, and never has its heading, lead, table, or first list group split into unrelated balancing pieces.
- **Balanced tails:** a complete column unit that opens with its heading (an ancestry, a Monster, an item) is one balancing piece; only a bare heading travels with the next piece.
- **Short last page:** a last page shorter than 250 pt (`layout.tiny_tail_pt`) pulls back the piece from the foot of the previous page, so the run fits that page or gives the last page a fuller close. A tail that keeps moving to new plans is refining; only a return to an earlier plan counts as oscillation.
- **Stacked column bands (2026-11-06):** where a two-column band starts directly beneath another on the same page (a balanced tail under a natural flow, or a page unit under a tail), a full-width 0.5 pt hairline in the gap between them marks the boundary, so the columns read band by band. It is placed, so it takes no height and moves nothing.
- **A bare heading before a page unit** opens that unit, glued to its first piece, whenever the heading and the unit fit one frame; it never closes the previous segment alone at a column foot (8.2).
- **An entry profile taller than a page** (a Basic Mode Hero) starts a fresh page, so its whole-unit subsections have full-height columns instead of leaving an empty column beside a short start.
- **Marker-only tails:** the zero-size end markers left after a full-width element are emitted as raw markers, which attach to the page they follow and never open a blank page.
- Avoid tiny two-column fragments around full-width tables: recompose the section opener, or use a sustained full-width procedure or reference region, when that reads more clearly.
- Complete the previous section before starting the next, and never put unrelated prose in a blank area to fill it. Deliberate whitespace at a section start is acceptable; an unexplained interior void from a failed balancing choice needs repair.
- Fresh pages, opener sharing, and run-on openings are decided from measured heights in the measurement pass, never from positions read during layout, which lag one iteration.
- Record exceptions by stable heading, block, and table IDs, never by frozen PDF page numbers.

## 9. Ink and fine lines

Solid black is limited to small structural marks; large black areas appear only in the art. No hairline is thinner than 0.3 pt (row hairlines are 0.35 pt). Tints are transparent black over the cream. Thumb tabs stop 3 pt short of the text frame, and their keywords stay inside the 27 pt safe line.

## 10. Adoption status

Adoption reskins the components the generator (`tools/build_book.py`) already emits. Their signatures are kept, the pagination machinery (`pm`, `bal`, `keeppage`, `munit`, `tmark`) is untouched, and new wrappers change presentation only, grouping entries the generator already recognises. Re-render the specimens, then run the gates of section 15.

**The book sets** sections 2 to 5 and 7 to 9; the chapter opener and its frame; full-width section heads and the heading hierarchy; the ledger tables, stat bar, formula stat card, and `cards`; the example and note panel; the figure band; the quiet separator; banner tags for bracketed roles and kickers; the Appendix C band and run-on sections; tailpieces; and one monster per column.

**Still specimen-only.** The book sets these structures as run-in labels and headings, or not at all: the power and item entry grammar with the tier band (6.13, 6.14); the scenario head, dossier, and outcome frame (6.16); the procedure shields (6.9); the gazetteer head (6.11); the character-entry head with its side-by-side portrait (6.12); the `entry-title` component (section 3) and the fixed bestiary portrait box (6.15); the panel banner tags (6.7); the title in the figure band (6.8); the 9% roll column (6.10, item 4: the token exists and the specimen uses it, but the book's tables do not tint it); the drop capital (section 12); column-aware tailpiece placement in a short right column; and the separate C.13 play aid (6.19), which the current build does not produce.

## 11. Owner decisions in force

Each owner decision is stated, with its date, where it applies; the full dated wording is in `docs/history/DESIGN_HISTORY.md`. The imprint decision of 2026-10-29 stands here: the version is the manuscript version, the author is Jordon, the publisher is Escutcheon Press, and there is no ISBN and no illustration credit.

## 12. The armoury: grim medieval heraldry

The owner's direction (2026-10-12) is more ornament, kept tasteful and never distracting from the text or art: grim medieval heraldry that is not on the nose. Every mark is an original vector, drawn in `typst/templates/system.typ` or traced by `tools/prepare_marks.py` onto the cream page colour, and shown on specimen 15, "The Armoury". The approvals are recorded in `production/art/marks/APPROVED.json`.

| Mark | Form | Where |
|---|---|---|
| **Chapter arms** | Owner-approved 2026-10-13 ("Approved. Make sure they are big enough to see."). One charge per part in flat black ink, with bold interior detail and no grey, inside one shared double-rimmed heater shield. World: raven on a crown broken in two. Mechanics: die. Round: hourglass. Actions: three arrows points down. Combat: bearded axe and notched sword. Party: tattered banner. Equipment: great helm. Powers: open hand with an eye. Monsters: horned wyvern's head. Scenarios: ruined arch. Campaign: war pavilion. Learn: key. Basic: lantern. Reference: open book. Index: quill and ink pot | Chapter opener (52 pt, about 0.72 in), index opener (40 pt), contents rows (20 pt), running head (15 pt), armoury sheet (52 pt). Never below 15 pt |
| **Castle logo** | Owner-approved 2026-10-13: a broken heater shield bearing a three-towered castle, cracked through its gate; "the arms of a fallen realm". It replaced the single broken-ring motif | Title-page head (1.7 in), opener-frame head (30 pt), flourish centre (22 pt), armoury sheet, player aids, and Hero records; the Escutcheon Press device takes its place on the back cover |
| **Brush rule** | A hand-inked stroke with tapered ends and a slightly uneven edge, drawn the same way every time | Section titles and table feet (2.2 pt), stat bars (2 pt), folios (1.2 pt), flourishes |
| **Engraved shield** | A heater shield with a paper inner line, carrying a number | Section numbers and folios; procedure steps and power numbers in the specimens |
| **Corner flourish** | A fine L with an inner hairline and lozenge finials | The opener frame (26 pt); scenario dossiers and outcome frames |
| **Banner tag** | A black strap with a pointed end | Bracketed roles and kickers in headings; in the specimens also EXAMPLE, RULES NOTE, scenario numbers, and place kickers |
| **Coin** | Owner-approved 2026-10-13: a hammered long-cross penny in heavy black ink (beaded border, solid cross, four pellets in each quarter), heavy enough to match bold figures; a reversed version serves black header bands. It sits on the baseline beside its figures | Stands for the source's "c" in tables and stat bars |
| **Opener frame** | A double border (1.4 pt and 0.4 pt) 0.42 in from the page edge, corner flourishes, the castle logo at the head, and the folio shield at the foot | Chapter openers; the covers draw the same frame |
| **Flourish** | Brush, castle logo, brush | Chapter openers, title pages, and front-matter boundaries only |
| **Quiet separator** | A short hairline pair around a lozenge (section 4) | The source's horizontal rules |
| **Lozenge** | A small black diamond | List bullets, subsection heads, separators |
| **Drop capital** | A blackletter initial reversed in an engraved black block, three lines deep (vendored droplet 0.3.1, MIT, `typst/vendor/`) | Specimen 3 only; the book does not set it |

**Restraint rules:**

1. Nothing ornamental inside text, table cells, or art.
2. At most one ornamental mark per heading or table edge, and at most two on an ordinary page.
3. Rules are one brush stroke or one thick-and-thin pair, never stacked.
4. Every reversed label is bold, on solid black, and no smaller than the 9 pt floor.
5. Black areas stay small and structural.

A setting-specific emblem needs a documented source meaning before it is added.

## 13. Typesetting and layout policy

The owner asked (2026-10-12) for typesetting that is easy to read, avoids page bloat, and avoids reading sections or paragraphs across pages. These rules bind the build, alongside the one-page keep rule in `docs/PROJECT_CONTRACT.md`.

**Paragraphs**

1. Justified within limits: word space 85% to 140% and letter spacing −2% to +2% of the em (Typst `justification-limits`), shared by rules text and flavour, so no line opens rivers; inspect spacing and rivers on rendered pages. Table cells, captions, stat blocks, data sidebars, and headings stay unjustified. Canadian English hyphenation is allowed in the 254.4 pt columns at normal cost (100%), so justified lines in narrow list items stay even; no hyphen in headings, names, or table cells. Short dice notation, bracketed costs, modifiers, numeric ranges, and values with units do not break, by layout rules, never by changing the text. Every list item (a talent, a starting package, a numbered step) is kept whole: it never splits across a column or a page.
2. No widows or orphans: a paragraph never leaves one line alone at the top or foot of a column (widow and orphan costs at the maximum), without forcing large gaps.
3. No runts: a paragraph's last line carries at least two words where possible (runt cost 160%).
4. A paragraph that fits a column never splits across a page turn. When a paragraph must split, it splits within a spread (verso to recto), never recto to verso, wherever the layout engine can achieve that by moving a whole unit.

12a. **Balanced columns.** Wherever a two-column run ends on a page (a section close, lore, a chapter opener's first section), the two columns are balanced to equal depth (`balanced` in `typst/templates/system.typ`), so no column stands half empty beside a full one. Lore and gazetteer text set in columns fills the full frame in two balanced columns, never a narrow single measure with a blank margin (owner 2026-10-12: the Deepwarden introduction).

**Units (what reads as one thing stays on one page)**

5. Every heading keeps its first full paragraph, or its first two list items, on the same page and column (sticky headings).
6. Examples, rules notes, procedures, stat profiles, monster, power, class, and place entries, short tables, and figures with captions are unbreakable keep units.
7. A fit-capable section or subsection moves whole to the next column or page rather than splitting (the keep rule in `docs/PROJECT_CONTRACT.md`). Only over-height units continue, with repeated headers or "(continued)".

**Avoiding page bloat**

8. Every numbered section starts on a fresh page (owner, 2026-10-12), except that the first section may share its chapter-opener page (6.5) and Appendix C runs on (6.19), both approved 2026-11-01. Space left at the end of a short section is never given to the next section; rule 9 handles it. To keep this from bloating the book, a section is composed to finish cleanly: its columns are balanced (12a), and its own figures and tables are placed so its last page is as full as the keep rules allow.
9. Space left at a section end is filled in this order (owner, 2026-10-30):
   - a source-faithful rules figure for that section (registry FIG-58 to FIG-77 close twenty short sections of Chapters 1 to 7), sized to the space the section leaves;
   - the section's own approved spot art or tailpiece (`production/art/END_ART_PLAN.json`), set by `endart` below the text only where the next heading already starts a later page, sized as section 7 describes, and omitted below 1.6 in tall;
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

**Verification** (each build): section 15, including a widow, orphan, and split-paragraph report by stable block ID; every exception is reviewed.

## 14. Source fidelity in the layout

- Preserve the manuscript bytes, every word and cell, source order, all source-bound figures, deliberate wide objects, and the existing figure and content checks. Reconciliation checks every word and cell.
- The layout changes presentation only. Typographic mappings (the coin, banner tags, the chapter label, and small capitals) keep the source's letters in the text layer.
- Running heads, continuation titles, repeated table identities, entry-name continuations, and printed figure numbers are publication furniture, not manuscript patches; the colophon names the edition's navigation additions.
- Use the source's exact headings and field labels. Never relabel mechanics or invent notes, metadata, phase labels, a callout taxonomy, or icons with rules meaning.

## 15. Review and acceptance

- **Gates on every requested build:** reconciliation of every word and cell; the one-page keep audit (`docs/PROJECT_CONTRACT.md`; 8.4); layout QA; the widow, orphan, and split-paragraph report; and the art resolution gate. Navigation and the package are rebuilt from the same final input hashes.
- **The layout audit** records semantic heading starts and their following content, page and column breaks inside short fit-capable tables and subsections, continuation titles and headers, figure-to-setup distance, row orphans, and unexplained large voids, keeping findings and reviewed exceptions by stable source IDs and current hashes. Hard failures: stranded headings or captions, missing repeat headers, an avoidable split of a fit-capable short table, content overlap or overflow, and missing or duplicate text or cells. Whitespace flags need actual inspection, not a universal ban on blank space; the density diagnostic ignores page-background furniture such as the thumb tab and reports sparse pages by chapter.
- **Visual review:** every page type at readable size; all revised pages at contact-sheet scale for rhythm; and every continuation, table exception, and scenario opening at readable size, using `docs/VISUAL_QA.md`. Whoever made the work may review and approve it once they have looked at it.
- **No pass on looks or compilation alone.** An attractive cover or opener, a successful compilation, or passing geometry checks is not evidence of editorial finish. The final design gate is usable ordinary pages, complete source reconciliation, and the table, figure, and verification checks of `docs/PROJECT_CONTRACT.md`. Record the current design outcome separately from older geometry passes.
- **Trying a change:** try it on actual-content pages (the template specimens, or a local proof of the affected pages) before applying it across the book, using real content, never invented rules or mockups. Make bounded repairs rather than wholesale redesigns, and record frozen token changes and their reference lessons in this document and `production/STATE.md`. Page savings and full-book acceptance come from same-source builds and their recorded review, not from token changes alone. Local specimens and measured builds are evidence of their stated scope, not a release approval.
- Builds, PDFs, and releases happen only on the owner's request (`AGENTS.md`).

## 16. Delivery

The book ships as one digital PDF of portrait US Letter pages, with its front and back covers inside it, and the screen companion `Heraldry_RC###_digital-compact.pdf` (`tools/digital_compact.py`): the same pages, bookmarks, and links, with rasters at 150 ppi. Navigation destinations must resolve in both. There is no print edition. Do not add a texture generator as a substitute for editorial craft.
