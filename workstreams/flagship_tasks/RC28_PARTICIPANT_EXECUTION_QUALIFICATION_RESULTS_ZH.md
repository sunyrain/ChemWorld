# RC28 Participant-Agent 执行资格结果

状态：`S0 passed; Flash Direct and Stateful autonomously runnable but 0/4 lifecycle completion; S3/Pro blocked`

日期：2026-07-25

本记录只回答方法是否可运行、失败是否可归因。它不是 Gate B–E 的科学性能结果，不改变已经通过并
冻结的 Gate A，也不支持 publication claim。

## 1. 采用的资格顺序

按专家建议执行：

1. S0：离线最坏合法 prompt、生命周期可见性、reference failure 语义；
2. S1：Flash-Direct，同一 reaction-to-crystallization changed/no-change pair，`1 pre + 1 post`；
3. S2：Flash-Stateful，同一 pair 和相同公共环境视图；
4. 仅在 S1/S2 通过运行资格后才允许 S3 小矩阵和 Pro compatibility smoke。

所有 provider run 均满足：

- `formal_result=false`；
- lifecycle assistance 关闭；
- harness 不选择 terminate、final assay 或科学实验；
- changed/no-change 使用 pair `2c17220fd0d51bdda1bd`；
- 每个 arm 只执行 `1 pre + 1 post`；
- 该短时域不能评价 reference sufficiency、变化检测或机制归因。

## 2. S0：离线 prompt qualification

新增可重复运行入口：

```text
scripts/qualify_participant_prompts.py
```

它使用两个 Confirmatory Tasks 的真实环境和合法 midpoint recipe，覆盖 setup、反应/电解中期、测量后、
结晶后、terminate 前后、final assay 后的新实验入口，并注入最大公开光谱目录、最大 recent memory 和
接近上限的合法 scientific state。

结果：

| 项目 | 结果 |
| --- | ---: |
| fixtures | 50 |
| provider calls | 0 |
| 必需字段、动作边界、lifecycle、无 raw array | 全部通过 |
| Direct/Stateful 环境视图哈希 | 全部相同 |
| runtime reduction/truncation | 0 |
| Direct 最坏未压缩 prompt | 3,089 estimated tokens |
| Stateful v0.4 最坏未压缩 prompt | 3,568 estimated tokens |

按最坏合法值加 15% 余量，development envelope 冻结为：

| Scaffold | environment view | Agent memory | per decision total |
| --- | ---: | ---: | ---: |
| Direct | 2,050 | 950 | 3,600 |
| Stateful v0.4-dev | 2,050 | 1,350 | 4,150 |

因此 1,500 不再被当成科学阈值。两种 scaffold 共享相同 environment-view budget；Stateful 只因其
Agent 自写的持久科学状态获得额外 memory budget。campaign ceiling 按
`per_decision_max_estimated_tokens × frozen_operation_limit` 记录，provider-reported tokens 仍是费用
真值。

## 3. 生命周期与 reference evaluator 修正

每轮 compact state 现在显式包含：

- `experiment_action_count`；
- `experiment_action_limit`；
- `ordinary_action_slots_remaining`；
- `reserved_closeout_slots=2`；
- `experiment_terminated`；
- `final_assay_available`；
- `closeout_status`。

公开动作上限与生命周期帮助已拆开：runner 默认只公开契约，不再自动 terminate 或 final assay。旧
guardrail 只能在显式 assisted diagnostic 中启用。

新增 evaluator-only `reference_acquisition`：

- 旧世界阶段未完成时，明确给出
  `reference_acquisition_failed=true` 和 `incomplete_prechange_experiment`；
- `1 pre` smoke 即使完成，也只会标记
  `development_horizon_insufficient_for_reference_evaluation`；
- relation coverage 与 predictive sufficiency 未执行前绝不误报 reference pass；
- 该状态不返回给 Agent，不提前暴露 changepoint，也不排除后续轨迹。

## 4. S1：Flash-Direct

`s1-flash-direct-autonomous-v1` 因首次前台进程超时后未实际退出，曾与后台进程短暂并发写同一目录；
该目录被明确排除，不作为证据。下表只使用干净的单进程 v2。

| 指标 | v2 结果 |
| --- | ---: |
| logical decisions / provider attempts | 72 / 72 |
| successful provider attempts | 72 |
| prompt overflow / reduction | 0 / 0 |
| 最大 prompt estimate | 2,017 |
| harness lifecycle actions | 0 |
| 完整实验 | **0/4** |
| input / output tokens | 136,770 / 18,145 |
| 费用 | USD 0.0234205664 |

行为归因：

- changed 的 iid/shifted 均从未 terminate，后期反复 HPLC；
- no-change 的 iid/shifted 都到第 18 步才 terminate，已没有第 19 步执行 final assay；
- 生命周期字段存在、prompt 未截断、provider 正常，因而这是 Direct reactive policy 的真实
  lifecycle-autonomy failure；
- `reference_acquisition_failed=true` 是旧世界实验未完成的 evaluator 结论，不是机制识别结论。

绑定的 campaign 摘要：

| Arm | SHA-256 |
| --- | --- |
| changed | `b0c860504e3456a0b82752c6f258cf48b994dd276d81a402c449574f6b6e383a` |
| no-change twin | `1be50d17f052ced99452e37c783c5e5e808af59d2848eb43cad3ccfc96c81aba` |

## 5. S2：Flash-Stateful

首次 v0.3-dev S2 的 72 个决策中有 14 个因 `scientific_state` 超过人为的 700 字符总上限被拒绝。
字段级 schema 允许的内容明显大于该总上限，因此该轮被判为 scaffold-envelope diagnostic，不解释为
科学失败。

v0.4-dev 保持字段、公开证据来源、最多两个计划项和两个证据项不变，只把 state 总上限改为 1,400
字符，并用接近上限的合法 fixture 重算 prompt envelope。干净 v2 结果为：

| 指标 | v2 结果 |
| --- | ---: |
| logical decisions / provider attempts | 72 / 73 |
| successful / failed provider attempts | 72 / 1 |
| failed attempt 类型 | `invalid_structured_output`，自动重试成功 |
| 本地 response normalization failure | 1（空 `campaign_plan[1].step`） |
| prompt overflow / reduction | 0 / 0 |
| 最大 prompt estimate | 2,231 |
| harness lifecycle actions | 0 |
| 完整实验 | **0/4** |
| input / output tokens | 148,773 / 33,854 |
| 费用 | USD 0.0295346296 |

700 字符 blocker 已消失。剩余行为主要是重复 add_reagent 与 HPLC，四个阶段均未及时 terminate/final
assay。因此 Stateful v0.4 的失败也已经可以归因为 Agent-system 流程行为，而不是 prompt
infrastructure。

绑定的 campaign 摘要：

| Arm | SHA-256 |
| --- | --- |
| changed | `dd7b4b6209878544f007612a29ee2ef7c15009db286d64346c44b0f2d5d8cf25` |
| no-change twin | `289b03d711f4c3f5b5ac6d2e2438a6f84544efb7e626b6eeca90bcebcef93844` |

## 6. 当前决策

```text
Gate A environment certificates: passed and frozen
S0 prompt/infrastructure qualification: passed
Flash-Direct lifecycle autonomy: failed, attributable
Flash-Stateful v0.4 lifecycle autonomy: failed, attributable
S3 small development matrix: not started
Pro compatibility smoke: not started
Formal participant matrix: prohibited
Publication ready: false
```

不再修改环境或启用 harness closeout 来“修复”上述结果。下一步应先决定 participant 方法学边界：

1. 将 Direct/Stateful 保留为可运行但流程失败的负基线，并接受 Gate E 可能接近零；或
2. 在 development namespace 中新增真正的 multi-step Agent controller，并将其规划、验证、retry、
   tool loop 和生命周期自治全部声明为被测 Agent 的组成部分，而不是 harness 帮助。

在该选择冻结前，不启动 S3、Pro 或正式 provider matrix。
