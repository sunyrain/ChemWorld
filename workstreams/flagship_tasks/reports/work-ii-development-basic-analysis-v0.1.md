# Work II 现有三任务实验：基础分析与审计

日期：2026-08-10。性质：development 描述性分析，不是 formal、held-out 或 confirmatory 结果。

机器摘要：`workstreams/flagship_tasks/reports/work-ii-development-basic-analysis-v0.1.json`，
SHA-256 `c210d085424693885a2a085bd42e15cdcb1835893af09e1e467d9184114b6f3f`。

## 1. 今晚可以得出的结论

1. **正确先验的 endpoint 作用明显但依赖任务。** 在电化学与结晶中，aligned prior 相对 opaque
   的每个配对 seed 都提高了 campaign 内最佳分数；平均差分别为 `+0.2108`（5/5 seeds）和
   `+0.0570`（5/5）。蒸馏中没有复现：仅有四个完整配对 seed，平均差为 `-0.0364`，正负各 2。
2. **错误先验并不等于 endpoint 失败。** misindexed prior 相对 opaque 的最佳分数差在电化学为
   `+0.0471`，结晶为 `-0.0055`，蒸馏为 `+0.0232`。因此 endpoint 本身不能证明 agent 使用了
   正确规律，也不能证明错误先验已经被排除。
3. **自报的 prior rejection 方向有信号，但鉴别能力不足。** misindexed 臂的平均可靠度从
   pre-evidence 到 final 在三个任务中均下降（`-0.072`、`-0.058`、`-0.090`），但 aligned
   结晶臂下降得更大（`-0.188`），且最终有 4/5 aligned cells 错误怀疑 dossier 被错配，而
   misindexed 结晶仅 2/5 报警。不能把 reliability 下降或 `suspected_misindexed_fields` 直接当作
   成功排除错误先验。
4. **已有 law summary 只能证明结构化总结能力，不能证明规律正确。** 44 个完成的 WellAU cells
   均有 final typed law summary；各臂平均自信度约为 0.718--0.832，但尚未执行 evaluator-truth
   prediction-error 和 blind recommendation replay。高自信度目前没有 accuracy 含义。
5. **当前最强的论文信号不是“agent 已经发现规律”，而是三者发生了分离：** prior 会改变实验路径，
   endpoint 可在错误先验下改善，而显式 prior rejection 又可能误报。这个分离正好支持第二篇的
   核心问题，但需要 held-out truth 才能升级为规律发现结论。

## 2. 分母与完整性审计

| Provider block | Scheduled/expected cells | Terminal records | Completed/qualified | Complete experiments | Operation attempts | Committed | Ledger validation failures | MCP tool failures | Provider error events | Resource rejections | Exact replay |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| WellAU fallback | 45 | 45 | 44 | 176 / 180 | 1,547 | 1,524 | 23 | 91 | 39 | 0 | 44 / 45 |
| DeepSeek attempted blocks | 33 | 21 | 18 | 78 / 132 | 620 | 617 | 2 | 14 | 1 | 1 | 21 / 21 started |

这里必须区分三个口径：

- `MCP tool failure` 是在领域工具边界被拒绝的调用，包括 snapshot/step schema 错误；它可能还未进入
  scientific operation ledger。
- `ledger validation failure` 是 operation attempt 与 committed/rejected 账本之间的差额，不等于全部
  MCP 错误。
- `resource rejection` 是 agent 提议超出公开资源卡的操作，属于 participant 行为；它不改变物理状态，
  但必须进入尝试分母。

WellAU 的唯一 terminal failure 是 distillation / seed 4 / aligned：provider turn 完成但没有调用 MCP，
因此没有物理 operation、experiment 或 checkpoint。它按冻结规则保留。WellAU 共记录 59,414,461
input tokens，其中 52,824,576 为 cache hit，cache ratio 为 88.9%；高 cache 不是重复输出。

DeepSeek 的两次中途终止都发生在第二个、且与第一个失败之间已有成功调用的 MCP schema failure；
并非连续失控重试。electrochemical 的失败 cell 已完成 4/4 experiments 和 exact replay，只因一次公开
resource rejection 未通过原来的 `no_resource_rejection` 资格门。DeepSeek 的 21 个 started cells 均可
exact replay，记录到 1 个 provider error event；两个被强制中断的 cell 没有 `turn.completed`，其 token
字段是 unavailable，而不是零消耗。

## 3. Endpoint 描述结果

表中为每个 arm 跨 world seed 的 campaign 内最佳分数均值；括号内是相对 opaque 的配对差和正向
seed 数。蒸馏 aligned 只有 4 个完成配对，其他均为 5。

| Task | Opaque | Aligned nominal | Misindexed nominal |
|---|---:|---:|---:|
| Electrochemical conversion | 0.4112 | 0.6220 (`+0.2108`, 5/5) | 0.4583 (`+0.0471`, 4/5，1 tie) |
| Reaction-to-crystallization | 0.4398 | 0.4968 (`+0.0570`, 5/5) | 0.4343 (`-0.0055`, 3/5) |
| Reaction-to-distillation | 0.2823 | 0.2590 (`-0.0364`, 2/4) | 0.3056 (`+0.0232`, 3/5) |

平均 experiment-score 轨迹进一步说明 endpoint 与发现过程不能混为一谈：

| Task / arm | Exp 1 | Exp 2 | Exp 3 | Exp 4 |
|---|---:|---:|---:|---:|
| Electrochemical / opaque | 0.3683 | 0.2957 | 0.2676 | 0.2829 |
| Electrochemical / aligned | 0.4268 | 0.3752 | 0.4936 | 0.6117 |
| Electrochemical / misindexed | 0.4083 | 0.3411 | 0.3741 | 0.3253 |
| Crystallization / opaque | 0.4074 | 0.3999 | 0.3550 | 0.3277 |
| Crystallization / aligned | 0.4633 | 0.4201 | 0.4621 | 0.4655 |
| Crystallization / misindexed | 0.3499 | 0.3485 | 0.3727 | 0.4177 |
| Distillation / opaque | 0.1276 | 0.2726 | 0.2573 | 0.2533 |
| Distillation / aligned | 0.1814 | 0.2276 | 0.2338 | 0.2554 |
| Distillation / misindexed | 0.1160 | 0.2474 | 0.2570 | 0.3047 |

aligned electrochemical 显示了最清晰的持续增益；misindexed electrochemical 的 final score 反而低于
首轮，即使其 campaign best 仍略高于 opaque。结晶 misindexed 和蒸馏三臂则表现为后期修复或普通优化。
这些形态值得后续用 evaluator prediction error 区分“证据驱动修正”和“只找到更好的局部 recipe”。

## 4. Prior rejection 与自我校准审计

| Task | Aligned reliability change | Misindexed reliability change | Aligned 最终误报 misindex | Misindexed 最终报警 |
|---|---:|---:|---:|---:|
| Electrochemical conversion | +0.040 | -0.072 | 1 / 5 | 2 / 5 |
| Reaction-to-crystallization | -0.188 | -0.058 | 4 / 5 | 2 / 5 |
| Reaction-to-distillation | +0.042 | -0.090 | 3 / 4 | 4 / 5 |

这组结果不支持“agent 已可靠识别错误先验”。较准确的表述是：misindexed 条件在平均意义上诱发了降权，
但显式诊断存在显著 false positive，且任务异质性很强。尤其是结晶，aligned 臂对 prior 的降权与误报
均比 misindexed 更严重；这可能来自 nominal dossier 与四次有限实验之间的表面冲突、探索不足，或模型
把一般模型失配错误归因于索引错位。held-out truth 与 evidence-reference 对齐审计是下一步必要条件。

## 5. 探索与资源侧观察

- 以四轮实验中的不同材料组合数衡量，opaque 在 electrochemical 与 crystallization 中平均探索
  3.8 和 4.0 个组合；aligned 为 3.2 和 3.2，misindexed 为 3.4 和 3.0。正确先验看起来促进了早期
  exploitation，但这只是材料组合多样性，不是完整 information gain。
- crystallization aligned 平均 uncached input 为约 241k/cell，高于 opaque 的 160k 和 misindexed 的
  134k；其 endpoint 较高，但不能将额外模型计算当作先验本身的纯效应。
- WellAU 的 44 个完成 cells 经历了 91 次可恢复 MCP tool failures 和 39 个 provider error events，仍然
  完成全部物理轨迹。由此可见，把任意第二次 schema failure 或任意第一次 provider error 设为整个
  campaign 的 fatal gate，会把工具可靠性噪声放大为大量科学样本损失。

## 6. 今晚审计后的 claim 边界

现有证据可以支持：

- prior condition 会改变实验路径与 endpoint；
- aligned prior 的收益具有任务异质性；
- misindexed prior 下仍可能达到较好 endpoint；
- 自报 prior rejection 与实际 prior condition 并不稳定对应；
- 当前 harness 的 fatal gate 过严，会将可恢复结构错误升级为 cell failure。

现有证据不能支持：

- agent 已发现或准确总结 hidden law；
- agent 已可靠排除错误先验；
- law summary 可迁移到 held-out conditions；
- DeepSeek 与 WellAU 的科学能力优劣比较；
- 把 operations、experiments、checkpoints 或 provider retries 当成独立样本。

## 7. 下一轮事前 amendment 的数据依据

在已观察 DeepSeek cells 中，每 cell 最多有 2 次 MCP failure，且最大连续失败数为 1；所有多次失败之间
都有成功工具调用。因此下一轮 development contract 拟冻结为：

- 每 cell 最多 3 次 recovered MCP tool failures；
- 最多 1 次连续 MCP failure，成功调用后连续计数归零；
- 每 cell 最多 1 次 recovered provider error event；
- 最多 1 次 resource rejection 可保留并继续，作为负向 participant behavior；
- resource、operation、stock、process-time、repeat 和 safety 物理边界不放宽；
- host 仍不补写 `decision_audit`、belief snapshot 或 action，不自动修复科学决策；
- 所有新结果进入新的 run root，旧失败与旧矩阵不被替换。

这些值必须在真实 provider pilot 前写入实验 note、配置和 readiness receipt；pilot 失败则停止扩展，不在
运行结果出现后再次调阈值。
