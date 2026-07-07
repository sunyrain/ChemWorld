# Year 2 过程模块

ChemWorld 的 Year 2 目标不是增加多个独立环境，而是在同一个物理化学世界中逐步开放更多过程操作。反应、萃取、结晶、蒸馏、连续流和电化学共享同一 ontology、constitution、operation registry、instrument registry、logging 和 benchmark protocol。

## 统一操作语言

所有过程操作仍使用同一种 JSON event action：

```json
{
  "operation": "cool_crystallize",
  "target_temperature_K": 278.15,
  "duration_s": 1800.0
}
```

同一个 action 会经过三层检查：

1. schema validation：字段类型和 operation 名称合法。
2. task policy：当前 task 是否允许该 operation 和 instrument。
3. constitution preconditions：当前 state 是否满足物理前置条件。

## Crystallization

操作：

- `seed_crystals`
- `cool_crystallize`
- `filter_crystals`

状态逻辑：

- `seed_crystals` 记录晶种质量，并轻微增加成本。
- `cool_crystallize` 根据冷却深度、时间和晶种因子生成 `crystal_yield`、`crystal_purity`、`crystal_size`。
- `filter_crystals` 要求此前已经发生结晶，否则 validator 会失败。

可观测指标：

- `crystal_yield`
- `crystal_purity`
- `crystal_size`

代表任务：

- `reaction-to-crystallization`

## Distillation

操作：

- `evaporate`
- `distill`
- `collect_fraction`

状态逻辑：

- `evaporate` 减少体积，增加能耗、成本和挥发风险。
- `distill` 使用时间、温度和 reflux ratio 的 proxy 形成 purity/recovery tradeoff。
- `collect_fraction` 要求此前已经执行 distillation。

可观测指标：

- `distillate_purity`
- `distillate_recovery`
- `solvent_loss`

代表任务：

- `reaction-to-distillation`

## Continuous Flow

操作：

- `set_flow_rate`
- `run_flow`

状态逻辑：

- `set_flow_rate` 写入流速和停留时间。
- `run_flow` 使用同一套反应 ODE 的投影来估计 flow conversion。
- `run_flow` 要求此前已经设置流动条件。

可观测指标：

- `flow_conversion`
- `yield`
- `safety_risk`

代表任务：

- `flow-reaction-optimization`

## Electrochemistry

操作：

- `set_potential`
- `electrolyze`

状态逻辑：

- `set_potential` 写入电位和电流，并根据高电位增加风险。
- `electrolyze` 根据电流、时间和电位 proxy 转化 A 到 P/B。
- `electrolyze` 要求此前已经设置电位。

可观测指标：

- `electrochemical_selectivity`
- `energy_efficiency`
- `yield`

代表任务：

- `electrochemical-conversion`

## 教学与评测建议

Year 2 教程可以放在 12 天课程之后，作为 3-5 天项目扩展：

- 第 13 天：结晶与纯度/收率权衡。
- 第 14 天：蒸馏与能耗/安全约束。
- 第 15 天：连续流和电化学的策略比较。
- 第 16 天：跨过程 project leaderboard。
- 第 17 天：机制解释、失败分析和最终提交包。

这些扩展仍然应使用同一个 `ChemWorld` 环境，不应拆成单独小游戏。
