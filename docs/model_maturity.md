# 模型成熟度怎么读

成熟度回答的是“这个模块在它声明的范围内经过了多少验证”，不是“它有多像现实世界”。每个任务
都会公开整体 `physics_maturity`、逐模块 `kernel_maturity` 和 `proxy_allowed`；整体等级由最弱的
必需模块决定。

| 等级 | 含义 |
| --- | --- |
| `proxy` | 只维持交互语义的有界近似；不能进入正式无-proxy 套件。 |
| `lite` | 满足基本趋势、单位和守恒合同，参考校准仍有限。 |
| `reference_validated` | 在明确小范围内通过解析、文献或独立参考对照。 |
| `professional_candidate` | 具备适用域、诊断、守恒、provenance 与参考证据，仍未达到工业验证。 |
| `professional` | 达到模型卡声明的广泛专业验证；当前任务不依赖此标签。 |

任务整体采用最保守聚合。当前 15 个任务整体均为 `lite` 且 `proxy_allowed=false`，因为反应或
合成观测仍是最弱必需模块；局部 provider 可以是 `reference_validated` 或
`professional_candidate`。

| 运行时表面 | 当前等级 | 解释边界 |
| --- | --- | --- |
| 反应网络与 batch runtime | `lite` | 机制驱动、守恒、带热账；不是反应数据库预测器。 |
| 合成仪器与谱图 | `lite` | 状态耦合、可复现的部分观测；不预测真实样品谱图。 |
| LLE 与 wash | `professional_candidate` | 稳定性门控、活度修正、夹带和物料闭合。 |
| 冷却结晶、连续流、蒸馏 | `professional_candidate` | 有设备/求解/守恒诊断；不是工业流程设计模型。 |
| 干燥、真空浓缩、转移 | `reference_validated` | 有限容量或有限设备的窄域 provider 与显式物料/能量账。 |
| 电化学 | `reference_validated` runtime + 候选子模块 | Nernst、Butler–Volmer、传质与电功账。 |

```python
from chemworld.tasks import get_task

card = get_task("reaction-to-purification").to_dict()
print(card["physics_maturity"], card["proxy_allowed"])
for module in card["kernel_maturity"]["modules"]:
    print(module["module_id"], module["level"], module["model_ids"])
```

模型成熟度和 benchmark 经验有效性是两道不同门禁。v0.4 后端已通过集成审计，四任务经典诊断
也已完成多 seed 回放；但该运行暴露了目标收益与风险退化的冲突，RL/LLM、机理泛化、私有评测和
独立复现仍缺失，因此当前仍是 benchmark candidate。
