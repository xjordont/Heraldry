# Set up the Heraldry publication project in Claude Code cloud

Prepared 5 October 2026 for the supplied RC484 manuscript. This kit contains a production prompt and starting configuration, not an already generated rulebook PDF.

## What this can realistically accomplish

Claude Code cloud can build the publishing software, make precise vector diagrams, typeset the whole manuscript, create navigation, and run repeatable PDF checks. Native subagents run in cloud sessions and support separate model and effort settings. Opus 5.5 and Sonnet 5.5 are documented current models; the kit pins their full model IDs instead of relying on moving aliases.

The difficult parts are content fidelity, the volume of pagination exceptions, illustrations, and printer-specific acceptance. No prompt can guarantee a flawless illustrated book within $100, keep a session alive indefinitely, or certify an unspecified printer's files. The master prompt requires implementation through delivery while preventing false claims about these limitations.

Your source is approximately **241,434 words with 332 pipe-table blocks and 833 headings**. The widest observed table has 12 columns. This is a substantial reference book, not a short skirmish pamphlet. The final page count must come from a real layout. The kit preserves the supplied manuscript exactly and requires lossless data checks for all tables.

## Recommended approach

Use one autonomous assignment with internal milestones: preserve and inventory the source, prove the design on difficult real pages, build the full book, integrate diagrams/art, stabilize navigation, then verify and package. There is no request for approval between those stages. Building a complete reading PDF early protects against spending all the credit on attractive first pages while the remaining chapters are unconverted.

Use Claude for **all instructional diagrams**: it can generate editable SVGs precisely from geometry and rules. Use an image generator for **atmospheric ink illustration**. Temporary artwork reservations are useful during typesetting; visible placeholder boxes do not belong in a finished reader edition. The prompt has three explicit routes: configured image generation, supplied images, or an honestly labelled art-light edition with a complete art manifest.

For your present situation, the economical route is to generate one style anchor and the main illustrations in ChatGPT Plus, save them into this repository, then let Claude integrate them. That involves a manual asset transfer. For a genuinely unattended illustrated build, configure a separately budgeted image API or compatible image-generation MCP before launch. Claude cloud credit does not pay for another provider.

## 1. Put the kit in a private repository

Unzip the package. Upload **the contents of `Heraldry_Claude_Publication_Kit/`** to the root of a new private GitHub repository. Keep `CLAUDE.md`, `MASTER_PROMPT.md`, `.claude/`, `config/`, `docs/`, and `source/` at that root. A browser file picker may hide `.claude`; confirm its agent files actually appear in the repository. The unchanged source is already included as `source/Heraldry_RC484.md`, so no transcription or filename editing is needed.

If using a local checkout, the ordinary setup is:

```bash
git init
git add .
git commit -m "Add Heraldry publication source and production brief"
```

Create the private remote using your normal GitHub workflow and push. A remote is convenient for cloud onboarding and durable work. Current Claude Code also documents bundling a local git repository into a cloud task; browser/GitHub onboarding is simpler when working from an iPhone.

The bundled manuscript retains its original content and SHA-256. The prompt instructs Claude to make publication edits in a separate patch/text layer rather than overwrite your finalized rules.

## 2. Configure the cloud environment once

Open [Claude Code cloud](https://claude.ai/code), connect the private repository, and select its branch. Verify that your $100 promotional credit is claimed, applies to this cloud session, and has the balance/expiry shown in your own account. This kit does not verify your entitlement, remaining credit, or promotion terms.

Configure the environment to allow the build dependencies and any selected external service. Depending on your environment, this may require GitHub/release downloads, Python package sources, licensed font sources, and the chosen image API domain. A prompt cannot enable network access that the environment denies. Claude is instructed to discover installed tools first and install only what is needed.

For minimal interruptions, choose an available execution permission mode that permits the intended in-repository builds, dependency setup, and asset processing. If your cloud UI offers **Bypass permissions**, it avoids routine tool prompts in the isolated cloud task; choose it only for this dedicated repository/environment, without unrelated credentials. Otherwise use the available automatic/allow-rule configuration and expect mandatory policy blocks to remain possible. The kit deliberately does not commit blanket permission bypasses or override your account policies. Do not start in Plan mode, which is unsuitable for immediate implementation.

Keep account-level paid overage/automatic recharge disabled, or set its cap to your intended authorized amount, before launching if you want a strict external spending boundary. The prompt targets $80 and holds $20 for repairs, but **instructions in a prompt are not a hard billing control**. The native subagents are preferred over separately billed API/CLI workers.

Cloud work may continue after you close your device. It can still stop because of usage limits, runtime expiry, inaccessible dependencies, or a completed agent turn. On-disk state, commits, and a resumable build protect progress; they cannot promise perpetual execution.

## 3. Select models and effort

Select **Opus 5.5, medium effort** for the primary session. The included `.claude/settings.json` requests the full Opus ID and medium effort. Confirm the cloud session actually applied them; configuration cannot grant access to a model your account lacks.

Where supported, explicit commands are:

```text
/model claude-opus-5-5
/effort medium
```

Send these individually if needed, before the launch instruction. Current cloud documentation supports argument-form model/effort commands. Do not assume a terminal picker is available in the browser.

| Task | Model | Effort |
|---|---|---|
| Main orchestration | Opus 5.5 | medium |
| Architecture, difficult source ambiguity, final acceptance | Opus 5.5 | high for a bounded review |
| Build/parser/index correctness | Sonnet 5.5 | high initially, medium for routine changes |
| Layout production | Sonnet 5.5 | medium |
| Diagram semantics and independent QA | Sonnet 5.5 | high |
| Simple inventory/report formatting | Haiku 4.5 | supported default |

Both 5.5 models support low, medium, high, xhigh, and max in current Claude Code documentation. Its default is medium for both, while the Sonnet API documentation lists a different API default; the kit sets task effort explicitly. `xhigh` and `max` are not economical blanket choices for this assignment. Haiku 4.5 does not receive an unsupported effort field.

The `.claude/agents/` files are ready before session startup, so cloud discovery is more reliable than creating them midway through the task. The master prompt limits concurrency to two and requires disjoint file ownership. It keeps expensive Opus focused on integration and consequential decisions.

## 4. Decide the artwork route

### Use ChatGPT Plus and transfer files

ChatGPT Plus includes image generation, but **API usage is separately billed**. I found no documented supported bridge by which Claude Code can spend your ChatGPT Plus image allowance as an image-generation API. Do not design the project around a speculative connector or automated signed-in ChatGPT browser session.

Use the style prompt in `docs/ART_DIRECTION.md` in ChatGPT. Generate the style anchor first; use it as an image reference for subsequent requests. Ask Claude's source-aware art plan for each asset's subject and placement size, or supply a small initial suite. Save originals into `assets/art/incoming/`, with clear stable filenames. Commit/push assets before launch, or send a follow-up directing the existing session to integrate them after they are available. Keep the original generated files; repeated screenshots and JPEG recompression reduce print quality.

A later art-integration pass is straightforward because image locations, dimensions, and crops live in a manifest rather than scattered hard-coded page edits. Insertion can change pagination, so it must trigger TOC/index/link and final-PDF rechecks.

### Use a configured image API/MCP for unattended generation

Configure the service in the cloud environment's secret settings. For an OpenAI API integration, use separately funded API credentials and current official image-generation documentation. Do not commit credentials. Set an explicit amount in `config/production.json` under `image_generation.external_spend_limit_usd`; default is **0**, so finding an API key does not authorize paid calls. For authorized paid generation, also set `paid_calls_authorized` to `true`; both the explicit limit and authorization must be present. An already configured, documented no-cost quota can be recorded separately.

The user, not this kit, must authorize and configure that external spend before launch. The master prompt can implement the adapter and use the service once these conditions exist. It does not contain invented endpoints or a promised price per image. Text and captions are typeset separately; precision diagrams stay vector-based.

For a single launch that reaches the requested **fully illustrated** result, choose this route or provide the complete image suite up front. Without either, Claude should finish the art-light edition and report the illustrated target as incomplete.

## 5. Set the print target if known

Default design: US Letter portrait, grayscale, clean non-bleed interior, binding-aware margins, separate cover. This is a sensible production starting point, not a universal printer-approved profile.

If you know the printer, binding, and paper, place its current specification and actual cover template in `config/printer/` and reference them in `config/production.json`. The cover wrap must use the template matching the actual final page count and stock. For a book this large, verify the printer's binding/page-count limits before placing an order.

Without those inputs, Claude can deliver complete cover panels, a parametric wrap candidate, and a generally preflighted print interior. It must label the printer-dependent files as candidates. It cannot honestly deliver a certified final spine/cover for an unspecified printer. PDF/A export is not PDF/X certification; Typst currently documents PDF versions, PDF/A, and PDF/UA output rather than native PDF/X export. The prompt includes a separate verified print-export route where required.

## 6. Launch

Paste the following short instruction into the configured Opus cloud session:

```text
Read MASTER_PROMPT.md and execute it completely as the production director.
Use source/Heraldry_RC484.md as the protected canonical manuscript.
Use the included production configuration and native Sonnet subagents.
Proceed autonomously through implementation, rendering, QA, repairs, and packaging.
Do not stop after planning or the specimen. Preserve the $20 repair reserve.
Use only configured, budget-authorized artwork services or supplied assets.
Report any external dependency honestly and complete all independent production work.
```

Do not paste the massive manuscript into the conversation. Claude reads it in targeted slices from the repository. `MASTER_PROMPT.md` is the complete reusable prompt if you prefer to paste it directly, but storing it in the repo makes it easier to recover after compaction.

If the session is interrupted, send:

```text
Resume from production/STATE.md and the latest committed checkpoint.
Read MASTER_PROMPT.md, retain its source-integrity and budget constraints,
and complete the remaining acceptance gates without repeating finished work.
```

## 7. What to expect at delivery

Look for a full reading PDF, print interior, cover panels/wrap status, editable sources, assets, actual TOC/index page maps, a complete table reconciliation report, reviewed-page ledger, preflight report, and ZIP. A specimen is not the finished publication. The final report should distinguish content, layout, figures, illustration, general print checks, printer-specific interior, and printer-specific cover status.

The $100 may support a strong production pipeline and substantial finished output if scripts do bulk conversion and context stays controlled. It is **not a reliable fixed-price estimate** for exhaustive visual polish of a 241,000-word illustrated book. Image generation is additional unless your existing service covers it. The prompt is designed to spend on reusable components and defect repair, while keeping a complete checkpoint if the credit runs out.

## Research and why the prompt is structured this way

All links below were checked on 5 October 2026. They support the workflow; they do not establish that this particular book has already passed production checks.

- [Claude Code cloud documentation](https://code.claude.com/docs/en/claude-code-on-the-web): cloud environments, repository access, continuing off-device, supported commands, and native subagents.
- [Custom subagents](https://code.claude.com/docs/en/sub-agents): project-scoped agent files, model selection, and effort frontmatter.
- [Model configuration](https://code.claude.com/docs/en/model-config): model IDs, supported effort settings, cloud controls, and per-model behaviour.
- [Claude Sonnet 5.5 specifications](https://platform.claude.com/docs/en/models/sonnet-5-5/overview) and [Opus 5.5 announcement](https://www.anthropic.com/claude-opus-5-5): current model availability and capabilities.
- [Configure permissions](https://code.claude.com/docs/en/permissions): execution modes and the limits of prompt-level autonomy.
- [Ashen RPG production instructions](https://github.com/HallowXIII/ashen-rules/blob/master/CLAUDE.md): a directly comparable public tabletop rulebook with a Typst assembly layer, chapter files, central styles, pinned toolchain, and Claude-specific build instructions. This is evidence that the architecture is used in a real project, not proof of its quality or permission to copy its assets.
- [Typst TTRPG templates](https://github.com/Collapsologist/typst-ttrpg-templates): tabletop-oriented reusable typesetting patterns. Inspect licences before reusing code; do not copy another game's identity or art.
- [Typst table documentation](https://typst.app/docs/reference/model/table/) and [PDF export documentation](https://typst.app/docs/reference/pdf/): repeating headers and export standards. The kit adds its own content reconciliation and design requirements rather than assuming a generic converter handles the tables well.
- [IngramSpark File Creation Guide](https://www.ingramspark.com/hubfs/downloads/file-creation-guide.pdf), edition 24 August 2026: an example of real printer-specific requirements for embedded fonts, resolution, bleed, PDF compliance, and cover preparation. This is a reference, not a printer selection for you.
- [ChatGPT Plus documentation](https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus) and [OpenAI image-generation API](https://developers.openai.com/api/docs/guides/image-generation): image access and separately billed API integration.

## Kit review

The prompt was reviewed a second time for: source protection; complete table coverage; model/effort realism; context efficiency; bounded credit use; art availability and style consistency; accurate diagram semantics; TOC/index convergence; original typography and covers; printer-specific requirements; no routine approval pauses; recovery; and honest final statuses. The findings and changes are recorded in `docs/PROMPT_REVIEW.md`.

## Version 2: reference-informed design

This kit includes `docs/DESIGN_SPEC.md` and `docs/REFERENCE_ANALYSIS.md`, distilled from representative rendered pages of the supplied books. MASTER_PROMPT.md now requires the design specification before the specimen build. The canonical manuscript is unchanged.

Default: upload this kit and start the build from its written specification. Optional: provide the 14 primary visual pages across six books for calibration. `references/README.md` explains hash-verified extraction, access, and exclusions. The complete commercial PDFs and their images are not bundled. Do not make their availability a build dependency.

Read `MASTER_PROMPT.md` and execute it completely remains the launch instruction.
