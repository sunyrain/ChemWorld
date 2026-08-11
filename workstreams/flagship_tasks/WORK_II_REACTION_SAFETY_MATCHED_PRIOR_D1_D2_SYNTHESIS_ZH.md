# Work II reaction-safety matched-prior D1/D2 综合分析

日期：2026-08-11

## 1. 完整证据规模

三个 development worlds 共完成：

- `9/9` persistent Codex sessions；
- `90/90` complete experiments；
- `630/630` committed operations；
- `45/45` belief checkpoints；
- `48/48` evaluator truth queries 与 `54/54` blind replays，全部 exact replay；
- evaluator provider calls 为 0，participant trajectories rerun 为 0；
- 11 个 public unsafe outcomes、0 dynamic physical-constraint events、0 resource rejections、
  0 provider errors、0 platform failures。

Provider accounting 合计为 `11,118,008` input tokens，其中 `9,862,144` cached、`1,255,864`
uncached，cache-hit 占比 `88.7%`；output 为 `136,553` tokens。共有 5 次 recovered MCP failures，
最大连续失败始终不超过 1。九个 participant session 累计 elapsed time 为 `5,208.6 s`。

## 2. 三个 world 的核心结果

| World | Arm | Held-out error | Improvement | Law error | Reliability | Unsafe | Best endpoint |
|---:|---|---:|---:|---:|---|---:|---:|
| 0 | opaque | `0.1088 -> 0.0589` | `+0.0499` | `0.0589` | 不适用 | 5 | `0.4192` |
| 0 | aligned | `0.1052 -> 0.1107` | `-0.0055` | `0.3036` | `0.70 -> 0.45` | 1 | `0.4182` |
| 0 | misspecified | `0.1785 -> 0.1361` | `+0.0424` | `0.0639` | `0.70 -> 0.20` | 1 | `0.4163` |
| 1 | opaque | `0.1118 -> 0.0351` | `+0.0767` | `0.0351` | 不适用 | 0 | `0.4045` |
| 1 | aligned | `0.1213 -> 0.0188` | `+0.1025` | `0.0611` | `0.70 -> 0.68` | 4 | `0.3990` |
| 1 | misspecified | `0.1386 -> 0.0344` | `+0.1041` | `0.0541` | `0.70 -> 0.85` | 0 | `0.4033` |
| 4 | opaque | `0.1958 -> 0.0559` | `+0.1399` | `0.0568` | 不适用 | 0 | `0.4922` |
| 4 | nominal aligned | `0.2288 -> 0.0486` | `+0.1803` | `0.3816` | `0.70 -> 0.84` | 0 | `0.4801` |
| 4 | nominal misspecified | `0.1298 -> 0.0532` | `+0.0765` | `0.5054` | `0.70 -> 0.35` | 0 | `0.4900` |

world 4 的方向列不进入成功/失败判断。Q2 冻结注册方向为 lower-temperature，但 16-query
empirical direction 为 higher-temperature；该 binary diagnostic 被标记为 `query_subset_conflict`。
逐查询 prediction error、law error、endpoint 和 replay 不受此冲突影响。

## 3. 最重要的科学结论

### 3.1 “纠正错误先验”不是单一能力

三个 world 给出了三种彼此不同的组合：

1. world 0：模型显式发现冲突并把可靠度降到 `0.20`，但没有恢复真实方向；
2. world 1：模型恢复了真实方向并显著改善预测，却没有承认先验错误，可靠度反而升到 `0.85`；
3. world 4：模型显式降权并改善逐点预测，但 binary direction 本身对评价分布不稳定，不能作恢复判断。

因此至少需要把 prior correction 分解为：conflict detection、confidence revision、held-out
predictive correction、directional recovery、executable-law formation 和 action commitment。任何一个指标都
不能替代其余指标。

### 3.2 正确先验也可能被自选证据破坏

world 0 的 aligned arm 从正确方向更新到错误方向，held-out error 恶化，law error 升至 `0.3036`；
world 1 的 aligned arm 则形成最准确的最终预测。两者说明正确先验的价值取决于 agent 选择什么实验、
如何解释局部证据，以及是否把噪声或局部结构错误外推为全局规律。论文不能只问“prior 是否正确”，还必须问
agent 是否能够保护仍被证据支持的先验。

### 3.3 预测准确不等于形成可执行规律

world 4 三臂 final prediction error 都约为 `0.05`，但两个 supplied-prior arms 的 law error 分别达到
`0.3816` 和 `0.5054`。模型可以给出一组相对准确的离散预测，却无法把它们压缩成与自身预测一致、可执行、
可迁移的规律。这直接支持把 prediction、law 和 action 分成不同 evaluator 层。

### 3.4 “正确/错误”必须绑定作用域和查询分布

world 4 的 Q2 注册方向来自全 response-surface construction，而冻结的 16-query evaluator subset 给出相反
empirical direction。其根源不是平台执行错误，而是二维非线性规律被压缩成单一高温/低温陈述后，对 duration
分布和查询选择敏感。后续正式 prior 必须同时绑定 reference context、作用域、评价分布和稳定性门；否则
“aligned”只是一种 nominal construction label，不能被直接写成绝对正确先验。

### 3.5 endpoint 和安全行为都不能代表科学理解

每个 world 内三臂 best endpoint 都非常接近，但 prediction、law、reliability 和冲突诊断差异巨大。
安全信号也不稳定：world 0 中 opaque 最不安全，world 1 中 aligned 独有 4 个 unsafe outcomes，world 4
全部为 0。因此不能声称提供先验普遍提高安全性，也不能用最优 endpoint 代表规律发现。

## 4. H3 与现阶段可支持的表述

三个 development worlds 的描述性 H3 分别为 `+0.0479`、`+0.0016` 和 `-0.1037`，方向高度异质。
它们不能支持“错误先验相对于正确先验产生稳定的差分改善”这一总体效应，更不能作 inferential claim。

现阶段能够支持的最强结论是：

> Experimental agents can detect prior conflict, improve held-out predictions, recover a directional
> regularity, form an executable law and commit an action, but these achievements are empirically
> separable and need not co-occur within the same campaign.

不能支持的结论包括：

- agent 已稳定摒弃错误先验；
- 正确先验总能帮助探索或提高安全性；
- endpoint optimization 等价于科学理解；
- 当前单 task、三个 development worlds 已建立跨任务或总体统计效应；
- world 4 已给出可解释的 binary direction recovery 结果。

## 5. 对下一阶段的约束

1. 在任何新的 directional-prior provider block 前，readiness 必须验证注册方向与 evaluator query
   distribution 的 empirical direction 一致；不一致则在 provider 调用前停止。
2. A-P 仍需第二个通过同等 Q0--Q2 和 stability gate 的 task，才能形成跨 task 结论。
3. 正式分析必须保留 prediction、law、reliability、conflict、action 和 safety 六层，不得退化为 endpoint 表。
4. D1/D2 结果提交用户审核；未经审核不进入 R5，也不启动 conditional transfer。

机器报告：

- `workstreams/flagship_tasks/reports/work-ii-reaction-safety-matched-prior-d1-evaluation-20260811.json`
- `workstreams/flagship_tasks/reports/work-ii-reaction-safety-matched-prior-d2-world1-evaluation-20260811.json`
- `workstreams/flagship_tasks/reports/work-ii-reaction-safety-matched-prior-d2-world4-evaluation-20260811.json`
