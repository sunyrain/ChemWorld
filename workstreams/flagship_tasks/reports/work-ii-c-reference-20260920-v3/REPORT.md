# C reference v3 development acceptance

Previously inspected development worlds; zero provider calls. Fixed recipes; unchanged physical laws, materials and thresholds.

Status: completed; passed: True.

| Seed | Batches | Execution/replay | Quality positive | Negative | Feasible | Resolved |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| 41 | 12/12 | True | 7 | 5 | 7 | 5 |
| 47 | 12/12 | True | 5 | 7 | 5 | 6 |

| Seed | Query | Factor | Recovery | Purity | Size | Fines |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| 41 | Q01 | solvent | 0.253383 | 0.990794 | 0.089221 | 0.155714 |
| 41 | Q02 | solvent | 0.192012 | 0.988806 | 0.082298 | 0.463716 |
| 41 | Q03 | seed | 0.287571 | 0.977991 | 0.085521 | 0.294662 |
| 41 | Q04 | seed | 0.287513 | 0.986158 | 0.085897 | 0.242977 |
| 41 | Q05 | cooling_history | 0.287549 | 0.985551 | 0.086586 | 0.218352 |
| 41 | Q06 | cooling_history | 0.287803 | 0.980873 | 0.044257 | 0.999207 |
| 41 | Q07 | thermal_history | 0.287803 | 0.984884 | 0.087197 | 0.204014 |
| 41 | Q08 | thermal_history | 0.330077 | 0.975605 | 0.053007 | 1.000000 |
| 41 | Q09 | continue_growth | 0.002910 | 0.999274 | 0.032372 | 0.976836 |
| 41 | Q10 | continue_growth | 0.148385 | 0.985416 | 0.047210 | 0.998790 |
| 41 | Q11 | upstream_loading | 0.287556 | 0.986161 | 0.086892 | 0.210843 |
| 41 | Q12 | upstream_loading | 0.321959 | 0.980151 | 0.055778 | 0.999118 |
| 47 | Q01 | solvent | 0.286160 | 0.990959 | 0.079673 | 0.571716 |
| 47 | Q02 | solvent | 0.094171 | 0.993309 | 0.060868 | 0.966000 |
| 47 | Q03 | seed | 0.206386 | 0.980086 | 0.089300 | 0.299669 |
| 47 | Q04 | seed | 0.206165 | 0.989063 | 0.081397 | 0.476496 |
| 47 | Q05 | cooling_history | 0.206244 | 0.988473 | 0.084144 | 0.433095 |
| 47 | Q06 | cooling_history | 0.206889 | 0.986298 | 0.047351 | 0.998776 |
| 47 | Q07 | thermal_history | 0.206889 | 0.987803 | 0.087067 | 0.391751 |
| 47 | Q08 | thermal_history | 0.250043 | 0.977511 | 0.050099 | 1.000000 |
| 47 | Q09 | continue_growth | 0.000170 | 0.999964 | 0.032077 | 0.621782 |
| 47 | Q10 | continue_growth | 0.048592 | 0.993096 | 0.045332 | 0.995726 |
| 47 | Q11 | upstream_loading | 0.206250 | 0.989065 | 0.083052 | 0.451947 |
| 47 | Q12 | upstream_loading | 0.248397 | 0.984351 | 0.064683 | 0.998313 |

Formal sources require a separately committed/frozen execution surface and a full five-world qualification. No model source is started by this script.
