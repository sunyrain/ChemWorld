# Work II electrochemical mechanism-oracle 阶段分析

日期：2026-08-11  
状态：provider-free qualification 完成；Q2 matched-prior construction 已授权；尚无新的 participant outcome

## 1. 本阶段回答的问题

本阶段不评价模型，也不寻找一条可直接放进 participant prompt 的最优配方。它验证
`electrochemical-conversion` 在五个预注册 world 中是否都具备：

1. 可安全执行并可精确重放的完整响应面；
2. 非孤立的高质量局部区域；
3. 能由实验辨认的 controlled-potential/current 局部规律；
4. 足够低的观测噪声，使后续 aligned 与 misspecified prior 可以被证伪；
5. 不依赖单个有利 seed 的跨 world 稳定性。

所有搜索、truth 读取与 noisy validation 均由 evaluator 执行，provider call 为零，不能把本阶段结果解释为
agent 已经发现了规律。

## 2. 完整分母与可靠性

| 项目 | 结果 |
|---|---:|
| Worlds | `5/5` passed |
| Unique mechanism outcomes | `14,160/14,160` classified and completed |
| Observed validations | `120/120` completed |
| Exact replays | `120/120` |
| Physical failures | `0` |
| Unclassified/platform failures | `0` |
| Provider calls | `0` |
| Wall time | `4,208.665 s` |

五个 raw world report 的绑定 hash 均已复核，逐 world 注册 checks 全部为 true。因而这是可用于下一资格阶段
的环境证据，而不是因执行缺口产生的“看起来通过”。

## 3. 逐 world 科学结果

| World | Oracle score | Risk | Observed absolute gap | Relative basin | Directional effect | Curvature | Historical-threshold hits |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | `0.849001` | `0.064272` | `0.003950` | `54` | `0.741141` | `0.370142` | `1,334/2,832` |
| 1 | `0.770420` | `0.040784` | `0.000645` | `36` | `0.488594` | `0.250119` | `877/2,832` |
| 2 | `0.837543` | `0.063469` | `0.005334` | `68` | `0.556397` | `0.284232` | `1,597/2,832` |
| 3 | `0.833371` | `0.064143` | `0.001934` | `47` | `0.583462` | `0.285408` | `994/2,832` |
| 4 | `0.809066` | `0.063913` | `0.003001` | `43` | `0.643489` | `0.320826` | `1,032/2,832` |

安全 score 的 `P90-P10` 为 `0.577977--0.700991`，selective-product-yield range 为
`0.544372--0.742297`。每个 world 都存在内部高质量点，且 local grid 上 potential/current 的方向效应和曲率
都远高于噪声门。这说明后续不是让模型在近乎平坦的表面上猜测微弱差异。

## 4. 实验价值

### 4.1 支持的结论

- **真实存在可发现的参数规律。** controlled potential/current 对结果有大幅且非纯线性的影响；曲率意味着
  agent 需要总结局部适用域，而不是只记住“越高越好”一条口号。
- **规律可以通过独立观测验证。** oracle candidate 的 noisy median 与 noiseless score 最大只差
  `0.005334`，远小于局部效应和响应面动态范围。
- **不是阈值校准造成的伪任务。** 每个 world 有 `877--1,597` 个点达到历史 `0.58` 阈值，约占
  `31.0%--56.4%`；与 reaction safety 不同，electrochemical 的成功区绝对可达。
- **具备跨 world 复制空间。** 五个 world 都通过而 basin 大小和最优分数仍有变化，可在不挑 seed 的前提下
  检查 prior correction 是否稳定。

### 4.2 不支持的结论

- **不能用本任务证明安全探索能力。** 所有 oracle risk 都远低于 `0.65`，五个 world 的 safety frontier
  count 均为零。安全与动态边界结论应由 reaction safety 承担。
- **不能声称 agent 已发现规律。** 本阶段是 evaluator oracle qualification，没有 participant session。
- **不能把 oracle optimum 交给模型。** Q2 只能使用压缩的规律、反证区域和 held-out query；精确 vector、
  hidden mechanism parameters 与 optimizer provenance 必须继续隔离。

## 5. 对 Q2 的直接约束

Q2 应围绕 `controlled_potential_delta_V` 与 `controlled_current_delta_mA` 构造三臂 matched cluster：opaque、
aligned 和 misspecified。两个 supplied priors 必须在 reference context 附近具有匹配的 baseline utility、字数、
置信度和字段集合，同时在 held-out 区域产生足够但不过度显然的预测分歧。强方向效应使 prior 具有可证伪性，
明显曲率则要求 held-out queries 同时覆盖方向、曲率和局部适用域，不能只测一个二元方向标签。

Q2 仍是零 provider 阶段。只有五个 world 的 baseline matching、双向反证、blind identifiability、leakage 和
schema gates 全部通过，才可生成 electrochemical D1 config。任何 Q2 失败都保留并停止该 task 的 provider
扩展，不根据结果放宽门或更换 world。

## 6. 阶段结论

`electrochemical-conversion` 已通过五 world mechanism-oracle qualification，并授权进入 Q2
matched-prior construction。它在论文矩阵中的最合理角色是 **A-P 参数/动力学规律发现与错误先验纠正任务**；
reaction safety 则继续承担 **安全探索与动态物理边界**。两者共同覆盖不同能力环节，但不能互相替代或混合
结论。
