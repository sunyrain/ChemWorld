# M3 information separation and context portability

Same-world context portability on new candidate plans. None, raw evidence, model law and fitted law are separated in fresh tool-free recipients. Ten reused M1 worlds, not ten additional replication worlds. Quadratic is a representation family, not simulator truth. No mechanism-transfer, equivalence, experimental-savings or internal-mediation claim.

Execution valid: True. Physical: 80/80; exact replay: 80/80; provider: 160/160; conditions: 160/160.

| Prespecified regret contrast | Mean | Interval |
| --- | ---: | --- |
| L_minus_none | -0.137231 | 95% [-0.155845, -0.122566] |
| raw_minus_none | -0.136032 | 99% [-0.166955, -0.106025] |
| F_minus_none | -0.132680 | 99% [-0.164488, -0.099817] |
| L_minus_raw | -0.001199 | 99% [-0.023529, 0.009508] |
| F_minus_raw | 0.003352 | 99% [-0.021421, 0.037629] |
| F_minus_L | 0.004551 | 99% [-0.008013, 0.031772] |

Negative differences favor the first arm. Primary material benefit supported: True.

Ten sampled task-world clusters, five per task. Percentile bootstrap intervals are approximate with this small sample. Models and repeated sessions are nested observations, not additional independent worlds. One primary 95% interval; 5 secondary intervals use 99% marginal coverage (Bonferroni family adjustment). These are the same ten M1 worlds with new candidate plans, not ten additional replication worlds. No equivalence or experimental-savings inference.

| Model | Condition | Completed/scheduled | Mean regret | Near-optimal |
| --- | --- | ---: | ---: | ---: |
| deepseek | none | 20/20 | 0.152699 | 3/20 |
| deepseek | raw | 20/20 | 0.016426 | 17/20 |
| deepseek | L | 20/20 | 0.011575 | 11/20 |
| deepseek | F | 20/20 | 0.023087 | 12/20 |
| gpt | none | 20/20 | 0.141840 | 10/20 |
| gpt | raw | 20/20 | 0.006049 | 13/20 |
| gpt | L | 20/20 | 0.008503 | 12/20 |
| gpt | F | 20/20 | 0.006091 | 12/20 |

| World | Primary L minus none | Completed pairs |
| --- | ---: | ---: |
| electrochemical-conversion--w01 | -0.329678 | 4/4 |
| electrochemical-conversion--w02 | -0.225114 | 4/4 |
| electrochemical-conversion--w03 | -0.237472 | 4/4 |
| electrochemical-conversion--w04 | -0.264495 | 4/4 |
| electrochemical-conversion--w05 | -0.240107 | 4/4 |
| reaction-to-crystallization--w01 | -0.012916 | 4/4 |
| reaction-to-crystallization--w02 | 0.000000 | 4/4 |
| reaction-to-crystallization--w03 | -0.014385 | 4/4 |
| reaction-to-crystallization--w04 | -0.037930 | 4/4 |
| reaction-to-crystallization--w05 | -0.010212 | 4/4 |

| Model | Information | Calls | Wall seconds | Input | Output | Prompt bytes |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| deepseek | none | 20/20 | 479.8 | 160559 | 49828 | 173750 |
| deepseek | raw | 20/20 | 626.4 | 237824 | 96412 | 419450 |
| deepseek | L | 20/20 | 265.7 | 161589 | 43485 | 176073 |
| deepseek | F | 20/20 | 306.2 | 162158 | 49812 | 177554 |
| gpt | none | 20/20 | 187.1 | 229545 | 1513 | 173750 |
| gpt | raw | 20/20 | 302.7 | 303401 | 5823 | 419450 |
| gpt | L | 20/20 | 263.7 | 230512 | 4260 | 175923 |
| gpt | F | 20/20 | 291.2 | 231133 | 4411 | 177554 |

## Descriptive controls and costs

| Selection rule | Units | Mean regret | Near-optimal | Top-1 |
| --- | ---: | ---: | ---: | ---: |
| L-X | 40 | 0.010039 | 23/40 | 20/40 |
| F-X | 40 | 0.006091 | 24/40 | 20/40 |
| nearest | 10 | 0.000000 | 10/10 | 10/10 |
| Uniform random (exact expectation) | 10 worlds | 0.120217 | - | - |

L-X/F-X copies are nested source states; nearest/random count once per world. These are descriptive controls, not additional recipient sessions or independent worlds.

| Model | Artifact | Agent/maximizer agreement |
| --- | --- | ---: |
| deepseek | L | 20/20 |
| deepseek | F | 19/20 |
| gpt | L | 20/20 |
| gpt | F | 20/20 |

| Contrast | Electrochemistry mean | Crystallization mean |
| --- | ---: | ---: |
| L_minus_none | -0.259373 | -0.015089 |
| raw_minus_none | -0.254998 | -0.017066 |
| F_minus_none | -0.248294 | -0.017066 |
| L_minus_raw | -0.004375 | 0.001978 |
| F_minus_raw | 0.006704 | 0.000000 |
| F_minus_L | 0.011079 | -0.001978 |

New physical execution/replay: 724.6 wall seconds; provider: 2722.6 seconds. Usage available for 160/160 attempted calls.

Provider output includes reasoning; cache is a subset of input. Missing usage is unknown. Physical CPU/wall includes replay; recipe resources count primary execution once. Reused M1 public experiments and source generation are historical shared costs, not new execution. The JSON records them separately. No currency estimate.

All failures (empty means none):

```json
[]
```

The JSON includes every slot, all six world contrasts, deterministic controls, agreement denominators, original artifacts, inputs and post-seal candidate scores. Raw provider events, session identities and credentials are excluded.
