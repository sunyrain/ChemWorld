# Baseline 参考

Baseline 用于校准任务难度、检查环境和建立可复现比较下限，不是为了制造单一总榜。

## Core preset

`core` 覆盖 `reaction-to-assay`、`reaction-to-purification` 与 `partition-discovery`，适合快速
回归完整运行/验证/产物链：

```bash
chemworld baselines report --preset core --output-dir runs/core_baselines
```

## Serious preset

`serious` 只包含无 proxy、指标可执行并通过机器合同审查的六个候选任务：

```bash
chemworld baselines report --preset serious --output-dir runs/serious_baselines
python scripts/run_serious_task_suite.py --smoke
```

默认 baseline 包括 `random`、`lhs`、`scripted_chemistry`、`gp_bo`、`safe_gp_bo`、
`tool_using_llm_stub` 和 `codex_subagent_replay`。replay agent 用于可复现 artifact，不应被描述
为在线模型能力。

## 汇总字段

Baseline 表按 `task_id + agent_name` 分组，至少报告：

- runs、seeds、mean/stderr total score；
- final best score、best-valid score 与 AUC；
- invalid-action rate、final-assay count；
- safety-aware 与 cost-aware score；
- BO initial/acquisition counts；
- 当前任务的领域指标，例如 crystallization、flow、electrochemistry 或 equilibrium metrics。

## 难度校准

候选任务提升为 validated 前必须满足：

- random 不接近满分，informed baseline 不长期停在零分；
- 至少一个 informed baseline 显著优于 random；
- baseline 排名在 seeds 上不由单个异常场景决定；
- invalid action 和 safety penalty 不应成为唯一分数差异来源；
- campaign optimizer 必须真正进入 acquisition，而非只执行初始化 recipe。

如果这些条件不满足，应调整任务隐藏变化、预算或评分合同，而不是选择性报告 seeds。
