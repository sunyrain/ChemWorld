# 前瞻重复巩固单因素材料关系，未做交叉检验的相加模型仍进入预测

`repeat-02/PA-W01-B12-discovery-E-Opaque`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-02__PA-W01-B12-discovery-E-Opaque.json)

## 问题与先验

无资料，以S0/X0为中心分别变萃取剂与溶剂，提出材料、相量及混合假说；每批额外加0.03mol reagent。七点星形设计能比较局部效应而无法识别完整交互。

## 预期与实验

v2/cursor70预告重复高有机S0/X3和S3/X0，若偏差大则考虑过程波动；另预告S0/X3相量及10s/100rpm低混合。后五批按计划执行，S0/X3重复还改为保留水相以检验分离语义。

## 实际证据

S0/X3两次HPLC有机0.467/0.453，S3/X0为0.429/0.436，支持局部重复。S0/X3低/标准/高相量有机0.307/约0.460/0.811，表观D约3.50/3.71—3.99/2.60。低混合0.381低于标准重复，时长与速度混杂。水相终检0.575与此前0.524大致相符但非严格闭合。

## 修订

v3明确未测交互不能按指数或相加推断，恒D全范围不足，四点直线拟合仅描述而未验证；把混合趋势保留为未辨别的传质或其他状态变化。真实重复提高了局部判断可信度，并未解决未测组合。

## 后续采用

Q的D2 Q06由S0下X3高于X0实测支持，但未测S2/X3仍预测有机0.69—0.72，借独立材料效应相加。K2直接承认separable extrapolation未建立，并建议按Q08条件直接测该配对，未执行。

## 未解决问题及解释限制

不能把读到边界就等同数值预测遵守边界，也不应抹去有效重复的正向作用。物料初始额外reagent及配方变化也属于迁移条件；本场K2未主动讨论该项，不补写它已识别。无强混合端或独立时速实验，平台没有证据。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 70, 'last_event_id': 'runner-operation-0070'}

> repeats of S0/X3 and S3/X0 should remain among the higher organic fractions

事件：runner-operation-0077, runner-operation-0087

v3 / cursor {'event_count': 120, 'last_event_id': 'runner-operation-0120'}

> untested pair interactions cannot be predicted from index or assumed additivity.

K2

> That simplification was useful for producing points but is more restrictive than the evidence justified
