# S0 v1.2 错误先验与恢复实验预注册

状态：**冻结前最终设计；任何 v1.2 provider 调用尚未发生。**

## 研究问题

ChemWorld 的主问题不是模型能否口头复述材料知识，而是：答案隐藏时，模型如何选择下一次实验、如何利用结果更新行动，并能否给出经盲测验证的最终方法。

本实验把这个问题扩展为三臂固定世界对照：

1. `opaque`：只给匿名材料 ID，不给材料属性；
2. `nominal`：给正确的匿名材料属性；
3. `misindexed`：世界、预算、模型和观测均不变，只把一个材料字段的两行属性固定错配。

错误先验臂不是新的认知问答 benchmark，也不是动态世界实验。三个臂都保留 20 轮自主闭环 campaign、最终综合、预测诊断和独立盲测。

## 固定干预

| 任务 | 错配字段 | 固定换位 | 保持正确的材料字段 |
|---|---|---|---|
| 电化学 | `electrolyte_profile` | `E1 ↔ E3` | `solvent` |
| 结晶 | `catalyst` | `C1 ↔ C2` | `solvent` |

映射在所有 seed 中完全相同，不读取世界级残差，不按世界挑选，也不改真实 action ID 的运行时效果。公开 dossier 仍只显示“匿名材料 ID + nominal properties”，不会出现 `misindexed`、目标字段或置换表。

映射选择仅依据已经冻结的材料族资格报告：

- 电化学资格 cohort（seeds 100–114）中 E1 是 9/15 个世界的 winner，E3 为 0/15；
- 结晶标准化资格设计的 winner 包含 C1，而 C2 是唯一未进入 winner 集的催化剂。

这是一个有意施加强冲突的族级 stress test。v1.2 是在 v1.1 正确信息 campaign 完成后设计的顺序扩展，因此不得描述成最初三臂同时预注册，也不得推广为任意错误先验的总体效应。

## 不变量

- 同一任务三个臂使用 seeds 0–9；
- 固定世界与真实 outcome law 不变；
- observation-noise namespace 不变；
- 模型固定为 `gpt-5.6-sol`，reasoning effort 为 `medium`；
- Codex subscription HTTPS provider；
- 每世界 20 次自主实验、1 次最终综合；
- 每世界 12 个预测诊断物理实验、6 个盲测实验；
- 每世界共 21 次模型调用、38 个物理实验；
- 最终 primary endpoint 是盲测后的 final recommendation score 均值；
- 验证结果不返回给 agent。

## 主要性能检验

独立单位是世界，按 `task_id + world_seed` 配对。

主要 estimand：

`mean(misindexed blind score - nominal blind score)`

两个任务分别计算配对世界 bootstrap 97.5% 区间（Bonferroni family，100,000 次重采样，随机种子 20260729）：

- 上界小于 0：该任务达到“错误先验有害”判据；
- 下界大于 0：该任务达到“错误先验有益”判据；
- 否则：不确定。

`misindexed - opaque` 是错误先验相对无信息的净影响，属于预注册 secondary contrast。

## “模型恢复”的分解判据

恢复不能用“最终分数没有显著下降”来宣称。需要按顺序满足三个组件：

1. **干预生效**：错误先验臂前 5 轮对 misleading action 的采用率高于正确信息臂；
2. **行动修正**：比较前 5 轮与后 5 轮，错误先验臂对 misleading action 的撤离幅度显著大于正确信息臂的同期变化；
3. **性能恢复到 opaque**：`misindexed - opaque` 的家族校正单侧 97.5% 下界不低于 `-0.05`。

只有三项均满足，才能在对应任务上写“观察到错误先验后的闭环恢复”。若前两项满足而第三项不满足，只能写“行动发生修正，但没有证明性能恢复”。若未通过干预生效检查，则错误先验结果只能作为弱 manipulation 的描述性结果。

更强的“完全恢复到正确信息臂”要求 `misindexed - nominal` 的家族校正单侧 97.5% 下界不低于 `-0.05`，单独报告，不与恢复到 opaque 混同。

行动统计来自每轮公开历史中的
`plan.recipe_parameters[target_field]`。前窗为 rounds 1–5，后窗为 rounds 16–20。最终 recommendation 的材料 ID 频率仅作描述性辅助，不替代 20 轮轨迹。

## 允许与禁止的结论

允许：

- 在这两个固定旗舰任务和十个冻结世界上，报告正确属性、无属性和固定错配属性如何改变实验行动及盲测最终方法；
- 按冻结判据分别报告信息价值、错误先验代价和恢复组件。

禁止：

- 把三臂结果写成模型普遍具备或不具备科学纠错能力；
- 把失败归因为 provider 的因果效应；
- 把匿名材料属性写成真实材料预测；
- 把 S0 固定世界结果写成 S1 动态机制变化适应；
- 用预测 Brier 或口头解释替代盲测 primary endpoint。

机器可审计冻结：
`configs/benchmark/scientific_optimization_s0_v1.2_misindexed_information_freeze_manifest.json`
