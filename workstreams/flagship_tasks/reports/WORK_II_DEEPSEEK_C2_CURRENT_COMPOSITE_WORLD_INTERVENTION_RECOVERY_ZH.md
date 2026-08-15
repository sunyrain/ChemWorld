# Work II current-composite world-intervention recovery

## 结论先行

v0.1 evaluator 虽把 `world_interventions` 绑定进 plan，却没有传入 runtime execution 与 exact replay，导致 A-S partition/crystallization truth 和 blind 实际按 baseline world 执行。v0.2 从第一单元重跑全部 420 truth、675 checkpoint scores、135 laws 和 726 eligible blind replays，保留 84 个未启动 blind 分母。

恢复后 C2 决策仍为 **False**；A-E 与 A-P 的 prediction/law/blind blocks 均与旧报告完全一致。A-S 数值发生实质变化，因此 v0.1 只保留为历史缺陷证据，当前论文只能引用 v0.2。

## 1. 完整分母

- 45 clusters、135 cells；participant 终态 121 completed、7 failed、7 right-censored。
- truth 420/420；checkpoint 675/675；law 135/135；blind 726/726 launched，84 unstarted。
- evaluator provider calls：0；participant trajectory、query roster、统计 gate、删失规则均未改变。

## 2. A-S 分任务变化

| Task | Arm | prediction gain old→new | law MAE old→new | law−final old→new | blind gain old→new |
|---|---|---:|---:|---:|---:|
| partition-discovery | opaque | 0.0798→0.0798 | 0.2461→0.2461 | 0.0292→0.0293 | 0.0000→0.0000 |
| partition-discovery | aligned_nominal | 0.2408→0.2408 | 0.1643→0.1643 | 0.0644→0.0644 | 0.0000→0.0000 |
| partition-discovery | misindexed_nominal | 0.1116→0.1116 | 0.1715→0.1715 | 0.0573→0.0573 | 0.0000→0.0000 |

该 task 的 observed primary contrast 为 -0.1292→-0.1293，正方向 worlds 2/5→2/5；failure-aware lower-bound mean 为 -0.1292→-0.1293。

| reaction-to-crystallization | opaque | 0.2332→0.3590 | 0.1229→0.0713 | -0.0042→0.0033 | -0.0250→-0.0296 |
| reaction-to-crystallization | aligned_nominal | 0.1434→0.2144 | 0.2291→0.1823 | -0.0066→-0.0513 | 0.0000→0.0000 |
| reaction-to-crystallization | misindexed_nominal | 0.1863→0.3304 | 0.1769→0.0957 | 0.0013→-0.0025 | 0.0000→0.0000 |

该 task 的 observed primary contrast 为 0.0429→0.1161，正方向 worlds 3/5→5/5；failure-aware lower-bound mean 为 -0.3842→-0.3189。

## 3. A-S 与 overall 收束

- A-S failure-aware locus estimate：-0.2567→-0.2241；observed-point estimate：-0.0432→-0.0066。两个 gate 仍不通过。
- A-S law MAE：0.1851→0.1552；pre→law improvement：0.1423→0.2059。
- A-S blind mean gain：-0.0037→-0.0044；better/equal/worse 保持 0/26/1。
- Overall law MAE：0.2438→0.2371；law better/equal/worse：49/1/85→50/1/84。
- Overall blind mean gain：-0.0008→-0.0010；better/equal/worse 仍为 1/119/1。

## 4. 当前证据处置

- `work-ii-deepseek-c2-current-composite-evaluation-v0.2.json` 是当前 evaluator 机器结果。
- v0.1 report/root 不删除、不覆盖，作为缺陷发现与 recovery 的历史记录。
- 原 Study B A-S packet 派生自 v0.1 A-S truth，因此该分支退出当前科学结论；A-P 不受影响。当前 A-S matched-evidence 结论由独立 B2 phase-process block 提供。
- 该恢复不产生新的 participant trajectory，也不改变 participant endpoint 结果；它只纠正 evaluator 真值、law scoring 与 blind replay。
