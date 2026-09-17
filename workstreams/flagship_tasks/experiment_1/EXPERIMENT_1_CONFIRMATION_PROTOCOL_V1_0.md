# Experiment 1 Confirmation and Challenge Protocol v1.0

状态：**FROZEN BEFORE CONVERGENCE REDESIGN**  
适用范围：Experiment 1 全部 candidate participant-ready loci

## 1. 两阶段证据语义

`development qualification` 用于发现设计缺陷，不是最终 release evidence。
`confirmation qualification` 用于检验冻结设计是否能推广到未参与 redesign 的公开坐标和
独立噪声。两者必须分别记录 run id、config digest、truth/prior digest、denominator 和失败。

当前 EC 15/15 只能称 `qualified-development`，直到本协议下的 confirmation 完成。

## 2. Freeze boundary

每个进入 confirmation 的 `system × locus` 必须先提交并绑定：

- system/locus version 和 executable source commit；
- W01–W05 private-truth digest；
- aligned/opaque/misspecified prior digest；
- public contract、Participant budget 和 Q1–Q8 thresholds；
- development diagnostic coordinates；
- confirmation coordinate generator version；
- confirmation noise generator version与 seed commitment；
- challenge-audit rules。

任何上述对象在 confirmation 后改变，都使该 confirmation 失效。

## 3. Confirmation-set isolation

Confirmation 坐标不得是 development 坐标的简单重复，也不得在 candidate selection 中使用。
每个 locus 的 generator 必须：

1. 从同一合法公开操作域中生成；
2. 保持任务预算和仪器合同不变；
3. 覆盖 development 判别区域之外至少两个预注册 region；
4. 在运行前只公开 generator id、domain 和 commitment，不公开 realized coordinates；
5. 对五个 Worlds 使用同一生成规则，不按单个 World 挑选容易点。

Secret salt 只存服务器的非 Git 权限受限文件；Git 只保存其 SHA-256 commitment。运行完成后，
evidence receipt 保存 salt disclosure、realized coordinates 和 digest，以允许精确 replay。作者不得
在 confirmation 前读取 realized set。若受同一操作者限制，只能声明
`process-isolated confirmation`，不得夸大为第三方独立验证。

## 4. Noise 与 replay

- Confirmation 使用与 development 不同的 keyed-noise namespace；
- replicate 数和 Gate 阈值必须在看到结果前冻结；
- primary execution 和 tolerance-zero replay 都必须完成；
- 缺失、异常或 non-finite execution 必须进入 denominator，不能静默丢弃；
- confirmation 是 one-shot；失败 set 退休，不能在同一 set 上迭代设计。

## 5. Confirmation decision

每个 atomic unit 仍按相同 Q1–Q8 全硬门判断。一个 locus 只有 W01–W05 全部通过才是
`qualified-confirmed`。一个 World 的 PASS 不能抵消另一个 World 的 FAIL，也不能以平均效应
替代预算内反证。

## 6. Challenge audit

每个候选 locus 在 confirmation 前必须执行：

| 检查 | Frozen requirement |
| --- | --- |
| Schema symmetry | A/M public shape、字段、精度、置信度、近似长度一致 |
| Plausibility | false claim 位于 system-specific plausible envelope |
| Non-triviality | 默认/one-shot recipe 不得跨全部 Worlds 稳定判别 |
| Information choice | 至少一个主动选择的实验对 posterior/decision 有实质信息价值 |
| Budget window | 最小可靠反证成本 `> trivial_lower_bound` 且 `<= participant_budget` |
| Consequence | 至少一个预注册策略区的 decision/action/utility regret 为正 |
| Leakage | public observation/prompt/path/hash 不泄漏 arm、seed、truth family |

难度标签（easy/medium/hard）只能依据冻结运行后的 cost 和 effect/noise margin 描述，不能为满足
配额反向调整样本。

## 7. Candidate selection isolation

结构候选比较必须使用独立 calibration Worlds 或 analytic calibration design，不得用正式五个
Worlds 的 confirmation 坐标选择赢家。候选必须展示无法由一个允许的标量重拟合吸收的结构差异。
冻结后只能有一个 family pair 进入正式 denominator；未选候选保留为 authoring evidence。
