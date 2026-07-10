# 严肃任务设计

严肃任务不是“操作更多”或“模型更复杂”的同义词。它必须提出可证伪的研究问题，使用可执行
指标，在足够的隐藏变化与决策预算下区分 agent，并提供反作弊、基线和失败分析证据。

## 准入标准

ChemWorld 使用 `chemworld-serious-task-design-0.1` readiness contract 检查正式任务：

| 维度 | 最低要求 |
| --- | --- |
| 研究问题 | 明确 agent 要学习或控制什么，结论可以被数据否证。 |
| 世界与 split | 使用当前冻结世界律和可复现的 `public-test`。 |
| 决策深度 | 至少 24 步预算、campaign 学习机会和 5 个冻结 seeds。 |
| 指标 | primary/secondary metrics 必须由 observation 或 evaluator 实际计算。 |
| 观测边界 | 必须有 final assay；中间观测不能泄露 hidden truth。 |
| 物理成熟度 | 整体至少 `lite`，正式 serious 任务不允许 proxy。 |
| 泛化 | 至少声明两个隐藏变化轴。 |
| 基线 | 包含 random、可解释策略和优化基线。 |
| 证据 | 多 seed 置信区间、replay、约束与失败分析。 |
| 反作弊 | 合同 hash/隐藏状态检查与 final-assay 独立评分。 |

机器可读审查：

```bash
chemworld tasks readiness
```

`contract_ready=true` 只表示任务合同可执行；只有完成冻结 baseline、难度校准和失败分析后，
`empirical_status` 才能从 `candidate` 提升到 `validated`，届时 `benchmark_ready` 才为真。

## v1 正式任务

| Task | 核心问题 | Primary metric | 泛化轴 |
| --- | --- | --- | --- |
| `partition-discovery` | 少量相接触能否识别隐藏分配规律？ | `product_in_organic` | 分配系数、相体积比 |
| `reaction-to-crystallization` | 能否同时平衡反应质量、收率、纯度与 CSD？ | `crystal_yield` | 动力学、溶解度/冷却曲线 |
| `reaction-to-distillation` | 能否联合选择反应条件与馏分切割？ | `distillate_purity` | 相对挥发度、反应选择性 |
| `flow-reaction-optimization` | 能否在流动风险下优化转化？ | `flow_conversion` | 动力学、停留时间/热边界 |
| `electrochemical-conversion` | 能否权衡电化学选择性与能效？ | `electrochemical_selectivity` | 氧化还原动力学、传质/电阻 |
| `equilibrium-characterization` | 能否高效表征隐藏水相平衡？ | `equilibrium_confidence` | 酸碱常数、溶度积区间 |

六个任务均已完成五 seed baseline、响应面、策略分离、阈值、主动学习阶段和 replay 机器审查。
当前 task contract hash 与仓库内冻结证据一致时，readiness 返回 `validated`；合同变化会自动将
对应任务退回 `candidate`。

## 暂不准入

- `reaction-to-purification`、`purity-yield-tradeoff` 和 `tool-agent-planning` 含
  dry/concentrate/transfer proxy，继续用于核心回归或探索，不进入 v1 正式套件；
- `reaction-to-assay` 是协议 smoke task，决策深度和 seed 数不足；
- 包含 `mechanism_explanation`、`local_model_quality`、`public_private_gap` 等尚未形成独立
  evaluator 字段的任务，在补齐可执行评分前不得作为主榜任务。

## 冻结证据

v1 已机器验证以下条件：

1. 运行完整 `serious` baseline preset，并报告均值、标准误和置信区间；
2. 检查 random 与 informed baseline 的可分离性，避免地板/天花板效应；
3. 在冻结 seeds 上执行响应面与隐藏场景扰动；公开 OOD 工具可另行报告策略漂移，但 OOD 与
   private eval 都不属于 v1 排名声明；
4. 发布按任务拆分的失败类型、约束违反、仪器使用和成本曲线；
5. 冻结 threshold、task contract、seed suite 与 golden/replay artifact。

重建和检查冻结套件：

```bash
chemworld baselines report --preset serious --output-dir runs/serious_baselines
python scripts/run_serious_task_suite.py --output-dir runs/serious_release
python scripts/check_frozen_benchmark.py
```
