# Large files and images

Owner instruction, 2026-10-11: "set up the leanest, most efficient, most logical high quality workflow for repeatedly dealing with large files and images for our project."

**The rule:**
- Git holds sources and small records.
- Git LFS holds original art: one copy of each image, versioned.
- Anything that can be rebuilt (PDFs, ZIP packages, contact sheets) is never committed. It is built on request and delivered as a GitHub Release or a workflow download.
- Clones fetch only what they use.

Git history still holds the PDFs and ZIPs committed before this policy (about 490 MB on GitHub by 2026-10-11). The history rewrite of 2026-11-02 removed only the owner's reference books, so those old files remain; this policy stops history growing, and partial clones never download them.

## Where each kind of file lives

| Files | Stored in | Produced by | Fetched by |
|---|---|---|---|
| Delivered artwork, `assets/art/incoming/<ID>.png\|jpg\|webp`, including the twelve original atmospheric masters (`ART-COVER-001`, `ART-CH01-001` to `ART-CH11-001`) | Git LFS (`.gitattributes`; `ship` and `doctor` refuse an image without it) | the art worker's `save` and `ship` | the intake only for new images (`art_intake.py needs-pull`); the build only for what it places |
| Ink derivatives `assets/art/ink/`, older raw masters `assets/art/masters/`, the cover art `assets/art/cover/` | Git LFS | the intake workflow; the owner | the build (cached between builds) |
| Generation records kept from retired routes: `assets/art/variants/`, `assets/art/marks/candidates/` | Git LFS | earlier runs; nothing adds to them now | nobody routinely; never packaged |
| Style references `assets/art/style/` (owner samples and public-domain prints) | plain Git, 0.1–4.5 MB each | the owner | every clone: the art worker attaches them and the tests read them |
| Publisher device `assets/art/brand/` (the owner's Escutcheon Press logo and its ink derivative) | plain Git, under 1 MB | the owner; `tools/brand_ink.py` makes the ink PNG | every clone and every build: the title page, colophon, and back cover place it |
| Built PDFs (the book, its compact companion, the player aids, the Hero records, and the specimen), the release ZIP, and `SHA256SUMS.txt` | a **GitHub Release** per requested build (tag `RC###-build-N`) | the `Rebuild verified delivery` workflow | the owner, from the Releases page |
| Build ledgers (`production/qa/`, provenance, inventory) and `dist/RELEASE.json` | plain Git | the same workflow | everyone; the ledgers are bound to the released files' SHA-256 |
| Candidate review images `production/qa/review/*.jpg` | Git LFS, committed by every candidate (about 57 images, about 19 MB), replacing the previous set in the tree; earlier sets stay in LFS storage | the `Build candidate` workflow | the reviewer, with `git lfs pull --include="production/qa/review/*"` |
| Art skill ZIP | not stored: `build/art/` | `make art-packages` (about 5 s), or the `Build art packages` workflow (a 30-day download) | whoever installs the skill, for example in ChatGPT Work |
| Art review contact sheets | not stored: `build/art/review/` | `tools/art_intake.py pending --sheet` (it fetches just the pending ink files) | the reviewer |
| Attempts and previews on the art PC | `C:\Heraldry\art-scratch` (outside the clone) | the art worker | nobody; delete it after the run |
| The PC's copy of delivered images | `C:\Heraldry\art-archive` (`HERALDRY_ARCHIVE`) | `save` writes a copy with no download; a redo replaces it | the owner |

## Clones

- **Art PC (Codex):**
  - `git clone --filter=blob:none` (commits and trees only, with each file fetched when it is first needed), with `git lfs install --local --skip-smudge` so LFS images stay as small pointers. The worker fetches only the queue's references.
  - An existing full clone keeps working; a new one downloads a fraction of the history.
  - `next` and `status` fast-forward it before each item.
- **CI and bots:** every workflow checks out with `filter: blob:none`. The history check still compares against the previous head, fetching only the few blobs it reads. The build pulls only the LFS art it places, through an `actions/cache` keyed on those objects, so a rebuild downloads only new art. Repository checks fetch no LFS files.
- **Agent sessions** work from the clone they are given and fetch LFS files only for the task at hand: `git lfs pull --include=<paths>`.

## Builds and delivery

When the owner asks for a build, the agent runs the GitHub candidate, review, and delivery chain in `docs/BUILD_AUTOMATION.md`. GitHub builds the candidate and its review images; the agent looks at every image and binds the review to the exact PDF. PDFs and ZIPs stay gitignored, so the commits are the ledgers and the candidate's LFS review images.

Delivery is the `Rebuild verified delivery` workflow:
1. It rebuilds from the ledger commit and verifies the result against the committed ledgers, which proves the build is reproducible.
2. It publishes the PDFs, the release ZIP, and `SHA256SUMS.txt` as a GitHub Release.
3. It commits `dist/RELEASE.json`, which records the tag, URL, and each asset's SHA-256.

The release ZIP is the rebuildable source package. Following its own rule that raw generated art never ships, it carries the ink derivatives, not the generated native images. It refuses to pack any file that is still an LFS pointer.

The current delivery is identified by `dist/RELEASE.json` and `production/RELEASE_RESULT.json`; don't infer it from this document's date. The last PDFs committed to Git, RC492's, are at commit `5351b31a746b21f0c8a4ca93c9a1cf65e1d05127` (after the 2026-11-02 rewrite; older records cite it as `3da756f`).

## Quotas to watch

- GitHub meters Git LFS storage and bandwidth per account. The owner should check the current allowance under GitHub → Settings → Billing. Candidate review images add about 19 MB of LFS storage per candidate.
- In the current tree the delivered images take about 1 GB (358 natives at about 3 MB each), the ink derivatives about 170 MB, and the retired variants and mark candidates about 490 MB. LFS storage also keeps every replaced version (redos and earlier review images). Each new image is downloaded about once: by the intake.
- Release assets do not count toward the repository's size.
