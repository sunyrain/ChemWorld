# Work II RX-P/S 五世界双目标执行协议 v1.0.1

状态：**启动门符号修正后重新冻结；尚无 provider source**
冻结日期：2026-09-19
任务编号：W2-131

本文件仅修正 [v1.0 master protocol](WORK_II_RX_PS_FIVE_WORLD_DUAL_GOAL_PROTOCOL_V1_0.md) 的 RX-S provider-free 启动门实现；其余60来源、720批、180后测、P/S profiles、prior、问题、资源、提示、真值隔离和失败规则全部不变。机器修正记录为 `configs/benchmark/work_ii_rx_ps_five_world_dual_goal_v1.0.1.json`。

## 1. 被保留的首次失败

v1.0 在 `runs/development/work-ii-rx-ps-five-world-dual-goal-20260919-v1` 完成P/S各12批工程路径，并完成RX-W01的18次S gate执行；所有执行和exact replay成功，三个条件均有3个独立噪声坐标，但继承的challenge helper返回information-choice与budget-window失败。此时provider calls为0，60个source均未启动。原目录永久保留，不覆盖、不删除，也不把修正后的判断回填到旧report。

## 2. 确认的实现错误

RX-S v1.1资格设计把结构效应定义为：

```text
gap(duration) = parent_deactivating_baseline - reversible_child
accumulation = gap(duration) - gap(shortest_duration)
```

这与真实parent、Aligned主张及“可逆通道随暴露时间产生更大后果”的科学问题一致。继承的challenge helper却计算 `reversible_child - parent`，因此同一个可逆效应越随时间增强，统计量越负，理论上永远无法通过正的`minimum_accumulation`。RX-W01三条件的`parent-child` yield gap由约`0.0099`增到`0.0679/0.0892`，conversion gap由约`0.0098`增到`0.0654/0.0818`，清楚暴露了符号反转。

## 3. 唯一修正

v1.0.1只把gate的paired gap恢复为资格协议已使用的`parent - child`方向，再计算相对最短时长的增长。绝对information、三噪声坐标要求、三个action、三个重复、阈值`0.03`、participant budget`4`和五world全过规则均不变。这是provider启动前的评价器纠错，不是依据Agent表现改题、改先验、降低阈值或追加有利条件。

v1.0.1在新的write-once目录从工程路径和全部90次S gate重新执行；不得复用旧目录冒充新版本。通过后才可启动60个Codex source sessions。
