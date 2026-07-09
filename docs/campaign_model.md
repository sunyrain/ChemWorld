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

- `interactive`：agent 在线观察并逐步决策。
- `recipe`：一次性提交固定 action 序列。
- `replay`：重放已有 trajectory，用于核验 determinism 和日志完整性。
- `evaluation`：关闭调试信息，只输出公开 observation 和评分。

## Replay 合同

Replay 不应依赖随机隐式状态。轨迹必须记录 seed、task metadata、action 序列、关键
observation 和评分版本。若 replay 结果与原始结果不一致，应视为环境或记录层缺陷。
