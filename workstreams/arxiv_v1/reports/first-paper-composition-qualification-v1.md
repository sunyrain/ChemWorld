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

## Failure classes

None.

## Claim boundary

- Deterministic virtual-instrument qualification only.
- Finite v1 component and interface coverage; not exhaustive task-space validation.
- No physical-laboratory external-validity or agent-intelligence claim.
