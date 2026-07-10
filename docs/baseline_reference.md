# Baseline 参考

Baseline 用于校准任务难度、检查环境和建立可复现比较下限，不是为了制造单一总榜。

## Core preset

`core` 覆盖 `reaction-to-assay`、`reaction-to-purification` 与 `partition-discovery`，适合快速
回归完整运行/验证/产物链：

```bash
chemworld baselines report --preset core --output-dir runs/core_baselines
```

## Serious preset

`serious` 只包含无 proxy、指标可执行并通过机器合同和经验有效性审查的六个正式任务：

```bash
chemworld baselines report --preset serious --output-dir runs/serious_baselines
python scripts/run_serious_task_suite.py --output-dir runs/serious_release
```

默认 baseline 包括 `random`、`lhs`、`scripted_chemistry`、`gp_bo`、`safe_gp_bo` 和
`tool_using_llm_stub`。它们使用按任务定义的搜索空间，不会把通用反应 recipe 错用于分配、
连续流、电化学或平衡任务。固定 replay trace 仍可用于诊断，但不作为跨任务官方 baseline。

## 汇总字段

Baseline 表按 `task_id + agent_name` 分组，至少报告：

- runs、seeds、mean/stderr 与 bootstrap 95% CI total score；
- final best score、best-valid score 与 AUC；
- invalid-action rate、final-assay count；
- safety-aware 与 cost-aware score；
- BO initial/acquisition counts；
- 当前任务的领域指标，例如 crystallization、flow、electrochemistry 或 equilibrium metrics。

## 难度校准

任务进入正式套件前必须满足：

- random 不接近满分，informed baseline 不长期停在零分；
- 至少三个策略产生可区分结果，primary metric 对策略变化有响应；
- baseline 排名在 seeds 上不由单个异常场景决定；
- invalid action 和 safety penalty 不应成为唯一分数差异来源；
- campaign optimizer 必须真正进入 acquisition，而非只执行初始化 recipe。

这些条件由 `scripts/validate_serious_benchmark.py` 自动检查，而不是靠文档声明。

如果这些条件不满足，应调整任务隐藏变化、预算或评分合同，而不是选择性报告 seeds。
