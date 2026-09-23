# C-W05 clean portrait v7 — imagegen prompt set

Built-in image_gen edits. Reference: c-w05-agent-portrait-v6.png. Final: c-w05-agent-portrait-v7-clean.png. Final outcome comparisons use paired numeric values instead of generated quantitative bar lengths.

## c-w05-agent-portrait-v7-clean-prompt.txt

Restyle the supplied portrait scientific figure into a clean, restrained, publication-style figure. This is a STYLE EDIT, not a change of scientific content or structure. Keep the portrait 2:3 canvas, the four sections a–d, the left 12-batch versus right 24-batch comparison, all experimental stages, all agent-consideration notes, all recorded actions, every numerical value and unit, recipe selection, chart labels, and reconstruction caveats.

The user wants it clean and quiet, with much less module background color and without a generic AI-generated infographic aesthetic.

ART DIRECTION:
Think a carefully typeset research figure drawn by a scientific illustrator: white paper, near-black type, precise hairline rules, consistent restrained stroke weight, compact neutral Helvetica/Arial-like type. Almost monochrome except sparse muted blue and desaturated teal to distinguish the two campaigns and chart series. A little muted rust may flag the failed fines constraint. 90–95% of background area should be plain white. No gradients or shadows anywhere. No glowing edges, gloss, decorative shapes, colorful sticker badges, UI cards, shiny icons, oversized marketing numerals, or heavy bold title. Do not add crystal or laboratory artwork.

SPECIFIC CHANGES:
1. Delete ALL blue, teal, pale-blue, pale-green, pink, purple and orange background fills from modules, results, recipes and the bottom takeaway. Replace with pure white. Remove the rounded rectangular enclosing borders around modules and whole sections. Group content with alignment and a few very thin light-grey separators instead.
2. Replace thick blue/teal section banners with plain dark headings on white. Campaign colors may appear as one short thin underline or a tiny color key only. Repeated large color blocks must disappear.
3. The section letters a, b, c, d become small plain lowercase bold letters on white, with no filled circles. The numbered 1–4 process badges become small grey numerals without circles. Main title becomes smaller, medium-weight, left-aligned, not a giant centered headline.
4. Replace the filled chevron research-stage ribbons with fine horizontal timeline lines, small ticks and the SAME batch-range and stage labels. Keep the 12-batch and 24-batch trajectories separate. Use understated monochrome line symbols rather than bright colored icon art. Preserve all five stage ranges per campaign.
5. All numerical readouts remain exactly the same, but are dark, sober typographic data labels rather than large neon-blue dashboard numbers. Use only a subtle accent for 52.8% failing the 50% threshold and for 21.5% passing it.
6. Remove filled checkmark medallions and warning triangles. Use a tiny simple tick or x beside the same short quality-status text, in grey/teal or muted rust. Do not remove pass/fail information.
7. Keep the idea of a simple Agent considering observations. Make each Agent icon a small, thin outlined abstract node or understated simple outline glyph, labelled "Agent". Remove the cartoon-like large face and speech-bubble styling. Put each EXISTING short consideration sentence alongside the Agent as a two-line annotation, connected by a fine leader or bracket. The flow observation → consideration → actual action → result must remain obvious. Preserve "Consideration*" and the clear illustrative-reconstruction note. Do NOT invent or rewrite thoughts.
8. Operation diagrams become precise dark-grey line drawings with fine arrowheads and sparse blue/teal highlights. Temperature targets must remain correct. The 12-batch example is a change of endpoint from batch 9 at 260 K to batch 10 at 250 K, NOT staged cooling within one experiment. The 24-batch example retains the actual 390 K / 30 min to 410 K / 20 min change and direct-to-staged cooling 320 → 290 → 260 K.
9. The selected-recipe strips should use plain text and small line symbols joined by thin arrows, not colored rounded buttons. Preserve S1/C3 versus S2/C1, 360 K · 60 min versus 450 K · 15 min, 20 mg versus 50 mg seed, direct 250 K versus 310 → 280 → 250 K, and quench only where present. Keep the requested-heat-target caveat.
10. Bottom charts: flat muted blue and muted teal bars, light grey axes, no gradient fill or panel-colored background. Keep all numbers, scales and series identities. Keep the comparison easy to read, not decorative.
11. The bottom takeaway becomes a simple one-line small/medium-weight sentence on white, separated by a thin rule if needed. Keep footnotes readable and discreet.
12. Reduce visual noise while retaining moderate explanatory text and useful diagrams. Use whitespace as narrow consistent separation, not as giant empty regions. The page should look like a journal figure, not a presentation dashboard.

SCIENTIFIC INVARIANTS:
Feasible counts 10/12 and 5/24; first feasible batches 1 and 20.
Examples: batches 9→10 and 19→20; selected recipes 10 and 23.
Observed source values: 49.8%,42.4% → 51.2%,45.7%; 49.0%,52.8% → 52.9%,21.5%.
Independent retest: recovery 50.4% versus 58.1%; fines 46.2% versus 19.3%.
Prediction MAE: recovery 0.1153 versus 0.0593; purity 0.0112 versus 0.0648.
Preserve exact values and don't reverse arrow directions or budget labels. Maintain both the independent-session statement and the note that immediate thoughts were not logged.

This edit should feel elegantly simplified, sober and human-designed, while preserving the useful detail of the existing portrait figure.


## c-w05-agent-portrait-v7-chart-fix-prompt.txt

Keep the entire supplied clean portrait figure EXACTLY unchanged except the bar lengths in the two bottom-right prediction-error charts. This is a precise scientific correction, not a redesign. Preserve all typography, colors, text, numbers, axes, positions, strokes, white background and every other element.

In panel d, under "Predictions for new conditions · MAE":
RECOVERY chart:
The horizontal axis runs from 0 to 0.12, with ticks 0.03, 0.06, 0.09, 0.12.
The BLUE "12 batches" bar labelled 0.1153 must extend from zero to 0.1153, which is 96.083% of the full axis length: its right edge must be just slightly LEFT of the 0.12 tick. It is currently too short.
The TEAL "24 batches" bar labelled 0.0593 must extend from zero to 0.0593, which is 49.417% of the full axis length: its right edge must be just slightly LEFT of the 0.06 tick.
Move the value labels beside the corrected ends without changing their numbers. Keep the small better annotation.

PURITY chart:
Same zero-based 0–0.12 axis.
BLUE "12 batches" 0.0112 must have length 9.333% of the full axis, ending just over one-third of the way from 0 to the first 0.03 tick. It is currently too long.
TEAL "24 batches" 0.0648 must have length 54% of the full axis, ending slightly RIGHT of the 0.06 tick.
Move labels alongside corrected bar ends. Keep the worse annotation.

For orientation in this 1024-pixel-wide reference: the recovery zero is approximately x=594 and its 0.12 tick approximately x=726, so corrected recovery endpoints are approximately x=721 and x=659. The purity zero is approximately x=823 and its 0.12 tick approximately x=975, so corrected purity endpoints are approximately x=837 and x=905. Use the axis proportions as the scientific authority if output resolution differs.

Do not touch the two independent-retest percent charts at bottom left. Do not change anything outside these four prediction-error bars and their adjacent value-label positions.


## c-w05-agent-portrait-v7-paired-values-prompt.txt

Edit ONLY section d at the bottom of the supplied clean portrait figure. Keep sections a, b, c, title, footer, typography, scientific data and all other content exactly unchanged.

In section d, REMOVE the four bar charts entirely, including all colored bars, axes, tick marks and numeric ticks. Replace them with compact, unscaled PAIRED NUMERICAL COMPARISONS. This avoids misleading generated bar proportions and is stylistically cleaner. Do not draw any length-encoded or position-scaled data marks.

Keep "Compare final outcomes", its blue "12 batches" and teal "24 batches" legend, the left group heading "Independent recipe retest", and the right group heading "Predictions for new conditions · MAE ↓". Keep the white background and thin grey rules. No colored panel backgrounds.

Within the LEFT group, use two simple metric rows, with column headings "12 batches" and "24 batches":
Recovery ↑          50.4%          58.1%
Fines ↓             46.2%          19.3%
Values for 12 batches are restrained blue; values for 24 batches restrained teal. Align the numerals precisely, moderate font size. Keep the short note "Both recommendations feasible." Do not surround cells with boxes or grid lines.

Within the RIGHT group, same column headings "12 batches" and "24 batches":
Recovery            0.1153         0.0593     ↓ better
Purity              0.0112         0.0648     ↑ worse
Blue for 12-batch numbers, teal for 24-batch numbers. The small "better" label can be teal; "worse" can be muted rust. The up/down arrows indicate change in prediction error, not a scaled measurement. Keep columns and rows aligned.

This bottom section must remain visually balanced and quiet, fitting in its existing vertical space. Use small line separators only where necessary, no large table borders, no graphics with a quantitative length. Preserve the concluding sentence below this section unchanged. Everything above section d MUST stay unchanged.
