# WF-40 相平衡、萃取与洗涤

范围：LLE、activity、flash、phase stability、tie-line、entrainment 和多级 extraction/wash。

Owned paths：`extraction_*.py`、`flash_*.py`、相平衡专属实现/cards/tests。共享 property 只通过 WF-00
provider protocol 获取。

不修改：dry/concentrate/transfer、runtime phase services、partition task/scenario。

交付：单相/两相极限、极端 K、相反转、不收敛和物料闭合参考证据；匿名虚拟物系与真实语义
property profile 分离。详细要求见主清单 WF-05。

## 已交付候选：稳定性耦合 LLE

`wf-40-lle-stability-coupling` 提供新的
`chemworld_stability_aware_lle_vnext` runtime 候选。每次 extraction/wash 接触在求解分配前先执行
两液相稳定性门禁，再迭代两相活度修正，并按显式或体积判定的连续相记录双向夹带。单液相、无分配或
非理想驱动力、分配迭代不收敛、接触器越界和逐组分闭合失败都会显式拒绝。

该 proposal 是 vNext staging 中首个真正的 `runtime_replacement`，请求替换
`activity_corrected_extraction_train_v1` 与独立的 `lle_phase_stability_diagnostic_v1`，避免 runtime
继续把“先分相”和“事后诊断”作为两条松散路线。当前 v0.3 runtime、任务合同和 benchmark 证据均未
修改；只有 WF-110 在完成状态映射审查、可达性检查和 benchmark 重冻结后才能执行替换。
