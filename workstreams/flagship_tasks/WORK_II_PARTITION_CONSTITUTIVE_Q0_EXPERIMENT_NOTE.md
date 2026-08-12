# Work II partition constitutive-law functional-form A-S Q0 — experiment note

状态：**provider-free seed-0 Q0 design freeze；尚未执行**  
执行边界：开发模式可在非 clean 工作树上运行，不生成旧式 source/C2 binding，结果一律标为
`development_only` 且不得进入 C2。问题、覆盖、分母、测量和门槛在开发/发布模式间完全相同；
只有功能与设计稳定后，才用一次最小执行面 release manifest 重跑发布证据。
适用阶段：A-S candidate qualification；通过只允许进入不变的 five-world Q1/Q2，不授权 participant/provider。

## Question

在固定 `partition-discovery` world、材料、仪器和公开操作合同下，线性 distribution-coefficient
response 与 power-response functional form 是否能被两个独立公开干预轴稳定区分？本候选研究固定世界中的
constitutive-law structure，不研究 contact 与 settling 哪个模块“更重要”，也不改变运行中的物理规律。

## Tested units and coverage

- `public-test` world seed `0`；两条 law 为 baseline exponent `1.0` 与冻结 power-response exponent
  `1.75`。
- `3 × 3` provider-free grid：aqueous dilution/load volume `{0.006, 0.015, 0.024} L` × organic
  extractant/phase volume `{0.008, 0.019, 0.030} L`。固定 solvent `0`、extractant `1`、solvent volume
  `0.020 L`、mix `420 s / 800 rpm`、settle `900 s`。
- 每个 cell 在两条 law 下执行相同行动，合计 `9 × 2 = 18` complete experiments。两边共享 keyed
  observation-noise namespace/seed；HPLC 与 final assay 的 noise coordinates 必须逐 cell 配对。
- 每条轨迹必须 exact replay。任一 platform failure 停止整个 block；修复后从第一个 cell 重新执行，
  不改变 exponent、grid 或门槛。

## Measurements

- 分相后的 HPLC 与 terminal final assay：`product_in_organic`、`product_in_aqueous`、`phase_ratio`。
- 每通道的完成数、physical/platform/unsafe outcomes、observed mask、finite values、exact replay、
  action-plan/noise pairing、constitutive binding、公共 payload leakage 与机器证据 hash。
- 双轴效应：固定另一轴时，各 metric 在 load levels 与 phase-volume levels 上的最大公开 range。
- functional-form signature：paired power-minus-linear gap 的 load curvature 或 load × phase-volume
  interaction contrast；不以单个 composite score 代替结构证据。

## Pass/failure rules

只有以下条件全部满足才通过 Q0：

1. `18/18` outcomes classified，`18/18` exact replay，`0` platform failures；两条 law 的 action plan、
   HPLC noise 与 final-assay noise 均逐 cell 相同。
2. 审计证明反应网络和公共合同不变，唯一 constitutive difference 是
   `partition_coefficient_exponent: 1.0 → 1.75`，并且执行绑定 deterministic。
3. HPLC 与 final assay 的三个注册 metrics 均 finite 且 publicly observed。
4. 对每个 instrument-metric channel，effect gate 固定为 `max(0.03, 6 × declared_sigma)`。至少一个
   注册通道在 load 轴超过自身 gate，且至少一个注册通道在 phase-volume 轴超过自身 gate。
5. 至少一个注册通道的 paired law-gap load curvature 或 load × phase-volume interaction contrast
   超过自身 gate。
6. 至少两个不同 grid cells 的 paired law gap 超过对应 channel gate；不能由一个孤立 cell 支撑。
7. participant-visible payload 不包含 intervention、hidden state、private seed 或 evaluator truth。

Scientific failure 被永久保留，不得降低 `6σ`、调大 exponent、换 seed、删 cell 或只保留有利 instrument。

## Expected outputs

1. 一个 raw task report，包含 18 条 receipt、两通道完整分母、全部失败和 constitutive audit。
2. 一个 readable machine summary，带 deterministic self-hash、raw binding、精确 gates、双轴与
   interaction/nonlinearity 结果。
3. 严格 validator；只有 summary 和 raw report 均通过且科学 gates 全通过，才允许进入不变的
   five-world provider-free Q1/Q2。Q0 不生成 12-round participant config。
