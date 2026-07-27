# S0-20 经典优化算法基线结果

日期：2026-07-27
状态：development-only；固定 world seed 0、五个算法 seed，不是跨世界正式结论

## 1. 本次实现了什么

为修正后的 S0 静态电化学环境新增了一套完整实验级经典优化接口。算法每次选择一个完整九参数电化学配方，执行到 final assay 后才接收反馈。

冻结 reward 合同如下：

- 主优化反馈：`terminal_summary.leaderboard_score`；
- 不使用环境的 `fresh_measurement_score_delta`；
- 安全标签：完整实验的 `peak_safety_risk`；
- 安全风险独立建模，不再次写入主 reward；
- 最终提交：探索期 best-observed 已测试配方；
- 主要终点：与 LLM 相同的三次配对盲验证推荐分数均值；
- 每个 run：20 次探索 + 3 次 incumbent 验证 + 3 次 recommendation 验证，共 26 次物理实验。

算法内部可使用 unit vector 和类别 one-hot，但收据始终保留命名物理参数。内部坐标不是科学证据，也不向 LLM 暴露。

## 2. 算法矩阵

共运行六种算法，每种五个算法 seed：

1. Uniform Random；
2. balanced Latin hypercube；
3. Greedy local perturbation；
4. Structured GP expected improvement；
5. Structured random-forest expected improvement；
6. Structured safety-constrained GP expected improvement。

所有方法使用同一个静态 world seed 0、相同的 20 轮 horizon、相同 observation-noise 语义坐标和相同盲验证噪声。总计执行 600 次探索实验和 180 次验证实验，无模型 API 调用。

## 3. 聚合结果

| 算法 | 盲验证均值 | 中位数 | 标准差 | 最小值 | 最大值 | 达到 0.58 | 第 8 轮 best 均值 | 第 20 轮 best 均值 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Random | 0.3572 | 0.4535 | 0.2013 | 0.0727 | 0.5665 | 0/5 | 0.2703 | 0.4315 |
| LHS | 0.4691 | 0.4278 | 0.1000 | 0.3597 | 0.5909 | 1/5 | 0.3237 | 0.4916 |
| Greedy | 0.4287 | 0.5115 | 0.2768 | 0.0183 | 0.7071 | 2/5 | 0.4002 | 0.4794 |
| Structured GP-EI | **0.5540** | **0.5921** | 0.1195 | 0.3889 | 0.7018 | **3/5** | 0.3937 | **0.5550** |
| Structured RF-EI | 0.3967 | 0.5185 | 0.2836 | 0.0498 | 0.7020 | 1/5 | 0.3929 | 0.5008 |
| Structured Safe GP-EI | **0.5540** | **0.5921** | 0.1195 | 0.3889 | 0.7018 | **3/5** | 0.3937 | **0.5550** |

当前 LLM S0-20 的单次最终盲验证均值是 `0.4508`。它高于 Random 的五-seed 均值，接近 LHS，但低于 Structured GP-EI 的均值约 `0.1032`。因为 LLM 目前只有一个运行，不能据此做正式方法显著性结论。

## 4. 最好结果

最高盲验证结果来自 Greedy seed 1：

```text
electrolyte_profile = 1
solvent = 0
reagent_amount_mol = 0.004434
probe_potential_V = 1.124410
probe_current_mA = 75.593660
probe_duration_s = 890.044496
controlled_potential_V = 0.906609
controlled_current_mA = 102.035805
controlled_duration_s = 3600
```

- 探索观测分数：`0.706655`；
- 三次盲验证：`0.709554, 0.703961, 0.707658`；
- 盲验证均值：`0.707058`。

Structured GP-EI seed 1 的盲验证均值为 `0.701763`，Structured RF-EI seed 1 为 `0.701956`。这证明当前修正世界中的 `0.58` 阈值是实际可达的；此前 100 点随机搜索得到的 `0.4860` 只是稀疏 sampled reference，不接近实际优化上界。

高分配方的共同特征是：

- solvent 0；
- electrolyte profile 1；
- 较低 reagent inventory；
- 较强且较长的 probe stage；
- controlled stage 常降低 potential，同时延长处理时间；
- selective product yield 约 `0.40-0.45`，远离 `0.02` gate；
- faradaic、transport、ohmic 和 energy efficiency 同时较高。

## 5. Reward 与噪声问题

直接使用 terminal leaderboard score 是正确的主 reward，但 raw best-observed 不是始终可靠的最终选择规则。

最明显的失败例子是 Random seed 3：

- 探索观测分数：`0.416324`；
- 探索 selective product yield：`0.022093`，刚刚超过 `0.02` gate；
- 盲验证 selective product yield 均值：`0.003568`；
- 最终盲验证分数：`0.072659`。

Structured RF-EI seed 0 也从探索 `0.419792` 降到盲验证 `0.144276`。这些都不是回放错误，而是 final-assay uncertainty 被乘法 gate 放大后的 winner's curse。

各算法“盲验证减探索最好分数”的均值：

- GP-EI：`-0.0010`；
- Safe GP-EI：`-0.0010`；
- LHS：`-0.0225`；
- Greedy：`-0.0507`；
- Random：`-0.0743`；
- RF-EI：`-0.1041`。

因此下一版强基线应增加 noisy/replicate-aware final selection，例如保留 2-4 个实验预算复测候选 incumbent，或者按后验均值而不是单次最大观测提交。benchmark 主要终点仍应保持独立盲验证，不应把验证反馈返还算法。

## 6. Safe BO 为什么没有区别

Safe GP-EI 与普通 GP-EI 的五条轨迹完全相同。原因不是代码没有执行风险模型，而是每轮 2048 个候选全部满足预测风险上界小于 `0.65`；所有实际实验的 peak risk 也低于约 `0.253`。

这说明当前 S0 参数边界内安全约束没有形成有效 trade-off。Safe GP-EI 在本任务上是冗余基线。若要测试安全优化，应降低安全阈值或扩展能产生真实风险差异的动作区域，而不能把两条相同轨迹当成独立算法证据。

## 7. 对 S0 任务语义的影响

当前 S0 Agent 在实验开始前一次性提交 probe 和 controlled 两个阶段的全部参数，因此它不能读取 probe 测量后再决定 controlled stage。经典优化器发现的高分配方会直接把 probe stage 当成第一个生产阶段优化，例如使用接近 900 秒的高电流 probe。

这在当前执行合同下是合法的，但意味着 S0 实际测量的是：

> 固定世界中的两阶段完整配方优化。

它不是：

> 根据 probe 结果在同一次实验内在线适配第二阶段。

LLM 的科学叙事倾向于把 probe 保持温和，而无叙事约束的 BO 会利用两个阶段的全部生产能力。这是 LLM 与 BO 差异的一部分，正式论文中必须明确，或者把真正的实验内适配拆成另一条任务。

## 8. 审计

- 30/30 cells 完成；
- 600/600 探索实验独立回放一致；
- 180/180 盲验证实验独立回放一致；
- 静态世界、隐藏字段隔离、已知 horizon、原子执行、最终提交匹配、receipt hash 和物理实验计数全部通过；
- provider 调用数为 0，token 数为 0；
- 结果仅反映一个固定 world seed 上的算法随机性，尚未测试跨 world seed 泛化。

结果目录：`runs/development/static_scientific_optimization_s0_classic_baselines_20_seed0_world_5algseeds_20260727`
