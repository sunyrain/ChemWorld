# 从催化剂溶剂筛选到时间和洗涤局部关系，形成接近门槛的有效推荐

`repeat-01/P-W05-B12-optimization-E-Aligned`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2，读取已有推荐复测；非独立双人编码。

[完整公开记录](../sessions/repeat-01__P-W05-B12-optimization-E-Aligned.json)

## 问题与先验

Aligned资料使X2成为主要工作萃取剂，提出温时内点最优与洗涤提纯预期。固定S0、370K/7200s比较C1/C2/C3，再固定C1比较四溶剂；C0温时不同被明确剔除于干净排名。

## 预期与实验

v2/cursor95依据C1/S2最高上游产率/选择性转向其温时变化并保持X2，预告低温若改善选择性可接受转化损失；后五批依次低温、缩时和小洗涤。340K/7200s未明显改善选择性，随后370K缩时更有效，形成由研究证据调整探索维度的过程。

## 实际证据

C1/S2在370K/7200s上游产率0.392、选择性0.582；340K同时间为0.304/0.576。370K/3600s三批选择性0.609—0.631，3000s0.674。无洗、0.010L洗、0.005L洗同3600s终态纯度/回收0.784/0.128、0.807/0.091、0.804/0.093；3000s无洗0.8038/0.103。

## 修订

v3及K1限定温度内点最优未建立，提出缩短时间减少副产物或后继损失、适度洗涤以回收换纯度。承认同反应HPLC波动使洗涤数值效果非精确因果估计；没有声称唯一降解机制。选最高观察合格回收batch12，注明纯度裕度小于噪声。既有复测0.80042/0.10472，仍勉强合格。

## 后续采用

Q采用低催化剂、低投料及新相量的机制外推，X0比X2更纯更低回收仍无匹配证据。K2准确指出Q01—06催化剂比例比源场低16倍，并将400K、低浓度及多次洗涤列为未检验条件；提出同器皿时间序列分开并行生成和后继损失，未执行。

## 未解决问题及解释限制

这是观察—定向探索—有用局部关系—推荐的正向过程，结果接近门槛不取消真实进展。单场不能证明资料使其因果上更善研究；其选择性机制仍存在未解决替代解释，局部成功也未使后测所有外推得到支持。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 95, 'last_event_id': 'runner-operation-0095'}

> Use C1/S2 and vary temperature/time to seek higher reaction selectivity, retaining a consistent X2 contact for comparison.

事件：runner-operation-0100, runner-operation-0113, runner-operation-0154

K1

> lowering temperature reduced conversion and yield but did not clearly improve reaction-stage selectivity.

v3 / cursor {'event_count': 162, 'last_event_id': 'runner-operation-0162'}

> Purity is only narrowly above 0.80 relative to the declared assay noise (0.008)
