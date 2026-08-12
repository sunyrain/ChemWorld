# Work II static catalyst-deactivation Q0 分析

日期：2026-08-12

## 1. 完成度与有效性

- `27` 个 temperature × duration × catalyst-dose cells，各执行 deactivating baseline 与
  stable-catalyst law，共 `54/54` completed；
- `54/54` intervention-aware exact replay，`27/27` action plans 与 keyed HPLC noise 完全配对；
- 0 physical failures、0 platform failures、0 unsafe completed outcomes；
- stable world 从构造起完整移除唯一 `catalyst_deactivation` reaction，保留 target、side 与 degradation
  三条反应；derived mechanism hash 确定、与所有执行记录一致；
- 54 trajectories、54 receipts、1 task report 和 tracked summary 的分母、自哈希与 raw binding 均通过审计；
- 0 provider calls、0 participant sessions。正式运行耗时 `74.357 s`，平均约 `43.6 executions/min`。

启动前曾有一次外层命令超时关闭 stdout；该尝试在生成 summary 前终止，未形成正式分母，残留 raw root 已整体
移至仓库外。随后从 seed 0、第一单元和同一冻结设计完整运行。本分析只绑定完整 `54` 次 block。

## 2. 冻结判定

决策为 `retain_q0_scientific_rejection_and_do_not_expand`。四项科学门失败：

- 没有至少两个 direct metrics 超过 topology effect gate；
- 没有达到门槛的两个分离 safe cells；
- 没有达到门槛且跨两个 catalyst doses 的支持；
- duration accumulation signature 未达到冻结阈值。

| Direct HPLC metric | 最大 stable − deactivating gap | Gate | 比值 |
|---|---:|---:|---:|
| yield | `0.006153` | `0.050` | `0.123×` |
| conversion | `0.005626` | `0.050` | `0.113×` |
| selectivity | `0.005316` | `0.054` | `0.098×` |

三项最大值均出现在 `410 K / 14,400 s / 0.000315 mol`。稳定催化剂在全部 `27/27` cells 的三项指标上
方向均为正，但平均 gap 仅为 yield `0.003047`、conversion `0.002822`、selectivity `0.003215`。
因此不能把方向一致误写为 participant-identifiable mechanism effect。

长时效应确有积累，但量级不足：yield gap 从最短时长均值 `0.000747` 增至最长时长 `0.004471`，增量
`0.003724 < 0.030`；conversion 对应增量为 `0.003290 < 0.030`。Final-assay 最大 yield/conversion/
selectivity gaps 同样只有 `0.006078/0.005558/0.005264`，safety-risk 最大差仅 `0.000313`。

## 3. 失败归因

这不是 mechanism compiler、runtime、measurement、replay 或 ledger 故障：

1. 结构变换真实且唯一，只移除了 `Cat_active -> Cat_dead`；
2. 每次实验从第一步至 final assay 使用一个固定 mechanism hash；
3. 所有 action/noise pairs、公开 HPLC、final assay 与 exact replay 均完整；
4. 运行时初始 `Cat_active=0`，公开 `add_catalyst` 是唯一催化剂注入。机制卡中的 `0.015 mol` 只是独立
   mechanism reference initialization policy，runtime reagent charging 明确排除 catalyst species，不存在隐藏库存
   淹没公开 dose 的问题。

失活通道也不是未被激发。以 `0.000315 mol` catalyst 的恒温机制诊断为例，`14,400 s` 后 active catalyst
损失约为 `14.5%`（350 K）、`25.5%`（410 K）和 `36.5%`（465 K）。但下游 product response 受底物耗尽、
uncatalyzed side pathway 和 product degradation 共同压缩，只形成千分位的公开 yield/conversion/selectivity
差异。故本结果是**任务—机制可辨识性科学拒绝**：机制存在、可达且有因果效应，但当前公开干预范围和
观测通道不足以让 participant 可靠区分该结构。

## 4. 后续边界

- 不提高 deactivation rate、不改 catalyst dose 上限、不延长冻结 task process envelope、不降低 `3 sigma`
  gates，也不选择性保留最有利 cell；
- 不扩展至 worlds 0–4，不生成 matched prior、participant D1 或 provider block；
- crystallization 的 static reversible-path 通过结果继续独立保留；reaction-safety 不与其组对；
- A-S 下一候选应优先选择已有强结构效应和直接下游测量的 task，而不是继续调大本失活机制。

机器摘要：`workstreams/flagship_tasks/reports/work-ii-catalyst-deactivation-q0-seed0-20260812.json`。

