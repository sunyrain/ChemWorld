# Work II WellAU serialized-MCP qualification

Status: frozen development qualification; not formal/R5/C2 evidence.

## Question and tested units

After declaring the ChemWorld MCP server non-parallel for Codex provider sessions, can WellAU
complete the unchanged A-P terminal D1 lifecycle without one provider response queueing many `step`
calls across a required belief-checkpoint boundary? The fixed block contains both seed-2 A-P tasks
(reaction safety and electrochemical conversion), each with the opaque, aligned-nominal and
misindexed-nominal arms, ten complete experiments per arm, and checkpoints at `0/2/4/7/10`.
The two task triplets may execute concurrently; their three arms execute concurrently. The exact
denominator is 2 tasks, 6 cells, 60 complete experiments, 30 typed checkpoints and 6 initial WellAU
sessions. Every task restarts at its first cell in a fresh output root. All earlier runs remain
immutable historical development evidence.

## Measurements and fixed rules

Record every operation, raw MCP success or failure, failure category, consecutive-failure count,
provider receipt, token/resource ledger, belief snapshot, final recommendation and exact replay.
The provider model, world, arms, checkpoint schedule, ten-experiment horizon, scientific repeat
rules, `3` recovered-agent-invalid limit, `1` consecutive-agent-invalid limit and provider-error
limit remain unchanged. `mcp_servers.chemworld_lab.supports_parallel_tool_calls=false` is the only
execution correction under test. Scientific or agent-invalid failures are retained and never
replaced; only the already typed pre-operation infrastructure-resume rule applies.

## Pass, failure and outputs

The platform qualification passes when all six cells reach retained terminal records, evidence and
resource ledgers reconcile, exact replay is reported for completed cells, and no unclassified
provider/harness event remains. Individual scientific qualification may pass, fail or right-censor.
Any provider, transport, runtime, observation, replay or accounting defect invalidates this fresh
block from its first cell. Expected outputs are two machine-readable task reports with exact
denominators and all failures, their progress streams, and one concise cross-task result summary.
