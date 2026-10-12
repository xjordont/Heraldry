# Release status — Heraldry Skirmish RC492

Build policy (owner, 2026-10-11): PDFs are rebuilt only on request. `dist/` and the build evidence below describe the last requested build; when the source or art has moved past it, the table says so. Last build: 2026-10-11, RC492 with the six ChatGPT Work anchors placed (inkjet PDF 1cef40de, 598 interior pages). Its PDFs predate the large-file policy (`docs/LARGE_FILES.md`): they are no longer in the working tree but remain in Git history at commit 3da756f; the next requested build is published as a GitHub Release.

Active revision and hashes: `source/versions.json`. Current build evidence: `production/build-provenance.json`, `production/qa/STATUS.json` and the scoped visual/figure ledgers. RC484–RC486 remain unchanged.

| Area | Status | Evidence and scope |
|---|---|---|
| RC492 owner corrections | PASS | Basilisk coded L without the ox comparison; Undermarches 6 Shadow Brand reverted to the allied Spectre Summon; art size words reverted. Figure gate 57/57; pages 280 and 434 inspected; 19/19 checks PASS on RC492 |
| RC489/RC490 audit resolution | PASS | Independent RC488 manuscript and art audits resolved: RC489 (31 owner-approved patches) and RC490 (correction of a duplicated clause). Figure gate 57/57 with 0 open; every changed page inspected; 19/19 checks PASS on RC490. RC491 settled the Desert Naga flavour (owner); its Noxcloth reward was reverted in RC492; judgement-call wording left as written |
| RC488 owner refinements | PASS | 13 owner-instructed patches: Undead Champion War Maul; Stone Sentinel stone greatsword; Orc and White Court Guard one-handed weapon plus Shield Wall; Scorpion and Frost Giant descriptions; Noxcloth size M; Mire 2 and 5 deploy only Mire creatures. FIG-52 redrawn, independent figure gate 57/57 with 0 open. 597 interior pages, 11 changed pages inspected, 19/19 checks PASS. Basilisk/Medusa Petrifying Gaze kept unchanged (owner, 2026-10-10) |
| Artwork route | Local Codex to GitHub main (owner 2026-10-11) | 275 planned; 142 approved from the Codex runs (2026-10-12), the rest queued or in review: the owner cleared all twelve earlier approvals on 2026-10-12 to start fresh. The RC492 build placed the six anchors of that time; the next requested build places only newly approved art (the twelve atmospheric masters remain the chapter and cover fallback). Batch queue: all 275 items, one generation per item (owner 2026-10-12), under the gritty old-school direction with reference mapping v8 (17 sets of up to five references (the image tool's limit), 66 distinct images: owner samples plus four public-domain prints) and skill v8. Delivery after every image, drift review every 10; the first seventeen items cover every reference set. Codex runs the whole list in one prompt (owner 2026-10-12); drift reviews are reported, not stops; at the ChatGPT Plus usage limit (resets every 5 hours) the same prompt resumes (`production/art/codex/CODEX_PROMPT.md`). The last build (dist/) predates this art |
| Manuscript repairs | COMPLETE | F01–F21 and U01–U06 resolved through one owner-authorized 48-patch batch; exact archived reconstruction and immutable parent hashes verified |
| Intentional item values | PRESERVED | All 835 printed Cost/Value cells unchanged; development pricing formula/multipliers and quality-table Value columns removed |
| Repository tests | PASS | 17 regression tests; 8 source preflight checks; locked dependencies installed before CI tests |
| Automated release gate | PASS | 19 checks bound to current inputs and PDF hashes; see `qa/STATUS.json` |
| Content integrity | PASS | 8,429 text blocks in order, 332 tables / 10,315 cells, no missing/duplicated/out-of-order content; bundled fonts |
| One-page keeps | PASS | 1,835 units audited, 1,539 fit-capable, no avoidable splits or missing coverage |
| Navigation | PASS | Current index/bookmark/internal-link and section-reference audits pass |
| Instructional figures | PASS (scoped) | 57 source-bound figures, no stale reviews or open major/minor findings; current review by repair author, historical independent review retained |
| Visual QA | PASS (scoped) | Last build: 598 pages, delta-reviewed against the reviewed 597-page RC492 PDF (changed pages 4-5, 11-14, 99-115, 265 and 277 inspected); earlier: all 597 cream interior pages at contact-sheet scale; nineteen detailed pages, inherited blank, covers, calibration and overscan specimen reviewed |
| Inkjet files | PASS (automated) | Cream/white Letter interiors, identical pagination, embedded fonts and safe essential text; calibration reviewed |
| Package | PASS | Archive uniqueness, integrity and checksums verified by `qa/package-audit.json`; GitHub CI rebuilds delivery independently |
| Artwork | Existing approved masters retained | Proposed replacement spot art is withheld; new candidate approval remains separate work |
| Original run annotations | UNVERIFIED | Three annotation texts unavailable through plugin; browser sign-in cancelled; no invented annotation causes |
| Physical printer proof | NOT TESTED | No printed sheets examined |
| Commercial wrap/PDF-X | NOT APPLICABLE | Not requested |

Digital: 600 pages. Interiors: 597 each. Specimen: 13 pages. Visual review is not glyph-level proofreading or independent second review. The audit closure explicitly distinguishes existing rules from owner-authorized procedural completions and new illustrative dice results. Author, publisher, ISBN and copyright-holder metadata remain unset.

The RC486 audit and its proposed value replacements remain historical evidence. CA10–CA13 are withdrawn because the owner confirmed listed values are intentional; use `qa/manuscript-contradiction-resolution.md` for current decisions. No RC484–RC486 snapshot was edited.


## Artwork instruction reconciliation - 2026-10-11

Owner authorization: after requesting GitHub main as the primary route, "Ok apply your proposals". This milestone updates standing prompts and the Codex runbook only. No manuscript revision, artwork generation, receipt, approval, layout build, or PDF was produced. Existing `dist/` and visual/build ledgers remain evidence of the last requested build. The local image-generation smoke/pilot and LFS artwork delivery are still untested.

Validation: source preflight PASS (8 checks); art preflight READY; documentation links, fenced blocks, allowlist, preserved offline procedure, and git diff --check PASS. The repository suite ran 71 tests (1 Windows helper-path failure, 23 skipped); the v6 suite ran 32 tests (1 Windows reference-path failure). Tests, helpers, queued prompts, receipts, and packaged inputs were unchanged. Local CRLF conversion was disabled after restoring unchanged text to its exact committed LF bytes. These failures remain open; no production smoke or LFS artwork push was tested.
