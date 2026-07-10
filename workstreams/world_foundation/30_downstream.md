# WF-30 Dry、Concentrate、Transfer

范围：移除 `chemworld_separation_proxy` 对应的三个 fallback。

Owned paths：新增独立 `drying_units.py`、`concentration_units.py`、`transfer_units.py` 及各自 cards、
fixtures 和 tests；不得与相平衡团队共改 `extraction_units.py`。

不修改：`phase_separation_services.py`、`world/separation_kernel.py`、task maturity 与 runtime route；
最终接管由 110 完成。

交付：湿组分/干燥剂、VLE/热量/真空、hold-up/dead-volume 三套 typed model；极限、守恒、设备
容量、失败诊断和 adapter proposal。详细要求见主清单 WF-04。
