# Work II A-S Study B3 GPT-5.6-sol medium 正式实验收束

状态：`formal_completed`。三臂 canary `3/3` 通过后，冻结的 formal matrix `30/30` cells 全部完成，失败 `0`；5 worlds × 3 arms × 2 independent sessions 的科学分母完整，canary 不进入 formal 分母。

## 科学结果

| arm | n | pre MAE | post MAE | family B | family+exponent recovery | Top-1 | mean rank | mean regret | eligible gain≥0.02 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| opaque | 10 | 0.2857 | 0.0367 | 5/10 | 0/10 | 0/10 | 6.20 | 0.7760 | 0/6 |
| aligned_nominal | 10 | 0.2084 | 0.0215 | 5/10 | 5/10 | 2/10 | 5.10 | 0.6524 | 0/6 |
| misindexed_nominal | 10 | 0.2963 | 0.0378 | 8/10 | 0/10 | 0/10 | 6.80 | 0.8499 | 0/6 |

所有 arm 的平均未见查询误差都明显下降；formal post MAE 分别为 `0.0367`、`0.0215`、`0.0378`。因此直接证据稳定支持数值插值。

结构层面没有出现普遍恢复。aligned arm 在 `5/10` sessions 同时保留 FAMILY_B_POWER 与 1.75±0.10；opaque 和 misindexed 均为 `0/10`。aligned 的 world-mean exponent error 对 opaque 和 misindexed 都在 `5/5`、`5/5` worlds 更低。值得注意的是 misindexed 有 `8/10` 选择了 power family，却有 `0/10` 恢复正确指数：family 标签本身不能视为结构识别。该结果支持“正确先验的部分保留”，不支持证据诱导的选择性错误先验修正。

证据到行动的桥接同样没有建立。全 30 cells 只有 `2/30` Top-1，且两次都来自 action-opportunity 不成立的同一 world；在预先冻结的 `18` 个 eligible cells 中，达到 gain≥0.02 的为 `0/18`。即使在 eligible 且结构恢复的 `2` 个 cells 中，也没有一个达到 0.02 action gain。

## 执行与资源审计

| phase | sessions | attempts | completed turns | same-thread | tools | physical experiments | wall time |
|---|---:|---:|---:|---:|---:|---:|---:|
| canary | 3 | 3 | 6/6 | 3/3 | 0 | 0 | 151.7 s |
| formal | 30 | 30 | 60/60 | 30/30 | 0 | 0 | 1436.8 s |

总计 33 provider session attempts、66/66 completed turn receipts、0 retries、0 tool events、0 physical experiments。formal 最后一个 opaque post turn 记录过 `1` 个 transient provider error event，但同一 turn 最终返回 completed receipt，cell 状态仍为 completed；该事件完整保留，既不误记为 formal failure，也不忽略。

总 usage：input `1522286`（其中 cached `297216`，uncached `1225070`），output `225874`，reasoning output `171977`。

## 结论边界

这是与 DeepSeek B3 provider-free science surface 逐字段匹配的 OpenAI GPT-5.6-sol medium 结果，但 DeepSeek block 没有形成 formal 科学分母，因此不能做 cross-provider leaderboard。可进入论文的是 GPT block 内部的冻结三臂结果：数值收敛、正确先验的部分结构保留、错误先验未被选择性修正，以及结构理解到新动作的非单调映射。
