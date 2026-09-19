# RX P/S five-world dual-goal block — aggregate final report

## Completion and evidence boundary

The development block completed 60/60 independent source sessions, 720/720 experimental batches, 180/180 sealed K1/Q/K2 posttests, 600/600 provider-free reference executions, and 60/60 independent recommendation retests. All effective cells completed without a retained final failure; original platform failures remain preserved outside the effective denominator.

Reference truth was generated only after all 60 posttest chains were sealed. The aggregate values below describe the completed development block; they are not a formal causal estimate of prior-arm effects because each agent followed an adaptive experimental trajectory.

## Aggregate by locus, task, and prior arm

Each row averages five worlds. Prediction columns macro-average the six scored Q metrics within each cell, then average cells.

| Locus | Task | Arm | Cells | Selected source score | Retest score | Retest delta | Prediction MAE | 80% coverage | Interval score |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| P | mechanism_discovery | Opaque | 5 | 0.3069 | 0.3024 | -0.0044 | 0.1019 | 0.6033 | 0.4221 |
| P | mechanism_discovery | Aligned | 5 | 0.4531 | 0.4552 | 0.0020 | 0.0570 | 0.7628 | 0.2870 |
| P | mechanism_discovery | MisIndexed | 5 | 0.4520 | 0.4523 | 0.0003 | 0.0546 | 0.8033 | 0.2616 |
| P | safety_constrained_optimization | Opaque | 5 | 0.3075 | 0.3026 | -0.0050 | 0.1389 | 0.4667 | 0.6950 |
| P | safety_constrained_optimization | Aligned | 5 | 0.4342 | 0.4332 | -0.0010 | 0.0838 | 0.7011 | 0.4382 |
| P | safety_constrained_optimization | MisIndexed | 5 | 0.4271 | 0.4200 | -0.0071 | 0.1297 | 0.6389 | 0.7562 |
| S | mechanism_discovery | Opaque | 5 | 0.2959 | 0.2945 | -0.0014 | 0.0840 | 0.8339 | 0.3717 |
| S | mechanism_discovery | Aligned | 5 | 0.3144 | 0.3092 | -0.0052 | 0.0921 | 0.7417 | 0.4392 |
| S | mechanism_discovery | MisIndexed | 5 | 0.3194 | 0.3183 | -0.0011 | 0.1016 | 0.6667 | 0.4829 |
| S | safety_constrained_optimization | Opaque | 5 | 0.2988 | 0.2935 | -0.0053 | 0.1123 | 0.6222 | 0.5614 |
| S | safety_constrained_optimization | Aligned | 5 | 0.3170 | 0.3144 | -0.0026 | 0.1193 | 0.6722 | 0.6312 |
| S | safety_constrained_optimization | MisIndexed | 5 | 0.3314 | 0.3290 | -0.0025 | 0.0922 | 0.6933 | 0.4418 |

## Aggregate by world

| World | Cells | Selected source score | Retest score | Retest delta | Prediction MAE | 80% coverage |
|---|---:|---:|---:|---:|---:|---:|
| RX-W01 | 12 | 0.3201 | 0.3175 | -0.0025 | 0.0838 | 0.7350 |
| RX-W02 | 12 | 0.2791 | 0.2762 | -0.0029 | 0.0745 | 0.7368 |
| RX-W03 | 12 | 0.3884 | 0.3843 | -0.0042 | 0.1174 | 0.6396 |
| RX-W04 | 12 | 0.3826 | 0.3807 | -0.0019 | 0.0924 | 0.7174 |
| RX-W05 | 12 | 0.4038 | 0.4014 | -0.0023 | 0.1183 | 0.5905 |

## Highest independent recommendation retests

| Rank | Cell | Retest score | Selected source score | Delta |
|---:|---|---:|---:|---:|
| 1 | [RX-W05--P--mechanism_discovery--MisIndexed](RX-W05/RX-W05--P--mechanism_discovery--MisIndexed/EXPERIMENT_REPORT.md) | 0.4968 | 0.4953 | 0.0015 |
| 2 | [RX-W03--P--safety_constrained_optimization--Aligned](RX-W03/RX-W03--P--safety_constrained_optimization--Aligned/EXPERIMENT_REPORT.md) | 0.4918 | 0.4947 | -0.0029 |
| 3 | [RX-W03--P--mechanism_discovery--Aligned](RX-W03/RX-W03--P--mechanism_discovery--Aligned/EXPERIMENT_REPORT.md) | 0.4897 | 0.4910 | -0.0013 |
| 4 | [RX-W03--P--mechanism_discovery--MisIndexed](RX-W03/RX-W03--P--mechanism_discovery--MisIndexed/EXPERIMENT_REPORT.md) | 0.4858 | 0.4939 | -0.0081 |
| 5 | [RX-W04--P--mechanism_discovery--MisIndexed](RX-W04/RX-W04--P--mechanism_discovery--MisIndexed/EXPERIMENT_REPORT.md) | 0.4844 | 0.4757 | 0.0087 |
| 6 | [RX-W04--P--mechanism_discovery--Aligned](RX-W04/RX-W04--P--mechanism_discovery--Aligned/EXPERIMENT_REPORT.md) | 0.4768 | 0.4719 | 0.0049 |
| 7 | [RX-W05--P--mechanism_discovery--Aligned](RX-W05/RX-W05--P--mechanism_discovery--Aligned/EXPERIMENT_REPORT.md) | 0.4735 | 0.4777 | -0.0042 |
| 8 | [RX-W05--P--safety_constrained_optimization--MisIndexed](RX-W05/RX-W05--P--safety_constrained_optimization--MisIndexed/EXPERIMENT_REPORT.md) | 0.4707 | 0.4736 | -0.0029 |
| 9 | [RX-W03--P--safety_constrained_optimization--MisIndexed](RX-W03/RX-W03--P--safety_constrained_optimization--MisIndexed/EXPERIMENT_REPORT.md) | 0.4580 | 0.4679 | -0.0100 |
| 10 | [RX-W05--P--safety_constrained_optimization--Aligned](RX-W05/RX-W05--P--safety_constrained_optimization--Aligned/EXPERIMENT_REPORT.md) | 0.4541 | 0.4598 | -0.0057 |

## Interpretation constraints

- `mechanism_discovery` and `safety_constrained_optimization` are separate source sessions; their outcomes should not be treated as repeated measurements of one policy.
- Opaque, Aligned, and MisIndexed arms differ in prior information, but adaptive experiment choices can mediate observed score and prediction differences. The five-world means are descriptive rather than a preregistered inferential test.
- Reference outcomes use five independent observation repeats per query. Coverage is empirical over 60 reference observations per metric and cell; it is not a confidence interval on population coverage.
- A high selected source score is sample-internal. The independent retest and its delta are the relevant repeatability check, not proof of global optimality.
- K1 and K2 remain qualitative research artifacts. This export preserves them verbatim but does not impose an after-the-fact mechanistic correctness score.

For full evidence, use the per-cell reports and JSON results linked from the five world indices. [SUMMARY.json](SUMMARY.json) contains the aggregate machine-readable table.
