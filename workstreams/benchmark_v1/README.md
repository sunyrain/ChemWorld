# Benchmark v1 科学有效性收束

本工作流把“代码和发布管线可以运行”与“benchmark 足以支持论文结论”分开验收。当前正式
readiness 只证明 6 个任务在 5 个冻结 seeds 上可执行、可重放且存在一定策略差异；它不能替代
统计功效、跨分布稳定性、真实方法覆盖、私评、反作弊和完整证据链。

## 审计口径

当前工作流只保留可重放的任务级证据：paired-seed 效应、预算曲线、类别表示对照和 provenance。
任何经验有效性 blocker 未关闭时只能称为 candidate，不能发布最终 benchmark 或论文结论。

## 已冻结的发表候选协议

`configs/benchmark/publication_protocol_v0.1.json` 已固定研究问题、六任务边界、逐任务主指标、
不可声称内容、20 个配对 seeds、40 次完整实验、确认性比较、SESOI、bootstrap、符号翻转检验、
Holm 校正和资源账本。`scripts/audit_publication_protocol.py` 会核对当前 World Law、任务合同哈希
和 agent registry；任何漂移均失败。该协议有效只代表预注册完整，不代表经验结果已经通过。

确认性实验使用 `structured_gp_bo` 对 `random`。LHS、原始编码 GP 和结构化安全 GP 是预声明的
次要比较/消融。stub 与 replay agent 已从科学 baseline 中排除。正式运行必须来自干净 commit，
每条轨迹回放通过，并完成恰好 40 次实验；结果仍需通过泛化、反作弊和独立复现门禁后才能进入
论文主张。

## 2026-07-11 正式经典方法矩阵

正式矩阵在干净提交 `6c5182c1393f5920b3fd37722328080549ea6168` 上完成：6 tasks × 5 methods ×
20 paired seeds，共 600 条 replay-verified 结果，每条 40 次完整实验。紧凑、失败关闭的机器摘要为
`reports/publication-classic20-full-summary.json`；它绑定协议哈希、结果摘要和原始 validity report
摘要，原始大轨迹不纳入 Git。

`structured_gp_bo - random` 的 total-score 配对效应在分配、结晶、蒸馏、连续流、电化学和平衡
任务分别为 +0.026、+0.066、+0.064、+0.069、+0.054、+0.023；六项 Holm 校正后均显著，
其中 4/6 达到 0.05 SESOI。任务主指标效应分别为 +0.049、+0.149、+0.120、+0.033、
+0.0002、+0.0026；只有结晶和蒸馏达到预注册 SESOI，前四项的 bootstrap 区间方向为正，
电化学和平衡不支持任务主指标改善。因此 suite 继续为 `blocked`，不能仅凭 total score 升级。

五方法对照进一步表明：LHS 大多接近 random，GP 系列在结晶、蒸馏和流动任务产生明确收益；
one-hot 相对原始 GP 的主要 total-score 改善集中在电化学（约 +0.026），但电化学 selectivity
主指标反而约 -0.003，说明表示修复改善的是复合奖励而非已声明的选择性能力。结构化安全 GP
也尚不能作为安全结论：600 条结果的 `mean_risk` 与 safety violations 全为零，其风险模型没有
可学习信号。下一门禁必须修复主指标对齐和安全信息量，而不是继续增加方法名称。

## 2026-07-11 validity/power 先导审计

早期 10-seed、最小预算和 acquisition-family 中间报告已经由长程预算曲线取代并删除。当前保留：

- `reports/campaign-budget-curve-pilot5.json`：4/8/12/20/40 完整实验的在线前缀曲线；
- `reports/validity-power-electro-structured40-pilot5.json`：电化学类别表示受控对照。

已确认：旧 response-surface maximum 不是 oracle；正式比较必须使用 paired seed；以 0.05
total-score 为 SESOI 时，当前方差支持先采用 20 seeds 作为正式实验起点。原任务预算只容纳
3–7 次完整实验，低于 `max(8, dimension + 2)`；修复 budget override 传递后，校准预算可提供
4–8 次 acquisition，但 EI/PI/UCB/RF-EI 仍没有任何任务达到 +0.05 的自适应收益。当前 blocker
因此是任务/搜索表示与自适应策略的联合分辨率，不是单纯 seed 数或 acquisition 名称。

正式 20-seed 矩阵已经证明可信、非特权的自适应策略在部分任务上形成可重复实际收益；当前新的
阻塞项是六任务主指标一致性、安全风险信号、泛化、反作弊和独立复现，故仍不得升级 readiness。

追加的 40-complete-experiment、5-seed paired diagnostic 显示，GP 相对 random 的 total-score
效应在平衡、流动、结晶、蒸馏、分配任务分别达到约 +0.045、+0.048、+0.049、+0.040、
+0.022，电化学为 -0.076。4/8/12/20/40 实验前缀曲线进一步显示流动与蒸馏在 20 个实验前
仍可能为负，到 40 个实验才转正。因此先前 `dimension + 2` 只能作为管线最低容量，不能作为
正式学习预算；后续应分别整改电化学表示，并以任务级预算曲线冻结协议。

电化学受控表示探针进一步确认了这一点：将溶剂 ID 从伪连续距离改为 one-hot 后，40-experiment
GP/random 配对效应由 -0.076 翻转到 +0.032（5 seeds，3 胜 2 负）。该结果仍低于 0.05 SESOI，
但说明首要缺陷在搜索表示而不是世界物理；下一轮须以 20 paired seeds 复核，并把类别编码纳入
正式 agent contract。

## 与近期公开工作的定位差异

ChemWorld 的合理定位是预算受限、部分可观测、闭环虚拟实验中的策略评测与训练研究，不是静态
化学问答，也不是实际产率预测。相关公开工作给出的最低比较维度包括：

- [ScienceAgentBench (ICLR 2025)](https://openreview.net/forum?id=6z4YKr0GK6)：可执行、可验证的
  科学任务与端到端 agent 评价；
- [SciAgentGym (ICML 2026)](https://openreview.net/forum?id=0Moj0YgFEF)：多步科学工具调用、长程
  退化与可训练轨迹；
- [MADE (ICML 2026)](https://openreview.net/forum?id=nrXxVDYMMF)：预算约束闭环发现、可交换组件
  和随搜索空间扩大的自适应收益；
- [ChemCost (2026)](https://arxiv.org/abs/2605.07251)：冻结数据快照、无需 LLM judge 的标量评分、
  阶段级失败诊断和受控噪声鲁棒性。

因此 ChemWorld 的论文主张必须由真实闭环策略排序、跨 world-family 泛化、资源匹配和逐轨迹证据
支撑，而不能只依赖任务能运行或不同 agent 得分不完全相同。

## 阶段顺序

1. 先让冻结检查器验证 release manifest、当前 task hash 与所有证据摘要，失配必须失败；
2. 统一接入已经通过 intake 的 vNext 物理模块并重冻结任务；
3. 修复低分辨率/不稳定任务，完成 paired-seed 功效分析；
4. 建立轴级 OOD、私评、metamorphic invariance 和 exploit 审计；
5. 在相同实验与资源预算下运行传统优化、主动学习、RL 和真实 LLM；
6. 从冻结摘要生成统计表、矢量图、AAAI LaTeX、PDF 与不可变 release tag。
