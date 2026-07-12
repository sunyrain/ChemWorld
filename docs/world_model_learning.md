# RL 与 World Model

!!! info "当前 RL 证据"
    修复后的 PPO 开发门禁已完成 5 个训练 seed、每个 seed 20 个 Dev episode，共 51,200 环境步；它只证明多 seed 学习与审计链可运行，`benchmark_claim_allowed=false`，尚未形成冻结 Bench 排名。下文 SAC 数值均为 pre-v0.5 diagnostic。

> **当世界规律隐藏且可能变化时，策略需要记住过去、推断当前世界，并在旧模型失效后快速恢复。**

ChemWorld 不只是把实验写成一个 Gym API。它将部分观测、混合动作、长程流程和 world-family shift
放进同一训练问题，用于研究 model-free、model-based 与快速适应方法。

## 为什么这是 POMDP

当前 observation 只包含任务允许公开的测量和过程摘要。速率律、隐藏组成、相行为参数和世界标签
都不可见；同一条读数可能对应多种机制解释。

```text
hidden world + history + current action
  → state transition
  → partial observation
```

因此最优决策通常依赖完整历史，而不是当前向量。单步 policy 可以作为下限，但机制识别需要记忆或
显式 belief/context state。

## 为什么需要两种记忆

- **实验内记忆**：当前 vessel 已经投了什么、经历哪些条件、哪些测量消耗了样品。
- **实验间记忆**：过去 recipe、终检、失败原因，以及哪些世界假设仍然成立。

Procedure Execution 依赖前者；Campaign Design 依赖后者；世界变化后的快速恢复需要同时使用两者。

## 动作不是一个简单连续 Box

ChemWorld Action 通常包含离散 Operation 和只在该 Operation 下有效的参数。例如 `heat` 需要温度与
时间，`measure` 需要仪器，`separate_phase` 需要相选择。这是条件混合动作空间：

```text
operation id
  ├── heat: temperature + duration
  ├── measure: instrument
  └── separate_phase: phase + fraction
```

直接把所有参数拼成一个连续向量，容易产生大量无效组合。合法动作 mask、条件 action head、层级
policy 或 planner—controller 分解更符合接口结构。

## 训练 Reward 与最终结果分开

训练可以使用过程 reward、cost signal 和辅助预测任务，但 benchmark 主结果来自 final assay 与轨迹
重算。Shaping 帮助学习，不应在评测时被当成化学目标本身。

需要分别检查：

- policy 是否只是利用 dense shaping；
- 移除 shaping 后是否仍能完成实验；
- checkpoint 选择是否只使用 Dev worlds；
- Bench 运行是否冻结参数并停止学习。

## 方法路线图

| 方法家族 | 典型用途 | 当前仓库状态 |
| --- | --- | --- |
| Model-free RL | 学习 procedure 或连续控制 | PPO/SAC 基础训练与回放链可用；正式多 seed 结果缺失 |
| Recurrent / hierarchical RL | 处理长程记忆和混合动作 | 研究候选，尚无冻结正式矩阵 |
| Surrogate + acquisition | Campaign Design 与信息效率 | 多种 GP/RF/安全方法可运行 |
| Surrogate + MPC | 局部动态模型与规划 | 接口方向，尚无正式 baseline |
| Latent world model | 压缩历史并预测未来观测 | 数据与评价接口具备，训练方案待建立 |
| Context-conditioned / meta-RL | 快速识别新 world family | 核心研究方向，正式适应实验未运行 |

Dreamer、TD-MPC、PEARL、VariBAD 或 RL² 等名称代表可能的研究家族，不表示仓库已经实现或验证这些
具体算法。

## 学习器可以使用哪些数据

公开 trajectory 提供：Action、observation、reward、constraint flags、instrument readings、任务合同、
公开 scenario metadata 与 Agent 自己的历史。隐藏 state、oracle mechanism 和 private-eval 参数不属于
输入。

可以训练的辅助目标包括：

- 下一步公开 observation；
- final-assay 结果分布；
- 风险、成本与失败概率；
- measurement value of information；
- world context 或 change-point representation。

## Train、Dev 与 Bench

| Split | 允许什么 |
| --- | --- |
| Train worlds | 更新 policy、encoder、dynamics 与 replay buffer |
| Dev worlds | 选择 checkpoint、architecture 和超参数 |
| Bench worlds | 冻结后一次运行，不继续训练 |
| Private / Bridge | 隐藏 world cells 或独立系统，只由评测端执行 |

World-family cells 应不重叠。仅换 seed 的多次训练不能替代未见机制适应。

## 不要只看 Prediction Loss

一个 world model 即使预测误差更低，也可能没有改善决策。正式评价至少同时报告：

- calibration 与未见 world prediction；
- adaptation regret；
- change detection 和 mechanism identification；
- recovery experiments；
- 固定预算下的 task outcome；
- 适应期间的风险与成本；
- 训练计算、数据量和模型更新资源。

## 当前证据边界

Pre-v0.5 SAC 工程运行在单个连续流任务、单个模型 seed 上完成 100,000 Train 步并保留 checkpoint，证明
训练、评测和 replay 链可以连通。但轨迹首先暴露的是动作覆盖、奖励和 checkpoint 选择问题，不支持
稳定 RL 排名，也不支持“训练越久越好”的一般结论。

下一步最重要的是：修复并冻结动作/奖励合同，进行 pooled multi-seed Dev 选择，再在未见 world
family 上测量 recovery 与 adaptation regret。

继续阅读：[选择交互层级](agent_tracks.md) · [数据集层](dataset_layer.md) ·
[Benchmark 设计](benchmark_overview.md)
