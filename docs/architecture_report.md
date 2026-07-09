# ChemWorld 架构快照

本文档给外部读者一个短版架构说明，只描述当前 `main` 分支已经落到代码里的结构。
更细的设计细节见 [技术架构](technical_architecture_zh.md)。

## 当前定位

ChemWorld-Bench 是一个统一的虚拟物理化学交互环境。正式入口只有一个：

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=1)
obs, info = env.reset(seed=1)
```

`task_id` 不是切换到另一个小游戏，而是在同一个 `world_law_id =
chemworld-physical-chemistry` 下选择不同 task slice。任务通过预算、初始场景、允许操作、
仪器权限、评分指标和终止策略定义差异。

## 源码分层

| 层 | 主要目录 | 责任 |
| --- | --- | --- |
| Gym 入口 | `src/chemworld/envs` | 提供 `ChemWorldEnv`、spaces、render、task info 和 Gym 五元组 |
| Runtime v2 | `src/chemworld/runtime` | profile、operation kernel、domain services、transaction、mechanism compile summary |
| 世界底座 | `src/chemworld/foundation` | ontology、constitution、typed ledgers、unit/state helpers、public leakage audit |
| 世界描述 | `src/chemworld/world` | operations、scenario、world law、instrument cards、observation/scoring contracts |
| 物理化学模块 | `src/chemworld/physchem` | 反应、分离、热力学、谱图、输运、电化学、成熟度和参考验证切片 |
| 任务合同 | `src/chemworld/tasks.py` | `TaskSpec`、task cards、allowed operations、seeds、maturity、contract hash |
| Agent 接口 | `src/chemworld/agent_interface.py`、`src/chemworld/wrappers.py` | task prompt、available actions、observation views、RL/LLM wrappers |
| Baseline | `src/chemworld/agents` | random、LHS、BO、safe BO、scripted、LLM replay/stub |
| 评测 | `src/chemworld/eval` | metrics、suite、leaderboard、verify、baseline report、paper artifact、agent probe |
| 数据 | `src/chemworld/data` | trajectory schema、logging、submission bundle、dataset export、anonymization |
| Schema | `src/chemworld/schemas` | action、recipe、trajectory、manifest、task、scenario、mechanism JSON schema |

## Step 执行链路

当前 `ChemWorldEnv.step(action)` 是薄编排层：

```text
canonicalize action
  -> OperationValidator
  -> ChemWorldRuntime.apply_transaction(...)
  -> ObservationKernel.observe(...)
  -> scoring / reward / info
  -> campaign bookkeeping
  -> Gymnasium tuple
```

核心状态改变不在 Gym 层完成，而由 Runtime v2 处理。

## Runtime v2

Runtime v2 的当前中心是 `ChemWorldRuntime`：

```text
ChemWorldRuntime
  ├── TaskRuntimeProfile
  ├── OperationKernelRegistry
  ├── DomainServiceRegistry
  ├── ChemWorldDomainServices
  ├── TransactionManager
  └── RuntimeContext
```

关键规则：

- task 只要求当前 profile 需要的 kernel/service，不要求全局所有操作都可用；
- operation kernel 负责 command dispatch，不承载大段物理模型；
- 物理语义由 domain services 执行；
- transaction 返回 `WorldEvent`、`StatePatch`、`affected_ledgers`、`cost_delta`、`risk_delta`；
- constitution failure 通过 transaction rollback 记录，不静默修改物料账本；
- `info` 中暴露 `kernel_id`、`kernel_version`、`transaction_status` 和 patch/event 摘要。

## 机制与场景

机制不在每一步 runtime 中读取。场景初始化时会编译为 `CompiledMechanism`，并记录：

- `mechanism_id`;
- `mechanism_hash`;
- species index;
- stoichiometric matrix;
- rate-law equation ids;
- reaction enthalpies;
- observable mapping;
- score spec;
- initial amount policy.

公开 agent-facing view 只暴露 hash、计数、contract 和 maturity，不暴露 hidden species identity、
rate constants、stoichiometry 或 private scenario seed。

## Typed Ledgers

`WorldState` 由强类型账本组织：

| Ledger | 主职责 |
| --- | --- |
| `SpeciesLedger` | 物种定义、公开角色、式量和标签 |
| `PhaseLedger` | 每个相中的物种量、体积、相类型、容器归属 |
| `VesselLedger` | 容器容量、相引用、温度、压力 |
| `EquipmentLedger` | 柱、流动反应器、电化学池、结晶器等设备状态 |
| `ThermalLedger` | per-vessel heat input、reaction heat、heat loss |
| `ProcessLedger` | elapsed time、cost、risk、sample consumption、process metrics |

物料状态以 phase ledger 为主来源；全局物种量是聚合视图。审计会检查 phase/vessel/equipment
交叉引用、非负性、process ledger 和 metadata 泄漏。

## Agent-facing API

环境直接暴露一组稳定 agent 接口：

```python
env.task_prompt()
env.available_actions()
env.action_schema("heat")
env.validate_action(action)
env.observation_view("rl")
env.observation_view("tool_json")
env.observation_view("lab_report")
env.campaign_state()
```

这些接口只聚合公开 task、validator、observation 和 campaign bookkeeping，不读取 hidden truth。
RL 使用 finite vector/mask/cost view；LLM 和学生使用 tool-json/lab-report view。

## 评测与数据

当前预发布评测链路包含：

- official seed suite；
- baseline report；
- submission bundle；
- replay verifier；
- paper artifact skeleton；
- dataset export；
- environment self-consistency audit；
- multi-round tool-agent probe。

每条轨迹应携带 task/scenario/mechanism/scoring/profile hash、operation metadata、transaction
status、constraint flags、agent metadata 和 maturity metadata。

## 当前限制

- 平台是虚拟半机理 benchmark，不是现实反应预测软件。
- 多数高等物理化学模块仍处于 proxy、lite 或 professional-candidate 阶段，需要 P3 深化。
- 预发布核心任务目前冻结为 `reaction-to-assay`、`reaction-to-purification`、
  `partition-discovery`；其余任务已经注册但不等同于第一版正式榜单任务。
- private eval 仍采用维护者本机 hidden salt / seed 方案，尚未升级为 server-side signed evaluator。
- 文档和教程正在 P4 阶段收束，长期专业模型深化暂缓。
