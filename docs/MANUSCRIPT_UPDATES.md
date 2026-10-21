# Updating the manuscript

Give Codex the complete updated UTF-8 Markdown file and say: "Prepare this manuscript update for review." After reviewing the exact changes, approve that batch. Codex uses the same commands below. No manuscript prose is generated during import.

The active version is always the last record in `source/versions.json`. Each approved update creates exactly one new RC, preserves every previous snapshot, and archives the exact replacements and owner authorization. A manuscript update does not request a PDF build.

## 1. Supply the updated file

Start from the active `source/Heraldry_RC###.md`. Save your edited copy outside `source/`, such as `C:/Heraldry/art-scratch/updated-manuscript.md`. Keep the existing Markdown headings, tables, and the single `**Release Candidate N (RCN)**` line. The importer keeps the uploaded manuscript's own RC number exactly. Any number higher than the active RC is accepted for review, including jumps; no extra flag or separate version-jump approval is required. A changed upload with the current or an older number is refused, never renumbered or overwritten. Duplicate markers and inconsistent numbers are refused. The selected jump target is bound into the review and archived import evidence. The optional legacy `--target-rc N` may only assert the number already printed in the upload; it cannot change that number. Skipped numbers create no snapshots. Exact-patch batches still use the next number. The exact-content review and approval steps below remain required.

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

Preparation validates the retained manuscript history, parses the proposed Markdown in memory, resolves each content anchor, and compares diagram dependencies against the changed sections. It does not write parser inventories, generate figures or PDFs, alter the active registry, or change release/review ledgers. The parser check confirms supported constructs; it does not decide whether a rules change is correct.

A `BLOCKED` report is saved and the command exits unsuccessfully. Repair unsupported Markdown in your input, or explicitly update a broken anchor/figure dependency in `config/content_anchors.json` or `config/figure_dependencies.json`, then prepare a new review. These two companion files may remain modified for approval and must be reviewed and committed with the revision. Do not edit the bundle or stamp a review hash to bypass a finding. Changed rule sections identify figures needing actual semantic review before the next release. Source-line shifts also require inspecting figure citations before regenerating figures; numeric citations are never automatically remapped.

## 3. Approve and apply once

Read the diff and candidate, resolve material rules ambiguities, and approve the actual content. Copy the command from `REVIEW.md`, replacing the reason and authorization with the actual owner decision. For example:

```sh
python tools/dev.py manuscript apply --review-dir "PATH-PRINTED-BY-PREPARE" --approve --reason "Describe the supplied update" --authorization "Actual owner instruction/date or decision reference"
```

The CLI requires main equal to freshly fetched origin/main and a clean working tree/index except for the two hash-bound companion configuration files above. It rechecks every review payload, current base, binding configuration, and structural finding. A changed bundle, stale base, or changed binding configuration requires preparing and reviewing again. `--approve` records explicit acceptance; a proposed batch cannot be promoted on its own.

The command calls `tools/revise_manuscript.py` and writes these four files as one checked transaction:

- `source/Heraldry_RC<N>.md`: the reviewed immutable snapshot, equal to the reviewed candidate hash.
- `editorial/history/RC<N>.json`: exact approved patches, input/candidate hashes, and normalisation record.
- `source/versions.json`: the appended revision, parent hash, reason, and authorization.
- `config/production.json`: the active source and publication version.

Earlier snapshots and archived patches remain byte-for-byte unchanged. Reapplying the same review refuses. The command does not commit, push, or build.

## 4. Validate and publish the revision

Run `python tools/dev.py check`. Update `production/STATE.md` with the actual update and `production/RELEASE_STATUS.md` to distinguish the new manuscript from the last requested PDF release. Commit the four revision files together with those notes and any reviewed companion changes, then push main normally after the required `make test`. Check the staged diff before committing. Never force-push or rewrite earlier revisions.

If a publishing build is running, wait for its final result before pushing. If remote main moves or a push is rejected, preserve the local work, inspect the difference, and reconcile without overwriting another revision. Do not apply the batch again to fix a push failure. Revert an approved text change by creating a later revision with its inverse.

Only an explicit build request starts the candidate/review/release process in [BUILD_AUTOMATION.md](BUILD_AUTOMATION.md). Old PDFs and visual/semantic review evidence retain their original hashes. A changed dependent section needs a fresh semantic review; a newly built PDF needs its own actual page review. Physical print remains **NOT TESTED** until sheets are examined.

## Small exact edits and recovery

The existing `tools/revise_manuscript.py --patches ... --reason ... --authorization ...` route remains available for approved exact patch batches; see [WORKFLOW.md](WORKFLOW.md). A batch can include `base_sha256` to refuse application to a different active snapshot. Full-file import is a convenience layer over this same revision engine.

Promotion holds an exclusive `source/.revision.lock`, stages the four payloads and original metadata, and rolls back ordinary write or final-validation failures to the exact earlier bytes. It never overwrites a pre-existing next snapshot or archive. A killed process or storage failure can still interrupt a multi-file transaction: preserve any lock and adjacent `.tmp` recovery files, inspect which files were published, and restore a consistent transaction before retrying. A retained lock deliberately refuses a second promotion. Do not delete recovery evidence or manually change snapshot hashes to silence a failure.
