# C public-baseline reanalysis

All 30 baselines are available: two omissions repaired and all 28 previously available results reproduced exactly. No provider or simulator calls; retained inputs unchanged.

Rejected resource requests consume attempts but do not add material to the executed recipe. The extractor retains them as rejection provenance. Unknown statuses still fail.

Original failures remain in `summary.json` and in each correction row. The current programme inventory explicitly consumes this correction; historical source results and release bindings are unchanged.

| Repaired source | Original failure | Training final assays |
|---|---|---:|
| C-W02-B12-E-Opaque | Unknown transaction status at step 145: campaign_resource_rejected | 11 |
| C-W05-B24-E-MisIndexed | Unknown transaction status at step 378: campaign_resource_rejected | 24 |

## Prediction comparison

Both baselines fit only the source's public final observations. Saved query truth is used only for evaluation. They are simple references, not an optimal system-identification algorithm. All four metrics and both budgets are shown.

| Budget | Metric | Agent MAE | Mean MAE | Nearest MAE | Agent wins vs mean | Agent wins vs nearest |
|---|---|---:|---:|---:|---:|---:|
| 12 | crystal_fines_fraction | 0.30999 | 0.31946 | 0.31877 | 9/15 | 9/15 |
| 12 | crystal_purity | 0.05029 | 0.00475 | 0.00783 | 0/15 | 2/15 |
| 12 | crystal_size | 0.07085 | 0.02114 | 0.02520 | 0/15 | 2/15 |
| 12 | crystal_yield | 0.10433 | 0.19196 | 0.19000 | 13/15 | 13/15 |
| 24 | crystal_fines_fraction | 0.27000 | 0.31357 | 0.32975 | 12/15 | 11/15 |
| 24 | crystal_purity | 0.03679 | 0.00489 | 0.01027 | 0/15 | 2/15 |
| 24 | crystal_size | 0.06762 | 0.02577 | 0.02896 | 4/15 | 5/15 |
| 24 | crystal_yield | 0.07937 | 0.15075 | 0.15617 | 13/15 | 13/15 |

Five physical world clusters underlie each budget, with three arms each; the fifteen cells are not fifteen independent worlds. C-W02/12/Opaque remains an eleven-assay source. Its valid observations are used without imputation. The nearest-neighbor recipe representation is retained unchanged and is limited; poor baseline performance does not establish mechanistic understanding.
