# Paper 2 / Work II 全部结果索引

更新日期：2026-08-15

本文件是 Paper 2 当前唯一的结果导航入口。它不替代 raw run、机器 summary、实验 note 或冻结 analysis plan；历史报告只描述各自执行时点，不再作为当前状态入口。

## 1. 当前论文状态

| 层级 | 状态 | 结论 |
|---|---|---|
| 物理化学平台与 exact replay | 已完成当前开发收束 | 正式连续路径、资源账本、稳定 batch identity 和 belief checkpoint 接口已通过回归 |
| Provider-free 可辨识性与机制资格 | 已完成 | 一部分 task/locus 通过，一部分按冻结门槛科学拒绝；失败结果全部保留 |
| DeepSeek C2 public participant | 终态 | 135/135 sessions，1,243/1,260 experiments，121/135 qualification |
| Participant prediction checkpoints | 已完成采集 | 675/675 snapshots，6,300 registered query predictions，24,300 query–metric values |
| Registered current-composite evaluator | 已完成 | 420/420 truth、675/675 checkpoints、135/135 laws、726/726 launched blind replays；0 provider calls |
| 删失与资源敏感性分析 | 已完成当前 public 主分析 | 7 failed、7 right-censored 与 84 个未启动 blind 分母全部保留；另报 observed-point sensitivity |
| Study B matched evidence | 30/30 终态，部分机制闭环 | A-P 支持 evidence-seeking bottleneck；A-S 暴露 evidence level 与 law level 错配，尚不能定位 updating failure |
| A-E private | 延期 | public evaluator 后仅在需要 held-out confirmation 时重新授权 |
| 跨 provider replication | 未启动 | WellAU/Qwen/Kimi 仅在保留跨 provider 泛化主张时需要 |
| Manuscript story | 第一阶段证据已整合 | `paper/prior_discovery_story_zh.md`；当前 cohort 被定位为大计划的首个完整能力剖面，而非投稿终点 |

## 2. 当前可以支持的中心论点

1. 正确先验并非普遍有益；其价值取决于任务是否能把先验差异转化为可辨识的实验结果。
2. 在 A-E partition 这类 strong-signal task 上，aligned entity dossier 同时改善首次选择与自由探索后的最佳结果。
3. 错误先验的影响具有任务异质性：它可能持续伤害搜索，也可能在后续实验中被纠正。
4. 给出结构化机制假设可以改善探索组织，但“有结构”不等于“恢复了正确机制”。
5. Endpoint optimization、prior rejection、held-out prediction correction 和 executable-law recovery 是不同能力，不能由 leaderboard score 互相替代。
6. 有限库存、操作次数和时间是任务的一部分；provider 调用预算不设上限不意味着实验室资源无限。
7. 固定高信息量反证可以使 A-P 错误参数方向在 5/5 worlds 被明确推翻，但相同数量的 A-S endpoint evidence 并不保证结构规律恢复。
8. 科学纠错不仅要求模型愿意更新，还要求 evidence 与待纠正 law 处于相同可识别层级。

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
| DeepSeek C2 public current | 135/135 sessions，1,243/1,260 experiments；420 truth、675 checkpoints、135 laws、726 blind executions | 当前 public participant 与 evaluator 已闭环；不等于 private、transfer 或跨 provider 已完成 |
| Study B matched evidence | 10 clusters、30/30 fresh sessions、60/60 provider turns、0 participant experiments | A-P 三臂 post-error 收敛；A-S endpoint 校准与 power-law recovery 分离 |

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
- 三个 locus 的平均 prediction error 都有下降，但注册 selective-correction gate 均未通过：A-E `p=0.990`、A-P `p=0.079`、A-S `p=1.000`。A-P 为 suggestive，不能升级为 positive claim。
- 135/135 final typed laws 全部可执行；overall law MAE `0.2438`，law 相对 final explicit prediction 更好/相等/更差为 `49/1/85`，说明可执行性与高保真规律压缩分离。
- 稳定 batch identity 下 133/135 final recommendations 选择精确 observed incumbent；121 个可评价 cells 的 726 次 blind replay 全部完成，better/equivalent/worse 为 `1/119/1`，mean gain `-0.0008`。
- 904 个 failed tool events 中 888 个来自 belief checkpoint 提交。所有 checkpoint 最终恢复，但该 schema friction 必须作为 agent-system 负担报告。

## 5. A-S crystallization 特别说明

旧 block 因空晶体群体再次冷却的 runtime-domain 缺陷作废；第一次修复后又暴露实验室热/冷资源卡不足。最终 resource-recovery block 保留物料库存约束，只提高热/冷操作能力并重跑完整 15 sessions。

最终结果为 179/180 experiments、12/15 qualification、2 次真实库存拒绝。历史推荐索引错配属于分析层缺陷：稳定生命周期重建显示 15/15 最终推荐身份有效且都选择公开 incumbent，observed-score regret 为 0。原始历史 qualification 仍保持 12/15，4 个 discard session 的 checkpoint timing 不作事后改写。

## 6. Study B matched-evidence 机制定位

Study B 使用 A-P electrochemical 与 A-S partition 各 5 个 public worlds；每个 world 的 opaque、aligned、
misindexed 三臂在同一 Codex thread 中先提交 pre-evidence prediction，再读取逐字相同的 8-row packet，最后对
8 个不重叠 queries 提交 post-evidence prediction。正式 block 为 30/30 sessions、60/60 turns、0 failures、
0 participant physical experiments，canary 不进入分析。

### A-P：固定反证使错误参数方向可纠正

opaque/aligned/misindexed 的平均误差分别从 `0.3037/0.2822/0.3105` 降到
`0.0816/0.0804/0.0778`；三臂 post-error 差异不足 `0.004`。misindexed 的注册 update-gain contrast 为
`+0.0309`，3/5 worlds 为正，exact one-sided sign-flip `p=0.125`；小样本不支持单靠 p 值升级普遍主张，
但 5/5 misindexed public summaries 都明确否定“高电位更可靠”，并恢复约 1.1 V 最优、1.3 V 以上坍塌。
结合 Study A 的 A-P suggestive signal，这支持自由探索损失至少部分来自未取得有效反证。

### A-S：数值适应不等于结构纠错

三臂 endpoint error 均下降约 83–86%，但 misindexed 0/5 恢复注册的 1.75 partition power law，仍主要使用
linear/distribution-coefficient 或通用传质缩放。注册主对比为 `-0.0519`、1/5 worlds 为正；该值受到
misindexed pre-error 更低的可改善空间影响，不能直接解释为 stubborn updating。更关键的是 packet 的 8 条
证据全部来自 identity/fixed-process 条件，而评分发生在 phase-process queries；4/5 misindexed summaries 也明确
指出这种证据局限。因此 A-S 当前是设计诊断：packet 能校准 endpoint，但没有提供足够干预去唯一反驳线性结构。

Study B 由此形成部分机制闭环：A-P 支持 evidence-seeking bottleneck；A-S 证明 endpoint adaptation 与
structural correction 可以分离，但尚不能完成 acquisition-vs-updating 的结构 locus 因果定位。若保留完整 C3
主张，需要独立 B2 给出直接分离 linear 与 1.75-power law 的 phase-process 成对证据，不能事后改写本次结果。

## 7. 负结果与不扩展决定

以下结果是论文边界证据，不是待“修好”的失败：

- 五任务 universal A-E distinguishability 未通过；
- crystallization observation-model 候选未达噪声门槛；
- flow reversible-path、catalyst deactivation 和 distillation rollback 效应不足；
- catalyst paired provider trajectories 的同配方机制 gap 未超 gate；
- electrochemical D1 为 retained operational failure；
- A-P 尚未表现稳定 parametric-prior 优势。

这些结果防止论文把 task-specific success 扩大成普遍机制恢复主张。

## 8. 当前结果与图表入口

- 当前 Paper 2 论文故事：`../../paper/prior_discovery_story_zh.md`
- Study B 机制分析：`reports/WORK_II_STUDY_B_MATCHED_EVIDENCE_RESULTS_ZH.md`
- Study B 机器结果：`reports/work-ii-study-b-matched-evidence-results-v0.1.json`
- C2 agent 行为与 prediction-collection 机器分析：`reports/work-ii-deepseek-c2-paper-story-analysis-v0.1.json`
- C2 current-composite evaluator 报告：`reports/WORK_II_DEEPSEEK_C2_CURRENT_COMPOSITE_EVALUATION_ZH.md`
- C2 current-composite evaluator 机器结果：`reports/work-ii-deepseek-c2-current-composite-evaluation-v0.1.json`
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

当前 DeepSeek public 的 participant、prediction truth/scoring、law evaluation、blind action 与 failure-aware sensitivity 已闭环。当前缺口不再是 evaluator 门禁，而是大研究计划的下一步选择：

1. **A-S Study B2（仅在保留完整 C3 时）。** 用 phase-process 成对干预直接分离 linear 与 1.75-power law，再用不重叠 phase-process queries 评分。
2. **Study D：artifact transfer。** 在 context reset 后分别测试 typed law、evidence bundle 和更高保真 artifact 对 prediction/law/action 的增益。
3. **Cross-provider replication。** 只有需要检验失效位置的模型普适性时，再把 Qwen、Kimi 或 WellAU 接入同一 frozen harness。
4. **A-E private。** 只承担 held-out within-family confirmation；继续延期，除非用户明确把该 claim 纳入下一阶段。
5. **开放式停止与推荐设计。** 未来可统一最大实验预算，允许 agent 提前结束并提交 final plan；这是一项新实验，不事后改写当前 8/10/12 次设计。

因此可以说当前 DeepSeek public prediction task 已完成，但不能说整个 Paper 2 programme 已结束。当前结果是能力链研究的第一阶段，而不是仓促收缩后的最终论文。
