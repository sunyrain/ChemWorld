# 中途把空样当S3无反应，后续纠正并保留有效局部筛选

`repeat-03/P-W03-B12-optimization-E-Aligned`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-03__P-W03-B12-optimization-E-Aligned.json)

## 问题与先验

资料使X2成为分离候选；每批双加0.04mol reagent/component耗共同库存，六批后0.48mol用尽。前六批仍形成固定S0催化剂与固定C1溶剂比较。

## 预期与实验

v2/cursor73称S3几乎无反应，并计划更强热暴露及把X2用于C1S2；但S3首次加料0065/0066已被库存拒绝，0069热处理也拒绝。随后400K/330K及完整后处理尝试都在同一未闭合空生命周期，至0145才弃置。

## 实际证据

C1/C2/C3在S0转换约0.297/0.285/0.271，产率0.155/0.056/0.101，支持局部分支差异。C1S2终态纯度0.606/回收0.230；首C0X2完整处理纯度0.704但回收0。共6有效终检、6弃置，无合格流程。

## 修订

v3、K1和K2明确把S3及后期温度试验排除为无投料记录，不再把空样解释成材料效应；先前v2的错误没有持续到封存结论。K1区分上游与相选择后转化，并承认component化学角色未识别。

## 后续采用

Q仍凭资料和一般关系给全12题纯度0.82—0.94、回收0.36—0.67，高于本场已见结果，且承认400K、低催化剂、去component和低投料未测。K2将绝对预测列为最弱，保留X2及洗涤方向为先验外推，未称已直接验证。

## 未解决问题及解释限制

数字大幅迁移不自动等于错误，需参考真值；可确定的是其经验支持仅覆盖六批及一个混杂后处理。正向结果为失误后排除无效证据、局部选择性认识和不宣称达标。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 73, 'last_event_id': 'runner-operation-0073'}

> S3 showed essentially no reaction in the preceding HPLC

v3 / cursor {'event_count': 162, 'last_event_id': 'runner-operation-0162'}

> Those control/discard events do not provide reaction evidence.

K1

> S3 was not validly screened

Q

> the queried 400 K conditions, much lower catalyst loading, omission of the added component, and 0.002 mol charge regime were not validly studied
