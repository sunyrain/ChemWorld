# ChemWorld 系统模型

> **本页是内部架构、数据字段和论文表述的规范性来源。** 当前证据状态以
> `configs/current.json` 为准；实现存在不等于科学结论已经成立。

ChemWorld 通过统一的**物理因果世界基座、实验交互运行时和任务与评测契约**，把材料搜索、实验执行、
规律识别和动态适应组织为同一个实验智能问题。Agent、训练器、模型权重和 Agent 私有记忆位于这三层
之外。

```text
训练器 / 预训练数据 / 微调
             │
             ▼
           Agent
             │  公开任务、动作、观测和历史
             ▼
┌────────────────────────────────────┐
│ Task and Evaluation Contract       │  要完成什么、允许看什么、怎样评价
├────────────────────────────────────┤
│ Experimental Interaction Runtime   │  实验怎样执行、测量、失败和结束
├────────────────────────────────────┤
│ Physical Causal World Substrate    │  什么物理世界存在、演化并产生结果
└────────────────────────────────────┘
```

ChemWorld 可以向外部训练器提供交互数据，也可以承载训练过程，但环境本身不更新 Agent 权重、不维护
Agent 信念，也不替 Agent 选择下一步实验。

## 三层职责

| 层 | 负责 | 不负责 |
| --- | --- | --- |
| Physical Causal World Substrate | 状态、动力学、构成律、设备、仪器生成规律、约束和受控世界干预 | 任务目标、排行榜权重、Agent 信念和训练 |
| Experimental Interaction Runtime | 动作合法性、事务、生命周期、测量调用、可见反馈、失败、资源账本和轨迹 | 选择 Agent 动作、替 Agent 收尾、定义跨任务排名 |
| Task and Evaluation Contract | 公开目标、动作/观测权限、预算、终止、评分和 scenario 分布 | 修改运行时物理、向 Agent 泄露 hidden truth |

当前源码中的评分编译器仍位于 `chemworld.world.scoring`，但目标与权重的**定义权**属于 Task Contract；
运行时只执行任务提供的 scoring contract。源码命名不应被解释为物理世界自行定义研究目标。

## 第一层：物理因果世界基座

一个世界族可抽象为：

\[
W=(\mathcal X,\mathcal U,T_\omega,O_\omega,C_\omega,\Delta_\omega)
\]

- \(\mathcal X\)：物料、相、温度、反应进度、设备和过程账本组成的 typed state；
- \(\mathcal U\)：可施加的物理操作；
- \(T_\omega\)：隐藏状态转移规律；
- \(O_\omega\)：仪器与观测生成规律；
- \(C_\omega\)：物理、设备和安全约束；
- \(\Delta_\omega\)：对参数、函数形式、拓扑、材料映射或设备边界的受控干预。

世界输出物理后果、传感器结果、成本和风险，但不判断什么结果“更值得在排行榜上获胜”。当前已经
实现参数、速率律、拓扑、构成律、材料映射和部分设备边界变化；观测噪声可配置，但独立的完整
sensor-law family 尚不能作为已验证能力主张。

相同 world 配置、seed、动作序列和干预计划应能够回放。换 seed 主要检查实例随机性；切换
world/mechanism family 才能检查预先定义的规律变化。

## 第二层：实验交互运行时

一次 Experiment 是从明确初始化的样品或过程状态开始，经过一系列 Operation 与 Measurement，并以
终检、显式终止、失败或预算截断结束的一次物理运行。只有满足任务合同的 final assay 才形成可比较
的正式实验结果；失败和未完成运行仍保留在自主性分母中。

```text
Campaign
└── Experiment
    └── Operation / Measurement
```

运行时同时保留两个循环：

- 实验内：投料 → 操作 → 取样 → 测量 → 调整 → 终止/终检；
- 实验间：读取结果 → 更新判断 → 设计下一实验 → 比较并积累证据。

三个交互尺度共享同一运行时：

| 尺度 | 决策单位 | 当前边界 |
| --- | --- | --- |
| Campaign Design | 一套完整 recipe 或 Experiment | 支持 BO、主动学习和 recipe-level Agent |
| Procedure Execution | 一个实验 Operation | 支持逐操作闭环、合法性和生命周期审计 |
| Process Control | 设备设定值或过程控制动作 | 当前是有界 setpoint/process-control 抽象，不声称通用高频连续控制 |

运行时负责暴露、校验和记录 closeout 语义，但在自主评测中不会替 Agent 选择 terminate 或 final assay。
如协议允许辅助收尾，必须把 `Autonomous score` 与 `Assisted scientific score` 分开报告。

## 第三层：任务与评测契约

任务可抽象为：

\[
\tau=(G,\mathcal A_\tau,\mathcal O_\tau,B_\tau,S_\tau,\Gamma_\tau)
\]

- \(G\)：公开目标；
- \(\mathcal A_\tau\)：允许的动作抽象；
- \(\mathcal O_\tau\)：允许释放的信息；
- \(B_\tau\)：实验、操作、测量、时间和成本预算；
- \(S_\tau\)：评分和约束规则；
- \(\Gamma_\tau\)：世界、干预和 reset 分布。

不同任务保留各自主指标和单位，不压成一个跨物理域总分。在线 shaping reward、正式终点、风险、成本、
信息效率、方法资源和程序自治分别记录。

## 规范性对象和字段

| 对象 | 规范定义 | 轨迹标识 |
| --- | --- | --- |
| Task | 稳定且公开的目标、权限、预算和评分合同 | `task_id`、`task_contract_hash` |
| World | 某个隐藏物理规律实例 | `world_id`、`mechanism_hash` |
| Scenario | Task 与 World 的组合，加上初态、干预、reset、反馈条件和 seed | `scenario_id` |
| Campaign | 一个 Agent 在一个 Task × Scenario × Seed 上的实际研究运行 | `campaign_id` |
| Experiment | Campaign 内从初始化到终检、终止、失败或截断的一次运行 | `experiment_index` |
| Operation | 改变状态、调用测量或结束实验的一步 | `operation_id`、`action` |
| Run | 一份具体执行实例的可追踪标识 | `run_id` |

规范 benchmark cell 是：

\[
\text{Task}\times\text{Scenario}\times\text{Agent}\times\text{Seed}
\]

Trajectory v0.1 曾把带 split/objective/seed 的运行标识写入 `task_id`，把真正任务名写入
`benchmark_task_id`。v0.2 起 `task_id` 恢复为稳定任务合同标识，`run_id` 保存运行标识；
`benchmark_task_id` 暂时作为兼容别名保留。

## 三类结果必须分开

Trajectory v0.2 固定三个顶层字段：

| 字段 | 含义 | 是否可被反馈消融改变 |
| --- | --- | --- |
| `environment_outcome` | 世界和运行时实际产生的事务、物理结果、原始观测和资源后果 | 否 |
| `agent_visible_observation` | 此条件下真正释放给 Agent 的观测、视图和反馈 | 是，可延迟、删除或置换 |
| `evaluation_outcome` | 评价器使用的真实 reward/终点和 scoring contract 绑定 | 否 |

旧字段 `observation`、`reward`、`agent_view` 和 `leaderboard_score` 在 v0.2 中继续作为兼容别名，但新分析
不得把它们混称为一个 `outcome`。历史 v0.1 轨迹仍可读取；新写出的轨迹统一使用 v0.2。

## 完整性怎样表述

ChemWorld 不声称穷尽化学空间、精确模拟全部材料体系或替代真实实验。完整性分为三个可审计目标：

| 完整性 | 定义 | 当前状态 |
| --- | --- | --- |
| 结构完整性 | 隐藏世界—行动—状态演化—测量—反馈—下一实验链条闭合 | 按设计实现，并持续接受运行时控制 |
| 评测完整性 | 结果、约束、资源、适应和自主性均有分开的评价合同 | 合同已定义，正式跨方法实证尚未闭合 |
| 归因完整性 | 能区分不可识别、实验选择、反馈利用、行动恢复和生命周期失败 | 诊断协议已定义，机制 Gate A 仍阻塞 |

因此规范边界句是：

> **ChemWorld 面向选定物理化学原型追求实验交互栈的结构完整性；化学覆盖与数值保真度均为有界、
> 显式声明，而非穷尽。**

## Core、Diagnostic 与 Extended

这三个名字只表示**评测角色**，不表示三个不同引擎：

- **Core**：六个 serious task 的 Agent 比较环境；环境合同已就绪，但方法、资源和结果尚未冻结；
- **Diagnostic**：可识别性、no-change、反馈分支、反事实、适应分解和自治归因协议；当前机制 v0.2.1
  首先覆盖 reaction-to-crystallization 与 electrochemical-conversion；
- **Extended**：其余已注册任务、训练用途和 demos，用于说明环境覆盖，不自动承担正式排名结论。

平衡、结晶、电化学和流动都是当前比较或诊断范围内的**物理原型**。Core 的任务范围由当前
evaluation contract 决定；改变范围需要新的协议版本和重新验证，不能沿用旧结果。

## 机制理解的三级证据

1. **Declared**：Agent 报告机制或 change probability；这是可审计声明，不等于内部真实信念。
2. **Predictive**：Agent 对未执行干预给出可检验的反事实预测。
3. **Actionable**：判断实际改变下一实验，并在固定预算内改善恢复或 regret。

当前机制 v0.2.1 主要覆盖 declared 与 action diagnostics；独立 predictive probe 是后续协议功能，不能
追溯性写成当前已完成结果。

## 代码职责映射

| 包 | 职责 |
| --- | --- |
| `chemworld.foundation` / `physchem` / `world` | typed state、物理模型、世界律、场景和干预 |
| `chemworld.runtime` / `envs` | 事务、操作服务、生命周期、Gymnasium 编排和公开观测 |
| `chemworld.tasks` / `task_design` | 任务合同、研究问题、准入和成熟度 |
| `chemworld.data` | 三层结果、trajectory、dataset 和 replay metadata |
| `chemworld.eval` | 只读重放、指标、约束、资源、统计和诊断协议 |

## 当前主张边界

| 可以声称 | 不应声称 |
| --- | --- |
| 提供统一的世界、实验运行时和任务契约 | 覆盖所有化学与材料 |
| 支持 campaign、procedure 和有界 process-control 交互 | 已实现通用高频连续控制 |
| 支持优化、预注册识别与适应研究 | 已实现开放式机制发现 |
| 支持受控隐藏规律变化和回放 | 是真实实验室的通用数字孪生 |
| 能把结果、反馈、评价和自治拆开 | 自报机制概率等于模型内部理解 |
| 可被外部训练器使用 | ChemWorld 本身是一种训练算法 |

当前候选后端和回放控制可运行；正式方法冻结仍阻塞，机制 Gate A 尚未通过，外部 Bridge 证据未完成。
任何论文或 README 状态句都必须服从 `configs/current.json`，不能从软件功能自动升级成科学结论。
