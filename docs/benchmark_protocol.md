# Benchmark 协议

本协议定义 ChemWorld 任务如何拆分、提交、评分和发布。

## 数据划分

- `train`：公开任务和公开 scenario，用于开发 agent。
- `validation`：公开但固定的检查集，用于调参和报告。
- `private_eval`：隐藏 scenario 或隐藏任务切片，用于 leaderboard。

所有 split 共享同一个 `world_law_id`，但隐藏参数和评分 seed 不应泄露。

## Seed Suite

正式报告必须声明使用哪一组 seed。预发布阶段的官方 seed suite 可由 CLI 查询：

```bash
chemworld seeds show
```

核心规则：

- `public-dev` seeds 可公开用于教学、调试和 smoke test；
- `public-test` seeds 公开且冻结，用于 baseline 表和外部复现实验；
- `private-eval` hidden seeds 和 salt 由维护者控制；
- 没有 `CHEMWORLD_PRIVATE_EVAL_SALT` 时，`private-eval` 只代表本地 placeholder；
- `chemworld suite --task ...` 和 `chemworld baselines report --tasks ...` 默认读取
  official seed suite；
- 显式 `--seeds` 是 smoke/debug override，不能冒充完整官方结果。

详见 [Official Seed Suite](seed_suite.md)。

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

## Golden Trajectory 合同

预发布阶段冻结三项核心任务的 scripted golden trajectory：

- `reaction-to-assay`
- `reaction-to-purification`
- `partition-discovery`

对应 fixture 位于 `tests/fixtures/golden/pre_release_scripted_trajectories.json`。它锁定：

- action sequence；
- public observation summary；
- reward 和 final metrics；
- transaction status；
- kernel id/version；
- affected ledgers；
- world event 和 state patch summary；
- final assay 输出。

测试会重新运行 `scripted_chemistry`，重算 summary，并与 fixture 做容差比较。只有当
task/runtime/scoring contract 被有意修改时，才应运行：

```bash
python scripts/update_golden_trajectories.py
```

更新后必须审查 fixture diff，确认变化是预期行为，而不是无意 drift。

## Scoring Contract Audit

预发布核心任务必须通过 scoring contract audit。审计入口是
`chemworld.eval.audit_scoring_contract(records)`，它会重新计算并核对：

- `obs["score"]` 是否符合当前 task scoring contract；
- `reward` 和 `observed_reward` 是否与公开 observation score 一致；
- final assay step 的 `leaderboard_score` 是否等于重新计算的 contract score；
- 非 final assay step 是否没有暴露 `leaderboard_score`；
- `processed_estimate` 中的公开指标是否与 observation 中同名指标一致；
- `scoring_contract_hash` 是否匹配 task contract；
- `evaluate_records(...).final_best_score` 是否等于 trajectory 中 final assay leaderboard score 的最优值。

测试会覆盖正常轨迹、篡改 observation score、以及非 final assay 暴露 leaderboard score
三类情况。

## Replay Verifier Hardening

`chemworld.eval.verify_records(records)` 是提交轨迹进入评测前的 replay gate。它会用
`task_id + seed + scenario/mechanism/task/profile/scoring hash + action sequence`
重新创建环境并逐步执行 action，然后比较：

- reward；
- public observation；
- terminated / truncated；
- mechanism hash；
- task contract hash；
- runtime profile hash；
- scoring contract hash；
- observation contract hash；
- operation type、kernel id、kernel version；
- affected ledgers；
- world events；
- state patch summary；
- state delta summary；
- transaction status 和 rollback reason；
- constitution checks。

预发布测试覆盖 reward 篡改、observation 篡改、首行和中途 contract hash 篡改、mechanism
hash 篡改、profile hash 篡改、transaction metadata 篡改、state patch summary 篡改，以及
early termination 轨迹重放。

## 发布产物

正式 release 应包含：

- 文档站；
- 任务卡；
- baseline 表；
- trajectory 示例；
- self-consistency audit；
- release checklist；
- paper artifact 说明。
