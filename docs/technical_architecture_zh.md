# ChemWorld-Bench 技术架构总览

更新日期：2026-07-09

## 1. 平台定位

ChemWorld-Bench 是一个面向 AI4Science、化工教育和闭环实验决策研究的虚拟物理化学交互环境。它不是一组互不相关的小游戏，也不声称预测真实反应体系；它的目标是在同一套物理化学世界规律下，提供可复现、可提交、可评测的任务切片。

正式 Gymnasium 入口统一为：

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-optimization-standard", seed=0)
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(action)
```

## 2. 当前核心分层

```text
chemworld
├── foundation      # ontology、constitution、typed state、unit、world law
├── world           # scenario、operation、instrument、recipe、world-law modules
├── runtime         # Runtime v2：transaction、kernel registry、mechanism compiler
├── envs            # 薄 Gymnasium adapter：ChemWorldEnv
├── tasks           # task registry 和 task card
├── schemas         # action、recipe、trajectory、manifest、task、scenario schema
├── agents          # random、LHS、greedy、BO、safe BO、scripted、LLM stub
├── eval            # runner、metrics、verify、suite、leaderboard
├── data            # logging、submission、dataset export、validation、anonymize
├── physchem        # 可复用物理化学模型库
├── wrappers        # action mask、safety/cost、NaN observation wrappers
└── cli             # run/evaluate/verify/tasks/scenarios/datasets/render
```

## 3. WorldLaw：同一个物理化学世界

所有 task 都指向同一个世界规律：

```text
world_law_id = chemworld-physical-chemistry
```

`WorldLawSpec` 记录 ontology、physical constitution、operation registry、instrument registry、transition module、observation module、backend spec 和 scenario generator。新增 task 时不新增独立环境，而是在同一世界规律下改变初始条件、预算、可用操作、可用仪器、目标函数和评价指标。

## 4. Runtime v2：新的运行时中心

当前运行时中心是 `chemworld.runtime`，不再由单个 batch reactor 文件承担全部调度。核心结构是：

```text
ChemWorldEnv
  → ChemWorldRuntime
      → ActionValidator
      → OperationKernelRegistry
      → DomainServices
      → TransactionManager
      → ConstitutionChecker
      → ObservationKernel
      → ScoringService
```

关键思想：

- Gym 环境只负责标准 `reset/step/render` 协议。
- operation kernel 表达“这个实验动作要做什么”。
- domain services 负责反应、传热、相平衡、分离、仪器和评分等计算。
- transaction manager 统一提交 `StatePatch`，并记录 `WorldEvent`。
- constitution check 失败时回滚 material ledger，只在 process ledger 中记录惩罚和失败原因。

这让后续加入结晶、精馏、连续流、电化学和更高保真后端时，不需要继续膨胀 Gym 环境或某个中心文件。

## 5. Mechanism Compiler：机制文件驱动世界

机制不再固定为某一个五反应网络。每个 scenario 绑定一个 mechanism YAML，初始化时编译为 `CompiledMechanism`：

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

运行时使用编译后的机制对象，不逐步读取 YAML。trajectory 和 verifier 会记录 `mechanism_id` 和 `mechanism_hash`，机制文件变化时 replay 可以直接失败。

## 6. Typed Ledgers：强类型状态账本

`WorldState` 现在包含 typed ledgers：

- `SpeciesLedger`：物种定义、角色、初始投料策略。
- `PhaseLedger`：各相中各物种的 amount，是 material state 的主要账本。
- `VesselLedger`：容器体积、温度、压力和相归属。
- `EquipmentLedger`：反应器、柱、电化学池、流动设备等挂载关系。
- `ThermalLedger`：按 vessel 记录夹套热、反应热和热损失。
- `ProcessLedger`：时间、成本、风险、样品消耗和废液。

当前迁移期仍保留一层 legacy scalar state adapter，但 typed ledger 会随状态更新同步，避免 phase totals 和 hidden species totals 漂移。

## 7. Scenario、Task、Campaign

平台正式区分：

```text
WorldLaw  →  共享物理化学规则
Scenario  →  hidden parameters + initial state + mechanism
Task      →  budget/objective/allowed operations/instruments/metrics
Campaign  →  某 agent 在某 task/seed 下的一次评测
Experiment→  campaign 内的一次实验
Operation →  单步实验动作
```

在 campaign task 中，`final_assay` 结束当前 experiment，但不结束整个 campaign；在 single-experiment task 中，`final_assay` 终止 episode。

## 8. 日志与回放

trajectory JSONL 现在记录：

- campaign、experiment、operation 三层 id；
- scenario id、initial state id；
- mechanism id 和 mechanism hash；
- kernel id、kernel version；
- affected ledgers；
- world events；
- state patch summary；
- transaction status 和 rollback reason；
- observation raw signal、processed estimate 和 uncertainty。

Verifier 使用 `task_id + scenario_id + mechanism_hash + seed + action sequence` 恢复运行时。机制 hash 不一致时，回放应失败。

## 9. 当前可以做什么

当前平台已经支持：

- 反应条件优化；
- 安全约束反应优化；
- 机制解释任务；
- 投料到 final assay 的完整单实验；
- 反应到萃取/分离/纯化再检测；
- partition discovery；
- purity-yield tradeoff；
- 结晶、精馏、连续流、电化学的初版任务切片；
- HPLC、GC、UV-vis、final assay 的多层观测；
- 本地 submission bundle、verify、evaluate、leaderboard 聚合；
- 教师端/学生端本机评测模拟；
- JSONL/Parquet dataset export；
- 12 天中文教程。

## 10. 下一步重点

下一阶段的重点不是继续堆 task 名称，而是继续把物理模块做深：

- 将 reaction network 深拆为 mechanism spec、rate law、thermochemical coupling、integrator、loader。
- 将 separation、distillation、crystallization、flow、electrochemistry 做成更成熟的 domain services。
- 将 macro operation 编译成 primitive/domain operation 序列，避免宏操作绕过 preconditions。
- 将 verifier 扩展到 transaction-level replay 和 mechanism-hash mismatch。
- 冻结一批 reference baseline table，并用 task/agent/seed 矩阵生成 paper artifact。

