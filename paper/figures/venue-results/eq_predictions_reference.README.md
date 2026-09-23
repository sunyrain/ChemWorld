# Approved EQ main-text figure

2026-09-23: the user approved the simplified five-world comparison and requested replacement in the manuscript. The Chinese NCS source uses `eq_predictions_reference.png`; `eq_predictions_reference.svg` retains editable vector elements. These files are exact copies of the approved [preview](../../../output/figures/eq-simple-preview/README.md). The English manuscript uses the same data and approved bar-comparison design, redrawn as editable PowerPoint charts and exported to `../final-ppt/figure05-eq-evidence.png`.

This design replaces the older multi-panel EQ asset in both NCS main texts. The [current PowerPoint figure set](../final-ppt/README.md) incorporates the simplified design. The exact preview copies remain separately reproducible here.

Main Table 1 now carries the three-arm, two-regime MAE/coverage summary as a real table. [Supplementary Table F1](../../venues/ncs/eq_prediction_details.md) preserves all fifteen original prediction intervals and source ranges. Main-text captions distinguish pooled research observations, point predictions, evaluator reference means and three-response aggregates. No result or uncertainty interval was discarded.

To reproduce the approved asset, run `uv run --no-sync python paper/tools/render_eq_simple_preview.py`, then copy the PNG and SVG from `output/figures/eq-simple-preview/eq-predictions-vs-reference.*` to this directory under `eq_predictions_reference.*`. Source values and machine-readable exports are linked from the preview README. This is retained-data figure production, without model or simulator calls.
