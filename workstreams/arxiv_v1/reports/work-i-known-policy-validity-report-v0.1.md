# Work I known-policy measurement-validity report

Status: **positive_control_established**.

Across the frozen five-world, two-arm matrix, the experimental-agency profile recovered the prespecified signatures, nulls, partial orderings, matched-arm invariance, resource expectations, and exact deterministic retest behavior for the three known policies. This establishes the bounded construct/discriminant-validity positive control for this simulated apparatus.

## Frozen design and counts

The primary estimand gives one equal weight to each campaign profile: ten world-arm campaigns per policy, 30 campaigns and 180 closed lifecycles total. The 30 same-identity retest campaigns and 180 retest lifecycles are reliability evidence only and are excluded from the primary estimand. Provider calls: 0.

## Campaign-equal policy summaries

| Policy | Assay | Discard | Measured | Continued | Non-final instruments | Operations |
|---|---:|---:|---:|---:|---:|---:|
| `assay_all` | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 6.000 |
| `start_then_discard` | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 2.000 |
| `measure_then_threshold` | 0.467 | 0.533 | 1.000 | 0.467 | 1.000 | 6.933 |

## Frozen gates

- `matrix_complete`: PASS
- `all_180_lifecycles_closed`: PASS
- `all_profiles_rebuilt`: PASS
- `all_resource_ledgers_replayed`: PASS
- `all_exact_replays_and_retests_match`: PASS
- `matched_arm_invariance`: PASS
- `zero_provider_calls`: PASS
- `threshold_non_degenerate`: PASS
- `exact_policy_signatures`: PASS
- `conditional_null_rules`: PASS
- `six_partial_orderings`: PASS
- `resource_expectations`: PASS

The frozen threshold policy produced 28 assays and 32 discards; both branches were observed. All V01 conditional nulls, V02 exact signatures and six prespecified partial orderings are published in the JSON report.

Explicit non-orderings remain descriptive and are not promoted to gates: mean_assayed_score; best_assayed_score; all outcome_trajectory metrics; cost or risk between assay_all and measure_then_threshold.

## Reliability and evidence

All 30 original/retest pairs matched in controller, trajectory identity, profile, and component hashes. V06 independently rebuilt all campaign profiles. V06 independently replayed all campaign resource ledgers. The V06 reconstruction exactly matched the immutable formal audit receipt.

## Interpretation boundary

This is a bounded construct/discriminant-validity positive control for three deterministic policies in five simulated worlds and two information arms. It is not an endpoint ranking, causal information-null result, provider/model capability claim, scalar intelligence score, or real-laboratory generalization.

Machine report SHA-256: `ebb56a052929944330acdf594e4a341c8c8fdb2b4ea2e276556384e7ce6b2064`
