# Paper 2 / Work II 全部结果索引

更新日期：2026-09-03

本文件是 Paper 2 当前唯一的结果导航入口。它不替代 raw run、机器 summary、实验 note 或冻结 analysis plan；历史报告只描述各自执行时点，不再作为当前状态入口。

## 1. 当前论文状态

| 层级 | 状态 | 结论 |
|---|---|---|
| 物理化学平台与 exact replay | 已完成当前开发收束 | 正式连续路径、资源账本、稳定 batch identity 和 belief checkpoint 接口已通过回归 |
| Provider-free 可辨识性与机制资格 | 已完成 | 一部分 task/locus 通过，一部分按冻结门槛科学拒绝；失败结果全部保留 |
| DeepSeek C2 public participant | 终态 | 135/135 sessions，1,243/1,260 experiments，121/135 qualification |
| Codex C2 public participant | 终态 successor | 135/135 scheduled sessions，1,253/1,260 experiments，126 completed、3 failed、6 right-censored |
| Participant prediction checkpoints | 已完成采集 | 675/675 snapshots，6,300 registered query predictions，24,300 query–metric values |
| Registered current-composite evaluator v0.2 recovery | 已完成 | 420/420 truth、675/675 checkpoints、135/135 laws、726/726 launched blind replays；0 provider calls |
| Codex current-composite evaluator | 已完成 | 420/420 truth、669/675 checkpoints、129/135 laws、756/810 scheduled blind replays；0 provider calls |
| 删失与资源敏感性分析 | 已完成当前 public 主分析 | 7 failed、7 right-censored 与 84 个未启动 blind 分母全部保留；另报 observed-point sensitivity |
| Matched evidence（A-P Study B + A-S B2） | DeepSeek + GPT matched formal 终态 | 两模型各完成 A-P `15/15` 与 B2 `15/15`、均 0 failures；A-P primary contrast 为 `0.0309/0.0602`，B2 为 `0.0645/0.0915`，且两模型 misindexed 均 `0/5` 恢复 exact 1.75 law |
| W2-56 identifiable-law/action control | GPT formal 30/30；DeepSeek canary rejection 单列 | GPT 三臂 joint family+exponent recovery 为 0/10、5/10、0/10，eligible gain≥0.02 为 0/18；支持 provider-specific 结构保留/修正与行动桥接诊断，不作跨 provider leaderboard |
| W2-57 shared-index cross-model control | 终态 canary rejection | DeepSeek canary `2/3`，但 `6/6` provider turns 均完成；opaque post 的合法 action index 被冗余 stage-status 文本拒绝。该失败完整保留、不补跑，GPT 未启动，formal 双方均 `0/30` |
| W2-58 runner-derived-status successor | 终态 canary rejection | DeepSeek 三臂均完成两轮 provider turn，但三条 post 均缺少合法 action index，终态 `0/3` participant-schema failures；GPT 未启动，formal 双方均 `0/30` |
| W2-59 cross-model main-evidence completion | block-specific 终态 | 计划 `270` formal sessions，终态 `36`、合格/可评分 `34`、保留失败 `2`、未启动 `234`；A-P/B2 获得完整双模型 matched formal，GPT C2 与 W2-50 在分母内 canary 停止，B3 因 DeepSeek 排除式 canary `2/3` 而双方 formal `0/30` |
| W2-61 four-condition action extension | 双模型 failure-aware 终态 | 两模型各 180、总计 360 scheduled condition slots；DeepSeek/Codex donor-eligible 为 42/26，共同可配对 26 strata；四条件均有冻结分母，所有 donor/recipient failures 保留 |
| W2-62 Codex C2 full-cohort successor | 双模型 135-coordinate 终态 | Codex 126/135 completed；与 DeepSeek 的 matched descriptive comparison 显示 Codex law MAE/compression loss 更低，但两模型 blind gain 均约为 0，三个 selective-correction loci 均未通过 |
| W2-63 DeepSeek B3 full-cohort successor | 双模型 30-cell failure-aware 终态 | DeepSeek 17 completed + 13 participant-schema failures；Codex 30 completed；joint law recovery 0/30 vs 5/30，Top-1 0/30 vs 2/30，eligible gain≥0.02 两者均为 0 |
| W2-50 fresh multi-task open action | 正式描述性终态 | `45/45` cell records、`42/45` eligible、`240/240` truth 与 exact replay；11/42 Top-1，三项 crystallization failures 保留，不作 causal action-transfer claim |
| W2-51 evidence-to-action 五条件分解 | 工作包 DONE；原 provider 前科学拒绝保留 | 前 8 个 clusters 完成 `896/896` truth 与 exact replay；candidate 8/8、oracle 7/8，fresh crystallization world 的 `rho=0.738095<0.80`；0 participant/provider calls、0 participant experiments，不产生五个因果对比；不再是 ICLR 写稿阻断项 |
| W2-52 320-grid oracle | 工作包 DONE；construction pass 与 prospective rank rejection 均保留 | 7/7 exposed construction 单元通过并修复四个历史失败，但首个 fresh prospective world 为 `rho=0.714286<0.80`；Top-1 正确、regret=0，余下 14 clusters 未启动；不再是 ICLR 写稿阻断项 |
| W2-53 oracle gate-action alignment | 回顾诊断终态 | 固定 `16/16` unit-version 全部复现；W2-51 为 rank gate 7/8 但 Top-1 1/8，首个 fresh 320-grid world 则 rank 失败但 Top-1 正确，证明完整排序与动作充分性分离 |
| A-E private | 延期 | public evaluator 后仅在需要 held-out confirmation 时重新授权 |
| 跨 provider replication | participant-bearing 主证据均有双模型 scheduled surface | A-P/B2 为完整 matched formal；C2 各有 135 scheduled cells；B3 各有 30 scheduled cells；四条件 action extension 各有 180 slots。比较均为 block-specific matched descriptive，不作 model leaderboard |
| Manuscript story | 正在整合 W2-61/62/63 | 不再等待 oracle；以 evidence acquisition、numerical revision、structural identification、artifact compression、action selection 与 evaluator validity 组织当前证据 |

### 1.1 模型与执行主体覆盖

结论先行：**当前所有 participant-bearing 主证据块都已有 DeepSeek 与 GPT-5.6-sol/Codex 的预定模型分母。** A-P 与 A-S B2 拥有完整 matched formal 分母；C2 现在各有 135 scheduled cells；B3 各有 30 scheduled cells；W2-50 的后继四条件 action extension 各有 180 scheduled slots。Provider-free W2-51/52/53 不涉及 participant，因此不按模型复制。这里的“双模型补全”指冻结 scheduled denominator 已执行并形成合法 failure-aware 终态，不表示每个 cell 都 completed，更不表示某个模型总体优于另一个模型。

这里还必须区分模型与运行框架：报告中的“DeepSeek--Codex participant”指 DeepSeek 模型运行在 Codex session/harness 中，不表示 DeepSeek 与 GPT 组成双模型 ensemble；只有明确标为 `GPT-5.6-sol` 的 block 才是 OpenAI 模型 participant。

| 当前证据块 | DeepSeek participant | GPT-5.6-sol participant | Provider-free 部分 | 可作跨模型比较？ |
|---|---|---|---|---|
| 前置三臂材料信息基线 | 无匹配 DeepSeek block | 60/60 cells，2,280 experiments | exact replay | 否；GPT 单模型前置证据 |
| 三 locus public prospective cohort / W2-62 successor | 135/135 sessions，1,243/1,260 experiments；121 completed | 135/135 scheduled，1,253/1,260 experiments；126 completed | 两边各 420 truth；675/669 scoring，135/129 laws，726/756 blind executions | 是，135-coordinate matched descriptive；不是 provider 因果效应 |
| A-P Study B + A-S B2 matched evidence | A-P 15/15 + B2 15/15 | A-P 15/15 + B2 15/15 | 两边 B2 各 80/80 truth | 是；同一 worlds/arms/packets 的 block-specific matched replication |
| Typed-law compression 与 incumbent replay | 135 个 final states；135 laws；121 blind-evaluable | 135 scheduled；129 laws；126 blind-evaluable | current-composite evaluator | 是，matched descriptive；DeepSeek capacity oracle 仍是单模型 control |
| W2-50 + W2-61 four-condition successor | 45/45 autonomous records，42 donor-eligible；180 condition slots | 45 autonomous donors，26 donor-eligible；180 condition slots | 共用 240-query truth surface，无新 recipient truth | 是，common-donor-eligible 26 strata；failure-aware 且不作 provider ranking |
| W2-51/W2-52/W2-53 oracle controls | 无 participant | 无 participant | 全部为 truth、oracle 与冻结回顾 | 不适用；它们检验 evaluator/control，不检验 LLM |
| W2-56 + W2-63 identifiable-law/action B3 | successor 30 scheduled：17 completed、13 schema failures | 30/30 completed | science surface 与 truth roster 匹配 | 是，30-coordinate failure-aware descriptive；differential schema failure 明示 |
| W2-57 shared-index B3 | canary 2/3、formal 0/30 | 未启动 | shared-index science surface 与 truth roster 匹配 | 否；终态 canary rejection，不补跑 |
| W2-58 runner-derived-status B3 | canary 0/3 completed、3/3 participant-schema failures；formal 0/30 | canary 0/3、formal 0/30，按 stop rule 未启动 | qualification/public truth/roster/public-packet hashes 完全一致 | 否；W2-58 终态不形成 matched formal denominator |
| W2-59 B3 successor | canary 2/3、formal 0/30 | 首次零 provider 平台缺陷修复后 canary 3/3、formal 0/30 | qualification/public truth/roster bindings 一致 | 否；共同门要求双方 canary 均通过 |

最准确的总体表述是：**participant-bearing main evidence has dual-model scheduled coverage；A-P/B2 是完整 matched formal，C2、B3 与四条件 action successor 是 failure-aware matched descriptive。** 现有证据支持两个模型配置共同复现 numerical--structural break，并把“更好的规律压缩仍不保证行动收益”扩展到完整 C2；但不同 provider 的 schema/completion 差异以及非随机失败阻止模型优劣排序。

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
17. W2-59 的 matched replication 在 A-P 上得到 DeepSeek/GPT primary contrast `+0.0309/+0.0602`，在 A-S B2 上得到 `+0.0645/+0.0915`；后者两个模型的 misindexed exact 1.75-law recovery 都是 `0/5`。因此数值纠错与结构识别的断裂不再只来自单一模型配置。
18. W2-62 为 Codex 补齐完整 C2 scheduled denominator。两模型 prediction improvement 为 `0.1198/0.1329`、law MAE 为 `0.2371/0.1753`、compression loss 为 `0.0686/0.0142`（DeepSeek/Codex），但 blind gain 均约为 0；更准确的规律压缩没有带来行动增益。
19. W2-63 为 DeepSeek 补齐 B3 的 30-cell failure-aware denominator：17 completed、13 participant-schema failures。DeepSeek/Codex joint recovery 为 `0/30` 与 `5/30`，Top-1 为 `0/30` 与 `2/30`，但 eligible gain≥0.02 两者均为 0。
20. W2-61 在两模型各 180 个四条件槽上给出 action-aligned successor。donor-eligible autonomous-minus-no-evidence regret 差在 DeepSeek/Codex 为 `-0.1214/-0.1379`，区间均跨零；learned-law-only 也没有稳定收益。yoked recipient 的大量 retained failures 要与纯 experiment-selection effect 分开。
21. 双模型 scheduled coverage 不等于 cross-provider causal effect，也不授权 model leaderboard；所有比较均保持 block、模型、failure-aware 分母与科学表面边界。

当前不能支持的强结论包括：aligned prior 在所有任务上稳定获胜；agent 已普遍恢复正确物理定律；自由探索或 learned law 因果性地改善未见 ActionPlan 选择；全部能力链结果可跨 provider 泛化；private replication 已完成。

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
| DeepSeek + Codex C2 current | 两模型各 135 scheduled；DeepSeek 121 completed、Codex 126 completed；两边各 420 truth，laws 135/129，blind 726/756 | 135-coordinate matched descriptive 闭环；两个模型均未通过 selective correction，Codex law 更准但 action gain 仍约为 0 |
| Study B A-P matched evidence | DeepSeek 与 GPT 各 5 clusters、15/15 fresh sessions、30/30 provider turns、0 failures | primary contrast `+0.0309/+0.0602`；固定反证后的数值纠错形成 matched cross-model replication |
| 原 Study B A-S branch | 5 clusters、15/15 sessions | truth source 未实际应用冻结的 world intervention；保留为历史平台缺陷证据，不进入当前 claim |
| A-S Study B2 phase-process evidence | DeepSeek 与 GPT 各 5 clusters、15/15 fresh sessions、30/30 provider turns、80/80 provider-free truth、0 failures | primary contrast `+0.0645/+0.0915`；两模型 misindexed 均 `0/5` exact law recovery，支持数值修正与结构识别分离 |
| W2-56 GPT identifiable-law/action control | 5 worlds × 3 arms × 2 sessions；canary 3/3，formal 30/30，60/60 formal turns，0 failures、0 tools、0 physical experiments | post MAE 0.0367/0.0215/0.0378；joint family+exponent 0/10、5/10、0/10；Top-1 2/30，eligible gain≥0.02 为 0/18 |
| A-S open-action five-world development | 5 worlds、15/15 sessions、180/180 experiments、13/15 eligible、120/120 truth + replay | 完整 ActionPlan 下 `0/15` Top-1；机制 adequacy 与 action correctness 分离，不作 arm-level formal claim |
| Multi-task open-action qualification | 三个额外任务各自仅 `seed=0`；最新未污染 blocks 合计 9/9 eligible、108/108 experiments、48/48 truth + replay | 证明同一 longitudinal/ranking-only harness 可跨电化学、结晶和反应安全运行；不是 5-seed 结果，不作 prior-arm 推断 |
| W2-50 fresh multi-task open action | 3 tasks × 5 worlds × 3 arms；45/45 records、42/45 eligible、240/240 truth 与 exact replay | 完整计划终端选择为有界描述性结果：11/42 Top-1，mean rank 3.31/8，normalized regret 0.297；无 no-evidence/pre-exploration control |
| W2-51 五条件 causal decomposition | 计划 15 clusters、225 sessions、540 participant experiments；正式完成前 8 clusters 的 896/896 truth/replay，candidate 8/8、oracle 7/8 | fresh crystallization oracle `rho=0.738095<0.80`，正式 provider 前科学拒绝；余下 7 clusters 与全部 participant 分母未启动，五个因果对比均未估计 |
| W2-52 large-grid oracle | exposed construction 7/7、2,352/2,352 truth/replay；fresh prospective 1/15、336/336 truth/replay | 320-grid 修复已知失败却在首个新 world 科学拒绝；Top-1 正确但完整排序 `rho=0.714286`，其余 14 clusters 未启动 |
| W2-53 gate-action alignment | 固定 16/16 unit-version，原 Spearman/Top-1 16/16 复现；0 新 truth/provider/物理实验 | rank gate 与 action endpoint 双向不充分：96-grid 有 6 个 rank-pass/Top-1-wrong，fresh 320-grid 为 rank-fail/Top-1-correct；作为 evaluator-design 结果进入正文 |
| W2-59 remaining main-evidence blocks | GPT C2 `3/135` terminal、GPT W2-50 `3/45` terminal、B3 DeepSeek/GPT canary `2/3` 与 `3/3` 后 formal 均 `0/30` | 精确限定 cross-model coverage；保留 2 个分母内失败与 234 个未启动 formal sessions，不补跑、不拼接 |
| W2-60 DeepSeek low reasoning budget | B2 canary `3/3`、formal `15/15`、30/30 turns、0 failures；A-P low 仅 platform-defective partial、formal `0/15` | B2 all-cell low error 与 misindexed exact-law `0/5` 保持，但 primary contrast 反向为 `-0.0405`；这是同 harness robustness，不是 reasoning-off 或配置排名 |
| W2-61 four-condition action successor | 两模型各 180 scheduled slots；donor-eligible DeepSeek/Codex 42/26，共同 26 strata；四条件结果与全部 failures 入表 | 首次直接比较 no evidence、yoked evidence、learned law 与 autonomous exploration；自主探索方向性优于 no evidence，但区间跨零，learned law 无稳定收益，yoked 受 retained failures 主导 |
| W2-62 Codex C2 successor | 135/135 scheduled，126 completed、3 failed、6 right-censored；1,253/1,260 experiments；420 truth、669 checkpoints、129 laws、756 blind | 补齐 C2 双模型；规律压缩明显改善但未转化为 blind action gain |
| W2-63 DeepSeek B3 successor | 30 scheduled，17 completed、13 schema failures；与 Codex 30/30 matched descriptive | joint recovery 0/30 vs 5/30、Top-1 0/30 vs 2/30、eligible gain≥0.02 均 0；结构恢复与行动收益分离 |

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

每个 matched-evidence block 都让 opaque、aligned、misindexed 三臂在同一 Codex thread 中先提交 pre-evidence prediction，再读取逐字相同的 8-row packet，最后对 8 个不重叠 queries 提交 post-evidence prediction。W2-59 使 DeepSeek 与 GPT-5.6-sol medium 都在完全匹配的 worlds、arms、packets 和评分语义上完成 A-P `15/15` 与 A-S B2 `15/15`。两模型合计 `60/60` formal sessions、`120/120` turns、0 failures、0 participant physical experiments；W2-60 又增加 DeepSeek-low B2 `15/15`，使当前有效 matched formal 总数为 `75` sessions。各自 canary 均不进入分析。

### A-P：固定反证使错误参数方向可纠正

opaque/aligned/misindexed 的平均误差分别从 `0.3037/0.2822/0.3105` 降到
`0.0816/0.0804/0.0778`；三臂 post-error 差异不足 `0.004`。misindexed 的注册 update-gain contrast 为
`+0.0309`，3/5 worlds 为正，exact one-sided sign-flip `p=0.125`；小样本不支持单靠 p 值升级普遍主张，
但 5/5 misindexed public summaries 都明确否定“高电位更可靠”，并恢复约 1.1 V 最优、1.3 V 以上坍塌。
结合 Study A 的 A-P suggestive signal，这支持自由探索损失至少部分来自未取得有效反证。

GPT replication 的 opaque/aligned/misindexed mean update gain 为 `0.2551/0.2054/0.2657`，注册 primary contrast `+0.0602`，`5/5` worlds 为正，exact one-sided `p=0.03125`。DeepSeek 与 GPT 的绝对数值不同，但同一固定反证在两个配置上都使三臂 post error 收敛并纠正错误方向；因此该断裂可以升级为 block-specific cross-model replication，而不是一般 LLM 结论。

### 原 A-S Study B：退出当前证据

原 A-S matched-evidence packet 派生自受 world-intervention 缺陷影响的 v0.1 truth source。其 15 个 participant sessions 和原始结果保留，但不再支持当前 Paper 2 claim，也不通过事后重算 truth 修补 participant 已看到的 evidence。

### A-S B2：law-level evidence 到达后仍未形成 exact law

B2 在五个 public worlds 中重新执行 80/80 power-law truth queries，证据与评分均使用不重叠 phase-process 坐标，并在 qualification worlds 预先验证每条 query 至少两个 metric 达到 paired-law effect gate。15/15 sessions、30/30 turns 均一次完成，same-thread 15/15，pre/post 各 360 scoring terms。

opaque/aligned/misindexed 平均 error 从 `0.2255/0.2736/0.3392` 降至 `0.0074/0.0060/0.0071`，对应 gain `0.2181/0.2676/0.3321`。注册主对比为 `+0.0645`，3/5 worlds 为正，exact one-sided sign-flip `p=0.125`，95% 描述区间 `[-0.0557, 0.1848]`。该方向说明 direct diagnostic evidence 带来一个 descriptive acquisition component，但不稳定。

结构表述却没有闭合：misindexed 0/5 明确恢复 exact 1.75 law，仅 1/5 明确拒绝 supplied linear partition form，5/5 转向局部饱和/endpoint 模型。B2 因此拒绝纯二分解释：模型不是“完全不更新”，因为 post error 下降约 98%；也不能说“问题只在没找到证据”，因为 law-level evidence 到达后仍未恢复注册结构。当前机制收束是 **acquisition、numerical revision 与 structural identification 三层分离**。

GPT B2 replication 的 opaque/aligned/misindexed mean update gain 为 `0.2138/0.2017/0.2931`，注册 primary contrast `+0.0915`，`4/5` worlds 为正，exact one-sided `p=0.0625`；misindexed exact 1.75-law recovery 同样为 `0/5`。两个匹配模型配置都表现出强数值收敛而没有错误先验下的结构恢复，使“phenomenological interpolation 不等于 mechanistic identification”成为当前最稳健的跨配置结果。

W2-60 在同一 DeepSeek Codex harness 中只把 reasoning effort 从 `high` 改为 `low`。B2 canary `3/3` 通过，formal `15/15`、30/30 turns、same-thread `15/15`、0 failures；opaque/aligned/misindexed mean post error 为 `0.0067/0.0069/0.0069`，全部 15 cells 低于 0.02，misindexed exact 1.75-law recovery 仍为 `0/5`。primary contrast 则反向为 `-0.0405`，`2/5` worlds 为正，exact one-sided `p=0.8125`，描述区间 `[-0.1559,0.0749]`。provider-reported reasoning output 从 high 的 `506,637` 降至 low 的 `400,639`（-20.9%）。所以 numerical--structural break 对该 reasoning budget 改变稳健，但 selective-update contrast 的方向并不稳健。`low` 不是 provider thinking-off，也不作配置优劣检验。A-P low canary 因外层监督缺陷只留下进度事件，没有 terminal cell receipts/canary summary，按 platform-defective partial 保留；formal `0/15`，不作 A-P low 估计。

W2-56 的独立冻结控制进一步把 1.75 exponent 做成 participant-identifiable。GPT-5.6-sol medium 在 3/3 canary 后完成 30/30 formal cells；opaque/aligned/misindexed post MAE 为 `0.0367/0.0215/0.0378`，joint family+exponent recovery 为 `0/10`、`5/10`、`0/10`。aligned 的 world-mean exponent error 对两个对照均在 5/5 worlds 更低，但错误先验没有发生选择性结构修正。行动侧 Top-1 为 2/30，eligible gain≥0.02 为 0/18。

W2-63 随后在相同 scientific surface 上为 DeepSeek high 建立独立的 30-cell successor，而不拼接或覆盖历史 canary。终态为 `17 completed + 13 participant-schema failures`；failure-aware joint recovery `0/30`、Top-1 `0/30`、regret `0.9579`、post MAE `0.0928`。与 Codex 的 30-coordinate 描述显示 Codex 对应值为 joint recovery `5/30`、Top-1 `2/30`、regret `0.7594`、post MAE `0.0320`，但两模型在 eligible action opportunity 上 gain≥0.02 都为 0。该结果补齐双模型 B3 分母，同时因 differential schema failure 而明确禁止 capability ranking。

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
- W2-59 的 GPT C2 aligned cell、GPT W2-50 misindexed cell 与 DeepSeek B3 canary failure 均按冻结规则保留；W2-61/62/63 是从第一单元开始、使用新 output root 与完整 scheduled denominator 的独立 successor，不是对 W2-59 未启动单元的补跑或结果替换。
- W2-61 的 DeepSeek/Codex yoked condition 仅完成 `10/42` 与 `24/26` donor-admitted sessions；全部 recipient failures 留在 failure-aware 分母，不能把 autonomous-minus-yoked 直接写成纯 experiment-selection advantage。
- W2-62 两模型 C2 selective-correction gate 均未通过；Codex 较低 law error 不得升级为模型总体优越性。
- W2-63 DeepSeek 的 13 个 participant-schema failures 不删除、不替换；B3 双模型差异只作 matched descriptive。
- W2-60 的 A-P low canary 缺 terminal receipts 与 summary，不能以 B2 的成功替代；A-P formal `0/15`。B2 low 的完整 15-session 分母独立保留。

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
- W2-59 双模型主证据收束：`reports/WORK_II_CROSS_MODEL_MAIN_EVIDENCE_COMPLETION_CLOSEOUT_ZH.md`、`reports/work-ii-w2-59-cross-model-main-evidence-closeout-v0.1.json`
- W2-59 GPT B2 机器分析：`reports/WORK_II_AS_STUDY_B2_GPT56_SOL_MEDIUM_RESULTS_ZH.md`、`reports/work-ii-as-study-b2-gpt56-sol-medium-results-v0.1.json`
- W2-60 DeepSeek-low B2：`reports/WORK_II_AS_STUDY_B2_DEEPSEEK_V4_FLASH_LOW_RESULTS_ZH.md`、`reports/work-ii-as-study-b2-deepseek-v4-flash-low-results-v0.1.json`
- W2-61 四条件双模型 action successor：`WORK_II_W250_ACTION_ALIGNED_CAUSAL_EXTENSION_EXPERIMENT_NOTE.md`、`reports/work-ii-w2-61-cross-model-action-aligned-causal-extension-v0.1.json`
- W2-62 Codex C2 与双模型 current-composite：`WORK_II_W262_CODEX_C2_FULL_REPLICATION_EXPERIMENT_NOTE.md`、`reports/WORK_II_W2_62_CODEX_C2_CURRENT_COMPOSITE_EVALUATION_ZH.md`、`reports/WORK_II_W2_62_C2_CROSS_MODEL_CURRENT_COMPOSITE_ZH.md`
- W2-63 DeepSeek B3 与双模型 failure-aware 收束：`WORK_II_W263_DEEPSEEK_B3_FULL_REPLICATION_EXPERIMENT_NOTE.md`、`reports/WORK_II_W2_63_B3_FAILURE_AWARE_CROSS_MODEL_ZH.md`
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

当前所有 participant-bearing 主证据都已有 DeepSeek 与 Codex/GPT-5.6-sol 的 scheduled surface。A-P/B2 是完整 matched formal；W2-62 将 C2 补齐为两模型各 135 scheduled cells；W2-63 将 B3 补齐为两模型各 30 scheduled cells；W2-61 将 W2-50 后继补齐为两模型各 180 个四条件 action slots。三类后继均保持 failure-aware 分母且不覆盖 W2-59 历史 stop boundary。W2-51/W2-52 已按原规则形成终态负/诊断结果，W2-53 进一步确认完整排序与动作充分性分离。当前投稿不再等待 oracle v0.5、W2-59 补跑或真正 thinking-off，下一步选择是：

1. **Study D：artifact transfer。** 在 context reset 后分别测试 typed law、evidence bundle 和更高保真 artifact 对 prediction/law/action 的增益。
2. **Additional-provider extension。** DeepSeek 与 Codex 的主证据覆盖已补齐；若要接入 Qwen、Kimi、WellAU，须另行冻结独立后继块，不能续跑 W2-59 的未启动分母。
3. **A-E private。** 只承担 held-out within-family confirmation；继续延期，除非用户明确把该 claim 纳入下一阶段。
4. **开放式停止与推荐设计。** 未来可统一最大实验预算，允许 agent 提前结束并提交 final plan；这是一项新实验，不事后改写当前 8/10/12 次设计。
5. **Formal action confirmation。** W2-61 已给出 development successor；若要升级为 confirmatory claim，需在稳定 recipient schema 与独立冻结分母上预注册主对比，不得 outcome-selectively 删除当前 yoked failures。

因此可以说当前 DeepSeek public prediction task 已完成，但不能说整个 Paper 2 programme 已结束。当前结果是能力链研究的第一阶段，而不是仓促收缩后的最终论文。
