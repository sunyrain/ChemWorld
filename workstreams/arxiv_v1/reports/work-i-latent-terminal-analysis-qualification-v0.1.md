# Work I Latent-Terminal Analysis Synthetic Qualification

Status: **qualified**

Report SHA-256: `f2113e77d8b3bca66f80ddd1e88d48c87bc25443ab52c29129f4aca4271747be`

## Boundary

This qualification used 36 deterministic synthetic score receipts bound to the frozen L01 identities. It executed **0 formal shadow evaluations**, accessed **0 formal shadow outcomes**, and made **0 agent/provider calls**.

It qualifies analysis code only. It is not a terminal-quality result and is never eligible for main-text scientific entry.

## Qualification cases

| Case | Result | Analysis SHA-256 |
| --- | --- | --- |
| `complete_synthetic_population` | **PASS** | `4b38aa4ef88a28a54dc009a6ed04082f3e9281c83b42a09c4a2a7dd886eb4393` |
| `threshold_equality_is_near_best` | **PASS** | `9f7b49f6a1cc94fa8c0980ffbc41dc043c8279a8587cb2cd1f992fd1e0f831dd` |
| `missing_receipt_retains_fixed_denominator` | **PASS** | `d9e5a4362b35bea401bc32f51ad7bb90295626e3ccef740e5ce52bc0960ca3e0` |
| `nonfinite_score_fails_closed` | **PASS** | `048923ada6bf3dc195edbe690755d0259fcdf37a3edd6976e1064dd1340d73f3` |
| `zero_denominator_and_decision_null` | **PASS** | `f6f5ed297882f5937650bf8e1dc8cdc3cda77bcb648465322f53b87210ab0fa3` |
| `tampered_binding_fails_closed` | **PASS** | `8970fcf43728de6cb29fbfcf5d69190ac9732d6922bdb38b9fd893d7c06967e2` |
| `forbidden_imputation_is_ignored` | **PASS** | `dee13378b22fe76e43d90cc34193c4608306b6e3297797a3bc60c845c9f1d516` |

## Qualified surface

- All eight L01-frozen estimands and their fixed denominators.
- The 60-lifecycle TP/FP/FN/TN table with equality classified near-best.
- Relative threshold rows at 0.80, 0.90 and 1.00, plus absolute 0.58.
- Finite-population micro, cell-macro and descriptive paired-arm outputs.
- The nine discard-opportunity-cell oracle; `cell-02` remains null.
- Decision-time regret with pre-assay discards null and no future imputation.
- Registered unresolved counts, all-zero/all-one endpoints and sharp bounds.
- Fail-closed missing, non-finite, tampered-binding and imputation handling.

Observed-only diagnostics never replace a registered point estimate. Any unresolved shadow receipt retains the frozen denominator and withholds all affected point estimates.

## Evidence binding

- Frozen contract: `55a0d6a7cb983ce4099dbea24586ea63ccc9433e106d36011d349472809efe30`
- Population manifest: `ab35b3214c4cdf9003afff3f0d6b9205e615b5c76afa4664677bc9b95c19a9ae`
- Source manifest: `d876af98bb146441147491c32efae829c4788821ce66b3c846155adaac601391`
