# WF-30 Dry、Concentrate、Transfer

范围：移除 `chemworld_separation_proxy` 对应的三个 fallback。

Owned paths：新增独立 `drying_units.py`、`concentration_units.py`、`transfer_units.py` 及各自 cards、
fixtures 和 tests；不得与相平衡团队共改 `extraction_units.py`。

不修改：`phase_separation_services.py`、`world/separation_kernel.py`、task maturity 与 runtime route；
最终接管由 110 完成。

交付：湿组分/干燥剂、VLE/热量/真空、hold-up/dead-volume 三套 typed model；极限、守恒、设备
容量、失败诊断和 adapter proposal。详细要求见主清单 WF-04。

## 当前进度

`wf-30-transfer-holdup` 已认领 transfer 的第一个独立 reference slice：均相源容器、source heel、
transfer capacity、FIFO line hold-up、已有管线库存和 flush displacement。它逐组分返回 source、
target 与 line final inventory，并对物料和体积执行硬闭合。

该 proposal 使用新的 `chemworld_transfer_holdup_vnext` model id，暂时是 `runtime_addition`，不声明
已经替代同时覆盖 dry/concentrate/transfer 的 `chemworld_separation_proxy`。只有 WF-110 在 vNext
为 transfer 单独切换路由并完成轨迹、成本和风险重冻结后，才允许从 transfer 正式路径移除 proxy。
