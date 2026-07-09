# 任务卡

任务卡是 ChemWorld benchmark 的发布合同。它把 registry 中的任务信息压缩成人类和
agent 作者都能理解的矩阵。

## 当前 Registry 矩阵

| 任务族 | 主要能力 | 典型指标 | 成熟度 |
| --- | --- | --- | --- |
| reaction-optimization | 反应条件优化 | yield、selectivity、cost | lite |
| reaction-to-purification | 反应到纯化闭环 | purity、yield、cost、safety | lite |
| safety-constrained-control | 安全约束控制 | objective、safety penalty | proxy/lite |
| mechanism-explanation | 机理解释 | explanation accuracy | proxy |
| characterization-planning | 表征规划 | information gain、cost | proxy/lite |
| partition-discovery | 分配规律发现 | prediction error、sample efficiency | lite |
| purity-yield-tradeoff | 纯度-产率权衡 | purity、recovery | lite |
| crystallization-control | 结晶控制 | purity、crystal quality | proxy/lite |
| distillation-cut-selection | 蒸馏切割选择 | purity、recovery、energy | proxy/lite |
| continuous-flow-optimization | 连续流优化 | yield、throughput、safety | proxy/lite |
| electrochemical-screening | 电化学筛选 | conversion、selectivity、risk | proxy/lite |
| tool-agent-planning | 工具型 agent 规划 | task score、invalid actions | proxy/lite |

## Baseline 行

每张任务卡应至少记录：

- random baseline；
- legal-random baseline；
- fixed recipe baseline；
- simple optimizer baseline；
- 可选 tool-agent baseline。

## 发布规则

任务卡必须与 registry 保持一致。若任务的 action space、metrics、maturity 或 hidden
scenario policy 改变，应视为 benchmark contract 变更。
