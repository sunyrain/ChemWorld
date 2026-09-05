# M0/M1 development summary

Two development worlds; no confidence interval, significance test, formal qualification, or generalization claim. Costs are simulator units and provider tokens/wall time; currency and billing overhead are not estimated.

L = model-generated quadratic; F = public-only ridge fit; A = fresh model decision; X = shared deterministic maximizer.

| Task | Model | L-A | L-X | F-A | F-X |
| --- | --- | ---: | ---: | ---: | ---: |
| electrochemical-conversion | deepseek | 0.024212 | 0.007440 | 0.007440 | 0.007440 |
| electrochemical-conversion | gpt | 0.007440 | 0.007440 | 0.007440 | 0.007440 |
| reaction-to-crystallization | deepseek | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| reaction-to-crystallization | gpt | 0.134529 | 0.134529 | 0.000000 | 0.000000 |

Regret uses fixed utility scale 1; near-optimality threshold 0.01.

| Task | Nearest public evidence | Uniform random (exact expectation) |
| --- | ---: | ---: |
| electrochemical-conversion | 0.024212 | 0.169826 |
| reaction-to-crystallization | 0.134529 | 0.189361 |

Physical execution and exact replay: 42/42 each. Provider completion: 12/12. Condition availability: 16/16.

| Model | Stage | Complete/scheduled | Wall seconds | Input | Output |
| --- | --- | ---: | ---: | ---: | ---: |
| deepseek | source | 2/2 | 328.2 | 18763 | 61596 |
| deepseek | decision | 4/4 | 120.1 | 47831 | 20103 |
| gpt | source | 2/2 | 327.2 | 25541 | 12475 |
| gpt | decision | 4/4 | 57.0 | 60881 | 1237 |

Output usage includes reasoning tokens; cached input is a subset of input. Recipe duration and measurement costs are simulator units. Physical CPU/wall includes replay; recipe resource sums count main executions once.

Failures: []

See the JSON companion for all slots, artifact errors, paired contrasts and costs.
