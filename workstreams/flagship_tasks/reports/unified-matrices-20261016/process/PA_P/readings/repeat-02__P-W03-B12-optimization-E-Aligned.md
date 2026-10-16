# 重复上游锚定洗涤反证，更新后的不利洗涤关系进入预测但仍有体积与剂量假设

`repeat-02/P-W03-B12-optimization-E-Aligned`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-02__P-W03-B12-optimization-E-Aligned.json)

## 问题与先验

正确资料指X2，首批较温和，后C1–C3/S0与C1四溶剂在400K3600s形成筛选。v2/cursor113以C1/S2为反应锚点，明确下一步固定反应检验洗量与其他X，洗失败再寻替代。

## 预期与实验

随后C1/S2固定反应，依次无洗、0.01L、0.02L、三次0.04L洗。最后降低350K1800s不洗，并同条件换X0。没有执行v2列出的水相或重复接触备选，不把计划当完成。

## 实际证据

四个400K3600s上游yield0.357/0.369/0.363/0.334、purity0.594–0.631，支持近似稳定反应背景。终态无/小/中/重洗纯度0.699/0.707/0.686/0.430、回收0.129/0.088/0.095/0.017。温和不洗X2得0.760/0.0304、X0得0.742/0.0355，均不合格。

## 修订

v3明确拒绝有用的洗涤纯度/回收权衡，选最高纯度第11批为不达标fallback。K1把上游稳定与后处理严重丢失连接为可见证据，同时保留微观原因未知；低严重度改变温度时间两因子，不能各自分离。

## 后续采用

Q07→08纯度0.66→0.65、回收0.19→0.13，双洗Q09→10亦双降，表明不利洗涤认识实际进入预测，而非机械坚持洗得更纯。Q却继续预期X0较X2更纯，尽管源匹配一次方向相反并不足稳定排除；资料公式把添加水0.012L直接当相体积，没有校准反应溶剂贡献。催化剂20倍缩放也未测。K2承认这些预测脆弱，提出时间序列而未执行。

## 未解决问题及解释限制

本场有完整前瞻洗涤承诺→近重复上游→失败→修订→预测采用，不必以纠错成功收束。体积式和低剂量迁移仍是模型假设；K1将加水与X体积当等体积不能作为已验证相量关系。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 113, 'last_event_id': 'runner-operation-0113'}

> Next test: keep C1/S2 reaction fixed and compare wash intensity and alternative extractants.

v3 / cursor {'event_count': 198, 'last_event_id': 'runner-operation-0198'}

> The expectation that washing would provide a useful purity/recovery tradeoff was not supported

Q

> staged washing is predicted to lose more target because repeated washing was destructive in batch 10.
