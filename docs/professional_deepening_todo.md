# 专业化深化 TODO

本页对应更长期的专业化深化路线。它位于基础工程收束之后，目标是把 ChemWorld 从可控
虚拟 benchmark 推向更有化学可信度的 research environment。

## 操作规则

- 先稳定 public API 和任务合同，再深化物理模块。
- 每个新增专业模块必须声明 maturity 和验证证据。
- 不把重型 backend 变成默认依赖。
- 所有深化工作都应保持 replay、trajectory 和评测协议兼容。

## 活跃深化工作

- 物性核心：密度、摩尔体积、扩散、黏度、热容等。
- 相平衡：分配、液液平衡、汽液平衡。
- 反应网络：机制库、速率模型、副反应和降解。
- 单元操作：萃取、结晶、蒸馏、反应器。
- 仪器：虚拟光谱、噪声、校准和观测代价。

## 模块家族

- `properties`
- `phase_equilibrium`
- `reaction_network`
- `reactor_models`
- `separation_units`
- `spectroscopy`
- `validation_backends`

## 第一批候选

优先选择能显著改善 task realism、同时不破坏 benchmark 可复现性的模块。建议从分配/
相平衡、反应选择性和仪器噪声模型开始。
