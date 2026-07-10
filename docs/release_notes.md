# 发布说明

## ChemWorld-Bench 0.2.0

本版本冻结 `chemworld-physical-chemistry-v0.3`、`chemworld-task-contract-0.5` 和
`chemworld-serious-v1`。改变任务转移、观测、评分或 seed 的后续修改必须提升合同版本；旧轨迹
不会被静默解释为新结果。

### Serious benchmark

- 六个正式任务统一采用 campaign 语义和 5 个冻结 seeds；
- 结晶与蒸馏任务允许 Agent 在一次实验后使用反馈选择后续实验；
- random、LHS、GP-BO 与 safe GP-BO 使用六类 task-aware 搜索空间；
- 分配任务从隐藏世界生成非零产物/杂质进料，不再对零产物和仪器噪声评分；
- 水相平衡任务的隐藏 pKa/Ksp 随世界变化，表征质量对实验组成有可测响应；
- 自动经验门禁检查合法动作、多轮实验、acquisition、策略区分、primary metric 灵敏度和成功
  阈值校准。

### 科学边界

本版本评估虚拟环境中的实验决策和主动探索，不预测真实反应产率。结晶、连续流和相接触使用
专业候选轻量模型；反应与合成仪器仍保持公开的 `lite` 边界。干燥、浓缩和转移 proxy 任务不
进入 serious suite。

### 复现与完整性

正式证据包括 5-seed baseline、响应面/近似上界审计、冻结任务合同、轨迹 replay、solver
provenance 和 wheel smoke。`python scripts/check_frozen_benchmark.py` 会拒绝缺少证据或合同
hash 已漂移的安装。
