# ChemWorld-Bench 技术架构总览

本文档描述当前 `main` 分支的主线架构。它不记录历史迁移细节，只回答：

- ChemWorld 现在是什么；
- 它如何组织实验动作、物理模型、观测、评分、日志和回放；
- 当前距离更成熟的 chemical world model 交互环境还差什么。

## 1. 平台定位

ChemWorld-Bench 是一个面向智能体交互训练、科研评测和课程扩展的虚拟物理化学世界。它不是一个真实反应预测软件，也不是一组彼此独立的小游戏，而是一个统一的 Gymnasium 环境：

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=1)
obs, info = env.reset(seed=1)
```

`ChemWorld` 是统一世界入口，`task_id` 是同一套物理化学世界规律下的任务切片。不同任务共享 ontology、physical constitution、operation language、instrument contracts、transaction runtime、trajectory schema、dataset schema 和 benchmark protocol。

合理的一句话表述是：

> ChemWorld-Bench 是一个机制驱动、事务化、可回放的虚拟化学实验交互环境，用于研究 agent 如何在有限预算、部分可观测、有成本和安全约束的物理化学世界中进行实验决策、局部 world model 学习和多目标优化。

## 2. 总体分层

```text
src/chemworld
├── envs        # Gymnasium 环境适配层，正式入口是 ChemWorld
├── runtime     # Runtime v2：task profile、kernel registry、domain services、transaction
├── foundation  # ontology、physical constitution、typed ledgers
├── world       # scenario、operation cards、instrument cards、scoring、world law
├── physchem    # 独立实现的物理化学和化工模型库
├── tasks       # benchmark task registry
├── agents      # baseline agents
├── eval        # evaluation、replay verify、leaderboard、artifact
├── data        # trajectory、submission、dataset export
└── schemas     # action、recipe、trajectory、manifest、task、scenario、mechanism
```

核心原则是：Gym 层保持薄，任务差异由 task/scenario/profile 声明，物理过程由 domain services 执行，状态变化由 transaction manager 提交，观测和评分由独立 contract 生成。

## 3. 世界概念层级

```text
WorldLaw    -> 共享物理化学规则
Scenario    -> hidden parameters + initial state + mechanism
Task        -> budget/objective/allowed operations/instruments/metrics
Campaign    -> agent 在某个 task/seed 下的一次完整评测
Experiment  -> campaign 内的一次实验尝试
Operation   -> 单步实验动作
```

任务不是独立小游戏，而是同一世界规律的不同切片。例如反应优化、反应到纯化、分配规律发现、结晶、蒸馏、连续流和电化学任务都运行在同一个 `ChemWorld` 入口下，只是初始状态、允许操作、仪器权限、预算、评分目标和终止条件不同。

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

`ChemWorldEnv.step()` 只做 Gym 编排：action canonicalize、schema/task/payload validation、runtime dispatch、observation、reward/info 和 campaign bookkeeping。真正改变世界状态的是 Runtime v2。

关键设计：

- `TaskRuntimeProfile` 声明当前任务需要哪些 operation、instrument、kernel、domain service 和 capability。
- `OperationKernelRegistry` 把 operation type 映射到小型 command handler。
- `DomainServiceRegistry` 声明物理服务和 operation-to-service 映射。
- operation kernel 不直接写大段物理模型，而是调用 domain services。
- kernel 返回 `WorldEvent` 和 `StatePatch`，不任意返回完整新 state。
- `TransactionManager` 统一提交 patch，执行 constitution checks，失败时 rollback。
- safety/cost 是一等信号，进入 `info["cost"]`、`cost_components`、constraint flags、trajectory 和 leaderboard metrics。

## 5. Domain Services

当前 runtime 已把主要物理过程拆成 focused services：

| Service | 主要职责 |
| --- | --- |
| primitive services | 投料、加溶剂、加催化剂、取样、淬灭、蒸发、非法动作惩罚 |
| reaction/thermal services | ODE 反应推进、加热/等待、热账本、压力和风险投影 |
| phase/separation services | 相账本、萃取、混合、静置、分相、洗涤、干燥、浓缩、转移 |
| crystallization services | 加晶种、冷却结晶、固相/母液相输出、过滤 |
| distillation services | VLE shortcut distillation、馏分收集、能耗、溶剂损失 |
| electrochemical services | 电位/电流设定、Nernst/Butler-Volmer、Faraday conversion、电功 |
| flow services | 流量设定、停留时间、连续流投影、flow conversion |
| instrument services | 测量成本、样品消耗、仪器状态、观测生成 |
| scoring services | 根据 task score contract 计算在线 reward 和 final leaderboard score |

这些 service 的成熟度不同。平台要求 proxy 不能伪装成 professional kernel，任务和报告必须暴露 maturity metadata。

## 6. Mechanism Compiler

机制文件不会在每一步 runtime 中直接读取，而是在 reset/scenario 初始化时编译为 `CompiledMechanism`。

Compiled mechanism 包含：

- `mechanism_id`;
- `mechanism_hash`;
- species index;
- stoichiometric matrix;
- rate-law evaluators;
- reaction enthalpies;
- species roles;
- observable mapping;
- score spec;
- initial amount policy.

trajectory 和 verifier 记录 `task_id`、`scenario_id`、`mechanism_hash`、`runtime_profile_hash`、`scoring_contract_hash` 和 `observation_contract_hash`。如果机制或 contract 漂移，replay 应直接失败。

## 7. Typed Ledgers

`WorldState` 使用强类型账本组织状态：

| Ledger | 内容 |
| --- | --- |
| SpeciesLedger | 物种定义、角色、式量、公开标签 |
| PhaseLedger | 每个相中的物种量、体积、相类型、容器归属 |
| VesselLedger | 容器容量、当前相、温度、压力 |
| EquipmentLedger | 柱、流动反应器、电化学池、结晶器、仪器状态 |
| ThermalLedger | per-vessel heat input、reaction heat、heat loss |
| ProcessLedger | elapsed time、cost、risk、sample consumption、process metrics |

物料状态以 phase ledger 为单一事实源，global species totals 是从 phase ledger 聚合得到的视图。`WorldState.species_amounts`
仍作为兼容视图存在，但每次 constitution check 会通过 ledger single-source audit 确认它与
`PhaseLedger.total_amounts_mol()` 同步。

同样，`ProcessLedger` 是时间、成本、风险、样品消耗和过程指标的主来源；legacy `Ledger`
只作为兼容视图。vessel、phase、equipment 和 thermal ledgers 的交叉引用也会被审计。
metadata 不允许保存 primary material、phase、vessel、equipment、instrument 或 process
state。普通 agent 只能看到 observation，不会直接读取 hidden material ledger。

## 8. Observation And Spectra

观测分三层：

| 层 | 含义 |
| --- | --- |
| `raw_signal` | HPLC、GC、UV-vis、IR、NMR、final assay packet 等仪器信号 |
| `processed_estimate` | yield、selectivity、purity、recovery、phase ratio 等处理后估计 |
| `uncertainty` | 噪声、LOD/LOQ、校准、估计置信信息 |

Gym 数组仍暴露稳定 numeric observation keys。没有被当前仪器观测到的字段在 Gym 中为 `NaN`，在 JSONL 中为 `null`，并由 `observed_mask` 和 `observed_keys` 标记。

自洽性审计会检查 raw spectra 与 processed metrics 是否语义一致，例如 high purity 不应同时出现明显由 reactant peak 主导的 final HPLC。

## 9. Task Registry

当前任务统一注册在 `chemworld.tasks`。任务固定：

- world law id；
- scenario id；
- split、budget、seeds；
- episode mode；
- allowed operations；
- allowed instruments；
- objective、threshold、safety limit；
- observation policy；
- termination policy；
- success metrics；
- maturity metadata。

当前注册任务包括反应优化、安全约束、机制解释、reaction-to-assay、reaction-to-purification、partition discovery、purity-yield tradeoff、public/private generalization、low-budget characterization、tool-agent planning、reaction-to-crystallization、reaction-to-distillation、continuous flow 和 electrochemical conversion。

## 10. Campaign 与 Experiment

`campaign` 和 `single_experiment` 是两个不同 episode 语义：

- `single_experiment`：`final_assay` 终止 Gym episode，适合完整单次流程。
- `campaign`：`final_assay` 结束当前 experiment，但 campaign 继续，适合 BO/LHS/greedy/leaderboard 优化。

这使得 recipe-space optimizer 可以在一个有限预算 campaign 内运行多个完整实验，而不会因为第一次 final assay 就结束整个 benchmark。

## 11. Benchmark 与提交

评测链路是：

```text
task card
  -> run/suite
  -> trajectory JSONL
  -> verify
  -> evaluate/leaderboard
  -> submission bundle or paper artifact
```

每条 trajectory 记录 operation、preconditions、state_delta_summary、constitution checks、raw_signal、processed_estimate、uncertainty、reward、leaderboard_score、hashes 和 maturity metadata。

正式提交包包含：

- manifest；
- trajectories；
- results；
- optional explanations；
- command、dependency、commit、agent metadata。

## 12. 本地教师端/学生端评测

推荐本机评测机结构：

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

## 13. 当前能力

当前平台可以支持：

- 多步自定义实验；
- 反应、测量、萃取、分相、纯化、结晶、蒸馏、连续流和电化学 task；
- HPLC、GC、UV-vis、IR、NMR 和 final assay 虚拟信号；
- task-based baseline reports；
- replay verification；
- dataset export；
- local evaluation machine；
- 12 天教学 notebook；
- self-consistency audit；
- maturity-gated benchmark artifacts。

## 14. 当前主要差距

距离更成熟的 chemical world model 交互环境，仍有几个关键差距：

- broad exploratory task profile 需要进一步收紧；
- proxy process modules 需要逐步替换为 reference-validated 或 professional-candidate kernels；
- baseline results 需要冻结为正式 paper artifact；
- private eval 仍是本地 maintainer-salt 工作流，不是 hosted hidden evaluator；
- explanation scoring 仍以结构化字段和人工/半自动评估为主；
- 高保真热力学、相平衡、反应机理和设备模型还需要长期专业化实现。

## 15. 当前结论

ChemWorld 已经具备“统一物理化学世界 + task registry + Runtime v2 + typed ledgers + instrument observation + replayable benchmark protocol”的主体框架。当前阶段最重要的工作不是继续横向增加页面或 proxy 任务，而是：

- 收紧 release task profiles；
- 冻结 task cards 和 baseline reports；
- 保持 self-consistency audit 作为门禁；
- 逐个深化物理模块成熟度；
- 让文档站始终围绕正式 benchmark contract 组织。
