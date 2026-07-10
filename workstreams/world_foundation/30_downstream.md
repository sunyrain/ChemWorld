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

`wf-30-drying-sorbent` 交付 dry 的有限容量 reference slice：声明式 sorbent card、竞争共享位点
平衡、有限接触时间、初始吸附库存/解吸、机械夹带和 spent-sorbent 废物流。湿液、干燥液、夹带液
和吸附相逐组分闭合；单组分平衡对照解析二次方程，多组分平衡独立对照 SciPy 非线性求解。

该 proposal 使用 `chemworld_sorbent_drying_vnext`，同样保持 `runtime_addition`。它不声称代表任意
真实干燥剂，也不覆盖真空或热干燥；参数必须来自后续带 provenance 的 sorbent/property card。
在 concentrate slice 和 WF-110 路由/基准重冻结完成前，共享 v0.3 proxy 仍不得删除。

`wf-30-vacuum-concentration` 补齐 concentrate 的 reference slice：在声明的物性求值温度下使用
gamma-Raoult 瞬时蒸气组成，显热升温后由加热功率与设备最大蒸发速率共同限制差分批式蒸发。
溶剂终点、产品回收下限、最低残液体积与泡点压力均为事件边界；蒸出物显式拆分为冷凝回收和
vent loss，并逐组分关闭液相/冷凝/放空以及等效液体体积和显热/潜热账本。

单挥发组分对照解析功率-潜热极限，二元理想体系对照闭式 Rayleigh 恒等式，多组分域扫描验证
设备与守恒边界。至此 dry、concentrate、transfer 三个独立 vNext proposal 均已有候选实现；共享
`chemworld_separation_proxy` 仍只允许由 WF-110 在新 World Law 路由接管和 benchmark 重冻结后移除。
