# Optional editable InDesign project

Owner decision, 2026-10-15: provide an optional InDesign editing route, only when specifically invoked. This supersedes the earlier hold on InDesign work. PDF production remains the normal release path.

## Run it

From current main, with dependencies installed:

```powershell
python tools/dev.py indesign export --output "C:/Heraldry/indesign/my-project"
```

Use a new external directory for each export. Existing output is refused, preserving manual edits. `build/indesign/<name>` is also permitted for disposable exports, but `make clean` deletes the build tree: keep editing projects outside it. Other output locations inside the repository are refused. Generated IDML/INDD/book/template files are ignored and must not be committed.

Export does not launch Adobe, modify the manuscript, compose the Typst book, generate PDFs, update production review/release records, commit, or push. It reads the active immutable source and approved assets directly; stale parser inventories are not used. No paid API or additional Python dependency is required. Missing LFS bytes refuse; fetch only the publication assets, then retry with a fresh output folder:

```powershell
git lfs pull --include="assets/art/ink/**,assets/art/cover/**"
```

Alternatively, use Actions > **Export editable InDesign project** > **Run workflow** on main. Its only trigger is `workflow_dispatch`. Download the complete artifact with Links and Document fonts. The hosted job creates IDML, not INDD; it has no InDesign installation. Artifacts expire after 14 days. No release is published or pushed to main.

## Editable components

| Component | Representation |
|---|---|
| Rules, headings, emphasis, lists and quotes | Native text and paragraph/character styles, never page images or outlines |
| Tables | Native tables/cells, measured column widths, header rows, editable table/cell styles |
| Reading flow | Threaded chapter stories, two-column frames, full-width tables/figures, and finishing script that adds pages until all text is composed |
| Organisation | Named layers, masters,  heading bookmarks, internal TOC hyperlinks, source maps and exact manuscript snapshot |
| Design | Editable page geometry, margins, typography, paper swatch, running furniture, rules and chapter marks |
| Illustrations and owner cover | Linked prepared raster bytes in editable native frames; actual resolution retained |
| Figures and marks | Linked vector SVGs with editable original paths/text in Links; edit the original in a vector editor and update its link |
| Fonts | Bundled files, family/style and variable-font metadata, and OFL licences in Document fonts |

SVG artwork is not decomposed into native InDesign paths/text frames. Placement and scale are editable in InDesign; individual paths/labels are edited in the SVG. Figures are not rasterised, and raster illustrations do not become vectors. Adobe documents [IDML support](https://helpx.adobe.com/in/indesign/desktop/get-started/system-and-product-info/supported-file-formats.html) and [live linked graphics](https://www.adobe.com/learn/indesign/web/link-graphics).

`config/indesign.json` initially follows the active v4 page size, margins, gutter and 11 pt body. This is a separate native layout with recomposed pagination. It does not promise the Typst PDF's exact pages, conditional keeps, drop caps, table transformations, generated index, or final page design. The source TOC remains editable and clickable. No rules are rewritten or omitted to fit. The original cover's low print resolution remains unchanged.

## Finish in InDesign

Use a current supported release, version 16.0 or later for this IDML profile. Keep the folder together. In Window > Utilities > Scripts, run its `Finish in InDesign.jsx`. Install the bundled fonts if document-local activation is unavailable; see Adobe's [font instructions](https://helpx.adobe.com/nz/indesign/desktop/fonts/install-and-activate-fonts.html).

On Windows, the equivalent explicit command is:

```powershell
python tools/dev.py indesign compose --project "C:/Heraldry/indesign/my-project"
```

Add `--compose` to `indesign export` for one invocation that exports, launches installed Windows InDesign, and attempts native completion. `compose --prog-id` accepts a version-specific COM ProgID. On macOS run the JSX in InDesign's Scripts panel.

The script opens this package, relinks and proportionally fits graphics, adds live folios, composes all manuscript stories, adds threaded pages, and removes empty trailing seed pages. It checks missing/substituted fonts, broken/outdated links, story overset and cell overset. A stalled story, unfit row/object or page limit causes failure; text is never deleted or reduced to pass. Smart Text Reflow is enabled for later editing. Application script preferences are restored; unrelated open documents are not changed or closed.

After successful checks it saves `Heraldry_RC<N>.indd`, exports `Heraldry_RC<N>.composed.idml`, reopens the saved INDD, repeats checks, and writes `native-report.json` bound to this export. Existing native outputs and their report are never overwritten. Failures preserve diagnostics and any output already written; use a fresh project for another attempt.

The initial IDML contains seed pages and complete editable stories. The finishing step is required for a fully composed native project. Python structural success does not imply application validation.

## Verification and later edits

```powershell
python tools/dev.py indesign verify --project "C:/Heraldry/indesign/my-project"
python tools/dev.py indesign verify --project "C:/Heraldry/indesign/my-project" --native
```

Structural verification checks packaged hashes, IDML parts/references, frame threads, graphic links and manuscript text in order, including cells. Native verification also requires the matching app report, nonempty INDD, and round-trip IDML preserving every tagged manuscript story. Its first pass records output hashes in `native-verification.json`; changed native files cannot retain that proof. Whitespace is normalised for comparison; words, numbers, punctuation and cell order remain significant.

Inspect the actual layout, especially section keeps, page breaks, tables, figure labels/scale and cover cropping. Automatic checks do not constitute visual approval or a physical proof. Physical print remains **NOT TESTED**. Native application, visual and print statuses are reported separately.

Save further editing in a separate working copy. Native edits do not change canonical Markdown or approved PDFs. Bring text back through a reviewed [manuscript update](MANUSCRIPT_UPDATES.md); no INDD-to-source import runs automatically. Re-exporting creates a new project and does not merge old layout edits. PDF delivery still follows [BUILD_AUTOMATION.md](BUILD_AUTOMATION.md) after its own explicit request.

Implementation references: Adobe's [IDML introduction](https://developer.adobe.com/indesign/?navID=documentation), [TextFrame DOM](https://developer.adobe.com/indesign/uxp/dom/api/t/text-frame/), [Smart Text Reflow](https://helpx.adobe.com/indesign/desktop/add-and-manage-text/add-and-import-text/set-up-smart-text-reflow.html), and [document/export operations](https://developer.adobe.com/indesign/uxp/dom/api/d/document/). The finishing step uses ExtendScript; no startup script, watcher, ordinary Make target, or PDF workflow invokes it.
