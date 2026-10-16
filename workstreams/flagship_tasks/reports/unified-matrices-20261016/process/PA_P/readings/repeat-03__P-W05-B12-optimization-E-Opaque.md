# 辨认失败操作的证据边界，局部溶剂与后处理关系仍不足以建立普遍法则

`repeat-03/P-W05-B12-optimization-E-Opaque`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-03__P-W05-B12-optimization-E-Opaque.json)

## 问题与先验

无资料条件从催化剂和溶剂筛选起步，初始笔记提出材料效应、富集和洗涤方向，目标为纯度至少0.80。只有首末两版笔记，不能由末稿倒推各次选择的同期动机。

## 预期与实验

批5–7在同C1、380K、7200s下比较S1/S2/S3，上游HPLC产率0.250/0.407/0.217，支持S2局部优势。批6/8/9相同C1/S2上游产率0.407/0.420/0.413，而X3单洗、X0三洗、X1双洗的完整后处理不同。

## 实际证据

批2省略初始双相建立，事件22–27的萃取、混合、分相、洗涤与干燥均因has_phase_system被拒，最终0.505纯度/0.0963回收是未萃取粗品。K1/K2明确识别该失败，拒绝把它作为X0流程证据。批6的X3单洗得到纯度0.659316/回收0.215380，作为未合格fallback；全部12批均无纯度达标。

## 修订

末笔记撤回额外洗涤有益的概括；K1正确指出失败流程不是名义操作的效果。后处理比较仍同时改变萃取剂和洗次，不足以分开二者。K1所称催化剂—溶剂交互必需也强于稀疏且部分严重度混杂的设计。

## 后续采用

Q对未直接建立的X2优势保留弱识别说明，但新浓度区间仍预测洗涤提高纯度、牺牲回收；这属于迁移假定而非源实验已证。K2提出降低试剂和催化剂、保持比例的反应前HPLC，以区别绝对催化剂浓度与催化剂/试剂比解释，直接回应后测的低浓度不确定性。

## 未解决问题及解释限制

批6/8/9是相同上游的重复，不是精确完整流程重复。批10水相与批6有机相比较同时改变温度/时间，不能归因为保留相。K2的比例判别尚未执行，且改变反应条件后的中间结果仍可有多种解释；这些提议不能计为已获得的新证据。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 181, 'last_event_id': 'runner-operation-0181'}

> suspend the claim that extra washing is beneficial.

K1

> Batch 2 is an important negative control for process interpretation.

K1

> It must not be treated as evidence for the nominal X0 workup.

Q

> X2 is only weakly identified, but campaign evidence suggests better target retention than X0
