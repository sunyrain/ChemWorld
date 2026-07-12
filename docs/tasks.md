# 选择任务

ChemWorld 当前提供 15 个任务。它们共享 World Law
`chemworld-physical-chemistry-v0.4` 和 Task Contract `chemworld-task-contract-0.6`，并由
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
| `electrochemical-conversion` | `9f86e8550be9f8de98f4152104ef981c075697bf8cf378f040f5af4593235d09` | `reference_validated` | `false` |
| `equilibrium-characterization` | `64393d1da00e28101f71246ef13c1b69e03b0b213542e97afcb1add8f52eaa62` | `reference_validated` | `false` |
| `flow-reaction-optimization` | `aa47c74db1753f062a3e5f59208db8278c25db778390607892e20eaaeb30cdc9` | `reference_validated` | `false` |
| `low-budget-characterization` | `3d8bb180e63016b49b0f2c09694ad4f2d965d8096c9c615d021c987204283a29` | `reference_validated` | `false` |
| `partition-discovery` | `ce378e7bc5e725ed266db2bb639194c05f5f615ba0795b158c3c976cc787117e` | `reference_validated` | `false` |
| `public-private-generalization` | `d2a07d58a7c09d317239794eb5757fdcd5ea68514fc531bd2ece6436b08aa3fd` | `reference_validated` | `false` |
| `purity-yield-tradeoff` | `931d1c9c2364888a9cf390557614f78c042d3e166a8ae495d57cd1fdacd1ee0f` | `reference_validated` | `false` |
| `reaction-mechanism-explanation` | `4b69716dcd93cc32eb82beb335fea7f53062e5785496daecfc1530ddcdc39006` | `reference_validated` | `false` |
| `reaction-optimization-standard` | `0c80793551675a61dbde5f3e2456929e6e6c92574ca2f3d5fa967a97ddcdb1a5` | `reference_validated` | `false` |
| `reaction-safety-constrained` | `780ac2c552c7652b1afb8581d76bb2884bb99a334f7b85dffe73cf4c35834263` | `reference_validated` | `false` |
| `reaction-to-assay` | `395402a224b27cdbd070470ab1d0131e01c3bd472b773170bdcf4ba4f5a1bc96` | `reference_validated` | `false` |
| `reaction-to-crystallization` | `f15de7356ab11588028bb0add31b3461e9b90bf273de6dcdb4e123ce6b2f65ac` | `reference_validated` | `false` |
| `reaction-to-distillation` | `939b171d164139699d94c78250a937ab637be201f23bd62fddc47a864becaba7` | `reference_validated` | `false` |
| `reaction-to-purification` | `ee5d6b82178abeaaa6975680f2a469cbdad43f6b655bb65d6e437294a55e052d` | `reference_validated` | `false` |
| `tool-agent-planning` | `9752398c5b05a0d3a20df7df811ebb59e46a1c7f1e52ab6340fed9c5526c3ee9` | `reference_validated` | `false` |

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
