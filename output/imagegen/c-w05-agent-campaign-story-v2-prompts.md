# C-W05 story figure v2 — imagegen prompts

Built-in image_gen generation and editing. Reference: c-w05-agent-campaign-sample-schematic.png. Final: c-w05-agent-campaign-story-v2.png.

## c-w05-agent-campaign-story-v2-prompt.txt

Redesign the supplied figure substantially to make the scientific story understandable from the picture ALONE. The reference is an EDIT TARGET and evidence reference, not a layout to preserve. Its problem is that it inventories operations without clearly connecting GOAL → AGENT CHOICES → OBSERVED OUTCOME → NEW TESTS. Solve that visual communication problem. Create one polished top-journal scientific sample figure, landscape 3:2, high resolution, English text.

ART DIRECTION
Quiet white background; refined sans-serif typography; ample whitespace; small lowercase panel letters; consistent fine strokes. Abstract scientific icons, not realistic instruments. Blue for agent choices and measurements; amber for product-quality failure; teal for satisfying quality constraints; red only for a rejected command. Elegant few translucent geometric crystals, no photographic equipment, metal fittings, control panels, robot, human, brain or decorative molecule wallpaper. No sprawling serpentine hardware pipelines. Use clear conceptual grouping, direct labels, short arrows, and local explanations. Four panels arranged: a thin full-width top explanatory band; b the main middle region spanning about 72% width; c two compact process zooms below b; d a clear right-hand evaluation column spanning b+c height. Use readable concise text and space generously. Do not use an enormous title or huge takeaway consuming the figure.

TITLE: "Better crystal production, uneven prediction"
SUBTITLE: "Two independent agent campaigns in the same simulated world | C-W05 | Aligned information"

PANEL a — "What is the agent trying to do?"
Left: a small elegant contrast of usable crystals versus excessive powder, purely schematic.
Text: "Recover more target as usable crystals"
A prominent objective rule: "Purity ≥ 80%   AND   Fines ≤ 50%"
Definition: "Fines = particles smaller than 20 µm"
Right: an explicit compact AGENT–LAB loop with three clearly labelled nodes:
"Agent chooses" → "Lab executes" → "Agent observes".
Under chooses, small words "Materials · amounts · operations · measurements".
Under observes, small words "Readouts · errors · product quality".
A returning arrow from observes to chooses labelled "Next batch". A separate exit labelled "After the final batch: recommend + predict".
This is a campaign-level loop, not a claim that batch 12 continues to batch 13. All measured readouts and tool feedback come from the simulated lab; do not depict hidden reasoning.

PANEL b — "How the research paths differ"
Two clearly separate lanes, both starting on the left. Label them "12-batch campaign" and "24-batch campaign". Caption between/under them: "Separate sessions; the 24-batch campaign is not an extension."
Use grouped phase blocks, not dozens of tiny numbered circles.

12-batch lane has these FIVE action blocks linked left to right:
"Batches 1–4" / "Compare catalysts"
"Batches 5–7" / "Compare solvents"
"Batches 8–10" / "Lower cooling endpoint"
"Batch 11" / "Increase seed amount"
"Batch 12" / "Measure within a batch"
This lane is blue-neutral, not all marked as failures or successes.
At its end put an explicitly separate small recommendation label, "Recommended recipe: batch 10".
A precise magnification connector from the "Batch 12" block leads to the first process zoom in panel c; its title repeats "12-batch campaign • batch 12". Distinguish it from recommended batch 10. Not every illustrated batch is the recommended one.

24-batch lane has these FIVE blocks:
"Batches 1–6" / "Explore materials"
"Batches 7–18" / "Vary dose, cooling and ageing"
"Batch 19" / "Hotter, shorter reaction"
"Batch 20" / "Change heating + staged cooling"
"Batches 21–24" / "Refine the feasible procedure"
Give batches 1–18 a simple brace "Product quality still fails".
Under batch 19 show a small amber badge "Fines 52.8% > 50%" and clearly "FAIL".
Under batch 20 show a small teal badge "Fines 21.5% ≤ 50%" and clearly "FIRST PASS".
The pass also satisfies the purity requirement; don't imply fines is the only constraint.
At the lane end: "Recommended recipe: batch 23".
A precise magnification connector from this recommendation leads to the second process zoom titled "24-batch campaign • batch 23".
This is the narrative pivot: repeated quality failure followed by a change in combined procedure and a feasible product. Do not claim the effect of heating or cooling was isolated experimentally.

PANEL c — "What happens inside a batch?"
Two compact side-by-side, explicitly partial operation zooms. Short heading beneath panel title: "Selected recorded operations".

FIRST ZOOM: "12-batch campaign • batch 12"
Short question: "How does particle size change during the procedure?"
Three simple vessel/readout pairs left-to-right:
"Cool to 280 K" → "Cool to 250 K" → "Age"
Each is followed by a small abstract measurement symbol, visibly indicating a measurement was taken at each point.
Their exact observed readouts:
"Fines 40.6%"    "Fines 36.2%"    "Fines 35.2%".
Use large percentages and no fake distribution histograms. A tiny line after the sequence: "Then filter and assay". Do not add a next-batch loop to this last batch. Crystal illustrations are schematic, not actual microscopy.

SECOND ZOOM: "24-batch campaign • batch 23"
Short question: "How does the agent handle tool feedback?"
A compact abstract sequence:
"Heat" with "450 K requested / 413.84 K reached"
→ "Quench + seed".
Then fork cleanly:
A dashed red rejected branch labelled "340 K cooling request" and "REJECTED: no state change", ending with an x.
The executed solid blue route is "310 K → 280 K → 250 K" labelled "Executed cooling stages".
Then "Age → Filter → Assay".
Keep the rejected request separate from the actual temperature path.
No need to repeat final source-batch values here; those are distinct from the independent retest in panel d.

PANEL d — "Does the result transfer?"
Create two plainly separated sections, with readable column headings "12 batches" and "24 batches".

First question: "1. Does the recommended recipe work?"
Subtitle: "Independent retest"
Two tidy rows:
"Crystal recovery ↑"    "50.4%"   "58.1%"
"Fines ↓"               "46.2%"   "19.3%"
A small teal line: "Both recipes pass the quality limits".
Use schematic small crystal shapes sparingly. The ↑/↓ denote desirable direction, not a third numerical data point.

Second question: "2. Can it predict new conditions?"
Subtitle: "Prediction error (MAE; lower is better)"
Two rows:
"Recovery"  "0.1153"  "0.0593"   with small teal "Improves".
"Purity"    "0.0112"  "0.0648"   with small amber "Worsens".
All values are exactly as above; do not turn prediction errors into purity outcomes or percentages.
No invented graph, error bar or statistical significance.

A modest concluding line, not a giant slogan:
"A better recipe does not ensure better predictions for every property."

FOOTER:
"Selected example, not an average effect. Stage labels summarize actions; immediate decision rationales were not recorded."
Small tag: "Schematic illustration of simulated experiments".

Ensure a reader can immediately identify: the objective, what the agent controls, why batches 19 and 20 differ, how choices expand into operations and measurements, and why operational achievement differs from predictive knowledge. The figure must visually EXPLAIN rather than merely list. Do not add unspecified measurements, hidden agent thoughts, causal isolation, extra experiments, exact crystal-size distributions, or links between the independent sessions. Prioritize clarity and scientific accuracy over retaining the old composition.


## c-w05-agent-campaign-story-v2-clarity-edit-prompt.txt

Make a strictly local clarity correction to this scientific figure. Preserve all layout, colors, illustrations, typography, batch ranges, numerical values, operation arrows within the process insets, and all other content.

1. DELETE the blue dashed connector and its text "Zoom in (panel c, left)" between the upper 12-batch lane and lower 24-batch lane. It currently points misleadingly at batch 20. Also DELETE the orange/red dashed vertical zoom connector and its text "Zoom in (panel c, right)". These two zoom leaders must be completely absent. Do not remove any genuine arrows connecting sequential experimental blocks, any agent-lab loop arrows, or the red rejected-command branch inside panel c.

2. Replace the removed leaders with explicit MATCHING SMALL BADGES, no connector lines:
Place a small navy circular badge containing "i" at the top-right corner of the "Batch 12 / Measure within a batch" block in panel b.
Place an identical navy "i" badge immediately before the title "12-batch campaign • batch 12" of the left panel-c inset.
Place a small teal circular badge containing "ii" at the top-right corner of the "Recommended recipe: batch 23" box in panel b.
Place an identical teal "ii" badge immediately before the title "24-batch campaign • batch 23" of the right panel-c inset.
These exactly paired badges identify the magnified examples without crossing between independent campaigns.

3. Under the "12-batch campaign" lane label change "(12 independent batches)" to "(budget: 12 batches)".
Under the "24-batch campaign" lane label change "(24 independent batches)" to "(budget: 24 batches)".
Keep the explicit separate-sessions sentence unchanged.

4. In panel a, remove the unsupported descriptive text "(high purity, larger size)" below "Usable crystals", and remove "(low value, < 20 µm)" below "Excessive powder". Relabel those two illustrations simply "Crystals" and "Excess fines". The adjacent existing definition "Fines = particles smaller than 20 µm" already explains the size meaning. Do not equate larger crystals with higher purity.

5. Change panel d title from "Does the result transfer?" to "What did the agent achieve?"
Change the prediction subtitle "Prediction error (MAE; lower is better)" to "Mean absolute error; lower is better".

Everything else must remain unchanged, especially all fractions/percentages, the 19/20 FAIL/FIRST PASS comparison, and 340 K being rejected rather than executed.


## c-w05-agent-campaign-story-v2-label-fix-prompt.txt

One tiny text correction only. In panel b, in the TOP BLUE 12-batch campaign lane, locate the FOURTH action box, immediately after "Batches 8–10 / Lower cooling endpoint" and immediately before the highlighted "Batch 12 / Measure within a batch" box with the navy i badge. That fourth box has a simple flask icon and was accidentally duplicated as Batch 12. Change ONLY its heading to "Batch 11" and its description to "Increase seed amount". Keep its flask icon, position, dimensions, border and arrows unchanged. The next fifth box MUST remain "Batch 12 / Measure within a batch" with its i badge. The correct full sequence of headings in the blue row is: Batches 1–4, Batches 5–7, Batches 8–10, Batch 11, Batch 12, Recommended recipe: batch 10. This correction applies ONLY to the fourth box. Do not change ANY other text, number, icon, image element, layout or style in the entire supplied figure.
