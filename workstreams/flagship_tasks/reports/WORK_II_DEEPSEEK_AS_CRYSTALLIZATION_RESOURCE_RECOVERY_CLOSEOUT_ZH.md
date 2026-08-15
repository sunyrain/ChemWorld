# Work II DeepSeek A-S crystallization 资源修正批次收束

更新日期：2026-08-15

## 阶段结论

本批次已经终态，可以收尾，不再原地补跑。15/15 个 session 均有可归因终态，完成 179/180 个计划实验；12/15 通过严格 qualification，14/15 实际完成全部 12 个实验。全部轨迹可 exact replay，provider error、基础设施缺失、动态物理失败和 unsafe outcome 均为 0。

资源修正有效：相对上一版 recovery 批次，严格通过数由 5/15 提高到 12/15，完整实验由 173/180 提高到 179/180，硬资源拒绝由 12 次降到 2 次。剩余两次拒绝集中在同一个 aligned session，分别是催化剂和晶种库存耗尽；没有新的加热、冷却或受保护收尾时间拒绝。这支持当前设计选择：提高热/冷操作能力，但不机械地把所有物料翻倍。

本批次不支持“aligned prior 在每个世界都优于其他 prior”的强结论。五个配对世界的平均最佳分数为：aligned 0.4423、opaque 0.3972、misindexed 0.3870；aligned 相对 opaque 平均 +0.0451，相对 misindexed 平均 +0.0554，但两个比较都只有 3/5 个世界同方向。更稳妥的表述是：aligned prior 提高了本任务的平均搜索前沿，但效果具有明显世界异质性，尚不能宣称稳定的机制恢复优势。

## 完成情况

| 指标 | 旧 physical-recovery v0.1 | 新 resource-recovery v0.2 |
|---|---:|---:|
| Terminal sessions | 15/15 | 15/15 |
| 严格 qualification | 5/15 | 12/15 |
| 完整实验 | 173/180 | 179/180 |
| Unique recipes | 164 | 175 |
| 硬资源拒绝 | 12 | 2 |
| Discarded batches | 7 | 10 |
| Provider errors | 1 | 0 |
| Dynamic physical failures | 0 | 0 |

新批次的 10 次 discard 中，7 次来自模型对结晶操作顺序的探索和纠错，3 次来自同一 session 在晶种耗尽后的行政性 closeout。Discard 增加不代表物理模型恶化：开放的正式物理路径允许模型犯错、观察失败并重启 batch；该指标应与资源规划、最终完成率和后续纠错联合解释。

## 三个严格未通过 session 的归因

1. seed 620418208 / aligned：实际完成 11/12，发生 4 次 discard 和 2 次库存拒绝。它是真正的 participant/resource incomplete，应按原样保留，不能补跑。
2. seed 620418208 / misindexed：实际完成 12/12，模型选择生命周期 batch 13，并且 host 的 `commit_final_recommendation` 已成功提交。旧分析器却把 13 当成“完成实验连续序号”，找不到第 13 条 completed row，因而把 `final_recommendation_committed` 错判为失败。这是结果分析的索引命名空间缺陷，不是 host 拒绝，也不是科学轨迹失败。
3. seed 918459813 / opaque：实际完成 12/12，并正确选择最高分 batch；唯一严格失败来自 campaign terminal 前的一次过早 final-recommendation 调用被归入 unclassified operational failure，之后模型已正常完成实验和推荐。这是 participant closeout sequencing，不是物理失败。

## 推荐索引缺陷

发生 discard 后，模型看到的是 batch 生命周期编号，而汇总器把 completed experiments 重新从 1 连续编号。由此会出现三种错误：

- 正确选择被映射到另一条 completed experiment，产生虚假的 recommendation regret；
- 已成功提交的 participant-visible batch 13 在旧分析层被误判为无效；
- 模型在资源状态中把“当前 batch 编号”误当成“已完成实验数”，可能过早判断目标已经达到。

按原始 trajectory 中的生命周期编号重新对齐后，15/15 个 session 的最终推荐身份都有效，15/15 都指向各自 participant-visible 历史中的最高分实验，真实 observed-score regret 均为 0；host 事实上也在 15/15 个 session 中完成了推荐提交。没有 session 被旧的“上限 12”在 host 层阻断。这个结果只说明模型能够从公开 leaderboard 中选出已观察到的最佳候选，不等同于 blind replay 或机制恢复成功。

该缺陷不要求重跑 provider：原始轨迹保留了足够的 batch 身份，可以在分析层修正。修正后的逐 session 结果保存在 `work-ii-deepseek-as-crystallization-resource-recovery-identity-corrected-v0.1.json`，重分析代码保存在 `scripts/reanalyze_work_ii_campaign_identity.py`。平台新结果同时保存 `batch_id`、`lifecycle_experiment_index` 和 `completed_ordinal`；推荐校验以实际 completed lifecycle 列表为准，不再用“完成数”充当 batch 编号上限。

需要保留一个边界：发生 discard 的 4 个 session 中，旧版 checkpoint 触发时机曾把 closed batch count 当作 completed experiment count。终点推荐和分数可以从原始轨迹可靠重建，但这些 session 的 belief checkpoint 时机不能事后改写，因此仍按 participant-affected 历史结果报告。

## 尚存的平台/交互问题

本批次共有 424 次失败的 MCP 工具尝试，其中 421 次是 belief snapshot schema 校验失败，3 次是 campaign terminal 前过早提交最终推荐。最主要的单项是 209 次 `law_summary contains an unknown feature ID`。这些失败没有造成物理状态伪造，也没有形成 provider error，但显著增加了交互、上下文和时间成本。

本轮平台修复已经完成：

1. batch/recommendation 使用稳定身份语义，并区分 closed、completed 与 lifecycle index；
2. 新增只读 `belief_snapshot_status`，直接返回当前阶段、下一步、精确字段类型和允许的 feature/metric/prior/evidence ID；
3. 相同 header 的 `begin_belief_snapshot` 重提改为幂等，字段错误返回可操作的局部修复信息；科学校验本身没有放宽；
4. 保留资源卡，不为了追求 15/15 人为消除 participant 的库存规划失败；
5. 暂不改变当前 12-experiment 设计，Anytime-12 作为未来独立协议候选另行讨论。

## 收尾口径

当前批次作为 development evidence 终态保存：不补齐唯一缺失实验，不覆盖三个历史严格未通过结果，也不因索引缺陷重跑 provider。论文层可以使用 179/180 的完整轨迹、资源修正前后对比和按稳定生命周期编号重建的推荐结果，但必须同时报告 1 个真实 incomplete、1 个 historical-analyzer namespace defect、2 个含 premature-closeout operational 记录的 session，以及 4 个 checkpoint timing 受旧计数语义影响的 session。

下一阶段先运行既定 task-aware evaluator、机制/预测恢复评分与删失/资源敏感性分析，再决定是否需要跨模型 replication。A-E private、WellAU 和新的 provider 实验继续保持未启动。
