# Baseline 参考

Baseline 的作用不是追求最高分，而是提供可复现的下限、诊断环境问题，并帮助新 agent
作者理解任务接口。

## 推荐 baseline

- 随机合法动作 agent。
- 固定 recipe agent。
- 规则型安全 agent。
- 简单 black-box optimizer。
- 带 tool 调用的 LLM recipe planner。

## 记录内容

每个 baseline run 应记录：

- 任务集合和 seeds；
- agent 配置；
- trajectory bundle；
- score table；
- constraint failure 分布；
- 代码版本和依赖版本。

## 解读方式

如果强 recipe 无法稳定得分，优先检查任务前置条件、reward timing、phase ledger 和
measurement contract。如果随机 agent 经常触发 constitution failure，说明环境本身的
状态守恒或错误处理需要加固。

## 发布要求

正式发布前至少提供一个简单 baseline 和一个可解释强 baseline。leaderboard 上的模型
分数应始终与这些 baseline 同表展示。
