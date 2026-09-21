# Experiment inventory: machine-generated snapshot

Observed at 2026-09-21T01:45:39+08:00; remote evidence at `1eda66585df7d8ae922bb251804dec1d3bb3d058`.

This report reads existing exports only. No provider call, physics execution, runtime checkout or evidence reclassification is performed.

## Current cohorts

| Block | Source sessions | Complete chains | Source batches | Sealed K1/Q/K2 | Other questions |
|---|---:|---:|---:|---:|---:|
| EC E, two goals, 12/24, five worlds | 60 | 60 | 1080 | 180 | 0 |
| PA E, discovery, 12/24, five worlds | 30 | 30 | 540 | 90 | 0 |
| EC P/S single-world supplements | 12 | 11 | 144 | 34 | 0 |
| RX P/S, two goals, 12, five worlds | 60 | 60 | 720 | 180 | 0 |
| EQ bounded/P v2, 12, five worlds | 15 | 15 | 180 | 45 | 15 EQS |
| EQ-S v0.2.1 closed-set pilot | 15 | 15 | 180 | 45 | 15 EQS |
| EQ-S v0.3 canonical free-mechanism study | 15 | 15 | 180 | 45 | 0 |
| C E v3, 12/24, five worlds | 30/30 | 29 | 539/540 | 90/90 | 0 |
| P E, 12 only | 15 | 14 | 178/180 | 45/45 | 0 |

P source batches count final-assayed batches. Its separate lifecycle totals are {'discarded': 2, 'final_assayed': 178, 'started': 180}; discarded batches consumed source resources and are not replacement sessions.

The current primary analysis pool contains 225 started sources, 223 complete chains, 3417/3420 source batches, and 675/675 K1/Q/K2 stages. The 15 EQ supplements are additional; C completion issues remain visible.

The four complete primary system cohorts contain 165 sessions, 2,520 source batches and 495 canonical posttest stages, plus 15 EQ-specific supplements. This is a scope subtotal, not a count of all historical research. Qualification recipes, reference repeats, replays, retries and reused source states are different units and are not added to it.

## EC/PA complete E cohort

| System / goal | Budget | n | MAE | Coverage | Task readout |
|---|---:|---:|---:|---:|---|
| EC / discovery | 12 | 15 | 0.17378 | 61.1% | retest 0.53638 |
| EC / discovery | 24 | 15 | 0.11222 | 71.7% | retest 0.54903 |
| EC / optimization | 12 | 15 | 0.17811 | 55.6% | retest 0.66404 |
| EC / optimization | 24 | 15 | 0.10818 | 73.9% | retest 0.74792 |
| PA / discovery | 12 | 15 | 0.08291 | 78.3% | decisions 25/30 |
| PA / discovery | 24 | 15 | 0.02379 | 98.9% | decisions 30/30 |

EC coverage is nominal 80%; PA is nominal 90%. MAEs have different targets and are not pooled.

## RX descriptive arm means

| Locus | Goal | Arm | n | Macro MAE | 80% coverage | Retest |
|---|---|---|---:|---:|---:|---:|
| P | mechanism_discovery | Aligned | 5 | 0.05701 | 76.3% | 0.45516 |
| P | mechanism_discovery | MisIndexed | 5 | 0.05457 | 80.3% | 0.45226 |
| P | mechanism_discovery | Opaque | 5 | 0.10186 | 60.3% | 0.30241 |
| P | safety_constrained_optimization | Aligned | 5 | 0.08384 | 70.1% | 0.43318 |
| P | safety_constrained_optimization | MisIndexed | 5 | 0.12967 | 63.9% | 0.42004 |
| P | safety_constrained_optimization | Opaque | 5 | 0.13893 | 46.7% | 0.30256 |
| S | mechanism_discovery | Aligned | 5 | 0.09209 | 74.2% | 0.30922 |
| S | mechanism_discovery | MisIndexed | 5 | 0.10159 | 66.7% | 0.31832 |
| S | mechanism_discovery | Opaque | 5 | 0.08404 | 83.4% | 0.29447 |
| S | safety_constrained_optimization | Aligned | 5 | 0.11932 | 67.2% | 0.31439 |
| S | safety_constrained_optimization | MisIndexed | 5 | 0.09221 | 69.3% | 0.32895 |
| S | safety_constrained_optimization | Opaque | 5 | 0.11227 | 62.2% | 0.29351 |

## EQ bounded/P v2 descriptive means

| Arm | n | Macro MAE | 80% coverage | Width |
|---|---:|---:|---:|---:|
| Aligned | 5 | 0.04314 | 69.0% | 0.04526 |
| MisIndexed | 5 | 0.03928 | 70.7% | 0.04507 |
| Opaque | 5 | 0.01214 | 91.3% | 0.07448 |

EQ-S v0.2.1 is a separate closed-set pilot (15/15 abstentions). The v0.3 note explicitly supersedes its participant contract. The canonical v0.3 export is now complete and included in the primary pool.

## Current C incompleteness

- C-W02-B12-E-Opaque: failed; batches 11/12; posttests 3/3; failure `None`; source nonconformance `{'completed_batches': 11, 'planned_batches': 12}`.

A missing C batch remains a source nonconformance; valid predictions remain analyzable with that label. A reporting/baseline exception after K2 is not a failed scientific answer.

## Historical inventory and source navigation

[summary.json](summary.json) retains the current registry entries, static programme denominators, explicit input locations and an index of the top-level historical JSON reports. It does not sum overlapping historical exports as independent experiments. [ANALYSIS.md](ANALYSIS.md) gives the evidence disposition and closure plan.
