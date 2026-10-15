# Building Heraldry Skirmish

Pipeline: active immutable Markdown snapshot → markdown-it-py semantic model → custom Typst components → searchable PDF. The active source and RC number come from `source/versions.json`; production configuration and snapshot hashes must agree. No LLM regenerates source prose or tables. PDF timestamps are pinned to the manuscript revision creation time so repeated builds can produce identical PDF bytes.

## Requirements

Python 3.12+ (tested here with 3.12.14; prior build used 3.13.16), pinned dependencies in `requirements.lock`, bundled OFL fonts. Use a virtual environment if required by your Python installation. System fonts are excluded. `make fonts` optionally regenerates the bundled static instances from the supplied variable fonts; ordinary builds use the already bundled static fonts.

The lock also includes NumPy and `potracer` (imported as `potrace`) for `tools/prepare_cover.py` and `tools/prepare_marks.py`. Ordinary publication builds use the prepared cover and SVG marks; installing the lock supports both publishing and these authoring tools. The pinned Python `typst` package supplies the compiler, so a standalone Typst CLI is unnecessary. Pandoc, Poppler, qpdf, and Ghostscript are optional diagnostics, not requirements of the current pipeline.

GitHub candidate and delivery jobs install this lock on their Ubuntu runner. They also use Git, Git LFS, GNU Make, Bash/core utilities, and GitHub CLI `gh`. The Windows orchestrator uses its existing Git login and Git LFS; it does not require a local GitHub CLI.

```sh
python3 -m pip install -r requirements.lock
make test
make clean all verify package
```

For the owner's Windows checkout, use the dedicated Python environment rather than the unrelated system Python or Windows `python3` alias:

```powershell
$env:PYTHONUTF8 = '1'
$heraldryPython = 'C:/Heraldry/art-venv/Scripts/python.exe'
& $heraldryPython -m pip install -r requirements.lock
& $heraldryPython -m pip check
& $heraldryPython tools/preflight.py --baseline
& C:/Heraldry/tools/gnuwin32/bin/make.exe test "PY=$heraldryPython"
```

These commands install and verify dependencies and run tests. A publication build still requires an owner request; use `docs/BUILD_AUTOMATION.md` for the GitHub build/review/release chain.

`make all` preflights, parses, indexes, builds covers/calibration, generates figures, balances the cream interior, compiles white/digital variants and exports the six current PDFs with input/PDF provenance. All targets run sequentially to avoid multiple writers and excess compiler memory. `make figures` first parses; it works from a clean checkout. `make verify` requires a current exported build and fails on crashes, missing reports, stale inputs or mandatory defects. New PDF bytes require a fresh visual review ledger before the currency gate passes; render and inspect, record coverage, then run `make verify package`. `make specimen` verifies first and uses the fresh table page map. `make package` verifies, creates the specimen and audits/checksums the archive.

## Outputs

Replace `RC###` with the active version; filenames are generated automatically.

| File in dist/ | Purpose |
|---|---|
| Heraldry_RC###_digital.pdf | Digital reading edition with covers, links and bookmarks |
| Heraldry_RC###_inkjet-borderless.pdf | Cream portrait Letter interior |
| Heraldry_RC###_inkjet-borderless-white.pdf | White interior with matching pagination |
| Heraldry_RC###_covers-front-back.pdf and -white.pdf | Separate front/back cover sheets |
| Heraldry_RC###_inkjet-calibration.pdf | Diagnostic test sheet |
| PRINT_INSTRUCTIONS.md | Device-aware printing instructions |
| specimen/Heraldry_RC###_specimen.pdf | Production sample extracted from the verified interior |
| Heraldry_RC###_release.zip, SHA256SUMS.txt | Rebuildable delivery archive and checksums |

These are build outputs and are gitignored. The `Rebuild verified delivery` workflow publishes them as a GitHub Release and commits `dist/RELEASE.json` (tag, URL and SHA-256 of each file) with the ledgers. See `docs/LARGE_FILES.md`.

## Iterations and review

Use [WORKFLOW.md](docs/WORKFLOW.md) for source changes and main commits. `make test` protects revision sequencing, snapshot immutability, patch authorization/matches, figure dependency currency and failure gates. GitHub Actions runs these inexpensive repository checks on main pushes, pull requests and manual dispatches; the verified-delivery workflow also rebuilds full PDFs when build provenance or the visual ledger changes, or on manual dispatch. It uses locked dependencies and the committed review ledger, retains a downloadable artifact, and commits only generated delivery/evidence to main with a normal fast-forward push. It never performs or invents visual review: new PDF bytes must already have an actual review ledger. If main advances, it retains the artifact and fails instead of pushing stale work. Visual inspection runs in the publishing environment.

Approved original artwork is named by `production/art/ART_MANIFEST.json`. Place masters in `assets/art/incoming/` and rebuild. Changed figure SVGs/captions or dependent rules sections invalidate their semantic review. Changed PDFs require current visual evidence; a passing automated gate does not certify physical printing or every rule's semantic consistency.

The release ZIP contains instructions, agent configuration and reference metadata required by preflight, plus editable sources, fonts/licences, figures, PDFs and evidence. The ZIP's own audit remains external to avoid circular self-checksums. Prior RC snapshots stay in source/ and prior releases remain in Git history.
