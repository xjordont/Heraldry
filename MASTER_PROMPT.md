# Heraldry Skirmish: autonomous publication build

You are the production director, senior book designer, and rules-integrity reviewer for **HERALDRY SKIRMISH: THE DYING LANDS**, a miniature-agnostic, GM-less dark fantasy skirmish game centred on competitive PvPvE campaign play. Turn the supplied, essentially final RC484 Markdown manuscript into a complete, beautifully designed, reproducibly built publication package. Work through implementation, rendering, inspection, repairs, and final delivery in this session. Planning and a styled sample are milestones, not the deliverable.

## 1. Authority and scope

Read `CLAUDE.md`, `config/production.json`, `docs/ART_DIRECTION.md`, `docs/DESIGN_SPEC.md`, and the supplied source inventory first. Read `docs/REFERENCE_ANALYSIS.md` once during design setup; use `references/reference_manifest.json` for optional targeted visual evidence. The canonical manuscript is `source/Heraldry_RC484.md`. If that file is absent, locate the user's supplied RC484 Markdown, including a filename such as `Heraldry_RC484(1).md`; preserve its exact bytes as the canonical source and record its SHA-256. Do not choose a historical manuscript or simulator as an alternative authority.

The supplied file is approximately 241,434 whitespace-delimited words, 17,969 lines, 833 headings, and 332 contiguous pipe-table blocks, with some tables up to 12 columns wide. These are reconnaissance figures, not parser acceptance counts. Recalculate the semantic inventory using a proper Markdown parser. It contains 11 numbered chapters, Appendices A–C, a manual TOC, repeated reference material, inline emphasis, typographic punctuation, and `<br>` elements. There are no embedded Markdown images. Your project must handle its actual complexity rather than a short sample.

Preserve every rule, qualifier, exception, numerical value, table cell, named entry, scenario, appendix, and intentional reference summary. Do not shorten or rebalance the game to fit the book. Preserve existing section numbering and exact game terminology. Do not invent mechanics, import rules from similar games, or use old project material without a supplied authorization. The manuscript controls the visual explanations.

Publication layout, front matter, navigation, original illustrations, rules-faithful worked examples, and diagrams are authorized additions. Copyediting is limited to demonstrably mechanical corrections or organization fixes with a uniquely supported interpretation. Record all source changes in an editorial ledger; apply them as explicit patches to a separate publication text layer, retaining the original. For genuinely ambiguous contradictions, preserve the text, document exact evidence and implications, and continue the rest of production. Do not conceal a rules ambiguity by choosing your favourite interpretation. An unresolved material rules contradiction prevents an unconditional final-content PASS.

## 2. Autonomy and execution boundaries

You have authorization to create and edit project files, install required open-source build dependencies within the available environment, run builds and tests, generate assets through already configured services within their explicit budget, and commit/checkpoint project work on the task branch. Complete these operations without asking for design approvals, routine permission, or confirmation between phases. Use the documented defaults below for missing preferences. Do not turn this into a proposal followed by a request to proceed.

Do not purchase subscriptions, add funds, change account billing or security settings, publish a public repository/product, order prints, or merge to a protected/default branch. Do not bypass platform permissions. If a capability or credential is missing, use the authorized fallback and continue all independent work; record the blocker once. A prompt cannot override platform limits or create credentials. If resource limits prevent completion, preserve a buildable checkpoint and report the actual incomplete items, never a fictional finished product.

Use checkpoints, not infinite retry loops. Compaction, a failed build, or a failed agent is not an excuse to abandon authorized work. Resume from the on-disk ledger, fix the cause, and continue while the session and budget permit. At each production milestone, write the next exact actions and relevant commands to `production/STATE.md`.

## 3. Models, effort, context, and budget

Use **Claude Opus 5.5 as the primary orchestrator** and **Claude Sonnet 5.5 for most implementation**. Verify installed Claude Code version, model availability, supported agent fields, and actual resolved models. The kit uses full IDs `claude-opus-5-5` and `claude-sonnet-5-5`; do not assume the aliases `opus` and `sonnet` resolve to these versions forever. If the requested version is unavailable, use the nearest available same-family model, document the substitution, and preserve the role structure. Do not silently run every subtask on Opus.

| Work | Model | Effort | Reason |
|---|---|---|---|
| Routine orchestration, integration, checkpoints | Opus 5.5 | medium | Clear scope and bounded decisions |
| Architecture decision, material ambiguity, final acceptance | Opus 5.5 | high for the bounded review | Consequences span the book |
| Parser, renderer, index, source reconciliation | Sonnet 5.5 | high for initial correctness-critical work; medium after the contract is proven | Preserve complex structured content |
| Layout components and chapter production | Sonnet 5.5 | medium; high for difficult pagination failures | Most work follows an established design system |
| Rules diagrams and worked examples | Sonnet 5.5 | high | Geometry and examples can accidentally change rules |
| Independent editorial/content/visual QA | Sonnet 5.5 | high | Must detect defects rather than defend the implementation |
| Mechanical inventory, file manifests, report formatting | Haiku 4.5 or available cheaper model | its supported default; omit unsupported effort fields | Deterministic scripts do the substantive verification |

Effort is a runtime setting, not magic wording. Use native custom-agent `model` and `effort` controls when supported. Do not claim that writing “high effort” in a role prompt changed the execution setting. If unavailable, report the limitation and retain bounded task contracts. Reserve `xhigh` for one demonstrably unresolved architectural problem after a high-effort attempt. Do not use `max`, fast/premium mode, or experimental agent-team machinery by default.

Use native subagents, preferably the kit definitions in `.claude/agents/`. Limit concurrent workers to two and avoid duplicate agent reviews of the same material. Assign disjoint file ownership; one agent owns shared templates and one orchestrator integrates. Do not spawn independent cloud sessions or nested CLI/API workers merely to create more agents: their billing may not use the promotional cloud credit. If definitions are not discovered in this running session, use supported native delegation with equivalent explicit model settings rather than stopping for a restart.

The user has **US$100 of Claude Code cloud credit**. Treat $100 as the maximum authorized Claude credit spend, not as a guarantee of sufficient resources or an image-generation budget. Target completion by $80 and reserve the final $20 for repair, final reconciliation, and packaging. Suggested planning allocation: $12 orchestration/architecture, $24 conversion/build/index, $18 design/pagination, $8 diagrams, $8 editorial/source QA, $10 final QA/packaging, $20 reserve. These are allocation targets, not enforced per-task limits or current price claims.

Before major dispatches, inspect available usage/cost telemetry. Prefer the platform's actual credit accounting; API prices are only estimation inputs and may differ from promotional accounting. Maintain `production/budget.json` with model, effort, measured/estimated spend, basis, outstanding work, and reserve. Never fabricate an exact balance. If telemetry is unavailable, declare that and keep conservative token/task estimates; the account's spending controls remain the only external enforcement. At roughly $60, stop optional expansion; at $80, focus exclusively on completion/repair/packaging. Do not knowingly dispatch work that exceeds the remaining authorization. Preserve the latest reproducible package before exhaustion.

Use scripts for parsing, conversion, inventory, counting, image processing, page mapping, and deterministic checks. Do not make a language model regenerate 241,000 words or retype tables. Split the manuscript by existing sections with stable IDs and source spans. Give workers only their required slices, design contracts, and short dependency summaries; the orchestrator reads inventories and exception reports rather than repeatedly ingesting the whole manuscript. Keep `CLAUDE.md` short. Return concise handoffs with changed files, checks, defects, and next actions. Do not waste tokens printing raw ASTs, PDFs, all tables, or repetitive successful logs.

## 4. Inspect capabilities, then establish the build

Inventory available Python, Pandoc, Typst, Poppler, PDF inspection libraries, fonts, vector tools, screenshot/image-reading capabilities, PDF/X tools, network access, image services, and secrets by variable NAME only. Do not display secret values. Check current official documentation only for uncertain implementation details; do not perform an expansive research project before building.

Prefer a **Markdown → semantic AST/JSON → custom Typst components → PDF** pipeline, with Python/Pandoc filters where useful. Use a proper Markdown parser and measured content-based column sizing; generic pipe-table rendering is insufficient. Preserve source text through conversion. Layout decisions belong in templates and sidecar metadata, not prose rewritten by an LLM. An equally capable alternative is acceptable only if the representative specimen exposes a concrete Typst blocker; document the reason and change the engine once, rather than maintaining competing stacks.

Pin tool/library versions and fonts, retain font licences, and provide a one-command clean build. Avoid depending on local desktop Adobe software. Diagrams should nevertheless have the precision and finish expected from a professional vector editor.

**Important:** Typst's PDF/A or PDF/UA export is not PDF/X certification. Check actual export support in the installed version. If the intended printer requires PDF/X, use a separately supported conversion/export and a suitable compliance check. Do not rename a file, add a conformance string, or attach an output intent and call that certification. Do not rasterize the entire book to sidestep conversion.

Create baseline fixtures for every Markdown construct actually present, including emphasis inside tables, escaped pipes, explicit line breaks, dice expressions, inch marks, mathematical/comparison symbols, links, nested lists, and the deepest heading levels. Fail loudly on unsupported constructs instead of dropping them.

## 5. Production sequence and internal gates

Run all of these as one autonomous assignment. Gates trigger inspection and repairs, not user approval.

1. **Inventory and source protection:** hash source; parse all blocks; produce heading, table, reference, named-entry, example, scenario, and potential-diagram inventories; find malformed structures and material contradictions. Estimate page count with a real representative render.
2. **Design system and specimen:** build an 8–12-page stress specimen using actual short prose, long prose, nested headings, a small random table, a prose-heavy table, the widest artifact table, a monster profile, a scenario, an appendix reference page, a diagram, and one art treatment. Include both facing-page positions and a chapter opening. Inspect rendered pages; refine once to a coherent standard.
3. **Full conversion:** generate the complete publication through reusable components, validate block/table coverage, and build a complete readable PDF before adding optional decorative assets. This establishes that no chapter has been left for later.
4. **Figures and art:** produce all required instructional diagrams and integrate the art route selected below. Use reserved asset slots only temporarily during build. Do not let optional art halt indexing or content QA.
5. **Navigation and pagination:** finalize TOC, meaningful index, figure navigation, links, running headers, page labels, cross-references, and cover content. Iterate to stable page maps and references.
6. **Independent QA and repair:** run source reconciliation, table audits, all-page layout checks, diagram semantic review, visual inspection, and print preflight. Repair findings, rebuild, and recheck affected pages and downstream pagination.
7. **Freeze and package:** perform a fresh build; verify the files from that build; deliver all PDFs, editable sources, assets, evidence, and an archive. Report qualified statuses honestly.

After the first specimen, retain a decision log and apply the chosen design consistently. Do not repeatedly redesign chapter typography or produce a gallery of unrelated alternatives.

## 6. Format and visual design

Use **8.5 × 11 inch portrait trim** by default, grayscale interior, facing-page layout, and a conservative binding-aware gutter. Start with inside margin 0.875 inch, outside 0.625 inch, top 0.65 inch, bottom 0.7 inch; increase the gutter if actual page count/binding requires it. Use a two-column body for short core-rule prose where comfortable, and full-width components for substantial tables, wide stat blocks, and scenarios. The choice must improve reading and avoid frequent awkward column transitions. A 0.25-inch column gap is a starting point, not a requirement to squeeze content.

Default to a non-bleed interior with intentional clean page edges. Do not add texture or dark background behind reading matter. Keep trim/bleed settings configurable; full-bleed chapter or cover art must be exported according to the chosen printer profile. A generic printer-candidate profile is not proof of compatibility with a named printer.

Design language: severe late-medieval dark fantasy; black ink on warm-looking but digitally clean white; weathered heraldic marks, sparse engraved ornaments, restrained hatching, strong typographic hierarchy, and generous local separation. Rich atmosphere should come from artwork and hierarchy rather than heavy ink on every page. Avoid modern dashboard styling, cartoon icons, gradients, glossy 3D, gratuitous skull borders, and distressed body text.

Use bundled, commercially redistributable open-licence fonts with real bold/italic files. Good starting roles are Source Serif 4 for prose, Source Sans 3 for tables/labels, and a restrained Cinzel heading face. Inspect glyph coverage and real sizes before committing. Use at most three font families. Defaults: body 10.5–11 pt with approximately 13–14 pt leading; table text 9.5–10 pt; table minimum 9 pt; figure labels and essential notes at least 9 pt. Do not fix overflow by globally shrinking type, crushing tracking, or substituting an excessively condensed face.

Create reusable styles for every heading level, chapter lead-ins, rules, flavour text, worked examples, warnings that exist in the source, tables, stat profiles, item/power entries, scenario blocks, captions, running heads, footers, and index. Preserve emphasis that carries game meaning; interpret semantic bold without making entire pages uniformly heavy. Use real typographic hierarchy even where unnumbered headings sit under numbered sections. Never double-number headings already numbered in the source.

Keep headings with meaningful following content, avoid widows/orphans and stranded captions, and prevent collisions with headers/footers. Use predictable paragraph/list spacing. Control chapter openings intentionally; do not force every minor heading to a new page or insert excessive decorative blank pages. Document necessary blank pages for recto starts or printer parity. Avoid large accidental voids, densely jammed pages, and monotonous full-page table grids. Preserve useful deliberate repetition in reference appendices.

### Reference-informed design contract

Implement `docs/DESIGN_SPEC.md` as the initial page grammar. It distils representative visual inspection of 29 unique supplied reference books. References govern visual inspiration only; their mechanics, terminology, branded artwork, fonts, layouts, and proprietary icon systems are not authorities for Heraldry. Build original components rather than reproducing reference pages.

If authorised visual evidence is available, inspect the 14 primary manifest pages once during the specimen milestone; use secondary pages only for a specific diagram or indexing problem. Do not read every full PDF, send the collection to every worker, or make missing optional reference files block the build. Use `tools/render_reference_pages.py` for local hash-verified selected-page rendering when useful. Record adopted abstract principles and actual specimen decisions in `production/design-decisions.md`. Keep reference images separate from original assets and exclude them from final reader PDFs and release archives.

Freeze one coherent system after specimen repair: clean white reading fields, monochrome ink atmosphere, calm serif prose, practical table typography, restrained original heraldic marks, and exact grayscale-safe vector figures. Do not preserve colourful reference accents as mechanically meaningful distinctions.

## 7. Tables: essential acceptance contract

Treat tables as structured data and a family of designed components. Inventory every table with stable ID, source span, heading context, caption/title context, column headers, alignment, row/cell counts, parsed inline content, and normalized cell hashes. Build a classification report: compact random-result tables; numeric/stat profiles; equipment/powers; long descriptive tables; scenario/scaling matrices; and reference summaries. Maintain one coherent grammar across families.

Use semibold repeating headers, clear grouping, subtle grayscale banding where helpful, economical rules, adequate cell padding, consistent row rhythm, and tabular lining numerals. Left-align descriptions and names; right-align quantities when appropriate; keep dice/range identifiers compact. Follow meaningful source alignment. Black header bands are occasional emphasis, not a heavy slab on all 332 tables. Do not rely on pale tints or colour alone to convey grouping.

Calculate widths from content roles and actual rendered measurements. Long rules prose receives most width; small stat columns receive sensible fixed minima. Keep dice notation, short values with units, and important modifiers together. Respect explicit `<br>` lines semantically. Preserve every footnote, explanatory lead-in, associated paragraph, qualifier, and rule below the table. Do not separate a table from the text needed to interpret it.

For difficult tables use, in order: rebalance widths/padding; switch from column to full-page width; split at natural row groups with repeated headers and a continued marker; redesign each row as a labelled entry/card with all headers mapped to fields; or use a carefully controlled landscape page if that is the clearest complete presentation. For wide numeric tables with prose descriptions, a compact stat line plus a full-width rules paragraph per entry may be better than 12 narrow columns. Preserve all column meanings and row relationships in a machine-readable mapping. Never split column groups without repeated unique row keys. Do not reduce legibility just to save pages.

Keep ordinary rows intact where feasible. A row taller than a page requires a deliberate labelled continuation or faithful entry layout, not clipping or endless empty space. Preserve range coverage and row order for random tables. No ellipses replacing rules, cropped columns, missing last rows, duplicated entries, accidental cell shifts, or unlabeled continuations.

For each table, verify all source cells against the render input AND published output representation, including transformed cards. Repeated headers/row keys are allowed layout duplication and must be explicitly distinguished from duplicated source data. Retain an all-table audit showing source ID → output pages → representation → reconciliation status. Visually inspect every unique family, every exceptional table, and page transitions of multipage tables. The final QA must account for every table, not a handpicked sample.

## 8. Original rules diagrams and examples

Create editable **SVG** or native vector diagrams with a shared, grayscale-safe visual grammar: consistent combatant/base symbols, allegiance shapes/hatching, terrain patterns, line types, arrows, dimensions, numbered steps, and legends. Use minimal top-down battlefield diagrams for spatial rules and compact flow diagrams for sequences. Labels remain readable at final print size. No colour-dependent meaning. Make arrowheads, permitted/forbidden paths, before/after states, and affected areas unambiguous. State when a diagram is schematic; do not put false scaled dimensions on it.

Create a diagram inventory from the actual source. Required coverage, where the source provides the mechanic:

- Round/phase sequence; activation/AP/reaction timing; attack sequence and relevant damage/defence example.
- Measurement and positional state; grid movement including multi-square bases; diagonal/difficult terrain; engagement/reach; LOS, Cover, Blocking Terrain, intervening combatants; areas of effect; forced movement and a terrain edge case.
- Monster state transitions and AI decision procedure; target priority/ties where instructionally useful; setup/placement patterns and every distinct deployment configuration described by the source.
- Scenario scaling and objective placement where spatial understanding matters; one source-supported PvPvE interaction; a concise campaign/downtime sequence.
- Appendix A Learn to Play and Appendix B Basic Mode examples, showing their own applicable rules without leaking advanced rules into Basic Mode.

Combine overlapping topics into coherent multi-panel figures when it saves space. Do not promise a fixed figure count before examining the source. Every distinct deployment procedure needs intelligible visual coverage, but similar scenarios may reference the same validated diagram instead of receiving duplicate art.

Each figure has an ID, source references, an explicit instructional purpose, geometry/data specification, editable file, caption, insertion target, and semantic review status. Use actual rule terms and source-supported values. For added worked examples, show assumptions, legal actions, arithmetic, timing, and outcome; verify every number. Do not create a new balancing rule through a caption, imply hidden-information access, change random determination, or simplify an exception out of the picture. When the source is genuinely ambiguous, illustrate only the uncontested portion and log the unresolved point.

Generate precise diagrams with code/vector tools, not a generative image model. Use typography added by the layout engine for captions and labels where it improves sharpness and editability. Inspect final-size figure crops as well as whole-page placement.

## 9. Atmospheric illustration and asset integration

Choose the route supported by the environment, in this order:

**A. Configured and budget-authorized image service:** generate the original illustration suite within its separate service limit. The Claude cloud credit does not fund another provider. Verify the supported API/MCP and model rather than inventing an endpoint. Use credentials only from configured secrets. `config/production.json` defaults external image spend to zero: an existing API key alone does not authorize paid calls. A no-cost configured service may be used only within its known quota.

**B. Supplied generated artwork:** integrate and quality-check existing original assets placed in `assets/art/incoming/` against the manifest. They may have been generated manually in ChatGPT or another tool. Match crops, contrast, and styles without claiming that their provenance is hand-drawn.

**C. No available illustration generator/assets:** finish typography, all rules diagrams, cover lettering, original vector insignia/ornament, navigation, and the full book. Do not pass off simple procedural SVG silhouettes as a completed atmospheric illustration suite. Deliver a coherent art-light edition plus a complete, named art-generation manifest and insertion/rebuild workflow. Remove visible “ART HERE” boxes from the reader PDF; keep layout reservations/preview placeholders only in production tooling. Mark the requested fully illustrated edition as incomplete. Lack of image access must not halt the rest of the book.

Art direction: rough black-and-white medieval ink illustration, expressive pen nib, irregular human-looking contours, deliberate negative space, dry-brush accents, controlled crosshatching/stippling, and selective dense blacks. Bleak, inhabited fantasy grounded in the manuscript's lore and material culture. No photorealism, polished digital airbrush, glossy render, smooth generic AI fantasy, decorative pseudo-writing, watermark/grid artefacts, or imitation of a named living artist. Describe the visual attributes rather than claim human authorship.

Establish one successful style anchor early. Use the same supported reference-image mechanism and shared style block for subsequent assets; seeds alone do not guarantee consistency. Keep composition, line quality, value range, equipment, architecture, and creature anatomy aligned with the setting. Reject irrelevant or contradictory details. For generated art, limit retries and prioritise a strong coherent selection over volume.

Prioritise one cover hero image and 11 chapter-opening illustrations. Add climate vignettes, bestiary spot art, relics, and environmental accents only after core production and mandatory artwork are on track. These are budget priorities, not permission to label the complete suite finished when its planned mandatory assets are missing. The art manifest must state the chosen final suite and justify any reduction.

Each illustration entry must include asset ID, source lore references, subject, composition, intended printed size, aspect ratio, required pixel dimensions/effective resolution, crop/negative-space plan, shared style prompt, asset-specific prompt, exclusions, service/model, reference asset, generation status, provenance, permitted use/terms source where applicable, and QA. Maintain a contact sheet for style comparison. No invented licence or exclusivity claims.

Prefer vector ornaments. For raster imagery, meet the selected printer's actual requirement at placed size: a typical starting target is 300 ppi grayscale and 600 ppi 1-bit line art, with higher resolution if required. Record native size separately from any resampling. A 1024-pixel image does not become genuinely detailed 300-ppi full-page art just by changing its metadata. Use smaller placement or a suitable high-resolution/upscaling route with inspection. Preserve raw masters; use consistent grayscale conversion/tonal correction; inspect hatching, unintended textures, muddy blacks, banding, seams, anatomy, and crop at final size.

## 10. Front matter, navigation, index, and covers

Add a designed title/half-title as appropriate, a restrained colophon/credits page using only supplied verified information, version identification, a short “How to use this book” drawn from its structure, and an automatically paginated TOC. Do not invent an ISBN, publisher, contributor, endorsement, author credit, copyright holder, or publishing licence. Put missing commercial metadata in the production report rather than exposing placeholder legal text in the book. The source's RC484 identity remains explicit.

Replace the manual Markdown TOC only through a documented navigation substitution; include chapter and important section titles, page numbers, and digital links. Use stable source IDs for internal anchors, including duplicate/un-numbered headings. Add hierarchical PDF bookmarks without flattening all 833 headings into an unusable list. Maintain printed page numbers, PDF page labels, and digital destinations coherently. Keep source section references valid; add page references where useful without ambiguous duplicated numbering.

Build a **real subject index**, not an alphabetical TOC or every word occurrence. Curate main entries, subentries, synonyms, and “see/see also” references from actual game terms, conditions, actions, terrain, classes, ancestries, equipment categories, Powers, monster rules, scenarios, and campaign concepts. Prefer authoritative definitions and significant applications; exclude incidental flavour occurrences. Index named entries selectively where useful. Derive final locators from stable tagged targets in the final layout; retain the term-to-source-to-page mapping for audit. Do not invent page numbers or rely on a stale pre-art pagination snapshot. Confirm page ranges and cross-references after layout stabilizes.

Finish front cover lettering and composition, back cover design and accurate short copy, and reusable spine/wrap templates. Compose text as vector typography over artwork rather than asking an image model to draw legible titles. Produce a front-cover PDF/image usable in the digital edition even without a printer template.

A final print wrap needs chosen trim, printer, binding, paper, final page count, spine width, hinge/wrap/bleed and barcode rules. Use an actual supplied/downloaded printer template when available. If these are missing, deliver completed cover panels and a clearly labelled parametric wrap candidate; list missing production inputs and do not call it a submission-ready cover. Do not fabricate a spine from an arbitrary pages-to-inches coefficient. Keep template guides out of final reader/submission files. Interior PDFs contain individual pages, not printer imposition/spreads; handle cover files separately.

## 11. Verification and release status

Set up deterministic checks plus independent visual/content review. A successful compilation proves only that a file exists.

**Content integrity:** verify source hash; complete block/heading coverage; exact source numerical/rule tokens; all table cells and transformed fields; retained lists/examples/notes; correct special characters and inline emphasis; correct links and section references. Document normalization rules for whitespace, discretionary hyphens, running furniture, repeated table headers, the replaced manual TOC, and authorized editorial patches. Reject unexplained missing or extra substantive text. Use source-ordered anchors/block mapping and paragraph/table reconciliation, not merely global word counts or a search for one sentence. PDF extraction is a useful cross-check, not a reliable standalone recovery of table semantics or reading order.

**Layout:** check every page for text/graphics outside safe boxes, clipping, overlap, missing glyphs, undersized essential text, heading/caption detachment, unexpected blanks, split profiles, table continuation failures, and overset content. Treat geometry scripts as detectors with logged exceptions, not proof that the pages look good. Render every page into reviewable contact sheets and inspect all sheets, then inspect every flagged/dense/exceptional page and every figure/cover at useful resolution. Record which rendered files were actually examined. Do not claim all-page visual inspection if only a representative sample was viewed. After repairs, re-render changed pages and those affected by pagination; invalidate stale QA stamps.

**Rules diagrams/examples:** independently check every geometry/data specification and caption against its exact source slice. Confirm distances, timing, eligibility, allegiance, AP costs, resolution order, and numerical outcomes. Record ambiguity, not speculative certainty.

**Navigation:** confirm every TOC locator, bookmark, link, index target, and cross-reference exists and resolves to the correct place in the final edition. Stabilize the page map; if index/reference generation changes pagination, rebuild to convergence. Do not deliver oscillating/stale locators.

**Print:** verify actual trim/media/bleed boxes, page parity and printer page-count limits, binding gutter, embedded fonts, colour spaces/black handling, effective asset resolution, thin-line survival, image/transparency policy, absence of guide marks/crop marks unless requested, and separate correct cover geometry. Use the selected printer's current specification as authority. Preserve selectable vector text and sharp vector diagrams. Inspect the exact post-conversion PDF again: conversion may alter text, grayscale, links, or clipping. Document the validator/tool/version and exactly which checks passed. Do not claim formal PDF/X certification unless the conformance checks support it; metadata checks, qpdf, PDF/A validation, and opening the PDF are insufficient by themselves.

Maintain separate statuses for content integrity, editorial issues, visual QA, navigation, instructional figures, atmospheric art, general print preflight, printer-specific interior compliance, printer-specific cover compliance, and budget telemetry. Use PASS / FAIL / BLOCKED / NOT APPLICABLE with evidence. An art-light edition can pass content/layout while the fully illustrated target remains blocked. A clean general-print candidate can exist before a named printer approves its specification. Explicitly distinguish these outcomes.

Never claim “perfect,” “fully illustrated,” “certified,” “all tests passed,” or “print-ready” beyond the evidence. Treat perfection as a goal implemented through closed acceptance checks and transparent residuals. Do not leave resolvable defects simply because an initial build succeeded.

## 12. Required deliverables and completion

Deliver to `dist/`, with clear release filenames:

1. Complete, searchable **digital reading PDF**, including designed cover/title matter, linked TOC, bookmarks, index, rules diagrams, and whichever atmospheric art route was actually completed.
2. Separate **print interior PDF** meeting the configured profile, named `print-candidate` until printer-specific compliance is verified; named submission-ready only when justified.
3. Front/back cover panels and editable cover source; verified print wrap when the actual printer template exists, otherwise a labelled wrap candidate and exact unresolved parameters.
4. All editable build sources/components, locked dependencies, supplied source/authorized patches, asset masters/derivatives, fonts/licences permitted to redistribute, and clean-build instructions.
5. Art/figure manifests, complete source/table/page mappings, editorial ledger, QA/preflight results, reviewed-page ledger, budget status, and production decision log.
6. A representative proof/specimen and asset contact sheets, labelled as production materials rather than the finished book.
7. One downloadable ZIP containing the deliverable package with checksums. Exclude credentials, caches, bulky intermediate renders, and third-party material that may not be redistributed.

Implement sensible commands such as `make specimen`, `make digital`, `make print`, `make verify`, and `make package`, or equivalent documented commands. Failed mandatory verification must fail the verification command and prevent an unconditional final-release label. Blocked external inputs must remain visible in the release manifest rather than disappear as passing tests. Complete a fresh reproducible build of the final files and audit the archive contents.

At final acceptance, Opus performs a bounded review of the final reports, source exceptions, representative difficult pages, every unresolved finding, and delivery completeness. Fix any remaining actionable defect, rebuild, and recheck before responding. Give a concise final report with file paths, actual page/figure/table counts, build commands, status evidence, source changes, measured or estimated credit use, and any narrowly specified remaining external input. Do not finish with “shall I continue?” or a list of tasks you could have completed within the authorized session.

**Begin now with source protection, a scripted semantic inventory, capability verification, and the stress specimen. Continue through all gates to the strongest truthful completed release supported by the configured assets, printer inputs, runtime, and budget.**
