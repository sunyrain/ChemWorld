# Experiment 1 executable challenge probe result v1.2

Status: **challenge development attempt 3; not confirmation**

| Block | Plausibility | Non-triviality | Information choice | Budget window | Measured costs | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| EC-E | False | True | False | False | `[None, None, None, None, None]` | challenge-failed |
| EC-P | False | True | False | False | `[None, None, None, None, None]` | challenge-failed |
| EC-S | False | True | False | False | `[None, None, None, None, None]` | challenge-failed |
| RX-P | False | True | False | False | `[None, None, None, None, None]` | challenge-failed |
| RX-S | True | True | False | False | `[None, None, None, None, None]` | challenge-failed |
| PA-E | True | True | True | True | `[2, 2, 2, 2, 2]` | challenge-passed |
| PA-P | True | False | False | False | `[1, 1, 1, 1, 1]` | challenge-failed |
| PA-S | True | True | False | False | `[None, None, None, None, None]` | challenge-failed |
| C-E | True | True | True | True | `[2, 2, 2, 2, 2]` | challenge-passed |
| C-P | True | True | True | True | `[3, 3, 3, 3, 3]` | challenge-passed |

World-probe denominator: `30/50` completed; `35` rows contain a failed probe.

Loci passed: `3/10`; failed: `7/10`.

Every measured cost comes from the frozen per-step trace. A missing stopping time remains a denominator failure. No confirmation secret was generated or consumed.
