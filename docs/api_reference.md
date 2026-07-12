# 查阅 API

这里集中列出最常用的稳定入口。第一次开发 Agent 时，建议先阅读带解释和循环示例的
[Agent 接口](agent_interface.md)，再把本页当作速查表。

## 创建并运行环境

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=1)
observation, info = env.reset(seed=1)
observation, reward, terminated, truncated, info = env.step(action)
```

## Agent-facing 方法

```python
env.unwrapped.task_info()
env.unwrapped.task_prompt()
env.unwrapped.available_actions()
env.unwrapped.action_schema("heat")
env.unwrapped.validate_action(action)
env.unwrapped.observation_view("tool_json")
env.unwrapped.observation_view("lab_report")
env.unwrapped.observation_view("rl")
env.unwrapped.campaign_state()
```

这些方法聚合公开任务、校验器、观测和 campaign 账本，不读取 hidden truth。

## 读取任务 Registry

```python
from chemworld.task_design import serious_task_readiness_manifest
from chemworld.tasks import get_task, list_tasks

task = get_task("flow-reaction-optimization")
all_tasks = list_tasks()
readiness = serious_task_readiness_manifest()
```

## 常用 Wrapper

```python
from chemworld.wrappers import (
    ActionMaskWrapper,
    SafetyCostWrapper,
    NaNObservationWrapper,
    AgentInfoWrapper,
    LLMObservationWrapper,
    RLObservationWrapper,
    ActionSuggestionWrapper,
)
```

Wrapper 的输入输出和选择建议见[使用 Wrapper](wrappers.md)。

## 轨迹与提交

Trajectory 保存每一步的 Action、observation、reward、termination、truncation 和公开 `info` 摘要。
公开数据还应附带 manifest、合同摘要、任务成熟度与 replay 状态。命令行流程见
[打包并提交结果](submission.md)。
