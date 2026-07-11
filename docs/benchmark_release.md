# 当前科学状态

ChemWorld 的 backend、任务合同、轨迹、回放与本地评测链路已经可以使用；六任务研究套件仍处于
`candidate`，不是已经验证的正式 leaderboard。本页把“软件能运行”和“科学主张已成立”分开说明。

## 一句话结论

当前系统适合开发和诊断闭环实验智能体，也适合生成可审计的候选证据；在 vNext 确认实验、完整
方法矩阵、安全门禁和独立复现完成前，不应声称 ChemWorld 已验证六任务 benchmark、给出 SOTA
排名，或证明了真实化学发现能力。

## 套件层级

| 层级 | 用途 | 当前状态 |
| --- | --- | --- |
| `core` | API、轨迹、回放和发布链路回归 | 可使用 |
| provisional research core | 分配、结晶、蒸馏、流动四项 campaign | 候选；待 vNext 确认 |
| exploratory | 电化学转化、平衡表征 | 探索性；主指标学习信号不足 |
| 其余注册任务 | 教学、接口实验和能力切片 | 不进入研究主排名 |

六个研究候选任务分别是：

| Task | 主要问题 | 当前证据判断 |
| --- | --- | --- |
| `partition-discovery` | 能否用有限实验学习隐藏分配行为 | core-confirmed，待新协议复核 |
| `reaction-to-crystallization` | 能否联合选择反应与结晶条件 | core-confirmed，待新协议复核 |
| `reaction-to-distillation` | 能否联合选择反应与馏分切割 | core-confirmed，待新协议复核 |
| `flow-reaction-optimization` | 能否权衡转化、热与风险 | core-candidate |
| `electrochemical-conversion` | 能否提高选择性并控制能耗 | exploratory |
| `equilibrium-characterization` | 能否高效辨识隐藏平衡 | exploratory |

这里的 `core-confirmed` 是任务有效性审计中的分类，不代表整个 benchmark 已经发布。

## 已建立的可信基础

- 任务、世界律、观测、评分和 trajectory 都有版本化合同与摘要；
- 正式运行时使用显式物理化学 provider，不经过旧的通用 proxy/fallback 路由；
- runner 对合同漂移、脏工作树、实验不足、非法值和 replay 失败执行 fail closed；
- final-assay objective、任务主指标、在线 shaping、约束、资源和有效性分层重算；
- 每个实验记录峰值运行风险，以及 total/process/measurement 成本账本；
- world-family 控制、机理族控制和语义不变性已有可执行探针；
- 经典方法资源、墙钟、模型调用、token、费用和训练步数使用统一账本；
- typed GP-EI/PI/UCB、typed RF-EI 与 constrained GP 使用类别物料表示，不把数字 ID 当成连续距离。

## 已有结果应如何解释

历史 v0.1 经典矩阵覆盖 6 tasks × 5 methods × 20 paired seeds，每条 campaign 含 40 次完整实验
并通过回放。结构化 GP 相对 random 的复合分数在六任务上为正，但任务主指标只有结晶和蒸馏达到
当时统一设置的 0.05 SESOI。分配和流动方向为正但较小；电化学与平衡主指标不支持稳定改善。

这些结果说明环境能够暴露方法差异，也同时暴露了任务有效性、指标敏感度和表示选择的问题。
它们是下一版确认协议的诊断依据，不能直接作为最终论文排名。统一 SESOI 也将被任务特异、预注册
阈值替代。

## 仍需关闭的硬门禁

1. 冻结 provisional core 的任务特异 SESOI、world severity 网格与 Train/Dev/Bench 分配。
2. 完成公开进程边界、扩展 exploit matrix、score/replay 只读重算门禁。
3. 在同一资源协议下加入 PPO、连续控制 RL 和至少两类 live LLM agent。
4. 使用新 seeds 完成 vNext 确认性矩阵，保留所有失败、资源和约束结果。
5. 运行谱图可见/不可见配对消融，确认模型是否真正使用表征反馈。
6. 从干净 wheel 和公开命令完成独立复现，再冻结图表、版本与引用产物。

## 主张矩阵

| 结论 | 当前是否支持 |
| --- | --- |
| 提供预算受限、部分可观测、可回放的多轮虚拟实验环境 | 支持 |
| 能用统一合同比较不同智能体的交互和资源使用 | 支持软件层能力；完整方法比较待确认 |
| 结构化主动学习在部分任务上显示稳定候选收益 | 支持，限历史诊断证据 |
| 六任务 benchmark 已完成科学验证 | 不支持 |
| safe BO 已被证明有效 | 不支持，历史安全约束未充分激活 |
| 已完成 RL、live LLM 或 SOTA 排名 | 不支持 |
| 数值结果代表真实反应产率、安全性或工业性能 | 不支持 |

## 机器可读检查

```bash
chemworld tasks readiness
python scripts/audit_task_validity.py
python scripts/audit_method_protocol.py
python scripts/run_release_gate.py
```

发表或引用结果时，应同时报告 commit、任务合同摘要、方法 manifest、seeds、完整实验预算、回放状态
和适用边界。详细运行规则见[评测协议](benchmark_protocol.md)，科学限制见[适用范围与限制](limitations.md)。
