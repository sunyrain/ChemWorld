# Work II DeepSeek three-task, five-seed campaign

Date: 2026-08-10. Status: development execution; not formal evidence.

Question: Can one persistent DeepSeek `deepseek-v4-flash` Codex session use the host-owned
ChemWorld MCP to perform operation-level discovery under opaque, aligned-nominal and
misindexed-nominal prior conditions across electrochemical conversion, reaction-to-crystallization
and reaction-to-distillation?

Coverage: three tasks x three prior arms x world seeds 0--4. Each cell contains four
resource-shared complete experiments, four typed belief checkpoints, one persistent Codex session,
and exact replay verification. The three arms of one seed run concurrently; a failed cell is
retained and the affected seed triplet is terminal before later seeds advance.

Measurements: operation attempts and committed operations; complete lifecycles; final metrics;
belief snapshots; campaign stock, process-time, instrument, sample, cost and risk ledgers; provider
usage; session/MCP receipts; failures; and exact replay. Task-specific process caps and repeat,
quench and transfer allowances remain those in the source task cards. DeepSeek method envelopes are
frozen before the first task pilot: electrochemical 2.75M cumulative input / 320k uncached / 50k
output tokens, crystallization and distillation 5.5M cumulative input / 800k uncached / 80k output,
with the task-card wall-time caps unchanged.

Pass/failure: a pilot or five-seed block passes only when every scheduled cell completes four
experiments and four checkpoints, retains one campaign session, stays within its task envelope,
has no resource rejection, and passes exact replay. Platform repairs require the affected task
block to restart from seed 0 without changing coverage or thresholds. If DeepSeek repeatedly fails
the frozen provider/session contract after bounded diagnosis, the pre-authorized fallback is the
already qualified WellAU task configuration; no mixed-provider scientific denominator is silently
combined.

Expected outputs: one machine-readable report per task, external heartbeat JSONL, concise combined
summary, and retained per-cell trajectories under `runs/development/`. Credentials, raw provider
payloads and private reasoning are not committed.

Provider qualification basis: the retained DeepSeek qualification-v2 seed-0 opaque
electrochemical cell completed four experiments, four typed checkpoints and exact replay in one
session with zero provider errors. The production catalog must keep `supports_search_tool=false`
so the domain MCP is exposed deterministically.
