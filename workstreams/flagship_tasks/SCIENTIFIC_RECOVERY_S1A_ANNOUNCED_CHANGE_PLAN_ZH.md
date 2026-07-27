# S1-A 已告知变化后的科学恢复实验设计

状态：`deferred research extension; not on the current S0 roadmap`

日期：2026-07-27

> 2026-07-27 路线调整：当前研究优先完成静态 S0 的复现、统计汇报、静态任务扩展和现实桥接。
> 隐藏或已告知的世界变化并不是当前 benchmark 主问题，本设计仅作为未来鲁棒性研究备忘，不启动
> Stage 0 或任何 provider 实验。

## 1. 核心判断

静态 S0 已回答“模型能否在固定世界中持续优化”。下一步不应立即把变化检测、机理归因、
恢复、Stateful scaffold 和 provider 差异重新塞进同一个大矩阵。最小的下一科学问题应是：

> 模型已经建立固定世界参照，并被明确告知环境发生变化后，能否利用新的实验反馈形成较正确的
> 局部判断，并恢复任务表现？

该轨记为 S1-A。它显式告知变化，因此不评估 detection。未告知变化的 detection 轨记为 S1-B，
只能在 S1-A 已证明恢复接口可运行后启动。

## 2. 为什么先做 S1-A

旧机制适应设计同时混合了五件事：建立旧世界参照、发现变化、判断变化类型、寻找新条件、
维持自主操作生命周期。任何一处失败都会使最终恢复失败，无法判断模型究竟缺少哪种能力。

S1-A 固定前三项边界：

- 使用已经审计的完整实验接口，不再测试 operation-level autonomy；
- 在第一轮 post-change 决策前明确给出 change notice；
- 不公开隐藏机制、材料映射、oracle 或候选世界 likelihood；
- 第一轮只使用 Direct scaffold，不引入额外持久状态；
- Declared 机理仍是次要诊断，Predictive 与实际恢复表现分开计分。

因此 S1-A 的失败可以解释为“已知发生变化后，证据到恢复策略的转换仍不足”，而不是
“模型没有猜到评估器何时切换世界”。

## 3. 实验单位

一个 S1-A cell 包含：

1. 一个冻结的 20 次完整实验 S0 pre-change prefix；
2. 一个明确、公开、固定措辞的 change notice；
3. 最多 12 次 post-change 完整实验，报告 `k={1,2,4,8,12}`；
4. 一次独立 final synthesis；
5. 配对 blind validation；
6. 同次 final synthesis 中的冻结 Predictive 问题和结构化机理声明；
7. 完整 receipt、资源账本和确定性 replay。

development qualification 可以复用现有 S0 的 20 次探索 prefix，不重做 provider 调用。该复用只
用于接口资格和成本估计，不把已触碰 seed 重新包装成新的正式 cohort。未来正式实验必须使用新的
冻结 world seeds，并完整记录其 pre-change lineage。

change notice 只允许表达：

```text
The environment has changed since the previous completed experiment.
The cause and new response law are hidden. Previous results remain available
as old-world reference evidence. Design the next complete experiment for the
current world. N post-change experiments remain before final synthesis.
```

不允许给出 family、changepoint likelihood、Gate A certificate 或推荐动作。

## 4. 任务与变化选择

第一轮仍使用两个确认性任务：

- `electrochemical-conversion`，保持六控制单阶段合同；
- `reaction-to-crystallization`，保持十控制完整反应–结晶合同。

在任何真实 provider 调用前，必须在当前源码上重新完成局部环境资格：

- 变化确实改变 response surface，而不是只改变隐藏标签；
- S0 incumbent 在新世界出现可测性能损失；
- 公开动作和测量在 12 次 post-change 实验内能够恢复；
- reset BO、warm-start BO 和 oracle-envelope 的结论可重放；
- 每个候选 family 的非平凡效应和恢复余量达到预冻结阈值。

开发阶段每个任务只选择一个通过上述检查的变化 family。不要一开始恢复 RC28 的全部
family、never twins 和四方法矩阵。family 扩展属于后续外部有效性，不属于首个接口资格实验。

## 5. 预算如何确定

`12` 是 development 上界，不是预先宣称合理的正式轮数。本地经典算法先报告
`k={1,2,4,8,12}` 恢复曲线，然后选择满足以下条件的最小预算作为正式候选：

- reset BO 在至少 90% 的开发世界达到其 12 轮最终恢复量的 80%；
- 至少保留两个非终点 checkpoint，可观察恢复速度；
- Agent prompt/history 不发生截断；
- blind validation 和 Predictive 的本地模拟成本已计入总物理实验数。

模型在开始 post-change campaign 时必须知道总实验数和剩余实验数。最后一次探索不视为最终
提交；final synthesis 永远是独立调用。

## 6. 估计量

### 6.1 主结果

S1-A 的主结果是 post-change recovery regret AUC。每个 checkpoint 同时报告：

- 当前世界的 best-so-far score；
- 最终 blind-validated recommendation score；
- 相对 transferred S0 incumbent 的恢复增益；
- 相对 post-change oracle envelope 的剩余 regret；
- 达到预冻结恢复阈值的首个实验序号。

不得只报告最后一轮分数，也不得把单次 noisy exploration peak 当成恢复完成。

### 6.2 世界认识

- Predictive：在最终综合中回答冻结的一因子干预方向，提交后才执行配对模拟；
- Declared：结构边、方向、机制标签、unsupported claim rate 和置信度校准；
- Evidence-to-action：机理判断正确与否和后续实验/最终方案是否沿该判断行动分别计分。

Predictive 或 Declared 正确不自动等于恢复成功；恢复成功也不自动等于正确认识机制。

## 7. 基线

至少包含四个本地基线：

- `transferred_incumbent`：变化后不调整，用于测量变化造成的性能损失；
- `reset_gp_or_rf_ei`：只使用 post-change 数据；
- `boundary_aware_warm_start`：保留 pre-change 数据，但显式建模变化边界；
- `post_change_oracle_envelope`：只用于归一化和环境资格，不进入 participant 排名。

若安全风险在所有开发轨迹中仍远低于阈值，不应重复宣称 Safe-GP 提供了额外安全收益。

## 8. 分阶段执行与停止条件

### Stage 0：零 API 成本

- 当前源码上的变化执行、守恒、reset 和 replay 检查；
- 两任务本地 baseline 的 `k={1,2,4,8,12}` 曲线；
- 冻结 change notice、公共上下文、指标和开发 seeds；
- mock agent 完整运行及 receipt tamper test。

### Stage 1：最小真实 provider 资格

- `gpt-5.6-sol medium`；
- 每个任务一个 development seed；
- Direct scaffold；
- 最多 12 次 post-change 调用加一次 final synthesis；
- 不作性能主张，只检查合同失败率、行为可解释性、token 与成本。

### Stage 2：小规模能力实验

只有 Stage 1 同时满足以下条件才启动：

- 100% receipt/replay 通过；
- method-contract failure 低于 5%；
- 无 prompt/history 截断；
- 至少一个任务出现非零恢复增益；
- Predictive 查询具有足够非平凡真实效应。

Stage 2 使用每任务三个新的 development seeds，并与本地 baseline 配对。是否改用 `high` 必须在
看到 Stage 2 结果前冻结，不能依据单个样本临时升级。

### Stage 3：scaffold 消融

只有 Direct 已能稳定完成 S1-A，才在相同 backend、task、prefix、change 和预算上比较
Direct 与 compact-Stateful。Stateful 只多一份有界、仅引用 evidence ID 的 Agent 自写状态。

### Stage 4：S1-B 未告知变化

S1-B 才加入 changed/never twins、detection delay、AUROC、FPR 和 changepoint 右删失。它不得
反向修改 S1-A 的恢复预算和指标。

## 9. 代码边界

S1-A 不修改冻结的 S0 schema、formal configs 或 receipts，也不继续扩张旧的 RC28 runner。
新的实现应复用：

- `StaticOptimizationPlan` 和具名完整实验 validator；
- task-aware recipe compiler；
- mechanical closeout；
- 公共 observation seed 和 postrun replay 基础设施。

只新增独立的 change notice、phase-boundary receipt 和 recovery scorer。runner、replay 与聚合器
必须分层，避免再次形成一个同时执行实验、补救失败和解释结果的巨型入口。

## 10. 当前启动结论

现在可以开始 Stage 0，本地完成环境与 baseline 资格；不应立即启动高成本正式 participant
矩阵。S1-A 的首个真实 provider pilot 预计只有两个 cells，待 Stage 0 产物冻结并确认后再调用。
