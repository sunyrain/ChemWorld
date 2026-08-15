# Paper 2 / Work II 全部结果索引

更新日期：2026-08-15

本文件是 Paper 2 当前唯一的结果导航入口。它不替代 raw run、机器 summary、实验 note 或冻结 analysis plan；历史报告只描述各自执行时点，不再作为当前状态入口。

## 1. 当前论文状态

| 层级 | 状态 | 结论 |
|---|---|---|
| 物理化学平台与 exact replay | 已完成当前开发收束 | 正式连续路径、资源账本、稳定 batch identity 和 belief checkpoint 接口已通过回归 |
| Provider-free 可辨识性与机制资格 | 已完成 | 一部分 task/locus 通过，一部分按冻结门槛科学拒绝；失败结果全部保留 |
| DeepSeek C2 public participant | 终态 | 135/135 sessions，1,243/1,260 experiments，121/135 qualification |
| Registered task-aware evaluator | 待完成 | A-E 配对 ITT、A-P ridge/turnover、A-S module/prediction/structure |
| 删失与资源敏感性分析 | 待完成 | 必须包含未通过和右删失 session |
| A-E private | 延期 | public evaluator 后仅在需要 held-out confirmation 时重新授权 |
| 跨 provider replication | 未启动 | WellAU/Qwen/Kimi 仅在保留跨 provider 泛化主张时需要 |
| Manuscript results integration | 进行中 | 当前结果足以形成 public DeepSeek 主体，但不能越过 evaluator 支持 law-recovery 强结论 |

## 2. 当前可以支持的中心论点

1. 正确先验并非普遍有益；其价值取决于任务是否能把先验差异转化为可辨识的实验结果。
2. 在 A-E partition 这类 strong-signal task 上，aligned entity dossier 同时改善首次选择与自由探索后的最佳结果。
3. 错误先验的影响具有任务异质性：它可能持续伤害搜索，也可能在后续实验中被纠正。
4. 给出结构化机制假设可以改善探索组织，但“有结构”不等于“恢复了正确机制”。
5. Endpoint optimization、prior rejection、held-out prediction correction 和 executable-law recovery 是不同能力，不能由 leaderboard score 互相替代。
6. 有限库存、操作次数和时间是任务的一部分；provider 调用预算不设上限不意味着实验室资源无限。

当前不能支持的强结论包括：aligned prior 在所有任务上稳定获胜；agent 已普遍恢复正确物理定律；结果可跨 provider 泛化；private replication 已完成。

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
| DeepSeek C2 public current | 135/135 sessions，1,243/1,260 experiments | 当前 public participant 主体；task-aware evaluator 尚待完成 |

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

## 5. A-S crystallization 特别说明

旧 block 因空晶体群体再次冷却的 runtime-domain 缺陷作废；第一次修复后又暴露实验室热/冷资源卡不足。最终 resource-recovery block 保留物料库存约束，只提高热/冷操作能力并重跑完整 15 sessions。

最终结果为 179/180 experiments、12/15 qualification、2 次真实库存拒绝。历史推荐索引错配属于分析层缺陷：稳定生命周期重建显示 15/15 最终推荐身份有效且都选择公开 incumbent，observed-score regret 为 0。原始历史 qualification 仍保持 12/15，4 个 discard session 的 checkpoint timing 不作事后改写。

## 6. 负结果与不扩展决定

以下结果是论文边界证据，不是待“修好”的失败：

- 五任务 universal A-E distinguishability 未通过；
- crystallization observation-model 候选未达噪声门槛；
- flow reversible-path、catalyst deactivation 和 distillation rollback 效应不足；
- catalyst paired provider trajectories 的同配方机制 gap 未超 gate；
- electrochemical D1 为 retained operational failure；
- A-P 尚未表现稳定 parametric-prior 优势。

这些结果防止论文把 task-specific success 扩大成普遍机制恢复主张。

## 7. 当前结果与图表入口

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

## 8. 收束 Paper 2 的最短剩余路径

1. 对当前 135-session public evidence 运行冻结的 task-aware evaluator。
2. 完成 ITT、右删失和资源拒绝敏感性分析。
3. 形成 endpoint / prediction / executable-law 三层结果表，避免能力概念混用。
4. 用 current source data 生成最终主图和补充图，并完成 Results/Discussion 文本。
5. 决定是否保留 private-confirmation 与 cross-provider claim；若不保留，相应实验不再是论文闭环前置。

因此当前 participant 实验阶段已经收束；论文尚未闭环的核心是 evaluator、统计整合和写作，不是继续扩大 provider 实验矩阵。
