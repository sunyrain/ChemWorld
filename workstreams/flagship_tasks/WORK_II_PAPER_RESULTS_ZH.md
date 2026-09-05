# Paper 2 / Work II 全部结果索引

更新日期：2026-09-05

本文件是 Paper 2 当前唯一的结果导航入口。它不替代 raw run、机器 summary、实验 note 或冻结 analysis plan；历史报告只描述各自执行时点，不再作为当前状态入口。

## 1. 当前结果概览

本文件只管理已完成结果和来源；执行状态见 [TODO](WORK_II_TODOLIST.md)，
新实验及既有证据处置见 [实验矩阵](WORK_II_EXPERIMENT_MATRIX.md)。

| 证据块 | 终态分母（DeepSeek / GPT，除非另注） | 可支持的结果 |
| --- | --- | --- |
| C2 public | 各135 scheduled；121/126 completed；1,243/1,253 completed experiments，各1,260 planned | 平均预测改善；原selective-correction gates均未通过 |
| C2 evaluator | 各420 truth；675/669 checkpoints；135/129 laws；726/756 blind executions，原scheduled各810 | law MAE 0.2371/0.1753、compression loss 0.0686/0.0142；incumbent gain约为零 |
| A-P/B2 matched | 每模型每块15/15 sessions，合计60；另DeepSeek-low B2为15/15 | 条件性packet后响应；B2三配置错误组exact expression均0/5，存在精确alias |
| B3 | 各30 scheduled；17/30 completed；13/0 schema failures | joint recovery 0/30与5/30；固定机会分母useful gain均0/18 |
| W2-50/64 | DeepSeek-only，45 scheduled、42 rankings、240 truth/replay | law Top-1 0/45、participant 11/45、follow-law 12/42；描述性差异 |
| W2-61 | 各180 slots、45 strata；donor eligible42/26；yoked完成10/42与24/26 | all-scheduled autonomy-minus-none regret -0.0913/+0.1102，两区间跨零；development系统策略比较 |
| M1正式复核 | 10 worlds、40来源状态、120/120 sessions、160/160条件、200/200物理与replay；零失败 | 主差−0.00538，95%区间[−0.01630,+0.00061]，未支持实质收益；F-A/F-X 40/40一致 |
| M3信息分离 | 复用M1的10 worlds与40来源；160/160接收会话、80/80新隐藏物理与replay，零失败 | L−none −0.13723，95%区间[−0.15584,−0.12257]，支持实质收益；nearest10/10最优，无新机制迁移结论 |
| W2-55 | DeepSeek 135同域prediction states | 合法schema容量充足，不证明泛化或表示替换收益 |
| W2-51/52/53 | 原五条件0 participant；16个完成unit-version诊断 | 完整排序与决策目标不同；旧stop rules及未启动分母保留 |

以上“双模型覆盖”指相应scheduled surface形成终态，不表示全部完成或模型优劣排序。
Codex是共同session harness；“DeepSeek--Codex participant”不是双模型ensemble。
前置材料信息三臂基线的60/60 cells、2,280 experiments是单独的GPT队列，不进入C2。

### M0/M1开发结果（独立于上述论文证据）

[机器摘要](reports/work-ii-m0-m1-development-20260905.json)与
[可读对照表](reports/work-ii-m0-m1-development-20260905.md)，规则见
[实验note](WORK_II_M0_M1_DEVELOPMENT_EXPERIMENT_NOTE.md)。2个开发task-worlds，
42/42执行与replay、12/12 provider sessions、16/16 factorial slots完成；没有失败或替换。
DeepSeek电化学规则替换改善regret 0.016772；GPT结晶拟合artifact替换改善0.134529。
其余固定执行器下artifact对比为零，所有F-A/F-X选择一致；全部结果和简单基线均保留。
这是功能/成本校准及局部现象，不是正式多world复核、一般规律发现或已验证方法贡献。

### M1独立世界正式复核

[完整报告](reports/work-ii-m1-replication-20260905.md)和[机器数据](reports/work-ii-m1-replication-20260905.json)
按[执行前说明](WORK_II_M1_REPLICATION_EXPERIMENT_NOTE.md)生成，绑定入口为current中的w2_72_m1_replication。
主对比F-X minus L-X为−0.0053838，95%区间[−0.0163027,+0.0006139]；事前实质收益规则未通过。
电化学/结晶task均值为−0.0108685/+0.0001009，收益集中在一个电化学world。
F-A/F-X 40/40选择一致，L-A/L-X 39/40一致；零宽区间仅描述样本，不证明总体等价。
拟合、最近邻、均匀随机期望regret分别为0.0042525、0.0035450、0.1110900。
两个模型的拟合条件均有14/20近优、10/20 Top-1；重复拟合副本不增加十个独立world的分母。

物理/replay29.7分钟，provider147.7分钟；输入1,623,791（cache450,816）、输出942,258
（reasoning939,441），120/120有usage记录。所有条件完成，scheduled与completed-only相同。
这是固定公开证据和局部二次类的正式边界证据；不支持普遍law-use失败、实质修复优势、
artifact-only迁移或新算法优势。独立artifact效用由后续M3测试；开发canary未回填正式分母。

### M3信息分离与同世界新候选

[完整报告](reports/work-ii-m3-portability-20260905.md)及[机器数据](reports/work-ii-m3-portability-20260905.json)
按[执行前说明](WORK_II_M3_PORTABILITY_EXPERIMENT_NOTE.md)生成，由current的w2_69_m3_portability绑定。
复用全部10个M1 worlds、40个封存来源和120次既有公开观测；8个新候选/world在结果前固定。
none/raw/L-only/F-only均为fresh、无工具接收者，L/F没有raw或来源对话；原始law不重拟合。
160/160会话与条件、80/80新隐藏物理和80/80 exact replay完成；零失败、重试或替换。
**新增独立world为0**；模型和重复嵌套于原10个world，不能将M1/M3合计成20个独立世界。

| 预设regret对比 | 均值 | 区间 |
| --- | ---: | --- |
| L−none（primary） | −0.137231 | 95% [−0.155845, −0.122566] |
| raw−none | −0.136032 | 99% [−0.166955, −0.106025] |
| F−none | −0.132680 | 99% [−0.164488, −0.099817] |
| L−raw | −0.001199 | 99% [−0.023529, +0.009508] |
| F−raw | +0.003352 | 99% [−0.021421, +0.037629] |
| F−L | +0.004551 | 99% [−0.008013, +0.031772] |

主区间上界低于−0.01，支持预设实质收益。电化学/结晶task主差−0.25937/−0.01509；
九个world负差、一个零差。均值与区间由20,000次按task分层、以world为单位的bootstrap得到，
保留模型/重复配对；每task仅五个world，区间仍是小样本近似。

| 信息/控制 | 平均regret | 近优 | Top-1 |
| --- | ---: | ---: | ---: |
| none | 0.147270 | 13/40 | 13/40 |
| raw | 0.011237 | 30/40 | 26/40 |
| L | 0.010039 | 23/40 | 20/40 |
| F | 0.014589 | 24/40 | 20/40 |
| nearest | 0 | 10/10 | 10/10 |

确定性L-X/F-X regret为0.010039/0.006091，均匀随机精确期望为0.120217。
L/maximizer选择一致40/40，F为39/40；一个合法F偏离使其recipient均值更高，原样保留。
nearest按world只计一次，不把来源副本算作40次独立成功。

新增physics/replay724.6秒、provider2,722.6秒；输入1,716,721（cache648,704），
输出255,544（reasoning253,304），160/160有usage回执。L/raw输入392,101/541,225，
少27.6%；prompt bytes351,996/838,900，少58.0%。两者不可混称为token压缩率。
来源取证与law生成已计入M1成本，另列历史共享成本，不重复收费式计数。

结果支持压缩知识在同世界新候选上的独立决策效用，不支持优于或等价于raw/nearest，
也不支持实验节省、新参数/机制/拓扑迁移或内部中介。M2/M4及机制匹配新条件块均未执行。

## 2. 当前可以支持的中心论点

1. 预测质量、提交的可执行规律与实际决策是不同可观测量。显式law不能等同于内部belief。
2. 初始描述的价值依任务而异；操作的是提供给参与者的信息，未随机干预内部知识或law使用。
3. C2有平均预测改善和规律压缩损失；H3受初始误差headroom影响，gate未通过不证明没有纠错能力。
4. W2-50/64的law与行为不一致尚未定位原因；11/42 Top-1本身不估计实验收益，也不是匹配随机对照。
5. W2-61估计的是包含availability与delivery failures的系统策略；不能隔离纯取证或因果中介。
6. B2只作表达与可识别性诊断；B3测试有界函数形式，不是一般因果图发现。
7. evaluator和interface缺陷与Agent科学表现分别报告；所有失败和历史拒绝继续保留。

8. M1直接干预未支持预设实质拟合收益，且拟合规律下40/40 A/X一致；限制普遍law-use断裂解释。
9. M3支持artifact脱离来源对话/raw后仍能支持同世界新候选，但nearest已达到实测最优，任务差异大。

尚不支持：普遍规律恢复、超过强基线的稳健方法、新物理条件迁移或真实实验室效度。

## 3. 证据角色与历史记录

主文、补充诊断、冻结Work I和未执行扩展的唯一处置表在 [实验矩阵](WORK_II_EXPERIMENT_MATRIX.md)。
本文件第4–7节保留当前C2/matched证据及不可替换的失败；第8节提供原始报告导航。
旧全景表、任务完成日志与候选扩展队列由Git历史保存，不继续维护平行研究计划。
原experiment notes、机器summary、runs和冻结规则没有因本次整理删除或改写。

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

- A-E distillation 的首次 aligned 优势在自由探索后大幅缩小，只显示两臂终点差距缩小，不能单独证明错误先验被纠正。
- A-E electrochemistry 和两个 A-P task 均无稳定 aligned 终点优势。
- 九个 task/locus 的 mean best-first 全为正，描述持续搜索后的最优值改善；随机或非自适应搜索也可能产生正值，不能单独识别反馈学习。

### Agent 工作与预测提交

- 91.2% 的完成实验为唯一 recipe；84.4% 的 session 最优值出现在预算后半段，说明持续搜索与观测，尚未隔离利用反馈的因果收益。
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

## 6. Matched-evidence 条件性响应：A-P Study B 与 A-S B2

每个 matched-evidence block 都让 opaque、aligned、misindexed 三臂在同一 Codex thread 中先提交 pre-evidence prediction，再读取逐字相同的 8-row packet，最后对 8 个不重叠 queries 提交 post-evidence prediction。它固定 packet 内容，但 packet 与额外 response turn 同时加入；没有 turn-matched no-packet control，因此只能解释为 conditional post-packet response，不能称为纯 evidence-packet 因果效应。W2-59 使 DeepSeek 与 GPT-5.6-sol medium 都在完全匹配的 worlds、arms、packets 和评分语义上完成 A-P `15/15` 与 A-S B2 `15/15`。两模型合计 `60/60` formal sessions、`120/120` turns、0 failures、0 participant physical experiments；W2-60 又增加 DeepSeek-low B2 `15/15`，使当前有效 matched formal 总数为 `75` sessions。各自 canary 均不进入分析。

### A-P：固定反证使错误参数方向可纠正

opaque/aligned/misindexed 的平均误差分别从 `0.3037/0.2822/0.3105` 降到
`0.0816/0.0804/0.0778`；三臂 post-error 差异不足 `0.004`。misindexed 的注册 update-gain contrast 为
`+0.0309`，3/5 worlds 为正，exact one-sided sign-flip `p=0.125`；小样本不支持单靠 p 值升级普遍主张，
但 5/5 misindexed public summaries 都明确否定“高电位更可靠”，并恢复约 1.1 V 最优、1.3 V 以上坍塌。
这为取证或上下文条件影响提供后续假设；由于额外response turn未单独控制，不能据此唯一定位自由探索损失。

GPT replication 的 opaque/aligned/misindexed mean update gain 为 `0.2551/0.2054/0.2657`，注册 primary contrast `+0.0602`，`5/5` worlds 为正，exact one-sided `p=0.03125`。DeepSeek 与 GPT 的绝对数值不同，但同一固定反证在两个配置上都使三臂 post error 收敛并纠正错误方向；因此该条件性响应具有 block-specific cross-model replication，而不是一般 LLM 结论。

### 原 A-S Study B：退出当前证据

原 A-S matched-evidence packet 派生自受 world-intervention 缺陷影响的 v0.1 truth source。其 15 个 participant sessions 和原始结果保留，但不再支持当前 Paper 2 claim，也不通过事后重算 truth 修补 participant 已看到的 evidence。

### A-S B2：低 post-packet error 未伴随稳定 exact-law expression

B2 在五个 public worlds 中重新执行 80/80 power-law truth queries，证据与评分使用不重叠 phase-process coordinates，并在 qualification worlds 验证每条 query 至少两个 metric 达到 paired-law effect gate。15/15 sessions、30/30 turns 均一次完成，same-thread 15/15，pre/post 各 360 scoring terms。后续 participant-visible audit 发现这些坐标只覆盖一个 nominal solvent/extractant pair，未公开 base partition coefficient，也没有 typed family/exponent 字段，因此 qualification 的数值 effect 不等于结构族可识别性。

opaque/aligned/misindexed 平均 error 从 `0.2255/0.2736/0.3392` 降至 `0.0074/0.0060/0.0071`，对应 gain `0.2181/0.2676/0.3321`。注册主对比为 `+0.0645`，3/5 worlds 为正，exact one-sided sign-flip `p=0.125`，95% 描述区间 `[-0.0557, 0.1848]`。该方向只支持 descriptive conditional post-packet response，不能把 packet 与额外 turn 拆成纯 acquisition effect。

事后 public-summary coding 显示：misindexed 0/5 表达 exact 1.75 law，仅 1/5 明确拒绝 supplied linear partition form，5/5 转向局部饱和/endpoint 模型。可是该表面存在 free-coefficient linear law 与 1.75-power law 的精确 alias（系数倍数 `3.13588`）；常数 endpoint baseline 的 mean MAE 已达 `0.00649`，aligned DeepSeek-high exact-law positive control 也只有 `1/5` 并未通过 readout criterion。因此 B2 只支持 **underidentifying free-text surface 上的 conditional post-packet numerical--exact-law-expression dissociation**，不能把 0/5 定位为 agent 内部 structural-identification failure。

GPT B2 replication 的 opaque/aligned/misindexed mean update gain 为 `0.2138/0.2017/0.2931`，注册 primary contrast `+0.0915`，`4/5` worlds 为正，exact one-sided `p=0.0625`；misindexed exact 1.75-law expression 同样为 `0/5`。两个匹配模型配置都表现出强数值收敛而没有稳定 exact-law expression；这是一致的 block-specific expression diagnostic，不是结构恢复率。

W2-60 在同一 DeepSeek Codex harness 中只把 reasoning effort 从 `high` 改为 `low`。B2 canary `3/3` 通过，formal `15/15`、30/30 turns、same-thread `15/15`、0 failures；opaque/aligned/misindexed mean post error 为 `0.0067/0.0069/0.0069`，全部 15 cells 低于 0.02，misindexed exact 1.75-law expression 仍为 `0/5`。primary contrast 则反向为 `-0.0405`，`2/5` worlds 为正，exact one-sided `p=0.8125`，描述区间 `[-0.1559,0.0749]`。provider-reported reasoning output 从 high 的 `506,637` 降至 low 的 `400,639`（-20.9%）。所以 numerical--expression pattern 对该 reasoning budget 改变稳健，但 selective-update contrast 的方向并不稳健。`low` 不是 provider thinking-off，也不作配置优劣检验。A-P low canary 因外层监督缺陷只留下进度事件，没有 terminal cell receipts/canary summary，按 platform-defective partial 保留；formal `0/15`，不作 A-P low 估计。

W2-56 的独立冻结控制进一步把 1.75 exponent 做成 participant-identifiable。GPT-5.6-sol medium 在 3/3 canary 后完成 30/30 formal cells；opaque/aligned/misindexed post MAE 为 `0.0367/0.0215/0.0378`，joint family+exponent recovery 为 `0/10`、`5/10`、`0/10`。aligned 的 world-mean exponent error 对两个对照均在 5/5 worlds 更低，但错误先验没有发生选择性结构修正。行动侧 Top-1 为 2/30，eligible gain≥0.02 为 0/18。

W2-63 随后在相同 scientific surface 上为 DeepSeek high 建立独立的 30-cell successor，而不拼接或覆盖历史 canary。终态为 `17 completed + 13 participant-schema failures`；failure-aware joint recovery `0/30`、Top-1 `0/30`、regret `0.9579`、post MAE `0.0928`。与 GPT-5.6-sol 的 30-coordinate 描述显示 GPT 对应值为 joint recovery `5/30`、Top-1 `2/30`、regret `0.7594`、post MAE `0.0320`，但两模型在 eligible action opportunity 上 gain≥0.02 都为 0。该结果补齐双模型 B3 分母，同时因 differential schema failure 而明确禁止 capability ranking。

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
- W2-61 的 DeepSeek/GPT yoked condition 仅完成 `10/42` 与 `24/26` donor-admitted sessions；全部 recipient failures 留在 failure-aware 分母，不能把 autonomous-minus-yoked 直接写成纯 experiment-selection advantage。
- W2-62 两模型 C2 selective-correction gate 均未通过；GPT 较低 law error 不得升级为模型总体优越性。
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
- W2-62 GPT-5.6-sol C2（经 Codex harness）与双模型 current-composite：`WORK_II_W262_CODEX_C2_FULL_REPLICATION_EXPERIMENT_NOTE.md`、`reports/WORK_II_W2_62_CODEX_C2_CURRENT_COMPOSITE_EVALUATION_ZH.md`、`reports/WORK_II_W2_62_C2_CROSS_MODEL_CURRENT_COMPOSITE_ZH.md`
- W2-63 DeepSeek B3 与双模型 failure-aware 收束：`WORK_II_W263_DEEPSEEK_B3_FULL_REPLICATION_EXPERIMENT_NOTE.md`、`reports/WORK_II_W2_63_B3_FAILURE_AWARE_CROSS_MODEL_ZH.md`
- W2-64 provider-free publication reanalysis：`WORK_II_W264_PUBLICATION_REANALYSIS_EXPERIMENT_NOTE.md`、`reports/work-ii-w2-64-publication-reanalysis-v0.1.json`
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

## 9. 下一阶段入口

先做M0测量/执行面，再做M1固定证据的表示×决策器干预；M3是新条件知识价值的优先扩展。
M2仅在主张取证因果价值时必需，M4提供独立外部复核。规模、对照、指标和停止边界统一见
[实验矩阵](WORK_II_EXPERIMENT_MATRIX.md)，任务状态仅在 [TODO](WORK_II_TODOLIST.md) 更新。
本次没有启动新实验，也没有把历史失败或未启动分母恢复为待补跑工作。
