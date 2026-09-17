# Experiment 1 RX-E repair authoring note v1.0.2

状态：**AUTHORING DESIGN FROZEN BEFORE CALIBRATION EXECUTION**

## Question

v1.0.1 固定 `C1 ↔ C2`，RX-W02 在 Q5/Q7、RX-W03 在 Q7 失败。需要判断问题是该 pair
偶然落在弱响应区，还是 entity prior 本身不适合 RX。不得按正式 W01–W05 的单个结果逐 World
挑选最容易的 pair。

## Calibration design

- 使用不进入 benchmark denominator 的 `public-test` calibration seeds `101..105`；
- 对每个 seed 执行当前合法公共合同下 2 nuisance anchors × 4 catalysts × 3 replicates；
- 记录 yield/selectivity/conversion/byproduct_signal、exact replay、noise coordinate 和 truth binding；
- 对全部六个 catalyst transpositions 使用相同 receipts 做 outcome-complete 比较；
- 候选必须在五个 calibration Worlds 中使用同一个 transposition；不得 world-specific cherry-pick；
- 选择规则按顺序为：五 World robust pass count、最小 anchor separation、最小 SNR、最后按 pair
  lexicographic order 打破平局；
- 阈值保持 v1.0.1：mean 0.05、single metric 0.03、SNR 2、behavior consequence 0.05；
- calibration evidence 不进入正式 qualification denominator。

若没有一个全局 pair 在 calibration Worlds 中科学合格，则 RX-E 不进入 v1.0.2 requalification，
而升级为 entity-question redesign；不得调低阈值。
