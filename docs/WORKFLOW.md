# Manuscript and commit workflow

Agent rules and checks are in `AGENTS.md`, layout iteration in [LAYOUT_WORKFLOW.md](LAYOUT_WORKFLOW.md), and builds in [BUILD_AUTOMATION.md](BUILD_AUTOMATION.md).

## Commits

Work on `main`, syncing first with `git pull --ff-only origin main`. Use descriptive messages such as `text(RC528): clarify ...`, `art: add ...`, `figures: correct ...`, or `layout: repair ...`. A change across several tracks notes each in `production/STATE.md`. GitHub refreshes the README's generated blocks after each push ([README_AUTOMATION.md](README_AUTOMATION.md)). Generated PDFs are named from the current registry, never from a hard-coded version.

## Manuscript changes

Every approved text-patch batch creates exactly one new RC snapshot. Whitespace, wording, values, table cells, and rules edits all count as text changes; artwork, figures, layout, tooling, docs, and a changed page count do not. Never edit a snapshot, reuse or decrement a number, hide text patches in the build (`editorial/patches.json` stays empty), or change only generated Typst or PDF text.

**A full owner upload** follows [MANUSCRIPT_UPDATES.md](MANUSCRIPT_UPDATES.md): `python tools/dev.py manuscript prepare --input <file.md>`, review the diff, then apply it with the owner's approval. A higher uploaded RC number is kept automatically.

**Exact patches:**

1. Read the active snapshot named in `source/versions.json` and write exact replacements. Get the owner's decision on substantive changes unless their instruction already covers them.
2. Put a JSON batch in `editorial/proposals/` with an ID, `status: "approved"`, and an exact `find`, `replace`, and `expected_count` for each patch. Drafts use `proposed` and cannot be promoted.

   ```json
   {"patches":[{"id":"P-08","status":"approved","find":"Exact existing text","replace":"Exact approved replacement","expected_count":1}]}
   ```

3. Promote it once:

   ```sh
   python3 tools/revise_manuscript.py \
     --patches editorial/proposals/my-change.json \
     --reason 'Concrete description of the edit' \
     --authorization 'Actual owner instruction and date'
   ```

   The tool checks every retained snapshot and match count, writes the next snapshot, archives the batch, and updates `source/versions.json` and `config/production.json`. Commit the new snapshot, its `editorial/history/` archive, and those two files together. If a run is killed, inspect and recover its lock and recovery files before running it again.
4. Run `make parse`. If a patched phrase is a content anchor, update `config/content_anchors.json`; if a figure's evidence changed, update `config/figure_dependencies.json`, and that figure then needs a fresh look. Note in `production/RELEASE_STATUS.md` that `dist/` predates the new RC, then commit and push.

To revert a text change, create the next RC with the inverse patch. A metadata or review fix that leaves the text alone is a normal commit with no RC bump.
