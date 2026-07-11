# Benchmark 科学有效性工作流

本目录保存 ChemWorld benchmark 的评测协议、紧凑机器摘要和审计结论。它明确区分三件事：

1. 环境可以运行并回放；
2. 方法在某个得分上存在差异；
3. benchmark 足以支持预先声明的科学结论。

前两项不能自动推出第三项。当前 backend 是 candidate，六任务 benchmark 总体状态是 `blocked`。

## 冻结协议与证据

`configs/benchmark/publication_protocol_v0.1.json` 固定了六个候选任务、逐任务主指标、20 个配对
seeds、40 次完整实验、确认性比较、0.05 SESOI、paired bootstrap、符号翻转检验、Holm 校正、
负结果报告和资源账本。该协议及结果保持不可变；后续任务整改必须升级版本。

正式经典矩阵在干净提交 `6c5182c1393f5920b3fd37722328080549ea6168` 上运行：

- 6 tasks × 5 methods × 20 seeds = 600 条 replay-verified 结果；
- 方法为 random、LHS、raw GP-BO、structured GP-BO、structured safe GP-BO；
- 每条运行完成恰好 40 次实验；
- 紧凑摘要为 `reports/publication-classic20-full-summary.json`。

`structured_gp_bo - random` 的结果如下：

| Task | Total effect | Primary effect | 结论 |
| --- | ---: | ---: | --- |
| partition | +0.026 | +0.049 | 正向稳定，primary 略低于 SESOI |
| crystallization | +0.066 | +0.149 | primary 达到 SESOI |
| distillation | +0.064 | +0.120 | primary 达到 SESOI |
| flow | +0.069 | +0.033 | 正向稳定，primary 低于 SESOI |
| electrochemistry | +0.054 | +0.0002 | 复合得分改善，主指标不成立 |
| equilibrium | +0.023 | +0.0026 | 主指标不成立 |

六项 total effect 经 Holm 校正后均显著，4/6 达到 total-score SESOI。主指标只有结晶和蒸馏
达到 SESOI，前四项的 bootstrap 区间方向为正，电化学和平衡跨零或接近零。因此不能用复合得分
替代任务主张。

one-hot 表示相对 raw GP 的主要 total-score 改善集中在电化学（约 +0.026），但 selectivity 主指标
约 -0.003。这说明类别表示影响搜索，却没有修复已声明的电化学能力。正式 600 条结果中的
`mean_risk` 与 safety violations 全为零，structured safe GP 没有可学习风险信号，也不能形成
安全结论。

## 泛化与安全审计

`configs/benchmark/generalization_security_v0.1.json` 声明每个任务两个 world-family 轴，并要求
interpolation、extrapolation、composition 和 observation noise 四种控制。当前结果是：

- 0/12 声明轴具备完整独立控制；
- 1/4 不变性可执行：action key order 已通过；
- 6 tasks × 6 基础 exploit probes = 36 项通过；
- public seeds 100–119 与 salted private seeds 200–219 各产生 240 条 replay-verified 结果；
- 两组 shift 均只有分配、结晶、蒸馏、流动通过 total 与 primary 置信区间为正的门禁；
- 电化学 primary 与平衡 total/primary 未通过。

紧凑摘要为 `reports/publication-generalization-security-summary.json`。salt 原值只存在于运行进程，
报告仅保存 SHA-256。seed/private shift 用于检验整体隐藏世界变化，不能替代轴级 OOD 证据。

## 当前科学判定

- **工程底座**：足以继续严肃实验；合同、回放、运行时 provenance 和失败关闭机制扎实。
- **可信任务子集**：分配、结晶、蒸馏、流动已有一致的主动探索证据，但仍需轴级 OOD 和独立复现。
- **待整改任务**：电化学与平衡的主指标不支持当前能力主张，应在新协议中修复或降为 exploratory。
- **安全评测**：当前风险信号退化，不能评价安全/约束方法。
- **发表状态**：尚缺 RL、真实 LLM、资源公平性、完整不变性、第三方复现、冻结图表与论文。

项目的合理定位是“预算受限、部分可观测的闭环虚拟实验智能”，不是静态化学问答、真实产率预测
或工业级流程模拟。完整任务包、依赖与验收标准统一维护在仓库根目录 `todolist.md`。

## 与近期工作的比较维度

- [ScienceAgentBench (ICLR 2025)](https://openreview.net/forum?id=6z4YKr0GK6)：可执行、可验证的
  科学任务和端到端 agent 评价；
- [SciAgentGym (ICML 2026)](https://openreview.net/forum?id=0Moj0YgFEF)：多步科学工具调用、长程
  退化与可训练轨迹；
- [MADE (ICML 2026)](https://openreview.net/forum?id=nrXxVDYMMF)：预算约束闭环发现、组件可交换
  和搜索空间扩展下的自适应收益；
- [ChemCost (2026)](https://arxiv.org/abs/2605.07251)：冻结评分、无需 LLM judge、阶段失败诊断和
  受控噪声鲁棒性。

ChemWorld 要形成有说服力的差异化，必须同时给出可训练 world-family、冻结 Bench、外部分布
Bridge，以及训练前后迁移收益；仅增加虚拟化学任务数量不足以构成 gym 贡献。
