# 旗舰实验

ChemWorld 当前有两个任务完成了正式 Participant 多世界 campaign：
Electrochemical Conversion 和 Reaction to Crystallization。另有三个任务完成五世界
development-only 比较，使当前完整比较覆盖五项任务。本页说明实验问题、对照和结果；
项目整体状态以[证据与当前状态](benchmark_release.md)为准。

## 1. 实验问题

两组实验回答不同问题：

1. **S0 v1.0 无 dossier：**在匿名材料、固定 20 轮探索预算下，Participant 相对经典优化器表现如何？
2. **S0 v1.2 三臂：**正确材料信息是否有价值？定向错误信息是否会误导？模型能否从实验反馈中恢复？

这不是“给出真实性能已知的材料属性”。Nominal dossier 提供的是正确但有限的匿名材料属性；
真实性能仍需通过实验学习。Opaque 不提供 dossier，Misindexed 则固定交换目标材料字段的两行。

## 2. 共同冻结合同

| 项目 | 冻结值 |
| --- | --- |
| 任务 | 电化学转换；反应—结晶 |
| 独立世界 | seeds 0–9 |
| 自主探索预算 | 每任务×世界×臂 20 次完整实验 |
| Participant | Codex subscription，`gpt-5.6-sol`，medium reasoning |
| 主终点 | 配对盲测的最终推荐分数 |
| Replay | 所有正式单元精确通过 |
| 推断单元 | 独立 world；不是模型调用或算法技术 seed |

### 信息臂

| Arm | Agent 可见信息 | 因果角色 |
| --- | --- | --- |
| `opaque` | 匿名 ID，不提供材料 dossier | 无信息基线 |
| `nominal` | ID 对应正确匿名属性 | 正确信息 |
| `misindexed` | 目标字段固定两行互换；其他字段保持正确 | 定向错误先验 |

同一任务和 world seed 的三臂复用语义世界、观察噪声键、预算、模型、scaffold 和盲测端点。
因此配对差主要归因于 dossier 条件，而不是换了更容易的世界。

## 3. S0 v1.0：Participant 与经典基线

| 任务 | Codex | 95% 世界区间 | 最佳信息匹配基线 | 最佳 privileged calibration |
| --- | ---: | ---: | ---: | ---: |
| 电化学转换 | **0.7150** | [0.6283, 0.7861] | Structured RF-EI 0.6159 | Descriptor RF-EI 0.6441 |
| 反应—结晶 | **0.5355** | [0.5045, 0.5644] | LHS 0.5708 | 不适用 |

电化学相对最佳 information-matched 基线的描述性差为 +0.0991，但与最佳 privileged
calibration 基线的区间比较不稳定。结晶低于 LHS。由于没有预注册 superiority 阈值和多重比较
方案，这些结果不能升级为广义 SOTA 或 provider 因果效应。

## 4. S0 v1.2：三臂结果

### 正确信息价值

| 任务 | Opaque | Nominal | 配对差 | 双任务 familywise 97.5% 区间 | 决策 |
| --- | ---: | ---: | ---: | ---: | --- |
| 电化学转换 | 0.7150 | **0.7874** | +0.0724 | [+0.0074, +0.1546] | 正信息价值 |
| 反应—结晶 | 0.5355 | **0.5615** | +0.0260 | [−0.0130, +0.0630] | 不确定 |

### 错误先验与恢复

| 任务 | Misindexed | Misindexed − Nominal | 操纵检验 | 差分动作纠偏 | 性能恢复至 Opaque | 整体恢复 |
| --- | ---: | ---: | --- | --- | --- | --- |
| 电化学转换 | 0.6853 | −0.1020；[−0.2101, −0.0078] | 通过 | 通过 | 未通过 | **未通过** |
| 反应—结晶 | 0.5845 | +0.0229；[+0.0046, +0.0419] | 通过 | 未通过 | 通过 | **未通过** |

整体恢复采用联合规则：错误信息必须先实质性影响早期动作，随后动作相对早期误导方向纠偏，
且最终性能恢复到 opaque 的实用界限内。单独满足其中一项不能称为“识别并纠正错误先验”。

结晶中的 Misindexed 得分反而高于 Nominal，只能表述为这次固定映射在采样世界中的收益。
它没有通过动作纠偏，因此不是模型发现 dossier 错误的证据。

## 5. 规模与审计

| 项目 | S0 v1.0 | S0 v1.2 三臂 |
| --- | ---: | ---: |
| 正式单元 | 20 | 60 |
| Participant provider 调用 | 420 | 1,260 |
| Participant 物理实验 | 760 | 2,280 |
| 含经典基线的物理实验 | 28,060 | 不重复计入基线 |
| 自动重试 | — | 5 |
| 方法失败 | 0 | 0 |
| 精确 replay | 全部通过 | 全部通过 |

三个 arm 复用 v1.0 的 opaque 结果，因此不能把 v1.0 与 v1.2 的 opaque 再当作独立样本。

## 6. 证据入口

- [v1.0 正式 summary JSON](https://github.com/sunyrain/ChemWorld/blob/main/workstreams/flagship_tasks/reports/static-s0-v1.0-formal-campaign-summary.json)
- [v1.2 三臂 summary JSON](https://github.com/sunyrain/ChemWorld/blob/main/workstreams/flagship_tasks/reports/static-s0-v1.2-three-arm-information-campaign-summary.json)
- [v1.2 中文结果审计](https://github.com/sunyrain/ChemWorld/blob/main/workstreams/flagship_tasks/STATIC_S0_V1_2_THREE_ARM_INFORMATION_RESULTS_ZH.md)
- [v1.2 预注册](https://github.com/sunyrain/ChemWorld/blob/main/workstreams/flagship_tasks/STATIC_S0_V1_2_MISINDEXED_INFORMATION_PREREGISTRATION_ZH.md)

## 7. 与机制适应的边界

静态三臂研究的是**先验信息如何改变一个固定世界中的搜索**。机制适应研究的是**规律在
campaign 中途变化后，Agent 能否检测、归因并恢复**。二者共享“证据能否纠正先验”的主叙事，
但不是同一个实验，不能用静态三臂结果替代 Gates B–E。

RC28 Gate A 只认证了历史冻结环境的可识别性和在线可达性；当前源码绑定已过期，Participant
Gates B–E 仍待执行。详细当前边界见[证据与当前状态](benchmark_release.md)。

## 8. 五任务 post-qualification 扩展

在当前源码 `74cfcdaa0d9780de2d21424ef8c329079554f8b5` 上，五个任务使用同一份中性
Codex prompt、world seed 0–4、20 轮探索和 3+3 次盲验证，并与五种经典方法比较。
这是完整审计的开发证据，不是正式 superiority 研究。

| 任务 | Codex | 最佳经典方法 | 差值 | 逐世界对当世最佳胜/平/负 |
| --- | ---: | ---: | ---: | ---: |
| 电化学转换 | **0.7454 ± 0.0522** | RF-EI 0.6622 | +0.0832 | 3 / 0 / 2 |
| 反应—结晶 | 0.5206 ± 0.0681 | **RF-EI 0.6071** | −0.0866 | 1 / 0 / 4 |
| 反应—蒸馏 | **0.4795 ± 0.0264** | GP-EI 0.4192 | +0.0603 | 4 / 0 / 1 |
| 分配规律 | 0.5426 ± 0.0870 | **GP-EI 0.5511** | −0.0085 | 1 / 0 / 4 |
| 连续流优化 | 0.1627 ± 0.0131 | **GP-EI 0.2145** | −0.0518 | 0 / 0 / 5 |

五任务合计 150 个方法×世界单元、3,900 次物理实验，全部精确 replay。新 13D
反应—蒸馏任务在五个世界中均达到任务阈值；partition 则没有任何方法跨世界达到冻结的
0.58 门槛。跨任务绝对分数不作直接比较。

- [五任务机器可读摘要](https://github.com/sunyrain/ChemWorld/blob/main/workstreams/flagship_tasks/reports/static-s0-five-task-postqualification-campaign-summary.json)
- [五任务中文结果审计](https://github.com/sunyrain/ChemWorld/blob/main/workstreams/flagship_tasks/STATIC_S0_FIVE_TASK_POSTQUALIFICATION_RESULTS_ZH.md)
