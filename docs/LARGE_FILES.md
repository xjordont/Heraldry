# Large files and images

Owner instruction, 2026-10-11: "set up the leanest, most efficient, most logical high quality workflow for repeatedly dealing with large files and images for our project."

**The rule:**
- Git holds sources and small records.
- Git LFS holds original art: one copy of each image, versioned.
- Anything that can be rebuilt (PDFs, ZIP packages, contact sheets) is never committed. It is built on request and delivered as a GitHub Release or a workflow download.
- Clones fetch only what they use.

Git history is permanent: earlier commits still hold old PDFs and ZIPs (about 490 MB on GitHub by 2026-10-11). Nothing rewrites that history. This policy stops it growing, and partial clones never download it.

## Where each kind of file lives

| Files | Stored in | Produced by | Fetched by |
|---|---|---|---|
| Delivered artwork, `assets/art/incoming/<ID>.png\|jpg\|webp` | Git LFS (`.gitattributes`; `ship` and `doctor` refuse an image without it) | the art worker's `save` and `ship` | the intake only for new images (`art_intake.py needs-pull`); the build only for what it places |
| Ink derivatives `assets/art/ink/`, the twelve atmospheric masters, `assets/art/masters/` | Git LFS | the intake workflow; the owner | the build (cached between builds) |
| Style references `assets/art/style/` (owner samples and public-domain prints) | plain Git, 0.1–4.5 MB each | the owner | every clone: the art worker attaches them and the tests read them |
| Publisher device `assets/art/brand/` (the owner's Escutcheon Press logo and its ink derivative) | plain Git, under 1 MB | the owner; `tools/brand_ink.py` makes the ink PNG | every clone and every build: the title page, colophon, and back cover place it |
| Owner reference books `references/private/pdfs/` | local only, ignored by Git (purged from history 2026-11-02) | the owner | copied by hand where needed (`references/README.md`); never committed; never packaged |
| Built PDFs and the release ZIP | a **GitHub Release** per requested build (tag `RC###-build-N`) | the `Rebuild verified delivery` workflow | the owner, from the Releases page |
| Illustrated Hero record PDFs (blank and 24 Basic Mode Heroes) | a **GitHub pre-release** per run (tag `RC###-hero-records-N`) | the `Build Hero records` workflow, on request | the owner, from the Releases page; not a book release |
| Build ledgers (`production/qa/`, provenance, inventory) and `dist/RELEASE.json` | plain Git | the same workflow | everyone; the ledgers are bound to the released files' SHA-256 |
| Skill ZIP and offline Work input package | not stored: `build/art/` | `make art-packages` (about 5 s), or the `Build art packages` workflow (a 30-day download) | the owner, only for the ChatGPT Work fallback |
| Review contact sheets | not stored: `build/art/review/` | `tools/art_intake.py pending --sheet` (it fetches just the pending ink files) | Claude Code, when reviewing |
| Work review bundles `production/art/work/inbox/*.zip` (fallback route) | plain Git until imported | ChatGPT Work | the import workflow, which moves the images into LFS and removes the ZIP |
| Attempts and previews on the art PC | `C:\Heraldry\art-scratch` (outside the clone) | the art worker | nobody; delete it after the run |
| The PC's copy of delivered images | `C:\Heraldry\art-archive` (`HERALDRY_ARCHIVE`) | `save` writes a copy with no download; a redo replaces it | the owner |

## Clones

- **Art PC (Codex):**
  - `git clone --filter=blob:none` (commits and trees only, with each file fetched when it is first needed), with `git lfs install --local --skip-smudge` so LFS images stay as small pointers. The worker fetches only the queue's references.
  - An existing full clone keeps working; a new one downloads a fraction of the history.
  - `next` and `status` fast-forward it before each item.
- **CI and bots:** every workflow checks out with `filter: blob:none`. The history check still compares against the previous head, fetching only the few blobs it reads. The build pulls only the LFS art it places, through an `actions/cache` keyed on those objects, so a rebuild downloads only new art.
- **Claude Code's container** works from the clone it is given. It fetches LFS files only for the task at hand: `git lfs pull --include=<paths>`.

## Builds and delivery

When the owner asks for a build, Codex uses the GitHub candidate/review/delivery chain in `docs/BUILD_AUTOMATION.md`. GitHub builds the candidate and review aids; Codex inspects every supplied image and binds the exact PDF. PDFs and ZIPs remain gitignored, so only ledgers and LFS review JPEGs are committed.

Delivery is the `Rebuild verified delivery` workflow:
1. It rebuilds from that commit and verifies the result against the committed ledgers (which proves the build is reproducible).
2. It publishes the PDFs, the release ZIP, `SHA256SUMS.txt` and the print instructions as a GitHub Release.
3. It commits `dist/RELEASE.json`, which records the tag, URL and each asset's SHA-256.

The release ZIP is the rebuildable source package. Following its own rule that raw generated art never ships, it carries the ink derivatives, not the generated native images. It refuses to pack any file that is still an LFS pointer.

The RC492 PDFs built before this policy are no longer in the working tree. They remain in Git history at commit `3da756f1f1da85b1bbc9dd4a26478ebcbd9c1053` (for example `https://github.com/xjordont/Heraldry/blob/3da756f1f1da85b1bbc9dd4a26478ebcbd9c1053/dist/Heraldry_RC492_digital.pdf`, then Download). Current delivery is identified by `dist/RELEASE.json` and `production/RELEASE_RESULT.json`; do not infer it from historical files or this document's date.

## Quotas to watch

- GitHub meters Git LFS storage and bandwidth per account. The owner should check the current allowance under GitHub → Settings → Billing before the full art run.
- The full art set is expected to be under 1 GB, at about 3 MB per native image plus small ink files, and each image is downloaded about once: by the intake.
- Release assets do not count toward the repository's size.
