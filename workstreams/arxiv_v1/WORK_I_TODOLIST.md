# Work I TODO — 可编程实验世界与实验智能体测量装置

最后更新：2026-08-03
工作边界：第一篇论文只证明 ChemWorld 是可执行、可控制、可干预、可审计的实验智能体测量装置；不承担规律适应、模型优劣、真实实验室迁移或通用 benchmark 排名主张。

## 1. 目标交付物

- 强化后的第一篇论文与六幅主图；
- world-fork programmability certificate；
- known-policy measurement-validity positive controls；
- 可选的 discarded-state latent terminal audit；
- 一致的派生数据、证据图、发布清单和标准 arXiv 包；
- 17.7 GB G0 原始数据的持久公开归档与完整作者信息。

建议标题仅在 world-fork certificate 通过后升级为：

> **Programmable Chemical Worlds Make Experimental Agency Measurable**

在此之前保留：

> **Executable Chemical Worlds Make Experimental Agency Measurable**

## 2. 认领与状态规则

- 每项任务只能勾选一个认领状态和一个执行状态。
- 认领后填写负责人；多人协作时指定一名最终负责人。
- `阻塞` 必须在备注中写明外部依赖或失败证据。
- `完成` 以验收标准全部满足为准，而不是以代码已提交或实验已启动为准。
- 正式实验协议冻结后不得根据结果修改 world、seed、阈值、指标或停止规则。

### 工作流负责人

- [ ] 总负责人已认领；负责人：`TBD`
- [ ] 实验设计负责人已认领；负责人：`TBD`
- [ ] 代码与审计负责人已认领；负责人：`TBD`
- [ ] 论文与图表负责人已认领；负责人：`TBD`
- [ ] 数据归档与发布负责人已认领；负责人：`TBD`

## 3. 已冻结的完成基线

以下项目不再作为待执行任务重复运行：

- [x] G0：29,580 次非重复正式执行；
- [x] Codex G2 v0.4：60 final assays、815 primitive operations；
- [x] DeepSeek G2：60 closed lifecycles，其中 24 assays、36 discards；
- [x] G2 fresh v0.5：114 executed vessels、112 final assays、8 complete pairs、2 right-censored pairs；
- [x] 55/55 evidence nodes、1,854 tests passed、clean wheel 与 independent checkout attestation；
- [x] 停止 16-world v0.6 扩张，不将其纳入第一篇估计量。

权威账本：[`reports/experimental-intelligence-experiment-ledger-v0.1.json`](reports/experimental-intelligence-experiment-ledger-v0.1.json)。

## 4. 任务总览

| ID | 优先级 | 任务 | 当前状态 | 关键依赖 |
| --- | --- | --- | --- | --- |
| W1-01 | P0 | 证据产物与脏工作区对齐 | 未开始 | 无 |
| W1-02 | P0 | 封存 scope-stopped v0.6 | 未开始 | W1-01 |
| W1-03 | P0 | 冻结 world-fork 证书协议 | 未开始 | W1-01 |
| W1-04 | P0 | 实现并验证 world-fork certificate | 未开始 | W1-03 |
| W1-05 | P0 | 冻结 known-policy positive controls | 未开始 | W1-01 |
| W1-06 | P0 | 实现 policy runner 与构念效度审计 | 未开始 | W1-05 |
| W1-07 | P0 | 执行新增的无 LLM 矩阵 | 未开始 | W1-04、W1-06 |
| W1-08 | P1 | discarded-state latent terminal audit | 未开始，可选增强 | W1-01 |
| W1-09 | P0 | 修订论文结构、术语和主张 | 未开始 | W1-03、W1-05 |
| W1-10 | P0 | 重构六幅主图与派生数据 | 未开始 | W1-07、W1-09 |
| W1-11 | P0 | 全量证据重建和发布验证 | 未开始 | W1-10 |
| W1-12 | P0 | 外部数据归档与作者元数据 | 阻塞 | 外部 DOI、作者输入 |
| W1-13 | P0 | 最终 arXiv 包与投稿冻结 | 未开始 | W1-11、W1-12 |

## 5. 详细任务卡

### W1-01 — 证据产物与脏工作区对齐

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 目标：消除两份未提交生成报告与当前可执行代码之间的假冲突。
- 操作范围：
  - `workstreams/benchmark_v1/reports/runtime-domain-affordance-audit-v0.4.json`；
  - `workstreams/world_foundation/reports/public-boundary-security-vnext.json`。
- 验收标准：
  - [ ] 保留或归档现有未提交内容，不静默覆盖用户证据；
  - [ ] 当前固定协议重新得到 12/12 semantic-invariance pairs；
  - [ ] public-boundary 35/35 probes 通过；
  - [ ] runtime-domain 237 candidates、235 committed、0 findings；
  - [ ] tracked report、`configs/current.json` 与 evidence DAG 指向同一版本；
  - [ ] 工作区无无法解释的生成产物漂移。
- 备注：`TBD`

### W1-02 — 封存 scope-stopped v0.6

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 目标：明确 16-world 扩张不是活跃实验，也不进入第一篇结果。
- 验收标准：
  - [ ] 保留 `OWNER_STOP.json`、启动 receipt 和全部已产生轨迹；
  - [ ] 将父级状态明确为 `owner_stopped_excluded` 或等价终态；
  - [ ] 记录 7 completed cells、1 right-censored cell、152 pending cells；
  - [ ] 禁止自动 resume、pool、replacement 或 confirmatory promotion；
  - [ ] 论文与发布清单只将其描述为 supplementary execution record。
- 备注：`TBD`

### W1-03 — 冻结 world-fork certificate 协议

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 目标：把“programmable worlds”从架构声明转化为预声明的组件级验证。
- 冻结矩阵：
  - 2 类 intervention：mechanism/constitutive-law fork 与 material-law counterfactual fork；
  - 3 个 seeds；
  - base/fork 两侧；
  - 每侧一次执行和一次 exact replay；
  - 共 24 条确定性执行轨迹，0 provider calls。
- 验收标准：
  - [ ] 冻结任务、seed、动作序列、预期分叉读数与容差；
  - [ ] public action、instrument、resource、scoring contract 保持相同；
  - [ ] hidden world identity 或 intervention identity 确实不同；
  - [ ] public payload 不泄露 hidden intervention；
  - [ ] 协议声明该证书不是 agent-performance 实验。
- 备注：`TBD`

### W1-04 — 实现并验证 world-fork certificate

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 依赖：W1-03
- 代码交付物：
  - [ ] certificate builder/runner；
  - [ ] machine-readable JSON report；
  - [ ] human-readable Markdown summary；
  - [ ] fail-closed unit/integration tests；
  - [ ] evidence-pipeline node 与发布清单绑定。
- 验收标准：
  - [ ] 24/24 轨迹执行成功；
  - [ ] base/fork 同一动作序列均合法；
  - [ ] 预声明的机制相关响应发生预期分叉；
  - [ ] 24/24 exact replay；
  - [ ] 相同 public contract 与不同 hidden identity 均由哈希证明。
- 备注：`TBD`

### W1-05 — 冻结 known-policy positive controls

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 目标：验证 ChemWorld profile 能稳定恢复已知实验政策。
- 冻结政策：
  - `assay_all`；
  - `start_then_discard`；
  - `measure_then_threshold`。
- 冻结矩阵：5 worlds × 2 information arms × 3 policies × 6 vessels，共 30 campaigns、180 lifecycles、0 provider calls。
- 验收标准：
  - [ ] 阈值在正式运行前冻结，并使用独立 qualification worlds 校验；
  - [ ] 冻结预期 assay/discard fraction、instrument-use ordering 和 resource-use ordering；
  - [ ] 明确 positive controls 只验证 measurement construct，不参与模型排名；
  - [ ] 定义 test-retest/exact-replay 判据和失败处理。
- 备注：`TBD`

### W1-06 — 实现 policy runner 与构念效度审计

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 依赖：W1-05
- 代码交付物：
  - [ ] 三种确定性 policy implementations；
  - [ ] matrix runner 与 immutable manifest；
  - [ ] policy-profile recovery audit；
  - [ ] resource-ledger 与 exact-replay audit；
  - [ ] fail-closed tests 与 publication report generator。
- 验收标准：
  - [ ] `assay_all` 恢复 100% assay commitment；
  - [ ] `start_then_discard` 恢复 100% explicit discard；
  - [ ] `measure_then_threshold` 恢复预声明的测量后条件分流；
  - [ ] 三类 profile 在 evidence acquisition、continued investment、assay/discard 和 resource use 上可区分；
  - [ ] 无自动 repair、自动 final assay 或隐藏 policy override。
- 备注：`TBD`

### W1-07 — 执行新增的无 LLM 矩阵

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 依赖：W1-04、W1-06
- 执行量：24 world-fork traces + 180 policy-control lifecycles。
- 验收标准：
  - [ ] 从干净提交运行；
  - [ ] 所有协议、代码、输入、输出和环境身份有 SHA-256 绑定；
  - [ ] 所有矩阵单元达到预声明终态；
  - [ ] 所有 exact replay 与 resource replay 通过；
  - [ ] 失败或删失按冻结规则保留，不事后替换。
- 备注：`TBD`

### W1-08 — discarded-state latent terminal audit（可选增强）

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P1
- 目标：判断 DeepSeek 的 36 次 discard 是否选择性关闭了低潜在价值状态。
- 设计：重放到 discard 前状态，仅将 terminal discard 替换为 final assay；不新增 agent action 或 provider call。
- 验收标准：
  - [ ] 36/36 pre-discard states 可唯一重建；
  - [ ] shadow branch 与原轨迹在分叉前逐步同一；
  - [ ] 预先定义 latent score、false-discard、discard regret 和 commitment precision；
  - [ ] 连续 latent-score 分析为主，阈值分类只作敏感性分析；
  - [ ] 不宣称节省了稀缺 assay quota，因为当前 6 assays/6 vessels 不构成绑定约束。
- 备注：是否进入主文须在读取 shadow scores 前冻结：`TBD`

### W1-09 — 修订论文结构、术语和主张

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 验收标准：
  - [ ] 按首次引用顺序重排 Figures 1–6；
  - [ ] 将 `independently configured` 改为 `distinct complete agent systems` 或等价表述；
  - [ ] 首次出现 120 closed lifecycles 时明确 84 assays + 36 discards；
  - [ ] 删除 Methods 10.7 中“6/8 是 primary conclusion”的残留；
  - [ ] raw-terminal 2/8 discordance 为 endpoint diagnostic；
  - [ ] 6/8 mixed 明确为 threshold-sensitive supporting analysis；
  - [ ] model、scaffold、transport 的完整系统边界全文一致；
  - [ ] programmability 在摘要、引言、结果和讨论中由 W1-04 证据直接支撑。
- 备注：`TBD`

### W1-10 — 重构六幅主图与派生数据

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 推荐主图结构：
  1. apparatus + programmable world fork；
  2. known-policy measurement validity；
  3. same completion, different terminal policy；
  4. compiled information controls；
  5. autonomous lifecycle and process profile；
  6. fresh-session trajectory variation。
- 验收标准：
  - [ ] 所有定量图只从冻结 derived-data JSON 生成；
  - [ ] SVG 保留可编辑文字与矢量元素；
  - [ ] PDF 字体嵌入、线宽、字号、色盲可读性和双栏尺寸通过；
  - [ ] figure order、caption、正文首次引用和 display-item 清单一致；
  - [ ] 不在主图中以单一总分重新压缩 experimental agency。
- 备注：`TBD`

### W1-11 — 全量证据重建和发布验证

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 验收标准：
  - [ ] evidence DAG 全节点通过且无 stale binding；
  - [ ] full pytest suite 0 failures；
  - [ ] clean non-editable wheel smoke 通过；
  - [ ] independent checkout 零差异重建；
  - [ ] final numeric/citation/statistical-language/claim audit 通过；
  - [ ] G0、G2、positive controls、world fork 和可选 shadow audit 的计数单位互不混用；
  - [ ] release manifest、experiment ledger、derived data 和论文数字一致。
- 备注：`TBD`

### W1-12 — 外部数据归档与作者元数据

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [ ] 未开始
  - [ ] 进行中
  - [x] 阻塞
  - [ ] 完成
- 优先级：P0
- 外部依赖：持久公开归档服务、作者与单位信息。
- 验收标准：
  - [ ] 1,441 个 G0 raw files、17,725,724,603 bytes 与冻结索引完全匹配；
  - [ ] 公开 HTTPS archive URL 可在未登录环境访问；
  - [ ] DOI/identifier、provider、byte count 和 raw-index SHA-256 写入 metadata；
  - [ ] 至少一名作者、完整 affiliations、且恰好一名 corresponding author；
  - [ ] ORCID、邮箱与作者顺序由项目负责人确认。
- 阻塞说明：等待外部归档标识和作者输入。

### W1-13 — 最终 arXiv 包与投稿冻结

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 依赖：W1-11、W1-12
- 验收标准：
  - [ ] `publication_ready=true`；
  - [ ] PDF、ZIP、TAR.GZ 各自两次无 shell escape 编译通过；
  - [ ] ZIP/TAR 成员内容逐字节一致；
  - [ ] 无 unresolved citation/reference/font；
  - [ ] arXiv 上传后下载核验 PDF、source 和 supplementary links；
  - [ ] 创建不可变 release tag 与最终提交记录。
- 备注：`TBD`

## 6. 完成定义

Work I 只有在以下条件全部满足时才标记完成：

- [ ] world programmability 有发布级实证证书；
- [ ] experimental-agency profile 通过已知策略正控制；
- [ ] 当前最强结果仍是“相同 completion 下的不同实验政策”；
- [ ] 第一篇不消费 Work II 的规律学习主结果；
- [ ] 科学矩阵、代码、论文、图表、数据和发布清单完全一致；
- [ ] 外部数据归档与作者信息已经写入最终包；
- [ ] arXiv 包可公开下载和独立重建。
