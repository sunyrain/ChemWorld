# 识别共享库存失败并排除空批，却低估了最佳材料比较的投料混杂

`repeat-03/P-W01-B12-optimization-E-Opaque`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-03__P-W01-B12-optimization-E-Opaque.json)

## 问题与先验

无资料，初始假设温和热处理与选择性洗涤可改善结果，先类别筛选再复制。首批无X造成分相与洗涤拒绝；后续每批reagent和component各0.04mol，实际共用库存。

## 预期与实验

没有中期化学计划笔记直到cursor135，此时七次有效终检后原料已耗尽。v2正确将后续空批视为资源混杂，暂停机制判断；v3结束于12闭批、7终检和5丢弃。

## 实际证据

C2/S0、S1、S2上游纯度0.470/0.352/0.568，最后C2S2终检纯度0.774、回收0.0595，被选为未达标的最佳候选。但事件0102第二份0.04mol component被拒绝，故C2S2总投料0.04与先前0.08不同，不能只作材料效应比较。

## 修订

笔记/K1明确add_component不是额外独立共反应物，正确识别共享库存；K1区分上游反应conversion与下游近1的conversion，避免把分离当完成反应。正向局部认识是净化常提高纯度但损失回收。

## 后续采用

Q把X2优于X0及分段洗更有效用于未测C1S2和低催化剂/小投料条件，并明确未控制的进料与X混杂、宽区间非拟合方差。K2提出固定C1S1降低热强度以区分类别与热暴露，未执行。

## 未解决问题及解释限制

K1/K2将C2S2优势视为材料交互，遗漏投料减半的实际影响；仅单一催化剂跨溶剂也不足识别不可加交互。无达标候选，推荐重测成功不代表达标。五空批是资源/操作失败，不是化学负结果。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 135, 'last_event_id': 'runner-operation-0135'}

> Do not interpret them as negative reaction evidence.

v3 / cursor {'event_count': 148, 'last_event_id': 'runner-operation-0148'}

> This is a best-available, noncompliant recommendation, not evidence that the research goal was fully met.

K1

> This result formed the main basis for believing that C2/S2 is a favorable interaction rather than C2 being universally superior.
