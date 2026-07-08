# ChemWorld-Bench 技术架构总览

更新日期：2026-07-09

## 1. 平台定位

ChemWorld-Bench 是一个面向 AI4Science、化工教育和闭环实验决策研究的虚拟物理化学交互环境。它不是一组互不相干的小游戏，也不声称预测真实反应体系；它的目标是在同一套物理化学世界规则下，为学生、LLM agent、贝叶斯优化器和混合系统提供可复现、可提交、可验证、可评测的实验任务。

正式 Gymnasium 入口统一为：

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-optimization-standard", seed=0)
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(action)
```

## 2. 总体分层

```text
chemworld
├── foundation      # ontology, constitution, typed state, units, world law
├── world           # scenario, operation, instrument, recipe, world-law modules
├── runtime         # Runtime v2: transaction, kernel registry, domain services
├── envs            # Gymnasium adapter: ChemWorldEnv
├── tasks           # task registry and task cards
├── schemas         # action, recipe, trajectory, manifest, task, scenario schemas
├── agents          # random, LHS, greedy, BO, safe BO, scripted, LLM replay/stub
├── eval            # runner, metrics, verify, suite, leaderboard
├── data            # logging, submission, dataset export, validation, anonymize
├── physchem        # reusable physical-chemistry and chemical-engineering models
├── wrappers        # action mask, safety/cost, NaN observation wrappers
└── cli             # run, evaluate, verify, tasks, scenarios, datasets, render
```

核心原则是：Gym 环境只负责交互协议；世界规则由 `foundation` 和 `world` 定义；运行时由 `runtime` 事务化执行；具体物理计算由 `physchem` 和 domain services 承担。

## 3. 单一 WorldLaw

所有正式任务都指向同一个世界规律：

```text
world_law_id = chemworld-physical-chemistry
```

新增任务时不新建独立环境，而是在同一个 WorldLaw 下改变：

- scenario 和初始状态；
- hidden mechanism 和参数；
- 可用操作与可用仪器；
- 预算、目标函数和安全约束；
- 观测权限和终止策略；
- success metrics 和 leaderboard 配置。

因此 `reaction-optimization-standard`、`reaction-to-purification`、`reaction-to-distillation`、`flow-reaction-optimization` 和 `electrochemical-conversion` 都是同一个物理化学世界的不同任务切片。

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

关键设计：

- `ChemWorldEnv.step()` 只做 action canonicalization、validation、runtime dispatch、observation、reward/info 和 campaign bookkeeping。
- `TaskRuntimeProfile` 声明当前任务需要哪些 operation、instrument、kernel、domain service 和 capability，不要求全局所有 kernel 都注册。
- `OperationKernelRegistry` 把操作类型映射到小型 command handler。
- `DomainServiceRegistry` 提供 JSON-friendly 的 service contract 和 operation-to-service map，供 `task_info()`、审计、trajectory event 和文档读取；runtime 启动时会用当前 task profile 校验 service/capability 覆盖。
- `ChemWorldDomainServices` 是轻量 operation composition surface，只负责编排独立服务、constitution checks 和 operation record assembly。
- `TransactionManager` 统一提交 `StatePatch`，记录 `WorldEvent`，并在 constitution failure 时回滚 material ledger。
- safety/cost 作为一等信号进入 `info["cost"]`、`info["cost_components"]` 和 leaderboard metrics。

这次重构后，primitive material handling、reaction/thermal advancement、phase/extraction workflow、crystallization、distillation、continuous flow、electrochemical conversion、measurement cost/sample consumption 和 operation record assembly 不再混在一个 state-changing domain service 里。专门服务负责各自物理过程，事务层负责提交或回滚，record service 负责把已接受的 pre/post state pair 写成可回放轨迹。每个 `operation_applied` event 还会记录 `domain_service_id`，方便审计某个动作到底由哪类物理服务处理。

`task_info()["runtime"]["profile"]` 现在会公开 `required_domain_services`。这意味着学生、agent、评测器和审稿人都能看到某个任务到底需要 reaction、separation、distillation、flow、electrochemistry 或 observation service 中的哪些能力，而不是只看到一串 operation 名称。

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

Trajectory 和 verifier 会记录 `mechanism_id` 与 `mechanism_hash`。如果机制文件变化，replay verifier 会失败，而不是产生悄悄漂移的结果。

运行时已经不再把通用逻辑写死到某一个五物种网络。`MechanismSpeciesView` 会从 compiled mechanism 中解析 reactant、target、impurity、catalyst、byproduct 和 degradation marker。旧的 batch-reaction 物种名只作为少数历史 benchmark mechanism 的 world-level role binding 存在，不再散落在 observation、scoring、phase bookkeeping 或 electrochemistry 服务中。

## 6. Typed Ledgers

`WorldState` 已经升级为 typed ledger 结构：

- `SpeciesLedger`：物种定义、角色、初始投料策略；
- `PhaseLedger`：各相中的物种 amount，是 material state 的主要账本；
- `VesselLedger`：容器体积、温度、压力和相归属；
- `EquipmentLedger`：反应器、柱、电化学池、流动设备、仪器状态等挂载关系；
- `ThermalLedger`：按 vessel 记录夹套热、反应热和热损失；
- `ProcessLedger`：时间、成本、风险、样品消耗和废液。

当前仍保留一层 scalar state adapter，用于快速迭代期间保持旧轨迹和 notebook 行为稳定。长期目标是让 phase/vessel/equipment ledger 成为唯一结构化状态源，并把剩余 derived metadata 限定为报告和观测摘要。

## 7. Task、Scenario、Campaign

平台正式区分：

```text
WorldLaw   -> 共享物理化学规则
Scenario   -> hidden parameters + initial state + mechanism
Task       -> budget/objective/allowed operations/instruments/metrics
Campaign   -> 某 agent 在某 task/seed 下的一次完整评测
Experiment -> campaign 内的一次实验
Operation  -> 单步实验动作
```

在 campaign task 中，`final_assay` 结束当前 experiment，但不必结束整个 campaign；在 single-experiment task 中，`final_assay` 会终止 episode。

## 8. Observation 与仪器

观测采用三层结构：

- `raw_signal`：HPLC、GC、UV-vis、IR、NMR、final assay packet 等原始信号；
- `processed_estimate`：yield、selectivity、conversion、purity、recovery、risk 等处理后估计；
- `uncertainty`：每个观测值的噪声和不确定性。

默认 observation 不泄露 hidden species amounts、rate constants、partition coefficients 或机制参数。Agent 只能通过 instrument action 获得有成本、有噪声、有样品消耗的观测。

## 9. Replay 与评测可信度

当前 replay verifier 已经支持：

- 使用 `task_id + seed + action sequence` 重放轨迹；
- 使用 task 原始 budget 处理 early termination，不再把轨迹长度误当 budget；
- 比对 reward、observation、terminated、truncated、operation type 和 constitution checks；
- 检查 `mechanism_hash`，机制文件漂移会导致验证失败；
- 比对 Runtime v2 transaction metadata，包括 kernel id/version、domain service id、affected ledgers、world events、state patch summaries、transaction status、rollback reason 和 state-delta summaries。

这让提交者不能只改 JSONL 里的分数、reward、观测或 transaction metadata 来伪造结果。后续仍需要进一步加强 ledger-level replay 和 private-eval signed runner。

## 10. 当前核心能力

当前平台已经支持：

- 反应条件优化；
- 安全约束优化；
- 机制解释任务；
- 投料到 final assay 的完整单实验流程；
- 反应到萃取、分相、纯化、检测的闭环流程；
- partition discovery；
- purity-yield-cost tradeoff；
- 结晶、蒸馏、连续流、电化学的初版任务切片；
- Runtime v2 transaction metadata、operation kernel metadata 和 domain service metadata；
- 本地教师端/学生端 submission pipeline；
- JSONL/Parquet dataset export；
- 12 天中文教程 notebook。

## 11. 当前边界

平台仍然是虚拟半机理 benchmark，不是：

- 真实反应预测软件；
- 真实机器人实验平台；
- DFT/MD/CFD 高保真模拟器；
- 在线账号式竞赛平台；
- 通用 chemical world model 的完成形态。

当前最重要的工程边界是：环境已经能表达统一物理化学世界下的多类任务，但许多物理模块还处于 `proxy`、`lite` 或 `reference_validated` maturity。后续要逐项把 property package、EOS、VLE、kinetics、reactor、crystallization、electrochemistry、spectroscopy 和 process-control 模块提升到更专业的可验证实现。

## 12. 后续主线

后续主线不是继续堆 task 数量，而是把同一个世界底座做深：

1. 继续减少 scalar-state adapter，让 typed ledger 成为 primary state。
2. 让 scenario/mechanism card 更完整地驱动物种、反应网络、观测映射和评分。
3. 增强 professional physchem 模块，逐项替换仍然过轻的 proxy。
4. 建立更强的 reference baseline 和 public/private generalization protocol。
5. 把教师端 private runner 升级为签名评测包或 server-side hidden evaluator。
