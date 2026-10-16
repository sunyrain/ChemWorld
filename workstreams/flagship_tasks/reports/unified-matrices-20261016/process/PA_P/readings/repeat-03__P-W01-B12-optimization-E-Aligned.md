# 前瞻加料和洗涤假设被结果收窄，混杂的单次低回收却主导全部浓缩预测

`repeat-03/P-W01-B12-optimization-E-Aligned`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-03__P-W01-B12-optimization-E-Aligned.json)

## 问题与先验

资料偏好X2；初始低转化在几种催化剂间相近，v2/cursor41提出缺失component0共反应物的替代解释，并预告补加检验。

## 预期与实验

批5加component0仍低转化，v3撤回必需共反应物解释。随后选择高回收的C2S2/400K3600s，做固定上游的0.01/0.02/0.04L洗涤。v3/cursor104明确预测最后洗量将跨0.80。

## 实际证据

三档终检纯度/回收为0.762/0.118、0.779/0.098、0.788/0.0748；方向符合纯度回收权衡，但未达标且纯度差小。投料双耗使第12批事件0120失败，X0计划未实现，空批没有化学意义。

## 修订

v4与K2保留洗涤局部趋势并明确跨阈值预期失败，选择非达标fallback而非宣称成功。反应热强度与溶剂变化混杂，虽K1称热强度最强变量，未获得同材料单因素热对照。

## 后续采用

Q洗涤方向承接局部数据；更突出的外推来自唯一浓缩批1回收0.000758：Q给所有浓缩流程极低回收，Q11不浓缩0.112、仅增浓缩的Q12为0.0045。批1同时是弱反应+萃取+洗涤+干燥，无法隔离浓缩损失。K2直接承认该推断依赖混杂批1。

## 未解决问题及解释限制

本场同时有明确前瞻检验、自然撤回，以及有限经历在Q中取得强解释地位。不能将Q低回收解释成已识别浓缩机制；也不能用有效执行重测证明0.80资格。K2建议补C1S2材料角点未执行。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 41, 'last_event_id': 'runner-operation-0041'}

> Batch 5 will add an equimolar component charge; a large conversion/yield change would support this formulation requirement rather than a catalyst effect.

事件：runner-operation-0047, runner-operation-0050

v3 / cursor {'event_count': 104, 'last_event_id': 'runner-operation-0104'}

> A 0.04 L wash is predicted before batch 11 to cross purity 0.80 with lower recovery.

事件：runner-operation-0119

Q

> The dominant recovery prediction is the 600 s concentration step

K2

> Their assumed severe concentration loss was inferred mainly from confounded batch 1.
