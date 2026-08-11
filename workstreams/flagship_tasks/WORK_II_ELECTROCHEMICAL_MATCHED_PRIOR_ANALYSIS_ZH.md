# Work II electrochemical matched-prior Q2 阶段分析

日期：2026-08-11  
状态：Q2 provider-free qualification 完成；D1 仅获准进入静态 readiness

## 1. 结果总览

| 项目 | 结果 |
|---|---:|
| Worlds | `5/5` passed |
| Surface queries | `605/605` classified and completed |
| Safe fit / held-out | `180 / 425` |
| Physical / platform failures | `0 / 0` |
| Provider calls | `0` |
| Wall time | `168.376 s` |
| Generated held-out queries | `16/world` |
| Prior word count | `127 / 127` in every world |

五个 raw world reports、Q2 package 与 D1 candidate config 均有 hash binding。生成的 D1 配置仍明确设置
`execution_authorized=false` 和 `formal_r5_authorized=false`，因此该结果没有偷偷开启 provider 或正式实验。

## 2. 逐 world 可辨识度

| World | Aligned normalized MAE | Selected axis | True side | Disagreement | Blind margin | Low/high support | Representative distance |
|---:|---:|---|---|---:|---:|---:|---:|
| 0 | `0.139583` | potential | lower | `73/85` | `0.094693` | `21/15` | `10` |
| 1 | `0.152401` | potential | lower | `73/85` | `0.445492` | `36/34` | `9` |
| 2 | `0.129809` | potential | lower | `73/85` | `0.346344` | `31/36` | `10` |
| 3 | `0.145140` | potential | lower | `73/85` | `0.416867` | `36/37` | `9` |
| 4 | `0.121554` | potential | lower | `73/85` | `0.308071` | `34/23` | `10` |

所有 world 的 baseline gap 均为 `0`。这不是把错误 prior 做得与正确 prior 完全一样：两者只在中心
reference neighborhood 一致，外围仍有 `85.88%` held-out queries 产生足够大的预测分歧。因此 agent 不能仅在
reference 附近做一两个保守实验就辨认真伪，必须覆盖 reference 外侧的 potential 区域。

## 3. 这一阶段证明了什么

1. **错误先验既可信又可反驳。** 正误 prior 在初始区域完全匹配，但在外部区域产生稳定、双侧且可盲辨识的
   差异；这比简单给出两个明显不同的最优点更接近真正的先验纠正问题。
2. **最关键规律是 controlled potential，而不是 current。** 五个 world 均首先通过 potential-axis candidate，
   且真实方向均为 lower controlled potential。这个跨 world 一致性使 D1 能测试证据利用，而不是让 world
   异质性掩盖 agent 行为。
3. **world 0 是保守的 D1 选择。** 它的 blind margin `0.094693` 是五个 world 中最小值，但仍接近冻结门
   `0.05` 的两倍。用 world 0 开始不会因挑选最容易 seed 而夸大能力。
4. **拟合并不等于泄露 truth。** aligned quadratic model 的 normalized MAE 为 `0.122--0.152`，不是完美
   oracle；participant 只看到方向性不完整模型，精确系数、optimizer vector 和 world identity 均未进入 prior。
5. **Q2 不贡献安全结论。** 本任务的 Q1 没有安全 frontier，Q2 也没有制造 risk contrast。安全行为继续由
   reaction safety 任务测量。

## 4. 对后续实验的约束

Electrochemical D1 使用 `10` 个共享预算 experiments：`8` 个 unique recipes，加最多 `2` 个 exact repeats。
任务自有资源卡为：

- `110` operation attempts；
- `20` electrolysis operations；
- `45,000 s` process time，其中 `36,000 s` 为八个 unique probe+controlled stage maxima，`9,000 s`
  为两次 exact-repeat allowance，quench/transfer allowance 为 `0`；
- `10` vessel starts、`10` final assays、`30` nonfinal instrument uses；
- reagent/solvent stock 为 `0.345 mol / 0.2875 L`。

这使 electrochemical 不再沿用 reaction-safety 的 `145,200 s`，也不再使用旧四实验的 `72,000 s` 历史上限。
模型选择导致的低分、错误方向、重复浪费或资源耗尽都是 participant 结果；只有 binding、replay、harness 或
provider 基础设施错误才是平台失败。

下一步必须先完成 clean-commit zero-provider readiness：构造 provider-ready execution config，检查 Codex
harness、MCP、credential、single-session、checkpoint、MethodResourceLimits 和方向一致性。Readiness 通过后只
运行 world-0 三臂 D1；由于五个 Q2 worlds 的 axis/direction 一致，不预注册 electrochemical D2。任何 D1
科学失败均保留，不通过追加 world 来“修好”结果。

## 5. 阶段结论

Electrochemical Q2 已把“正确/错误参数先验”收敛成一个真正可控的实验问题：相同 reference evidence 下，
agent 是否会主动探索具有反证价值的 potential 区域，是否降低错误先验可靠度，是否改善 held-out prediction，
并最终形成与行动一致的可执行规律。当前证据只授权 D1 readiness，不授权 provider execution、D2 或 R5。
