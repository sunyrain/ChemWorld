# 阅读任务卡

任务卡是 Agent 的实验说明书：目标、预算、允许操作、仪器、评分、合同 hash、成熟度和适用边界都从
同一份可执行 `TaskSpec` 生成。不要把网页中的示例参数当成固定最优配方。

## 先看这六个字段

| 字段 | 如何使用 |
| --- | --- |
| `task_id` | 创建环境与绑定结果的稳定标识 |
| `contract_hash` | 检测任务、轨迹与结果是否属于同一合同 |
| `allowed_operations` | 当前任务允许出现的操作全集；实际可执行性还取决于状态 |
| `budget` / `episode_mode` | 区分单次实验和多实验 campaign，并限制资源 |
| `physics_maturity` | 最弱必需模块的保守聚合等级 |
| `proxy_allowed` | 正式路径是否允许 proxy；当前 15 个任务均为 `false` |

当前 backend v0.5 candidate 下，全部任务均为 `reference_validated` 且
`proxy_allowed=false`。完整 15 任务 hash 表以[任务目录](tasks.md#current-task-contracts)为唯一用户文档
来源，避免在多个页面复制后漂移。

## 查看一张任务卡

```bash
chemworld tasks card reaction-to-assay
chemworld tasks card reaction-to-purification
chemworld tasks card partition-discovery
```

也可以在 Python 中读取：

```python
from chemworld.tasks import get_task, get_task_card

task = get_task("partition-discovery")
card = get_task_card(task.task_id)

print(task.contract_hash)
print(task.allowed_operations)
print(card["physics_maturity"], card["proxy_allowed"])
```

## 三类常用入口

### 最小闭环：`reaction-to-assay`

适合验证动作顺序、终止、final assay 与 replay。它是接口回归任务，不是复杂优化排行榜。

### 多阶段流程：`reaction-to-purification`

覆盖反应、液液分离、洗涤、干燥、浓缩和转移。高分必须同时面对物料损失、成本和操作约束。

### 主动探索：`partition-discovery`

Agent 在 campaign 中通过有限测量学习隐藏分配规律。它适合实验间主动学习，但不自动证明现实溶剂
体系的分配系数。

## 解释成熟度

`reference_validated` 只表示模型卡声明的窄域参考证据已经通过；它不等于工业验证。没有 proxy route
只说明正式运行路径明确，也不意味着能够预测任意真实材料。进一步边界见[模型成熟度](model_maturity.md)
与[适用范围](limitations.md)。
