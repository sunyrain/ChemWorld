# W2-60 DeepSeek 低推理预算 matched-evidence 收口

## 结论

W2-60 形成一个完整科学分母和一个平台缺陷 partial：

- A-S B2 low canary 3/3 通过，formal 15/15、30/30 turns、same-thread 15/15、0 failures；
- A-P low canary 只有进度与 terminal 事件，没有 cell receipts 或 canary summary，formal 0/15；
- B2 三臂 post error 均约 0.007，全部 15 cells 低于 0.02，但 misindexed exact 1.75-law recovery 仍为 0/5；
- primary contrast 从 DeepSeek high 的 +0.0645 反向为 low 的 -0.0405，仅 2/5 worlds 为正，exact one-sided p=0.8125；
- provider-reported reasoning output 从 506,637 降到 400,639 tokens，下降 20.9%。

因此，最稳健的结论是 numerical revision 与 structural identification 分离；不能把
misindexed 相对 aligned 的 update-gain 方向写成跨推理预算稳定效应。`low` 仍会产生大量
provider-reported reasoning tokens，不是 reasoning-off，也不支持推理预算或模型优劣排名。

## B2 完整分母

| Arm | Mean pre error | Mean post error | Mean gain |
|---|---:|---:|---:|
| opaque | 0.2473 | 0.0067 | 0.2406 |
| aligned | 0.2855 | 0.0069 | 0.2787 |
| misindexed | 0.2451 | 0.0069 | 0.2382 |

主对比为 -0.0405，描述区间 [-0.1559, 0.0749]；2/5 worlds 为正、3/5 为负。
misindexed 的 5/5 worlds 都达到 post error <=0.02，0/5 恢复 exact 1.75 law，4/5 使用
saturation/endpoint 型公开总结。一次 receipt tool event 出现在隔离的只读临时 workspace；
没有 participant 物理实验、turn.failed 或 infrastructure predecessor。

## 与 high/GPT 的分层对照

| Configuration | Sessions | Primary contrast | Positive worlds | Low-error misindexed | Exact law |
|---|---:|---:|---:|---:|---:|
| DeepSeek high | 15/15 | +0.0645 | 3/5 | 5/5 | 0/5 |
| GPT medium | 15/15 | +0.0915 | 4/5 | 5/5 | 0/5 |
| DeepSeek low | 15/15 | -0.0405 | 2/5 | 5/5 | 0/5 |

三种配置都支持低误差插值不等于注册结构恢复。只有 DeepSeek high/low 的 token 与 wall-time
变化作同 provider 描述；GPT usage 语义不进入资源优劣比较。

## A-P partial 的处置

A-P 三个 canary cell 均建立线程并产生 terminal-failed 进度事件，但外层前台监督超时后没有
留下正式 cell receipt 或 canary summary。由于无法证明零 provider/scientific exposure，也不能从
进度事件重建 participant payload，该 root 作为 platform-defective partial 原样保留。没有建立 restart
root，没有进入 formal，也不把 B2 成功外推到 A-P。

## 论文与图表边界

Figure 4 同时展示 A-P 的 DeepSeek-high/GPT-medium 对比，以及 B2 的 DeepSeek-high、GPT-medium、
DeepSeek-low 对比。Panel d 只画三种完整 B2 配置；A-P low 明确不展示。正文可以写
“数值--结构断裂对该 reasoning budget 改变稳健”，但不得写 reasoning-off、low 更优、high 更优或
完整 A-P/B2 reasoning ablation。
