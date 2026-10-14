# Research-opportunity comparison

TERMINAL: 30/30 sessions; 29 complete chains; 29 valid forecasts.
Source batches 180/180; sealed stages 117/120.

Lower macro MAE is better. World means have equal weight; repeats are not worlds.

| World | Research Q /3 | NoResearch Q /3 | Research MAE | NoResearch MAE | Difference |
|---|---:|---:|---:|---:|---:|
| W01 | 3 | 3 | 0.057096 | 0.174482 | -0.117386 |
| W02 | 3 | 3 | 0.040502 | 0.101026 | -0.060524 |
| W03 | 2 | 3 | 0.033076 | 0.102890 | -0.069814 |
| W04 | 3 | 3 | 0.028111 | 0.180595 | -0.152485 |
| W05 | 3 | 3 | 0.019374 | 0.101434 | -0.082061 |

| Query group | Research | NoResearch | Paired world difference |
|---|---:|---:|---:|
| all | 0.035632 | 0.132086 | -0.096454 (n=5) |
| dilute | 0.103677 | 0.061467 | 0.042210 (n=5) |
| other | 0.012950 | 0.155625 | -0.142675 (n=5) |

Individual all-query macro MAEs, in repeat order (no query-level pseudoreplication):

| World | Research repeats | NoResearch repeats | Dilute difference | Other difference |
|---|---|---|---:|---:|
| W01 | 0.056735, 0.059241, 0.055311 | 0.097477, 0.104395, 0.321575 | 0.079898 | -0.183148 |
| W02 | 0.062682, 0.011292, 0.047534 | 0.086437, 0.098404, 0.118238 | 0.065500 | -0.102532 |
| W03 | 0.044852, 0.021299, missing | 0.097565, 0.094482, 0.116623 | 0.066388 | -0.115215 |
| W04 | 0.035504, 0.041674, 0.007154 | 0.314567, 0.107223, 0.119995 | -0.016437 | -0.197834 |
| W05 | 0.009812, 0.037601, 0.010708 | 0.110002, 0.104525, 0.089775 | 0.015700 | -0.114647 |

Secondary outcomes, equal-world averages. Coverage is over all five reference
observations per query; intervals are the participant's stated 80% intervals.
Lower interval score is better; coverage alone rewards excessively wide intervals.

| Group | Response | Arm | MAE | Coverage | Width | Interval score |
|---|---|---|---:|---:|---:|---:|
| all | pH_normalized | Research | 0.012591 | 0.918333 | 0.056723 | 0.077467 |
| all | pH_normalized | NoResearch | 0.072952 | 0.983333 | 0.353500 | 0.355774 |
| all | acid_dissociation_fraction | Research | 0.057211 | 0.900556 | 0.172358 | 0.338802 |
| all | acid_dissociation_fraction | NoResearch | 0.099741 | 0.901111 | 0.471515 | 0.500389 |
| all | precipitation_signal | Research | 0.037093 | 0.782778 | 0.095436 | 0.202354 |
| all | precipitation_signal | NoResearch | 0.223563 | 0.915556 | 0.620167 | 0.727575 |
| dilute | pH_normalized | Research | 0.037733 | 0.722222 | 0.128060 | 0.210358 |
| dilute | pH_normalized | NoResearch | 0.029967 | 1.000000 | 0.370889 | 0.370889 |
| dilute | acid_dissociation_fraction | Research | 0.191034 | 0.655556 | 0.440189 | 1.104098 |
| dilute | acid_dissociation_fraction | NoResearch | 0.083088 | 1.000000 | 0.872733 | 0.872733 |
| dilute | precipitation_signal | Research | 0.082265 | 0.524444 | 0.131811 | 0.421346 |
| dilute | precipitation_signal | NoResearch | 0.071347 | 0.933333 | 0.357111 | 0.417828 |
| other | pH_normalized | Research | 0.004210 | 0.983704 | 0.032944 | 0.033170 |
| other | pH_normalized | NoResearch | 0.087281 | 0.977778 | 0.347704 | 0.350736 |
| other | acid_dissociation_fraction | Research | 0.012604 | 0.982222 | 0.083081 | 0.083703 |
| other | acid_dissociation_fraction | NoResearch | 0.105292 | 0.868148 | 0.337775 | 0.376274 |
| other | precipitation_signal | Research | 0.022036 | 0.868889 | 0.083311 | 0.129356 |
| other | precipitation_signal | NoResearch | 0.274302 | 0.909630 | 0.707852 | 0.830824 |

Incomplete terminal chains: 1/30.
Scientific public-input matches: 15/15 available pairs.
Only the random campaign label is excluded from this comparison.
- repeat-03 / EQ-W03-Research: retained_nonconforming; missing Q, K2, EQS; {'Q': 'provider_failure'}

Posthoc conservative [0,1] macro-MAE bounds for missing forecasts; fixed 3 sessions per arm/world, then 5 equal worlds. Not imputation or sampling uncertainty.

| Group | Difference lower bound | Difference upper bound |
|---|---:|---:|
| all | -0.098659 | -0.031992 |
| dilute | 0.036768 | 0.103434 |
| other | -0.143801 | -0.077134 |

The package includes source experiments, observation history and notebook opportunity.
Selection, feedback, notebook effects and internal learning are not isolated.
Missing stages are retained. Model sampling seed is not controlled.
Initial-public-input equality is reported per pair in the JSON; all scientific outputs
and resource counts are exported without provider conversations or credentials.
