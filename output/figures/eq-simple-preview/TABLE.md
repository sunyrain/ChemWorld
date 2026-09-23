# Table. Equilibrium prediction performance across test regimes

| Information arm | Macro MAE: other nine | Macro MAE: dilute three | 80% interval coverage: other nine | 80% interval coverage: dilute three |
| :--- | ---: | ---: | ---: | ---: |
| Opaque | 0.01008 | 0.01833 | 90.7% | 93.3% |
| Aligned | 0.00465 | 0.15862 | 91.3% | 2.2% |
| MisIndexed | 0.00439 | 0.14397 | 89.6% | 13.8% |

Values are means over five worlds per arm and aggregate three response targets (normalized pH, acid dissociation fraction and precipitation signal). The figure separately shows only dissociation at the single most dilute recipe.

The dilute group contains the three lowest nominal-concentration recipes (Q03, Q08, Q09); the other nine queries include boundary conditions and are not all interpolation. Grouping was performed post hoc. Macro MAE is calculated against the original five-observation reference means. Coverage uses all reference observations: 225 judgments per arm for the dilute group and 675 for the other nine. These are not independent world replicates.

Compared with Opaque, Aligned has lower MAE on the other nine queries and higher MAE on the dilute three in each of the five worlds. The ratio of the across-world mean MAEs corresponds to a 53.9% reduction on the other nine and 8.65 times the error on the dilute three. This is a full-process contrast, not a causal attribution to an internal reasoning mechanism.

Source: [retained regime analysis](../../../workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921/STORY_WORLD_ANALYSIS.json).
