# Repository and publishing audit — 2026-10-06

Scope: main parent commit 3818324466aec2d3ab0515f48f93c7c498a0a6ab, publishing scripts/templates/figure generators, Claude instructions, configuration, QA/package and GitHub state. This is a code/production audit, not a complete rules contradiction audit.

| Finding | Implemented repair |
|---|---|
| Brief required task branches and prohibited default-branch integration | Main authorized consistently; exceptions require owner decision; historical branch distinguished |
| Seven approved clarifications shipped under RC484 | Exact patch layer promoted into immutable RC485 with original/archive retained |
| Source/version/output names and metadata hard-coded | Shared registry authority, dynamic filenames/metadata and safe sequential revision command |
| Crashed QA could inherit an old PASS | Remove old report, require successful exit and fresh evidence; execution errors produce overall FAIL |
| Generated model/PDFs not bound to current inputs | Source/code/template/font/asset/generated/PDF hashes; package requires matching passing QA |
| Figure review did not expire after rule changes | Source-section dependency hashes; duplicate/empty manifests and duplicate reviews/placements rejected |
| Figure/cover/specimen placement inherited line/table numbers | Section/text anchors resolved against current parse; missing/ambiguous targets fail |
| Out-of-order text could reconcile as PASS | Fail and exit nonzero; remove unused repeated whole-stream concatenation |
| QA repeatedly queried the compiler in one process | Cache all three location queries from one disposable compiler process |
| Figures/specimen dependencies incomplete | Parse before figures, fresh verified table map before specimen, sequential writers |
| Monster-name audit absent from mandatory gate | Add it, traverse nested lists and fail on missing bestiary names |
| Raster PPI width only; white bookmark errors ignored | Check lower horizontal/vertical PPI and both variants' bookmark targets |
| Overscan crop used corner after translation | Scale and crop centrally |
| Build PDF timestamps varied | Pin to revision date; clean repeat build bytes confirmed identical |
| Calibration ruler crossed into next column | Correctly ticked three-inch ruler and compact version heading |
| ZIP omitted rebuild configuration and duplicated checksum entry | Include agents/reference metadata/instructions; unique verified checksums; own audit external |
| Historical kit/scratch reports obscured current evidence | Archive launch-kit/old visual evidence and remove scratch/debug artifacts |
| No repository regressions/history guard | Main push/PR/manual preflight/tests and base-commit snapshot/record immutability check |
| Large binary connector uploads stall | GitHub rebuilds the reviewed delivery with pinned dependencies, preserves artifacts and fast-forward commits generated outputs to main |
| Locked unused libraries increased setup | Remove unused PDF analysis, Markdown plugin and Brotli packages |

12 regression tests pass: revision sequencing, immutable history, artwork without RC bump, unapproved/no-op/mismatched/replayed patch rejection, tamper detection, figure-rule currency, stale/missing QA and visual currency. All 18 release checks pass; 332 tables and 19 figures remain intact. All 436 interior pages were inspected on contact sheets, with limited detailed review separately documented. The original RC484 and font blobs were verified unchanged. Package entries/checksums are verified; extracted clean-build evidence is production/qa/rebuild-audit.json.

GitHub initially had main and the identical historical Claude branch, no open issues/PRs and no Actions runs. Main was already default and unprotected. Rulesets were unavailable for this private repository's account plan; repository instructions/CI cannot override platform restrictions. No account/security settings were changed. The first repository-check run and full verified-delivery run both passed on GitHub. The delivery workflow committed RC485 PDFs and the release archive directly to main; all six primary PDF Git blob hashes matched the locally reviewed files exactly. The delivery job also runs the base-commit immutability guard before publishing.

The parser rejects unsupported Markdown; new constructs need explicit parser/rendering work. Persistent attachments use content anchors; figure dependencies are deliberately conservative and can invalidate a review after a broader section change. Inspect the actual diff before renewing a semantic review; copying a hash is not review.

Automatic table checks establish normalized cell presence in a local PDF text window and representation mappings, not every repeated-cell multiplicity, every font run's local association or game-mechanics meaning. Contact sheets are not glyph-level proofreading. Atmospheric art, physical printing and complete contradiction review remain explicitly unresolved scope.

Built binaries are no longer committed (owner, 2026-10-11: "set up the leanest, most efficient, most logical high quality workflow for repeatedly dealing with large files"). Each requested build is published as a GitHub Release; art ZIPs are built on request (`docs/LARGE_FILES.md`). Earlier binaries remain in Git history, unaltered. Never silently remove deliverables or change access. Manuscript history uses immutable numbered snapshots on main, rather than Git branches.
