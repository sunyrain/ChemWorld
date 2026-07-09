# Baseline 参考

Baseline 的作用不是追求最高分，而是给 benchmark 提供可复现的比较下限、环境诊断信号和任务难度校准。

## AAAI Baseline Preset

AAAI preset 冻结 6 个任务：

- `reaction-optimization-standard`
- `reaction-to-purification`
- `partition-discovery`
- `reaction-to-distillation`
- `electrochemical-conversion`
- `equilibrium-characterization`

默认 baseline agent：

- `random`
- `lhs`
- `scripted_chemistry`
- `gp_bo`
- `safe_gp_bo`
- `tool_using_llm_stub`
- `codex_subagent_replay`

生成命令：

```powershell
chemworld baselines report --preset aaai --output-dir runs/aaai_2027/baseline_report
```

快速 smoke：

```powershell
python scripts/run_aaai_experiments.py --smoke
```

`codex_subagent_online` 是人工触发的在线 LLM 基线；默认 baseline report 使用 `codex_subagent_replay` 保证 artifact 可复现。

## 预发布 Baseline

公开预发布 benchmark 的核心任务仍可单独运行：

- `reaction-to-assay`
- `reaction-to-purification`
- `partition-discovery`

```powershell
chemworld baselines report --output-dir runs/baseline_report
```

smoke 运行：

```powershell
chemworld baselines report `
  --tasks reaction-to-assay `
  --agents random llm_replay `
  --seeds 0 `
  --output-dir runs/baseline_smoke
```

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

AAAI equilibrium 任务还应报告：

- `mean_pH_normalized`
- `mean_acid_dissociation_fraction`
- `mean_precipitation_signal`
- `mean_equilibrium_residual`
- `mean_equilibrium_confidence`

## BO 校准要求

ChemWorld 的 campaign task 使用 recipe 作为优化单元。当前 BO 默认 `n_initial=4`，在 `reaction-optimization-standard` 的默认 budget 下应至少进入一次 acquisition 阶段。

正式报告应显示：

- `mean_bo_initial_recipe_count >= 4`
- `mean_bo_acquisition_recipe_count >= 1`
- `mean_bo_entered_acquisition == 1.0`

如果 BO 没有进入 acquisition，应优先检查 `budget`、recipe 长度和 `n_initial`，而不是直接解释为 BO 性能差。

## 解释原则

- 如果 random 很快接近满分，说明任务过窄或评分过宽；
- 如果 scripted baseline 无法稳定 final assay，优先检查 task policy 和 precondition；
- 如果 invalid action rate 高，优先检查 affordance、validator 和 action schema；
- 如果 public-test 和 private-eval 差距过大，需要报告 generalization gap，而不是只报 public score。
