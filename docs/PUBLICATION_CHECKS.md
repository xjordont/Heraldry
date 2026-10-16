# Targeted publication checks

Owner instruction, 2026-10-15: "Continue as you suggest", following the publication-improvement report. This authorises the initial authority review, bounded editorial review, calibration correction, and preparation of reader, accessibility, and physical-proof checks. It does not resolve a substantive rules conflict, approve an unseen manuscript patch, commission a person, or request a new book PDF.

Owner approval update, 2026-10-15: "Approve all as proposed." The five canon alignments are recorded in `CANON_AUTHORITY.md`; the ten approved editorial replacements are applied in RC493 and archived in `editorial/history/RC493.json`. No new publication build was requested.

Current delivered-file baseline: RC492-build-37. Use `source/versions.json`, `dist/RELEASE.json`, and `production/RELEASE_RESULT.json` to confirm the current source and last delivery when executing this protocol. Later code changes do not update the released files. These checks supplement the existing release gates; this document does not add automatic publication gates or replace the existing ledgers.

## Evidence and status

The first-pass record is [publication-first-pass.md](../production/qa/publication-first-pass.md). Authority questions are in [publication-authority-review.md](../production/qa/publication-authority-review.md); contextual editorial findings and exact draft edits are in [independent-editorial-first-pass.md](../production/qa/independent-editorial-first-pass.md) and `editorial/history/RC493.json`.

Use these distinct statuses:

- **PROPOSED:** an edit or decision has not been approved.
- **PLANNED / NOT RUN:** a procedure exists, but no observation has been made.
- **SOURCE REVIEW ONLY:** the named source scope was actually examined; no final-format claim follows.
- **OBSERVED:** record the exact file, task, device, result, and limits. A result applies only to that scope.
- **PHYSICAL PRINT: NOT TESTED:** retain until real sheets are examined.

Record the file's SHA-256 and byte count against the release manifest before a PDF test. Preserve any existing file with a different hash; do not rename an older PDF to stand in for the release or rebuild the book to obtain evidence without a separate build request. Put downloaded PDFs, page renders, and execution notes in ignored `build/checks/` or an external scratch folder. Keep actual release ledgers intact.

## Authority and editorial review

1. Obtain a disposition for each scoped brief/source conflict. The matrix distinguishes inherited RC484 rules from subsequent exact patches. Do not infer that a later owner's unrelated approval authorises an earlier mechanical choice.
2. Review the concrete editorial patch packet against the full rule and any affected profile. Keep timing/rider/activation effects intact. Proposed patches cannot be promoted.
3. After explicit approval of exact text, use the revision engine for one new immutable RC. Check content anchors and figure dependencies; do not change old snapshots or manufacture fresh semantic approvals.
4. Arrange a complete human copyedit when an editor is selected. No recruitment, outreach, or paid commissioning has occurred. The fresh delegated source pass is a second model review, not a human editorial sign-off.
5. For final-format proofreading, use the exact delivered PDF at readable detail. Allocate all PDF pages to a named reviewer and log their coverage. Examine glyphs, measurements, line endings, table continuations, captions, index locators, links, and running matter. Check the same passage in source when a layout or wording issue is suspected. Contact-sheet coverage does not count as character-level coverage.

Each finding needs a stable source location, PDF viewer page where observed, issue, proposed exact correction, mechanical impact, disposition, and reviewer. Any changed PDF needs its own review; a source edit does not approve its eventual typesetting.

## Bounded reader study

Begin with a small formative round using the unchanged released edition. Include new readers in Tabletop and Grid Mode and readers able to attempt campaign/PvE lookup tasks. Log experience and mode. Small samples diagnose problems; they do not establish population success rates or balance.

Provide the files and ordinary equipment intended for that task. Give a goal without naming the answer's heading or teaching the procedure. An observer records behaviour without correcting the participant. Record an intervention if assistance is necessary; do not relabel an assisted completion as independent success. Stop a task at its agreed limit and retain what happened.

| Task | Goal supplied to the participant | Authoritative comparison |
| --- | --- | --- |
| R01 | Find the intended route for a first game. | 1.1 reading routes and Appendix A |
| R02 | Set up the teaching game and complete a round. | Appendix A, including its explicit teaching exceptions |
| R03 | Prepare a Basic Mode game and identify what an optional variant needs. | Appendix B; compare the component-list finding without silently supplying a correction |
| R04 | Determine when a defensive Reaction must be chosen and resolve a stated attack using its existing printed rolls. | 5.2 and 5.5; use the approved current rules, not an inferred brief |
| R05 | Reproduce a spatial interaction or map setup in the assigned mode and distinguish mandatory from illustrative placements. | Relevant full movement/LOS rule, existing figure, caption, and key |
| R06 | Resolve a Monster activation with no visible enemy and a potential Hidden enemy. | 9.5, then compare the C.13 reference route |
| R07 | Find and apply the solo/cooperative setup and phase-order rules. | 10.5, including scenario overrides |
| R08 | Find the ordinary Town Phase allowance and one applicable exception. | 11.2.4 and the stated Journey result |

Prepare any task state from the current rulebook before testing; do not invent die results and report them as observed play. For R04, distinguish reading a printed example from rolling an actual game. Retain the scenario's declared positions and mode when interpreting spatial errors.

Record time to first useful source, time to a ruling, searched terms, wrong destinations, omitted steps, legal setup/application, assistance, and unresolved questions. Classify a failure as wording, navigation, diagram interpretation, arithmetic, or state tracking only when observations support it.

Proposed initial targets are unassisted tutorial setup and one complete round, correct tested mandatory procedures, and common lookups within 60 seconds. These are project targets, not industry standards. Confirm task limits before running; use the baseline to decide suitable later thresholds. Do not change a target after seeing results merely to record success.

Only recurring observed problems justify an index alias, session sheet, new example, or changed figure/caption. Draft the smallest remedy and repeat the affected task. Preserve all mechanics and both play modes. No reader study has yet been executed under this protocol.

## Delivered-PDF accessibility

First obtain and hash-check the actual released digital PDF. Existing tags, language, bookmarks, and semantic headers are useful evidence, not a complete accessibility result. Lack of explicit image alternatives in a source helper is a concern to investigate; it does not by itself prove the delivered document's state.

1. Record document title/language, permissions, outline/link structure, tag-tree presence, and any claimed conformance. A tag tree alone does not prove useful reading order.
2. With a supported PDF viewer and screen reader, follow a two-column rules page, a table, a glossary/index passage, and a chapter-to-reference route. Record exact application, screen reader, version, and pages/tasks.
3. Check header-to-cell relationships, heading navigation, text selection/copying, and how coin amounts are spoken. The current source retains currency text; test for one correct announcement including its unit.
4. Inventory all instructional figures and classify informative/decorative assets. Review meaningful alternatives against the same rule and diagram. Captions that only name a diagram may not convey its lesson. Decorative marks should not interrupt reading; informative diagrams must not be hidden as decoration.
5. Record observed failures and propose source-level fixes. Review the alternatives for rules fidelity. Re-test exact changed files and preserve visible design unless an observed problem requires a change.

Do not claim PDF/UA conformance from a compile flag, extracted text, a validator alone, or this plan. Automated and manual evidence must cover the claimed standard and exact output. No screen-reader or delivered-PDF accessibility result has yet been recorded here.

Technical references: [Typst accessibility](https://typst.app/docs/guides/accessibility/), [Typst PDF export](https://typst.app/docs/reference/pdf/), [W3C reading order](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF3), [W3C images](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF1), and [W3C tables](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF6).

## Physical reproduction and binding

Follow [INKJET_PRINT.md](INKJET_PRINT.md) and the intended printer's actual manual once its model is known. The corrected calibration source is available for the next requested build. Its newly rendered PNGs are diagnostics for source validation, not replacement print PDFs or evidence of a physical proof.

1. Record printer/driver, media, quality, borderless expansion, application scale, duplex/flip direction, and intended binding. Do not guess settings or send a print job without the intended physical setup.
2. Print the appropriate released calibration and representative dense rules, table, index, small illustration, diagram, dark opener, and cover at actual size. The old release's calibration still contains the documented label mismatch; identify that limitation if using it before a new build.
3. Measure the calibration inch and edge-safe frame. Inspect fine hatch separation, small text, bands, dark solids, offset, drying, and cream/white reproduction. Note the exact asset and placed size for any art issue.
4. If binding is intended, inspect front/middle/rear inner columns in a representative bound block or actual proof. Existing 0.75-inch inner margins are not automatically too small. A gutter change requires demonstrated need and downstream pagination review.
5. Photograph or record actual observations and propose only the smallest evidenced remedy. Upsampled cover pixels do not establish native detail; an approved illustration does not need a redo without an observed defect.

Physical printing remains **NOT TESTED**. Printer, paper, binding, and examined sheets are still required for execution. Commercial manufacturing and cover-wrap work remain separate owner decisions.

## Execution record

For each completed task record: date; operator/reviewer; manuscript revision; build/tag; file path, bytes, and SHA-256; device/application/mode; source and PDF-page scope; procedure; observations; assistance; failures; disposition; and limits. Keep planned tasks distinct from observed results. Never refresh production release, semantic, or visual approval hashes merely to remove a warning.
