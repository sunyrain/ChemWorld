# Work II WellAU recovery-episode qualification

Status: frozen development qualification; not formal/R5/C2 evidence.

## Question and tested units

After exposing actionable MCP errors and separating raw tool calls from feedback-aware recovery
episodes, can WellAU complete the unchanged A-P terminal D1 lifecycle without being censored by an
already-queued duplicate tool-call burst? The fixed block contains seed 2 for both A-P tasks
(reaction safety and electrochemical conversion), each with opaque, aligned-nominal and
misindexed-nominal arms, ten complete experiments per arm, and belief checkpoints at `0/2/4/7/10`.
The denominator is 2 tasks, 6 cells, 60 complete experiments, 30 typed checkpoints and 6 initial
WellAU sessions. Both task triplets and the three arms within each triplet may execute concurrently.
Every task restarts at its first cell in a fresh output root; earlier runs remain immutable.

## Measurements and fixed rules

Retain every raw MCP call, operation, provider receipt, token/resource entry, belief snapshot, final
recommendation and exact replay. Report raw failures and recovery episodes separately. A recovery
episode is one maximal consecutive burst of an identical failed outcome, with no intervening
successful tool call, whose adjacent calls begin within the frozen 1000 ms duplicate-burst window.
The recovered and consecutive agent-invalid limits remain `3` and `1`, but consume recovery episodes
rather than already-queued raw calls. Provider/network and transport failures remain separately typed;
no action is repaired automatically. The task design, worlds, arms, checkpoint schedule, ten-run
horizon and scientific pass rules are unchanged.

## Pass, failure and outputs

Platform qualification passes when all six cells reach retained terminal records, evidence/resource
ledgers reconcile, exact replay is reported for completed cells, and no unclassified provider or
harness event remains. Individual scientific qualification may pass, fail or right-censor. Any new
provider, transport, runtime, observation, replay or accounting defect invalidates this block from
its first cell. Expected outputs are two machine-readable task reports with exact denominators and all
failures, their progress streams, and one concise cross-task result summary.
