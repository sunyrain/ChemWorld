# 从错配边际提示进入实测配对和局部定律，未测配对决策保留不确定性

`repeat-02/PA-W04-B12-discovery-E-MisIndexed`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-02__PA-W04-B12-discovery-E-MisIndexed.json)

## 问题与先验

v1受S2与X0有利的错配资料启发，但明确允许配对筛选推翻边际排序。S2四X得到0.503、0.568、0.493、0.615，v2/cursor40改为交互或错配候选，并事前要求固定X0比较溶剂。

## 预期与实验

后续S0/S1/S3-X0份额0.413/0.572/0.618，重复S2/X0为0.517，支持类别差异；相量低/高使目标由0.354有机、0.628水相转至0.808有机、0.203水相。v3/cursor100预言若标准混合已足够则加强后应接近基线；最后弱/强混合为0.431/0.623，而基线重复0.503/0.517，未支持标准条件已充分。

## 实际证据

低相量及两基线表观D约5.2–5.5，高相量仅2.55；高相量还改变溶剂/萃取剂组成并增加杂质，不能把偏离唯一归因于饱和。实际分相操作依据HPLC更大库存改变：S2/X2、S0/X0、低相量、弱混合都留水相，其余留有机相，终测大体保留对应库存。

## 修订

四次笔记给出清晰连续转变：资料线索→配对反例→固定X0溶剂检验→局部D及高相量失效→混合平台未识别。v4把混合标为联合效应，避免把D称为全局常数。即使错配信息存在，实测仍产生了可用的局部认识及保留行为。

## 后续采用

Q保留相量与混合方向，D1选水相，D2明确uncertain；但点估计仍将未测S0/X0优于S0/X3，借用与S2实测相反的边际排序。K2指出点排序支持弱，也承认有限体积插值超出已支持的r<约0.2范围。宽区间和uncertain是部分校准，不能等同于点值已被证实。

## 未解决问题及解释限制

单点配对、相量与混合测试不识别全部交互或动力学；局部D约5.2–5.5也受相率测量误差影响。K2提出固定组成减半目标负载来区别负载与组成原因，既未执行，也未从本记录建立该操作能改变固定初始目标库存的实现性，不能作已完成鉴别证据。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 40, 'last_event_id': 'runner-operation-0040'}

> Prediction before solvent contrast: holding X0 and process fixed, solvent identity can shift the split by a similarly meaningful amount.

事件：runner-operation-0047, runner-operation-0057, runner-operation-0067

v3 / cursor {'event_count': 100, 'last_event_id': 'runner-operation-0100'}

> if 300 s/600 rpm is already adequate, a much stronger mix should resemble baseline within combined variability

事件：runner-operation-0117

Q

> Q05 versus Q06 remains uncertain because S0/X3 was not measured
