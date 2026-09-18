# Experiment 1 executable challenge probe result v1.2

Status: **challenge development attempt 3; not confirmation**

| Block | Plausibility | Non-triviality | Information choice | Budget window | Measured costs | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| EC-E | True | True | True | True | `[2, 2, 2, 2, 2]` | challenge-passed |
| EC-P | True | True | True | True | `[2, 2, 2, 2, 2]` | challenge-passed |
| EC-S | True | True | True | True | `[2, 2, 2, 2, 2]` | challenge-passed |
| RX-P | True | True | True | True | `[2, 2, 2, 2, 2]` | challenge-passed |
| RX-S | True | True | False | False | `[None, None, None, None, None]` | challenge-failed |
| PA-E | True | True | True | True | `[2, 2, 2, 2, 2]` | challenge-passed |
| PA-P | True | False | False | False | `[1, 1, 1, 1, 1]` | challenge-failed |
| PA-S | True | True | False | False | `[None, None, None, None, None]` | challenge-failed |
| C-E | True | True | True | True | `[2, 2, 2, 2, 2]` | challenge-passed |
| C-P | True | True | True | True | `[3, 3, 3, 3, 3]` | challenge-passed |

World-probe denominator: `50/50` completed; `15` rows contain a failed probe.

Loci passed: `7/10`; failed: `3/10`.

Every measured cost comes from the frozen per-step trace. A missing stopping time remains a denominator failure. No confirmation secret was generated or consumed.
