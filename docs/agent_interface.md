# 从 Agent 接口开始

Agent 不需要理解 ChemWorld 的内部 runtime。它只需要回答四个问题：**目标是什么、现在能做什么、
刚才看到了什么、下一步是否值得做。** 这些信息都通过公开接口提供。

## 创建环境

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=0)
observation, info = env.reset(seed=0)
```

## 最常用的六个接口

```python
env.unwrapped.task_prompt()                 # 这项任务要解决什么
env.unwrapped.available_actions()           # 当前真正能做什么
env.unwrapped.action_schema("heat")         # 参数应该怎么写
env.unwrapped.validate_action(action)       # 动作是否合法，但不执行
env.unwrapped.observation_view("tool_json") # 机器可读的公开观测
env.unwrapped.campaign_state()              # 预算与实验进度
```

建议的循环很简单：

```text
读取任务与进度 → 查看合法动作 → 生成并校验 Action
→ env.step() → 读取新观测 → 更新策略
```

## 读懂任务说明

`task_prompt()` 同时返回自然语言说明和结构化字段。LLM 可以阅读 `text`，程序化 Agent 可以直接
消费其余字段。

| 字段 | Agent 可以从中得到什么 |
| --- | --- |
| `task_goal` | 当前实验要优化或确认的目标 |
| `constraints` | 预算、episode 模式、安全边界和前置条件 |
| `success_criteria` | 怎样才算完成任务 |
| `allowed_tools` | 可以使用的 operation、operation group 和 instrument |
| `measurement_policy` | 测量的成本、噪声与终检规则 |
| `recommended_strategy` | 不依赖隐藏信息的起步建议 |
| `failure_modes` | 最常见的失败方式 |
| `submission_requirements` | 轨迹、manifest 与复现要求 |

例如，`reaction-to-assay` 强调完成一次合法终检；`reaction-to-purification` 还要求兼顾纯度、回收率
和物料闭合；`partition-discovery` 则要求在多次实验中学习隐藏分配规律。

## 只生成当前可执行的动作

`available_actions()` 的每个条目都包含：

- `operation`：操作名；
- `valid` 与 `invalid_reasons`：现在是否可做，以及为什么；
- `preconditions`：还缺少哪些状态条件；
- `schema`：所需字段、单位、范围与类别选项。

`validate_action(action)` 复用环境的正式校验器，只检查、不执行，也不会消耗预算。对于需要连续运行的
Agent，这比提交后再用异常处理猜测规则更稳定。

## 为不同 Agent 选择观测视图

=== "RL"

    `observation_view("rl")` 返回固定长度、NaN-safe 的向量视图：

    | 字段 | 内容 |
    | --- | --- |
    | `vector` | 未观测值填为 `-1.0` 的数值向量 |
    | `mask` | 与向量对齐的观测 mask |
    | `bounds` | 每个维度的上下界 |
    | `cost` | 来自公开信息的 safety/cost channel |

    `RLObservationWrapper` 使用同一份 spec 构造 Gymnasium `Box`，因此 observation space、mask 和
    `info["rl_view"]` 保持一致。

=== "LLM / Tool Agent"

    `observation_view("tool_json")` 返回机器可读字典，包括公开观测、仪器信号、不确定性、约束、
    campaign 进度和可用动作。

    `observation_view("lab_report")` 把同样的信息整理成短实验报告，适合放入 prompt 或课堂记录。

=== "人类与教学"

    `lab_report` 会突出可见指标、仪器摘要、终检状态、预算、失败原因和下一步提示。它不会展示
    隐藏物种量、速率常数或 private-eval 参数。

## 失败后如何恢复

动作被拒绝时，优先读取：

```python
check["invalid_reasons"]
info["failure_summary"]
info["recovery_suggestion"]
env.unwrapped.available_actions()
```

恢复建议只解释公开前置条件，不会替 Agent 自动修正或执行动作。这样既能减少无意义失败，也保留
方法本身的决策责任。

## 用 Wrapper 减少样板代码

```python
from chemworld.wrappers import (
    AgentInfoWrapper,
    LLMObservationWrapper,
    RLObservationWrapper,
    ActionSuggestionWrapper,
)
```

| Wrapper | 主要作用 |
| --- | --- |
| `AgentInfoWrapper` | 在 reset/step 的 `info` 中加入任务、进度与合法动作 |
| `LLMObservationWrapper` | 加入 `lab_report` 和 `tool_json` |
| `RLObservationWrapper` | 直接返回向量 observation，并附带 mask 与 cost |
| `ActionSuggestionWrapper` | 加入合法动作和恢复建议，不自动替 Agent 改动作 |

更多组合方式见[使用 Wrapper](wrappers.md)。

!!! warning "公开接口不是调试真值"
    Agent 逻辑应停留在 task prompt、Action、公开观测和轨迹层。`_state`、隐藏 ledger、机理参数与
    private scenario 只供环境测试和审计使用，不属于方法输入。
