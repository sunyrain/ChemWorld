# Campaign 模型

Campaign 模型把一次 agent 研究过程拆成三层：`campaign`、`experiment` 和
`operation`。这样可以同时支持单个 Gym episode、批量优化、课程任务和未来 hosted
evaluation。

## Campaign：研究批次

Campaign 是一个目标明确的研究批次，例如“在 20 次实验预算内优化产率和纯度”。它包含：

- 任务集合和 split；
- budget、seed 和隐藏 scenario 规则；
- agent 配置和 baseline 配置；
- scoring protocol；
- 输出 manifest。

## Experiment：单次实验

Experiment 是 campaign 中的一次 episode。它绑定一个 `task_id`、一个 seed、一个隐藏
scenario 和一次环境 reset。实验过程中的所有 action、observation、reward、ledger
变更和仪器读数都应可回放。

## Operation：单步操作

Operation 是 agent 提交给环境的单步动作，例如 `add_reagent`、`heat`、`measure`、
`separate_phase`。operation 必须通过 action schema 校验，并在运行时产生结构化
transaction record。

## Episode 模式

ChemWorld 目前只使用两种正式 episode 语义：

- `single_experiment`：一次 Gym episode 对应一次完整实验。合法 `final_assay` 会返回
  `leaderboard_score`，同时 `terminated=True`、`truncated=False`，之后必须
  `reset()` 才能继续。
- `campaign`：一次 Gym episode 对应一个有限预算 campaign。合法 `final_assay`
  只结束当前 experiment，不结束整个 Gym episode；环境返回
  `experiment_ended=True`、`terminated=False`，并在预算未耗尽时返回
  `next_experiment_ready=True`。

这一区分避免把 recipe-space optimizer 错误限制为“一次 final assay 后就结束”。
在 campaign task 中，一个 recipe 通常是一组 operation，并以 `final_assay` 产生一个
可用于 BO、LHS、greedy 或 leaderboard 聚合的 experiment-level 观测。

## Campaign Final Assay 信息合同

在 `campaign` task 中，合法 `final_assay` 后的 `info` 必须包含：

- `experiment_ended=True`
- `leaderboard_score`
- `experiment_summaries`
- `last_terminal_summary`
- `next_experiment_index`
- `next_experiment_ready`

其中 `experiment_index` 指刚结束的 experiment，`next_experiment_index` 指下一次
experiment 的编号。若预算已经耗尽，`truncated=True` 且
`next_experiment_ready=False`。

在 `single_experiment` task 中，合法 `final_assay` 后不返回
`next_experiment_ready` 或 `next_experiment_index`，因为 episode 已经结束。

## Replay 合同

Replay 不应依赖随机隐式状态。轨迹必须记录 seed、task metadata、action 序列、关键
observation 和评分版本。若 replay 结果与原始结果不一致，应视为环境或记录层缺陷。
