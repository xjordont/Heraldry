# Anchor review, round 2: hand-inked direction (Codex, 2026-10-11)

Bundle from Codex on the owner's PC: `batch_ART-CLI-THE-GREENMARK__ART-ANC-DWARF.zip`, sha256 955599f3...625e3d. Source commit 5d8fbc5; model label "not shown", and the tool exposed no size or quality selector. `verify-bundle`: PASS. Smoke record: the Greenmark's two references attached, and the native PNG was readable.

Codex's own push was blocked by a delivery_guard bug: the porcelain status was stripped, so the first path lost its first letter. That is fixed in 3887ed6. The bundle was then delivered with the fixed guard (`ship --execute`, commit 081ee0e, PNGs through LFS with oids equal to the bundle's native SHA-256). The intake workflow ran in 0e11e1f with no warnings.

Reviewer: Claude Code orchestrator, by visual inspection at full size, with a close crop of the tarantula's legs. These are AI-generated images, not hand-drawn.

| ID | Native | Attempts | Codex self-QA | Verdict | Notes |
|---|---|---|---|---|---|
| ART-CLI-THE-GREENMARK | 1536x1024 | 3 | flags (style, margins) | APPROVE | Clearly a notch more hand-drawn than round 1: bolder contours, more open paper, root-broken road and milestone, a small mossy stone ring in the middle distance, bark warning cuts now drawn as slashes. Minor: tight top margin; the hounds are small but readable as wolves rather than barely seen shapes; the ground is still busy at the bottom. |
| ART-MON-GIANT-TARANTULA | 1254x1254 | 3 | flags (legs, style, margins) | REJECT (redo) | Seven feet are visible (four left, three right), with the eighth at best implied behind the helm: the same defect as round 1, and "exactly eight legs" is a must-show requirement. The style improved (bolder, less texture). Composition brief amended so all eight legs splay clear and the helm lies apart. |
| ART-MON-UNDEAD-CHAMPION | 1254x1254 | 3 | pass | APPROVE | Two-handed maul whose fused-bone head is bound in riveted iron, both hands on the haft; pale dead flesh, rusted plate scraps, chains, ash patch. Bold, clean inking. Reads as undead, not an ogre. |
| ART-CLA-FIGHTER | 1024x1536 | 3 | flag (left margin) | APPROVE | Ring shirt over padding, open nasal helm, round boss shield, shortsword and belt dagger, braced low on flagstone. Clean hand-inked look. The sword tip sits about 7% from the left edge, acceptable for an isolated figure. |
| ART-ANC-DWARF | 1024x1536 | 3 | pass | APPROVE | Very broad, heavy build; braided beard with rings; lantern forward with the shield on that arm; single handaxe; no horned helm or comic proportions. |

Direction check against the owner's 2026-10-11 brief ("a notch more hand drawn"): met for all five. Line economy and open paper are clearly better than round 1. Approved images are not style references (owner-samples-only rule). The anchor gate (`approve-anchors`) waits for the tarantula redo.
