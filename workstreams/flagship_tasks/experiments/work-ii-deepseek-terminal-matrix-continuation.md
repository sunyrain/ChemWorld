# Work II DeepSeek terminal matrix continuation

Date: 2026-08-10. Status: development execution; not formal evidence.

Question: What complete five-seed development trajectories are produced on partition discovery and
safety-constrained reaction when the already retained seed-0 terminal failures are preserved and the
previously unstarted seeds 1--4 are executed without outcome-dependent replacement?

Coverage: execute exactly world seeds 1--4 for `partition-discovery` and
`reaction-safety-constrained`, three prior arms per seed and one persistent DeepSeek
`deepseek-v4-flash` Codex/MCP session per cell. The existing seed-0 triplets remain immutable and
are hash-bound into readiness and final analysis. They are not rerun or requalified. Each new cell
targets four resource-shared experiments, four typed checkpoints and exact physical/resource replay;
the three arms of one seed run concurrently and seeds remain serial.

Frozen task envelopes:

- Partition: process time is 9,000 s = four required `(mix 600 s + settle 1,200 s)` stages plus one
  extra mix and settle; repeats are `mix <= 5`, `settle <= 5`, `separate_phase <= 4`; 48 operation
  attempts; provider caps are 4.8M input, 640k uncached input and 66k output tokens.
- Safety: process time is 36,480 s = four required `(heat 7,200 s + quench 120 s)` stages plus one
  extra heat, including 480 s total quench reserve; repeats are `heat <= 5`, `quench <= 4`; 40
  operation attempts; provider caps are 6.4M input, 640k uncached input and 80k output tokens.
- Both: one provider turn/session, 1,800 s session wall, at most three recovered MCP failures in
  total, at most one consecutively, at most one provider-error event, zero resource rejections and
  no hidden action repair. Physical stocks, closeout reserves and exact replay rules are unchanged.

Measurements: terminal/completed/qualified cells; experiments; attempts and commits; token/cache
usage; wall and simulated process time; MCP/provider failures; resource rejections; belief snapshots;
final recommendations; exact replay; and paired prior-arm endpoint descriptions by task and seed.

Pass/failure: every scheduled seed 1--4 cell remains in the denominator. A cell passes only if all
existing qualification checks and the frozen task envelope pass. Participant, resource or tool
failures are retained and never replaced. A whole task may stop early only if all three arms of a
seed fail before the first committed scientific operation. The historical seed-0 outcomes retain
their original failure labels even where the continuation uses a larger task-specific token tail.

Expected outputs: ignored run roots under `runs/development/`, external progress JSONL at least once
per minute, zero-provider readiness receipts, two immutable task matrix reports, and one combined
five-task development analysis with exact denominators and every failure. No formal, transfer or
cross-provider ranking claim is authorized.
