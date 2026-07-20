# 跟着示例学习

示例按“先看懂一次实验，再逐步自动化”的顺序排列。第一次使用建议先运行手动事件序列，然后根据
目标进入 Agent API、Baseline、提交验证或 Notebook。

| 你想学习什么 | 从哪里开始 |
| --- | --- |
| 一条实验路线怎样执行 | 手动事件序列 |
| Agent 怎样读取公开接口 | Agent-Facing API |
| 多种方法怎样比较 | Baseline 对比 |
| 怎样生成可提交结果 | 验证与提交包示例 |
| 怎样完成系统课程 | 十二天教程 |

## 先选择学习路线

完整课程路线见 [ChemWorld 教程课程地图](tutorial_curriculum_zh.md)。课程从环境 reset
和单步 action 开始，逐步进入 recipe、baseline、任务族、光谱、分离和 agent planning。

## 运行一条手动实验路线

最小示例：

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=1)
obs, info = env.reset(seed=1)

recipe = [
    {"operation": "add_solvent", "volume_L": 0.03, "solvent": 1},
    {"operation": "add_reagent", "amount_mol": 0.012},
    {"operation": "add_catalyst", "catalyst": 2, "catalyst_amount_mol": 0.0004},
    {
        "operation": "heat",
        "target_temperature_K": 350.0,
        "duration_s": 1200.0,
        "stirring_speed_rpm": 800.0,
    },
    {"operation": "quench"},
    {"operation": "terminate"},
    {"operation": "measure", "instrument": "final_assay"},
]

for action in recipe:
    obs, reward, terminated, truncated, info = env.step(action)
    print(action["operation"], reward, info.get("constraint_flags", {}))
    if terminated or truncated:
        break
```

如果 reward 始终为 0，应先检查任务阶段、前置条件和最终 measurement 是否真的触发评分。

## 让 Agent 使用公开接口

```python
print(env.unwrapped.task_prompt()["text"])
env.unwrapped.available_actions()
env.unwrapped.action_schema("heat")
env.unwrapped.validate_action({"operation": "heat", "duration_s": 10.0})
env.unwrapped.observation_view("lab_report")
env.unwrapped.campaign_state()
```

也可以直接运行：

```bash
python examples/demo_agent_facing_api.py
python examples/demo_llm_replay_harness.py
python examples/demo_rl_vector_wrapper.py
python examples/demo_dataset_agent_trace_export.py
python examples/demo_submission_bundle.py
```

## 比较几个 Baseline

建议至少比较三类：

- 随机合法动作 baseline；
- 固定 recipe baseline；
- 简单 optimizer 或 tool-agent baseline。

不要只报告平均 reward，也要报告 invalid action、safety、cost 和 selectivity flags。

## 验证轨迹与安装

```bash
chemworld verify --constitution --submission runs/<trajectory>.jsonl
chemworld evaluate --submission runs/<trajectory>.jsonl
```

这些命令会检查合同、回放和指标重算。运行 Agent 的完整公开入口见[本地评测机](local_eval_machine.md)，
不要依赖尚未发布的占位命令。

## 模拟教师端评测

本地评测机接收 agent、任务和 seeds，输出 trajectory、score 和 report。见
[本地评测机](local_eval_machine.md)。

## 生成提交包

构建一个完整、可验证、可回放的 submission bundle：

```bash
chemworld submission example runs/example_submission \
  --task-id reaction-to-purification \
  --agent tool_using_llm_stub \
  --seeds 0
chemworld submission validate runs/example_submission
chemworld submission summarize runs/example_submission
```

该示例会生成 manifest、trajectory、results、explanations、dependency notes 和 README。
详情见 [提交包](submission.md)。

## 用 Notebook 逐步探索

Notebook 应保持短小：每个 notebook 聚焦一个概念，避免把全部任务、全部指标和全部
debug 信息塞进同一页。

## 运行端到端闭环 Notebook

仓库提供三份完整闭环 notebook，位置在 `notebooks/end_to_end/`：

| Notebook | 任务 | 覆盖内容 |
| --- | --- | --- |
| `reaction_to_assay_end_to_end.ipynb` | `reaction-to-assay` | 任务规划、action validation、中间 HPLC、final assay、谱图和下一轮实验 |
| `reaction_to_purification_end_to_end.ipynb` | `reaction-to-purification` | 反应、相系统、萃取、分相、洗涤、干燥、浓缩、final assay |
| `partition_discovery_end_to_end.ipynb` | `partition-discovery` | campaign 多轮实验、分配趋势、final assay packet、局部 world model |

它们不是最高分策略，而是可验证流程模板：每份都包含 planning、execution、spectra、metrics 和 reflection。

## 浏览六个研究任务 Demo

`notebooks/task_demos/` 一一覆盖当前六个 serious research tasks。与上面的流程教学不同，这组 Demo
把操作看作干预、把测量看作公开反馈，重点展示同一干预在不同隐藏规律下产生的可观测差异。

| Notebook | Task | World-model 观察重点 |
| --- | --- | --- |
| `01_partition_discovery.ipynb` | `partition-discovery` | 分配构成律与相条件响应 |
| `02_reaction_crystallization.ipynb` | `reaction-to-crystallization` | 上游动力学到下游结晶的耦合传播 |
| `03_reaction_distillation.ipynb` | `reaction-to-distillation` | 隐藏反应通道与馏分反馈 |
| `04_flow_reaction.ipynb` | `flow-reaction-optimization` | 流量、停留时间、温度与速率律 |
| `05_electrochemical_conversion.ipynb` | `electrochemical-conversion` | 诊断反馈与电化学构成律 |
| `06_equilibrium_characterization.ipynb` | `equilibrium-characterization` | 浓度探针与非理想平衡响应 |

每份 notebook 都读取公开 task card，使用任务自身的 recipe adapter 生成三组候选干预，展示完整测量
轨迹，并执行一次 World A/World B 配对控制。配对条件由教学代码构造；Agent-facing 数据不会包含
隐藏机理名称、参数或 hidden state。这些 notebook 展示环境能力，不实现或要求特定训练算法。

## 完成十二天教程

课程应先让学生理解 `reset`、`step`、`info` 和 `constraint_flags`，再逐步引入
reaction、separation、spectroscopy、world-model learning 和 tool-agent planning。
