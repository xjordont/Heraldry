# Release status — Heraldry Skirmish RC492

## Current delivery - 2026-10-15 handoff

Tooling update, 2026-10-15: manuscript/preflight UTF-8 handling, review gates, Windows ZIP paths, and release-result reporting have changed since build 37. The PDFs, package, and hash-bound ledgers below remain evidence for that last requested release. These code repairs have not been exercised in a new publication build; the manuscript remains RC492. Physical print remains **NOT TESTED**.

Dependency audit, 2026-10-15: the Windows virtual environment matches all 9 locked packages, including newly declared cover/mark authoring dependencies NumPy and potracer. Runtime smoke checks pass; `BUILD.md` records the explicit Windows commands. This lock update has not triggered a publication build or replaced build 37's evidence.

Workflow refinement, 2026-10-15: developer checks now use `python tools/dev.py check` and write only ignored local diagnostics. CI adds Windows coverage, dependency checks/caching, a shared publishing queue, strict candidate gating, and compact failure artifacts. Request/review helpers test and scope their commits without automatic rebasing. Production build/QA records below still describe build 37; no new publication build was requested for these changes.

Repository cleanup, 2026-10-15: removed exact duplicate applied proposals, a retired mark generator, a redundant ignore file, and unused Typst definitions; current artwork/figure sources and all immutable history/review evidence remain. The removal inventory is `production/cleanup/2026-10-15.json`. No new PDF build was requested; the production records below remain bound to build 37.

Manuscript workflow, 2026-10-15: full UTF-8 Markdown updates now have a deterministic prepare/review/apply path, documented in `docs/MANUSCRIPT_UPDATES.md`. It checks exact hashes, anchors, affected figures, and current main before promoting an approved batch through the revision engine, with rollback for ordinary write failures. No real manuscript update was supplied or promoted; RC492 and all build 37 PDF/review evidence remain unchanged. This tooling has not been exercised in a new publication build.

Latest requested delivery: [RC492-build-37](https://github.com/xjordont/Heraldry/releases/tag/RC492-build-37), built from `5eebea0ac89a0d0f10728c8e0c19d78e6db38fe0`. `production/RELEASE_RESULT.json` records RELEASED; `dist/RELEASE.json` lists all 10 assets and SHA-256 hashes. The release contains six edition/cover/calibration PDFs, the specimen PDF, release ZIP, SHA256SUMS, and print instructions. Interiors: 672 pages each; digital: 675 pages. All 275 illustrations are approved and the art queue is empty. This documentation handoff does not rebuild or change the manuscript, artwork, layout, or released files.

| Area | Current release evidence |
|---|---|
| Automated release gate | 19/19 PASS in `production/qa/STATUS.json` |
| Visual review | PASS for cream PDF SHA-256 `10e4f8bea8cff69404a6ee1385077e0533b767ff1815714cd0b2532e245a8e78`; recorded inspection of 28 contact sheets covering all 672 pages, 29 detail pages, both covers, and calibration. Minor whitespace accepted on pages 92, 123, 162, 187, and 249; no major findings. Not glyph-level proofreading or an independent second review |
| One-page keeps | 1,557 units audited, 1,250 fit-capable, no avoidable splits or missing coverage; visual review remains the backstop |
| Package | PASS: 705 entries, 704 checksums verified, no duplicate entries; ZIP SHA-256 `3b29c62cb1ddc72888da05a22e3750fd7fcaafe57a22fca9ea64559f14ed924d` |
| Cover | Owner picture is the whole front cover. Title/subtitle alignment with the title page and back cover awaits owner decision; source resolution is 912x1168 pixels (about 118 ppi at print size) |
| Physical printer proof | **NOT TESTED**: no printed sheets examined |

The records below are historical status for the 2026-10-13 build and earlier work. Their page counts, art counts, test counts, and review scope do not describe build 37. Current release evidence remains bound to build 37; the later handoff documentation is not part of its ZIP. See `production/STATE.md` for the reconciled handoff and open owner items.

## Historical status - 2026-10-13 and earlier

Build policy (owner, 2026-10-11): PDFs are rebuilt only on request. `dist/` and the build evidence below describe the last requested build; when the source or art has moved past it, the table says so. Last build: 2026-10-13, RC492 in design v4 "Grim Heraldry" (owner request 2026-10-13: step 2, adopt the design into the book with a build), inkjet PDF e5dfc3c6 (clean build), 656 interior pages (digital 659). It places the art approved at that time (184 of 275); the PDFs are published as a GitHub Release by the `Rebuild verified delivery` workflow, never committed.

Active revision and hashes: `source/versions.json`. Current build evidence: `production/build-provenance.json`, `production/qa/STATUS.json` and the scoped visual/figure ledgers. RC484–RC486 remain unchanged.

| Area | Status | Evidence and scope |
|---|---|---|
| Design v4 adoption | PASS | Owner-approved specimens (2026-10-12/13) applied book-wide: 11 pt justified text, IM FELL flavour, Grenze Gotisch titles, ledger tables with the coin mark, chapter arms on tabs, running heads and contents, castle logo on the opener frames, title page and covers. Reconciliation maps: IM FELL counts as emphasis; labels use small caps, never upper case; the coin overlays the source "c". Page count 598 -> 656 from the 11 pt body |
| RC492 owner corrections | PASS | Basilisk coded L without the ox comparison; Undermarches 6 Shadow Brand reverted to the allied Spectre Summon; art size words reverted. Figure gate 57/57; pages 280 and 434 inspected; 19/19 checks PASS on RC492 |
| RC489/RC490 audit resolution | PASS | Independent RC488 manuscript and art audits resolved: RC489 (31 owner-approved patches) and RC490 (correction of a duplicated clause). Figure gate 57/57 with 0 open; every changed page inspected; 19/19 checks PASS on RC490. RC491 settled the Desert Naga flavour (owner); its Noxcloth reward was reverted in RC492; judgement-call wording left as written |
| RC488 owner refinements | PASS | 13 owner-instructed patches: Undead Champion War Maul; Stone Sentinel stone greatsword; Orc and White Court Guard one-handed weapon plus Shield Wall; Scorpion and Frost Giant descriptions; Noxcloth size M; Mire 2 and 5 deploy only Mire creatures. FIG-52 redrawn, independent figure gate 57/57 with 0 open. 597 interior pages, 11 changed pages inspected, 19/19 checks PASS. Basilisk/Medusa Petrifying Gaze kept unchanged (owner, 2026-10-10) |
| Artwork route | Local Codex to GitHub main (owner 2026-10-11) | 275 planned; 142 approved from the Codex runs (2026-10-12), the rest queued or in review: the owner cleared all twelve earlier approvals on 2026-10-12 to start fresh. The RC492 build placed the six anchors of that time; the next requested build places only newly approved art (the twelve atmospheric masters remain the chapter and cover fallback). Batch queue: all 275 items, one generation per item (owner 2026-10-12), under the gritty old-school direction with reference mapping v8 (17 sets of up to five references (the image tool's limit), 66 distinct images: owner samples plus four public-domain prints) and skill v8. Delivery after every image, drift review every 10; the first seventeen items cover every reference set. Codex runs the whole list in one prompt (owner 2026-10-12); drift reviews are reported, not stops; at the ChatGPT Plus usage limit (resets every 5 hours) the same prompt resumes (`production/art/codex/CODEX_PROMPT.md`). The last build (dist/) predates this art |
| Manuscript repairs | COMPLETE | F01–F21 and U01–U06 resolved through one owner-authorized 48-patch batch; exact archived reconstruction and immutable parent hashes verified |
| Intentional item values | PRESERVED | All 835 printed Cost/Value cells unchanged; development pricing formula/multipliers and quality-table Value columns removed |
| Repository tests | PASS | 17 regression tests; 8 source preflight checks; locked dependencies installed before CI tests |
| Automated release gate | PASS | 19 checks bound to current inputs and PDF hashes; see `qa/STATUS.json` |
| Content integrity | PASS | 8,429 text blocks in order, 332 tables / 10,315 cells, 22,828 bold and 447 emphasis runs, no missing/duplicated/out-of-order content; bundled fonts |
| One-page keeps | PASS | 1,857 units audited, 1,550 fit-capable, no avoidable splits or missing coverage |
| Navigation | PASS | Current index/bookmark/internal-link and section-reference audits pass |
| Instructional figures | PASS (scoped) | 57 source-bound figures, no stale reviews or open major/minor findings; current review by repair author, historical independent review retained |
| Visual QA | PASS (scoped) | Last build: all 656 pages of the exact PDF at contact-sheet scale, fourteen pages in detail, covers and calibration; six layout findings repaired before sign-off (two blank pages, a three-page Basic scenario, stranded table headings, upscaled opener art, tab overscan, text-layer labels) |
| Inkjet files | PASS (automated) | Cream/white Letter interiors, identical pagination, embedded fonts and safe essential text; calibration reviewed |
| Package | PASS | Archive uniqueness, integrity and checksums verified by `qa/package-audit.json`; GitHub CI rebuilds delivery independently |
| Artwork | Existing approved masters retained | Proposed replacement spot art is withheld; new candidate approval remains separate work |
| Original run annotations | UNVERIFIED | Three annotation texts unavailable through plugin; browser sign-in cancelled; no invented annotation causes |
| Physical printer proof | NOT TESTED | No printed sheets examined |
| Commercial wrap/PDF-X | NOT APPLICABLE | Not requested |

Digital: 659 pages. Interiors: 656 each. Visual review is not glyph-level proofreading or independent second review. The audit closure explicitly distinguishes existing rules from owner-authorized procedural completions and new illustrative dice results. Author, publisher, ISBN and copyright-holder metadata remain unset.

The RC486 audit and its proposed value replacements remain historical evidence. CA10–CA13 are withdrawn because the owner confirmed listed values are intentional; use `qa/manuscript-contradiction-resolution.md` for current decisions. No RC484–RC486 snapshot was edited.


## Artwork instruction reconciliation - 2026-10-11

Owner authorization: after requesting GitHub main as the primary route, "Ok apply your proposals". This milestone updates standing prompts and the Codex runbook only. No manuscript revision, artwork generation, receipt, approval, layout build, or PDF was produced. Existing `dist/` and visual/build ledgers remain evidence of the last requested build. The local image-generation smoke/pilot and LFS artwork delivery are still untested.

Validation: source preflight PASS (8 checks); art preflight READY; documentation links, fenced blocks, allowlist, preserved offline procedure, and git diff --check PASS. The repository suite ran 71 tests (1 Windows helper-path failure, 23 skipped); the v6 suite ran 32 tests (1 Windows reference-path failure). Tests, helpers, queued prompts, receipts, and packaged inputs were unchanged. Local CRLF conversion was disabled after restoring unchanged text to its exact committed LF bytes. These failures remain open; no production smoke or LFS artwork push was tested.
