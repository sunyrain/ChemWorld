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

任务整体采用最保守聚合。当前 15 个任务的正式必需路径均至少为
`reference_validated`，且 `proxy_allowed=false`。这只表示窄域 benchmark 合同已有参考、失败域、
运行时和回放证据；不表示能够预测任意真实化学体系，也不等于工业验证。

| 运行时表面 | 当前等级 | 解释边界 |
| --- | --- | --- |
| 反应网络与 batch runtime | `reference_validated` | 动态调用质量作用量/Arrhenius 网络与 batch 能量模型；不是反应数据库预测器。 |
| 合成仪器与谱图 | `reference_validated` | UV/Vis、HPLC、GC、pH 与终点 assay 均有有界参考合同；不预测真实样品谱图。 |
| LLE 与 wash | `professional_candidate` | 稳定性门控、活度修正、夹带和物料闭合。 |
| 冷却结晶、蒸馏 | `professional_candidate` | 具备正式 provider、设备/求解/守恒诊断；不是工业流程设计模型。 |
| 连续流 | `reference_validated` | 单相不可压缩几何 PFR、分布传热与 Darcy–Weisbach 压降；不是完整连续流平台。 |
| 干燥、真空浓缩、转移 | `reference_validated` | 有限容量或有限设备的窄域 provider 与显式物料/能量账。 |
| 电化学 | `reference_validated` runtime + 候选子模块 | Nernst、Butler–Volmer、传质、双电层、水相平衡与电功账。 |

```python
from chemworld.tasks import get_task

card = get_task("reaction-to-purification").to_dict()
print(card["physics_maturity"], card["proxy_allowed"])
for module in card["kernel_maturity"]["modules"]:
    print(module["module_id"], module["level"], module["model_ids"])
```

模型成熟度和 benchmark 经验有效性是两道不同门禁。v0.4 后端的正式 provider 路由已通过动态
事务审计，但完整回归、golden 重建、任务区分度/可学习性、算法公平矩阵、私有评测和独立复现仍需
在 backend freeze 后执行。因此目前仍是 benchmark candidate，不能从模型等级直接推导论文结论。
