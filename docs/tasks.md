# Benchmark 任务

ChemWorld 的任务不是彼此独立的小游戏，而是同一个 `world_law_id` 下的切片。每个任务
突出不同能力：反应优化、安全、机理、表征、分离、连续流、电化学或 tool planning。

## 内置任务

当前注册任务族包括：

- `reaction-optimization`
- `reaction-to-purification`
- `safety-constrained-control`
- `mechanism-explanation`
- `characterization-planning`
- `partition-discovery`
- `purity-yield-tradeoff`
- `crystallization-control`
- `distillation-cut-selection`
- `continuous-flow-optimization`
- `electrochemical-screening`
- `tool-agent-planning`

具体数量以 registry 和 [任务卡](task_cards.md) 为准。

## 物理成熟度

每个任务必须声明 maturity。常见层级：

- `proxy`
- `lite`
- `reference-validated`
- `professional-candidate`

没有 maturity 的任务不应进入正式 benchmark claim。

## Episode 模式

`episode_mode` 描述 final assay 对 Gym episode 的影响，而不是 agent 的交互方式：

- `single_experiment`：一次 Gym episode 只包含一个完整实验。合法 `final_assay`
  终止 episode，适合 `reaction-to-assay`、`reaction-to-purification` 这类完整流程任务。
- `campaign`：一次 Gym episode 包含多个 experiment。合法 `final_assay` 结束当前
  experiment，但不终止 episode；环境会在预算未耗尽时准备下一次 experiment，适合
  BO、LHS、greedy 和 leaderboard 优化任务。

交互式 step-by-step、固定 recipe、replay 和 evaluation 是运行方式；它们可以作用在
任一 episode mode 上。

## World、Scenario、Task

`world` 定义统一规则，`scenario` 定义一次 episode 的隐藏条件和可见条件，`task` 定义
目标、预算、评分和可见接口。三者分开是 ChemWorld 可扩展性的核心。
