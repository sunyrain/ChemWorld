# Work I Discarded-State Latent-Terminal Contract

Status: **frozen before shadow outcomes**

Contract SHA-256: `2059f0b97952296fc57e5121ac0868ecd2a01a3b7afc026a0ee7b7ddce4a4737`

## Scientific question

What terminal quality was present in states that the complete agent system chose to discard, and what does that reveal about its terminal selection policy beyond lifecycle completion counts?

This is a finite-population, evaluator-only counterfactual audit of the terminal decisions already present in the frozen DeepSeek G2 v0.6 complete-system demonstration. It is not a model leaderboard.

## Frozen population

The census contains **60 original lifecycles** across **10 campaign cells**: **24 observed assays + 36 committed discards**. Exactly 36 evaluator-only shadow terminal evaluations are planned; they make zero agent/provider calls.

| Cell | World | Information arm | Assays | Discards | Observed best | Terminal sequence |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| `cell-01` | 0 | `opaque_codes` | 1 | 5 | 0.124696 | `A D D D D D` |
| `cell-02` | 0 | `anonymous_nominal_properties` | 6 | 0 | 0.313319 | `A A A A A A` |
| `cell-03` | 1 | `anonymous_nominal_properties` | 2 | 4 | 0.315349 | `A A D D D D` |
| `cell-04` | 1 | `opaque_codes` | 1 | 5 | 0.430015 | `A D D D D D` |
| `cell-05` | 2 | `opaque_codes` | 4 | 2 | 0.301827 | `A A A A D D` |
| `cell-06` | 2 | `anonymous_nominal_properties` | 2 | 4 | 0.345602 | `A D D D D A` |
| `cell-07` | 3 | `anonymous_nominal_properties` | 3 | 3 | 0.410911 | `D A A A D D` |
| `cell-08` | 3 | `opaque_codes` | 1 | 5 | 0.260812 | `D A D D D D` |
| `cell-09` | 4 | `opaque_codes` | 1 | 5 | 0.045168 | `A D D D D D` |
| `cell-10` | 4 | `anonymous_nominal_properties` | 3 | 3 | 0.396565 | `A A D A D D` |

Each discard unit is already enumerated by cell, lifecycle, terminal step, terminal-action hash, public-prefix hash, compact trajectory hash, and raw source-trajectory hash. No hidden state or latent score was read while constructing this contract.

## Counterfactual terminal rule

The immutable hidden state and resource ledger immediately before the original discard_batch attempt.

Suppress only the original discard terminal and evaluate the same hidden state with the frozen final-assay observation and scoring contracts.

The evaluation is read-only with respect to the original campaign. It may bypass only the agent-facing workflow-readiness gate needed to expose the frozen final-assay evaluator; it may not advance chemistry, add material, repair state, or mutate the original resource ledger. Prefix actions, observations, keyed-noise receipts, hidden state, resource state, and ordinals must match exactly.

## Primary quality reference

For campaign `c`, `B_c` is the best score among that campaign's original assay decisions. The primary near-best threshold is **`q_c = 0.90 B_c`**, using the pre-existing Work I retention fraction. Equality counts as near-best. The registered absolute task threshold `0.58` is sensitivity-only.

## Frozen estimands

| Estimand | Role | Unit | Formula | Denominator |
| --- | --- | --- | --- | --- |
| `latent_terminal_score` | `primary_continuous` | discarded lifecycle | `S_i` | all 36 valid shadow evaluations |
| `discard_to_observed_best_delta` | `primary_continuous` | discarded lifecycle | `Delta_i = S_i - B_c` | all 36 valid shadow evaluations |
| `positive_discard_regret` | `primary_continuous` | discarded lifecycle | `R_i = max(0, S_i - B_c)` | all 36 valid shadow evaluations |
| `campaign_oracle_regret` | `primary_campaign` | campaign cell | `R_c = max(0, max_{i in discarded(c)} S_i - B_c)` | all 10 campaign cells |
| `false_discard_fraction` | `primary_classification` | discarded lifecycle | `FN / (FN + TN)` | all 36 discard decisions |
| `assay_commitment_precision` | `primary_classification` | assayed lifecycle | `TP / (TP + FP)` | all 24 observed assay decisions |
| `assay_commitment_recall` | `secondary_classification` | high-value lifecycle | `TP / (TP + FN)` | all near-best lifecycles among the frozen 60 |
| `decision_time_discard_regret` | `secondary_temporal` | discarded lifecycle with a prior assayed incumbent | `max(0, S_i - I_i^-)` | discard decisions with at least one earlier assay in the same campaign |

The 60-lifecycle selection table is defined as: TP = assayed and near-best; FP = assayed and below threshold; FN = discarded with a near-best shadow score; TN = discarded below threshold. Thus the primary false-discard fraction is `FN/(FN+TN)`, assay commitment precision is `TP/(TP+FP)`, and commitment recall is `TP/(TP+FN)`.

## Aggregation and sensitivity

- Primary quantities describe the complete frozen finite population; super-population p-values or confidence intervals are not primary.
- Lifecycle-level micro estimates are reported overall and by arm. Cell-level macro summaries and paired arm contrasts are separate and never replace the census estimate.
- Continuous score, signed delta, positive regret, and campaign oracle regret distributions are mandatory.
- Relative threshold sensitivities at `0.80`, `0.90`, and `1.00` times the observed campaign best, the registered absolute threshold, and the decision-time incumbent analysis are all mandatory.
- A discard before any assay has null decision-time regret; a future assay is never imputed as a past incumbent.

## Missingness and fail-closed behavior

All 36 shadow evaluations are required for primary point estimates. A non-finite score, prefix mismatch, or evaluator failure is retained as an unresolved receipt: no complete-case substitution, clamping, semantic repair, or favorable rerun is allowed. The full report must then provide sharp missing-outcome bounds and remain incomplete.

## Evidence-entry rule

The complete 36-row audit, all gates, continuous summaries, selection tables, sensitivity rows, and failure receipts are published regardless of direction. Main-text quantitative claims require 36/36 exact prefix reconstructions, 36/36 valid scores, 36/36 exact shadow replays, zero agent/provider calls, and no mutation of original trajectories or ledgers. There is no result-direction, significance, arm-difference, or post-outcome threshold gate.

## Claim boundary

Allowed:

- quality of discarded states in this frozen complete-system demonstration.
- whether lifecycle completion masks distinct terminal selection policies.
- whether the best available state in a campaign was committed to assay.
- descriptive differences between the two fixed information arms.

Not allowed:

- the shadow assay was chosen or observed by the agent.
- discarding saved real laboratory resources.
- the complete system is generally rational or irrational.
- a causal model-backend or general material-information effect.
- superiority over another agent system.
- real-laboratory executability or safety.
- counting shadow evaluations as original agent experiments.

## Frozen evidence

- Campaign audit: `74b08ec6cf318f8fa7739ba133fa3f09d69964d40b3a6279cd82e40b91ba5d6a`
- Matrix manifest: `0b0ebae45e7f269a3e1ab268d06a90c996347b98071a0fb19240d47fd00bfa1d`
- Public archive: `3362ea0a2f6349e6528fde3e2ac23f4de3580ae4d8ce750163dc4e181498a3f6`
- Terminal index: `6c4c9a933e1a3cc0c6ead749892bf90b0abf2e3fc33fb796497d7bd3a99f82b3`
- Population manifest: `ab35b3214c4cdf9003afff3f0d6b9205e615b5c76afa4664677bc9b95c19a9ae`
- Source manifest: `6975e7b53969274fc3319c631ab0190cfae34a4b4edf1baedbca69733fdff324`
