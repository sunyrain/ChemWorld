# S0 反应到结晶静态科学优化正式实验报告

日期：2026-07-27

## 结论

`reaction-to-crystallization` 已完成与电化学旗舰对称的五世界正式 S0 实验。模型面对固定世界，每轮提交一个完整反应、结晶和过滤方法；20 轮探索结束后，另用一次调用提交最终综合方案。五个 world seed 的探索、最终综合、Predictive、盲验证和逐实验 replay 全部完成。

核心结果：

- 盲最终分均值 `0.4829`，中位数 `0.4980`，范围 `0.4219–0.5258`。
- 五个世界的最佳探索均出现在第 16–20 次实验，最佳轮次均值为 `17.4`；20 轮不是冗余预算。
- 五次最终提交全部为 `tested`，没有使用插值或外推；相对配对 incumbent 的盲增益全部为 `0`。
- Predictive 为 `20/45 = 44.4%`，低于电化学 S0 的 `64.4%`，说明局部响应方向知识仍弱。
- Declared structural edge F1 为 `0.242`，unsupported claim rate 为 `75.1%`；自由声明的机理解释不可靠。
- 最佳经典算法为 GP-EI / Safe-GP，25-cell 盲均值均为 `0.5324`；LLM 低 `0.0495`。

因此，模型在结晶旗舰中表现为“能够持续改进完整工艺，但尚未稳定超过结构化黑箱优化，也没有可靠地把观察转成可迁移机理判断”。

## 单次实验合同

模型直接选择 10 个具名物理控制：

```text
reaction_temperature_K
reaction_duration_s
reagent_amount_mol
stirring_speed_rpm
catalyst
catalyst_amount_mol
solvent
seed_mass_g
crystallization_temperature_K
crystallization_duration_s
```

结晶温度的公开耦合约束为：

```text
crystallization_temperature_K <= min(315 K, reaction_temperature_K - 55 K)
```

固定执行序列为：

```text
add_solvent
add_reagent
add_catalyst
heat
quench
hplc
seed_crystals
cool_crystallize
hplc
filter_crystals
terminate
final_assay
```

模型每轮只决策一次，不在实验内部再次调用。两个 HPLC 槽位分别表示结晶前反应结果和过滤前浆料结果。单位向量只保留为算法基线的内部编码，不向模型展示。

## 正式结果

| World seed | 最佳探索分 | 最佳轮次（0-based） | 盲最终分 | Predictive | 最终类型 | 峰值风险 |
|---:|---:|---:|---:|---:|---|---:|
| 0 | 0.4402 | 18 | 0.4219 | 4/9 | tested | 0.1738 |
| 1 | 0.5348 | 15 | 0.5258 | 4/9 | tested | 0.1945 |
| 2 | 0.5096 | 18 | 0.4980 | 4/9 | tested | 0.1813 |
| 3 | 0.5064 | 19 | 0.5039 | 4/9 | tested | 0.1761 |
| 4 | 0.4642 | 17 | 0.4648 | 4/9 | tested | 0.1953 |

100 次正式探索的峰值安全风险均值为 `0.1842`，最大为 `0.1953`，远低于 `0.65`。因此当前 Safe-GP 约束没有绑定，不能把 Safe-GP 与 GP 的同轨迹解释为安全算法的额外优势。

## 经典基线

6 个算法、5 个算法 seed、5 个 world seed，共 150 cells、3,000 次探索和 900 次盲验证。所有 cell receipt 哈希一致。

| 方法 | 25-cell 盲均值 | 中位数 | 最低 | 最高 | 平均最佳轮次 |
|---|---:|---:|---:|---:|---:|
| GP-EI | 0.5324 | 0.5319 | 0.4916 | 0.5732 | 14.48 |
| Safe-GP | 0.5324 | 0.5319 | 0.4916 | 0.5732 | 14.48 |
| RF-EI | 0.5257 | 0.5296 | 0.4539 | 0.5939 | 17.68 |
| LHS | 0.5252 | 0.5253 | 0.4576 | 0.5738 | 8.40 |
| Random | 0.5071 | 0.5014 | 0.4528 | 0.5671 | 12.44 |
| Greedy | 0.5043 | 0.5061 | 0.4401 | 0.5551 | 14.92 |
| LLM，单次运行/世界 | 0.4829 | 0.4980 | 0.4219 | 0.5258 | 18.40（1-based） |

LLM 在五个世界均低于该世界表现最好的算法家族均值。150 个基线 cell 中有 110 个最佳点出现在第 11–20 轮，进一步支持 20 轮预算。

## 世界理解

### Predictive

最终综合在同一次调用中预测三个冻结的一因子干预：反应温度、晶种质量和结晶温度。预测提交后才执行配对模拟，每个查询 2 个配对重复，共 12 次物理实验，不增加模型调用。

- 方向正确率：`20/45 = 44.4%`。
- confidence Brier：均值 `0.2712`，越低越好。
- 真实非平凡效应率：`66.7%`。
- 五个 seed 都是 `4/9`，表明模型形成了相似但系统性不完整的局部规律。

### Declared

- structural edge F1：`0.242`。
- matched-edge directional accuracy：`0.900`，但只在少量结构匹配声明上计算。
- mechanism tag F1：`0.175`。
- unsupported claim rate：`0.751`。
- confidence Brier：`0.793`。

Declared 不能支持“模型正确理解了结晶世界”的结论；Predictive 更直接，但当前准确率也只支持弱局部知识。

## 交互例子

seed 1 展示了较稳定的优化：

- round 0：`0.4130`，使用 catalyst 1 / solvent 1、298.15 K 结晶、10,800 s。
- round 10：切换到 catalyst 0 / solvent 0，并把结晶温度降到 292.15 K，得分 `0.4992`。
- round 15：把结晶延长到 14,400 s、温度降到 287.15 K，得分 `0.5348`。
- 最终提交 round 15 条件，配对盲均值 `0.5258`。

seed 0 展示了跨世界差异：

- round 0 为 `0.2975`。
- 在识别 catalyst 2 / solvent 2 后，继续降低结晶温度并延长到 14,400 s。
- round 18 达到 `0.4402`，最终盲均值 `0.4219`。

模型在所有世界都倾向把结晶时间推到上界，四个世界把晶种质量推到或接近上界。这是可观察的策略收敛，不等于它已经正确识别全部成核和生长机理。

## 资源和审计

- Provider calls：`105`；attempts：`113`。
- Provider-reported tokens：`1,269,110`。
- 当前正式统计：100 次探索 + 60 次 Predictive + 15 次 incumbent 验证 + 15 次 recommendation 验证 = `190` 次物理实验。
- 五个 seed 均为 `cell_status=completed`，逐实验 replay 全部通过。
- 最大探索 prompt 估算 `14,866`，最大最终综合 prompt 估算 `17,192`，低于 `30,000 / 42,000` 上限。
- WellAU 没有提供可核实定价，货币成本继续标记为 accounting incomplete。

主要资产：

- 协议：`configs/benchmark/scientific_optimization_s0_v0.5_crystallization_high_20_formal.json`
- 方法：`configs/methods/llm_v0.5/participant_methods_s0_wellau_codex_sol_high_crystallization_20.json`
- 五 seed 聚合：`runs/formal/static_scientific_optimization_s0_v05_crystallization_high_20_5seed_20260727/multiseed_report.json`
- 基线聚合：`runs/development/static_scientific_optimization_s0_v05_crystallization_classic_baselines_20_5worlds_20260727/multiseed_report.json`
