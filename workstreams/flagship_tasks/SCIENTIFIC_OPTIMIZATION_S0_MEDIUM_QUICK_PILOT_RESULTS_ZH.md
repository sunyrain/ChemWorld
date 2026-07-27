# S0 电化学静态优化：WellAU medium quick-pilot 结果

日期：2026-07-26
状态：development quick-pilot 完成；不是正式 benchmark 结果

## 1. 结果位置

- 完成运行：`runs/development/static_scientific_optimization_s0_wellau_codex_sol_medium_quick_r7_seed0_completed_v2_20260726`
- 主报告：`report.json`
- 单格收据：`receipts/s0_codex_sol_medium_quick--electrochemical-conversion.json`
- 独立回放：`postrun_audit.json`

方法为 WellAU `gpt-5.6-sol`、`reasoning_effort=medium`、单一静态世界 seed 0。科学预算未缩减：
8 次 exploration、1 次最终综合、12 次 Predictive 配对模拟、6 次 Actionable 盲验证。

## 2. 执行审计

最终收据中的 11 次 provider calls 和 11 次 attempts 均有 usage 记录：

- prompt tokens：78,127；
- completion tokens：16,279；
- total tokens：94,406；
- 最大 experiment-design prompt estimate：7,855；
- final-synthesis prompt estimate：10,376。

另有 2 次已知但未形成收据的 provider calls。它们来自第一版 continuation 在全部完成前不写
checkpoint：一次第 8 轮决策和一次被本地 schema 拒绝的最终综合。报告显式记录：

- `known_unreceipted_provider_call_count = 2`；
- `effective_minimum_provider_call_count = 13`；
- `provider_token_accounting_complete = false`。

因此本轮不能把 94,406 当作完整 token 成本，只能作为有收据部分的下界。WellAU 没有仓库可核实
单价，USD accounting 仍不完整。

本地重放结果：

- exploration：8/8 verified；
- Predictive：12/12 verified；
- Actionable validation：6/6 verified；
- query、result、score、receipt hash、物理实验计数和 atomic executor 全部一致。

## 3. 优化结果

八轮 leaderboard scores：

`0.05688, 0.25831, 0.26114, 0.25995, 0.01539, 0.02089, 0.06800, 0.25642`

最佳探索实验是 experiment 2，experiment 7 对同一 recipe 做了复测。模型最终提交 tested recipe：

- electrolyte profile 2；solvent 2；reagent 0.012 mol；
- probe：0.80 V、40 mA、300 s；
- controlled：1.10 V、110 mA、3300 s；
- 三个 diagnostic slots 全部保留。

盲验证：

- recommendation scores：`0.26180, 0.26319, 0.15668`；
- recommendation mean：`0.22723`；
- incumbent mean：`0.22723`；
- recommendation gain over incumbent：`0.0`。

这说明 medium 模型正确地把“最终方法”理解为已经重复测试的稳健 incumbent，而不是为了提交
一个不同答案强行外推。它没有在 Actionable 层超过 incumbent；单 seed 也不能支持方法优越性结论。

## 4. Predictive 层

三个冻结单因素问题共 9 个方向预测：

- directional accuracy：`7/9 = 0.77778`；
- confidence Brier score：`0.17234`；
- nontrivial actual-effect rate：`7/9 = 0.77778`。

模型正确预测了全部 current 和 electrolyte-profile 指标。两个错误都来自 potential query：

- 预测 energy efficiency 会下降，实际变化 `-0.00691`，未越过 0.01 阈值；
- 预测 leaderboard score 会下降，实际增加 `+0.01126`。

因此本轮有初步证据表明模型能把证据转成未执行干预的方向预测，尤其对电流和介质效应较好；
但 potential 附近的效应幅度和综合得分方向仍不稳定。该结论仅适用于一个 world seed。

## 5. Declared 层

Declared score 很低：

- structural edge F1：`0.11765`；
- directional accuracy：`0.0`；
- unsupported claim rate：`1.0`；
- confidence Brier score：`0.90691`。

这不等于模型完全没有科学理解。模型声明的是联合介质条件、matched-pair 差异和多变量操作窗口，
例如 `solvent + electrolyte_profile -> leaderboard_score`，而隐藏 reference 主要是单 cause、单 effect
边。模型的经验叙述与 Predictive 成绩明显好于 Declared graph score。

这暴露了下一版必须预冻结的设计选择：Declared scorer 是只接受单变量局部边，还是允许条件化边、
联合原因和 operating-window claims。不能在本 seed 的结果上修改 reference 后重新宣称本轮得分提高。

## 6. 本轮暴露的工程问题

1. mock 历史低估了真实模型文本长度，第 8 轮提示为 7,855，原 7,500 cap 在发请求前主动停止。
2. 第一版 continuation 缺少逐阶段 checkpoint，造成 2 次已知调用没有 token 收据；现已改为探索完成立即落盘。
3. 模型返回 `schema_version`，原严格 validator 将其视为未知 extra；现在该字段必须等于冻结版本。
4. recipe 使用 `controlled_potential_V/current_mA/duration_s`，旧 claim vocabulary 使用无阶段名称；
   现在只做等价重命名，不增加 reference edges 或 endpoints。

上述修正均属于 development qualification。本轮结果不得标记为 formal benchmark。

## 7. 当前判断

medium quick-pilot 已达到目的：验证完整 S0 + Predictive 流程能在真实 provider 上运行，并得到一个
可解释样本。当前不应立即启动 high 五 seed，因为 high 方法配置仍使用 mock-derived 7,500/9,000
prompt caps，而且 Declared 条件化 claim contract 尚未重新预冻结。

下一步应先冻结 high 的真实文本预算与 Declared scorer v0.2，再开始独立 seeds；本 medium seed 只作为
开发证据和协议诊断，不混入未来 high 主结果。
