# Benchmark v1 科学有效性收束

本工作流把“代码和发布管线可以运行”与“benchmark 足以支持论文结论”分开验收。当前正式
readiness 只证明 6 个任务在 5 个冻结 seeds 上可执行、可重放且存在一定策略差异；它不能替代
统计功效、跨分布稳定性、真实方法覆盖、私评、反作弊和完整证据链。

## 审计口径

机器审计覆盖八类证据：研究主张、逐任务有效性、方法覆盖、泛化与安全、backend 可信度、发布
证据链、训练环境就绪度和论文就绪度。`blocker` 采用 fail-closed：任何 blocker 未关闭时只能称为
candidate，不能发布“完整且有意义的 benchmark”或最终论文结论。

先生成 held-out seed 诊断，再生成缺口报告：

```powershell
.\.venv\Scripts\python.exe scripts\audit_serious_generalization.py `
  --output-dir runs/benchmark_v1_gap_audit/generalization_runs `
  --output runs/benchmark_v1_gap_audit/generalization_audit.json

.\.venv\Scripts\python.exe scripts\audit_benchmark_v1_gap.py
```

`--require-ready` 用于最终门禁；在整改完成前它应返回非零，而不是制造虚假的绿色状态。

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
