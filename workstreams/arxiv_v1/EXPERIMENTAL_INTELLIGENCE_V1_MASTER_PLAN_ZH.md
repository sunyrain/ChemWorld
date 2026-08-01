# ChemWorld 第一版 arXiv 总规格：可执行化学世界中的实验智能

状态：`authoritative working plan; terminal scientific matrix incorporated`

工作标题：*Experimental Intelligence in Executable Chemical Worlds*

机器总账：`workstreams/arxiv_v1/reports/experimental-intelligence-experiment-ledger-v0.1.json`

终态实验审计：`workstreams/arxiv_v1/ARXIV_V1_READINESS_AUDIT_ZH.md`

相关工作审计：`workstreams/arxiv_v1/RELATED_WORK_AUDIT_2026_08_ZH.md`

## 0. 第一版的一句话故事

> **The agent is the subject; the chemical world is the apparatus.**

ChemWorld 的第一版不讲“从配方优化走向自主实验”，也不以 LLM 是否胜过 BO 为中心。它把正在做实验的 Agent 变成一个可受控干预、可重复测量、可逐步回放的科学对象：Agent 在隐藏化学世界中选择操作、表征、停止与 final assay，承担材料、仪器、容器和失败后果；我们由此测量端点分数之外的 discovery、retention、drawdown、recovery、evidence response 和 cognition。

第一版的核心经验发现是：

> **端点方向性不保证产生它的实验生命周期可重复。**

在固定物理世界与配对身份下，fresh trajectories 的 prior effect 仍频繁翻转。部分 endpoint 在某个世界中保持方向性，但 discovery、retention、drawdown 与 terminal behavior 大多不形成稳定 phenotype。这不是“先验好或坏”的结论，而是一个此前难以严格测量的实验智能结构。

## 1. 科学对象与研究问题

本文把 experimental intelligence 定义为：Agent 在部分可观测、有限资源且操作有后果的世界中，选择实验、使用证据、修正策略并完成实验生命周期的能力结构。

它至少包含六个不能互换的维度：

1. lifecycle autonomy：能否自主建立、推进、停止并 final-assay 实验；
2. discovery：何时首次找到高质量条件；
3. retention：找到条件后能否继续保持；
4. drawdown/recovery：离开 incumbent 后损失多少、是否以及何时恢复；
5. evidence response：表征之后如何改变可比较的控制动作；
6. cognitive reliability：held-out prediction、calibration、结构声明和 unsupported claims 是否可靠。

四个研究问题为：

- RQ1 — Endpoint underdetermination：相似 endpoint 是否来自不同生命周期？
- RQ2 — Prior intervention：先验首先改变分数，还是改变实验选择与轨迹稳定性？
- RQ3 — Within-world repeatability：开发期观察到的行为模式能否在固定世界内跨 fresh trajectories 重现？
- RQ4 — Optimization–cognition dissociation：优化、预测、声明可靠性和恢复是否给出一致能力排序？

## 2. ChemWorld 的方法学位置

ChemWorld 不是机器人实验室的替代品。现实自动化实验室回答物理可执行性、硬件编排与部署可靠性；ChemWorld 回答 Agent 的实验决策、证据使用和行为结构能否在受控条件下被隔离测量。

ChemWorld 也不是一个只返回目标函数值的优化 oracle。每个实验由有状态 primitive operations 构成；Agent 选择加料、过程控制、表征、终止和 final assay，并在 campaign-wide 资源账本下承担真实机会成本。

当前可独立控制的实验轴包括：

| 干预轴 | 当前实现 | 科学用途 |
| --- | --- | --- |
| 物理身份 | world、material instance、mechanism、keyed noise | 克隆世界、配对与世界异质性 |
| Agent 先验 | opaque、anonymous nominal、misindexed | 受控信息干预 |
| 行动权限 | compiled complete experiment、primitive operations | 低行动权校准与自主主界面 |
| 证据权限 | 仪器选择、测量时机、历史 artifact 访问 | 主动表征与证据响应 |
| 资源 | 原料、溶剂、vessel、instrument、operation、provider | 资源分配和失败进入结果 |
| 复现身份 | config/source/world hashes、immutable attempts、exact replay | 区分物理身份与 Agent 新轨迹 |

第一版的可辩护独占交集是：

1. chemistry-native、stateful、partially observable runtime；
2. Agent 自主选择操作、测量、终止和 final assay；
3. campaign-wide material/instrument/vessel/operation/provider ledger；
4. matched physical identity 下的 paired prior intervention；
5. immutable trajectories、exact replay 与 fixed-world fresh replication；
6. 用 discovery/retention/drawdown/recovery 而非单一 endpoint 研究 Agent。

## 3. 贡献顺序

论文按下列顺序声明贡献：

1. **Executable chemical worlds**：提供有状态、部分可观测、任务约束的化学/化工运行时；
2. **Experimental interaction substrate**：逐操作、主动测量、事务、失败、资源账本、生命周期与回放；
3. **Experimental-intelligence measurement**：把 lifecycle、discovery、retention、recovery、evidence response 与 cognition 分开；
4. **Controlled intervention evidence**：展示任务依赖、先验操纵以及优化—认知解耦；
5. **Fresh-trajectory replication**：揭示 endpoint directionality 与 lifecycle repeatability 的分离。

环境贡献与行为发现必须并列。只讲平台会像软件论文，只讲现象则无法说明为什么过去难以严格测量。

## 4. 证据层级

### 4.1 环境资格

- 15 个注册任务；
- 28 类 operation；
- 5 类 instrument；
- 415 个 deterministic complete-experiment cases；
- 62/62 declared endpoints 绑定 evaluator。

这只证明声明能力、可达性和 evaluator binding，不证明 Agent 在 15 个任务上的性能，也不支持“任意化学”或“无限物理规律”。

### 4.2 G0 compiled control

- classic baselines：1,050 cells、27,300 个物理实验；
- three-arm participant：60 cells、2,280 个物理实验；
- opaque slice 与 v1.0 重用，只计一次；
- 去重总计：29,580 个物理实验。

论文作用：低行动权校准、任务异质性、正确/错误先验干预、优化与 prediction/cognition 端点解耦。G0 不是故事起点，也不与 G2 形成“谁更强”的总体比赛。

### 4.3 G2 v0.4 autonomous development

- 5 worlds × 2 information arms = 10 cells；
- 60/60 vessels 完成；
- 815 个 Agent 自主 primitive operations；
- 164 次 nonfinal characterization + 60 次 final assay；
- 60 provider sessions；
- exact replay、资源账本和物理配对全部通过。

论文作用：证明 Agent 的确逐步完成实验，建立 lifecycle endpoints，并产生需要 fresh trajectories 检验的开发期现象。它是 hypothesis-generating matrix，不用于总体 prior-effect 推断。

### 4.4 G2 v0.5 fresh-trajectory replication

- 固定 world seeds 1 与 3；
- 每个 world 5 个 replicate block；
- 每个 block 配对 opaque 与 anonymous nominal；
- 10 pair blocks、20 cells、120 个预设 vessel opportunities；
- 18 completed cells、2 right-censored cells；
- 114 executed vessels、112 completed final assays；
- 8 complete pairs、2 right-censored pairs；每世界 4 complete + 1 censored；
- 1,615 个 accepted primitive operations；
- attempt selection、physical identity、resource replay、exact replay 全部通过。

证据等级：development-selected, pre-specified fresh-trajectory replication。它回答两个被选择世界内的重复性，不估计一般世界总体 prior effect。

## 5. 终态行为发现

### 5.1 G0：能力不是单一标量

同一 participant scaffold 相对经典方法的表现依赖任务；正确与 misindexed material information 能改变选择，却不统一地产生 recovery。优化得分、held-out directional prediction、Brier calibration、structural/mechanistic declarations 和 unsupported claims 构成不同 profile。

允许结论：optimization 和 cognition endpoints 不可互换。

禁止结论：LLM 普遍优于或劣于 BO。

### 5.2 G2 v0.4：端点掩盖生命周期

Agent 可在 6-vessel campaign 中自主选择操作、表征、停止和 final assay。相似或较高的 best/mean endpoint 可能对应早期发现后丢失、逐步改善、严重回撤或终局恢复等不同轨迹。开发期 nominal arm 平均更晚发现，但 retention 更高、drawdown 更低；一个世界出现反向模式，因此必须复制。

### 5.3 G2 v0.5：端点方向性与生命周期可重复性分离

冻结 outcome-blind mapping 机械选择 `frequent_within_world_reversal`：

- 8 个 world × core-lifecycle 分类中，6 个为 mixed；
- 0/4 core metrics 在两个世界中形成各自稳定、方向相反的模式；
- world 1 的 best 和 mean endpoint 均为 3 正 1 负，但 discovery/retention mixed；
- world 3 的 mean endpoint 为 3 负 1 正，但 best 为 2 正 2 负，四个 lifecycle metrics 全 mixed。

因此不能把 prior response 写成模型或世界的稳定标量属性。更准确的经验描述是：信息、物理上下文和 fresh Agent trajectory 共同决定可观察行为；在当前两个 selected worlds 中，轨迹波动足以频繁翻转 lifecycle effect。

“provider-trajectory variability”是冻结 policy 的原句，但 provider sampling seed 未受控，因此只能描述 fresh-trajectory variability，不能声称 provider 是已识别的因果来源。

## 6. 论文结构

1. Introduction — Experimental intelligence is not an endpoint score
2. Relation to existing systems
3. ChemWorld as an apparatus for studying agents
4. Compiled experiments reveal task- and prior-dependent behavior
5. Optimization, prediction and explanation do not collapse to one competence
6. Agent-directed campaigns expose experimental lifecycles
7. Fresh trajectories test within-world repeatability
8. Discussion
9. Methods
10. Data and code availability

G0/G2 是协议术语，不进入标题和主叙事起点。

## 7. 图表设计

### Figure 1 — ChemWorld is a controlled apparatus for experimental intelligence

展示 closed-loop interaction、可独立控制的 physics/prior/agency/evidence/resources、transaction-to-replay spine 和 qualified environment surface。

### Figure 2 — One complete agent-directed experiment and its ledger

用一个 v0.4 vessel 展示七个自主 primitive operations 与 campaign resource receipt，证明不是固定步骤参数填表。

### Figure 3 — Endpoint summaries conceal distinct trajectories

展示多个 development worlds 的 final-assay sequences、first maximum、loss 与 terminal recovery。

### Figure 4 — Prior interventions reshape behavior without guaranteeing recovery

并列 G0 prior effect、misindexed manipulation/action correction/recovery 与 G2 v0.4 world-wise lifecycle effects。

### Figure 5 — Fresh trajectories test within-world repeatability

显示两个 selected worlds 的全部十个 pre-specified pairs；右删失 pair 用 `x` 保留，不插补。图注必须报告 8 complete pairs、2 right-censored pairs、6/8 mixed classifications 和 selected branch，不合并总体 p 值。

### Figure 6 — Experimental intelligence is a profile, not a scalar

并列 compiled control 的 endpoint/prediction/calibration/unsupported claims 与 autonomous control 的 completion/retention/recovery/terminal-best，禁止构造跨协议 composite score。

主表为：环境与证据范围、G0 capability profiles、G2 v0.4 development summaries、G2 v0.5 all-pair terminal table。

## 8. 主张边界

### 8.1 可写入摘要与主文

- ChemWorld 使实验 Agent 成为可受控、可重复研究的对象；
- Agent 在 stateful chemical world 中自主逐操作、主动测量并承担资源后果；
- endpoint、prediction、cognition 与 lifecycle metrics 不构成单一能力；
- G2 v0.5 中 6/8 core world-metric classifications mixed；
- endpoint directionality 不保证 lifecycle phenotype 可重复。

### 8.2 只能限定性描述

- G0 participant 与经典方法的任务内差异；
- G2 v0.4 的 arm average 与 diagnostic-aligned temporal association；
- G2 v0.5 两个 selected worlds 内的 sign patterns；
- provider sampling 不可控带来的 fresh-trajectory limitation。

### 8.3 禁止主张

- 首个或最完整虚拟化学实验室；
- 任意化学、任意现实反应或无限物理规律；
- 首次 stepwise operation、closed loop、agent behavioral science 或 environment engineering；
- LLM 普遍优于 BO，或 G2 优于 G0；
- correct material information 具有一般总体正效应；
- Agent 形成正确机制理解；
- diagnostic-to-control temporal alignment 是因果反馈效应；
- provider 是轨迹翻转的已识别因果来源；
- 结果可直接迁移到现实机器人实验室。

## 9. 实验数量终态审计

### 9.1 第一版完成量

| Layer | Executed physical experiments | Completed experiments/final assays |
| --- | ---: | ---: |
| G0 | 29,580 | 29,580 |
| G2 v0.4 | 60 | 60 |
| G2 v0.5 | 114 | 112 |
| 合计 | **29,754** | **29,752** |

两次 G2 qualification vessels 和整个第一次被排除的 G2 v0.5 detached launch 均不进入科学总量。

### 9.2 固定机会分母

```text
29,640 existing + 120 pre-specified opportunities = 29,760
```

29,760 不是最终执行数。两个 right-censored cells 各有一个 started-but-incomplete vessel 和三个 never-started slots，因此得到 114 executed 与 112 completed。

### 9.3 还需多少实验

- G0 新实验：0；
- G2 v0.5 新实验：0；
- pending cells：0；
- unresolved opportunities：0；
- optional post-arXiv experiments required for v1：0。

## 10. 剩余发布门禁

### 已解决

- B1 科学矩阵：20/20 terminal，audit passed；
- B4 G0 source binding：四个历史 commits 均存在且为 `origin/main` ancestors；
- B7 figures：frozen derived JSON、6 CSV、Figures 1--6、Tables 1--4；
- G2 terminal data：677-file index 与四-cell replay subset 已生成。

### 仍开放

1. 最终 source commit 后刷新 55-node evidence graph；
2. clean-wheel、full-test、terminal replay；
3. 独立 checkout 重建与一致性验证；
4. 约 17.7 GB G0 raw roots 的持久外部 archive identifier；
5. 参考文献目标格式、statistical-language 和 final-claim audit。

在这些门禁完成前，release manifest 必须保持 `publication_ready=false`。外部 archive identifier 不能伪造；它是目前唯一需要用户或外部服务完成的依赖。

## 11. 第一版摘要逻辑

摘要按六步收束：

1. endpoint 或少量现实实验无法区分 lucky discovery、stable learning 与 evidence use；
2. ChemWorld 提供研究 experimental intelligence 的 executable chemical worlds；
3. Agent 逐操作控制实验、主动测量并承担资源和失败后果；
4. G0 显示 task dependence、prior manipulation 与 optimization–cognition dissociation；
5. G2 显示 endpoint 掩盖 lifecycle，fresh replication 中 6/8 core classifications mixed；
6. controlled chemical worlds 因而成为研究 experimenting agents 的实验装置，而非新 leaderboard。

## 12. arXiv 后路线

按科学价值而非第一版补洞排序：

1. misindexed prior × G2：研究错误先验锁定、修正与 recovery；
2. counterfactual feedback branching：因果分离证据敏感性；
3. 多任务、多模型与可控 provider sampling 复制；
4. world diversity 与规律结构泛化；
5. 窄现实体系 bridge，连接 controlled behavior 与 physical deployment。

这些是下一篇或增强版的经验外推，不是第一版成立的先决条件。

## 13. 最终故事

> **ChemWorld makes scientific agents experimentally measurable. Across compiled and agent-directed chemical campaigns, endpoint performance, prior response, prediction, discovery, retention and recovery do not collapse into a single notion of competence. Fresh trajectories within fixed chemical worlds further show that directional endpoint effects need not correspond to repeatable experimental lifecycles.**

中文：

> **ChemWorld 让科学 Agent 本身成为可被实验研究的系统。编译式与自主化学 campaign 表明，端点性能、先验响应、预测、发现、保持与恢复不能压缩成单一能力；固定化学世界中的 fresh trajectories 进一步显示，有方向性的端点效应并不必然对应可重复的实验生命周期。**
