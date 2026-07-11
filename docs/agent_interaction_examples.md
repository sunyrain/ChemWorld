# Agent Interaction Examples

ChemWorld 支持四类典型交互方式：RL、主动学习/BO、LLM tool agent 和 human/student。它们共享
任务和轨迹合同，但学习阶段、决策频率与资源字段不同，不能只按最终分数混为一个方法列表。

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

正式 RL 结果还必须区分训练与评测：训练只使用 Train worlds，Dev 只用于 checkpoint 选择，Bench
运行不得继续更新。未训练 policy 或短 smoke 只能验证接口。

## BO

BO agent 在 campaign task 中把每个完整 experiment 当作一次 trial。推荐读取：

- `env.task_prompt()`
- `env.available_actions()`
- `env.validate_action(action)`
- `env.campaign_state()`
- final assay 的 `leaderboard_score`

若方法只在终检后选择下一 recipe，应报告为实验间主动学习；只有根据同一实验的中间测量改变后续
operation，才属于实验内自适应控制。

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

在线运行保存结构化 evidence、谱图解读、假设、不确定性和 action rationale，不保存私有逐字
思维链。失败请求、重试、token 和费用必须计入资源账本。

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
