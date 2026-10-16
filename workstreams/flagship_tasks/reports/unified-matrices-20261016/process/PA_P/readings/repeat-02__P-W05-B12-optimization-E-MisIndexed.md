# 洗涤失败确实修订后续预测，末批空样却被事后解释为控制运行导致物料消失

`repeat-02/P-W05-B12-optimization-E-MisIndexed`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-02__P-W05-B12-optimization-E-MisIndexed.json)

## 问题与先验

错配资料指向X0，全场只用X0；起始计划以匹配X比较反驳先验，但实际没有比较其他X。第4批额外0.04 mol component与11批普通加料共同消耗0.48 mol，导致第12批一开始就不能加入试剂。

## 预期与实验

高条件430 K/7200 s的S1四催化剂上游支持C1较好；C1改S2上游纯度/回收0.608/0.485，高于S1的0.394/0.303及S3的0.410/0.270。第9/11批C1/S2上游HPLC0.608/0.485与0.599/0.467接近，处理唯一实质差异为两次0.010 L洗涤，终纯度/回收0.592/0.235降为0.510/0.132。

## 实际证据

匹配洗涤对照同时降低纯度与回收，具有超过测量噪声的局部支持；它不识别传质、选择损失或其他处理机制。第1批纯度0.816回收零，按阈值被推荐，但末笔记/K1明确没有满意隔离流程。第146事件明确stock_limit拒绝第12批加料，第150事件热处理即因has_material被拒，后第151空样HPLC为近零；之后才出现大量控制器调试。

## 修订

末笔记否定X0资料可靠保证完整反应混合物富集、否定洗涤改善该流程。K1对第12批却提出过长加热、控制器误用或完全分解造成空样，遗漏加料被拒在先的明确原因；空样不是经历长控制后才出现。K2虽排除其化学比较价值，也未修复该解释错误。只有首末笔记，不能把K1的转变叙述视作全部同期证据。

## 后续采用

Q确实保留洗涤损害纯度/回收的局部发现：Q07→08由0.61/0.120降到0.55/0.058，理由明说依据研究而非理想分配模型；分次洗仍预测更多损失。另一方面Q保留未验证X0优于X2，且把未独立测试的浓缩视为损失/降解风险，属于新迁移假设。

## 未解决问题及解释限制

11次有效终测和1次物料耗尽弃置必须同时计入；不是12次完成的化学实验，也不是氮气使目标消失。可用作同场正向修订与错误原因赋予并存案例：洗涤修订有匹配观测，控制失败的化学候选则与操作先后冲突。后者应由公开ledger核对，而不是仅照抄笔记。

## 已核验引文与事件锚点

Q

> based on the campaign rather than ideal partition theory, slightly reduce purity.

K1

> Plausible causes include excessive cumulative controlled heating, controller-stage misuse, or complete destruction/depletion of the assayable solute pool.

v2 / cursor {'event_count': 215, 'last_event_id': 'runner-operation-0215'}

> Batch 12 was discarded

事件：runner-operation-0146, runner-operation-0150, runner-operation-0215
