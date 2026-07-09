# Agent-Facing Interface

ChemWorld 的正式 Gym 入口仍是 `gym.make("ChemWorld", task_id=...)`。本层新增的是 agent 能直接调用的公开交互接口，目标是让 RL、BO、LLM 和学生不需要阅读内部 runtime 代码，也能理解任务、检查动作、读取观测并恢复错误。

## Env Methods

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=0)
obs, info = env.reset(seed=0)

env.task_prompt()
env.available_actions()
env.action_schema("heat")
env.validate_action({"operation": "heat", "duration_s": 10.0})
env.observation_view("tool_json")
env.observation_view("lab_report")
env.observation_view("rl")
env.campaign_state()
```

`task_prompt()` 返回自然语言任务说明和结构化字段：任务目标、预算、可用操作、可用仪器、成功指标、安全限制和隐藏信息政策。

`available_actions()` 返回当前 state 下真正可执行的 operation affordance，每个条目带 schema、preconditions 和 invalid reason 摘要。

`action_schema(operation)` 返回单个 operation 的 JSON-friendly schema，包括 required fields、单位、推荐范围和 categorical choices。

`validate_action(action)` 只检查，不执行，不改变 state。它复用 `OperationValidator`，覆盖 schema、task policy、instrument policy 和 stateful preconditions。

`campaign_state()` 返回 campaign id、experiment index、operation count、remaining budget、final assay count、best score 和 last terminal summary。

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

`AgentInfoWrapper` 在 reset/step info 中加入 `task_prompt`、`campaign_state` 和 `available_actions`。

`LLMObservationWrapper` 在 info 中加入 `lab_report` 和 `tool_json`。

`RLObservationWrapper` 返回 vector observation，并在 info 中加入 `rl_view`、`observation_mask` 和 `cost_signal`。

`ActionSuggestionWrapper` 只暴露合法动作建议和失败恢复建议，不自动修正 agent 提交的 action。

## Design Rule

Agent-facing 接口是 public view，不是 debug truth。它不会泄露 hidden species id、hidden amounts、rate constants、partition coefficients 或 private eval 参数。
