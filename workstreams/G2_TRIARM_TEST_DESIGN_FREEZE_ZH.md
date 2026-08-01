# G2 三臂测试设计冻结与资源评估

更新时间：2026-07-31

## 1. 目标与边界

本设计固定同一个 `electrochemical-conversion` 任务、同一个物理 world seed 和同一套 observation-noise namespace，只改变 Agent 获得的材料信息：

1. **未知**：`opaque_codes`，只有匿名 action codes。
2. **已知**：`anonymous_nominal_properties`，正确的匿名 nominal properties。
3. **错配**：`anonymous_misindexed_properties`，Agent 不知情地看到 solvent-S1 与 solvent-S3 交换后的整行属性；物理世界不变。

错配固定为：

```json
{"target_field": "solvent", "descriptor_permutation": [0, 3, 2, 1]}
```

本轮不研究物理规律改变；错配只用于检验错误先验如何改变 operation-level 行为，以及 Agent 是否能依靠后续实验纠错。

## 2. 预先冻结的评价门槛

设计选择采用词典序规则：

1. 所有计划 batch 必须闭合，不能 right-censor。
2. 每条 trajectory 必须 exact replay 通过。
3. 已知臂相对未知臂应出现可见的行为/得分差异。
4. 错配臂首批必须被错误 solvent prior 操纵，后期必须出现离开错误 solvent 的恢复迹象。
5. 满足以上门槛后，优先最小 hard operation envelope；再看 score per hard operation slot 和 unused capacity。

共同报告的指标为：

- paired-world best final score；
- operation-normalized incumbent AUC；
- paired `known - unknown`、`mismatched - known`、`mismatched - unknown`；
- first material choice、late material choice；
- late-minus-early score change；
- lifecycle completion、invalid/resource rejection、ledger utilization；
- exact replay 与 resource-ledger integrity。

五个 seed 只作小样本描述性 paired evidence，不作 confirmatory significance claim。

## 3. 离线候选方案实验

| 设计 | batches | hard operations | 非最终诊断上限 | 实测 cells | replay/lifecycle | 操纵/恢复 | mean best score | all-arm incumbent AUC | score / hard op |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `lean-k4-one-stage` | 4 | 24 | 0 | 15（5 seeds） | 全通过 | 全通过 | 0.77680 | 0.56765 | **0.03237** |
| `diagnostic-k6-one-stage` | 6 | 42 | 6 UV-vis | 9（3 seeds） | 全通过 | 全通过 | 0.74109 | **0.59810** | 0.01765 |
| `adaptive-k6-two-stage` | 6 | 54 | 6 UV-vis | 3（1 seed） | 全通过 | 全通过 | 0.66572 | 0.50850 | 0.01233 |
| `diagnostic-k8-one-stage` | 8 | 56 | 8 | 3（1 seed smoke） | 全通过 | 全通过 | 0.81169 | 0.68545 | 0.01449 |
| `current-rich-k6-control` | 6 | 84 | 18 | 3（1 seed smoke） | replay/lifecycle 通过 | **恢复门槛失败** | 0.81025 | 0.64357 | 0.00965 |

### lean-k4（最终 5-seed）

- 15/15 cells 完成；所有 lifecycle、exact replay、manipulation、recovery gates 通过。
- `known - unknown` 平均：`+0.28368`，5/5 paired worlds 为正。
- `mismatched - known` 平均：`-0.01921`，4 次为负、1 次 tie。
- 错配首批选择 transposed solvent 的比例：100%。
- 错配后期离开 transposed solvent 的比例：100%。
- 错配 late-minus-early score 平均：`+0.10986`。
- 平均 best score：`0.77680`；平均 operation utilization：100%。

典型错配 cell 的资源账本为：24/24 operation attempts、4/4 closed batches、4/4 final assays、0 discard、0 invalid、reagent/solvent stocks 清零，exact replay 通过。

### diagnostic-k6-one-stage（3-seed screen）

- 9/9 cells 完成，所有门槛通过。
- `known - unknown` 平均：`+0.39954`。
- `mismatched - known` 平均：`-0.03377`。
- 错配后期 score recovery 仅约 `+0.00497`，但诊断行为可观测。
- all-arm incumbent AUC 为 `0.59810`，略高于 lean-k4 的 `0.56765`；这说明诊断预算能改善早期 incumbent 曲线，但代价是 hard operations 从 24 增到 42。
- 诊断资源使 hard envelope 增至 42 次，单位 hard operation 得分约为 lean-k4 的 54%。

### adaptive-k6-two-stage（单 seed 账本 smoke）

该方案用于覆盖 UV-vis 与第二电化学 stage 的账本路径，不作为与 5-seed lean 同等统计强度的竞争者：

- 3/3 cells 完成；54/54 operations；6/6 batches；每臂 6 次 UV-vis；0 invalid；stocks 清零；exact replay 全通过。
- 因此 instrument quota、第二 stage、生命周期和精确回放链路均已实际走通。

### diagnostic-k8 与 current-rich-control（单 seed stress smoke）

- `diagnostic-k8-one-stage`：3/3 cells、56/56 operations、8/8 batches、每臂 8 次 UV-vis、0 invalid、stocks 清零、exact replay 全通过；但单位 operation 得分仅 `0.01449`。
- `current-rich-k6-control`：3/3 cells 的 lifecycle 和 replay 通过，但 calibration policy 实际只消耗 42/84 attempts，剩余 12 次 non-final instrument quota；错配恢复门槛失败（late-minus-early score 为负），因此不适合作为默认测试 envelope。

## 4. 最终选择

冻结 **`lean-k4-one-stage`** 为 G2 的最合适正式测试 envelope：

- 它是目前最小的 hard operation 设计；
- 在 5 个 paired world 上仍能稳定观察到已知/未知差异、错配初始操纵和后期恢复；
- 不依赖诊断仪器，账本更简单、成本更低、操作归因更清晰；
- K=6/K=8/rich 方案保留为需要更高诊断密度或恢复曲线时的 sensitivity/control envelope，而不是当前默认测试。

若实验目标改为“最大化早期 incumbent AUC”而不优先控制资源，则 `diagnostic-k6-one-stage` 是合理的 sensitivity 方案；当前目标同时要求寻找最合适的资源总量，因此默认仍选择 lean-k4。

这不是“单次最高分”选择：如果只按最高 final score，可能漏掉错配先验根本没有影响 Agent，或把偶然命中误判成恢复。

## 5. 三臂真实 Codex 执行协议

已新增冻结协议：

- [3x3 tri-arm protocol](/D:/Projects/ChemWorld/configs/benchmark/g2_autonomous_electrochemical_material_3x3_v0.1_dev.json)
- [tri-arm Codex runner](/D:/Projects/ChemWorld/scripts/run_g2_autonomous_material_triarm.py)

runner 支持：

- 15-cell 全量执行（5 seeds × 3 arms）；
- 按 seed mod 3 counterbalance 三臂顺序；
- 每个 cell 独立记录 trajectory、provider receipts、campaign ledger、exact replay；
- 三臂 world identity/public contract 审计；
- 完成真实 cell 后自动汇总 paired score、incumbent AUC、first/late solvent、错配恢复和生命周期/replay 门槛；
- `--world-seeds 0` 形式的分阶段 smoke，避免一次消耗全部 provider quota。
- `--resume` 只接受经过 config、trajectory、resource-ledger、provider receipt 和 exact replay 校验的连续 cell prefix。

不调用 provider 的 15-cell dry-run 已通过：5 个 world audit 全部通过；单 seed dry-run 也通过（3 cells、12 planned physical experiments）。

真实 Codex provider 当前因账户级 quota 暂不可用；恢复后建议顺序：

1. `--world-seeds 0` 跑一个完整三臂 K4 smoke；
2. 检查 provider session、账本、生命周期和 exact replay；
3. 再扩展到 seeds `0,1,2`；
4. 资源允许时完成 5-seed 全量。

Calibration-agent 的结果只用于冻结资源/评价协议，不直接作为 Codex scientific-performance 结论。

## 6. 证据索引

- [lean-k4 5-seed result](/D:/Projects/ChemWorld/runs/development/g2-triarm-resource-design-final-lean-k4-v1/resource_design_summary.json)
- [diagnostic-k6 3-seed result](/D:/Projects/ChemWorld/runs/development/g2-triarm-resource-design-screen-diagnostic-k6-v1/resource_design_summary.json)
- [adaptive-k6 ledger smoke](/D:/Projects/ChemWorld/runs/development/g2-triarm-resource-design-smoke-adaptive-k6-v1/resource_design_summary.json)
- [diagnostic-k8 ledger smoke](/D:/Projects/ChemWorld/runs/development/g2-triarm-resource-design-smoke-diagnostic-k8-v1/resource_design_summary.json)
- [rich-control ledger smoke](/D:/Projects/ChemWorld/runs/development/g2-triarm-resource-design-smoke-rich-k6-v1/resource_design_summary.json)
- [tri-arm 15-cell dry-run](/D:/Projects/ChemWorld/runs/development/g2-autonomous-electrochemical-material-3x3-dry-run-final-v1.json)
