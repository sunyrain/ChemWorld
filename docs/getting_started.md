# 安装与首次运行

本页带你从源码安装 ChemWorld，运行一次合法 episode，并验证生成的轨迹。推荐 Python 3.11
或更高版本。

## 安装

```bash
git clone https://github.com/sunyrain/ChemWorld.git
cd ChemWorld
python -m pip install -e ".[dev]"
```

需要构建文档或执行完整科学参考门禁时：

```bash
python -m pip install -e ".[dev,docs,physchem-ref]"
```

## 创建环境

```python
import gymnasium as gym
import chemworld  # 注册 ChemWorld 环境

env = gym.make(
    "ChemWorld",
    task_id="reaction-to-assay",
    seed=0,
)

observation, info = env.reset(seed=0)
print(info["task_id"], info["physics_maturity"])
```

未测量的 observation 字段使用 `NaN`；JSONL 轨迹中对应值为 `null`。请始终结合
`observed_mask` 或 `observed_keys` 判断信息是否真正可见。

## 运行第一个合法流程

```python
actions = [
    {"operation": "add_solvent", "volume_L": 0.025, "solvent": 1},
    {"operation": "add_reagent", "amount_mol": 0.010},
    {"operation": "heat", "target_temperature_K": 360.0, "duration_s": 600.0},
    {"operation": "terminate"},
    {"operation": "measure", "instrument": "final_assay"},
]

for action in actions:
    observation, reward, terminated, truncated, info = env.step(action)
    if info["constraint_flags"]["precondition_failed"]:
        raise RuntimeError(info["invalid_reasons"])
    if terminated or truncated:
        break

env.close()
```

不同任务允许的操作、仪器、预算和终止条件不同。不要硬编码一套流程到所有任务；从 reset
返回的任务信息或[任务卡](task_cards.md)读取合同。

## 使用 CLI

```bash
chemworld run --task reaction-to-assay --agent random --seed 0
chemworld run --task reaction-to-purification --agent scripted_chemistry --seed 0
chemworld verify --constitution --submission runs/<trajectory>.jsonl
```

执行 official suite：

```bash
chemworld suite --agent gp_bo --world-splits public-test private-eval --seeds 0 1 2
```

## 下一步

- 选择能力切片：[任务列表](tasks.md)
- 编写 agent：[Agent 交互接口](agent_interface.md)
- 理解动作合法性：[操作协议](operations.md)
- 生成可发布结果：[提交与验证](submission.md)
- 复现完整门禁：[验证与质量保证](validation.md)
