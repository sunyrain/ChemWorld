# Work II DeepSeek recovery-amended development block

Date: 2026-08-10. Status: frozen development experiment; not formal evidence.

Question: after separating participant mistakes from provider/platform failures, can one persistent
DeepSeek `deepseek-v4-flash` Codex session complete operation-level discovery without the previous
one-error gate prematurely censoring otherwise recoverable cells?

Coverage: electrochemical conversion, reaction-to-crystallization and reaction-to-distillation;
opaque, aligned-nominal and misindexed-nominal priors; world seeds 0--4. Each cell remains one
persistent Codex session controlling four resource-shared complete experiments. Each task first
runs only the seed-0 three-arm pilot. A task may expand to seeds 0--4 only when that pilot passes.
The three arms of a seed run concurrently; cells are serial internally.

Frozen recovery boundaries per cell: at most three failed MCP calls in total, at most one failed
MCP call consecutively before a successful call, at most one provider error event, and at most one
resource-rejected operation attempt. A resource rejection is retained as participant behavior and
is never repaired by the host. Cell-local failure is terminal for that cell but does not suppress
later scheduled seeds. Execution stops early only if all three arms of one seed fail before any
committed operation, which is treated as a systemic provider/platform guard.

Unchanged boundaries: physical stock, samples, instruments, cost, risk, operation attempts,
required stages, operation-specific repeat limits, task-pattern process-time cards, explicit
quench/transfer allowance, safety rules, four-experiment denominator and exact replay. The session
wall limit remains 1,800 s. No result is replaced because a later result is more favorable, and all
earlier DeepSeek and WellAU runs remain historical development evidence.

Measurements: terminal and completed cell denominators; complete experiments; attempted and
committed operations; resource rejections; total/current/maximum-consecutive MCP failures with
bounded error code, field path, detail, byte count and hash; provider error events; observed or
explicitly unavailable token usage; session liveness; physical/resource ledgers; belief
checkpoints; final recommendation; and exact replay. Raw tool arguments, provider payloads and
private reasoning are not retained.

Pass/failure: a pilot passes only at 3/3 qualified cells, four experiments and four checkpoints per
cell, usage within the frozen envelope, recovery counts within the limits above, and exact replay.
A five-seed block is complete when all 15 scheduled cells have terminal records; participant
failures remain in the denominator and do not make the runner silently discard later seeds. Any
platform repair after launch requires the affected task block to restart from seed 0 under the same
coverage and pass/failure rules.

Expected outputs: an ignored per-task pilot and five-seed report, per-cell summaries and
trajectories under `runs/development/`, and progress/heartbeat JSONL outside the repository. A
machine-readable combined analysis and concise audit are committed only after the new matrices are
terminal. Credentials and raw provider responses never enter Git.
