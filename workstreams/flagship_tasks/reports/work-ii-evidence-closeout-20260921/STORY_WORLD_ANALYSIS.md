# Exploratory story analysis: complete world comparisons

Retained development evidence: 240 campaigns in 80 world/condition groups, three arms each. All five worlds, unfavorable outcomes, and source shortfalls are retained. This is descriptive post hoc analysis, not a new experiment or an inferential test. The JSON keeps all response metrics and calibration values; the table shows named readouts, with no pooled cross-system score.

## Goals by world

Each row has six matched goal pairs: two budgets in EC, two prior loci in RX. These are clustered observations, not six independent worlds.

| System | World | Pairs | Better retest | Better prediction | Better retest / worse prediction |
|---|---|---:|---:|---:|---:|
| EC | EC-W01 | 6 | 6 | 3 | 3 |
| EC | EC-W02 | 6 | 6 | 4 | 2 |
| EC | EC-W03 | 6 | 5 | 2 | 3 |
| EC | EC-W04 | 6 | 4 | 3 | 1 |
| EC | EC-W05 | 6 | 5 | 2 | 4 |
| RX | RX-W01 | 6 | 1 | 1 | 1 |
| RX | RX-W02 | 6 | 3 | 1 | 2 |
| RX | RX-W03 | 6 | 3 | 4 | 1 |
| RX | RX-W04 | 6 | 1 | 1 | 1 |
| RX | RX-W05 | 6 | 1 | 1 | 0 |

## EQ/P: question regime

The three most dilute public recipes are Q03, Q08 and Q09. The other nine include boundary questions and must not be called an in-domain set. Mean-source predictions are an additional post hoc diagnostic, not a strong learned mechanism. Coverage uses five reference observations per question; MAE uses their means. Every cell's subgroup means reproduce its original MAE.

| Arm | Question group | Agent MAE | Source-mean MAE | Coverage | Width |
|---|---|---:|---:|---:|---:|
| Opaque | three_most_dilute | 0.01833 | 0.16961 | 93.3% | 0.15676 |
| Opaque | other_nine | 0.01008 | 0.00553 | 90.7% | 0.04706 |
| Aligned | three_most_dilute | 0.15862 | 0.16833 | 2.2% | 0.08084 |
| Aligned | other_nine | 0.00465 | 0.00518 | 91.3% | 0.03340 |
| MisIndexed | three_most_dilute | 0.14397 | 0.16836 | 13.8% | 0.09633 |
| MisIndexed | other_nine | 0.00439 | 0.00494 | 89.6% | 0.02798 |

## C: paired recovery/purity effects

Differences are dossier arm minus Opaque MAE. Negative favors the dossier. Each budget uses five world pairs; arms and responses are correlated.

| Budget | Arm | Recovery improves and purity worsens | Both-conforming pairs |
|---|---|---:|---:|
| 12 | Aligned | 5/5 | 4/4 |
| 12 | MisIndexed | 5/5 | 4/4 |
| 24 | Aligned | 2/5 | 2/5 |
| 24 | MisIndexed | 3/5 | 3/5 |

## P: intervention-specific direction correctness

Uses the original fixed 0.02 resolution. Fifteen campaign answers per factor/metric, nested in five worlds. Small-effect controls do not demonstrate a universal invariance.

| Factor | Metric | Correct | Resolved | Small-effect |
|---|---|---:|---:|---:|
| concentration | purity | 14/15 | 0/0 | 14/15 |
| concentration | recovery | 15/15 | 0/0 | 15/15 |
| extractant | purity | 8/15 | 8/15 | 0/0 |
| extractant | recovery | 3/15 | 3/15 | 0/0 |
| phase_ratio | purity | 3/15 | 3/15 | 0/0 |
| phase_ratio | recovery | 7/15 | 7/15 | 0/0 |
| upstream_time | purity | 9/15 | 9/15 | 0/0 |
| upstream_time | recovery | 9/15 | 9/15 | 0/0 |
| wash_staging | purity | 2/15 | 0/0 | 2/15 |
| wash_staging | recovery | 14/15 | 0/0 | 14/15 |
| washing | purity | 8/15 | 8/15 | 0/0 |
| washing | recovery | 13/15 | 13/15 | 0/0 |

## All 80 world/condition groups

O/A/M = Opaque / Aligned / MisIndexed. An asterisk marks a source shortfall; it is not an imputed result. World identifiers remain scoped to their study block.

### C / E / delivery / 12

| World | Response | Opaque MAE | Aligned MAE | MisIndexed MAE |
|---|---|---:|---:|---:|
| C-W01 | crystal_yield | 0.08489 | 0.04602 | 0.05685 |
| C-W01 | crystal_purity | 0.01355 | 0.09831 | 0.10414 |
| C-W01 | crystal_size | 0.02893 | 0.02935 | 0.02123 |
| C-W01 | crystal_fines_fraction | 0.23468 | 0.26652 | 0.20325 |
| C-W02 | crystal_yield | 0.38131* | 0.04016 | 0.17649 |
| C-W02 | crystal_purity | 0.01432* | 0.03516 | 0.04266 |
| C-W02 | crystal_size | 0.17666* | 0.04166 | 0.09916 |
| C-W02 | crystal_fines_fraction | 0.37834* | 0.25268 | 0.37949 |
| C-W03 | crystal_yield | 0.06160 | 0.04091 | 0.05475 |
| C-W03 | crystal_purity | 0.00591 | 0.03376 | 0.08710 |
| C-W03 | crystal_size | 0.09448 | 0.07402 | 0.02453 |
| C-W03 | crystal_fines_fraction | 0.45718 | 0.22537 | 0.29454 |
| C-W04 | crystal_yield | 0.13965 | 0.06039 | 0.06472 |
| C-W04 | crystal_purity | 0.00730 | 0.07001 | 0.10710 |
| C-W04 | crystal_size | 0.03152 | 0.05252 | 0.02877 |
| C-W04 | crystal_fines_fraction | 0.23379 | 0.30796 | 0.27783 |
| C-W05 | crystal_yield | 0.14864 | 0.11528 | 0.09333 |
| C-W05 | crystal_purity | 0.00651 | 0.01123 | 0.11733 |
| C-W05 | crystal_size | 0.05672 | 0.11429 | 0.18887 |
| C-W05 | crystal_fines_fraction | 0.33554 | 0.49554 | 0.30721 |

### C / E / delivery / 24

| World | Response | Opaque MAE | Aligned MAE | MisIndexed MAE |
|---|---|---:|---:|---:|
| C-W01 | crystal_yield | 0.14364 | 0.05519 | 0.09976 |
| C-W01 | crystal_purity | 0.01773 | 0.01495 | 0.09498 |
| C-W01 | crystal_size | 0.04224 | 0.05558 | 0.16183 |
| C-W01 | crystal_fines_fraction | 0.17761 | 0.27986 | 0.27134 |
| C-W02 | crystal_yield | 0.11634 | 0.05426 | 0.09093 |
| C-W02 | crystal_purity | 0.03016 | 0.03849 | 0.03807 |
| C-W02 | crystal_size | 0.03043 | 0.01631 | 0.13333 |
| C-W02 | crystal_fines_fraction | 0.13532 | 0.26956 | 0.28667 |
| C-W03 | crystal_yield | 0.08714 | 0.11798 | 0.06047 |
| C-W03 | crystal_purity | 0.02888 | 0.06460 | 0.00960 |
| C-W03 | crystal_size | 0.02860 | 0.10615 | 0.06995 |
| C-W03 | crystal_fines_fraction | 0.28577 | 0.28399 | 0.35388 |
| C-W04 | crystal_yield | 0.06986 | 0.05520 | 0.06047 |
| C-W04 | crystal_purity | 0.01094 | 0.01631 | 0.08001 |
| C-W04 | crystal_size | 0.17245 | 0.01467 | 0.10252 |
| C-W04 | crystal_fines_fraction | 0.33197 | 0.23950 | 0.34796 |
| C-W05 | crystal_yield | 0.03839 | 0.05933 | 0.08154 |
| C-W05 | crystal_purity | 0.01104 | 0.06483 | 0.03133 |
| C-W05 | crystal_size | 0.00936 | 0.02714 | 0.04371 |
| C-W05 | crystal_fines_fraction | 0.20971 | 0.31393 | 0.26294 |

### EC / E / discovery / 12

| World | Response | Opaque MAE | Aligned MAE | MisIndexed MAE |
|---|---|---:|---:|---:|
| EC-W01 | score | 0.08839 | 0.26198 | 0.24672 |
| EC-W02 | score | 0.27380 | 0.07176 | 0.12581 |
| EC-W03 | score | 0.06497 | 0.24537 | 0.06011 |
| EC-W04 | score | 0.25955 | 0.26551 | 0.16542 |
| EC-W05 | score | 0.28997 | 0.12505 | 0.06224 |

### EC / E / discovery / 24

| World | Response | Opaque MAE | Aligned MAE | MisIndexed MAE |
|---|---|---:|---:|---:|
| EC-W01 | score | 0.07074 | 0.23245 | 0.03676 |
| EC-W02 | score | 0.13659 | 0.04861 | 0.06307 |
| EC-W03 | score | 0.17245 | 0.07279 | 0.07562 |
| EC-W04 | score | 0.10838 | 0.07765 | 0.06676 |
| EC-W05 | score | 0.11242 | 0.29455 | 0.11444 |

### EC / E / optimization / 12

| World | Response | Opaque MAE | Aligned MAE | MisIndexed MAE |
|---|---|---:|---:|---:|
| EC-W01 | score | 0.22940 | 0.05723 | 0.16618 |
| EC-W02 | score | 0.04784 | 0.07412 | 0.13889 |
| EC-W03 | score | 0.24565 | 0.24599 | 0.12289 |
| EC-W04 | score | 0.15484 | 0.18360 | 0.26232 |
| EC-W05 | score | 0.29595 | 0.21964 | 0.22718 |

### EC / E / optimization / 24

| World | Response | Opaque MAE | Aligned MAE | MisIndexed MAE |
|---|---|---:|---:|---:|
| EC-W01 | score | 0.12331 | 0.17917 | 0.19199 |
| EC-W02 | score | 0.05349 | 0.03751 | 0.05460 |
| EC-W03 | score | 0.08403 | 0.05822 | 0.09233 |
| EC-W04 | score | 0.04319 | 0.12086 | 0.18134 |
| EC-W05 | score | 0.25232 | 0.10230 | 0.04799 |

### EQ / E / characterization / 12

| World | Response | Opaque MAE | Aligned MAE | MisIndexed MAE |
|---|---|---:|---:|---:|
| EQ-E-W01 | macro | 0.01596 | 0.03044 | 0.01716 |
| EQ-E-W02 | macro | 0.01273 | 0.01221 | 0.01264 |
| EQ-E-W03 | macro | 0.01552 | 0.01590 | 0.01327 |
| EQ-E-W04 | macro | 0.01502 | 0.01368 | 0.01380 |
| EQ-E-W05 | macro | 0.01492 | 0.01139 | 0.01614 |

### EQ / P / characterization / 12

| World | Response | Opaque MAE | Aligned MAE | MisIndexed MAE |
|---|---|---:|---:|---:|
| EQ-W01 | macro | 0.01381 | 0.05115 | 0.05158 |
| EQ-W02 | macro | 0.01150 | 0.04962 | 0.05168 |
| EQ-W03 | macro | 0.01042 | 0.04075 | 0.01954 |
| EQ-W04 | macro | 0.01424 | 0.03880 | 0.03857 |
| EQ-W05 | macro | 0.01073 | 0.03539 | 0.03507 |

### EQ / S / characterization / 12

| World | Response | Opaque MAE | Aligned MAE | MisIndexed MAE |
|---|---|---:|---:|---:|
| EQ-S-W01 | macro | 0.00265 | 0.00309 | 0.02244 |
| EQ-S-W02 | macro | 0.00892 | 0.00726 | 0.00819 |
| EQ-S-W03 | macro | 0.05222 | 0.01838 | 0.01344 |
| EQ-S-W04 | macro | 0.00456 | 0.03603 | 0.00594 |
| EQ-S-W05 | macro | 0.00206 | 0.01472 | 0.01724 |

### P / E / delivery / 12

| World | Response | Opaque MAE | Aligned MAE | MisIndexed MAE |
|---|---|---:|---:|---:|
| P-W01 | purity | 0.18955 | 0.19198 | 0.13039 |
| P-W01 | recovery | 0.04491 | 0.04898 | 0.02621 |
| P-W02 | purity | 0.15906 | 0.14496 | 0.26246 |
| P-W02 | recovery | 0.09348 | 0.06481 | 0.12793 |
| P-W03 | purity | 0.14633 | 0.15906 | 0.32767 |
| P-W03 | recovery | 0.05322 | 0.09605 | 0.07809 |
| P-W04 | purity | 0.33580 | 0.25233 | 0.40158 |
| P-W04 | recovery | 0.04346 | 0.04496 | 0.07005 |
| P-W05 | purity | 0.28906* | 0.19316 | 0.13180 |
| P-W05 | recovery | 0.09880* | 0.08847 | 0.06126 |

### PA / E / discovery / 12

| World | Response | Opaque MAE | Aligned MAE | MisIndexed MAE |
|---|---|---:|---:|---:|
| PA-W01 | product_in_organic | 0.04834 | 0.06699 | 0.05243 |
| PA-W02 | product_in_organic | 0.10998 | 0.03332 | 0.13023 |
| PA-W03 | product_in_organic | 0.09832 | 0.01487 | 0.09590 |
| PA-W04 | product_in_organic | 0.20285 | 0.19271 | 0.05089 |
| PA-W05 | product_in_organic | 0.03481 | 0.04829 | 0.06371 |

### PA / E / discovery / 24

| World | Response | Opaque MAE | Aligned MAE | MisIndexed MAE |
|---|---|---:|---:|---:|
| PA-W01 | product_in_organic | 0.01294 | 0.00683 | 0.02168 |
| PA-W02 | product_in_organic | 0.00888 | 0.03491 | 0.01926 |
| PA-W03 | product_in_organic | 0.02668 | 0.01284 | 0.01770 |
| PA-W04 | product_in_organic | 0.02866 | 0.01096 | 0.01970 |
| PA-W05 | product_in_organic | 0.02811 | 0.08256 | 0.02522 |

### RX / P / discovery / 12

| World | Response | Opaque MAE | Aligned MAE | MisIndexed MAE |
|---|---|---:|---:|---:|
| RX-W01 | macro | 0.09362 | 0.03081 | 0.03168 |
| RX-W02 | macro | 0.11733 | 0.02770 | 0.03904 |
| RX-W03 | macro | 0.12606 | 0.13325 | 0.11752 |
| RX-W04 | macro | 0.07325 | 0.04276 | 0.03131 |
| RX-W05 | macro | 0.09905 | 0.05052 | 0.05329 |

### RX / P / optimization / 12

| World | Response | Opaque MAE | Aligned MAE | MisIndexed MAE |
|---|---|---:|---:|---:|
| RX-W01 | macro | 0.19266 | 0.04791 | 0.08934 |
| RX-W02 | macro | 0.10526 | 0.05208 | 0.05560 |
| RX-W03 | macro | 0.12611 | 0.07759 | 0.21875 |
| RX-W04 | macro | 0.09421 | 0.05217 | 0.20889 |
| RX-W05 | macro | 0.17640 | 0.18946 | 0.07576 |

### RX / S / discovery / 12

| World | Response | Opaque MAE | Aligned MAE | MisIndexed MAE |
|---|---|---:|---:|---:|
| RX-W01 | macro | 0.09195 | 0.07004 | 0.09231 |
| RX-W02 | macro | 0.06500 | 0.06573 | 0.07986 |
| RX-W03 | macro | 0.07685 | 0.09806 | 0.11807 |
| RX-W04 | macro | 0.10342 | 0.07154 | 0.07127 |
| RX-W05 | macro | 0.08299 | 0.15505 | 0.14647 |

### RX / S / optimization / 12

| World | Response | Opaque MAE | Aligned MAE | MisIndexed MAE |
|---|---|---:|---:|---:|
| RX-W01 | macro | 0.10517 | 0.07578 | 0.08420 |
| RX-W02 | macro | 0.09395 | 0.08427 | 0.10857 |
| RX-W03 | macro | 0.12390 | 0.09569 | 0.09656 |
| RX-W04 | macro | 0.14072 | 0.11718 | 0.10203 |
| RX-W05 | macro | 0.09763 | 0.22366 | 0.06968 |
