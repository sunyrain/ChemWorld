# WF-100 物性、设备、安全与成本

范围：component/property provider、equipment cards、heat/transport property、安全包络和成本分项。

Owned paths：`properties*.py`、`property_*.py`、`eos*.py`、`equipment_*.py`、`safety_*.py`、
`transport_properties.py` 及专属 tests。现有交叉调用通过兼容 adapter 保持，不直接改调用方。

不修改：各工艺模块内部、runtime validation、task safety limit/score。

交付：统一单位/来源/温区/外推/冲突策略，设备约束和 safety/cost typed provider，参考后端对照及
adapter proposal。详细要求见主清单 WF-11。
