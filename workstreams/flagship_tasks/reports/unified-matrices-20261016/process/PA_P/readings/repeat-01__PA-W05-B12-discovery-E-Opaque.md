# 配对反转和局部重复形成认识，保留相表述随后被证据纠正

`repeat-01/PA-W05-B12-discovery-E-Opaque`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-01__PA-W05-B12-discovery-E-Opaque.json)

## 问题与先验

无资料，以配对、相量及混合假说组织12批，每批另加0.02mol reagent。首批仅加有机相未加萃取剂，模型后续正确区分它与X0批，不当成同条件重复。

## 预期与实验

v2/cursor70从S0与S1的X0/X1反向效应形成配对假说，预告低高相量、弱强混合及末批标准重复。事件71—120完成这些检验；全部分离均保留有机，未直接终检水相。

## 实际证据

X0→X1在S0有机0.187→0.287、S1为0.326→0.262。S1/X0标准重复0.326/0.342，低高相比例0.078/0.494对应有机0.102/0.475，弱混合0.314、强0.459。强混合超过标准重复差异，而弱与标准差异未分辨；每次HPLC水相仍高于有机。

## 修订

v3限制恒分配系数、拒绝已示平台，保留慢传质与分散/沉降等候选。但同版末尾却写为目标回收应retain organic，与已测水相更多不符。K1改为保留预测目标库存较多的一相，并明确有机被测不等于已证明有机最大回收；Q的D1正确选aqueous。

## 后续采用

Q将D2答为uncertain，理由是S0/X3未测且已有配对反转；具体点预测仍外推未测配对。Q09→10有机0.19→0.15，与唯一测过的S1/X0延长混合正效应方向不同；K2明确承认缺乏S0下该方向证据。同时识别全部源批有reagent而问卷无reagent这一额外迁移假定。

## 未解决问题及解释限制

该场有真实交叉与重复支撑的关系，也展示笔记结尾、最终解释和决策并非同一认识读数。不能将v3错误持续到K1/Q，亦不能把一个配对的混合方向扩为全部配对规律。水相优势依据HPLC而非水相终检，候选辨别实验仅建议未执行。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 70, 'last_event_id': 'runner-operation-0070'}

> Reserve the final batch as a standard-condition repeat to assess repeatability.

事件：runner-operation-0117

v3 / cursor {'event_count': 120, 'last_event_id': 'runner-operation-0120'}

> retain organic when the goal is target recovery.

K1

> the directly supported rule is to retain whichever phase has the larger predicted target inventory, not automatically the organic phase.

K2

> All campaign batches also contained 0.02 mol reagent, whereas the prediction batches did not
