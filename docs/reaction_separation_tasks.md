# 反应与分离任务

本页描述反应和后处理耦合任务。它们是 ChemWorld 区分普通 reaction optimization toy
environment 和完整 chemical world model gym 的关键。

## 反应到纯化

该任务要求 agent 先完成反应，再进行萃取、洗涤、干燥、浓缩或终点评测。评分通常同时
考虑产率、纯度、成本和安全。

典型路线：

1. 加 solvent、reagent、catalyst。
2. 加热或搅拌推进反应。
3. `terminate` 结束反应阶段。
4. 加 extractant 并混合、静置、分相。
5. 选择目标相并进行 wash、dry、concentrate。
6. 使用 `final_assay` 测量并触发最终评分。

## 分配发现

该任务强调 agent 通过有限测量学习物质在不同相之间的分配规律。它适合测试 exploration、
active learning 和 instrument cost tradeoff。

## 纯度-产率权衡

该任务要求 agent 在纯度和回收率之间做取舍。过度纯化可能降低产率，过少后处理可能
导致 impurity penalty。

## 为什么重要

真实化学工作流往往不是“反应结束即成功”。agent 需要理解反应、相行为、分离、测量和
成本之间的耦合。ChemWorld 应优先把这些耦合做成可交互任务。
