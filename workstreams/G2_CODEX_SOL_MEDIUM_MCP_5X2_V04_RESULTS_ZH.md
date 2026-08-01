# G2 原生 Codex 逐操作 5×2 v0.4 开发结果

更新日期：2026-08-01

## 结论

G2 已经从“参数选择世界”进入可完整运行的自主逐操作实验世界。新矩阵使用原生 OpenAI Codex CLI，模型为 `gpt-5.6-sol`，reasoning effort 为 `medium`，通过 host-owned STDIO MCP 让 agent 独立完成加料、设定、电解、中间表征、终点检测和跨容器适应。

v0.4 的 5 个物理世界 × 2 个材料信息条件共 10 个 cell 全部完成：

- 60/60 个新鲜容器均以 final assay 关闭；
- 815 个 agent 自主提交的原子操作，0 个无效或资源拒绝动作；
- 164 次非终点仪器表征，另有 60 次 final assay，共 224 个 `measure` 操作；
- 60/60 个 Codex provider session 完整；
- 10/10 资源账本、10/10 exact replay 和 5/5 物理世界配对审计通过；
- 38,526,170 input tokens，179,062 output tokens。

本轮不支持将故事收缩为“提供材料先验会使优化更强”。更准确的开发性结论是：

> 材料信息改变了 agent 如何发现、修改、丢失和重新找回高分策略；这种影响随物理世界和评价时标而改变，不能被一个最终 best score 表示。

## 协议与审计边界

| 项目 | 冻结值 |
|---|---|
| protocol | `g2-electrochemical-autonomous-material-information-5x2-v0.4` |
| world seeds | 0, 1, 2, 3, 4 |
| arms | `opaque_codes`, `anonymous_nominal_properties` |
| model | `gpt-5.6-sol` |
| reasoning | `medium` |
| transport | `host_owned_stdio_mcp` |
| vessel starts / final assay opportunities | 6 / 6 per cell |
| non-final instrument quota | 18 per cell |
| campaign stock | 0.48 mol reagent, 0.96 L solvent |
| primitive-operation ceiling | 144 per cell |
| automatic repair / closeout | false / false |
| audit status | `completed_audited_descriptive_matrix` |
| audit schema | `chemworld-autonomous-material-campaign-audit-0.3` |
| audit SHA-256 | `bc7495315745272c95fb326b7b50fb509081ad70323354899a233abac6c7b4a9` |

本矩阵是 n=5 paired worlds、每个 arm/world 只有一条随机 Codex 轨迹的开发性实验。它用于检查任务、资源、接口、估计量和可观察行为，不是总体水平的确证性先验效应试验。

本地权威证据位于：

- `runs/development/g2-autonomous-electrochemical-material-5x2-codex-sol-medium-mcp-v2/matrix_manifest.json`
- `runs/development/g2-autonomous-electrochemical-material-5x2-codex-sol-medium-mcp-v2/autonomous_material_campaign_audit.json`
- `runs/development/g2-autonomous-electrochemical-material-5x2-codex-sol-medium-mcp-v2/autonomous_material_campaign_audit.md`

`runs/` 不进入 Git；本文档保留可推送的紧凑结果与审计哈希。

## 逐 cell 结果

| seed | arm | operations | measurements | six final scores | best | mean |
|---:|---|---:|---:|---|---:|---:|
| 0 | opaque | 69 | 17 | .5307, .0000, .4388, .6034, .4858, .5987 | .6034 | .4429 |
| 0 | nominal | 52 | 6 | .2214, .3393, .4136, .5083, .5697, .6193 | .6193 | .4453 |
| 1 | opaque | 99 | 18 | .7432, .6817, .7091, .7170, .7123, .6508 | .7432 | .7023 |
| 1 | nominal | 75 | 17 | .4502, .5173, .5076, .5424, .4705, .4933 | .5424 | .4969 |
| 2 | opaque | 101 | 18 | .7865, .5827, .4010, .5949, .3961, .3824 | .7865 | .5240 |
| 2 | nominal | 98 | 18 | .2492, .7427, .6346, .7624, .8544, .8352 | .8544 | .6797 |
| 3 | opaque | 71 | 18 | .3388, .3254, .3931, .3624, .4067, .4191 | .4191 | .3743 |
| 3 | nominal | 100 | 18 | .3009, .4745, .4245, .7408, .6086, .6042 | .7408 | .5256 |
| 4 | opaque | 73 | 18 | .6050, .5900, .4329, .6028, .3817, .0000 | .6050 | .4354 |
| 4 | nominal | 77 | 16 | .6823, .6205, .5756, .5411, .6945, .7894 | .7894 | .6506 |

## 不同估计量给出不同答案

arm 汇总：

| arm | completion | mean ops | mean measurements | mean best | batch AUC | realized attempt AUC | fixed-144 attempt AUC |
|---|---:|---:|---:|---:|---:|---:|---:|
| opaque | 1.000 | 82.6 | 17.8 | .6314 | .6167 | .5204 | .5632 |
| nominal | 1.000 | 80.4 | 15.0 | .7093 | .5892 | .5014 | .5908 |

每个世界的 nominal - opaque 差：

| seed | Δbest | Δmean final | Δbatch AUC | Δattempt AUC | Δfixed-144 AUC | Δops |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | +.0159 | +.0024 | -.1218 | -.1379 | -.0288 | -17 |
| 1 | -.2009 | -.2055 | -.2246 | -.1115 | -.1280 | -24 |
| 2 | +.0678 | +.1558 | -.0856 | -.0265 | +.0073 | -3 |
| 3 | +.3217 | +.1514 | +.1971 | +.1479 | +.1854 | +29 |
| 4 | +.1844 | +.2152 | +.0972 | +.0330 | +.1021 | +4 |
| mean | +.0778 | +.0638 | -.0275 | -.0190 | +.0276 | -2.2 |

关键点是：

1. nominal 在 4/5 个世界有更高 best，平均 `Δbest=+.0778`，但范围从 `-.2009` 到 `+.3217`。
2. 如果问“六批中多早找到高分”，batch AUC 平均反而是 `-.0275`。
3. 如果按 agent 实际使用的操作步数求 AUC，平均是 `-.0190`。
4. 如果将终端 incumbent 补齐到共同 144 步上限，平均又变成 `+.0276`。

因此“先验是否有用”不是一个单标量问题。最终高分、早期发现、实际操作效率和固定资源价值是不同 estimand。

## 轨迹结构比单一排名更有信息

当前最有信息量的不是 arm 均值，而是具体探索轨迹：

- seed 0 opaque 首批即为 `.5307`，但第二批为 0；nominal 则从 `.2214` 连续改进到 `.6193`。两者 best 和 mean 几乎相同，学习形状完全不同。
- seed 2 opaque 首批即发现 `.7865`，但之后始终无法保留，末批只有 `.3824`。这是“发现了好解，但没有学会保留好解”。
- seed 2 nominal 从 `.2492` 经过 `.7427, .6346, .7624, .8544` 到 `.8352`，展示了非单调但可保留的纠偏。
- seed 3 nominal 的第三批用了长操作路径却只得 `.4245`，第四批类似长路径却跃升到 `.7408`。更多操作不是充分条件，证据如何被转化为控制才是问题。
- seed 4 opaque 首批 `.6050`，最后一批在长探索后归零；nominal 经历三批回落后重新恢复并以 `.7894` 结束。

这些轨迹支持将后续故事集中在“探索的结构”，而不是 LLM 与 BO 的输赢。

## 发现—保留—恢复的可审计结果

audit v0.3 将上述观察冻结为在线可计算指标：

- **最佳发现进度**：全局最佳首次出现位置映射到 0—1，0 为首批、1 为末批；
- **在线保留率**：后续 final score 达到此前 incumbent 的 90% 即视为保留；
- **loss/recovery**：跌破阈值时冻结此前 incumbent，首次重新达到同一阈值视为恢复；终局未恢复的恢复时延按右删失记录；
- **最大回撤**：final score 相对此前 incumbent 的最大绝对跌幅；
- **终点/最佳**：末批分数与轨迹内全局最佳之比；
- **诊断改控转化**：含至少一次“诊断后、可比较控制字段改变”的 batch 中，final score 高于上一 batch 的比例。分析单位是 batch，不重复计算同一 batch 内的多个诊断事件。

两臂开发性汇总：

| arm | 平均最佳发现进度 | 平均在线保留率 | 平均最大回撤 | 平均终点/最佳 | loss：恢复/未恢复 | 诊断改控后正增量 |
|---|---:|---:|---:|---:|---:|---:|
| opaque | 32% | 52% | .3326 | 67% | 6：3/3 | 4/14（29%） |
| nominal | 80% | 72% | .0915 | 94% | 5：4/1 | 8/17（47%） |

每个配对世界的 nominal - opaque 轨迹差：

| seed | Δ最佳发现进度 | Δ在线保留率 | Δ最大回撤 | Δ终点/最佳 |
|---:|---:|---:|---:|---:|
| 0 | +40 pp | +60 pp | -.5307 | +.008 |
| 1 | +60 pp | 0 pp | -.0206 | +.034 |
| 2 | +80 pp | +80 pp | -.2961 | +.491 |
| 3 | -40 pp | -60 pp | +.1059 | -.184 |
| 4 | +100 pp | +20 pp | -.4638 | +1.000 |
| mean | +48 pp | +20 pp | -.2410 | +.270 |

这给出了一个比“先验是否提高分数”更深的候选结构：在当前五个世界中，nominal 并没有更早找到其最终最佳，反而平均更晚；但它通常更能保留已获得的性能，并以更接近自身最佳的状态结束。换言之，**发现速度、在线保留和终局优化可以解耦**。

这个模式仍然不能被写成总体因果结论。seed 3 对保留率、回撤和终点/最佳均反向；诊断改控后的正增量也只是时间对齐描述，既受策略选择影响，也受世界难度和回归均值影响。它的价值是把下一轮复现实验的待检验机制变得明确，而不是提前证明机制。

## v0.3 为何作废，v0.4 为何可用

v0.3 中 seed 3 nominal 在第 84 步提交符合公开 schema 的 `discard_batch(reason=...)`，资源 preflight 也允许。环境却在“先扣最后一步，再检查 discard 是否可用”时错误地判定操作不可用。这是边界实现 bug，不能被解释为 agent 资源治理失败。

v0.4 修复了最后一步 discard 的 preflight/validation 顺序边界，并将原子操作上限从 84 提高到 144。物理资源仍然由六个容器、全局原料库、18 次非终点仪器和 6 次 final assay 机会控制。

新矩阵中有 4 个 cell 自然使用了超过 84 步：99、101、98 和 100 步。如果仍用 v0.3，它们都会被设计性删失。v0.4 中最大只用到 101/144，且 10 个 cell 全部完成，证明原子步数已基本恢复为非绑定安全护栏。

## 对旧开发观察的修正

v0.3 曾暗示 nominal 先验会收缩材料空间探索，同时将探索重分配到过程控制。v0.4 中：

- 材料首选策略多样性的平均差只有 `-0.2`，范围 `-2` 到 `+2`；
- 诊断后控制改变的平均差为 `-0.8`，范围 `-11` 到 `+5`；
- setpoint 跨批改变的平均差为 `-0.4`，范围 `-5` 到 `+5`。

因此该“空间重分配”在当前不是可重复的总体结论，不应进入 arXiv 摘要或主结论。它可以作为后续多轨迹复现要检验的候选机制。

## 下一阶段 roadmap

1. 将 v0.4 保持为 arXiv 阶段的开发性自主环境实例，不将 n=5 的 arm 均值包装为确证效应。
2. 冻结四类不可互换的主要估计量：生命周期完成、batch AUC、realized attempt AUC 和 fixed-budget AUC；best/mean final 作结果端点。
3. **已完成**“发现—保留—恢复”指标审计：最佳首次发现、在线/最佳后保留、回撤、恢复时延、终局未恢复，以及诊断改控到 final score 的 batch 级时间对齐。
4. 下一实验优先对效应相反的 seed 1 和 seed 3 做多条独立 Codex 轨迹，并在运行前冻结上述指标，分离世界交互与单次模型随机性。
5. 经典算法仍只作接口、资源和基本难度校验，不将“LLM 比 BO 强”作为主故事。
6. 新轨迹必须同时报告 endpoint、四类预算估计量和轨迹学习指标；不能只挑选支持某种先验叙事的单一数字。

## 验证状态

- v0.4 配对环境 dry run：5/5 pair audits 通过。
- seed 3 nominal K6 针对性 qualification：59 步，6/6 final assay，0 invalid，provider/replay 通过。
- v0.4 完整矩阵：10/10 cells 和全部严格审计通过。
- G2 相关回归：113 passed，1 个与本轮 G2 无关的既有默认 episode 断言明确 deselected。
- 另有 1 个与本轮 G2 无关的既有 `reaction-optimization-standard` 默认 episode 断言失败，本轮不将它重新解释为 G2 失败。
