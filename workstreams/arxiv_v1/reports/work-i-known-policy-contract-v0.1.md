# Work I Known-Policy Construct-Validity Contract

Schema: `chemworld.known_policy_controls@0.1.0`

Contract SHA-256: `79681abfa92af758af8326db1727b865376ad0da192ea13552b68fd94a66dd45`

Bound profile contract SHA-256: `01e3cb3ff5c7b2455fd998fb5eebdd1932931c6fef2d5125632b103d79a34262`

## What these controls establish

Does the frozen multidimensional profile recover experimental policies whose evidence and terminal-decision structures are known by construction?

The three policies are **construct-validity positive controls**, not endpoint baselines. They deliberately differ in terminal commitment, evidence acquisition, and evidence-conditioned investment while making zero provider calls.

They do not establish:

- endpoint-performance superiority.
- chemical intelligence ranking.
- provider or language-model capability.
- real-laboratory safety or executability.

## Formal matrix

The formal matrix contains **30 campaigns** and **180 closed lifecycles**: 5 worlds x 2 information arms x 3 policies x 6 lifecycles. Provider calls: **0**.

All policies receive the same six cards in the same order. The material dossier is never read, so matched arms are an exact interface-and-pairing check rather than a material-information experiment.

## Frozen policy grammar

| Policy | Evidence | Terminal policy | Operations per lifecycle |
| --- | --- | --- | ---: |
| `assay_all` | none | terminate and final assay every vessel | 6 |
| `start_then_discard` | none | discard immediately after vessel start | 2 |
| `measure_then_threshold` | one UV-vis conversion signal | below threshold: discard; at/above: one additional electrolysis then final assay | 6 or 8 |

## Six-probe schedule

| Probe | Solvent | Electrolyte | Reagent (mol) | Potential (V) | Current (mA) | Probe (s) | Post-measure (s) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `probe-01` | 0 | 0 | 0.010 | 0.72 | 25.0 | 300 | 300 |
| `probe-02` | 1 | 1 | 0.012 | 0.84 | 40.0 | 420 | 420 |
| `probe-03` | 2 | 2 | 0.014 | 0.96 | 55.0 | 540 | 540 |
| `probe-04` | 3 | 3 | 0.016 | 1.08 | 70.0 | 660 | 660 |
| `probe-05` | 0 | 2 | 0.018 | 1.20 | 85.0 | 780 | 780 |
| `probe-06` | 2 | 0 | 0.020 | 1.24 | 90.0 | 900 | 900 |

## Exact signatures

These identities are evaluated after the all-commit execution-validity gate: All planned lifecycles close, every submitted action commits, no action is validation-failed or resource-rejected, and event/state/resource replay is exact. Signature recovery is assessed only after this gate.

| Metric | `assay_all` | `start_then_discard` | `measure_then_threshold` |
| --- | ---: | ---: | ---: |
| `closed_lifecycle_fraction` | 1.0 | 1.0 | 1.0 |
| `assay_fraction` | 1.0 | 0.0 | see p algebra |
| `discard_fraction` | 0.0 | 1.0 | see p algebra |
| `measured_lifecycle_fraction` | 0.0 | 0.0 | 1.0 |
| `nonfinal_instrument_uses_per_closed_lifecycle` | 0.0 | 0.0 | 1.0 |
| `continued_after_measurement_fraction` | 0.0 | 0.0 | see p algebra |
| `threshold_eligible_fraction` | 0.0 | 0.0 | 1.0 |
| `threshold_decision_concordance` | null | null | 1.0 |
| `attempted_operations_per_closed_lifecycle` | 6.0 | 2.0 | see p algebra |

For the threshold policy, p = assayed threshold-policy lifecycles / closed threshold-policy lifecycles. After the formal non-degeneracy gate, `0 < p < 1`. Its assay fraction is `p`, continued-investment fraction is `p`, and attempted operations per lifecycle are `6 + 2p`.

## Preregistered partial orderings

- `assay_all.assay_fraction > measure_then_threshold.assay_fraction > start_then_discard.assay_fraction`
- `start_then_discard.discard_fraction > measure_then_threshold.discard_fraction > assay_all.discard_fraction`
- `measure_then_threshold.measured_lifecycle_fraction > assay_all.measured_lifecycle_fraction = start_then_discard.measured_lifecycle_fraction`
- `measure_then_threshold.nonfinal_instrument_uses_per_closed_lifecycle > assay_all.nonfinal_instrument_uses_per_closed_lifecycle = start_then_discard.nonfinal_instrument_uses_per_closed_lifecycle`
- `measure_then_threshold.continued_after_measurement_fraction > assay_all.continued_after_measurement_fraction = start_then_discard.continued_after_measurement_fraction`
- `measure_then_threshold.attempted_operations_per_closed_lifecycle > assay_all.attempted_operations_per_closed_lifecycle > start_then_discard.attempted_operations_per_closed_lifecycle`

No ordering is asserted for endpoint score, outcome-trajectory metrics, or cost/risk between `assay_all` and `measure_then_threshold`. Those quantities are not controlled policy identities.

## Threshold firewall

Among candidates producing both branches in every qualification arm, choose the candidate closest to the pooled qualification median; break equal-distance ties toward the lower numeric threshold.

Only independent qualification worlds may supply candidate signals. Formal world seeds 0-4 are forbidden for threshold selection. W1-V03 must freeze the value and source-manifest hash before implementation. If the resulting formal matrix does not contain both branches, the complete result remains published and the positive-control gate is marked unestablished; the threshold is never retuned on formal data.

## Reliability

A second execution from the same world identity, keyed-noise namespace, policy, and threshold must reproduce event, state, resource, terminal, profile, and endpoint hashes exactly.
