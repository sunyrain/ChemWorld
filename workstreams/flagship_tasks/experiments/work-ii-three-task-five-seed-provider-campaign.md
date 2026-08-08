# Work II three-task, five-seed provider campaign

Date: 2026-08-08. Status: development execution; not formal evidence.

Question: Across electrochemical conversion, reaction-to-crystallization and
reaction-to-distillation, do opaque, aligned-nominal and misindexed-nominal priors produce
reproducible differences in operation-level discovery, belief revision, law summaries and endpoint
outcomes when one persistent Codex session controls four resource-shared experiments?

Coverage: three tasks × three prior arms × world seeds 0--4. The completed electrochemical
WellAU block is retained unchanged. New crystallization and distillation blocks each contain 15
cells. Each cell uses one WellAU `gpt-5.6-sol` medium Codex session, four complete experiments and
four typed checkpoints. The three arms of one task/seed run concurrently; seeds and tasks advance
only after the in-flight triplet reaches terminal state. Two preliminary DeepSeek
`deepseek-v4-flash` Codex-session attempts produced no physical operation and are retained as
provider qualification failures, not scientific samples; execution therefore uses the frozen
WellAU fallback.

Measurements: operation attempts and committed operations; lifecycle completion; final metrics;
belief reliability, suspected misindexed fields, held-out predictions and executable law summary;
campaign stock, process-time, sample, cost and risk ledgers; provider usage, MCP receipts, failures
and exact replay. Crystallization and distillation use task-specific process-time caps of 144,000 s:
115,200 s for four maximum-duration required heat-plus-separation pairs and 28,800 s for one
allowed repeat of each required timed stage.

Pass/failure: a task block passes only if all 15 cells finish four experiments and four checkpoints,
retain exactly one session identity, reconcile the task-pattern resource card, remain within token
and wall-time limits, and pass exact replay. Any failed cell is retained; the current seed triplet
finishes and later seeds stop. A platform repair requires the affected task block to restart from
seed 0 without changing coverage or thresholds.

Expected outputs: ignored per-cell trajectories and summaries under `runs/development/`, one
machine-readable matrix report per task with exact denominators and failures, an external heartbeat
JSONL, and one concise repository report combining all three tasks. Credentials, raw provider
payloads and private reasoning are never retained.
