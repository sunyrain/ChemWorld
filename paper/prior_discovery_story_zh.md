# Paper 2 大故事：从实验优化到可执行科学智能

更新时间：2026-08-15

本文档是 Work II 的作者侧论证入口。它不是投稿定稿，也不把当前 DeepSeek cohort 当作研究终点；当前结果是更大研究计划的第一个完整、可干预、可逐层判定的能力剖面。原始 run、机器摘要、实验 note 和注册 evaluator 仍是证据来源。

## 1. 研究对象与中心命题

我们研究的不是“模型能否在化学游戏里拿高分”，而是：一个自主科学 agent 在带着正确、错误或缺失的初始世界模型进入实验后，能否把有限实验转化为可预测、可执行并最终能改善行动的科学知识。

ChemWorld 将这条链拆成彼此不可替代的层级：

> initial world model → evidence seeking → endpoint adaptation → counterfactual prediction → executable law → blind action → transfer

当前 DeepSeek public cohort 给出的核心发现是能力链的系统性解耦：agent 会持续搜索，三个 locus 的平均预测误差也普遍下降；但注册的“错误先验应被更强纠正”并未通过，135 条规律虽然全部可执行，却多数比 final explicit prediction 更有损，blind action 又几乎完全复现 incumbent。换言之，实验适应、预测学习、规律压缩和行动改进不是同一个能力，也不会自动级联。

这不是一个低档次的模型失败故事。它建立了一个此前常被总分掩盖的研究对象：**科学智能的转换损失与失效位置**。当前 cohort 是第一张失效地图，后续 provider、private world、主动取证和 artifact transfer 都可在同一能力链上定位，而不是继续堆叠不可解释的 leaderboard。

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

当前分析严格组合 corrected-semantics cohort 中未受影响的 120 cells 与从首 cell 完整重跑的 15-cell A-S crystallization replacement。旧的缺陷块不拼接；participant 轨迹、evaluator truth 和 blind replay 彼此分离。

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
| A-S | +0.157 | +0.192 | +0.149 |

但注册主问题不是“误差是否下降”，而是错误先验的改善是否显著大于正确先验，同时正确先验不退化。三个 locus 均未通过：

| Locus | Failure-aware primary contrast | Registered p | 结论 |
|---|---:|---:|---|
| A-E | -0.214 | 0.990 | 不通过；aligned noninferiority 通过，但 misindexed selective improvement 不通过 |
| A-P | +0.033 | 0.079 | 两任务均为正，属 suggestive，未过注册阈值 |
| A-S | -0.257 | 1.000 | 不通过；partition 的负方向抵消 crystallization 的局部信号 |

观察点敏感性也不改变结论：A-E 约为 0、A-S 仍为负。失败-aware 规则确实使 crystallization 的非终态 cells 更保守，但总体失败不能被解释成纯删失伪影。

科学含义是：agent 获得了新信息并改善了预测，却没有按干预位置稳定地把额外改进集中在错误初始模型上。**general learning 不等于 targeted model repair。**

### 3.2 规律恢复：可执行性已解决，忠实压缩尚未解决

135/135 final typed laws 均能在 evaluator 坐标上执行。这排除了“只是格式不合法”的浅层解释，但执行后暴露了更深的规律保真问题：

| Locus | Law MAE | Pre→law improvement | Law − final prediction error |
|---|---:|---:|---:|
| A-E | 0.2765 | +0.0161 | +0.0855 |
| A-P | 0.2206 | -0.0156 | +0.0780 |
| A-S | 0.1851 | +0.1423 | +0.0236 |
| Overall | 0.2438 | +0.0371 | +0.0701 |

与 final explicit prediction 相比，law 更好/相等/更差为 49/1/85。A-S 的 pre→law 改善最强，说明结构干预确实最接近规律恢复；但即使在 A-S，规律通常仍比 agent 对具体 query 的最终预测更差。当前瓶颈因此不是 schema 或执行器，而是将局部、条件化 belief 压缩成一个保持预测质量的可复用关系。

### 3.3 Blind action：可复现，但几乎没有新行动价值

121 个可评价 cells 的 726 次 blind replay 全部完成。推荐相对 incumbent 的 better/equivalent/worse 为 1/119/1，平均 gain 为 -0.00082。A-E 仅 1 个极小正增益，A-S crystallization 有 1 个明显负例；其余全部等价。

这与 participant 历史中 133/135 推荐精确 incumbent 一致：final action 接口稳定地重放已知最好方案，却没有显示规律驱动的未观察条件优化。可复现性是必要能力，但不是发现增益。

### 3.4 Matched evidence：参数纠错与结构纠错再次分离

Study B 在 A-P electrochemical 和 A-S partition 各选择 5 个 worlds，为三种 prior arms 提供逐字相同且不占用
participant 实验预算的证据。每个 fresh session 先提交 pre-evidence prediction，再在同一 thread 中读取 8 条证据，
最后预测 8 个不重叠 queries。30/30 sessions、60/60 turns 全部完成，0 failures、0 participant physical
experiments。

A-P 给出了清晰的 seeking 定位。opaque/aligned/misindexed 的平均误差从 `0.3037/0.2822/0.3105` 收敛到
`0.0816/0.0804/0.0778`；5/5 misindexed sessions 都明确推翻“高电位更可靠”，并恢复约 1.1 V 最优、
1.3 V 以上坍塌的响应。错误参数方向在固定反证到达后不再持续，说明 Study A 中的 A-P 损失至少部分发生在
如何取得高信息量证据。

A-S 没有给出同样简单的 updating 结论。三臂 endpoint error 都下降约 83–86%，但 misindexed 0/5 恢复注册的
1.75 partition power law，仍用 linear/distribution-coefficient 或通用传质缩放。与此同时，输入证据全部来自
identity/fixed-process 条件；4/5 misindexed summaries 主动指出缺少 phase-process 证据。因此这里同时观察到
数值适应与结构规律未恢复，却不能断言模型在看到充分结构反证后仍拒绝更新——packet 本身没有在 law level
形成充分反证。

Study B 由此揭示新的转换条件：**correction requires intervention-complete evidence at the same abstraction
level as the law**。参数规律可以被局部方向性证据修正；结构规律需要能区分 mechanism family 的干预证据，
不能由 endpoint 校准自动替代。

## 4. 第一阶段的统一结论

当前 cohort 与 Study B 同时支持以下五句话：

1. 初始世界模型会因任务和干预位置不同而改变实验起点、搜索组织和 endpoint。
2. Persistent agent 能利用实验反馈进行搜索，并普遍降低 held-out prediction error。
3. 这种学习没有自动形成选择性的错误先验纠正，也没有可靠压缩成高保真 executable law。
4. 最终 action 大多复现 incumbent，说明 prediction、law 和 action 之间存在独立转换损失。
5. Matched evidence 能消除 A-P 错误参数方向，却不能在缺乏结构区分干预时保证 A-S power-law recovery。

最重要的不是某个 p value “阴性”，而是我们获得了同一个系统在完整能力链上的联合观测：**搜索成功与科学纠错可以分离；预测改进与规律恢复可以分离；规律执行与行动增益也可以分离。**

## 5. 更大的论文计划

### Phase I — Controlled capability map（当前已完成 public DeepSeek）

在 A-E、A-P、A-S 三类世界模型干预下，测量 endpoint、prediction、law 和 action 的转换损失。当前 135-session public cohort 与 current-composite evaluator 已闭环。

### Phase II — Evidence seeking versus belief updating（Study B 已执行，部分闭环）

Study B 已完成 10 clusters、30 fresh sessions。A-P 支持 evidence-seeking bottleneck；A-S 则证明只匹配证据数量
并不足够，证据还必须与待纠正 law 的干预层级匹配。若要把结构 locus 也归因到 seeking 或 updating，需要独立
A-S B2 提供直接分离 linear 与 1.75-power law 的 phase-process paired evidence，而不是事后修改当前 packet。

### Phase III — Law portability and compositional transfer（Study D，未启动）

将 agent 生成的 artifact 在 context reset 后交给新 session，测试它能否改善 target prediction、law 和 action。当前 law fidelity 结果意味着 D 不能默认成功；未来可以比较原始 typed law、结构化 evidence bundle 和更高保真 artifact。

### Phase IV — Generality（需用户另行授权）

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
| Agent 选择性纠正错误先验 | Study A overall not supported；Study B matched evidence 下 A-P supported，A-S unresolved |
| Final typed laws 可以执行 | supported，135/135 |
| Agent 恢复高保真可复用规律 | not supported overall；A-S 有部分相对恢复 |
| Final recommendation 超越 incumbent | not supported，1/119/1 |
| 结论跨 provider 泛化 | 未测试 |
| 规律可以 transfer | 未测试 |

## 7. 主文叙事与图表

1. **Figure 1 — Scientific intelligence chain**：定义从实验到 transfer 的层级和转换损失。
2. **Figure 2 — Intervention programme**：A-E/A-P/A-S、qualification funnel 与 negative candidates。
3. **Figure 3 — Endpoint archetypes**：持续优势、head-start attenuation、structured scaffold。
4. **Figure 4 — Agent work**：实验序列表、measurement、recipe diversity 和 search timing。
5. **Figure 5 — Prediction, law and action dissociation**：45 matched worlds、135 laws、121 blind-evaluable cells 的 current-composite 结果。
6. **Figure 6 — Matched-evidence mechanism localization**：A-P 参数纠错、A-S endpoint/law 分离与 evidence-level mismatch。
7. **Figure 7 — Failure anatomy and next experiments**：seeking、updating、compression、action、transfer 的定位框架。

## 8. 现在是否可以说“预测任务完成”

可以精确地说：**当前 DeepSeek public cohort 的 prediction 数据采集、provider-free truth、675 个 checkpoint scoring、注册 selective-correction decision、135 个 law evaluation 和 726 次 blind replay 已全部完成。**

不能说整个 Paper 2 programme 已完成。尚未完成的是：跨 provider 泛化、A-E private confirmation、可选的
A-S Study B2、Study D 的 artifact transfer，以及最终是否采用这些扩展轴的研究决策。它们是下一阶段科学问题，
不再是 current-composite evaluator 或已完成 Study B block 的遗留门禁。
