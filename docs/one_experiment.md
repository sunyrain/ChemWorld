# 一次闭环实验

> **Agent 在 ChemWorld 中经历的不是一张输入表，而是一段会留下后果的实验过程。**

这一页从任务开始，沿着一次 Action、测量、终检和回放走完整个循环。具体 API 放在技术文档；这里
先解释 Agent 实际面对的决策。

## 从目标、预算和可用工具开始

每次 reset 会给 Agent 一份公开任务合同，包括：

- 要优化或确认的目标；
- 完整实验、操作、测量或时间预算；
- 当前允许使用的 Operation 与仪器；
- 风险、成本和终止条件；
- 结果需要怎样提交与验证。

Agent 不会得到最佳 recipe、隐藏机理或 private-eval 参数。

## Agent 看得到什么

| 公开信息 | 例子 |
| --- | --- |
| 当前合法操作 | 可以投料、加热、测量、分相或终检 |
| 已释放观测 | 温度、公开过程指标、峰表或终检结果 |
| 实验历史 | 已执行 Action、仪器、预算和失败摘要 |
| 不确定性 | 处理后估计的范围或观测 mask |
| 约束状态 | 剩余预算、风险、成本和前置条件 |

## 世界隐藏什么

真正组成、速率常数、反应网络、分配系数、私有扰动和 debug truth 留在世界内部。Agent 只能通过
操作带来的后果与仪器观测推断它们。

## 一个 Action 怎样产生后果

```text
Agent 提交 Action
  → schema 与当前前置条件校验
  → 路由到声明的物理 Provider
  → 在事务中更新物料、相、设备和时间
  → 计算风险、成本与公开观测
  → 成功提交或完整回滚
```

例如连续两次 `heat` 会从当前温度与组成继续推进；没有形成两相时执行 `separate_phase` 会被拒绝，
而不是假装成功。无效动作、回滚和失败原因都会留在轨迹中。

## 测量怎样释放证据

测量也是 Operation。它可能消耗样品、费用、时间和实验预算，并返回：

- raw signal；
- processed estimate；
- uncertainty；
- observed mask；
- 仪器与样品消耗摘要。

Agent 必须判断这份信息是否值得它的资源，而不是免费读取完整状态。

轨迹会把结果拆成三层：`environment_outcome` 保存世界实际产生的后果，
`agent_visible_observation` 保存真正释放给 Agent 的反馈，`evaluation_outcome` 保存评价器使用的真实终点。
因此反馈延迟或置换不会改写世界实际发生了什么，也不会污染正式评分真值。

## 一个连续流例子

Agent 第一次实验得到低转化。至少存在三种解释：反应太慢、副反应太强，或设备传热使真实温度低于
设定值。它可以直接提高温度，也可以测量中间产物或改变停留时间来区分解释。不同选择会改变后续
状态、风险和可用证据；这正是闭环决策与静态预测的差别。

## Experiment 何时结束

合法 `final_assay` 形成一个可比较 Experiment 结果。中间 reward 只用于学习和诊断，不能冒充终检
指标。`single_experiment` 模式随后结束；`campaign` 模式则保存结果，在预算允许时换一只 fresh
vessel，继续在同一个隐藏世界中设计下一次实验。

## 为什么可以回放

Trajectory 绑定任务、世界律、scenario、mechanism、Action、观测、评分合同与必要随机流信息。
评价器重新执行轨迹并重算指标，不信任 Agent 自报的分数。

<div class="cw-button-row" markdown>

[安装并运行一次实验](getting_started.md){ .md-button .md-button--primary }
[打开本地可视化实验室](interactive_task_lab.md){ .md-button }
[查看 Agent API](agent_interface.md){ .md-button }

</div>

!!! note "在线体验状态"
    当前网站是静态文档，Student Lab 与 Agent Observatory 需要在本地启动。页面不会伪装成已经部署
    的云端实验服务。
