# 模型成熟度

成熟度表示模型在声明适用域内的证据强度，不代表 ChemWorld 能预测真实化学。每个任务公开
`physics_maturity`、逐模块 `kernel_maturity` 和 `proxy_allowed`。

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

模型成熟度和 benchmark 经验有效性是两道不同门禁。v0.4 后端已通过集成审计，但新合同的
多 seed 有效性、功效、泛化与方法对比尚未冻结，因此当前只能称为 backend candidate。
