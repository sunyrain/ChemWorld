# ChemWorld-Bench 技术架构总览

更新日期：2026-07-09

## 1. 平台定位

ChemWorld-Bench 是一个面向 AI4Science、化工教育和闭环实验决策研究的虚拟物理化学交互环境。它不是一组互不相关的小游戏，也不声称预测真实反应体系；它的目标是在同一套物理化学世界规则下，为学生、LLM agent、贝叶斯优化器和混合系统提供可复现、可提交、可验证、可评测的实验任务。

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
├── runtime         # Runtime v2: transaction, kernel registry, mechanism compiler
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

核心原则是：Gym 环境只负责交互协议；世界规则由 foundation/world 定义；运行时由 runtime 事务化执行；具体物理计算由 physchem 和 domain services 承担。

## 3. 单一 WorldLaw

所有正式任务都指向同一个世界规律：

```text
world_law_id = chemworld-physical-chemistry
```

新增任务时不新建独立环境，而是在同一 WorldLaw 下改变：

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
      -> DomainServices
      -> PrimitiveServices
      -> ReactionThermalServices
      -> PhaseSeparationServices
      -> CrystallizationServices
      -> DistillationServices
      -> FlowServices
      -> ElectrochemicalServices
      -> InstrumentCostServices
      -> OperationRecordServices
      -> TransactionManager
      -> ConstitutionChecker
      -> ObservationServices
      -> ScoringService
```

关键设计：

- `ChemWorldEnv.step()` 只做 action canonicalization、validation、runtime dispatch、observation、reward/info 和 campaign bookkeeping。
- `TaskRuntimeProfile` 声明当前任务需要哪些 operation、instrument、kernel 和 capability，不要求全局所有 kernel 都注册。
- `OperationKernelRegistry` 把操作类型映射到小型 command handler。
- `DomainServices` 是轻量 operation composition surface，负责委托独立服务、constitution checks 和 operation record assembly。
- `TransactionManager` 统一提交 `StatePatch`，记录 `WorldEvent`，并在 constitution failure 时回滚 material ledger。
- safety/cost 作为一等信号进入 `info["cost"]`、`info["cost_components"]` 和 leaderboard metrics。

这次重构后，primitive material handling、reaction/thermal advancement、phase/extraction workflow、crystallization、distillation、continuous flow、electrochemical conversion、measurement cost/sample consumption 和 operation record assembly 不再混在一个 state-changing domain service 中。专门服务负责各自物理过程，事务层负责提交或回滚，record service 负责把已接受的 pre/post state pair 写成可回放轨迹。

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

trajectory 和 verifier 会记录 `mechanism_id` 与 `mechanism_hash`。如果机制文件变化，replay verifier 会失败，而不是产生悄悄漂移的结果。

运行时已经不再把通用逻辑写死到某一个五物种网络。`MechanismSpeciesView` 会从 compiled mechanism 中解析 reactant、target、impurity、catalyst、byproduct 和 degradation marker。旧的 batch-reaction 物种名只作为少数历史 benchmark mechanism 的 world-level fallback role bindings 存在，不再散落在 observation、scoring、phase bookkeeping 或 electrochemistry 服务中。

## 6. Typed Ledgers

`WorldState` 已经升级为 typed ledger 结构：

- `SpeciesLedger`：物种定义、角色、初始投料策略；
- `PhaseLedger`：各相中的物种 amount，是 material state 的主要账本；
- `VesselLedger`：容器体积、温度、压力和相归属；
- `EquipmentLedger`：反应器、柱、电化学池、流动设备等挂载关系；
- `ThermalLedger`：按 vessel 记录夹套热、反应热和热损失；
- `ProcessLedger`：时间、成本、风险、样品消耗和废液。

当前仍保留一层 scalar state adapter，以便快速迭代期间维持旧轨迹和 notebook 行为稳定。长期目标是让 phase/vessel/equipment ledger 成为唯一结构化状态源。

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

- `raw_signal`：HPLC/GC chromatogram、UV-vis、IR、NMR、final assay packet 等原始信号；
- `processed_estimate`：yield、selectivity、conversion、purity、recovery、risk 等处理后估计；
- `uncertainty`：每个观测值的噪声和不确定性。

默认 observation 不泄露 hidden species amounts、rate constants、partition coefficients 或机制参数。Agent 只能通过 instrument action 获得有成本、有噪声、有样品消耗的观测。

## 9. Replay 与评测可信度

当前 replay verifier 已经支持：

- 使用 `task_id + seed + action sequence` 重放轨迹；
- 使用 task 原始 budget 处理 early termination，不再把轨迹长度误当 budget；
- 比对 reward、observation、terminated、truncated、operation type 和 constitution checks；
- 检查 `mechanism_hash`，机制文件漂移会导致验证失败；
- 比对 Runtime v2 transaction metadata，包括 kernel id/version、affected ledgers、world events、state patch summaries、transaction status、rollback reason 和 state-delta summaries。

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
- HPLC、GC、UV-vis、IR、NMR、final assay 的合成仪器信号；
- random、LHS、greedy、BO、safe BO、scripted chemistry、LLM replay/stub agent；
- JSONL trajectory、submission bundle、verify、evaluate、leaderboard aggregation；
- 本地教师端/学生端评测机模拟；
- dataset export 和 dataset card；
- 12 天中文 notebook 教程。

## 11. 当前技术债

最重要的技术债不是任务数量，而是专业底座深度：

- `runtime/domain_services.py` 已经变成轻量组合层，后续要保持它轻，不把过程公式写回 composition layer。
- `reaction_network.py`、`eos.py`、`equilibrium_chemistry.py`、`spectroscopy.py` 仍是较大模块，需要按算法族继续拆分。
- reaction integration 仍有一部分历史 batch-reactor 数值假设，需要逐步完全由 mechanism spec 和 compiled mechanism 驱动。
- separation、distillation、crystallization、flow、electrochemistry 目前是 benchmark-oriented semi-mechanistic models，还不是专业流程模拟器。
- reference backend validation 仍处于局部完成阶段，距离 Cantera/CoolProp/Reaktoro/pycalphad 等系统级对照还有距离。
- 中文教程和中文架构文档已经逐步修复，但仍需要持续检查 notebook 输出是否出现编码问题。

## 12. 下一阶段方向

下一阶段不应继续堆 task 名称，而应继续加深底座：

1. 保持 `runtime/domain_services.py` 为轻量组合层，并继续减少 focused runtime service 中的 legacy scalar-state adapter。
2. 让 reaction network、observation mapping 和 scoring 完全由 mechanism/task spec 驱动。
3. 把 macro operation 编译为 primitive/domain operation 序列，避免宏操作绕过 precondition 和 transaction。
4. 强化 ledger-level replay、state patch 审计和 private-eval 机制。
5. 为每个主要任务生成 reference baseline table 和 paper artifact。
6. 对照专业库逐步补足 property、EOS、equilibrium、reactor、separation、spectroscopy 的参考验证。

一句话概括：当前 ChemWorld 已经从“反应优化环境”升级为“统一物理化学世界下的可交互 benchmark 原型”。距离真正专业级 chemical world model gym，核心差距在高保真物理模块、机制驱动彻底性、typed ledger 单一事实源、reference validation 和任务级 benchmark 可信度。
