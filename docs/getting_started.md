# 安装与首个回合

本页从源码安装 ChemWorld，运行一次合法 episode，并验证输出。推荐 Python 3.11 或更高版本。

## 安装

```bash
git clone https://github.com/sunyrain/ChemWorld.git
cd ChemWorld
python -m pip install -e ".[dev]"
```

验证命令是否可用：

```bash
chemworld --help
chemworld tasks list
```

Windows 如果把 `python` 解析为 Microsoft Store 别名，请使用真实 Python 路径或先激活仓库的
`.venv`。构建文档或执行完整科学参考门禁时，安装扩展依赖：

```bash
python -m pip install -e ".[dev,docs,physchem-ref]"
```

## 创建环境

```python
import gymnasium as gym
import chemworld  # 注册 ChemWorld 环境

env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
observation, info = env.reset(seed=0)

print(info["task_id"])
print(info["physics_maturity"])
print(env.unwrapped.available_actions())
```

未测量的数组字段使用 `NaN`，JSONL 中对应 `null`。读取字段前同时检查 `observed_mask` 或
`observed_keys`，不能把未观测状态当成零值。

## 运行第一条完整轨迹

最稳妥的首次运行方式是使用官方 runner：

```bash
chemworld run --task reaction-to-assay --agent random --seed 0
```

命令会在 `runs/` 下写入 trajectory JSONL 和 manifest。终端输出给出实际文件路径。随后执行：

```bash
chemworld verify --constitution --submission runs/<trajectory>.jsonl
chemworld evaluate --submission runs/<trajectory>.jsonl
```

`verify` 检查 schema、合同摘要、回放一致性与物理构成；`evaluate` 从轨迹重算结果，不信任提交者
写入的分数。

## 手动调用动作

使用当前状态的 affordance 和 schema 生成动作，不要把一套固定流程硬编码到全部任务：

```python
available = env.unwrapped.available_actions()
schema = env.unwrapped.action_schema("add_reagent")
check = env.unwrapped.validate_action(
    {"operation": "add_reagent", "amount_mol": 0.01}
)

if check["valid"]:
    observation, reward, terminated, truncated, info = env.step(
        {"operation": "add_reagent", "amount_mol": 0.01}
    )
```

动作无效时，环境通过 `invalid_reasons` 和 precondition 标志提供可恢复反馈。不同任务的允许操作、
仪器、预算、终止条件和 campaign 语义不同；以 reset 信息和任务卡为准。

## 启动可视化界面

```bash
python -m apps.task_lab.server --port 8876
```

- Agent Observatory：<http://127.0.0.1:8876/agent/>
- Student Lab：<http://127.0.0.1:8876/student/>

经典方法无需在线凭证。在线模型密钥只应通过环境变量传入，不要写入脚本、Markdown 或提交包。

## 下一步

- [选择任务](tasks.md)
- [理解 Agent 接口](agent_interface.md)
- [运行可复现评测](benchmark_protocol.md)
- [查看当前科学状态](benchmark_release.md)
