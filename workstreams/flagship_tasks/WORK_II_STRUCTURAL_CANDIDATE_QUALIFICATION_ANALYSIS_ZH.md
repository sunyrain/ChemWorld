# Work II structural candidate qualification：阶段分析

日期：2026-08-11  
状态：provider-free qualification 已完成；尚未产生 participant/provider outcome。

## 结论先行

本阶段完成了两个候选机制、五个 world seed、每个 world 18 条固定查询，共 `180/180`
provider-free executions。所有结果均有 exact replay，`0` platform failure、`0` physical boundary
failure、`0` unsafe completed outcome。

最终没有候选获得进入 12-experiment participant D1 的资格：

- electrochemical transport：响应面上的电位效应、电流效应和高电流效率损失在 `5/5` worlds
  均清楚存在，但 Q2 的 aligned/misspecified prior disagreement 只有 `4/9` 的 worlds 达到
  `40%` gate；world `0` 和 `3` 只有 `2/9`，因此不能宣称跨 world 的 prior-discrimination
  qualification。
- crystallization nucleation/growth：cooling effect 在 `5/5` worlds 通过，但 seed effect 和
  seed-specific topology 只有 world `2` 达到 `6 sigma`；其余四个 world 的 seed 信号低于噪声
  门，且五个 world 的 Q2 prior disagreement 都为 `0/9`。该候选在当前公开观测和固定背景下不能
  稳定区分 seed-mediated 与 seed-negligible 结构。

这是科学资格门的结果，不是平台故障，也不是 participant/model failure。D1 配置没有生成，因而
不应启动真实模型 participant session。

## v0.1 设计缺陷及处理

首次 180 条执行使用了 `(low,low) → (middle,middle) → (high,high)` 的 diagonal validation
groups。两个干预轴同时变化，不能识别“current 造成的 transport 差异”或“seed 造成的 CSD
差异”。此外，电化学 reduced prior 的效率项错误允许 current-dependent linear term，与其
“efficiency approximately stable”的文字 prior 不一致。

v0.1 的执行层本身是完整的（`180/180` replay、无平台/物理失败），但 Q2 identification
contract 无效；其 rejection 不进入科学分母。按照平台缺陷规则，修正后两项 candidate 都从
world `0` 重新执行。v0.2 固定：

- electrochemical：固定中间 potential，验证 current `{low, middle, high}`；
- crystallization：固定中等 cooling，验证 seed `{low, middle, high}`；
- 保持 world、主网格、`6 sigma` effect floor、`40%` disagreement gate 和所有 pass/failure
  规则不变。

## v0.2 执行审计

| 候选 | 主网格 | noisy validation | 完成 | exact replay | physical | platform | 通过 worlds |
|---|---:|---:|---:|---:|---:|---:|---:|
| Electrochemical transport | 45 | 45 | 90 | 90 | 0 | 0 | 3/5 |
| Crystallization nucleation/growth | 45 | 45 | 90 | 90 | 0 | 0 | 0/5 |
| 合计 | 90 | 90 | 180 | 180 | 0 | 0 | 0/2 candidates |

### Electrochemical transport

| World | Potential effect | Current effect | High-current signature | Q2 disagreement | 结果 |
|---:|---:|---:|---:|---:|---|
| 0 | pass | pass | pass | 2/9 = 22.2% | reject |
| 1 | pass | pass | pass | 4/9 = 44.4% | pass |
| 2 | pass | pass | pass | 4/9 = 44.4% | pass |
| 3 | pass | pass | pass | 2/9 = 22.2% | reject |
| 4 | pass | pass | pass | 4/9 = 44.4% | pass |

因此，候选的物理结构是有价值的：五个 world 都显示高电流效率损失，而且两条控制轴均有
足够大的 endpoint response。但在 world `0` 和 `3`，高电流反例相对 noisy validation 的
`6 sigma` margin 不足，只有低电流一侧的两个 efficiency pairs 被 prior disagreement gate
识别。它支持“存在 transport limitation”的 evaluator-level规律，不支持“agent 可以在所有
world 稳定区分两个初始结构”的更强 claim。

### Crystallization nucleation/growth

| World | Seed effect | Cooling effect | Seed topology | Q2 disagreement | 结果 |
|---:|---:|---:|---:|---:|---|
| 0 | fail (`0.0479 < 0.0920`) | pass | fail | 0/9 | reject |
| 1 | fail (`0.0238 < 0.0485`) | pass | fail | 0/9 | reject |
| 2 | pass (`0.1524 > 0.1357`) | pass | pass | 0/9 | reject |
| 3 | fail (`0.0277 < 0.0385`) | pass | fail | 0/9 | reject |
| 4 | fail (`0.0456 < 0.0565`) | pass | fail | 0/9 | reject |

这不是“结晶模块没有规律”。Cooling 规律在五个 world 都很强；失败点是 seed intervention
在大多数 world 的公开 CSD/fines 观测中没有超过预注册噪声门，且 seed-negligible prior 与
aligned prior 在固定 cooling 的 validation pairs 上没有达到 40% disagreement。换言之，
当前背景下 seed-mediated structure 不是一个稳定可辨识的 participant task。

## 责任归因

本 block 没有 participant agent，所有查询由冻结的 evaluator action plan 发出，因此没有“模型
选择错误操作”的责任项。也没有 schema-valid 操作触发 dynamic constitution boundary；故
physical failure 为 `0`。如果后续 participant 自主选择超温或不安全条件，那些结果应在另一个
participant 分母中标为 participant-induced physical/unsafe outcome，不得与本 block 的
platform audit 混淆。

## 阶段价值和下一步边界

1. 已验证 ChemWorld 能在不调用 provider 的情况下完成跨 world、带噪声、可 replay 的机制筛选，
   并把执行完整性与科学资格分开。
2. Electrochemical candidate 可作为“transport-limited response surface”的 evaluator-level
   结果保留，但不能升级为 participant capability claim。
3. Crystallization candidate 在当前固定背景下应作为科学拒绝保留；不能通过降低 `6 sigma`、
   放宽 `40%` 或删除失败 world 来制造通过。
4. 当前没有任何 candidate 获得 D1 授权，因此本阶段不消耗 WellAU/DeepSeek provider budget。
   下一步只能在新的、独立冻结的 candidate 或观测设计上继续 provider-free screen；不能把本阶段
   结果直接扩成正式 participant/R5 实验。

