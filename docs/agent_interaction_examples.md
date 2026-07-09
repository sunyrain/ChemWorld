# Agent Interaction Examples

ChemWorld 现在支持四类典型交互方式：RL、BO、LLM/tool agent 和 human/student。

## RL

```python
import gymnasium as gym
import chemworld
from chemworld.wrappers import RLObservationWrapper

env = RLObservationWrapper(gym.make("ChemWorld", task_id="reaction-to-assay", seed=0))
obs, info = env.reset(seed=0)

obs, reward, terminated, truncated, info = env.step(
    {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2}
)
```

RL wrapper 返回 NaN-safe vector，并通过 `info["observation_mask"]`、`info["cost_signal"]` 暴露 mask 和 cost。

## BO

BO agent 可以使用 recipe 或 terminal assay 作为评价单位，也可以在 campaign task 中把每个 experiment 当作一次完整 trial。推荐读取：

- `env.task_prompt()`
- `env.available_actions()`
- `env.validate_action(action)`
- `env.campaign_state()`
- final assay 的 `leaderboard_score`

## LLM / Tool Agent

```python
import gymnasium as gym
import chemworld
from chemworld.wrappers import LLMObservationWrapper, AgentInfoWrapper

env = AgentInfoWrapper(
    LLMObservationWrapper(gym.make("ChemWorld", task_id="reaction-to-purification", seed=0))
)
obs, info = env.reset(seed=0)

prompt = info["task_prompt"]["text"]
actions = info["available_actions"]
```

每一步执行后，LLM 可以读取：

- `info["lab_report"]["text"]`
- `info["tool_json"]`
- `info["available_actions"]`
- `info["campaign_state"]`

## Human / Student

学生可以使用相同接口，但通常从 `lab_report` 和 `available_actions` 开始：

```python
print(env.unwrapped.task_prompt()["text"])
print(env.unwrapped.observation_view("lab_report")["text"])
```

课程要求不应只是跑代码，而是提交：

- 轨迹 JSONL；
- 自己的实验表格和图；
- 机制假设；
- 下一轮实验建议；
- 对 GPT/工具使用方式的记录。

## Important Boundary

所有交互示例都只使用 public observation。不要在 agent 逻辑中读取 `env.unwrapped._state`、hidden ledgers 或 debug truth；这些只用于测试、审计和环境开发。
