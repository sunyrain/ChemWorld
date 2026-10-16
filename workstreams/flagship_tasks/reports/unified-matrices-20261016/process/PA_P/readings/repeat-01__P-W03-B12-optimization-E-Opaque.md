# 低有机回收使探索转向水相，成套后处理差异仍不能唯一归因

`repeat-01/P-W03-B12-optimization-E-Opaque`

阅读覆盖：同一分析智能体阅读全部笔记/差异、公开动作观测、K1/Q/K2及既有推荐复测；非独立双人编码。

[完整公开记录](../sessions/repeat-01__P-W03-B12-optimization-E-Opaque.json)

## 问题与先验

无资料起手假设有机保留可富集目标，并以反应HPLC与终态区分上游和下游。前四批材料、温度、时间、萃取剂和保留相均有变化，属于筛选而非独立因果对照。

## 预期与实验

v2/cursor60注意前两批有机回收0/0.0233，后两批水相回收0.1099/0.0816但不纯，明确改以水相保留进行反应选择性筛选，并预告交叉C1/S1搭档。批5—9实际继续水相路线，得到C1/S2候选；后续批11回试有机路线。

## 实际证据

C1/S2/360K/7200s批8与11上游收率0.3420/0.3511、纯度0.5705/0.5720接近。批8水相终纯度/回收0.6189/0.2563，批11有机加洗涤干燥为0.3468/0.0212。推荐批8明确不合格，已有复测0.6029/0.2679。四洗批12纯度0.0422、回收0，但催化剂和萃取剂也不同。

## 修订

v3承认有机保留的最初期望未在受测流程成立，转为水相保留较优的局部操作判断，并保持没有任何批达0.80的结论。K1正确区分分离后conversion近1和反应前HPLC，未将目标几乎耗尽的有机样品称反应成功。

## 后续采用

Q将全部有机端点回收预测压低（0.006—0.058），并依已有重洗损失，预测洗涤使纯度和回收都降低。X2有机并未直接测，X0较纯又主要取自不同C0/S0、近空样品，迁移依然很强。K2建议同源分样、两相最少后处理以区分真正分配与洗涤/干燥损失，承认当前比较剩余混杂。

## 未解决问题及解释限制

K1把批8/11大部分差异直接归于相选择过强：有机支路同时增加wash和dry，只有整体流程差异得到支持，不能仅凭终态估计DP<1。材料筛选也不足独立识别催化剂×溶剂交互；可支持材料组合的局部差异。其正向链是低回收观察改变研究策略并形成重复上游证据，不要求最终合格才算学习。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 60, 'last_event_id': 'runner-operation-0060'}

> This supports retaining aqueous for screening, but the evidence is confounded by different reaction recipes and extractants.

事件：runner-operation-0074, runner-operation-0088, runner-operation-0102, runner-operation-0116

v3 / cursor {'event_count': 183, 'last_event_id': 'runner-operation-0183'}

> This is a best-available recommendation, not evidence that the purity constraint was satisfied.

K2

> If both aliquots had similar recovery, I would weaken the phase-preference claim and attribute much of the batch 8/11 difference to washing, drying, or independent process variation.
