# ChemWorld-Bench

<p class="cw-site-version">Research environment · World Law v0.4 · evidence updated 2026-07-12</p>

ChemWorld-Bench 用统一的 Gymnasium 合同组织虚拟反应、分离、仪器、安全与成本。Agent 需要在
有限预算和部分可观测条件下提出操作、读取测量、更新假设，并把早期实验经验用于后续决策。

!!! warning "使用边界"
    本项目评估虚拟世界中的闭环决策，不预测真实反应，不提供工艺设计、危险评估或实验室控制
    建议。当前是可用的研究环境和 benchmark candidate，不是已验证 leaderboard。

<div class="cw-status-grid" markdown>

<div class="cw-status-card" markdown>

**15**

已注册任务，共享同一操作与回放合同。

</div>

<div class="cw-status-card" markdown>

**160 / 160**

最新经典主切片轨迹已独立重放。

</div>

<div class="cw-status-card" markdown>

**0**

当前获准的完整 benchmark 或 SOTA 主张。

</div>

</div>

<div class="cw-hero-grid" markdown>

<div class="cw-hero-card" markdown>

### 第一次使用

安装环境，完成一个 episode，并理解 observation、mask 和合法性反馈。

[五分钟开始 →](getting_started.md)

</div>

<div class="cw-hero-card" markdown>

### 运行一个比较

固定任务、seeds、实验预算和资源合同，保存轨迹并从回放重算结果。

[阅读评测协议 →](benchmark_protocol.md)

</div>

<div class="cw-hero-card" markdown>

### 接入算法或模型

同一接口支持主动学习、RL、LLM tool agent 和学生程序。

[查看 Agent 接口 →](agent_interface.md)

</div>

<div class="cw-hero-card" markdown>

### 判断证据强度

区分软件就绪、诊断结果、预注册确认实验和仍未支持的科学结论。

[查看科学状态 →](benchmark_release.md)

</div>

</div>

## 最短可复现路径

```bash
python -m pip install -e ".[dev]"
chemworld run --task reaction-to-assay --agent random --seed 0
chemworld verify --constitution --submission runs/<trajectory>.jsonl
chemworld evaluate --submission runs/<trajectory>.jsonl
```

评测端不信任 Agent 自报分数。只有通过 schema 校验、确定性回放、指标重算和轨迹摘要绑定的结果，
才能进入汇总。

## 研究对象

- 有限实验预算下的主动探索与 sample efficiency；
- 实验间更新和实验内操作调整；
- 仪器、谱图与不确定性是否真正影响决策；
- 反应与下游分离的联合规划；
- 目标、安全、成本与信息价值的权衡；
- 从训练世界和机理族向未见世界的迁移；
- 不同 Agent 范式在统一资源合同下的行为差异。

## 当前最重要的证据结论

最新冻结经典切片覆盖四个任务、两种方法、20 个配对 seeds，每次 40 个完整实验。结构化 GP 的
任务主指标在四项任务上都优于 random，并通过 objective-only 规则；但它在三项任务上的风险预算
超限率更高。原协议没有预注册安全和成本非劣门槛，因此这批结果被保留为诊断证据，不发布方法
胜负或完整 benchmark 主张。详情见[科学状态与证据](benchmark_release.md)。

## 阅读路线

| 目标 | 建议顺序 |
| --- | --- |
| 体验系统 | [安装](getting_started.md) → [任务目录](tasks.md) → [可视化实验室](interactive_task_lab.md) |
| 实现 Agent | [Agent 接口](agent_interface.md) → [操作语言](operations.md) → [交互示例](agent_interaction_examples.md) |
| 运行评测 | [科学状态](benchmark_release.md) → [协议](benchmark_protocol.md) → [提交与验证](submission.md) |
| 审查可信度 | [架构](architecture.md) → [成熟度](model_maturity.md) → [限制](limitations.md) |

左侧目录按用户旅程分组。顶部按钮可一次折叠或展开全部分组，并记住本机选择。
