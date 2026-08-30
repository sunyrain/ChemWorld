# Work II A-S Study B3 shared-index DeepSeek canary 收束

状态：`terminal_canary_rejected_before_formal`。

DeepSeek `deepseek-v4-flash / high` 的三条 fresh canary sessions 全部发起并各完成两轮
provider turn：总计 `6/6` completed turns、`3` provider attempts、`0` retries、`0` tools、
`0` infrastructure failures、`0` participant physical experiments。aligned 与 misindexed 两条
session 完整通过；opaque 的 post payload 被完整保留，其中 `selected_action_index=3` 合法，
但冗余 `status` 仍为 `pre_submission_complete`，因此按冻结 explicit-status contract 记为
participant-schema failure。

最终 canary 分母为 `2/3 completed + 1/3 failed`，不补跑、不替换，也不把两条完成 session
当作科学分母。按预定 DeepSeek 后 GPT 的顺序 stop rule，GPT canary `0/3`，DeepSeek 与 GPT
formal 均 `0/30`。该结果证明整数 action encoding 消除了旧 canary 的非法 query-ID 问题，
但 DeepSeek 仍会在冗余 stage-status 字段上发生序列化漂移；它不支持跨模型 formal 比较。

机器摘要：`work-ii-as-study-b3-shared-index-deepseek-canary-closeout-v0.1.json`。
