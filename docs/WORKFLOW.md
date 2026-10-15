# Iteration workflow

`main` is the single working and delivery branch. The owner has authorized ordinary verified iterations on main. Create another branch only following an explicit owner decision with a recorded purpose; one project does not require a branch per component. The existing Claude build branch is an archived checkpoint, not a destination for new work.

Before editing, inspect `git status`, the current branch, and the remote main head. Bring an untouched checkout up to date with `git fetch origin` and `git switch main`, then `git pull --ff-only`. Preserve unrelated local work and inspect divergence rather than force-pushing or resetting it. Claude cloud may impose its own branch restrictions; report an actual restriction if encountered. Do not invent an exception to this policy or change account settings.

## Routine development

Run `python tools/dev.py check` after syncing and before publishing an ordinary iteration. It selects the project Python environment, checks every locked version and import, runs baseline preflight and snapshot-history protection against the local `origin/main` tracking ref, checks whitespace, and runs `make test`. Use `--base <commit>` when a different confirmed history boundary is required. `doctor` checks only the environment; `status` shows local Git state and the last requested release. These commands do not fetch, build the book, edit release ledgers, commit, or push. Their reports live in ignored `build/checks/`.

The build-request and visual-review publishing helpers require a clean, current main before writing. They rerun `make test`, recheck main and the exact allowed files, and commit only their own request or ledger. Keep review records outside the checkout, such as `C:/Heraldry/art-scratch/review.json`. A rejected push preserves the local commit and stops for inspection; no automatic pull, rebase, reset, or force-push occurs.

## Four work tracks

| Track | Authoritative files | Version and review |
|---|---|---|
| Manuscript text | `source/versions.json`, immutable `source/Heraldry_RC###.md`, `editorial/history/RC###.json` | Each approved text-patch batch advances RC by exactly one; retain all earlier snapshots and exact patch evidence |
| Atmospheric artwork | `production/art/ART_MANIFEST.json`, `assets/art/incoming/` | Git commits and asset manifest; no manuscript bump; review the art itself now, and fit and repagination at the next requested build |
| Rules figures | `figures/src/`, `figures/out/`, manifests, `config/figure_dependencies.json` | Git commits; semantic review bound to SVG, caption and dependent rule sections; no manuscript bump unless rules prose changes |
| Layout and publishing | `typst/`, `config/design_tokens.json`, `tools/`, `editorial/how_to_use.json` | Git commits; PDF/visual QA at the next requested build; no manuscript bump |

Use descriptive commits such as `text(RC486): clarify ...`, `art: add ...`, `figures: correct ...`, or `layout: repair ...`. A coordinated change may touch several tracks; record each impact in the state/ledger. Generated PDFs are named from the current registry, never from a hard-coded version.

## Manuscript changes

For a complete updated Markdown manuscript, use the reviewed import path in [MANUSCRIPT_UPDATES.md](MANUSCRIPT_UPDATES.md): `python tools/dev.py manuscript prepare --input <file.md>`, inspect its exact diff/candidate and impact report, then run its explicit `apply --approve` command with the actual owner authorization. Preparation changes no active manuscript or production evidence. Approval calls the same revision engine described below, checks the exact candidate hash and current base, and creates one next RC. No PDF build, commit, or push occurs automatically.

RC485 contains the seven previously authorized clarifications P-01–P-07, promoted from the former RC484 publication patch layer. RC484 remains byte-for-byte the supplied original. The published version now accurately identifies the interactive manuscript snapshot.

One revision represents one approved, committed batch. Several related replacements approved together can share a revision; a subsequent text-patch batch always increments again. Whitespace, wording, values, table cells and rules edits all count as manuscript text changes. Artwork or a changed page count alone does not. Do not overwrite RC485 to prepare RC486, or make changes only in generated Typst/PDF text.

1. Read the active snapshot named in `source/versions.json` and propose exact replacements. Obtain a decision for substantive ambiguities unless the current user instruction already authorizes the specific change. Do not invent an authorization.
2. Put a JSON patch batch in `editorial/proposals/` with an ID, `status: "approved"`, exact `find`, exact `replace`, and `expected_count` for each replacement. `applied` is accepted solely for migration of historical approved batches. Draft batches use `proposed` and cannot be promoted.
3. Promote once:

```sh
python3 tools/revise_manuscript.py \
  --patches editorial/proposals/my-change.json \
  --reason 'Concrete description of the edit' \
  --authorization 'Actual owner instruction/date or decision reference'
```

The command verifies every retained snapshot and patch archive, checks exact match counts, rejects empty/no-op/unapproved batches and number reuse, writes the next full Markdown snapshot, archives the batch, and updates the registry and production source/version together. An optional `base_sha256` binds a batch to the active snapshot. It owns the release marker. Promotion uses an exclusive revision lock, staged files, and exact-byte rollback for ordinary write/final-check failures. Publish all four files in one Git commit. A killed process or failed storage can leave a lock and recovery files; inspect/recover that transaction before running again, and never overwrite an existing revision. One orchestrator promotes revisions; workers do not run this command concurrently.

4. Reparse (`make parse`; a full rebuild only when the owner requests a build). Content anchors resolve by section and text prefix; if the target phrase itself changes, explicitly update `config/content_anchors.json` and verify its placement. Add/update `config/figure_dependencies.json` when a diagram's evidence changes. A changed dependent section invalidates that figure's semantic review; unaffected reviews can remain valid.
5. Run tests. Release checks, page review and contact-sheet review belong to the next requested build. Update the editorial ledger, note in `production/RELEASE_STATUS.md` that `dist/` predates this revision, then commit and push the revision to main without force. Do not label old PDFs as the new version.

Example patch:

```json
{"patches":[{"id":"P-08","status":"approved","find":"Exact existing text","replace":"Exact approved replacement","expected_count":1}]}
```

`editorial/patches.json` is intentionally empty: hidden build-only text patches are prohibited. To revert a rules change, create the next revision containing its inverse patch; never decrement the number or alter history. To fix a metadata/review error without changing the manuscript, make a normal Git commit with no RC bump.

## Build and evidence

The optional InDesign route is separate: [INDESIGN_EXPORT.md](INDESIGN_EXPORT.md). Only an explicit `python tools/dev.py indesign export|compose` invocation or the manual `Export editable InDesign project` workflow starts it. It exports current immutable source into a new editable project; normal checks, manuscript updates, artwork intake, and PDF builds never invoke it. IDML structural checks, actual InDesign composition, visual review, and physical proof are distinct evidence. A native layout edit does not update the canonical manuscript.

**Build on request only** (owner decision 2026-10-11). A change does not trigger a new layout or PDF. Commit it with `make test` and its own track's checks: revision tool, art intake and approval, figure semantic review, skill and package tests. The PDFs in `dist/`, `production/qa/` and the visual ledger stay bound to the last requested build. Reports and `production/RELEASE_STATUS.md` must say when the source has moved past that build, and must never present those PDFs as current. The candidate starts from an owner-requested `production/build-request.json` push; `Rebuild verified delivery` follows a bound visual-review push or an owner-requested manual dispatch. Work in the book's own build pipeline, such as typst, layout or pagination repairs, may build and inspect locally while doing that requested work; the standard Codex route uses GitHub.

When the owner asks for a build, a new PDF or a layout pass: run `make test`, then `make clean all verify package`. A new PDF deliberately fails the visual-review currency gate until the actual page inspection is recorded; inspect it, update the ledger, then run `make verify package` again. `make all` builds and exports the six current PDFs; verification uses fresh reports, isolated Typst queries and a fingerprint of source, fonts, code, templates and assets. `make package` requires matching passing checks and creates the specimen from the current table page map before packing.

`production/build-provenance.json` and `production/qa/STATUS.json` bind files and checks to the current inputs. `production/qa/visual-review.json` separately records the actual inspected PDF hash, exact page coverage, detail pages, observations and limits. Do not carry its PASS to a different PDF. `production/RELEASE_STATUS.md` must qualify missing artwork, unresolved rules questions and physical proof. Never infer semantic correctness from merely matching a hash.

Release ZIPs include all instructions, agents, reference metadata, source snapshots, tools, fonts/licences, figures, PDFs and evidence needed for a new clean build (art as ink derivatives plus the twelve atmospheric masters; generated native images stay in Git LFS). Archive checksums are unique and verified; `package-audit.json` stays outside its own ZIP to avoid a circular checksum. Each requested build is published as a GitHub Release by the `Rebuild verified delivery` workflow; `dist/` holds the local build and its small ledgers, and its PDFs and ZIPs are never committed (`docs/LARGE_FILES.md`). PDFs from before that policy remain recoverable from Git history. Keep secrets, caches and review renders out of Git and packages. The owner-authorized sample PDFs are the exception for Git storage: track them with LFS under references/private/pdfs, follow references/README.md, and keep their bytes out of every publication package.
