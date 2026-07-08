# ChemWorld-Bench 技术架构总览

更新日期：2026-07-09

## 1. 平台定位

ChemWorld-Bench 是一个面向 AI4Science、化工教育和闭环实验决策研究的虚拟物理化学交互环境。它的目标不是预测某个真实实验体系，也不是把许多互不相关的小游戏拼在一起，而是在同一套物理化学世界规则下，为学生、LLM agent、贝叶斯优化器、强化学习 agent 和人机协作系统提供可交互、可复现、可提交、可验证、可评测的实验任务。

正式 Gymnasium 入口统一为：

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-optimization-standard", seed=0)
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(action)
```

这里的 `ChemWorld` 是一个统一世界环境，`task_id` 只是世界中的任务切片。不同任务共享 ontology、physical constitution、operation language、instrument contracts、runtime transaction、trajectory schema 和评测协议。

## 2. 总体分层

当前代码按职责分为以下层：

```text
chemworld
├── foundation      # ontology, physical constitution, typed state, units
├── world           # scenario, operation, instrument, recipe, world-law modules
├── runtime         # Runtime v2: transaction, kernel registry, domain services
├── envs            # Gymnasium adapter: ChemWorldEnv
├── tasks           # task registry and task cards
├── schemas         # action, recipe, trajectory, manifest, task, scenario schemas
├── agents          # random, LHS, greedy, BO, safe BO, scripted, LLM replay/stub
├── eval            # runner, metrics, verify, suite, leaderboard
├── data            # logging, submission, dataset export, validation, anonymize
├── physchem        # physical-chemistry and chemical-engineering model library
├── wrappers        # action mask, safety/cost, NaN observation wrappers
└── cli             # run, evaluate, verify, tasks, scenarios, datasets, render
```

核心原则是：

- Gym 环境只负责交互协议，不承载化学分支逻辑。
- `foundation` 和 `world` 定义世界规则、状态账本、任务切片和动作语言。
- `runtime` 负责事务化执行实验动作。
- `physchem` 和 runtime domain services 承担具体物理化学计算。
- `eval`、`data` 和 schemas 让每次实验轨迹可复现、可回放、可审计、可比较。

## 3. 单一 WorldLaw

所有正式任务都指向同一套世界规律：

```text
world_law_id = chemworld-physical-chemistry
```

新增任务时不新建独立环境，而是在同一个世界下改变：

- scenario 和初始状态；
- hidden mechanism 和参数；
- 可用 operations 和 instruments；
- 预算、目标函数和安全约束；
- 观测权限和终止策略；
- success metrics 和 leaderboard 配置。

因此，`reaction-optimization-standard`、`reaction-to-purification`、`reaction-to-distillation`、`flow-reaction-optimization`、`electrochemical-conversion` 等任务都是同一个物理化学世界的不同切片，而不是不同小游戏。

## 4. Runtime v2

当前运行时中心是 `chemworld.runtime`：

```text
ChemWorldEnv
  -> ChemWorldRuntime
      -> ActionValidator
      -> OperationKernelRegistry
      -> DomainServiceRegistry
      -> ChemWorldDomainServices
      -> PrimitiveServices
      -> ReactionThermalServices
      -> PhaseSeparationServices
      -> CrystallizationServices
      -> DistillationServices
      -> FlowServices
      -> ElectrochemicalServices
      -> InstrumentCostServices
      -> ObservationServices
      -> OperationRecordServices
      -> TransactionManager
      -> ConstitutionChecker
```

`ChemWorldEnv.step()` 的职责很薄：canonicalize action、做 schema/task/payload validation、调用 runtime、生成 observation、计算 reward/info、维护 campaign bookkeeping。真正的实验动作由 Runtime v2 执行。

Runtime v2 的关键设计包括：

- `TaskRuntimeProfile` 声明当前任务需要哪些 operation、instrument、kernel、domain service 和 capability。
- `OperationKernelRegistry` 把 operation type 映射到小型 command handler。
- `DomainServiceRegistry` 提供 JSON-friendly 的 service contract 和 operation-to-service map，供 `task_info()`、trajectory event、审计和文档使用。
- `ChemWorldDomainServices` 是轻量 operation composition surface，负责编排独立服务、constitution checks 和 operation record assembly。
- `TransactionManager` 统一提交 `StatePatch`，记录 `WorldEvent`，并在 constitution failure 或 stateful precondition failure 时回滚 material ledger。
- safety/cost 是一等信号，会进入 `info["cost"]`、`info["cost_components"]`、constraint flags 和 leaderboard metrics。

当前失败路径已经分成两类：

- schema、task-policy、instrument-policy、payload-shape 或 payload-bound 错误在 env 层被拒绝，记录为 `validation_failed`。
- stateful physical precondition failure 会进入 Runtime v2，记录 `operation_rejected` 和 `transaction_rollback`，只提交 process-ledger penalty patch，不改变 material、phase、vessel 或 equipment ledger。

例如，未 `terminate` 就进行 `final_assay` 不会泄露观测，也不会被当成普通成功动作；它会成为一次可审计的 rollback transaction。

## 5. Mechanism Compiler

机制文件不在每一步 runtime 中直接读取，而是在 reset/scenario 初始化时编译为 `CompiledMechanism`。

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

trajectory 和 verifier 会记录 `mechanism_id` 与 `mechanism_hash`。如果 mechanism 文件发生变化，replay verifier 会失败，而不是悄悄产生漂移结果。

运行时已经不再依赖固定五物种网络。`MechanismSpeciesView` 会从 compiled mechanism 中解析 reactant、target、impurity、catalyst、byproduct 和 degradation marker。旧的 `A/P/B/D/E` 只应出现在具体 mechanism fixture 或显式 reference code 中，不应成为通用 runtime、observation、scoring 或 phase bookkeeping 的隐含前提。

## 6. Typed Ledgers

`WorldState` 已经升级为 typed ledger 结构：

- `SpeciesLedger`：物种角色和初始投料策略。
- `PhaseLedger`：各相中的 species amount，是 material state 的主要账本。
- `VesselLedger`：容器体积、温度、压力和相归属。
- `EquipmentLedger`：反应器、结晶器、电化学池、流动装置、仪器状态等设备记录。
- `ThermalLedger`：按 vessel 记录夹套热、反应热和热损失。
- `ProcessLedger`：时间、成本、风险、样品消耗和废液。

当前仍保留一层 scalar state adapter，用于快速迭代期间维持旧轨迹、notebook 和部分测试稳定。长期目标是让 phase/vessel/equipment ledger 成为唯一结构化状态源，并把 scalar state 限定为观测摘要或报告视图。

## 7. Operation Language

统一实验动作格式为：

```python
{"operation": "heat", "target_temperature_K": 360.0, "duration_s": 900.0}
```

operation 分为三类：

- primitive operation：如 `add_reagent`、`add_solvent`、`heat`、`wait`、`sample`、`measure`、`terminate`。
- domain operation：如 `distill`、`electrolyze`、`run_flow`、`cool_crystallize`。
- macro recipe：如 `wash`、`dry`、`concentrate`，可编译为 primitive/domain operation sequence。

macro 不允许绕过 primitive preconditions。recipe compiler 会输出可审计的 operation sequence，再由同一套 validator 和 runtime 执行。

## 8. Observation 与仪器

观察采用三层结构：

- `raw_signal`：HPLC、GC、UV-vis、IR、final assay packet 等原始信号。
- `processed_estimate`：从仪器信号估计出的 yield、selectivity、purity、recovery 等。
- `uncertainty`：观测噪声、检测限、峰重叠、校准不确定性等。

agent 默认不能直接读取 hidden species amount、rate constants、partition coefficients 或 mechanism parameters。观测必须通过 instrument contract 生成，并消耗成本、时间或样品。

当前已具备：

- HPLC/GC/UV-vis/final assay 的观测协议。
- IR functional-group band slice：根据 formula、species role 和功能团规则生成可解释 IR peaks，并记录宽峰、重叠和干扰 metadata。
- final assay 作为 leaderboard scoring source。

## 9. Task、Scenario、Campaign

平台正式区分：

```text
WorldLaw   -> 共享物理化学规则
Scenario   -> hidden parameters + initial state + mechanism
Task       -> budget/objective/allowed operations/instruments/metrics
Campaign   -> 某 agent 在某 task/seed 下的一次完整评测
Experiment -> campaign 内的一次实验
Operation  -> 单步实验动作
```

在 campaign task 中，`final_assay` 结束当前 experiment，但不一定结束整个 campaign；在 single-experiment task 中，`final_assay` 会终止 episode。

当前任务覆盖：

- 反应条件优化；
- 安全约束优化；
- 机制解释；
- 从投料到 final assay 的完整实验；
- 反应到萃取/纯化；
- 分配规律发现；
- purity/yield/cost tradeoff；
- public/private generalization；
- low-budget characterization；
- flow、distillation、crystallization、electrochemistry 等扩展场景。

## 10. Benchmark 闭环

ChemWorld-Bench 的 benchmark 闭环包括：

1. agent 或学生在本地 Gym 环境中执行有限预算实验。
2. 每个 operation 产生 observation、reward、cost、risk、constraint flags 和 transaction metadata。
3. trajectory JSONL 记录 action、observation、info、mechanism hash、world events、state patches 和 rollback reason。
4. verifier 使用 task、scenario、mechanism hash、seed 和 action sequence 重放轨迹。
5. evaluator 计算 task-specific metrics、sample efficiency、安全成本、public/private gap 和 leaderboard summary。
6. submission bundle 包含 manifest、trajectories、results 和可选 explanations。

当前 verifier 已经会比对 Runtime v2 transaction metadata，包括 kernel id/version、domain service id、affected ledgers、world events、state patch summaries、transaction status、rollback reason 和 state-delta summaries。这让提交者不能只修改 JSONL 中的 reward、score 或观测来伪造结果。

## 11. 当前可以实现的核心能力

当前平台已经可以支持：

- 多步实验：投料、加溶剂、加催化剂、加热、等待、终止、测量。
- 后处理流程：萃取、混合、静置、分相、洗涤、干燥、浓缩、final assay。
- 专题任务：distillation、continuous flow、crystallization、electrochemical conversion。
- 可重复评测：固定 config、task、scenario、seed、agent、commit 后可重放。
- 安全/成本信号：高温、高风险、测量成本、前置条件失败、constitution failure 进入 cost channel。
- agent baselines：random、LHS、greedy、BO、safe BO、scripted chemistry、LLM replay/stub。
- 数据导出：JSONL、submission bundle、dataset export、匿名化样例。
- 本机教师端/学生端评测组织：学生提交 bundle，教师端 validate、verify、evaluate、summarize。

这意味着 ChemWorld 目前已经不只是单个反应优化 demo，而是一个具备统一 world law、任务注册、事务运行时、轨迹审计和 benchmark 协议的科研原型。

## 12. 当前主要差距

距离理想的 chemical world model 交互环境，仍有几个关键差距：

- 物理模型深度：许多模块已有专业化切片，但 distillation、crystallization、flow、electrochemistry、phase equilibrium、safety 仍需要更严格的机理模型和验证矩阵。
- 状态账本一致性：typed ledgers 已经存在，但 scalar adapter 仍在过渡期；未来应进一步减少重复状态源。
- 机制驱动广度：runtime 已经使用 compiled mechanism，但更多 task 的 observation、score、instrument mapping 还需要完全由 mechanism/task spec 驱动。
- 真实 benchmark 难度：需要更多 hidden scenarios、多机制 families、private-eval seeds、强 baseline calibration 和 public/private generalization audit。
- 数据层成熟度：dataset card、trajectory schema、submission protocol 已有雏形，但还需要更接近 Minari 风格的数据版本治理和离线学习任务。
- agent 生态：LLM adapter 和 replay/stub 已有，但还缺真正 tool-using chemical agent baseline、planner memory、实验假设日志和解释评分闭环。
- 文档和教程：已有 12 天教程和架构文档，但仍需要把 notebook 工作量、挑战任务、评分 rubrics 和教师端评测流程继续打磨。

## 13. 下一阶段优先级

建议后续按以下顺序推进：

1. 继续收紧 Runtime v2，让 phase/vessel/equipment ledger 成为唯一结构化状态源。
2. 将 observation mapping、score spec 和 instrument response 全面绑定到 compiled mechanism 和 task card。
3. 为 distillation、extraction、crystallization、flow、electrochemistry 增加更专业的物理模型和参考验证。
4. 增加更有价值的 benchmark tasks：reaction calorimetry safety、VLE flash/distillation、LLE solvent selection、CSTR multiplicity、PFR hotspot、electrochemical selectivity-energy、crystallization purity/recovery。
5. 建立 official baseline report generator 和 private-eval signed runner。
6. 把教程从“点完代码”升级为“每天都有设计实验、解释机制、比较策略和提交报告”的项目制课程。

一句话总结：

ChemWorld 当前已经具备“统一物理化学世界 + 事务化实验运行时 + 可回放 benchmark 协议”的主体框架；下一阶段的重点不是继续堆更多 proxy 任务，而是让每个任务都由更强的 typed ledger、mechanism compiler、instrument model、physics service 和 evaluation contract 真正驱动。
