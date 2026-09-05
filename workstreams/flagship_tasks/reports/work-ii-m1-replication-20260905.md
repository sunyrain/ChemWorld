# M1 independent-world replication

Fixed local quadratic response surfaces in two task families. Ten world clusters; repeated models/sessions are nested. Candidate outcomes are single keyed-noise measurements. Fit plus argmax is a classical baseline. No topology-transfer, experimental-savings or internal-mediation claim.

Quadratic describes the permitted representation family on two-dimensional control coordinates. Simulator utilities are not assumed to be exact quadratic functions.

Execution valid: True. Physical: 200/200; exact replay: 200/200; provider: 120/120; conditions: 160/160.

| Prespecified contrast | Mean regret difference | Interval |
| --- | ---: | --- |
| F-X_minus_L-X | -0.005384 | 95% [-0.016303, 0.000614] |
| L-X_minus_L-A | 0.000331 | 98.75% [0.000000, 0.001323] |
| F-A_minus_L-A | -0.005053 | 98.75% [-0.017329, 0.001582] |
| F-X_minus_F-A | 0.000000 | 98.75% [0.000000, 0.000000] |
| interaction | -0.000331 | 98.75% [-0.001323, 0.000000] |

Material primary benefit supported: False.

Ten sampled task-world clusters, five per task. Percentile bootstrap intervals are approximate with this small sample. Models and repeated sessions are nested observations, not additional independent worlds. One primary 95% interval; four secondary intervals use 98.75% marginal coverage (Bonferroni family adjustment).

| Model | Condition | Completed/scheduled | Failure-aware regret | Near-optimal |
| --- | --- | ---: | ---: | ---: |
| deepseek | L-A | 20/20 | 0.014359 | 13/20 |
| deepseek | L-X | 20/20 | 0.015020 | 12/20 |
| deepseek | F-A | 20/20 | 0.004253 | 14/20 |
| deepseek | F-X | 20/20 | 0.004253 | 14/20 |
| gpt | L-A | 20/20 | 0.004253 | 14/20 |
| gpt | L-X | 20/20 | 0.004253 | 14/20 |
| gpt | F-A | 20/20 | 0.004253 | 14/20 |
| gpt | F-X | 20/20 | 0.004253 | 14/20 |

| Model | Stage | Completed/scheduled | Wall seconds | Input | Output |
| --- | --- | ---: | ---: | ---: | ---: |
| deepseek | source | 20/20 | 4174.7 | 253166 | 693668 |
| deepseek | decision | 40/40 | 700.4 | 506259 | 113980 |
| gpt | source | 20/20 | 3229.4 | 255394 | 123231 |
| gpt | decision | 40/40 | 754.9 | 608972 | 11379 |

Output includes reasoning; cached input is a subset. Physics CPU/wall includes exact replay; recipe resources count primary executions once. No currency estimate.

Failures (all levels retained):

```json
[]
```

The JSON companion contains all 160 slots, world contrasts, artifact errors, agreement denominators, baselines and resource totals.

For each simple contrast, negative regret favors the first condition. Interaction is (F-X minus L-X) minus (F-A minus L-A): a negative value means the representation replacement is more favorable under the maximizer than under the fresh agent.

## Per-world paired effects

Each value averages the two models and two repeats within one world. Repeats do not increase the independent-world denominator.

| World | F-X_minus_L-X | L-X_minus_L-A | F-A_minus_L-A | F-X_minus_F-A | interaction |
| --- | ---: | ---: | ---: | ---: | ---: |
| electrochemical-conversion--w01 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| electrochemical-conversion--w02 | -0.054342 | 0.000000 | -0.054342 | 0.000000 | 0.000000 |
| electrochemical-conversion--w03 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| electrochemical-conversion--w04 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| electrochemical-conversion--w05 | 0.000000 | 0.003307 | 0.003307 | 0.000000 | -0.003307 |
| reaction-to-crystallization--w01 | 0.003070 | 0.000000 | 0.003070 | 0.000000 | 0.000000 |
| reaction-to-crystallization--w02 | -0.002565 | 0.000000 | -0.002565 | 0.000000 | 0.000000 |
| reaction-to-crystallization--w03 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| reaction-to-crystallization--w04 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| reaction-to-crystallization--w05 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |

| Task mean (five worlds each) | F-X_minus_L-X | L-X_minus_L-A | F-A_minus_L-A | F-X_minus_F-A | interaction |
| --- | ---: | ---: | ---: | ---: | ---: |
| electrochemical-conversion | -0.010868 | 0.000661 | -0.010207 | 0.000000 | -0.000661 |
| reaction-to-crystallization | 0.000101 | 0.000000 | 0.000101 | 0.000000 | 0.000000 |

## Shared public baselines

| World | Nearest evidence regret | Uniform random expected regret |
| --- | ---: | ---: |
| electrochemical-conversion--w01 | 0.000000 | 0.193562 |
| electrochemical-conversion--w02 | 0.000000 | 0.179243 |
| electrochemical-conversion--w03 | 0.000000 | 0.196878 |
| electrochemical-conversion--w04 | 0.022129 | 0.160390 |
| electrochemical-conversion--w05 | 0.000000 | 0.132677 |
| reaction-to-crystallization--w01 | 0.012278 | 0.048942 |
| reaction-to-crystallization--w02 | 0.000715 | 0.042698 |
| reaction-to-crystallization--w03 | 0.000000 | 0.045030 |
| reaction-to-crystallization--w04 | 0.000000 | 0.073014 |
| reaction-to-crystallization--w05 | 0.000328 | 0.038467 |

## Artifact prediction and decision agreement

Candidate MAE is descriptive, conditional on finite available predictions. Models/repeats remain nested within their shared world; fitted-law copies are not new evidence. Agreement uses pairs with both A and X available.

| Model | Artifact | Finite MAE/scheduled | Mean candidate MAE | A/X agree/eligible |
| --- | --- | ---: | ---: | ---: |
| deepseek | L | 20/20 | 0.050282 | 19/20 |
| deepseek | F | 20/20 | 0.044595 | 20/20 |
| gpt | L | 20/20 | 0.048319 | 20/20 |
| gpt | F | 20/20 | 0.044595 | 20/20 |

## Physical resources by role

| Task | Role | Completed/scheduled | CPU seconds | Wall seconds | Measurement units |
| --- | --- | ---: | ---: | ---: | ---: |
| electrochemical-conversion | public_evidence | 60/60 | 363.8 | 367.0 | 13.68 |
| electrochemical-conversion | hidden_evaluation | 40/40 | 243.2 | 245.2 | 9.12 |
| reaction-to-crystallization | public_evidence | 60/60 | 697.1 | 701.6 | 19.2 |
| reaction-to-crystallization | hidden_evaluation | 40/40 | 464.3 | 467.1 | 12.8 |

Input/output usage is reported for 120/120 attempted calls. Token totals sum reported receipt usage. Missing usage is unknown, not zero billing; no currency or unreported billing overhead is estimated.

Public-test worlds. Candidate scores were hidden throughout participant execution and are released only after choices were sealed. Scientific artifacts and token/timing totals are included; raw provider events, identities and credentials are excluded. This export changes no execution, selection, score or inference.
