# 本地评测机

本地评测机用于在不依赖托管服务的情况下运行 ChemWorld 任务、收集轨迹、计算分数并
生成报告。它是未来 hosted leaderboard 的最小可运行前身。

## 目录布局

```text
local_eval/
├── submissions/
├── runs/
├── scores/
├── reports/
└── manifests/
```

`submissions/` 存放 agent 或 recipe；`runs/` 存放原始轨迹；`scores/` 存放结构化评分；
`reports/` 存放人类可读报告；`manifests/` 存放版本、seed 和配置。

## 一条命令演示

```bash
python scripts/audit_environment_consistency.py --tasks all --seeds 0 1 2
```

这个命令侧重环境自洽性，不等同正式 leaderboard，但它能快速检查任务注册、reset/step、
replay、spectra 和 constitution 是否处于可发布状态。

## 手动评测流程

1. 选择任务集和 seeds。
2. 加载 agent 或 recipe。
3. 逐个 episode 运行环境。
4. 保存 trajectory、task_info、score 和 manifest。
5. 生成汇总表和失败案例报告。

最小 API 形态：

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=1)
obs, info = env.reset(seed=1)
```

## 安全模型

本地评测机默认只执行受信任代码。若允许第三方提交 Python agent，应使用隔离进程、
资源限制、超时、只读数据目录和明确的输出协议。不要在教师机或发布机上直接运行未知
代码。
