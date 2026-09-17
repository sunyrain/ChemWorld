# Experiment 1 FL qualification specification v1.1.0

状态：**冻结用于 provider-free development qualification；不授权 Participant 或正式 benchmark。**

日期：2026-09-18。父规范为 `EXPERIMENT_1_MINIMUM_EXECUTION_SPEC_V1_0_1.md`。
本规范完整取代 FL v1.0.1 的 15 个 development units，但不删除其历史证据。

## 1. 修复理由与设备不变量

v1.0.1 把公开输入 `residence_time_s` 与流速同时作为自由变量，并按
`V = Q tau` 重建反应器体积。这会把参数比较混入设备几何变化，因而不能证明同一
流动反应器内 residence-time prior 的可辨识性。

v1.1.0 冻结同一套硬件：

- reactor volume `V = 0.018 L`；
- internal diameter `d = 0.004 m`；
- geometry length 由 `V` 和 `d` 唯一推导并在所有 receipts 中保持不变；
- 公开操纵量是 `flow_rate_mL_min`；
- 物理停留时间由 `tau_s = 1080 / Q_mL_min` 唯一推导；
- 兼容字段 `residence_time_s` 可以由 action 携带，但 runtime 不用它改变几何或物理。

正式 optimization recipe 保持 8 维以兼容现有 Agent adapter，但不保留死坐标：旧的独立
residence coordinate 在 search-space v1.3 中改为真实可控的 `feed_volume_L`；流速、温度和
run duration 的坐标含义不变。action 中的 `residence_time_s` 仅声明由流速推导出的值。

本修复不改变五个 World、观测噪声、公开 direct metrics、Q1--Q8 名称或已冻结的
数值门槛。旧 `flow.residence-thermal-boundary` axis 在 v1.1.0 中只扰动热边界，
不再缩放 residence time。extrapolation 正向端冻结为 wall-UA multiplier `0.02`，表示
弱耦合/近绝热边界；负向为其对数对称的强耦合方向。这个跨度必须通过通用 world-axis
真实响应测试，不能只产生不同 hash。

## 2. 五个 Worlds

W00 使用 seed 900003，仅做 canary，不进入 denominator。FL-W01--W05 保留 seeds
0--4 与原 intervention manifests；其角色更新为：中央参考、快动力学、慢动力学、
弱热边界、动力学--强热边界耦合。五个 World 的实际 private truth 仍由 runtime
manifest 推导并写入 receipt，不由本文人工指定输出。

## 3. FL-E：催化剂 dossier 映射

- Misspecified arm 仅交换 catalyst-C1 与 catalyst-C2，permutation 固定为
  `[0, 2, 1, 3]`；公开模板和 schema 与 aligned arm 同构。
- 固定 solvent-S0、temperature `390 K`，比较 C1/C2。
- 两个流速 anchor 为 `3.6` 和 `1.2 mL/min`，对应推导 residence `300` 和
  `900 s`；每 cell 3 个独立 keyed-noise replicates。
- 每 World 12 次、五 World 共 60 次。公开判别指标为
  `yield / selectivity / flow_conversion`。
- 每个 anchor 都必须通过冻结的 mean separation、single-metric separation 与 SNR
  门槛；真实 World 中 aligned catalyst mapping 还必须未被 residual 反转。

## 4. FL-P：固定硬件上的流速效应

- 固定 solvent-S0、catalyst-C1；temperature 为 `{370, 410} K`。
- 流速为 `{2.4, 0.72} mL/min`，对应推导 residence `{450, 1500} s`；每点
  3 个 keyed-noise replicates。
- Aligned prior：在冻结局部域内，较慢流速（较长推导 residence）对公开 product
  metrics 的净效应为非负；Misspecified prior 使用同构格式并反转方向。
- 每 World 12 次、五 World 共 60 次；Participant 最小反证设计仍为 4 个唯一
  temperature-by-flow cells。
- Q7 除 endpoint consequence 外，必须证明全部 receipts 使用同一个 reactor volume
  与 geometry length，且 action 流速与 runtime configuration 一致。

## 5. FL-S：不可逆 vs reversible target pathway

- parent 为 baseline compiled network；paired child 只增加
  `reversible_target_pathway_stress_v1`。
- grid 为 temperature `{350, 390, 425} K` x flow rate
  `{3.6, 1.2, 0.6} mL/min`，对应推导 residence `{300, 900, 1800} s`。
- 两种 law 在每个 cell 共用 action plan 和 observation-noise coordinate；每 World
  18 次、五 World 共 90 次。
- 直接指标、effect thresholds、空间分离、duration accumulation、mechanism binding、
  exact replay 与 noise pairing 规则沿用 v1.0.1；support 的第二坐标改为真实操纵的
  flow-rate index，分析时仍用推导 residence 判断 accumulation。

## 6. 执行、失败与停止规则

执行顺序为 W00 -> entity -> parametric -> structural -> composite。所有 outputs
write-once；先执行 primary，再在独立目录进行 exact replay。平台失败停止受影响 block
并写 recovery note；科学门禁失败冻结为 `failed-development` 后继续，不允许看到结果
后修改门槛或删减 denominator。

本轮 provider call 与 Participant execution 均为 0。结果只代表 development
qualification；不得解释为 Participant 表现或正式 benchmark score。
