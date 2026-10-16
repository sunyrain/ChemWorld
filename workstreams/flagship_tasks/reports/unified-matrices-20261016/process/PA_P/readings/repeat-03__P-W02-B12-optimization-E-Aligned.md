# 实测筛选引导C3后续研究，洗涤增纯预期被收窄而损失关系保留

`repeat-03/P-W02-B12-optimization-E-Aligned`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-03__P-W02-B12-optimization-E-Aligned.json)

## 问题与先验

资料优先X2；S0固定390K3600s四催化剂筛选后，v2/cursor37选择C3转向溶剂与净化研究。真实C3最佳事件0030，v2笼统列四事件不按催化剂排列。

## 预期与实验

后续C3跨S1/S2/S3筛选，固定C3S2净化及0、0.005、0.04L洗涤；另7200s批改变热时长同时改变洗量，但上游测量仍能考察时间变化。

## 实际证据

C3S2直接终检纯度/回收0.647/0.327；X2无洗0.767/0.166、小洗0.776/0.140、大洗0.762/0.098。7200s上游产率0.429高于3600s约0.31—0.33，但杂质增、纯度降，最终0.588。

## 修订

末笔记与K1/K2明确洗量增大没有建立单调纯度收益，保留回收损失，推荐未达标小洗候选。还清楚区分上游反应与分离后conversion近1，不把后者作全反应完成。

## 后续采用

Q保留长时间可能增加杂质、洗涤损失方向，对新C1S2小投料仍赋予不确定的增纯收益和分段洗优势，承认这些未测。没有直接矛盾，但不能把未测增纯幅度当已建立定律；X2装载资料的近似量级与观察相容也不验证全材料排序。

## 未解决问题及解释限制

C3被筛选后驱动后续材料与净化探索，是清楚的研究自组织轨迹；真实检验导致局部解释收窄。推荐纯度0.776低于0.80，小洗比无洗0.009差需重复；K2时间序列未执行，串联降解机制未确定。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 37, 'last_event_id': 'runner-operation-0037'}

> Decision: use C3 for solvent and workup tests; reconsider only if a solvent interaction reverses ranking.

事件：runner-operation-0042, runner-operation-0049, runner-operation-0056

v3 / cursor {'event_count': 113, 'last_event_id': 'runner-operation-0113'}

> These numerical differences are not firm evidence of a monotone purity benefit

K2

> The clear result was target loss with stronger washing; a reproducible purity benefit remained unresolved.
