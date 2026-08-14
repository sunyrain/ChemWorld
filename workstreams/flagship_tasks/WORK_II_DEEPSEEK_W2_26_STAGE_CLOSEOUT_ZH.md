# Work II DeepSeek W2-26 阶段收束与深入分析

日期：2026-08-14  
状态：DeepSeek development cohort 已终态收束；WellAU 按用户指令暂停；不属于 formal / R5 / private evidence。

## 1. 执行结论

本阶段已经得到可分析的完整 DeepSeek 开发矩阵，不再重跑或补齐不利结果：

- `9/9` 个 task triplets 和 `27/27` 个 cells 均有终态记录；
- 完成 `251/252` 个计划实验，`26/27` 个 cells 达到完整轮次；
- `135/135` 个 typed belief checkpoints 完成；
- `27/27` 个终态 provider receipts 正常完成，终态记录中 provider error 为 `0`；
- `27/27` 个 cells 的已执行轨迹均通过 exact replay；
- 平台缺陷 `0`，unsafe outcome `0`；
- 唯一科学分母缺口是 A-E partition 的 aligned arm：`7/8`。该 session 已接受科学操作并形成终态，必须保留，不能补跑成更有利结果。

因此，应同时保留两个口径：

1. **冻结原始口径**：总 summary 为 `failed`，旧 method gate 为 `19/27` 通过，另有 7 个 retained method findings 和 1 个不完整 cell。
2. **结果优先科学口径**：`26/27` cells 完整、`251/252` experiments 完整，所有终态 provider sessions 和 replay 完整；旧 token/call 上限不再被解释为科学失败。

原始状态不能被改写，但也不能让已经退役的资源门禁掩盖已获得的科学轨迹。

## 2. 原始 `failed` 状态究竟包含什么

总 summary 的 `failed` 不是“DeepSeek 矩阵没有结果”，而是三类事件的合并标签：

| 类别 | cells | 对科学分母的影响 | 解释 |
|---|---:|---|---|
| 真正未完成计划轮次 | 1 | 是 | A-E partition aligned 为 `7/8`；保留，不重跑 |
| 完成全部实验但超过旧 token/resource 记账上限 | 6 | 否 | provider 正常结束、完整推荐、exact replay 通过；旧上限只作为历史运行标签 |
| clean provider turn 与旧 process/session 完成判定不一致 | 1 | 否 | A-E electrochemical aligned 的 receipt 为 completed、return code 0、usage complete，但旧 gate 标为 `provider_session_completed=false` |

上表三类互斥，共对应严格旧口径下的 8 个非通过 cells：1 个不完整 cell，加 7 个 method findings。三次 participant physical-resource rejection 与其中的旧 token/resource findings 重叠，不另加 cell；它们仍保留为方法行为证据，因为物理资源约束不能取消，但没有阻止对应 cell 完成计划实验。

## 3. 九个 task triplets 的最终推荐结果

下表使用每个 arm 已提交 final recommendation 对应的 leaderboard score。不同任务和 locus 的 score 不是共同科学终点，因此只能在同一行三臂内比较；跨行平均仅作描述。

| Locus / task | 轮次 | Opaque | Aligned | Misindexed | 行内最高 | 主要观察 |
|---|---:|---:|---:|---:|---|---|
| A-E electrochemical | 8 | 0.3685 | **0.4335** | 0.4125 | aligned | 两种 prior 均优于 opaque；aligned 比 misindexed 高 0.0210 |
| A-E partition | 8 | 0.2058 | 0.4114† | **0.5793** | misindexed | prior 强烈改变搜索；aligned 仅完成 7/8，不能作完整时域比较 |
| A-E reaction safety | 8 | 0.1231 | **0.1496** | 0.0743 | aligned | 本矩阵中最清楚的 correct-vs-wrong 分离之一，差 0.0753 |
| A-E crystallization | 8 | **0.6013** | 0.5502 | 0.5930 | opaque | aligned 低于 opaque；misindexed 与 opaque 接近 |
| A-E distillation | 8 | 0.3481 | 0.4199 | **0.4565** | misindexed | 两种 prior 均提高 endpoint，misindexed 最高 |
| A-P electrochemical | 10 | 0.8304 | **0.9053** | 0.7977 | aligned | aligned 优势稳定；misindexed 低于 opaque |
| A-P reaction safety | 10 | 0.4124 | 0.4131 | **0.4208** | misindexed | 三臂在 0.0084 内，数值上接近收敛 |
| A-S partition | 12 | **0.6112** | 0.1973 | 0.2674 | opaque | supplied prior 两臂均出现大幅负效应；aligned−opaque 为 −0.4138 |
| A-S crystallization | 12 | **0.4462** | 0.4444 | 0.4413 | opaque | 三臂在 0.0049 内，基本收敛 |

† A-E partition aligned 的 final recommendation 存在，但来自 7 个而非计划的 8 个完整实验。

## 4. 聚合信号：没有“普遍更好的先验臂”

### 4.1 胜者和 paired contrasts

- 九块中 opaque、aligned、misindexed 各赢 `3` 块。
- Aligned 高于 opaque 的块数是 `6/9`，但 paired mean 为 `−0.0025`，median 为 `+0.0265`。A-S partition 的 `−0.4138` 足以反转均值。
- Misindexed 高于 opaque 的块数是 `4/9`，paired mean 为 `+0.0107`，median 为 `−0.0048`。
- Aligned 高于 misindexed 仅 `4/9`；paired mean 为 `−0.0131`，median 为 `−0.0078`。
- 留一块后的 paired mean 会跨过 0，说明任何全局平均方向都依赖少数任务，不能作为稳定主效应。
- A-E crystallization、A-P safety、A-S crystallization 的胜者 margin 均小于 `0.01`；它们是数值近似，不是预注册的 equivalence test。

结论是：**prior correctness 没有单调映射到 endpoint quality。** Correct prior 有时明显有利，有时中性，有时造成严重伤害；misindexed prior 也可能赢得单块任务。

### 4.2 搜索随轮次的改善

- 后半程 mean 高于前半程：`21/27` cells。
- 后半程发现了高于前半程的 best endpoint：`21/27` cells。
- Opaque、aligned、misindexed 的后半程 mean 改善分别为 `8/9`、`7/9`、`6/9`；后半程 best 改善分别为 `8/9`、`5/9`、`8/9`。
- 三臂 task-macro trajectory mean 分别为 `0.3434 / 0.3454 / 0.3348`，macro selected score 为 `0.4386 / 0.4361 / 0.4492`。这些宏平均不构成跨任务共同终点。
- 单 cell 内 score 的平均标准差为 opaque `0.0824`、aligned `0.0935`、misindexed `0.0979`。显式 prior，尤其 misindexed prior，与更高的搜索波动同时出现。

这说明 DeepSeek 不是只复述初始 prior；它在多数 cell 中继续从实验反馈学习。但“继续学习”不等于“正确识别 prior 是否可信”。

### 4.3 最终选择质量

- `25/27` 个 final recommendations 精确选择了该 cell 已观察到的最高分实验。
- A-P electrochemical aligned 只错过最高分 `0.0024`。
- A-E partition aligned 在不完整轨迹中选择 `0.4114`，而已观察 best 为 `0.4811`，regret 为 `0.0697`。

因此，主要短板不是一般性的“看见好结果却不会选”，而是 prior 如何塑造搜索覆盖，以及少数任务中的生命周期/方法失败。

## 5. 任务与 locus 的交互

重复出现的任务给出了比全局平均更有价值的模式，但 locus 与轮次同时变化，不能把差异单独归因为 horizon：

- **Electrochemical**：aligned−opaque 在 A-E 和 A-P 分别为 `+0.0650`、`+0.0748`，是最稳定的 aligned-prior utility 候选。misindexed−opaque 从 A-E 的 `+0.0440` 变为 A-P 的 `−0.0327`。
- **Reaction safety**：A-E 中 aligned 与 misindexed 相差 `+0.0753`；到 A-P 后三臂在 `0.0084` 内。这更像 task/locus/horizon interaction，而不是固定的 prior 主效应。
- **Partition**：A-E 中 supplied-prior 两臂都高于 opaque；A-S 中两臂都显著低于 opaque。A-S aligned 虽然显式降低了 prior reliability，仍未恢复 endpoint。
- **Crystallization**：A-E 中 opaque 略胜；A-S 中三臂几乎完全收敛。较长时域并没有在所有任务上放大 prior 效应。
- **Distillation**：当前只有 A-E 单块，misindexed 获得最高 endpoint，不能据此推断错误 prior 有益。

核心科学候选不是“scale 越大越能纠错”，而是：**prior 与任务几何、可辨识反馈和搜索时域发生强交互。**

## 6. 自报 belief 不能可靠区分正确与错误 prior

对有 nominal dossier 的 18 个 cells：

- Aligned reliability 平均从 `0.667` 升到 `0.763`：`6/9` 上升、`2/9` 不变、`1/9` 下降。
- Misindexed reliability 平均从 `0.619` 升到 `0.722`：`5/9` 上升、`3/9` 不变、`1/9` 下降。
- Final suspected-field warning 在 aligned 中出现 `4/9`，在 misindexed 中只出现 `3/9`。

这意味着 warning 的 false-positive 数量不低于 true-positive 数量，错误 prior 也常得到更高的最终自报可靠度。最明显的反例是 A-S partition：

- aligned 从 `0.70` 降到 `0.50` 并指出 `partition_coefficient_exponent`，但 selected score 只有 `0.1973`；
- misindexed 从 `0.50` 升到 `0.85`、没有 final misindex warning，selected score 只有 `0.2674`；
- opaque 达到 `0.6112`。

因此，conflict detection、confidence revision、prior rejection、搜索恢复和 endpoint recovery 必须作为不同变量测量，不能用一句“模型发现了错误先验”合并。

## 7. 科学失败与运行代价

### 7.1 物理/方法行为

- 动态物理失败共 `9` 次，全部集中在 partition：A-E aligned `3`、A-E misindexed `4`、A-S opaque `2`。
- Participant physical-resource rejection 共 `3` 次：A-P electrochemical opaque/misindexed 各 1 次，A-S partition misindexed 1 次。
- Unsafe outcome 为 `0`。
- `230` 个 unique recipes、`21` 个 exact repeats；多样性覆盖总体充足。

Partition 同时承载唯一不完整 cell、全部动态物理失败和最大的 prior endpoint 反转，是下一阶段最值得保留的 stress-test，而不是应被删掉的“异常任务”。

### 7.2 为什么这一阶段耗时很长

仅终态矩阵累计记录：

- input tokens `864.1M`，其中 uncached `13.37M`，约 `98.45%` 为 cache-hit input；
- output tokens `1.69M`；
- 27 个终态 session 的 provider elapsed 累加为 `22,072 s`，约 `6.13 h`；
- recovered agent-invalid tool failures 计数为 `172`；
- operation attempts 与累计 input tokens 的描述性相关为 `0.966`。

长耗时主要来自长工具轨迹、累计上下文和失败恢复，而不是 252 个模拟实验本身。

完整 attempt archive 还包含 `35` 个 triplet attempt directories、`31` 份 reports 和 `85` 份 provider/session receipts。基础设施恢复过程中有 `16` 份 zero-action reports 和 `212` 个 provider error events；A-S crystallization 的作废 attempts 额外完成了 `101` 个实验，约为最终保留分母的 `40.2%`，但这些结果因整块 restart 规则全部排除。最终有效科学分母只使用终态矩阵，不能把作废结果拼回去。

## 8. 与既有 DeepSeek 开发证据的独立对照

此前独立的五任务、五 world DeepSeek evaluator cohort 保留 `75/75` participant cells，其中 `69/75` runner-qualified；完成 `100/100` truth queries、`414/414` blind replays。其 task×seed 描述性 H3 mean 为 `−0.0421`，但 task-level 方向高度异质，blind recommendation gain 多为 0，且 misindex warnings 不具特异性。

两个 cohort 的任务合同、worlds、轮次和测量不同，不能合并分母或做 pooled test；但它们在定性上相互支持：

1. 显式 prior 会显著改变 DeepSeek 的搜索路径和 endpoint；
2. aligned prior 的收益是 task-specific，而不是普遍主效应；
3. misindexed prior 不会被稳定、选择性地拒绝；
4. 自报 reliability/warnings 不能替代 held-out predictive evaluation；
5. DeepSeek 能从反馈中适应，但 epistemic correction 与 optimization success 明显分离。

## 9. 对 Paper 2 的阶段性价值

### 可以作为正式实验设计依据的结论

- 将 prior 视为对 search policy 的干预，而不是天然的信息增益。
- 正式分析必须注册 `prior arm × task/locus` interaction，不能只报告跨任务平均。
- Endpoint、held-out prediction、law accuracy、warning specificity、reliability calibration、failure/completion 必须分开报告。
- Provider token/call/currency 只作描述性资源账本，不再作为科学拒绝门槛；物理资源和安全规则继续生效。
- Participant failure 必须留在分母中；平台修复后只能整块前瞻重跑，不能用结果更好的轨迹替换。
- Partition 应作为高信息量 stress-test 保留，electrochemical 可作为 aligned-prior utility 的重点确认任务，crystallization/safety 可检验 prior effect 是否随 locus/horizon 衰减或收敛。

### 当前仍不能声称

- 不能把本 cohort 写成 H1-H4 的正式检验；
- 不能声称 DeepSeek 已发现可迁移的化学规律；
- 不能声称 aligned prior 整体优于 opaque 或 misindexed；
- 不能声称模型能可靠识别、拒绝或修正错误 prior；
- 不能与 WellAU 做能力排名；
- 不能把不同任务的 leaderboard score 当作同一量纲进行显著性检验。

## 10. 阶段决策

DeepSeek 本阶段应标记为 **TERMINAL / DEVELOPMENT ANALYZED**：不再补跑旧失败，不再因 token、调用数或费用上限重做门禁，也不把作废 attempts 拼入科学分母。当前最有价值的候选主结论是：

> DeepSeek 能在闭环实验中持续适应，并且外部先验会实质改变搜索；但先验的正确性并不稳定转化为更好的 endpoint，模型的显式置信度和 misindex warnings 也不能可靠区分正确与错误信息。先验效用主要由任务/locus 结构调节，epistemic correction 与 optimization success 必须分开验证。

该结论是下一阶段正式设计的依据，不是当前 development cohort 的正式论文结论。
