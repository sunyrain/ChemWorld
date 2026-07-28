# 首次 arXiv 前的论断—证据账本

状态：`窄范围双任务描述性论文可继续；广义 benchmark 论断仍禁止`

权威机器文件：
`workstreams/flagship_tasks/reports/pre-arxiv-claim-evidence-ledger-v1.json`

## 已经可以写什么

- 15 个任务通过 415 个确定性完整配方案例；62 个声明指标全部绑定到可执行评估端点。
- 电化学 Codex 均值 0.7150，最佳 information-matched 基线为 0.6159，描述性配对差
  +0.0991，世界 bootstrap 区间为 [+0.0103,+0.1748]。
- 结晶 Codex 均值 0.5355，低于 LHS 的 0.5708；差值 −0.0353，区间
  [−0.0650,−0.0085]。这是负结果，必须保留。
- 参与者和基线的全部 task/world artifact 均精确 replay，总账为 28,060 次物理实验。

## 现在不能写什么

- 不能写 Codex 普遍优于全部经典算法；电化学相对最佳 privileged calibration 基线的区间跨 0。
- 不能写 Codex 在结晶上优于经典算法。
- 不能把优化分数解释为正确机理理解或新方法综合；所有最终 recommendation 相对已验证 incumbent
  的增益均为 0。
- 不能推广到 15 个任务、private worlds、其他 provider/scaffold、机制变化、真实化学或高保真 backend。
- 不能把内部精确 replay 称为独立复现。

## 哪些新实验是“论断所需”

窄范围首次 arXiv 若只报告双任务描述性结果和负结果，本身不强制再做科学实验；但必须明确没有
预注册 superiority 阈值和多重比较方案，并排除 SOTA、provider 因果、private 泛化、participant
机制适应和现实迁移论断。

任何更强论断分别需要：

1. 结晶优越性：先冻结 v1.1 participant policy、主比较、superiority margin 和多重比较规则，再跑
   未触碰世界；不得改写 v1.0。
2. 独立可重复性：使用独立模型/provider 和干净 checkout 复现。
3. public→private 泛化：运行对齐的 public/private campaign，使用已实现的 gap 与 rank-confidence
   端点。
4. 机制适应：若要声称适用于当前源码，先重认证 Gate A，再冻结并执行 participant Gates B–E。
5. 现实迁移：完成独立 backend、真实数据或窄物理系统 bridge，并预注册 transfer endpoint。

当前真正的首次 arXiv 工程 blocker 是 clean-release attestation、全文一致性、统计措辞审阅和独立
artifact reproduction，而不是为了隐藏结晶负结果而继续追加实验。
