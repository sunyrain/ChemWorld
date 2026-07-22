# 任务分类与套件角色

任务不能只按化学名称罗列。ChemWorld 使用三个正交维度描述研究问题，再用 Core、Diagnostic 和
Extended 表示证据角色。

## 三个分类维度

### 交互尺度

| 尺度 | Agent 的决策单位 |
| --- | --- |
| Campaign Design | 下一套完整 recipe 或 Experiment |
| Procedure Execution | 当前 Experiment 的下一 Operation |
| Process Control | 有界设备 setpoint 或过程控制动作 |

当前 Process Control 是有界控制抽象，不代表已经提供任意频率、任意装置的连续控制。

### 认识目标

| 目标 | 要回答的问题 | 当前主张边界 |
| --- | --- | --- |
| Optimization | 固定世界中怎样找到更好结果 | 支持 |
| Identification | 怎样区分预注册规律或参数家族 | 支持协议与受控诊断 |
| Adaptation | 怎样检测旧模型失效并在变化后恢复 | 协议已定义，正式实证未闭合 |
| Open-ended discovery | 怎样提出候选集合之外的新规律 | 未来范围，不是当前主张 |

### 物理原型

| 原型 | 主要隐藏结构 | 当前任务例子 |
| --- | --- | --- |
| Equilibrium / partition | 平衡与分配构成关系 | `partition-discovery`、`equilibrium-characterization` |
| Kinetics / network / phase change | 速率律、拓扑和相变 | `reaction-to-crystallization` |
| Constitutive / material mapping | 电化学响应与材料身份—作用映射 | `electrochemical-conversion` |
| Dynamic apparatus boundary | 流动、传热和设备边界 | `flow-reaction-optimization` |
| Separation process | 相分离、蒸馏、回收与能耗 | `reaction-to-purification`、`reaction-to-distillation` |

这些原型用于解释结构覆盖，不表示对相应化学领域具有穷尽或通用数值保真度。

## Core、Diagnostic 与 Extended

| 套件 | 作用 | 当前范围 |
| --- | --- | --- |
| Core | 正式确认比较和主要方法结论 | v0.4 冻结四任务 |
| Diagnostic | 可识别性、no-change、反馈、反事实、适应和自治归因 | 机制 v0.2.1 等分解协议 |
| Extended | 训练、教学、覆盖展示和方法开发 | 其余已注册任务与 demos |

当前 v0.4 Core 明确是：

- `partition-discovery`；
- `reaction-to-crystallization`；
- `reaction-to-distillation`；
- `flow-reaction-optimization`。

电化学和平衡是重要物理原型，也进入 Diagnostic/Extended 研究，但不会追溯性替换这份冻结列表。
改变正式 Core 必须提升 major protocol，并重新冻结方法、资源、统计和证据绑定。

同一任务可以在不同 scenario 和协议中承担不同角色。例如 crystallization 既可在 Core 中比较固定任务
结果，也可在 Diagnostic 中测试隐藏速率律、拓扑或材料映射变化。套件角色因此不是任务名称的永久
属性，而是 `Task × Scenario × Evaluation Contract` 的属性。

## 旧任务家族怎样映射

| 旧家族 | 主要维度 | 代表任务 |
| --- | --- | --- |
| 反应优化 | Campaign/Procedure × Optimization | `reaction-optimization-standard` |
| 安全约束 | 任一尺度 × Optimization under constraints | `reaction-safety-constrained` |
| 表征与解释 | Campaign/Procedure × Identification | `reaction-mechanism-explanation`、`low-budget-characterization` |
| 反应—分离流程 | Procedure × Optimization/Autonomy | crystallization、distillation、purification |
| 规律发现 | Campaign × Identification | `partition-discovery` |
| 泛化与适应 | 任一尺度 × Adaptation | mechanism/world-family scenarios |
| 工具规划 | Procedure × Procedural autonomy | `tool-agent-planning` |

## 新任务怎样进入系统

新任务必须声明：

1. Task Contract：目标、动作/观测权限、预算、终止和评分；
2. World/Scenario：物理原型、隐藏轴、初态、干预和 seed；
3. 交互尺度与认识目标；
4. 套件角色，以及该角色所需的可识别性、资源、公平性和回放证据。

注册成功只说明任务可执行，不表示进入 Core、完成科学验证或获得发表级证据。完整目录见
[选择一个任务](tasks.md)，逐任务合同见[阅读任务卡](task_cards.md)。
