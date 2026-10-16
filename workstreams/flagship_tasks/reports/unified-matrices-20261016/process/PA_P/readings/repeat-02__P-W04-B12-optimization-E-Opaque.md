# 六批有效研究建立局部催化剂与萃取剂对照，资源误配使其余六批不能回答化学问题

`repeat-02/P-W04-B12-optimization-E-Opaque`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-02__P-W04-B12-optimization-E-Opaque.json)

## 问题与先验

无物性资料。v1预期完整加料、热处理及萃洗可能达到0.80纯度。实际每批add_reagent和add_component各0.04 mol共同扣除共享库存，六批即耗尽0.48 mol；不是模型调用或仪器故障。仅起始与最终两次笔记，不能从终稿叙述还原未记录的逐次内部判断。

## 预期与实验

首批0.08 L溶剂与0.02 L水后仅加入0.0002 L X0即分相，之后才加0.04 L X0，终测纯度0.014、回收0；其异常相几何不能当标准X0性质。第2与5批上游均C1/S0、360 K/7200 s，HPLC产率0.1986/0.1985近重复；下游X0与X3分别纯度0.202/0.393、回收0.0178/0.0363，支持该流程中X3更好。

## 实际证据

C2、C3同上游条件HPLC产率0.0877/0.1187低于C1，形成局部催化剂对照，尽管其末端X类别同时改变。第6批改S1并三次洗涤，反应产率升至0.252，终纯度/回收降至0.188/0.0179；洗涤与溶剂混杂，不能从中独立确定洗次因果效应。第100–101事件拒绝加料；其后空样加溶剂、反复取样、极小补料尝试及仪器请求均不提供新反应结果，最终只有6次有效终测。

## 修订

v2/cursor171与K1/K2明确撤回流程能达标的预期、排除耗尽后零读数对S2/S3的解释，并区分相内近一转化与反应真正转化。这是认识修订和操作边界识别；不是完成12次有效化学比较。K1把干燥影响小等解释说得比其分阶段证据更强，应保留未拆分。

## 后续采用

推荐不合格第5批并明确只是最好观察；Q却对未有效研究的S2、400 K、低催化剂、小投料、浓缩给出回收0.16–0.46，远高于源流程。理由承认大幅外推，但仍假设稀释减少杂质及洗涤提高纯度；洗涤方向并非六批数据已建立。K2进一步列出薄弱预测，并提出双相物料衡算以区分分配损失、分解与报告器差异。

## 未解决问题及解释限制

不能把空样字符化视作新增化学负对照，尽管K2称其operational negative controls；这不是预先设计的化学对照。资源选择实际限制了可获得证据，保留下来的正向局部比较也不能消除未达标或迁移未验证。独立温度/时间规律、洗损原因及S2/S3效应均未识别。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 171, 'last_event_id': 'runner-operation-0171'}

> This is a design failure, not evidence that those categories are chemically inactive.

事件：runner-operation-0100, runner-operation-0171

K1

> The nearly identical yields support reproducibility of target formation

事件：runner-operation-0023, runner-operation-0071

Q

> For the dilute 0.002 mol recipes, I expect fewer concentration-driven impurities and therefore higher purity, although this is conjectural.
