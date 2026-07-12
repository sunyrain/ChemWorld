# 浏览任务类型

任务分类帮助你从研究问题出发选任务，而不是只记一串 Task ID。

| 家族 | 核心问题 | 代表任务 |
| --- | --- | --- |
| 反应优化 | 怎样选择条件提高目标结果 | `reaction-optimization-standard` |
| 安全约束 | 怎样在目标、风险和成本间取舍 | `reaction-safety-constrained`、`flow-reaction-optimization` |
| 表征与解释 | 测什么、何时测、如何用证据更新假设 | `reaction-mechanism-explanation`、`low-budget-characterization` |
| 反应—分离流程 | Agent 能否完成多阶段后处理 | `reaction-to-purification`、`reaction-to-crystallization`、`reaction-to-distillation` |
| 规律发现 | 能否用多次实验学习隐藏关系 | `partition-discovery` |
| 泛化 | 策略能否适应未见场景 | `public-private-generalization` |
| 工具规划 | 能否在长流程中持续合法地使用工具 | `tool-agent-planning` |

## 新任务怎样进入系统

一个新任务应先回答：目标和主指标是什么、Agent 能看到什么、哪些操作合法、预算如何计算、失败如何
处理、使用哪些物理模块，以及 replay 怎样验证。注册成功只说明它能运行；进入研究候选套件还要通过
可辨识性、资源公平、泛化与实证检查。

完整目录见[选择一个任务](tasks.md)，逐任务合同见[阅读任务卡](task_cards.md)。
