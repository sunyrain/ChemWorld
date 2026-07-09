# Benchmark 协议

本协议定义 ChemWorld 任务如何拆分、提交、评分和发布。

## 数据划分

- `train`：公开任务和公开 scenario，用于开发 agent。
- `validation`：公开但固定的检查集，用于调参和报告。
- `private_eval`：隐藏 scenario 或隐藏任务切片，用于 leaderboard。

所有 split 共享同一个 `world_law_id`，但隐藏参数和评分 seed 不应泄露。

## 提交要求

提交包应包含 agent 入口、依赖、配置和 manifest。评测端负责创建环境、运行 episode、
保存 trajectory 并计算分数。

提交包不得：

- 读取 hidden scenario；
- 根据文件名或 seed 表作弊；
- 写入评测目录以外的位置；
- 访问未授权网络资源；
- 修改环境代码。

## 基础记录

每次评测都应记录：

- ChemWorld commit；
- Python 和依赖版本；
- `task_id`；
- `world_law_id`；
- task maturity；
- seed；
- scenario id；
- scoring protocol version；
- agent manifest。

## 指标

指标应按任务声明，常见维度包括：

- yield；
- purity；
- selectivity；
- information gain；
- mechanism accuracy；
- safety penalty；
- cost penalty；
- invalid-action penalty；
- sample efficiency。

总分可以是加权组合，但每个子指标都应单独报告，便于诊断。

## Agent-Facing 指标

除最终性能外，agent 交互质量也需要记录：

- invalid action rate；
- precondition failure recovery；
- final assay count；
- best-so-far AUC；
- cost-aware score；
- observation-use summary；
- instrument-use summary；
- 是否使用 validator 或 action affordance。

trajectory 可选记录 `agent_view` 和 `agent_trace`。`agent_view` 是环境公开视图，包含 RL vector、tool JSON 和 lab report；`agent_trace` 是 agent 行为摘要，包含 prompt input、selected action、validator result、observation summary 和 hypothesis note。

## 发布产物

正式 release 应包含：

- 文档站；
- 任务卡；
- baseline 表；
- trajectory 示例；
- self-consistency audit；
- release checklist；
- paper artifact 说明。
