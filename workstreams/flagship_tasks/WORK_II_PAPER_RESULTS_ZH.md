# Paper 2 / Work II 全部结果索引

更新日期：2026-08-31

本文件是 Paper 2 当前唯一的结果导航入口。它不替代 raw run、机器 summary、实验 note 或冻结 analysis plan；历史报告只描述各自执行时点，不再作为当前状态入口。

## 1. 当前论文状态

| 层级 | 状态 | 结论 |
|---|---|---|
| 物理化学平台与 exact replay | 已完成当前开发收束 | 正式连续路径、资源账本、稳定 batch identity 和 belief checkpoint 接口已通过回归 |
| Provider-free 可辨识性与机制资格 | 已完成 | 一部分 task/locus 通过，一部分按冻结门槛科学拒绝；失败结果全部保留 |
| DeepSeek C2 public participant | 终态 | 135/135 sessions，1,243/1,260 experiments，121/135 qualification |
| Participant prediction checkpoints | 已完成采集 | 675/675 snapshots，6,300 registered query predictions，24,300 query–metric values |
| Registered current-composite evaluator v0.2 recovery | 已完成 | 420/420 truth、675/675 checkpoints、135/135 laws、726/726 launched blind replays；0 provider calls |
| 删失与资源敏感性分析 | 已完成当前 public 主分析 | 7 failed、7 right-censored 与 84 个未启动 blind 分母全部保留；另报 observed-point sensitivity |
| Matched evidence（A-P Study B + A-S B2） | 当前有效 30 sessions 终态 | A-P 支持 evidence-seeking component；B2 给出 mixed predictive contrast，但 misindexed 0/5 恢复 1.75 law，结构识别仍是独立瓶颈 |
| W2-56 identifiable-law/action control | GPT formal 30/30；DeepSeek canary rejection 单列 | GPT 三臂 joint family+exponent recovery 为 0/10、5/10、0/10，eligible gain≥0.02 为 0/18；支持 provider-specific 结构保留/修正与行动桥接诊断，不作跨 provider leaderboard |
| W2-57 shared-index cross-model control | 终态 canary rejection | DeepSeek canary `2/3`，但 `6/6` provider turns 均完成；opaque post 的合法 action index 被冗余 stage-status 文本拒绝。该失败完整保留、不补跑，GPT 未启动，formal 双方均 `0/30` |
| W2-58 runner-derived-status successor | 终态 canary rejection | DeepSeek 三臂均完成两轮 provider turn，但三条 post 均缺少合法 action index，终态 `0/3` participant-schema failures；GPT 未启动，formal 双方均 `0/30` |
| W2-50 fresh multi-task open action | 正式描述性终态 | `45/45` cell records、`42/45` eligible、`240/240` truth 与 exact replay；11/42 Top-1，三项 crystallization failures 保留，不作 causal action-transfer claim |
| W2-51 evidence-to-action 五条件分解 | 工作包 DONE；原 provider 前科学拒绝保留 | 前 8 个 clusters 完成 `896/896` truth 与 exact replay；candidate 8/8、oracle 7/8，fresh crystallization world 的 `rho=0.738095<0.80`；0 participant/provider calls、0 participant experiments，不产生五个因果对比；不再是 ICLR 写稿阻断项 |
| W2-52 320-grid oracle | 工作包 DONE；construction pass 与 prospective rank rejection 均保留 | 7/7 exposed construction 单元通过并修复四个历史失败，但首个 fresh prospective world 为 `rho=0.714286<0.80`；Top-1 正确、regret=0，余下 14 clusters 未启动；不再是 ICLR 写稿阻断项 |
| W2-53 oracle gate-action alignment | 回顾诊断终态 | 固定 `16/16` unit-version 全部复现；W2-51 为 rank gate 7/8 但 Top-1 1/8，首个 fresh 320-grid world 则 rank 失败但 Top-1 正确，证明完整排序与动作充分性分离 |
| A-E private | 延期 | public evaluator 后仅在需要 held-out confirmation 时重新授权 |
| 跨 provider replication | W2-58 已终态停止，paired formal comparison 尚不可用 | W2-56 只有 GPT formal；W2-57 与 W2-58 均在 DeepSeek canary 终止，GPT 未启动；当前仍无 matched cross-model formal denominator |
| Manuscript story | 内部稿与 ICLR 匿名稿已整合 | `paper/prior_discovery_story_zh.md`；不再等待 oracle v0.5，以五层能力分解和 evaluator validity 组织当前证据，并明确模型覆盖边界 |

### 1.1 模型与执行主体覆盖

结论先行：**当前 programme 出现了 DeepSeek 与 GPT-5.6-sol 两类 participant，但没有任何一个科学证据块同时拥有两者完整、匹配的 formal 分母。** 因此可以说论文包含两个模型配置的互补证据，不能说“所有实验都由两个模型完成”或“结论已经跨模型复现”。

这里还必须区分模型与运行框架：报告中的“DeepSeek--Codex participant”指 DeepSeek 模型运行在 Codex session/harness 中，不表示 DeepSeek 与 GPT 组成双模型 ensemble；只有明确标为 `GPT-5.6-sol` 的 block 才是 OpenAI 模型 participant。

| 当前证据块 | DeepSeek participant | GPT-5.6-sol participant | Provider-free 部分 | 可作跨模型比较？ |
|---|---|---|---|---|
| 前置三臂材料信息基线 | 无匹配 DeepSeek block | 60/60 cells，2,280 experiments | exact replay | 否；GPT 单模型前置证据 |
| 三 locus public prospective cohort | 135/135 sessions，1,243/1,260 experiments | 无 | 420 truth、675 scoring、135 law evaluations、726 blind replays | 否；DeepSeek 主队列 |
| A-P Study B + A-S B2 matched evidence | 30/30 sessions，60/60 turns | 无 | B2 80/80 truth | 否；DeepSeek 机制定位 |
| Typed-law capacity 与 incumbent replay | 复用 DeepSeek 的 135 个 final states | 无 | capacity fit 与 replay evaluator | 否；同一模型输出的零-provider 分析 |
| W2-50 fresh multi-task open action | 45/45 records，42/45 eligible | 无 | 240/240 truth + replay | 否；DeepSeek 描述性动作结果 |
| W2-51/W2-52/W2-53 oracle controls | 无 participant | 无 participant | 全部为 truth、oracle 与冻结回顾 | 不适用；它们检验 evaluator/control，不检验 LLM |
| W2-56 identifiable-law/action B3 | canary 1/3 completed、formal 0/30 | canary 3/3、formal 30/30 | science surface 与 truth roster 匹配 | 否；只有 GPT 形成 formal 科学分母 |
| W2-57 shared-index B3 | canary 2/3、formal 0/30 | 未启动 | shared-index science surface 与 truth roster 匹配 | 否；终态 canary rejection，不补跑 |
| W2-58 runner-derived-status B3 | canary 0/3 completed、3/3 participant-schema failures；formal 0/30 | canary 0/3、formal 0/30，按 stop rule 未启动 | qualification/public truth/roster/public-packet hashes 完全一致 | 否；W2-58 终态不形成 matched formal denominator |

最准确的总体表述是：**programme-level multi-model，block-level single-model，matched cross-model formal comparison 未完成。** 现有证据足以支持 DeepSeek 主队列与 GPT B3 控制各自的 provider-specific 结论，但不能把两者拼成模型优劣排序，也不能将 GPT 的 30/30 结果写成对 DeepSeek 全部结果的复现。

## 2. 当前可以支持的中心论点

1. 正确先验并非普遍有益；其价值取决于任务是否能把先验差异转化为可辨识的实验结果。
2. 在 A-E partition 这类 strong-signal task 上，aligned entity dossier 同时改善首次选择与自由探索后的最佳结果。
3. 错误先验的影响具有任务异质性：它可能持续伤害搜索，也可能在后续实验中被纠正。
4. 给出结构化机制假设可以改善探索组织，但“有结构”不等于“恢复了正确机制”。
5. Endpoint optimization、prior rejection、held-out prediction correction 和 executable-law recovery 是不同能力，不能由 leaderboard score 互相替代。
6. 有限库存、操作次数和时间是任务的一部分；provider 调用预算不设上限不意味着实验室资源无限。
7. 固定高信息量反证可以使 A-P 错误参数方向在 5/5 worlds 被明确推翻，支持自由探索损失包含 evidence-acquisition component。
8. A-S B2 的 phase-process evidence 使 misindexed prediction gain 平均高于 aligned（+0.0645），但仅 3/5 worlds 为正，且 0/5 恢复 exact 1.75 law。
9. 科学纠错不能压缩为 seeking/updating 二分：evidence acquisition、numerical belief revision 与 structural law identification 是三个可分离层级。
10. 机制形成与动作迁移也不能合并：A-S 五世界 open-action 中 `0/15` Top-1，且 2 个 adequate-law readout 仍选择错误 action。
11. 完整公开 ActionPlan 的纵向协议已在 partition 及三个额外任务跑通，旧 feature-only packet 的动作语义缺口已关闭。
12. W2-51/W2-52 暴露了 oracle-control 泛化边界：exposed construction 上的成功不能保证 fresh-world 完整排序。
13. 完整排序与动作充分性不能互相替代：W2-51 的 96-grid fresh 单元中 rank gate 7/8、Top-1 1/8；首个 fresh 320-grid 单元则 `rho=0.714286` 但 Top-1 正确、regret=0。原 stop rule 仍合法执行，但论文不再把单一 rank gate 当作动作质量代理。
14. W2-51/52 均已按终态结果完成并移出当前 ICLR 阻断项；这不回溯授权原 225-session cohort，也不把未估计的五条件因果对比写成完成。
15. W2-56 的 participant-identifiable control 中，aligned joint family+1.75±0.10 recovery 为 `5/10`，opaque 与 misindexed 均为 `0/10`；misindexed 虽 `8/10` 选择 power family，却 `0/10` 恢复正确 exponent。
16. 同一控制只有 `2/30` Top-1，且均来自 action-opportunity 不成立的 world；预先冻结的 eligible 分母中 gain≥0.02 为 `0/18`，结构保留没有自动转化为有用新动作。

当前不能支持的强结论包括：aligned prior 在所有任务上稳定获胜；agent 已普遍恢复正确物理定律；自由探索或 learned law 因果性地改善未见 ActionPlan 选择；结果可跨 provider 泛化；private replication 已完成。

## 3. 证据程序全景

| 证据块 | 分母 / 结果 | Paper 2 作用 |
|---|---|---|
| 三臂材料信息基线 | 60/60 cells，2,280 experiments，全部 exact replay | 证明初始材料信息会改变探索与结果；overall recovery claim 未通过 |
| A-E distinguishability v0.2 | 1,200/1,200 primary + 1,200/1,200 replay | crystallization/partition 5/5 通过，其余任务未达 universal gate；拒绝五任务普遍 A-E claim |
| Reaction-safety mechanism oracle | 5/5 worlds | Q1 机制候选可辨识 |
| Electrochemical mechanism oracle | 5/5 worlds | Q1 机制候选可辨识 |
| Reaction-safety matched prior | 5/5 worlds | Q2 匹配先验合格 |
| Electrochemical matched prior | 5/5 worlds | Q2 匹配先验合格 |
| Reaction-safety D1/D2 | 9/9 cells，90/90 experiments，45/45 checkpoints，48/48 truth、54/54 blind replay | 展示 confidence、direction、prediction、law 和 action 的分离；world 4 注册方向冲突不计 binary direction |
| Electrochemical world-0 D1 | retained operational failure | 不补跑、不进入 D2/R5；保留中间 checkpoint 信号 |
| Observation/measurement screen | 24/24 | electrochemical 通过；crystallization 科学拒绝，不扩展 A-O |
| Static reversible-path screen | 36/36 | crystallization topology 通过；flow 效应不足，科学拒绝 |
| Catalyst-deactivation Q0 + chain | 54/54 + 63/63 | 结构真实但机制效应远低于 gate，科学拒绝 |
| Catalyst paired provider campaigns | 2 sessions、16/16 experiments、32/32 paired replay | 闭环轨迹显著分岔，但固定配方纯物理效应 0/16 超 gate；不作机制因果主张 |
| Distillation rollback Q0 | 18/18 | 物理路径成立但效应不足，科学拒绝 |
| A-S crystallization/partition Q1-Q2 | 10,240/10,240 primary + replay | 两候选均 5/5 worlds 通过，支持进入 public C2 |
| DeepSeek C2 public current | 135/135 sessions，1,243/1,260 experiments；420 truth、675 checkpoints、135 laws、726 blind executions | 当前 public participant 与 evaluator 已闭环；不等于 private、transfer 或跨 provider 已完成 |
| Study B A-P matched evidence | 5 clusters、15/15 fresh sessions、30/30 provider turns、0 participant experiments | 5/5 misindexed sessions 明确推翻错误电位方向；当前保留 |
| 原 Study B A-S branch | 5 clusters、15/15 sessions | truth source 未实际应用冻结的 world intervention；保留为历史平台缺陷证据，不进入当前 claim |
| A-S Study B2 phase-process evidence | 5 clusters、15/15 fresh sessions、30/30 provider turns、80/80 provider-free truth、0 failures | prediction primary contrast +0.0645（3/5，exact p=0.125）；misindexed 0/5 exact law recovery |
| W2-56 GPT identifiable-law/action control | 5 worlds × 3 arms × 2 sessions；canary 3/3，formal 30/30，60/60 formal turns，0 failures、0 tools、0 physical experiments | post MAE 0.0367/0.0215/0.0378；joint family+exponent 0/10、5/10、0/10；Top-1 2/30，eligible gain≥0.02 为 0/18 |
| A-S open-action five-world development | 5 worlds、15/15 sessions、180/180 experiments、13/15 eligible、120/120 truth + replay | 完整 ActionPlan 下 `0/15` Top-1；机制 adequacy 与 action correctness 分离，不作 arm-level formal claim |
| Multi-task open-action qualification | 三个额外任务各自仅 `seed=0`；最新未污染 blocks 合计 9/9 eligible、108/108 experiments、48/48 truth + replay | 证明同一 longitudinal/ranking-only harness 可跨电化学、结晶和反应安全运行；不是 5-seed 结果，不作 prior-arm 推断 |
| W2-50 fresh multi-task open action | 3 tasks × 5 worlds × 3 arms；45/45 records、42/45 eligible、240/240 truth 与 exact replay | 完整计划终端选择为有界描述性结果：11/42 Top-1，mean rank 3.31/8，normalized regret 0.297；无 no-evidence/pre-exploration control |
| W2-51 五条件 causal decomposition | 计划 15 clusters、225 sessions、540 participant experiments；正式完成前 8 clusters 的 896/896 truth/replay，candidate 8/8、oracle 7/8 | fresh crystallization oracle `rho=0.738095<0.80`，正式 provider 前科学拒绝；余下 7 clusters 与全部 participant 分母未启动，五个因果对比均未估计 |
| W2-52 large-grid oracle | exposed construction 7/7、2,352/2,352 truth/replay；fresh prospective 1/15、336/336 truth/replay | 320-grid 修复已知失败却在首个新 world 科学拒绝；Top-1 正确但完整排序 `rho=0.714286`，其余 14 clusters 未启动 |
| W2-53 gate-action alignment | 固定 16/16 unit-version，原 Spearman/Top-1 16/16 复现；0 新 truth/provider/物理实验 | rank gate 与 action endpoint 双向不充分：96-grid 有 6 个 rank-pass/Top-1-wrong，fresh 320-grid 为 rank-fail/Top-1-correct；作为 evaluator-design 结果进入正文 |

## 4. DeepSeek C2 public 当前终态

当前分析使用 corrected-semantics v0.2 的 120 个未受影响 session，并以从第一单元重跑的 resource-recovery v0.2 完整替换 15 个 A-S crystallization session。

| Locus / task | Qualification | Experiments | Mean best | Mean best-first |
|---|---:|---:|---:|---:|
| A-E Electrochemistry | 15/15 | 120/120 | 0.448 | +0.134 |
| A-E Crystallization | 9/15 | 105/120 | 0.525 | +0.077 |
| A-E Distillation | 15/15 | 120/120 | 0.342 | +0.145 |
| A-E Partition | 14/15 | 120/120 | 0.275 | +0.181 |
| A-E Reaction safety | 15/15 | 120/120 | 0.140 | +0.060 |
| A-P Electrochemistry | 11/15 | 149/150 | 0.811 | +0.265 |
| A-P Reaction safety | 15/15 | 150/150 | 0.442 | +0.065 |
| A-S Partition | 15/15 | 180/180 | 0.406 | +0.288 |
| A-S Crystallization replacement | 12/15 | 179/180 | 0.409 | +0.088 |

### 最强信号

- A-E partition：aligned − misindexed 首次实验 +0.106、best score +0.200，均 5/5 worlds 同方向。
- A-E reaction safety：best score +0.036，5/5 同方向，但绝对效应较小。
- A-S partition：aligned 和 misindexed 都显著优于 opaque，但二者仅差 +0.020、3/5 同方向，说明结构化提示效应强于正确索引分离。
- A-S crystallization replacement：aligned − misindexed +0.055、aligned − opaque +0.045，均为 3/5 同方向，平均优势存在但世界异质性明显。

### 边界信号

- A-E distillation 的首次 aligned 优势在自由探索后大幅缩小，支持错误先验可被实验纠正。
- A-E electrochemistry 和两个 A-P task 均无稳定 aligned 终点优势。
- 九个 task/locus 的 mean best-first 全为正，表明模型确实进行了有效的 session 内搜索。

### Agent 工作与预测提交

- 91.2% 的完成实验为唯一 recipe；84.4% 的 session 最优值出现在预算后半段，说明 persistent agent 持续利用反馈搜索。
- 666/1,269 个 closed lifecycles 使用非终点测量，共 872 次 instrument uses；测量率从 A-E electrochemistry 的 0% 到 A-S crystallization 的 98.4%，反映任务路径差异而不是统一的“是否调用仪器”。
- 675/675 belief checkpoints 均提交成功；A-E 每 checkpoint 含 4 个 registered queries，A-P/A-S 含 16 个，总计 6,300 query predictions，并已全部完成 evaluator scoring。
- 三个 locus 的平均 prediction error 都有下降；修复后的 A-S opaque/aligned/misindexed pre→final improvement 为 `0.2194/0.2276/0.2210`。注册 selective-correction gate 均未通过：A-E `p=0.990`、A-P `p=0.079`、A-S `p=1.000`。A-P 为 suggestive，不能升级为 positive claim。
- 135/135 final typed laws 全部可执行；recovered overall law MAE `0.2371`，law 相对 final explicit prediction 更好/相等/更差为 `50/1/84`，说明可执行性与高保真规律压缩分离。
- 稳定 batch identity 下 133/135 final recommendations 选择精确 observed incumbent；121 个可评价 cells 的 726 次 blind replay 全部完成，better/equivalent/worse 为 `1/119/1`，recovered mean gain 约 `-0.0010`。
- 904 个 failed tool events 中 888 个来自 belief checkpoint 提交。所有 checkpoint 最终恢复，但该 schema friction 必须作为 agent-system 负担报告。

## 5. A-S crystallization 特别说明

旧 block 因空晶体群体再次冷却的 runtime-domain 缺陷作废；第一次修复后又暴露实验室热/冷资源卡不足。最终 resource-recovery block 保留物料库存约束，只提高热/冷操作能力并重跑完整 15 sessions。

最终结果为 179/180 experiments、12/15 qualification、2 次真实库存拒绝。历史推荐索引错配属于分析层缺陷：稳定生命周期重建显示 15/15 最终推荐身份有效且都选择公开 incumbent，observed-score regret 为 0。原始历史 qualification 仍保持 12/15，4 个 discard session 的 checkpoint timing 不作事后改写。

### Current-composite world-intervention recovery

后续审计发现 v0.1 truth/blind evaluator 虽将 `world_interventions` 绑定进 plan，却未传入 runtime 与 exact replay，影响 A-S partition/crystallization。v0.2 在全新输出根从第一单元重跑 420 truth 与 726 eligible blind executions；A-E/A-P prediction、law、blind blocks 与旧报告完全一致，A-S 数值被修正，C2 总判定仍不通过。A-S law MAE 从 `0.1851` 修正为 `0.1552`，overall law MAE 从 `0.2438` 修正为 `0.2371`。v0.1 只保留为历史缺陷证据。

## 6. Matched-evidence 机制定位：A-P Study B 与 A-S B2

每个 matched-evidence block 都让 opaque、aligned、misindexed 三臂在同一 Codex thread 中先提交 pre-evidence prediction，再读取逐字相同的 8-row packet，最后对 8 个不重叠 queries 提交 post-evidence prediction。当前有效证据由 A-P Study B 的 15 sessions 与 A-S B2 的 15 sessions 组成，合计 30/30 sessions、60/60 turns、0 failures、0 participant physical experiments；各自 canary 均不进入分析。

### A-P：固定反证使错误参数方向可纠正

opaque/aligned/misindexed 的平均误差分别从 `0.3037/0.2822/0.3105` 降到
`0.0816/0.0804/0.0778`；三臂 post-error 差异不足 `0.004`。misindexed 的注册 update-gain contrast 为
`+0.0309`，3/5 worlds 为正，exact one-sided sign-flip `p=0.125`；小样本不支持单靠 p 值升级普遍主张，
但 5/5 misindexed public summaries 都明确否定“高电位更可靠”，并恢复约 1.1 V 最优、1.3 V 以上坍塌。
结合 Study A 的 A-P suggestive signal，这支持自由探索损失至少部分来自未取得有效反证。

### 原 A-S Study B：退出当前证据

原 A-S matched-evidence packet 派生自受 world-intervention 缺陷影响的 v0.1 truth source。其 15 个 participant sessions 和原始结果保留，但不再支持当前 Paper 2 claim，也不通过事后重算 truth 修补 participant 已看到的 evidence。

### A-S B2：law-level evidence 到达后仍未形成 exact law

B2 在五个 public worlds 中重新执行 80/80 power-law truth queries，证据与评分均使用不重叠 phase-process 坐标，并在 qualification worlds 预先验证每条 query 至少两个 metric 达到 paired-law effect gate。15/15 sessions、30/30 turns 均一次完成，same-thread 15/15，pre/post 各 360 scoring terms。

opaque/aligned/misindexed 平均 error 从 `0.2255/0.2736/0.3392` 降至 `0.0074/0.0060/0.0071`，对应 gain `0.2181/0.2676/0.3321`。注册主对比为 `+0.0645`，3/5 worlds 为正，exact one-sided sign-flip `p=0.125`，95% 描述区间 `[-0.0557, 0.1848]`。该方向说明 direct diagnostic evidence 带来一个 descriptive acquisition component，但不稳定。

结构表述却没有闭合：misindexed 0/5 明确恢复 exact 1.75 law，仅 1/5 明确拒绝 supplied linear partition form，5/5 转向局部饱和/endpoint 模型。B2 因此拒绝纯二分解释：模型不是“完全不更新”，因为 post error 下降约 98%；也不能说“问题只在没找到证据”，因为 law-level evidence 到达后仍未恢复注册结构。当前机制收束是 **acquisition、numerical revision 与 structural identification 三层分离**。

W2-56 的独立冻结控制进一步把 1.75 exponent 做成 participant-identifiable。GPT-5.6-sol medium 在 3/3 canary 后完成 30/30 formal cells；opaque/aligned/misindexed post MAE 为 `0.0367/0.0215/0.0378`，joint family+exponent recovery 为 `0/10`、`5/10`、`0/10`。aligned 的 world-mean exponent error 对两个对照均在 5/5 worlds 更低，但错误先验没有发生选择性结构修正。行动侧 Top-1 为 2/30，eligible gain≥0.02 为 0/18。该 block 强化结构识别与行动迁移分离，但因 DeepSeek formal 0/30，不构成跨 provider 排名。

## 7. 负结果与不扩展决定

以下结果是论文边界证据，不是待“修好”的失败：

- 五任务 universal A-E distinguishability 未通过；
- crystallization observation-model 候选未达噪声门槛；
- flow reversible-path、catalyst deactivation 和 distillation rollback 效应不足；
- catalyst paired provider trajectories 的同配方机制 gap 未超 gate；
- electrochemical D1 为 retained operational failure；
- A-P 尚未表现稳定 parametric-prior 优势；
- W2-51 与 W2-52 都已按固定规则形成终态：fresh-world 冻结排序门槛的科学拒绝保留，原 provider cohort 不执行，也不把 W2-50 事后升级为 causal action-transfer evidence；两项工作包本身已完成，不再列为投稿阻断；
- W2-53 证明该排序门槛与动作目标不等价，但这只改变论文解释，不回溯改变任何 stop rule 或终态。

这些结果防止论文把 task-specific success 扩大成普遍机制恢复主张。

## 8. 当前结果与图表入口

- 当前 Paper 2 / ICLR 论文故事：`paper/prior_discovery_story_zh.md`
- ICLR 2027 投稿清单：`paper/ICLR_2027_SUBMISSION_CHECKLIST.md`
- W2-51 正式收口：`reports/WORK_II_EVIDENCE_TO_ACTION_FORMAL_CLOSEOUT_ZH.md`
- W2-51 机器收口：`reports/work-ii-evidence-to-action-formal-closeout-v0.1.json`
- W2-52 large-grid construction/qualification：`reports/WORK_II_EVIDENCE_TO_ACTION_LARGE_GRID_V1_CONSTRUCTION_CLOSEOUT_ZH.md`、`reports/WORK_II_EVIDENCE_TO_ACTION_LARGE_GRID_V1_QUALIFICATION_CLOSEOUT_ZH.md`
- W2-53 gate-action alignment：`reports/WORK_II_EVIDENCE_TO_ACTION_GATE_ALIGNMENT_ZH.md`、`reports/work-ii-evidence-to-action-gate-alignment-v0.1.json`
- W2-56 GPT formal：`reports/WORK_II_AS_STUDY_B3_GPT56_SOL_MEDIUM_FORMAL_CLOSEOUT_ZH.md`、`reports/work-ii-as-study-b3-gpt56-sol-medium-formal-closeout-v0.1.json`
- W2-57 shared-index 终态 canary：`WORK_II_AS_STUDY_B3_SHARED_INDEX_CROSS_MODEL_EXPERIMENT_NOTE.md`、`reports/WORK_II_AS_STUDY_B3_SHARED_INDEX_DEEPSEEK_CANARY_CLOSEOUT_ZH.md`、`reports/work-ii-as-study-b3-shared-index-deepseek-canary-closeout-v0.1.json`
- W2-58 runner-derived-status 终态：`WORK_II_AS_STUDY_B3_RUNNER_DERIVED_STATUS_CROSS_MODEL_EXPERIMENT_NOTE.md`、`reports/work-ii-as-study-b3-runner-derived-status-deepseek-canary-closeout-v0.1.json` 与 `reports/WORK_II_AS_STUDY_B3_RUNNER_DERIVED_STATUS_DEEPSEEK_CANARY_CLOSEOUT_ZH.md`；跨模型 formal 汇总器未运行，也未生成空结果
- W2-50 正式审计：`reports/WORK_II_MULTI_TASK_OPEN_ACTION_FORMAL_AUDIT_ZH.md`
- Open-action development 收束：`reports/WORK_II_OPEN_ACTION_DEVELOPMENT_CLOSEOUT_ZH.md`
- 原 Study B 机制分析（A-P 保留、A-S 历史）：`reports/WORK_II_STUDY_B_MATCHED_EVIDENCE_RESULTS_ZH.md`
- A-S B2 当前机制分析：`reports/WORK_II_AS_STUDY_B2_PHASE_PROCESS_RESULTS_ZH.md`
- A-S B2 机器结果：`reports/work-ii-as-study-b2-phase-process-results-v0.1.json`
- C2 agent 行为与 prediction-collection 机器分析：`reports/work-ii-deepseek-c2-paper-story-analysis-v0.1.json`
- C2 current-composite evaluator 报告：`reports/WORK_II_DEEPSEEK_C2_CURRENT_COMPOSITE_EVALUATION_V0.2_ZH.md`
- C2 current-composite evaluator 机器结果：`reports/work-ii-deepseek-c2-current-composite-evaluation-v0.2.json`
- C2 world-intervention recovery 审计：`reports/WORK_II_DEEPSEEK_C2_CURRENT_COMPOSITE_WORLD_INTERVENTION_RECOVERY_ZH.md`
- C2 public 详细报告：`reports/figures/work-ii-deepseek-c2-public/REPORT_ZH.md`
- C2 current 机器 summary：`reports/figures/work-ii-deepseek-c2-public/current/summary.json`
- C2 current source data：`reports/figures/work-ii-deepseek-c2-public/current/source_data/`
- C2 current figures：`reports/figures/work-ii-deepseek-c2-public/current/`
- A-S crystallization 稳定身份重分析：`reports/work-ii-deepseek-as-crystallization-resource-recovery-identity-corrected-v0.1.json`
- A-S crystallization 收束：`reports/WORK_II_DEEPSEEK_AS_CRYSTALLIZATION_RESOURCE_RECOVERY_CLOSEOUT_ZH.md`
- A-S five-world Q1/Q2：`reports/work-ii-as-paired-law-q1-q2-five-world-20260812.json`
- Reaction-safety synthesis：`WORK_II_REACTION_SAFETY_MATCHED_PRIOR_D1_D2_SYNTHESIS_ZH.md`
- Electrochemical Q1/Q2：`WORK_II_ELECTROCHEMICAL_MECHANISM_ORACLE_ANALYSIS_ZH.md`、`WORK_II_ELECTROCHEMICAL_MATCHED_PRIOR_ANALYSIS_ZH.md`
- Catalyst paired provider：`WORK_II_CATALYST_DEACTIVATION_PAIRED_PROVIDER_ANALYSIS_ZH.md`

其余版本化 readiness、authorization、manifest、旧图包和 pre-fix 结果不作为当前入口。不可复现的中间控制投影由 Git 历史保存；raw provider 数据和 `runs/` 继续留在本地、不会进入 Git。

## 9. 当前闭环与下一阶段研究决策

当前 DeepSeek public 的 participant、prediction truth/scoring、law evaluation、blind action、failure-aware sensitivity 与 matched-evidence mechanism follow-up 已闭环。A-S B2 已完成，二元 C3 强主张没有得到支持；当前结果以三层机制分离收束。W2-50 随后完成多任务未见 ActionPlan 终端排序，但因缺少 no-evidence/pre-exploration control 仍是描述性结果。W2-51/W2-52 已按原规则形成终态负/诊断结果并移出当前 ICLR 阻断项；W2-53 进一步确认完整排序与动作充分性分离。W2-56 GPT formal 30/30 又提供 participant-identifiable 的结构保留/修正与行动桥接控制，但不作跨 provider leaderboard。W2-57 与 W2-58 的 DeepSeek canary 终态失败均完整保留，GPT 未启动；当前 matched cross-model formal denominator 仍不存在。当前投稿不再等待 oracle v0.5，下一步选择是：

1. **Study D：artifact transfer。** 在 context reset 后分别测试 typed law、evidence bundle 和更高保真 artifact 对 prediction/law/action 的增益。
2. **Cross-provider replication。** W2-58 已终态，不再补跑；若仍需匹配双模型证据，须另行设计并授权独立后继块，再决定是否有必要把 Qwen、Kimi 或 WellAU 接入同一 harness。
3. **A-E private。** 只承担 held-out within-family confirmation；继续延期，除非用户明确把该 claim 纳入下一阶段。
4. **开放式停止与推荐设计。** 未来可统一最大实验预算，允许 agent 提前结束并提交 final plan；这是一项新实验，不事后改写当前 8/10/12 次设计。
5. **新的 action-aligned causal study。** 仅在另行冻结同时报告 complete ranking、near-tie-aware ordering 与 regret 的 control 后再授权；不得把它称为 W2-51 补跑，也不得用 W2-53 回溯放宽原门槛。

因此可以说当前 DeepSeek public prediction task 已完成，但不能说整个 Paper 2 programme 已结束。当前结果是能力链研究的第一阶段，而不是仓促收缩后的最终论文。
