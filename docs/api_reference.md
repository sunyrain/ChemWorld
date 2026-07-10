# API 参考

本页给出 ChemWorld 当前最小 API 面。字段名保持英文，因为它们是包的稳定接口。

## 环境

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=1)
obs, info = env.reset(seed=1)
obs, reward, terminated, truncated, info = env.step(action)
```

`info` 中应包含任务元数据、约束 flags、评分细节和可选调试信息。

## 任务

```python
env.task_info()
env.task_prompt()
env.available_actions()
env.action_schema("heat")
env.validate_action(action)
env.observation_view("tool_json")
env.observation_view("lab_report")
env.observation_view("rl")
env.campaign_state()
```

任务信息应说明 `task_id`、`world_law_id`、maturity、预算、指标、允许操作和主要约束。
agent-facing 方法是推荐的交互入口；它们只聚合公开 task、validator、observation 和
campaign bookkeeping，不读取 hidden truth。

任务 registry 与严肃任务 readiness：

```python
from chemworld.task_design import serious_task_readiness_manifest
from chemworld.tasks import get_task, list_tasks

task = get_task("flow-reaction-optimization")
manifest = serious_task_readiness_manifest()
```

## Wrapper

常用 wrapper：

- `ActionMaskWrapper`
- `SafetyCostWrapper`
- `NaNObservationWrapper`
- `AgentInfoWrapper`
- `LLMObservationWrapper`
- `RLObservationWrapper`
- `ActionSuggestionWrapper`

Wrapper 不改变底层任务语义，只增强 agent 训练和诊断时的可用性。

## Agent

Agent 最小形态是一个接收 observation 并返回 action 的对象或函数。正式评测应固定随机
种子、超时、资源限制和输出目录。

## 轨迹

Trajectory 应保存每一步的 action、observation、reward、termination、truncation 和
`info` 摘要。用于公开数据集时，还需要 manifest 和 task maturity metadata。
