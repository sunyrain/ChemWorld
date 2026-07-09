# Baseline 参考

Baseline 的作用不是追求最高分，而是提供可复现的比较下限、诊断环境问题，并帮助
agent 作者确认任务接口、预算语义、仪器观测和 leaderboard 指标是否一致。

当前预发布 benchmark 固定三项核心任务：

- `reaction-to-assay`
- `reaction-to-purification`
- `partition-discovery`

官方 baseline agent 集合：

| Agent | 作用 |
| --- | --- |
| `random` | 合法随机动作下限 |
| `scripted_chemistry` | 规则型化学流程基线 |
| `gp_bo` | 高斯过程 BO 基线 |
| `safe_gp_bo` | safety-aware BO 基线 |
| `tool_using_llm_stub` | 不依赖在线 API 的 tool-using LLM stub |
| `llm_replay` | 固定 reasoning/action trace 的离线 LLM replay |

## 生成官方表格

默认命令会使用预发布三任务、官方 baseline agent 集合和每个任务冻结的 public seeds：

```powershell
chemworld baselines report --output-dir runs/baseline_report
```

输出文件：

| 文件 | 内容 |
| --- | --- |
| `baseline_results.json` | 每个 task / agent / seed 的逐 run 指标 |
| `baseline_summary_table.json` | 按 task 和 agent 聚合的论文表格字段 |
| `baseline_leaderboard.json` | 按 task 分开的 leaderboard 聚合 |
| `baseline_report.json` | 报告总 manifest，含版本、commit、seeds、maturity 和表格 |

`baseline_summary_table.json` 至少包含：

- `task_id`
- `agent_name`
- `runs`
- `seeds`
- `mean_total_score` / `stderr_total_score`
- `mean_final_best_score` / `stderr_final_best_score`
- `mean_auc` / `stderr_auc`
- `mean_invalid_action_rate` / `stderr_invalid_action_rate`
- `mean_final_assay_count` / `stderr_final_assay_count`
- `mean_safety_aware_score`
- `mean_cost_aware_score`

需要快速 smoke 时可以显式缩小任务、agent 和 seed：

```powershell
chemworld baselines report `
  --tasks reaction-to-assay `
  --agents random llm_replay `
  --seeds 0 `
  --output-dir runs/baseline_smoke
```

## 当前预发布 baseline 表

以下表格由 `chemworld baselines report --output-dir runs/baseline_report_official`
生成。它用于校准当前 alpha benchmark 的难度，不代表最终正式榜单。

| Task | Agent | Runs | Mean total | Stderr total | Mean final best | Mean AUC | Invalid rate | Final assays |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `partition-discovery` | `gp_bo` | 3 | 0.006 | 0.001 | 0.008 | 0.005 | 0.333 | 8.00 |
| `partition-discovery` | `llm_replay` | 3 | 0.113 | 0.001 | 0.151 | 0.120 | 0.771 | 1.00 |
| `partition-discovery` | `random` | 3 | 0.000 | 0.000 | 0.001 | 0.000 | 0.625 | 1.00 |
| `partition-discovery` | `safe_gp_bo` | 3 | 0.006 | 0.001 | 0.008 | 0.005 | 0.333 | 8.00 |
| `partition-discovery` | `scripted_chemistry` | 3 | 0.106 | 0.000 | 0.153 | 0.087 | 0.438 | 2.00 |
| `partition-discovery` | `tool_using_llm_stub` | 3 | 0.137 | 0.001 | 0.152 | 0.119 | 0.000 | 4.00 |
| `reaction-to-assay` | `gp_bo` | 1 | 0.124 | 0.000 | 0.163 | 0.027 | 0.000 | 1.00 |
| `reaction-to-assay` | `llm_replay` | 1 | 0.296 | 0.000 | 0.385 | 0.048 | 0.000 | 1.00 |
| `reaction-to-assay` | `random` | 1 | 0.139 | 0.000 | 0.187 | 0.010 | 0.000 | 1.00 |
| `reaction-to-assay` | `safe_gp_bo` | 1 | 0.124 | 0.000 | 0.163 | 0.027 | 0.000 | 1.00 |
| `reaction-to-assay` | `scripted_chemistry` | 1 | 0.252 | 0.000 | 0.332 | 0.030 | 0.000 | 1.00 |
| `reaction-to-assay` | `tool_using_llm_stub` | 1 | 0.306 | 0.000 | 0.395 | 0.056 | 0.000 | 1.00 |
| `reaction-to-purification` | `gp_bo` | 5 | 0.089 | 0.033 | 0.118 | 0.020 | 0.067 | 1.00 |
| `reaction-to-purification` | `llm_replay` | 5 | 0.231 | 0.012 | 0.311 | 0.018 | 0.000 | 1.00 |
| `reaction-to-purification` | `random` | 5 | 0.037 | 0.015 | 0.091 | 0.001 | 0.000 | 1.00 |
| `reaction-to-purification` | `safe_gp_bo` | 5 | 0.089 | 0.033 | 0.118 | 0.020 | 0.067 | 1.00 |
| `reaction-to-purification` | `scripted_chemistry` | 5 | 0.134 | 0.007 | 0.324 | 0.015 | 0.000 | 1.00 |
| `reaction-to-purification` | `tool_using_llm_stub` | 5 | 0.239 | 0.012 | 0.321 | 0.021 | 0.000 | 1.00 |

当前诊断：

- `tool_using_llm_stub` 和 `llm_replay` 在反应与纯化任务上强于随机下限。
- `partition-discovery` 的随机、LLM replay、scripted agent invalid rate 偏高，说明该任务的
  action affordance / planner contract 还需要进入 P1/P2 继续治理。
- `gp_bo` 和 `safe_gp_bo` 在当前 event-sequence 任务上表现接近，BO budget 与 recipe
  acquisition 行为仍应由 `P0-BENCH-04` 单独校准。

## 解读原则

- 如果 `scripted_chemistry` 或 `llm_replay` 无法稳定产生 final assay，优先检查
  action precondition、episode mode、instrument policy 和 termination policy。
- 如果 `random` 经常触发 constitution failure，优先检查 validator、transaction rollback
  和 ledger non-negativity。
- 如果 BO 类方法没有进入 acquisition 阶段，优先检查 task budget、recipe 长度和
  `n_initial` 设置。
- 如果 `mean_auc` 高但 `mean_final_best_score` 低，说明 agent 早期探索有信号但未能
  稳定保留最佳实验。
- 如果 `mean_invalid_action_rate` 高，说明该 agent 不适合作为强基线，或者
  `available_actions()` / validator / task policy 之间还有不一致。

## 发布要求

正式发布前，baseline 表必须和 task card、scenario card、mechanism hash、score contract
以及 replay verifier 同步发布。leaderboard 不应只展示模型排名，还应同时展示上述官方
baseline，作为判断任务难度和环境健康度的参考。
