# 证据与当前状态

本页是网站的人类可读状态真源；机器可读真源是
[`configs/current.json`](https://github.com/sunyrain/ChemWorld/blob/main/configs/current.json)。
实验设计和完整数值见[旗舰实验](flagship_experiments.md)，解释见[研究发现](research_findings.md)。

!!! warning "当前不是可发布的完整 benchmark"
    候选后端通过了合同验证和 clean-release attestation，但机制证据与当前源码的绑定已经过期，
    Participant Gates B–E 尚未执行。当前 `benchmark_ready=false`、`publication_ready=false`，
    不支持 SOTA、完整模型排名或现实世界迁移主张。

## 状态总览

| 层级 | 当前状态 | 已经证明 | 尚未证明 |
| --- | --- | --- | --- |
| 运行时与任务合同 | **通过候选验证** | v0.5 candidate 可运行；15 个任务适配器和 62 个指标端点可执行 | 科学真实性或模型优越性 |
| 双旗舰静态优化 | **正式描述性结果完成** | 两个任务、10 个独立世界、每世界 20 轮、经典基线、精确 replay | 预注册 superiority、跨任务或跨 provider 泛化 |
| 匿名材料三臂实验 | **正式确认性分析完成** | `opaque / nominal / misindexed` 配对设计、60 个单元、完整审计 | 两个任务上的统一“错误先验恢复”能力 |
| 机制环境 Gate A | **历史通过，当前绑定过期** | RC28 冻结版本上的 A1/A2/A3 环境证书 | 当前源码上的重新认证；Participant 能力 |
| Participant Gates B–E | **待方法冻结与执行** | 协议骨架和部分开发诊断存在 | 时序检测、反馈归因、恢复和迁移结论 |
| 其余 13 个任务 | **设计可执行** | 边界案例、动作和评分合同通过 | 正式多世界方法比较 |
| 外部有效性 | **未建立** | 无 | 独立 backend、真实数据或物理系统复现 |

## 当前正式结果

### 静态 S0 v1.0：无材料 dossier

旧的固定世界双任务结果已经撤回。替代实验在相同协议下使用 Codex subscription participant，
完成 10 个独立世界、每世界 20 次自主探索、盲测终点和完整经典基线。

| 任务 | Participant 均值 | 世界 bootstrap 95% 区间 | 最佳 information-matched 基线 | 解释 |
| --- | ---: | ---: | ---: | --- |
| Electrochemical Conversion | **0.7150** | [0.6283, 0.7861] | 0.6159 | 描述性领先；未预注册 superiority |
| Reaction to Crystallization | **0.5355** | [0.5045, 0.5644] | 0.5708 | 低于 LHS，不支持领先 |

这组结果是**正式描述性结果**，不是完整 benchmark 排名。两任务合计 28,060 次物理实验，
其中 participant 760 次、420 次 provider 调用；全部 recommendation 均实际盲测并精确 replay。

### 静态 S0 v1.2：正确与错误的匿名材料信息

三臂只改变 dossier 与匿名材料 ID 的映射；世界、噪声、预算、模型和评分保持配对一致。

| 任务 | Opaque | Nominal | Misindexed | Nominal − Opaque | Misindexed − Nominal |
| --- | ---: | ---: | ---: | ---: | ---: |
| Electrochemical Conversion | 0.7150 | **0.7874** | 0.6853 | +0.0724；97.5% CI [+0.0074, +0.1546] | −0.1020；[−0.2101, −0.0078] |
| Reaction to Crystallization | 0.5355 | **0.5615** | 0.5845 | +0.0260；[−0.0130, +0.0630] | +0.0229；[+0.0046, +0.0419] |

由此可以说：

- 正确信息对电化学有确认的正信息价值；结晶的正信息价值仍不确定。
- 错误先验在两个任务中都改变了早期动作，但性能方向相反。
- 两个任务都没有通过预注册的整体恢复联合规则，因此不能声称模型普遍识别并纠正错误先验。

60 个任务×世界×臂单元全部精确 replay；共 2,280 次物理实验、1,260 次成功
Codex subscription 调用、5 次自动重试、0 次方法失败。

## 机制适应证据

RC28 在其冻结源码上完成了正式 Gate A 环境证书：A2 为 4,896 条 receipts，主预算 top-1
为 98.26%；A3 为 2,016 条 receipts，`k=8` 端到端成功率为 96.57%。这些数字说明冻结环境
在受控协议下可识别、参考策略可在线达到，**不说明 Participant Agent 已具备机制适应能力**。

当前源码指纹已经变化，相关 evidence nodes 标记为 `stale`。在重新认证前，历史
`gate_a_pass=true` 不得被解释为当前 `benchmark_ready=true`。

历史证据没有删除：

- [RC28 Gate A 运行后审计](https://github.com/sunyrain/ChemWorld/blob/main/workstreams/flagship_tasks/RC28_GATE_A_POSTRUN_SANITY_AUDIT_ZH.md)
- [RC28 Participant 正式实验计划](https://github.com/sunyrain/ChemWorld/blob/main/workstreams/flagship_tasks/RC28_PARTICIPANT_FORMAL_EXPERIMENT_PLAN_AND_TODO_ZH.md)
- [预 arXiv 论断—证据账本](https://github.com/sunyrain/ChemWorld/blob/main/workstreams/flagship_tasks/PRE_ARXIV_CLAIM_EVIDENCE_LEDGER_ZH.md)

## 发表边界

当前材料足以支持一篇范围严格的、以环境设计和双旗舰描述性实验为中心的工作稿，但还不是
submission-ready benchmark paper。第一次 arXiv 前至少要完成：

1. 重新绑定或重新执行当前源码上的机制 Gate A。
2. 冻结 Participant 方法、provider、功效和成本合同。
3. 执行 Gates B–E，或在论文中明确删除相应机制适应主张。
4. 冻结论文数字、表格、commit 与证据哈希，并做独立复核。

如果只发表窄范围描述性论文，不新增更强的机制适应、跨 provider 或现实迁移主张，则不需要
为了“补齐故事”盲目增加科学实验；需要做的是证据绑定、边界收紧和独立复核。

## 状态读取规则

页面出现冲突时按以下优先级处理：

1. `configs/current.json`
2. 冻结 summary / audit JSON
3. 本页
4. 其他解释性页面

早于 v0.5 的 classical、Safe-GP 和 SAC 数字只保留为开发诊断，不得与当前正式结果混合排名。
