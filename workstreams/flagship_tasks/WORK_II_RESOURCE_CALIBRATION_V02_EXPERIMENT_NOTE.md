# Work II resource-calibration triplets v0.2 — experiment note

状态：**九任务设计冻结；尚未启动本 v0.2 provider 执行**
适用阶段：W2-26；不进入 A-E public/private scientific denominator。

## Question and coverage

Can every task-specific 8-, 10-, and 12-experiment C2 contract complete in one persistent
Codex + ChemWorld MCP session while preserving closeout reserve, typed checkpoints, exact replay,
and auditable resource accounting? The fixed coverage is nine task triplets: five A-E tasks at 8
experiments, two A-P tasks at 10, and two A-S tasks at 12. Every triplet contains `opaque`,
`aligned_nominal`, and `misindexed_nominal`; no task, arm, seed, round count, checkpoint plan, or
failure rule may change after launch. Exact denominators are 9 triplets, 27 cells, 252 complete
experiments, 135 typed checkpoints, 27 provider sessions, and 27 participant model calls.

## Measurements

For every cell retain complete experiments, unique recipes, exact repeats, attempted and committed
operations, checkpoint validity, final recommendation, lifecycle closeout, exact replay, process
time and closeout reserve, token usage, provider elapsed time and currency, all provider/platform/
physical/resource failures, raw MCP invalid-call counts, and deterministic participant-invalid
recovery-episode totals and maximum consecutive episodes.

## Pass and failure rules

- Every runtime config and authorization binds `agent_invalid_enforcement=measure_only` for W2-26
  only. Participant-invalid calls do not inherit the source config's uncalibrated 3/1 or 0/0 online
  cutoff. Ordinary qualification and formal execution retain their normal hard limits.
- Every runtime config and authorization also binds `provider_error_enforcement=measure_only` for
  W2-26 only. Provider errors remain counted and retained but do not force-kill the live calibration
  session; any nonzero count still invalidates the affected triplet after receipt closure, produces
  no resource card or authorization, and requires a full triplet restart. Ordinary qualification
  and formal execution retain their source-config provider-error hard limits.
- Raw invalid calls and submitted participant payloads remain in the receipt. The host never
  repairs, reorders, or substitutes participant content. A participant that never commits every
  required valid checkpoint or never closes the lifecycle remains a retained method failure.
- Calls emitted before the participant can observe tool feedback form one deterministic recovery
  episode. Raw call maxima are descriptive only. Task-triplet maxima for total and maximum
  consecutive recovery episodes generate the two later hard caps using the prospectively frozen
  rule `max(1, ceil(observed maximum * 1.2))`.
- MCP taxonomy must be complete and `unclassified=0`. Provider, transport, platform, replay, or
  accounting defects remain fail-closed and invalidate the affected triplet. No participant method
  failure is replaced because its resource use is unfavorable.
- A cell passes only if every planned experiment closes, all typed checkpoints and the final
  recommendation are committed, exact replay passes, and all resource ledgers reconcile. A-E/A-P
  keep 15% protected process reserve; A-S keeps 20%. Repeat design stays fixed at 6/8/10 unique
  recipes plus at most two participant-selected exact repeats.

## Expected outputs

1. A machine-readable nine-triplet summary with exact denominators and all failures.
2. Nine task-owned resource cards recording raw invalid-call maxima descriptively and proposing
   process, operation, closeout, token, currency, total recovery-episode, and maximum-consecutive-
   episode caps.
3. A readiness receipt stating whether method qualification may be authorized. No result supports
   H1-H4, law discovery, transfer, scientific endpoint comparison, or model ranking.
