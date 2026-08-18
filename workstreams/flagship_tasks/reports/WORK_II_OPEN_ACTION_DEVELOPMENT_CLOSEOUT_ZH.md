# Work II 开放动作开发阶段收束（2026-08-17）

状态：开发证据终态整理；不升级为 formal claim，不触发 release freeze。

## 1. 结论先行

当前开放动作支线已经回答了两个阶段性问题。

第一，平台已经能够让同一 persistent agent 在多个物理化学任务中自主完成 12 轮实验、按
`0/3/6/9/12` 提交 belief checkpoints，并在最终 checkpoint 后对结果未知、但操作计划完整公开的候选
进行排序。A-S partition 五世界矩阵完成 `15/15` sessions、`180/180` participant experiments、
`120/120` provider-free truth 与 `120/120` exact replay，public/truth plan binding 全部通过；其中
`13/15` cells 满足完整资格，另外 2 个保留为 campaign/checkpoint 不完整。

第二，接口跑通不等于决策能力已经闭环。A-S 五世界矩阵 `0/15` 选择真实 Top-1；13 个合格 cell 中，
opaque、aligned、misindexed 的平均选择名次分别为 `4.25/6.50/6.60`，平均 normalized regret 为
`0.3671/0.7658/0.7477`。全部 15 个 terminal readout 中，`2` 个属于 adequate-law/wrong-action，
`13` 个属于 inadequate-law/wrong-action。这个结果直接支持“机制表述质量与新动作选择质量必须分开测量”，
但由于本 block 是 development、仅 3 个完整三臂 clusters，不能据此给出 arm-level 因果结论。

## 2. A-S 五世界开放动作矩阵

| arm | scheduled | eligible | mean selected rank | Top-1 | mean normalized regret |
|---|---:|---:|---:|---:|---:|
| opaque | 5 | 4 | 4.25 | 0 | 0.3671 |
| aligned_nominal | 5 | 4 | 6.50 | 0 | 0.7658 |
| misindexed_nominal | 5 | 5 | 6.60 | 0 | 0.7477 |

两个不合格 cell 都完成了 12 轮实验并提交排序，但 campaign/checkpoint 完整性未通过；它们继续留在
`15` 个 scheduled denominator 中，不从分析中消失。候选 ActionPlan、truth plan 与执行计划的 binding
通过，候选 outcome 和 rank 对 participant 保持隐藏，所以当前主要失败不是 evaluator 偷加操作或候选泄漏，
而是 agent 从自主实验轨迹到新计划排序的 transfer 质量不足。

这一矩阵深化了 W2-43 单世界 canary 的观察：agent 会形成内部规律、会持续利用反馈，也会在终点给出
连贯解释，但局部优化经验、机制近似和候选区的真实排序可能错位。尤其是正确或更准确的 law 并不自动
给出正确 action；本矩阵中两个达到 law adequacy 的 readout 仍然选错。

## 3. B3/B4 的处置

- B3 完成 provider-free 结构可辨识性资格，但它本身不构成 participant action 结果。
- B4 两轮 law-guided decision 共尝试 `15/15` cells，完成 `11/15`，只有 `3/5` 完整 clusters；4 个失败
  全部为 participant schema failure（2 个 decision type、1 个 post status、1 个 pre-final payload），
  不是 provider、物理 runtime 或资源失败。
- B4 的 11 个完成 cell 为 `0/11` Top-1、`0/11` exact family recovery、`0/11` exponent-within-0.10。
  该 block 保留为“不完整的固定证据/两轮终端协议诊断”，不补跑，也不进入当前论文分母。
- W2-48 的 12 轮开放探索 + 完整公开 ActionPlan 更接近当前科学问题，已取代 B4 作为开发主结果；若未来
  需要 formal action claim，应在一次新的 release freeze 后运行 fresh block，而不是修补 B4。

## 4. 多任务开放动作资格

最初单世界 pilot 暴露了电化学 solvent stock 和结晶 catalyst/seed/time reserve 不足。资源契约按已观察
失败类别固定修正并从首 arm 重跑后，最新 v2 recovery 得到：

| task | eligible sessions | experiments | truth / replay | selected true ranks（opaque/aligned/misindexed） |
|---|---:|---:|---:|---|
| electrochemical-conversion | 3/3 | 36/36 | 16/16 + 16/16 | 2 / 8 / 1 |
| reaction-to-crystallization | 3/3 | 36/36 | 16/16 + 16/16 | 4 / 4 / 4 |

原 pilot 中 reaction-safety-constrained 已为 `3/3` eligible、`36/36` experiments、`16/16` truth 与
`16/16` replay，三臂都选择真实第 2 名。因而以各任务最新未污染 block 计，完整 ActionPlan + ranking-only
协议已在 electrochemical、crystallization、reaction-safety 三个额外任务达到 `9/9` eligible sessions、
`108/108` participant experiments；加上 A-S partition，说明开放动作 harness 不是单任务特例。

这些都仍是单世界或 development 证据。电化学中 misindexed 反而 Top-1、aligned 排第 8，结晶和 safety
三臂给出相同选择，均不能解释为先验臂稳定效应；它们的价值是平台跨任务资格和后续任务选择，而不是
扩大论文主张。

## 5. 当前科学结论

1. 从“会做实验”到“会形成数值预测”、再到“会形成结构规律”和“会选对新动作”是至少四个可分离层级。
2. 12 轮自主实验足以让 agent 形成稳定叙述和局部策略，但对未见完整计划的排序仍可能系统失真。
3. 正确先验不保证更广的探索覆盖；局部最优化可能让 aligned arm 在候选分布发生变化时更难迁移。
4. 完整公开 ActionPlan 解决了旧 feature-only packet 的语义缺口，因此当前负结果不能再归因于 evaluator
   隐藏了执行流程。
5. 当前证据支持把“科学智能”写成由 evidence acquisition、numerical revision、structural
   identification 和 action transfer 组成的能力链，而不是单一 leaderboard endpoint。

## 6. 收束决定

- 保留：DeepSeek C2 public、current-composite evaluator v0.2、A-P Study B、A-S B2 作为当前论文基线；
  W2-48 和多任务 open-action 作为下一层 development evidence。
- 归档/终止：B3 provider-free qualification、B4 incomplete protocol、W2-41/42/47 diagnostics、
  W2-44–46 matched-action negative branch；不追加同型补跑。
- 延期：Study D、A-E private、cross-provider replication。它们是下一阶段研究选择，不是本次收束欠账。
- 若未来升级为 formal action claim：冻结稳定后的 open-action execution surface，使用 fresh worlds 从首单元
  完整运行；不拼接当前 development records。

## 7. 完整性检查

- 当前没有正在运行的 provider/experiment 进程。
- 本次相关平台与 evaluator 聚焦测试：`81/81` passed。
- raw provider payload 与 `runs/` 继续只保留在本地；本报告只记录可公开的分母、失败和结论边界。
