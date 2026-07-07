# Year 1-2 完成度报告

更新日期：2026-07-08

本文记录 ChemWorld 当前已经完成的 Year 1-2 能力边界。这里的“完成”指代码、测试、文档入口和最小可运行演示已经闭环；不等于真实化学预测软件，也不等于最终 1.0 版本。

要求-证据级验收见 [Year 1-2 验收审计](year1_year2_acceptance_audit.md)。

## Year 1：Benchmark 底座冻结

当前已经具备以下科研 benchmark 底座：

- 统一 Gymnasium 入口：`gym.make("ChemWorld", task_id=..., seed=...)`。
- 统一 `WorldLawSpec`：所有内置 task 共享 `world_law_id = chemworld-physical-chemistry`。
- 任务注册：`TaskSpec` 覆盖 scenario、budget、episode mode、allowed operations、allowed instruments、success metrics 和 safety limit。
- 场景注册：`ScenarioSpec` 记录 split、hidden seed、initial-state seed、parameter profile 和定性行为。
- 三层日志：campaign / experiment / operation 已写入 trajectory JSONL。
- schema：action、recipe、trajectory、manifest、task、scenario 都有运行时 schema 和静态 JSON schema。
- validator：统一执行 schema validation、task policy、instrument policy、constitution preconditions 和 payload bounds。
- 仪器合同：HPLC、GC、UV-vis、FinalAssay 都有 observable keys、noise、cost、sample consumption 和 raw signal。
- safety/cost channel：`info["cost"]`、`info["cost_components"]`、`constraint_budget_remaining` 进入评测信息。
- dataset layer：支持 JSONL/Parquet 导出和 dataset card。
- baseline report：`chemworld baselines report` 可以按 task/agent/seed 生成基线结果、leaderboard 和元数据。
- signed private-eval artifact：`chemworld private-eval sign` 用 maintainer salt 对结果签名，只发布 salt hash 和 HMAC。
- paper artifact：`chemworld artifact create` 生成 task cards、scenario cards、schema snapshot、baseline report、dataset example 和复现实验脚本。
- 本机评测机：教师端/学生端模拟、submission inbox、validate、verify、evaluate、leaderboard export 已有结构。
- 教程体系：12 天 notebook + Day 13 Year 2 process modules + project leaderboard blueprint 已形成课程路径。

## Year 2：同一世界下的物理过程扩展

当前新增的 Year 2 过程不是独立小游戏，而是挂在同一 `ChemWorld` 下的 world law modules：

| 模块 | 操作 | 主要观测指标 |
| --- | --- | --- |
| Crystallization | `seed_crystals`, `cool_crystallize`, `filter_crystals` | `crystal_yield`, `crystal_purity`, `crystal_size` |
| Distillation | `evaporate`, `distill`, `collect_fraction` | `distillate_purity`, `distillate_recovery`, `solvent_loss` |
| Continuous Flow | `set_flow_rate`, `run_flow` | `flow_conversion`, `yield`, `safety_risk` |
| Electrochemistry | `set_potential`, `electrolyze` | `electrochemical_selectivity`, `energy_efficiency`, `yield` |

这些模块已经进入：

- `world_law_spec().transition_kernel_registry`
- `world_law_spec().ontology_registry["modules"]`
- `operation_contracts()`
- `ActionCodec` 和 Gym action space
- `OperationValidator`
- `PhysicalConstitution.check_preconditions`
- `InstrumentContract`
- `ChemWorldObservationKernel`
- `eval.metrics`

## 新增任务切片

新增 task 仍然使用同一个 `env_id=ChemWorld`：

- `reaction-to-crystallization`
- `reaction-to-distillation`
- `flow-reaction-optimization`
- `electrochemical-conversion`

原有任务继续存在：

- `reaction-optimization-standard`
- `reaction-safety-constrained`
- `reaction-mechanism-explanation`
- `reaction-to-assay`
- `reaction-to-purification`
- `partition-discovery`
- `purity-yield-tradeoff`
- `public-private-generalization`
- `low-budget-characterization`
- `tool-agent-planning`

## 已验证能力

新增测试覆盖：

- 所有 task 共享同一 `world_law_id`。
- Year 2 process modules 出现在 `WorldLawSpec`。
- 新 task 可以实例化并 reset/step。
- `filter_crystals`、`collect_fraction`、`run_flow`、`electrolyze` 有状态依赖前置条件。
- scripted baseline 能完成 crystallization、distillation、flow 和 electrochemistry 的最小闭环。
- final assay 可观测 Year 2 过程指标。
- evaluation metrics 聚合 crystal、distillate、flow 和 electrochemical 指标。
- 静态 JSON schema 与运行时 schema 保持一致。

## 当前边界

这些内容属于正式发布前的全量运行、Year 2 后半段或 Year 3，不应在当前版本中过度宣称：

- `chemworld.world` 已接管 ontology、parameter generation、instrument registry、operation registry、recipe compiler、reaction ODE、thermal risk、phase partition、downstream truth、observation helper 和 scoring helper；`core/batch_reactor.py` 当前只保留事件调度、ledger 写入和少量过程 proxy 编排。
- Crystallization、distillation、flow、电化学仍是定性半机理 proxy，不是真实单元操作模拟器。
- private eval 当前是本机 hidden salt + signed artifact 模式，不是远端托管评测服务。
- official baseline table 生成器已经完成；正式 release 前需要用完整 task/agent/seed 矩阵重新运行并冻结结果。
- Year 2 教程已有 Day 13 总览；正式课程版仍可继续拆成 3-5 个更细 notebook。

## 快速验收命令

```bash
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy src\chemworld
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m mkdocs build --strict
```
