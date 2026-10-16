# 有效反应筛选引导后续实验，未检验的萃取先验仍进入迁移

`repeat-03/P-W05-B12-optimization-E-MisIndexed`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-03__P-W05-B12-optimization-E-MisIndexed.json)

## 问题与先验

资料使X0成为唯一萃取剂；v2/cursor117明确说未比较所以未确认。初始计划要求后期完整重复，但实际没有重复最终推荐流程。

## 预期与实验

批5–7同C1、390K、3600s和相同总投料的S1/S2/S3比较得到上游纯度0.482/0.642/0.485、回收0.240/0.324/0.201。v2明确据此将后续聚焦S2催化剂及后处理，随后批8–10确实比较C0/C2/C3，批11–12回到C1。

## 实际证据

后段C1上游纯度0.669/0.674、回收0.336/0.336，支持该局部区域，但与批6投料略有不同（总0.0368对0.036mol），不是三次精确重复。批11/12同上游及0.04L洗，仅X0量0.018→0.012L，终态纯度0.749→0.675、回收0.0695→0.0480。批6对11改变洗量也略改投料，不能称严格单变量。

## 修订

v3不把近阈值0.797当达标，并选早期批2的纯度0.848/回收0.00770，区分最佳上游线索与实际可行完整流程。v3/K2承认X0优先只是资料引导；K2撤回洗得更多或相量更小必提高纯度的简单关系。

## 后续采用

Q仍按错配资料计算X0优于X2的分配比例，尽管X2从未使用；新的低浓度区间又假设洗涤提高纯度、分次洗更选择性。宽区间和明确未检验说明保留，但并不使这些点预测成为已建立关系。K2提出同样品洗前洗后测量以定位损失，尚未执行。

## 未解决问题及解释限制

批1实际同时加0.04mol reagent与0.04mol component，故v2泛称早期350K均只add_reagent不准确；K1后来明确例外。不同加料命令的化学角色未由本场识别，不能把拆分加料当已确立新反应物机制。全部测量位置支持反应和完整流程分开解释；无下游中间测量限制损失定位。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 117, 'last_event_id': 'runner-operation-0117'}

> The next tests will screen other catalysts in S2 and then trade extraction/wash severity against recovery.

v3 / cursor {'event_count': 202, 'last_event_id': 'runner-operation-0202'}

> It is therefore a prior-guided choice, not an experimentally isolated extractant effect.

K1

> C1/S2 is the best reaction hypothesis, whereas batch 2 is the best demonstrated constraint-respecting complete process.

Q

> Thus Q03 is predicted to have greater recovery and somewhat greater purity than Q04.

K2

> no extractant comparison.
