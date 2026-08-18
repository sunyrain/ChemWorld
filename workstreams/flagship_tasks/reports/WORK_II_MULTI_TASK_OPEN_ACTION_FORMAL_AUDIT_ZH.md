# Work II 多任务 open-action 五世界矩阵：审计与收束

日期：2026-08-17

状态：原始矩阵执行终止；失败单元保留；另有一个独立的 `seed2 / aligned_nominal`
技术敏感性 repair block 已完成，但不替换原始 cell，也不回写原始 45-cell 分母。

## 1. 固定范围与完整性

本 block 固定为 3 个任务 × 5 个 world seed × 3 个 arm，共 15 个 cluster、45 个
session、540 个 participant experiment slots。provider-free truth 与 exact replay 各
240 次，候选 ActionPlan 对 agent 公开，候选结果和真实排名隐藏。

完整性复核结果：

- 45/45 cell result records 已生成；
- 45/45 cell hash 与机器汇总一致；
- aggregate summary hash 通过；
- 42/45 cells 为 `completed_uncontaminated`，且其 qualification 全部通过；
- 3 个失败 cell 均保留在总分母，不以有利结果替换；
- 没有 truth/replay、资源拒绝、隐藏边界或 accounting 缺陷。

## 2. 三个失败 cell 的因果审计

| cell | 轨迹终点 | provider / 资源状态 | 判定 |
|---|---|---|---|
| reaction-to-crystallization / seed 1 / opaque | 7 个完成批次、5 个 discarded batches；最后因 heat 与 seed 资源耗尽而 discard | provider session 正常结束；0 provider error；0 resource rejection；campaign terminal reason 为 resources exhausted after batch close | agent 轨迹诱导的资源/流程失败，保留为负结果 |
| reaction-to-crystallization / seed 0 / misindexed_nominal | 10 个完成批次、2 个 discarded batches；最后因无 heat 且无法继续 seed→reaction 流程而 discard | provider session 正常结束；0 provider error；0 resource rejection；campaign terminal reason 为 resources exhausted after batch close | agent 轨迹诱导的资源/流程失败，保留为负结果 |
| reaction-to-crystallization / seed 2 / aligned_nominal | 10 个完成批次；最后一个 action 后未进入下一个可执行操作 | provider session `interrupted_before_next_action`；0 provider error event；right-censored；无 terminal readout | provider/session 中断，保留为操作性失败 |

前两个 cell 不是 host-side stock rejection：资源合同允许动作执行，失败发生在 agent 自主
选择的操作序列和批次收口上。第三个 cell 不是物理世界失败，而是会话在未完成协议前中断。

## 3. 可报告的描述性结果

动作质量统计只使用 42 个合格 cell，不把失败 cell 的不完整轨迹伪装成排名结果：

| arm | 合格 cells | Top-1 | 平均真实排名 | 平均 normalized regret |
|---|---:|---:|---:|---:|
| opaque | 14/15 | 5/14 | 3.14 | 0.274 |
| aligned_nominal | 14/15 | 3/14 | 3.36 | 0.296 |
| misindexed_nominal | 14/15 | 3/14 | 3.43 | 0.322 |

这些数值是本 block 的 bounded descriptive result；由于 3 个 crystallization cell 未完成，
不宣称 15/15 全 cell 的普适 arm-level 结论。

## 4. 收束决定

1. 本五世界三臂 block 关闭，失败单元及其原始 trajectory、summary、resource ledger 和
   replay 均永久保留。
2. 不补跑、不删除、不用替代 cell 补齐 45/45；后续分析使用 42 个合格 cell 作为动作
   指标分母，并单独报告 3 个失败。
3. 失败模式应作为结果边界的一部分：结晶任务暴露了自主流程规划的资源耗尽风险；另有
   一个独立的 provider/session 中断风险。
4. 原始 block 后续只做结果解释、图表和论文 claim-boundary 整合；repair 仅作为独立的
   技术敏感性结果，不再对原始 45-cell block 增加补齐实验。

机器汇总：

`runs/formal/work-ii-deepseek-multi-task-open-action-five-world-v0.1-20260817-formal2/summary.json`

## 5. seed2 / aligned_nominal 独立 repair 审计

为检验原始 `reaction-to-crystallization / seed2 / aligned_nominal` 是否只是
provider/session 中断，按原 experiment note 固定 protocol、candidate、资源、停止规则和
terminal contract，新开同线程 session 做了一次独立 repair。原始失败记录没有被覆盖：

`runs/formal/work-ii-multi-task-open-action-repair-v0.1-seed2-aligned-20260817/`

结果如下：

- 12/12 个实验完成，12/12 个 final assay 和 final checkpoint 均生成；
- provider error event 为 0；session 正常结束，terminal reason 为
  `campaign_complete`；
- hidden-boundary、execution audit、exact replay、tool integrity 和 usage reconciliation
  均通过；
- 但第 8 个实验中 agent 先提出 `seed_crystals(0.02 g)`，被固定资源账本以
  `stock_limit:seed_g` 拒绝，随后 agent 自主改为 `0.001 g` 并继续；该拒绝被原样保留，
  没有 host-side 自动修复；因此 repair qualification 的 `no_resource_rejection` 检查失败，
  repair cell 不属于合格动作指标分母；
- repair 仍然产生了可读的 held-out action readout：agent 选择 `c420`，真实排名第 8/8，
  `top1=false`，normalized regret 为 1.0；其 law 评估为 `inadequate_law__wrong_action`。

这条 repair 的科学含义是：原始中断确实可以在 fresh session 中被跨越，但该 agent 仍会在
结晶资源紧张时提出不可执行的 seed 动作，随后才调整。因此它同时支持“原始中断含有
session 层偶发成分”和“结晶任务存在 agent 资源规划风险”两个边界判断。repair 结果可写入
审计与补充分析，不能作为原始 45-cell formal aggregate 的替代 cell，也不能据此宣称
`aligned_nominal` 的正式 arm-level 性能。
