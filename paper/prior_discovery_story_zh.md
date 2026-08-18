# Paper 2 作者论证稿：已完成研究与未来计划

## 核心边界

本文只把三类已完成证据放入主文：prospective cohort、有效 matched-evidence 结果和正式
open-action assay。早期 exploratory cohorts、单世界 preliminary parametric study、不完整
prototype、repair trajectory、运行计数以及被排除或替换的原始输出全部放入补充材料。

全文围绕三条问题组织：

1. 先验是否改变搜索和终点？
2. 证据是否选择性修正错误先验，并形成可执行规律？
3. 学到的信息能否支持未见行动？

## 已完成研究

### 1. 先验改变搜索和终点

Prospective cohort 完成 135/135 sessions 和 1,243/1,260 planned experiments。正确的 entity
信息在 partition 中形成持续优势；正确的 structural 信息在 crystallization 中形成明显的
initial head start，但后续探索会缩小差距；在 structural partition 中，aligned 和 misspecified
都优于 opaque，说明结构化搜索引导与模型正确性可以分离。

91.2% 的完成实验采用唯一 recipe，84.4% 的 session 最优点出现在 campaign 后半段。这说明
agent 确实利用了反馈持续搜索，但不能据此推出它已经修正了错误先验。

### 2. 证据、选择性修正与可执行规律

所有 135 个 session 都完成五个 typed checkpoints。预测误差总体下降，但 selective-correction
gate 在 entity、parametric 和 structural 三个 locus 均未通过：$p=0.990$、$0.079$ 和 $1.000$。

有效 matched-evidence 结果将能力链拆成三段：parametric block 在固定反证到达后能排除错误
方向；structural block 的 misspecified-minus-aligned prediction-update contrast 为 +0.0645，
但仅 3/5 worlds 为正，且 0/5 summaries 恢复预注册 power law。因此 evidence acquisition、
数值 belief revision 和 structural-law identification 不是同一个结果。

135 个 final executable laws 全部可执行，但相对 final explicit predictions，better/equal/worse
为 50/1/84。blind incumbent replay 的 better/equal/worse 为 1/119/1，说明可重放已有行动，
不等于获得新的行动优势。

### 3. 未见行动选择

正式 multi-task open-action assay 完成 45/45 scheduled cell records、240/240 truth 和 240/240
exact replay；42 个 cell 可用于 action metrics。只有 11/42 选择真实 Top-1；30/42 为 inadequate
law/wrong action，11/42 为 inadequate law/correct action，1/42 为 adequate law/wrong action，
0/42 同时满足 adequate law 和 correct action。

这个结果是 transfer boundary，而不是 arm-level effect：crystallization 的失败集中，只有 12 个
task--world clusters 保留完整三臂结构。

## 未来计划

- private within-family replication：使用全新 sealed worlds 检验当前能力剖面的稳定性；
- context-reset artifact portability：比较 raw evidence、structured evidence bundle 和 typed law
  在新 target context 中的可迁移性；
- cross-model replication：在冻结同一科学合同后，检验失效位置是否跨 agent-system 稳定。

这些计划都需要独立协议和独立 denominator，不能回写当前主文结果，也不能被写成已经完成的
研究。

## 读者-facing 叙事原则

- 不在正文使用服务名称、运行代号、内部任务矩阵编号或接口级计数；
- 不把 endpoint success、prediction improvement、law execution 和 action transfer 合并为单一
  intelligence score；
- 不把 private replication 或 artifact portability 写成当前研究的结果；
- 所有失败、缺失和未执行内容保留在证据记录和补充材料中，但不替换正式 denominator。
