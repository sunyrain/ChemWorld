# Experiment 1 C qualification specification v1.0.1

状态：**冻结用于 provider-free development qualification；不授权 Participant 或正式 benchmark。**

日期：2026-09-17。父规范为 `EXPERIMENT_1_MINIMUM_EXECUTION_SPEC_V1_0_1.md`。

## 1. 判定范围

本规范冻结 `reaction-to-crystallization` 的五个可执行 Worlds 与实体、参数、结构
三个 prior loci。15 个 `World × locus` unit 独立判定；科学 FAIL 保留并继续 P，
平台失败才停止受影响 block。

## 2. 五个 Worlds

| World | seed | world-axis intervention | 角色 |
|---|---:|---|---|
| C-W01 | 0 | 无 | 中央参考 |
| C-W02 | 1 | `crystallization.kinetic-profile`, extrapolation `+0.75` | 强成核 |
| C-W03 | 2 | `crystallization.kinetic-profile`, extrapolation `-0.75` | 弱成核 |
| C-W04 | 3 | `crystallization.solubility-cooling-profile`, extrapolation `+0.80` | 高溶解度尺度 |
| C-W05 | 4 | kinetic `+0.45`；solubility/cooling `-0.80` | 耦合边界 |

W00 使用 seed 900004，只作 canary，不进入 15-unit denominator。

## 3. C-E：结晶溶剂 dossier 映射

- 使用已审计的 crystallization-specific catalyst/solvent dossier 与
  `reaction-crystallization-latent-materials-v1`。
- Misspecified arm 只交换 solvent-S1/S3，permutation `[0, 3, 2, 1]`；catalyst
  dossier 保持不变。
- 固定 upstream reaction、catalyst-C0、seed mass `0.008 g`；在 crystallization
  temperature `290 K` 与 `270 K` 两个 cooling anchors 比较 S1/S3。
- 每 cell 3 个 keyed-noise replicates：每 World 12 次，共 60 次。
- final assay 指标固定为 crystal yield、purity、size、CSD quality、fines 与 score。

## 4. C-P：成核/冷却局部阈值

- 固定 catalyst-C0、solvent-S0、seed mass `0.008 g` 与 upstream composition。
- crystallization temperature 固定为 `310 / 290 / 270 K`，每点 3 replicates：
  每 World 9 次，共 45 次。
- aligned threshold generator 只读取 private
  `crystallization_solubility_multiplier`：
  `clip(290 + 20 ln(multiplier), 275, 305) K`；misspecified band 相对 aligned
  center 向高温平移 `20 K`，两个 band 等宽 `10 K`。
- qualification 要求公开 crystal-yield crossing：高/低温端点差异超过
  `max(0.10, 3 sigma)`，并且三个点中至少一对相邻点跨过 yield `0.15`。
- Participant 最小反证预算为 3 个 batch；不得改变 seed、solvent 或 upstream feed。

## 5. C-S：seed-mediated nucleation–growth

- 直接复用已冻结的 structural-candidate design：seed mass
  `0.001 / 0.008 / 0.015 g` × crystallization temperature
  `310 / 290 / 270 K` 的 3×3 grid；中等 cooling 下三个 seed levels 各做 3 个
  validation replicates。
- 每 World 18 次，共 90 次。分析使用 axis effects、seed×cooling topology
  signature、noise gate、held-out disagreement 与 blind aligned advantage。
- 本 locus 测试同一个 PBM 内的 seed-mediated causal relationship，不伪称存在两个
  PBM law families。历史 Work II 的 0/5 结果只是设计审计依据，不替代本轮证据。

## 6. 执行安全

所有 blocks write-once、exact replay、provider call 0、Participant/正式 benchmark
未授权。执行顺序 W00 → entity → parametric → structural → composite。完成后无论
是否有科学失败，campaign action 为 `record_c_result_and_continue_to_p`。
