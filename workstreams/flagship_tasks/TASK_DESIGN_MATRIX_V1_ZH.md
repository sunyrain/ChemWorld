# ChemWorld 15 任务设计矩阵 v1

日期：2026-07-27

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
- 两个 Confirmatory 任务均已完成具名物理控制、20 轮、五静态世界、最终综合、Predictive、盲验证和 replay。
- 其余 13 个任务完成注册合同与完整实验适配器设计；当前发布不要求昂贵正式模型实验。
- 15 个任务的确定性中点配方均已端到端执行；全部 transaction committed，均包含 final assay 且未超操作预算。
- 所有任务均为 `proxy_allowed=false`；成熟度声明仍受各自 model card 边界约束。

## 已清理问题

- 删除 `equilibrium-characterization` 中从未进入操作的第 4 个死坐标，配方由 4 维降为 3 维。
- 为 reaction、flow、partition、equilibrium、crystallization、distillation 和 purification 的内部坐标补齐物理名称、范围与单位。
- 两个 Confirmatory 任务不再向模型暴露归一化向量。
- `reaction-to-purification`、`purity-yield-tradeoff` 和 `tool-agent-planning` 不再退化为通用 8 步反应配方；现在使用 16 维反应—纯化设计，编译后执行 22 个操作。
- distillation 的蒸发温度、蒸发时间、蒸馏温度和蒸馏时间已经拆成四个独立控制，配方为 13 维。
- 生成器实际比较每个坐标的低/高干预并执行中点配方；当前 15 个任务死坐标为 0，未解决正式化 blocker 为 0。

## 正式实验边界

当前正式结论只覆盖静态 S0。机制适应 RC28 的 Gate A 是环境可辨识性结果；Participant Gates B–E 仍未启动，不能与本轮固定世界模型能力结果混同。
