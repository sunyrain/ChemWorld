# Agent-Facing Interface

ChemWorld 的正式 Gym 入口仍是：

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=0)
obs, info = env.reset(seed=0)
```

本层提供 agent 可直接调用的公开交互接口，目标是让 RL、BO、LLM 和学生不需要阅读内部 runtime，也能理解任务、检查动作、读取观测、恢复错误并复现实验。

## Env Methods

```python
env.task_prompt()
env.available_actions()
env.action_schema("heat")
env.validate_action({"operation": "heat", "duration_s": 10.0})
env.observation_view("tool_json")
env.observation_view("lab_report")
env.observation_view("rl")
env.campaign_state()
```

## Task Prompt

`task_prompt()` 返回两层信息：

- `text`：给 LLM、学生或人类 reviewer 阅读的紧凑任务说明。
- 结构化字段：给 tool agent、planner、dataset exporter 和 replay harness 使用。

当前结构化字段包括：

| 字段 | 含义 |
| --- | --- |
| `task_goal` | 当前任务的自然语言目标 |
| `constraints` | 预算、episode mode、安全、前置条件等约束 |
| `success_criteria` | agent 应优化或满足的成功标准 |
| `allowed_tools` | 可用 operation、operation group 和 instrument |
| `measurement_policy` | 仪器观测的成本、噪声和终端测量规则 |
| `recommended_strategy` | 不读取 hidden truth 的任务策略建议 |
| `failure_modes` | 常见失败模式 |
| `hidden_information_policy` | 明确说明不可见的 hidden state / mechanism 信息 |
| `submission_requirements` | trajectory、manifest 和复现实验命令要求 |

三项预发布任务已有专门 prompt profile：

| Task | Prompt 重点 |
| --- | --- |
| `reaction-to-assay` | 单实验闭环，从投料到 `final_assay`；强调合法终止、final assay score 和 trajectory validity。 |
| `reaction-to-purification` | 反应、相分离、洗涤/干燥/浓缩和终端检测；强调 purity、recovery、mass balance 和 final assay。 |
| `partition-discovery` | campaign 式分配规律学习；强调 phase ratio、organic/aqueous enrichment、有限测量和 hidden partition policy。 |

`task_prompt()` 是 public view。它不会泄露 hidden species id、hidden amounts、rate constants、partition coefficients、mechanism internals 或 private scenario 参数。

## Action Affordance

`available_actions()` 返回当前 state 下真正可执行的 operation affordance。每个条目包含：

- `operation`
- `valid`
- `invalid_reasons`
- `preconditions`
- `schema`

`action_schema(operation)` 返回单个 operation 的 JSON-friendly schema，包括 required fields、单位、推荐范围和 categorical choices。

`validate_action(action)` 只检查，不执行，不改变 state。它复用 `OperationValidator`，覆盖 schema、task policy、instrument policy 和 stateful preconditions。

## Observation Views

`observation_view("rl")` 输出 NaN-safe vector、mask、cost 和 constraint flags，适合 RL 或 bandit-style agent。

RL view 使用固定合同：

| 字段 | 含义 |
| --- | --- |
| `schema_version` | 当前为 `chemworld-rl-view-0.2` |
| `keys` | `OBSERVATION_KEYS` 加可选 `cost_signal` |
| `vector` | NaN-safe float vector；缺失观测写为 `-1.0` |
| `mask` | 与 `vector` 对齐的 observed mask，取值为 `0.0` 或 `1.0` |
| `bounds` | vector 的低/高界；观测值为 `[-1, 1]`，cost 为 `[0, 1]` |
| `mask_bounds` | mask 的低/高界 `[0, 1]` |
| `cost` | safety/cost channel，来自 public info |

`RLObservationWrapper` 使用同一份 RL spec 构造 Gymnasium `Box` observation space，因此 wrapper 输出、`info["rl_view"]` 和 `info["observation_mask"]` 的长度与 bounds 保持一致。

`observation_view("tool_json")` 输出机器可读 dict：public observation、raw signal、processed estimate、uncertainty、cost、constraints、campaign state、available actions 和 lab report。

`observation_view("lab_report")` 输出 LLM/学生可读实验摘要。它只由 public observation/info 派生，不读取 hidden species amounts、rate constants 或 private scenario 参数。

`lab_report` 当前包含：

| 字段 | 含义 |
| --- | --- |
| `visible_metrics` | 从 public observation 中提取的有限数值指标 |
| `instrument_summary` | 当前 instrument、observed keys、measurement cost、sample consumption |
| `spectra_summary` | public peak group fractions、dominant peak、spectral channels、warnings |
| `final_assay_summary` | 是否 final assay、leaderboard score、episode/campaign terminal 状态 |
| `campaign_progress` | step/budget、experiment index、remaining budget、final assay count、best score |
| `failure_summary` | precondition/constitution/rollback/error 摘要 |
| `next_action_hints` | 当前可执行 operation 的有限列表 |
| `recovery_suggestion` | 失败动作后的恢复建议 |

报告文本固定由这些 public 字段渲染，因此可用于 LLM prompt、课堂日志和 replay dataset。

## Wrappers

```python
from chemworld.wrappers import (
    AgentInfoWrapper,
    LLMObservationWrapper,
    RLObservationWrapper,
    ActionSuggestionWrapper,
)
```

| Wrapper | 行为 |
| --- | --- |
| `AgentInfoWrapper` | 在 reset/step info 中加入 `task_prompt`、`campaign_state` 和 `available_actions`。 |
| `LLMObservationWrapper` | 在 info 中加入 `lab_report` 和 `tool_json`。 |
| `RLObservationWrapper` | 返回 vector observation，并在 info 中加入 `rl_view`、`observation_mask` 和 `cost_signal`。 |
| `ActionSuggestionWrapper` | 暴露合法动作建议和失败恢复建议，不自动修正 agent 提交的 action。 |

## Design Rule

Agent-facing 接口是 public protocol，不是 debug truth。它提供规划所需的 affordance、schema、任务合同和观测摘要，但不暴露 hidden world internals。
