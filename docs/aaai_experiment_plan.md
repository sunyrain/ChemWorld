# AAAI 实验计划

本页定义 ChemWorld 面向 AAAI 投稿准备的冻结实验 preset。目标不是把所有长期物理模块一次性做完，而是围绕一组可复现、可审计、能支撑论文主张的 agent benchmark 实验收束。

## 论文主线

ChemWorld 是一个机制驱动、带仪器观测和安全成本的物理化学交互世界，用于评测 agent 在有限预算下的实验规划、局部 world model 学习、过程决策和泛化能力。

核心主张应限定为虚拟交互 benchmark，不声称真实化学反应预测软件，也不声称替代真实实验机器人平台。

## AAAI 6 任务集合

AAAI preset 固定为以下 6 个任务：

| Task ID | 主要能力 | 观测/约束重点 |
| --- | --- | --- |
| `reaction-optimization-standard` | 闭环反应条件优化 | final assay、sample efficiency |
| `reaction-to-purification` | 反应到后处理的过程规划 | purity/recovery trade-off |
| `partition-discovery` | 分配规律探索 | phase observation、measurement cost |
| `reaction-to-distillation` | 反应到蒸馏切片 | separation score、cost/risk |
| `electrochemical-conversion` | 电化学转化规划 | current/voltage proxy、safety cost |
| `equilibrium-characterization` | 平衡表征 | pH-meter、precipitation signal、equilibrium diagnostic |

代码入口：

```python
from chemworld.tasks import AAAI_TASK_IDS
```

CLI 入口：

```powershell
chemworld baselines report --preset aaai --output-dir runs/aaai_2027/baseline_report
chemworld artifact create --preset aaai --output-dir runs/aaai_2027/artifact
```

快速 smoke：

```powershell
python scripts/run_aaai_experiments.py --smoke
```

## Baseline Agents

AAAI 自动复现实验默认使用：

| Agent | 作用 |
| --- | --- |
| `random` | 随机下限 |
| `lhs` | 系统探索下限 |
| `scripted_chemistry` | 规则化化学流程 |
| `gp_bo` | Gaussian-process BO |
| `safe_gp_bo` | 安全约束 BO |
| `tool_using_llm_stub` | 不依赖在线 API 的 tool-agent stub |
| `codex_subagent_replay` | Codex 在线评测轨迹的可复现 replay |

`codex_subagent_online` 作为人工触发的在线基线保留协议和 manifest 字段，但不进入 CI 或默认本地复现命令。论文表格可以单列在线运行结果；artifact 以 replay trace 保证复现。

## 主实验

主实验采用 `6 tasks x frozen seeds x baseline agents`。每个任务单独排名，不合并成一个总榜。

建议报告字段：

- best score；
- final assay score；
- campaign AUC；
- invalid action rate；
- precondition failures；
- safety cost；
- final assay count；
- sample efficiency；
- task-specific metrics，例如 purity、recovery、partition signal、equilibrium confidence。

## 泛化实验

泛化实验比较 public-test 与 private-eval：

- 使用同一 `world_law_id`；
- public/private 共享机制族，不共享 hidden parameters；
- private-eval 由维护者 salt 和 hidden seed 生成；
- 报告 public/private gap、rank stability 和 confidence interval。

当前公开仓库只提供 private-eval placeholder 机制；正式论文评测应由教师端或 maintainer-side runner 持有 private salt。

## Agent 交互消融

建议消融：

| Setting | 移除内容 | 目的 |
| --- | --- | --- |
| full interface | 无 | 完整 agent-facing API |
| no affordance | `available_actions()` | 测合法动作提示是否重要 |
| no validator retry | `validate_action()` recovery | 测失败恢复 |
| no lab report | 谱图/观测摘要 | 测自然语言实验报告价值 |
| no safety cost | cost channel | 测安全成本信号 |

每个消融仍必须记录 agent trace、validator result 和 public observation summary。

## 机制发现案例

建议选 2-3 条 Codex 或 tool-agent 轨迹做 qualitative case study：

- 根据 HPLC/GC/UV-vis 调整反应时间、温度或后处理；
- 根据 pH-meter 与 precipitation signal 调整 equilibrium-characterization 策略；
- 根据 safety cost 避免高风险条件；
- 根据失败 precondition 恢复到合法实验流程。

案例只说明 agent 在隐藏虚拟机制中学习局部 world model，不把轨迹解释为真实化学发现。

## Artifact 要求

AAAI artifact 应包含：

- task cards 与 contract hashes；
- scenario cards 与 mechanism hashes；
- solver/provenance manifest；
- maturity labels；
- baseline report；
- trajectories；
- Codex replay traces；
- figure/table source data；
- release checklist。

生成入口：

```powershell
python scripts/run_aaai_experiments.py --smoke
python scripts/run_aaai_experiments.py --output-dir runs/aaai_2027
```
