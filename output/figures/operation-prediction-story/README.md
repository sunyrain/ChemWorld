# Operation and prediction: four-panel manuscript figure

2026-09-23. Replaces the signed-delta scatterplot in English Figure 3 and Chinese
Figure 2. Both manuscripts use the same vector asset. This is a retained-data
editorial replot, with no new model or simulator calls.

## Reading sequence

- **a: Does optimization improve the delivered recommendation?** Five-world
  electrochemical retest means compare discovery with optimization directly.
  The overall mean rises from 0.54270 to 0.70598; 26/30 matched pairs improve.
- **b: Do the same campaigns also predict better?** The same world grouping and
  goal colours show score-prediction MAE. Overall means are 0.14300 and 0.14315;
  only 14/30 pairs improve. Close overall means are not an equivalence test.
- **c: How do the two endpoints combine?** All four outcome categories are
  retained for electrochemistry and reaction processing. The latter provides a
  boundary: optimization is not consistently better even at delivery.
- **d: Is the electrochemical discordance confined to one world?** Counts of
  better-retest/worse-prediction pairs are 3/6, 2/6, 3/6, 1/6 and 4/6.

Panels a/b are descriptive means of six campaigns per goal and world; c/d count
the original paired outcomes, not directions inferred from those means. Bars
start at zero. Colours separate goals in a/b and systems in c, with local
legends. Regular-weight Arial and lowercase panel letters match the current
manuscript figures. There is no decorative title block or slide footer.

## Exact counts and scope

| Optimization relative to discovery | Electrochemistry | Reaction processing |
|---|---:|---:|
| Both better | 13/30 | 4/30 |
| Better retest, worse prediction | 13/30 | 5/30 |
| Worse retest, better prediction | 1/30 | 4/30 |
| Both worse | 3/30 | 17/30 |

The 120 campaigns produce 60 matched pairs. Electrochemical pairs cover five
worlds, three arms and two budgets at the entity prior locus. Reaction-processing
pairs cover five worlds, three arms and two prior loci at twelve batches.
Comparisons fix world, arm, budget and locus. Pairs share worlds; they are not
sixty independent world replicates. Classification uses the strict sign of
each difference, without a significance or minimum-effect threshold. There are
no exact ties. Full magnitudes are retained in the paired CSV.

The electrochemical sensitivity excluding infrastructure-driven source restarts
retains 17 pairs: 15 better retests, eight better forecasts and seven
better-retest/worse-prediction outcomes. These counts remain in both Results
sections. Reaction processing's six-response macro error is a separate endpoint
from score MAE; its 6/30 improvement count remains in the text. Purification
remains in the text and Supplementary Fig. S5a (English) / S6a (Chinese).

The figure contrasts complete autonomous research processes. It does not
identify internal beliefs or separate experiment selection from inference.

## Data, assets and rebuild

Inputs are the retained
[`campaign_metrics.csv`](../../../paper/figures/integrated-results/campaign_metrics.csv)
and [`analysis.json`](../../../paper/figures/integrated-results/analysis.json).
The renderer reconstructs every pair and checks both numerical deltas against
the retained analysis to absolute tolerance 1e-12, then checks all counts and the
restart sensitivity.

- [Full paired values](all-60-pairs.csv)
- [World means](world-means.csv)
- [Machine summary](summary.json)
- [Preview](operation-prediction-four-panels.png)
- [Vector PDF](../../../paper/figures/venue-results/figure03-operation-prediction.pdf)
- [Editable SVG](../../../paper/figures/venue-results/figure03-operation-prediction.svg)
- [Publication PNG](../../../paper/figures/venue-results/figure03-operation-prediction.png)

From the repository root:

```powershell
uv run --no-sync python paper/tools/render_operation_prediction_story.py
```

The authoritative captions are next to the figure in
[`article.md`](../../../paper/venues/ncs/article.md) and
[`ChemWorld_NCS_中文正文_v1.md`](../../../paper/venues/ncs/ChemWorld_NCS_中文正文_v1.md).
The old combined PowerPoint slide remains historical and is not the current
manuscript asset.

Both manuscripts were rebuilt and visually checked: the English edition has
35 pages with this Figure 3 on page 6; the Chinese edition has 38 pages with
this Figure 2 on page 5. Their figure/table counts remain unchanged. No missing
glyphs, undefined citations or overflow warnings were reported.
