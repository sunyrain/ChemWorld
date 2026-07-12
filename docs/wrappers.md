# 使用 Wrapper

Wrapper 把同一个 ChemWorld 环境整理成更适合 RL、LLM 或调试的视图，但不会改变任务目标、预算
或底层状态转移。

## 怎么选

| Wrapper | 适合谁 | 提供什么 |
| --- | --- | --- |
| `AgentInfoWrapper` | 通用 Agent | 在 `info` 中加入任务说明、campaign 状态和合法动作 |
| `LLMObservationWrapper` | LLM / tool agent | 人类可读 `lab_report` 与机器可读 `tool_json` |
| `RLObservationWrapper` | RL / bandit | 固定长度向量、观测 mask、bounds 与 cost signal |
| `ActionSuggestionWrapper` | 教程与恢复策略 | 合法动作和失败后的恢复建议，不代替 Agent 决策 |
| `ActionMaskWrapper` | RL / 搜索 | 当前可能合法的 operation mask |
| `SafetyCostWrapper` | 安全约束学习 | 更直接的安全与成本通道 |
| `NaNObservationWrapper` | 调试 | 检查 NaN、inf 与形状异常 |

## 组合示例

```python
import gymnasium as gym
import chemworld
from chemworld.wrappers import AgentInfoWrapper, LLMObservationWrapper

env = AgentInfoWrapper(
    LLMObservationWrapper(
        gym.make("ChemWorld", task_id="reaction-to-purification", seed=0)
    )
)
observation, info = env.reset(seed=0)
print(info["lab_report"]["text"])
```

## 两个容易踩的坑

1. Wrapper 提供的便利信息也是交互资源。正式比较时要声明方法能否读取 action mask、恢复建议等字段。
2. `SafetyCostWrapper` 可以重排训练信号，但不应覆盖原始 `constraint_flags`；原始轨迹仍是验证依据。

Wrapper 不是 oracle，也不应读取隐藏状态替 Agent 做决定。完整公开接口见
[从 Agent 接口开始](agent_interface.md)。
