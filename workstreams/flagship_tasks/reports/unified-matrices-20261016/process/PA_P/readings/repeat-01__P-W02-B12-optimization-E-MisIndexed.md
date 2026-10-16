# 流程语义纠正与化学局部认识并行，未测资料仍参与外推

`repeat-01/P-W02-B12-optimization-E-MisIndexed`

阅读覆盖：同一分析智能体完整阅读笔记与修订差异、全部公开事件、K1/Q/K2及已有推荐复测；非人类独立编码。

[完整公开记录](../sessions/repeat-01__P-W02-B12-optimization-E-MisIndexed.json)

## 问题与先验

错配资料引导X0高回收/高选择性起手，计划以反应HPLC区分上游不足和后处理损失。第一批双加试剂和component，后续调整为约0.036364mol，以保留全12批机会。

## 预期与实验

v2/cursor100在S0共同390K/7200s催化剂筛选后选C3，看到X0单洗仍不能达纯度门槛，明确下一步转向S1—S3而非单纯继续洗涤。后续确实进行溶剂切片，再尝试X1双洗、较低温度和小X0体积。小相量会提高纯度的预期只在K1/K2事后讲出，不能当作同期承诺。

## 实际证据

C0/C1/C2/C3的反应收率约0.184/0.254/0.136/0.299，C3虽转化非最高却选择性最高。C3/S2批8收率0.460、终纯度/回收0.7187/0.1501。小X0体积批12终态0.4675/0.0473，未提高纯度；X1双洗0.6377/0.1008也未达标。推荐仍为不合格批8，已有复测0.7027/0.1617。

## 修订

v2区分第二批操作失败与化学证据：事件24浓缩无相系统被拒，26加萃取剂超体积，选不存在有机相后无样品；补0.001L有机液后获得空白式终检不能解释为该反应本身无产物。第三批起先建水相再浓缩，实际顺序修正早于v2记录，故有操作改变但不能声称v2前瞻推动该修复。v3承认没有任何合格流程且不再保证局部分配锚点可迁移。

## 后续采用

Q仍凭错配资料把未测X2排在X0之后，Q03X0纯度/回收0.76/0.041，高于Q04X2 0.72/0.035；小X2相体积仍预估较纯。后者与X0小相量失败构成未解决迁移问题，因材料不同不能直接称逻辑矛盾。K2列出未测催化剂浓度、C1/S2及X2等来源，提出催化剂阶跃实验但未执行。

## 未解决问题及解释限制

本场同时建立了活性与选择性的局部区分、修正可执行流程、诚实降级推荐，却保留未经本地比较的资料排序。混杂洗涤和温度不能唯一解释下游失败；操作契约学习与化学机制识别必须分别叙述。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 100, 'last_event_id': 'runner-operation-0100'}

> Reaction-solvent screening is now preferred over assuming more washing alone will solve selectivity.

事件：runner-operation-0105, runner-operation-0121, runner-operation-0137

v3 / cursor {'event_count': 198, 'last_event_id': 'runner-operation-0198'}

> I will recommend batch 8 while explicitly noting that it misses the purity specification

Q

> X0 is predicted to outperform X2 modestly, consistent with its higher nominal product partition coefficient and selectivity.
