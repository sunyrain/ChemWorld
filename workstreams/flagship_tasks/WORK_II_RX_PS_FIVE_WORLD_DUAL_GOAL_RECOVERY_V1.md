# Work II RX-P/S five-world dual-goal recovery v1

Status: authorized recovery, 2026-09-19.

## Trigger and retained state

The frozen v1.0.1 run stopped at 2026-09-19 05:47 +08:00 after a shared pre-action
provider connection failure. The retained run root is:

`runs/development/work-ii-rx-ps-five-world-dual-goal-20260919-v2`

At the stop boundary, 16 of 60 source cells had been attempted. Fifteen cells had
completed all 12 physical batches (180 retained batches); 12 had sealed K1/Q/K2 chains.
Reference truth, prediction evaluation, and recommendation retests had not started.

The original source folders, posttest receipts, result files, startup failures, and summary
are immutable evidence. Recovery artifacts must be written under explicit repair directories
and must not replace an original failed or nonconforming artifact.

## Authorized repair set

The following posttest-only repairs reuse the original source trajectory and the same archived
Codex thread. They cannot call the laboratory, add experiments, change a frozen question, or
receive truth feedback.

| Cell | Retained valid outputs | Repair turns |
| --- | --- | --- |
| `RX-W01--S--mechanism_discovery--Opaque` | source, K1, K2 | Q, then K2 again so the final retrospective follows the repaired Q |
| `RX-W01--S--safety_constrained_optimization--MisIndexed` | source, K1, K2 | Q, then K2 again so the final retrospective follows the repaired Q |
| `RX-W02--P--mechanism_discovery--MisIndexed` | source | K1, Q, K2 |

The first two original Q turns stopped at the operational calculator budget. The third cell's
posttests were affected by provider connectivity. The public-numerics call ceiling is raised
from 128 to 512 for repaired and subsequent posttest turns. This is an operational allowance,
not a scientific intervention: prompts, schemas, query rows, model, reasoning effort, source
observations, and information boundaries remain frozen.

## Source continuation

`RX-W02--P--safety_constrained_optimization--Opaque` failed before its first executable
laboratory action (0 operations, 0 batches). It is rerun once in a separate write-once source
repair directory with the same frozen cell definition and deterministic seeds. The original
zero-action failure remains intact.

After that cell seals successfully, the 44 never-started cells continue in the original frozen
schedule. Existing completed cells are read, not rerun. Any new zero-action shared provider
failure stops the block again rather than emitting a fallback action.

## Truth embargo and completion rule

Reference truth remains forbidden until all 60 effective cells have:

1. a completed 12-batch source trajectory with exact replay;
2. valid English K1, Q, and K2 payloads;
3. a sealed posttest chain; and
4. no unresolved cell failure.

Only then may the runner generate the frozen 600 provider-free reference executions, evaluate
blind predictions, and run recommendation retests. Recovery summaries live under
`recovery-v1/`; original run summaries are not overwritten.
