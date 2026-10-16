# 从高转化转向提前终止：形成可行局部方案但阈值稳定性未定

`repeat-01/P-W02-B12-optimization-E-Opaque`

阅读覆盖：同一分析智能体逐版阅读笔记、全部公开操作与测量、K1/Q/K2及既有推荐复测；非独立双人编码。

[完整公开记录](../sessions/repeat-01__P-W02-B12-optimization-E-Opaque.json)

## 问题与先验

无资料时先假设催化剂/溶剂、反应程度及有机保留共同决定纯度回收。初始350K/900s反应转化很低，后续延长时间并寻找材料组合。

## 预期与实验

前十批确定C3/S2/330K的局部反应区，四次7200s前处理HPLC转化0.399—0.435、目标收率0.210—0.244；v2/cursor160由纯度仍不合格明确提出缩短停留以降低杂质，再选择或细化较好点。随后3600s及4200s两批实际检验这一方向。

## 实际证据

同X2后处理下7200s批9终态纯度/回收0.714/0.127；3600s批11为0.823/0.0663；4200s批12为0.8023/0.0814。局部时间取舍有直接对照支持。其推荐选择批12，已有复测为0.7990/0.0831，略低于纯度门槛；retest.passed只代表执行及重放校验通过，不能解释为科学目标合格。

## 修订

v3把短时降低杂质写成局部支持，承认批12只超门槛0.0023，小于纯度噪声0.008。K1区分反应前处理HPLC与分离后近1的conversion，未将后者误读为整个反应完全转化。并行反应和继发降解只是竞争解释，未以局部优化宣布已确定动力学。

## 后续采用

Q以局部时间取舍外推到C1/400K、低催化剂和低投料；对Q07—Q12凭催化剂/反应物比例推更大反应程度，回收点估计0.145—0.21，均承认超出已测浓度。洗涤及浓缩效应多依赖通用近似。K2提出同瓶时间序列辨别并行副反应与目标降解，但未执行。

## 未解决问题及解释限制

K1称批1/2为最干净催化剂比较，实际同时将S0体积0.08降为0.04L，不能视为纯催化剂效应。两次洗涤批8同时用X0，与一次洗涤X1—X3比较也有混杂。正向成果在于同期解释引出有效时间检验和可行局部点，不能据此建立所有催化剂、相量和浓度条件下的模型。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 160, 'last_event_id': 'runner-operation-0160'}

> Test C3/S2 at a shorter hold to trade conversion for composition, use X2 and one wash

事件：runner-operation-0164, runner-operation-0176, runner-operation-0180, runner-operation-0192

v3 / cursor {'event_count': 192, 'last_event_id': 'runner-operation-0192'}

> The margin over 0.80 is small relative to assay noise, so robustness at the threshold remains unresolved.

K2

> the goal favored finding a feasible operating point over identifying a globally reliable mechanism.
