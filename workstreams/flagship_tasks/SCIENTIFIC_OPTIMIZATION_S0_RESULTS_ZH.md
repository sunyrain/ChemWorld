# S0 静态科学优化实验结果

日期：2026-07-26

状态：`development-only; formal_result=false; benchmark_claim_allowed=false`

S0 的目的只有一个：在世界固定不变、没有 hidden-world 字段、没有机制候选和没有 world intervention 的条件下，测量 Agent 是否能利用公共实验反馈优化任务性能。

最终采用的真实 provider 运行是 WellAU `gpt-5.6-sol` Direct，r2 方法合同：

`runs/development/static_scientific_optimization_s0_wellau_codex_sol_r3_20260726`

机器可读结果：

- [report.json](D:/Projects/ChemWorld/runs/development/static_scientific_optimization_s0_wellau_codex_sol_r3_20260726/report.json)
- [postrun_audit.json](D:/Projects/ChemWorld/runs/development/static_scientific_optimization_s0_wellau_codex_sol_r3_20260726/postrun_audit.json)

## 1. 合同边界

S0 每个 task 执行 8 个连续完整实验：

- world seed 固定为 `0`；
- 整个 campaign `world_policy=static_for_entire_campaign`；
- `interventions=[]`；
- 没有 phase change；
- public context 不包含机制候选、hidden truth、changed/no-change arm 或 change point；
- Agent 只输出 search vector、measurement slots、measurement objective、expected effect 和 uncertainty；
- executor 只负责 recipe compilation、操作执行、terminate 和 final_assay。

S0 不测量 change detection、mechanism attribution、change recovery 或 Stateful-vs-Direct effect。

## 2. 执行结果

| 指标 | 结果 |
| --- | ---: |
| Cells | 2 |
| Tasks | reaction-to-crystallization、electrochemical-conversion |
| 完成实验 | 16/16 |
| Provider calls / attempts | 16/16 |
| Provider-reported tokens | 84,210 |
| Accounting | incomplete；WellAU 无可核实定价 |
| 已知 billed cost | USD 0，不能解释为免费 |
| Infrastructure failures | 0 |
| 最大 prompt estimate | 6,392 / 7,000 |

确定性 postrun audit 结果：

- 2/2 receipts replay verified；
- 16/16 experiments exact replay verified；
- report receipt hashes 全部匹配；
- static world policy 验证通过；
- 所有 plan 均无 `mechanism_distribution`、`belief_update_rule`、`scientific_state`。

## 3. Task 结果

### reaction-to-crystallization

score 曲线：

```text
0.2285, 0.3296, 0.3276, 0.3485,
0.3486, 0.3424, 0.3229, 0.3449
```

- first score：`0.2285`；
- best score：`0.3486`；
- last score：`0.3449`；
- last-minus-first：`+0.1163`。

模型先探索较宽的区域，随后围绕实验 4 的高分区域做局部 refinement。后半段 search vectors 变化幅度变小，说明模型在固定世界中表现出从探索到局部利用的行为转换。

### electrochemical-conversion

score 曲线：

```text
0.0716, 0.3519, 0.3555, 0.3650,
0.3565, 0.3563, 0.3570, 0.3575
```

- first score：`0.0716`；
- best score：`0.3650`；
- last score：`0.3575`；
- last-minus-first：`+0.2859`。

模型在第 1、2、3 次迅速找到显著更好的 operating region，随后多次保持 solvent/electrolyte 组合不变，只做局部 refinement；后四次 score 稳定在 `0.356-0.358` 附近。这个结果说明它不仅能发现高分区域，也能在本轮静态条件下进行局部确认，但仍需要更多 seeds 才能判断这种稳定性是否可重复。

这也是 S0 当前最有价值的静态基线信号：

> 在固定世界中，模型可以进行有效探索，也能找到高分条件；本轮 electrochemical cell 的局部利用较稳定，但 reaction cell 仍有小幅回落，整体稳定性必须由多 seed baseline 验证。

## 4. r1/r2 资格诊断与 r3 最终冻结

先前的 S0 r1 运行不是科学失败，而是合同资格失败：

- reaction task 完成 8/8；
- electrochemical 完成 7/8；
- 第 8 次决策在 provider call 之前被 prompt cap 拦截；
- 估算值 `6298` 超过 r1 上限 `6250`；
- provider 没有收到该次请求；
- world 和物理执行均未出错。

r2 新建独立 development freeze，将静态 prompt cap 从 `6250` 调整为 `7000`，完整重跑 16 个实验并全部通过。但 r2 审阅时发现 system prompt 仍以否定句提到 hidden-world 和 mechanism 概念，虽然没有提供对应字段，仍不符合“静态 S0 完全不引入变化概念”的要求。

r3 在保留 `7000` cap 的基础上移除这类词汇诱导，重新完整执行 16 个实验；本报告只把 r3 作为最终干净 S0 结果。r1/r2 receipts 均保留为可追溯资格诊断，没有覆盖或伪装成 r3 结果。

这个过程说明：即使去掉机制候选，electrochemical task 的公共历史仍可能接近 prompt 边界。S0 后续仍需要更紧凑的 observation/history 表示，而不是无限提高 cap。

## 5. 当前可以得出的结论

可以得出：

1. 固定世界中的静态优化任务可以独立运行，不需要 changed/no-change protocol；
2. WellAU Direct 能在两个 task 上完成完整连续 experiment loop；
3. 模型会利用历史进行探索和局部 refinement；
4. electrochemical task 的最优区域更脆弱，局部利用不稳定；
5. 当前 S0 contract 和静态 replay 基础设施已经可用。

暂时不能得出：

- 该模型具有一般化科学优化能力；
- reaction task 的 `+0.0344` 或 electrochemical task 的 `+0.1292` 是正式优化效果；
- WellAU 优于 DeepSeek 或其他 Agent；
- S0 的 Direct baseline 足以证明 Stateful 没有价值；
- 单个固定 seed 下的 score 曲线可以代表任务总体性能。

## 6. 下一步

S0 的合理下一步不是立刻加入世界变化，而是先补静态基线的可重复性：

1. 使用多个固定 seed 和独立 task repeats；
2. 为每个 task 增加 scripted/random/BO baseline；
3. 记录 best-so-far、last score、local-regret 和重复条件的稳定性；
4. 单独冻结 compact-stateful S0，不带任何 change-detection 字段；
5. 只有静态优化 baseline 稳定后，才重新引入 announced-change，再引入 hidden-change。

因此，S0 不是原来 changed 实验的删减版，而是一个独立的科学基线：先测固定世界中的实验优化，再逐步增加检测、诊断和恢复难度。
