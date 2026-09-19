# Published RX source-record synthesis

Remote snapshot: `25537865465fdaadcee704912305d17d3f84c7bc`.

This analysis reads the published records only. It does not generate, access or estimate the withheld reference truth.

## Coverage

```json
{
  "published_cells": 48,
  "source_batches": 576,
  "operations": 4149,
  "sealed_chains": 47,
  "valid_posttests": 143,
  "nonfinal_measurements": 523,
  "cells_varying_catalyst_reagent_ratio": 3,
  "cells_measuring_between_heat_actions": 13
}
```

All 48 physical sources completed and their reports record verified replay. One chain is incomplete:

- RX-W04--S--safety_constrained_optimization--MisIndexed: missing K1; valid Q/K2 do not repair the sealing order.

## Observed source behavior

Scores below belong to the recommended batch observed during exploration, not an independent retest. They are not comparable to EC or PA scores.

| Locus | Goal | Cells | Mean selected source score | Varying dose ratio | Measurement between heats |
|---|---|---:|---:|---:|---:|
| P | mechanism_discovery | 12 | 0.39347 | 3 | 5 |
| P | safety_constrained_optimization | 12 | 0.38130 | 0 | 1 |
| S | mechanism_discovery | 12 | 0.29628 | 0 | 4 |
| S | safety_constrained_optimization | 12 | 0.29919 | 0 | 3 |

P: optimization has a higher selected source score in 5/12 matched conditions.

S: optimization has a higher selected source score in 5/12 matched conditions.

These are descriptive action counts: a measurement between heat calls does not establish a model reflection or feedback-dependent decision. Dose variation is not a mechanism-discovery score. P/S Opaque sources have the same prior input but different prediction questions; their difference is not a prior-locus treatment effect.

## Complete source index

| Cell | Sealed chain | Source score |
|---|:---:|---:|
| [RX-W01--P--mechanism_discovery--Aligned](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W01/RX-W01--P--mechanism_discovery--Aligned/EXPERIMENT_REPORT.md) | True | 0.41001 |
| [RX-W01--P--mechanism_discovery--MisIndexed](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W01/RX-W01--P--mechanism_discovery--MisIndexed/EXPERIMENT_REPORT.md) | True | 0.38057 |
| [RX-W01--P--mechanism_discovery--Opaque](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W01/RX-W01--P--mechanism_discovery--Opaque/EXPERIMENT_REPORT.md) | True | 0.25663 |
| [RX-W01--P--safety_constrained_optimization--Aligned](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W01/RX-W01--P--safety_constrained_optimization--Aligned/EXPERIMENT_REPORT.md) | True | 0.41178 |
| [RX-W01--P--safety_constrained_optimization--MisIndexed](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W01/RX-W01--P--safety_constrained_optimization--MisIndexed/EXPERIMENT_REPORT.md) | True | 0.36161 |
| [RX-W01--P--safety_constrained_optimization--Opaque](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W01/RX-W01--P--safety_constrained_optimization--Opaque/EXPERIMENT_REPORT.md) | True | 0.28404 |
| [RX-W01--S--mechanism_discovery--Aligned](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W01/RX-W01--S--mechanism_discovery--Aligned/EXPERIMENT_REPORT.md) | True | 0.31139 |
| [RX-W01--S--mechanism_discovery--MisIndexed](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W01/RX-W01--S--mechanism_discovery--MisIndexed/EXPERIMENT_REPORT.md) | True | 0.31771 |
| [RX-W01--S--mechanism_discovery--Opaque](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W01/RX-W01--S--mechanism_discovery--Opaque/EXPERIMENT_REPORT.md) | True | 0.28667 |
| [RX-W01--S--safety_constrained_optimization--Aligned](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W01/RX-W01--S--safety_constrained_optimization--Aligned/EXPERIMENT_REPORT.md) | True | 0.28457 |
| [RX-W01--S--safety_constrained_optimization--MisIndexed](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W01/RX-W01--S--safety_constrained_optimization--MisIndexed/EXPERIMENT_REPORT.md) | True | 0.29071 |
| [RX-W01--S--safety_constrained_optimization--Opaque](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W01/RX-W01--S--safety_constrained_optimization--Opaque/EXPERIMENT_REPORT.md) | True | 0.24544 |
| [RX-W02--P--mechanism_discovery--Aligned](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W02/RX-W02--P--mechanism_discovery--Aligned/EXPERIMENT_REPORT.md) | True | 0.41504 |
| [RX-W02--P--mechanism_discovery--MisIndexed](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W02/RX-W02--P--mechanism_discovery--MisIndexed/EXPERIMENT_REPORT.md) | True | 0.41432 |
| [RX-W02--P--mechanism_discovery--Opaque](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W02/RX-W02--P--mechanism_discovery--Opaque/EXPERIMENT_REPORT.md) | True | 0.21102 |
| [RX-W02--P--safety_constrained_optimization--Aligned](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W02/RX-W02--P--safety_constrained_optimization--Aligned/EXPERIMENT_REPORT.md) | True | 0.35582 |
| [RX-W02--P--safety_constrained_optimization--MisIndexed](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W02/RX-W02--P--safety_constrained_optimization--MisIndexed/EXPERIMENT_REPORT.md) | True | 0.38085 |
| [RX-W02--P--safety_constrained_optimization--Opaque](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W02/RX-W02--P--safety_constrained_optimization--Opaque/EXPERIMENT_REPORT.md) | True | 0.22870 |
| [RX-W02--S--mechanism_discovery--Aligned](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W02/RX-W02--S--mechanism_discovery--Aligned/EXPERIMENT_REPORT.md) | True | 0.21496 |
| [RX-W02--S--mechanism_discovery--MisIndexed](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W02/RX-W02--S--mechanism_discovery--MisIndexed/EXPERIMENT_REPORT.md) | True | 0.25567 |
| [RX-W02--S--mechanism_discovery--Opaque](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W02/RX-W02--S--mechanism_discovery--Opaque/EXPERIMENT_REPORT.md) | True | 0.15830 |
| [RX-W02--S--safety_constrained_optimization--Aligned](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W02/RX-W02--S--safety_constrained_optimization--Aligned/EXPERIMENT_REPORT.md) | True | 0.25695 |
| [RX-W02--S--safety_constrained_optimization--MisIndexed](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W02/RX-W02--S--safety_constrained_optimization--MisIndexed/EXPERIMENT_REPORT.md) | True | 0.23462 |
| [RX-W02--S--safety_constrained_optimization--Opaque](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/RX-W02/RX-W02--S--safety_constrained_optimization--Opaque/EXPERIMENT_REPORT.md) | True | 0.22351 |
| [RX-W03--P--mechanism_discovery--Aligned](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W03/RX-W03--P--mechanism_discovery--Aligned/EXPERIMENT_REPORT.md) | True | 0.49101 |
| [RX-W03--P--mechanism_discovery--MisIndexed](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W03/RX-W03--P--mechanism_discovery--MisIndexed/EXPERIMENT_REPORT.md) | True | 0.49390 |
| [RX-W03--P--mechanism_discovery--Opaque](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W03/RX-W03--P--mechanism_discovery--Opaque/EXPERIMENT_REPORT.md) | True | 0.35043 |
| [RX-W03--P--safety_constrained_optimization--Aligned](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W03/RX-W03--P--safety_constrained_optimization--Aligned/EXPERIMENT_REPORT.md) | True | 0.49469 |
| [RX-W03--P--safety_constrained_optimization--MisIndexed](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W03/RX-W03--P--safety_constrained_optimization--MisIndexed/EXPERIMENT_REPORT.md) | True | 0.46794 |
| [RX-W03--P--safety_constrained_optimization--Opaque](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W03/RX-W03--P--safety_constrained_optimization--Opaque/EXPERIMENT_REPORT.md) | True | 0.33777 |
| [RX-W03--S--mechanism_discovery--Aligned](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W03/RX-W03--S--mechanism_discovery--Aligned/EXPERIMENT_REPORT.md) | True | 0.33698 |
| [RX-W03--S--mechanism_discovery--MisIndexed](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W03/RX-W03--S--mechanism_discovery--MisIndexed/EXPERIMENT_REPORT.md) | True | 0.32859 |
| [RX-W03--S--mechanism_discovery--Opaque](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W03/RX-W03--S--mechanism_discovery--Opaque/EXPERIMENT_REPORT.md) | True | 0.31561 |
| [RX-W03--S--safety_constrained_optimization--Aligned](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W03/RX-W03--S--safety_constrained_optimization--Aligned/EXPERIMENT_REPORT.md) | True | 0.32646 |
| [RX-W03--S--safety_constrained_optimization--MisIndexed](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W03/RX-W03--S--safety_constrained_optimization--MisIndexed/EXPERIMENT_REPORT.md) | True | 0.38602 |
| [RX-W03--S--safety_constrained_optimization--Opaque](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W03/RX-W03--S--safety_constrained_optimization--Opaque/EXPERIMENT_REPORT.md) | True | 0.33164 |
| [RX-W04--P--mechanism_discovery--Aligned](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W04/RX-W04--P--mechanism_discovery--Aligned/EXPERIMENT_REPORT.md) | True | 0.47186 |
| [RX-W04--P--mechanism_discovery--MisIndexed](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W04/RX-W04--P--mechanism_discovery--MisIndexed/EXPERIMENT_REPORT.md) | True | 0.47570 |
| [RX-W04--P--mechanism_discovery--Opaque](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W04/RX-W04--P--mechanism_discovery--Opaque/EXPERIMENT_REPORT.md) | True | 0.35121 |
| [RX-W04--P--safety_constrained_optimization--Aligned](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W04/RX-W04--P--safety_constrained_optimization--Aligned/EXPERIMENT_REPORT.md) | True | 0.44892 |
| [RX-W04--P--safety_constrained_optimization--MisIndexed](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W04/RX-W04--P--safety_constrained_optimization--MisIndexed/EXPERIMENT_REPORT.md) | True | 0.45156 |
| [RX-W04--P--safety_constrained_optimization--Opaque](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W04/RX-W04--P--safety_constrained_optimization--Opaque/EXPERIMENT_REPORT.md) | True | 0.35197 |
| [RX-W04--S--mechanism_discovery--Aligned](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W04/RX-W04--S--mechanism_discovery--Aligned/EXPERIMENT_REPORT.md) | True | 0.33305 |
| [RX-W04--S--mechanism_discovery--MisIndexed](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W04/RX-W04--S--mechanism_discovery--MisIndexed/EXPERIMENT_REPORT.md) | True | 0.34118 |
| [RX-W04--S--mechanism_discovery--Opaque](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W04/RX-W04--S--mechanism_discovery--Opaque/EXPERIMENT_REPORT.md) | True | 0.35520 |
| [RX-W04--S--safety_constrained_optimization--Aligned](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W04/RX-W04--S--safety_constrained_optimization--Aligned/EXPERIMENT_REPORT.md) | True | 0.34228 |
| [RX-W04--S--safety_constrained_optimization--MisIndexed](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W04/RX-W04--S--safety_constrained_optimization--MisIndexed/EXPERIMENT_REPORT.md) | False | 0.33631 |
| [RX-W04--S--safety_constrained_optimization--Opaque](https://github.com/sunyrain/ChemWorld/blob/25537865465fdaadcee704912305d17d3f84c7bc/workstreams/flagship_tasks/reports/work-ii-rx-ps-five-world-dual-goal-20260919-w03-w04/RX-W04/RX-W04--S--safety_constrained_optimization--Opaque/EXPERIMENT_REPORT.md) | True | 0.33173 |

## Interpretation boundary

RX contributes parameter and structural prior interventions, time/temperature/history experiments, free mechanism reports and paired research objectives. Prediction errors, calibrated interval coverage, independently retested recommendations and causal explanations of failures are not established by these published records. Do not pool it with the completed EC/PA prediction analysis or call all nine systems completed.
