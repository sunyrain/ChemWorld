# First-paper composition qualification

Status: **PASSED**

## Exact deterministic counts

| Quantity | Passed | Denominator |
| --- | ---: | ---: |
| Registered task/world units | 64 | 64 |
| Valid midpoint/boundary/category recipes | 1786 | 1786 |
| Negative runtime probes | 192 | 192 |
| Generated compositions | 52 | 52 |
| Frozen unseen reaction--distillation cases | 8 | 8 |
| Compile-time mutants | 7 | 7 |
| Module probes | 32 | 32 |
| Cross-component interface paths | 7 | 7 |

Public/private leakage findings: `0`.
Missing receipts: `0`.

## Generated pattern matrix

| Pattern | Passed | Denominator |
| --- | ---: | ---: |
| phase-observation | 6 | 6 |
| reaction-thermal-observation | 6 | 6 |
| phase-separation-observation | 6 | 6 |
| reaction-crystallization-observation | 6 | 6 |
| reaction-distillation-observation | 8 | 8 |
| reaction-continuous-flow-observation | 6 | 6 |
| reaction-electrochemistry-observation | 7 | 7 |
| reaction-phase-separation-observation | 7 | 7 |

## Composition depth and runtime envelope

### `component_count`

| Value | Passed | Denominator | Mean elapsed (s) | Mean bytes |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 6 | 6 | 0.435560 | 549964.2 |
| 3 | 19 | 19 | 2.142645 | 872229.1 |
| 4 | 20 | 20 | 2.570348 | 1121260.0 |
| 5 | 7 | 7 | 3.156860 | 2045016.0 |

### `workflow_stage_count`

| Value | Passed | Denominator | Mean elapsed (s) | Mean bytes |
| ---: | ---: | ---: | ---: | ---: |
| 5 | 9 | 9 | 0.470064 | 556212.9 |
| 6 | 3 | 3 | 0.863102 | 687308.0 |
| 7 | 3 | 3 | 1.336186 | 791798.3 |
| 8 | 3 | 3 | 1.575438 | 874582.0 |
| 9 | 6 | 6 | 0.652365 | 959014.3 |
| 10 | 4 | 4 | 1.349368 | 1145719.5 |
| 11 | 7 | 7 | 4.655650 | 1007173.0 |
| 12 | 7 | 7 | 3.072168 | 1291887.1 |
| 13 | 3 | 3 | 5.256477 | 1266657.0 |
| 16 | 3 | 3 | 2.516756 | 1891291.3 |
| 18 | 4 | 4 | 3.636937 | 2160309.5 |

### `action_count`

| Value | Passed | Denominator | Mean elapsed (s) | Mean bytes |
| ---: | ---: | ---: | ---: | ---: |
| 5 | 9 | 9 | 0.470064 | 556212.9 |
| 6 | 3 | 3 | 0.863102 | 687308.0 |
| 7 | 3 | 3 | 1.336186 | 791798.3 |
| 8 | 3 | 3 | 1.575438 | 874582.0 |
| 9 | 6 | 6 | 0.652365 | 959014.3 |
| 10 | 4 | 4 | 1.349368 | 1145719.5 |
| 11 | 7 | 7 | 4.655650 | 1007173.0 |
| 12 | 7 | 7 | 3.072168 | 1291887.1 |
| 13 | 3 | 3 | 5.256477 | 1266657.0 |
| 16 | 3 | 3 | 2.516756 | 1891291.3 |
| 18 | 4 | 4 | 3.636937 | 2160309.5 |

## Module reference boundary

| Module | Low/high classification | Maximum absolute error | Tolerance |
| --- | --- | ---: | ---: |
| reaction | numerical_reference_fixture | 0 | 1e-12 |
| thermal | numerical_reference_fixture | 4.00178e-11 | 1e-08 |
| phase | numerical_reference_fixture | 1.73472e-18 | 1e-12 |
| separation | numerical_reference_fixture | 0 | 1e-12 |
| crystallization | conceptual_or_synthetic | n/a | n/a |
| distillation | numerical_reference_fixture | 4.54747e-13 | 1e-12 |
| continuous_flow | numerical_reference_fixture | 0 | 1e-12 |
| electrochemistry | numerical_reference_fixture | 0 | 1e-12 |

## Interface receipts

| Path | Cases | Named checks passed |
| --- | ---: | ---: |
| reaction--thermal | 6 | 14/14 |
| reaction--phase--separation | 7 | 14/14 |
| phase--separation | 6 | 14/14 |
| reaction--crystallization | 6 | 14/14 |
| reaction--distillation | 8 | 14/14 |
| reaction--continuous-flow | 6 | 14/14 |
| reaction--electrochemistry | 7 | 14/14 |

## Receipt completeness

Status: `passed`; errors: `0`.

## Failure classes

None.

## Claim boundary

- Deterministic virtual-instrument qualification only.
- Finite v1 component and interface coverage; not exhaustive task-space validation.
- No physical-laboratory external-validity or agent-intelligence claim.
