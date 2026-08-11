# Electrochemical matched-prior D1 阶段分析

日期：2026-08-11  
状态：development evidence，`failed_retained`；不进入 R5，不自动扩展，不替换或重跑本次 participant trajectory。

## 1. 冻结分母

本轮是 world 0 的 opaque / aligned / misspecified 三臂、每臂一个 persistent Codex campaign session。
provider 为 WellAU `gpt-5.6-sol` medium，Codex Responses harness + ChemWorld MCP。

| 指标 | 结果 |
|---|---:|
| terminal scientific trajectories | 2/3 |
| operationally qualified cells | 0/3 |
| complete experiments | 20/30 |
| committed operations | 180 |
| belief checkpoints | 8/15 |
| evaluator truth queries / exact replay | 16/16 |
| blind executions / exact replay | 0/18 |
| provider sessions / logical Codex turns | 3/3 |
| evaluator provider calls / participant reruns | 0 / 0 |
| public unsafe / dynamic physical / resource rejection / platform execution failure | 0 / 0 / 0 / 0 |
| cumulative input / cached / uncached / output | 3,154,356 / 2,892,544 / 261,812 / 38,699 |
| recovered MCP failures / provider errors | 18 / 0 |

`aligned_nominal` 和 `opaque` 各完成 10/10 experiments、exact replay 和 resource replay；但分别记录
6 和 7 次 recovered MCP contract/tool failures，超过冻结的每 cell 上限 3。二者均没有 final
belief snapshot 或 committed final recommendation。`misindexed_nominal` 在任何 physical operation 之前
因 5 次连续 belief-snapshot contract 错误被冻结上限正确中止，完成 0 个 experiment。

## 2. 归因

| 现象 | 归因 | 是否 platform physical failure |
|---|---|---|
| 合法 operation 的得分、探索方向和重复选择 | participant scientific outcome | 否 |
| invalid snapshot schema、缺字段、错误 prediction denominator、重复/过早 checkpoint | participant method / tool-contract failure | 否 |
| final assay 后没有 final snapshot / recommendation | participant lifecycle/finalization failure | 否 |
| recovered MCP 总数超过冻结上限 | operational qualification failure；保留 participant 结果 | 否 |
| 16/16 truth exact replay、轨迹 resource replay | platform execution evidence | 平台通过 |
| provider error、resource rejection、物理 rollback、未分类异常 | 本轮均为 0 | 无可归因事件 |

`misindexed_nominal` 的 5 次失败具体包括缺少 `schema_version`、prediction denominator 不匹配、
空 `metric_laws`、law term 缺 `link` 以及 law 未覆盖全部 held-out metrics。它没有形成科学轨迹，
因此不能把它解释成“错误先验被纠正失败”；只能解释为 agent 没有通过实验协议入口。

## 3. 已有科学信号

Q2 truth 的方向审计为稳定的 `lower_controlled_potential`，三组 matched-current 对的
lower-minus-higher score contrast 为 `+0.031954`。因此方向资格本身成立。

在没有 final checkpoint 的前提下，不能把冻结的 primary improvement=0 当作科学上“没有学习”；它是
缺失 final 的失败惩罚。中间 checkpoint 的 held-out normalized error 如下：

| arm | pre | after exp 2 | after exp 4 | after exp 7 | final |
|---|---:|---:|---:|---:|---|
| opaque | 0.290720 | 0.094089 | 0.095843 | 0.090182 | unavailable |
| aligned | 0.250258 | 0.087897 | 0.155712 | 0.142923 | unavailable |
| misspecified | unavailable | unavailable | unavailable | unavailable | unavailable |

这给出三个有限但有价值的观察：

1. aligned prior 在 pre-evidence 已比 opaque 低 `0.040462` 的误差；在 experiment 2 后两臂都出现明显预测改善。
2. opaque 到 experiment 7 仍保持较低 error，而 aligned 在后续 checkpoint 回升，说明探索和 updating
   并非单调，正确先验也可能在噪声下被过度怀疑。
3. aligned 的自报 prior reliability 从 `0.70` 降到 `0.40`，并持续把
   `controlled_potential_V` / `controlled_current_mA` 标为 challenged；这可作为“预测修正”和
   “先验信任更新”分离的 development observation，但不能作为正式效应量。

aligned 的最高 observed endpoint 为 `0.773854`（1.05 V / 90 mA controlled stage），opaque 为
`0.730108`；由于没有 participant final recommendation 和 blind replay，这只是搜索轨迹描述，不能
声称 aligned 的最终策略优于 opaque。

## 4. 这轮支持和不支持什么

支持：

- 当前 electrochemical world、Q2 matched prior、potential-direction truth 和 operation-level
  replay 可以在真实 provider session 中被执行和审计；
- agent 能在部分 checkpoint 上从实验反馈改善 held-out prediction；
- endpoint search、prior reliability self-report 和 predictive correction 必须分开报告。

不支持：

- 错误先验纠正：misspecified arm 没有完成第一条 physical operation；
- final executable law、final action、blind recommendation gain；
- 三臂 H3 或跨 provider / 跨 world 推断；
- D2 或 R5 扩展授权。

因此机器报告中的 complete-case H3 为 `NA`；`0.0000` 仅是冻结的 missing-final failure penalty，不能
写成“没有 H3 效应”。

## 5. 分析和 harness 修复

本轮之后修复了四类不改变 participant 数据的分析/记录问题：

- interrupted-session receipt 现在保留已完成 belief snapshot 和 final-recommendation audit；
- evaluator 对缺失 recommendation 的 cell 保留 blind 分母但跳过执行，不伪造推荐；
- evaluator 支持当前 electrochemical `expected_relation` prior 和 controlled-potential direction；
- evaluator 只把最后一个 controlled electrolysis duration 计入 parametric distance，不再把 probe 630 s
  错加到 3540 s controlled stage。

这些修复不使本轮变成 qualified，也不改变任何实验覆盖、失败规则或 participant outcome。未来若要继续，
必须在用户审核后以新的冻结 block 启动；不得用新结果替换本轮失败轨迹。

机器报告：`workstreams/flagship_tasks/reports/work-ii-electrochemical-matched-prior-d1-evaluation-20260811.json`。

