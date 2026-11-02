# Updating the manuscript

Give Codex the complete updated UTF-8 Markdown file and say: "Prepare this manuscript update for review." After reviewing the exact changes, approve that batch. Codex uses the same commands below. No manuscript prose is generated during import.

The active version is always the last record in `source/versions.json`. Each approved update creates exactly one new RC, preserves every previous snapshot, and archives the exact replacements and owner authorization. A manuscript update does not request a PDF build.

## 1. Supply the updated file

Start from the active `source/Heraldry_RC###.md`. Save your edited copy outside `source/`, such as `C:/Heraldry/art-scratch/updated-manuscript.md`. Keep the existing Markdown headings, tables, and the single `**Release Candidate N (RCN)**` line. The importer keeps the upload's own RC number: any number higher than the active RC is accepted (jumps included; skipped numbers create no snapshots), while the current or an older number, duplicate markers, or inconsistent numbers are refused. The optional legacy `--target-rc N` may only restate the number printed in the upload. Exact-patch batches use the next number.

Use UTF-8 `.md` or `.markdown`. Export Word or other editor formats to Markdown first and inspect the export. Word/PDF conversion and rules rewriting are outside this import command. A UTF-8 BOM and Windows line endings are accepted: the review records BOM removal and conversion to LF. Every other character, including the final newline, is preserved exactly apart from the managed RC marker. A marker-only or unchanged submission creates no revision.

Sync a clean `main` with `git pull --ff-only origin main`. Run commands from the repository root. The developer entry point selects the installed project Python environment; no additional packages are required.

## 2. Prepare and inspect

```sh
python tools/dev.py manuscript prepare --input "C:/Heraldry/art-scratch/updated-manuscript.md"
```

The command prints a review directory under ignored `build/manuscript-updates/`. Its name includes the target RC and hashes of the input/configuration. Use `--review-dir "C:/Heraldry/art-scratch/my-review"` to keep a review outside build caches. An existing review directory is never overwritten; use a new directory when preparing again.

| File | What to review |
|---|---|
| `REVIEW.md` | Change counts, normalisations, affected figures, blocking findings, and the exact approval command |
| `changes.diff` | Every text edit, including the managed RC marker |
| `candidate.md` | The exact prospective snapshot |
| `summary.json` | Base/input/candidate hashes, binding configuration hashes, anchor results, and figure impacts |
| `incoming.md` | Your unmodified input bytes |
| `proposed-patches.json` | Deterministic exact replacements; still unapproved |

Preparation validates the manuscript history, parses the proposed Markdown in memory, resolves each content anchor, and compares diagram dependencies against the changed sections. It changes nothing in the repository. The parser confirms supported constructs; it does not judge whether a rules change is correct.

A `BLOCKED` report is saved and the command exits unsuccessfully. Repair unsupported Markdown in your input, or explicitly update a broken anchor/figure dependency in `config/content_anchors.json` or `config/figure_dependencies.json`, then prepare a new review. Commit those two companion files with the revision. Changed rule sections list the figures to re-check before the next build; source-line shifts can also move figure citations, which are never remapped automatically.

## 3. Approve and apply once

Read the diff and candidate, settle any material rules ambiguity with the owner, and approve. Copy the command from `REVIEW.md`, filling in the reason and the owner's authorization. For example:

```sh
python tools/dev.py manuscript apply --review-dir "PATH-PRINTED-BY-PREPARE" --approve --reason "Describe the supplied update" --authorization "Actual owner instruction/date or decision reference"
```

The CLI requires `main` equal to freshly fetched `origin/main` and a clean tree apart from the two companion files, and rechecks the review bundle, base, and configuration; if any changed, prepare again. `--approve` records the acceptance.

The command calls `tools/revise_manuscript.py` and writes these four files as one checked transaction:

- `source/Heraldry_RC<N>.md`: the reviewed immutable snapshot, equal to the reviewed candidate hash.
- `editorial/history/RC<N>.json`: exact approved patches, input/candidate hashes, and normalisation record.
- `source/versions.json`: the appended revision, parent hash, reason, and authorization.
- `config/production.json`: the active source and publication version.

Earlier snapshots and archived patches remain byte-for-byte unchanged. Reapplying the same review refuses. The command does not commit, push, or build.

## 4. Commit the revision

The apply step validates the revision itself; CI runs the full test suite after you push. Add a short `production/STATE.md` entry and note in `production/RELEASE_STATUS.md` that the last PDF release predates the new RC. Commit the four revision files with those notes and any companion changes in one commit, and push to `main`.

If a publishing build is running, wait for it to finish before pushing. If a push is rejected, keep the local work and reconcile it; don't apply the batch again. To revert an approved text change, create a later revision with its inverse.

A manuscript update never starts a build; only an owner request starts [BUILD_AUTOMATION.md](BUILD_AUTOMATION.md).

## Small exact edits and recovery

The existing `tools/revise_manuscript.py --patches ... --reason ... --authorization ...` route remains available for approved exact patch batches; see [WORKFLOW.md](WORKFLOW.md). A batch can include `base_sha256` to refuse application to a different active snapshot. Full-file import is a convenience layer over this same revision engine.

Promotion holds an exclusive `source/.revision.lock`, stages its four files, and rolls back ordinary failures to the exact earlier bytes; it never overwrites an existing snapshot or archive. A killed process can still leave a lock and adjacent `.tmp` recovery files: inspect which files were written and restore a consistent set before retrying. Never change snapshot hashes by hand to silence a failure.
