# DeepSeek 机制诊断 v0.1.1 严格重分析

- 状态：`strict_reanalysis_complete`
- 原始 v0.1 报告和轨迹保持不变；本文件只做可追溯重分析。
- ChemWorld 的角色是 Agent 能力测试/训练环境；本次评测不训练、不微调、也不更新 DeepSeek 权重。
- 当前仍不可发表为‘DeepSeek 已具备可靠机制发现能力’。

## 最终判断

The v0.1 run supports the benchmark-design story but does not establish reliable mechanism discovery by DeepSeek. Its sole former genuine result is a provisional threshold-level joint success with assisted campaign history.

原报告唯一的 `genuine_experimental` 现在降为 `provisional_threshold_joint_success`：确认级机制发现为 0，暂定阈值级联合成功为 1。原因不是抹掉结果，而是它来自单种子、两次 post-change 实验、尚无可识别性证书，且其 campaign 历史含系统辅助收尾。

## 结果与理解重新分类

| 任务 | 反馈 | 最终得分 | 真值概率 | 旧分类 | v0.1.1 分类 | 自主性 |
| --- | --- | --- | --- | --- | --- | --- |
| reaction-to-crystallization | true_feedback | 0.3973 | 0.1500 | joint_failure | joint_failure | fully_autonomous_campaign |
| electrochemical-conversion | true_feedback | 0.2570 | 0.3000 | joint_failure | joint_failure | fully_autonomous_campaign |
| reaction-to-crystallization | permuted_feedback | 0.4404 | 0.2500 | accidental_optimizer | high_outcome_without_identification | fully_autonomous_campaign |
| reaction-to-crystallization | delayed_feedback | 0.0028 | 0.2500 | accidental_optimizer | high_outcome_without_identification | autonomous_current_experiment_with_assisted_history |
| reaction-to-crystallization | critical_measurement_deleted | 0.3967 | 0.2000 | accidental_optimizer | high_outcome_without_identification | autonomous_current_experiment_with_assisted_history |
| electrochemical-conversion | permuted_feedback | 0.5176 | 0.3000 | joint_failure | joint_failure | fully_autonomous_campaign |
| electrochemical-conversion | delayed_feedback | 0.7578 | 0.5000 | genuine_experimental | provisional_threshold_joint_success | autonomous_current_experiment_with_assisted_history |
| electrochemical-conversion | critical_measurement_deleted | 0.2778 | 0.4000 | joint_failure | identification_without_recovery | fully_autonomous_campaign |
| reaction-to-crystallization | true_feedback | 0.5785 | 0.1000 | accidental_optimizer | high_outcome_without_identification | autonomous_current_experiment_with_assisted_history |
| electrochemical-conversion | true_feedback | 0.7629 | 0.1000 | accidental_optimizer | high_outcome_without_identification | fully_autonomous_campaign |

分类计数：`{"high_outcome_without_identification": 5, "identification_without_recovery": 1, "joint_failure": 3, "provisional_threshold_joint_success": 1}`。

## 自报分布更新审计

旧算法形成 201 个相邻 belief 对，其中 9 个涉及 `model_failure`，1 个跨过未产生模型 belief 的生命周期动作。清洁口径只保留相邻且两端都是 `model_decision` 的 191 对。
清洁口径下，平均自报信息值为 0.2524，平均 JS 分布变化仅 0.0021，平均 `Δlog q(truth)` 为 -0.0094。
这些量只能叫‘自报分布更新’，不能叫已校准 EIG 或 Bayesian posterior 更新。

## change probability 一致性

在 438 个有效模型决策中，独立上报的 `change_probability` 与 `1-q(no_change)` 的平均绝对差为 0.3138；71.23% 的决策差异超过 0.2。
v0.2 已删除这一重复自由度，变化概率一律由 `1-q(no_change)` 推导。

## 生命周期与自主性

共有 7 次系统收尾动作，影响 4/40 个实验、4/20 个阶段和 4/10 个独立 campaign。
因此不能再用 7/40=17.5% 同时代表动作率和实验覆盖率；正确实验影响率是 10%。
唯一暂定联合成功的最佳当前实验是自主完成的，但此前 shifted 实验有辅助 final assay，所以标为 `autonomous_current_experiment_with_assisted_history`。

## 排名与反馈的解释边界

平局改用 average rank；IID/shifted Spearman 仍为 0.0896，严格反转为 6 对。
recipe 级方法与 operation 级方法的决策接口不同，因此总体混合排名只保留为描述性结果。
旧的 `J_true-J_permuted` 平均值仍可作为分数对比，但不能解释为错误反馈更好或正确反馈降低性能；它没有隔离 provider 采样噪声。

## 资源与完整性

- 独立 DeepSeek campaign：10
- 模型调用：450；provider failure：10；重试：2
- 输入/输出 token：3984857 / 180916
- 估算费用：USD 0.499251
- 20 条阶段轨迹哈希核验：`True`

## 下一版的确认门槛

- Gate 0: integrity, leakage, receipts, exclusions, replay
- Gate A: active-oracle and fixed-decoder identifiability
- Gate B: paired no-change twins and randomized change time
- Gate C: local feedback sensitivity separated from provider noise
- Gate D: open-loop world effect, frozen policy, adaptation and recovery
- Gate E: procedural autonomy and separate assisted scientific score

在外部多种子 DeepSeek campaign 真正运行并通过全部 Gate 前，v0.2 状态必须保持 `publication_ready=false`。
