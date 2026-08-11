# Work II DeepSeek development evaluator confirmation

Date: 2026-08-11. Participant matrix completed 2026-08-10; evaluator confirmation completed 2026-08-11. Status: development evidence only; not formal or private evidence.

## Exact denominators

- Participant cells retained: **75/75**.
- Completed and runner-qualified participant cells: **69/75**; failed or unqualified: **6/75**.
- Evaluator truth queries: **100/100** completed and **100/100** exact replay.
- Blind replays: **414/414** completed.
- Final checkpoint predictions scored: **72/75**; executable final law summaries: **71/75**.
- Evaluator provider calls: **0**; participant resource-ledger impact: **0**.

## Development observations

The retained task x seed H3 contrast has n=25 clusters and descriptive mean -0.0421. Positive values mean that the misindexed arm reduced held-out prediction error more than the aligned arm; this is descriptive and is not a formal test.

| Task | Arm | n cells | pre error | final error | improvement | law error | blind gain |
|---|---|---:|---:|---:|---:|---:|---:|
| electrochemical-conversion | opaque | 5 | 0.2452 | 0.2006 | 0.0446 | 0.2622 | 0.0000 |
| electrochemical-conversion | aligned_nominal | 5 | 0.2653 | 0.1852 | 0.0801 | 0.4078 | 0.0000 |
| electrochemical-conversion | misindexed_nominal | 5 | 0.2426 | 0.2211 | 0.0216 | 0.5886 | 0.0000 |
| partition-discovery | opaque | 5 | 0.3982 | 0.0960 | 0.2418 | 0.0657 | -0.0199 |
| partition-discovery | aligned_nominal | 5 | 0.4266 | 0.1104 | 0.3162 | 0.1966 | -0.0489 |
| partition-discovery | misindexed_nominal | 5 | 0.3729 | 0.1504 | 0.2226 | 0.1741 | 0.0000 |
| reaction-safety-constrained | opaque | 5 | 0.3462 | 0.1027 | 0.2435 | 0.1937 | 0.0000 |
| reaction-safety-constrained | aligned_nominal | 5 | 0.3421 | 0.1610 | 0.1812 | 0.1529 | 0.0000 |
| reaction-safety-constrained | misindexed_nominal | 5 | 0.3293 | 0.0983 | 0.2310 | 0.1845 | 0.0000 |
| reaction-to-crystallization | opaque | 5 | 10.8906 | 0.1214 | 8.6153 | 0.1001 | 0.0000 |
| reaction-to-crystallization | aligned_nominal | 5 | 0.2500 | 0.1151 | 0.1349 | 0.2314 | 0.0000 |
| reaction-to-crystallization | misindexed_nominal | 5 | 0.2433 | 0.1826 | 0.0486 | 0.2278 | 0.0000 |
| reaction-to-distillation | opaque | 5 | 0.2901 | 0.2057 | 0.0844 | 0.3046 | 0.0000 |
| reaction-to-distillation | aligned_nominal | 5 | 0.3210 | 0.2115 | 0.1095 | 0.2630 | 0.0000 |
| reaction-to-distillation | misindexed_nominal | 5 | 0.2916 | 0.2040 | 0.0876 | 0.3558 | 0.0000 |

## Interpretation boundary

This analysis adds evaluator-held prediction scoring, executable-law checks and blind replay to the already frozen DeepSeek development trajectories. It does not rerun any participant cell, replace failures, perform a formal hypothesis test, evaluate private transfer or support a cross-provider capability ranking.

Machine report SHA-256: `efdd7952835872a1fed1e9066befb61f31ff24439e7b5bef2d61e8145c6136f8`.
