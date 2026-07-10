# WF-60 受设备与热负荷约束的蒸馏候选

本工作流已交付 `chemworld_duty_limited_distillation_vnext`，作为下一版 World Law 对
`vle_shortcut_distillation` 的显式 runtime replacement proposal。当前版本只提交专业候选及机器可读
适配契约；WF-110 在统一集成、可达性审计和基准重冻结前不会修改 v0.3 runtime。

## 已交付能力

- 保留现有参考校验过的恒相对挥发度多组分分配核，并用精确组分账本验证 distillate/bottoms 闭合；
- 计算进料组成泡点压力，未完成显热升温或未达到泡点时返回可解释的零切割结果；
- 同时核算显热、再沸潜热、全凝器负荷和内部汽相流量；
- 用二分求解把目标切割收缩到再沸器、冷凝器、汽相流量、塔器最大切割和最小残液量共同允许的范围；
- 报告轻重关键组分纯度与回收率；对满足二元适用域的请求报告 Fenske 最少级数、Underwood
  最小回流比和 Gilliland 理论级数/安装裕量；
- 所有单位、有效域、设备能力、失败策略、来源与成熟度均进入 provider contract 和 adapter manifest。

## 模型边界

这是面向 agent 环境的受约束 shortcut column，不是严格的逐板 MESH 动态模拟。当前假设包括恒相对
挥发度、给定温度下的组分性质、全凝器、无压降/热损以及以批次总时长折算的平均汽相负荷。
FUG 诊断仅在二元、关键组分有效且实际回流高于最小回流比时成立；其它情况保留分离、物料和能量
结果，同时以 `fug_available=false` 和 warning 明示诊断缺口。

参考边界固定到 IDAES commit `4275c45bfa76cd5b05926beaa8eee58f7b0b05e8` 的 tray column、
condenser 和 reboiler 约定。该引用用于设备边界与术语对齐，不宣称数值结果等同于 IDAES 严格求解。

## 集成与验收

proposal 位于 `adapters/wf-60-duty-limited-distillation.json`，目标 operation 为 `distill`，替代对象为
`vle_shortcut_distillation`。WF-110 集成时仍须完成 runtime/reference 双证据、operation → model
可达性、旧路由移除、World Law 升级以及 golden/benchmark 重冻结；在此之前不得删除现有实现或提升
正式任务成熟度。

专项测试覆盖无约束等价、FUG 诊断、五类独立能力瓶颈、热/泡点零切割、回流与切割响应、三组分
输入、超域失败、provider failure policy、清单一致性和 20 组守恒参数扫描。
