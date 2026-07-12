# ChemWorld-Bench

<p class="cw-site-version">World Law v0.4 · 2026-07-12</p>

**把一次化学实验交给 Agent：让它选择操作、读取仪器、承担成本，并用下一次实验修正判断。**

ChemWorld-Bench 是一个可回放的虚拟化学实验环境。RL、贝叶斯优化、LLM tool agent 和学生程序
使用同一套任务与操作接口；每次决策都会留下轨迹，最终结果由环境重新计算，而不是由 Agent
自行报分。

<div class="cw-hero-grid" markdown>

<div class="cw-hero-card" markdown>

### 我想先跑起来

安装项目，完成一次投料—反应—检测流程，再验证生成的轨迹。

[五分钟快速开始 →](getting_started.md)

</div>

<div class="cw-hero-card" markdown>

### 我想开发 Agent

读取当前合法动作，把公开观测转换为决策，并在失败后继续恢复。

[从 Agent 接口开始 →](agent_interface.md)

</div>

<div class="cw-hero-card" markdown>

### 我想做方法比较

固定任务、实验预算与资源口径，比较目标、风险、成本和样本效率。

[设计一场公平评测 →](benchmark_protocol.md)

</div>

<div class="cw-hero-card" markdown>

### 我想理解证据边界

快速分清哪些能力已经验证，哪些结果仍属于开发诊断。

[查看当前科学状态 →](benchmark_release.md)

</div>

</div>

## ChemWorld 里的一次闭环

```text
选择任务
  → 查看当前可执行操作
  → 提交 Action
  → 获得仪器与过程观测
  → 更新策略
  → 完成 final assay
  → 回放并验证结果
```

这里最重要的不是“猜中一个最佳配方”，而是完整的决策过程：Agent 看到了什么、为什么测量、
如何响应失败，以及它是否在预算内得到一个可以重放的结果。

## 现在可以做什么

<div class="cw-status-grid" markdown>

<div class="cw-status-card" markdown>

**15 个任务**

从单次反应到多轮 campaign，覆盖反应、分离、结晶、流动、电化学与平衡表征。

</div>

<div class="cw-status-card" markdown>

**统一交互合同**

任务、Action、观测、预算、风险、轨迹与回放都带有明确版本。

</div>

<div class="cw-status-card" markdown>

**候选 Benchmark**

环境和控制链可用；完整跨方法排名、私有泛化与独立复现仍在补齐。

</div>

</div>

| 使用场景 | 推荐入口 | 你会得到什么 |
| --- | --- | --- |
| 体验完整流程 | [可视化实验室](interactive_task_lab.md) | 可操作的 Student Lab 与实时 Agent Observatory |
| 编写 RL / BO / LLM Agent | [Agent 接口](agent_interface.md) | 任务说明、合法动作、观测视图与恢复信号 |
| 选择研究任务 | [任务目录](tasks.md) | 15 个任务的目标、模式和成熟度 |
| 复现实验结果 | [提交与验证](submission.md) | trajectory、manifest、回放与评分流程 |
| 阅读系统设计 | [系统架构](architecture.md) | 世界、任务、运行时、物理模块与证据层的关系 |

## 立即运行

```bash
python -m pip install -e ".[dev]"
chemworld run --task reaction-to-assay --agent random --seed 0
chemworld verify --constitution --submission runs/<trajectory>.jsonl
chemworld evaluate --submission runs/<trajectory>.jsonl
```

运行完成后，你会在 `runs/` 中得到一条 JSONL 轨迹和对应 manifest。未测量值写作 `NaN`
（JSONL 中为 `null`）；读取数值时同时检查 `observed_mask` 或 `observed_keys`。

!!! note "先从简单任务开始"
    第一次使用建议选择 `reaction-to-assay`。它包含完整的投料、反应、测量和终检流程，
    又不会一开始就引入多轮 campaign 与复杂后处理。

## 当前证据，简短版

- 软件接口、状态账本、物理路由、轨迹回放和验证器已经形成完整工作链。
- 六个研究任务具备可执行、可辨识的隐藏机理或构成律变化。
- Safe-GP 和单任务 SAC 已产生有价值的开发证据，也暴露了安全退化与 checkpoint 选择问题。
- 正式 RL/LLM 排名、私有世界泛化和完整 benchmark 发布仍未完成。

这意味着 ChemWorld **适合开发、教学、协议研究和诊断实验**，但还不应被描述为已经定型的
SOTA leaderboard。详细数字与未完成项集中在[当前科学状态](benchmark_release.md)，不会散落在
入门步骤里打断阅读。

## 按目标继续阅读

| 你的目标 | 阅读顺序 |
| --- | --- |
| 第一次使用 | [快速开始](getting_started.md) → [选择任务](tasks.md) → [可视化实验室](interactive_task_lab.md) |
| 开发智能体 | [Agent 接口](agent_interface.md) → [操作语言](operations.md) → [交互示例](agent_interaction_examples.md) |
| 运行研究评测 | [当前科学状态](benchmark_release.md) → [评测协议](benchmark_protocol.md) → [选择 Baseline](baseline_reference.md) |
| 理解环境实现 | [系统架构](architecture.md) → [世界律](world_law.md) → [物理化学核心](physchem_core_design.md) |

!!! warning "现实世界边界"
    ChemWorld 研究虚拟世界中的实验决策，不预测真实反应，也不替代流程模拟、安全评估、
    实验室审批或设备控制。
