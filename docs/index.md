<section class="cw-home-hero" markdown>

<span class="cw-eyebrow">A causal world engine for experimental intelligence</span>

# 让实验智能拥有自己的世界引擎

**静态基准问模型知道什么；ChemWorld 问它在不知道答案时会怎样做实验。**

<p class="cw-lead">ChemWorld 构造可回放、因果可干预的虚拟化学与化工世界。Agent 在部分观测、有限预算和安全约束下选择操作与测量、形成假设并更新策略；世界的动力学、相行为和过程规律可以改变，因此记住一个最佳配方并不足以成功。</p>

它不是通用真实反应预测器，而是训练和检验实验决策能力的研究环境。

<div class="cw-button-row" markdown>

[走进一次未知世界](one_experiment.md){ .md-button .md-button--primary }
[阅读研究主线](vision.md){ .md-button }
[构建一个 Agent](agent_tracks.md){ .md-button }

</div>

<div class="cw-pill-row">
  <span class="cw-pill">Gymnasium API</span>
  <span class="cw-pill">Replay-verified trajectories</span>
  <span class="cw-pill">Causal world shifts</span>
  <span class="cw-pill">BO · RL · LLM · World Models</span>
</div>

</section>

## 实验数据不能像文本和游戏经验一样无限生成

语言模型可以读取海量文本，机器人策略可以在模拟器里经历数百万次失败；化学与化工 Agent 却无法
在真实实验室中以同样规模安全试错。真实实验的成本、速度与风险不仅限制训练规模，也让我们很难
判断：一个 Agent 是真的会实验，还是只复用了已知配方、静态知识或某个固定模拟器的规律。

| 静态化学 Benchmark | ChemWorld |
| --- | --- |
| 给定问题，生成答案 | 给定目标，决定下一步实验 |
| 一次性输入输出 | 多轮观测、行动与恢复 |
| 测试知识与预测 | 测试探索、测量、适应与控制 |
| 数据和规律固定 | 隐藏世界规律可以改变 |
| 错误主要表现为分数下降 | 错误会消耗预算、触发风险或改变状态 |

[为什么需要 ChemWorld →](vision.md)

## 实验智能不是化学知识的另一种考试

<div class="cw-capability-grid" markdown>

<div class="cw-capability-card" markdown>

### 观察

区分已经测量的证据与仍然未知的状态。

</div>

<div class="cw-capability-card" markdown>

### 假设

对隐藏规律形成暂时、可被实验否定的解释。

</div>

<div class="cw-capability-card" markdown>

### 设计

选择能区分不同解释、而不只是重复确认的实验。

</div>

<div class="cw-capability-card" markdown>

### 操作

按合法顺序控制物料、设备、仪器与实验阶段。

</div>

<div class="cw-capability-card" markdown>

### 更新

新证据出现后改变模型、置信度和后续行动。

</div>

<div class="cw-capability-card" markdown>

### 约束

在收益、安全、成本、测量与时间之间做选择。

</div>

</div>

> **真正的实验能力不是第一次猜对，而是在猜错后知道下一步该测什么。**

[什么是实验智能 →](experimental_intelligence.md)

## Agent 如何完成一次 ChemWorld 实验

<div class="cw-flow">
  <div class="cw-flow-step"><strong>获得任务</strong><span class="cw-muted">目标、预算和约束</span></div>
  <div class="cw-flow-step"><strong>选择操作</strong><span class="cw-muted">投料、设备或测量</span></div>
  <div class="cw-flow-step"><strong>获得证据</strong><span class="cw-muted">公开观测与不确定性</span></div>
  <div class="cw-flow-step"><strong>更新判断</strong><span class="cw-muted">修改假设与策略</span></div>
  <div class="cw-flow-step"><strong>回放验证</strong><span class="cw-muted">重算结果与资源</span></div>
</div>

例如，一个 Agent 要在有限实验预算内提高连续流转化率。它不知道真实速率规律，只知道可用流量、
停留时间、测量工具与安全边界。第一次实验转化率很低：它可以延长停留时间，也可以先测中间产物，
区分“反应太慢”和“副反应太强”。两种选择会产生不同成本、证据和后续世界状态。

[查看一次完整闭环 →](one_experiment.md)

## 同一个任务，可以运行在不同的世界规律之下

普通 benchmark 换 seed 往往只改变噪声或初态。ChemWorld 还可以改变实际执行的速率律、反应拓扑、
相平衡关系或过程边界，同时保持任务目标、操作接口和可见仪器不变。

| 世界 A | 世界 B | 世界 C |
| --- | --- | --- |
| 标准速率律 | 温度依赖发生变化 | 出现新的竞争反应通道 |
| 相同任务目标 | 相同操作接口 | 相同可见仪器 |
| 最佳策略 α | 最佳策略 β | 最佳策略 γ |

Agent 不会收到世界标签。只有主动选择诊断实验、根据证据更新判断的方法，才有机会发现规律已经改变。
这让我们能研究**机制识别、变化检测、恢复速度与跨世界迁移**，而不是只比较固定参数上的最高分。

[了解会改变规律的世界 →](causal_worlds.md)

## 四个旗舰世界覆盖不同类型的实验推理

<div class="cw-world-grid" markdown>

<div class="cw-world-card" markdown>

### Partition Discovery

在有限测量下学习未知液液分配规律，测试主动学习、测量选择与低成本探索。

</div>

<div class="cw-world-card" markdown>

### Reaction to Crystallization

连接反应、晶种、冷却、生长和过滤，测试长程操作与产率—纯度—粒径权衡。

</div>

<div class="cw-world-card" markdown>

### Reaction to Distillation

从反应结果规划蒸馏条件与切割策略，在纯度、回收率、能耗和风险间取舍。

</div>

<div class="cw-world-card" markdown>

### Flow Reaction Optimization

在隐藏动力学与传热边界下调节流量和停留时间，测试系统辨识与快速适应。

</div>

</div>

[探索旗舰世界与完整任务目录 →](worlds.md)

## 同一个世界，三种不同层级的智能体

<div class="cw-track-grid" markdown>

<div class="cw-track-card" markdown>

### Campaign Design

每次选择一个完整实验。适合 BO、Safe-BO、主动学习与 recipe-level LLM。

</div>

<div class="cw-track-card" markdown>

### Procedure Execution

每次选择一个实验操作。适合层级 RL、状态机和 operation-level LLM。

</div>

<div class="cw-track-card" markdown>

### Process Control

调节有界设备设定与过程状态。适合 SAC、MPC、system identification 与 world-model control；当前不声称
通用高频连续控制。

</div>

</div>

跨越三条 Track 的共同问题是 **World-Model Adaptation**：Agent 能否从历史推断当前世界，并在规律
改变后用更少实验恢复。系统级结果可以并列展示，但算法归因需要保持相同交互层级和信息条件。

[选择适合你的 Agent Track →](agent_tracks.md)

## 高分不是唯一结果

ChemWorld 分开报告任务主指标、风险和约束、实验与测量成本、适应速度、信息效率，以及计算和模型
调用资源。不同任务、物理单位和交互层级不会被压成一个“总智能分数”。

<div class="cw-flow">
  <div class="cw-flow-step"><strong>Agent 提交</strong><span class="cw-muted">Action 与轨迹</span></div>
  <div class="cw-flow-step"><strong>确定性回放</strong><span class="cw-muted">重建状态转移</span></div>
  <div class="cw-flow-step"><strong>指标重算</strong><span class="cw-muted">不信任自报分数</span></div>
  <div class="cw-flow-step"><strong>约束审计</strong><span class="cw-muted">风险、成本与资源</span></div>
  <div class="cw-flow-step"><strong>可信结果</strong><span class="cw-muted">绑定版本与摘要</span></div>
</div>

[Benchmark 到底怎样判断实验能力 →](benchmark_overview.md)

## ChemWorld 已经暴露了哪些问题

<div class="cw-evidence-grid" markdown>

<div class="cw-evidence-card" markdown>

### 只看目标会误判方法

无约束优化提高了多个任务的目标值，却同时增加操作风险。更高产率不自动等于更好的实验策略。

</div>

<div class="cw-evidence-card" markdown>

### 严格规则允许有意义的失败

Safe-GP 改善目标并通过安全与成本规则，但一个任务未达到预注册实质阈值，因此整体结论保持失败。

</div>

<div class="cw-evidence-card" markdown>

### 环境变化不等于 Agent 会适应

隐藏机理与构成律变化具有可执行、守恒和回放控制，控制匹配可识别性证书已经通过；但在线策略可行
证书尚未完成，因此 Gate A 整体仍未通过，Agent 的识别与迁移解释保持关闭。

</div>

</div>

LLM 交互、记忆、资源账本和谱图消融协议已经具备；真实模型矩阵仍未形成正式结果。现有单 seed RL
运行主要是动作、奖励和训练合同的工程诊断，不作为训练尺度或方法排名结论。

[阅读研究发现与证据等级 →](benchmark_release.md)

## 不直接迁移配方，而是迁移适应能力

ChemWorld Engine 使用受控、可干预的虚拟规律，不承诺匿名催化剂或虚拟最优条件对应某个现实体系。
现实相关性需要逐级验证：先连接独立模型与真实数据，再进入 shadow-mode 物理实验，最后才讨论
窄域闭环。

<div class="cw-bridge-flow">
  <div class="cw-bridge-step"><strong>Causal Core</strong><span class="cw-muted">受控因果世界</span></div>
  <div class="cw-bridge-step"><strong>Independent Backend</strong><span class="cw-muted">独立高保真模型</span></div>
  <div class="cw-bridge-step"><strong>Real Dataset</strong><span class="cw-muted">真实历史实验</span></div>
  <div class="cw-bridge-step"><strong>Shadow Lab</strong><span class="cw-muted">只建议、不执行</span></div>
  <div class="cw-bridge-step"><strong>Narrow Closed Loop</strong><span class="cw-muted">审批后的窄域控制</span></div>
</div>

关键终点不是“虚拟产率是否等于真实产率”，而是：在相同现实实验预算下，虚拟预训练 Agent 是否
比从零开始更快、更安全地适应。**这是一条待验证路线，不是当前已经完成的 Bridge 产品。**

[查看从 Core 到现实的验证路线 →](real_world_bridge.md)

## 从这里进入

<div class="cw-hero-grid" markdown>

<div class="cw-hero-card" markdown>

### 亲手完成一次实验

在 Student Lab 选择操作，观察仪器、预算和世界状态怎样变化。

[打开可视化实验室 →](interactive_task_lab.md)

</div>

<div class="cw-hero-card" markdown>

### 观察一个 Agent 如何决策

查看模型请求了什么证据、为什么改变动作，以及结果能否回放。

[了解 Agent Observatory →](interactive_task_lab.md#agent-observatory)

</div>

<div class="cw-hero-card" markdown>

### 编写自己的 Agent

五分钟跑通环境，再选择 campaign、procedure 或 control Track。

[开始开发 →](getting_started.md)

</div>

<div class="cw-hero-card" markdown>

### 复现或评测方法

固定任务、信息、预算与失败规则，从轨迹重算结果。

[阅读公平评测协议 →](benchmark_protocol.md)

</div>

</div>

<p class="cw-status-footer">Research status: benchmark candidate · World Law v0.5 · Evidence is versioned on the research findings page · <a href="benchmark_release/">查看最新证据</a> · <a href="limitations/">查看适用边界</a></p>
