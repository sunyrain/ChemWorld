# 模型成熟度

成熟度描述模型在声明适用域内的证据强度，不是对整个任务或项目的笼统评级。每个任务都会
公开 `physics_maturity`、`kernel_maturity` 和 `proxy_allowed`。

## 等级定义

| 等级 | 含义 |
| --- | --- |
| `proxy` | 用于稳定交互语义的有界近似；不能作为现实预测。 |
| `lite` | 满足基本物理趋势与守恒合同，但参考校准范围有限。 |
| `reference_validated` | 在明确小范围内通过解析解、文献值或独立参考后端对照。 |
| `professional_candidate` | 具备单位、适用域、诊断、守恒、provenance 和参考证据，可进入更专业验证。 |
| `professional` | 已达到模型卡声明的广泛专业验证要求；当前正式任务不依赖此标签。 |

任务整体成熟度采用最保守聚合：任何必需模块为 proxy，任务就不会被描述为更高成熟度。

## 当前运行时边界

| 运行时表面 | 当前等级 | 说明 |
| --- | --- | --- |
| 反应网络与 batch runtime | `lite` | 机制驱动、守恒、带热账；不是数据库级真实反应预测。 |
| 冷却结晶 | `professional_candidate` | van't Hoff 溶解度、PBM、晶种、CSD 与物料闭合。 |
| 连续流 PFR | `professional_candidate` | 几何、停留时间、轴向热边界、压降和求解器诊断。 |
| 萃取与洗涤 | `professional_candidate` | 活度修正分配、逐级收敛、夹带、TPD-style 诊断与守恒。 |
| 蒸馏 | `reference_validated` | 受控 VLE shortcut 切片；不是完整精馏塔设计。 |
| 电化学任务运行时 | `professional_candidate` 子模块 + `lite` 任务 | Nernst/Butler-Volmer、传质、控制和双电层均有明确适用域。 |
| 干燥、浓缩、转移 | `proxy` | 尚无覆盖相同任务语义的专业实现，继续显式标记。 |
| 合成仪器与谱图 | `lite`/局部候选 | 用于部分可观测 benchmark，不预测真实样品谱图。 |
| 安全与成本 | `lite`/候选 screening | 作为约束信号；不是法规合规或装置安全认证。 |

## 如何读取任务声明

```python
from chemworld.tasks import get_task

card = get_task("flow-reaction-optimization").to_dict()
print(card["physics_maturity"])
print(card["proxy_allowed"])
for module in card["kernel_maturity"]["modules"]:
    print(module["module_id"], module["level"], module["model_ids"])
```

发布结果时必须保留这些字段。只展示分数而省略模型成熟度，会让结果失去正确的解释边界。
