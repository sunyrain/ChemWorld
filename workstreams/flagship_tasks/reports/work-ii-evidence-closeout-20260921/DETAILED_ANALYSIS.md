# Completed programme: detailed quantitative analysis

240 sources, 238 source-conforming assessment chains; all 720 posttest stages. Descriptive development evidence. Every prior comparison has five world pairs. Budget comparisons have fifteen pairs nested in five worlds. All response metrics are retained in the companion JSON, including unfavorable comparisons.

## Goals and operating recommendations

| System / prediction endpoint | Pairs | Better retest | Lower prediction MAE | Better retest but worse prediction |
|---|---:|---:|---:|---:|
| EC | 30 | 26 | 14 | 13 |
| RX | 30 | 9 | 8 | 5 |
| RX_macro | 30 | 9 | 6 | 5 |

EC and RX use score MAE; RX_macro additionally retains the original six-metric macro endpoint. These results do not support a universal goal effect.

## Budget: 24 versus 12 batches

Negative differences favor 24 batches. The larger condition has a larger resource envelope, not just more observations. Leave-one-world-out ranges are influence diagnostics, not confidence intervals.

| System / goal | Metric | MAE 12 -> 24 | Improved pairs | Mean difference | Leave-one-world-out range | Conforming paired difference (n) |
|---|---|---:|---:|---:|---:|---:|
| C / delivery | crystal_fines_fraction | 0.30999 -> 0.27000 | 8/15 | -0.03999 | [-0.05831, -0.02068] | -0.02549 (14) |
| C / delivery | crystal_purity | 0.05029 -> 0.03679 | 7/15 | -0.01350 | [-0.01809, -0.00951] | -0.01559 (14) |
| C / delivery | crystal_size | 0.07085 -> 0.06762 | 7/15 | -0.00323 | [-0.01905, 0.01927] | 0.00698 (14) |
| C / delivery | crystal_yield | 0.10433 -> 0.07937 | 8/15 | -0.02496 | [-0.04044, -0.00317] | -0.00782 (14) |
| EC / discovery | electrochemical_selectivity | 0.23314 -> 0.11993 | 11/15 | -0.11321 | [-0.14266, -0.07984] | -0.11321 (15) |
| EC / discovery | energy_efficiency | 0.24251 -> 0.13928 | 11/15 | -0.10323 | [-0.13713, -0.07747] | -0.10323 (15) |
| EC / discovery | faradaic_efficiency | 0.20649 -> 0.12800 | 11/15 | -0.07850 | [-0.10463, -0.05724] | -0.07850 (15) |
| EC / discovery | score | 0.17378 -> 0.11222 | 11/15 | -0.06156 | [-0.08063, -0.04047] | -0.06156 (15) |
| EC / discovery | selective_product_yield | 0.07153 -> 0.05577 | 12/15 | -0.01576 | [-0.02141, -0.01140] | -0.01576 (15) |
| EC / discovery | transport_efficiency | 0.20378 -> 0.12807 | 11/15 | -0.07571 | [-0.10056, -0.05488] | -0.07571 (15) |
| EC / optimization | electrochemical_selectivity | 0.26491 -> 0.11732 | 14/15 | -0.14759 | [-0.17927, -0.11259] | -0.14759 (15) |
| EC / optimization | energy_efficiency | 0.25917 -> 0.16876 | 11/15 | -0.09041 | [-0.11594, -0.06783] | -0.09041 (15) |
| EC / optimization | faradaic_efficiency | 0.24508 -> 0.13716 | 13/15 | -0.10793 | [-0.13466, -0.08032] | -0.10793 (15) |
| EC / optimization | score | 0.17811 -> 0.10818 | 12/15 | -0.06994 | [-0.09089, -0.05576] | -0.06994 (15) |
| EC / optimization | selective_product_yield | 0.07145 -> 0.05332 | 12/15 | -0.01813 | [-0.02485, -0.01498] | -0.01813 (15) |
| EC / optimization | transport_efficiency | 0.22492 -> 0.14160 | 11/15 | -0.08332 | [-0.11417, -0.04799] | -0.08332 (15) |
| PA / discovery | product_in_aqueous | 0.08291 -> 0.02513 | 13/15 | -0.05778 | [-0.07131, -0.03997] | -0.05778 (15) |
| PA / discovery | product_in_organic | 0.08291 -> 0.02379 | 13/15 | -0.05911 | [-0.07298, -0.04163] | -0.05911 (15) |

## C predictions versus repaired public baselines

Both references use the same agent-acquired public observations. Neither is a strong mechanistic learner. The mean baseline can perform well when a response varies little over the query domain. Reference difficulty must be interpreted with target range; a larger MAE does not identify a cognitive cause.

| Budget | Metric | Baseline | Agent MAE | Baseline MAE | Agent wins | Conforming mean difference (n) |
|---|---|---|---:|---:|---:|---:|
| 12 | crystal_yield | public_mean | 0.10433 | 0.19196 | 13/15 | -0.11685 (14) |
| 12 | crystal_yield | public_nearest_neighbor | 0.10433 | 0.19000 | 13/15 | -0.11095 (14) |
| 12 | crystal_purity | public_mean | 0.05029 | 0.00475 | 0/15 | 0.04814 (14) |
| 12 | crystal_purity | public_nearest_neighbor | 0.05029 | 0.00783 | 2/15 | 0.04489 (14) |
| 12 | crystal_size | public_mean | 0.07085 | 0.02114 | 0/15 | 0.04415 (14) |
| 12 | crystal_size | public_nearest_neighbor | 0.07085 | 0.02520 | 2/15 | 0.03769 (14) |
| 12 | crystal_fines_fraction | public_mean | 0.30999 | 0.31946 | 9/15 | -0.01678 (14) |
| 12 | crystal_fines_fraction | public_nearest_neighbor | 0.30999 | 0.31877 | 9/15 | -0.01587 (14) |
| 24 | crystal_yield | public_mean | 0.07937 | 0.15075 | 13/15 | -0.07138 (15) |
| 24 | crystal_yield | public_nearest_neighbor | 0.07937 | 0.15617 | 13/15 | -0.07680 (15) |
| 24 | crystal_purity | public_mean | 0.03679 | 0.00489 | 0/15 | 0.03191 (15) |
| 24 | crystal_purity | public_nearest_neighbor | 0.03679 | 0.01027 | 2/15 | 0.02652 (15) |
| 24 | crystal_size | public_mean | 0.06762 | 0.02577 | 4/15 | 0.04185 (15) |
| 24 | crystal_size | public_nearest_neighbor | 0.06762 | 0.02896 | 5/15 | 0.03866 (15) |
| 24 | crystal_fines_fraction | public_mean | 0.27000 | 0.31357 | 12/15 | -0.04357 (15) |
| 24 | crystal_fines_fraction | public_nearest_neighbor | 0.27000 | 0.32975 | 11/15 | -0.05975 (15) |

## Prior contrasts and uncertainty

The JSON includes every metric-specific A-O, M-O and A-M contrast, paired conforming sensitivity, leave-one-world-out ranges, and mean interval width alongside coverage. A negative error difference is not proof that the prior was understood or correctly revised. World-level trace annotation remains necessary. No tally of metric-level wins is interpreted as independent scientific replications. The selected summary below uses score for EC, organic fraction for PA, within-system macro for RX/EQ, fines/recovery for C and both P metrics.

| System / locus / goal / budget | Metric | MAE O / A / M | A beats O | M beats O | A-O leave-one-world-out range |
|---|---|---:|---:|---:|---:|
| C / E / delivery / 12 | crystal_fines_fraction | 0.32791 / 0.30961 / 0.29246 | 2/5 | 3/5 | [-0.06286, 0.03509] |
| C / E / delivery / 12 | crystal_yield | 0.16322 / 0.06055 / 0.08923 | 5/5 | 5/5 | [-0.12316, -0.04304] |
| C / E / delivery / 24 | crystal_fines_fraction | 0.22808 / 0.27737 / 0.30456 | 2/5 | 0/5 | [0.02805, 0.08473] |
| C / E / delivery / 24 | crystal_yield | 0.09107 / 0.06839 / 0.07863 | 3/5 | 4/5 | [-0.03606, -0.00624] |
| EC / E / discovery / 12 | score | 0.19534 / 0.19393 / 0.13206 | 2/5 | 4/5 | [-0.04685, 0.04876] |
| EC / E / discovery / 24 | score | 0.12011 / 0.14521 / 0.07133 | 3/5 | 4/5 | [-0.01416, 0.05628] |
| EC / E / optimization / 12 | score | 0.19474 / 0.15612 / 0.18349 | 2/5 | 3/5 | [-0.05546, -0.00523] |
| EC / E / optimization / 24 | score | 0.11127 / 0.09961 / 0.11365 | 3/5 | 1/5 | [-0.03399, 0.02293] |
| EQ / E / characterization / 12 | macro | 0.01483 / 0.01672 / 0.01460 | 3/5 | 3/5 | [-0.00126, 0.00325] |
| EQ / P / characterization / 12 | macro | 0.01214 / 0.04314 / 0.03928 | 0/5 | 0/5 | [0.02922, 0.03261] |
| EQ / S / characterization / 12 | macro | 0.01408 / 0.01590 / 0.01345 | 2/5 | 2/5 | [-0.00560, 0.01073] |
| P / E / delivery / 12 | purity | 0.22396 / 0.18830 / 0.25078 | 3/5 | 2/5 | [-0.04776, -0.02060] |
| P / E / delivery / 12 | recovery | 0.06677 / 0.06865 / 0.07271 | 2/5 | 2/5 | [-0.00836, 0.00952] |
| PA / E / discovery / 12 | product_in_organic | 0.09886 / 0.07124 / 0.07863 | 3/5 | 2/5 | [-0.03919, -0.01366] |
| PA / E / discovery / 24 | product_in_organic | 0.02106 / 0.02962 / 0.02071 | 3/5 | 3/5 | [-0.00291, 0.01513] |
| RX / P / discovery / 12 | macro | 0.10186 / 0.05701 / 0.05457 | 4/5 | 5/5 | [-0.05786, -0.03366] |
| RX / P / optimization / 12 | macro | 0.13893 / 0.08384 / 0.12967 | 4/5 | 3/5 | [-0.07212, -0.03267] |
| RX / S / discovery / 12 | macro | 0.08404 / 0.09209 / 0.10159 | 2/5 | 1/5 | [-0.00796, 0.01802] |
| RX / S / optimization / 12 | macro | 0.11227 / 0.11932 / 0.09221 | 4/5 | 4/5 | [-0.02270, 0.01615] |

## C response range and prediction bias

Means weight each campaign equally. Query counts describe predictions, not independent experimental replications. Signed bias is prediction minus target.

| Budget | Metric | Source mean | Query truth mean | Prediction mean | Mean within-world query span | Signed bias | Underestimated queries |
|---|---|---:|---:|---:|---:|---:|---:|
| 12 | crystal_fines_fraction | 0.59912 | 0.67646 | 0.45756 | 0.70558 | -0.21890 | 126/180 |
| 12 | crystal_purity | 0.98549 | 0.98508 | 0.93544 | 0.02442 | -0.04964 | 167/180 |
| 12 | crystal_size | 0.07702 | 0.06739 | 0.13354 | 0.05752 | 0.06615 | 19/180 |
| 12 | crystal_yield | 0.42815 | 0.23832 | 0.31275 | 0.34502 | 0.07443 | 46/180 |
| 24 | crystal_fines_fraction | 0.71584 | 0.67646 | 0.49372 | 0.70558 | -0.18274 | 134/180 |
| 24 | crystal_purity | 0.98519 | 0.98508 | 0.94893 | 0.02442 | -0.03615 | 168/180 |
| 24 | crystal_size | 0.08168 | 0.06739 | 0.13167 | 0.05752 | 0.06428 | 21/180 |
| 24 | crystal_yield | 0.37655 | 0.23832 | 0.28370 | 0.34502 | 0.04538 | 55/180 |

[Author interpretation and next analyses](INTERPRETATION_ZH.md).
