# Iteration workflow

`main` is the single working and delivery branch. The owner has authorized ordinary verified iterations on main. Create another branch only following an explicit owner decision with a recorded purpose; one project does not require a branch per component. The existing Claude build branch is an archived checkpoint, not a destination for new work.

Before editing, inspect `git status`, the current branch, and the remote main head. Bring an untouched checkout up to date with `git fetch origin` and `git switch main`, then `git pull --ff-only`. Preserve unrelated local work and inspect divergence rather than force-pushing or resetting it. Claude cloud may impose its own branch restrictions; report an actual restriction if encountered. Do not invent an exception to this policy or change account settings.

## Four work tracks

| Track | Authoritative files | Version and review |
|---|---|---|
| Manuscript text | `source/versions.json`, immutable `source/Heraldry_RC###.md`, `editorial/history/RC###.json` | Each approved text-patch batch advances RC by exactly one; retain all earlier snapshots and exact patch evidence |
| Atmospheric artwork | `production/art/ART_MANIFEST.json`, `assets/art/incoming/` | Git commits and asset manifest; no manuscript bump; review fit, ink coverage, resolution and repagination |
| Rules figures | `figures/src/`, `figures/out/`, manifests, `config/figure_dependencies.json` | Git commits; semantic review bound to SVG, caption and dependent rule sections; no manuscript bump unless rules prose changes |
| Layout and publishing | `typst/`, `config/design_tokens.json`, `tools/`, `editorial/how_to_use.json` | Git commits; rebuild and PDF/visual QA; no manuscript bump |

Use descriptive commits such as `text(RC486): clarify ...`, `art: add ...`, `figures: correct ...`, or `layout: repair ...`. A coordinated change may touch several tracks; record each impact in the state/ledger. Generated PDFs are named from the current registry, never from a hard-coded version.

## Manuscript changes

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

The command verifies every retained snapshot and patch archive, checks exact match counts, rejects empty/no-op/unapproved batches and number reuse, writes the next full Markdown snapshot, archives the batch, and updates the registry and production source/version together. It owns the release marker. Publish all these files in one Git commit. If an interrupted command leaves partial files, inspect/recover that transaction before running again; never overwrite an existing revision. One orchestrator promotes revisions; workers do not run this command concurrently.

4. Reparse and rebuild. Content anchors resolve by section and text prefix; if the target phrase itself changes, explicitly update `config/content_anchors.json` and verify its placement. Add/update `config/figure_dependencies.json` when a diagram's evidence changes. A changed dependent section invalidates that figure's semantic review; unaffected reviews can remain valid.
5. Run tests, all release checks, affected detailed page review and full-page contact-sheet review if pagination changes. Update editorial and release ledgers, then commit and push the revision to main without force. Do not label old PDFs as the new version.

Example patch:

```json
{"patches":[{"id":"P-08","status":"approved","find":"Exact existing text","replace":"Exact approved replacement","expected_count":1}]}
```

`editorial/patches.json` is intentionally empty: hidden build-only text patches are prohibited. To revert a rules change, create the next revision containing its inverse patch; never decrement the number or alter history. To fix a metadata/review error without changing the manuscript, make a normal Git commit with no RC bump.

## Build and evidence

Run `make test`, then `make clean all verify package`. A new PDF deliberately fails the visual-review currency gate until the actual page inspection is recorded; inspect it, update the ledger, then run `make verify package` again. `make all` builds and exports the six current PDFs; verification uses fresh reports, isolated Typst queries and a fingerprint of source, fonts, code, templates and assets. `make package` requires matching passing checks and creates the specimen from the current table page map before packing.

`production/build-provenance.json` and `production/qa/STATUS.json` bind files and checks to the current inputs. `production/qa/visual-review.json` separately records the actual inspected PDF hash, exact page coverage, detail pages, observations and limits. Do not carry its PASS to a different PDF. `production/RELEASE_STATUS.md` must qualify missing artwork, unresolved rules questions and physical proof. Never infer semantic correctness from merely matching a hash.

Release ZIPs include all instructions, agents, reference metadata, source snapshots, tools, fonts/licences, figures, PDFs and evidence needed for a new clean build. Archive checksums are unique and verified; `package-audit.json` stays outside its own ZIP to avoid a circular checksum. `dist/` is the current delivery set; historical PDFs remain recoverable from Git history. Keep secrets, commercial reference PDFs, caches and review renders out of Git and packages.
