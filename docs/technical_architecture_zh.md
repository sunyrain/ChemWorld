# ChemWorld-Bench 技术架构总览

本文档描述当前 `main` 分支的主线架构。它不记录临时迁移细节，而是回答三个问题：

- ChemWorld 现在是什么？
- 它如何把化学实验动作、物理模型、观测、评分和回放组织成一个 benchmark？
- 距离更成熟的 chemical world model 交互环境还缺什么？

## 1. 平台定位

ChemWorld-Bench 是一个面向智能体交互训练、科研评测和课程扩展的虚拟物理化学世界。它不是一个真实反应预测软件，也不是一组彼此独立的小游戏，而是一个统一的 Gymnasium 环境：

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=1)
obs, info = env.reset(seed=1)
```

`ChemWorld` 是统一世界入口，`task_id` 是同一套物理化学规则下的任务切片。不同任务共享 ontology、physical constitution、operation language、instrument contracts、transaction runtime、trajectory schema、dataset schema 和评测协议。

当前平台的合理表述是：

> ChemWorld-Bench 是一个机制驱动、事务化、可回放的虚拟化学实验交互环境，用于研究 agent 如何在有限预算、部分可观测、有成本和安全约束的物理化学世界中进行实验决策、局部 world model 学习和多目标优化。

## 2. 总体分层

```text
src/chemworld
├── envs            # Gymnasium 环境适配层，正式入口是 ChemWorld
├── runtime         # Runtime v2: kernel registry, domain services, transaction
├── foundation      # ontology, physical constitution, typed ledgers
├── world           # scenario, operations, instruments, scoring, kernels
├── physchem        # 独立实现的物理化学/化工模型库
├── tasks           # benchmark task registry
├── agents          # baseline agents
├── eval            # evaluation, replay verify, leaderboard, artifacts
├── data            # trajectory, submission, dataset export
└── schemas         # action, recipe, trajectory, manifest, task, scenario, mechanism
```

核心原则是：Gym 层保持薄，物理和实验动作由 Runtime v2 与 domain services 执行；任务差异由 `TaskSpec`、`ScenarioSpec`、机制文件、评分合同和观测合同声明。

## 3. 世界概念层级

ChemWorld 明确区分以下层级：

```text
WorldLaw   -> 共享物理化学规则
Scenario   -> hidden parameters + initial state + mechanism
Task       -> budget/objective/allowed operations/instruments/metrics
Campaign   -> agent 在某个 task/seed 下的一次完整评测
Experiment -> campaign 内的一次实验
Operation  -> 单步实验动作
```

这意味着任务不是独立小游戏，而是同一世界规律的不同切片。例如反应优化、反应到纯化、分配规律发现、结晶、蒸馏、连续流和电化学任务都运行在同一个 `ChemWorld` 入口下，只是初始状态、允许操作、仪器权限、预算、评分目标和终止条件不同。

## 4. Runtime v2

Runtime v2 是当前执行中心：

```text
ChemWorldEnv
  -> ChemWorldRuntime
      -> ActionValidator
      -> TaskRuntimeProfile
      -> OperationKernelRegistry
      -> DomainServiceRegistry
      -> TransactionManager
      -> ConstitutionChecker
      -> ObservationKernel
      -> ScoringService
      -> OperationRecorder
```

`ChemWorldEnv.step()` 只做 Gym 编排：action canonicalize、schema/task/payload validation、runtime dispatch、observation、reward/info、campaign bookkeeping。真正改变世界状态的是 Runtime v2。

Runtime v2 的关键设计包括：

- `TaskRuntimeProfile` 声明当前任务需要哪些 operation、instrument、kernel、domain service 和 capability。
- `OperationKernelRegistry` 把 operation type 映射到小型 command handler。
- `DomainServiceRegistry` 声明当前 runtime 可用的物理服务，以及 operation 到 service 的映射。
- domain-service validation 是 task-scoped 的：只做反应任务时，不要求注册蒸馏、电化学、结晶等无关服务。
- operation kernel 不直接实现大段物理模型，而是调用 domain services。
- kernel 返回 `WorldEvent` 和 `StatePatch`，不任意返回完整新 state。
- `TransactionManager` 统一提交 patch，执行 constitution checks，失败时 rollback。
- safety/cost 是一等信号，进入 `info["cost"]`、`info["cost_components"]`、constraint flags、trajectory 和 leaderboard metrics。

失败路径分为两类：

- schema、task-policy、instrument-policy、payload-shape 或 payload-bound 错误在 env 层被拒绝，记录为 `validation_failed`。
- stateful physical precondition failure 进入 Runtime v2，记录 `operation_rejected` 和 `transaction_rollback`，只提交 process-ledger penalty patch，不改变 material、phase、vessel 或 equipment ledger。

## 5. Domain Services

当前 runtime 已经把大部分物理过程拆成 focused services：

| Service | 主要职责 |
| --- | --- |
| primitive services | 投料、加溶剂、加催化剂、取样、淬灭、蒸发、非法动作惩罚 |
| reaction/thermal services | ODE 反应推进、加热/等待、热账本、压力和风险投影 |
| phase/separation services | 相账本、萃取、混合、静置、分相、洗涤、干燥、浓缩、转移 |
| crystallization services | 加晶种、冷却结晶、固相/母液相输出、过滤 |
| distillation services | shortcut VLE 蒸馏、馏出相/釜残相输出、热负荷、收集馏分 |
| flow services | 流量设置、停留时间反应推进、连续流转化率和通量指标 |
| electrochemical services | 电位/电流设置、Nernst/Butler-Volmer 转化、电功和法拉第指标 |
| instrument-cost services | 测量成本、破坏性取样、final-assay 仪器状态 |
| observation services | raw signal、processed estimate、uncertainty 和观测时评分 |
| record services | operation record、constitution summary、state delta 和 replay metadata |

这些 service 仍然处于不同成熟度：部分已经是 lite/reference-validated，部分仍是明确标记的 proxy。平台要求 proxy 不能伪装成 professional kernel，任务和报告必须暴露 maturity metadata。

## 6. Mechanism Compiler

机制文件不在每一步 runtime 中直接读取，而是在 reset/scenario 初始化时编译为 `CompiledMechanism`。机制文件采用版本化 YAML schema，目前主版本为 `chemworld_mechanism_v1`。

`CompiledMechanism` 包含：

- `mechanism_id`
- `mechanism_version`
- `mechanism_hash`
- `species_index`
- `stoichiometric_matrix`
- `reaction_enthalpies`
- `species_roles`
- `observable_mapping`
- `score_spec`
- `initial_amount_policy`
- `manifest`

`manifest` 包含 validation report、rate-law families、score spec 和 initial amount policy。`task_info()` 会暴露 `mechanism_manifest`，trajectory 和 verifier 会记录 `mechanism_id` 与 `mechanism_hash`。如果 mechanism 文件变化，replay verifier 会明确失败，而不是悄悄比较语义不同的轨迹。

评分和观测协议也进入合同层：

- `TaskSpec.contract_hash` 锁定任务边界。
- `TaskRuntimeProfile.profile_hash` 锁定 runtime profile。
- `TaskScoringContract.contract_hash` 锁定评分规则。
- `TaskObservationContract.contract_hash` 锁定可见观测口径。

运行时已经不再依赖固定 `A/P/B/D/E` 五物种网络。`A/P/B/D/E` 只应出现在具体 mechanism fixture 或显式 reference case 中，不应成为通用 runtime、observation、scoring 或 phase bookkeeping 的隐含前提。

## 7. Typed Ledgers

`WorldState` 已经升级为 typed ledger 结构：

| Ledger | 作用 |
| --- | --- |
| `SpeciesLedger` | 物种定义、角色和初始投料策略 |
| `PhaseLedger` | 各相中的 species amount，是 material state 的主要事实源 |
| `VesselLedger` | 容器体积、温度、压力和相归属 |
| `EquipmentLedger` | 反应器、结晶器、电化学池、流动装置和仪器状态 |
| `ThermalLedger` | 按 vessel 记录夹套热、反应热和热损失 |
| `ProcessLedger` | 时间、成本、风险、样品消耗、废液和过程指标 |

当前 `ProcessLedger.metrics` 已经承接下游分离、结晶、蒸馏、连续流和电化学等过程派生指标，例如 purity、recovery、crystal yield/purity/size、distillate purity/recovery、flow conversion、flow throughput、faradaic efficiency、energy efficiency、overpotential、charge 和 electrical work。constitution 会拒绝把这些 primary/derived process metrics 放回 `metadata`，避免 `metadata` 重新变成隐藏状态垃圾箱。

仍需注意：快速迭代期内还保留少量 scalar adapter，用于稳定旧轨迹、notebook 和测试路径。长期目标是让 phase/vessel/equipment/process ledgers 成为唯一结构化状态源。

## 8. Operation Language

统一实验动作格式为：

```python
{"operation": "heat", "target_temperature_K": 360.0, "duration_s": 900.0}
```

操作分为三类：

- primitive operation：`add_reagent`、`add_solvent`、`add_catalyst`、`heat`、`wait`、`sample`、`measure`、`terminate`、`transfer`。
- domain operation：`distill`、`electrolyze`、`run_flow`、`cool_crystallize`。
- macro recipe：`wash`、`dry`、`concentrate` 等，可编译为 primitive/domain operation sequence。

macro 不允许绕过 primitive preconditions。Recipe compiler 输出可审计的 operation sequence，再由同一套 validator、runtime 和 transaction manager 执行。

## 9. Observation 与仪器

观测采用三层结构：

- `raw_signal`：HPLC、GC、UV-vis、IR、NMR proxy、final assay packet 等原始信号。
- `processed_estimate`：由仪器信号估计出的 yield、selectivity、conversion、purity、recovery 等。
- `uncertainty`：观测噪声、检测限、峰重叠、校准不确定性等。

agent 默认不能直接读取 hidden species amount、rate constants、partition coefficients 或 mechanism parameters。观测必须通过 instrument contract 生成，并消耗成本、时间或样品。

当前 observation kernel 读取 task-specific observation contract：反应任务只暴露反应诊断；纯化、分配、结晶、蒸馏、连续流和电化学任务只额外暴露各自评分需要的观测键。raw signal 也只使用 task-visible 的公开角色聚合量，不把 full hidden species ledger 或机制内部物种名直接交给 agent。

当前已有 HPLC、GC、UV-vis、final assay，以及 IR/NMR 风格的紧凑谱图信号。`final_assay` 是主要 leaderboard scoring source。

## 10. Benchmark 闭环

ChemWorld-Bench 的评测闭环如下：

1. agent 或学生在本地 Gym 环境中执行有限预算实验。
2. 每个 operation 产生 observation、reward、cost、risk、constraint flags 和 transaction metadata。
3. trajectory JSONL 记录 action、observation、info、task/profile contract hash、mechanism hash、scoring/observation contract hash、world events、state patches 和 rollback reason。
4. verifier 使用 task、scenario、mechanism hash、seed 和 action sequence 重放轨迹。
5. evaluator 计算 task-specific metrics、sample efficiency、安全成本、public/private gap 和 leaderboard summary。
6. submission bundle 包含 manifest、trajectories、results 和可选 explanations。
7. dataset export 可生成 JSONL/Parquet 分析数据和 dataset card。

当前 dataset card 已经记录 schema version、trajectory schema versions、task/runtime/mechanism/scoring/observation protocol hashes、replay verification summary、agent manifests 和 privacy/anonymization summary。这让离线分析、课程日志、baseline report 和后续 private eval 更容易审计。

## 11. 本机教师端/学生端评测组织

当前推荐的本机评测机组织是：

```text
local_eval_server/
  teacher_server/
    tasks/
    private_salt.env
    grading_scripts/
    leaderboard/
    submissions_inbox/
  student_sandboxes/
    student_001/
    student_002/
  shared_specs/
    task_cards/
    action_schema/
    recipe_schema/
```

学生端只获得 public task cards、schema、SDK 和示例 notebook。教师端持有 private salt、hidden seeds、最终评测脚本和 leaderboard 生成流程。学生提交 submission bundle 后，由教师端统一执行：

```text
validate -> verify -> evaluate -> summarize -> leaderboard review
```

这不是云端防作弊系统，但已经足够支持课程、pilot study 和本机模拟 Docker 的 benchmark 工作流。

## 12. 当前核心能力

当前平台可以支持：

- 多步自定义实验：投料、加溶剂、加催化剂、加热、等待、取样、终止、测量。
- 反应后处理：萃取、混合、静置、分相、洗涤、干燥、浓缩、final assay。
- 专题任务：reaction optimization、purification、partition discovery、crystallization、distillation、continuous flow、electrochemical conversion。
- 机制驱动任务：从 mechanism YAML 编译物种、反应网络、角色、观测映射和评分绑定。
- 可重复评测：固定 task、scenario、seed、agent、commit 和 mechanism hash 后可回放。
- 安全/成本通道：高温、高风险、测量成本、前置条件失败、constitution failure 进入 cost channel。
- baseline agents：random、LHS、greedy、BO、safe BO、scripted chemistry、LLM replay/stub。
- 数据与提交：trajectory JSONL、submission bundle、dataset export、dataset card、匿名化样例。
- 文档和教程：体系结构、任务、操作、仪器、dataset、benchmark protocol、课程 notebooks。

## 13. 当前主要差距

距离理想的 chemical world model 交互环境，仍有几个关键差距：

- 物理模型深度：distillation、crystallization、flow、electrochemistry、phase equilibrium、safety 还需要更严格的机理模型和验证矩阵。
- 状态账本一致性：typed ledgers 已经覆盖主路径，但仍需继续移除 scalar adapter 和残留 metadata 派生状态。
- 机制驱动广度：score、processed observation 和 raw signal 已有 task-level contract；下一步要把仪器校准、谱峰归属、检测限、方法条件和物种性质进一步绑定到 mechanism/species/instrument card。
- scenario 生成：需要更丰富的 hidden parameter family、initial-state family、difficulty ladder 和 public/private generalization audit。
- benchmark 难度：需要更多 hidden scenarios、多机制 families、强 baseline calibration 和 private-eval 工作流。
- 数据层成熟度：dataset card、trajectory schema、submission protocol 已有基础，但还需要更接近 Minari 风格的数据版本治理和离线学习任务。
- agent 生态：LLM adapter 和 replay/stub 已有，但还缺真正 tool-using chemical agent baseline、planner memory、实验假设日志和解释评分闭环。

## 14. 总结

ChemWorld 当前已经具备“统一物理化学世界 + 机制驱动 runtime + typed ledgers + 事务化实验执行 + 可回放 benchmark 协议”的主体框架。下一阶段的重点不是继续堆更多 proxy 任务，而是让每个任务都由更强的物理模型、机制编译、仪器模型、scenario generator、dataset protocol 和 baseline calibration 真正驱动。
