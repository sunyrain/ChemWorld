# Baseline 参考

Baseline 的作用不是追求最高分，而是给 benchmark 提供可复现的比较下限、环境诊断信号和任务难度校准。

当前预发布 benchmark 固定三项核心任务：

- `reaction-to-assay`
- `reaction-to-purification`
- `partition-discovery`

官方 baseline agent 集合：

| Agent | 作用 |
| --- | --- |
| `random` | 随机动作下限，用于暴露任务是否过窄或奖励是否过宽 |
| `scripted_chemistry` | 规则化化学流程 baseline，用于检查 task contract 和前置条件 |
| `gp_bo` | Gaussian-process Bayesian optimization recipe baseline |
| `safe_gp_bo` | Safety-aware GP-BO baseline |
| `tool_using_llm_stub` | 不依赖在线 API 的 tool-using planner stub |
| `llm_replay` | 固定 reasoning/action trace 的离线 LLM replay |

## 生成报告

默认命令会使用预发布三任务、官方 baseline agent 集合和每个任务冻结的 seeds：

```powershell
chemworld baselines report --output-dir runs/baseline_report
```

快速 smoke 可缩小任务、agent 和 seed：

```powershell
chemworld baselines report `
  --tasks reaction-to-assay `
  --agents random llm_replay `
  --seeds 0 `
  --output-dir runs/baseline_smoke
```

输出文件：

| 文件 | 内容 |
| --- | --- |
| `baseline_results.json` | 每个 task / agent / seed 的逐 run 指标 |
| `baseline_summary_table.json` | 按 task 和 agent 聚合的论文表格字段 |
| `baseline_leaderboard.json` | 按 task 分开的 leaderboard 聚合 |
| `baseline_report.json` | 报告总 manifest，含版本、commit、seeds、maturity 和表格 |

## 汇总字段

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
- `mean_bo_initial_recipe_count`
- `mean_bo_acquisition_recipe_count`
- `mean_bo_entered_acquisition`

后三个 BO 字段用于证明 BO baseline 是否真的进入 acquisition 阶段。对于非 BO agent，这些值应为 0。

## BO 校准要求

ChemWorld 的 campaign task 使用 recipe 作为优化单元：一个 recipe 通常由 6 个 event 组成，并以 `final_assay` 产生一个可用于优化的观测。

当前 BO 默认设置：

| Agent | `n_initial` | 默认候选数 | 校准目标 |
| --- | ---: | ---: | --- |
| `gp_bo` | 4 | 512 | 默认 budget 下至少进入一次 acquisition |
| `safe_gp_bo` | 4 | 768 | 默认 budget 下至少进入一次 safety-aware acquisition |
| `rf_ei` | 4 | 512 | 作为可选 RF surrogate baseline |

`reaction-optimization-standard` 的默认 budget 为 72，对应最多约 12 个完整 recipe，因此 BO 会先运行 4 个随机初始 recipe，再进入 acquisition 阶段。正式报告必须显示：

- `mean_bo_initial_recipe_count >= 4`
- `mean_bo_acquisition_recipe_count >= 1`
- `mean_bo_entered_acquisition == 1.0`
- BO 分数高于 random，但不接近满分，保留研究空间

当前本地校准命令：

```powershell
chemworld baselines report `
  --tasks reaction-optimization-standard reaction-safety-constrained partition-discovery `
  --agents random gp_bo safe_gp_bo `
  --output-dir runs/bo_calibration_current
```

当前校准结果摘要：

| Task | Agent | Mean total | Mean final best | Final assays | Initial recipes | Acquisition recipes | Entered acquisition |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `reaction-optimization-standard` | `random` | 0.004 | 0.010 | 1.00 | 0.00 | 0.00 | 0.00 |
| `reaction-optimization-standard` | `gp_bo` | 0.237 | 0.297 | 12.00 | 4.00 | 8.00 | 1.00 |
| `reaction-optimization-standard` | `safe_gp_bo` | 0.278 | 0.360 | 12.00 | 4.00 | 8.00 | 1.00 |
| `reaction-safety-constrained` | `random` | 0.001 | 0.003 | 1.00 | 0.00 | 0.00 | 0.00 |
| `reaction-safety-constrained` | `gp_bo` | 0.100 | 0.142 | 12.00 | 4.00 | 8.00 | 1.00 |
| `reaction-safety-constrained` | `safe_gp_bo` | 0.094 | 0.134 | 12.00 | 4.00 | 8.00 | 1.00 |
| `partition-discovery` | `random` | 0.000 | 0.001 | 1.00 | 0.00 | 0.00 | 0.00 |
| `partition-discovery` | `gp_bo` | 0.006 | 0.008 | 8.00 | 4.00 | 4.00 | 1.00 |
| `partition-discovery` | `safe_gp_bo` | 0.006 | 0.008 | 8.00 | 4.00 | 4.00 | 1.00 |

解读：BO 在默认 budget 下已经进入 acquisition 阶段，并且在反应优化与安全约束任务上明显强于 random；最高均值仍低于 0.4，没有出现任务被轻易打满的问题。`partition-discovery` 的 BO 分数仍低且 invalid/precondition failure 偏高，这更像是 action affordance 与 planner contract 问题，应进入 P1/P2 治理，而不是继续调高 BO 初始样本。

## 解读原则

- 如果 BO 没有进入 acquisition，优先检查 `budget`、recipe 长度和 `n_initial`。
- 如果 `random` 频繁触发 invalid action，优先检查 action affordance、validator 和 task policy。
- 如果 `scripted_chemistry` 或 `llm_replay` 不能稳定 final assay，优先检查 campaign/single-experiment 语义和 instrument policy。
- 如果 `mean_auc` 高但 `mean_final_best_score` 低，说明 agent 早期探索有信号，但未能稳定保留最佳实验。
- 如果某个 baseline 很快接近满分，说明任务太窄、隐藏机制太容易或评分过宽。

## 发布要求

正式发布前，baseline 表必须和 task cards、scenario cards、mechanism hash、score contract、replay verifier 以及 maturity metadata 同步发布。Leaderboard 不应只展示模型排名，还应展示这些官方 baseline，作为判断任务难度和环境健康度的参照。
