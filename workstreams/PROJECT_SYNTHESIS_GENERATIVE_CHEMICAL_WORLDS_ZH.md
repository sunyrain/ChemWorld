# ChemWorld 项目总收束：生成式化学世界、现有证据与 Nature 级路线图

状态：内部研究母文档，2026-07-30。
审计基线：仓库 HEAD `0005e239a26c276a95ea8ce291ab559caf00857d`；审计开始与证据复核时 tracked worktree clean。
用途：统一项目身份、已有系统、现有结果、数据资产、相关工作、可守主张和下一阶段实验。本文不是论文，也不提升任何已有证据的等级。

## 0. 一页结论

### 0.1 项目到底是什么

ChemWorld 最准确的定位不是“虚拟实验室机器人”，也不是“又一个化学优化 benchmark”，而是：

> **一个可回放、有状态、部分可观测的化学/化工因果世界运行时；它在稳定的实验交互契约下，允许隐藏世界的动力学形式、反应拓扑、构成关系、材料映射和部分设备边界发生受控变化，从而研究智能体能否通过实验识别并适应未知规律。**

现实实验室和高保真数字孪生主要回答“如何在我们这个物理世界里可靠执行实验”；ChemWorld 要回答的是“当世界规律本身来自一个分布时，什么样的系统具有可迁移的实验智能”。两者可以连接，但不是在争夺同一个机器人操作问题。

### 0.2 当前项目已经到哪里

当前仓库已经有一套相当完整的**实验交互运行时和证据治理框架**：

- 统一的物理状态、操作、测量、成本、安全、失败和生命周期语义；
- 15 个注册任务，全部有可执行 midpoint/boundary 设计与绑定指标；
- 28 类操作和 5 类仪器，支持整轮实验、逐操作实验和过程控制三种抽象；
- 固定公共任务下的 seeded 参数世界，以及有限、可审计的机制/构成关系反事实变换；
- 冻结协议、精确回放、provider 账本、world-level bootstrap 和证据 DAG；
- 两个 fixed-world 任务的正式描述性结果，以及两个任务的正式三臂材料信息实验。

但当前还**不是**“近乎无限的化学规律生成器”：

- `seed` 主要扩展参数化实例，不等于扩展规律结构；
- 当前 world axes 只有 12 条，覆盖 6 个任务；
- 当前机制变化是少量硬编码模板，覆盖 6 个任务；
- 任务、拓扑、材料语义和物理模型仍以人工枚举为主；
- 没有一般化、组合式、维度类型安全的 law grammar；
- 当前正式性能实验明确没有测试 hidden world change。

因此，现阶段最诚实的表述是：

> **ChemWorld 已经是一个有限但真实可执行、可审计的多世界化学运行时；它具备升级成生成式化学世界平台的架构骨架，但尚未完成支持“开放世界规律分布”主张所需的生成器和资格验证。**

### 0.3 现有结果真正说明了什么

现有结果支持四个有限但有价值的观察：

1. 同一 Agent scaffold 在不同化学任务上的相对表现高度异质：电化学上相对信息匹配经典基线为正，结晶上为负；五任务开发实验同样出现排序反转。
2. 正确材料信息的价值不是跨任务常数：对电化学有正的确认性信息价值，对结晶不确定。
3. 错误先验会改变行为，但行为改变不等于正确理解；在一个任务中错误先验甚至提高了 sampled-world 分数。
4. 固定世界里的优化成绩与机制理解相分离：当前二级预测和机制声明指标，尤其在结晶任务上，并不支持强机制理解。

这些结果是未来“优化不等于科学理解”和“世界结构决定实验策略价值”的动机证据，但它们还没有直接验证跨规律泛化。

### 0.4 最有潜力的 Nature 正刊故事

框架本身应当是方法学主角，但 Nature 级论文还需要一个由框架首次允许严格检验的普适发现。最有潜力的目标命题是：

> **在相同交互预算下，决定智能体能否迁移到未见化学规律的关键变量，是训练世界的结构多样性而不是轨迹数量；而操作自由度的价值只在规律存在结构不确定性时显现。**

对应的目标标题可以是：

> **World diversity governs the emergence of experimental intelligence**

或更偏平台：

> **A generative multiverse for experimental intelligence in chemistry**

这两个标题目前都是**待验证的论文方向**，不是现有结果。

### 0.5 接下来最重要的五件事

1. 先修复当前证据 registry 的一致性失败，冻结一份可信的项目基线。
2. 把有限 transform registry 升级为组合式、守恒约束的 chemical-world grammar。
3. 为每个生成世界自动产生物理、数值、可实验、可识别和决策相关性证书。
4. 在同一个底层转移核上提供 recipe、staged-adaptive、primitive 三档 agency，而不是押注一种动作粒度。
5. 预注册并执行“世界结构新颖度 × agency × 方法家族”的正式实验；现有 fixed-world 结果降为 pilot/动机和补充材料。

---

## 1. 项目身份与科学问题

### 1.1 不是什么

ChemWorld 不应再被主要描述为以下任何一种系统：

| 邻近方向 | 该方向的核心问题 | ChemWorld 不应在此处竞争的原因 |
| --- | --- | --- |
| 实验室机器人/具身智能 | 视觉、抓取、仪器控制、长程工作流是否可物理执行 | 它们研究一个现实宇宙中的执行可靠性；ChemWorld 的核心变量是隐藏规律分布 |
| 高保真数字孪生 | 某个现实装置或流程能否被准确复现并 sim-to-real | ChemWorld 不承诺任一现实装置的通用数值预测 |
| 化学 BO/DoE benchmark | 哪个优化器以更少实验找到高分条件 | ChemWorld 还要允许主动表征、机制假设、反事实检验、规律变化和跨世界迁移 |
| 方程恢复 benchmark | 能否从黑箱输入输出恢复一个隐藏公式 | ChemWorld 的实验会改变有状态材料和设备，观测来自可选择仪器，失败和资源也进入轨迹 |
| 教学式虚拟实验室 | 能否遵循已知实验步骤完成预定任务 | ChemWorld 的关键不是复现教材规律，而是在公共任务不变时隐藏规律可以改变 |

### 1.2 是什么

仓库现有架构把一个世界写成：

\[
W=(\mathcal X,\mathcal U,T_\omega,O_\omega,C_\omega,\Delta_\omega),
\]

其中：

- \(\mathcal X\)：有类型的材料、相、设备和过程状态；
- \(\mathcal U\)：实验操作与测量；
- \(T_\omega\)：由隐藏世界参数/结构 \(\omega\) 决定的转移；
- \(O_\omega\)：部分观测和仪器响应；
- \(C_\omega\)：安全、资源、设备和适用域约束；
- \(\Delta_\omega\)：受控世界干预。

下一阶段应进一步把它写成一个生成过程：

\[
W \sim \mathcal G(z \mid I,\mathcal L),
\]

其中 \(I\) 是所有世界必须满足的不变量，\(\mathcal L\) 是允许组合和改变的规律语言。稳定的公共任务 \(\tau\) 不披露 \(W\)，Agent 根据历史

\[
h_t=(u_1,o_1,\ldots,u_t,o_t)
\]

选择下一次实验、操作、测量或终止决策。

因此主问题不是“能否把某个 recipe 调好”，而是：

> **在有限实验预算、部分观测和可能错误先验下，Agent 能否设计区分性实验，形成可证伪的世界模型，并把这种能力迁移到没有见过的规律结构？**

### 1.3 真正需要保持的三层系统

现有三层划分应该保留：

1. **Physical Causal World Substrate**：拥有状态、动力学、构成关系、设备、观测生成和受控世界变化。
2. **Experimental Interaction Runtime**：拥有操作合法性、事务、测量、失败、资源账本、生命周期和轨迹。
3. **Task and Evaluation Contract**：拥有公共目标、允许动作/观测、预算、终止、评分和世界分布。

Agent、训练器、模型权重和私有记忆都在环境之外。这样才能把“世界是什么”“Agent 看到了什么”“最后如何评价”严格分开。

内部规范入口：

- [`docs/architecture.en.md`](../docs/architecture.en.md)
- [`docs/causal_worlds.en.md`](../docs/causal_worlds.en.md)
- [`docs/world_validity.md`](../docs/world_validity.md)
- [`configs/current.json`](../configs/current.json)

---

## 2. 当前系统资产审计

### 2.1 注册面与执行面

下表是源码注册数量，不代表相同数量的正式评估证据：

| 资产 | 当前数量/状态 | 含义 | 主要来源 |
| --- | ---: | --- | --- |
| Gym 环境 | 1 个统一环境 | 不是每个任务一个独立引擎 | `src/chemworld/registration.py` |
| 注册任务 | 15 | 15/15 midpoint 与 boundary 可执行 | `src/chemworld/tasks.py`、`configs/current.json` |
| 注册场景规格 | 15 | 组织为 8 类 scenario family | `src/chemworld/world/scenario.py` |
| 操作类型 | 28 | 从加料、反应、分离到测量、终止 | `src/chemworld/world/operations.py` |
| 仪器类型 | 5 | HPLC、GC、UV–vis、pH meter、final assay | `src/chemworld/world/instruments.py` |
| domain service | 8 类 | 操作通过表驱动服务路由到底层物理模型 | `src/chemworld/runtime/domain_service_registry.py` |
| model provider | 20 个注册 contract | “注册”不等于全部具有同等外部验证等级 | `src/chemworld/runtime/model_reachability.py` |
| 机制卡 | 10 张 | 当前注册任务实际映射到 8 个 mechanism default | `src/chemworld/runtime/mechanisms.py` |
| world axes | 12 条 | 仅覆盖 partition、crystal、distill、flow、electrochem、equilibrium 六任务 | `src/chemworld/world/world_family.py` |
| 机制变换模板 | 6 个 | 两个 rate-law、一个 topology、三个 constitutive 模板，仅覆盖六任务 | `src/chemworld/world/mechanism_family.py` |
| material counterfactual | 3 个字段、最多 69 个单字段非恒等置换 | catalyst/solvent/electrolyte 各有四个匿名标签；一次 scenario 最多绑定一个置换 | `src/chemworld/world/material_counterfactual.py` |
| 公共标量观测键 | 37 | task-specific mask 决定实际可见子集 | `src/chemworld/world/operations.py` |
| typed hidden ledgers | 6 | species、phase、vessel、equipment、thermal、process | `src/chemworld/foundation/state_ledgers.py` |
| 绑定成功指标 | 62/62 | 15 个任务没有 dead recipe coordinate 或 formalization blocker | `workstreams/flagship_tasks/reports/task-design-matrix-v1.json` |
| deterministic boundary cases | 415 | 证明任务设计可执行，不是 415 个独立科学世界 | 同上 |

当前 15 个任务中，只有 `electrochemical-conversion` 与 `reaction-to-crystallization` 有正式模型实验；另外 13 个任务的正式经验比较仍 pending。

20 个 model provider 中，17 个用于 runtime、3 个只作 reference；当前 maturity registry 标记 15 个为 `reference_validated`、5 个为 `professional_candidate`。这是一套适用域有界的 model-card contract，不等于工业级验证。28 个 operation 虽然都有统一 service/kernel 路由，但只有 12 个声明了显式 model provider；另外 16 个是有类型的 ledger/equipment transition。因而“28 个可执行操作”成立，“28 步均由独立高保真物理求解器驱动”不成立。

### 2.2 当前交互链为什么已经有价值

ChemWorld 已经实现了很多“单个黑箱函数 benchmark”没有的结构：

- 一个 Experiment 从显式初态开始，经过多次状态改变和测量，直到 final assay、主动终止、失败或预算截断；
- 测量可能消耗样品、时间或成本；
- 非法操作、物理失败、provider failure 和生命周期失败不会被静默修复；
- `environment_outcome`、`agent_visible_observation`、`evaluation_outcome` 被分开记录；
- material identity 可以匿名，隐藏真值和 evaluator provenance 不出现在 Agent 视图；
- 同一底层状态核可以暴露整轮实验、逐操作和过程控制三种动作抽象；
- 冻结 manifest、源码 hash、运行账本、精确 replay 和证据状态共同约束结果。

这套“隐藏世界 → 操作 → 状态转移 → 可选择测量 → 反馈 → 下一实验”的闭环，是项目目前最扎实的系统资产。

五类 instrument packet 可以包含 sample state、raw signal、peaks、assignments、processed estimate、uncertainty、calibration 和 missingness。它们支持“Agent 主动申请表征并根据结果继续实验”的研究，但信号是 synthetic contract，不是真实样品谱图预测器。

### 2.3 当前多世界能力的准确边界

已经实现的变化包括：

- 参数与工作区间变化；
- 少量速率律形式变化；
- 少量反应拓扑变化；
- 分配、电化学、平衡等构成关系变化；
- 材料身份/性质映射变化；
- 少量设备边界和观测噪声变化；
- interpolation、extrapolation、composition 和 observation-noise 等预定义 world modes。

但这些目前仍是**有限注册表上的受控变换**。必须区分：

| 概念 | 当前是否成立 | 说明 |
| --- | --- | --- |
| 可复现的 seeded 参数世界 | 是 | 同一配置和 seed 可重放 |
| 固定公共任务下的受控反事实世界 | 部分成立 | 六任务有有限的机制/构成变换 |
| 可组合生成大量规律结构 | 否 | 缺少一般 law grammar |
| 近乎任意的化学/化工世界 | 否 | 任务、拓扑和物理模型仍高度枚举 |
| 任意 sensor law | 否 | 可配置噪声不等于一般、独立验证的传感规律族 |
| 普适数字孪生 | 否 | 当前是适用域受限的 benchmark worlds |

最重要的表述纪律是：

> **无限 seed 只可能给出无限多个随机实例；只有规律的函数形式、拓扑和组合结构本身可系统生成并能做结构外推时，才可以讨论开放的世界分布。**

还存在四个需要在正式生成研究前修复的实现边界：

1. 当前 `composition` 和 `observation_noise` mode 会与指定 physical axis 一起变化，干预并不严格正交；
2. 未知 scenario 的 mechanism lookup 会静默回退到 `simple_batch_reaction`，正式系统应 fail closed；
3. `reset` 替换 scenario 时需要显式检查 task–scenario compatibility，避免动作、预算和评分仍绑定旧 task；
4. `private-eval` 未配置外部 salt 时会成为 public placeholder，不能当作真正封闭的 private distribution。

### 2.4 下一代世界生成器应是什么

目标不是继续追加 task-specific `if/else`，而是形成组合式的 world grammar：

\[
\mathcal G =
G_{\text{species}}
\;G_{\text{reaction graph}}
\;G_{\text{kinetics}}
\;G_{\text{thermo/phase}}
\;G_{\text{transport}}
\;G_{\text{apparatus}}
\;G_{\text{observation}}
\;G_{\text{cost/safety}}.
\]

每一层至少需要：

- 有类型的变量、单位和适用域；
- 可组合的符号/可执行表示；
- 结构与参数的独立采样；
- provenance 和 canonical hash；
- 与公共 action/observation contract 的编译；
- 可自动验证的世界证书。

建议把世界分为三个明确层级：

1. **Reality-anchored**：采用已知化学/化工模型与合理参数，承担现实相关性和外部桥接。
2. **Counterfactual-lawful**：系统改变指数、耦合、拓扑或构成关系，但保持维度、守恒、因果和数值可解。
3. **Alien-but-coherent**：规律显著偏离现实先验，但仍满足事先声明的不变量，用于测试“真正从证据学习”而非背诵现实知识。

“千奇百怪”必须意味着**违反现实先验但不违反世界内部一致性**，不能意味着任意函数或不可证伪噪声。

### 2.5 每个生成世界必须携带的证书

建议每个 `WorldSpec` 在进入正式分布前通过六类 gate：

| 证书 | 必须回答的问题 |
| --- | --- |
| 结构/类型证书 | 变量、单位、相、物种、设备和公式能否合法组合？ |
| 物理不变量证书 | 质量/电荷/必要能量账本、因果方向、非负性和边界是否成立？ |
| 数值证书 | 在预注册 stress range 内是否稳定、可解、可重复？ |
| 实验可达证书 | Agent 的合法操作能否到达有信息的状态，而不是永远被约束挡住？ |
| 可识别证书 | 是否存在预算内实验区分候选世界；若不可识别，是否被显式标注为 such？ |
| 决策相关证书 | 世界差异是否会改变最优实验/决策，而不只是产生无关数值扰动？ |

生成器可以开放；正式 benchmark 分布必须有限、冻结、版本化、隐藏并可审计。两者不冲突。

---

## 3. 当前结果与证据等级

### 3.1 证据读取规则

本项目不能按“文件最新”或“数字最大”选择证据。当前权威入口是 [`configs/current.json`](../configs/current.json)，证据分四级：

| 等级 | 含义 | 当前主要对象 |
| --- | --- | --- |
| A：current formal result | 冻结、可回放、当前证据 DAG 标为 formal | Static-S0 v1.0；Static-S0 v1.2 三臂 |
| B：current development diagnostic | 可审计但未冻结为正式结论 | 五任务 postqualification；cross-provider pilots |
| C：historical/stale | 曾在旧源码/协议通过，当前绑定已失效 | RC28 Gate A；旧 agent pilot |
| D：not evaluated | 协议或代码存在，但没有当前正式结果 | hidden-law 跨世界 Agent 泛化、Gates B–E、外部 bridge |

证据管线整体失败不自动撤销 immutable 的 A 类正式结果；它意味着 current registry 不能整体宣称 coherent、benchmark-ready 或 publication-ready。

### 3.2 Static-S0 v1.0：两任务固定世界正式结果

设计：

- 2 个任务；
- 每任务 10 个独立 world；
- 每个 world 20 次探索实验；
- 算法 seed 是嵌套技术重复，world 才是不确定性单位；
- 所有 Participant 和 baseline 报告精确 replay；
- 没有预注册 superiority threshold 或多重比较方案，所以比较只能是 descriptive；
- `hidden_world_change_evaluated=false`。

主要结果：

| 任务 | Participant mean（world bootstrap 95%） | 最强 information-matched baseline | 配对差（95%） | 合理解释 |
| --- | ---: | ---: | ---: | --- |
| Electrochemical Conversion | 0.7150 [0.6283, 0.7861] | Structured RF-EI 0.6159 | +0.0991 [0.0103, 0.1748] | sampled worlds 上相对信息匹配经典基线为正的描述性结果 |
| Reaction to Crystallization | 0.5355 [0.5045, 0.5644] | LHS 0.5708 | −0.0353 [−0.0650, −0.0085] | Participant 在 sampled worlds 上弱于 LHS |

电化学中最强 privileged calibration baseline 是 Descriptor RF-EI 0.6441；Participant 差值为 +0.0708 [−0.0072, 0.1354]，区间跨零。因此不能写“优于所有经典方法”。

实验账本：

| 部分 | result/cell 口径 | 模拟物理实验执行 | provider calls |
| --- | ---: | ---: | ---: |
| Participant | 20 task×world reports | 760 | 420 |
| Baselines | 1,050 algorithm-seed×world cells | 27,300 | 不适用 |
| 合计 | 不应视为 28,060 个独立样本 | 28,060 | 420 |

28,060 是物理 kernel 的执行次数，不是统计学 \(N\)。正式不确定性来自每任务 10 个 independent worlds。

二级“世界理解”诊断进一步说明了优化和理解的分离：

| 任务 | 预测方向准确率 | Brier | 结构边 F1 | mechanism-tag F1 | unsupported-claim rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Electrochemical | 0.744 | 0.186 | 0.389 | 0.190 | 0.611 |
| Crystallization | 0.478 | 0.298 | 0.275 | 0.144 | 0.714 |

这些是二级诊断，不应与主评分混成一个“科学智能总分”。尤其结晶上的方向预测接近无信息水平，不能声称 Agent 已理解机制。

此外，所有最终推荐都是先前已测试过的条件，相对 incumbent 的 recommendation gain 为 0；当前结果不是“Agent 合成了未测试的新改进方法”。

机器证据：

- [`workstreams/flagship_tasks/reports/static-s0-v1.0-formal-campaign-summary.json`](flagship_tasks/reports/static-s0-v1.0-formal-campaign-summary.json)
- [`configs/benchmark/scientific_optimization_s0_v1.0_freeze_manifest.json`](../configs/benchmark/scientific_optimization_s0_v1.0_freeze_manifest.json)

### 3.3 Static-S0 v1.2：正式三臂材料信息实验

设计：

- `opaque`：材料匿名，无 nominal dossier；
- `nominal`：给出正确的匿名材料名义属性；
- `misindexed`：给出预注册的错误映射；
- 2 tasks × 10 worlds × 3 arms = 60 cells；
- 1,200 exploration + 720 predictive + 360 blind validation = 2,280 次模拟物理实验；
- 1,260 个成功 provider calls，5 次 retry，0 method failure；
- 60/60 cells exact replay。

确认性结果：

| 任务 | opaque / nominal / misindexed | nominal − opaque（familywise 97.5% CI） | misindexed − nominal（97.5% CI） | 结论 |
| --- | --- | --- | --- | --- |
| Electrochemical | 0.7150 / 0.7874 / 0.6853 | +0.0724 [0.0074, 0.1546] | −0.1020 [−0.2101, −0.0078] | 正确信息有正价值；错误先验有成本 |
| Crystallization | 0.5355 / 0.5615 / 0.5845 | +0.0260 [−0.0130, 0.0630] | +0.0229 [0.0046, 0.0419] | 正确信息效应不确定；错误先验在 sampled worlds 中反而获益 |

预注册的 overall recovery claim 在两个任务都失败：

- Electrochemical：manipulation check 和 differential action correction 通过，但 performance recovery 不通过；
- Crystallization：manipulation check 和 performance noninferiority 通过，但 differential action correction 不通过。

最稳妥的科学解释是：

> 正确先验的效用具有任务依赖性；错误先验能改变策略，但策略变化和端点改善都不足以证明 Agent 识别、纠正并利用了真实机制。

机器证据：

- [`workstreams/flagship_tasks/reports/static-s0-v1.2-three-arm-information-campaign-summary.json`](flagship_tasks/reports/static-s0-v1.2-three-arm-information-campaign-summary.json)
- [`workstreams/flagship_tasks/STATIC_S0_V1_2_THREE_ARM_INFORMATION_RESULTS_ZH.md`](flagship_tasks/STATIC_S0_V1_2_THREE_ARM_INFORMATION_RESULTS_ZH.md)

### 3.4 五任务 postqualification：当前但仅 development-only

设计：

- 5 tasks × 5 worlds ×（1 Participant + 5 baselines）= 150 result cells；
- 3,900 次模拟物理实验；
- 526 个 Participant provider calls；
- 全部 replay；
- 非 formal，不能升级成 provider 排名或广泛泛化结论。

| 任务 | Participant mean ± SD | 最佳经典均值 | 差值 | 当前信号 |
| --- | ---: | ---: | ---: | --- |
| Electrochemical | 0.7454 ± 0.0522 | 0.6622 | +0.0832 | 正 |
| Crystallization | 0.5206 ± 0.0681 | 0.6071 | −0.0866 | 负 |
| Distillation | 0.4795 ± 0.0264 | 0.4192 | +0.0603 | 正 |
| Partition | 0.5426 ± 0.0870 | 0.5511 | −0.0085 | 负/接近 |
| Flow | 0.1627 ± 0.0131 | 0.2145 | −0.0518 | 负 |

`partition-discovery` 上没有任何方法达到冻结的 0.58 threshold。该实验最重要的用途不是“2 胜 3 负”，而是证明同一 Agent scaffold 与经典方法之间存在显著 task heterogeneity，不能用一个任务代替“化学实验智能”。

证据：

- [`workstreams/flagship_tasks/STATIC_S0_FIVE_TASK_POSTQUALIFICATION_RESULTS_ZH.md`](flagship_tasks/STATIC_S0_FIVE_TASK_POSTQUALIFICATION_RESULTS_ZH.md)
- [`workstreams/flagship_tasks/reports/static-s0-five-task-postqualification-campaign-summary.json`](flagship_tasks/reports/static-s0-five-task-postqualification-campaign-summary.json)

### 3.5 RC28 机制环境资格：强历史环境证据，但当前失效

RC28 在它冻结的旧源码上曾给出很强的 environment-side 结果：

| Gate | 历史结果 |
| --- | --- |
| A2 matched identifiability | 4,896 trials；primary budget 5；active/fixed top-1 均为 0.98264 |
| A3 online attainability | 2,016 trials；360 independent task×world clusters；reference sufficiency 0.99167 |
| A3 change detection | sensitivity 0.99346；AUROC 0.99902；no-change FPR 0.02801 |
| A3 attribution/recovery | conditional attribution 0.98026；end-to-end success 0.96574 |

但当前权威状态是：

- `historical_gate_a_pass_current_binding_stale`；
- design audit、semantics audit 和 release qualification 的当前绑定不通过；
- Gate A evidence current = false；
- Participant Gates B–E pending 或未执行；
- `benchmark_ready=false`、`publication_ready=false`。

这些结果只能证明“旧冻结版本曾具备环境可识别性/可达性”，不能当作当前源码的 environment certificate，更不是 Agent 适应性能。

### 3.6 其它开发与失败证据

Cross-provider scientific-adaptation pilot：

- 24 terminal cells，19 complete、5 method failures；
- 174/192 experiments，179 successful calls / 182 attempts；
- 1,167,782 tokens，known cost USD 0.40276；
- 0 infrastructure failure，174/174 completed experiments replay；
- 10 个 complete changed cells 只有 2 个识别出正确 family；
- 两个正确归因 cell 的 post−pre 仍为负；两个改善 cell 反而都未正确识别。

它不能支持 provider 优势或 stateful-adaptation claim，但应作为方法/协议失败证据保留。

历史 v0.2.1 Agent pilot 只有 1 pair / 2 campaigns；Gate B 仅 descriptive 且 pairs 不足，C/D 未评，E 观察到 protocol failure。当前 `evidence_current=false`。

旧 fixed-world 0.3902/0.4829 数字已经撤回，不属于当前正式证据。

### 3.7 当前证据管线硬阻断

在新增本文之前的 clean 审计 HEAD 上运行：

```text
.\.venv\Scripts\python.exe scripts\evidence_pipeline.py --check
```

返回失败：

```text
current registry executable source fingerprint is stale
registry freshness state mismatch: runtime_affordance
registry gate state mismatch: runtime_affordance
repository stale binding count is inconsistent
repository stale binding identities are inconsistent
```

`configs/current.json` 当前写了 10 个 stale IDs，但 `runtime-domain-affordance-audit-v0.4.json` 的 source binding 也已过期，因此实际 stale surface 至少还缺这一项登记。

新增本文后，worktree 按设计变为 dirty；证据 provenance 会据此把更多 generated nodes 报为 dirty-state freshness/gate mismatch。这不代表正式科学结果突然失效，而是说明任何仓库改动都必须在提交并执行受控 DAG refresh 后，才能恢复 coherent current surface。本次审计没有自动刷新或改写既有 reports/results。

这意味着：

- Static-S0 v1.0 和三臂 v1.2 的 immutable formal results 仍可引用；
- 五任务仍是 development diagnostic；
- RC28 仍是 stale/historical；
- 整个 registry 不能声称 coherent；
- benchmark 和 publication 仍未 ready；
- 当前 working manuscript 没有整合三臂正式结果，也没有承载新的生成式世界故事。

---

## 4. 数据资产与可发布性

### 4.1 当前本机数据盘点

审计时本机 `runs/`：

| 指标 | 数值 |
| --- | ---: |
| 文件数 | 17,714 |
| 总字节 | 34,636,665,442 bytes |
| 二进制容量 | 约 32.26 GiB |
| tracked `runs/` 文件 | 0 |

主要分布：

| 区域 | 文件数 | 容量 |
| --- | ---: | ---: |
| `runs/formal` | 1,494 | 约 16.831 GiB |
| `runs/development` | 1,339 | 约 9.869 GiB |
| `runs/dev` | 1,018 | 约 4.770 GiB |
| RC28 及其 autonomy/site/logs | 7,068 | 约 0.252 GiB |

Static-S0 raw roots：

| campaign | 文件数 | 容量 |
| --- | ---: | ---: |
| baselines | 1,133 | 约 15.125 GiB |
| opaque Participant | 105 | 约 0.461 GiB |
| nominal Participant | 102 | 约 0.461 GiB |
| misindexed Participant | 101 | 约 0.461 GiB |

RC28 confirmatory store 有 6,912 个 JSON receipts，恰好对应 A2 的 4,896 和 A3 的 2,016。

### 4.2 不能把当前仓库称为公开数据集

- 根目录没有正式 `data/` 或 `artifacts/` 发布树；
- `.gitignore` 整体忽略 `runs/`；
- 完整 raw campaigns 只存在于本机/外部 run storage；
- tracked workstreams 主要保存 compact reports、receipts、hash 和决策，不是全部原始轨迹；
- 全部 `runs/` 中只有 51 个显式 `.jsonl` trajectory 文件、827 records；大型 static campaigns 主要嵌在 JSON report/receipt，而不是统一 trajectory table。

因此现在可以说“有本地原始运行和 tracked audit evidence”，不能说“数据集已随仓库发布”。

### 4.3 不要计算一个未经去重的“总实验数”

现有 campaigns 之间可能复用 opaque arm、报告或底层执行。28,060、2,280、3,900、4,896 和 2,016 代表不同协议下的执行账本，不能直接相加后包装成项目总样本量。

未来至少要同时报告：

- simulated kernel executions；
- complete experiments；
- provider calls/attempts/retries；
- task×world×arm cells；
- independent world instances；
- independent law-family/topology clusters；
- technical repeats；
- failures 与截断；
- token、货币、虚拟时间和材料成本。

### 4.4 正式发布前的数据工程

建议建立四层发布物：

1. **Frozen manifests**：每项结果绑定 protocol、source commit、world hash、agent/method hash。
2. **Derived tidy tables**：每行一条 experiment/campaign/world，明确独立单位和嵌套结构。
3. **Replay bundle**：小型公开 smoke subset + 全量 hash index + 可复现实行脚本。
4. **Archive**：压缩、去重、带 schema/data card/license 的 Zenodo 或同等级持久化存储。

私有 hidden-test worlds 可以只发布承诺 hash 和 evaluator；公共训练 worlds、资格证书和生成器必须足够开放，才能审查规律多样性和数据泄漏。

---

## 5. 截至 2026-07-30 的相关工作与主张边界

相关工作必须按问题分组；把所有 virtual labs 混成一个表会掩盖 ChemWorld 真正的差异，也会制造错误的“首个”主张。

### 5.1 化学优化和过程控制环境

| 工作 | 已解决的核心问题 | 对 ChemWorld 的边界 |
| --- | --- | --- |
| [Summit](https://doi.org/10.1002/cmtd.202000051) | 化学启发的虚拟反应优化 benchmark，比较 BO 等策略 | 已经覆盖可重复的 in-silico reaction optimization；ChemWorld 不能以此作为 novelty |
| [Olympus](https://arxiv.org/abs/2010.04153) | 基于实验数据 emulator 的 noisy optimization/experiment planning | 已经系统化实验规划算法比较；ChemWorld 必须超出固定 objective/emulator |
| [PC-Gym](https://arxiv.org/abs/2410.22093) | 非线性化工过程、扰动、约束以及 RL 对 NMPC | 已经覆盖过程控制；ChemWorld 的差异应是隐藏规律分布和科学识别 |
| [ChemGymRL](https://doi.org/10.1039/D3DD00183K) | 反应、萃取、蒸馏等互联虚拟 benches 上的细粒度 RL 操作 | 它直接削弱“首个可操作虚拟化学实验室”主张；ChemWorld 要靠固定任务下的受控世界变换、审计和跨规律评价区分 |

### 5.2 交互式科学发现环境

| 工作 | 已解决的核心问题 | 对 ChemWorld 的边界 |
| --- | --- | --- |
| [ScienceWorld](https://aclanthology.org/2022.emnlp-main.775/) | 文本环境中的基础科学实验和概念推理 | 交互科学推理不是新概念；ChemWorld 的优势需落在可执行物化机制与反事实世界 |
| [DiscoveryWorld](https://proceedings.neurips.cc/paper_files/paper/2024/hash/13836f251823945316ae067350a5c366-Abstract-Datasets_and_Benchmarks_Track.html) | 24 个虚构、多模态、长程科学任务及参数变化，评估完整发现循环 | “fictional scientific worlds + hypothesis/experiment/report” 已存在；ChemWorld 必须展示更系统的化学规律生成和 paired causal control |
| [DeepMind Alchemy](https://arxiv.org/abs/2102.02926) | 每 episode 重采样 latent causal structure，要求结构学习、在线推断和假设检验 | 隐因果结构的 procedural resampling 早已存在；ChemWorld 的贡献是物化化学/化工运行时而非抽象游戏 |
| [CausalWorld](https://arxiv.org/abs/2010.04296) | 可干预因果变量、可控训练/测试任务分布和 transfer | “因果世界分布”不是新词；ChemWorld 必须证明化学规律和实验语义上的独特性 |
| [XLand](https://arxiv.org/abs/2107.12808) / [AdA](https://arxiv.org/abs/2301.07608) | 大规模程序生成任务分布、开放式训练和快速适应 | “世界/任务多样性产生一般适应”已有强先例；ChemWorld 应把这一问题变成化学实验智能的可控科学研究 |
| [BoxingGym](https://arxiv.org/abs/2501.01540) | 10 个生成式概率科学环境；交互实验设计以 EIG 评价，同时测模型发现、解释和预测 | 生成式科学实验环境和信息增益评价不是空白；ChemWorld 的差异需来自可执行材料—过程与结构规律干预 |
| [SciGym systems-biology dry lab](https://arxiv.org/abs/2507.02083) | 在 SBML 系统上做迭代扰动、实验设计和分析；发布 350 个系统 | 大量可查询生物动力系统已有先例；ChemWorld 需靠化学单元操作、仪器和跨物理组件组合区分 |

### 5.3 最直接的反事实规律与主动发现竞品

这一组工作使“首个 counterfactual law / hidden mechanism / active discovery benchmark”完全不可守。

| 工作 | 规模与能力 | ChemWorld 还能守住什么 |
| --- | --- | --- |
| [NewtonBench, ICLR 2026](https://arxiv.org/abs/2510.07172) | 12 个物理域、324 个规律发现任务；通过 counterfactual law shifts 抵抗记忆；Agent 主动探测复杂模型系统 | NewtonBench 已拥有“大规模反事实规律 + 交互发现”；ChemWorld 要证明有状态材料/过程、操作、仪器、资源和多物理组合带来本质不同的问题 |
| [ActiveSciBench-Chem / LLM-AutoSciLab](https://arxiv.org/abs/2605.24043) | 57 个酶动力学任务；共享 7D assay 接口；隐藏机制、参数和相关变量；预算化主动实验；符号机制恢复 | 不能再声称首个化学隐藏机制或闭环定律恢复 benchmark；ChemWorld 的差异是超出 query→initial-rate 的有状态多步实验世界和跨模型组件反事实 |
| [DiscoverPhysics](https://arxiv.org/abs/2605.26087) | 22 个刻意偏离现实的物理世界；多轮实验；同时输出解释与可执行规律；预测和解释分开评价 | “陌生物理规律检验 out-of-the-box scientific thinking” 已存在；ChemWorld 必须展示化学/过程组合生成、实验操作链和世界分布规模 |

其中 ActiveSciBench-Chem 当前在“机制任务数量、主动 law recovery 和正式模型比较”上比 ChemWorld 的现有机制结果更成熟；NewtonBench 当前在“结构规律多样性与 held-out law discovery”上也更强。论文必须正面比较，不能只引用传统 virtual labs。

### 5.4 生成式因果世界与可执行机制评价

| 工作 | 已解决的核心问题 | 对 ChemWorld 的边界 |
| --- | --- | --- |
| [CausaLab](https://arxiv.org/abs/2605.26029) | 每 episode 随机采样隐藏 SCM，允许观测和干预，并把预测成功与图/结构方程恢复分开 | 不能声称首次随机隐藏因果实验室或首次区分预测与理解；ChemWorld 的差异是连续、守恒、有状态的化学过程 |
| [ReplaySCM](https://arxiv.org/abs/2605.08197) | 1,300 个 Boolean-SCM worlds；输出受限 DSL 机制并在训练及 held-out interventions 上执行重放 | 不能声称首次用可执行 replay 评价机制恢复；ChemWorld 要证明材料轨迹、单元操作和连续物理带来新难题 |

这些工作进一步说明，“paired replay”“机制可执行性”“prediction ≠ understanding”都不能单独作为 novelty。ChemWorld 必须依靠它们与化学/化工实验运行时、稳定动作/仪器语义和可控规律组件的交集。

### 5.5 机器人实验室与数字孪生：重要但正交

| 工作 | 主要贡献 | 与 ChemWorld 的关系 |
| --- | --- | --- |
| [LabUtopia](https://arxiv.org/abs/2505.22634) | 高保真实验室模拟、procedural scenes、五级动作层次、30 tasks 和 200+ assets | 重点是科学具身感知、规划和控制；可作为未来视觉/机器人前端，而非 ChemWorld 的主竞争轴 |
| [MATTERIX](https://www.nature.com/articles/s43588-025-00924-4) | 化学实验室多尺度高保真数字孪生、层级技能与 sim-to-real | 强调现实实验室 workflow 和 robotic transfer；ChemWorld 强调多个可能规律的世界分布 |
| [化工数字孪生知识图谱](https://www.nature.com/articles/s44286-026-00392-1) | 用 ontology、Law/Formula、规则、数据库和 agents 自动组装、搜索、校准现实化工过程模型 | 不能声称首个系统化构建化工模型的框架；ChemWorld 要把模型变体变成隐藏世界分布和对照评价 |
| [Robotic chemistry stress test](https://arxiv.org/abs/2607.23045) | 45 workstations、4,608 trials，测量物理可执行 workflow 和反馈后重规划 | 它测 deployment readiness；ChemWorld 测规律不确定性下的实验智能 |
| [LabOSBench](https://arxiv.org/abs/2606.16802) | 科学仪器 GUI/computer-use 控制 | 可连接为 instrumentation front-end，但不是世界生成核心 |
| [LabRobFail](https://arxiv.org/abs/2607.23704) | 化学 self-driving lab 的机器人失败分析 | 提醒 ChemWorld 保留失败和资源账本，但不改变其核心定位 |

### 5.6 最安全、也最有价值的差异化表述

当前不要使用：

- “世界上第一个化学隐藏机制 benchmark”；
- “第一个反事实物理规律环境”；
- “第一个交互式科学发现世界”；
- “最完整的虚拟实验室”；
- “可以生成近乎无限的化学规律”；
- “首个自动构建化工模型/数字孪生的框架”。

当前最可守的是一个**交集创新**：

> **ChemWorld 统一了有状态材料—过程动力学、多步实验操作、可选择仪器测量、部分观测、资源/安全/失败账本，以及在稳定公共任务下对隐藏机制、构成关系、材料映射和设备边界的配对反事实干预。**

这仍应写成“we introduce / we study this combination”，而不是未经系统综述验证的绝对 “the first”。

完成下一代 generator 后，可以升级为：

> **ChemWorld provides a compositional, conservation-constrained distribution of executable chemical-process worlds for studying experimental intelligence under held-out laws.**

一个更适合作为全文概念句、同时不依赖 “first” 的表述是：

> **ChemWorld makes the laws of the laboratory experimentally assignable, allowing experimental strategy itself—not recalled chemical knowledge or robot dexterity—to become the object of controlled measurement.**

---

## 6. 可声明与不可声明

### 6.1 现在可以声明

- 有一个统一、可回放的 candidate 物理化学运行时；
- 结构上闭合了 task/world/scenario/campaign/experiment/operation 层级；
- 15 个任务设计可执行，415 个 boundary cases 可确定性运行，62 个指标全部绑定；
- 支持整轮实验、逐操作实验和 bounded process-control 抽象；
- 有 seeded 参数世界与六任务上的有限机制/构成变换；
- 两个固定世界任务有 current formal descriptive results；
- 两个任务有 current formal 三臂信息结果；
- 结果显示显著 task heterogeneity、任务依赖的信息价值，以及行为改变不等于正确恢复；
- 本地保存了大规模 raw execution，tracked evidence 可审计，但完整数据尚未发布。

### 6.2 现在不可以声明

- 已实现近乎无限或开放式的化学规律生成；
- seed robustness 等价于结构规律泛化；
- Agent 已经在规律变化后实现机制适应；
- 当前 Agent 具有广义科学理解；
- Participant 跨任务优于经典方法；
- 当前结果是通用 provider/model 排名；
- 15 个任务都有正式比较；
- RC28 是当前有效 environment certificate；
- benchmark-ready、publication-ready 或 submission-ready；
- 完整 raw dataset 已随仓库公开；
- 当前结果具有 real-lab 或 sim-to-real 外部有效性。

### 6.3 主张阶梯

| 阶段 | 可守主张 | 必要证据 |
| --- | --- | --- |
| C0：现在 | 有限、可审计的多世界化学实验运行时 | 当前源码、任务矩阵、正式 fixed-world 结果 |
| C1：generator qualified | 可组合生成结构多样、内部自洽的化学/过程世界 | grammar + 六类 world certificate + held-out structure splits |
| C2：formal agent study | 世界结构多样性/agency 对跨规律实验智能有因果影响 | 预注册 factorial study，多方法、多任务、law-family 为独立单位 |
| C3：external bridge | 该效应对现实相关化学/过程模型具有外部意义 | 独立 backend、现实数据或高保真模型 bridge |
| C4：Nature-level | 得到跨任务、跨模型、跨 backend 的一般规律 | replication、强 controls、开放数据与生成器 |

---

## 7. 核心论文故事与实验设计

### 7.1 故事主轴

论文不应以“我们做了 15 个任务、Agent 得了多少分”为主线。更强的叙事是：

1. 现实世界只给科学智能一个固定物理宇宙，实验昂贵，无法系统操纵“规律本身”；
2. 现有化学优化环境多数固定规律；现有反事实规律 benchmark 多为抽象物理或单次黑箱查询；
3. ChemWorld 构建可执行的化学/过程世界分布，使同一公共任务可在不同隐藏规律下配对重放；
4. 这允许首次在该系统中因果分解：数据量、世界结构多样性、动作自由度、先验、主动测量和世界模型分别贡献什么；
5. 核心经验发现应是一个关于实验智能的普适规律，而不仅是 leaderboard。

### 7.2 四个主要待验证假设

**H1：固定世界表现不能预测 held-out-law competence。**
在 parameter-IID 上高分的方法，会在未见 rate-law form、topology 或 composition 上发生显著排序反转。

**H2：结构世界多样性比同量轨迹更重要。**
固定总 kernel calls、训练 tokens 和模型容量，提高独立 law-family 多样性应改善 held-out structure 的适应速度；只增加同一规律的参数 seed 不应产生同等收益。

**H3：agency 的价值与规律不确定性存在交互。**
在固定/熟悉世界中，recipe-level 优化可能更稳定；当规律结构未知时，选择测量、分阶段修改实验和终止的能力才产生优势。

**H4：端点优化与世界理解可以分离。**
高 endpoint score 不保证正确预测新干预、恢复机制或在 changepoint 后恢复；需要独立评价 declared、predictive 和 actionable understanding。

### 7.3 主实验矩阵

世界新颖度与 agency 应当正交：

| 世界 split | 变化内容 | 主要问题 |
| --- | --- | --- |
| W0：fixed / parameter-IID | 同一结构内参数变化 | 传统优化能力 |
| W1：parameter extrapolation | 同结构、区间外参数 | 数值外推 |
| W2：held-out law form | 未见速率律/构成函数 | 规律形式迁移 |
| W3：held-out topology | 未见反应/过程连接 | 结构发现 |
| W4：held-out composition | 见过组件、未见组合 | 组合泛化 |
| W5：changepoint | campaign 内规律改变 | 在线检测与恢复 |
| W6：reality-anchored external | 独立模型或现实数据 | 外部有效性 |

| Agency | Agent 能决定什么 | 论文角色 |
| --- | --- | --- |
| A0：recipe parameters | 一次填写完整实验参数 | 与 BO/DoE 公平比较的低 agency 基线 |
| A1：staged adaptive experiment | 在预定义阶段选择操作、表征和条件，可基于中间结果调整 | 建议作为主 benchmark 接口 |
| A2：primitive operations | 每一步加料、反应、测量、分离、终止 | 自主性/执行诊断与高自由度 track |

主模型家族至少包括：

- random、LHS、DoE、BO/Safe-BO；
- active system identification / Bayesian experimental design / symbolic regression；
- RL、meta-RL 或 learned world-model agent；
- LLM agent；
- oracle/privileged calibration 与 information-matched controls。

### 7.4 动作粒度问题的解决方案

不需要在“逐操作太难训练”和“固定 recipe 太限制 Agent”之间二选一。应当建立一个有类型的实验 DSL 和公共编译器：

```text
recipe proposal ─┐
staged policy ───┼─> canonical experiment program ─> primitive transition kernel
primitive policy ┘
```

公平性来自：

- 三种接口最终调用同一底层物理核；
- 使用同一成本、安全、测量和失败账本；
- 高层 recipe 不是环境偷偷补全，而是显式、可审计地编译；
- 经典方法在它们自然的参数空间比较，不强迫逐 token 操作；
- LLM/Agent 的额外自由度通过单独 agency factor 和等预算对照计算；
- 同一实验程序可跨分辨率重放，以验证语义等价。

A1 staged-adaptive 是最适合正式主实验的折中：保留中间表征与反馈后的真正决策，同时减少无意义的低层动作信用分配。A2 应保留为平台亮点和 autonomy track，但不必成为所有模型的唯一入口。

### 7.5 关键因果对照

1. **固定经验量的世界多样性干预**：相同总实验执行，改变 law-family 数量和结构熵。
2. **参数 seed vs 结构 diversity**：证明收益不是更多随机实例。
3. **相同信息/成本的 agency 对照**：A0/A1/A2 的观测和预算匹配。
4. **主动测量消融**：可选择仪器 vs 固定 assay schedule。
5. **显式假设/证伪消融**：去掉 competing hypotheses、反事实预测或 falsification objective。
6. **正确/错误/无先验**：扩展现有三臂设计到 held-out laws。
7. **paired twin worlds**：每次只改变一个规律组件，控制其它状态、噪声和预算。
8. **no-change controls**：避免把随机波动当作规律改变。
9. **independent backend**：排除只学习 ChemWorld 实现伪影。

### 7.6 主要终点

不要把所有量压成一个总分。至少分开：

- endpoint utility / normalized regret；
- 达到性能阈值所需实验数；
- held-out intervention prediction；
- law/topology equivalence 或 posterior calibration；
- changepoint detection delay、false-positive rate 和 recovery regret；
- measurement information efficiency；
- invalid action、failure、resource 和 safety rates；
- 对 law family、task、model、provider 和 backend 的层级泛化。

未来统计的最高独立单位应该是 **law family / topology family**，world parameter instances 嵌套其中，算法 seeds 再嵌套于 world。不能继续只对随机调用或轨迹做 bootstrap。

### 7.7 目标图组

| 图 | 内容 | 需要证明什么 |
| --- | --- | --- |
| Fig. 1 | world grammar、不变量、运行时和稳定任务接口 | 平台确实生成“有规律的世界”，不是随机函数 |
| Fig. 2 | 生成世界的物理/数值/可识别/决策相关资格 | 世界分布有效且多样 |
| Fig. 3 | paired counterfactual worlds 与最优区分实验 | 规律变化可因果隔离 |
| Fig. 4 | world novelty × agency × method 的性能曲面 | agency 的价值随结构不确定性出现 |
| Fig. 5 | 固定总经验下的 world-diversity scaling | 结构多样性而非轨迹数量驱动 held-out-law transfer |
| Fig. 6 | 优化、预测、解释、恢复的分离；外部 backend bridge | 结论不只是 simulator leaderboard |

现有 fixed-world 和三臂结果适合成为 Fig. 0/pilot 或 Extended Data，而不应充当 Fig. 4–6 的替代品。

---

## 8. 分阶段 Roadmap 与 go/no-go gate

### P0：证据与项目基线复位

工作：

- 修复 `runtime_affordance` 和 stale binding registry；
- 让 `scripts/evidence_pipeline.py --check` 在 clean HEAD 通过；
- 将三臂正式结果纳入 claim ledger 和新稿；
- 冻结当前正式、开发、历史和撤回证据清单；
- 建立 raw campaign 去重 manifest 与数据字典；
- 明确当前 manuscript 仅是旧的 narrow fixed-world 稿。
- 将 unknown scenario mechanism lookup 改为 fail closed；
- 增加 task–scenario compatibility gate；
- 解耦 physical-axis、composition 和 observation-noise interventions；
- private-eval 正式运行强制要求外部 salt。

退出 gate：

- evidence pipeline 0 error；
- `current_evidence_coherent=true` 仅在实际满足时设置；
- 所有正式数字能从冻结 summary 单源生成；
- 不再存在未登记的 raw dependency 或撤回数字。

### P1：Chemical World Grammar v1

工作：

- 为 species/reaction graph、kinetics、thermo/phase、transport/apparatus、observation 建立 typed IR；
- 提供 dimension-aware expression grammar 和 topology composition；
- 把现有六个 mechanism transforms 迁移成 grammar 实例；
- 实现 reality-anchored、counterfactual-lawful、alien-but-coherent 三层；
- 稳定 `world_spec`、`law_family_id`、`topology_family_id`、`world_hash`。

退出 gate：

- 结构变化不再依赖 task-specific 硬编码分支；
- 能生成真正未见的 law form、topology 和 component composition；
- seed、parameter instance、law family 和 task 被独立标识；
- 每个 world 可完整回放和 provenance 追踪。

### P2：World Qualification

工作：

- 运行结构/类型、守恒、数值、可达、可识别、决策相关六类证书；
- 对失败世界自动 quarantine，而不是静默修补；
- 构造 matched twins 和 no-change twins；
- 量化 world diversity，避免只报生成数量；
- 冻结 train/public-validation/private-test 的结构级 split。

退出 gate：

- 预注册 stress suite 上的类型/守恒错误为 0；
- 数值稳定、非退化、可达和 decision-relevance 达到预设阈值；
- held-out law/topology/composition 无泄漏；
- 人工专家抽查和自动证书一致；
- 资格失败率与失败原因公开。

### P3：Agency Compiler 与预实验

工作：

- 用一个 canonical experimental-program IR 统一 A0/A1/A2；
- 验证跨动作分辨率的语义等价；
- 为经典方法、active discovery、RL 和 LLM 建立 information-matched baselines；
- 在至少三个物理机制不同的 core tasks 上做小规模 power pilot；
- 通过 simulation-based power analysis 确定 law-family cluster 数，而不是按调用成本拍脑袋。

退出 gate：

- 同一程序跨接口的终态/账本在容差内一致；
- action resolution 不引入隐藏信息或隐性 assist；
- primary endpoints、exclusions、failure denominators 和统计模型全部冻结；
- pilot 只用于估计方差和可行性，不用于选择有利假设。

### P4：正式 “World Diversity × Agency” 实验

工作：

- 固定总训练/实验预算，操纵结构多样性；
- 覆盖 W0–W5 与 A0–A2；
- 多模型家族、多 LLM provider、经典与 oracle controls；
- 以 law-family 为最高独立单位做层级推断；
- 预注册主效应、交互、multiplicity 和 failure handling；
- private worlds 在方法冻结后一次性打开。

退出 gate：

- H1–H4 中至少一个跨任务、跨模型稳定成立，并有预注册效应；
- 结论不由单个 task/provider 驱动；
- 排除参数数量、调用数量、上下文长度和信息不匹配解释；
- 所有 cells replay，失败进入分母。

No-go：

- 若效应只在一个任务或一个 provider 出现，降级为领域 benchmark 论文；
- 若更多 seed 与更多 law family 无法区分，不能写 world-diversity principle；
- 若 A2 优势来自更高信息/预算，不能写 agency 效应；
- 若世界证书无法保证内部一致性，暂停大规模 Agent 实验。

### P5：外部 bridge

工作：

- 接入至少一个独立实现的高保真 process/chemistry backend；
- 选择现实已有数据或公开模型可验证的 reality-anchored worlds；
- 检验 ChemWorld 内的 method ranking、信息价值或诊断能否预测外部表现；
- 可以连接数字孪生/机器人前端，但不把物理操作成功率改写成主问题。

退出 gate：

- 主要现象在独立 backend 上方向一致；
- 明确哪些结论只对 synthetic worlds 有效；
- 不依赖 ChemWorld 私有变量命名、模板或评分伪影。

### P6：发布与论文

工作：

- 发布 generator、public worlds、证书、baselines、derived data、replay bundle 和 evaluator；
- 私有测试集保留 cryptographic commitment；
- 重写 manuscript，而不是在现有 fixed-world 稿上追加一节；
- Nature 主稿只保留一个中心结论，其余成为 Methods/Extended Data；
- 同步准备更低风险的平台/数据论文路线。

退出 gate：

- 独立团队可从公开包复现主要图表；
- 所有 claim 都能映射到一条 current evidence edge；
- benchmark/publication readiness 由机器检查而非手工判断。

### P7：provenance 与 replay 加固

这部分可以与 P1–P6 并行，但应在正式发布前完成：

- 每一步记录 canonical hidden-state digest；
- replay 比较完整 raw signal、processed estimate、uncertainty 和 solver diagnostics；
- 明确当前 “exact replay” 只表示通过既定 trajectory verifier contract，不写成逐字节完整隐藏状态相同；
- 为 generator 记录采样概率、rejection reason、parent component hashes 和 exogenous random tape；
- paired worlds 复用相同初态与 keyed noise/random tape，只改变预注册的一项 world intervention。

---

## 9. 项目资源配置建议

在下一阶段，不建议把主要算力和人力投入到“让当前最简单 Agent 在固定任务上再涨几分”。建议优先级：

1. **世界生成和资格验证**：项目最独特、也最薄弱的部分；
2. **结构级数据划分和因果实验设计**：决定论文结论是否成立；
3. **agency compiler 与公平 baseline**：解决动作粒度争论；
4. **Agent 方法**：保持多家族、有代表性，但暂时不是唯一主角；
5. **外部 bridge 和发布工程**：决定 Nature 级可信度。

一个合理的原则是：

> 在 P1/P2 通过前，不再用大量 provider calls 扩大 fixed-world leaderboard；每一笔新增实验预算都应回答一个 world-level 或 attribution-level 问题。

### 9.1 论文路线应当分叉，而不是用一篇稿承担所有风险

| 路线 | 核心贡献 | 最低成熟度 | 当前材料的作用 |
| --- | --- | --- | --- |
| 平台/数据论文 | 可执行化学世界运行时、world grammar、资格证书、公开基准和回放 | P0–P3 | 架构、任务矩阵、fixed-world 与信息实验可直接继承 |
| Nature 主故事 | world diversity 与 agency 如何因果决定 held-out-law experimental intelligence | P0–P5 | 当前结果仅作 pilot、动机和方法验证 |
| Agent/方法论文 | 特定 hypothesis-testing、world-model 或 adaptation 算法 | P2–P4 | RC28 协议和失败 pilots 可指导方法设计 |

这三条路线可以共享同一个世界与数据基础，但不能互相“借证据”。平台可执行不等于 Agent 适应；Agent 在一个任务进步也不等于 world-diversity principle。

---

## 10. 最终叙事模板

### 10.1 对外一句话

> ChemWorld is a replayable, stateful chemical-process world engine that exposes the same experimental task across controlled distributions of hidden physical laws, enabling causal studies of how agents learn to experiment, identify and adapt.

### 10.2 摘要逻辑骨架

1. 真实实验昂贵且只允许在一个固定物理宇宙里观察科学智能。
2. 我们构建了一个由守恒约束的生成式化学/过程世界分布，同一任务可以在不同隐藏动力学、拓扑、构成关系和设备规律下执行。
3. 统一运行时允许 Agent 选择实验、操作和测量，同时精确记录状态、成本、安全、失败和反事实配对。
4. 在固定经验量的正式实验中，我们研究结构世界多样性和 agency 如何决定对未见规律的迁移。
5. 目标发现是：结构世界多样性而不是重复轨迹驱动跨规律适应，且高 agency 的价值只在规律不确定时出现。
6. 现实相关/独立 backend 的 bridge 证明该规律不是单一 simulator 伪影。

第 4–6 句目前尚未由现有结果完成，必须由 P1–P5 产生。

### 10.3 当前仓库在未来论文中的角色

| 当前资产 | 未来论文位置 |
| --- | --- |
| 三层架构、事务运行时、操作/测量语言 | Fig. 1 / Methods |
| 15 个任务和 62 个指标 | 平台覆盖与 Extended Data |
| Static-S0 两任务 | fixed-world motivation / pilot |
| 三臂信息实验 | priors 与 behavior-understanding dissociation |
| 五任务开发结果 | task heterogeneity 动机 |
| RC28 历史 Gate A | 资格方法的前身，重认证后再用 |
| replay/evidence DAG | reproducibility 与 release |
| 新 world grammar 和正式 factorial study | Nature 主结果 |

---

## 11. 单一事实入口

内部证据应按以下顺序读取：

1. [`configs/current.json`](../configs/current.json)：当前状态与证据角色；
2. 冻结 manifest 和 immutable formal summary：正式数字；
3. [`scripts/evidence_pipeline.py`](../scripts/evidence_pipeline.py)：生成依赖与 freshness；
4. source registries：实现能力和计数；
5. 本地 `runs/`：原始执行，不自动构成 current evidence；
6. working manuscript：叙事消费者，不是事实源。

关键入口：

- [`README.md`](../README.md)
- [`docs/research_findings.md`](../docs/research_findings.md)
- [`docs/benchmark_release.md`](../docs/benchmark_release.md)
- [`paper/chemworld_benchmark_manuscript.md`](../paper/chemworld_benchmark_manuscript.md)
- [`workstreams/README.md`](README.md)

---

## 12. 最后判断

ChemWorld 的真正机会不在于把现实实验室的机械执行做得更像，也不在于比一个 BO baseline 多赢几个固定任务。它的机会是把“物理规律本身”变成可设计、可冻结、可干预、可配对、可重放的实验变量，并让化学实验智能第一次可以在**世界分布**而不是单一世界上被研究。

当前仓库已经完成了困难但偏基础的一半：交互栈、物理执行、任务契约、回放和证据治理。另一半——组合式规律生成、世界资格、结构级泛化实验和外部 bridge——才是决定项目能否从一个扎实 benchmark 变成 Nature 级科学故事的部分。

最关键的战略选择因此不是“recipe 还是逐操作”，而是：

> **先把世界空间变成真正的研究对象，再把动作粒度作为受控实验变量。**
