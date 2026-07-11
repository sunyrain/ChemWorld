# Baseline

Baseline 用来校准任务难度、验证交互协议和比较 sample efficiency。ChemWorld 逐任务报告结果，
不发布掩盖物理域与失败模式差异的单一总榜。

## 快速回归

```bash
chemworld baselines report --preset core --output-dir runs/core_baselines
```

`core` 覆盖 `reaction-to-assay`、`reaction-to-purification` 与 `partition-discovery`，适合检查从
运行、轨迹、回放到汇总的完整链路。

## 研究候选套件

```bash
chemworld baselines report --preset serious --output-dir runs/serious_baselines
python scripts/run_serious_task_suite.py --output-dir runs/serious_release
```

`serious` 是六任务研究候选 preset，不等于已验证 leaderboard。其当前用途是运行诊断和确认协议。
任何方法排名都必须同时满足当前方法资源协议和[科学状态页](benchmark_release.md)列出的门禁。

## 方法家族

| 家族 | 代表实现 | 作用 |
| --- | --- | --- |
| 随机与空间填充 | `random`, `lhs` | 非自适应下限与覆盖对照 |
| 局部搜索 | `greedy_local` | 简单自适应对照 |
| 类型化 GP | `structured_gp_bo`, `structured_gp_pi`, `structured_gp_ucb` | EI/PI/UCB 主动学习 |
| 类型化树模型 | `structured_rf_ei` | 非 GP surrogate 对照 |
| 安全约束 GP | `structured_safe_gp_bo` | 峰值风险代理与约束 acquisition；已有四任务边界确认，尚未通过联合主规则 |
| LLM 工程探针 | `tool_using_llm_stub` | 协议回归，不是 live LLM 证据 |

旧 ordinal 表示变体只用于兼容或消融。正式候选方法必须把材料选择编码为类别变量；数字代号只是稳定
序列化标识，不表示材料间具有欧氏顺序。

## 公平资源合同

候选协议为每个 task-seed-method 固定完整实验预算，并在预注册 checkpoint 记录学习曲线。当前经典
诊断使用 40 次完整实验和 4、8、12、20、40 checkpoints。每次运行还记录：

- 决策、模型更新和总墙钟；
- CPU/GPU 使用与训练环境步数；
- 模型调用、输入/输出 token 与费用；
- 完整实验数、操作数、测量数与成本；
- 非法动作、约束触发、修复和回放状态。

live LLM 还必须冻结 provider、模型标识、prompt hash、请求参数和 token 来源。replay 或 stub 不得
冒充在线模型结果。

## 当前经典证据

0.3 诊断的 160 条新 cohort 结果显示，`structured_gp_bo` 相对 `random` 达到四项 objective SESOI，
但在三项任务未通过安全非劣。随后 `structured_safe_gp_bo` 仅在 Dev seeds 1100–1119 上修复和选择：
风险标签改为单次实验的操作峰值，低强度初始设计与不确定性约束进入 acquisition，材料类别与连续
用量解耦为 recipe space 0.2。

修复策略在运行前绑定实现摘要，并在未触碰 seeds 500–519 上完成 240 条确认运行与独立回放。
它相对 `random` 通过四项 safety 与 cost 规则，四项目标方向均为正；分配、结晶和蒸馏达到 SESOI，
连续流效应 0.018752 略低于 SESOI 0.020000。因此完整 baseline 主比较仍失败，不能用这批 Bench
结果继续调参；任何新策略都需要新的 Dev 选择和未触碰确认 cohort。

后续在新的五世界开发切片中比较了风险置信系数 2.0、1.5 和 1.0。2.0 同时得到最高平均连续流
转换率、最低风险超限率和最低单实验成本；较低系数对 incumbent 的配对目标效应为负，成本回退也
超过 5%。因此保留原策略，不用这一小样本诊断改写确认结论。

## 强化学习开发状态

SAC 已在连续流 Train 环境精确完成 100,000 步并保留五个 checkpoint。20 个开发 episodes 与 10 条
标准轨迹通过完成率、非法动作和回放门禁；但 80k checkpoint 明显优于 100k，且只有一个模型 seed。
正式 RL baseline 必须先进行 pooled multi-seed checkpoint 选择，再扩展任务并访问冻结评测世界。

## 最低报告字段

- 逐任务 paired effect、bootstrap 置信区间和多重比较校正；
- best-so-far 与预算—收益曲线，而不只报告终点；
- 任务主指标、final objective、风险、成本和无效动作；
- 方法资源账本和失败运行；
- public、private 和 world-family shift 下的稳定性；
- 轨迹摘要、合同摘要和确定性回放状态。

如果 random 接近满分、强方法长期停在零分、primary metric 不随合理策略变化，或方法没有进入其
声明的更新阶段，任务不能因为软件测试通过就进入正式比较。
