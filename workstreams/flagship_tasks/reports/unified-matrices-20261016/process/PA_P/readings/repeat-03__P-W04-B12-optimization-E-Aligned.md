# 小洗量前瞻预测跨过纯度门槛，随后的重复选择响应双目标结果

`repeat-03/P-W04-B12-optimization-E-Aligned`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-03__P-W04-B12-optimization-E-Aligned.json)

## 问题与先验

X2资料引导全场唯一萃取剂，固定360K/1800s先催化剂再溶剂。v2/cursor64把C1的合格回收优势转成下一步溶剂筛选。

## 预期与实验

v3/cursor158预测高有机批10加0.005L洗可使纯度跨0.80；若且回收超过0.0479则复验该洗涤流程。后批11确实执行，纯度0.8013达门槛但回收0.0441未胜，末批回到较好无洗批9并重复。

## 实际证据

同相量批8有0.02L洗和批9无洗，纯度/回收0.863/0.0177对0.814/0.0479；不是v3所说同时增加相量。更高有机无洗批10为0.789/0.0562，加小洗批11为0.801/0.0441。批9重复纯度0.8149、回收0.0368。

## 修订

末笔记及K1/K2明确两次无洗流程均达纯度门槛而回收有变动，推荐最高观察值但不称精确最优。小洗资格极贴近噪声，K2不将其称稳健；相量改变与反应溶剂体积仍混杂。

## 后续采用

Q07/08纯度0.775→0.867、回收0.047→0.009沿实测洗涤方向；未测X0、400K、低催化剂、分段洗涤的量化外推均列为不确定。K2提出共同进料分样的洗涤对照，未执行。

## 未解决问题及解释限制

这是目标—局部关系—具体阈值预期—结果—选择重复的连续正向案例，不能以绝对回收低抹去。正确资料未在此得到萃取剂排名验证，X2全部成功仅支持该流程局部可行。

## 已核验引文与事件锚点

v3 / cursor {'event_count': 158, 'last_event_id': 'runner-operation-0158'}

> a small 0.005 L wash should remove enough impurity to cross purity 0.80

v3 / cursor {'event_count': 158, 'last_event_id': 'runner-operation-0158'}

> if it passes with recovery above 0.0479, replicate it in batch 12.

v4 / cursor {'event_count': 189, 'last_event_id': 'runner-operation-0189'}

> Batch 12 supplies partial reproducibility support for qualification but lower recovery.

K2

> X0, X1, and X3 were never used
