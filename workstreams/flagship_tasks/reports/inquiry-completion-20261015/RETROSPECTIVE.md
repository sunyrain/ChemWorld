# Source-only references and research paths

Retrospective analysis under W2-257. Cohorts and worlds are kept separate.

Corrected crystallization: 42/45 valid Q; missing sessions retained.
All means below weight the five world means equally. Lower MAE is better.

| Arm | Response | Agent | Source mean | Same-solvent mean |
|---|---|---:|---:|---:|
| all | crystal_yield | 0.101292 | 0.204430 | 0.201849 |
| all | crystal_purity | 0.038535 | 0.005099 | 0.006810 |
| all | crystal_size | 0.076867 | 0.023611 | 0.023732 |
| all | crystal_fines_fraction | 0.319726 | 0.307554 | 0.290161 |
| Opaque | crystal_yield | 0.112728 | 0.201029 | 0.180902 |
| Opaque | crystal_purity | 0.016242 | 0.004742 | 0.006001 |
| Opaque | crystal_size | 0.062510 | 0.019649 | 0.018896 |
| Opaque | crystal_fines_fraction | 0.322664 | 0.306509 | 0.280942 |
| Aligned | crystal_yield | 0.102667 | 0.195220 | 0.201526 |
| Aligned | crystal_purity | 0.051329 | 0.005525 | 0.006997 |
| Aligned | crystal_size | 0.094661 | 0.032278 | 0.031455 |
| Aligned | crystal_fines_fraction | 0.309550 | 0.307566 | 0.301415 |
| MisIndexed | crystal_yield | 0.088987 | 0.219352 | 0.226733 |
| MisIndexed | crystal_purity | 0.052614 | 0.005112 | 0.007631 |
| MisIndexed | crystal_size | 0.073908 | 0.018435 | 0.020434 |
| MisIndexed | crystal_fines_fraction | 0.327772 | 0.309612 | 0.290930 |

Matching uses committed solvent addition/resuspension IDs, not quantities or thermal history.
References assess retention of observed levels, not an optimal learned model.

| Cohort | Goal | Budget | Arm | n | Solvents | Interim measurements | Prep repeats |
|---|---|---:|---|---:|---:|---:|---:|
| corrected_recovery_45 | optimization | 12 | Aligned | 15 | 2.93 | 11.27 | 0.20 |
| corrected_recovery_45 | optimization | 12 | MisIndexed | 15 | 2.40 | 10.40 | 0.27 |
| corrected_recovery_45 | optimization | 12 | Opaque | 15 | 4.00 | 11.33 | 0.07 |
| retained_EC60 | discovery | 12 | Aligned | 5 | 4.00 | 12.00 | 0.00 |
| retained_EC60 | discovery | 12 | MisIndexed | 5 | 3.80 | 12.00 | 0.00 |
| retained_EC60 | discovery | 12 | Opaque | 5 | 4.00 | 12.00 | 0.00 |
| retained_EC60 | discovery | 24 | Aligned | 5 | 4.00 | 24.00 | 0.20 |
| retained_EC60 | discovery | 24 | MisIndexed | 5 | 4.00 | 24.00 | 0.40 |
| retained_EC60 | discovery | 24 | Opaque | 5 | 4.00 | 24.00 | 0.00 |
| retained_EC60 | optimization | 12 | Aligned | 5 | 4.00 | 7.60 | 0.00 |
| retained_EC60 | optimization | 12 | MisIndexed | 5 | 3.20 | 12.00 | 0.00 |
| retained_EC60 | optimization | 12 | Opaque | 5 | 4.00 | 12.00 | 0.00 |
| retained_EC60 | optimization | 24 | Aligned | 5 | 4.00 | 24.00 | 0.00 |
| retained_EC60 | optimization | 24 | MisIndexed | 5 | 4.00 | 24.00 | 0.00 |
| retained_EC60 | optimization | 24 | Opaque | 5 | 4.00 | 24.00 | 0.00 |
| retained_EQ45 | characterization | 12 | Aligned | 15 | 1.00 | 12.00 | 0.93 |
| retained_EQ45 | characterization | 12 | MisIndexed | 15 | 1.00 | 12.00 | 1.13 |
| retained_EQ45 | characterization | 12 | Opaque | 15 | 1.00 | 12.00 | 0.60 |

EC uses historical effective sources; original failures and recoveries retained.
EQ information arms span two periods; corrected C is a separate cohort.
Nominal loading is cumulative added reagent/solvent, not instantaneous concentration.
No causal attribution to notes, goal or information from these path summaries alone.

Session paths, failures, first choices and ranges: research_paths.json.
Query predictions, fitting denominators, fallbacks and errors: source_references.json.
