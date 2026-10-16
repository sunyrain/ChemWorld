# 预告的强化洗涤确实实施，失败后收缩判断却仍作范围外预测

`repeat-01/P-W03-B12-optimization-E-MisIndexed`

阅读覆盖：同一分析智能体阅读完整笔记及修订、全部公开操作测量、K1/Q/K2及已有复测；非独立双人编码。

[完整公开记录](../sessions/repeat-01__P-W03-B12-optimization-E-MisIndexed.json)

## 问题与先验

错配资料赋X0高分配/选择性，初始希望有机保留加洗涤可净化。先在S0低温短时筛催化剂，再在430K/3600s筛C0溶剂和S2催化剂，找到C1/S2高收率区域。

## 预期与实验

v2/cursor132明确以最佳C1/S2反应试X0有机保留加洗涤，预期较水相更纯甚至过0.80，并预告不合格则末批强化洗涤。批11实际单洗0.02L，未合格；批12其他主要步骤相同，变为十次0.04L洗涤。这是前瞻条件决策实际支配后续行动的可定位链。

## 实际证据

C1/S2三次上游纯度0.624/0.625/0.630、收率0.448/0.457/0.436，局部重复较一致。水相批8终态0.6105/0.2628；有机单洗批11为0.6639/0.0999；十洗批12为0.0080/0。洗涤次数和单次量同时改变，支持强化整体流程严重耗损，不识别各自贡献或洗涤定律。

## 修订

v3撤回X0足够净化及更多洗涤单调改善的解释，推荐批8回收导向fallback且明确不满足纯度。已有复测0.5945/0.2744。K1/K2将反应上游重复与终态失败分开，但温度/时长比较还混杂溶剂：低条件全S0，高条件S1—S3，不能仅归因于更热更久。

## 后续采用

Q仍借错配资料将X0排在未测X2之前；对低投料X2查询预估洗涤将纯度0.79升至0.86，两次分段洗至0.90，同时降低回收。这与已见极端X0重洗失败存在范围迁移张力，不是同条件直接矛盾。K2建议匹配批11省去洗涤以区分萃取和洗涤损失，未执行。

## 未解决问题及解释限制

能清楚说明初始资料、局部反应进展及门槛目标如何组织末两批；失败又如何改变公开解释。不能据此宣布模型掌握了普遍洗涤机制或自主研究只能强化错误；它确实撤回充分净化预期，尚未建立的新区域判断仍依一般推断。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 132, 'last_event_id': 'runner-operation-0132'}

> If purity remains below 0.80, intensify washing in the last batch rather than claim a qualifying process.

事件：runner-operation-0147, runner-operation-0159, runner-operation-0168, runner-operation-0171

v3 / cursor {'event_count': 171, 'last_event_id': 'runner-operation-0171'}

> Ten large washes catastrophically depleted target

Q

> A wash is predicted to raise purity but lower recovery (Q08 versus Q07).
