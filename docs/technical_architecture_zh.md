# ChemWorld-Bench 技术架构文档

更新日期：2026-07-07

## 1. 平台定位

ChemWorld-Bench 当前定位为一个面向 AI4Science、化工教育和闭环实验决策研究的虚拟自驱化工实验 benchmark。它不是一个真实反应预测软件，也不是机器人实验室控制系统，而是一个可复现、可评测、可扩展的物理化学世界环境。

核心设计原则是：

> ChemWorld 不是一组彼此独立的小游戏，而是一个共享物理化学世界规律的统一 Gym 环境。不同 benchmark task 只是同一套 world law 下的不同切片。

当前正式入口是：

```python
import gymnasium as gym
import chemworld

env = gym.make(
    "ChemWorld",
    task_id="reaction-optimization-standard",
    seed=0,
)
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(action)
```

## 2. 总体架构

当前代码采用 Python monorepo 风格组织，核心包位于 `src/chemworld/`。

```text
chemworld
├── foundation      # 世界底座：ontology、constitution、state、ledger、units、world law
├── core            # 物理化学机制：反应、相分配、分离、目标函数、动作规范
├── backends        # transition 实现规格：当前为 semi_mechanistic
├── envs            # Gymnasium 环境注册与 step/reset 接口
├── tasks           # benchmark task registry
├── models          # agent 侧 belief state、surrogate model、uncertainty model
├── action_codec    # EventAction、CanonicalAction、Gym vector action 转换
├── operation_validator # task policy + physical preconditions 的统一验证器
├── wrappers        # action mask、安全成本、动作验证等可选增强
├── agents          # random、LHS、greedy、BO、safe BO、scripted、LLM adapter
├── eval            # runner、metrics、leaderboard、verify、explanation rubric
├── data            # trajectory schema、logging、validation、submission、anonymize
└── cli             # chemworld run/evaluate/verify/suite/tasks/submission
```

从研究系统角度看，运行链路为：

```text
Agent / Student / Optimizer
        ↓
event action
        ↓
ChemWorldEnv
        ↓
task-aware operation validation
        ↓
OperationValidator
        ↓
PhysicalConstitution preconditions
        ↓
TransitionKernel
  ├── reaction ODE
  ├── phase partition
  ├── separation operations
  └── instrument/sample/cost updates
        ↓
hidden WorldState + Ledger
        ↓
ObservationKernel
        ↓
partial noisy observation
        ↓
trajectory JSONL + evaluation metrics
```

## 3. Foundation 层

`chemworld.foundation` 是所有后续世界模块复用的底座。它的目标是把化学直觉写成可执行约束和可回放状态账本，而不是只停留在文档描述。

Foundation 只描述世界本体和世界规则，不放置 agent 学到的 surrogate。`BeliefState`、`SurrogateModel` 等可学习局部 world model 接口已经放入 `chemworld.models`，以保持“真实隐藏世界”和“学习到的世界近似”之间的边界清晰。

### 3.1 Ontology

当前 ontology primitives 包括：

| 类型 | 作用 |
| --- | --- |
| `Substance` | 物质、化学式、角色、相态 |
| `Phase` | 相，如 reactor liquid、aqueous、organic、solid |
| `Vessel` | 容器体积、温度、压力边界 |
| `Instrument` | 仪器可观测字段、成本、样品消耗、噪声 |
| `Operation` | 实验动作、必需字段、前置条件 |
| `Reaction` | 化学计量、反应热 |
| `StateVariable` | 状态变量、单位、是否 hidden |

### 3.2 Physical Constitution

`PhysicalConstitution` 是平台的“世界宪法”，每个 transition 后都会生成可审计检查结果。当前覆盖：

- 非负性：amount、volume、temperature、pressure、cost、risk、time、sample consumed 不得非法为负。
- 单位一致：状态和观测字段必须使用 canonical unit。
- 容器边界：体积、温度、压力不能超过 vessel 上限。
- 物料守恒：除投料、采样、测量、相操作等允许账本变化外，元素账本不能凭空变化。
- 观测非全知：默认 observation 不得泄露 hidden species amounts、rate constants、theta 等。
- 测量有成本：HPLC、GC、UV-vis、final assay 必须消耗成本或样品。
- 动作前置条件：无体积不能加热，无物料不能终止，final assay 必须在 terminate 后执行。
- 分离前置条件：分离操作需要 phase system；`separate_phase` 需要先 `settle`。
- 安全约束：高温、高浓度、压力、溶剂风险、放热等共同影响 risk。

### 3.3 State 与 Ledger

`WorldState` 是 hidden state 的核心数据结构。它包含：

- `species_amounts`：A、P、B、D、E、Cat_active、Cat_dead；
- `volume_L`；
- `temperature_K`；
- `pressure_Pa`；
- `phase`；
- `terminated` / `quenched`；
- `ledger`；
- `metadata`。

`Ledger` 记录实验账本：

- elapsed time；
- cost；
- risk；
- sample consumed；
- jacket energy；
- reaction heat；
- heat loss。

分离模块通过 `metadata.phase_ledger` 记录有机相、水相、产品分配、杂质、溶剂损失等 downstream 状态。

### 3.4 WorldLawSpec

`WorldLawSpec` 是当前统一世界设计的关键抽象。它记录：

- `law_version`；
- ontology registry；
- physical constitution；
- operation registry；
- transition kernel registry；
- observation kernel registry。

当前 world law id 为：

```text
chemworld-physical-chemistry
```

所有内置 benchmark task 都指向同一个 world law，而不是注册成多个独立环境。

## 4. Core 层

`chemworld.core` 当前包含 reaction + phase/separation 的第一套物理化学模块。

当前物理实现被显式声明为 `semi_mechanistic` backend。`WorldLawSpec` 定义世界规律，backend 负责以某个保真度实现 transition。这样当前半机理实现不会被误认为 ChemWorld 的全部未来物理核心，后续可接入 Cantera、IDAES、DWSIM、ASE/MLIP 或真实实验适配器。

### 4.1 反应网络

当前反应网络为：

```text
A -> P              目标反应
A -> B              副反应
P -> D              产物降解
A + P -> E          高温/高浓度耦合杂质
Cat_active -> Cat_dead   催化剂失活
```

速率结构采用 Arrhenius 形式：

```text
k_i(T) = A_i exp(-Ea_i / RT) * f_catalyst * f_solvent
```

并叠加：

- catalyst effect；
- solvent effect；
- concentration effect；
- stirring effect；
- catalyst activity；
- degradation；
- coupled impurity formation。

### 4.2 能量与安全

连续演化通过 `scipy.integrate.solve_ivp` 积分。温度演化使用简化能量平衡：

```text
rho Cp V dT/dt =
    Q_jacket
  - UA(T - T_env)
  - sum(deltaH_i r_i V)
```

safety risk 综合以下因素：

- temperature risk；
- concentration risk；
- exotherm risk；
- solvent risk；
- pressure proxy。

### 4.3 相分配与分离模块

当前同一 world law 下已经加入 downstream processing，不另注册独立 extraction world。

新增操作包括：

| 操作 | 作用 |
| --- | --- |
| `add_phase` | 加入 aqueous 或 organic 相 |
| `add_extractant` | 加入萃取剂 |
| `mix` | 根据 partition behavior 分配产品和杂质 |
| `settle` | 让相分离并满足后续前置条件 |
| `separate_phase` | 保留目标相，同时产生夹带损失 |
| `wash` | 降低 impurity signal，但损失部分产品 |
| `dry` | 降低 solvent loss |
| `concentrate` | 降低体积，带来成本和风险权衡 |
| `transfer` | 转移样品并产生 handling loss |

downstream truth 通过 hidden phase ledger 计算：

- purity；
- recovery；
- phase_ratio；
- product_in_organic；
- product_in_aqueous；
- impurity_signal；
- solvent_loss；
- process_mass_balance_error。

这些字段不会直接暴露给 agent，只能通过 HPLC、UV-vis、final assay 等 observation kernel 获得。

## 5. Gym 环境层

正式 Gymnasium 环境为：

```text
ChemWorld
```

环境实现位于：

```text
src/chemworld/envs/chemworld_env.py
```

公开注册环境统一为 `ChemWorld`。

### 5.1 action space

action 统一采用 event-action 语言：

```python
{"operation": "heat", "target_temperature_K": 385.0, "duration_s": 1200.0}
```

也支持 payload 形式：

```python
{
    "operation": "heat",
    "payload": {
        "target_temperature_K": 385.0,
        "duration_s": 1200.0,
    },
}
```

为了兼顾人类/LLM 与 Gym/RL 生态，动作层拆成四个概念：

- `EventAction`：人类和 LLM 面向的 JSON 动作；
- `CanonicalAction`：经过规范化的 operation、instrument、phase 名称；
- `ActionCodec`：在 canonical JSON 和稳定 numeric vector 之间转换；
- `OperationValidator`：统一执行 task-aware 和 constitution-aware 的动作有效性检查。

因此文档中的 event action 是语义动作语言，底层仍有稳定的 action codec 服务 BO、RL、replay 和 evaluator。

### 5.2 observation space

Gym observation 是稳定数值字段。未观测值用 `NaN` 表示。

当前 observation keys 包括：

- yield；
- selectivity；
- conversion；
- cost；
- safety_risk；
- score；
- byproduct_signal；
- degradation_warning；
- virtual_spectrum_summary；
- purity；
- recovery；
- phase_ratio；
- product_in_organic；
- product_in_aqueous；
- impurity_signal；
- solvent_loss；
- process_mass_balance_error。

JSONL 中未观测值保存为 `null`，并通过 `observed_mask` 和 `observed_keys` 标记哪些字段是真实被仪器观测到的。

### 5.3 info 字段

每一步 `info` 包含 rich audit trail：

- task id；
- world law id；
- world split；
- operation type；
- preconditions；
- state delta summary；
- constitution checks；
- instrument source；
- observed keys；
- raw signal；
- processed estimate；
- uncertainty；
- measurement cost；
- sample consumed；
- leaderboard score；
- constraint flags。

## 6. Task Registry

`chemworld.tasks` 是正式 benchmark 任务入口。任务不是新环境，而是同一 `ChemWorld` 下的 world slice。

`TaskSpec` 字段包括：

- `task_id`；
- `env_id`；
- `world_law_id`；
- `scenario_id`；
- `initial_state_id`；
- `world_split`；
- `objective`；
- `budget`；
- `seeds`；
- `threshold`；
- `allowed_operations`；
- `allowed_instruments`；
- `observation_policy`；
- `termination_policy`；
- `success_metrics`；
- `safety_limit`；
- `difficulty`；
- `description`；
- `tags`。

当前内置任务：

| Task ID | 核心目标 | 操作切片 |
| --- | --- | --- |
| `reaction-optimization-standard` | 反应优化 | reaction |
| `reaction-safety-constrained` | 安全约束优化 | reaction |
| `reaction-mechanism-explanation` | 优化并解释机制 | reaction |
| `reaction-to-assay` | 从投料到 final assay | reaction |
| `reaction-to-purification` | 反应、萃取、分离、纯化、检测 | reaction + separation |
| `partition-discovery` | 学习相分配规律 | phase/partition |
| `purity-yield-tradeoff` | 产率、纯度、回收率、成本权衡 | reaction + separation |
| `public-private-generalization` | 检测 public 到 private 的泛化 | reaction |
| `low-budget-characterization` | 极低预算下建立局部模型 | reaction |
| `tool-agent-planning` | LLM/tool agent 操作语言规划 | reaction + separation |

## 7. Wrappers 与动作有效性

`chemworld.wrappers` 提供可选 Gym wrapper，不改变底层五元组 API。

wrappers 不再重复实现验证逻辑，而是读取 `OperationValidator` 的输出，避免出现 mask、env.step 和 constitution 之间不一致。

### 7.1 ActionMaskWrapper

在 `reset` 和 `step` 的 `info` 中加入：

- `valid_operations`；
- `action_mask`；
- `operation_types`；
- `invalid_reasons`。

mask 同时考虑：

- 当前 task 的 `allowed_operations`；
- 当前 state 的 physical preconditions。

因此：

- reaction-only task 不会暴露 separation-only 操作；
- purification task 会在加相、加萃取剂、settle 等前置条件满足后逐步开放后续操作。

### 7.2 SafetyCostWrapper

在 `info` 中加入：

- `cost_signal`；
- `cost_components`；
- `constraint_budget_remaining`。

成本来源：

- unsafe；
- high cost；
- precondition failure；
- constitution failure。

### 7.3 NaNObservationWrapper

`NaNObservationWrapper` 面向 RL 和 sklearn pipeline，把 dict observation 中的 `NaN` 转成向量：

```text
filled_values + observed_mask
```

默认用 `-1.0` 替代缺失值，并把 observed mask 拼接到 observation vector 后半段。

## 8. Agents 与 Baselines

当前官方 baseline 包括：

- `random`；
- `lhs`；
- `greedy`；
- `scripted_chemistry`；
- `gp_bo`；
- `rf_ei`；
- `safe_gp_bo`；
- `LLMPlannerAgent` adapter；
- `ReplayLLMAgent`。

BO 类 agent 默认 `n_initial=4`。主 reaction optimization task 的预算为 72，使 recipe-based BO 能够在默认设置下进入 acquisition 阶段，而不是把全部预算消耗在初始化。

`scripted_chemistry` 已能根据 task 的 allowed operations 自动选择是否执行 downstream purification sequence。

LLM 相关组件当前是可复现 adapter/replay 层，不是已经验证过的 autonomous chemical agent。任何在线 LLM 结果都应报告模型名、调用日期、prompt、temperature、成本、缓存策略和 replay artifact。

## 9. 数据、日志与提交协议

### 9.1 Trajectory JSONL

每一步记录：

- task info；
- step；
- action；
- observation；
- reward；
- terminated/truncated；
- info；
- agent metadata；
- timestamp。

这使得一次实验可以被：

- validate；
- evaluate；
- replay verify；
- anonymize；
- aggregate leaderboard。

### 9.2 Submission Bundle

正式提交包结构为：

```text
submission/
├── manifest.json
├── trajectories/
├── results/
└── explanations/   # optional
```

CLI 支持：

```bash
chemworld submission init
chemworld submission validate
chemworld submission summarize
```

manifest 记录：

- agent name；
- agent family；
- platform version；
- commit hash；
- dependency file；
- command used；
- task id；
- seeds；
- LLM metadata if applicable。

## 10. Evaluation 与 Leaderboard

当前 evaluation 使用 final-assay `leaderboard_score` 作为正式性能来源。中间 HPLC、GC、UV-vis 的观测可以给 agent 在线反馈，但不会直接成为 leaderboard 成绩。

核心指标：

- final best score；
- best valid score；
- best valid yield；
- area under best score；
- sample efficiency；
- safety violations；
- high cost violations；
- mean cost；
- mean safety risk；
- safety-aware score；
- total score；
- public/private gap。

解释质量目前作为结构化研究字段和 rubric artifact，不进入默认自动总分。后续 leaderboard 应区分两类：

- Performance Leaderboard：只使用自动化指标；
- Scientific Understanding Leaderboard：结合 performance、mechanism explanation 和 counterfactual prediction。

## 11. CLI 工作流

常用命令：

```bash
chemworld tasks list
chemworld tasks show reaction-optimization-standard
chemworld tasks card reaction-optimization-standard

chemworld run --task reaction-optimization-standard --agent scripted_chemistry
chemworld run --task reaction-to-purification --agent scripted_chemistry

chemworld evaluate --submission runs/example.jsonl
chemworld verify --constitution --submission runs/example.jsonl
chemworld suite --task reaction-optimization-standard --agent gp_bo
chemworld leaderboard --results results/*.json

chemworld submission init submissions/example --task-id reaction-optimization-standard
chemworld submission validate submissions/example
chemworld submission summarize submissions/example

chemworld inspect-constitution --env ChemWorld
```

## 12. 可复现性设计

当前可复现性由以下机制保证：

- `world_split + seed + private salt` 生成 world parameters；
- task 固定 budget、objective、seeds、allowed operations；
- trajectory JSONL 记录完整 action 和 info；
- manifest 记录命令、版本、依赖、commit；
- replay verifier 重放 transition 和 observation；
- private-eval 可通过 `CHEMWORLD_PRIVATE_EVAL_SALT` 生成维护者隐藏参数。

当前 private-eval 仍是本地可运行的 placeholder/private-salt 双模式。正式公开榜单后，应由维护者侧隐藏 registry 或签名评测包执行。

## 13. 当前验证状态

当前验证命令：

```bash
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy src\chemworld
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

当前结果：

```text
ruff: passed
mypy: passed
pytest: 44 passed
mkdocs build --strict: passed
```

notebook JSON 有效性也已抽查：

```text
valid_notebooks=14
```

## 14. 当前边界

当前平台仍然明确不做：

- 真实反应预测软件；
- DFT 或分子动力学；
- 真实机器人实验接入；
- 在线账号系统；
- 自动防作弊云端竞赛；
- 通用 chemical world model 宣称。

当前目标是：

> 在受限、半机理、部分可观测、有限预算的虚拟物理化学世界中，研究 human、optimizer、LLM agent、human+LLM 如何进行闭环实验决策、局部 world model learning、多目标优化和机制解释。

## 15. 后续建议

### P0：Benchmark 硬化

- 为每个 task 增加 task card。
- 固化 baseline reference table。
- 增加 Gymnasium checker 测试。
- 增加 signed private-eval result artifact。
- 提供 paper artifact 一键脚本。

### P1：数据与发布

- JSONL 转 Parquet/HDF5。
- dataset card。
- human pilot anonymization report。
- public/private gap calibration。
- 更稳定的 private registry 流程。

### P2：世界模块扩展

继续坚持“同一 world law 下扩展模块”，而不是注册互不相干的新小游戏。优先候选：

- crystallization；
- continuous flow；
- distillation；
- electrochemistry；
- solid handling。

这些模块应复用 ontology、constitution、state ledger、operation language、observation kernel 和 task registry。
