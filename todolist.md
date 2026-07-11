# ChemWorld 主路线图

最后更新：2026-07-12

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
| 任务主指标 | 新 task-validity 协议下分配/结晶/蒸馏达到 absolute SESOI，流动仅尺度归一化通过；旧 publication gate 仍为 2/6；电化学/平衡不成立 | 建议 provisional core-4；冻结 task-specific SESOI 后重跑确认 |
| public/private seed shift | 两组各 240 条结果；分配、结晶、蒸馏、流动为 4/6 稳定 | 部分通过 |
| 独立分布轴 | 6 tasks × 2 axes 已具备可执行 interpolation、extrapolation、composition、observation-noise 控制；12/12 单轴探针改变真实任务响应 | 控制层通过；严重度校准、split 冻结和方法实验未完成 |
| 机理族 | 六任务均有实际 provider 消费的机理/构成律族：三类反应任务使用速率律/拓扑族，分配、电化学、平衡使用专属 constitutive-law 族；5 seeds × 5 配方下 9/9 任务-模式组合可区分、非灾难且守恒 | core-6 控制层通过；agent 机理识别、适应与跨族迁移未测 |
| 不变性 | 4 项中仅 action key order 可执行并通过 | 1/4，未通过 |
| 基础 exploit | 6 tasks × 6 probes = 36 项通过 | 基础门禁通过 |
| 风险与成本信号 | 600 runs / 24,000 experiments 已按 calibration/holdout 重算；任务级峰值风险触发率 14.9%–43.3%，过程成本触发率 8.5%–14.8% | 控制层可辨识；旧方法未收到新策略，仍不支持 safe BO 主张 |
| 评价分层 | vNext 0.3 分离 final-assay objective、task primary、在线 shaping、constraint、resource 与 validity，并增加不入总分的交互层级、实际适应证据、外部资源账本和脚手架协助诊断 | 控制层通过；旧正式方法未统一接收 vNext 风险策略，评价结论仍不可识别 |
| 方法交互覆盖 | recipe-search / operation-open-loop / operation-closed-loop 已分层；官方 live-LLM adapter 支持谱图消融、跨实验记忆、失败计费且不代办收尾；单 seed 100k SAC 通过 Dev 门槛但 checkpoint 非单调 | 控制层通过；真实 LLM 运行、RL 多 seed/全任务与同层正式比较未完成 |
| 独立复现 | 尚无第三方从干净 wheel 重现冻结摘要 | 未完成 |
| 论文产物 | 尚无冻结图表、Nature Article 稿件、PDF 与可引用 release tag | 未开始，按门禁暂缓 |

机器证据以以下摘要为准：

- `workstreams/benchmark_v1/reports/publication-classic20-full-summary.json`；
- `workstreams/benchmark_v1/reports/publication-generalization-security-summary.json`；
- `workstreams/benchmark_v1/reports/world-family-axis-controls.json`；
- `workstreams/benchmark_v1/reports/agent-interaction-contract.json`；
- `workstreams/benchmark_v1/reports/evaluation-identifiability-controls.json`；
- `workstreams/benchmark_v1/reports/mechanism-family-controls.json`；
- `workstreams/benchmark_v1/reports/risk-cost-signal-controls.json`；
- `workstreams/benchmark_v1/reports/task-validity-vnext.json`；
- `workstreams/benchmark_v1/reports/method-protocol-vnext.json`；
- `workstreams/benchmark_v1/reports/rl-100k-development.json`；
- `workstreams/benchmark_v1/reports/live-llm-controls.json`；
- `workstreams/benchmark_v1/reports/safe-policy-confirmatory.json`；
- `configs/benchmark/publication_protocol_v0.1.json`；
- `configs/benchmark/generalization_security_v0.1.json`；
- `configs/benchmark/generalization_security_vnext.json`；
- `configs/benchmark/agent_interaction_vnext.json`；
- `configs/benchmark/evaluation_vnext.json`；
- `configs/benchmark/mechanism_families_vnext.json`。
- `configs/benchmark/risk_cost_vnext.json`。
- `configs/benchmark/task_validity_vnext.json`。
- `configs/benchmark/method_protocol_vnext.json`。

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
| `benchmark-vnext-task-validity` | 核心评测 | 六张有效性卡已完成：分配/结晶/蒸馏 core-confirmed，流动 core-candidate，电化学/平衡 exploratory；建议 provisional core-4；旧 publication gate 的 2/6 历史结论保持不变 | 控制实现完成；冻结 task-specific SESOI 后确认重跑 |
| `wf-vnext-risk-cost-signal` | 世界基座团队 | 任务级 operational-risk budget 与 process-cost limit 已由独立校准切片冻结；评价使用实验全过程峰值风险并拆分 total/process/measurement 三账 | 控制实现完成；方法重跑待 method protocol |
| `wf-vnext-world-family-axes` | 世界基座团队 | 每任务两个轴及四模式的可执行控制已完成；下一步冻结严重度网格与 Train/Dev/Bench 分配，并运行配对方法实验 | 控制实现完成 |
| `wf-vnext-mechanism-families` | 世界基座团队 | ReactionNetwork 三任务与分配/电化学/平衡专属 constitutive-law family 已完成多 seed/多配方强度校准、opaque hash 和精确回放绑定；下一步为 Train/Dev/Bench 机理迁移实验 | core-6 控制实现完成 |
| `benchmark-vnext-agent-interaction-contract` | Agent/环境 | 逐操作公共上下文、谱图递交、显式能力声明和结构化 decision audit 已完成；三层资源预算冻结与正式方法重跑仍待 method protocol | 控制实现完成 |
| `benchmark-vnext-evaluation-identifiability` | 核心评测 | 六层端点评价、交互能力分层、适应证据、脚手架协助 provenance、实验峰值风险与环境/模型/训练资源账本已绑定 replay；跨层只允许系统级解释 | 控制实现完成；全方法新风险策略重跑待 method protocol |
| `benchmark-vnext-semantic-invariance` | 核心评测 | 物料代号重映射、observation 字段重排、等价动作序列和格式扰动可执行；定义配对容差并通过 | world-family 合同 |
| `benchmark-vnext-public-harness` | 安全/评测 | 独立进程仅通过公开 action/observation 交互；隐藏状态、debug、异常、路径和任务文本泄漏扫描通过 | task validity |
| `benchmark-vnext-exploit-matrix` | 安全/评测 | 覆盖无成本测量、预算边界、非法动作刷分、NaN/Inf、重复 assay、提前结束和 replay 差异；全部 fail closed | public harness |

P0 退出条件：正式任务全部通过 G1/G2，或明确形成 core suite + exploratory suite；生成新的协议版本，
旧 v0.1 结果不被覆盖。

### P1：冻结评测与方法公平性

| Task ID | 负责面 | 交付与验收 | 依赖 |
| --- | --- | --- | --- |
| `benchmark-vnext-score-replay` | 核心评测 | primary score 与在线 reward 分离；单位、方向、缺失值、异常值固定；结果只能从初始轨迹重算，篡改被拒绝 | evaluation identifiability |
| `benchmark-vnext-method-protocol` | 方法协议 | 统一资源账本已接入 runner；冻结 40 次完整实验、20 个新 paired seeds、5 个 checkpoint，并对墙钟、CPU/GPU、模型调用、token、费用和 provenance 执行 fail closed | 控制实现完成；P0 冻结与缺失方法实现后才能正式重跑 |
| `benchmark-vnext-classic-baselines` | 经典方法 | random、LHS、greedy、typed GP-EI/PI/UCB、typed RF-EI 与 typed constrained GP 均已实现；正式矩阵须验证行为不退化为同一策略 | method protocol 已完成；P0 冻结后重跑 |
| `benchmark-vnext-rl-baselines` | RL | SAC 单 seed 精确 100k Train/Dev 已通过稳定性、完成率、有效性与 10/10 replay 门槛；80k Dev 明显优于 100k，下一步预注册 pooled multi-seed checkpoint 选择，再扩展 core task；Bench 尚未访问 | 先解决 checkpoint 稳定性；随后 method protocol |
| `benchmark-vnext-llm-baselines` | LLM agent | 官方逐操作 adapter、公开谱图/遮蔽配对、跨实验记忆、结构化公开审计、token/费用/重试账本与失败保留已实现并通过 fake-client replay；真实 Pro/Flash 矩阵仍缺凭证与运行 | method protocol、真实 API 运行与独立复现 |
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
- [x] `wf-vnext-world-family-axes`：六任务共 12 个物理解释轴接入真实 provider；四种 shift、确定性
  干预 hash、零干预兼容、公共视图隐藏和逐轴任务响应均通过机器审计，但方法泛化实验仍未开始。
- [x] `benchmark-vnext-agent-interaction-contract`：正式 runner 向兼容 Agent 提供逐操作公共决策上下文，
  下一决策可读取公开谱图；recipe 方法、BO/greedy 的跨/实验内适应能力被分别如实声明，结构化决策证据写入轨迹。
- [x] `benchmark-vnext-evaluation-identifiability`：v0.3 evaluator 在六层终点之外绑定交互能力层级、
  实际适应证据、脚手架协助 provenance 与方法资源账本；所有新增诊断不入总分，跨层不得作算法归因。
- [x] `wf-vnext-mechanism-families`：ReactionNetwork 三任务与分配、电化学、平衡专属 constitutive
  family 通过 5 seeds × 5 配方的可区分/非灾难/守恒校准；干预版本与 opaque hash 入轨迹，精确上下文缺失或篡改时回放失败关闭。
- [x] `wf-vnext-risk-cost-signal`：600 条正式 run 的 24,000 次实验按 calibration/holdout 重算；
  风险用每次实验峰值、成本拆为 total/process/measurement。六任务信号均非零非饱和，但旧方法未接收新策略，
  且经典 recipe 的测量日程固定，因此 safe-method 与 measurement-efficiency 主张继续关闭。
- [x] `benchmark-vnext-task-validity`：六张机器可读有效性卡绑定正式 20-seed 方法证据、响应面与风险—成本审计；
  推荐 provisional core-4（分配、结晶、蒸馏、流动），电化学和平衡降为 exploratory。该建议不是发布结论，
  task-specific SESOI 与 vNext confirmatory rerun 仍是硬门禁。
- [x] `benchmark-vnext-method-protocol`：经典、RL 与真实 LLM 共用的累积资源账本已接入正式 runner；
  pre-freeze 结果强制为 diagnostic-only，replay/stub 明确排除出 LLM 证据。当前仍缺 PPO、SAC、两类 live LLM，
  正式方法矩阵继续关闭。
- [x] `benchmark-vnext-classic-typed-acquisitions`：GP-PI、GP-UCB 与 RF-EI 已新增 typed categorical
  material encoding，并由实际 manifest 门禁确认；旧 ordinal 变体只保留兼容用途，不进入正式方法矩阵。
- [x] `live-llm-official-adapter`：逐操作官方 adapter 已实现公开谱图与遮蔽消融、跨实验记忆、公开
  decision audit、provider 重试/token/费用账本和失败保留；无自动修复/终止/终测，fake-client 轨迹精确回放。
- [x] `rl-100k-accounting`：修复后 SAC 在 Train 上精确完成 100,000 步，五个 checkpoint 与 replay
  buffer 均有摘要；20 个 Dev episode 与 10 条标准回放通过开发门槛，但 80k→100k 显著退化，正式矩阵仍关闭。

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

1. 冻结 provisional core-4 的 task-specific SESOI；core-6 机理/构成律控制已完成，但电化学与平衡仍须通过任务有效性确认，不能因机理族就升级为核心任务。
2. 预注册 SAC pooled multi-seed 的 80k/100k Dev checkpoint 选择；真实 LLM 只从官方 adapter 运行 Pro/Flash 与谱图消融。
3. 冻结机制、交互、评价、风险—成本和 world-family 新合同，运行 core-4 confirmatory round。
4. 冻结严重度网格与 Train/Dev/Bench 世界分配，再完成 semantic invariance、public harness、
   exploit matrix 和 score/replay。
5. method protocol 控制已冻结；完成 typed classic、RL 和 live LLM adapter 后再并行正式重跑，
   先跑方法后改任务的结果全部作废。
6. 先证明 Train→未见 Bench/Bridge 的迁移收益；独立复现通过后才生成 Nature 投稿稿和 release，
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
