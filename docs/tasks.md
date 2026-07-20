# 选择任务

ChemWorld 当前提供 15 个任务。它们共享 World Law
`chemworld-physical-chemistry-v0.4` 和 Task Contract `chemworld-task-contract-0.9`，并由
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
| `electrochemical-conversion` | `9cc0c792e171737c5ffd5dc03772dcff724a19ae5c504b7d573257eadfa89d63` | `reference_validated` | `false` |
| `equilibrium-characterization` | `046067c1c75a57032b3b4307f386b23c706507178856ee20cffa70478cd0e42a` | `reference_validated` | `false` |
| `flow-reaction-optimization` | `834207984ba38bfab373c400fc715d63908100db3ca9549185daf4fb5aca5a4f` | `reference_validated` | `false` |
| `low-budget-characterization` | `c9a46ddac7960377bfce556c15d841ed9c6093684ac48966f0a6cf79aa6693fc` | `reference_validated` | `false` |
| `partition-discovery` | `8f5e648c9c4ad3138391014a536dc9df3008b99152c70da0f2a173914ec0d37c` | `reference_validated` | `false` |
| `public-private-generalization` | `5aec9b64b8ed4cc5da009ea669978a83f76c913b3bc7e497236d231571ab7c3d` | `reference_validated` | `false` |
| `purity-yield-tradeoff` | `431b4b6f8c25ea53a937b94ea07966d32609e2db2a76bd73589109bb5aaf98dd` | `reference_validated` | `false` |
| `reaction-mechanism-explanation` | `addead31f7c7a85fa81278445bdf85a9fb03c89c5bb740ac6262cd28c0853142` | `reference_validated` | `false` |
| `reaction-optimization-standard` | `e8de4285f89c507c305226c9f1f37454879517c1069b9bfab6ae26154ac1e4bc` | `reference_validated` | `false` |
| `reaction-safety-constrained` | `867e1a8473a40e679af88ad4679d5753ea7aa90ae5bf9555aa2d9903860c63ec` | `reference_validated` | `false` |
| `reaction-to-assay` | `1366e4e73eedeee2fa5d630831614f07a7c4f09d5661e9fb6cfccab57643bd1f` | `reference_validated` | `false` |
| `reaction-to-crystallization` | `756ca669f81a27290cd72e25c05cf9ed1f7cae0db6b299f1332d8a907b642e8f` | `reference_validated` | `false` |
| `reaction-to-distillation` | `d19adb180200831acca5bdbb6e05a6a9de1760b494eb03f6be5a43162c6b9109` | `reference_validated` | `false` |
| `reaction-to-purification` | `9bb160c677f4feb72c06dfb4985e29abfce68499a0a6df02607b2cbeb720b0ca` | `reference_validated` | `false` |
| `tool-agent-planning` | `a7972dfc2519fc48e1e7eb6f635ba703aa52f0bbf66688e86dbb0df105a32ddf` | `reference_validated` | `false` |

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
