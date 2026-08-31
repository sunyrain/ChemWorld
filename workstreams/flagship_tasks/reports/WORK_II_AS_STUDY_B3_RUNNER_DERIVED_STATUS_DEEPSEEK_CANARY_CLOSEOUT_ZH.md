# Work II A-S Study B3 runner-derived-status DeepSeek canary 终态收束

状态：`terminal_canary_rejected_before_formal`；启动决策：`terminal_outcome`。

DeepSeek `deepseek-v4-flash / high` 的三条 fresh canary sessions 全部发起，最终为
`0/3 completed + 3/3 failed`。三条 session 均各尝试一次、各取得两轮 completed provider
receipt：合计 `6/6` completed turns、返回码均为 `0`、`0` provider errors、`0` retries、
`0` infrastructure predecessors、`0` tools、`0` participant physical experiments。每条 session
的两份 receipt 使用相同 thread ID；由于 post schema 未通过，结果对象没有把
`same_thread` 提升为已完成会话指标。

| arm | 终态 | post family | exponent | predictions | 直接失败 | elapsed |
|---|---|---|---:|---:|---|---:|
| opaque | failed | FAMILY_A_LINEAR | 1.0 | 8 | post selected action index is invalid | 445.406 s |
| misindexed_nominal | failed | FAMILY_A_LINEAR | 1.0 | 8 | post selected action index is invalid | 541.968 s |
| aligned_nominal | failed | FAMILY_B_POWER | 1.0 | 8 | post selected action index is invalid | 618.514 s |

三条 post payload 都保留了 mechanism family、exponent、typed law、8 个 predictions、
confidence 与 summary，但没有 `selected_action_index`、`selected_action_query_id` 或
`evidence_assessment`。生产 validator 首先在动作索引处终止，因此三条均按冻结规则记为
`participant_schema`，属于参与者方法/输出合同结果，而非基础设施故障。所有未评分的
family、law 与 predictions 只作失败记录保留，不计算 MAE、rank、Top-1 或 regret，也不以
新 session 替换。

| 事件或控制 | class / impact | 证据 | 决策与动作 | 验证 |
|---|---|---|---|---|
| 三条 post action 合同失败 | participant_schema / interface qualification | 3/3 缺少合法 action index | 原样保留，terminal；不 retry、不替换 | production validator 与三份 result 一致 |
| provider transport/runtime | K1 / 无 outage 或 receipt corruption | 6/6 completed、rc=0、0 errors、0 predecessors | 保留 receipts；不作瞬时 infrastructure retry | receipt、result 与 closeout hashes 通过 |
| CLI/provider schema enforcement | A/U / formal 科学证据不可用 | post schema required 两字段，但 3/3 invalid JSON 以 rc=0 返回 | formal 阻断；只能由独立后继 block 重新取得证据 | prompt/schema 重建与独立 JSON Schema 校验 |
| DeepSeek→GPT stop rule | K0 / scientific validity | DeepSeek canary 0/3 | GPT 不启动；formal 保持阻断 | GPT canary 0/3，双方 formal 0/30 |

## 事后接口诊断

生产路径核对排除了“runner 把 pre schema 错传给 post”的解释。W2-57 与 W2-58 的
pre/post prompt hashes 逐臂完全相同；W2-58 从冻结 manifest 重建的 post schema 明确把
`selected_action_index` 和 `evidence_assessment` 列为 required，`codex exec resume` 也收到
对应 post schema。尽管如此，三条 session 都以 return code 0 返回了与 pre 相同的六字段
JSON。独立 Draft 2020-12 校验对每条 payload 都同时检出两个 required-property failures。

[OpenAI 官方 Codex 命令文档](https://learn.chatgpt.com/docs/developer-commands#codex-exec)
说明 `--output-schema` 用于验证预期的最终响应形状；本次 `codex-cli 0.145.0` 连接 DeepSeek
custom provider 的实测行为没有兑现该合同。因此最精确的因果定位是 provider/adapter schema
enforcement 与 participant compliance 交界处的接口资格失败，而不是模型完成科学回答后的
负结果，也不是可瞬时 retry 的 provider outage。机器结果中的直接分类仍原样保留为
`participant_schema`。

收束后只做前瞻性 runner 修复：post prompt 显式声明 first-turn JSON shape 已不足，并逐名
要求两个新增字段；本地 validator 也补齐 `evidence_assessment` 与 `model_summary` 验证。
DeepSeek/GPT 当前协议的 canary 与 formal authorization 均已关闭。这些修改不重算、不修补、
不提升三条历史 canary，也不构成新 participant 实验授权。

## 完整性与资源

- DeepSeek input manifest、3/3 canary result 与 canary closeout 的 canonical hashes 均验证通过；
  GPT input manifest 也验证通过。
- qualification、public truth、roster 与五个 public packet hashes 在两个 provider manifest
  之间仍完全一致。
- 六轮 receipt 合计记录 input `277,250`、cached input `178,048`、output `263,267`、
  reasoning output `256,213` tokens；cache-write input 为 `0`。
- outcome replacement 为 `0`，canary scientific outcomes 未用于改动设计。

## Stop rule 与证据边界

DeepSeek 没有达到预定 `3/3` canary gate，因此按冻结的 DeepSeek→GPT 顺序，GPT canary
保持 `0/3`；DeepSeek 与 GPT formal 均保持 `0/30`。canary-only 授权到此终止，formal
授权从未生效。W2-58 不形成 structural recovery、action selection 或 matched cross-model
科学分母，不能用于模型比较，也不改写 W2-56 的 GPT-only formal 结果或 W2-57 的历史失败。

机器摘要：`work-ii-as-study-b3-runner-derived-status-deepseek-canary-closeout-v0.1.json`。
