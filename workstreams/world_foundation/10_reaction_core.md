# WF-10 反应动力学与反应器

范围：reaction network、rate law、thermochemistry coupling、batch/semibatch/CSTR/PFR solver。

Owned paths：`reaction_network*.py`、`reaction_rate_laws.py`、`reaction_reference_cases.py`、
`batch_reactors.py`、`semibatch_reactors.py`、`cstr_*.py`、`reactor_*.py`、模块专属测试。

不修改：task、runtime services/registry、instrument、flow/electrochemistry、顶层 `__init__.py`。

交付：解析极限、守恒/非负性、热耦合、solver failure、Cantera 或等价参考对照、独立 adapter
proposal。详细要求见主清单 WF-01/WF-02。
