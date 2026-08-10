# Work II DeepSeek five-task development completion block

Date: 2026-08-10. Status: development execution; not formal evidence.

Question: Does the current operation-level DeepSeek Codex/MCP harness complete the two remaining
prior-identifiable tasks in the frozen five-task development scope, after the electrochemical,
crystallization and distillation recovery-amended blocks were closed?

Coverage: `partition-discovery` and `reaction-safety-constrained`; each task uses opaque,
aligned-nominal and misindexed-nominal prior arms, world seeds 0--4, one persistent DeepSeek
`deepseek-v4-flash` Codex session per task × arm × seed cell, four resource-shared complete
experiments, four typed checkpoints and exact physical/resource replay. Each seed triplet runs the
three arms concurrently; cells remain serial internally. The prior dossier is nominal and
incomplete; public outcomes remain authoritative.

Measurements: terminal and completed cell counts; complete experiments; operation attempts and
committed operations; provider usage and wall time; MCP validation/recovery and provider errors;
resource rejections; safety/risk ledgers; belief checkpoints; final recommendation; and exact
replay. Raw provider payloads, credentials and private reasoning are excluded from Git.

Pass/failure: seed-0 pilot passes only when all three cells complete four experiments and four
checkpoints, stay within the task-specific DeepSeek envelope, retain one session, have zero provider
errors and no resource rejection, and pass exact replay. A passing pilot permits the unchanged
five-seed schedule. Any platform repair requires restarting the affected task from seed 0 under the
same coverage and gates. Participant failures are retained in the denominator and are never
replaced by a favorable rerun; a failed task falls back to its retained WellAU development matrix
for coverage accounting, while the DeepSeek attempt remains separately reported.

Expected outputs: ignored run roots under `runs/development/`, external heartbeat JSONL with at least
30-second liveness, one machine-readable per-task report, a combined provider-separated analysis,
and concise audit prose. No formal claim, cross-provider ranking or held-out transfer claim is
authorized from this block.
