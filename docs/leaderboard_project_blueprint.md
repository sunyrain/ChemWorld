# 榜单与项目蓝图

ChemWorld 的 leaderboard 应鼓励 agent 学会在统一化学世界中做长期决策，而不是只记住
固定 recipe。榜单设计需要同时衡量性能、约束遵守、样本效率和可解释性。

## 挑战原则

- 公开训练任务与隐藏评测任务共享同一个 `world_law_id`。
- 任务成熟度必须显示在榜单上。
- 评分同时考虑目标指标、成本、安全和无效操作。
- 提交包必须可复现，不能依赖隐藏 state 或手工调参。

## 可见榜单

- `reaction-optimization`
- `reaction-to-purification`
- `safety-constrained-control`
- `characterization-planning`
- `mechanism-explanation`
- `tool-agent-planning`

未来可以按任务成熟度分为 `lite`、`reference-validated` 和
`professional-candidate` track。

## 项目赛道

- 规则 baseline 与强 recipe。
- Bayesian optimization / black-box optimizer。
- RL agent。
- Tool-using LLM agent。
- World-model learner。
- Curriculum learning / self-play。

## 提交合同

提交包应包含 agent 入口、依赖、运行配置、manifest 和安全声明。托管评测应以只读任务
配置、固定资源限制和结构化输出为默认。

## Notebook 教学

教学 notebook 应先演示可解释的 recipe，再逐步进入自动优化和 agent planning。不要让
学生一开始面对完整隐藏世界；课程需要坡度。
