# Experiment 1 EC qualification v1.0.1 — development result

日期：2026-09-17。状态：**development qualification 完成；不是正式 benchmark 结果；未授权 Participant。**

## 结论

`EC-W00` canary 通过。`EC-W01..W05 × entity/parametric/structural` 的 15 个原子单元全部完成：

- 11/15 原子单元 `qualified`，4/15 `failed`；
- 815/815 计划执行已尝试，815/815 exact replay；
- 0 platform failures，0 physical failures，0 Participant/provider calls；
- EC-P 为 `five_world_qualified`（5/5）；
- EC-E 为 `failed`（3/5），EC-S 为 `failed`（3/5）；
- EC 整体不得进入 Participant development，正式 benchmark execution 仍未授权。

通过的 World 不抵消失败单元，退出码 1 表示冻结科学 gate 未全过，不表示执行器崩溃。

| World | Entity | Parametric | Structural |
| --- | --- | --- | --- |
| EC-W01 | failed: Q5 | qualified | failed: Q5, Q6 |
| EC-W02 | qualified | qualified | qualified |
| EC-W03 | qualified | qualified | qualified |
| EC-W04 | failed: Q5, Q8 | qualified | failed: Q5, Q6 |
| EC-W05 | qualified | qualified | qualified |

## 失败定位

### EC-E

- `EC-W01`：anchor 1 的实体对绝对 separation 为 `0.032702665 < 0.05`；SNR 为 `3.751043`，因此是效应幅度不足，Q5 失败。
- `EC-W04`：anchor 0 的 separation 为 `0.008601834 < 0.05`，SNR 为 `1.186623 < 2.0`，因此 Q5 与 Q8 同时失败。
- W02、W03、W05 的两个 anchors 均达到冻结 separation 与 SNR 门槛。

### EC-S

- `EC-W01`、`EC-W04` 的 held-out disagreement fraction 均为 `0.222222 < 0.40`，且高电流侧 counterexample support 均为 `0`，所以 Q5/Q6 失败。
- 两个失败 World 仍有强的 high-current efficiency-loss topology signature；失败不是“没有 transport effect”，而是当前 aligned/misspecified 结构模型在公开验证点上的可辨识覆盖与预算内双侧反证不足。
- W02、W03、W05 的 disagreement fraction 均为 `0.444444`，低/高侧 support 均为 `2/2`，通过冻结 gate。

### EC-P

五个 World 全部通过。aligned normalized MAE 范围为 `0.121554–0.152401`（门槛 `<= 0.20`）；
held-out disagreement fraction 均为 `0.858824`（门槛 `>= 0.25`）；blind error margin 范围为
`0.094693–0.445492`（门槛 `>= 0.05`）。605/605 主表面点全部分类并独立重放一致。

## 绑定与复核

- 最新远端基线：`main@52fdf4c0bdccf599b0137f4fef1d0a26ad44d007`；
- qualification 分支：`codex/experiment1-v1.0.1-ec-qualification`；
- 科学 runner commit：`941110ee7c84`；汇总器 commit：`867e0c7312ff`；
- 合同文件 SHA-256：`7f6ebfe6fbee597552ea8f10e3f269f1733197c2ec82bb0cff82b0a14f77588e`；
- canonical contract SHA-256：`69464a4912ee55cb72b9e418b09a498c396337bb568c24bdcc64a3b4d1e7a186`；
- final registry file SHA-256：`f320b54836bd018e7940df98c5e906a755baf940ce5080a7cc7c2f4700df1ff1`；
- final registry self-hash：`ad3b0a7c7f2561375bdd99372f277d0d678014c32d2bdc86fc88b3ea84675b26`；
- final summary file SHA-256：`ccc29884d24e3a3622d05c7f108d5c9b4de7123f35924ba436fb5f0b66b90c06`；
- final summary self-hash：`e5a0939f4f93723af6110de1ea249f2b4257108d982e349c8d6c9e2543090f90`。

服务器证据根目录为：

`runs/development/experiment-1-ec-v1.0.1-941110e/`

其中 `parametric/` 是因旧 ignored raw 依赖在首个数据点前停止并保留的 platform attempt；修复后的完整参数结果位于
`parametric-restart1/`。旧合同/旧 commit 的 W00 与 entity attempts 也保留，未覆盖或冒充最终分母。

## 下一步边界

不能直接启动 O/A/M Participant 实验。下一轮应只针对四个失败原子单元做事前 redesign：

1. EC-E 核对实体 transposition、anchors 与五 World 的可辨识覆盖，不能降低 `0.05`/`SNR 2.0` 门槛；
2. EC-S 调整真实可执行的 misspecified structural family 或 outcome-blind 查询覆盖，使高侧反证在四实验预算内存在，不能把 0.40 门槛降到 0.222；
3. 冻结新的 repair note/manifest 后，从受影响 qualification block 的第一个单位重跑；
4. EC-P 的通过证据保留，但若共同 World、公共合同、噪声或阈值改变，也必须重新资格化。
