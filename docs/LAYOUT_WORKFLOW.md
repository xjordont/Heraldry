# Repeatable layout workflow

Use this workflow for an owner-requested layout pass. The local runner never publishes or edits release ledgers.

## Entry points

Run these commands from the repository root with the project's Python environment:

```text
python tools/dev.py layout plan
python tools/dev.py layout check
python tools/dev.py layout run
```

`plan` reads the active manuscript and prints the stages without generating PDFs. `check` runs dependency and baseline checks plus focused regression tests, including small compiler fixtures. `run` prepares the current manuscript, composes the interior, runs core gates, then compiles the digital PDF (with its covers) and makes review images only after those gates pass. Run focused tests while editing; CI runs the full suite when you push.

Each check/run writes commands, durations, logs, report hashes, and status to `build/checks/layout-runs/<run>/run.json`. A successful full local run ends at `LOCAL_QA_PASS_REVIEW_REQUIRED`: look at the review images, both covers, and any suspect pages before calling the layout done. The archived digital PDF is the one the review images were made from.

Do not run concurrent composition commands in the shared checkout. The runner holds `build/layout-workflow.lock`; after an interrupted process, inspect its receipt and confirm no process is running before removing a stale lock. Do not clean away proof evidence during iteration.

## Measurement cache

Verified unit measurements live in ignored `.cache/layout-measurements/`, outside `build/`, so `make clean` preserves them. The key includes the exact measurement source, full publication input identity, compiler identity, fonts, and compilation options. A hit requires matching evidence and the exact PDF hash, then extracts and validates the measurement rows from that PDF again. Corruption is a cache miss; warning-bearing exports are not stored. Input changes during measurement fail the run.

An updated manuscript or other bound input requires fresh measurements. There is no approximate per-unit height reuse across edited manuscripts. GitHub candidate and delivery jobs restore the same cache namespace and verify its identity the same way; the cache skips measurement only, never a gate.

Converged column-balancing plans may be restored as starting hints from the same verified measurement entry. Segment signatures bind rendered content and layout settings, rather than only heading IDs and item counts. Every hint is followed by real composition, balancing, and convergence checks. Failed or uncompiled proposals cannot become converged cache entries. For a diagnostic fresh measurement, use `python tools/build_book.py --no-measurement-cache` after normal preparation; this bypasses measurement and persisted hint caches. To ignore local balancing hints as well, add `--no-balance` (this disables balancing, so it is a diagnostic comparison, not the production default).

## Manuscript changes and table widths

Always parse the active RC before composition. The runner verifies the parsed model against the current manuscript and freezes publication inputs after preparation. Changes during composition or validation stop the run. Start a new run after changing any bound input.

Reviewed table-width preferences in `config/design_tokens.json` use normalized complete heading paths and exact plain header cells. They do not use sequential T-numbers. Renumbered sections and inserted tables therefore retain their intended selectors. A changed table is freshly measured and allocated, with changed-content diagnostics. Removed targets produce warnings and remain unapplied; ambiguous or overlapping selectors fail before compilation. Inspect `production/mappings/table_scope_policies.json` and the run's composition diagnostics whenever a manuscript changes.

## Measuring a layout change

`python tools/layout_flow.py BASE.pdf TRIAL.pdf` compares two digital PDFs; use the last release as BASE. It reports the page count and chapter spans, low right-column section starts, uneven chapter ends, rules through text, and every column foot left more than 60 pt short. It classifies each short column by what tops the next column, read from the positions the build embeds:

- **section end:** a numbered section starts there (the fresh-page rule);
- **keep gap:** a heading, figure, table, or flow piece was carried there whole;
- **interior void:** nothing; the text simply continues. These need repair (DESIGN 8.5).

`layout_qa` (run by verify) carries the same measures in `production/qa/layout.json` as advisory notes, and fails the gate on a composition hairline drawn through text.

Trial a layout idea in a scratch clone, one change at a time, as a full local proof:

1. Compare it with `layout_flow.py`.
2. Look at every page that changed.
3. Keep it only if the book reads better, no page is added without reason, and no type falls below the 9 pt essential minimum.

A full book compile peaks at about 7.5 GB, so run one build at a time on a 15 GB machine.

## Lessons retained from the rulebook-layout review (2026-11-06)

Every part of the rulebook-layout skill was trialled against RC528-build-44 (owner request).

**Adopted:**
- the column-flow report and the rule-through-text gate;
- figure fit: a full-width figure carried to the next page is scaled to close the page above it, but only as far as its labels stay at 9 pt (about 96%; the skill's 80% would set them at 7.9 pt);
- card tables keep their first two and last two entries together;
- a Contents page-number gutter, so a long title wraps short of its number;
- index filing that ignores a leading "The";
- index letter heads keep two entries.

**Rejected:**
- **Reusing approved art in short columns.** It cleared space, but every piece appeared twice, most under unrelated content (weapons under Potions, armour under Poisons), and art at a column foot decorates a void rather than closing it. Purpose-made gap art, commissioned through the owner's art workflow, is the route if gaps are to carry art.
- **Moving a figure within its section.** The composer's column bands would need redesigning, and reading order would change.
- **The low right-column start rule.** It has one real case, and moving it only trades a low start for a bare column foot.

**Confirmed already in place:** a readable measure (a median of 49 characters a line in two columns); tables whose rows never split and whose headers repeat; split example panels that keep their tint and rule; two editions that paginate identically; and no painting repeated on a spread.

**Pending the owner:** one continuous flow per chapter (sections run on, in-column heads, only the chapter's last page balanced). It cut Combat from 21 pages to 14 and its bare column space by 86%. It reverses the fresh-page rule, D-01, and 12a, and drops most section tailpieces. It is being trialled on two more chapters before the owner decides.

## Lessons retained from the compact-layout pass

Keep the approved 10.5 pt body, 9 pt tables, narrow margins, two-column rules, and full-width introduction flavour in the shared layout profile. Improve components and flow rather than repeatedly shrinking text. Preserve source coverage, substantive heading keeps, fit-capable keep units, continuation identities, and rendered page evidence. Cosmetic whitespace alone does not justify violating those constraints.

Use focused fixtures while editing, then freeze inputs and run the complete checks once. Stop a failed interior proof before paying for the digital PDF or all-page images. Use recorded timings to identify the next bottleneck instead of repeating expensive probes blindly.

Published delivery follows [BUILD_AUTOMATION.md](BUILD_AUTOMATION.md).
