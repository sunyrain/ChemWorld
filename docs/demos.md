# 演示

本页整理 ChemWorld 的最小演示路径。目标是让读者先跑通一次可解释流程，再进入自动化
agent 或课程 notebook。

## 教程课程

完整课程路线见 [ChemWorld 教程课程地图](tutorial_curriculum_zh.md)。课程从环境 reset
和单步 action 开始，逐步进入 recipe、baseline、任务族、光谱、分离和 agent planning。

## 手动事件序列

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

## Agent-Facing API

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
python scripts/probe_tool_agent_rounds.py --seeds 0 1 2 --budget 18 --min-rounds 12
```

## Baseline 对比

建议至少比较三类：

- 随机合法动作 baseline；
- 固定 recipe baseline；
- 简单 optimizer 或 tool-agent baseline。

不要只报告平均 reward，也要报告 invalid action、safety、cost 和 selectivity flags。

## 验证与检查

```bash
python -m pytest
python scripts/audit_environment_consistency.py --tasks all --seeds 0 1 2
python -m mkdocs build --strict
```

## CLI 等价入口

未来可把 notebook 示例收束成 CLI：

```bash
chemworld run --task reaction-to-purification --agent baseline_recipe --seed 1
chemworld score --run artifacts/runs/example.jsonl
```

## 本地评测机

本地评测机接收 agent、任务和 seeds，输出 trajectory、score 和 report。见
[本地评测机](local_eval_machine.md)。

## 提交包示例

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

## Notebook 走读

Notebook 应保持短小：每个 notebook 聚焦一个概念，避免把全部任务、全部指标和全部
debug 信息塞进同一页。

## 端到端闭环 Notebook

预发布包现在提供三份完整闭环 notebook，位置在 `notebooks/end_to_end/`：

| Notebook | 任务 | 覆盖内容 |
| --- | --- | --- |
| `reaction_to_assay_end_to_end.ipynb` | `reaction-to-assay` | 任务规划、action validation、中间 HPLC、final assay、谱图和下一轮实验 |
| `reaction_to_purification_end_to_end.ipynb` | `reaction-to-purification` | 反应、相系统、萃取、分相、洗涤、干燥、浓缩、final assay |
| `partition_discovery_end_to_end.ipynb` | `partition-discovery` | campaign 多轮实验、分配趋势、final assay packet、局部 world model |

它们不是最高分策略，而是可验证流程模板：每份都包含 planning、execution、spectra、metrics 和 reflection。

## 十二天教程

课程应先让学生理解 `reset`、`step`、`info` 和 `constraint_flags`，再逐步引入
reaction、separation、spectroscopy、world-model learning 和 tool-agent planning。
