# ChemWorld 15 任务设计矩阵 v1

日期：2026-07-29

机器可读权威文件：`workstreams/flagship_tasks/reports/task-design-matrix-v1.json`

## 统一边界

所有任务保留同一个三层语义：

1. 环境原语：一步是一个通过前置条件和守恒校验的操作。
2. 完整实验适配器：优化器或 S0 agent 一次提交一个完整实验配方。
3. 评估：在线 reward 仍是新测量带来的分数增量；正式优化反馈和排行榜终点使用 final assay score。

这消除了“环境操作预算”和“科学实验轮次”混用。S0 的 20 轮是 20 个完整实验，任务注册表中的 budget 仍是原语操作预算。

## 当前状态

- 注册任务：15。
- Confirmatory 任务：`electrochemical-conversion`、`reaction-to-crystallization`。
- 两个 Confirmatory 任务均已完成具名物理控制、10 个独立世界、每世界 20 轮、最终综合、Predictive、盲验证、完整经典基线和精确 replay。
- 其余 13 个任务已完成注册合同、完整实验适配器和指标端点实现；它们具备运行正式比较的设计条件，但尚无正式多世界比较证据。
- 15 个任务共执行 415 个确定性设计案例，覆盖中点、每个坐标的低/高干预和全部离散类别；全部 transaction committed，均包含 final assay 且未超操作预算。
- 62 个声明成功指标已全部绑定到可执行端点，没有再把非观测指标静默忽略。
- 所有任务均为 `proxy_allowed=false`；成熟度声明仍受各自 model card 边界约束。

## 指标端点

指标现在按产生证据的层级显式区分：

- `terminal_observation`：最终已提交 final assay 的直接物理观测。
- `trajectory_aggregate`：样本效率、约束事件、轨迹有效性和 validator 使用率。
- `structured_artifact`：机制解释、失败分析和规划解释，使用透明 rubric 与轨迹 evidence ID。
- `predictive_holdout`：低预算表征的冻结 holdout RMSE 与区间评分。
- `paired_split_campaign`：public/private 均值偏移和按世界 bootstrap 的排序一致性。

缺少 holdout、结构化解释或成对 split 时，评估器返回
`not_evaluated_missing_input`，不会以零分或默认值冒充已测结果。

## 已清理问题

- 删除 `equilibrium-characterization` 中从未进入操作的第 4 个死坐标，配方由 4 维降为 3 维。
- 为 reaction、flow、partition、equilibrium、crystallization、distillation 和 purification 的内部坐标补齐物理名称、范围与单位。
- 两个 Confirmatory 任务不再向模型暴露归一化向量。
- `reaction-to-purification`、`purity-yield-tradeoff` 和 `tool-agent-planning` 不再退化为通用 8 步反应配方；现在使用 16 维反应—纯化设计，编译后执行 22 个操作。
- distillation 的蒸发温度、蒸发时间、蒸馏温度和蒸馏时间已经拆成四个独立控制，配方为 13 维。
- 生成器实际执行每个坐标的低/高干预并枚举全部离散类别；当前 15 个任务死坐标为 0，指标实现 blocker 为 0。
- 原先没有端点的 7 个任务已经补齐：`sample_efficiency`、`constraint_violations`、`final_assay_score`、`trajectory_validity`、`mechanism_explanation`、`failure_analysis`、`validator_use`、`explanation`、`uncertainty`、`local_model_quality`、`public_private_gap` 和 `rank_confidence` 均有明确定义。

## 正式实验边界

当前正式结论只覆盖静态 S0 v1.0：

- 电化学 Codex 盲测均值 0.7150；相对最佳 information-matched 基线的描述性配对差为 +0.0991，但相对最佳 privileged calibration 基线的区间跨 0。
- 结晶 Codex 盲测均值 0.5355；低于 LHS 的 0.5708，当前不能支持“优于经典基线”的论断。
- 所有比较均为描述性结果；没有预注册 superiority 阈值或多重比较方案。

其余 13 个任务的状态是“设计与端点合格、正式比较待执行”，不能因为实现 blocker 为 0 就写成已有经验论证。机制适应 RC28 的 Gate A 是历史环境可辨识性结果；Participant Gates B–E 也不能与本轮固定世界模型能力结果混同。
