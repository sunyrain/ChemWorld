# Work II Study B：matched evidence 结果与机制分析

## 结论先行

Study B 完成了 30/30 fresh sessions、10/10 task-world clusters，0 失败、0 participant 物理实验。结果支持一个分 locus 的机制结论，而不是统一的 seeking/updating 二分答案：

1. **A-P electrochemical 支持 evidence-seeking bottleneck。** 固定反证到达后，错误方向先验在 5/5 worlds 都被公开文字明确否定，模型恢复了约 1.1 V 最优、1.3 V 以上性能坍塌的响应；三 arm 的 post-error 收敛到几乎相同水平。
2. **A-S partition 尚不能定位 belief-updating failure。** misindexed sessions 没有恢复注册的 1.75 power law，但输入证据全部来自同一个 identity/process 条件，模型也明确指出缺少 phase-process 干预。这个 packet 足以校准 endpoint，却不足以唯一反驳 linear/distribution law。
3. 因此当前 Study B 是 **部分机制闭环**：A-P 闭环；A-S 暴露了 evidence level 与 law level 的错配。不能把 A-S 的负 primary contrast 直接写成‘模型看见充分反证仍拒绝更新’。

## 1. 完整性与执行

- 正式 sessions：30/30；clusters：10/10；失败 0。
- 两轮同 thread：30/30；provider turns：60/60；全部一次完成，无 infrastructure predecessor。
- participant 物理实验：0；正式 wall time：40.2 min；中位 cell wall time：245.0 s。
- 60 个 turns 中出现 2 个工具事件，分布于 2 个 pre turns；隔离 workspace、禁用 web/apps/plugins，无 evaluator truth 或仓库数据访问路径，且不影响两轮分母。

## 2. 注册主指标

主指标保持冻结定义：`(misindexed pre − post) − (aligned pre − post)`；正值表示在相同证据下，misindexed 比 aligned 获得更多纠错增益。统计单位是 world，单 locus 只有 n=5，因此 exact sign-flip 只作小样本方向校验。

| Locus | opaque gain | aligned gain | misindexed gain | primary contrast | positive worlds | exact one-sided p | 95% descriptive CI |
|---|---:|---:|---:|---:|---:|---:|---:|
| A-P | 0.2221 | 0.2018 | 0.2327 | 0.0309 | 3/5 | 0.125 | [-0.0316, 0.0935] |
| A-S | 0.2164 | 0.2339 | 0.1820 | -0.0519 | 1/5 | 0.938 | [-0.1239, 0.0202] |

A-P 的主对比为正但 n=5 下未达到常规显著阈值；证据强度主要来自 5/5 明确文字纠错与三臂 post-error 收敛，而不是 p 值。A-S 的主对比为负，但其 misindexed pre-error 本来更低，gain 受可改善空间影响，不能单独视为结构更新失败。

## 3. A-P：固定反证使错误参数方向可纠正

| Arm | pre error | post error | absolute gain | relative reduction |
|---|---:|---:|---:|---:|
| opaque | 0.3037 | 0.0816 | 0.2221 | 73.1% |
| aligned_nominal | 0.2822 | 0.0804 | 0.2018 | 71.0% |
| misindexed_nominal | 0.3105 | 0.0778 | 0.2327 | 74.6% |

misindexed − aligned 的 post-error 均值差为 -0.0026；misindexed − opaque 为 -0.0038。三臂最终误差差异不到 0.004，说明反证到达后初始 prior 的方向影响基本被消除。

公开 summary 审计显示：5/5 misindexed worlds 明确否定 supplied direction，5/5 恢复 peak-and-collapse 响应。该结果与 Study A 的 A-P suggestive、但未过 selective-correction gate 结合，支持自由探索中的主要损失至少部分发生在反证获取，而不是反证到达后的参数更新。

## 4. A-S：endpoint 校准不等于结构规律纠正

| Arm | pre error | post error | absolute gain | relative reduction |
|---|---:|---:|---:|---:|
| opaque | 0.2623 | 0.0459 | 0.2164 | 83.0% |
| aligned_nominal | 0.2794 | 0.0455 | 0.2339 | 85.2% |
| misindexed_nominal | 0.2135 | 0.0314 | 0.1820 | 85.9% |

三个 A-S arms 的相对误差下降都约 83–86%，说明 packet 能强力校准 endpoint。但这一数值不能证明 power law 被恢复：24 个评分项中，16 个是接近常数的 `phase_ratio` 和 `product_in_aqueous`；真正承载结构变化的 `product_in_organic` 只有 8 项。

在 `product_in_organic` 上，aligned gain 为 0.1242，misindexed gain 为 0.0444，主对比 -0.0798，仅 1/5 worlds 为正。可是 misindexed 的 pre-error 也明显更低，因此该 gain gap 仍不能单独识别 stubborn updating。

公开 summary 中，misindexed arm 恢复注册 1.75 partition power law 为 0/5；继续使用 linear/distribution coefficient 类模型为 4/5；明确识别固定 process 证据局限为 4/5。这说明模型做了数值更新，却没有完成结构更新；同时 packet 本身也没有提供足够的 phase-process 对照去唯一要求结构更新。

## 5. 对 Paper 2 故事的影响

Study B 把能力链进一步拆开：

- **参数规律层**：错误方向可以被高信息量反证覆盖；自由探索表现不佳包含 evidence-seeking loss。
- **结构规律层**：相同数量的 endpoint evidence 可以显著降低 prediction error，却仍无法保证机制 family recovery。问题不只是‘模型是否愿意更新’，还包括 evidence 是否与 law 的可识别层级匹配。
- 因此论文不应把 matched evidence 简化成一个 yes/no treatment；更强的表述是 **correction requires intervention-complete evidence at the same abstraction level as the law**。

## 6. 当前证据边界

- Study B 的 A-P 子结论已经闭环。
- Study B 的 A-S 子结论是设计诊断，不足以完成 acquisition-vs-updating 的结构 locus 因果定位。
- 若要完成 A-S 定位，后续独立 B2 应给出能直接分离 linear 与 1.75-power law 的 phase-process 成对干预，并用另一组不重叠 phase-process queries 评分；不能事后改写本次 30-cell block。
- 当前结果不需要补跑或删除；它作为‘endpoint adaptation 与 structural correction 分离’的证据永久保留。
