# GPT artwork routes — 2026-10-07

Status: implementation handoff; no generation runner or paid calls added by this review. The required suite is the existing cover plus eleven chapter images in production/art/ART_MANIFEST.json. The current project still has zero supplied/approved masters. This document does not authorize spending or claim that artwork is complete.

## Available routes

ChatGPT has a built-in image-generation tool in the current session. It can generate and revise the twelve subjects using the existing asset prompts, with no OpenAI API key supplied to this chat. Selected project masters then need to be uploaded as assets/art/incoming/<ASSET-ID>.png and checked by the book build. Claude Code does not automatically inherit this tool or ChatGPT's subscription allowance.

For unattended generation inside Claude Code cloud or GitHub Actions, use OpenAI's Images API with OPENAI_API_KEY available as an environment secret to the chosen runner. A GitHub Actions secret is not automatically available to Claude cloud, or vice versa. Never commit or print the key, and do not ask the owner to paste it into chat. API billing is separate from ChatGPT and Claude credit.

Official documentation checked today lists gpt-image-2.5-flare-2026-09-08 and gpt-image-2.5-sunburst-2026-09-08 as image models with transparent PNG output. Choose and record an explicit available model after access/price checks at execution; do not silently substitute a model. An account may require API organization verification. Useful validated request dimensions: a chapter scene 2048x1056 is approximately the 7x3.6in slot; transparency avoids separate cream/white mattes. For the 300ppi chapter target, 2112x1088 meets dimension multiples and exceeds required 2100x1080. Check actual returned pixels and effective placed resolution. Cover resolution/crop must separately meet its own manifest target; resampling or a DPI metadata tag does not manufacture fine detail.

## Bounded automation contract

Before implementing/enabling live calls, the owner must authorize the service and a separate dollar limit in config/production.json; paid_calls_authorized currently remains false and external_spend_limit_usd remains 0. Credentials alone are not authorization. A dry run should validate asset IDs, expanded prompts, input references, dimensions and output destinations with no API/network call. No ordinary main push/build should trigger paid generation.

Implement a separate, manually invoked generation step, not a dependency of make all or make verify. Generate one chapter anchor first and review its ink character, anatomy, equipment, negative space and placed-size quality. That is an internal production gate; no routine owner approval pause is needed. Use the selected original anchor as reference input for subsequent edits/generations where supported. Describing a shared style or reusing a seed alone does not guarantee a coherent suite.

Generate one asset per bounded job; save each successful candidate before proceeding. Resume by asset ID, prompt/model/input hash and output hash; never regenerate an unchanged satisfactory asset simply because a build reruns. Preserve native masters and versioned candidates; promote a selected final PNG to the stable filename only after inspection. Record provider/model, exact prompt, date, reference input, resolution, usage/cost basis and QA in the manifest. Never put commercial reference-page images into final artwork assets.

Restrict request count, quality/size, retry count and concurrency before calling the service; reserve a conservative per-request allowance from the remaining owner budget. Persist the cost ledger after each response. Stop when the remaining allowance cannot cover the next request and retain a repair reserve. If a timeout leaves billing uncertain, mark that attempt's reservation spent/unknown until reconciled; do not blindly retry and charge twice. Configuration is a workflow guard, not a guarantee that the vendor's billing cannot exceed a cap; use available account controls as well.

Required image checks: exact source-supported subject; plausible construction/anatomy; coherent contour/hatching across the suite; no lettering/pseudo-runes; clean alpha/matte; no white halos; sufficiently open negative space; native detail legible at placed print size. Choose specific subjects rather than repeating skull/hood/smoke compositions. Integration must check both cream and white pages, update pagination/navigation, reconcile the full book and refresh current visual evidence. Do not claim generated art was hand-drawn.

Rules and deployment figures remain editable vectors with source-bound semantic review. The atmospheric generator does not replace their exact geometry, labels or measurements.

## Sources

- Images API guide: https://developers.openai.com/api/docs/guides/image-generation
- Request parameters/models: https://developers.openai.com/api/reference/resources/images/methods/generate
- Separate billing: https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform
