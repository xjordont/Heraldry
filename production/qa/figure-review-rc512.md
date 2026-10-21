# RC512 figure review - 2026-10-21

Reviewed all 57 instructional figures against the current RC512 manuscript, compared with RC493. Source SHA-256: `816a3f9c81f91351cf24209580c18b3bd26e95ad747c9a13623304cf584ac5dd`. No manuscript bytes changed.

Fifteen SVGs changed: FIG-01, FIG-02, FIG-03, FIG-06, FIG-07, FIG-08, FIG-11, FIG-12, FIG-13, FIG-15, FIG-16, FIG-19, FIG-20, FIG-39, and FIG-57. Captions, placements, current source citations, setup specifications and figure dependency bindings were reconciled.

## Review and limits

Each figure has actual observations and matching SVG, caption, rule-section and inspected PNG hashes in `figure-semantic-review.json`. Standalone specimens use the book's Typst SVG renderer and bundled fonts. Direct PyMuPDF SVG renders showed fallback fonts and pattern failures, so they were rejected and replaced before final review. Scenario maps were inspected on six-figure contact sheets; rules, appendix and detailed scenario diagrams were inspected individually. Root additionally inspected the corrected attack, Chasm and setup specimens.

This is a model/repair-author review, not independent human proof, glyph-by-glyph proofreading, full-book placement or physical proof. No full-book build or publication was requested. Last delivered PDFs remain RC492-build-37. Physical print **NOT TESTED**.

## Changes and coverage

The rules diagrams now reflect pre-roll Reaction declaration/payment or commitment, AV-first mitigation, Temporary HP expiry, PvE initiative, Knocked Out Engagement and AI targeting, legal attack selection, ranged Power Cover and an orthogonal Shift example. Scenario figures reflect step 7 deployment zones/terrain spacing, step 11 placing order, failed Jump versus Chasm Fall, automatic Monster Terrain Checks, automatic Entangling Roots, and Basic Mode pickup/extraction/tie handling. One illustrative Pale City wall arrangement was moved to satisfy the new Blocking spacing.

Maps illustrate setup. Changes to boss HP, post-animation states, Powers and other rules not depicted by a setup map were checked for impact without adding invented map content. The 24 Basic Mode Hero profiles do not change the setup/scoring example used by FIG-19.

## Verification

Repository development check PASS: 326 tests, dependencies, baseline contracts, immutable history and whitespace. Full figure generation/selfchecks/validation PASS; semantic review gate 57/57 PASS, no stale entries or open major findings.

## Per-figure observations

### FIG-01

Compared 3.1-3.5: four phases and override loop retained. Added competitive versus PvE initiative route and Temporary HP removal at End of Round step 2. Inspected final render: phase headers, bullet lists and loop fit within frame. Final Typst render inspected with actual bundled sans-serif typography: no clipped text or overlapping boxes.

Sources: 3.1, 3.2, 3.3, 3.4, 3.5, 10.5.4, 5.4.2.

### FIG-02

Compared 2.5,3.3,4.5,5.5.1: activation eligibility, Stunned/Sleeping zero-AP exception and 3-to-1-to-0 AP example retained. Added pre-roll declaration and cost payment or commitment. Block now explicitly declared and paid before damage and resolved during defence. Render inspected: AP squares, boxes and notes fit. Final Typst render inspected with actual bundled sans-serif typography: no clipped text or overlapping boxes.

Sources: 2.5, 3.3.1, 3.3.2, 4.2, 4.5, 5.5.1, 3.3, 3.5.

### FIG-03

Compared 5.1.1,5.2,5.3,5.4.3: all Reactions declared before dice, result-dependent commitments and no new post-roll declaration made explicit; AV precedes other flat mitigation in controller order. Block example pays before damage. Both arithmetic examples verified. Render inspected: five steps and both tables legible without overlap. Final Typst render inspected with actual bundled sans-serif typography: no clipped text or overlapping boxes.

Sources: 5.1.1, 5.2, 5.3, 5.4.3, 4.5.

### FIG-04

Compared 2.6,2.6.1: closest-footprint Tabletop measurement, 1/1.5 grid range, S/M/L/H footprints and declaration/verification/lock timing remain correct. Render inspected: four panels, distances and flow boxes fit. No content change. Final Typst render inspected with actual bundled sans-serif typography: no clipped text or overlapping boxes. Monster hatch distinguishes footprints; all size labels and measurements fit.

Sources: 2.6, 2.6.1.

### FIG-05

Compared 2.6,2.9.3,4.4.3,4.4.7: 1+1.5+1.5+1=5, forbidden next diagonal5.5, Difficult costs2/3, maximum overlapping movement cost and diagonal intermediate-position rule verified. Render inspected: path totals, footprints and allowed/forbidden corners remain clear. No content change. Final Typst render inspected with actual bundled sans-serif typography: no clipped text or overlapping boxes. Difficult Terrain stipple, footprint hatch and dashed destination remain distinct; cost labels readable.

Sources: 2.6, 2.9.3, 4.4.3, 4.4.7.

### FIG-06

Compared5.1,4.4.4,5.5.4: added Knocked Out exclusion from Engagement; horizontal melee/Reach square bands retained. Move trigger point, Shift and forced movement exclusions correct. Render inspected: bands, tokens, paths and expanded caption fit. Final Typst render inspected with actual bundled sans-serif typography: no clipped text or overlapping boxes. Dashed ghosts and solid movement arrows visible; Reach shades remain distinct.

Sources: 2.6.1, 4.4.4, 5.1, 5.5.4.

### FIG-07

Compared2.7.2,2.8.4,2.9.1: sight lines verified against interiors and shared corners, ally Cover and Impassable defaults. Fixed illegal diagonal Shift1 to orthogonal1 and moved callout clear of token. Added ranged Power base-dice and harmful LOS-based Power Check Cover effects. Render inspected: six panels and expanded strip fit with clear callout2. Final Typst render inspected with actual bundled sans-serif typography: no clipped text or overlapping boxes. Patterned Cover, Impassable, and Monster marks are distinct; dashed LOS and solid Shift separate clearly. Orthogonal Shift clears the ally.

Sources: 2.7.1, 2.7.2, 2.8.4, 2.9.1, 4.4.4.

### FIG-08

Compared2.7.3,4.5,5.1.1: 13-square Aura2 and 7-square Cone3 masks correct, blocking excludes screened cone square; footprint aura note preserved. Shared-roll flow now redirection/confirmation/all-Reactions/costs before dice; AV-first ordered flat mitigation and no post-roll declaration. Render inspected: all panels and expanded flow boxes fit. Final Typst render inspected with actual bundled sans-serif typography: no clipped text or overlapping boxes. Area hatching and solid Blocking square render correctly; seven cone squares and blocked-square cross visible.

Sources: 2.7.3, 4.5, 5.1.1, 5.4.3, 8.2.

### FIG-09

Compared4.4.6,4.4.7,4.4.10: Push/Pull/Slide direction, costs, no Reflex Attack, last-legal Collision with no inherent damage and ledge edge-point then falling sequence remain correct. Render inspected: paths, ledge dimensions and explanatory paragraphs fit. No content change. Final Typst render inspected with actual bundled sans-serif typography: no clipped text or overlapping boxes. Dotted forced-movement arrows, terrain hatch and edge-point target distinct.

Sources: 4.4.6, 4.4.7, 5.6.1.

### FIG-10

Compared9.3,9.4: Resting default, Guard Point, group placement, five wake-up triggers,6-inch no-LOS and Hidden/Invisible exceptions retained. Render inspected: distance circles and three examples clear. No content change. Final Typst render inspected with actual bundled sans-serif typography: no clipped text or overlapping boxes. Dashed 12-inch ring, solid 6-inch ring, sight lines and wall crosses render clearly.

Sources: 5.9, 9.3, 9.4.

### FIG-11

Compared9.5C-F: added Knocked Out Primary Target melee attack without Engagement and random legal attack selection, including ranged Multi-Attack choice. First valid AI Step, Search and No Visible Target unchanged. Render inspected: expanded outcome boxes and yes/no connectors fit. Final Typst render inspected with actual bundled sans-serif typography: no clipped text or overlapping boxes.

Sources: 3.4.3, 9.5.

### FIG-12

Compared9.5E-F and2.3: nearest visible selection, HP/Most Recent Attacker/random ties and movement priorities retained. Blocked-route example now explicitly says no attack route this activation including Climb/Jump, respecting new automatic Terrain Check success. Render inspected: tie ladder and route caption fit. Final Typst render inspected with actual bundled sans-serif typography: no clipped text or overlapping boxes. Hatched enclosure permits LOS through it; target and route remain readable.

Sources: 9.5, 2.6, 2.9.1, 2.3.

### FIG-13

Five deployment panels inspected: 6-inch edge and 8-inch corner zones, step 7 choice/depth and step 11 alternate placement labels fit; enlarged Hero markers and compact key are clear.

Sources: 10.1, 10.4.

### FIG-14

Four deployment cases inspected: Trail, shared-edge Chasm, enlarged central Safe Zone and Ravine. Nearest opposing edges show 7 inches versus 6-inch limit and 4 versus 3-inch limit; dimensions and keys readable.

Sources: 10.4, 2.6.

### FIG-15

Chasm map, 3-inch objective placements, platform schematic and all eight notes inspected. Failed Jump now ends Prone before gap without Chasm Fall; all forced movement into Chasm, 5.8 Wound/Injuries and removal despite restored HP, and automatic Monster Terrain Checks explicit. Text and key fit.

Sources: 10.4, 4.4.9, 2.3.

### FIG-16

Whispering Grove target arrow, Stone spacing, 4-inch Clearing-edge placement and Warden 2-inch footprint inspected. Entangling Roots automatically Immobilizes; removed DEX Check. Six steps and compact key legible.

Sources: 10.4, 9.5.

### FIG-17

Compared11.2.1-11.2.4: four-phase cycle,4TAP default/Journey override, checklist and six locations remain correct. Render inspected: phase boxes, loop, checklist and location rows fit. No content change. Final Typst render inspected with actual bundled sans-serif typography: no clipped text or overlapping boxes.

Sources: 11.2, 11.2.1, 11.2.3, 11.2.4.

### FIG-18

Appendix A map, relative Wolves inset and fixed Round 1 table inspected against A.4/A.11. Initiative14/10, damage5/6/0 and3/3, final Edric5HP Prone, AP pips and blocked Wolves3/4 match current source; panels and key fit.

Sources: A.

### FIG-19

Appendix B 24-inch map, 4-inch zones, three Resting groups and Satchels, Strongbox and road inspected. Ironscar Speed4 to2 and six-Move minimum and21c sum correct; extraction removes carrier, pickup adjacency/not Engaged and Round6 tie-break now explicit. Text, arithmetic rows and key fit.

Sources: B.

### FIG-20

Shared key inspected: all terrain hatch patterns, Hero/Monster footprints, status rings, arrival/exit arrows and dimension glyphs visible. Orientation, scale, representative counts and steps7/11 default notes fit and match RC512.

Sources: 10.1, 10.4, 2.6, 2.9.1.

### FIG-21

Compared Greenmark 1 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Boar·A, c1, c2, c3, G1·R, G2·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-22

Compared Greenmark 2 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Stone, s2, s3, c1, c2, G1·R, G2·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-23

Compared Greenmark 3 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: W1 · 8" from edge, W2, W3 · 8" from edge, Captain·A, G1·R, G2·R, G3·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-24

Compared Greenmark 4 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: b1, Central Bundle, b3, Brood·A, t1, Tarantula·A, t3. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-25

Compared Greenmark 5 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Clue, k2, k3, k4, c1, c2, G1·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-26

Compared Greenmark 6 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Treant·A, Totem, c1, c2, c3, G1·R, G2·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-27

Compared Ashlands 1 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: pc1, pc2, Lens, u1, u2, u3, Sentinel·A. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-28

Compared Ashlands 2 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Insight, Might, Will, c1, c2, G1·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-29

Compared Ashlands 3 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: G1·R, G2·R, G3·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-30

Compared Ashlands 4 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Dust, dh2, dh3, Codex, Warden·R, Cache, ca2. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-31

Compared Ashlands 5 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Reliquary, Revenants·R, rv2, Bone, bf2, c1, c2. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-32

Compared Ashlands 6 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: bp1, bp2, bp3, Record, c1, c2, G1·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame. Vault Presence correctly absent at setup; first simultaneous all-Broken placement remains a later event.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-33

Compared Undermarches 1 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Node, n1, n2, n4, n5, Lurker·A, G1·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-34

Compared Undermarches 2 setup against RC512 source citations and RC493-to-RC512 diff; 1 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Map, Stone, c1, c2, c3, 1, 2. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-35

Compared Undermarches 3 setup against RC512 source citations and RC493-to-RC512 diff; 1 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Vein, v2, v3, c1, G1·R, G2·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-36

Compared Undermarches 4 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Plans, c1, c2, Commander·A, Guard·A, gd2, G1·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-37

Compared Undermarches 5 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Font, f2, f3, Heart, Shade·A, c1, c2. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-38

Compared Undermarches 6 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Orb, o2, o3, Caller·A, G1·A, G2·R, c1. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-39

Compared Pale City 1 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: c1, c2, c3, c4, c5, G1·R, G2·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame. Moved illustrative walls to give 2.5-inch and3-inch gaps from Buildings, meeting new >2-inch Blocking spacing.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-40

Compared Pale City 2 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Reagent, rc2, rc3, Chest, Golem·A, G1·R, G2·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-41

Compared Pale City 3 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Sarcophagus, sa2, sa3, sa4, sa5, Chest, G1·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-42

Compared Pale City 4 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Conduit, sc2, sc3, sc4, Chest, c2, c3. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-43

Compared Pale City 5 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Wyrm·A, Hoard, c1, c2, G1·R, G2·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-44

Compared Pale City 6 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Bailiff·A, Mephit·A, c1, c2, G1·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-45

Compared Sun-Drowned 1 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Wellspring, c1, c2, c3, Chieftain·A, G1·A, G2·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-46

Compared Sun-Drowned 2 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Locus (Impassable), lc2, lc3, c1, c2, G1·R, G2·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-47

Compared Sun-Drowned 3 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Herald·A, sa1, sa2, sa3, Chest, G1·R, G2·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame. Pressure Plates explicitly remain undrawn until1d3 placement before deployment; new disarm range is outside this setup drawing.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-48

Compared Sun-Drowned 4 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: c1, c2, G1·R, G2·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-49

Compared Sun-Drowned 5 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Rune, Heartstone, c1, c2, G1·R, G2·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame. Inert Colossus is terrain at setup; animated Sz H replacement occurs during play and is not a setup token.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-50

Compared Sun-Drowned 6 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Stone (Impassable), gs2, gs3, c1, c2, Mephit·A, mp2. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-51

Compared The Mire 1 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Reliquary, Leeches·A, c1, c2, c3, G1·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-52

Compared The Mire 2 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Pile, of2, of3, Shaman·A, Swamp Goblins·A, Reeds 1. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-53

Compared The Mire 3 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Geode, ge2, ge3, Titan·A, Reeds 1, G2·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-54

Compared The Mire 4 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Heartwood, c1, c2, Treant·A, Thornlings·A, Vine 1, G1·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-55

Compared The Mire 5 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: Salttide·A, Effigy, ef2, ef3, Croc·A, cr2, c1. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-56

Compared The Mire 6 setup against RC512 source citations and RC493-to-RC512 diff; 2 deployment zones, required objective/Monster placement and status labels checked. Render inspected: hc1, hc2, Hoard, G1·R, G2·R. Terrain patterns, dashed illustrative positions, dimensions, compass and footnotes remain visible within the frame.

Sources: 10.4, 10.1, 2.6, 2.9.1.

### FIG-57

Twelve-step flow and two generic boards inspected. Zones established at step7, 6-inch edge/8-inch corner areas hatched; no obsolete 3-inch edge or6-inch zone bands. Step7 Blocking spacing >2 inches (Grid >2 squares), scenario exceptions and step11 alternating deployment fit.

Sources: 10.1, 2.6.
