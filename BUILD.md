# Building Heraldry Skirmish

Pipeline: the active immutable Markdown snapshot, a markdown-it-py semantic model, custom Typst components, and a searchable PDF. `source/versions.json` names the active source and RC; `config/production.json` and the snapshot hashes must agree. No LLM regenerates source prose or tables. PDF timestamps are pinned to the manuscript revision's creation time, so repeated builds can produce identical PDF bytes.

## Toolchain

- Python 3.12 or later with the pinned packages in `requirements.lock` (`make deps`; use a virtual environment if your Python requires one). The pinned `typst` package supplies the compiler, so no separate Typst CLI is needed.
- The bundled OFL fonts in `fonts/`, with their licences in `fonts/licences/`. System fonts are never used. `make fonts` regenerates the static instances from the variable fonts; ordinary builds don't need it.
- GNU Make, Git, and Git LFS. The art the book places is in LFS; fetch it with `git lfs pull` before building.
- For the Hero records only: Playwright 1.63.0 and its Chromium (`python3 -m pip install playwright==1.63.0`, then `python3 -m playwright install chromium`).

`python tools/dev.py doctor` checks the environment, and `python tools/dev.py check` runs the full local check (dependencies, preflight, snapshot history, whitespace, and both test suites) without building PDFs.

## Make targets

| Target | What it does |
|---|---|
| `make all` | Preflights, parses, indexes, writes the cover data, generates the figures, balances the interior, compiles the digital edition, and exports it with its compact companion and provenance |
| `make verify` | Requires a current exported build; fails on crashes, missing reports, stale inputs, mandatory defects, or a visual-review ledger that does not match the exact PDF |
| `make specimen` | Verifies, then extracts the specimen from the verified interior |
| `make package` | Builds the specimen, then the release ZIP, its checksums, and its audit |
| `make test` | Both test suites (the repository's and the art skill's), one module per process in parallel |
| `make parse`, `make figures` | The first stages of `make all` on their own; both work from a clean checkout |
| `make clean` | Removes `build/`; the verified measurement cache in `.cache/` survives |
| `make deps`, `make doctor`, `make check`, `make status` | Install the lock, check the environment, run the full local check, and show Git and last-release state |
| `make fonts`, `make art-packages` | Regenerate the static fonts; build the installable art skill ZIP in `build/art/` |

The full build is `make clean all verify package`. Targets run one at a time to avoid concurrent writers and excess compiler memory. The interior composition (`build/book-cream.pdf`) is what the structural checks read; it is never delivered. New PDF bytes need a fresh visual-review ledger before `verify` passes, so a fresh build reaches `package` only after its pages are reviewed and bound (`docs/BUILD_AUTOMATION.md`).

The player aids and Hero records are built outside `make`:

```sh
python3 tools/render_aids.py                      # build/aids/all.pdf, the ten two-sided sheets
python3 assets/hero-record/sheet.py blank --pdf build/hero-records/hero-record-blank.pdf
python3 assets/hero-record/sheet.py heroes --pdf build/hero-records/basic-heroes.pdf
```

## Outputs

Replace `RC###` with the active version; filenames are generated automatically.

| File | Purpose |
|---|---|
| `Heraldry_RC###_digital.pdf` | The digital reading edition, with its covers, links, and bookmarks |
| `Heraldry_RC###_digital-compact.pdf` | The same edition with rasters downsampled to 150 ppi for screens (about a third of the size) |
| `Heraldry_RC###_player-aids.pdf` | The ten double-sided player aids |
| `Heraldry_RC###_hero-record-blank.pdf` | The blank two-sided Hero record |
| `Heraldry_RC###_basic-heroes.pdf` | The 24 Basic Mode Heroes on the Hero record |
| `specimen/Heraldry_RC###_specimen.pdf` | A production sample extracted from the verified interior |
| `Heraldry_RC###_release.zip` | The rebuildable source package |
| `SHA256SUMS.txt` | Checksums of every release file |

These are build outputs and are never committed. `make` writes the book files, the specimen, and the ZIP to `dist/`; the `Rebuild verified delivery` workflow adds the player aids and Hero records with the commands above, publishes everything as a GitHub Release, and commits `dist/RELEASE.json` (the tag, URL, and SHA-256 of each file) with the ledgers. See `docs/LARGE_FILES.md`.

The release ZIP holds the instructions and agent configuration, editable sources, every manuscript snapshot, fonts and licences, figures, ink art, and evidence ledgers. The PDFs are separate release files. The ZIP's own audit (`production/qa/package-audit.json`) stays outside it to avoid a circular checksum.
