# Work II W2-59 双模型主证据补齐收束

状态：`terminal_with_block_specific_cross_model_coverage`。全部预定主证据块均按冻结协议启动或接受 stop-rule 判定；只有 A-P 与 A-S B2 形成 DeepSeek + GPT 的完整 matched formal 分母。C2、W2-50 与 B3 的不完整性是保留的 canary 终态，不是待补跑队列。

## 总分母

| 项目 | 计划 | 终态观察 | 合格/可评分 | 保留失败 | 未启动 |
|---|---:|---:|---:|---:|---:|
| formal sessions | 270 | 36 | 34 | 2 | 234 |
| 排除式 canary sessions | 12 | 12 | 11 | 1 | 0 |
| participant complete physical experiments | 1,800 | 53 | 40 | 13 | 1,747 |

## 完整 matched cross-model 结果

主指标均为 `misindexed update gain − aligned update gain`，统计单位为同一个 fresh world。跨模型差值只作配对描述，不作模型排行榜。

| Block | 模型 | sessions | primary contrast | positive worlds | exact one-sided p | 结构恢复 |
|---|---|---:|---:|---:|---:|---:|
| A-P | deepseek | 15/15 | 0.0309 | 3/5 | 0.125 | — |
| A-P | gpt | 15/15 | 0.0602 | 5/5 | 0.031 | — |
| A-S B2 | deepseek | 15/15 | 0.0645 | 3/5 | 0.125 | 0/5 |
| A-S B2 | gpt | 15/15 | 0.0915 | 4/5 | 0.062 | 0/5 |

A-P 在 DeepSeek 上为 0.0309（3/5 worlds），在 GPT 上为 0.0602（5/5 worlds）。两个配置都支持反证到达后的数值纠错；GPT 的 5/5 方向一致增强了跨配置复现，但 n=5 仍不支持一般 LLM 结论。

A-S B2 在 DeepSeek/GPT 上分别为 0.0645 与 0.0915；两者的 misindexed exact 1.75-law recovery 都是 0/5。因而“数值收敛不等于结构识别”现在由两个模型配置在完全匹配的 15-session 分母上共同支持。

## 被 stop rule 收束的块

| Block | DeepSeek | GPT | 结论 |
|---|---|---|---|
| Public C2 | 135 cells 完整 evaluator | 3/135 terminal、2 合格、1 provider/session qualification failure、132 未启动 | 无 matched effect；DeepSeek 主结果保留 |
| W2-50 | 45 scheduled、42 eligible、11/42 Top-1 | 3/45 terminal、2 eligible、1 session interruption、42 未启动 | 无 matched action effect |
| B3 successor | excluded canary 2/3 | 修复平台零调用缺陷后 canary 3/3 | 共同门要求双方通过，故 formal 均 0/30 |

GPT C2 三个 sessions 均完成 8/8 physical experiments；aligned session 因 provider/session 错误触发资格失败。GPT W2-50 的 opaque 与 aligned 各完成 12/12，misindexed 在 5/12 后中断。两者都不是零行动基础设施失败，因此不能按冻结规则补跑或替换。

## W2-55 零 provider 重算

DeepSeek 的原 W2-55 仍完整。GPT 新输出经过同一分母可用性检查后，W2-50 只有 2 个 eligible cells，C2 只有 3 个 terminal cells且没有 135-cell current-composite dataset；连续 law-action 相关和 typed-law capacity 因此均为 `not_estimable_after_frozen_canary_stop`。本次新增 provider calls=0，也没有将 DeepSeek 结果拼入 GPT 分母。

## 事件处置

| 事件 | 分类 | 决策 |
|---|---|---|
| GPT C2 aligned in-denominator canary cell | S | terminal_scientific_or_participant_outcome：stop remaining 132 sessions; preserve all raw evidence |
| GPT W2-50 misindexed in-denominator canary cell | B_with_frozen_retention_rule | terminal_operational_outcome：stop remaining 42 sessions; do not replace partial trajectory |
| DeepSeek B3 excluded canary | S | terminal_canary_rejected_before_formal：leave both providers at 0/30 formal |
| GPT B3 first canary root | A_zero_action_platform_defect | full_canary_restart：preserve first root; restart from first canary unit after platform repair |

## 论文边界

可以升级的表述是：A-P evidence acquisition/numerical correction 与 A-S numerical revision/structural identification 的断裂已在两个匹配模型配置上复现。不能升级的表述是：C2、W2-50 或 B3 已有完整双模型 formal 分母，或某个模型总体优于另一个模型。

Launch decision：`terminal_outcome`。W2-59 不再有可合法继续的 provider session；下一步仅是论文、图表和发布整合。
