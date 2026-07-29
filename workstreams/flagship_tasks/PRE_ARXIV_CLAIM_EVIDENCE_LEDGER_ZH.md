# 首次 arXiv 前的论断—证据账本

状态：`窄范围双任务描述性论文可继续；广义 benchmark 与模型恢复论断仍禁止`

权威机器文件：`workstreams/flagship_tasks/reports/pre-arxiv-claim-evidence-ledger-v1.json`

## 已经可以写什么

- 15 个任务通过 415 个确定性完整配方案例；62 个声明指标全部绑定到可执行评估端点。
- 静态 S0 v1.0 中，电化学 Codex 均值 0.7150，最佳 information-matched 基线为
  0.6159，描述性配对差 +0.0991，世界 bootstrap 区间为 [+0.0103,+0.1748]。
- 结晶 Codex 均值 0.5355，低于 LHS 的 0.5708；差值 −0.0353，区间
  [−0.0650,−0.0085]。这是负结果，必须保留。
- 正确匿名材料属性的十世界确认性结果具有任务差异：电化学 0.7874 vs opaque
  0.7150，配对差 +0.0724，双任务 familywise 97.5% 区间
  [+0.0074,+0.1546]；结晶 0.5615 vs 0.5355，配对差 +0.0260，区间
  [−0.0130,+0.0630]。因此只能确认电化学的信息价值，结晶仍不确定。
- 固定、定向的错误材料先验在两个任务中都通过了操纵检验，说明 dossier 确实改变了早期动作。
  但电化学只通过行为纠偏、未证明性能恢复到 opaque；结晶性能不低于 opaque，却未通过差分行为
  纠偏。两个任务都没有通过预注册的整体恢复联合规则。
- 三臂材料信息实验的 60 个 task/world/arm 单元全部完成并精确 replay：1,260 次成功
  Codex subscription 调用、5 次自动重试、2,280 次物理实验、0 个方法失败。
- 静态 v1.0 参与者与经典基线 artifact 也全部精确 replay，总账为 28,060 次物理实验。

## 现在不能写什么

- 不能写 Codex 普遍优于全部经典算法；电化学相对最佳 privileged calibration 基线的区间跨 0。
- 不能写 Codex 在结晶上优于经典优化。
- 不能把优化分数解释为正确机理理解或新方法综合。
- 不能把结晶错误先验条件下较高的样本均值解释为“模型识别并纠正了错误信息”。
- 不能写模型普遍能从错误先验中恢复；两个任务均未通过预注册联合恢复规则。
- 不能推广到 15 个任务、private worlds、其他 provider/scaffold、真实化学或高保真 backend。
- 不能把内部精确 replay 称为独立复现。

## 哪些新实验是论断所需

窄范围首次 arXiv 若忠实报告双任务描述性结果、信息价值的任务差异和恢复失败，本身不强制再做新的
科学实验。当前工程 blocker 是 clean-release attestation、全文一致性、统计措辞审阅与独立
artifact reproduction。

任何更强论断分别需要：

1. 结晶优越性：另行冻结主要经典 comparator、superiority margin、多重比较规则与未触碰世界。
2. 广义材料信息价值：使用独立模型/provider 和新冻结世界复现；当前确认性正结果仅限电化学。
3. 广义错误先验恢复：预注册多个映射、任务、provider 与世界，并继续要求操纵、差分行为纠偏和
   性能恢复三者联合通过。
4. public→private 泛化：运行对齐的 public/private campaign，使用冻结的 gap 与
   rank-confidence 端点。
5. 机制适应：若要声称适用于当前源码，先重认证 Gate A，再冻结并执行 participant Gates B–E。
6. 现实迁移：完成独立 backend、真实数据或窄物理系统 bridge，并预注册 transfer endpoint。
