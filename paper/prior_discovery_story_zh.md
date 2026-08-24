# Paper 2 大故事：从实验优化到可执行科学智能

更新时间：2026-08-17

本文档是 Work II 的作者侧论证入口。它不是投稿定稿，也不把当前 DeepSeek cohort 当作研究终点；当前结果是更大研究计划的第一个完整、可干预、可逐层判定的能力剖面。原始 run、机器摘要、实验 note 和注册 evaluator 仍是证据来源。

## 1. 研究对象与中心命题

我们研究的不是“模型能否在化学游戏里拿高分”，而是：一个自主科学 agent 在带着正确、错误或缺失的初始世界模型进入实验后，能否把有限实验转化为可预测、可执行并最终能改善行动的科学知识。

ChemWorld 将这条链拆成彼此不可替代的层级：

> initial world model → evidence acquisition → endpoint adaptation → counterfactual prediction → executable law → unseen action selection → artifact portability

当前 DeepSeek public cohort 给出的核心发现是能力链的系统性解耦：agent 会持续搜索，三个 locus 的平均预测误差也普遍下降；但注册的“错误先验应被更强纠正”并未通过，135 条规律虽然全部可执行，却多数比 final explicit prediction 更有损，blind action 又几乎完全复现 incumbent。新的五世界开放动作矩阵进一步把这一边界推进到未见行动：15 个 persistent sessions 完成 180 次自主实验后，面对结果未知但执行语义完全公开的候选 ActionPlan，0/15 选择真实 Top-1；其中两个达到 law-adequate 的 readout 仍然选错。换言之，实验适应、数值学习、结构识别、规律压缩和行动迁移不是同一个能力，也不会自动级联。

这不是一个低档次的模型失败故事。它建立了一个此前常被总分掩盖的研究对象：**科学智能的转换损失与失效位置**。当前证据已经从 endpoint 一直观测到未见行动选择，形成第一张贯穿取证、预测、规律与行动的失效地图；后续 provider、private world 和 context-reset artifact portability 都可在同一能力链上定位，而不是继续堆叠不可解释的 leaderboard。

## 2. 当前第一阶段的完整证据

### 2.1 Participant 与 evaluator 分母

| 层级 | 结果 | 含义 |
|---|---:|---|
| Matched task–world clusters | 45 | 9 个 task–locus，5 worlds/task |
| Participant sessions | 135/135 terminal | opaque、aligned、misindexed 三臂完整入组 |
| Participant experiments | 1,243/1,260 | 所有失败和未完成分母保留 |
| Qualification | 121/135 | 7 failed、7 right-censored 不做完成者筛选 |
| Belief checkpoints | 675/675 | pre、3 个中间、final |
| Registered query predictions | 6,300 | 共 24,300 query–metric values |
| Evaluator truth | 420/420 | 1,620 个 query–metric truth values，0 provider calls |
| Checkpoint scoring | 675/675 | 全部可评分 |
| Final typed laws | 135/135 | 全部成功执行和评价 |
| Blind replay | 726/810 | 121 个 terminal-evaluable cells 全部完成；84 次因 14 个非终态 participant cells 预定不启动 |

当前分析严格组合 corrected-semantics cohort 中未受影响的 120 cells 与从首 cell 完整重跑的 15-cell A-S crystallization replacement。随后发现 v0.1 evaluator 没有把冻结的 A-S `world_interventions` 传入 truth/blind runtime；v0.2 又从第一 evaluator 单元完整重跑 420 truth 与 726 eligible blind executions。旧 participant/evaluator 缺陷块均不拼接；participant 轨迹、evaluator truth 和 blind replay 彼此分离。

### 2.2 Agent 确实进行了实质性实验搜索

九个 task–locus 的平均 `best − first` 全为正；91.2% 的完成实验采用唯一 recipe，84.4% 的 session 最优点出现在预算后半段。整个 cohort 有 666/1,269 个 closed lifecycles 使用非终点测量，共 872 次 instrument uses。测量率随物理路径变化：结晶和分配高，电化学路径在 electrolysis 后直接 final assay，因此非终点测量为零。该结果证明 agent 利用了连续反馈，不等同于“只执行先验给出的首个方案”。

### 2.3 初始世界模型的 endpoint 效应具有三种原型

1. **持续正确性优势：A-E partition。** aligned 相对 misindexed 的首次实验差为 +0.106，best-score 差为 +0.200，均为 5/5 worlds 同方向。
2. **起跑优势被探索追平：A-S crystallization。** aligned 的首次优势为 +0.141（5/5 worlds），到 best score 缩至 +0.055（3/5）。正确结构主要改变进入搜索空间的位置。
3. **结构化脚手架与事实正确性分离：A-S partition。** aligned 和 misindexed 相对 opaque 的 best-score 优势分别为 +0.163 和 +0.143，而 aligned–misindexed 仅 +0.020。

其余任务提供异质性边界：A-E reaction safety 只有小效应；distillation 的起始差异随后衰减；electrochemistry、A-E crystallization 和两个 A-P 任务均没有稳定的 aligned endpoint 优势。因此不能把正确先验写成普遍性能增强器。

## 3. 决定性结果：能力链在何处断裂

### 3.1 科学纠错：有学习，但没有注册意义上的选择性纠错

所有 135 cells 从 pre 到 final 都有可评分的 held-out predictions，三臂和三个 locus 的平均误差均下降：

| Locus | Opaque | Aligned | Misindexed |
|---|---:|---:|---:|
| A-E | +0.111 | +0.097 | +0.097 |
| A-P | +0.090 | +0.033 | +0.065 |
| A-S | +0.219 | +0.228 | +0.221 |

但注册主问题不是“误差是否下降”，而是错误先验的改善是否显著大于正确先验，同时正确先验不退化。三个 locus 均未通过：

| Locus | Failure-aware primary contrast | Registered p | 结论 |
|---|---:|---:|---|
| A-E | -0.214 | 0.990 | 不通过；aligned noninferiority 通过，但 misindexed selective improvement 不通过 |
| A-P | +0.033 | 0.079 | 两任务均为正，属 suggestive，未过注册阈值 |
| A-S | -0.224 | 1.000 | 不通过；partition 的负方向抵消 crystallization 的局部信号 |

观察点敏感性也不改变结论：A-E 约为 0、A-S 为 -0.0066。失败-aware 规则确实使 crystallization 的非终态 cells 更保守，但总体失败不能被解释成纯删失伪影。

科学含义是：agent 获得了新信息并改善了预测，却没有按干预位置稳定地把额外改进集中在错误初始模型上。**general learning 不等于 targeted model repair。**

### 3.2 规律恢复：可执行性已解决，忠实压缩尚未解决

135/135 final typed laws 均能在 evaluator 坐标上执行。这排除了“只是格式不合法”的浅层解释，但执行后暴露了更深的规律保真问题：

| Locus | Law MAE | Pre→law improvement | Law − final prediction error |
|---|---:|---:|---:|
| A-E | 0.2765 | +0.0161 | +0.0855 |
| A-P | 0.2206 | -0.0156 | +0.0780 |
| A-S | 0.1552 | +0.2059 | +0.0167 |
| Overall | 0.2371 | +0.0513 | +0.0686 |

与 final explicit prediction 相比，law 更好/相等/更差为 50/1/84。A-S 的 pre→law 改善最强，说明结构干预确实最接近规律恢复；但即使在 A-S，规律通常仍比 agent 对具体 query 的最终预测更差。当前瓶颈因此不是 schema 或执行器，而是将局部、条件化 belief 压缩成一个保持预测质量的可复用关系。

### 3.3 Blind action：可复现，但几乎没有新行动价值

121 个可评价 cells 的 726 次 blind replay 全部完成。推荐相对 incumbent 的 better/equivalent/worse 为 1/119/1，recovered 平均 gain 约为 -0.0010。A-E 仅 1 个极小正增益，A-S crystallization 有 1 个明显负例；其余全部等价。

这与 participant 历史中 133/135 推荐精确 incumbent 一致：final action 接口稳定地重放已知最好方案，却没有显示规律驱动的未观察条件优化。可复现性是必要能力，但不是发现增益。

### 3.4 Matched evidence：从二分定位转向三层机制

当前有效 matched-evidence 证据由 A-P Study B 和 A-S B2 各 5 个 worlds 组成。每个 fresh session 先提交
pre-evidence prediction，再在同一 thread 中读取 8 条证据，最后预测 8 个不重叠 queries；合计 30/30 sessions、
60/60 turns、0 failures、0 participant physical experiments。原 Study B A-S branch 的 truth source 没有实际
应用冻结的 structural intervention，该 15-session 结果保留为历史平台缺陷证据，不进入当前 claim。

A-P 给出了清晰的 acquisition 定位。opaque/aligned/misindexed 的平均误差从 `0.3037/0.2822/0.3105` 收敛到
`0.0816/0.0804/0.0778`；5/5 misindexed sessions 都明确推翻“高电位更可靠”，并恢复约 1.1 V 最优、
1.3 V 以上坍塌的响应。错误参数方向在固定反证到达后不再持续，说明 Study A 中的 A-P 损失至少部分发生在
如何取得高信息量证据。

A-S B2 则直接提供预先验证可区分 linear 与 1.75-power response 的 phase-process evidence，并用另一组
phase-process queries 评分。opaque/aligned/misindexed error 从 `0.2255/0.2736/0.3392` 降至
`0.0074/0.0060/0.0071`；misindexed-minus-aligned update-gain contrast 为 `+0.0645`，3/5 worlds 为正，
exact one-sided sign-flip `p=0.125`。这说明 law-level evidence 到达后存在 descriptive prediction-level
acquisition component，但方向不稳定。

更关键的是，misindexed 0/5 恢复 exact 1.75 law，仅 1/5 明确拒绝 supplied linear partition form，5/5 转向
经验饱和/endpoint 模型。模型显然进行了 numerical revision，却没有形成注册结构规律。因此最终机制不再是
“seeking 或 updating”单标签，而是 **evidence acquisition、numerical belief revision 与 structural law
identification 三层分离**。

### 3.5 Open action：规律形成仍不保证未见行动正确

C2 的 blind replay 主要比较 final recommendation 与 participant 已经观察过的 incumbent，因此它能证明
推荐是否可重放，却不能充分检验 agent 能否把实验知识迁移到一个新的行动集合。W2-48 为此引入纵向
open-action assay：同一 persistent session 先自主完成 12 次实验和 `0/3/6/9/12` checkpoints，final
checkpoint 后才看到 8 个完整公开的 ActionPlan；候选 outcome、真实排序和其他臂证据保持隐藏。Public plan、
truth plan 与 executed plan 逐字绑定，从而排除了旧 feature-only packet 隐藏执行语义的解释。

旧 W2-48 五个 fresh partition worlds 的三臂矩阵完成 `15/15` sessions、`180/180` participant
experiments、`120/120` provider-free truth 和 `120/120` exact replay，binding 全部通过。`13/15`
cells 满足完整资格；另外两个虽然完成 12 次实验并提交排序，但 campaign/checkpoint 完整性未通过，
继续保留在 scheduled denominator。它是历史 development block，不与新矩阵合并。

| Arm | Eligible | Mean selected rank | Mean normalized regret | Top-1 |
|---|---:|---:|---:|---:|
| Opaque | 4/5 | 4.25 | 0.3671 | 0/5 |
| Aligned | 4/5 | 6.50 | 0.7658 | 0/5 |
| Misindexed | 5/5 | 6.60 | 0.7477 | 0/5 |

旧 W2-48 的 15 个 terminal readout 均未选择真实 Top-1。更新后的 W2-50 多任务五世界矩阵包含
`45/45` cell records、`42/45` 可评分 cells、`240/240` truth 和 `240/240` exact replay；其中
`11/42` 选择真实 Top-1。W2-50 的 mechanism–action joint outcome 为 `30/42`
inadequate-law/wrong-action、`11/42` inadequate-law/correct-action、`1/42` adequate-law/wrong-action、
`0/42` adequate-law/correct-action。三条结晶失败保留在 scheduled denominator；seed2/aligned repair
只作技术敏感性结果，不替换原始 cell。

W2-50 已经把 full-plan/ranking-only 接口放入 electrochemical、reaction-to-crystallization 和
reaction-safety-constrained 三个任务的五世界矩阵。任务异质性很明显：Top-1 分别为 4/15、3/12 和
4/15，平均 selected rank 分别为 3.60、4.58 和 2.00。这里支持的是跨任务运行和 law-to-action
边界，不支持 pooled prior-arm 泛化；三条结晶失败仍作为结果的一部分保留。

W2-50 仍没有 no-evidence 或 pre-exploration ranking control，因此不能回答“探索证据本身是否因果性地
改善未见计划选择”。W2-51 为此冻结了 no evidence、yoked evidence、autonomous exploration、
learned-law-only 与 oracle-law 五条件设计，计划 15 个 task-world clusters、225 个 fresh sessions 和
540 次 participant experiments。正式 provider-free preparation 在前 8 个 clusters 完成 `896/896`
truth 与 exact replay，candidate gates 为 8/8，但 oracle gates 仅 7/8：第三个 fresh
crystallization formal world 的候选排序 `rho=0.738095`，低于冻结 `0.80`。因此全部 provider sessions
在 operational canary 前被拒绝，剩余 7 个 clusters 未启动，五个 participant contrasts 均未估计。
这不是 W2-50 的阴性 participant effect，而是 causal control 本身未能跨 fresh world 资格化；它进一步
限制了我们把终端排序升级为 action-transfer 因果主张。

## 4. 第一阶段的统一结论

当前 cohort、Study B 与 open-action evidence 同时支持以下七句话：

1. 初始世界模型会因任务和干预位置不同而改变实验起点、搜索组织和 endpoint。
2. Persistent agent 能利用实验反馈进行搜索，并普遍降低 held-out prediction error。
3. 这种学习没有自动形成选择性的错误先验纠正，也没有可靠压缩成高保真 executable law。
4. 最终 action 大多复现 incumbent，说明 prediction、law 和 action 之间存在独立转换损失。
5. Matched evidence 能消除 A-P 错误参数方向；在 A-S，直接结构证据带来 mixed prediction gain，却仍不能保证 exact power-law recovery。
6. 即使候选执行语义完整公开，较合格的规律也不保证 agent 能在未见 ActionPlan 中选出正确行动。
7. 当前还不能把这一 action boundary 解释为探索或 learned law 的因果效应：W2-51 的 fresh formal oracle control 未达冻结正确性门槛，participant cohort 因而没有启动。

最重要的不是某个 p value “阴性”，而是我们获得了同一个系统在完整能力链上的联合观测：**搜索成功与科学纠错可以分离；预测改进与规律恢复可以分离；规律执行与行动迁移也可以分离。**

## 5. 更大的论文计划

### Phase I — Controlled capability map（当前已完成 public DeepSeek）

在 A-E、A-P、A-S 三类世界模型干预下，测量 endpoint、prediction、law 和 action 的转换损失。当前 135-session public cohort 与 current-composite evaluator 已闭环。

### Phase II — Evidence acquisition versus belief revision（A-P Study B + A-S B2 已终态）

当前有效 block 已完成 10 clusters、30 fresh sessions。A-P 支持 evidence-acquisition component；A-S B2 得到
mixed positive prediction contrast 与 0/5 exact law recovery。二元 C3 强主张不支持，Phase II 以三层机制图谱
终态收束，不再追加同类 B2 追求单一标签。

### Phase III — From recovered law to unseen action（描述性终态；causal follow-up 已关闭）

W2-50 在三个任务、五个 world 和三个 arm 中完成 45 个 cell records，并在 final checkpoint 后揭示 8 个
完整 ActionPlan。42 个可评分 readout 中有 11 个 Top-1；唯一 adequate-law cell 仍然选错 action，
因此 Phase III 不是缺失实验，而是当前新的转换损失结果：从规律到未见行动的迁移尚未闭合。

W2-51 随后尝试用五条件设计把这个描述性边界分解为 evidence acquisition、experiment choice、artifact
portability 和 artifact-quality loss。development oracle 在 15/15 worlds 通过，但 fresh formal
preparation 的第 8 个 cluster 以 `rho=0.738095<0.80` 失败。按冻结规则，`896/896` 已完成 truth/replay
和失败结果保留，0 participant sessions、0 provider calls、0 participant experiments；不更换 world、
不补跑，也不报告不存在的因果对比。若未来重新研究 causal action transfer，必须提出明确不同且能在 fresh
worlds 稳健资格化的新 control construction，作为新实验另行授权。

### Phase IV — Artifact portability and compositional transfer（Study D，未启动）

将 agent 生成的 artifact 在 context reset 后交给新 session，测试它能否改善 target prediction、law 和 action。当前 law fidelity 结果意味着 D 不能默认成功；未来可以比较原始 typed law、结构化 evidence bundle 和更高保真 artifact。

### Phase V — Generality（需用户另行授权）

- A-E private：只用于 held-out within-family confirmation，不是当前 public 结论的修补实验。
- Cross-provider：Qwen、Kimi、WellAU 等进入同一 frozen harness，检验失效位置是 agent-system 特异还是跨模型稳定。
- 开放式任务：在统一的最大实验预算与主动 stop/final-plan 接口下，研究何时继续探索、何时停止和如何推荐下一组实验。

这些是大故事的扩展轴，不应在当前结果之后机械地全部跑满。每一阶段都应有独立问题、experiment note、分母和授权。

## 6. 当前 claim 边界

| Claim | 当前状态 |
|---|---|
| 初始世界模型改变实验搜索 | supported，限当前 DeepSeek agent system |
| 正确先验普遍提高 endpoint | rejected；只有 task-specific effects |
| Agent 普遍降低 held-out prediction error | supported descriptively |
| Agent 选择性纠正错误先验 | Study A overall not supported；A-P matched evidence 支持 acquisition component；A-S B2 prediction contrast mixed、exact law recovery 不支持 |
| Final typed laws 可以执行 | supported，135/135 |
| Agent 恢复高保真可复用规律 | not supported overall；A-S 有部分相对恢复 |
| Final recommendation 超越 incumbent | not supported，1/119/1 |
| 结论跨 provider 泛化 | 未测试 |
| Agent 能从 12 轮实验迁移到未见完整 ActionPlan | W2-50 不支持可靠迁移：42 个可评分 cells 中 11/42 Top-1；adequate-law/wrong-action 仍为 1/42 |
| Open-action harness 已跨任务运行 | supported as bounded multi-task matrix：45/45 records、42/45 eligible、240/240 truth 与 replay；不支持 pooled arm effect |
| 自主探索或 learned law 因果性地改善未见计划选择 | 未估计；W2-51 在 participant 前因 fresh crystallization oracle `rho=0.738095<0.80` 科学拒绝，0/225 sessions 启动 |
| 规律 artifact 可在 context reset 后 portability/transfer | 未测试 |

## 7. 主文叙事与图表

1. **Figure 1 — Scientific intelligence chain**：定义从实验到 transfer 的层级和转换损失。
2. **Figure 2 — Intervention programme**：A-E/A-P/A-S、qualification funnel 与 negative candidates。
3. **Figure 3 — Endpoint archetypes**：持续优势、head-start attenuation、structured scaffold。
4. **Figure 4 — Agent work**：实验序列表、measurement、recipe diversity 和 search timing。
5. **Figure 5 — Prediction, law and action dissociation**：45 matched worlds、135 laws、121 blind-evaluable cells 的 current-composite 结果。
6. **Matched-evidence companion analysis**：A-P 参数纠错、A-S B2 world-level gain 与 0/5 exact law recovery；当前作为 Figure 5 的文字/表格伴随分析。
7. **Figure 6 — Multi-task open-action transfer**：W2-50 的 rank、regret、law–action joint categories 与任务异质性；完整 ActionPlan binding 由正文说明。
8. **Supplementary qualification funnel — W2-51**：只展示 15 planned、8 attempted、7 passed、1 oracle rejection、7 not started 与 0 participant calls；不绘制 participant effect panel。
9. **Figure 7 — Failure anatomy and next experiments**：暂不生成新图，先以表格保留 incumbent retrieval 与工具失败边界。

## 8. 现在是否可以说“预测任务完成”

可以精确地说：**当前 DeepSeek public cohort 的 prediction 数据采集、provider-free truth、675 个 checkpoint scoring、注册 selective-correction decision、135 个 law evaluation 和 726 次 blind replay 已全部完成。**

还可以进一步说：**当前 W2-50 多任务五世界 open-action 已完成 45/45 cell records、42/45 可评分
cells、240/240 truth 与 240/240 exact replay，并把 action transfer 确立为独立失效层。**

同时可以说：**W2-51 已按冻结规则完成正式判定并在 provider 前科学拒绝；它关闭了当前五条件设计，
但没有测得 action-transfer 因果效应。**

不能说整个 Paper 2 programme 已完成。尚未完成的是：跨 provider 泛化、A-E private confirmation、
Study D 的 context-reset artifact portability，以及最终是否采用这些扩展轴的研究决策。它们是下一阶段
科学问题，不再是 current-composite evaluator、Study B、W2-50 或 W2-51 的遗留门禁。
