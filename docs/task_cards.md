# 任务卡

任务卡是 ChemWorld benchmark 的发布合同。它必须与 `src/chemworld/tasks.py`
中的 registry 保持一致。若任务的 action space、budget、metrics、maturity、
hidden scenario policy 或 scoring contract 改变，应视为 benchmark contract 变更。

当前预发布阶段只冻结三个核心任务。其它已注册任务仍可用于研发、教学或扩展实验，但不作为
pre-release benchmark claim 的主依据。

## 预发布核心任务

| Task ID | 作用 | Split | Budget | Seeds | Episode | Threshold | Maturity |
| --- | --- | --- | ---: | --- | --- | ---: | --- |
| `reaction-to-assay` | 从投料到 final assay 的最小合法闭环 | `public-dev` | 18 | `0` | `single_experiment` | 0.55 | `lite` |
| `reaction-to-purification` | 反应、萃取/相分离、纯化、最终检测 | `public-test` | 90 | `0,1,2,3,4` | `single_experiment` | 0.70 | `proxy` |
| `partition-discovery` | 学习未知溶剂/萃取体系的分配规律 | `public-test` | 48 | `0,1,2` | `campaign` | 0.60 | `lite` |

## 合同哈希

这些 hash 由 `TaskSpec.contract_hash` 生成，用于 replay、dataset、submission 和 release
artifact 审计。

| Task ID | Contract Hash |
| --- | --- |
| `reaction-to-assay` | `1da420e2636c9eeeed286efb34be3cfdd3c0ba9441d6080bbde36dc0d47761c5` |
| `reaction-to-purification` | `b13ea85f8e00bb5a14ce253e8e7ee5ca76c216dd47bc7413e07ae03d6c47da57` |
| `partition-discovery` | `50b342f6fd2582d7f27b79e793b8aecca6e1c2b131a7225cdfdbc0f4cb2cf3b9` |

## `reaction-to-assay`

目标：验证 agent 能完成一次最小合法实验，从加料、反应、终止到 final assay。

允许操作：

`add_reagent`, `add_solvent`, `add_catalyst`, `heat`, `wait`, `sample`, `quench`,
`terminate`, `measure`

允许仪器：

`hplc`, `gc`, `uvvis`, `final_assay`

成功指标：

- `final_assay_score`
- `trajectory_validity`

预期定性行为：

- final assay 必须在终止后才是合法的最终检测；
- 没有足够物料、体积或终止状态时，相关动作应触发 precondition failure；
- 该任务主要测试 event sequence 合法性，不作为复杂优化主榜。

## `reaction-to-purification`

目标：执行反应后处理，完成萃取、相分离、洗涤/干燥/浓缩，并通过 final assay 评价纯度和回收率。

允许操作：

`add_reagent`, `add_solvent`, `add_catalyst`, `heat`, `wait`, `sample`, `quench`,
`terminate`, `measure`, `add_phase`, `add_extractant`, `mix`, `settle`,
`separate_phase`, `wash`, `dry`, `concentrate`, `transfer`

明确不允许：

`seed_crystals`, `cool_crystallize`, `filter_crystals`, `evaporate`, `distill`,
`collect_fraction`, `set_flow_rate`, `run_flow`, `set_potential`, `electrolyze`

成功指标：

- `score`
- `purity`
- `recovery`
- `process_mass_balance_error`

预期定性行为：

- 反应质量决定纯化上限；
- 相分配会在纯度和回收率之间形成权衡；
- wash 和 concentrate 可以提高纯度，但会增加损失、成本或风险；
- 高 score 不应只来自反应产率，必须通过 downstream process 保持质量。

## `partition-discovery`

目标：在有限预算内学习未知产品在水相/有机相之间的分配规律。

允许操作：

`add_solvent`, `add_reagent`, `add_phase`, `add_extractant`, `mix`, `settle`,
`separate_phase`, `measure`, `terminate`

成功指标：

- `phase_ratio`
- `product_in_organic`
- `product_in_aqueous`

预期定性行为：

- extractant 和 solvent choices 控制产品分配；
- settle 时间和 entrainment 会影响相选择与有效回收；
- 相接触使用活度修正 extraction train，内禀分配系数仍是 benchmark 校准参数；
- agent 应通过少量测量形成局部分配模型，而不是只追求单次 final assay score。

## 发布规则

- pre-release benchmark 只引用上面三个任务。
- 任务合同版本：`chemworld-task-contract-0.3`。
- 每个 task card 必须暴露 `task_contract_hash`、`kernel_maturity`、`physics_maturity`
  和 `proxy_allowed`。
- `reaction-to-purification` 仍含 dry/concentrate/transfer proxy；`partition-discovery`
  的相接触已升级为 `professional_candidate`，但任务整体仍受 `lite` 反应/仪器层约束。
- 任何合同字段变更都需要更新测试、文档和 release artifact。

## Baseline 行

每张任务卡至少需要记录：

- random baseline；
- legal-random baseline；
- fixed/scripted recipe baseline；
- simple optimizer baseline；
- 可选 tool-agent baseline。

官方 baseline 的运行方式、适用任务和解释边界见[Baseline 参考](baseline_reference.md)。
