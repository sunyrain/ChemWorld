# Work I Experimental-Agency Profile Contract

Schema: `chemworld.experimental_agency_profile@0.1.0`

Contract SHA-256: `01e3cb3ff5c7b2455fd998fb5eebdd1932931c6fef2d5125632b103d79a34262`

## Construct

The observable organization of resource-constrained experimental choices over typed operations, active evidence acquisition, post-evidence action, and lifecycle termination in a hidden stateful chemical world.

The measurement unit is **one campaign in one fixed world and information arm**. The result is a **multidimensional profile; no composite score**.

The profile measures observable experimental policy. It does not claim:

- a unitary intelligence, reasoning, or chemical-knowledge score.
- equivalence with endpoint optimization performance.
- real-laboratory executability or safety.
- direct measurement of private beliefs or internal cognition.
- comparability across resource cards without an explicit contrast.

## Construct axes

| Axis | Operational role | Metrics |
| --- | --- | ---: |
| `terminal_commitment` | How often a started experimental lifecycle is closed, and whether the agent commits it to final assay or discards it. | 3 |
| `evidence_acquisition` | Whether, how often, and how early the agent requests non-final instrument evidence before a terminal decision. | 3 |
| `evidence_conditioned_action` | Whether observed evidence is followed by further physical investment and whether a preregistered evidence rule predicts the terminal choice. | 4 |
| `resource_deployment` | How operation attempts, committed physical operations, monetary cost, and risk budget are deployed across closed lifecycles. | 4 |
| `outcome_trajectory` | When high-scoring assayed conditions are found and whether later assayed conditions retain, lose, or recover the running incumbent. | 5 |

## Frozen metric dictionary

Endpoint scores are listed separately below; they are never combined with the construct axes. `null` denotes an absent denominator, not zero behavior.

| Metric | Axis | Unit | Denominator | Null rule | Positive-control role |
| --- | --- | --- | --- | --- | --- |
| `closed_lifecycle_fraction` | `terminal_commitment` | fraction | `planned_lifecycle_count` | never | completion gate |
| `assay_fraction` | `terminal_commitment` | fraction | `closed_lifecycle_count` | no lifecycle is closed | primary |
| `discard_fraction` | `terminal_commitment` | fraction | `closed_lifecycle_count` | no lifecycle is closed | primary |
| `measured_lifecycle_fraction` | `evidence_acquisition` | fraction | `closed_lifecycle_count` | no lifecycle is closed | primary |
| `nonfinal_instrument_uses_per_closed_lifecycle` | `evidence_acquisition` | uses/lifecycle | `closed_lifecycle_count` | no lifecycle is closed | primary |
| `mean_first_measurement_operation_fraction` | `evidence_acquisition` | fraction of lifecycle operations | `measured_lifecycle_count` | no closed lifecycle contains a committed non-final measurement | secondary |
| `continued_after_measurement_fraction` | `evidence_conditioned_action` | fraction | `closed_lifecycle_count` | no lifecycle is closed | primary |
| `post_measure_process_operations_per_closed_lifecycle` | `evidence_conditioned_action` | operations/lifecycle | `closed_lifecycle_count` | no lifecycle is closed | secondary |
| `threshold_eligible_fraction` | `evidence_conditioned_action` | fraction | `closed_lifecycle_count` | no lifecycle is closed | eligibility gate |
| `threshold_decision_concordance` | `evidence_conditioned_action` | fraction | `threshold_eligible_lifecycle_count` | no closed lifecycle has a finite preregistered diagnostic signal | primary |
| `attempted_operations_per_closed_lifecycle` | `resource_deployment` | attempts/lifecycle | `closed_lifecycle_count` | no lifecycle is closed | primary |
| `committed_operations_per_closed_lifecycle` | `resource_deployment` | operations/lifecycle | `closed_lifecycle_count` | no lifecycle is closed | secondary |
| `total_cost_per_closed_lifecycle` | `resource_deployment` | cost units/lifecycle | `closed_lifecycle_count` | no lifecycle is closed | primary |
| `total_risk_per_closed_lifecycle` | `resource_deployment` | risk units/lifecycle | `closed_lifecycle_count` | no lifecycle is closed | secondary |
| `global_best_discovery_fraction` | `outcome_trajectory` | fraction of assayed sequence | `final_assay_count` | no committed final assay exists | descriptive extension |
| `online_incumbent_retention_rate` | `outcome_trajectory` | fraction | `final_assay_count_minus_one` | fewer than two committed final assays exist | descriptive extension |
| `maximum_absolute_incumbent_drawdown` | `outcome_trajectory` | score units | `final_assay_count_minus_one` | fewer than two committed final assays exist | descriptive extension |
| `loss_episode_recovery_rate` | `outcome_trajectory` | fraction | `loss_episode_count` | no loss episode is observed | descriptive extension |
| `terminal_to_global_best_ratio` | `outcome_trajectory` | ratio | `final_assay_count` | no positive committed final-assay score exists | descriptive extension |

## Endpoint context (outside the construct)

| Metric | Definition |
| --- | --- |
| `mean_assayed_score` | Arithmetic mean of committed final-assay scores. |
| `best_assayed_score` | Maximum committed final-assay score in the campaign. |

## Counting and aggregation

- **operation attempt:** Every environment step admitted to campaign resource preflight, including validation failures and transactional rollbacks, is an attempted operation.
- **committed operation:** An attempt with transaction_status=committed.
- **measurement:** A committed measure operation whose instrument is not final_assay; cached observations and failed measurements do not count.
- **closed lifecycle:** Exactly one committed terminal action, final_assay or discard, closes a started vessel lifecycle.
- **post measure process operation:** A committed non-measure, non-terminal physical operation strictly after the first committed non-final measurement in the same lifecycle.
- **cost and risk:** Use campaign ledger deltas; penalties from charged failed attempts remain included, while rejected candidate-state physical changes remain excluded.

Profiles are computed at the `campaign` level. A formal cell is `world_id x information_arm x policy_id`, with 6 lifecycles. Compute each campaign profile first. Report policy summaries across the ten matched world-arm cells; do not pool lifecycle rows before profile creation.

## Frozen invariants and reliability

- `closed_lifecycle_count = final_assay_count + discard_count`
- `closed_lifecycle_count <= planned_lifecycle_count`
- `measured_lifecycle_count <= closed_lifecycle_count`
- `threshold_eligible_lifecycle_count <= measured_lifecycle_count`
- `assay_fraction + discard_fraction = 1 when closed_lifecycle_count > 0`
- `endpoint_context is null when final_assay_count = 0`
- `profile values are reconstructed from immutable events and resource ledgers`

Exact replay requires matching event, state, resource, and profile hashes. Known-policy controls make zero provider calls. The construct and all metric definitions were frozen before formal policy outcomes; threshold values are reserved to W1-V03 qualification worlds.
