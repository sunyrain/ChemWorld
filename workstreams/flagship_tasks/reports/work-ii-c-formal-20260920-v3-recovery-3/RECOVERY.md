# C completion recovery 3

Declared before provider calls in [the governing note](../../WORK_II_C_REFERENCE_V3_NOTE.md#completion-recovery-3-declared-before-new-calls), under the user's instruction to finish C first.

Recovery 2 stopped at 18:44 local time on 2026-09-20 after the W02/24/Opaque provider stream disconnected. Its 18 completed batches and 313 operations are preserved, with exact replay verified and no recommendation or posttest exposure. The controller had exited. The existing local proxy returned HTTP 405 in 0.77 seconds during the connectivity check; this established endpoint reachability, not sustained stream reliability.

Retain eight completed sources, covering all six W01 cells and W02/24/Aligned and MisIndexed, with 156 completed source batches, 24 posttests and eight recommendation retests. All 545 source files were verified byte-identical during recovery validation. The frozen design, release binding and passed five-world qualification are copied without changes. No physical qualification is repeated.

The declared continuation was one fresh full-source attempt of W02/24/Opaque, followed by the 21 never-started cells in frozen order. The runner has no supported restoration of the interrupted model/tool session; its old prefix is not spliced into the new source. Same Sol medium, English prompts, budgets, evaluator and session limits; one executor with a 30-second heartbeat, stopping on any new transport failure. No completed or scientifically unsuccessful chain is rerun.

Launched at 19:07, the retry received model responses and performed seven operations, then disconnected after 75 seconds at 19:08. It completed no new batch or posttest. All seven steps pass exact replay. The controller exited and the queue remains interrupted: 8/30 complete chains and 22 outstanding. No further retry or P model experiment has started. Endpoint reachability was insufficient to ensure reliable model sessions; ETA is suspended.

| Preserved interrupted attempts | Source batches | Operations | Provider sources |
| --- | ---: | ---: | ---: |
| Initial zero-action connection failure | 0 | 0 | 1 |
| Recovery 1: three source disconnections | 8 | 270 | 3 |
| Recovery 2: W02/24/Opaque | 18 | 313 | 1 |
| Recovery 3: W02/24/Opaque | 0 | 7 | 1 |
| Total additional consumption | 26 | 590 | 6 |

The frozen report exporter labels inherited `final_assays` as "reference final assays". Here that means interrupted **source** batch assays, not qualification references. The inherited count is 26/583/5; this root adds 0/7/1. These do not enter the effective 30-source / 540-batch / 90-posttest denominators. All original roots and failure records remain intact. The displayed failure count in the new root does not replace this cross-attempt accounting. Failed-session token snapshots are incomplete and must not be read as zero consumption.

Focused validation passed: correct eight-source selection and byte preservation, inherited 26/583/5 accounting, frozen runtime verification, two negative cases rejecting undeclared coverage, and Ruff. The [generated report](REPORT.md) supplies source-level results.
