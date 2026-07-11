# ChemWorld 主路线图

最后更新：2026-07-11

这是仓库内唯一的执行级路线图。它服务于维护者与协作者，不加入公开站点导航。面向使用者的
状态、运行方法和限制以 `docs/benchmark_release.md` 与 `docs/limitations.md` 为准。

## 维护与认领规则

- 所有代码、实验、文档和发布任务都必须先按 `claims/README.md` 创建并推送 active claim。
- 一个 claim 只对应下文一个任务包；环境合同、方法实现、实验结果和论文写作不得混在同一 claim。
- `[x]` 仅表示验收证据已生成且门禁通过；代码存在、任务可运行或报告生成均不等于科学结论成立。
- 修改 task、scenario、world law、observation、scoring 或 replay 语义时，必须升级合同版本并重跑证据。
- `publication_protocol_v0.1` 及其结果保持不可变。任何针对任务的整改进入下一协议版本，禁止事后
  调整旧协议以改善结果。
- 发布门禁在本地执行，不依赖 CI 或 GitHub Actions。

## 当前结论

ChemWorld 已经具备扎实的 benchmark 工程底座和可审计的正式实验管线，但六任务整体还不能称为
“科学验证完成”或“发表就绪”。最准确的状态是：

- backend：`candidate_backend_only`；
- benchmark：`blocked`；
- 可靠的初步能力证据：4/6 个 serious task；
- 可发布论文主张：尚未解锁。

当前瓶颈不是继续堆更多 agent 名称，而是让任务主指标、风险信号、独立分布轴和外部复现共同
闭环。工程 ready 与科学 validated 必须继续分开报告。

## 可复核成熟度记分卡

| 维度 | 当前证据 | 判定 |
| --- | --- | --- |
| 工程合同与运行时 | 6/6 serious task 合同可审计；World Law v0.4 接入 8 个正式 provider，旧正式 proxy/fallback 已移除 | 已完成候选底座 |
| 正式经典方法实验 | 6 tasks × 5 methods × 20 paired seeds = 600 条结果；每条 40 次完整实验并通过 replay | 已完成 v0.1 |
| 主比较 total score | structured GP 相对 random 为 6/6 正向且 Holm 显著，4/6 达到 0.05 SESOI | 支持复合得分收益 |
| 任务主指标 | 2/6 达到 SESOI，4/6 置信区间方向为正；电化学、平衡不成立 | 阻塞六任务统一主张 |
| public/private seed shift | 两组各 240 条结果；分配、结晶、蒸馏、流动为 4/6 稳定 | 部分通过 |
| 独立分布轴 | 6 tasks × 2 declared axes 中 0/12 具备 interpolation、extrapolation、composition、noise 全套控制 | 未通过 |
| 不变性 | 4 项中仅 action key order 可执行并通过 | 1/4，未通过 |
| 基础 exploit | 6 tasks × 6 probes = 36 项通过 | 基础门禁通过 |
| 安全学习信号 | 更正字段映射后，600 条结果的 `mean_safety_risk` 均为非零，但 safety violations 仍为 0；约束从未激活 | 有连续风险、无约束辨识，不支持 safe BO 主张 |
| 方法交互覆盖 | 正式 5 方法只在实验间更新完整 recipe，均不使用中间谱图；GP-PI/UCB、RF-EI、greedy 与真实 LLM 缺少保留的正式 artifact | 不完整 |
| 独立复现 | 尚无第三方从干净 wheel 重现冻结摘要 | 未完成 |
| 论文产物 | 尚无冻结图表、AAAI LaTeX、PDF 与可引用 release tag | 未开始 |

机器证据以以下摘要为准：

- `workstreams/benchmark_v1/reports/publication-classic20-full-summary.json`；
- `workstreams/benchmark_v1/reports/publication-generalization-security-summary.json`；
- `configs/benchmark/publication_protocol_v0.1.json`；
- `configs/benchmark/generalization_security_v0.1.json`。

## 论文主张边界

| 状态 | 可以或不可以声称 |
| --- | --- |
| 已支持 | ChemWorld 提供预算受限、部分可观测、可回放的多轮虚拟实验任务；结构化 GP 在四个任务上显示跨 seed/public/private shift 一致的自适应收益；所有结果可从冻结轨迹审计 |
| 仅探索性 | 六任务 total-score 均有统计差异；one-hot 表示改善电化学复合得分；当前虚拟物理足以用于方法诊断 |
| 禁止 | 六任务 benchmark 已验证；safe BO 有效；结果代表真实化学产率、安全性或工业性能；已达到 agent benchmark SOTA；在没有 RL/真实 LLM/资源对齐时声称全面方法排名 |

论文的最小可信故事应是“受控虚拟化学世界中的闭环实验智能”，而不是“LLM 发现真实化学”。其
贡献必须落在可交换的环境合同、主动探索效应、分布外评测、反作弊和训练迁移，而不是物理数值
与现实一一对应。

## 发布决策门禁

1. **G0 — Backend candidate（已通过）**：正式运行时、合同、回放和基础 provider provenance
   可审计，但不授予 benchmark 科学有效性。
2. **G1 — Task validity**：每个正式任务的主指标存在非退化学习信号，风险/成本字段真实影响决策，
   且最低合理策略、random、强策略形成可解释排序。
3. **G2 — Generalization/security**：每个正式任务至少两个独立 world-family 轴可控制，四种 shift
   模式、不变性、仅公开 observation harness 和扩展 exploit 门禁通过。
4. **G3 — Method fairness**：经典优化、RL、真实 LLM 使用冻结 adapter 和清晰的实验/墙钟/token/
   费用账本；失败与负结果完整报告。
5. **G4 — Reproduction/release**：第三方从干净 wheel 重建公开摘要，冻结图表和论文只读取签名
   摘要，候选包通过本地 release gate 并打不可变 tag。

若电化学与平衡在下一协议的两轮定向整改后仍不能通过 G1/G2，默认发布通过门禁的四任务 core
suite，并把这两个任务降为 exploratory。不得为了保留“六任务”而降低门禁。

## 可并行认领的任务包

表中任务包在 owned paths 不重叠时可以并行。`依赖` 是开始正式实验前必须满足的门禁，不是认领
文档或设计工作的限制。

### P0：决定正式任务集

| Task ID | 负责面 | 交付与验收 | 依赖 |
| --- | --- | --- | --- |
| `benchmark-vnext-task-validity` | 核心评测 | 六个逐任务有效性卡：响应面、主指标对齐、最低合理策略、失败案例、接受/降级决定；明确 core-4 或 core-6 | 无 |
| `wf-vnext-risk-cost-signal` | 世界基座团队 | 保留已有连续 risk，同时校准任务级安全阈值/危险区，使约束命中率既非全零也非饱和；策略改变必须改变风险—性能前沿 | 无 |
| `wf-vnext-world-family-axes` | 世界基座团队 | 每任务至少两个有物理解释的独立轴，支持插值、外推、组合变化和观测噪声；生成器与 Bench seed 隔离 | 无 |
| `benchmark-vnext-semantic-invariance` | 核心评测 | 物料代号重映射、observation 字段重排、等价动作序列和格式扰动可执行；定义配对容差并通过 | world-family 合同 |
| `benchmark-vnext-public-harness` | 安全/评测 | 独立进程仅通过公开 action/observation 交互；隐藏状态、debug、异常、路径和任务文本泄漏扫描通过 | task validity |
| `benchmark-vnext-exploit-matrix` | 安全/评测 | 覆盖无成本测量、预算边界、非法动作刷分、NaN/Inf、重复 assay、提前结束和 replay 差异；全部 fail closed | public harness |

P0 退出条件：正式任务全部通过 G1/G2，或明确形成 core suite + exploratory suite；生成新的协议版本，
旧 v0.1 结果不被覆盖。

### P1：冻结评测与方法公平性

| Task ID | 负责面 | 交付与验收 | 依赖 |
| --- | --- | --- | --- |
| `benchmark-vnext-score-replay` | 核心评测 | primary score 与在线 reward 分离；单位、方向、缺失值、异常值固定；结果只能从初始轨迹重算，篡改被拒绝 | P0 |
| `benchmark-vnext-method-protocol` | 方法协议 | 统一 adapter、checkpoint、随机性、实验次数、墙钟、CPU/GPU、token、费用、prompt/model provenance；资源超限 fail closed | P0 |
| `benchmark-vnext-classic-baselines` | 经典方法 | random、LHS、greedy、GP-EI/PI/UCB、RF-EI、约束/安全方法；验证行为不退化为同一策略 | method protocol |
| `benchmark-vnext-rl-baselines` | RL | 独立 Train world-family、向量环境、至少 PPO 与一个连续控制/离线对照；只在冻结 Bench worlds 评测 | world-family axes、method protocol |
| `benchmark-vnext-llm-baselines` | LLM agent | 至少两类真实模型，多轮读谱/实验/更新；只保存结构化 hypothesis/evidence/uncertainty/decision summary，不要求私有 chain-of-thought | method protocol、public harness |
| `benchmark-vnext-reference-regret` | 评测统计 | 冻结独立 best-known/reference 协议，给出 coverage 与不确定性；不得再把随机采样最大值称为 oracle | score replay |

P1 退出条件：所有方法使用同一任务合同和资源账本；逐任务报告 effect、sample efficiency、regret、
约束违反和资源前沿，任何方法失败不得静默丢弃。

### P2：复现、论文与发布

| Task ID | 负责面 | 交付与验收 | 依赖 |
| --- | --- | --- | --- |
| `benchmark-vnext-independent-reproduction` | 独立复现者 | 从干净 wheel 和公开命令重跑指定 seeds；摘要、合同 hash、trajectory digest 与容差一致 | P1 |
| `benchmark-vnext-statistics-figures` | 统计/绘图 | paired bootstrap、Holm、rank stability、预算曲线、OOD、constraint/resource frontier；矢量图只从冻结摘要生成 | P1 |
| `paper-nature-chemworld` | 论文 | 仅在训练迁移、独立复现和方法门禁通过后启动 Nature Article；正文、Methods、source data、代码/数据可用性和 PDF 严格服从主张矩阵 | figures、independent reproduction、Train→Bench/Bridge transfer |
| `benchmark-vnext-release` | 发布 | wheel、公开合同、seed suite、报告、golden trajectory、验证命令、限制说明和私评摘要；本地门禁通过并打不可变 tag | 论文结果冻结 |

## 已完成并关闭的任务包

- [x] `benchmark-v1-release-integrity`：release manifest、task hash、commit、dirty tree、evidence digest
  与轨迹索引执行失败关闭。
- [x] `wf-110-vnext-runtime-integration`：8 个 World Law v0.4 provider 接入正式运行时，旧 proxy/
  fallback 路由移除，重建 candidate backend 证据。
- [x] `benchmark-v1-validity-power`：冻结 v0.1 的 paired-seed、SESOI、功效与正式经典方法矩阵；
  结论为部分通过、suite blocked。
- [x] `benchmark-v1-generalization-security`：完成 seed OOD、salted private shift、基础 exploit 以及
  轴/不变性缺口的机器化审计；结论为 4/6 稳定、suite blocked。
- [x] `benchmark-vnext-agent-interaction-audit`：更正 publication risk 字段映射；确认连续风险存在但
  约束未激活，并机器化记录经典方法、谱图、实验内自适应和真实 LLM artifact 缺口。

## Phase 2：Bench 冻结后的 Train / Bench / Bridge

Phase 2 不阻塞当前 benchmark 冻结，但接口约束应在 P0/P1 中预留。

- **ChemWorld-Bench**：只评测、版本化、可回放；公开测试与私评使用同协议、不同隐藏世界族。
- **ChemWorld-Train**：程序化 world generator、向量化 reset/step、课程难度和 train/dev/OOD split；
  禁止在冻结 Bench worlds 上训练。
- **ChemWorld-Bridge**：对接真实 HTE 数据、外部优化 benchmark、数字孪生或设备抽象；以策略排序
  一致性和训练前后迁移提升证明外部有效性，不要求模拟值精确复现现实。
- **共同合同**：typed action、observation、trajectory、provenance、verifier；物料同时支持中性代号
  与真实语义 skin，用配对实验分离预训练知识和主动探索能力。

Phase 2 的第一个研究里程碑不是扩大任务数量，而是证明“在 Train world-family 学习后，在未见
Bench worlds 或外部 data-replay 上显著优于同预算从零开始的 agent”。这才回答 ChemWorld 能否
作为 gym 让 agent 变强。

## 当前建议的执行顺序

1. 并行认领 `benchmark-vnext-task-validity`、`wf-vnext-risk-cost-signal` 和
   `wf-vnext-world-family-axes`。
2. 根据逐任务卡作 core-4/core-6 决策，冻结新合同与协议版本。
3. 并行完成 semantic invariance、public harness、exploit matrix 和 score/replay。
4. 冻结 method protocol 后再并行跑经典、RL 和真实 LLM；先跑方法后改任务的结果全部作废。
5. 先证明 Train→未见 Bench/Bridge 的迁移收益；独立复现通过后才生成 Nature 投稿稿和 release，
   论文不得反向驱动调参。

## 本地常用门禁

```powershell
python scripts/manage_claims.py check
python scripts/audit_publication_protocol.py
python scripts/audit_publication_generalization_security.py
python scripts/run_release_gate.py
python -m pytest
python -m ruff check .
python -m mypy src
python -m mkdocs build --strict
```
