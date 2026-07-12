# 选择交互层级

> **不同 Agent 的关键区别，不只是算法名字，而是它们控制实验的粒度。**

BO、RL 和 LLM 如果在不同时间尺度上决策，就不能只按最终分数作算法归因。ChemWorld 将 Agent 分为
三条主要 Track，并把世界模型适应作为跨 Track 能力。

## Campaign Design：下一次完整实验做什么

一个决策对应一套完整 recipe 或一次 Experiment。Agent 在 final assay 后更新模型，再选择下一套
条件。

**典型方法**：random、LHS、BO、Safe-BO、active learning、batch design、recipe-level LLM。

**主要问题**：

- 如何用少量完整实验找到高价值区域？
- 何时探索未知区域，何时利用当前最好条件？
- 哪次测量或实验最能降低关键不确定性？
- 怎样在目标、风险和实验成本间取舍？

**适合任务**：Partition Discovery、反应配方优化、多实验 campaign。

## Procedure Execution：当前流程下一步做什么

一个决策对应一次实验 Operation。Agent 必须维护同一只反应器的状态，按合法顺序完成投料、反应、
测量、分离和终检。

**典型方法**：状态机、层级 RL、recurrent PPO、operation-level LLM、规划器—执行器。

**主要问题**：

- 如何在长流程中记住物料、阶段与历史证据？
- 动作失败后怎样恢复，而不浪费预算？
- 中间测量是否改变同一次实验的后续操作？
- 如何处理离散操作与条件参数组成的混合动作空间？

**适合任务**：Reaction to Purification、Crystallization、Distillation、tool-agent planning。

## Process Control：怎样连续调节设备状态

决策集中在连续或高频设备设定，如流量、停留时间、温度和电化学控制。它要求 Agent 从传感器反馈中
识别动态系统，而不只是选择一套静态 recipe。

**典型方法**：SAC、TD3、MPC、system identification、world-model control。

**主要问题**：

- 如何在动态响应与安全边界之间控制？
- 设备滞后、传热或隐藏动力学变化时怎样恢复？
- 控制频率、观察延迟和连续资源如何公平计量？

**适合任务**：Flow Reaction Optimization、Electrochemical Conversion。

## World-Model Adaptation：现在是哪一种世界

这不是第四种动作频率，而是贯穿三条 Track 的能力。Agent 根据多次交互建立当前世界表示，在规律
变化后检测偏差、更新模型并减少恢复实验数。

可能的方法包括 context encoder、latent dynamics、meta-RL、机制识别、surrogate + MPC，以及
context-conditioned policy。关键不在模型名称，而在是否用未见 world family 检查 adaptation。

## 为什么跨 Track 排行榜会误导

一个 Campaign Agent 每次选择完整 recipe；Procedure Agent 可以根据中间测量改变流程；Process
Control Agent 甚至持续接收反馈。后两者通常拥有更多决策机会和不同信息结构。

系统级比较可以回答“哪套完整系统在给定资源下表现更好”，但算法归因需要保持：

- 相同交互层级；
- 相同公开信息；
- 相同实验、测量与计算资源；
- 相同失败和终止处理。

## 我应该从哪条 Track 开始

| 你的研究问题 | 推荐 Track | 入口 |
| --- | --- | --- |
| 比较下一套配方怎样选择 | Campaign Design | [Baseline 与资源](baseline_reference.md) |
| 让 Agent 完成一条长实验流程 | Procedure Execution | [Agent API](agent_interface.md) |
| 研究动态反馈与设备控制 | Process Control | [RL 与 World Model](world_model_learning.md) |
| 研究规律变化后的快速恢复 | 任一 Track + Adaptation | [会改变规律的世界](causal_worlds.md) |
| 让 LLM 提出假设并调用工具 | Campaign 或 Procedure | [LLM 实验智能体](llm_agent_harness.md) |

下一步：[五分钟开始](getting_started.md) · [Benchmark 设计](benchmark_overview.md)
