# RC493 approved editorial application

Follow-up, 2026-10-16: the owner subsequently authorized all figure repairs. All 57 figures received fresh review; the four figure-copy proposals recorded below are now resolved. See [all-figure review](figure-review-all-rc493.md). The original source application evidence below remains historical.

Owner instruction, 2026-10-15: **"Approve all as proposed."** This approves the ten exact manuscript replacements and five future-work canon alignments presented after commit `bb0e4b30`. The subsequent instruction **"Continue"** confirms continuation of this integration. No new publication build was requested.

## Applied source

The revision engine created `source/Heraldry_RC493.md` once. SHA-256: `c8e72ea694fde5c85df112514b5aaaabd03b34900c143eab082a2f73b5c039dd`; 1,454,196 bytes. Parent RC492 remains byte-for-byte unchanged. The canonical approved batch is [RC493.json](../../editorial/history/RC493.json), SHA-256 `a9303b69f0b167350d87b83dd2ec2cb7c1baa5f8f2cb1300205dd48eaccca1dc`.

| Finding | Applied correction |
| --- | --- |
| E01 | The teaching Dire Wolf selects its Engaged target without attacking twice, skips movement when already Engaged, applies Pack Tactics before damage, and resolves the damage-triggered STR/Prone rider before ending. |
| E02 | C.13 includes the existing full-rule Search branch, including the enemy controller's Check and activation ending. |
| E03 | The Shortsword Parry example uses the legal STR +2 modifier and total/Riposte 10; its printed dice remain 6 and 2. |
| E04 | The teaching Block example declares and pays for Block before rolling damage; its existing mitigation arithmetic is unchanged. |
| E05 | Mara's alternative Reaction is Dodge rather than unavailable Block. |
| E06 | Three contextual definition/Monster AI pronoun corrections preserve their meaning. |
| E07 | Basic Mode lists the fourth Satchel and Entry marker required by the existing Advanced Ogre variant. |

The six-step Dire Wolf procedure was traced for an initially Engaged wolf and an initially unengaged wolf: each reaches at most one Bite; the unengaged branch may end without attacking; Pack Tactics precedes base dice and the STR/Prone rider follows damage. This is a source-procedure check, not a newly played game or new dice observation.

All ten replacements and the revision marker reconstruct the exact RC493 bytes. All prior manuscript/archive files remain unchanged; all 332 table-cell hashes match the prior inventory. Reparse preserved 833 headings, 332 tables without ragged rows, and all 63 content-anchor resolutions. Source/index inventories were updated without running the Make parse target's PDF-producing extras. No manuscript prose outside the approved replacements and version marker changed. [Verification record](rc493-editorial-verification.json).

The applied proposal copy was removed only after its byte identity with the canonical archive and archive hash were recorded. Existing Git history retains the reviewed proposed form; the immutable archive retains the exact approved form. The batch cannot be replayed as a new revision.

## Approved canon alignment

[CANON_AUTHORITY.md](../../docs/CANON_AUTHORITY.md), linked prominently by `CLAUDE.md` and `AGENTS.md`, records the five approved alignments: 4 TAP with Journey exceptions; Druidic Rituals; Appendix C as the subordinate reference; automatic armour with shield mitigation through Block and no Brace; and no Monster ability Checks, preserving the stated immunities and higher-LVL casting restriction. These retain existing rules rather than introducing a mechanical conversion.

## Figure review

FIG-06, 11, 12, 16, 18, and 19 depend on changed source sections. Each current SVG was actually rendered to PNG and viewed, with its caption and relevant full rules compared. Their six source-review bindings were updated after those reviews. All SVG and caption bytes remain unchanged; the other 51 review entries remain unchanged. The current semantic gate passes 57/57, with no stale entries or open major findings.

Four newly recorded minor follow-ups remain **open and unapplied**: FIG-11's singular pronoun and caption continuation exception, FIG-12's four em dashes, and FIG-18's compact Dodge-declaration wording. These were discovered during the delta review and were not part of the ten approved manuscript replacements. The reports contain the precise proposed copy fixes: [AI/geometry review](rc493-figure-review-ai.md) and [setup/teaching review](rc493-figure-review-setup.md). Existing resolved/accepted limitations are retained with current observations distinguished from historical ones.

## Validation and limits

Baseline and post-integration developer checks both passed 190 tests with 3 expected empty-art-queue skips, locked dependencies/pip consistency, 8 baseline contracts, all 17 protected prior manuscript/archive files, and whitespace. The final run completed in 118.112 seconds. The current figure gate passes 57/57 with no stale or open major entries and 4 open minor notes. The exact reconstruction, preserved table hashes, anchor resolution, and real six-figure reviews are separate evidence from the unit suite. Hosted CI and publication builds were not run by this validation.

The last delivered PDFs remain **RC492-build-37**. RC493 has not been typeset, visually reviewed as a book, packaged, or released. The previous release's PDF/visual/package ledgers remain intact. This work does not complete human copyediting, reader studies, screen-reader testing, native InDesign composition, or physical proof. **Physical print: NOT TESTED.**
