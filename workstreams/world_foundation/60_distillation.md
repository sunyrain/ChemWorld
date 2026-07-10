# WF-60 蒸馏

范围：现有 VLE shortcut、多组分 flash、batch cut，以及明确选择后的 column model 边界。

Owned paths：蒸馏专属 `separations.py` 切片、新增 distillation model/card/fixtures/tests。

不修改：concentration、runtime distillation service、task cut/threshold。

交付：Fenske/Underwood/Gilliland 或明确 shortcut 极限、物料/能量闭合、回流/切割响应、超域失败
与 adapter proposal。详细要求见主清单 WF-07。
