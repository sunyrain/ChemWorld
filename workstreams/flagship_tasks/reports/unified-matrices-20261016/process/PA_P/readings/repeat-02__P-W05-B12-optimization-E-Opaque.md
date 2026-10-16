# 可重复反应产量引导洗涤探索，却未找到同时达标且高回收的完整流程

`repeat-02/P-W05-B12-optimization-E-Opaque`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-02__P-W05-B12-optimization-E-Opaque.json)

## 问题与先验

无资料。最初四批同时改变类别与严重度，首批温和C0/S0唯一终纯度合格0.837但回收零；C3/S2第4批上游产率0.151、终纯度0.725/回收0.091。v2/cursor64明确选该区域做温度时间与强化洗涤，不能把前四批混杂筛选当纯催化剂比较。

## 预期与实验

第5–8批同C3/S2、380 K/5400 s，四次上游产率0.226/0.227/0.217/0.240，对比第4批370 K/3600 s的0.151，形成重复支持的局部严重度与生成关系。后段X3双洗、X0单洗、X0留水相、X2单洗均未达纯度0.80。第11批把单次0.04 mol改为0.02+0.02 mol双加料，并同时改条件，不能识别component机制，但未像其他场一样耗尽试剂。

## 实际证据

最接近X比较是第6和8批同上游及洗涤的X0/X2，末纯度0.638/0.655、回收0.125/0.134，差较小而无重复；X3配方洗强度不同。第6与7的相选择比较还同时去除洗涤与干燥，水相0.376/0.064较差只说明所测流程，非单一相选择效应。第2与12相同上游产率0.125/0.127构成另一局部重复，下游不同。

## 修订

v3撤回靠增加洗强度就能达标的泛化，承认生产区上游稳定但下游未解决质量约束，按硬纯度规则退回第1批。K1/K2明确区分末端近一转化与前段转化，没有把相选择解释为后续继续反应。首批零回收仅是读数边界，不能说物理产物绝对不存在。

## 后续采用

Q以未测C1/S2、400 K、低催化剂的新条件外推，采用X2略优X0及延时提高产量/降低纯度的方向，并以催化剂比例分开回收等级。洗涤提高纯度仍作为模型，但与本场撤回的‘增加洗涤必达标’不是同一命题；不能据此直接说逻辑自相矛盾，只能说该新条件洗涤量效应未识别。

## 未解决问题及解释限制

任务找到一个读数合格但低回收方案，同时获得反应重复性和若干局部比较；不能以低优化成绩抹掉认识进展。无整个工艺严格重复、温度/时间解耦、分阶段物料衡算或浓缩对照；K2的定时取样诊断尚未执行。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 64, 'last_event_id': 'runner-operation-0064'}

> Test stronger washing on the productive C3/S2 region; accept some loss only if purity crosses 0.80.

事件：runner-operation-0081

v3 / cursor {'event_count': 194, 'last_event_id': 'runner-operation-0194'}

> Repeated larger washes did not rescue purity in the tested productive mixtures

事件：runner-operation-0081, runner-operation-0177

K1

> Across those four nominal reaction replicates, mean conversion was 0.480
