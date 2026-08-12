# Work II 蒸馏附加回滚 A-S Q0 分析

日期：2026-08-12

## 结论

provider-free seed-0 Q0 完成 `18/18` 执行和 `18/18` exact replay，0 physical failure、
0 platform failure、0 unsafe outcome。原生 `Acid + Alcohol <=> Ester + Water` 可逆反应被完整保留，
干预仅增加一条确定性的 `Ester + Water => Acid + Alcohol` 回滚路径，effective rate constant 为
`0.0005 s^-1`；执行时机制哈希、paired action plan、paired observation noise 与 participant-visible
leakage 门禁全部通过。

科学门禁未通过。蒸馏前 HPLC 的最大 paired yield/conversion gap 均为 `0.02324`，低于冻结门槛
`0.05`；selectivity 最大 gap 约为数值零。最长时长相对最短时长的平均 yield/conversion gap 增量为
`0.01505`，低于 `0.03` accumulation gate；因此没有两个注册 direct metrics 或两个相互分离的
grid cells 支持该拓扑效应。

该候选保留为完整科学拒绝，不扩展五 worlds，不生成 Q1/Q2 或 participant 配置，也不调整反应
强度、grid 或阈值。结果说明机制改动真实且平台可测，但当前公开 HPLC 终点不足以承担 A-S
terminal admission。

机器证据：
`workstreams/flagship_tasks/reports/work-ii-distillation-additional-rollback-q0-seed0-20260812.json`。
