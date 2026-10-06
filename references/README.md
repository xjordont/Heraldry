# Visual reference PDF library

The owner authorized the 22 supplied sample books for visual inspiration on 2026-10-06. Originals belong in `references/private/pdfs/`, using Git LFS. The exact filenames, byte counts and SHA256 hashes are in [sample_pdfs.json](sample_pdfs.json); its status distinguishes a prepared transfer from a completed, hash-verified upload. Reference availability never blocks the Heraldry build.

## Use in Claude Code

Read `docs/DESIGN_SPEC.md`, `docs/REFERENCE_ANALYSIS.md`, `docs/ART_DIRECTION.md` and `docs/INKJET_PRINT.md` first. Then inspect a small selection relevant to the current design problem: typography and hierarchy, readable rules/table layouts, art integrated with negative space, scenario maps and legends, or navigation/index design. These PDFs are visual references, not Heraldry source manuscripts or original Heraldry assets.

Git LFS pointers are small text files, not readable PDFs. Fetch only the books needed for the current task, for example:

```sh
git lfs install --local
git lfs pull --include="references/private/pdfs/06-FLftB-Core-Rules-3rd-Edition.pdf,references/private/pdfs/14-Hametsu-3-.pdf"
```

To fetch all 22 originals, use `git lfs pull --include="references/private/pdfs/*.pdf"`. This downloads about 887 MiB. Check files against the catalog before choosing pages. If LFS authentication, quota or tool availability blocks retrieval, report the exact limitation and continue with the distilled guides.

The earlier curated `reference_manifest.json` contains edition-specific page selections for nine books; only some are among this 22-book upload. Match the SHA256 hash before reusing page numbers. Other books need fresh page inspection. Do not claim all sample pages were reviewed merely because their files are available.

Inspect representative pages as images at readable scale. Record actual PDF viewer page numbers and concrete observations for useful specimens. Adopt principles such as disciplined spacing, hierarchy, column rhythm, restrained ink drawing, legible table rules and clear deployment geometry. Adapt them to Heraldry's clean dark fantasy identity, light substrate and portrait borderless US Letter inkjet constraints. Do not copy reference artwork, lettering, prose or mechanics into Heraldry.

## Catalog

| ID | Sample | File |
|---|---|---|
| SAMPLE-01 | Frostgrave | [PDF](private/pdfs/01-Frostgrave.pdf) |
| SAMPLE-02 | Nimble — Core Rules | [PDF](private/pdfs/02-Nimble-CoreRules.pdf) |
| SAMPLE-03 | Lasting Tales | [PDF](private/pdfs/03-Lasting-Tales.pdf) |
| SAMPLE-04 | Pathfinder 2e — Player Core Remaster | [PDF](private/pdfs/04-Pathfinder-2e-Player-Core-Remaster.pdf) |
| SAMPLE-05 | Dungeoneers Rulebook — v16 | [PDF](private/pdfs/05-Dungeoneers-Rulebook-v16.pdf) |
| SAMPLE-06 | Five Leagues from the Borderlands — Core Rules, Third Edition | [PDF](private/pdfs/06-FLftB-Core-Rules-3rd-Edition.pdf) |
| SAMPLE-07 | Arena Contest | [PDF](private/pdfs/07-ARENACONTEST-4-.pdf) |
| SAMPLE-08 | ATO — Core Rulebook v1.1 | [PDF](private/pdfs/08-ATO_CORE_Rulebook_v1.1.pdf) |
| SAMPLE-09 | SAS Rulebook | [PDF](private/pdfs/09-SAS-Rulebook-3-.pdf) |
| SAMPLE-10 | Dungeon Universalis Rulebook | [PDF](private/pdfs/10-Rulebook-web-Dungeon-Universalis-2-.pdf) |
| SAMPLE-11 | Middara | [PDF](private/pdfs/11-Middara.pdf) |
| SAMPLE-12 | EAHQ | [PDF](private/pdfs/12-EAHQ.pdf) |
| SAMPLE-13 | Ker Nethalas — Carnage Aether | [PDF](private/pdfs/13-Ker-Nethalas-Carnage-Aether-3-.pdf) |
| SAMPLE-14 | Hametsu | [PDF](private/pdfs/14-Hametsu-3-.pdf) |
| SAMPLE-15 | The Walking Dead — All Out War | [PDF](private/pdfs/15-The-Walking-Dead-All-Out-War.pdf) |
| SAMPLE-16 | XCOM — The Miniatures Game Core Rules | [PDF](private/pdfs/16-XCOM-The-Miniatures-Game-Core-Rules-digital.pdf) |
| SAMPLE-17 | The Village Hunt — Veil Hollow | [PDF](private/pdfs/17-The-Village-Hunt-Veil-Hollow.pdf) |
| SAMPLE-18 | Relicblade — The Seekers Handbook, Second Edition | [PDF](private/pdfs/18-Relicblade-The-Seekers-Handbook-2nd-Edition.pdf) |
| SAMPLE-19 | Call of Dungeons | [PDF](private/pdfs/19-Call-of-Dungeons.pdf) |
| SAMPLE-20 | GoN — Dux Disciplinam | [PDF](private/pdfs/20-FINAL-GoN-Dux-Disciplinam.pdf) |
| SAMPLE-21 | GoN — Tome of Knowledge | [PDF](private/pdfs/21-FINAL-GoN-Tome-of-Knowledge.pdf) |
| SAMPLE-22 | GoN — Scenario Book | [PDF](private/pdfs/22-FINAL-GoN-Scenario-Book.pdf) |

## Publication boundary

`references/private/` remains excluded from publication ZIPs and local render caches remain ignored. The original PDFs are explicitly tracked through LFS despite this directory's default ignore rule. Never include reference PDF bytes or reference page images in the Heraldry digital/print PDFs, specimen or release archive. Preserve the repository's private visibility.

All 22 original PDFs were uploaded and downloaded back from GitHub LFS on 2026-10-06. Every file's SHA256 and byte count matched the supplied original before its pointer was committed to main. The successful one-time import workflow and helper remain recoverable in Git history; they have been removed from the active project. No repository credentials or temporary upload URLs were committed.
