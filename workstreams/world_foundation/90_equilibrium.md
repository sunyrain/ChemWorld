# WF-90 水相与平衡化学

范围：acid/base、activity、complexation、precipitation 和小规模 Gibbs minimization。

Owned paths：`equilibrium*.py`、`equilibrium_chemistry*.py` 及专属 fixtures/tests。

不修改：pH instrument、runtime observation、equilibrium task/scenario/threshold。

交付：元素/电荷/KKT residual、相出现/消失、初值不变性、多元酸碱与同时沉淀 reference cases，
以及 Reaktoro/Cantera/解析对照。详细要求见主清单 WF-10。
