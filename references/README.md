# Owner-selected visual reference PDFs

The active reference set is exactly the ten books named by the owner on 2026-10-06. It replaces the mistakenly uploaded 22-book set. Do not add other books without an owner instruction.

The PDFs are the owner's own copies and are **not in this repository**: keep them in `references/private/pdfs/`, which Git ignores, on the machine where you need them (ask the owner for a copy). They were purged from Git history on 2026-11-02 when the repository became public. [sample_pdfs.json](sample_pdfs.json) lists exact editions, filenames, byte counts, and the first 16 hex characters of each SHA-256 (`sha256_prefix`); full hashes are not published.

## Claude usage

Read the repository design and art guides first. Then inspect selected reference pages relevant to the task: hierarchy and typesetting, text flow, table design, restrained ink illustration, negative space, scenario deployment maps, legends or navigation. The books inform visual decisions; the active Heraldry manuscript remains the sole authority for rules and lore.

If the books are not in `references/private/pdfs/` on this machine, say so and continue with the distilled guides (`docs/REFERENCE_ANALYSIS.md`); never commit them. Check a local copy against `sha256_prefix` before reusing page numbers.

[reference_manifest.json](reference_manifest.json) contains edition-specific selected viewer pages for these ten books. Render a limited selection with `python3 tools/render_reference_pages.py --source-root references/private/pdfs`; use `--ids` for a particular problem and `--all` only when needed. The renderer matches local files by `sha256_prefix`. Inspect pages as images and record actual observations; file availability alone does not imply a fresh visual review.

Adapt the references to Heraldry's clean dark fantasy identity, pale cream/white background and portrait borderless US Letter inkjet output. Keep readable type, disciplined spacing, restrained ornament, coherent ink artwork and clear diagram geometry. Do not copy reference artwork, typography assets, prose or mechanics into Heraldry.

## The ten intended books

| Reference | File |
|---|---|
| TNA Ultimate | `TNA-Ultimate-Rulebook.pdf` |
| Five Leagues from the Borderlands — Core Rules, Third Edition | `FLftB-Core-Rules-3rd-Edition.pdf` |
| Deth Wizards | `Deth-Wizards-2024.pdf` |
| Mythras — Classic Fantasy Imperative | `Mythras-Classic-Fantasy-Imperative.pdf` |
| The Village Hunt — Veil Hollow | `The-Village-Hunt-Veil-Hollow.pdf` |
| Dread Nights | `DREAD-NIGHTS-11-singles.pdf` |
| Hellcrawl | `Hellcrawl-2026-09-13.pdf` |
| The Elder Scrolls — Call to Arms Core Rules | `TES-CTA-Core-Rulebook-DIGITAL-v001sk.pdf` |
| Hametsu — Second Printing | `Hametsu-Second-Printing.pdf` |
| BlackDeathCity — Playtest 101 | `BlackDeathCity-Playtest-101.pdf` |

## Publication boundary

The full reference PDFs and reference-page renders remain excluded from Heraldry's published PDFs, specimen and release ZIP. Neither the originals nor rendered pages are ever committed; `tests/test_repository_hygiene.py` fails CI on any tracked PDF. This reference correction does not change the manuscript RC number.

All ten originals were verified by SHA-256 and byte count on 2026-10-06. They, and an earlier mistaken set, were stored through Git LFS until 2026-11-02, when they were purged from history.


The latest actual-page observations are in `docs/REFERENCE_ANALYSIS.md`; the owner's requested design and pagination iteration is `docs/DESIGN_REFINEMENT.md`. The older larger reference analysis has been replaced. These documents are a production handoff, not a claim that the current PDFs have already been redesigned.
