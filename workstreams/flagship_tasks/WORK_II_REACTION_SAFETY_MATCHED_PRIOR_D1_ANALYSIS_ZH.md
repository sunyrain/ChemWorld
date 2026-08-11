# Work II reaction-safety matched-prior D1 阶段分析

日期：2026-08-11  
性质：单个 development world 的描述性证据；不是 R5、跨 world 推断或模型排名。

## 1. 这次实验完成了什么

- participant：`3/3` persistent Codex sessions、`30/30` 完整实验、`210/210` committed
  operations、`15/15` belief checkpoints；三臂各有 8 个 unique recipes 和 2 个 exact repeats。
- evaluator：`16/16` held-out truth queries 与 `18/18` blind replays 全部完成并 exact replay；
  evaluator provider calls 为 0，participant trajectories rerun 为 0。
- 运行可靠性：0 resource rejections、0 provider errors、0 platform failures；misspecified arm
  有 1 次 recovered MCP failure，最大连续次数为 1。
- participant safety outcomes：opaque 有 5 个 experiment 出现公开 unsafe heat outcome，aligned
  和 misspecified 各 1 个；没有任何操作触发动态 constitution rollback。因此这里的 unsafe
  outcome 是模型选择产生的科学/安全行为，不是平台故障。

## 2. 主要结果

| Arm | Held-out MAE: pre -> final | 最佳 endpoint | prior reliability | final direction | executable-law MAE |
|---|---:|---:|---:|---|---:|
| opaque | `0.1088 -> 0.0589` | `0.4192` | NA | higher，错误 | `0.0589` |
| aligned | `0.1052 -> 0.1107` | `0.4182` | `0.70 -> 0.45` | higher，错误 | `0.3036` |
| misspecified | `0.1785 -> 0.1361` | `0.4163` | `0.70 -> 0.20` | higher，仍错误 | `0.0639` |

真实 held-out surface 在五组可配对 duration 上平均偏好 lower-temperature side，
`lower - higher score = +0.0168`。三臂最终显式预测均未恢复这一方向。

完整 checkpoint 轨迹为：

- opaque：`0.1088 -> 0.0553 -> 0.0526 -> 0.0498 -> 0.0589`；
- aligned：`0.1052 -> 0.0640 -> 0.0732 -> 0.1135 -> 0.1107`；
- misspecified：`0.1785 -> 0.1148 -> 0.1094 -> 0.1518 -> 0.1361`。

这说明学习不是单调过程。opaque 在实验 7 后最好、final 略回退；aligned 在最初两次实验后
短暂改善，随后发生明显 harmful updating；misspecified 先改善、后退、最终部分恢复。

## 3. 能够支持的结论

1. **错误先验可以被发现并显著降权。** misspecified arm 从第二次实验开始持续把
   `reaction_temperature_K` 标为冲突字段，可靠度最终降至 `0.20`。这不是一次偶然自报，而是跨四个
   post-evidence checkpoints 的稳定诊断。
2. **冲突检测不等于规律恢复。** misspecified held-out error 改善 `0.0424`，但最终仍预测错误方向；
   executable law 只输出常数面，无法表达其显式预测中声称的 nonlinear optimum。
3. **正确先验也可能被有限、自选证据带偏。** aligned arm 的 pre-evidence 方向正确，但 final direction
   反转，final prediction error 略恶化，law error 大幅升高且与 final explicit predictions 的一致性误差为
   `0.3881`。这支持研究 evidence selection bias 和 harmful belief update，而不是只研究错误先验纠正。
4. **endpoint 与科学理解明显分离。** 三臂 best scores 仅相差 `0.0029`，但预测误差、方向、law fidelity
   和安全探索差异很大。只看最佳配方会掩盖这次实验最重要的能力断裂。
5. **先验可能改变安全探索。** opaque 产生 5 个公开 unsafe experiments，而两个 supplied-prior arms
   各 1 个。这在单 world 中只能作为描述性信号，但值得在 D2 检查是否可重复。

## 4. 不能支持的结论

- 不能声称 agent 已经恢复真实温度规律或成功摒弃错误先验；
- 不能声称 aligned prior 稳定有益；当前 world 中它反而发生 harmful update；
- 不能把 self-reported reliability、suspected field 或正的 H3 单独当作纠错成功；
- 不能用三臂近似相同的 endpoint 推断其世界模型同样准确；
- 不能把 blind recommendation gap 归因于模型行动能力。

## 5. action-layer 索引混淆

D1 运行时，participant-visible completed history 暴露的是 0-based index，而提交工具按 1-based index
校验。三臂 rationale 中的 score 都唯一对应实际 incumbent，但提交 index 均小 1：opaque `9->10`、
aligned `4->5`、misspecified `6->7`。

处理原则：

- 原始提交永久保留，不自动 `+1`，不替换 participant output；
- blind evaluator 继续 replay 实际提交 index；
- rationale-matched index 只作为平台诊断；
- experiment selection、observations、belief snapshots 和 law summaries 仍是有效科学轨迹；
- D2 起 participant 所见 current experiment、completed history、next index 与 commit schema 全部统一为
  1-based，并由回归测试覆盖。

## 6. D2 的价值与边界

D2 不是因为 D1 结果“好看”而追加。它已由 participant 前冻结的跨 world heterogeneity trigger 授权，
worlds 固定为 1 和 4。D2 需要回答三个具体问题：

1. misspecified arm 的“稳定降权但方向未恢复”是否跨 world 重现；
2. aligned arm 的 harmful update 是 world-0 偶然现象，还是自选证据下的系统性风险；
3. supplied prior 减少 unsafe exploration 的描述性信号是否能在相反温度方向 world 与典型 world 中复现。

D2 不改 prior 文本、实验数、checkpoint、resource ceiling 或 pass/failure rules。完成后提交用户审核；
未经审核不进入 R5。

机器报告：
`workstreams/flagship_tasks/reports/work-ii-reaction-safety-matched-prior-d1-evaluation-20260811.json`。
报告 SHA-256：`b6417882a1286a3e6f3b79f705af3386f4e7fca0dbf0556bedbd5336d41ef31b`。
