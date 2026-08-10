# Work II DeepSeek five-task development completion

Date: 2026-08-10. Status: complete development evidence; not formal or held-out evidence.

Machine analysis:
`workstreams/flagship_tasks/reports/work-ii-deepseek-five-task-development-complete-20260810.json`.
Source manifest:
`configs/benchmark/work_ii_deepseek_five_task_development_complete_analysis_sources_20260810.json`.

## Scope and execution

The completed development matrix contains five prior-identifiable tasks, three prior arms
(`opaque`, `aligned_nominal`, `misindexed_nominal`) and five world seeds per task. The first three
tasks use the retained recovery-amended five-seed matrices. Partition discovery and safety-
constrained reaction combine their immutable seed-0 gate triplets with a new terminal-preserving
continuation for seeds 1--4. The continuation never reran or replaced seed-0 outcomes.

Every scheduled cell reached a terminal record: **75/75**. The retained trajectories, including
failed prefixes, all passed physical exact replay: **75/75**. The combined source records contain
**69/75 completed and qualified cells**, **290/300 complete experiments**, **2,663 operation
attempts**, **2,587 committed operations**, **73 validation failures**, **3 resource rejections**,
**69 recovered MCP tool failures** and **0 provider-error events**. Provider usage accounting is
complete for 72/75 cells; the three cells stopped before a provider terminal event retain usage as
unavailable rather than zero.

| Task | Terminal | Completed/qualified | Complete experiments | Attempts / committed | Resource rejects | MCP failures | Provider errors | Exact replay |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Electrochemical conversion | 15/15 | 15/15 | 60/60 | 373 / 372 | 0 | 13 | 0 | 15/15 |
| Reaction to crystallization | 15/15 | 13/15 | 54/60 | 606 / 605 | 0 | 18 | 0 | 15/15 |
| Reaction to distillation | 15/15 | 15/15 | 60/60 | 637 / 637 | 0 | 7 | 0 | 15/15 |
| Partition discovery | 15/15 | 12/15 | 58/60 | 553 / 501 | 3 | 14 | 0 | 15/15 |
| Safety-constrained reaction | 15/15 | 14/15 | 58/60 | 494 / 472 | 0 | 17 | 0 | 15/15 |
| **Total** | **75/75** | **69/75** | **290/300** | **2,663 / 2,587** | **3** | **69** | **0** | **75/75** |

Provider accounting totals are **267,929,149 input tokens**, of which **260,033,536 were cached**
(97.05% cache-hit fraction), **7,895,613 uncached input tokens**, and **2,932,468 output
tokens**. The cache fraction is repeated shared context accounting; it is not repeated model output.

## Retained failures

- Crystallization retains the earlier seed-3 misindexed and seed-4 opaque MCP-recovery failures.
- Partition retains the earlier seed-0 misindexed output-cap failure, plus continuation seed-3 aligned
  with one participant resource rejection and continuation seed-4 opaque terminated at two
  experiments after the frozen MCP-recovery limit.
- Safety retains the earlier seed-0 aligned token/operation-budget failure. All 12 continuation cells
  (seeds 1--4) completed and passed.

No failed cell was replaced by a favorable rerun. The two continuation task-specific token-tail
ceilings were frozen before execution; physical process-time formulas, operation/repeat budgets,
resource rejection policy, recovery limits, one-session semantics and exact replay were unchanged.

## Interpretation boundary

This is a provider-separated development completion, not the public formal matrix. It supports an
audited description of how the frozen DeepSeek Codex/MCP harness behaved across the five-task prior
conditions, including successful trajectories, resource allocation failures and tool-recovery
tails. It does not provide evaluator-truth prediction-error scoring, blind recommendation replay,
private transfer confirmation, formal hypothesis tests or a DeepSeek-versus-WellAU capability
ranking. Endpoint contrasts remain descriptive and task-specific; they are not collapsed into a
single leaderboard score.
