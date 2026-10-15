# Calibration source and PNG review

Date: 2026-10-15. Reviewer: independent Codex worker. Scope: the current diff in `typst/calibration.typ`, `typst/heraldry.typ`, and `docs/INKJET_PRINT.md`, plus both existing cream/white calibration PNGs under `build/checks/publication-first-pass/`. No blocking findings within this scope.

- The active body binding remains `templates/system.typ`: Source Serif 4, 11 pt, 3.55 pt paragraph leading. The table binding is Source Sans 3, 9.3 pt, 2.7 pt leading. The sheet derives its body/table labels and samples from these values; the configured essential minimum is 9 pt. The older 10.5/9.5 pt starting values do not control these samples.
- Inlining the new `table-size` and `table-lead` constants and removing their declarations reproduces `HEAD:typst/heraldry.typ` exactly. The shared-type refactor preserves the previous values and body implementation.
- The current source paragraph resolves exactly once, contains 289 characters, and remains unchanged in RC492. Its actual SHA-256 is `a5ca7e72ad05a0cd69bb0bdca8238c10a635cf18345ae719c047c42fd3a8552a`. The assertion rejects a missing or duplicated prefix match; it does not freeze that paragraph against a future authorised manuscript revision.
- Both rendered pages were viewed directly. Labels, source paragraph, table rows/header, rules, hatch boxes, and grayscale steps are legible, with no visible clipping. The 21 pt heading wraps cleanly within its column. All inset frames are visible; the edge labels intentionally sit outside the book's essential margin.
- Both PNGs are 1224x1584 pixels, consistent with Letter at 144 ppi. The 1-inch square's vertical-border centres are 144 pixels apart. Source geometry remains 612x792 pt, with a 1-inch square and 3-inch ruler.
- No diff was present in the manuscript, main body template, prior visual-review/STATUS ledgers, or `dist/RELEASE.json` at review time.

Reviewed image SHA-256: cream `cb15f1c9db16fad5587fba2b3e2c7fb1a3bf1af61ee0d88ef05250427620120c`; white `36dd7a5082cc22c9d4322d8b6f99ff8f145fdea2ce60f3c5af80d06379603817`.

Limits: this is a source and 144 ppi PNG review, not a production PDF proof, a full-book layout review, or a physical printer proof. No compilation, production build, test suite, commit, push, or release was performed by this reviewer. Fine hatch/rule survival and true printed size still require physical examination. Physical print: **NOT TESTED**. Existing release QA remains bound to its earlier build.
