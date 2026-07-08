# ChemWorld-Bench 技术架构总览

本文档描述当前 `main` 分支的整体架构。它不记录临时迁移细节，只说明目前已经稳定的主线设计、能够完成的核心功能，以及下一阶段还需要加强的方向。

## 1. 定位

ChemWorld-Bench 是一个面向智能体交互训练和科研评测的虚拟物理化学世界。它不是一个真实反应预测软件，也不是一组彼此独立的小游戏，而是一个统一的 Gymnasium 环境：

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=1)
```

`ChemWorld` 是统一世界，`task_id` 是同一套物理化学规则下的任务切片。不同任务共享 ontology、physical constitution、operation language、instrument contracts、transaction runtime、trajectory schema 和评测协议。

## 2. 包结构

```text
src/chemworld
├── envs            # Gymnasium 环境适配层，正式入口是 ChemWorld
├── runtime         # Runtime v2: kernel registry, domain services, transaction
├── foundation      # ontology, physical constitution, typed ledgers
├── world           # scenario, operations, instruments, scoring, kernels
├── physchem        # 独立实现的物理化学/化工模型库
├── tasks           # benchmark task registry
├── agents          # baseline agents
├── eval            # evaluation, replay verify, leaderboard, artifact
├── data            # trajectory, submission, dataset export
└── schemas         # action, recipe, trajectory, manifest, task, scenario, mechanism
```

当前核心原则是：Gym 层保持薄，物理和实验动作由 Runtime v2 与 domain services 执行；任务差异由 `TaskSpec`、`ScenarioSpec` 和机制文件声明。

## 3. 世界分层

ChemWorld 正式区分六层：

```text
WorldLaw   -> 共享物理化学规则
Scenario   -> hidden parameters + initial state + mechanism
Task       -> budget/objective/allowed operations/instruments/metrics
Campaign   -> agent 在某个 task/seed 下的一次评测
Experiment -> campaign 内的一次实验
Operation  -> 单步实验动作
```

在 campaign task 中，`final_assay` 结束当前 experiment，但不一定结束整个 campaign；在 single-experiment task 中，`final_assay` 会终止 episode。

## 4. Runtime v2

Runtime v2 的当前主干是：

```text
ChemWorldEnv
  -> ChemWorldRuntime
      -> TaskRuntimeProfile
      -> OperationKernelRegistry
      -> DomainServiceRegistry
      -> ChemWorldDomainServices
      -> TransactionManager
      -> ConstitutionChecker
      -> ObservationServices
      -> ScoringService
      -> OperationRecordServices
```

`ChemWorldEnv.step()` 只负责 Gym 编排：action canonicalize、schema/task/payload validation、runtime dispatch、observation、reward/info、campaign bookkeeping。真正的实验状态更新由 Runtime v2 执行。

Runtime v2 的关键设计包括：

- `TaskRuntimeProfile` 声明当前任务需要哪些 operation、instrument、kernel、domain service 和 capability。
- `OperationKernelRegistry` 将 operation type 映射到小型 command handler。
- `DomainServiceRegistry` 提供 JSON-friendly 的 service contract 和 operation-to-service map。
- domain-service validation 是 task-scoped 的：一个只做反应测定的任务不需要注册萃取、蒸馏、电化学等无关服务。
- `TransactionManager` 统一提交 `StatePatch`、记录 `WorldEvent`，并在 constitution failure 或 stateful precondition failure 时回滚 material ledger。
- safety/cost 是一等信号，会进入 `info["cost"]`、`info["cost_components"]`、constraint flags 和 leaderboard metrics。

失败路径分为两类：

- schema、task-policy、instrument-policy、payload-shape 或 payload-bound 错误在 env 层被拒绝，记录为 `validation_failed`。
- stateful physical precondition failure 进入 Runtime v2，记录 `operation_rejected` 和 `transaction_rollback`，只提交 process-ledger penalty patch，不改变 material、phase、vessel 或 equipment ledger。

## 5. Mechanism Compiler

机制文件不在每一步 runtime 中直接读取，而是在 reset/scenario 初始化时编译为 `CompiledMechanism`。机制文件采用版本化 YAML schema，目前版本为 `chemworld_mechanism_v1`。

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

`manifest` 内含 validation report、rate-law families、score spec 和 initial amount policy。`task_info()` 会暴露 `mechanism_manifest`，trajectory 和 verifier 会记录 `mechanism_id` 与 `mechanism_hash`。如果 mechanism 文件发生变化，replay verifier 应失败，而不是悄悄比较不同隐藏世界产生的轨迹。

运行时已经不再依赖固定五物种网络。`A/P/B/D/E` 只应出现在具体 mechanism fixture 或显式 reference code 中，不应成为通用 runtime、observation、scoring 或 phase bookkeeping 的隐含前提。

## 6. Typed Ledgers

`WorldState` 已经升级为 typed ledger 结构：

- `SpeciesLedger`：物种角色和初始投料策略。
- `PhaseLedger`：各相中的 species amount，是 material state 的主要账本。
- `VesselLedger`：容器体积、温度、压力和相归属。
- `EquipmentLedger`：反应器、结晶器、电化学池、流动装置、仪器状态等设备记录。
- `ThermalLedger`：按 vessel 记录夹套热、反应热和热损失。
- `ProcessLedger`：时间、成本、风险、样品消耗和废液。

当前仍保留一层 scalar state adapter，用于快速迭代期间维持部分轨迹、notebook 和测试稳定。长期目标是让 phase/vessel/equipment ledger 成为唯一结构化状态源。

## 7. Operation Language

统一实验动作格式为：

```python
{"operation": "heat", "target_temperature_K": 360.0, "duration_s": 900.0}
```

operation 分为三类：

- primitive operation：如 `add_reagent`、`add_solvent`、`heat`、`wait`、`sample`、`measure`、`terminate`。
- domain operation：如 `distill`、`electrolyze`、`run_flow`、`cool_crystallize`。
- macro recipe：如 `wash`、`dry`、`concentrate`，可编译为 primitive/domain operation sequence。

macro 不允许绕过 primitive preconditions。Recipe compiler 输出可审计的 operation sequence，再由同一套 validator 和 runtime 执行。

## 8. Observation 与仪器

观测采用三层结构：

- `raw_signal`：HPLC、GC、UV-vis、IR、final assay packet 等原始信号。
- `processed_estimate`：由仪器信号估计出的 yield、selectivity、purity、recovery 等。
- `uncertainty`：观测噪声、检测限、峰重叠、校准不确定性等。

agent 默认不能直接读取 hidden species amount、rate constants、partition coefficients 或 mechanism parameters。观测必须通过 instrument contract 生成，并消耗成本、时间或样品。

当前已经具备 HPLC、GC、UV-vis、final assay，以及 IR functional-group band slice。`final_assay` 是主要 leaderboard scoring source。

## 9. Benchmark 闭环

ChemWorld-Bench 的评测闭环包括：

1. agent 或学生在本地 Gym 环境中执行有限预算实验。
2. 每个 operation 产生 observation、reward、cost、risk、constraint flags 和 transaction metadata。
3. trajectory JSONL 记录 action、observation、info、mechanism hash、world events、state patches 和 rollback reason。
4. verifier 使用 task、scenario、mechanism hash、seed 和 action sequence 重放轨迹。
5. evaluator 计算 task-specific metrics、sample efficiency、安全成本、public/private gap 和 leaderboard summary。
6. submission bundle 包含 manifest、trajectories、results 和可选 explanations。

当前 verifier 已经会比对 Runtime v2 transaction metadata，包括 kernel id/version、domain service id、affected ledgers、world events、state patch summaries、transaction status、rollback reason 和 state-delta summaries。

## 10. 当前核心能力

当前平台可以支持：

- 多步实验：投料、加溶剂、加催化剂、加热、等待、终止、测量。
- 后处理流程：萃取、混合、静置、分相、洗涤、干燥、浓缩、final assay。
- 专题任务：distillation、continuous flow、crystallization、electrochemical conversion。
- 可重复评测：固定 config、task、scenario、seed、agent、commit 后可回放。
- 安全/成本信号：高温、高风险、测量成本、前置条件失败、constitution failure 进入 cost channel。
- agent baselines：random、LHS、greedy、BO、safe BO、scripted chemistry、LLM replay/stub。
- 数据导出：JSONL、submission bundle、dataset export、匿名化样例。
- 本机教师端/学生端评测组织：学生提交 bundle，教师端 validate、verify、evaluate、summarize。

## 11. 当前主要差距

距离理想的 chemical world model 交互环境，仍有几个关键差距：

- 物理模型深度：distillation、crystallization、flow、electrochemistry、phase equilibrium、safety 还需要更严格的机理模型和验证矩阵。
- 状态账本一致性：typed ledgers 已经存在，但 scalar adapter 仍在过渡期。
- 机制驱动广度：observation、score、instrument mapping 还需要进一步完全由 mechanism/task spec 驱动。
- benchmark 难度：需要更多 hidden scenarios、多机制 families、private-eval seeds、强 baseline calibration 和 public/private generalization audit。
- 数据层成熟度：dataset card、trajectory schema、submission protocol 已有雏形，但还需要更接近 Minari 风格的数据版本治理和离线学习任务。
- agent 生态：LLM adapter 和 replay/stub 已有，但还缺真正 tool-using chemical agent baseline、planner memory、实验假设日志和解释评分闭环。

## 12. 总结

ChemWorld 当前已经具备“统一物理化学世界 + 事务化实验运行时 + 可回放 benchmark 协议”的主体框架。下一阶段的重点不是继续堆更多 proxy 任务，而是让每个任务都由更强的 typed ledger、mechanism compiler、instrument model、physics service 和 evaluation contract 真正驱动。
