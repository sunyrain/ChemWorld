# 未达纯度目标仍形成局部溶剂与工艺认识，单步洗涤解释超出联合处理对照

`repeat-03/P-W03-B12-optimization-E-Opaque`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-03__P-W03-B12-optimization-E-Opaque.json)

## 问题与先验

无先验，以组合筛选寻找纯度≥0.80流程。前四批同时改催化剂、溶剂与严重度，v2/cursor58正确将C1S1优势限定为配方，而非独立催化剂排名。

## 预期与实验

v2提出在C1S1下比较萃取剂与有机保留，检验洗涤能否以回收换纯度。随后X0/X1/X2有机流程及水相二次萃取，再固定C1/350K/7200s比较S0/S2/S3，最后试S2低温长时。

## 实际证据

有机X0/X1/X2最终纯度0.369/0.396/0.436、回收0.048/0.054/0.069；水相C1S1较高但并非纯相选择匹配。S0/S2/S3局部终态纯度0.498/0.572/0.370、回收0.171/0.199/0.109。S2改330K/14400s后0.553/0.191，无合格终态。

## 修订

末笔记和K1拒绝本场已找到可行流程，保留批10为least-infeasible。K1明确后处理转化近1可以来自移除富反应物相，而非反应完全；并列平行副反应与目标降解候选。

## 后续采用

Q把X2优于X0及洗涤损失方向带入新条件；Q07/08纯度0.57→0.50、回收0.153→0.096。该洗涤方向源自洗前HPLC与洗/干燥/浓缩后终检的联合变化，未独立分离洗涤。K2承认低催化剂/低投料迁移及独立浓缩未识别，提出反应时间序列，未执行。

## 未解决问题及解释限制

局部溶剂比较与不可行性承认有实证依据；二次萃取后仍有浓缩和跨测量，不能把全部损失唯一归给第二次萃取。K1详细机制是现象兼容模型，不能提升为已识别反应网络。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 58, 'last_event_id': 'runner-operation-0058'}

> the apparent ranking is therefore a recipe-combination effect, not an ordered material trend.

v3 / cursor {'event_count': 180, 'last_event_id': 'runner-operation-0180'}

> any selected batch is a least-infeasible candidate, not a demonstrated solution.

Q

> Campaign batches 5–7 showed that washing reduced both recovery and apparent purity

K1

> discarding a reactant-rich phase can make the retained phase appear highly converted
