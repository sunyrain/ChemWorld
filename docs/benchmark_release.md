# Benchmark 状态与发布协议

ChemWorld-Bench 评估 Agent 在未知、部分可观测、实验有成本的虚拟化学系统中，能否通过多轮
实验改进后续决策。当前版本是可审计的 backend candidate，不是已经完成科学验证的正式榜单。

## 候选任务

| Task | 核心能力 | Primary metric |
| --- | --- | --- |
| `partition-discovery` | 主动探索未知分配行为 | `product_in_organic` |
| `reaction-to-crystallization` | 反应–结晶联合决策 | `crystal_yield` |
| `reaction-to-distillation` | 反应–馏分联合决策 | `distillate_purity` |
| `flow-reaction-optimization` | 流动、热与风险权衡 | `flow_conversion` |
| `electrochemical-conversion` | 电化学选择性与能效权衡 | `electrochemical_selectivity` |
| `equilibrium-characterization` | 有限仪器预算下的平衡表征 | `equilibrium_confidence` |

这些任务采用 campaign 形式：一次 final assay 结束当前实验，但 Agent 可以在总预算内根据反馈启动
下一次实验。正式结果逐任务解释，不用任意权重合成跨任务总排名。

## 已经验证的能力

- task、scenario、world law、observation、scoring 和 trajectory 具有版本化合同与摘要；
- 正式 runner 对合同漂移、脏工作区、实验不足和 replay 失败执行失败关闭；
- World Law v0.4 的正式运行时使用显式 provider，已经替代旧 proxy/fallback 路由；
- 冻结的 v0.1 发表候选协议完成了 6 tasks × 5 methods × 20 paired seeds，共 600 条经典方法
  结果，每条包含 40 次完整实验并通过回放；
- 结构化 GP 相对 random 的复合得分在六个任务上均为正且经多重比较校正后显著；分配、结晶、
  蒸馏和流动四个任务同时显示较稳定的主指标与新 seed/private shift 收益；
- 基础非法动作、提前结束、重复 assay、非有限数值和 action key 重排检查已经通过。

## 尚未通过的发布门禁

- 六个任务中只有两个任务的主指标收益达到预注册的 0.05 SESOI；电化学和平衡的主指标区间
  不能支持自适应能力改善；
- 12 个声明的 world-family 轴尚不具备完整的插值、外推、组合变化和观测噪声控制；
- 除 action key order 外，物料重映射、observation 重排和等价动作序列不变性尚未实现；
- 正式经典方法矩阵有连续风险观测，但 600 条结果没有一次 safety violation，约束从未激活；
  structured safe GP 也没有一致降低风险，因此当前结果不能证明 safe BO 或约束学习有效；
- 正式五方法只在完整实验之间更新 recipe，不消费中间谱图；扩展经典方法和真实 LLM 缺少保留的
  多 seed replay artifact；
- 尚缺统一资源预算下的 RL、真实 LLM、独立复现和最终论文 artifact。

因此，当前 `benchmark/releases/chemworld-serious-vnext` 标记为
`release_status=candidate_backend_only`、`benchmark_claim_allowed=false`。历史
`chemworld-serious-v1` 只保留为旧候选证据，不代表当前运行时的冻结结论。

## 运行候选任务

安装后可以列出任务并运行本地交互或基线：

```bash
chemworld tasks list
chemworld tasks readiness
chemworld baselines report --preset serious --output-dir runs/serious
```

维护者可以验证当前候选包与发表协议：

```bash
python scripts/audit_vnext_runtime_integration.py
python scripts/audit_publication_protocol.py
python scripts/audit_publication_generalization_security.py
python scripts/run_release_gate.py
```

这些命令通过表示合同、证据和运行时一致，不表示所有科学门禁已经通过。正式 release 还要求
主指标有效性、独立 world-family 泛化、资源公平的方法矩阵和第三方复现同时成立。

## 如何解释分数

分数用于比较 Agent 在同一冻结虚拟世界合同中的实验策略。它不预测真实物料产率、装置安全或
工业性能，也不应跨合同版本直接比较。任务中的物料名称、仪器输出和物理模块是可审计的虚拟
实验接口；其适用域和已知限制应与结果一同引用。
