# 四种 Agent 如何与环境交互

RL、贝叶斯优化、LLM tool agent 和人类学生可以运行同一个任务，但它们的学习位置和决策频率不同。
比较方法前，先说清楚它在**什么时候更新、读取哪些信息、消耗哪些资源**。

## RL：每个操作都可以是一个决策

```python
import gymnasium as gym
import chemworld
from chemworld.wrappers import RLObservationWrapper

env = RLObservationWrapper(
    gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
)
observation, info = env.reset(seed=0)

observation, reward, terminated, truncated, info = env.step(
    {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2}
)
```

RL 视图提供固定长度向量、观测 mask 和 cost signal。正式训练还要把 Train、Dev 与 Bench 分开：
Train 用于更新参数，Dev 用于选择 checkpoint，Bench 只运行冻结策略。未训练 policy 或短 smoke
可以验证接口，但不构成方法结果。

## BO：每个完整实验是一个 Trial

在 campaign 任务里，BO 通常完成一整套 recipe，读取 final assay，再选择下一次实验：

```python
prompt = env.unwrapped.task_prompt()
progress = env.unwrapped.campaign_state()
actions = env.unwrapped.available_actions()
```

如果方法只在两次终检之间更新 recipe，它属于**实验间主动学习**。只有当它根据同一实验的中间
测量调整后续 operation 时，才属于**实验内闭环控制**。

## LLM：读取报告，再选择一个工具动作

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

task = info["task_prompt"]["text"]
report = info["lab_report"]["text"]
actions = info["available_actions"]
```

每次执行后，模型可以读取最新实验报告、结构化公开观测、合法动作与 campaign 进度。在线运行应保留
公开 evidence、假设、不确定性、谱图解释和简短依据；私有逐字思维链不请求也不保存。超时、重试、
token 与费用都属于方法资源。

## 人类与学生：从实验报告出发

```python
print(env.unwrapped.task_prompt()["text"])
print(env.unwrapped.observation_view("lab_report")["text"])
```

一份有意义的课程提交不应只有运行截图，还应包含：

- 完整 trajectory JSONL；
- 自己整理的实验表格或图；
- 当前机制假设与支持证据；
- 下一轮实验建议；
- 使用 GPT 或其它工具的说明。

## 比较时不要混淆这些层级

| 方法 | 常见更新频率 | 典型资源 |
| --- | --- | --- |
| RL | 每个 operation | 训练环境步、checkpoint、GPU/CPU |
| BO / 主动学习 | 每个完整 experiment | 实验数、surrogate 拟合与 acquisition 时间 |
| LLM tool agent | 每个 operation 或计划周期 | 请求数、token、费用、重试 |
| Human / Student | 人工决策 | 时间、允许工具和提示条件 |

最终分数相同，不代表这些方法使用了相同信息或成本。公平口径见
[设计公平评测](benchmark_protocol.md)。

!!! warning "所有示例只使用公开观测"
    Agent 不应读取 `env.unwrapped._state`、隐藏 ledger 或 debug truth。它们只用于环境开发、测试和
    审计。
