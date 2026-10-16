# Publication improvement first pass

Approval update, 2026-10-15: the owner approved all proposed canon alignments and ten exact manuscript corrections. The revision engine has created RC493; approved evidence is archived at `editorial/history/RC493.json`. See `rc493-editorial-verification.json` and the RC493 figure-review reports. The original first-pass checkpoint below is retained as history; its pending decisions are now resolved for this batch.

Date: 2026-10-15. Owner authorisation: "Continue as you suggest", following the research report's recommended initial package. Base commit: `1a890818694fd03f6f2d44e6508e787b6879280c`.

## Outcome and scope

The first pass traces inherited authority conflicts, performs a bounded second source review, corrects the calibration source, and establishes executable human/accessibility/print protocols. It does not complete a human copyedit, a reader study, a delivered-PDF accessibility audit, or physical printing. No manuscript revision or publication build is requested or claimed by this work.

The active manuscript remains RC492, SHA-256 `a5ca7e72ad05a0cd69bb0bdca8238c10a635cf18345ae719c047c42fd3a8552a`. The last delivery remains RC492-build-37. Existing release and review ledgers describe that delivery and have not been replaced.

| Work | Actual result | Remaining input or action |
| --- | --- | --- |
| Authority trace | [Five scoped conflicts](publication-authority-review.md) traced to original supplied RC484; proposed preservation of settled text | Owner disposition before aligning the standing brief |
| Bounded editorial review | [1,517 lines read](independent-editorial-first-pass.md); seven findings and ten exact draft replacements | Review exact proposals; no batch is approved or promoted |
| Calibration source | Body/table/minimum labels derive from active settings; current body excerpt and actual header style added | Rebuild the PDF only on a separate requested publication build |
| Calibration image validation | Cream and white each rendered as one 1224x1584 PNG at 144 ppi; integrating reviewer viewed both | Not a physical print or a new released PDF |
| Reader usability | [Bounded tasks and recording protocol](../../docs/PUBLICATION_CHECKS.md) prepared | Real participants and recorded execution |
| Accessibility | Source concerns and exact-file/manual test protocol recorded | Exact released PDF plus viewer/screen-reader execution |
| Physical proof | Procedure and specimen-selection criteria prepared | Actual printer/media/binding and examined sheets; NOT TESTED |

## Calibration change

`typst/calibration.typ` formerly labelled 10.5 pt as the body size and 9.5 pt as the table size. It now consumes active 11 pt body and 9.3 pt table values, plus the configured essential minimum. `typst/heraldry.typ` shares the existing 9.3 pt/2.7 pt table values through named constants; their numerical values and the book's body settings are unchanged. The sample paragraph is read verbatim from the active snapshot and must match exactly once. The sample table uses the active band and type size, and a separate swatch calls the actual header renderer. Diagnostic font/rule tests remain diagnostic rather than manuscript additions.

Both PNG diagnostics were directly inspected: labels and samples are visible, the two-column sheet remains on one page, the heading sample wraps within its column, and no sample overlap or clipping was observed. Image files remain ignored at `build/checks/publication-first-pass/calibration-cream.png` and `calibration-white.png`. This validates the diagnostic source only. No PDF, release image, or release approval was regenerated.

## Exact-file limitation

No local released PDF matching build 37 was found in the checked project, scratch, Downloads, Documents, or current manuscript workspace. The three PDFs in the preserved old checkout were hashed read-only; none matches the corresponding build-37 manifest hash, so none was copied or used as the current release. The release page in the in-app browser showed an unauthenticated GitHub 404. No credentials were extracted and no build was dispatched to substitute for the missing delivery.

The next actual PDF checks require the authorised build-37 downloads or a matching local copy. Verify against `dist/RELEASE.json` before use. For example, the digital PDF must have SHA-256 `bc53109ef539e3ac21c8bd37f342ca1abb01b28a6544909f0f22fb5373ee879b` and 152,931,880 bytes. This is an access/input limitation, not an assertion that the released file fails accessibility or proofreading.

## Validation

Baseline and post-change `python tools/dev.py check` passed: 190 tests each, 3 expected empty-art-queue skips; locked dependencies, 8 baseline contracts, all 17 protected prior snapshots/evidence files, and whitespace passed. The post-change run completed in 118.123 seconds. No additional unit tests were added for the reversible style correction; real PNG compilation and visual inspection exercise the changed source.

[A fresh calibration reviewer](calibration-source-review.md) independently viewed both PNGs, checked their 1224x1584 dimensions and 144-pixel calibration inch, confirmed excerpt uniqueness and unchanged RC492 hash, and verified that inlining the new table constants reproduces the previous adapter exactly. This is independent source/PNG review within the same model family, not human or physical certification.

All ten proposed manuscript replacements were checked against the current source and an in-memory sequential application: each matches exactly once, every status remains `proposed`, and the base SHA-256 matches. A readable diff is ignored at `build/checks/publication-first-pass/editorial-draft.diff`. No candidate manuscript file or next revision was written.

## Decision disposition

The owner subsequently approved the matrix and exact editorial packet; both are applied as recorded above. The earlier pending status describes the first-pass checkpoint only. Continue to distinguish approved source from released-file review, fresh model review from human independence, and file preflight from physical proof. Reader/accessibility/physical execution remains outstanding.
