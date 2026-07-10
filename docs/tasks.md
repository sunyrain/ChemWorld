# Benchmark 任务

当前发布注册 15 个任务。它们共享 `chemworld-physical-chemistry-v0.2`，但在目标、预算、允许
操作、仪器、episode 模式和隐藏场景上形成不同能力切片。

## 任务目录

| Task ID | 主要能力 | 整体成熟度 |
| --- | --- | --- |
| `reaction-optimization-standard` | 反应条件优化 | `lite` |
| `reaction-safety-constrained` | 安全约束下的反应控制 | `lite` |
| `reaction-mechanism-explanation` | 机理辨识与解释 | `lite` |
| `reaction-to-assay` | 从投料到最终检测的最小闭环 | `lite` |
| `reaction-to-purification` | 反应、萃取、纯化和 final assay | `proxy` |
| `partition-discovery` | 有限预算下学习隐藏分配规律 | `lite` |
| `purity-yield-tradeoff` | 纯度、回收率、成本的多目标权衡 | `proxy` |
| `public-private-generalization` | 跨公开/私有场景泛化 | `lite` |
| `low-budget-characterization` | 低预算仪器规划 | `lite` |
| `tool-agent-planning` | tool-using agent 长程规划 | `proxy` |
| `reaction-to-crystallization` | 晶种、冷却结晶与过滤 | `lite` |
| `reaction-to-distillation` | 反应后蒸馏与切割 | `lite` |
| `flow-reaction-optimization` | 几何解析 PFR 条件优化 | `lite` |
| `electrochemical-conversion` | 电化学转化与能效 | `lite` |
| `equilibrium-characterization` | 平衡体系表征 | `lite` |

任务整体等级按最弱必需模块聚合。例如 flow 任务包含 `professional_candidate` PFR，但其反应和
合成仪器层仍为 `lite`，所以任务整体为 `lite`。纯化任务仍使用 dry/concentrate/transfer proxy，
因此整体保持 `proxy`。

## Episode 模式

- `single_experiment`：一次 Gym episode 只包含一条完整实验流程，合法 final assay 后终止；
- `campaign`：一次 episode 可在总预算内完成多条 experiment，适合 BO、LHS、greedy 或
  world-model learner。

交互式 step、固定 recipe、LLM tool call 和 replay 是运行方式，可作用于任一 episode 模式。

## 选择任务

```python
from chemworld.tasks import list_tasks, get_task

for task in list_tasks():
    print(task.task_id, task.to_dict()["physics_maturity"])

card = get_task("reaction-to-crystallization").to_dict()
print(card["allowed_operations"])
print(card["kernel_maturity"])
```

正式评测前请阅读[任务卡与冻结合同](task_cards.md)、[评测协议](benchmark_protocol.md)和
[Official Seed Suite](seed_suite.md)。
