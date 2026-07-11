# 任务分类

任务分类用于组织 ChemWorld 的能力覆盖，而不是替代 registry。它帮助读者理解某个任务
主要考察什么能力。

## 当前任务家族

- 反应优化：条件搜索、产率、选择性和成本。
- 安全约束控制：在限制内完成目标。
- 机理解释：从观测和结果推断合理机制。
- 表征规划：选择仪器和测量顺序。
- 反应-纯化闭环：把反应、相分离和终点评测连起来。
- 分配发现：学习相间分配规律。
- 结晶和蒸馏：下游单元操作。
- 连续流和电化学：不同实验 affordance。
- Tool-agent planning：调用工具、检查约束和组合 recipe。

## 扩展原则

新增任务必须回答：

- 属于哪个能力家族；
- 是否共享现有 `world_law_id`；
- 哪些 observation 对 agent 可见；
- 评分指标是什么；
- 物理成熟度是什么；
- 是否需要新的 operation 或 instrument contract。

新任务注册后默认只是可运行切片。若要进入后续 research suite，还必须通过指标可执行性、
无正式 proxy、seed 深度、world-family 泛化、baseline、回放证据和反作弊门禁。当前准入状态见
[科学状态页](benchmark_release.md)。
