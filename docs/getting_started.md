# 从安装到可回放实验

本页针对当前开发运行时，不复现论文旧物理。软件世界不是真实实验操作指南。
[English source](https://github.com/sunyrain/ChemWorld/blob/main/docs/getting_started.en.md) · [发行范围与验证边界](community_release.md)

## 选择入口

| 目的 | 路径 |
| --- | --- |
| 使用当前功能 | 安装从 main 构建的 wheel；没有授权发布新版 PyPI/tag，不把旧的 0.2.0 当成当前 main |
| 开发、贡献或运行完整例子 | Git checkout + 已提交 uv.lock，如下 |
| 复现旧论文 | [独立冻结快照及其依赖](https://github.com/sunyrain/ChemWorld-Public/tree/03e8026301c185fd6ba5bdbda7460765d9b3e724)，不要使用当前 main 解释旧轨迹 |

Python 3.11/3.12 是本轮验证目标；各操作系统实际结果见发行说明。
已有 wheel 时，在独立虚拟环境执行
`python -m pip install /absolute/path/to/chemworld_bench-0.2.0-py3-none-any.whl`。
从源码构建用 Git clone 或生成的 sdist，不用 GitHub ZIP。

## 开发安装

需要已安装的 uv 和 Python 3.11 或 3.12：

```bash
git clone https://github.com/sunyrain/ChemWorld.git
cd ChemWorld
uv sync --locked --extra dev
uv run --no-sync chemworld tasks list
```

以下命令在 checkout 执行；wheel 环境中直接使用其 `python`、`chemworld`、`chemworld-lab`。
例子源文件位于仓库/源码发行包，不假定安装 wheel 后当前目录有 `examples/`。

## 第一次终检和最小 Agent

```bash
uv run --no-sync python examples/demo_manual_event_sequence.py
uv run --no-sync python examples/demo_agent_facing_api.py
uv run --no-sync python examples/demo_minimal_agent.py --output runs/minimal-agent.jsonl
uv run --no-sync chemworld verify --submission runs/minimal-agent.jsonl --tolerance 0
uv run --no-sync chemworld evaluate --submission runs/minimal-agent.jsonl
```

选择新的输出路径，例子拒绝覆盖已有结果。`FourStepAgent` 展示 `BaseAgent.act(history)` 与 runner
的扩展点，不声称优化能力或在线学习。`terminate` 不是终检；只有提交的
`measure` + `instrument="final_assay"` 才计入终检。得分低仍是有效实验结果。

## 研究笔记、预测、失败与导出

```bash
uv run --no-sync python examples/demo_offline_research.py --output runs/offline-example
```

[完整范例设计](offline_research.md)在实验前固定七条路径；预测先封存，再执行两条留出实验，输出
真实误差。原生 JSONL 保留拒绝、开放和截断记录，每条轨迹在新进程零容差回放。
数组未观测值是 NaN，JSON 中是 null，须同时读取 `observed_mask`；不要补零。
本例仅导出 JSONL，未安装/未验证的 Parquet 可选后端不作为已通过功能。

## 可写 Lab

```bash
uv run --no-sync chemworld-lab --no-browser
```

打开打印的本机地址：选择任务 → 开始 → 操作 → 终止 → final_assay → 精确回放 → 下载/复制 JSONL → 关闭。
关闭不会补做终检。下载受阻时使用页面导出副本，离开页面前确认保存。
只监听回环地址，不经端口转发对外开放。它不是运行陌生代码的安全沙箱。
`apps.task_lab.server` 是另外的 checkout 研究工具，不属于 wheel 的命令入口。

## 公开接口

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
try:
    _, info = env.reset(seed=0)
    print(info["task_id"])
    print(env.unwrapped.action_schema("heat"))
    print(env.unwrapped.available_actions())
finally:
    env.close()
```

支持操作以 `task_info()` 为准，当前可用性以 `available_actions()` 和 `validate_action()` 为准。
查看[操作语言](operations.md)、[Agent API](agent_interface.md)和
[贡献说明](https://github.com/sunyrain/ChemWorld/blob/main/CONTRIBUTING.md)。
