# Work II DeepSeek A-S crystallization physical-continuity rerun note

## Question

在空晶体群体重新进入冷却/加晶种路径时使用物理有效的成核参考尺度后，冻结的 A-S
reaction-to-crystallization 三臂比较能否在不伪造结晶、不放松安全或实验资源约束的前提下完成，
以及 aligned、opaque、misindexed 三种初始世界模型如何影响机制恢复、实验决策和终态推荐？

## Fixed units and coverage

- 只重跑原 public C2 计划中 A-S `reaction-to-crystallization` 的完整 task block。
- 使用原计划的 5 个 world、每个 world 的 3 个 prior arms，共 15 sessions；每 session 固定 12 个
  完整实验，共 180 experiments。
- world、arm、顺序、模型 `deepseek-v4-flash`、reasoning、prompt、动作 schema、噪声配对和 runtime
  config 均从原冻结计划读取。旧 15-session 结果完整保留，不覆盖、不拼接进新 block。
- provider 总调用预算为 report-only，不作为在线停止条件；实验室库存、器皿、操作次数、仪器、过程时间、
  final assay 与 participant 主动重复配方预算保持原资源卡边界。

## Measurements

记录每个 session 的完整实验数、操作与测量轨迹、belief checkpoints、机制模块与干预后果预测、终态推荐、
blind evaluation、运行时拒绝与恢复、资源账本、provider token/错误回执、right-censoring 和 exact replay。

## Pass, failure, and stop rules

- 目标分母为 15/15 terminal sessions 与 180 scheduled experiments；completed、right-censored 和 retained
  failure 均进入报告，不按结果替换。
- 修复后的正例要求：上层声明可用且满足公开参数边界的空群体再冷却/加晶种路径不再因零粒径表示被
  `runtime_domain_valid` 拒绝。向上冷却、无物料结晶、非法资源参数和物理求解失败仍不得伪装为有效实验。
- 本轮不修正一般数值求解器非收敛；若出现，保留为明确运行终态并报告，不能在运行中改变求解或实验设计。
- 若发现新的平台缺陷会改变 participant 可见反馈或已提交轨迹，则停止后续尚未启动的 triplet，并将本次
  15-session block 整体标为需从头重跑；纯基础设施故障仅按原计划恢复未形成科学轨迹的缺失 cell。

## Outputs

输出到新的 ignored run root，包括原计划副本、逐 cell trajectory/summary、进度、终态汇总和 provider
账本；原始 provider payload 不进入 Git。终态后更新可复用分析与汇报图，不创建额外 readiness、SHA
inventory 或全局审计包。
