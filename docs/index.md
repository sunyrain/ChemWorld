# ChemWorld-Bench

<p class="cw-site-version">Backend candidate · World Law v0.4 · 2026-07-11</p>

ChemWorld-Bench 是一个可回放的闭环虚拟化学实验环境。智能体在统一的 Gymnasium
接口中选择操作、请求测量、管理实验预算，并根据前几轮观测改进后续决策。环境把反应、相态、
分离、仪器、成本和安全信号组织成版本化的世界合同。

!!! warning "科学边界"
    ChemWorld 评估的是受控虚拟世界中的实验决策能力，不预测真实反应，不提供工艺设计或实验室
    控制建议。六任务研究套件仍是 candidate；当前结果不能解释为真实化学发现或 SOTA 排名。

<div class="cw-hero-grid" markdown>

<div class="cw-hero-card" markdown>

### 第一次使用

安装环境，运行一个 episode，并读懂 observation、`info` 与合法性反馈。

[五分钟开始 →](getting_started.md)

</div>

<div class="cw-hero-card" markdown>

### 评测一个 Agent

选择任务、固定 seeds、保存轨迹，并通过确定性回放重算结果。

[阅读评测协议 →](benchmark_protocol.md)

</div>

<div class="cw-hero-card" markdown>

### 接入算法或模型

使用统一动作合同接入经典优化、主动学习、RL、LLM 或学生程序。

[查看 Agent 接口 →](agent_interface.md)

</div>

<div class="cw-hero-card" markdown>

### 判断结果能否引用

区分结构门禁、诊断实验、确认实验与尚未支持的科学主张。

[查看当前科学状态 →](benchmark_release.md)

</div>

</div>

## 最短可复现路径

```bash
python -m pip install -e ".[dev]"
chemworld tasks list
chemworld run --task reaction-to-assay --agent random --seed 0
chemworld verify --constitution --submission runs/<trajectory>.jsonl
chemworld evaluate --submission runs/<trajectory>.jsonl
```

评测端不信任 agent 自报的最终分数。轨迹经过 schema 校验、确定性回放、指标重算和摘要绑定后，
才进入结果汇总。

## 你可以研究什么

- 有限实验预算下的主动探索与 sample efficiency；
- 部分可观测条件下的实验规划、仪器选择与跨轮更新；
- 反应与下游分离的联合决策；
- 安全、成本、收益和信息价值之间的权衡；
- 从训练世界族到未见评测世界的迁移；
- 不同智能体范式在相同交互与资源合同下的行为差异。

## 选择正确入口

| 你的目标 | 建议阅读顺序 |
| --- | --- |
| 体验环境 | [安装与首个回合](getting_started.md) → [选择任务](tasks.md) → [示例](demos.md) |
| 实现智能体 | [Agent 接口](agent_interface.md) → [操作语言](operations.md) → [交互示例](agent_interaction_examples.md) |
| 运行比较 | [当前科学状态](benchmark_release.md) → [评测协议](benchmark_protocol.md) → [提交包](submission.md) |
| 审查可信度 | [模型成熟度](model_maturity.md) → [验证](validation.md) → [限制](limitations.md) |

左侧目录按上述用户旅程分组。每个分组可以独立展开或折叠；目录顶部的按钮可以一次收起全部分组。
