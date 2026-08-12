# Work II TODO — Experimental Intelligence

最后更新：2026-08-12

当前状态：**正式/R5 participant outcomes 尚未执行；reaction-safety mechanism-oracle Q1、matched-prior
Q2、world-0 D1 与预注册 D2 worlds 1/4 均已完成；electrochemical mechanism-oracle 与 matched-prior Q2
均已通过 5/5 worlds；electrochemical world-0 D1 已完成但为 retained operational failure，当前不进入 D2/R5。**
Reaction-safety D1/D2 共 `9/9` cells、`90/90` experiments、
`630/630` operations、`45/45` checkpoints、`48/48` truth 与 `54/54` blind exact replay，0 platform
failures。结果显示 conflict detection、confidence revision、predictive correction、direction recovery、law
formation、action 和 safety 明显分离；world 4 的注册方向与 16-query empirical direction 冲突，因此 binary
direction 不计分。新的 zero-provider readiness direction gate 已用 world 1/4 回归为 pass/fail，能够在
provider 调用前拦截同类冲突。结果待用户审核；未经审核不进入 R5。
当前 A-E formal design 已从四实验完整重构为八实验：75 个 public cells、600 个 public complete
experiments、375 个 belief checkpoints，并为 private confirmation 保留相同的 600 个实验分母。每个 cell
至少 6 个 unique recipes、最多 2 个 participant-chosen exact repeats；checkpoints 固定为 `0/2/4/6/8`。
五个 task pattern 的 planning resource cards、formal manifest、analysis denominators、power/resource audit 和
preregistration readiness 已同步重建。资源数值仍明确标为 W2-26 calibration 前的 planning envelope，formal
execution 继续锁死。当前 WellAU 三臂 method-qualification readiness 还额外受 W2-26 未完成及四项外部授权要求
阻断；没有启动新的真实 provider call。
W2-31 observation/measurement seed-0 screen 已完成 `24/24` provider-free executions 与 exact replay，
0 physical/platform failures。Electrochemical 通过，而 crystallization 仅因 seed-mass effect 未超过冻结噪声门
被科学拒绝；因此不扩展至五 worlds、不生成 A-O participant D1。若保留 A-O participant claim，需独立重建
至少两个可识别候选，不能降低当前门槛或只保留通过任务。
新的 static reversible-path A-S Q0 已完成 `36/36` paired executions 与 exact replay，0 physical/platform
failures。Reaction-to-crystallization 通过全部 topology gates；flow 的 mechanism binding 正确，但最大公开效应
`0.024–0.054` 低于 UV/Vis gates `0.120–0.135`，因此整体科学拒绝、不扩展五 worlds。该结果明确研究固定世界
中的初始结构认识，不恢复旧“运行中物理变化”故事。

论文作者顺序固定为 **Jiangjie Qiu, Yijun Li, Yaotian Yang, Honghao Chen, Wentao Li, Xiaonan Wang**。
Jiangjie Qiu、Yijun Li、Yaotian Yang 为共同第一作者；Xiaonan Wang 为通讯作者，通讯邮箱为
`wangxiaonan@tsinghua.edu.cn`。稿件 front matter 是作者信息的唯一当前入口，后续构建不得改变顺序、共同一作
标记或通讯作者标记。

## 1. 核心问题与论文边界

中心问题：

> 在隐藏规律固定、公开契约和资源预算匹配的条件下，agent 能否通过自主实验修正初始世界模型，并把证据
> 依次转化为可靠预测、可执行规律、行动和可迁移知识；若不能，能力链在哪一环断裂？

能力链：

`initial model → experiment selection → evidence → prediction/update → executable law → action → transfer`

- Work I 提供可组合世界、有效测量、资源账本、事务语义和 exact replay。
- Work II 的基本实验对象不是“材料提示”，而是外部可执行世界与 agent 初始世界模型之间的可控错配：
  - 外部世界记为 `W = (E, G, Θ, O, C)`，分别表示实体、机制/因果图、参数与动力学、观测映射以及公开契约；
  - agent 初始世界模型记为 `M0 = (Ê, Ĝ, Θ̂, Ô, Ŝ)`，最后一项表示规律的适用域、模块边界与可组合性认识；
  - 同一个 matched cluster 内固定 `W`，只把 `M0` 中一个预注册 locus 设为 opaque、aligned 或
    misspecified，其他信息量、置信度、资源、噪声和安全面匹配。
- 可干预的初始认识不局限于材料名称：
  - **A-E：entity / ontology**，材料、类别、实体关系和属性归属；
  - **A-P：parametric / dynamical**，连续规律、阈值、响应面、最优窗口和 turnover；
  - **A-S：structural / mechanistic**，因果拓扑、主导路径、交互模块和干预后果；
  - **A-O：observation / measurement**，仪器映射、偏差、噪声结构、可靠性和可观测性假设；
  - **D-Scope：scope / compositionality**，某条规律能否跨模块、组合世界或条件域迁移，只在 context-reset
    transfer 中研究，不与同任务 private replication 混同。
- `C` 中的真实预算、安全限制、允许操作和观测接口始终是权威公开契约，不制造错误契约来冒充科学先验；
  否则测到的是 instruction conflict、风险服从或接口理解，而不是世界模型修正。
- 世界可编程定义的是**干预宇宙**，不是全因子执行义务。每个正式比较只改变一个 locus；论文用稀疏、
  机制覆盖导向的代表性 blocks 建立跨层结论，不把 entity、process、mechanism、observation 和 transfer
  一次性全部放开。
- 每个 world 内物理规律保持固定；不把“运行中物理规律变化”作为主问题。
- A-E 是实体层 confirmatory backbone；A-P/A-S 是形成 general initial-world-model claim 所必需的预注册
  non-entity blocks。A-O 先作为独立边界 probe 资格化，不能在看见 participant outcome 后临时并入主结论；
  D-Scope 由 Study D 单独承担。
- 当前 formal participant 只允许 WellAU `gpt-5.6-sol`、medium reasoning、Codex harness + ChemWorld MCP。
  DeepSeek `deepseek-v4-flash` 只用于 development harness 和预实验，结果不能混入 formal denominator。
- 论文结论归属于完整 agent system，不外推为裸模型能力或跨模型排名。

## 2. 冻结执行语义

- 一个 cell 是 `task × world seed × initial-model arm × participant method`。
- 每个 cell 使用一个长驻 Codex process/session；模型在同一上下文中读取公开 outcome，并逐 operation 决策。
- 一个 complete experiment 从新 batch 的首个 vessel-starting operation 开始，以 committed `final_assay`
  或允许的 discard 关闭；`terminate` 本身不等于 final assay。
- 同一 cell 内 experiments 共享 hidden law、session context 和 `CampaignResourceLedger`。新 batch 重置物理状态，
  但历史、已耗资源和剩余预算不重置。
- 独立统计单位是 `task × world seed` cluster；operations、experiments、checkpoints、queries、blind replays
  和 provider retries 都是嵌套观测。
- 三个 arm 为 `opaque / aligned / misspecified`。同一 cluster 内 world、noise、resource、safety、公开契约、
  prior 字数和置信度预算匹配，只改变一个 agent-facing initial-model locus。
- participant campaign 中所有实验均由 agent 自主选择；不插入 protocol-owned diagnostic experiments。
  provider-free oracle screen 不进入 participant 分母。
- provider retry 不产生新科学样本。科学或方法失败保留且不替换；只有尚未形成 scientific trajectory 的纯
  基础设施缺失可按冻结规则 resume 一次。
- 每个正式 task block 最多 5 个预注册 world seeds；超过 5 seeds 必须重新取得用户审核。

## 3. 为什么必须重构当前环境筛选

Reaction-safety parametric development screen 只在固定材料背景上运行了 `4 × 4` 温度—时间网格：

- 温度只有 340/360/390/420 K，时间只有 900/1800/3600/7200 s；
- 当前 reaction-safety vessel 的实际公开可执行范围为 250–470 K、单次 heat 1–14,400 s、100–1200 rpm，另有 catalyst、solvent、
  loading 和 volume；
- 网格内 best 为 420 K/7200 s，位于右上边界，不能证明已经找到内部最优或 turnover；
- best score 仅 `0.1043173`，远低于任务成功阈值 `0.70`；worst 被 score floor 截为 `0`，因此旧 gap
  `0.1043173` 部分来自 floor effect；
- safety risk 只覆盖约 `0.060–0.080`，远低于 limit `0.35`，没有激发安全—产率权衡；
- 旧 prior 是网格内 best point 对 worst point，不是匹配、可信且需要多次实验才能反驳的两种规律模型。

隐藏 world 本身并不简单：reaction-safety 包含 6 species、4 条反应路径、Arrhenius 动力学、催化剂/溶剂/
搅拌修饰、产物降解、催化剂失活、热释放、换热、压力与安全 envelope。当前问题是**机制复杂但实验切片没有
充分激发机制**，不能用“反应数很多”替代有效实验复杂度。

现有每 cell 4 个 experiments 也只适合 harness smoke：二维 `2 × 2` 没有重复、中心点、曲率或独立验证，
而三个 arm 的实际探索覆盖并不对称。因此旧四轮结果可以说明 session、ledger、replay 和基本 prior challenge
可运行，但不能支撑最优窗口识别、规律恢复或机制发现。

## 4. 新的资格漏斗：Oracle → Prior → Participant

任何新 task/locus 必须依次通过下列层级。某层失败即停止；不能看见结果后换阈值、换 world 或只保留有利轨迹。

| Gate | 内容 | Provider | 通过后允许做什么 |
|---|---|---:|---|
| Q0 | mechanism/reachability audit：确认目标机制真实存在、可被公开操作激发、测量可见 | 0 | 进入响应面筛选 |
| Q1 | oracle response-surface qualification：全空间侦察、局部加密、exact replay、复杂度与可达性审计 | 0 | 构造 prior pair |
| Q2 | matched-prior qualification：匹配可信度、基线 utility、反证难度和 blind identifiability | 0 | 生成 D1 config |
| D1 | 1 world × 3 arms persistent-session pilot；同时审计 science、harness、ledger、snapshot 和 evaluator | 3 sessions | 必要时进入 D2 |
| D2 | 仅当预注册触发条件命中时，执行 2 个预注册 worlds；不是默认加样本 | 6 sessions | 提交用户审核 |
| R5 | 用户审核后一次性执行 5-world registered block | 15 sessions/task | 进入论文证据 |

D2 是否需要在 Q1 summary 冻结时决定：只有跨 world response-surface heterogeneity 落入预注册 amber band
才执行。D1 的科学效果方向、H3 数值或 agent 行为不得成为追加 D2 的理由。

legacy DeepSeek reaction-safety D1 的 3/3 terminal、2/3 operationally qualified、12/12 experiments、
4/4 truth、18/18 blind 结果永久保留为 development pilot。aligned arm 连续 2 次 snapshot schema validation
failure 超过冻结上限 1，因此该 D1 不通过；不把它重跑成更有利结果。WellAU matched-prior D1 是后续独立、
已重新资格化的 10-experiment 设计，不替换该 legacy 结果。

### 4.1 Q1：不再用单个 gap 判定环境可分性

每个候选 task 先冻结完整 5-world cohort，不允许逐 seed 挑选。每个 world 使用确定性 namespace 完成：

1. **384 个 broad space-filling recipes**：覆盖该 locus 允许的连续、类别和交互维度；
2. **128 个 adaptive refinement recipes**：围绕候选高质量区、turnover、机制分歧区和安全边界加密；
3. **512/512 exact replays**：不得只复核最优点；
4. 输出机器可读 summary，报告所有失败、完整分母、边界位置、饱和比例和逐指标响应面。

A-P 采用两段式筛选：先在完整可执行空间中寻找满足机制条件的 reference context，再冻结材料、loading 和
stirring；participant cell 只自主改变预注册的两个连续变量。reference context 按下述资格门选择，**不是按
最大 score gap 选择**。这既使用了可编程世界的全空间能力，又保持了 parametric locus 的可解释性。

所有 5 个预注册 worlds 都必须通过；若任一 world 不通过，拒绝整个候选 cohort 或在看 participant outcome
之前整体重建设计，不能只替换失败 seed。

### 4.2 Q1 通用与 locus-specific 资格门

| 维度 | 冻结最低要求 |
|---|---|
| 完整性与 replay | 512/512 recipes 成功关闭且 exact replay；任何失败必须在 participant 前解决并从 Q1 起重跑 |
| 绝对可达性 | 达到 task success threshold 的不同 recipes 占 valid recipes 至少 1%，且绝对数不少于 5；安全任务还必须低于 safety limit |
| 稳健动态范围 | feasible recipes 的 `P90(score)-P10(score) ≥ 0.15`，且至少一个 primary metric 的效应 ≥ `max(0.10, 3σ_noise)` |
| 非饱和 | score floor 和 ceiling 的比例分别不超过 20%；不能主要依靠截断制造 gap |
| 非边界解 | top-5% 区域必须包含连续维度内部点；若最优只在边界，不能据此构造“内部最优/turnover” prior |
| 稳健高质量区 | 达标不能只来自一个孤立点；局部 refinement 中必须形成可重复的 feasible basin/ridge |
| 指标可分性 | prior pair 必须在 prediction metric vector 上可分，而不只在 composite score 上可分 |
| 跨 world | 预注册 5/5 worlds 分别通过；报告 world 间效应方向和幅度，不以平均值掩盖失败 world |

额外的 locus-specific 门：

- **A-E**：至少有两个独立材料/实体对比能改变 primary metric，且不存在一眼可见的全局支配材料。
- **A-P**：目标二维局部响应面至少在两个条件切片上出现可重复的斜率改变或 sign reversal；二阶/交互效应
  必须超过 noise gate，且 optimum ridge 位于可执行内部。
- **Reaction-safety A-P**：oracle 样本必须同时覆盖 safety limit `0.35` 两侧，至少 5% valid recipes 位于
  `[0.30, 0.40]`，并存在低于 limit 且达到 score threshold 的非孤立区域。否则该 world 不适合研究安全规律发现。
- **A-S**：至少两个不同 intervention families 能区分候选机制；baseline endpoint 可以相近，但干预后的
  held-out outcome 必须分离，避免把结构问题退化为材料查表。

### 4.3 Q2：构造匹配、可信、可反驳的 prior

不再使用“oracle 最好点 = aligned、最差点 = misspecified”。三个 arms 的正式语义为：

- **opaque**：不提供目标 locus 的世界模型；其他公开信息与两种 supplied-prior arms 相同。
- **aligned**：提供对真实局部规律的压缩描述，例如 response ridge、条件性交互或“升温先加速、过高温/过长
  时间触发失活和降解”；不直接泄露 oracle optimum。
- **misspecified**：提供初始上合理但可被定向反证的替代规律，例如错误单调性、错误交互方向、错误主导机制
  或系统偏移的 ridge；不能用 score=0、越界或明显不安全点制造一次实验即证伪的 strawman。

每对 aligned/misspecified prior 必须满足：

- schema、字数、置信度和公开 reference context 匹配；
- 在预注册 baseline region 的 predicted utility 差异不超过 `0.05`，避免起点质量完全不匹配；
- 在 held-out surface 至少 25% queries 上发生排序、方向或机制预测分歧；
- 至少存在两个彼此分离的反证区域，且需要至少两次不同干预才能稳健排除错误 prior；
- oracle evaluator 能在 blind labels 下区分两种规律，但 participant prompt 不含 arm identity、oracle score、
  screening seed 或 hidden mechanism name；
- prior pair、query set、pass/failure rules 在 D1 前冻结，D1 outcome 不得反向修改 prior。

## 5. 正式实验矩阵

### 5.1 Study A — prior-conditioned free discovery

| Block | Locus / tasks | Clusters | Sessions | Experiments/cell | Complete experiments | Checkpoints |
|---|---|---:|---:|---:|---:|---|
| A-E public | entity/ontology；5 tasks × 5 worlds | 25 | 75 | 8 | 600 | 0/2/4/6/8 |
| A-E private | sealed within-family replication；5 tasks × 5 worlds | 25 | 75 | 8 | 600 | 0/2/4/6/8 |
| A-P | local parametric；2 tasks × 5 worlds | 10 | 30 | 10 | 300 | 0/2/4/7/10 |
| A-S | structural/mechanistic；2 tasks × 5 worlds | 10 | 30 | 12 | 360 | 0/3/6/9/12 |

A-E 的五个 task family 保持 electrochemical、crystallization、distillation、partition 和 reaction safety；
A-P 当前候选为 electrochemical 与重新设计后的 reaction safety；A-S 需重新产生两个通过 Q0–Q2 的任务候选。
A-O 不直接膨胀当前基线矩阵：先在至少两个 task family 上完成 provider-free identifiability screen 和一个 D1，
再由用户决定是否注册成独立 formal block。即使 A-O 不执行，论文也可以准确声称初始世界模型具有观测层；
但不能声称 agent 已在该层完成修正。D-Scope 只通过 Study D 的 target-context 初始状态与 artifact hand-off 测量。

轮次依据：

- A-E 的 8 轮允许侦察、对比、一次有限重复和独立确认；四轮不足以区分偶然命中与实体关系学习。
- A-P 的二维二阶局部模型至少需要 6 个独立支撑点；10 轮为曲率、交互、重复/验证保留自由度。
- A-S 需要跨多个 intervention families 做因果区分；12 轮避免仅凭单一 endpoint 宣称机制恢复。
- 不建立“materials + process + structure 全部同时自由变化”的混合 A-P。全世界条件模型
  `f(process | material, structure)` 只有在 C2 成立后才作为新研究问题资格化，不能与当前 locus 对比混在一起。

增加实验轮次不会增加独立样本量：A-E 的 primary inference 仍只有 25 个 public clusters。8/10/12 轮的作用是
提高单个 cell 内规律的可识别性并减少“预算太短导致未挑战 prior”的测量失败；统计功效仍按 cluster 计算。
对 A-P/A-S 的 10 clusters 采用 task-stratified/hierarchical analysis，并要求两个 task 的效应方向一致；不把
某一 task 的 5 seeds 当作强单任务显著性证据。

Primary H3 保持为：

`C_prior = (E_misspecified,pre - E_misspecified,final) - (E_aligned,pre - E_aligned,final)`

A-E primary success 同时要求：

- `C_prior > 0` 的预注册单侧 cluster-level inference；
- misspecified arm 自身 held-out prediction error 改善；
- aligned arm 不劣于冻结容差 `-0.05`；
- 失败、缺失和 right-censoring 按预注册规则进入分母。

### 5.2 Studies B–D

- **B — matched-evidence falsification**：2 loci × 1 task × 5 worlds = 10 clusters、30 fresh sessions。
  所有 arms 读取同一 contradictory evidence packet，用于区分 evidence-seeking failure 与 belief-updating
  failure；不属于 free discovery，不增加 physical experiments。
- **C — prediction → law → action evaluator**：不调用 provider，不新增 participant session。统一计算 held-out
  prediction error、typed executable-law error、`L_prediction→law`、`L_law→action`、calibration、blind action
  regret/gain 和 exact replay。endpoint score 只作 secondary outcome。
- **D — context-reset artifact-only transfer**：2 source-pair→target families × 5 targets = 10 clusters；
  none、token-matched raw evidence、prose law、executable law 四 arms，共 40 fresh sessions、8 experiments/cell、
  320 complete experiments。target session 必须是全新 process/context。

D 保持 conditional：C2 未证明规律可被形成和执行前，不启动 transfer。A-E private 是 within-family replication，
不得改称 compositional transfer。

### 5.3 Claim ladder 与累计规模

| Claim | 必需证据 | Sessions | Complete experiments | 允许的最高表述 |
|---|---|---:|---:|---|
| C1 | A-E public + private + C | 150 | 1,200 | entity-level explicit-prior correction |
| C2 | C1 + terminal A-P + A-S，且每 locus 两个 tasks | 210 | 1,860 | cross-locus initial-world-model effects across entity, dynamics and mechanism |
| C3 | C2 + B | 240 | 1,860 | acquisition failure 与 updating failure 的机制区分 |
| C4 | C3 + D | 280 | 2,180 | context-reset compositional transfer of executable laws |

缺少后续 block 时自动收窄标题、摘要和结论；不为维持大标题而补做未资格验证的矩阵。

## 6. Pattern-owned resource contract

不再给所有任务套一个统一 process-time ceiling。每个 task pattern 在 D1 前独立生成并冻结：

`campaign process limit = required stage maxima + allowed repeat stages + protected closeout reserve`

| Block | Experiments | 最少 unique recipes | 允许的 participant-chosen exact repeats | Protected reserve |
|---|---:|---:|---:|---:|
| A-E | 8 | 6 | 2 | 15% time/stock + 每 batch quench/final-assay slots |
| A-P | 10 | 8 | 2 | 15% time/stock + 每 batch quench/final-assay slots |
| A-S | 12 | 10 | 2 | 20% time/stock + transfer/quench/final-assay slots |
| D | 8 | 7 | 1 | 15% time/stock + quench/final-assay slots |

- `required stage maxima` 来自该 pattern 完成必要物理阶段所需的最大时长，不使用历史全局常数。
- `allowed repeats` 是 participant 主动重复配方的科学预算；provider retry、MCP schema retry 和基础设施 resume
  单独记账，永远不是新 experiment。
- closeout reserve 对探索不可支出；当只剩 reserve 时，harness 仅允许 quench、transfer、final assay、discard
  或安全 termination。
- operation attempt、stock、instrument、vessel-start 和 process-time limits 必须由同一 pattern formula 生成，
  防止出现物理时间够但操作数不够，或反之。
- 每种 8/10/12-experiment pattern 先各跑一个 development triplet，验证实际 operation 数、process time、
  snapshot 稳定性、上下文增长和 token 分布，再冻结 formal hard caps。

## 7. 评价框架

每个 locus 都必须分开报告能力链，而不是把 best endpoint 当作“发现规律”：

| 层级 | Primary measurements |
|---|---|
| Experiment selection | 反证信息增益、unique intervention coverage、重复与无效操作比例、resource efficiency |
| Belief update | pre→checkpoint→final held-out prediction error、calibration、错误 prior reliability 下降 |
| Law | typed executable-law error、方向/交互/turnover 恢复、跨 held-out queries 一致性 |
| Action | blind recommendation regret/gain、是否执行自己总结的规律、safety violations |
| Transfer | context reset 后 artifact 对 target prediction、law 和 action 的增益 |

A-P 额外报告 optimum-ridge distance、turnover detection 和局部梯度/交互误差；A-S 额外报告机制模块识别与
干预预测误差；A-E 报告实体关系和跨材料反事实预测。自报 confidence 只作为 calibration 输入，不单独视为修正。

## 8. 资源与 ETA 重新基准化

旧 ETA 来自 4-experiment session：45 scheduled cells、176/180 complete experiments、15 个三臂 triplets，
平均 13.2 min/triplet；当前并发冻结为 3 cells，即同一 world 三臂并发，cell 内不并发。

由于 persistent session 的累计 cached input 会随上下文长度非线性增长，不能把旧 token 表简单乘以 2 或 3。
正式 token/currency ceiling 必须等待 8/10/12-experiment calibration triplets。临时资源规划只采用以下 wall-time
区间，不作为 formal cap：

| Block | Triplets / waves | 理想 | 正常 | 不乐观 |
|---|---:|---:|---:|---:|
| A-E public | 25 | 8–9 h | 12–15 h | 21–30 h |
| A-E private | 25 | 8–9 h | 12–15 h | 21–30 h |
| A-P | 10 | 4–5 h | 6–8 h | 11–15 h |
| A-S | 10 | 5–6 h | 8–10 h | 13–18 h |
| B | 10 short waves | <1 h | 1–2 h | 3–5 h |
| C | local evaluator | <0.5 h | 0.5–1 h | 1–2 h |
| D | 14 three-cell waves | 5–6 h | 7–10 h | 12–18 h |

累计 provider execution 粗估：C1 理想 17–19 h、正常 25–31 h、不乐观 42–60 h；C2 理想 26–30 h、
正常 39–49 h、不乐观 66–93 h。日历时间还必须加入资格筛选、用户审核、public/private 中间冻结和论文整合。

在 calibration 前只允许使用 planning envelope：8-experiment session 约为旧四轮 token 的 2–3 倍，
10-experiment 约 2.5–4 倍，12-experiment 约 3–5 倍；这不是采购预算。最终报告必须拆分 cumulative input、
uncached input、cache-hit input 和 output，不能把 cache token 误解为重复输出。

长任务每 30 秒写 liveness；用户可见更新每 10 分钟一次，至少包含 block、completed/total、throughput、ETA
和最近失败计数。wrapper logs/probes 放在仓库外。

## 9. 当前证据的定位

| Evidence | 结论 | 新矩阵中的状态 |
|---|---|---|
| electrochemical parametric v2 screen, seed 1 | 20/20 exact replay；旧 gap `0.5849161` | 需按 Q1/Q2 五-world 响应面门重新资格化 |
| electrochemical D1, WellAU seed 1 | 3/3 cells、12/12 experiments；descriptive H3 `+0.0173` | development evidence；不自动扩展 |
| electrochemical D1, DeepSeek seed 1 | 3/3 cells、12/12 experiments；descriptive H3 `-0.0025` | operational pass；未观察到科学修正 |
| electrochemical mechanism-oracle v0.2, seeds 0–4 | `14,160/14,160` outcomes completed；`120/120` validation replay；0 physical/platform failures；5/5 worlds pass | Oracle score `0.770–0.849`、relative basin `36–68`、strong potential/current direction and curvature；历史 `0.58` threshold 每 world 有 `877–1,597` 个点达到。授权 Q2；因未激发安全边界，只用于参数规律结论。 |
| electrochemical matched-prior Q2 v0.3, seeds 0–4 | `605/605` completed；`180` safe fit、`425` safe held-out；0 physical/platform；5/5 worlds pass | 五个 world 均选择 lower-controlled-potential law；aligned MAE `0.122–0.152`、blind margin `0.095–0.445`、disagreement `73/85`；supplied priors 均为 127 words 且只改 directional claim。授权 world-0 D1 static readiness，不授权 provider/R5；无 heterogeneity-triggered D2。 |
| electrochemical matched-prior WellAU D1, world 0 | `2/3` terminal scientific trajectories；`0/3` qualified；`20/30` experiments、`180` operations、`8/15` checkpoints；`16/16` truth exact replay；`0/18` blind（缺 final recommendation）；0 physical/platform execution failures | opaque/aligned 中间 checkpoint prediction error 分别 `0.2907→0.0902`、`0.2503→0.1429`，但最终 checkpoint/recommendation 均缺失；misspecified 在 physical operation 前因 5 次 snapshot contract failures 中止。保留为 retained operational failure；不支持错误先验纠正、final law、H3 或 R5。详见 `WORK_II_ELECTROCHEMICAL_MATCHED_PRIOR_D1_ANALYSIS_ZH.md`。 |
| current WellAU method-qualification readiness | zero provider calls；3 qualification cells；6 provider-attempt hard cap；`formal_execution_authorized=false` | readiness 内部校验通过，但缺 provider contract confirmation、credential rotation confirmation、pricing/currency ceiling 和真实 triplet；不得启动 provider。 |
| reaction-safety old screen, seed 0 | 16/16 exact replay；旧 gap `0.1043173` | 不满足新 absolute-quality、interior、non-saturation 与 safety-frontier gates |
| reaction-safety Q1-v0.2, seeds 0–4 | 表面为 2,560/2,560 final assays 与 exact replay；事后逐 operation 审计发现 403/2,560 recipes 的 heat 因使用通用 `520 K` 而非任务可执行 `470 K` 上限被拒绝（357 broad、46 adaptive） | 平台缺陷导致该 block 无法作 scientific rejection；旧 artifact 永久保留为 defective development audit，但 `0/5`、floor saturation、local structure 与 adaptive 结论均不得继续作证据。修复后的 Q1-v0.3 与独立 mechanism-oracle block 均须从 world 0 开始。 |
| reaction-safety Q1-v0.3, seeds 0–4 | 2,560 attempted；2,557 recipes 全 operation committed 且 exact replay；3 个 schema-valid heat 触发动态 `vessel_temperature_bound` rollback；0/5 worlds pass；max score `0.291–0.433`；45–81 safety-frontier recipes/world | 有效 absolute-Q1 scientific rejection：3 个 clean worlds 仍独立失败 absolute reachability、floor saturation、local structure 与 success basin；动态范围与 primary-metric range 成立。禁止据此进入原 Q2，但允许执行已独立冻结的 mechanism-oracle relative question。 |
| reaction-safety mechanism-oracle v0.1, seeds 0–4 | `14,121/14,121` unique requests classified；`13,878` committed endpoints；`243` dynamic constitution failures；`120/120` noisy validations exact replay；0 platform failures；1/5 worlds pass | 五个 world 的 oracle optimum、relative basin、dynamic/primary range、local law、frontier 与 observed agreement 全通过；4 个 world 仅因把 physical failure 计作 incomplete 而失败。v0.1 正式拒绝且不进入 Q2；冻结只修正分类语义的 v0.2 后从 world 0 重跑。 |
| reaction-safety mechanism-oracle v0.2, seeds 0–4 | `14,121/14,121` outcomes classified；`13,878` committed endpoints；`243` physical failures；0 platform/unclassified；`120/120` validation replay；5/5 worlds pass | 与 v0.1 的全部科学数值逐 world 完全一致，唯一变化为 outcome classification gate；确认五个 world 均存在安全 relative basin、可识别 local law 与充分 frontier，授权进入 reaction-safety Q2 matched-prior construction。历史 `0.70` 仍无任何点达到。 |
| reaction-safety matched-prior Q2, seeds 0–4 | `605/605` surface queries classified；`64` physical failures；0 platform failures；`150` safe fit、`391` safe held-out；5/5 worlds pass | 五个 world 均形成基线匹配但可反驳的温度方向 prior：baseline gap `0.00050–0.01608`、held-out disagreement `48.1–53.8%`、blind margin `0.267–0.284`；supplied priors 均为 149 words 且只改 directional claim。前两次科学结果相同但 D1 config 被旧 arm-ID/四-checkpoint 硬编码静态拒绝，未启动 provider；最终 pattern-owned harness 与 D1 config 已通过静态预检，授权 reaction-safety D1。 |
| reaction-safety matched-prior WellAU D1, seed 0 | `3/3` qualified；`30/30` experiments；`210/210` committed operations；`15/15` checkpoints；`16/16` truth 与 `18/18` blind exact replay；0 platform failures | misspecified error `0.1785->0.1361`、reliability `0.70->0.20` 且持续定位 temperature，但方向未恢复；aligned `0.1052->0.1107` 并从正确方向更新到错误方向；三臂 endpoint 近似相同。推荐动作层因可见 0-based/commit 1-based 冲突而混淆，原提交保留，D2 起已统一 1-based。 |
| reaction-safety matched-prior D2 world 1 | `3/3` qualified；`30/30` experiments；`210/210` committed operations；`15/15` checkpoints；`16/16` truth 与 `18/18` blind exact replay；4 unsafe、0 physical、0 platform failures | 三臂最终均恢复真实 higher-temperature 方向；misspecified error `0.1386->0.0344`，但 reliability `0.70->0.85` 且无 challenged field，显示预测纠正与显式先验拒绝分离；aligned 独有 4 个 unsafe outcomes，D1 的 supplied-prior safety 信号未复现。 |
| reaction-safety matched-prior D2 world 4 | `3/3` qualified；`30/30` experiments；`210/210` committed operations；`15/15` checkpoints；`16/16` truth 与 `18/18` blind exact replay；0 unsafe、0 physical、0 platform failures | 三臂 prediction 均改善；nominal misspecified reliability `0.70->0.35` 且持续挑战 temperature，但两个 supplied-prior law errors 为 `0.3816/0.5054`。注册 lower-temperature 与 16-query empirical higher-temperature 冲突，修复 evaluator 后 binary direction 标为 not scored，participant 未重跑。 |
| reaction-safety DeepSeek D1, seed 0 | 3/3 terminal、2/3 qualified；descriptive H3 `+0.1005` | retained operational failure；不重跑 |
| 首批 crystallization/partition structural screens | module gap 分别 `0.0069301`、`0.0744505` | 拒绝；不能解释为 agent 推理失败 |
| W2-28 structural candidate screen v0.1 | `180/180` provider-free、`180/180` exact replay、0 physical/platform failures | diagonal validation 同时改变两个干预轴，Q2 identification contract 无效；不作科学 rejection；两项 candidate 从 world 0 重跑 |
| W2-28 structural candidate qualification v0.2 | `180/180` provider-free、`180/180` exact replay、0 physical/platform failures；electrochemical `3/5` worlds pass、crystallization `0/5` | electrochemical 五 world 均有强 current/potential response，但 world 0/3 的 Q2 disagreement 仅 `2/9`；crystallization cooling `5/5` 通过而 seed effect 仅 `1/5` 通过、Q2 disagreement `0/9`；两项均不生成 D1。详见 `WORK_II_STRUCTURAL_CANDIDATE_QUALIFICATION_ANALYSIS_ZH.md` |
| W2-31 observation/measurement Q0 | 五类 spectral instruments、pH、三种 disclosure conditions 与 request-only archive 的 `12/12` controls 通过；0 provider | 观测层同时保留可识别、不可识别和低信号退化区域，允许进入两个 task family 的 seed-0 provider-free screen；不授权 participant/D1。详见 `WORK_II_OBSERVATION_MODEL_Q0_ANALYSIS_ZH.md` |
| W2-31 observation/measurement seed-0 screen | `18/18` noisy + `6/6` truth，`24/24` exact replay；0 physical/platform/unsafe；electrochemical pass、crystallization reject | Electrochemical transport/Faradaic/energy effects 明显超过噪声门；crystallization seed-mass 的最大 CSD effect `0.0390 < 0.0950`，yield `0.0143 < 0.0303`。保留科学拒绝，不扩展五 worlds，不生成 D1。详见 `WORK_II_OBSERVATION_SCREEN_ANALYSIS_ZH.md` |
| static reversible-path A-S seed-0 Q0 | `36/36` paired executions/exact replay；0 physical/platform/unsafe；crystallization pass、flow reject | 两任务均正确增加固定 reverse target channel，且 action/noise 完全配对。Crystallization yield/conversion/selectivity effects 为 `0.1757/0.0730/0.1703`，yield accumulation `0.1176`；flow 最大效应仅 `0.0245/0.0269/0.0538`，低于 UV/Vis gates。保留科学拒绝，不扩展。详见 `WORK_II_STATIC_TOPOLOGY_Q0_ANALYSIS_ZH.md` |

正式 A-E 尚未执行，因此可以在不污染 participant outcomes 的情况下把 4 轮改为 8 轮；但已有 formal design、
analysis plan、manifest preflight 和 power/resource 文件在重新生成前只视为历史 planning artifacts，不能作为执行授权。

## 10. 下一执行顺序

### P0 — 先把环境和 prior 做对

- [x] **W2-21** 写一个 concise experiment note，冻结 Q0–Q2 的 5-world coverage、512 recipes/world、指标、
  pass/failure rules 和输出文件。
- [x] **W2-22** 实现 provider-free oracle response-surface runner 与 readable machine summary；
  reaction-safety Q1-v0.2 因 403 个未提交 heat operations 被判定为平台缺陷、结论失效；修复后的
  Q1-v0.3 已从 world 0 完整重跑并作为 absolute qualification 被拒绝。当前执行独立冻结的
  reaction-safety 与 electrochemical 当前 relative mechanism-oracle blocks 均已完整运行；absolute reaction-safety
  rejection 与 relative qualification 分开保留，不再要求 electrochemical 重复一条已由相对资格替代的旧 absolute route。
- [x] **W2-23** 按预注册 lexicographic gates 选择 reference context，构造 matched aligned/misspecified laws，
  完成 blind leakage/identifiability audit；reaction-safety 与 electrochemical Q2 均为 5/5 worlds、605/605
  classified、0 platform failures。Reaction-safety D1 静态预检已通过；electrochemical 当前待独立 readiness。
- [x] **W2-24** reaction-safety 三臂 D1 与预注册 D2 worlds 1/4 均已完成 participant、provider-free
  evaluator 和综合分析。world 4 direction diagnostic 冲突已隔离；其他通过 Q2 的 task 仍须分别完成 D1。
- [ ] 用户审核 D1/D2、轨迹样例、资源和 evaluator 结果；未经审核不进入 R5。
- [x] **W2-30** 完成 electrochemical matched-prior WellAU world-0 D1 participant/evaluator 审计；失败轨迹、
  中间 checkpoint 信号、model/platform 归因和 evaluator 修复均已冻结。未经用户审核不得重启新的 D1 block。
- [x] **W2-28** A-S provider-free qualification 已完成 v0.2：2 tasks × 5 worlds、`180/180` exact replay、0
  physical/platform failures。v0.1 因 diagonal validation 轴混杂被标为 analysis-contract defect 并从 world 0
  重跑；v0.2 的 electrochemical 只通过 `3/5` worlds，crystallization 通过 `0/5`，所以不生成
  12-experiment D1 config、不进入 participant/R5。下一步只能另行冻结可识别的新 candidate；不得降低
  `6 sigma` 或 `40%` gates，也不把 observation-model/scope 扩展加入本分母。A-O 仍需独立 identifiability/D1
  决策卡。
- [x] **W2-29** 运行 mechanism-oracle relative qualification：先直接求 reaction-safety 的安全相对最优、
  Pareto/局部规律和独立 noisy replay，再以同一原则审计 electrochemical。旧 Q1-v0.2 artifact 永久保留为
  platform-defect audit，不再称为 scientific rejection；historical leaderboard threshold 只作诊断，不直接改值。
- [x] **W2-31** A-O observation/measurement Q0 与 two-task seed-0 screen 均已完成。Seed 0 为 `24/24`
  completed/exact replay、0 physical/platform/unsafe；electrochemical 通过，crystallization 因 seed-mass
  effect 低于冻结噪声门被科学拒绝。按预注册规则不扩展到 seeds `0–4`、不生成 participant D1。若继续 A-O，
  必须独立冻结新的双任务候选；不得只扩展 electrochemical 或降低当前门槛。
- [x] **W2-32** static reversible-path A-S seed-0 Q0 已完成：batch crystallization 与 continuous flow
  各 9 个 grid cells × baseline/reversible laws，共 `36/36` completed/exact replay、0 physical/platform。
  Crystallization 通过全部 topology/accumulation gates；flow 因公开效应低于 UV/Vis 噪声门科学拒绝。
  按冻结规则不扩展五 worlds；若继续 A-S，需把保留的 crystallization 与一个新的独立 task 候选重新组对，
  不得放大当前 intervention、降低门槛或删除 flow 结果。

### P1 — 重冻正式矩阵

- [x] **W2-25** A-E formal design 已从 4 改为 8 experiments/cell；checkpoints 为 `0/2/4/6/8`，每 cell
  至少 6 个 unique recipes、最多 2 个 exact repeats。五个 planning resource cards、analysis denominators、
  manifest preflight、power/resource audit、method-qualification readiness 与 preregistration readiness 已同步重建；
  formal execution 仍被 W2-26/W2-27 和用户授权锁死。
- [ ] **W2-26** 实验 note 已写入 `WORK_II_RESOURCE_CALIBRATION_EXPERIMENT_NOTE.md`；待用户确认当前
  provider/credential/pricing/currency 边界后，分别运行 8/10/12-experiment resource calibration triplet，
  冻结 task-pattern process time、repeat count、closeout reserve、token 和 currency ceilings。
- [ ] **W2-27** 完成 current WellAU method qualification triplet，只按 harness/lifecycle/replay 资格，不按科学效果。
- [ ] 用户冻结 submission route、currency ceilings、failure-escalation 和 public/private 执行授权。
- [ ] 生成 final freeze receipt；此后不再改变 coverage、worlds、arms、轮次或 failure rules。

### P2 — 执行与条件扩展

- [ ] 执行 A-E public 25 triplets；只报告 blinded progress，完成后冻结 public analysis hash。
- [ ] 一次性解封并执行 A-E private；不得因 public 结果方向调整。
- [ ] 完成 Study C 和 C1 analysis。
- [ ] 只有两个 A-P 和两个 A-S tasks 都通过完整资格漏斗后，才执行 C2 registered blocks。
- [ ] 只有确需区分 seeking 与 updating 时执行 B；只有 C2 成立且保留 transfer claim 时执行 D。

## 11. Task tracker

| Work package | 状态 | 说明 |
|---|---|---|
| W2-01–06 | DONE | scope、questions、cohort、estimands、participant contract |
| W2-07–11 | REOPENED | 旧 4-experiment resource/design freeze 被新矩阵替代，需在 W2-25–27 后重新关闭 |
| W2-12–14 | NOT STARTED | A-E public/private 与 confirmatory analysis |
| W2-15 | DOING | manuscript skeleton/figures 已有；formal results 待补 |
| W2-17–18 | DOING | non-entity qualification；转由 W2-21–24 管理 |
| W2-19 | CONDITIONAL | matched-evidence probe B |
| W2-20 | CONDITIONAL | artifact-only transfer D |
| W2-21 | DONE | five-world oracle qualification note 已冻结 |
| W2-22 | DONE | provider-free response-surface runner 与 readable summaries 已完成；reaction-safety absolute rejection 和两个 task 的 relative qualification 分层保留 |
| W2-23 | DONE | reaction-safety 与 electrochemical matched-prior Q2 均以 5/5 worlds 通过；baseline、disagreement、双反证区域、blind identification、word/schema matching 与 leakage gates 全通过 |
| W2-24 | DONE | reaction-safety world-0 D1 与 D2 worlds 1/4 participant/evaluator 已完成；综合结论待用户审核 |
| W2-25 | DONE | 8-experiment A-E formal redesign；600 public experiments、375 checkpoints、6 unique + 2 repeats/cell；静态审计通过，资源上限待 W2-26 校准 |
| W2-26 | READY/BLOCKED | calibration experiment note 已完成；等待 provider contract、credential rotation、pricing/currency ceiling 授权后执行 |
| W2-27 | READY/BLOCKED | current WellAU method qualification triplet 已完成零 provider readiness；等待显式 provider contract、credential rotation、pricing/currency ceiling 授权 |
| W2-29 | DONE | reaction-safety 与 electrochemical mechanism-oracle 均已 5/5 通过；electrochemical 当前授权进入 Q2 matched-prior construction |
| W2-30 | DONE | electrochemical matched-prior WellAU world-0 D1 已完成并完成 provider-free evaluator；`failed_retained`，中间 checkpoint 信号和失败归因已冻结，未经用户审核不重启新 block |
| W2-31 | DONE | Q0 `12/12` controls passed；seed-0 screen `24/24` completed/exact replay，electrochemical pass、crystallization scientific reject；按冻结规则不扩展、不生成 D1 |
| W2-32 | DONE | static reversible-path seed-0 Q0 `36/36` completed/exact replay；crystallization pass、flow scientific reject；固定世界语义通过，整体不扩展 |

## 12. 不可违反的规则

- 不根据 participant outcome 选择、删除或新增 task/world/arm。
- qualification 修复平台缺陷后，受影响 qualification block 从第一单元重跑；已经形成的 scientific trajectory
  永不替换。
- participant trajectory 与 evaluator truth/blind trajectory 严格分离，资源和分母不混用。
- endpoint success 不等于 law discovery；文字总结不等于 executable law；自报 confidence 不等于 belief update。
- 一项 locus 只有一个 task 达到终态时，只能作为 task-specific case study。
- private within-family replication 不能支持 compositional transfer；C4 未完成时标题和摘要不得声称 transferable laws。
- raw provider payload、credentials、`runs/`、private seeds 和 local cache 不进入 Git。

## 13. 当前证据入口

- Formal design（W2-25 八实验设计）：`configs/benchmark/work_ii_formal_design_v0.1.json`
- Analysis plan（W2-25 八实验分母）：`configs/benchmark/work_ii_analysis_plan_v0.1.json`
- Power/resource audit（W2-25 planning envelope）：`workstreams/flagship_tasks/reports/work-ii-analysis-power-audit.json`
- Formal preflight（600 public experiments；execution blocked）：`workstreams/flagship_tasks/reports/work-ii-formal-matrix-runner-preflight-v0.1.json`
- WellAU development timing：`workstreams/flagship_tasks/reports/work-ii-three-task-five-seed-campaign.md`
- Electrochemical parametric reports：
  `workstreams/flagship_tasks/reports/work-ii-parametric-initial-model-diagnostic-seed1-v2-20260811.json`、
  `workstreams/flagship_tasks/reports/work-ii-parametric-initial-model-pilot-evaluation-20260811.json`、
  `workstreams/flagship_tasks/reports/work-ii-deepseek-parametric-initial-model-pilot-evaluation-20260811.json`、
  `workstreams/flagship_tasks/reports/work-ii-mechanism-oracle-electrochemical-classified-v0.2-20260811.json`、
  `workstreams/flagship_tasks/WORK_II_ELECTROCHEMICAL_MECHANISM_ORACLE_ANALYSIS_ZH.md`、
  `workstreams/flagship_tasks/reports/work-ii-electrochemical-matched-prior-qualification-20260811.json`、
  `configs/benchmark/work_ii_electrochemical_matched_prior_package.json`、
  `configs/benchmark/work_ii_electrochemical_matched_prior_d1.json`、
  `workstreams/flagship_tasks/WORK_II_ELECTROCHEMICAL_MATCHED_PRIOR_ANALYSIS_ZH.md`
- Structural/non-entity screens：`workstreams/flagship_tasks/reports/work-ii-structural-initial-model-diagnostic-20260811.json`、
  `workstreams/flagship_tasks/reports/work-ii-crystallization-structural-screen-20260811.json`、
  `workstreams/flagship_tasks/reports/work-ii-partition-structural-screen-20260811.json`
- Reaction-safety screen/evaluator：
  `workstreams/flagship_tasks/reports/work-ii-reaction-safety-parametric-screen-20260811.json`、
  `workstreams/flagship_tasks/reports/work-ii-deepseek-reaction-safety-parametric-pilot-evaluation-20260811.json`、
  `workstreams/flagship_tasks/reports/work-ii-q1-reaction-safety-five-world-20260811.json`、
  `workstreams/flagship_tasks/reports/work-ii-q1-reaction-safety-five-world-v0.3-20260811.json`、
  `workstreams/flagship_tasks/reports/work-ii-mechanism-oracle-reaction-safety-five-world-20260811.json`、
  `workstreams/flagship_tasks/reports/work-ii-mechanism-oracle-reaction-safety-classified-v0.2-20260811.json`、
  `workstreams/flagship_tasks/reports/work-ii-reaction-safety-matched-prior-qualification-20260811.json`
- Reaction-safety matched-prior package / D1 config：
  `configs/benchmark/work_ii_reaction_safety_matched_prior_package.json`、
  `configs/benchmark/work_ii_reaction_safety_matched_prior_d1.json`、
  `workstreams/flagship_tasks/reports/work-ii-reaction-safety-matched-prior-d1-evaluation-20260811.json`、
  `workstreams/flagship_tasks/WORK_II_REACTION_SAFETY_MATCHED_PRIOR_D1_ANALYSIS_ZH.md`

Git history 保存本文件过去的详细任务卡和运行日志；不恢复并行的旧主控入口。
