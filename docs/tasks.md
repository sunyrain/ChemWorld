# 选择任务

ChemWorld 当前提供 15 个任务。它们共享 World Law
`chemworld-physical-chemistry-v0.5` 和 Task Contract `chemworld-task-contract-1.1`，并由
`chemworld-physical-chemistry-v0.5-candidate` 后端候选冻结绑定。

!!! info "当前统一事实"
    15 个任务的正式必需路径均为 `reference_validated`，且全部
    `proxy_allowed=false`。这表示窄适用域内已有参考、失败域、守恒、运行时与回放证据；它不表示真实
    化学预测、工业验证或完整 benchmark 排名已经成立。

## 从研究问题开始

| 你想研究什么 | 推荐任务 | 交互形式 |
| --- | --- | --- |
| 完成一次合法实验闭环 | `reaction-to-assay` | 单次实验 |
| 串联反应与后处理 | `reaction-to-purification` | 单次长流程 |
| 用有限实验学习隐藏规律 | `partition-discovery` | 多实验 campaign |
| 研究目标、风险与成本权衡 | `reaction-safety-constrained`、`flow-reaction-optimization` | 约束优化 |
| 选择测量并解释证据 | `low-budget-characterization`、`reaction-mechanism-explanation` | 部分可观测 |
| 规划结晶或蒸馏路线 | `reaction-to-crystallization`、`reaction-to-distillation` | 多阶段流程 |
| 测试世界变化下的适应 | `public-private-generalization` | 分布变化 |

## 15 个当前任务合同 { #current-task-contracts }

下表是 backend v0.5 candidate 冻结绑定的当前 hash。运行时也会把相同 hash 写入任务信息和轨迹；
hash 不一致时，旧轨迹不能被静默解释为当前结果。

| Task ID | Task contract hash | Maturity | Proxy |
| --- | --- | --- | --- |
| `electrochemical-conversion` | `45b6cdbaf1f9c7fc313e1589f37b17bde9fd678d40e0bd98e64a62622ecac494` | `reference_validated` | `false` |
| `equilibrium-characterization` | `77e1c30cd83e1a09363cef3ea58b1ddefb415bb1d790d6d63a3c519f45325917` | `reference_validated` | `false` |
| `flow-reaction-optimization` | `697a5956fd3ad242b78144c6fd11e6d3ca5335c493336d5b9cacb13decefc16b` | `reference_validated` | `false` |
| `low-budget-characterization` | `2cd44cd76937b9e95a9ae4282994a540f4d390b3f9a59c963ca60ff2db72706b` | `reference_validated` | `false` |
| `partition-discovery` | `efa54ba1ab6c5c40c0bdc77f57b2234487a58d98ed5043f273496ef103b6599e` | `reference_validated` | `false` |
| `public-private-generalization` | `bf092340dfcbb59fe261a7e73b3042449d57858a60f73d3b19336f15b627e8b8` | `reference_validated` | `false` |
| `purity-yield-tradeoff` | `2d2ab14c61e90b87c1c530f74b9e6fbf0c82966199d78e99ec755ba5ba208e76` | `reference_validated` | `false` |
| `reaction-mechanism-explanation` | `097bd39293eae4063dc84ed0af299935aefce5c391183944302431d5d6c93f6e` | `reference_validated` | `false` |
| `reaction-optimization-standard` | `c7a5bee5dffa318f30097f745a043ca1c6521f4b5770e48023c067206bd6c902` | `reference_validated` | `false` |
| `reaction-safety-constrained` | `a7a705dc87bce6684aa8022439c4cb256486df875bbce9a624111e51047bd102` | `reference_validated` | `false` |
| `reaction-to-assay` | `afb93071e7571ec58206a4eb62170e39c7982bd15f0dd12db97ceb08f42df49b` | `reference_validated` | `false` |
| `reaction-to-crystallization` | `a73d3d0b3c86b7a3a11f334ba2efd8f8bca55ba740207f39b1b123f5913a7416` | `reference_validated` | `false` |
| `reaction-to-distillation` | `49e465bce0c5d2fd4a8f73d298cf9d4d2d37c2ca0605aaf6caaab8a9358bff74` | `reference_validated` | `false` |
| `reaction-to-purification` | `17dd0ecbb478790013f511f373cbc3ca9c9489240b1dce0e35c84bfcd3a661e0` | `reference_validated` | `false` |
| `tool-agent-planning` | `2d0309f3ad1bef65d2f1cf65d8ef778d980143305bfb201df26a713f944b5aba` | `reference_validated` | `false` |

## 单次实验与 Campaign

- `single_experiment`：从初始物料出发，完成一条实验流程，通常以 final assay 结束。
- `campaign`：在总预算内完成多次实验，用前一次结果决定下一次配方、操作或测量。

只在每次终检后更新 recipe 的方法属于**实验间主动学习**；根据同一实验内的中间测量调整后续操作，
则属于**实验内自适应控制**。跨层级只能作系统比较，算法归因必须在相同信息与交互合同下完成。

## 在代码中读取合同

```python
from chemworld.tasks import get_task, get_task_card, list_tasks

for task in list_tasks():
    card = get_task_card(task.task_id)
    print(task.task_id, task.contract_hash, card["physics_maturity"], card["proxy_allowed"])

task = get_task("reaction-to-distillation")
print(task.allowed_operations)
```

也可以使用已经发布的 CLI：

```bash
chemworld tasks list
chemworld tasks readiness
chemworld tasks card flow-reaction-optimization
```

任务可执行不等于任务已适合论文主张。当前算法证据边界见[研究发现与证据](benchmark_release.md)，
比较口径见[公平评测协议](benchmark_protocol.md)。
