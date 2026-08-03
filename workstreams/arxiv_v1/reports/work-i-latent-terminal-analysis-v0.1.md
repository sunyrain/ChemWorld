# Work I Latent-Terminal Formal Analysis

Status: **incomplete_full_report_required**

Analysis SHA-256: `548f8cd8d7d108773f19f6f0eb44c4b1eacd690eaa141ace4d5b62b94ff63934`

## Frozen result

The formal gate did not pass: 6 of 36 shadow receipts resolved and 30 remain unresolved. Terminal quality is therefore unresolved. All latent-dependent primary point estimates are withheld; the six resolved rows are retained only inside registered observed-only diagnostics and bounds.

No formal assay was rerun or replaced. The analyzer made zero agent/provider calls and executed zero shadow evaluations.

## Registered continuous bounds

| Estimand | Fixed denominator | Primary point | Sharp mean bound |
| --- | ---: | --- | --- |
| Latent terminal score | 36 | withheld | [8.5863e-05, 0.833419] |
| Discard - observed-best delta | 36 | withheld | [-0.276951, 0.556382] |
| Positive discard regret | 36 | withheld | [0, 0.599173] |
| Decision-time discard regret | 34 | withheld | [0, 0.595351] |

Campaign-oracle regret is also withheld over its nine opportunity cells; its registered mean bound is [0, 0.707673].

## Threshold sensitivity

All rows use the frozen 60-lifecycle population. Point tables are withheld.

| Threshold | Primary | False-discard bound | Precision bound | Recall bound |
| --- | --- | --- | --- | --- |
| `relative_0.80` | no | 0 (0/36) to 0.833333 (30/36) | 0.625 (15/24) to 0.625 (15/24) | 0.333333 (15/45) to 1 (15/15) |
| `relative_0.90` | yes | 0 (0/36) to 0.833333 (30/36) | 0.541667 (13/24) to 0.541667 (13/24) | 0.302326 (13/43) to 1 (13/13) |
| `relative_1.00` | no | 0 (0/36) to 0.833333 (30/36) | 0.416667 (10/24) to 0.416667 (10/24) | 0.25 (10/40) to 1 (10/10) |
| `absolute_0.58` | no | 0 (0/36) to 0.833333 (30/36) | 0 (0/24) to 0 (0/24) | 0 (0/30) to null (0/0) |

## Missingness and execution boundary

Unresolved fraction: 0.833333 (30/36).

The analyzer conservatively maps unregistered L05 exception-class labels to the registered evaluator category while retaining every literal failure reason in the 36-row machine report. The frozen L05 source artifacts were unchanged on disk, but its original-resource-ledger execution gate failed.

This bounded result is not eligible for a main-text latent-terminal quality claim. It does not imply that discarding saved laboratory resources, that the shadow branch was agent-selected, or that either information arm is generally superior.
