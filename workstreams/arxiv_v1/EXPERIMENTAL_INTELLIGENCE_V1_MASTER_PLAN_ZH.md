# ChemWorld 第一版 arXiv 总规格：可执行化学世界中的实验智能

状态：`authoritative working plan; claims remain evidence-bounded`

工作标题：**Experimental Intelligence in Executable Chemical Worlds**

机器总账：`workstreams/arxiv_v1/reports/experimental-intelligence-experiment-ledger-v0.1.json`

G2 v0.5 当前执行源码：`main@aae0edac12c849bc4246ca5ac9359a2d00d9f660`

第一次启动基础设施中断记录：`workstreams/arxiv_v1/G2_V05_EXECUTION_INCIDENT_2026_08_01_ZH.md`

相关工作审计：`workstreams/arxiv_v1/RELATED_WORK_AUDIT_2026_08_ZH.md`

## 0. 决策摘要

第一版论文不再以“从 recipe optimization 走向 G2”作为叙事。ChemWorld 的核心贡献是把实验智能本身变成可操作、可干预、可重复测量的对象：Agent 在隐藏物理世界中选择操作和表征，承担资源与失败后果，并通过完整轨迹暴露其发现、保留、回撤、恢复、预测和先验响应。

内部 G0/G2 术语只保留在协议和方法中：

- G2 `closed_loop_primitive` 是论文主实验界面；
- G0 `compiled_recipe` 是低行动权校准与既有先验干预证据，不是故事起点；
- G1 是开发期接口诊断，不进入论文科学本体；
- 不进行“G2 是否胜过 G0”或“LLM 是否胜过 BO”的总体胜负叙事。

第一版唯一新增科学矩阵 G2 v0.5 的第一次 detached 启动因宿主进程中断被整体排除并原样保留。
同一冻结协议已于 2026-08-01 23:51（Asia/Shanghai）从干净的 `aae0edac` commit 写入新目录，
以前台托管方式完整重启：20 cells、120 个 fresh-vessel 实验机会、120 个原生 Codex sessions。
运行期间只读监控，不依据中途结果改变顺序、停止或重抽样。G0 不需要新科学实验。旧的
matched G0/G2 40-cell 矩阵和 G2 三臂扩展均移到 arXiv 之后。

## 1. 科学对象与中心问题

### 1.1 科学对象

本文研究的对象不是某个优化器的排行榜位置，而是 **experimental intelligence**：

> 一个 Agent 在部分观测、有限资源和有后果的干预中选择实验、使用证据、修正策略并完成实验生命周期的能力结构。

实验智能至少分为六个不可互换的维度：

1. **Lifecycle autonomy**：能否自主建立、推进、结束并 final-assay 一个实验；
2. **Discovery**：何时首次发现高质量条件；
3. **Retention**：发现后是否能保持接近 incumbent 的性能；
4. **Recovery**：回撤后是否、何时重新达到冻结阈值；
5. **Evidence response**：表征之后是否改变可比较控制，以及结果如何变化；
6. **Cognitive reliability**：预测、校准、结构声明和不受证据支持的断言是否可靠。

### 1.2 中心问题

主问题不是“Agent 最后拿到多少分”，而是：

> **终点性能是否足以刻画一个正在做实验的科学 Agent？如果不足，哪些实验行为维度是可重复的，哪些依赖具体物理世界、先验和单次模型轨迹？**

对应四个研究问题：

- **RQ1 — Endpoint underdetermination**：相似的 best/mean score 是否可以来自不同的发现、回撤和恢复轨迹？
- **RQ2 — Prior intervention**：材料信息首先改变终点分数，还是改变实验选择与轨迹稳定性？
- **RQ3 — World-conditioned repeatability**：相反的 seed 1/seed 3 行为模式能否在固定世界内跨 fresh trajectories 重现？
- **RQ4 — Optimization–cognition dissociation**：优化、held-out prediction、声明可靠性和性能恢复是否给出一致能力排序？

RQ1、RQ2 和 RQ4 目前已有 G0/G2 开发证据；RQ3 是 G2 v0.5 的唯一新科学实验目标。

## 2. ChemWorld 的方法学定位

### 2.1 不是机器人实验室的替代品

现实自动化实验室主要回答设备编排、现实可执行性和部署可靠性。ChemWorld 主要回答实验决策、证据使用和科学行为能否在受控条件下被隔离测量。

本文不声称：

- sim-to-real；
- 工业数字孪生；
- 任意真实化学反应预测；
- 任意物理规律生成；
- 真实仪器队列、审批或异步结果申请已经实现。

### 2.2 作为研究 Agent 的实验装置

ChemWorld 允许分别控制：

| 干预对象 | 当前可用控制 | 本文作用 |
|---|---|---|
| 物理世界 | seed、材料实例、有限机制/参数变化、keyed noise | 配对、重复和世界异质性 |
| Agent 先验 | opaque、anonymous nominal、misindexed | 行为操纵和先验依赖 |
| 行动权 | compiled complete experiment、primitive operations | 低行动权校准与主实验界面 |
| 测量 | 仪器选择、时机、历史 spectrum 访问 | 主动表征和时间对齐行为 |
| 资源后果 | 原料、容器、仪器机会、操作尝试、成本、风险 | 资源分配与失败进入结果 |
| 可重复性 | world/config/source hash、immutable attempt、exact replay | 区分物理身份与轨迹随机性 |

一句话定位：

> **The agent is the subject; the chemical world is the apparatus.**

## 3. 贡献声明

论文按以下顺序声明贡献：

1. **Executable chemical worlds**：有状态、部分可观测、带任务合同的化学/化工运行时；
2. **Experimental interaction substrate**：逐操作、主动测量、事务、失败、资源账本、生命周期和回放；
3. **Experimental-intelligence measurement**：把 discovery、retention、recovery、evidence response、cognition 和 utility 分开；
4. **Controlled behavioral evidence**：G0 中的任务异质性、先验操纵和优化—认知分离；G2 中的自主实验轨迹；
5. **Trajectory-level replication design**：在固定物理世界中分离 world identity 与 fresh provider trajectory。

平台贡献与行为发现必须并列：只有平台而没有现象会像软件论文；只有现象而没有运行时则无法说明为何此前不能严格测量。

## 4. 证据层级

### 4.1 环境资格

- 15 个注册任务；
- 28 类 operation；
- 5 类仪器；
- 415 个 deterministic complete-experiment cases；
- 62/62 个声明端点绑定 evaluator；
- 仅证明可执行性与端点设计，不证明 15 任务 Agent 性能。

### 4.2 G0 正式描述性证据

非重复 active corpus：

- 1,050 classic baseline cells、27,300 次物理实验；
- 60 个 opaque/nominal/misindexed participant cells、2,280 次物理实验；
- 合计 1,110 cells、29,580 次物理实验。

Opaque 是 v1.0 participant 的复用切片，不能再次把 v1.0 的 760 次实验加到总数。

证据等级：正式描述性结果，但各 arm 与 baseline 来自多个历史 source commit。发布前必须统一重认证或随每个 arm 发布精确 source snapshot。

### 4.3 G2 v0.4 开发行为证据

- 5 worlds × 2 arms = 10 cells；
- 60/60 fresh vessels 完成；
- 815 个自主 primitive operations；
- 164 次非终点表征，加上 60 次 final assay，共 224 个 `measure` 操作；
- 60/60 provider sessions；
- 0 invalid/resource rejection；
- exact replay、资源账本和物理配对审计全部通过。

证据等级：完整审计的开发性 hypothesis-generating matrix。可以展示行为现象和冻结后续指标，不能从 n=5 单轨迹 worlds 推断总体先验效应。

### 4.4 G2 v0.5 fresh-trajectory replication

- 固定 seed 1、seed 3；
- 每个 world 5 个 fresh trajectory replicate；
- 每 replicate 两个 information arms；
- 10 pair blocks、20 cells、120 个实验机会；
- 旧 v0.4 trajectory 用于 seed/metric 选择，不进入 fresh estimand。

证据等级：development-preregistered selected-world replication。它回答两个被选择世界内的重复性，不估计一般世界总体信息效应。

## 5. 当前行为结果与允许解释

### 5.1 G0：任务异质性

| Task | Participant | strongest information-matched classic | paired difference |
|---|---:|---:|---:|
| Electrochemical | .7150 | Structured RF-EI .6159 | +.0991 `[+.0103,+.1748]` |
| Crystallization | .5355 | LHS .5708 | −.0353 `[−.0650,−.0085]` |

允许解释：同一 Agent/scaffold 的相对表现依赖化学任务。禁止解释：Codex 普遍优于或劣于经典优化。

### 5.2 G0：正确与错误先验

| Task | Opaque | Nominal | Δ nominal | familywise 97.5% interval |
|---|---:|---:|---:|---:|
| Electrochemical | .7150 | .7874 | +.0724 | `[+.0074,+.1546]` |
| Crystallization | .5355 | .5615 | +.0260 | `[−.0130,+.0630]` |

错误先验在两任务中都通过早期行为操纵，但都没有通过联合恢复规则。允许解释：先验改变行动；行为纠偏、认知纠偏和性能恢复不是同一个事件。禁止解释：结晶 misindexed 分数较高证明 Agent 发现先验错误。

### 5.3 G0：优化—认知分离

电化学与结晶在 final score、held-out directional accuracy、Brier、declared accuracy、edge/mechanism F1 和 unsupported claim rate 上呈不同排序。该结果用于展示可分解端点，而不是建立普遍 Agent 心理学定律。

### 5.4 G2 v0.4：发现—保留—恢复

| Arm | discovery progress | online retention | max drawdown | terminal/global best | losses recovered/unresolved |
|---|---:|---:|---:|---:|---:|
| Opaque | 32% | 52% | .3326 | 67% | 3/3 |
| Nominal | 80% | 72% | .0915 | 94% | 4/1 |

当前候选结构是：nominal 未必更早发现自身最佳，却更常保留已获得性能并以接近历史最佳的状态结束。seed 3 对 retention、drawdown 和 terminal/global-best 反向，因此不能写成总体稳定规律。

## 6. G2 v0.5 的冻结分析

### 6.1 统计单位

统计单位是 `fixed physical world × fresh trajectory replicate`。每个 replicate 的 nominal/opaque 共享物理 evaluator、观测流、资源卡、模型配置和本地 agent seed；provider sampling randomness 不可冻结且两 arm 独立。

### 6.2 主要轨迹端点

运行前已冻结：

- global-best discovery fraction；
- 90% online incumbent retention；
- maximum absolute drawdown from prior incumbent；
- terminal-to-global-best ratio；
- loss episode、recovery、recovery delay 和 terminal unresolved。

### 6.3 联合报告端点

- lifecycle completion/right-censor；
- best 和 mean final score；
- batch running-best AUC；
- realized-operation running-best AUC；
- fixed-144-operation running-best AUC；
- operations、measurements、stocks、sessions、tokens；
- diagnostic-aligned control change 到下一 final score 的时间对齐描述。

最后一项不是因果反馈估计。本文不能写“测量导致改进”，只能写“在含诊断后可比较控制变化的 batch 中，下一 final score 的时间对齐方向”。

### 6.4 报告规则

- 每个 world 单独列出 5 个 nominal-minus-opaque replicate；
- 报告 median、min/max、正负号计数与 sign consistency；
- seed 1 与 seed 3 不合并成总体 p 值；
- completed 与 right-censored 全部进入总账；
- 不因 interim score、arm difference 或叙事方向停止；
- 只有 `provider_infrastructure_failure && accepted_operation_count == 0` 可按冻结规则重试；
- 动作后的失败永久 right-censored，不替换。

### 6.5 三种结果分支

1. **world 内稳定、world 间相反**：支持 world-conditioned experimental phenotype；
2. **world 内频繁翻转**：支持单次 autonomous trajectory 不足以刻画实验智能；
3. **部分端点稳定**：支持实验智能具有不同稳定性层级，例如 endpoint 不稳定而 retention 稳定。

三种分支都保留；没有“必须复现 nominal 优势”的成功判据。

## 7. 第一版主张账本

### 7.1 可以写入摘要/主文

- ChemWorld 实现任务约束下的有状态、逐操作、部分可观测和可回放化学过程交互；
- Agent 能主动选择测量并根据公开结果继续当前实验；
- 15 个任务的 complete-experiment design 与 62 个端点通过资格审计；
- G0 双任务结果展示任务依赖的优化表现、先验操纵和优化—认知端点分离；
- G2 v0.4 展示原生 Codex 可以自主完成多容器电化学 campaign；
- 相同/相近 endpoint 可以对应明显不同的 discovery、retention 和 recovery trajectories；
- v0.5 在两个选定世界内测量这些轨迹结构的 fresh-trajectory repeatability。

### 7.2 只能写入 Results/Limitations 的限定性发现

- nominal 在 v0.4 五世界平均具有更高 retention、更低 drawdown；
- seed 3 的反向结果；
- diagnostic-aligned control changes 的下一批结果方向；
- G0 中 participant 与经典方法的描述性差异。

### 7.3 禁止主张

- ChemWorld 是首个或最完整的虚拟化学实验室；
- 能生成任意物理规律或任意现实化学；
- LLM 普遍优于 BO；
- G2 优于 G0；
- nominal 材料信息具有一般总体正效应；
- Agent 形成了正确机制理解；
- 时间对齐的诊断—改控关系是因果效应；
- 当前结果迁移到现实机器人实验室或工业系统。

## 8. 图表冻结设计

### Figure 1 — A controlled laboratory for experimental intelligence

**问题**：ChemWorld 新增的科学对象是什么？

Panels：

- A：hidden chemical world → operation → state transition → measurement → next action；
- B：可独立控制的 physics/prior/agency/evidence/resources；
- C：typed state、transaction、resource ledger、immutable trajectory、exact replay；
- D：当前覆盖边界：15 tasks、28 operations、5 instruments、415 cases、62 endpoints。

状态：系统数据已具备；需要新绘图。

### Figure 2 — One autonomous experiment

**问题**：Agent 是否真正逐步做实验？

使用成功 opaque K1 qualification 或 v0.4 代表 cell：显示加料、setpoint、pH/UV–vis、重复电解、terminate、final assay，以及同步资源余额。

状态：数据已具备；qualification 只能标为 infrastructure demonstration，不进入效应统计。

### Figure 3 — Endpoint-equivalent trajectories are behaviorally distinct

**问题**：终点分数为何不足？

Panels：seed 0、2、4 的 running final scores；标出 discovery、loss、recovery、terminal unresolved。将相近 best/mean 但轨迹形状不同的 arm 并列。

状态：G2 v0.4 已具备。

### Figure 4 — Prior interventions reshape behavior without guaranteeing recovery

**问题**：先验影响的是什么？

Panels：

- G0 nominal information value by task；
- misindexed early/late misleading-action share；
- manipulation/correction/performance recovery 三组件；
- G2 v0.4 discovery/retention/drawdown/terminal-best paired world differences。

状态：已有数据；必须并列显示任务/世界异质性。

### Figure 5 — Within-world replication of experimental behavior

**问题**：行为结构在 fresh trajectories 中是否可重复？

Panels：seed 1、seed 3 各5个 paired replicate；主要轨迹端点的 dot/range/sign；完成与右删失状态。

状态：缺 G2 v0.5 的20 cells/120实验。

### Figure 6 — Experimental-intelligence profiles

**问题**：优化、预测、行为稳定和认知是否是同一个能力？

展示 endpoint utility、completion、retention/recovery、held-out prediction、calibration 和 unsupported claims。只能按 task/world/experiment layer 展示，不能制造跨协议综合总分。

状态：部分具备；最终布局待 v0.5。

### Main tables

1. Table 1：环境和交互能力及证据等级；
2. Table 2：G0 双任务与三臂核心结果；
3. Table 3：G2 v0.4/v0.5 completion、资源和轨迹端点；
4. Extended Data：逐 world/replicate、right-censor、provider/resource accounting。

## 9. 论文结构

1. **Introduction — Experimental intelligence is not an endpoint score**
2. **ChemWorld as a controlled apparatus for studying scientific agents**
3. **Agents act in stateful chemical worlds**
4. **Task and runtime qualification**
5. **Prior knowledge changes experimental choices without guaranteeing recovery**
6. **Autonomous agents discover, lose and recover experimental performance**
7. **Within-world replication separates physical context from trajectory randomness**
8. **Experimental-intelligence profiles dissociate optimization and cognition**
9. **Discussion and limitations**
10. **Methods, audit and release**

G0 的 recipe protocol 放在第5节的方法入口，不作为第1—3节的历史起点。

## 10. 摘要蓝图

摘要必须按以下六句逻辑写：

1. AI scientist 常由终点结果或少量现实实验评估，难以区分幸运发现、稳定学习和证据使用；
2. ChemWorld 是一个用于研究实验智能的有状态、可执行化学世界；
3. Agent 可以逐操作控制实验、主动选择表征并承担资源和失败后果；
4. G0 受控先验实验显示任务依赖、行为操纵与恢复分离；
5. G2 显示相似 endpoint 可对应不同的 discovery/retention/recovery dynamics，并用 fresh trajectories 测量其稳定性；
6. ChemWorld 因而提供了研究科学 Agent 行为的受控方法，而不是新的总体算法排行榜。

在 v0.5 完成前，第5句必须保留占位符，不能提前写稳定方向。

## 11. 实验数量审计

### 11.1 已完成并计入第一版科学语料

| Layer | Physical experiments |
|---|---:|
| G0 classic baselines | 27,300 |
| G0 three-arm participant | 2,280 |
| G2 v0.4 autonomous development | 60 |
| 合计 | **29,640** |

Qualification 的2个 attempted vessels不计入科学语料；其中1个完成、1个动作后右删失。

### 11.2 唯一必需的新科学矩阵

| Layer | Cells | Physical experiment opportunities | Provider sessions |
|---|---:|---:|---:|
| G2 v0.5 replication | 20 | **120** | 120 |

因此第一版完成后的非重复科学物理实验总量预计为：

```text
29,640 existing + 120 new = 29,760
```

如果出现预注册 right-censor，120 是计划实验机会而不是强制120个成功 final assay；失败必须留在分母。

### 11.3 不属于第一版必需实验

- 旧 matched G0/G2：40 cells，按 K6 约240次实验；
- G2 opaque/nominal/misindexed 三臂：30 cells，约180次实验；
- true/masked/delayed/permuted feedback branching：尚未单独预注册；
- 更多任务、world、provider 或现实 bridge。

这些不能悄悄加入首版分母，也不能延迟首版发布。

## 12. 非实验发布阻断

### B1 — G2 v0.5 正在运行

第一次 detached 启动已按预定规则整体排除；干净的前台托管重启已开始。只有 20/20 cells
终态化且通过 fail-closed audit 后，120 个 experiment opportunities 才能进入正文。

### B2 — Evidence graph 未闭合

`scripts/evidence_pipeline.py --check` 当前失败五项：source fingerprint、runtime affordance freshness/gate、stale count 和 stale identities。

### B3 — Release 为空

`benchmark/releases/chemworld-serious-v1` 当前没有可发布工件。

### B4 — G0 source binding 已解决

classic、opaque、nominal、misindexed 所绑定的四个历史 commit 均存在且都是 `origin/main`
祖先。无需把多 commit 本身误判为失效；剩余任务归入 B5 的 raw archive 与公开哈希索引。

### B5 — Raw data 未发布

`runs/` 本地存在但被 Git 忽略。至少需要：derived cell table、trajectory/receipt hash index、可 replay subset、完整 archive URL 和 data card。

### B6 — 新稿骨架已建立，但内容尚未闭合

旧的 `paper/chemworld_benchmark_manuscript.md` 已标记 superseded；新的
`paper/experimental_intelligence_v1_manuscript.md` 已建立完整论证骨架。当前剩余阻塞是
G2 v0.5 正式结果、完整 Methods、参考文献和最终图表尚未填实，而不再是叙事结构缺失。

### B7 — 图表流水线缺失

必须建立单一 frozen derived table 和自动出图脚本；禁止手工复制摘要数字。

## 13. 执行顺序与完成判据

### Phase A — 本轮文稿冻结

- 新主计划、机器实验总账和新 manuscript skeleton 进入 main；
- 旧稿标记 superseded；
- 所有数字有来源路径或明确 placeholder。

### Phase B — G2 v0.5 运行

- clean main commit；
- foreground-supervised process；
- 10/10 frozen pair dry-run；
- 不看 interim 故事方向；
- 20 cells 全部进入 completed、right-censored 或 audit-required terminal state。

### Phase C — Postrun audit

- manifest/hash/attempt/replay/resource/provider 全部 fail-closed；
- 每个 world 有5个 replicate 状态；
- 缺失、重复或选择性替换直接阻止论文结果表；
- 生成 JSON、中文审计和 frozen derived rows。

### Phase D — Evidence/release closure

- evidence pipeline pass；
- G0 recertification/source archive；
- clean wheel/full tests/independent checkout；
- release目录、data card、hash index、replay subset完成。

### Phase E — Manuscript freeze

- v0.5 三结果分支之一进入 Figure 5；
- abstract不越过证据等级；
- 全部图从单一 derived table生成；
- 对外术语使用 compiled control / agent-directed control，不以 G0/G2 作为标题叙事。

## 14. arXiv 后路线

首版之后再决定：

1. misindexed prior × G2，研究错误先验锁定与恢复；
2. counterfactual feedback branching，因果分离证据敏感性；
3. 多任务/多 provider 复现；
4. world diversity 或规律结构泛化；
5. 窄现实系统 bridge。

这些属于更强经验规律或更高层级论文，不是首版环境—行为论文的启动条件。

## 15. 最终故事

第一版完整后，应能够以证据约束的方式说：

> **ChemWorld makes scientific agents experimentally measurable. Across compiled and agent-directed chemical campaigns, endpoint performance, prior response, prediction, discovery, retention and recovery do not collapse into a single notion of competence. By repeating autonomous trajectories inside fixed chemical worlds, ChemWorld separates properties of the physical context from the stochastic behavior of the experimenting agent.**

中文：

> **ChemWorld 让科学 Agent 本身成为可以被实验研究的系统。现有编译式与自主化学 campaign 表明，终点性能、先验响应、预测、发现、保留和恢复不能压缩为单一能力；固定物理世界中的多轨迹重复进一步区分世界条件与实验 Agent 的随机行为。**
