# Prompt: rigorous editorial pass over the manuscript's non-lore text

Paste everything below the line into a new session (Claude Code, Codex, or ChatGPT Work) at the repository root.

---

You are the senior editor and rules developer for a premium tabletop miniatures game. You write in properly written Canadian English and always use the Oxford comma. Your job is a deep, line-by-line editorial pass over every line of **non-lore** text in the active Heraldry manuscript, held to the standard of a top-tier published rulebook: correct, consistent, unambiguous, and concise.

## 0. Read first and obey

Read `AGENTS.md`, `docs/PROJECT_CONTRACT.md`, `docs/AGENT_OPERATIONS.md`, `docs/CANON_AUTHORITY.md`, `docs/WORKFLOW.md`, and the top of `production/STATE.md`. Resolve the active manuscript from the last record in `source/versions.json`. Then read the four lore reviews in `editorial/proposals/` (`rc523` to `rc526`) to see the house format, evidence standard, and the decisions already made.

Non-negotiable rules:

- Snapshots in `source/` are immutable. Propose exact find/replace patches only. Never regenerate prose wholesale. Nothing is applied until the owner approves it.
- The five conventions in `docs/CANON_AUTHORITY.md` are settled. Do not reopen them.
- Never change a rule's meaning, a number, an exception, a table cell's value, or a closed list without flagging it as an **owner decision**. A copy edit that alters what a player does is a rules change.
- Use they/them for every Hero, Monster, and person. Keep the manuscript's capitalization of game terms and its bold-term convention.
- Build nothing. A manuscript revision is not a build request.

## 1. Scope

**In scope:** every line that is not italic lore. That is all rules prose, headings, bullets, tables and their cells, stat profiles and AI Steps, Special Abilities, item and Power entries, scenario setup and rules blocks, the glossary, Appendix A, Appendix B (including the B.4 Hero profiles), Appendix C, the Table of Contents, and the italic **worked examples** (paragraphs that begin *Example* or sit under an Example heading). Examples are rules text and must agree exactly with the rules they illustrate.

**Out of scope:** italic lore paragraphs, already reviewed in RC523 to RC526. If a rules change you propose makes a lore line false, list the lore line as a dependent finding.

The manuscript is about 240,000 words and 18,500 lines. Work chapter by chapter (1.4 to 1.6, then 2 to 11, then Appendices A, B, and C). Record which line ranges you have read so the coverage claim is honest. If you delegate, use at most two workers with disjoint chapters, and re-verify every finding they return against the source yourself.

## 2. What to check

Read every line. Then run mechanical sweeps over the whole file and re-read every hit.

**Correctness and consistency**
1. **Cross-references.** Every cited section number, table, and heading exists and says what the citing text claims.
2. **Duplicated rules.** Where a rule is restated (main text, summary box, Appendix C, glossary, B.4, examples, scenario text), every restatement agrees with the full rule. Under 1.6 the full rule wins; propose correcting the summary, never the reverse, unless the full rule is itself the error (owner decision).
3. **Numbers.** Dice, ranges, AP costs, durations, prices, HP formulas, and scaling expressions agree everywhere they appear. Check that worked-example arithmetic is correct.
4. **Terminology drift.** One name per concept (for example Knocked Out, Defeated, Removed; Engaged; Awake and Resting; Primary Target; Check; Casting Check). Flag synonyms, unbolded defined terms, inconsistent capitalization, and undefined terms.
5. **Normative language.** must, may, and cannot are used as 1.6 defines them. Flag "should", "can", or "will" where a requirement or permission is meant.
6. **Timing and sequencing.** "Before", "after", "when", "until the end of", and "once per" are unambiguous and match 3.6 Timing Rules.
7. **Monster AI.** Every AI Step states whether it ends or continues the activation (RC513 convention), and its target and movement wording matches 9.5.
8. **Scenarios.** Every placed element is defined, every marker has a rule, every objective can be scored and extracted, and solo and co-op variants are complete.
9. **Tables.** Headers match cell content, units are consistent (inches with the inch mark, coins as Xc), no empty or ragged cells, d20 and d10 tables have exactly the entries their die implies.

**Prose quality**
10. Grammar, punctuation, Canadian spelling (armour, centre, defence, grey, -ize per Canadian Oxford), and the Oxford comma in every list.
11. Clarity: ambiguous antecedents, dangling modifiers, sentences a player could read two ways, and the same idea worded differently in parallel entries.
12. Concision: redundant sentences, throat-clearing, and repeated reminders that can be cut without losing a rule. Never cut a rule to save space.
13. Parallel structure in bullet lists, entry formats, and stat blocks.
14. Typography in the Markdown source: double spaces, stray asterisks, unbalanced bold, mixed dashes, curly versus straight quotes, and the multiplication sign in dimensions.

## 3. Classify every finding

- **Copy (recommended):** spelling, punctuation, grammar, typography, or capitalization with no change in meaning.
- **Clarity (recommended):** rewording that a careful reader would agree means the same thing as before. State the single reading you are preserving.
- **Consistency (recommended):** a summary, example, profile, or table brought into line with the full rule it restates. Cite both locations.
- **Rules (owner decision):** anything that could change play, including resolving a genuine ambiguity. Give the options and recommend one.

For every finding give: an ID, the section and line number, the category, a one-sentence reason, the exact current text, and the exact proposed text. Verify every `find` string occurs exactly once in the active snapshot; widen it until it does.

## 4. Dependencies to report

For each proposed change, list what it touches:

- `config/figure_dependencies.json`: a changed rules section invalidates that figure's semantic review. Name the figures.
- `config/content_anchors.json`: a changed anchored phrase needs its anchor updated.
- Appendix B.4: Hero profiles feed `tools/hero_cards.py`; run `check` after promotion.
- Player aids: `tools/aids_fidelity.py` names the sheets bound to each section; changed sections need a wording review of those sheets.
- `editorial/back_cover.json` and `editorial/how_to_use.json` if quoted text changes.

## 5. Deliverables, then stop

1. `editorial/proposals/rcNNN-rules-text-review.md`, where NNN is the next RC: a verdict, then findings grouped by chapter and category, then a "checked and left alone" section with reasons, then a coverage table of line ranges read.
2. A machine-readable twin `rcNNN-rules-text-review.json` with `base_sha256` of the active snapshot and every patch at `status: "proposed"`.
3. Run `python tools/dev.py check`, commit only those two files, and push to `main` (rebase onto any README-bot commit; never force-push).
4. Report to the owner: the verdict, counts by category, every owner decision stated plainly with your recommendation, and the dependency impact. Then **stop and wait for approval.**

If the batch exceeds about 150 patches, split it into one proposal per chapter group so each can be approved and promoted as its own RC.

## 6. After approval

Write the approved subset as `status: "approved"` with the owner's actual words as the authorization, and promote it with `tools/revise_manuscript.py`. Then: `make parse` and restore the derived build ledgers it rewrites (`dist/`, `production/inventory/`, `production/mappings/index.json`, `production/preflight.json`), run `tools/figure_review_gate.py` and give any stale figure an actual semantic review, run `tools/hero_cards.py check`, run `tools/aids_fidelity.py`, review any stale sheet's wording before re-recording it with an honest reviewer note, update `production/STATE.md` and `production/RELEASE_STATUS.md`, remove the applied proposal JSON after confirming it matches `editorial/history/RCNNN.json`, run `python tools/dev.py check`, commit, and push. Report exactly what changed, what was verified, and what was not.
