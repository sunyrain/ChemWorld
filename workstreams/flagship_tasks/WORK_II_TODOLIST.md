# Work II TODO — Experimental Intelligence

最后更新：2026-08-17

## 0. 已冻结的执行理念：开发优先、最后一次冻结

Work II 默认处于 **development mode**，直到功能、候选机制、测量契约和完整实验矩阵均稳定，且用户明确授权
正式证据生产。开发期间优先推进平台功能与科学设计；全树 SHA、clean-worktree、preregistration readiness、
evidence graph、release qualification 和旧 Gate A 证书均不是新增功能、定向测试或明确标注的 development
experiment 的前置条件。旧审计或哈希因合理的新功能失效时，将其标为 stale/historical，留到最终 release freeze
统一重建，不在每次改动后循环修复。

开发态仍不可放松的部分是实验本身：数据产生前必须有简洁 experiment note；一旦 block 启动，不得按结果修改
问题、coverage、分母、测量、阈值、失败/停止规则；必须保留全部失败、exact replay、资源账本和机器可读 summary，
不得用更有利的重跑覆盖旧结果。Development evidence 可以用于调试和设计，但不会自动升级为 formal evidence。

只有进入 **release-freeze mode** 后，才一次性完成：冻结最终执行面、建立最小必要 source binding、生成 prereg/
release audit、运行正式 qualification，并在同一冻结 cohort 上进入 participant/formal/private execution。绑定范围
必须限于真正影响 runtime/evaluator 的代码与配置；测试、论文、无关配置和历史报告不得仅因目录便利被纳入全树
hash。此理念优先于本文件中历史遗留的“每次开发改动后重建审计/SHA”表述。

当前状态：**DeepSeek C2 public participant 已终态，当前有效组合为 `135/135` sessions、
`1,243/1,260` experiments、`121/135` qualification；registered current-composite evaluator v0.2 recovery 已完成
`420/420` truth executions、`675/675` checkpoint scores、`135/135` law evaluations 与 `726/726` launched
blind replays，0 provider calls。7 failed、7 right-censored 和 84 个未启动 blind 分母均保留。三个 locus 的
selective-correction gate 均未通过；A-P `p=0.079` 仅属 suggestive。A-E private 延期，
WellAU/Qwen/Kimi 未启动新的 replication。Paper 2 当前结果统一从 `WORK_II_PAPER_RESULTS_ZH.md` 进入，
当前论文故事见 `paper/prior_discovery_story_zh.md`。** Reaction-safety mechanism-oracle Q1、matched-prior Q2、world-0 D1
与预注册 D2 worlds 1/4 均已完成；electrochemical mechanism-oracle 与 matched-prior Q2 均通过 5/5 worlds，
electrochemical world-0 D1 为 retained operational failure，不进入 D2/R5。
Matched-evidence 当前有效证据已终态：A-P Study B 保留 `5/5` clusters、`15/15` fresh sessions、`30/30`
provider turns；A-S B2 完成 `5/5` clusters、`15/15` fresh sessions、`30/30` provider turns、`80/80`
provider-free truth，均为 0 failures、0 participant physical experiments。A-P 的错误方向先验在 5/5 worlds 被固定
反证明确定推翻，支持 evidence-acquisition component。A-S B2 的 misindexed-minus-aligned update-gain contrast 为
`+0.0645`、3/5 worlds 为正、exact one-sided sign-flip `p=0.125`，但 misindexed 0/5 恢复 exact 1.75 law，
因此收束为 acquisition、numerical revision 与 structural identification 三层分离，而不是 seeking/updating 二分。
原 Study B A-S truth source 未实际应用冻结 world intervention，该 15-session 分支保留为历史缺陷证据并退出当前 claim。
已完成的材料信息三臂是 Work II 的前置实体层证据，不属于已经投稿的 Work I 基座论文结论：它包含
electrochemical/crystallization、10 worlds、opaque/nominal/misindexed 三臂共 `60/60` cells 与 `2,280`
physical experiments，全部 exact replay。Electrochemical 的正确匿名材料属性相对 opaque 提升 `0.0724`，
错位先验相对正确先验降低 `0.1020`；crystallization 的正确信息效应不确定，错位先验却提高 sampled-world
endpoint。两任务均未通过预注册 overall recovery claim，因此该基线证明初始信息会改变探索和结果，但不证明
agent 能稳定摒弃错误材料先验。
Reaction-safety D1/D2 共 `9/9` cells、`90/90` experiments、
`630/630` operations、`45/45` checkpoints、`48/48` truth 与 `54/54` blind exact replay，0 platform
failures。结果显示 conflict detection、confidence revision、predictive correction、direction recovery、law
formation、action 和 safety 明显分离；world 4 的注册方向与 16-query empirical direction 冲突，因此 binary
direction 不计分。新的 zero-provider readiness direction gate 已用 world 1/4 回归为 pass/fail，能够在
provider 调用前拦截同类冲突。结果待用户审核；未经审核不进入 R5。
当前 A-E formal design 已从四实验完整重构为八实验：75 个 public cells、600 个 public complete
experiments、375 个 belief checkpoints，并为 private confirmation 保留相同的 600 个实验分母。每个 cell
至少 6 个 unique recipes、最多 2 个 participant-chosen exact repeats；checkpoints 固定为 `0/2/4/6/8`。
五个 task pattern 的 planning resource cards、formal manifest 与 analysis denominators 已同步重建。旧
power/resource audit 只描述 v0.1 的 calibration 前 planning envelope，现已退役；当前资源上限只从 W2-26
task cards 进入执行面。current WellAU 三臂 method qualification 已终态通过，但 formal execution 继续受
W2-26 未完成、private-seal 迁移和 release 用户授权阻断；formal/R5 尚未启动。用户授权的 W2-34
development block 已独立完成 2 个真实 provider sessions，
不进入 formal denominator。
W2-31 observation/measurement seed-0 screen 已完成 `24/24` provider-free executions 与 exact replay，
0 physical/platform failures。Electrochemical 通过，而 crystallization 仅因 seed-mass effect 未超过冻结噪声门
被科学拒绝；因此不扩展至五 worlds、不生成 A-O participant D1。若保留 A-O participant claim，需独立重建
至少两个可识别候选，不能降低当前门槛或只保留通过任务。
新的 static reversible-path A-S Q0 已完成 `36/36` paired executions 与 exact replay，0 physical/platform
failures。Reaction-to-crystallization 通过全部 topology gates；flow 的 mechanism binding 正确，但最大公开效应
`0.024–0.054` 低于 UV/Vis gates `0.120–0.135`，因此整体科学拒绝、不扩展五 worlds。该结果明确研究固定世界
中的初始结构认识，不恢复旧“运行中物理变化”故事。
W2-33 reaction-safety catalyst-deactivation static A-S seed-0 Q0 已完成 `54/54` executions 与 exact replay，
0 physical/platform/unsafe。Stable catalyst 在全部 27 cells 的 direct metrics 上方向一致，但最大 yield/
conversion/selectivity gaps 仅 `0.00615/0.00563/0.00532`，远低于 `0.050/0.050/0.054` gates；duration
accumulation 也低于门槛。该候选为任务—机制可辨识性科学拒绝，不扩展五 worlds。
W2-34 双真实-provider campaign 已按澄清后的定义完成：失活/稳定世界各 1 个 WellAU
`gpt-5.6-sol` medium 持久 Codex session，每个 `8/8` experiments，共 `16/16` experiments、`112/112`
operations、`2/2` session exact replay，0 provider/platform failures。两个自主 session 的同轮闭环终点在
`5/8` 轮至少一项、`4/8` 轮至少两项超过 W2-33 reference gate，但两边从第一轮即选择不同 recipe，不能作
物理因果归因。全部 16 个 provider-selected recipes 的双定律 `32/32` paired replay 显示最大 yield/
conversion/selectivity 纯物理 gaps 仅 `0.01026/0.01226/0.00899`，分别为 gate 的
`0.205x/0.245x/0.167x`，0/16 超门。因此保留“闭环轨迹可显著分岔”的观察，但不声称真实 provider 已使
固定配方机制差超过 gate，不推翻 W2-33 科学拒绝。

W2-40 原 full-32-prediction 纵向方案从未执行，现已归档并移除独立 launcher。它按隐藏真实名次从 128-grid
抽取候选，同时把机制测量和综合决策捆绑在 32 项 terminal prediction 中；不再是当前设计入口。其候选网格
配置仅因 W2-43 历史 canary 的可解释性保留，并显式标为 historical input。

W2-41 保留为 terminal schema 历史诊断：`6/6` retained sessions、`4/6` completed；进入 terminal 的样本中
full-32 相对 ranking-only 增加约 `35,164 vs 2,368` output tokens，证明完整数值表操作负担过高，但不单独
估计 action quality。

W2-42 保留为 fixed-context 历史诊断：`6/6` records、`4/6` completed；所有完成样本即使获得正确
`FAMILY_B_POWER / exponent=1.75` law，仍选择真实第 5 名，平均 normalized regret `0.5418`。它证明旧 packet
不是单机制可识别动作题，但不否定现实多维综合决策。

W2-43 是当前有效的真实纵向 canary：`3/3` same-thread sessions、`36/36` autonomous experiments、
`15/15` checkpoints、`3/3` ranking-only terminal readouts，0 collisions/provider/platform failures。三臂选择
真实第 `8/3/1` 名，说明单一 world 同时混合探索策略、直接经验和局部外推；它验证接口和行为可观测性，
不支持 arm-level 结论。

W2-44–W2-46 strict exponent-sensitive matched-action 支线终态：合计 `800/800` truth 与 exact replay、
0 failures、0 provider calls；修正版仍仅 `2/20` contrast×world、`0/5` rosters 通过。负结果、配置和 note
保留，独立 launchers、专用实现和专属 tests 已退役；不再恢复近似 crossover 主路径。

W2-47 已归档为 **HISTORICAL / PROTOCOL-DIAGNOSTIC ONLY**：单 world 三臂 development run 完成
`36/36` participant experiments 与 `24/24` provider-free truth/replay，但 terminal packet 只公开
feature values，未公开完整 executable action plan；因此不作为 action-quality 证据。

W2-48 五世界开放动作 development 矩阵已终态：`15/15` persistent sessions、`180/180` 自主实验、
`120/120` provider-free truth 与 `120/120` exact replay，public/truth plan binding 通过；`13/15` cells
eligible，2 个 campaign/checkpoint 不完整单元保留在分母。`0/15` 选择真实 Top-1；opaque/aligned/
misindexed 的 eligible mean rank 为 `4.25/6.50/6.60`，mean normalized regret 为
`0.3671/0.7658/0.7477`。2 个 terminal readout 为 adequate-law/wrong-action，13 个为
inadequate-law/wrong-action。该结果验证完整 ActionPlan 纵向协议并暴露 action-transfer 缺口，但因属
development 且只有 3 个完整三臂 clusters，不作 arm-level formal claim，也不为追求完整率补跑。

W2-49 多任务 open-action development 资格已完成当前收束。资源契约按 pilot 已观察到的 stock/time
失败类别冻结修正并从首 arm 重跑后，electrochemical 与 reaction-to-crystallization 最新 block 各为
`3/3` eligible、`36/36` experiments、`16/16` truth 与 replay；原 pilot 中 reaction-safety-constrained
为 `3/3` eligible、`36/36` experiments、`16/16` truth 与 replay。三个额外任务的最新未污染 blocks
合计 `9/9` eligible、`108/108` experiments，证明 full-plan/ranking-only harness 可跨任务运行；均为
单世界 development evidence，不作 prior-arm 泛化。

2026-08-12 平台/设计收束快照：当前正式预检继续诚实锁定为 `75` cells、`25` clusters、`600`
experiments，`formal_execution_allowed=false`，并显式保留 `11` 个未满足门禁。C2 的 outcome-blind task
selection 已改为受保护的事前协议，分别冻结 A-P 的 reaction-safety/electrochemical 与 A-S 的 partition/
reaction-to-crystallization 候选及排序；动态结果只能填写终态资格 disposition，不能自行宣称候选表或规则已预冻结。
D1 admission 现在还要求 action layer 可解释且未替换 participant recommendation，因而历史 reaction-safety
confounded D1 与 electrochemical incomplete D1 均不能误入正式矩阵。严格 A-S five-world runner、validator、
12-experiment D1 生成器与实验 note 已完成但尚未执行；发布测试 roster 现为 `29` files / `225` tests。

2026-08-12 development qualification 更新：两项 A-P matched-prior Q2 已在新 development execution mode
从头完成，reaction-safety 与 electrochemical 均为 `605/605` classified、`5/5` worlds 通过且 0 platform
failures；两项仅生成未授权执行的 D1 静态配置，不能升级为 release evidence。A-E prior-distinguishability
qualification 已完成 `300/300` executions 与 exact replay，0 physical/platform failures，但仅 `14/50` regions、
`5/25` task-worlds、`0/5` tasks 通过，因此原 A-E block 科学拒绝。诊断同时发现现有三指标平均会稀释仅由一个
注册指标承载的强可观测反差、paired-noise 坐标会使左右 recipe 的噪声近乎完全抵消、8-round reachability
只证明 oracle recipe 数量可容纳而未证明盲策略可达；该结果保留，不原样重跑、不放宽阈值，另写 v0.2 新问题。
v0.2 已冻结为 construction/held-out 各 600 primary、合计 `1,200` primary + `1,200` exact replay，采用独立
左右噪声、事前 support/control 指标分离和真实八轮盲诊断策略。首次 development 启动在 `167/1,200` 后因
contract/plan/receipt/trajectory 最小直接绑定与篡改校验不完整而主动停止；167 条完成记录原样保留但不构成科学
结果。该缺陷不改变 v0.2 科学问题、coverage 或阈值；修复资格 validator 后必须从 execution 0 全块重跑。
停止过程另有 2 条在途执行完成，最终落盘为 `169` completed receipts、0 failed、无 report；该 partial 仍整体
视为 defective development audit。新 deterministic held-out 25 worlds 已在任何 v0.2 科学结果产生前冻结为
未来 prospective formal public participant cohort；旧 public 25 worlds 降为 exposed construction-only，永不
进入 participant denominator。Formal design、C2、preregistration 与 release 入口须在重跑前同步这一 cohort
语义；旧 audit/preflight 标 stale，留到最终 release freeze 一次重建。

2026-08-13 v0.2 从 execution 0 完整重跑并通过运行时对应版本的独立落盘复核：`1,200/1,200`
primary、`1,200/1,200` tolerance-zero exact replay、0 physical/platform failures、validator `0` errors。该块是
有效的 scientific rejection，不是缺失分母或平台中断：held-out 中 crystallization 与 partition 均
`5/5` worlds 通过，electrochemical `1/5`、distillation `0/5`、safety `3/5`，整体 `2/5` tasks
通过而拒绝五任务普适 A-E claim。`150/150` policy replicates 均完成 8 rounds、8 unique recipes、
两 anchor 的全部四类覆盖，因此不是 reachability 失败。所有 held-out 失败 anchor 均首先因
mean support separation `<0.05`；distillation 的全部 held-out anchor 仅 `0.00487–0.01932`，原 solvent
pair 不具备足够物理可识别性。v0.2 结果原样保留，不降阈值、不重用已暴露 worlds；若继续 A-E，
必须把全部 v0.2 worlds 降为 exposed construction，先做 task/locus 的物理 oracle 资格，再冻结全新
prospective held-out cohort 与 v0.3 问题。正式 A-E participant matrix 不得基于 v0.2 升级。
进一步语义复核确认：v0.2 盲 policy 未读取 permutation 并完成全类覆盖，但 hidden analyzer
事后读取真实 pair 只计算该 pair 的 contrast，未在 6 个 transposition hypotheses 中盲选。因此
positive cells 只证明 analyzer-specified pairwise locus separability，不证明 blind pair identification；negative
result 仍有效，因为它连盲识别的必要物理可分条件都未满足。v0.3 候选开发须冻结一个
不读 permutation 的 classifier，枚举 H0 + 6 个 row-transposition hypotheses，仅依据 agent-visible
dossier、事前 primary endpoints 和两 task-aware anchors 输出 pair 或 abstain，真实 pair 只供离线计分。
候选 screen 可覆盖全五任务，但 Paper2 的正式 claim 应改为事前限定的 qualified-locus claim；若
仍坚持五任务 universal claim，须先使五个 loci 在全新 prospective worlds 全部通过。

2026-08-13 A-E v0.3 development qualification 的完整四阶段设计与执行入口已通过独立数学和科学复核，
当前状态为 **DESIGN READY / NOT YET EXECUTED**。固定分母为 classifier fit `14,400` primary +
`14,400` exact replay、untouched validation `14,400 + 14,400`、prospective screen `1,200 + 1,200`，
以及 confirmation `120 x selected_task_count` primary + replay。后续阶段必须由上一阶段的 deterministic
plan、完整 raw receipts 和重建 report 直接解锁；仅自哈希 summary/report 不能解锁。41 项聚焦测试、Ruff、
plan-only `14,400/14,400` 与单 execution final-assay/replay smoke 均通过；smoke 不进入任何科学分母。
此 development block 不生成 audit package 或 release hash inventory，正式证据仍等待最终 release-freeze。

严格 A-S 的旧 partition load-by-phase-volume Q0 保留科学拒绝。新的 nominal-pair partition Q0 已在执行前
冻结为完整 `4 x 4` categorical solvent-by-extractant 表，并完成 `32/32` primary 与 `32/32` exact replay，
0 physical/platform/unsafe failures。Final-assay 与 HPLC 的公开 allocation log-ratio slopes 分别为 `1.5224`
和 `1.4895`，均越过冻结的 `abs(slope - 1) >= 0.20` 门；4 个 product-allocation channels 满足至少
`8/16` pairs 的效应门。该 Q0 只授权进入不变的 five-world provider-free qualification，不授权 D1/C2。

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
- 已投稿的 Work I 只承担基座/仪器贡献；材料信息三臂、规律先验三臂以及后续 A-E/A-P/A-S/A-O/B/C/D
  均作为 Work II 证据组织，不回写为 Work I 的实验主张。
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
- 用户已将当前 formal participant 改为 DeepSeek `deepseek-v4-flash`、high reasoning、Codex harness +
  ChemWorld MCP；WellAU 暂停。旧 DeepSeek development/calibration 结果仍不混入 formal denominator，新的
  prospective cohort 使用独立 world identities 和单独终态存储。
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
  failure；不属于 free discovery，不增加 physical experiments。当前有效 block 为 A-P 原 Study B 15 sessions 与
  A-S B2 15 sessions：A-P 支持 evidence acquisition component；B2 给出 mixed positive prediction contrast，
  同时 0/5 exact structural-law recovery。原 Study B A-S 分支因 evaluator truth 缺陷降为 historical。
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
当前 B/B2 已全部执行并终态。C3 的二元跨-locus 强主张不受支持；允许的结论是 A-P acquisition component 与
A-S structural-identification bottleneck 并存，且 B2 的 prediction-level contrast 为 mixed/weak。该结果是终态科学
处置，不再追加同类 B2 追求更有利方向。

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
| material-information triarm baseline | electrochemical/crystallization、10 worlds、3 arms，`60/60` cells exact replay；三臂共 `2,280` physical experiments | Work II 的已完成实体层前置证据。Electrochemical nominal−opaque `+0.0724`、misindexed−nominal `−0.1020`；crystallization nominal−opaque `+0.0260` 且不确定、misindexed−nominal `+0.0229`。两任务 overall recovery 均失败，不能声称稳定摒弃错误先验；不属于已投稿 Work I 的结论。 |
| electrochemical parametric v2 screen, seed 1 | 20/20 exact replay；旧 gap `0.5849161` | 需按 Q1/Q2 五-world 响应面门重新资格化 |
| electrochemical D1, WellAU seed 1 | 3/3 cells、12/12 experiments；descriptive H3 `+0.0173` | development evidence；不自动扩展 |
| electrochemical D1, DeepSeek seed 1 | 3/3 cells、12/12 experiments；descriptive H3 `-0.0025` | operational pass；未观察到科学修正 |
| electrochemical mechanism-oracle v0.2, seeds 0–4 | `14,160/14,160` outcomes completed；`120/120` validation replay；0 physical/platform failures；5/5 worlds pass | Oracle score `0.770–0.849`、relative basin `36–68`、strong potential/current direction and curvature；历史 `0.58` threshold 每 world 有 `877–1,597` 个点达到。授权 Q2；因未激发安全边界，只用于参数规律结论。 |
| electrochemical matched-prior Q2 v0.3, seeds 0–4 | `605/605` completed；`180` safe fit、`425` safe held-out；0 physical/platform；5/5 worlds pass | 五个 world 均选择 lower-controlled-potential law；aligned MAE `0.122–0.152`、blind margin `0.095–0.445`、disagreement `73/85`；supplied priors 均为 127 words 且只改 directional claim。授权 world-0 D1 static readiness，不授权 provider/R5；无 heterogeneity-triggered D2。 |
| electrochemical matched-prior WellAU D1, world 0 | `2/3` terminal scientific trajectories；`0/3` qualified；`20/30` experiments、`180` operations、`8/15` checkpoints；`16/16` truth exact replay；`0/18` blind（缺 final recommendation）；0 physical/platform execution failures | opaque/aligned 中间 checkpoint prediction error 分别 `0.2907→0.0902`、`0.2503→0.1429`，但最终 checkpoint/recommendation 均缺失；misspecified 在 physical operation 前因 5 次 snapshot contract failures 中止。保留为 retained operational failure；不支持错误先验纠正、final law、H3 或 R5。详见 `WORK_II_ELECTROCHEMICAL_MATCHED_PRIOR_D1_ANALYSIS_ZH.md`。 |
| current WellAU method qualification | 3/3 arms terminal；各 8/8 experiments；exact replay 48 steps/arm、0 mismatches；receipt validator 0 errors | development qualification 已通过且 `formal_execution_authorized=false`；authorization、cost、receipt 与 local manifest 直接校验，重复 readiness 投影已退役。 |
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
| reaction-safety catalyst-deactivation A-S seed-0 Q0 | `54/54` completed/exact replay；0 physical/platform/unsafe；stable law 在 27/27 cells 方向一致 | 最大 yield/conversion/selectivity gaps `0.00615/0.00563/0.00532`，仅为 gates 的约 `0.10–0.12×`；机制真实激发但下游公开效应不足。科学拒绝，不扩展。详见 `WORK_II_CATALYST_DEACTIVATION_Q0_ANALYSIS_ZH.md` |

正式 A-E 尚未执行，因此可以在不污染 participant outcomes 的情况下把 4 轮改为 8 轮；但已有 formal design、
旧 manifest preflight 与 power/resource 文件只视为历史 planning artifacts，不能作为执行授权；当前 v0.2
design 与 analysis 由 formal builder 分别绑定，并通过人口、三臂、checkpoint 和模型分母的字段级关系互证。

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
- [x] **W2-33** reaction-safety catalyst-deactivation static A-S seed-0 Q0 已完成：`54/54`
  completed/exact replay、0 physical/platform/unsafe。Stable catalyst 的结构绑定、动作/噪声配对和 effect 方向均
  正确，但最大 direct gap 只有 `0.0053–0.0062`，未达到 `0.050–0.054` gates，duration accumulation 也失败。
  保留任务—机制可辨识性科学拒绝，不扩展、不生成 D1/provider；下一候选不得通过调大该机制继续试探。
- [x] **W2-34** 按用户澄清后的定义执行两个真实 provider campaign：reaction-safety seed 0，失活与稳定
  世界各一个 WellAU `gpt-5.6-sol` medium 持久 Codex session，每个自主完成 8 次实验。两边公共合同完全
  匹配；随后将 16 个 provider-selected recipes 在两种定律下做 `32` 次 provider-free paired replay，直接
  检验 yield/conversion/selectivity 是否超过 W2-33 的 `0.050/0.050/0.054` gates。此前 1 session × 2
  experiments 是范围误解下的 development pilot，永久保留但不进入 W2-34 分母。正式 W2-34 为
  `2/2` sessions、`16/16` experiments、`112/112` operations、`32/32` paired replay；闭环描述性差异
  可超过 gate，但同配方纯物理最大 gap 仅 `0.00899–0.01226`，所以 requested fixed-action claim 未通过。

### P1 — 重冻正式矩阵

- [x] **W2-25Q** v0.1 的 `300/300` development qualification 已科学拒绝并暴露配对噪声、指标稀释和
  oracle-only reachability 缺陷；旧结果永久保留。v0.2 在首次 defective partial 后已从 execution 0
  完整重跑，`1,200/1,200` primary 与 `1,200/1,200` exact replay 全部落盘、0 physical/platform
  failures、独立复核 `0` errors。held-out 仅 crystallization/partition 各 `5/5` 通过；
  electrochemical `1/5`、distillation `0/5`、safety `3/5`，因此五任务 universal A-E claim 被科学拒绝。
  不得降低 v0.2 阈值、筛掉失败任务或重用已暴露 worlds；若提出 v0.3，须先重建失败 task/locus
  的物理可识别性，并使用全新 prospective held-out cohort。
- [x] **W2-25** A-E formal design 已从 4 改为 8 experiments/cell；checkpoints 为 `0/2/4/6/8`，每 cell
  至少 6 个 unique recipes、最多 2 个 exact repeats。五个 planning resource cards、analysis denominators、
  135-cell C2 manifest/preflight、task-aware analysis 与 private/public evaluator 均已实现；派生的
  当前 method qualification 已终态通过，task-resource cards 仍须由完整 W2-26 闭合；不再重建旧 power
  audit、method-qualification readiness 或 preregistration readiness。formal execution 仍被 W2-26、
  private-seal 迁移和用户 release 授权锁死。
- [x] **W2-26 旧 WellAU calibration lane 已历史收束，不再是当前 public 执行门禁。** r9/r10/r11 的完整、
  部分和不利结果均保留，不能拼接或覆盖；`gpt-5.6-sol` 特异后端故障是当时的终态归因。连续生成的版本化
  authorization/manifest 只是开发期控制投影，不进入当前结果入口。DeepSeek 后续使用直接 task resource cards
  和终态机器 summary 完成 public C2；若未来重启 WellAU replication，必须建立新的独立 experiment note、预算
  和 canary，而不是恢复旧 W2-26 授权链。
- **W2-26 DeepSeek 子阶段（2026-08-14）**：已按结果优先语义终态收束，`9/9` triplets、`27/27`
  terminal cells、`251/252` complete experiments、`135/135` checkpoints、`27/27` exact replay，0
  platform defects、0 terminal provider errors、0 unsafe。唯一科学分母缺口是 A-E partition aligned
  的 `7/8` retained participant failure，不补跑。旧 method gate 的 token/resource findings 原样保留但不再
  作为科学拒绝；DeepSeek 结果只属 development，不补齐 WellAU W2-26，也不进入 formal/R5。深入分析见
  `WORK_II_DEEPSEEK_W2_26_STAGE_CLOSEOUT_ZH.md`。WellAU 按用户指令暂停。
- **DeepSeek C2 corrected-semantics public cohort（2026-08-15 终态）**：基准 v0.2 的 120 个未受影响
  sessions 与从第一单元重跑的 A-S crystallization resource-recovery 15 sessions 在完整 block 边界组合，
  共 `45/45` triplets、`135/135` sessions terminal、`121/135` qualification、`1,243/1,260` complete
  experiments。全 cohort 为 0 provider errors、0 dynamic physical failures、0 unsafe outcomes。硬 campaign
  resource card 继续作为实验变量，故 completion 不能解释为纯 prior 效应。A-E partition 是当前最强
  signal：aligned 相对 misindexed 的 first/best 配对差分别为 `+0.106/+0.200`，均为 `5/5` worlds 同方向；
  A-S partition 显示两种 structured prior 的搜索后成绩均高于 opaque，但 aligned-vs-misindexed 尚未稳定
  分开。A-E private 与 WellAU 继续延期。终态汇报和可复用图表位于
  `WORK_II_PAPER_RESULTS_ZH.md` 与 `reports/figures/work-ii-deepseek-c2-public/REPORT_ZH.md`。
- [x] **W2-27** current WellAU method qualification triplet 已完成并通过：3/3 arms terminal、各 8/8
  experiments、每臂 1 次 provider attempt、0 provider/infrastructure failures；三臂 exact replay 各验证
  48 steps、0 mismatches，receipt validator 为 0 errors。该 development qualification 只证明当前
  harness/lifecycle/replay，`formal_execution_authorized=false`，不按科学效果评分，也不补齐 W2-26 的
  9-task resource summary。
- [x] **W2-38** 两项 A-P 独立 terminal D1 已完成 provider-free readiness：不再维护人工历史报告清单，
  而是语义发现已有 participant provider 暴露，并按事前确定的 `最小 Q2-passed 未暴露 seed` 规则为
  reaction-safety 与 electrochemical 均选择 seed 2。两份三臂、10-experiment、`0/2/4/7/10`
  checkpoint 静态配置已生成；仅表示执行设计 ready，provider/R5 仍锁定，旧失败/混淆结果不被替换。
- [x] **W2-39** A-P 独立 terminal D1 的 development execution 平台重资格已完成并通过。修复共享 token、
  MCP taxonomy、checkpoint/final closeout 与零操作基础设施失败语义后，按 DeepSeek 后 WellAU 的冻结顺序，
  四个受影响 blocks 已在新输出目录从首 cell 完整重跑：`4/4` blocks、`12/12` cells 均形成不可覆写终态，
  共完成 `94/120` experiments，`9/12` cells 达到 10/10，`4/12` qualification completed。全部 `11/11`
  有 committed operations 的 cells 均通过 exact replay；provider errors、missing cells、invalid store receipts
  与 unclassified MCP failures 均为 `0`，typed taxonomy 为 agent-invalid `142`、transport/IPC/OS `1`、
  provider/network `0`。因此冻结的平台门禁通过，不再要求因同一平台缺陷重跑；但删失仍依赖 provider、task
  与 arm，当前轨迹不支持 provider/model/arm 科学比较，也不替代 W2-26 task-specific resource calibration 或
  W2-27 current-method qualification，不进入 R5/C2。
- [ ] 用户冻结 submission route、currency ceilings、failure-escalation 和 public/private 执行授权。
- [ ] 生成 final freeze receipt；此后不再改变 coverage、worlds、arms、轮次或 failure rules。

### P2 — 完整 C2 冻结、执行与条件扩展

- [x] DeepSeek corrected-semantics public 核心 scope 已固定并终态执行：**C2 public = A-E + 2 A-P +
  2 A-S**，共 `45` task/world clusters、`135` sessions、`1,260` planned experiments；历史 pre-fix cohort
  不与其拼接。终态后直接从 canonical summaries 生成分析，不另造 manual SHA/readiness gate。
- [x] A-E public 25 triplets 已作为同一 DeepSeek public cohort 的组成部分全部 terminal。
- [ ] A-E private 保持延期；只有用户在 public task-aware analysis 后重新授权才执行，且不得按 public 结果
  方向修改 sealed coverage 或 prior arms。
- [x] 完成当前 DeepSeek public Study C / current-composite v0.2 recovery：45 clusters、135 cells、420 truth、
  675 checkpoint scores、135 executable laws、726 launched blind replays；failure-aware 与 observed-point
  sensitivity 均已生成。v0.1 未传递 A-S `world_interventions`，已从第一单元重跑并降为 historical。历史 C1 若
  定义为包含 A-E private，则该更强 private claim 仍未完成。
- [x] 两个 A-P 与两个 A-S DeepSeek public blocks 已按 corrected-semantics v0.2 plan 终态；registered
  task-aware evaluator 与删失敏感性分析已完成，不再重复 participant execution。
- [x] Matched-evidence 机制块已终态：A-P Study B 15/15 current；原 A-S Study B 15-session branch historical；
  A-S B2 15/15 current。B2 主对比 `+0.0645`、3/5 positive、`p=0.125`，misindexed 0/5 exact law recovery。
- [x] C3 机制问题已收束为非二元结果；seeking/updating 的跨-locus 单标签强主张不支持。C4/D 仅在保留
  transfer claim 时执行，不能按结果临时改为主实验。

## 11. Task tracker

| Work package | 状态 | 说明 |
|---|---|---|
| W2-01–06 | DONE | scope、questions、cohort、estimands、participant contract |
| W2-07–11 | REOPENED | 旧 4-experiment resource/design freeze 被新矩阵替代，需在 W2-25–27 后重新关闭 |
| W2-12–14 | PUBLIC EVALUATOR COMPLETE / PRIVATE DEFERRED | DeepSeek public participant 与 current-composite evaluator 终态；A-E private 延期，需用户另行授权 |
| W2-15 | CURRENT PUBLIC + MATCHED-EVIDENCE ANALYSIS COMPLETE / PROGRAMME EXPANSION PENDING | Paper 2 全结果索引、current figures、agent-behavior、recovered evaluator、删失敏感性和 A-P/B2 matched evidence 已整合；Study D、private 与 cross-provider 为独立下一阶段决策 |
| W2-17–18 | DOING | non-entity qualification；转由 W2-21–24 管理 |
| W2-19 | TERMINAL / THREE-LAYER MECHANISM CLOSURE | 当前有效 matched-evidence 30 sessions terminal；A-P 支持 acquisition component，A-S B2 为 mixed prediction signal + unrecovered exact law；二元 C3 强主张不支持，不再追加同类 block |
| W2-20 | CONDITIONAL | artifact-only transfer D |
| W2-21 | DONE | five-world oracle qualification note 已冻结 |
| W2-22 | DONE | provider-free response-surface runner 与 readable summaries 已完成；reaction-safety absolute rejection 和两个 task 的 relative qualification 分层保留 |
| W2-23 | DONE | reaction-safety 与 electrochemical matched-prior Q2 均以 5/5 worlds 通过；baseline、disagreement、双反证区域、blind identification、word/schema matching 与 leakage gates 全通过 |
| W2-24 | DONE | reaction-safety world-0 D1 与 D2 worlds 1/4 participant/evaluator 已完成；综合结论待用户审核 |
| W2-25 | SCIENTIFICALLY REJECTED | v0.2 已完成 1,200 primary + 1,200 exact replay、0 platform failures；held-out 仅 2/5 tasks 通过，五任务 A-E universal claim 不得进入 formal participant matrix |
| W2-26 | HISTORICAL / SUPERSEDED | 旧 WellAU calibration lane 的 r9/r10/r11 原样保留，不再阻断 DeepSeek public；未来 WellAU replication 需新协议，不恢复版本化授权链 |
| W2-27 | TERMINAL / METHOD QUALIFICATION PASSED | current WellAU 三臂均 8/8 terminal、qualification passed、exact replay 48 steps/arm 且 0 mismatches；receipt validator 0 errors。仅为 development method qualification，formal execution 仍未授权，W2-26 仍不完整 |
| W2-38 | READY/BLOCKED | A-P 两项独立 terminal D1 均按最小未暴露 Q2-passed seed 选择 seed 2；静态三臂 10-experiment 配置 ready，provider/R5 未授权 |
| W2-39 | TERMINAL / PLATFORM REQUALIFICATION PASSED | A-P seed-2 DeepSeek→WellAU 四块已在共享执行语义修复后从首 cell 完整重跑：`12/12` cells terminal、`94/120` experiments、`4/12` qualification completed、`9/12` 达到 10/10、全部 `11/11` 个有 committed operations 的 cells exact replay；0 provider errors、0 missing/invalid store、0 unclassified MCP failures。平台门禁通过；删失非随机，故不作 provider/model/arm 科学比较，不替代 W2-26/W2-27，也不进入 R5/C2。 |
| W2-40 | ARCHIVED / SUPERSEDED BY W2-47 | 原 5-world full-32-prediction 设计从未执行；note 已归档、launcher 已删除。旧 config 只作为 W2-43 候选网格历史输入保留，不是当前执行入口。 |
| W2-41 | TERMINAL / DEVELOPMENT DIAGNOSTIC ONLY | terminal schema canary 保留 `6/6` sessions，完成 `4/6`；full/lean 各有 1 个 pre-reveal law-turn schema failure。已进入 terminal 的 full 相对 lean 平均增量 output tokens 为 `35,164 vs 2,368`，elapsed 为 `244.6 vs 18.8 s`；仅证明 full-32 操作负担过高，不作 action-quality 结论。 |
| W2-42 | TERMINAL / DIAGNOSTIC; FOLLOW-UP BRANCH CLOSED | fixed correct-law terminal replay 保留 `6/6` records、完成 `4/6`；full/lean 各缺 1 个 payload，lean failure 带 provider error。全部完成样本均选择真实第 5 名，full/lean regret 同为 `0.5418`。它证明旧多维 packet 不能由 target law 单独排序，并触发 W2-44–W2-46；后续严格 partition matched-action 支线已终态拒绝。 |
| W2-43 | TERMINAL / TRUE 12-ROUND DEVELOPMENT CANARY | 三个持久 sessions 各自主完成 `12/12` experiments 与 `5/5` checkpoints，final 后揭示候选并 ranking-only 排序；修复旧 full-metrics qualification 误分类后为 `3/3` completed uncontaminated、`36/36` participant experiments、0 collisions/failures。misindexed/aligned/opaque 分别选择真实第 `1/3/8` 名，normalized regret `0/0.3620/1.0`；三条 final-law MAE 均不合格。单一已暴露 world 仅作纵向流程和行为 canary，不作 arm-level claim；W2-41/W2-42 不回答该纵向问题。 |
| W2-44 | TERMINAL / SCIENTIFICALLY REJECTED BEFORE PROVIDER | 固定过程 64-action pool 在 5 worlds × 2 laws 完成 `640/640` truth 与 exact replay、0 failures、0 provider；仅 1 组 contrast 满足冻结的跨-world reversal/gap，低于 4 组要求，不放宽门槛。 |
| W2-45 | TERMINAL / ANALYTIC ROSTER REJECTED BEFORE PROVIDER | 解析 crossover 完成 `80/80` truth/replay、0 failures、0 provider；设计公式遗漏固定 `0.020 L` solvent 对总 organic volume 的贡献，4 组 contrast 均未跨 5 worlds 通过。正确 runtime truth 保留，解析 roster 被否定。 |
| W2-46 | TERMINAL / STRICT EXPONENT-ACTION BRANCH CLOSED | 修正总 organic volume 并使用 common-random-number evaluator truth 后完成 `80/80` truth/replay、0 failures、0 provider；仅 `2/20` contrast×world 与 `0/5` world rosters 通过。当前 partition 严格 exponent→action 支线终止，不再建立同类 crossover 后继块。 |
| W2-47 | HISTORICAL / PROTOCOL DIAGNOSTIC ONLY | 单 world 三臂 development run 已完成；旧 feature-only terminal packet 未公开完整 action plan，结果不进入 action-quality claim。原始 runs 保留，旧 note/config/launcher/materializer/tests 已归档。 |
| W2-48 | TERMINAL / DEVELOPMENT FIVE-WORLD MATRIX | `15/15` sessions、`180/180` participant experiments、`13/15` eligible、`120/120` truth + replay、binding passed；`0/15` Top-1，2 adequate-law/wrong-action + 13 inadequate-law/wrong-action。仅 3 个完整三臂 clusters，不作 arm-level formal claim，不补跑。 |
| W2-49 | TERMINAL / MULTI-TASK DEVELOPMENT QUALIFICATION | electrochemical、reaction-to-crystallization 与 reaction-safety 的最新未污染单世界 blocks 合计 `9/9` eligible、`108/108` participant experiments、`48/48` truth + replay；full-plan/ranking-only harness 跨任务通过，科学比较留待 fresh multi-world block。 |
| W2-50 | TERMINAL / FRESH MULTI-WORLD OPEN ACTION AUDITED | `45/45` cell records、`15/15` clusters、`240/240` truth 与 `240/240` exact replay 完成；`42/45` cells 为 `completed_uncontaminated`，`3` 个 reaction-to-crystallization failures 保留（2 个 agent-induced resource/process exhaustion，1 个 provider/session interruption）。动作指标只使用 42 个合格 cells；不补跑、不替换、不宣称 15/15 全 cell 的 arm-level 普适结论。另完成独立 `seed2/aligned_nominal` repair：12/12 final assays，但 1 次 `stock_limit:seed_g` rejection，故仅作技术敏感性结果，不回写原始分母。审计与收束见 `reports/WORK_II_MULTI_TASK_OPEN_ACTION_FORMAL_AUDIT_ZH.md`。 |
| W2-51 | DESIGN + PROVIDER-FREE QUALIFICATION PASSED / PROVIDER NOT AUTHORIZED | 新 evidence-to-action 五条件因果分解固定为 3 tasks × 5 fresh worlds × 3 priors × 5 conditions：225 fresh sessions；仅 45 autonomous donors 执行 12 轮，共 540 participant experiments。No-evidence 首次见候选即直接排序；artifact-only fresh context 同时接收规律与候选；autonomous/yoked 完成证据阶段后揭示候选。旧 hash-split 开发块完成 240/240 truth/replay，但候选门仅 11/15；public-feature maximin 重分组为 15/15。8-point oracle 仅 3/15 通过；修正 categorical coverage 后的 96-point global grid 完成 1,440/1,440 provider-free truth，但仅 7/15 通过。固定 32 global + 64 outcome-blind candidate-neighborhood、扩展同一 typed schema 的 cubic 与 categorical-conditional 项后，compact-ID restart 完成 1,440/1,440 并 15/15 通过：electrochemical、crystallization、reaction-safety 均 5/5，rho=0.810–1.000，fit/candidate overlap=0，provider calls=0；Top-1 4/15 仍仅描述。recipient reveal/hidden-field/terminal runtime、donor dependency、yoked checkpoints、clustered analysis 与 law-action agreement 均已实现；单 stratum 五条件 orchestrator 也已通过成功 donor 与失败 donor 两条 fake-provider canary，能规范化 terminal submission、精确计数调用/物理实验并保留 blocked descendants。下一步只剩把现有 autonomous campaign executor 与正式 15-cluster launcher 接线；provider execution 仍未授权。 |
| W2-37 | DONE / BOTH CANDIDATES PASSED | restart3 从 execution 0 完成 `10,240/10,240` primary 与 `10,240/10,240` exact replay，0 physical/platform/unsafe；crystallization reversible topology 与 partition power response 均 `5/5` worlds 通过，已生成两份 locked D1 config。它们仍 `formal_result=false`、`execution_authorized=false`，不等于 participant/R5 授权 |
| W2-29 | DONE | reaction-safety 与 electrochemical mechanism-oracle 均已 5/5 通过；electrochemical 当前授权进入 Q2 matched-prior construction |
| W2-30 | DONE | electrochemical matched-prior WellAU world-0 D1 已完成并完成 provider-free evaluator；`failed_retained`，中间 checkpoint 信号和失败归因已冻结，未经用户审核不重启新 block |
| W2-31 | DONE | Q0 `12/12` controls passed；seed-0 screen `24/24` completed/exact replay，electrochemical pass、crystallization scientific reject；按冻结规则不扩展、不生成 D1 |
| W2-32 | DONE | static reversible-path seed-0 Q0 `36/36` completed/exact replay；crystallization pass、flow scientific reject；固定世界语义通过，整体不扩展 |
| W2-33 | DONE | reaction-safety deactivating-vs-stable catalyst static A-S seed-0 Q0；`54/54` completed/exact replay，结构真实但公开效应不足，科学拒绝 |
| W2-34 | DONE | `2 x 8` real-provider campaigns + `32/32` paired replay；闭环轨迹明显分岔，但固定配方纯物理效应 0/16 超 gate，严格 claim 不通过 |

- [x] **W2-35** catalyst-effect chain 诊断已完成：`63/63` 主执行、`63/63` 官方 exact replay、0 failures，
  destructive sampling、catalyst inventory、fresh-batch reset 与 topology checks 全通过。催化剂相对无催化剂的
  最大真实 yield 效应为 `0.36470`，但 stable-vs-deactivating 最大 yield gap 仅 `0.00620`，9 个高温比较均未达到
  冻结 tradeoff gate；归因为 fresh-batch 设计遮蔽、endpoint compression、机制可辨识性与参数校准不足，继续拒绝
  该 A-S 候选且不降低阈值。
- [x] **W2-36** reaction-to-distillation additional-rollback A-S seed-0 Q0 已完成：`18/18` completed、
  `18/18` exact replay、0 physical/platform/unsafe；原生可逆反应保留且仅新增一条 `0.0005 s^-1` rollback
  path。最大 yield/conversion gap 为 `0.02324 < 0.05`，最长减最短时长的平均 accumulation gap 为
  `0.01505 < 0.03`，科学拒绝且不扩展。
- [x] **W2-37** crystallization reversible-topology 与新 nominal-pair partition constitutive-power 已在 restart3
  从 execution 0 完整终结：`10,240/10,240` primary、`10,240/10,240` exact replay，0 physical/platform/unsafe；
  两候选均 `5/5` worlds 通过，Q2 继续按每 task-world coordinate-only 规则盲选 16 个 held-out queries，
  两份 locked D1 config 已生成。旧 load/volume partition Q0 的科学拒绝与两次 platform-defective partial 原样
  保留。不得恢复共线设计或 generic quadratic surrogate；D1 仍 `formal_result=false`、执行未授权。

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

- Paper 2 全部结果与 claim 边界：`workstreams/flagship_tasks/WORK_II_PAPER_RESULTS_ZH.md`
- DeepSeek C2 current 结果、图表与 source data：
  `workstreams/flagship_tasks/reports/figures/work-ii-deepseek-c2-public/REPORT_ZH.md`、
  `workstreams/flagship_tasks/reports/figures/work-ii-deepseek-c2-public/current/summary.json`
- Formal design（W2-25 八实验设计）：`configs/benchmark/work_ii_formal_design_v0.2.json`
- Analysis plan（W2-25 八实验分母）：`configs/benchmark/work_ii_analysis_plan_v0.2.json`
- W2-37 A-S five-world terminal summary：`workstreams/flagship_tasks/reports/work-ii-as-paired-law-q1-q2-five-world-20260812.json`
- W2-48/W2-49 open-action development 收束：
  `workstreams/flagship_tasks/reports/WORK_II_OPEN_ACTION_DEVELOPMENT_CLOSEOUT_ZH.md`、
  `workstreams/flagship_tasks/WORK_II_AS_OPEN_ACTION_DECISION_EXPERIMENT_NOTE.md`、
  `configs/benchmark/work_ii_as_open_action_decision_v0.1.json`、
  `workstreams/flagship_tasks/WORK_II_MULTI_TASK_OPEN_ACTION_RESOURCE_RECOVERY_V2_EXPERIMENT_NOTE.md`
- W2-41 terminal schema development canary：
  `workstreams/flagship_tasks/WORK_II_TERMINAL_SCHEMA_LEAN_CANARY_EXPERIMENT_NOTE.md`
- W2-42 fixed-context terminal-only replay：
  `workstreams/flagship_tasks/WORK_II_TERMINAL_SCHEMA_FIXED_CONTEXT_REPLAY_EXPERIMENT_NOTE.md`
- W2-43 true twelve-round longitudinal ranking canary：
  `workstreams/flagship_tasks/WORK_II_AS_LONGITUDINAL_RANKING_CANARY_EXPERIMENT_NOTE.md`、
  `configs/benchmark/work_ii_as_longitudinal_ranking_canary_v0.1.json`、
  `workstreams/flagship_tasks/reports/WORK_II_AS_LONGITUDINAL_RANKING_CANARY_ZH.md`
- W2-40 与 W2-44–W2-46 归档入口及终态收束：
  `workstreams/flagship_tasks/archive/longitudinal_action_design/README.md`、
  `workstreams/flagship_tasks/reports/WORK_II_AS_LONGITUDINAL_MATCHED_ACTIONS_CLOSEOUT_ZH.md`
- Formal preflight（当前仅 A-E 75 public cells / 600 complete experiments，execution blocked；四份
  A-P/A-S terminal receipts、A-E qualification 与 W2-26 同提交证据齐全后，确定性扩展为 C2 135 cells /
  1,260 experiments）：`workstreams/flagship_tasks/reports/work-ii-formal-matrix-runner-preflight-v0.1.json`
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
- Catalyst-deactivation real-provider paired campaigns：
  `workstreams/flagship_tasks/reports/work-ii-catalyst-deactivation-paired-provider-seed0-20260812.json`、
  `workstreams/flagship_tasks/WORK_II_CATALYST_DEACTIVATION_PAIRED_PROVIDER_ANALYSIS_ZH.md`

Git history 保存本文件过去的详细任务卡和运行日志；不恢复并行的旧主控入口。
