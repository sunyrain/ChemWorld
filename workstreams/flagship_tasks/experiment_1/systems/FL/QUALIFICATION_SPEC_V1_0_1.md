# Experiment 1 FL qualification specification v1.0.1

状态：**冻结用于 provider-free development qualification；不授权 Participant 或正式 benchmark。**

日期：2026-09-17。父规范为 `EXPERIMENT_1_MINIMUM_EXECUTION_SPEC_V1_0_1.md`。

## 1. 范围与判定语义

本规范把 `flow-reaction-optimization` 的五个可执行 Worlds 与实体、参数、结构
三个 prior loci 冻结为 15 个独立 atomic units。每个 unit 独立给出
`qualified` 或 `failed`；不要求 15 个全部通过，科学失败保留后继续下一个体系。

本轮只运行冻结的 truth-replay qualification，provider call 为 0。任何结果均不得
解释为 Participant 表现或正式 benchmark 分数。

## 2. 五个 Worlds

五个 Worlds 使用 seeds 0–4，并以已经注册的 flow world axes 形成不同的可执行
private truth。所有数值由 runtime intervention manifest 推导，不把 guidance 中的
authoring proposal 当作已经实现的物理参数。

| World | seed | world-axis intervention | 角色 |
|---|---:|---|---|
| FL-W01 | 0 | 无 | 中央参考 |
| FL-W02 | 1 | `flow.reaction-kinetics`, extrapolation `+0.75` | 快动力学 |
| FL-W03 | 2 | `flow.reaction-kinetics`, extrapolation `-0.75` | 慢动力学 |
| FL-W04 | 3 | `flow.residence-thermal-boundary`, extrapolation `+0.80` | 长有效停留/强热边界 |
| FL-W05 | 4 | kinetics `+0.45`；residence/thermal `-0.80` | 耦合边界 |

W00 使用独立 seed 900003，只做环境、dossier、truth binding 与 exact replay canary，
不进入 15-unit denominator。

## 3. FL-E：催化剂 dossier 映射

- 公开 prior 使用通用反应 catalyst/solvent nominal dossier；FL 被显式加入 audited
  task registry，因为流动 runtime 使用同一 compiled reaction network 与 catalyst
  residual。
- Misspecified arm 只交换 catalyst-C1 与 catalyst-C2，permutation 固定为
  `[0, 2, 1, 3]`；solvent dossier 与文本模板不变。
- 固定 solvent-S0、flow rate `1.2 mL/min`、temperature `390 K`；在 nominal
  residence `300 s` 与 `900 s` 两个 anchor 比较 C1/C2。
- 每个 cell 3 个独立 keyed-noise replicates：每 World 12 次，共 60 次。
- 判别指标为公开 UV `yield / selectivity / flow_conversion`。每个 anchor 均要求
  mean support separation、single-metric separation 与 SNR 通过；同时要求真实
  world 中 aligned catalyst mapping 未被 residual 反转。

## 4. FL-P：温度—停留时间局部关系

- 固定 solvent-S0、catalyst-C1、flow rate `1.2 mL/min`。
- 公开最小局部面为 temperature `{370, 410} K` × nominal residence
  `{450, 1500} s`，每点 3 个 keyed-noise replicates：每 World 12 次，共 60 次。
- Aligned prior：在该冻结局部域内，更长 residence 对公开 product metrics 的净效应
  为非负；Misspecified prior 使用完全同构格式并把方向反转。
- Qualification 不以几何字段变化本身作为证据。必须观测到 outlet
  `yield / flow_conversion` 的 paired consequence；receipt 同时记录 configured
  residence、effective minimum duration、reactor volume、geometry length 与 action
  hash，防止把接口自动构造设备只当作 bookkeeping 差异。
- Participant 最小反证设计恰为 4 个唯一 grid cells；replicates 仅用于 qualification。

## 5. FL-S：不可逆 vs reversible target pathway

- parent law 为 baseline compiled network；paired child 增加
  `reversible_target_pathway_stress_v1`，不改其它 action 或 observation-noise 坐标。
- grid 固定为 temperature `{350, 390, 425} K` × residence
  `{300, 900, 1800} s`；两种 law 各一次：每 World 18 次，共 90 次。
- 直接指标为公开 UV `yield / selectivity / flow_conversion`。
- 门禁继承 static-topology Q0：至少两个 direct metrics 超过各自
  `max(0.05, 3 sigma)`；支持点空间分离；至少一个 product metric 出现 duration
  accumulation signature；mechanism hash、paired action、paired noise 和 exact replay
  全部匹配。
- 历史 seed-0 Q0 的科学失败只说明此设计可能再次失败，不能替代本次五 World
  qualification，也不得在看到本轮结果后修改阈值。

## 6. 执行与停止规则

所有 blocks 均要求 Q1–Q8、write-once output、exact replay、truth binding、零
participant/provider call。平台失败停止受影响 block 并先写 recovery note；科学门禁
失败被记录后继续。执行顺序为 W00 → entity → parametric → structural → composite。

完成后输出 FL 的 15-unit registry，并与 EC、RX、PA registry 合并。若存在科学失败，
campaign action 仍为 `record_fl_result_and_continue_to_c`。
