# Work II three-task, five-seed campaign summary

Date: 2026-08-09. Status: development evidence; not a formal or held-out result.

## Execution result

The frozen development programme reached terminal state in all three tasks. Electrochemical
conversion and reaction-to-crystallization passed all 15 cells. Reaction-to-distillation passed
14/15 cells and therefore failed its all-cells task criterion. The combined programme is 44/45
passed cells and 176/180 complete experiments; the failed cell is retained without replacement.

| Task | Cells passed | Experiments | Checkpoints | Operation attempts | Exact replay | Matrix wall time |
|---|---:|---:|---:|---:|---:|---:|
| Electrochemical conversion | 15 / 15 | 60 / 60 | 60 / 60 | 367 | 15 / 15 | 2,661.4 s |
| Reaction-to-crystallization | 15 / 15 | 60 / 60 | 60 / 60 | 663 | 15 / 15 | 6,120.0 s |
| Reaction-to-distillation | 14 / 15 | 56 / 60 | 56 / 60 | 517 | 14 / 15 | 3,068.9 s |
| **Combined** | **44 / 45** | **176 / 180** | **176 / 180** | **1,547** | **44 / 45** | **11,850.3 s task sum** |

The per-task machine reports are ignored development artifacts:

- `runs/development/work-ii-electrochemical-five-seed-20260808T184013/matrix_report.json`
- `runs/development/work-ii-crystallization-five-seed-rerun2/matrix_report.json`
- `runs/development/work-ii-distillation-five-seed-run1/matrix_report.json`

## Exact attempt and failure accounting

| Task | Committed | Validation failed | Resource rejected | Provider error events | Provider error entries |
|---|---:|---:|---:|---:|---:|
| Electrochemical conversion | 367 | 0 | 0 | 1 | 1 |
| Reaction-to-crystallization | 651 | 12 | 0 | 5 | 4 |
| Reaction-to-distillation | 506 | 11 | 0 | 33 | 19 |
| **Combined** | **1,524** | **23** | **0** | **39** | **24** |

All provider errors in completed sessions were recovered inside the original session. Validation-
failed calls did not commit a scientific operation. All 1,547 recorded attempts replay exactly;
the distillation failure has zero recorded operations, so it contributes no replayable step.

The sole terminal failure was `reaction-to-distillation / world_seed=4 / aligned_nominal`. The
provider completed one Codex turn with 15,873 input tokens and 170 output tokens, no provider error
and no MCP call. The participant emitted explanatory text instead of invoking the experiment tool,
leaving zero experiments and zero checkpoints. This is an unrecovered participant/harness failure,
not a transport or resource rejection. Per the frozen rule, the cell is retained and is not rerun.

## Provider and context accounting

| Task | Input | Cached input | Uncached input | Output |
|---|---:|---:|---:|---:|
| Electrochemical conversion | 19,459,659 | 17,652,224 | 1,807,435 | 157,356 |
| Reaction-to-crystallization | 28,993,580 | 26,322,048 | 2,671,532 | 149,774 |
| Reaction-to-distillation | 10,961,222 | 8,850,304 | 2,110,918 | 99,481 |
| **Combined** | **59,414,461** | **52,824,576** | **6,589,885** | **406,611** |

## Scope boundary

This campaign is method-development evidence. It does not execute evaluator-owned held-out queries,
blind recommendation replicates, a preregistered public formal matrix or private sealed confirmation.
Because the distillation block failed its all-cells rule, no three-task prior-effect estimate should
be promoted from this programme. The current evidence supports runner/resource/replay qualification
and exposes failure modes that must be frozen before W2-12; it does not authorize formal claims.
