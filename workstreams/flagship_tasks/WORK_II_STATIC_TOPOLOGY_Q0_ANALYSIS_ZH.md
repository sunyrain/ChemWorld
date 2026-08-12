# Work II static reversible-path topology Q0：阶段分析

日期：2026-08-12
状态：provider-free seed-0 Q0 已完成；不扩展至 worlds `0–4`。

## 结论先行

本阶段研究的是**固定世界中的因果拓扑差异**，不是运行过程中物理规律发生变化。每条执行从初始化到
final assay 始终使用 baseline irreversible-target world 或 reversible-target world；两类世界只在目标路径
是否增加 `P → A` reverse channel 上不同。Agent、participant session 和 provider 均未参与。

两个任务共完成 `36/36` paired executions、`36/36` intervention-aware exact replay，耗时
`208.443 s`。0 physical failure、0 platform failure、0 unsafe outcome。36 个 baseline/reversible pairs
全部共享相同 action-plan hash 与 keyed observation-noise hash；机制 hash 在每条执行内固定，公开 payload
无 mechanism/intervention/private/evaluator leakage。summary self-hash、两个 raw task bindings、36 条轨迹和
36 个 receipts 全部通过后审计。

冻结结果为：

- **Reaction-to-crystallization：通过。** 可逆目标路径在 batch reaction 后积累出清楚、可重复的
  yield/conversion/selectivity 差异，并呈现长时间下更大的 yield gap。
- **Flow-reaction-optimization：科学拒绝。** 同一 topology 确实被正确编译和执行，但在当前连续流
  装置、停留时间范围与 UV/Vis 观测下效应远小于冻结噪声门。

因此整体决定为 `retain_q0_scientific_rejection_and_do_not_expand`：不进入五-world Q1/Q2，不构造
aligned/misspecified structural priors，也不启动 participant D1。

## 完整分母与执行完整性

| Task | executions | exact replay | physical | platform | unsafe | 结果 |
|---|---:|---:|---:|---:|---:|---|
| Reaction-to-crystallization | 18 | 18 | 0 | 0 | 0 | pass |
| Flow-reaction-optimization | 18 | 18 | 0 | 0 | 0 | reject |
| 合计 | 36 | 36 | 0 | 0 | 0 | do not expand |

两任务均通过以下基础门：

- topology 恰好增加一条 reverse reaction；
- effective reverse rate constant 为 `0.0005 s^-1`；
- baseline/reversible mechanism hashes 不同且 deterministic；
- 执行轨迹绑定到预期 mechanism hash，执行中不改变；
- paired action plans、paired observation noise、finite/observed direct metrics 和 exact replay 全部通过；
- participant-visible leakage 为 0。

这些结果把“世界结构正确执行”与“公开实验能否识别结构”分开：flow 的失败不能归因于平台。

## Batch crystallization：强且具有时间累积的拓扑信号

| Direct metric | 最大 paired effect | declared sigma | 冻结门 | 结果 |
|---|---:|---:|---:|---|
| Yield | 0.1757 | 0.012 | 0.050 | pass |
| Conversion | 0.0730 | 0.012 | 0.050 | pass |
| Selectivity | 0.1703 | 0.018 | 0.054 | pass |

共有 6 个彼此分离的 grid cells 超过至少一个 direct-metric gate，覆盖三个温度水平的中/长 reaction
times；不是单一孤立最优点。Yield 的 baseline-minus-reversible gap 从最短时间平均 `0.0348` 增至最长
时间平均 `0.1525`，增加 `0.1176`，显著超过 `0.0300` accumulation gate。这与可逆路径随反应时间
积累回流损失的结构解释一致。

因此 crystallization 不只是“endpoint 数值有差”，而是形成了可反驳的 intervention signature：若目标路径
不可逆，延长时间不会产生同等程度的 target rollback；若存在 reverse channel，长时间下 yield gap 扩大。
它可保留为未来 A-S 重新组对时的强候选。

## Continuous flow：物理差异存在，但公开可辨识性不足

| Direct metric | 最大 paired effect | declared sigma | 冻结门 | 结果 |
|---|---:|---:|---:|---|
| Yield | 0.0245 | 0.045 | 0.135 | fail |
| Flow conversion | 0.0269 | 0.040 | 0.120 | fail |
| Selectivity | 0.0538 | 0.040 | 0.120 | fail |

没有 grid cell 达到 direct-metric gate。最长与最短 residence-time 的 gap increase 只有：

- yield：`0.0137 < 0.0900`；
- flow conversion：`0.0130 < 0.0800`。

这不是“reverse channel 没有执行”：机制 audit、hash binding、paired noise 和 replay 全部通过，raw paired
values 也显示非零效应。失败来自当前连续流切片的物理时间尺度与 UV/Vis 噪声共同作用：反应物在装置中的
有效停留时间不足以让 `0.0005 s^-1` reverse channel 积累出稳定可见的差异。

不应事后把 severity 或 reverse rate constant 调大，因为这会改变已经冻结的候选结构强度；也不应降低
`3 sigma` 门或改用无噪声 evaluator truth 代替 public observation。这样的修改只能属于新的独立候选，不能
修补本 block。

## 实验价值、边界与下一步

1. 结果证明 ChemWorld 可以在不引入动态世界变化的情况下研究 static initial-world-model topology：同一
   structural law 在每条 session 内固定，Agent 后续只需通过实验区分不同候选结构。
2. “结构被正确编译”不等于“结构对 participant 可识别”。相同 reversible topology 在 batch 与 continuous
   apparatus 中产生了截然不同的 observation identifiability，这本身是重要的方法学结论。
3. Reaction-to-crystallization 作为 A-S 强候选永久保留；flow 候选作为有效科学负结果保留。不得只扩展
   crystallization、删除 flow 或换 world 来制造双任务通过。
4. 若继续 A-S，下一步应另行冻结一个与 crystallization 组对的新 task/apparatus candidate，优先选择能提供
   低噪声直接 reaction measurements 且具足够物理时间尺度的任务。新候选必须先独立 seed-0 Q0，再进入五-world
   qualification；本次结果不被替换。
