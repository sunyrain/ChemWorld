# Work II DeepSeek C2 current-composite 评估

本报告把修复后的 A-S crystallization 完整替换块与其余 public participant 结果组合，完成 provider-free 的科学纠错、规律恢复和 blind action 评估。

## 完整分母

- Participant cells：**135**；matched worlds：**45**。
- Participant 终态：completed=121，failed=7，right_censored=7。
- Held-out truth：**420/420**；checkpoint：**675/675**。
- Final typed law：**135/135**；blind executions：**726/810**，其中未启动 **84** 次属于 participant 失败/右删失的预定分母。
- Evaluator provider calls：**0**。

## 科学纠错

| Locus | failure-aware contrast | lower bound | p value | observed-point contrast | gate |
|---|---:|---:|---:|---:|---:|
| A_E | -0.2138 | -0.3592 | 0.990148 | 0.0004 | False |
| A_P | 0.0326 | -0.0063 | 0.079130 | 0.0326 | False |
| A_S | -0.2241 | -0.6286 | 1.000000 | -0.0066 | False |

Public C2 要求三个 locus 同时通过；当前 intersection-union 决策为 **False**，整体 p value 为 **1.000000**。

三个 locus 均存在从 pre 到 final 的平均预测误差下降，但注册检验要求错误先验相对正确先验获得更强修复。A-E 的 aligned noninferiority 通过，而 misindexed selective-improvement component 不通过；A-P 两任务方向均为正，但证据只达到 suggestive；A-S 中 crystallization 的局部信号被 partition 的负方向抵消。观察点敏感性仍不通过。

| Locus | Opaque pre→final | Aligned pre→final | Misindexed pre→final |
|---|---:|---:|---:|
| A_E | 0.1106 | 0.0970 | 0.0974 |
| A_P | 0.0895 | 0.0325 | 0.0651 |
| A_S | 0.2194 | 0.2276 | 0.2210 |

所以当前最重要的区分是：**general prediction learning 存在，但 targeted wrong-model repair 未被支持。**

## 规律恢复

| Locus | evaluated laws | law MAE | pre→law improvement | law−final error |
|---|---:|---:|---:|---:|
| A_E | 75/75 | 0.2765 | 0.0161 | 0.0855 |
| A_P | 30/30 | 0.2206 | -0.0156 | 0.0780 |
| A_S | 30/30 | 0.1552 | 0.2059 | 0.0167 |
| overall | 135/135 | 0.2371 | 0.0513 | 0.0686 |

135 条规律全部可以执行，但与 final explicit predictions 相比，law 更好/相等/更差为 **50/1/84**。可执行性与高保真规律压缩因此必须分开。

## Blind action

| Locus | evaluable cells | blind executions | mean gain | better/equal/worse |
|---|---:|---:|---:|---:|
| A_E | 68/75 | 408/450 | 0.0000 | 1/67/0 |
| A_P | 26/30 | 156/180 | 0.0000 | 0/26/0 |
| A_S | 27/30 | 162/180 | -0.0044 | 0/26/1 |
| overall | 121/135 | 726/810 | -0.0010 | 1/119/1 |

14 个 participant failed/right-censored cells 对应的 84 次 replay 按既定规则未启动，不被填成失败或零增益。当前 action 层证明的是重放稳定性，不是新方案发现。

## Evaluator 实现与缺陷修复

- Evaluator 直接绑定 120 个未受平台缺陷影响的 public cells 与 15 个完整 A-S crystallization replacement cells，不混入 superseded block。
- v0.1 truth/blind 路径未把冻结的 `world_interventions` 传入 runtime 与 exact replay；v0.2 在新输出根从第一单元完整重跑，旧结果仅保留为历史缺陷证据。
- A-S partition 的合法 evaluator query 可将 `settle_duration_s` 外推到 participant 搜索框之外。Truth compiler 已按物理 runtime domain 直接编译，4 个外推 query 未 clip、未删除。
- 该修复不改变 participant 数据、注册 query、统计分母或判定阈值。

## 解释边界

这是当前 public DeepSeek cohort 的完整 evaluator 闭环，也是更大研究计划的第一阶段证据；它不等于整篇 Paper 2 已完成。Private transfer、跨 provider 复现和新的开放式实验设计均未由本报告回答。所有 participant 失败、右删失和未启动 blind 分母均被保留。
