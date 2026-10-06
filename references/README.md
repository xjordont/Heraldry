# Owner-selected visual reference PDFs

The active reference set is exactly the ten books named by the owner on 2026-10-06. It replaces the mistakenly uploaded 22-book set. Do not add other books without an owner instruction.

Original PDFs live under `references/private/pdfs/` through Git LFS. [sample_pdfs.json](sample_pdfs.json) lists exact editions, filenames, byte counts and SHA256 hashes. Its status distinguishes a pending correction from completed storage verification. All ten files match the earlier inspection records.

## Claude usage

Read the repository design and art guides first. Then inspect selected reference pages relevant to the task: hierarchy and typesetting, text flow, table design, restrained ink illustration, negative space, scenario deployment maps, legends or navigation. The books inform visual decisions; the active Heraldry manuscript remains the sole authority for rules and lore.

Install/enable Git LFS and fetch only relevant books, for example:

```sh
git lfs install --local
git lfs pull --include="references/private/pdfs/Deth-Wizards-2024.pdf,references/private/pdfs/Mythras-Classic-Fantasy-Imperative.pdf,references/private/pdfs/BlackDeathCity-Playtest-101.pdf"
```

Fetch the full selected set with `git lfs pull --include="references/private/pdfs/*.pdf"` if necessary. Small text pointers are not PDFs; check retrieval and hashes before inspecting pages. If LFS retrieval fails, report the specific problem and continue with the distilled guides.

[reference_manifest.json](reference_manifest.json) contains edition-specific selected viewer pages for these ten books. Render a limited selection with `python3 tools/render_reference_pages.py --source-root references/private/pdfs`; use `--ids` for a particular problem and `--all` only when needed. Match hashes before reusing page numbers. Inspect pages as images and record actual observations; file availability alone does not imply a fresh visual review.

Adapt the references to Heraldry's clean dark fantasy identity, pale cream/white background and portrait borderless US Letter inkjet output. Keep readable type, disciplined spacing, restrained ornament, coherent ink artwork and clear diagram geometry. Do not copy reference artwork, typography assets, prose or mechanics into Heraldry.

## The ten intended books

| Reference | File |
|---|---|
| TNA Ultimate | [PDF](private/pdfs/TNA-Ultimate-Rulebook.pdf) |
| Five Leagues from the Borderlands — Core Rules, Third Edition | [PDF](private/pdfs/FLftB-Core-Rules-3rd-Edition.pdf) |
| Deth Wizards | [PDF](private/pdfs/Deth-Wizards-2024.pdf) |
| Mythras — Classic Fantasy Imperative | [PDF](private/pdfs/Mythras-Classic-Fantasy-Imperative.pdf) |
| The Village Hunt — Veil Hollow | [PDF](private/pdfs/The-Village-Hunt-Veil-Hollow.pdf) |
| Dread Nights | [PDF](private/pdfs/DREAD-NIGHTS-11-singles.pdf) |
| Hellcrawl | [PDF](private/pdfs/Hellcrawl-2026-09-13.pdf) |
| The Elder Scrolls — Call to Arms Core Rules | [PDF](private/pdfs/TES-CTA-Core-Rulebook-DIGITAL-v001sk.pdf) |
| Hametsu — Second Printing | [PDF](private/pdfs/Hametsu-Second-Printing.pdf) |
| BlackDeathCity — Playtest 101 | [PDF](private/pdfs/BlackDeathCity-Playtest-101.pdf) |

## Publication boundary

The full reference PDFs and reference-page renders remain excluded from Heraldry's published PDFs, specimen and release ZIP. Only owner-selected originals are tracked through LFS; rendered pages remain local. Preserve private repository visibility. This reference correction does not change the manuscript RC number.

The transfer status and exact-file verification are recorded in the catalog. Temporary import tooling is retired after the corrected originals are verified and committed.
