# Work II DeepSeek C2 current-composite 评估

> **HISTORICAL / PLATFORM-DEFECTIVE.** 本 v0.1 evaluator 未把冻结的 A-S `world_interventions`
> 传入 truth/blind runtime 与 exact replay。当前结果见
> `WORK_II_DEEPSEEK_C2_CURRENT_COMPOSITE_EVALUATION_V0.2_ZH.md`；本文件仅保留为恢复前记录。

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
| A_E | -0.2138 | -0.3592 | 0.990148 | +0.0004 | False |
| A_P | +0.0326 | -0.0063 | 0.079130 | +0.0326 | False |
| A_S | -0.2567 | -0.6476 | 1.000000 | -0.0432 | False |

Public C2 要求三个 locus 同时通过；当前 intersection-union 决策为 **False**，整体 p value 为 **1.000000**。

三个 locus 均存在从 pre 到 final 的平均预测误差下降，但注册检验要求错误先验相对正确先验获得更强修复。A-E 的 aligned noninferiority 通过，而 misindexed selective-improvement component 不通过；A-P 两任务方向均为正，但证据只达到 suggestive；A-S 中 crystallization 的 observed-point contrast 为正，partition 的负方向使跨任务 locus 失败。观察点敏感性仍不通过，因此总体结论不是删失规则单独造成的。

| Locus | Opaque pre→final | Aligned pre→final | Misindexed pre→final |
|---|---:|---:|---:|
| A_E | +0.1106 | +0.0970 | +0.0974 |
| A_P | +0.0895 | +0.0325 | +0.0651 |
| A_S | +0.1565 | +0.1921 | +0.1489 |

所以当前最重要的区分是：**general prediction learning 存在，但 targeted wrong-model repair 未被支持。**

## 规律恢复

| Locus | evaluated laws | law MAE | pre→law improvement | law−final error |
|---|---:|---:|---:|---:|
| A_E | 75/75 | 0.2765 | 0.0161 | 0.0855 |
| A_P | 30/30 | 0.2206 | -0.0156 | 0.0780 |
| A_S | 30/30 | 0.1851 | 0.1423 | 0.0236 |
| overall | 135/135 | 0.2438 | 0.0371 | 0.0701 |

135 条规律全部可以执行，说明 schema/executability 已闭环；但与 final explicit predictions 相比，law 更好/相等/更差为 **49/1/85**。A-S 的 pre→law improvement 最大，支持结构干预有一部分规律恢复信号；然而 `law−final error` 仍为正，说明当前 typed law 通常是有损压缩，而不是对最终 belief 的无损、可复用表达。

## Blind action

| Locus | evaluable cells | blind executions | mean gain | better/equal/worse |
|---|---:|---:|---:|---:|
| A_E | 68/75 | 408/450 | 0.0000 | 1/67/0 |
| A_P | 26/30 | 156/180 | 0.0000 | 0/26/0 |
| A_S | 27/30 | 162/180 | -0.0037 | 0/26/1 |
| overall | 121/135 | 726/810 | -0.0008 | 1/119/1 |

14 个 participant failed/right-censored cells 对应的 84 次 replay 按既定规则未启动，不被填成失败或零增益。两个非零 cell 分别是 A-E reaction-safety 的极小正增益和 A-S crystallization 的负增益；其余 119 个均与 incumbent 等价。当前 action 层证明的是重放稳定性，不是新方案发现。

## Evaluator 实现与缺陷修复

- evaluator 直接绑定 120 个未受平台缺陷影响的 public cells 与 15 个完整 A-S crystallization replacement cells，不混入 superseded block；
- 420/420 truth executions、675/675 checkpoint scores、135/135 law executions 和 726/726 launched blind executions 均落盘；
- 运行期间发现 A-S partition 的合法 evaluator query 可将 `settle_duration_s` 外推到 participant 搜索框之外。旧 truth compiler 错把搜索框当成物理 runtime 边界；现已按 runtime operation domain 直接编译，4 个外推 query 均保持原值，未 clip、未删除；
- 该修复只恢复 evaluator 的物理语义，不改变 participant 数据、注册 query、统计分母或判定阈值。

## 对论文大故事的贡献

这组结果不是最终投稿结论，而是 Work II 的第一张完整能力链剖面：实验搜索、counterfactual prediction、law compression 和 blind action 在同一 matched programme 中被独立测量，并显示三处转换损失。下一阶段可用 Study B 定位 seeking 与 updating，用 Study D 检验 artifact transfer，并用第二 provider 判断这些失效位置是否具有模型普适性。

## 解释边界

这是当前 public DeepSeek cohort 的完整 evaluator 闭环，也是更大研究计划的第一阶段证据；它不等于整篇 Paper 2 已完成。Private transfer、跨 provider 复现和新的开放式实验设计均未由本报告回答。所有 participant 失败、右删失和未启动 blind 分母均被保留。
