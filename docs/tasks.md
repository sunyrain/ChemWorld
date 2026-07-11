# Benchmark 任务

ChemWorld 注册 15 个任务，全部使用 `chemworld-physical-chemistry-v0.4` 和
`chemworld-task-contract-0.6`。任务之间只改变目标、预算、允许操作、仪器、episode 模式与
场景切片，不改变公共操作语义。

| Task ID | 主要能力 | 整体成熟度 |
| --- | --- | --- |
| `reaction-optimization-standard` | 反应条件优化 | `lite` |
| `reaction-safety-constrained` | 安全约束控制 | `lite` |
| `reaction-mechanism-explanation` | 机理表征与解释 | `lite` |
| `reaction-to-assay` | 投料到最终检测 | `lite` |
| `reaction-to-purification` | 反应、LLE、洗涤、干燥、浓缩与转移 | `lite` |
| `partition-discovery` | 预算内学习隐藏分配规律 | `lite` |
| `purity-yield-tradeoff` | 纯度、回收率和成本权衡 | `lite` |
| `public-private-generalization` | 场景泛化 | `lite` |
| `low-budget-characterization` | 低预算仪器规划 | `lite` |
| `tool-agent-planning` | 长程工具调用 | `lite` |
| `reaction-to-crystallization` | 晶种、冷却结晶与过滤 | `lite` |
| `reaction-to-distillation` | 反应后蒸馏与切割 | `lite` |
| `flow-reaction-optimization` | 几何解析 PFR 优化 | `lite` |
| `electrochemical-conversion` | 电化学转化与能效 | `lite` |
| `equilibrium-characterization` | 水相平衡表征 | `lite` |

`core` 套件用于 API、回放和发布回归。六个 `serious` 任务定义研究候选边界。其历史 v1 证据
对应旧 World Law；当前 v0.4 合同在新的有效性与统计证据完成前显示 `candidate`，即使所有结构
合同均通过也不会自动显示 `validated`。

```python
from chemworld.tasks import get_task, list_tasks

for task in list_tasks():
    print(task.task_id, task.to_dict()["physics_maturity"])

task = get_task("reaction-to-distillation")
print(task.contract_hash)
print(task.allowed_operations)
```

`single_experiment` 表示一条完整实验流程；`campaign` 允许在总预算内完成多次实验并用前次观测
选择后续实验。运行 `chemworld tasks readiness` 查看当前合同与经验状态。正式比较方法前阅读
[评测协议](benchmark_protocol.md)和[限制](limitations.md)。
