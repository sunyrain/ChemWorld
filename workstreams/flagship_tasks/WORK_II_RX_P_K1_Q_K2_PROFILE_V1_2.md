# Work II RX-P K1–Q–K2 profile v1.2

状态：**五世界扩展后冻结**
冻结日期：2026-09-19
任务编号：W2-131-P

本版本替代 v1.1 作为新五世界执行的 RX-P profile；v1.1 保留为单世界设计历史。通用提示与封存规则继承 `WORK_II_CANONICAL_K1_Q_K2_PROTOCOL_V1_1.md`，完整执行边界继承 `WORK_II_RX_PS_FIVE_WORLD_DUAL_GOAL_PROTOCOL_V1_0.md`。

## 1. 范围与 prior

适用于 `RX-W01...RX-W05 × P × {Opaque,Aligned,MisIndexed} × {mechanism_discovery,safety_constrained_optimization}`，共 30 个独立 source sessions、360 个 source batches、90 个后测。

P-Opaque 的 `initial_world_model` 必须为 `null`，不得收到实例参考中心、容差、方向、窗口、方程或可行性提示。P-Aligned 与 P-MisIndexed 从匹配资格包中逐 world 读取同一 reference context、锚点、置信度与 schema，只允许温度方向主张相反。任何带 `approximate_reference_region` 的 opaque 记录只能作为历史 `ContextOnly`，不能进入本块。

## 2. 冻结 Q

共同固定配方：solvent `2`, `0.005 L`; reagent `0.003 mol`; catalyst `1`, `0.000525 mol`; stirring `400 rpm`。每条 thermal history 后按表决定是否 quench，再 `terminate → final_assay`。

| Q | thermal history `(K, s)` | quench | 设计角色 |
| --- | --- | --- | --- |
| Q01 | `(420,3300)` | no | 共同评测中心 |
| Q02 | `(420,3300)` | yes | 中心 quench 配对 |
| Q03 | `(390,3300)` | no | 温度轴低端 |
| Q04 | `(450,3300)` | no | 温度轴高端 |
| Q05 | `(420,1500)` | no | 时间轴短时 |
| Q06 | `(420,5100)` | no | 时间轴长时 |
| Q07 | `(390,1800) → (450,1800)` | no | 升温顺序 |
| Q08 | `(450,1800) → (390,1800)` | no | 反向顺序 |
| Q09 | `(440,1500)` | no | 高温短时 |
| Q10 | `(440,1500)` | yes | 迁移 quench 配对 |
| Q11 | `(370,5700)` | no | 低温长时外推 |
| Q12 | `(460,6300)` | no | 高温长时边界 |

完整机器动作由 `configs/benchmark/work_ii_rx_ps_five_world_dual_goal_v1.0.json` 与 runner 在来源前物化并哈希。Q 只在 K1 封存后公开，因此其中的 `420 K / 3300 s` 不构成 source prior。

## 3. 指标与参考

逐题预测 `yield`, `conversion`, `selectivity`, `byproduct_signal`, `safety_risk`, `score`，每项均给 point estimate 和 80% interval，逐题附英文 rationale。每个 `world × query` 在全部 K2 后生成 5 个独立 keyed-noise 参考重复；同 world 的六个 P sessions 共用参考样本。
