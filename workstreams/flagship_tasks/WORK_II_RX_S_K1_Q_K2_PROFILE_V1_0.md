# Work II RX-S K1–Q–K2 profile v1.0

状态：**冻结，受五世界噪声启动门约束**
冻结日期：2026-09-19
任务编号：W2-131-S

通用提示与封存规则继承 `WORK_II_CANONICAL_K1_Q_K2_PROTOCOL_V1_1.md`，完整执行边界继承 `WORK_II_RX_PS_FIVE_WORLD_DUAL_GOAL_PROTOCOL_V1_0.md`。

## 1. 科学问题与 prior

适用于 `RX-W01...RX-W05 × S × {Opaque,Aligned,MisIndexed} × {mechanism_discovery,safety_constrained_optimization}`，共 30 个独立 source sessions、360 个 source batches、90 个后测。

S 层检验目标通道在公共支持域内是否可近似视为有效不可逆，及可逆通道这一竞争结构能否被温度、暴露时长与催化剂剂量的联合作用区分。participant 的真实物理世界保持资格合同声明的 parent `deactivating_baseline`：

- Opaque：`initial_world_model = null`；
- Aligned：`confidence=moderate`，主张目标通道在公共支持域内可能有效不可逆；
- MisIndexed：相同 schema/confidence，主张目标通道可能存在显著逆通道。

可逆 child 只用于来源前的 evaluator-only falsifiability gate，绝不进入 source task contract、material information 或观测。

## 2. 冻结 Q

共同固定配方：solvent `2`, `0.005 L`; reagent `0.003 mol`; catalyst `1`; stirring `400 rpm`。每条 heat 后按表决定是否 quench，再 `terminate → final_assay`。

| Q | T (K) | duration (s) | catalyst (mol) | quench | 设计角色 |
| --- | ---: | ---: | ---: | --- | --- |
| Q01 | 410 | 1800 | 0.000120 | no | 中温短时低剂量 |
| Q02 | 410 | 14400 | 0.000120 | no | 同温同剂量长时积累 |
| Q03 | 410 | 1800 | 0.000520 | no | 中温短时高剂量 |
| Q04 | 410 | 14400 | 0.000520 | no | 时长×剂量交互 |
| Q05 | 350 | 7200 | 0.000120 | no | 低温中时低剂量 |
| Q06 | 465 | 7200 | 0.000120 | no | 温度配对高端 |
| Q07 | 350 | 7200 | 0.000520 | no | 低温高剂量 |
| Q08 | 465 | 7200 | 0.000520 | no | 温度×剂量交互 |
| Q09 | 410 | 7200 | 0.000315 | no | 网格中心 |
| Q10 | 410 | 7200 | 0.000315 | yes | 中心 quench 配对 |
| Q11 | 350 | 14400 | 0.000315 | no | 低温长时边界 |
| Q12 | 465 | 1800 | 0.000315 | no | 高温短时边界 |

这 12 题在来源前冻结，不根据 agent 的实验或 K1 换题。它们覆盖 duration accumulation、temperature×dose、quench 与边界迁移；Q 的设计角色不发给 agent。

## 3. 指标、参考与启动条件

逐题预测 `yield`, `conversion`, `selectivity`, `byproduct_signal`, `safety_risk`, `score`，每项给 point estimate 和 80% interval，逐题附英文 rationale。每个 `world × query` 在全部 K2 后生成 5 个独立 keyed-noise 参考重复；同 world 的六个 S sessions 共用参考样本。

来源启动前，必须按 master protocol 对五个 worlds 完成 90 次 provider-free repeated-noise gate，并且五个 world 全部满足 challenge v1.2 的三噪声坐标、accumulation、information-gain 与 budget-window 条件。该 gate 只决定整块是否可启动，不用于改变 Q、prior 或资源。
