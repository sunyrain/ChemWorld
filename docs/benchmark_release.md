# Benchmark v1

`chemworld-serious-v1` 是 ChemWorld 的冻结研究套件。它评估 Agent 在未知、部分可观测、实验
有成本的虚拟化学系统中，能否通过多轮实验改进后续决策。它不用于预测真实物料、产率或装置
安全性。

## 正式任务

| Task | 核心能力 | Primary metric | Budget | Seeds |
| --- | --- | --- | ---: | --- |
| `partition-discovery` | 主动探索未知分配行为 | `product_in_organic` | 48 | 0–4 |
| `reaction-to-crystallization` | 反应–结晶联合决策 | `crystal_yield` | 72 | 0–4 |
| `reaction-to-distillation` | 反应–馏分联合决策 | `distillate_purity` | 72 | 0–4 |
| `flow-reaction-optimization` | 流动、热与风险权衡 | `flow_conversion` | 60 | 0–4 |
| `electrochemical-conversion` | 电化学选择性与能效权衡 | `electrochemical_selectivity` | 48 | 0–4 |
| `equilibrium-characterization` | 有限仪器预算下的平衡表征 | `equilibrium_confidence` | 24 | 0–4 |

所有任务都是 campaign：一次 final assay 结束当前实验，但只要总预算未耗尽，Agent 就能根据
反馈启动下一次实验。

## 冻结条件

正式证据要求：

- 六种官方 baseline 覆盖全部 5 个 seeds；
- 官方 baseline 不依赖非法动作；
- 每个任务完成多次独立实验；
- GP-BO 与 safe GP-BO 在初始化后进入 acquisition；
- 分数不存在全体地板或天花板，且至少三个策略可区分；
- primary metric 对策略变化有响应；
- success threshold 可达到但不饱和；
- 轨迹、结果和发布产物均可重放验证。

这些条件由机器读取冻结证据并核对当前 task contract hash。任何合同变化都会使任务自动退回
candidate，而不是沿用旧的 validated 标签。

## 运行与验证

```bash
chemworld baselines report --preset serious --output-dir runs/serious
python scripts/run_serious_task_suite.py --output-dir runs/serious_release
python scripts/check_frozen_benchmark.py
```

结果必须逐任务报告。ChemWorld 不定义跨任务总分，因为不同物理域、量纲和失败方式不应被一个
任意权重掩盖。

## 解释边界

任务中的物料、仪器和物理模块构成可审计的虚拟实验世界。分数支持比较 Agent 的实验策略，
不支持把数值当作现实化学预测。模块成熟度、限制和参考证据随任务卡与结果一起发布。
