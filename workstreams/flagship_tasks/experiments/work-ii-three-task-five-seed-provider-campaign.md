# Work II three-task, five-seed provider campaign

Date: 2026-08-08. Status: development execution; not formal evidence.

Question: Across electrochemical conversion, reaction-to-crystallization and
reaction-to-distillation, do opaque, aligned-nominal and misindexed-nominal priors produce
reproducible differences in operation-level discovery, belief revision, law summaries and endpoint
outcomes when one persistent Codex session controls four resource-shared experiments?

Coverage: three tasks x three prior arms x world seeds 0--4. The completed electrochemical
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
and exact replay. Crystallization uses a 146,400 s task-specific cap: 115,200 s for four
maximum-duration heat-plus-crystallization pairs, 1,920 s for four committed filters, 28,800 s for
one allowed repeat of each required timed stage and 480 s for at most one quench per experiment.
Distillation uses 202,080 s: 172,800 s for four maximum-duration heat, evaporation and distillation
triples, the same 28,800 s heat/distillation repeat allowance and a 480 s quench allowance.

Pass/failure: a task block passes only if all 15 cells finish four experiments and four checkpoints,
retain exactly one session identity, reconcile the task-pattern resource card, remain within token
and wall-time limits, and pass exact replay. Any failed cell is retained; the current seed triplet
finishes and later seeds stop. A platform repair requires the affected task block to restart from
seed 0 without changing coverage or thresholds.

Expected outputs: ignored per-cell trajectories and summaries under `runs/development/`, one
machine-readable matrix report per task with exact denominators and failures, an external heartbeat
JSONL, and one concise repository report combining all three tasks. Credentials, raw provider
payloads and private reasoning are never retained.

DeepSeek tool-exposure canary (frozen before execution, 2026-08-09): keep the same public seed-0
opaque cell, Responses endpoint, model, prompt, budgets and direct `tool_mode`; change only the model
catalog's `supports_search_tool` value from true to false. The canary establishes direct MCP-tool
exposure if the session calls `material_information` and at least one physical `step`; full four-
experiment completion is reported separately. If no domain tool is exposed, a later diagnostic may
test `code_mode_only`, but it is not part of this canary. The run is provider qualification only and
never enters the 45-cell scientific denominator.

DeepSeek canary result (2026-08-09): direct MCP exposure passed and the same turn completed 4/4
experiment lifecycles, 4/4 checkpoints, 25/25 committed operations and exact replay with zero
provider error or resource rejection. Full cell qualification still failed: cumulative input was
2,490,494 versus the 2,400,000 cap, output was 43,647 versus the 24,000 cap, and the final agent
message did not validate as the required campaign-complete JSON payload. The result isolates tool
visibility from the remaining budget/finalization problems and is not a scientific sample.

DeepSeek qualification-v2 repair freeze (before execution, 2026-08-09): promote
`supports_search_tool=false` to the production DeepSeek catalog; retain the same public seed-0
opaque cell, one model call, one persistent session, high reasoning effort, 28-operation physical
envelope and four checkpoint schedule. Based only on the retained v1 resource overrun, set the
qualification-only limits to 2,750,000 cumulative input tokens, 320,000 uncached input tokens and
50,000 output tokens. MCP 0.5 returns an exact JSON-only response contract at the final checkpoint;
the monitor accepts either exact JSON or a single whole-message JSON fence and records which
encoding was used, but still rejects JSON embedded in prose. Finalization retry limit is zero. The
cell passes only if every existing qualification check passes; any failure is retained without
replacement. This repair block remains provider qualification and does not enter the scientific
denominator.

DeepSeek qualification-v2 result (2026-08-09): the one frozen seed-0 opaque cell passed 4/4
experiments, 4/4 typed checkpoints, all resource/token/session/tool-integrity checks and 26/26-step
exact replay. It recorded 26 operation attempts: 25 committed, one validation failure and zero
resource rejection. The sole session completed with zero provider errors, 2,031,397 input tokens
(1,944,704 cached; 86,693 uncached), 38,993 output tokens and an exact-JSON `campaign_complete`
payload. Wall time was 332.2 s. The run is retained as provider qualification only and does not
enter the scientific denominator.

Platform repair record (2026-08-09): the first crystallization seed-0 triplet exposed that campaign preflight
reserved zero seconds for implicit-duration `filter_crystals` and `quench` operations even though
the runtime advanced the physical clock. The failed triplet is retained outside the scientific
denominator. The resource card now carries explicit per-operation implicit-time reservations; the
crystallization and distillation envelopes were recomputed before restarting the affected block
from seed 0.

Second platform repair record (2026-08-09): the repaired crystallization seed-0 pilot passed 3/3
cells, 12/12 experiments and 132/132 committed operations with zero resource rejection and exact
replay for every cell. The subsequent five-seed block reached 5/15 completed cells and 23/60
complete experiments across six started cells before the seed-1 aligned cell ended after step 39
with a transient Windows `PermissionError` while atomically replacing `active_session.json`.
All 236 recorded steps replay exactly and no resource rejection occurred. Host IPC, the generated
lab tool and the MCP writer now retry atomic replace for at most 40 attempts separated by 25 ms;
exhaustion still raises the original error. The failed block remains excluded and the five-seed
crystallization block restarts from seed 0 without changing scientific coverage or thresholds.

Terminal execution record (2026-08-09): the replacement crystallization block passed 15/15 cells,
60/60 experiments and 15/15 exact replays with 663 recorded attempts, 651 committed operations,
12 validation failures and zero resource rejection. The distillation seed-0 pilot passed 3/3 cells,
12/12 experiments and 3/3 exact replays. Its five-seed block then reached the frozen terminal state
at 14/15 cells, 56/60 experiments, 517 recorded attempts, 506 committed operations, 11 validation
failures, zero resource rejection and 14/15 exact replays. The sole failure, seed-4 aligned nominal,
completed a provider turn but made no MCP call or physical operation. It is retained without rerun.
Across the three tasks the final development denominator is therefore 44/45 cells and 176/180
experiments; the concise combined report is
`workstreams/flagship_tasks/reports/work-ii-three-task-five-seed-campaign.md`.
