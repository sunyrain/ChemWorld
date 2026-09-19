# Work II RX-P/S 五世界双目标执行协议 v1.0

状态：**已冻结，待启动门通过后执行**
冻结日期：2026-09-19
任务编号：W2-131

后续状态：首次provider-free gate发现继承challenge helper的accumulation符号与RX-S v1.1资格定义相反；本版本及失败目录保留，新的执行入口由[协议v1.0.1](WORK_II_RX_PS_FIVE_WORLD_DUAL_GOAL_PROTOCOL_V1_0_1.md)替代。纠正发生时provider calls为0。

本块继承 [通用 K1–Q–K2 协议 v1.1](WORK_II_CANONICAL_K1_Q_K2_PROTOCOL_V1_1.md)，使用 [RX-P profile v1.2](WORK_II_RX_P_K1_Q_K2_PROFILE_V1_2.md) 与 [RX-S profile v1.0](WORK_II_RX_S_K1_Q_K2_PROFILE_V1_0.md)。机器可读的唯一运行配置是 `configs/benchmark/work_ii_rx_ps_five_world_dual_goal_v1.0.json`。

## 1. 冻结研究单位

一个 source session 对应且只对应一个 `world × locus × arm × goal` cell，每个 cell 只跑一次独立持久会话：

```text
2 loci × 5 worlds × 3 arms × 2 goals = 60 source sessions
60 sessions × 12 complete batches = 720 source batches
60 sessions × (K1 + Q + K2) = 180 posttests
```

- Worlds：`RX-W01...RX-W05`，seeds `0...4`；
- loci：`P`（局部温度—时间响应）与 `S`（结构机理：有效不可逆目标通道 vs 可逆目标通道）；
- arms：`Opaque`、`Aligned`、`MisIndexed`；
- goals：`mechanism_discovery`、`safety_constrained_optimization`；
- provider：Codex cached-login API，`gpt-5.6-sol`，`medium` reasoning；
- 物理真值：两个 locus 的 participant source 都使用 RX 默认 `deactivating_baseline` 世界。`reversible_target_pathway` 只用于 S 的 evaluator-only 可证伪性启动门，不进入 participant 可见材料。

60 个会话相互独立，不共享 thread、实验记录、机理报告、预测或推荐。比较中的配对来自冻结设计，不来自跨会话传递信息。

## 2. 严格信息边界

三臂按被干预的 locus 定义。`Opaque(L)` 允许公共操作、合法范围、仪器、评分、安全合同和 L 以外的公共信息，但不得提供任何从目标 world、资格结果或历史标定得到的 L 层实例知识。

- P-Opaque：`initial_world_model = null`；不得出现 `420 K / 3300 s`、容差、方向、局部窗口、方程或最优暗示。
- P-Aligned/MisIndexed：使用相同参考 context、锚点、置信度与 schema，只改变温度方向主张。
- S-Opaque：`initial_world_model = null`；不得出现不可逆/可逆 target-pathway 主张。
- S-Aligned/MisIndexed：相同 schema 与 `moderate` confidence；Aligned 为“公开支持域内目标通道可能有效不可逆”，MisIndexed 为“可能存在显著逆通道”。

P-Opaque 与 S-Opaque 的 source 可见 prior payload 相同，但仍各自独立运行，因为后续 Q 不同。两者不是 locus 处理效应对照，禁止把它们之间的差异解释成 P vs S 因果效应。

## 3. 来源资源和交付

每个 session 必须完成 12 个独立 batch，最多 12 次非终检测量及 12 次 final assay，360 次操作尝试。物料上限为 reagent `0.48 mol`、solvent `0.96 L`、catalyst `0.06 mol`。过程时间上限为 `216000 s`，使 12 个 `14400 s` 长时条件及 quench/合理分段仍可合法完成；该上限对所有 P/S/arm/goal 一致。

每批必须显式 `terminate` 后做 `final_assay`。来源结束后，从已完成批次中封存一个推荐操作；探索任务的推荐只是次要读出。来源最终摘要和推荐理由必须为英文。

## 4. 后测与真值时序

每个来源严格按 `source → K1 → Q → K2` 在同一 thread 续接。K1、Q、K2 逐字使用通用 v1.1，所有报告及 rationale 用英文；后测只开放无外部数据的公共数值计算器，单阶段上限 128 次，不开放实验室、网络、仓库或隐藏真值。

任何 participant session 的 K2 封存前不得生成或读取该块参考真值。所有 60 个 K2 结束后，评价器为每个 `world × locus × query` 生成 5 个独立 keyed-noise 重复：`2 × 5 × 12 × 5 = 600` 次 provider-free 参考执行。相同 `world × locus` 的六个来源共享同一参考样本；这不增加 participant 样本量。

每指标点预测按 5 次参考的均值计算 MAE；80% 区间对 5 次观测逐个计算 empirical coverage、mean width 与 interval score。推荐复测也只能在 K2 后运行，并与盲预测真值分开保存。

## 5. RX-S 启动门

现有 S development qualification 的科学门为 5/5 worlds 通过，但历史 challenge receipt 每个条件只有一个噪声坐标。为避免带着已知证据缺口启动 provider，本块在首个 source 前执行 write-once provider-free gate：

- 每个 world 固定三个条件：`410 K`、catalyst `0.000120 mol`，duration 分别 `1800/7200/14400 s`；
- baseline 与 `reversible_target_pathway` 使用完全相同动作；
- 每个 action × family 做 3 个独立 keyed-noise 重复，共 `5 × 3 × 2 × 3 = 90` 次；
- 每次必须完成、HPLC 三项 direct metrics 可见、零非预期 rollback、exact replay；
- 使用 challenge v1.2 的冻结计算：`minimum_accumulation = 0.03`、`minimum_information_gain = 0.03`、最少 3 个唯一 target noise identities、可靠停止必须落在 participant budget `2...4`；
- 五个 world 全部通过才放行 60 个 provider source；失败则保留 gate 结果并停止，不允许在同一块看结果改条件。

## 6. 失败、续跑和可审计性

结果目录 write-once；已存在 cell 只读取，不覆盖。科学失败、合法 partial、预测格式失败分别保留并按冻结 denominator 报告。共同的 pre-action 鉴权/启动失败会停止尚未开始的 provider block；单个科学失败不改变后续 cell 的题目、资源或顺序。

每个 cell 保存 source prompt/stdout/stderr、trajectory、exact replay、provider receipts、workspace、K1/Q/K2 原文和解析结果、资源使用及推荐。顶层保存 `design.json`、启动门、共享参考真值、逐 cell 评价和增量 `summary.json`。任何 repair 必须续接原 thread、使用相同提示、不给真值且不新增物理实验。

## 7. 推断边界

实验单位是 source session；12 batches 是同一 agent 的序列决策，不能当作 12 个独立 agent。world 是预注册异质性维度，arm 和 goal 是会话级处理。报告 arm/goal 差异时必须先按 world 配对并展示逐 world 结果；不可把 720 batches 当成 720 个独立 treatment replicates。
