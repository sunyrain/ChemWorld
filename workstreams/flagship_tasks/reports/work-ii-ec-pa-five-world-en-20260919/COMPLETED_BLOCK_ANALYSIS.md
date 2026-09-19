# Descriptive analysis: complete EC and PA world blocks

Generated: 2026-09-19T18:03:19+08:00. complete entity-prior cohort; descriptive development evidence.

Selection: EC: W01, W02, W03, W04, W05; PA: W01, W02, W03, W04, W05. All arms, both budgets and both EC goals are included. Any unfinished world blocks and the P/S pilot are outside this comparison, not excluded from the live study denominator. Scope is determined by completion in the fixed schedule, never by observed performance.

[Live matrix](REPORT.md) · [Machine-readable analysis](completed-block-analysis.json)

## Coverage

```json
{
  "campaigns": 90,
  "source_batches": 1620,
  "posttests": 270,
  "first_attempt_completed": 68,
  "recovered_campaigns": 22,
  "ec_recommendation_retests": 60
}
```

22 recovered campaigns and 68 first-attempt completions form this 90-campaign block. Source batches here count effective campaigns; abandoned attempts, replay and recommendation retests are additional. All included campaigns have complete posttests and verified source replay.

## Budget summaries

EC reports score-prediction MAE and nominal 80% intervals; PA reports organic-product-fraction MAE and nominal 90% intervals. The metrics are not combined across systems. Each row averages all arms in the selected worlds, with equal campaign weights.

| System / assignment | Budget | Mean MAE | Interval coverage | Mean interval width | Task readout |
|---|---:|---:|---:|---:|---|
| EC / discovery | 12 | 0.17378 | 61.1% | 0.19831 | Mean retest score 0.53638 |
| EC / discovery | 24 | 0.11222 | 71.7% | 0.22007 | Mean retest score 0.54903 |
| EC / optimization | 12 | 0.17811 | 55.6% | 0.19935 | Mean retest score 0.66404 |
| EC / optimization | 24 | 0.10818 | 73.9% | 0.20814 | Mean retest score 0.74792 |
| PA / discovery | 12 | 0.08291 | 78.3% | 0.25122 | 25/30 decisions |
| PA / discovery | 24 | 0.02379 | 98.9% | 0.18553 | 30/30 decisions |

## Matched contrasts and recovery sensitivity

Counts describe paired conditions, not independent worlds or significance tests.

| Comparison | All effective pairs | Pairs with both first attempts complete |
|---|---:|---:|
| EC discovery: lower MAE at 24 | 11/15 | 4/5 |
| EC optimization: lower MAE at 24 | 12/15 | 8/11 |
| PA discovery: lower MAE at 24 | 13/15 | 8/10 |
| EC optimization: higher recommendation score | 26/30 | 15/17 |
| EC optimization: lower prediction MAE | 14/30 | 8/17 |

Optimization has both a better retest and lower prediction MAE in 13/30 pairs. It has a better retest but higher MAE in 13/30 pairs (7/17 first-attempt-only pairs). There are 0 pairs tied on either outcome.

## All six electrochemical prediction metrics

Each entry counts matched conditions with lower MAE. These correlated outcomes do not constitute six independent replications of the experiment.

| Metric | 24 vs 12: discovery | 24 vs 12: optimization | Optimization vs discovery |
|---|---:|---:|---:|
| electrochemical_selectivity | 11/15 | 14/15 | 15/30 |
| energy_efficiency | 11/15 | 11/15 | 16/30 |
| faradaic_efficiency | 11/15 | 13/15 | 11/30 |
| score | 11/15 | 12/15 | 14/30 |
| selective_product_yield | 12/15 | 12/15 | 15/30 |
| transport_efficiency | 11/15 | 11/15 | 12/30 |

## Prior-arm results

Each mean uses all selected worlds for that system. A lower MAE is better; EC retest score and PA decision accuracy are separate task outcomes.

| System / assignment | Budget | Arm | Campaigns | Mean MAE | Task readout |
|---|---:|---|---:|---:|---|
| EC / discovery | 12 | Opaque | 5 | 0.19534 | Retest 0.50686 |
| EC / discovery | 12 | Aligned | 5 | 0.19393 | Retest 0.47306 |
| EC / discovery | 12 | MisIndexed | 5 | 0.13206 | Retest 0.62922 |
| EC / discovery | 24 | Opaque | 5 | 0.12011 | Retest 0.49276 |
| EC / discovery | 24 | Aligned | 5 | 0.14521 | Retest 0.53549 |
| EC / discovery | 24 | MisIndexed | 5 | 0.07133 | Retest 0.61884 |
| EC / optimization | 12 | Opaque | 5 | 0.19474 | Retest 0.60726 |
| EC / optimization | 12 | Aligned | 5 | 0.15612 | Retest 0.75512 |
| EC / optimization | 12 | MisIndexed | 5 | 0.18349 | Retest 0.62972 |
| EC / optimization | 24 | Opaque | 5 | 0.11127 | Retest 0.78160 |
| EC / optimization | 24 | Aligned | 5 | 0.09961 | Retest 0.79539 |
| EC / optimization | 24 | MisIndexed | 5 | 0.11365 | Retest 0.66677 |
| PA / discovery | 12 | Opaque | 5 | 0.09886 | 8/10 decisions |
| PA / discovery | 12 | Aligned | 5 | 0.07124 | 10/10 decisions |
| PA / discovery | 12 | MisIndexed | 5 | 0.07863 | 7/10 decisions |
| PA / discovery | 24 | Opaque | 5 | 0.02106 | 10/10 decisions |
| PA / discovery | 24 | Aligned | 5 | 0.02962 | 10/10 decisions |
| PA / discovery | 24 | MisIndexed | 5 | 0.02071 | 10/10 decisions |

Paired counts below compare the same world, goal and budget. Differences include experiment-selection differences and stochastic session variation.

| System / assignment | Budget | First vs second arm | First lower MAE | Mean MAE difference | First-attempt-only wins/pairs |
|---|---:|---|---:|---:|---:|
| EC / discovery | 12 | Aligned vs Opaque | 2/5 | -0.00140 | 1/3 |
| EC / discovery | 12 | MisIndexed vs Opaque | 4/5 | -0.06328 | 2/2 |
| EC / discovery | 12 | Aligned vs MisIndexed | 1/5 | 0.06187 | 1/2 |
| EC / discovery | 24 | Aligned vs Opaque | 3/5 | 0.02509 | 1/1 |
| EC / discovery | 24 | MisIndexed vs Opaque | 4/5 | -0.04879 | 2/2 |
| EC / discovery | 24 | Aligned vs MisIndexed | 2/5 | 0.07388 | 1/2 |
| EC / optimization | 12 | Aligned vs Opaque | 2/5 | -0.03862 | 1/4 |
| EC / optimization | 12 | MisIndexed vs Opaque | 3/5 | -0.01124 | 2/4 |
| EC / optimization | 12 | Aligned vs MisIndexed | 4/5 | -0.02737 | 3/4 |
| EC / optimization | 24 | Aligned vs Opaque | 3/5 | -0.01166 | 1/3 |
| EC / optimization | 24 | MisIndexed vs Opaque | 1/5 | 0.00238 | 0/4 |
| EC / optimization | 24 | Aligned vs MisIndexed | 4/5 | -0.01404 | 3/3 |
| PA / discovery | 12 | Aligned vs Opaque | 3/5 | -0.02762 | 2/4 |
| PA / discovery | 12 | MisIndexed vs Opaque | 2/5 | -0.02023 | 1/3 |
| PA / discovery | 12 | Aligned vs MisIndexed | 3/5 | -0.00739 | 1/3 |
| PA / discovery | 24 | Aligned vs Opaque | 3/5 | 0.00856 | 3/5 |
| PA / discovery | 24 | MisIndexed vs Opaque | 3/5 | -0.00034 | 2/4 |
| PA / discovery | 24 | Aligned vs MisIndexed | 3/5 | 0.00891 | 2/4 |

## World-level means

Each row averages the three arms. These retain between-world heterogeneity; the worlds are instances within a shared system family.

| System / assignment | World | Budget | Mean MAE |
|---|---|---:|---:|
| EC / discovery | EC-W01 | 12 | 0.19903 |
| EC / discovery | EC-W02 | 12 | 0.15712 |
| EC / discovery | EC-W03 | 12 | 0.12348 |
| EC / discovery | EC-W04 | 12 | 0.23016 |
| EC / discovery | EC-W05 | 12 | 0.15909 |
| EC / discovery | EC-W01 | 24 | 0.11332 |
| EC / discovery | EC-W02 | 24 | 0.08276 |
| EC / discovery | EC-W03 | 24 | 0.10696 |
| EC / discovery | EC-W04 | 24 | 0.08426 |
| EC / discovery | EC-W05 | 24 | 0.17380 |
| EC / optimization | EC-W01 | 12 | 0.15094 |
| EC / optimization | EC-W02 | 12 | 0.08695 |
| EC / optimization | EC-W03 | 12 | 0.20484 |
| EC / optimization | EC-W04 | 12 | 0.20025 |
| EC / optimization | EC-W05 | 12 | 0.24759 |
| EC / optimization | EC-W01 | 24 | 0.16482 |
| EC / optimization | EC-W02 | 24 | 0.04853 |
| EC / optimization | EC-W03 | 24 | 0.07819 |
| EC / optimization | EC-W04 | 24 | 0.11513 |
| EC / optimization | EC-W05 | 24 | 0.13420 |
| PA / discovery | PA-W01 | 12 | 0.05592 |
| PA / discovery | PA-W02 | 12 | 0.09117 |
| PA / discovery | PA-W03 | 12 | 0.06969 |
| PA / discovery | PA-W04 | 12 | 0.14882 |
| PA / discovery | PA-W05 | 12 | 0.04894 |
| PA / discovery | PA-W01 | 24 | 0.01381 |
| PA / discovery | PA-W02 | 24 | 0.02102 |
| PA / discovery | PA-W03 | 24 | 0.01907 |
| PA / discovery | PA-W04 | 24 | 0.01978 |
| PA / discovery | PA-W05 | 24 | 0.04529 |

## Complete per-campaign table

Asterisk indicates a separately retained infrastructure recovery. EC score and PA organic fraction are different outcomes.

| Campaign | Prediction MAE | Coverage | Width | Task readout |
|---|---:|---:|---:|---|
| [EC-W01-B12-discovery-E-Opaque](EC-W01-B12-discovery-E-Opaque/REPORT.md) | 0.08839 | 75.0% | 0.25000 | Retest 0.71759 |
| [EC-W01-B12-discovery-E-Aligned*](EC-W01-B12-discovery-E-Aligned/network-recovery/REPORT.md) | 0.26198 | 50.0% | 0.12083 | Retest 0.38066 |
| [EC-W01-B12-discovery-E-MisIndexed*](EC-W01-B12-discovery-E-MisIndexed/network-recovery/REPORT.md) | 0.24672 | 50.0% | 0.13042 | Retest 0.46525 |
| [EC-W01-B12-optimization-E-Opaque](EC-W01-B12-optimization-E-Opaque/REPORT.md) | 0.22940 | 41.7% | 0.27833 | Retest 0.75612 |
| [EC-W01-B12-optimization-E-Aligned](EC-W01-B12-optimization-E-Aligned/REPORT.md) | 0.05723 | 91.7% | 0.24400 | Retest 0.73620 |
| [EC-W01-B12-optimization-E-MisIndexed](EC-W01-B12-optimization-E-MisIndexed/REPORT.md) | 0.16618 | 66.7% | 0.28917 | Retest 0.76748 |
| [PA-W01-B12-discovery-E-Opaque](PA-W01-B12-discovery-E-Opaque/REPORT.md) | 0.04834 | 100.0% | 0.16833 | 2/2 decisions |
| [PA-W01-B12-discovery-E-Aligned](PA-W01-B12-discovery-E-Aligned/REPORT.md) | 0.06699 | 75.0% | 0.23833 | 2/2 decisions |
| [PA-W01-B12-discovery-E-MisIndexed](PA-W01-B12-discovery-E-MisIndexed/REPORT.md) | 0.05243 | 100.0% | 0.17417 | 2/2 decisions |
| [EC-W01-B24-discovery-E-Opaque*](EC-W01-B24-discovery-E-Opaque/host-recovery/REPORT.md) | 0.07074 | 83.3% | 0.20458 | Retest 0.59822 |
| [EC-W01-B24-discovery-E-Aligned](EC-W01-B24-discovery-E-Aligned/REPORT.md) | 0.23245 | 50.0% | 0.18358 | Retest 0.48830 |
| [EC-W01-B24-discovery-E-MisIndexed](EC-W01-B24-discovery-E-MisIndexed/REPORT.md) | 0.03676 | 100.0% | 0.16667 | Retest 0.53391 |
| [EC-W01-B24-optimization-E-Opaque](EC-W01-B24-optimization-E-Opaque/REPORT.md) | 0.12331 | 75.0% | 0.21000 | Retest 0.84341 |
| [EC-W01-B24-optimization-E-Aligned](EC-W01-B24-optimization-E-Aligned/REPORT.md) | 0.17917 | 41.7% | 0.09833 | Retest 0.77910 |
| [EC-W01-B24-optimization-E-MisIndexed](EC-W01-B24-optimization-E-MisIndexed/REPORT.md) | 0.19199 | 58.3% | 0.25000 | Retest 0.54716 |
| [PA-W01-B24-discovery-E-Opaque](PA-W01-B24-discovery-E-Opaque/REPORT.md) | 0.01294 | 100.0% | 0.18167 | 2/2 decisions |
| [PA-W01-B24-discovery-E-Aligned](PA-W01-B24-discovery-E-Aligned/REPORT.md) | 0.00683 | 100.0% | 0.14167 | 2/2 decisions |
| [PA-W01-B24-discovery-E-MisIndexed](PA-W01-B24-discovery-E-MisIndexed/REPORT.md) | 0.02168 | 100.0% | 0.21833 | 2/2 decisions |
| [EC-W02-B12-discovery-E-Aligned](EC-W02-B12-discovery-E-Aligned/REPORT.md) | 0.07176 | 83.3% | 0.23167 | Retest 0.67930 |
| [EC-W02-B12-discovery-E-MisIndexed](EC-W02-B12-discovery-E-MisIndexed/REPORT.md) | 0.12581 | 75.0% | 0.24250 | Retest 0.63568 |
| [EC-W02-B12-discovery-E-Opaque](EC-W02-B12-discovery-E-Opaque/REPORT.md) | 0.27380 | 41.7% | 0.13292 | Retest 0.42021 |
| [EC-W02-B12-optimization-E-Aligned](EC-W02-B12-optimization-E-Aligned/REPORT.md) | 0.07412 | 83.3% | 0.20500 | Retest 0.80652 |
| [EC-W02-B12-optimization-E-MisIndexed](EC-W02-B12-optimization-E-MisIndexed/REPORT.md) | 0.13889 | 50.0% | 0.23917 | Retest 0.67930 |
| [EC-W02-B12-optimization-E-Opaque](EC-W02-B12-optimization-E-Opaque/REPORT.md) | 0.04784 | 100.0% | 0.25583 | Retest 0.67930 |
| [PA-W02-B12-discovery-E-Aligned](PA-W02-B12-discovery-E-Aligned/REPORT.md) | 0.03332 | 100.0% | 0.21000 | 2/2 decisions |
| [PA-W02-B12-discovery-E-MisIndexed](PA-W02-B12-discovery-E-MisIndexed/REPORT.md) | 0.13023 | 50.0% | 0.26000 | 1/2 decisions |
| [PA-W02-B12-discovery-E-Opaque](PA-W02-B12-discovery-E-Opaque/REPORT.md) | 0.10998 | 75.0% | 0.36250 | 1/2 decisions |
| [EC-W02-B24-discovery-E-Aligned](EC-W02-B24-discovery-E-Aligned/REPORT.md) | 0.04861 | 91.7% | 0.20333 | Retest 0.61502 |
| [EC-W02-B24-discovery-E-MisIndexed](EC-W02-B24-discovery-E-MisIndexed/REPORT.md) | 0.06307 | 75.0% | 0.23750 | Retest 0.56638 |
| [EC-W02-B24-discovery-E-Opaque](EC-W02-B24-discovery-E-Opaque/REPORT.md) | 0.13659 | 50.0% | 0.28667 | Retest 0.59826 |
| [EC-W02-B24-optimization-E-Aligned*](EC-W02-B24-optimization-E-Aligned/network-recovery/REPORT.md) | 0.03751 | 100.0% | 0.22917 | Retest 0.82546 |
| [EC-W02-B24-optimization-E-MisIndexed](EC-W02-B24-optimization-E-MisIndexed/REPORT.md) | 0.05460 | 83.3% | 0.23333 | Retest 0.79824 |
| [EC-W02-B24-optimization-E-Opaque](EC-W02-B24-optimization-E-Opaque/REPORT.md) | 0.05349 | 91.7% | 0.18958 | Retest 0.84322 |
| [PA-W02-B24-discovery-E-Aligned](PA-W02-B24-discovery-E-Aligned/REPORT.md) | 0.03491 | 100.0% | 0.23750 | 2/2 decisions |
| [PA-W02-B24-discovery-E-MisIndexed](PA-W02-B24-discovery-E-MisIndexed/REPORT.md) | 0.01926 | 100.0% | 0.22667 | 2/2 decisions |
| [PA-W02-B24-discovery-E-Opaque](PA-W02-B24-discovery-E-Opaque/REPORT.md) | 0.00888 | 100.0% | 0.22083 | 2/2 decisions |
| [EC-W03-B12-discovery-E-MisIndexed](EC-W03-B12-discovery-E-MisIndexed/REPORT.md) | 0.06011 | 100.0% | 0.29250 | Retest 0.73089 |
| [EC-W03-B12-discovery-E-Opaque](EC-W03-B12-discovery-E-Opaque/REPORT.md) | 0.06497 | 75.0% | 0.22167 | Retest 0.52708 |
| [EC-W03-B12-discovery-E-Aligned](EC-W03-B12-discovery-E-Aligned/REPORT.md) | 0.24537 | 50.0% | 0.13667 | Retest 0.36815 |
| [EC-W03-B12-optimization-E-MisIndexed](EC-W03-B12-optimization-E-MisIndexed/REPORT.md) | 0.12289 | 83.3% | 0.29833 | Retest 0.53350 |
| [EC-W03-B12-optimization-E-Opaque](EC-W03-B12-optimization-E-Opaque/REPORT.md) | 0.24565 | 50.0% | 0.10583 | Retest 0.59037 |
| [EC-W03-B12-optimization-E-Aligned](EC-W03-B12-optimization-E-Aligned/REPORT.md) | 0.24599 | 41.7% | 0.10833 | Retest 0.61365 |
| [PA-W03-B12-discovery-E-MisIndexed*](PA-W03-B12-discovery-E-MisIndexed/network-recovery-2/REPORT.md) | 0.09590 | 75.0% | 0.24917 | 1/2 decisions |
| [PA-W03-B12-discovery-E-Opaque*](PA-W03-B12-discovery-E-Opaque/network-recovery-2/REPORT.md) | 0.09832 | 66.7% | 0.30083 | 2/2 decisions |
| [PA-W03-B12-discovery-E-Aligned*](PA-W03-B12-discovery-E-Aligned/network-recovery-3/REPORT.md) | 0.01487 | 100.0% | 0.19167 | 2/2 decisions |
| [EC-W03-B24-discovery-E-MisIndexed*](EC-W03-B24-discovery-E-MisIndexed/network-recovery-2/REPORT.md) | 0.07562 | 83.3% | 0.21417 | Retest 0.56404 |
| [EC-W03-B24-discovery-E-Opaque](EC-W03-B24-discovery-E-Opaque/REPORT.md) | 0.17245 | 50.0% | 0.22417 | Retest 0.57684 |
| [EC-W03-B24-discovery-E-Aligned*](EC-W03-B24-discovery-E-Aligned/network-recovery-2/REPORT.md) | 0.07279 | 91.7% | 0.23667 | Retest 0.63755 |
| [EC-W03-B24-optimization-E-MisIndexed](EC-W03-B24-optimization-E-MisIndexed/REPORT.md) | 0.09233 | 83.3% | 0.20917 | Retest 0.87219 |
| [EC-W03-B24-optimization-E-Opaque](EC-W03-B24-optimization-E-Opaque/REPORT.md) | 0.08403 | 83.3% | 0.19583 | Retest 0.87467 |
| [EC-W03-B24-optimization-E-Aligned](EC-W03-B24-optimization-E-Aligned/REPORT.md) | 0.05822 | 91.7% | 0.20625 | Retest 0.73115 |
| [PA-W03-B24-discovery-E-MisIndexed](PA-W03-B24-discovery-E-MisIndexed/REPORT.md) | 0.01770 | 100.0% | 0.12875 | 2/2 decisions |
| [PA-W03-B24-discovery-E-Opaque](PA-W03-B24-discovery-E-Opaque/REPORT.md) | 0.02668 | 100.0% | 0.22833 | 2/2 decisions |
| [PA-W03-B24-discovery-E-Aligned](PA-W03-B24-discovery-E-Aligned/REPORT.md) | 0.01284 | 100.0% | 0.15333 | 2/2 decisions |
| [EC-W04-B12-discovery-E-Opaque](EC-W04-B12-discovery-E-Opaque/REPORT.md) | 0.25955 | 16.7% | 0.08125 | Retest 0.40469 |
| [EC-W04-B12-discovery-E-Aligned](EC-W04-B12-discovery-E-Aligned/REPORT.md) | 0.26551 | 41.7% | 0.16167 | Retest 0.31060 |
| [EC-W04-B12-discovery-E-MisIndexed*](EC-W04-B12-discovery-E-MisIndexed/network-recovery/REPORT.md) | 0.16542 | 33.3% | 0.22917 | Retest 0.69784 |
| [EC-W04-B12-optimization-E-Opaque](EC-W04-B12-optimization-E-Opaque/REPORT.md) | 0.15484 | 50.0% | 0.21042 | Retest 0.53050 |
| [EC-W04-B12-optimization-E-Aligned](EC-W04-B12-optimization-E-Aligned/REPORT.md) | 0.18360 | 41.7% | 0.15042 | Retest 0.76520 |
| [EC-W04-B12-optimization-E-MisIndexed](EC-W04-B12-optimization-E-MisIndexed/REPORT.md) | 0.26232 | 25.0% | 0.09292 | Retest 0.42463 |
| [PA-W04-B12-discovery-E-Opaque](PA-W04-B12-discovery-E-Opaque/REPORT.md) | 0.20285 | 41.7% | 0.37833 | 1/2 decisions |
| [PA-W04-B12-discovery-E-Aligned](PA-W04-B12-discovery-E-Aligned/REPORT.md) | 0.19271 | 33.3% | 0.24333 | 2/2 decisions |
| [PA-W04-B12-discovery-E-MisIndexed](PA-W04-B12-discovery-E-MisIndexed/REPORT.md) | 0.05089 | 91.7% | 0.26917 | 2/2 decisions |
| [EC-W04-B24-discovery-E-Opaque](EC-W04-B24-discovery-E-Opaque/REPORT.md) | 0.10838 | 75.0% | 0.29167 | Retest 0.54534 |
| [EC-W04-B24-discovery-E-Aligned*](EC-W04-B24-discovery-E-Aligned/network-recovery/REPORT.md) | 0.07765 | 91.7% | 0.21500 | Retest 0.53238 |
| [EC-W04-B24-discovery-E-MisIndexed](EC-W04-B24-discovery-E-MisIndexed/REPORT.md) | 0.06676 | 91.7% | 0.22750 | Retest 0.72503 |
| [EC-W04-B24-optimization-E-Opaque](EC-W04-B24-optimization-E-Opaque/REPORT.md) | 0.04319 | 83.3% | 0.16000 | Retest 0.68556 |
| [EC-W04-B24-optimization-E-Aligned](EC-W04-B24-optimization-E-Aligned/REPORT.md) | 0.12086 | 58.3% | 0.21917 | Retest 0.80136 |
| [EC-W04-B24-optimization-E-MisIndexed](EC-W04-B24-optimization-E-MisIndexed/REPORT.md) | 0.18134 | 50.0% | 0.22300 | Retest 0.47695 |
| [PA-W04-B24-discovery-E-Opaque](PA-W04-B24-discovery-E-Opaque/REPORT.md) | 0.02866 | 100.0% | 0.19833 | 2/2 decisions |
| [PA-W04-B24-discovery-E-Aligned](PA-W04-B24-discovery-E-Aligned/REPORT.md) | 0.01096 | 100.0% | 0.19083 | 2/2 decisions |
| [PA-W04-B24-discovery-E-MisIndexed*](PA-W04-B24-discovery-E-MisIndexed/network-recovery/REPORT.md) | 0.01970 | 100.0% | 0.16250 | 2/2 decisions |
| [EC-W05-B12-discovery-E-Aligned*](EC-W05-B12-discovery-E-Aligned/network-recovery/REPORT.md) | 0.12505 | 75.0% | 0.30667 | Retest 0.62659 |
| [EC-W05-B12-discovery-E-MisIndexed*](EC-W05-B12-discovery-E-MisIndexed/network-recovery-2/REPORT.md) | 0.06224 | 100.0% | 0.26833 | Retest 0.61645 |
| [EC-W05-B12-discovery-E-Opaque](EC-W05-B12-discovery-E-Opaque/REPORT.md) | 0.28997 | 50.0% | 0.16833 | Retest 0.46472 |
| [EC-W05-B12-optimization-E-Aligned*](EC-W05-B12-optimization-E-Aligned/network-recovery-2/REPORT.md) | 0.21964 | 33.3% | 0.17250 | Retest 0.85404 |
| [EC-W05-B12-optimization-E-MisIndexed*](EC-W05-B12-optimization-E-MisIndexed/network-recovery/REPORT.md) | 0.22718 | 41.7% | 0.20917 | Retest 0.74371 |
| [EC-W05-B12-optimization-E-Opaque](EC-W05-B12-optimization-E-Opaque/REPORT.md) | 0.29595 | 33.3% | 0.13083 | Retest 0.48004 |
| [PA-W05-B12-discovery-E-Aligned](PA-W05-B12-discovery-E-Aligned/REPORT.md) | 0.04829 | 91.7% | 0.21250 | 2/2 decisions |
| [PA-W05-B12-discovery-E-MisIndexed*](PA-W05-B12-discovery-E-MisIndexed/network-recovery/REPORT.md) | 0.06371 | 75.0% | 0.22500 | 1/2 decisions |
| [PA-W05-B12-discovery-E-Opaque](PA-W05-B12-discovery-E-Opaque/REPORT.md) | 0.03481 | 100.0% | 0.28500 | 2/2 decisions |
| [EC-W05-B24-discovery-E-Aligned*](EC-W05-B24-discovery-E-Aligned/network-recovery/REPORT.md) | 0.29455 | 41.7% | 0.13042 | Retest 0.40422 |
| [EC-W05-B24-discovery-E-MisIndexed](EC-W05-B24-discovery-E-MisIndexed/REPORT.md) | 0.11444 | 41.7% | 0.20167 | Retest 0.70482 |
| [EC-W05-B24-discovery-E-Opaque*](EC-W05-B24-discovery-E-Opaque/network-recovery-2/REPORT.md) | 0.11242 | 58.3% | 0.27750 | Retest 0.14513 |
| [EC-W05-B24-optimization-E-Aligned*](EC-W05-B24-optimization-E-Aligned/network-recovery/REPORT.md) | 0.10230 | 66.7% | 0.20333 | Retest 0.83988 |
| [EC-W05-B24-optimization-E-MisIndexed*](EC-W05-B24-optimization-E-MisIndexed/network-recovery/REPORT.md) | 0.04799 | 100.0% | 0.27583 | Retest 0.63931 |
| [EC-W05-B24-optimization-E-Opaque*](EC-W05-B24-optimization-E-Opaque/network-recovery/REPORT.md) | 0.25232 | 41.7% | 0.21917 | Retest 0.66113 |
| [PA-W05-B24-discovery-E-Aligned](PA-W05-B24-discovery-E-Aligned/REPORT.md) | 0.08256 | 83.3% | 0.19958 | 2/2 decisions |
| [PA-W05-B24-discovery-E-MisIndexed](PA-W05-B24-discovery-E-MisIndexed/REPORT.md) | 0.02522 | 100.0% | 0.15750 | 2/2 decisions |
| [PA-W05-B24-discovery-E-Opaque](PA-W05-B24-discovery-E-Opaque/REPORT.md) | 0.02811 | 100.0% | 0.13708 | 2/2 decisions |

## Interpretation limits

- One realization per condition; world instances within each system share a model family; no significance or population claim.
- 12/24 sessions are independent and do not share an experimental prefix.
- Queries, six EC metrics and complementary PA fractions are correlated readouts, not independent agent replicates.
- Means weight each campaign equally; the systems and EC metrics are not pooled into a total score.
- Recovery sensitivity excludes complete pairs containing a recovery; it is not a randomized first-attempt comparison.
- Mechanism correctness and causal information loss have not been established by this numerical analysis.
- The unfinished fixed queue and all infrastructure failures remain in the live matrix denominator.
