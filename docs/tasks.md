# 选择一个任务

ChemWorld 当前提供 15 个任务。它们共享同一套世界律和操作语义，但会改变实验目标、预算、仪器、
允许操作与 episode 结构。

!!! tip "不知道选哪个？"
    - 第一次使用：`reaction-to-assay`
    - 开发分离流程：`reaction-to-purification`
    - 测试主动学习：`partition-discovery`
    - 研究安全约束优化：`flow-reaction-optimization`
    - 研究长流程规划：`reaction-to-crystallization` 或 `reaction-to-distillation`

## 按研究问题选择

| 你想测试什么 | 推荐任务 | 任务形式 |
| --- | --- | --- |
| Agent 能否完成一次合法实验 | `reaction-to-assay` | 单次实验 |
| Agent 能否把反应与后处理连起来 | `reaction-to-purification` | 单次长流程 |
| Agent 能否用有限实验学习隐藏规律 | `partition-discovery` | 多实验 campaign |
| Agent 能否处理目标—安全权衡 | `reaction-safety-constrained`、`flow-reaction-optimization` | 约束优化 |
| Agent 能否选择测量并解释证据 | `low-budget-characterization`、`reaction-mechanism-explanation` | 部分可观测 |
| Agent 能否规划结晶或蒸馏路线 | `reaction-to-crystallization`、`reaction-to-distillation` | 反应—分离耦合 |
| Agent 能否跨场景泛化 | `public-private-generalization` | 公开/私有世界 |

## 完整任务目录

| Task ID | 适合研究 | 当前角色 |
| --- | --- | --- |
| `reaction-optimization-standard` | 反应条件优化 | 能力切片 |
| `reaction-safety-constrained` | 带安全约束的控制 | 能力切片 |
| `reaction-mechanism-explanation` | 测量、机理表征与解释 | 能力切片 |
| `reaction-to-assay` | 从投料到最终检测的基本闭环 | core 回归 |
| `reaction-to-purification` | 反应、LLE、洗涤、干燥、浓缩与转移 | core 回归 |
| `partition-discovery` | 在预算内学习隐藏分配规律 | core + 研究候选 |
| `purity-yield-tradeoff` | 纯度、回收率与成本权衡 | 能力切片 |
| `public-private-generalization` | 场景泛化 | 能力切片 |
| `low-budget-characterization` | 低预算仪器规划 | 能力切片 |
| `tool-agent-planning` | 长程工具调用 | 能力切片 |
| `reaction-to-crystallization` | 晶种、冷却结晶与过滤 | 研究核心候选 |
| `reaction-to-distillation` | 反应后蒸馏与切割 | 研究核心候选 |
| `flow-reaction-optimization` | 几何解析 PFR 优化 | 研究核心候选 |
| `electrochemical-conversion` | 电化学转化与能效 | 探索任务 |
| `equilibrium-characterization` | 水相平衡表征 | 探索任务 |

所有任务当前整体成熟度均为 `lite`。这表示它们具有稳定接口、守恒与趋势检查，但不表示能够预测
真实化学，也不表示所有任务已经适合作为正式排行榜。

## 单次实验还是 Campaign？

- `single_experiment`：从初始物料出发，完成一条实验流程，通常以 `final_assay` 结束。
- `campaign`：在总预算内完成多次实验，用前一次结果决定下一次配方或测量。

如果你的方法只在每次终检后更新下一套 recipe，它属于**实验间主动学习**；如果它会根据同一实验
里的中间测量调整后续操作，才属于**实验内自适应控制**。

## 在代码中读取任务合同

```python
from chemworld.tasks import get_task, list_tasks

for task in list_tasks():
    print(task.task_id, task.episode_mode, task.budget)

task = get_task("reaction-to-distillation")
print(task.contract_hash)
print(task.allowed_operations)
```

命令行也可以查看当前任务和 readiness：

```bash
chemworld tasks list
chemworld tasks readiness
```

任务使用 World Law `chemworld-physical-chemistry-v0.4` 与 Task Contract
`chemworld-task-contract-0.6`。`core`、`serious` 等套件名描述的是用途，不是质量徽章；正式比较前
请继续阅读[当前科学状态](benchmark_release.md)与[评测协议](benchmark_protocol.md)。
