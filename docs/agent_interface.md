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

`observation_view("tool_json")` 输出机器可读 dict：public observation、raw signal、processed estimate、uncertainty、cost、constraints、campaign state、available actions 和 lab report。

`observation_view("lab_report")` 输出 LLM/学生可读实验摘要。它只由 public observation/info 派生，不读取 hidden species amounts、rate constants 或 private scenario 参数。

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
