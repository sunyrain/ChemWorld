# Work II observation/measurement seed-0 screen：阶段分析

日期：2026-08-12  
状态：provider-free seed-0 probe 已完成；不扩展至 worlds `0–4`。

## 结论先行

两个任务共完成 `18/18` noisy executions 和 `6/6` evaluator-truth executions，合计
`24/24` completed、`24/24` deterministic exact replay，耗时 `134.375 s`。全程为零 provider、
零 participant session、零 physical/platform failure、零 unsafe outcome；summary self-hash、
两个 raw report bindings、18 条 noisy trajectories 和 6 个 truth audits 均通过后审计，公开 payload
未发现 evaluator/private leakage。

冻结结果为：

- **Electrochemical observation：通过。** controlled current 对 transport、Faradaic 和 energy
  efficiency 的公开效应分别为 `0.3779`、`0.3858`、`0.3688`，对应噪声门为 `0.0415`、
  `0.0563`、`0.0620`；三者均能在 seed 0 稳定区分干预水平。
- **Crystallization observation：科学拒绝。** 所有执行、观测完整性、bias、replay 和 leakage
  checks 均通过，唯一失败项为 `task_owned_effect_above_noise`。因此整个预注册 seed-0 probe 按规则
  保留为 `retain_probe_and_do_not_expand`，不执行五-world扩展，也不生成 participant D1。

## 完整分母

| Screen | noisy | truth | completed | exact replay | physical | platform | unsafe | 结果 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Electrochemical | 9 | 3 | 12 | 12 | 0 | 0 | 0 | pass |
| Crystallization | 9 | 3 | 12 | 12 | 0 | 0 | 0 | reject |
| 合计 | 18 | 6 | 24 | 24 | 0 | 0 | 0 | do not expand |

## Electrochemical：可见的直接物理指标

| Metric | 三水平效应 | max replicate sigma | 冻结门 | max truth bias | 结果 |
|---|---:|---:|---:|---:|---|
| transport efficiency | 0.3779 | 0.0138 | 0.0415 | 0.0168 | pass |
| Faradaic efficiency | 0.3858 | 0.0188 | 0.0563 | 0.0090 | pass |
| energy efficiency | 0.3688 | 0.0207 | 0.0620 | 0.0098 | pass |
| selective-product yield | 0.0149 | 0.0093 | 0.0300 | 0.0119 | fail |
| ohmic efficiency | 0.0161 | 0.0099 | 0.0300 | 0.0085 | fail |

这说明 public final assay 可以可靠暴露 high-current transport limitation，但并非每个输出都同样
可识别。尤其 composite score 在低电流水平出现 `0.2111` 的 truth bias：direct yield 的小幅正偏差
跨过 scoring multiplicative gate 后被非线性放大。该 score 按冻结的自身噪声门仍通过 bias check，
所以不反向修改本次结果；但它不适合作为后续 A-O prior 的主要观测目标。若以后重新设计 A-O
participant block，应优先使用 transport/Faradaic/energy efficiency 等直接物理指标，并把 score 仅作
secondary outcome。

## Crystallization：失败来自真实 seed 信号过弱

| Metric | 三水平公开效应 | max replicate sigma | 冻结门 | truth 低到高变化 | 结果 |
|---|---:|---:|---:|---:|---|
| CSD quality | 0.0390 | 0.0317 | 0.0950 | 0.0161 | fail |
| crystal yield | 0.0143 | 0.0101 | 0.0303 | 0.0007 | fail |
| crystal size | 0.0151 | 0.0283 | 0.0849 | 0.00004 | fail |
| fines fraction | 0.0056 | 0.0075 | 0.0300 | 0.0003 | fail |
| score | 0.0080 | 0.0046 | 0.0300 | 0.0003 | fail |

所有 metric 的 replicate-mean truth bias 都在冻结门内；失败并非仪器系统偏差或 runner 缺陷。
evaluator truth 本身显示，在固定 `290 K` 背景下将 seed mass 从 `0.001 g` 增至 `0.015 g`，对 yield、
size、fines 和 score 的真实影响近乎为零。CSD 的真实变化稍大，但仍小于 replicate noise。因此当前
世界切片没有提供足够可识别的 seed-mass observation law。

这一结果与 W2-28 structural screen 独立一致：此前 cooling effect 为 `5/5` worlds 可见，而 seed
effect 只有 `1/5` worlds 通过。两条证据共同表明问题不是“结晶没有规律”，而是当前固定背景下
seed intervention 太弱，不能支撑跨 world 的 observation/mechanism prior 研究。

## 实验价值、边界与下一步

1. Q0 的 observation infrastructure 能够在完整任务轨迹中正确工作：公开测量、truth bias、keyed
   replicates、deterministic replay 和 leakage isolation 均已实际验证，而不只是单元测试通过。
2. Electrochemical current-response 是可保留的 A-O 候选，但单任务 seed-0 pass 不足以独立进入
   participant D1；当前冻结 block 要求两个任务共同通过后才扩展。
3. Crystallization seed-mass 候选是有效科学负结果。不得事后降低 `3 sigma`、删除该任务、只扩展
   electrochemical，或把 cooling 替换进同一分母以制造通过。
4. 因 seed-0 gate 未全部通过，当前 A-O 路线到此停止。若仍需 A-O participant claim，必须另写独立
   experiment note，重新冻结至少两个具有直接可观测物理指标的 task/intervention candidates，并从
   新的 seed-0 qualification 开始；本次结果永久保留，不被替换。
