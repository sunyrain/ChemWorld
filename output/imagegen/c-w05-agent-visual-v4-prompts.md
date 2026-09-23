# C-W05 visual figure v4 — imagegen prompt set

Built-in image_gen edits. Reference: c-w05-agent-reasoning-v3.png. Final: c-w05-agent-visual-v4.png.

## c-w05-agent-visual-v4-prompt.txt

Redesign the supplied scientific figure to satisfy a strict new requirement: LESS TEXT, MORE VISUAL EXPLANATION, BETTER USE OF SPACE. The supplied image is an edit target and factual source, NOT a layout to preserve. It currently looks like a text-heavy slide with large empty blocks. Replace this with an art-directed, data-rich scientific diagram in which geometry, comparison, miniature protocols, icons and branching structure do most of the communication.

NONNEGOTIABLE STYLE
No decorative crystals, powder, gemstones, realistic instruments, photorealism, 3D, gradients, robot, brain, faces or thought bubbles. Small abstract glyphs are welcome: categorical material tokens, droplets for solvent categories, seed dots, temperature-program paths, measurement crosshairs, a padlock for fixed conditions, a check/cross for quality. Every mark must encode a scientific variable or relationship, never filler.
White background, dark charcoal typography, thin precise vector-like strokes, restrained blue for the 12-batch campaign and teal for the 24-batch campaign; amber means quality failure. Small panel letters, editorial typography, minimal card framing, no giant colored rounded rectangles. Use the full canvas intelligently, with consistent narrow gutters and small margins, but keep good local separation. Roughly 70% diagrams/charts and 30% short labels or less. NO explanatory paragraphs. High-resolution landscape 3:2.

HEADER, small and compact:
"From experiments to scientific inference"
"C-W05 | Independent 12- and 24-batch campaigns"
One thin objective line, with small target symbol:
"Recovery ↑    Purity ≥ 80%    Fines ≤ 50%"
Define in very small type: "Fines: particles <20 µm"

MAIN GRID: three full-height vertical regions a, b, c, about 35%, 43%, 22% of available width. All regions should contain useful visual content throughout their height, without empty lower-right areas. Do not draw large surrounding boxes. Let aligned elements and short headings establish structure.

REGION a — "Experimental choices"
Two parallel vertical research paths, independently starting at the top, labelled "12 batches" and "24 batches". NEVER connect the two paths as a continuation. Use bold readable batch-range labels, mostly iconographic phase glyphs, at most 1–3 descriptive words per phase.

12-batch blue path, five vertically connected stations:
"1–4" with small categorical token comparison glyph; label "Catalysts"
"5–7" with small categorical solvent-droplet grid; label "Solvents"
"8–10" with a descending temperature-endpoint glyph; label "Cooling endpoint"
"11" with seed dots and a plus sign; label "Seed amount"
"12" with three measurement crosshairs along a cooling/hold program; label "Measurements"
At bottom, an outlined selection badge "Selected: 10".

24-batch teal path, five stations:
"1–6" with material-token grid; label "Materials"
"7–18" with small parameter dials and alternative cooling glyphs; label "Process variation"
"19" with a tall short heating-program glyph followed by a direct-cooling glyph; label "Hot / short"
"20" with a hotter short heating-program glyph followed by a stepwise cooling glyph; label "Staged cooling"
"21–24" with a small local parameter-search glyph; label "Refinement"
Amber brace alongside stations 1–18 labelled simply "Quality fails".
Small amber cross at 19 and small teal check at 20.
At bottom selection badge "Selected: 23".
Stage icons are category/protocol symbols, NOT fabricated measurements. No tiny repeated prose boxes.

Use the lower portion of region a for a COMPACT WITHIN-BATCH VISUAL:
Header "12-batch run · batch 12"
Three distinct process landmarks with measurement symbols:
"280 K" → "250 K" → "Hold".
Immediately below their measurement symbols, the exact fines readings:
"40.6%" → "36.2%" → "35.2%".
Label the data "Measured fines".
Do not draw invented distribution histograms. Use clearly labelled measured points or a sparse three-point progression, no physical-time axis.
An unobtrusive footnote for region a: "Two separate sessions".

REGION b — "Evidence → interpretation"
This is the largest and most visual region. Its TOP HALF presents three aligned rows of actual experimental programs and the observed fines results, so the reader can SEE why the agent considered process history important.

Heading "Recorded programs" and tiny qualifier "Requested settings; schematic".
Columns or aligned subregions: "Batch" | "Heat" | "Cool" | "Fines".
Rows:
14: heat target "370 K", duration "60 min"; cooling targets 310 → 300 → 290 → 280 → 270 → 260 K; observed fines 55.1%.
19: heat target "390 K", duration "30 min"; direct cooling target 260 K; observed fines 52.8%.
20: heat target "410 K", duration "20 min"; cooling targets 320 → 290 → 260 K; observed fines 21.5%.

VISUAL ENCODING: show heat as three schematic pulses, first lower/longer, second higher/shorter, third highest/shortest, annotated by the exact targets and durations. These are PROGRAM SCHEMATICS, not measured temperature curves; label accordingly. For cooling use an elegant staircase path for row 14, one downward transition for row 19, and three steps for row 20. Label final temperature "260 K" at each path end; optional small intermediate labels only if legible. The exact sequence is above and must not be changed.
Fines are shown as horizontal mini-bars on ONE SHARED ZERO-BASED SCALE, 0 to 60%. Put one clearly labelled vertical dashed threshold at 50% across all three rows. Bar lengths must be proportional to 55.1, 52.8, 21.5. Exact labels at bar ends: "55.1%", "52.8%", "21.5%". First two amber with small x, last teal with a check. Label threshold "Limit 50%". This is a visual scientific comparison, not a prose table.

Below this program comparison, a fine grouping arrow leads to the AGENT'S REPORTED INTERPRETATION, not a hidden-thought trace:
Small heading "Post-campaign reasoning".
A triangular dependency sketch with three nodes labelled "Reaction", "Seed entry", "Cooling", joined by dashed connections and a central "?". A compact label above or below: "K1: process history".
Small nearby label "Effects not isolated".
This diagram represents the agent's interpretation and uncertainty, not proven causal edges.

BOTTOM of region b: a visual proposed controlled comparison, headed "K2: proposed test — NOT RUN".
A padlock icon plus label "Same batch-23 upstream recipe".
A single input line splits into two thin contrasting cooling paths:
TOP: three-step path labelled "Staged", ending at 250 K; small label "Observed recipe".
BOTTOM: one direct downward path labelled "Direct", ending at 250 K; small label "Proposed".
The lower unexecuted route MUST use dashed strokes and end in an outlined "?" readout. Never assign it a made-up numerical result.
Below that question readout, two compact hypothetical branches:
"Quality retained" → small tag "Upstream favored"
"Fines rise" → small tag "Cooling matters".
Keep these phrases short. This is the agent's retrospective proposal, not a completed extra experiment.
NO arrows from prediction evaluations back into the reasoning diagram.
This whole bottom graphic should replace long K1/K2 prose.

REGION c — "Outcome"
Replace the old two tables by FOUR small paired horizontal bar charts, arranged top to bottom and occupying the full region height. Use a tiny common legend: blue "12 batches", teal "24 batches". Include exact labels at bar ends. No statistical error bars, no invented uncertainty, no significance stars.

Group heading "Recipe retest".
Chart 1: "Recovery ↑". Blue 50.4%, teal 58.1%. Common zero-based percent scale.
Chart 2: "Fines ↓". Blue 46.2%, teal 19.3%. Common zero-based percent scale. A small "Both feasible" label below. The higher recovery and lower fines should be visible from length differences.

Group heading "New-condition prediction".
Subtitle "MAE ↓".
Chart 3: "Recovery". Blue 0.1153, teal 0.0593.
Chart 4: "Purity". Blue 0.0112, teal 0.0648.
Use the SAME ZERO-BASED AXIS 0 to 0.12 for both error charts, with simple ticks 0, 0.06, 0.12. Keep the bars proportional and the literal labels exact. Blue and teal continue to identify budgets, even where teal is worse. Add only a small directional text "better" for recovery and "worse" for purity; no long conclusion paragraph.
Small final visual shorthand, if room: "Recipe ↑   Prediction ±".
Do not leave a giant empty rectangle under the data. Space charts evenly and compactly.

ONLY FOOTER, one short sentence:
"Selected case. Reasoning summarizes post-campaign reports; immediate thoughts were not logged. Proposed test not executed."

Do not repeat the full explanatory sentences from the old image. Aim for exceptionally clear, professional VISUAL REASONING: program contrasts, an explicit quality threshold, coupled-factor uncertainty, and a controlled-test branch. Accurate labels and graph proportions are essential. No crystal art anywhere.


## c-w05-agent-visual-v4-data-fix-prompt.txt

Make ONLY the following precise scientific corrections to the supplied figure. Preserve its overall layout, all diagrams, all other labels, typography, style and every other data value.

1. In panel b, the three horizontal Fines bars and the 50% limit line are inconsistent: the 55.1% and 52.8% bars currently stop before the 50% dashed limit. Correct the bar geometry. Keep the shared horizontal axis ranging from 0 to 60%. Keep the limit at exactly 50%, which is 5/6 of the distance from the 0 origin to the 60% endpoint.
- Batch 14 bar must extend from 0 to exactly 55.1%, i.e. 91.833% of the full 0–60 plotting width. It visibly CROSSES the 50% dashed line. Amber bar, exact value "55.1%", small x.
- Batch 19 bar must extend from 0 to exactly 52.8%, i.e. 88% of the full 0–60 plotting width. It also visibly CROSSES the 50% dashed line, and is slightly shorter than the batch 14 bar. Amber bar, exact value "52.8%", small x.
- Batch 20 bar extends from 0 to exactly 21.5%, i.e. 35.833% of the full 0–60 plotting width. It ends well BEFORE the 50% limit. Teal bar, exact value "21.5%", small check.
Make these endpoints mathematically consistent with the axis ticks. If needed, put the numeric labels just BELOW their bars to avoid text overlap with the limit line, but do not alter any numbers.
This correction applies ONLY to the central Fines graph. The four right-hand Outcome charts are already correct; do not touch them.

2. In the lower panel-b K2 diagram, the small top-right solid observed-result box currently says "(observed result)" and shows an uninformative tilde "~". Replace only those contents with "Observed fines" and "14.2%". This is the source result for the observed staged-cooling recipe in batch 23. Keep the proposed direct-cooling result as an EMPTY dashed question-mark box, with no value. The proposed experiment was NOT RUN.

Do not change any other content, any batch labels, or any process paths. Do not redesign anything else.
