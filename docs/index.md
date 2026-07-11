# ChemWorld-Bench

<p class="cw-site-version">World Law v0.4 · evidence snapshot 2026-07-12</p>

ChemWorld-Bench 是面向闭环实验智能体的可回放虚拟化学环境。经典优化、主动学习、强化学习、
LLM tool agent 和学生程序使用同一套任务、操作、观测、预算与评价合同；结果由轨迹回放重算，
不信任智能体自行提交的分数。

!!! warning "研究边界"
    ChemWorld 研究虚拟世界中的实验决策，不预测真实反应，不替代流程模拟、安全评估或实验室控制。
    当前版本是可用的研究环境和 benchmark candidate，不是已经验证的 leaderboard。

<div class="cw-status-grid" markdown>

<div class="cw-status-card" markdown>

**15**

注册任务，共享版本化操作、观测和回放合同。

</div>

<div class="cw-status-card" markdown>

**9 / 9**

六任务机理/构成律控制组合通过多种子、多配方可辨识性与守恒检查。

</div>

<div class="cw-status-card" markdown>

**0**

当前获准的完整 benchmark、SOTA 或真实化学迁移主张。

</div>

</div>

## 从这里开始

<div class="cw-hero-grid" markdown>

<div class="cw-hero-card" markdown>

### 五分钟运行

安装环境，完成一个 episode，并验证轨迹。

[快速开始 →](getting_started.md)

</div>

<div class="cw-hero-card" markdown>

### 构建智能体

读取 affordance、提交合法动作，并在测量后更新决策。

[Agent 接口 →](agent_interface.md)

</div>

<div class="cw-hero-card" markdown>

### 运行公平比较

固定任务、预算和资源口径，逐任务报告目标、风险、成本与失败。

[评测协议 →](benchmark_protocol.md)

</div>

<div class="cw-hero-card" markdown>

### 判断证据强度

区分软件控制、开发诊断、确认实验和仍未支持的主张。

[科学状态 →](benchmark_release.md)

</div>

</div>

## 最短可复现路径

```bash
python -m pip install -e ".[dev]"
chemworld run --task reaction-to-assay --agent random --seed 0
chemworld verify --constitution --submission runs/<trajectory>.jsonl
chemworld evaluate --submission runs/<trajectory>.jsonl
```

未测量数组使用 `NaN`（JSONL 中为 `null`）。读取数值前同时检查 `observed_mask` 或
`observed_keys`。

## 当前证据快照

| 证据 | 已知结果 | 可以如何解释 |
| --- | --- | --- |
| Safe-GP 确认切片 | 四任务 safety/cost 全部通过；连续流目标效应 0.018752，低于 SESOI 0.020000 | 有效失败案例，不支持完整方法优越性 |
| SAC 开发运行 | 精确 100,000 Train 步；80k Dev 优于 100k | 证明训练链可运行，要求多 seed checkpoint 选择 |
| 机理控制 | 六任务、9 种模式均可执行、可辨识、非灾难且守恒 | 证明环境控制成立，不证明 Agent 会识别或迁移 |
| LLM adapter | Pro/Flash、逐操作调用、费用账本和因果隔离谱图消融通过离线控制 | 尚无真实 API 轨迹或模型排名 |
| 全局发布门禁 | 控制层一致；正式证据层仍有 11 项活动问题 | 不发布完整 benchmark 或 SOTA 主张 |

详情见[科学状态](benchmark_release.md)和[适用范围与限制](limitations.md)。

## 文档路线

| 目标 | 建议阅读 |
| --- | --- |
| 体验系统 | [快速开始](getting_started.md) → [任务目录](tasks.md) → [可视化实验室](interactive_task_lab.md) |
| 实现 Agent | [Agent 接口](agent_interface.md) → [操作语言](operations.md) → [交互示例](agent_interaction_examples.md) |
| 运行评测 | [科学状态](benchmark_release.md) → [评测协议](benchmark_protocol.md) → [提交与验证](submission.md) |
| 理解环境 | [系统架构](architecture.md) → [世界律](world_law.md) → [机理协议](mechanism_schema.md) |
