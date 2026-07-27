# Scientific Adaptation 小规模 development 实验结果

日期：2026-07-25

状态：`development shakedown completed; formal_result=false; no method-effect claim`

本记录只覆盖新的 experiment-level Scientific Adaptation Track。它不修改 RC28 Gate A，不使用
formal/private namespace，不刷新 Evidence DAG，也不允许形成 C1、C2、C3 或 O1–O5 的正式结论。

## 1. 固定范围

- Task：`reaction-to-crystallization`；
- public pair：`2c17220fd0d51bdda1bd`；
- arms：changed rate-law family 与 no-change twin；
- methods：Pro/Flash × Direct/Stateful；
- v2 horizon：每个 cell `1 pre + 2 post`；
- v3 Stateful qualification：每个 cell `1 pre + 1 post`；
- r4 双任务资格：每个 cell `6 pre + 2 post`；
- Agent 选择完整 experiment plan；executor 只执行选择并机械 closeout；
- 每个 cell 独立 provider context，write-once terminal receipt；
- 所有 artifact 均声明 `formal_result=false` 和 `benchmark_claim_allowed=false`。

## 2. Mock 四格 shakedown

目录：`runs/development/scientific_adaptation_mock_shakedown_20260725`

| 项目 | 结果 |
| --- | ---: |
| Cells | 8 |
| 计划/完成实验 | 24/24 |
| Mock logical calls | 24 |
| 成本 | USD 0 |

该轮证明四格 materialization、changed/no-change 配对、跨 phase evidence ID、完整 recipe 执行、
机械 closeout、原子 receipt 和 `--resume` 均可运行。它不测试真实模型能力。

## 3. DeepSeek v1 runner diagnostic

目录：`runs/development/scientific_adaptation_deepseek_shakedown_20260725`

Pro Direct 两个 cells 均完成 3/3，已知 receipt 成本合计 USD 0.02308255。随后 Pro Stateful
返回非法 `scientific_state.belief`，validator 正确拒绝，但 runner 在写 terminal failure receipt
前退出。整个 v1 被标记为 `excluded_runner_diagnostic`，不得用于方法比较。

未落盘 Stateful attempt 的调用数下界为 1，实际费用未知。该缺口不以估算值填补。

## 4. DeepSeek v2 四格 shakedown

目录：`runs/development/scientific_adaptation_deepseek_shakedown_v2_20260725`

| Method | Arm | 完成实验 | Cell status | Failure |
| --- | --- | ---: | --- | --- |
| Pro Direct | changed | 3/3 | completed | — |
| Pro Direct | no-change | 3/3 | completed | — |
| Flash Direct | changed | 3/3 | completed | — |
| Flash Direct | no-change | 3/3 | completed | — |
| Pro Stateful | changed | 1/3 | method failure | controlled variables 超过 6 项 |
| Pro Stateful | no-change | 2/3 | method failure | 3 attempts 后仍为非法 JSON |
| Flash Stateful | changed | 0/3 | method failure | belief 未包含精确候选集合 |
| Flash Stateful | no-change | 0/3 | method failure | belief 未包含精确候选集合 |

汇总：

| 项目 | 结果 |
| --- | ---: |
| Completed/failed cells | 4/4 |
| 计划/完成实验 | 24/15 |
| Logical calls / provider attempts | 19/26 |
| Provider billed cost | USD 0.0668973804 |

Direct 四格全部完成，证明 experiment-level executor 消除了 operation-level 0/4 lifecycle
混杂。Stateful 失败主要来自输出合同，而不是物理流程失败。所有模型/schema 失败均 fail closed，
没有 harness 修复或科学重试。

## 5. Stateful schema v3 qualification

v2 后只把原有合同写得更明确：belief 必须含精确 candidate keys、controlled variables 最多 6
项、evidence IDs 必须来自公共 catalog。validator、候选答案、物理预算和 scoring 均未放宽。

目录：`runs/development/scientific_adaptation_stateful_qualification_v3_20260725`

| Method | Arm | 完成实验 | Cell status | Failure |
| --- | --- | ---: | --- | --- |
| Flash Stateful | changed | 2/2 | completed | — |
| Flash Stateful | no-change | 2/2 | completed | — |
| Pro Stateful | changed | 1/2 | method failure | 3 attempts 后仍为非法 JSON |
| Pro Stateful | no-change | 1/2 | method failure | 3 attempts 后仍为非法 JSON |

| 项目 | 结果 |
| --- | ---: |
| Completed/failed cells | 2/2 |
| 计划/完成实验 | 8/6 |
| Logical calls / provider attempts | 8/13 |
| Provider billed cost | USD 0.0335446294 |

显式 schema 修正使 Flash Stateful 从 v2 的 0/3 提升为两个 arms 均 2/2。Pro 的剩余失败均为
provider 在三次 attempts 后仍未返回合法 JSON，不能解释为科学性能失败。

## 6. 公平性、安全与成本审计

- 有合法首轮决策的 methods 使用相同 public-context SHA-256；
- Direct/Stateful 的公共上下文相同性另有 deterministic tests；
- 输出不保存 prompt、key 或 private reasoning；
- 八个 Scientific Adaptation development 目录共扫描 41 个文件，key 命中 0；
- 本轮真实 pilot 前已记账费用合计 USD 0.1755308828；加上 r4 真实 pilot 后为
  USD 0.5782915186，另有 v1 一个未落盘 attempt 的费用未知；
- v2/v3 均低于各自 USD 0.50/USD 0.20 停止阈值。

一次本地安全扫描命令因参数顺序错误，将 key 写入内部命令 stderr，但未写入任何实验 artifact。
该凭据随后已轮换；r4 真实 pilot 使用新 key，key 只注入执行进程环境，未写入 artifact。

## 7. Pro Stateful 根因与 runner 恢复加固

v4 新增脱敏 provider attempt ledger，只记录 request ID、usage、finish reason、content/reasoning
字符数和 parse error 类型，不保存响应正文。Pro Stateful 的第二决策三次 attempts 均为：

- `finish_reason=length`；
- `completion_tokens=4000`；
- reasoning 为 16k–17k 字符；
- 两次 content 为空，一次只有 789 字符。

因此 v3 的 Pro 非法 JSON 根因是 4k 输出预算被 reasoning 耗尽。runner 同时新增 experiment-level
checkpoint：基础设施失败只写 append-only attempt，不产生科学终端 receipt；`--resume` 可恢复公共
历史、Agent-authored state、资源账本，并只执行缺失实验。deterministic interruption test 已证明
实验编号和 evidence IDs 在恢复后保持连续。

按 backend 内公平原则，Pro Direct/Stateful 的 max output tokens 同步提高到 8,000。v5 不再截断，
但暴露原先“最多 6 个 controlled variables”的人为限制；该限制窄于 10 维 reaction recipe，属于
过度协议。r3 将上限放宽到 10，同时继续受 2,800 字符总状态上限约束。v6 Pro Stateful changed
资格测试随后 2/2 完成，2 calls/attempts，费用 USD 0.008258214。

## 8. r3 同版本四格 v7

目录：`runs/development/scientific_adaptation_r3_four_grid_v7_20260725`

该轮是当前唯一可横向审计的同版本小矩阵：四种 methods、两个 arms 均使用 r3 合同，每个 cell
`1 pre + 1 post`，不拼接早期方法版本。

| 项目 | 结果 |
| --- | ---: |
| Completed cells | 8/8 |
| 完成实验 | 16/16 |
| Logical calls / provider attempts | 16/16 |
| Infrastructure/method failures | 0/0 |
| Provider billed cost | USD 0.027685618 |
| First public-context hashes | 8/8 相同 |

资源边界：

- Direct 最大 prompt tokens：2,322，小于 3,600 cap；
- Stateful 最大 prompt tokens：2,898，小于 4,150 cap；
- Pro 最大 completion tokens：4,764，小于 8,000 cap；
- Flash 最大 completion tokens：721，小于 1,000 cap；
- 16 个 attempts 的 finish reason 全部为 `stop`，没有 provider retry。

这证明 r3 方法合同在最小四格真实 provider execution 中已具备运行资格。时域仍太短，不能估计
reference sufficiency、变化检测、regret AUC 或任何方法效应。

## 9. r3 双任务扩大时域 mock：执行通过、资源资格失败

目录：`runs/development/scientific_adaptation_r3_two_task_mock_20260725`

该轮首次同时 materialize 两个 Confirmatory Tasks，每任务 1 个 public pair，四方法 ×
changed/no-change，每个 cell `6 pre + 2 post`。

| 项目 | 结果 |
| --- | ---: |
| Completed cells | 16/16 |
| 完成实验 / logical calls | 128/128 |
| Infrastructure/method failures | 0/0 |
| Mock cost | USD 0 |

执行、accounting 和 missing-only resume 均通过，但资源资格不通过。第 8 次决策的估算输入最大达到：

- Direct：reaction 7,816，electrochemical 10,629 tokens；
- Stateful：reaction 8,495，electrochemical 11,345 tokens；
- r3 继承的 operation-level caps 只有 Direct 3,600、Stateful 4,150。

根因不是历史本身，而是公共适配器同时回放 raw observation 与 processed estimate、完整自由文本
计划，并在 evidence catalog 重复测量元数据。这与“单一 compact observation representation”的原
设计相冲突。因此 r3 只能证明多任务执行图可运行，不能作为真实 provider 扩大实验的 manifest。

## 10. r4 单一表示与双任务资格

r4 将 Scientific Adaptation prompt 合同从 operation-level 合同中独立出来，并把公共历史压缩为：

- 实验条件向量、测量选择、mechanism distribution 与 uncertainty；
- 唯一的 `processed_estimate + uncertainty + reward`，不再重复 raw observation；
- 终端 score/cost/risk；
- 最多 8 条历史，超长 campaign 固定保留最早 reference 半窗和最近半窗；
- evidence catalog 只列 exact IDs；完整原始 evidence 仍保留在 receipt，不进入 prompt。

接口版本升为 `chemworld-scientific-adaptation-interface-0.2-dev`。先在
`runs/development/scientific_adaptation_r4_two_task_prompt_profile_20260725` 用 12k 临时 ceiling
profile，再按 observed maximum 加 15% headroom 冻结：Direct 6,250、Stateful 7,100；同一 scaffold
上的 Pro/Flash 使用相同 cap。

最终目录：`runs/development/scientific_adaptation_r4_two_task_mock_qualification_20260725`

| 项目 | 结果 |
| --- | ---: |
| Freeze | `chemworld-participant-factorial-development-r4-2026-07-25` |
| Completed cells | 16/16 |
| 完成实验 / logical attempts | 128/128 |
| Infrastructure/method failures | 0/0 |
| Direct observed max / cap | 5,434 / 6,250 |
| Stateful observed max / cap | 6,157 / 7,100 |
| First public-context hashes | 每个 task 内 8/8 相同 |
| Prompt budget | 128/128 decisions within contract |
| Mock cost | USD 0 |

相对 r3 的最坏双任务输入，Direct 从 10,629 降到 5,434，Stateful 从 11,345 降到 6,157。
16 个 terminal receipts 的 method config、四个 method contract、runner 与 canonical receipt hashes
均可重算匹配；`--resume` 前后 16 个 receipt 文件 SHA-256 不变，infrastructure attempt 文件为 0。
448 个 evidence IDs 在各 receipt 内唯一，以 `method/pair/arm/evidence_id` 为地址时全局唯一；所有
128 个决策的 private/Gate-A truth supplied 计数为 0。

真实 pilot 的只读成本预审使用 r4 estimated input tokens、v7 同合同真实 completion 分布和冻结
provider pricing。每个 method 计划 32 calls：

| Method | Input tokens | v7 mean output/call | 预计费用 | 全部打满 output cap |
| --- | ---: | ---: | ---: | ---: |
| Flash Direct | 88,744 | 231.50 | USD 0.014498 | USD 0.021384 |
| Flash Stateful | 109,931 | 558.25 | USD 0.020392 | USD 0.024350 |
| Pro Direct | 88,744 | 2,365.75 | USD 0.104466 | USD 0.261324 |
| Pro Stateful | 109,931 | 3,539.00 | USD 0.146346 | USD 0.270540 |
| Total | — | — | **USD 0.285703** | **USD 0.577598** |

建议真实 development pilot 使用 `128 calls / USD 0.75` 的不可突破上限；该值给保守输出上界保留
额外运行余量，不是已批准预算，也不是 formal 成本估计。实际 usage、cache、retry 与 wall time 必须
从真实 receipts 重新审计。

该轮是 mock execution/resource qualification，不是模型能力实验。它没有使用外部 key，也不增加
已记账 provider 费用。

## 11. r4 双任务真实 provider development pilot

目录：`runs/development/scientific_adaptation_r4_two_task_deepseek_pilot_20260725`

执行使用轮换后的 key、r4 冻结合同、`128 calls / USD 0.75` cap。外层终端在 1 小时时限关闭后，
原 Python 进程继续完成 8 个 Pro terminal receipts，但随后因 stdout 断开退出；`--resume` 验证已完成
receipts 后只运行剩余 Flash cells。没有部分 cell 遗失，也没有重复执行已完成 Pro cells。

| 项目 | 结果 |
| --- | ---: |
| Terminal cells | 16/16 |
| Completed / method-failure cells | 13 / 3 |
| 完成 / 计划实验 | 115 / 128 |
| Logical calls / provider attempts | 118 / 121 |
| Provider retries | 3，均为 `finish_reason=length` 后成功 |
| Infrastructure failures | 0 |
| Provider billed cost | USD 0.4027606358 |
| Execution complete | true，仅表示无可恢复基础设施缺口 |

| Method | Completed cells | 完成实验 | Calls / attempts | Cost USD |
| --- | ---: | ---: | ---: | ---: |
| Pro Direct | 4/4 | 32/32 | 32/32 | 0.155090 |
| Pro Stateful | 3/4 | 29/32 | 30/32 | 0.209505 |
| Flash Direct | 3/4 | 30/32 | 31/31 | 0.018080 |
| Flash Stateful | 3/4 | 24/32 | 25/26 | 0.020085 |

三个 method failures 均保留为 terminal development 结果，不自动重试：

- Pro Stateful，electrochemical no-change twin：第 6 次决策的整个 `scientific_state` 超过
  2,800 字符上限，完成 5/8；
- Flash Direct，electrochemical no-change twin：第 7 次决策的 `belief_update_rule` 超过
  700 字符上限，完成 6/8；
- Flash Stateful，electrochemical changed：首轮 `varied_variable` 为空，完成 0/8。

真实 prompt 最大估算为 Direct Pro/Flash 5,432/5,449，Stateful Pro/Flash 6,591/6,404，均低于
6,250/7,100 cap。121 个脱敏 attempt records 中 118 succeeded、3 failed；三次失败均为
`invalid_structured_output` 且 `finish_reason=length`。总费用高于均值预审 USD 0.285703，但低于
全部输出打满的保守估计 USD 0.577598 和停止 cap USD 0.75。

描述性样本显示：

- 结晶 changed 的 Pro Stateful 把 rate-law belief 提高到 0.88，但 post 分数低于自身 pre；
- 对应 no-change twin 也把 rate-law belief 维持在 0.90，提示明显的过度归因风险；
- 电化学 changed 的 Pro Stateful 把 no-change belief 提到 0.50，且两次 post score 为 0，属于漏检加恢复失败；
- Flash Direct/Stateful 在结晶 changed 上均未显示 post 恢复优势；Flash 成本显著低于 Pro。

这些只是每 task 一个 pair 的 development 样本。不得据此比较 scaffold/backend 主效应，也不得计算
C1–C3、regret AUC 或 O1–O5。它们只证明当前接口能够同时暴露漏检、过度归因、识别后不恢复和
schema failure，而不是把所有失败压缩为一个 completion 指标。

审计结果：method/config/runner/canonical receipt hashes 全部可重算匹配；`--resume` 前后 16 个
receipt 文件 hash 不变；private/Gate-A truth supplied 为 0；17 个 artifact 文件中通用 key pattern
命中 0。reaction 任务的 8 个 cells 首轮 public-context hash 全部相同；electrochemical 为 7/7 相同，因
Flash Stateful changed 在首轮 validator 前失败，没有成功 plan audit，这是已记录的审计缺口。

## 12. WellAU Codex Sol high 单 backend development pilot

模型发现与兼容探针使用用户提供的 `key2.md`，只把 key 注入调用进程环境。认证后的
`GET https://api.wellau.com/v1/models` 返回精确 model ID `gpt-5.6-sol`；模型详情与 OpenAPI
端点均不存在。一次最小可能计费探针验证 `/chat/completions` 接受
`response_format={"type":"json_object"}`、`reasoning_effort="high"` 和 `max_tokens`，返回精确
model identity、合法 JSON 与 provider usage。该探针使用 317 input、12 output、329 total tokens。
模型目录和 key 文件均未提供可验证定价，因此禁止推算或填报 USD 成本。

独立配置：
`configs/methods/llm_v0.4/participant_methods_wellau_codex_sol_development.json`。单一 backend
只运行 Direct/Stateful 两种 scaffold，不复制无意义的 backend 轴。两方法沿用 r4 的两任务、每任务
1 pair、changed/no-change、`6 pre + 2 post`、compact history、terminal receipt、attempt ledger 和
missing-only resume 合同。Direct/Stateful prompt caps 分别为 6,250/7,100 estimated tokens，单次
output cap 均为 8,000；全轮额外冻结 64 logical calls 和 1,000,000 provider-reported total tokens。

稳定 mock 目录：
`runs/development/scientific_adaptation_r4_two_task_wellau_codex_sol_mock_20260725`。8/8 cells、
64/64 experiments/calls 完成，Direct/Stateful 最大 prompt 为 5,434/6,157；`--resume` 不改变 report
hash，9 个 artifact 文件没有通用 key pattern 命中。

真实目录：
`runs/development/scientific_adaptation_r4_two_task_wellau_codex_sol_pilot_20260725`。

| 项目 | 结果 |
| --- | ---: |
| Terminal cells | 8/8 |
| Completed / method-failure cells | 6 / 2 |
| 完成 / 计划实验 | 59 / 64 |
| Logical calls / provider attempts | 61 / 61 |
| Provider-reported input / output / total tokens | 249,688 / 104,669 / 354,357 |
| Infrastructure failures / provider retries | 0 / 0 |
| Wall time | 2,709.4 s |
| Provider billed cost | unknown；`accounting_complete=false` |

| Method | Completed cells | 完成实验 | Calls / attempts | Total / output tokens |
| --- | ---: | ---: | ---: | ---: |
| Codex Sol Direct | 4/4 | 32/32 | 32/32 | 161,752 / 42,002 |
| Codex Sol Stateful | 2/4 | 27/32 | 29/29 | 192,605 / 62,667 |

两个 method failures 均保留为 terminal development 结果，不自动重试：

- Stateful，reaction changed：第 5 次决策的整个 `scientific_state` 超过 2,800 字符上限，完成
  4/8，失败发生在 change 前，因此不能形成该 cell 的 post-change 判断；
- Stateful，electrochemical no-change twin：第 8 次决策的整个 `scientific_state` 超过
  2,800 字符上限，完成 7/8；第 7 次决策已把 `no_change` belief 降至 0.02，显示强假阳性。

描述性样本显示：

- reaction Direct 在 changed 与 no-change twin 的最终 `no_change` belief 都是 0.82，没有区分该
  pair；changed 的两次 post score 为 0.2997/0.2973，接近其较高 pre 水平；
- electrochemical Direct 在 changed 中把 `no_change` 降至 0.05，但两次 post score 都为 0；对应
  no-change twin 为 0.75，属于“能区分变化、没有恢复”的样本；
- electrochemical Stateful 在 changed 中把 `no_change` 降至 0.09，但两次 post score同样为 0；
  no-change twin 则在失败前降至 0.02，暴露过度归因；
- reaction Stateful no-change twin 最终 `no_change` 为 0.68，两次 post score 为 0.3982/0.3923；
  changed cell 在 changepoint 前失败，不能与 twin 作适应效果比较。

完整性审计通过：61 个 attempt records 全部 `succeeded/stop`，返回 model ID 均精确为
`gpt-5.6-sol`，单 attempt 最大 output 4,072，低于 8,000 cap；Direct/Stateful 最大 prompt 为
5,469/6,503，低于 6,250/7,100 cap。每个 pair 的四个 cell 首轮 public-context hash 完全相同，
所有成功决策的 private/Gate-A truth supplied 为 0。config、runner 和 8 个 canonical receipt hashes
均可重算匹配；类型收窄后的最终零调用 `--resume` 保持 8 个 receipt 文件逐字节不变，report SHA-256 为
`8b83ba26a5da36f796b7e6ab97979cc202baaee6803a6b89030b3826c6bf10b4`。9 个真实 artifact
文件中，精确 key 与通用 key pattern 命中均为 0。本轮 runner 创建的 Process-scope
`WELLAU_API_KEY` 注入已在 `finally` 中移除；工作站另有与 `key2.md` 相同的预存 User-scope
持久变量，它不是本轮创建，按主任务要求未删除，不能误写成 runner artifact 或进程残留。

真实实验外另有一次上述 329-token 兼容探针，因此本次授权下已知可能计费总量为 62 calls、
354,686 tokens；由于没有可验证价格，USD 总费用仍必须报告为 unknown。该 pilot 只提供跨 provider
的 development contract sensitivity 样本，不估计 provider、scaffold 或方法效应，不触碰
formal/private/Gate A。

## 13. 允许与禁止的解释

允许：

- 新 experiment-level executor 能稳定完成完整物理实验；
- Direct 主路径在本次小规模 shakedown 中可运行；
- Stateful schema 必须显式列出 exact candidate keys 和容量限制；
- Flash Stateful 在 schema 修正后通过了最小运行资格；
- Pro Stateful 的 4k structured-output 截断已定位并在 r3 最小资格矩阵中消失。
- r4 双任务 materialization、硬 prompt 预算和 resume 已通过 mock 资格。
- r4 双任务真实 provider pilot 已完整产生 16 个 terminal outcomes，费用和失败均可审计。
- WellAU `gpt-5.6-sol` high 的单 backend pilot 已产生 8 个 terminal outcomes，usage、失败和未知
  定价状态均可审计。

禁止：

- 比较 Direct 与 Stateful 的科学适应优劣；
- 比较 Pro 与 Flash 的科学性能；
- 从一个 pair 和短 horizon 估计 regret AUC、O1–O5 或 C1–C3；
- 将 v3 与 v2 Direct 拼接成同一冻结方法矩阵；
- 把 r4 mock 的零失败解释为真实 provider 或科学性能资格；
- 因三个 development method failures 事后放宽 schema，并把重跑结果拼回本轮；
- 因 development 结果修改 Gate A 或查看 private namespace。
- 把 WellAU 未知定价误写成 USD 0，或用本轮一个 pair/task 比较 provider/scaffold 优劣。

下一步先做 development-only failure/contract sensitivity 与 replay audit，区分必要的科学约束和
任意长度限制；任何 r5 修改都必须形成新 freeze 并完整重跑资格，不能覆盖本轮。随后才能围绕 C1
进入 power/cost audit；formal/private execution 仍然禁止。
