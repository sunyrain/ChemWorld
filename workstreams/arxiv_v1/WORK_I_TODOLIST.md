# Work I Master TODO — Programmable Chemical Worlds

版本：1.1

最后更新：2026-08-03

状态：`ACTIVE / CLAIM-DRIVEN / PARALLEL-READY`

本文件是第一篇论文的唯一主控 TODO。它负责协调代码、实验、论文、图表、证据和发布；历史计划只作为背景，不覆盖本文件的任务边界、认领状态和完成定义。

## 0. 第一篇的最终目标

中心命题：

> **Programmable chemical worlds make experimental agency measurable.**

第一篇要完整证明一条装置论文的证据链：

1. ChemWorld 把实验定义为可执行的状态、操作、仪器、资源、失败和评价契约；
2. 世界组件可以被受控分叉，同时保持公开实验接口不变；
3. 行为测量能够恢复预先已知的实验政策，具有构念效度；
4. 真实 complete agent systems 可以逐操作完成实验生命周期；
5. 相同 completion 或相近 endpoint 可以掩盖不同的证据获取、继续投资、assay、discard、发现、保持和恢复政策；
6. 所有结论都能从冻结轨迹、资源账本、世界身份和 exact replay 独立重建。

标题只有在 world-fork certificate 与 known-policy controls 均通过后才升级为：

> **Programmable Chemical Worlds Make Experimental Agency Measurable**

在此之前保留：

> **Executable Chemical Worlds Make Experimental Agency Measurable**

### 第一篇明确包含

- executable-world apparatus；
- world component contract 与 fork lineage；
- public/private boundary；
- typed primitive experimentation；
- campaign-wide resource accounting；
- exact replay 与证据图；
- G0 compiled information controls；
- Codex 与 DeepSeek complete-system policy profiles；
- fresh-session process profiles；
- world-fork programmability validation；
- known-policy measurement-validity controls；
- discarded-state latent terminal audit；
- 标准论文、数据和软件发布包。

### 第一篇明确不包含

- “LLM 优于 BO”或统一排行榜；
- model-only backend 因果效应；
- 大规模规律冲突、belief revision 或 mechanism adaptation；
- 真实实验室迁移或机器人操作能力；
- 任意第三方世界 DSL 的完全通用性；
- 以更多随机 LLM world 扩张替代测量效度；
- 将历史 Gate A 写成当前 agent 规律学习结果。

这些问题分别归入 Work II、system-ablation work 和 physical-bridge work。

## 1. 已冻结完成基线

以下结果已经完成并保留，不得为了制造新叙事重复选择或覆盖：

- [x] 15 个注册任务设计；
- [x] 28 类操作、5 类仪器；
- [x] 415 个 deterministic complete-experiment boundary cases；
- [x] 62/62 declared endpoints 已绑定 evaluator；
- [x] G0：29,580 次非重复正式物理执行；
- [x] Codex G2 v0.4：60 final assays、815 accepted primitive operations；
- [x] DeepSeek G2：60 closed lifecycles，其中 24 assays、36 discards、889 operations；
- [x] G2 fresh v0.5：114 executed vessels、112 final assays、8 complete pairs、2 right-censored pairs；
- [x] 双系统 10/10 matched physical cells；
- [x] 55/55 evidence nodes；
- [x] 1,854 tests passed、3 skipped、0 failed；
- [x] clean wheel、independent checkout 和 final claim audit 通过；
- [x] 16-world v0.6 已由 owner 按范围决策停止，不进入第一篇估计量。

权威入口：

- `reports/experimental-intelligence-experiment-ledger-v0.1.json`
- `../../benchmark/releases/chemworld-serious-v1/manifest.json`
- `../../benchmark/releases/chemworld-serious-v1/verification-attestation.json`
- `../../paper/arxiv/main.tex`

## 2. 认领制度

### 2.1 基本原则

- 所有任务必须先声明认领，再开始写代码或改稿。
- 每个任务同一时刻只能有一个 accountable owner。
- owner 可以列 collaborators，但最终验收、冲突处理和交接由 owner 负责。
- 默认一个任务对应一个 branch、一个独立 worktree 和一个声明文件。
- 不允许两个任务同时修改同一个共享热文件。
- 未认领任务可以自由阅读、设计和评论，但不能产生准备合并的实现改动。
- formal protocol 冻结后不得根据结果修改 world、seed、阈值、estimand、停止规则或主图进入规则。

### 2.2 声明文件

认领者应从 `claims/TEMPLATE.md` 创建：

`claims/<TASK-ID>--<owner>.md`

声明至少包含：

- task ID；
- owner 与 collaborators；
- UTC claim time；
- lease expiry；
- base commit；
- branch/worktree；
- declared write set；
- shared hot-file requests；
- deliverables；
- validation commands；
- expected handoff date。

只有 coordinator 可以修改本文件的总状态表。执行者通过独立 claim 文件更新进度，避免多人同时编辑主 TODO。

### 2.3 租约、心跳与接管

- 默认认领租约：48 小时；
- active task 至少每 24 小时更新一次 claim heartbeat；
- `BLOCKED` 必须记录证据、解除条件、责任方和下一检查时间；
- 租约过期且 24 小时无心跳，coordinator 可以声明释放；
- 接管必须创建新 claim 文件并引用原 claim，不覆盖原记录；
- 同一 task 出现竞争认领时，以最早进入 `main` 的 claim commit 为准。

### 2.4 状态枚举

- `OPEN`：无人认领；
- `CLAIMED`：已声明，尚未产生实现；
- `ACTIVE`：正在实现；
- `BLOCKED`：无法继续，已记录解除条件；
- `REVIEW`：交付物完成，等待独立验收；
- `CHANGES_REQUESTED`：验收未通过；
- `DONE`：全部验收标准通过且已合并；
- `RELEASED`：已进入最终论文/数据/软件发布包；
- `CANCELLED`：由 coordinator 记录范围决策，不得静默删除。

### 2.5 Branch 与 worktree 约定

- branch：`work1/<task-id>-<short-slug>`；
- worktree：仓库同级的 `ChemWorld-<task-id>`；
- commit：以 task ID 开头，例如 `W1-F04 add world-fork certificate runner`；
- 每个 PR/合并提交只覆盖一个主 task；
- 不得把 `runs/` 原始输出和源代码实现混在同一提交；
- 不得在 worker branch 上重写或重新生成全局 evidence DAG。

### 2.6 完成与合并

任务进入 `DONE` 必须同时满足：

- 交付物存在；
- task-local tests 通过；
- `git diff --check` 通过；
- 没有越过 declared write set；
- 没有覆盖冻结协议或历史证据；
- 有独立 reviewer 或 coordinator 验收；
- claim 文件记录最终 commit、测试和 handoff；
- 如产生数据，已生成 immutable manifest、hash 和 counting rule。

## 3. 并行工作拓扑

### 3.1 Track 划分

| Track | 目标 | 可立即开始 | 独占写入区 | 最终依赖 |
| --- | --- | --- | --- | --- |
| M — Coordination | scope、认领、集成与冻结 | 是 | 本 TODO、claims、integration notes | 无 |
| F — Foundation & worlds | 世界组件、fork、身份、公开边界 | 是 | foundation/world 新模块及 F 前缀配置/测试 | M02 |
| V — Measurement validity | 已知策略正控与 profile recovery | 是 | known-policy 新模块及 V 前缀配置/测试 | M02 |
| L — Latent terminal audit | 36 个 discard 的 shadow evaluation | 是 | latent-terminal 新模块及 L 前缀配置/测试 | M02 |
| S — Story & manuscript | claim map、结构、正文和术语 | 是 | manuscript source、story notes | M02；最终数字等 D03 |
| P — Figures & visual system | 六幅主图、SVG、版式 | 是，可先做布局 | figure source 与 P 前缀脚本 | 最终数据等 D03 |
| D — Data, evidence & release | 数据索引、derived data、DAG、arXiv | 是 | release staging 与 D 前缀工具 | 各 track 交付 |
| Q — Independent review | 方法、系统、化学、编辑审稿 | 是，可先建 rubric | review reports | 对应版本 |

### 3.2 最小硬依赖

只保留以下不可消除的硬依赖：

1. formal execution 必须晚于 protocol freeze 与 runner qualification；
2. final quantitative figures 必须晚于 frozen derived data；
3. evidence DAG integration 必须晚于各 track 的 immutable reports；
4. final arXiv release 必须晚于全文、图表、数据归档和作者元数据；
5. 任何使用 outcome 的主文进入规则必须在读取相应 outcome 前冻结。

其余任务应并行推进：

- F、V、L 可同时设计和实现；
- S 可基于现有结果先完成 80% 结构和文本；
- P 可先冻结设计系统、panel geometry 和占位数据接口；
- D 可并行推进 17.7 GB 归档、schema 和 release tooling；
- Q 可在 protocol、implementation、paper 三个阶段分别审查。

### 3.3 建议并发配置

资源充足时建议 8 个 accountable owners：

1. coordinator/integration；
2. foundation/world；
3. policy validity；
4. latent audit；
5. manuscript；
6. figures；
7. evidence/release；
8. independent QA。

额外人员优先作为 task reviewer，不再拆分共享热文件。

## 4. 共享热文件与写集隔离

以下文件由 M/D integration owner 独占。其他 track 只能提交 patch proposal 或生成独立输入，不得直接修改：

- `../../configs/current.json`
- `../../scripts/evidence_pipeline.py`
- `reports/experimental-intelligence-experiment-ledger-v0.1.json`
- `../../benchmark/releases/chemworld-serious-v1/manifest.json`
- `../../benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.json`
- `../../paper/arxiv/main.tex`
- `../../paper/arxiv/figure-manifest.json`
- `../../paper/exports/experimental-intelligence-v1-arxiv/`

Track 默认写集：

| Track | 默认可写路径 |
| --- | --- |
| F | `src/chemworld/foundation/*world_fork*`、`src/chemworld/eval/*world_fork*`、`scripts/*world_fork*`、`configs/benchmark/work_i_world_fork*`、`tests/test_*world_fork*`、本 track reports |
| V | `src/chemworld/agents/known_policy*`、`src/chemworld/eval/*policy_validity*`、`scripts/*policy_control*`、`configs/benchmark/work_i_policy*`、`tests/test_*policy*`、本 track reports |
| L | `src/chemworld/eval/*latent_terminal*`、`scripts/*latent_terminal*`、`configs/benchmark/work_i_latent*`、`tests/test_*latent_terminal*`、本 track reports |
| S | `../../paper/experimental_intelligence_v1_manuscript.md`、`../../paper/experimental_intelligence_v1_display_items.md`、story/claim notes |
| P | `../../paper/figures/experimental-intelligence-v1/`、figure-specific render helpers；不直接改主文 |
| D | `../../benchmark/releases/chemworld-serious-v1/` 的集成输出、release tools、archive metadata |
| Q | `reviews/`；只读其他路径 |

如必须修改既有核心文件，claim 中必须逐项列出，并由 coordinator 先授予 hot-file reservation。

## 5. 总任务矩阵

### 5.1 Coordination

| ID | P | 状态 | 任务 | 硬依赖 | 可并行 |
| --- | --- | --- | --- | --- | --- |
| W1-M01 | P0 | DONE | 建立 claims 目录、模板和 coordinator 规则 | 无 | 是 |
| W1-M02 | P0 | DONE | 冻结 Work I scope、claim hierarchy 与非目标 | 无 | 是 |
| W1-M03 | P0 | OPEN | 对齐两份历史生成报告与当前 evidence binding | 无 | 是 |
| W1-M04 | P0 | OPEN | 封存 v0.6 scope-stopped extension | 无 | 是 |
| W1-M05 | P0 | OPEN | 建立 integration staging 与 hot-file queue | M01 | 是 |
| W1-M06 | P0 | OPEN | 最终跨 track 集成与 release freeze | F/V/L/S/P/D 完成 | 否 |

M01 与 M02 由本主计划及 `claims/` 的初次发布完成；后续只有通过可审计的 scope-change 记录才能重新打开。

### 5.2 Foundation & programmable worlds

| ID | P | 状态 | 任务 | 硬依赖 | 可并行 |
| --- | --- | --- | --- | --- | --- |
| W1-F01 | P0 | DONE | 冻结 world component inventory 与 manifest schema | M02 | 是 |
| W1-F02 | P0 | DONE | 定义 WorldForkSpec、parent/child lineage 和 component diff | M02 | 是 |
| W1-F03 | P0 | DONE | 定义 public-contract invariance certificate | M02 | 是 |
| W1-F04 | P0 | DONE | 定义预期物理/观测 divergence oracle | M02 | 是 |
| W1-F05 | P0 | DONE | 实现 world-fork builder、runner 与 audit | F01–F04 freeze | 是 |
| W1-F06 | P0 | DONE | 执行并冻结 24 条 world-fork qualification traces | F05 | 否 |
| W1-F07 | P0 | DONE | 将 fork certificate 写入 machine/human reports | F06 | 是 |
| W1-F08 | P1 | OPEN | 完善 world-authoring contract、示例和 validator 文档 | F01 | 是 |
| W1-F09 | P0 | DONE | 审计 15 tasks/28 operations/5 instruments/62 endpoints 的展示口径 | M02 | 是 |
| W1-F10 | P0 | DONE | 完成 transaction、resource、failure、instrument semantics 总资格表 | F01 | 是 |

### 5.3 Measurement-validity positive controls

| ID | P | 状态 | 任务 | 硬依赖 | 可并行 |
| --- | --- | --- | --- | --- | --- |
| W1-V01 | P0 | DONE | 冻结 experimental-agency construct 与 profile schema | M02 | 是 |
| W1-V02 | P0 | OPEN | 冻结三种 known policies 和预期 profile ordering | M02 | 是 |
| W1-V03 | P0 | OPEN | 在独立 qualification worlds 冻结 threshold | V02 | 是 |
| W1-V04 | P0 | OPEN | 实现 deterministic policy implementations | V02 draft | 是 |
| W1-V05 | P0 | OPEN | 实现 5×2×3 matrix runner、manifest 与 resume policy | V02 draft | 是 |
| W1-V06 | P0 | OPEN | 实现 construct-validity、resource 与 exact-replay audit | V01 draft | 是 |
| W1-V07 | P0 | OPEN | runner qualification 与 protocol freeze | V03–V06 | 否 |
| W1-V08 | P0 | OPEN | 执行 30 campaigns / 180 lifecycles | V07 | 否 |
| W1-V09 | P0 | OPEN | 输出 profile recovery、discriminant validity 与 test–retest report | V08 | 是 |

### 5.4 Latent terminal policy audit

| ID | P | 状态 | 任务 | 硬依赖 | 可并行 |
| --- | --- | --- | --- | --- | --- |
| W1-L01 | P0 | OPEN | 冻结 shadow-state estimands 与主文进入规则 | M02 | 是 |
| W1-L02 | P0 | OPEN | 审计 36 个 discard 的 pre-discard state 可重建性 | 无 | 是 |
| W1-L03 | P0 | OPEN | 实现 prefix-identity replay 与 terminal branch replacement | L01 draft | 是 |
| W1-L04 | P0 | OPEN | 实现 latent-score、regret、false-discard 与 commitment audit | L01 draft | 是 |
| W1-L05 | P0 | OPEN | qualification、protocol freeze 与 36 shadow assays | L02–L04 | 否 |
| W1-L06 | P0 | OPEN | 输出连续主分析和阈值敏感性报告 | L05 | 是 |

### 5.5 Story & manuscript

| ID | P | 状态 | 任务 | 硬依赖 | 可并行 |
| --- | --- | --- | --- | --- | --- |
| W1-S01 | P0 | OPEN | 建立逐主张 claim–evidence–figure map | M02 | 是 |
| W1-S02 | P0 | OPEN | 冻结发布会式故事结构与章节职责 | M02 | 是 |
| W1-S03 | P0 | OPEN | 重写 title/abstract/introduction 的占位版本 | S01 draft | 是 |
| W1-S04 | P0 | OPEN | 重写 platform/world programmability Results 与 Methods | F protocol | 是 |
| W1-S05 | P0 | OPEN | 重写 measurement-validity Results 与 Methods | V protocol | 是 |
| W1-S06 | P0 | OPEN | 重写 complete-system policy 与 latent audit 结果结构 | L protocol | 是 |
| W1-S07 | P0 | OPEN | 修正 figure first-reference、120 closure、6/8 和术语残留 | 无 | 是 |
| W1-S08 | P0 | OPEN | 重构 related work：SDL 互补、agent evaluation、virtual worlds | M02 | 是 |
| W1-S09 | P0 | OPEN | 完成 limitations/boundaries，不扩大第一篇责任 | S01 | 是 |
| W1-S10 | P0 | OPEN | 读取冻结结果后完成最终 title/abstract/results/conclusion | F/V/L reports | 否 |

### 5.6 Figures & visual system

| ID | P | 状态 | 任务 | 硬依赖 | 可并行 |
| --- | --- | --- | --- | --- | --- |
| W1-P01 | P0 | OPEN | 冻结六图信息架构、字体、配色、线宽和 panel grid | S02 | 是 |
| W1-P02 | P0 | OPEN | Fig. 1 apparatus + programmable world fork | F protocol | 是 |
| W1-P03 | P0 | OPEN | Fig. 2 known-policy measurement validity | V protocol | 是 |
| W1-P04 | P0 | OPEN | Fig. 3 same completion, different terminal policy | 现有数据；L 可后补 | 是 |
| W1-P05 | P0 | OPEN | Fig. 4 compiled information controls | 现有数据 | 是 |
| W1-P06 | P0 | OPEN | Fig. 5 autonomous lifecycle/process profile | 现有数据 | 是 |
| W1-P07 | P0 | OPEN | Fig. 6 fresh-session trajectory variation | 现有数据 | 是 |
| W1-P08 | P0 | OPEN | SVG editability、高清素材、PDF 字体与双栏尺寸审计 | P02–P07 | 否 |
| W1-P09 | P0 | OPEN | caption、正文引用、display items 与 manifest 一致性 | P08、S10 | 否 |

### 5.7 Data, evidence & release

| ID | P | 状态 | 任务 | 硬依赖 | 可并行 |
| --- | --- | --- | --- | --- | --- |
| W1-D01 | P0 | OPEN | 冻结新增实验的数据 schema、单位和 counting rules | M02 | 是 |
| W1-D02 | P0 | BLOCKED | 17.7 GB G0 raw roots 持久归档与公开 identifier | 外部服务 | 是 |
| W1-D03 | P0 | OPEN | 构建单一 frozen derived-data layer | F/V/L reports | 否 |
| W1-D04 | P0 | OPEN | 为 F/V/L 新增 evidence DAG nodes 与 source binding | reports ready | 是 |
| W1-D05 | P0 | OPEN | 更新 experiment ledger、release manifest 和 data card | D03–D04 | 否 |
| W1-D06 | P0 | BLOCKED | 作者、单位、corresponding author 与 ORCID metadata | 项目负责人 | 是 |
| W1-D07 | P0 | OPEN | 标准 arXiv PDF、ZIP、TAR.GZ 与 proof rebuild | S/P/D 完成 | 否 |
| W1-D08 | P0 | OPEN | full tests、clean wheel、independent checkout、claim audit | D07 | 否 |
| W1-D09 | P0 | OPEN | publication-ready finalizer、tag 与 upload verification | D02、D06、D08 | 否 |

### 5.8 Independent review & QA

| ID | P | 状态 | 任务 | 硬依赖 | 可并行 |
| --- | --- | --- | --- | --- | --- |
| W1-Q01 | P0 | OPEN | protocol reviewer：world fork、policy control、latent audit | draft protocols | 是 |
| W1-Q02 | P0 | OPEN | systems reviewer：security、identity、ledger、replay | implementations | 是 |
| W1-Q03 | P0 | OPEN | methods reviewer：construct validity、estimands、censoring | analysis drafts | 是 |
| W1-Q04 | P0 | OPEN | chemistry/chemical-engineering reviewer：世界与实验语义 | F/V reports | 是 |
| W1-Q05 | P0 | OPEN | editorial reviewer：故事、主图、scope、期刊适配 | paper draft | 是 |
| W1-Q06 | P0 | OPEN | 三位全新独立审稿人 blind review | integrated PDF | 否 |
| W1-Q07 | P0 | OPEN | review adjudication 与逐条 closure matrix | Q06 | 否 |

## 6. 三个新增实验包的冻结规格

### 6.1 World-fork programmability certificate

目标：证明“programmable”是执行事实，而不是讨论中的未来愿景。

建议正式矩阵：

- intervention classes：2；
  - mechanism/constitutive-law fork；
  - material-law counterfactual fork；
- seeds：3；
- variants：base + fork；
- executions：一次原始执行 + 一次 exact replay；
- 总量：24 deterministic traces；
- provider calls：0。

必须证明：

- parent 与 child 有可审计 lineage；
- 只允许预声明组件发生改变；
- public action schema 相同；
- public instrument interface 相同；
- resource/failure/scoring contract 相同；
- public payload 不泄露 fork identity；
- 同一动作序列在两侧均可执行；
- 预声明机制相关响应达到 divergence 容差；
- 每条轨迹 exact replay；
- 证书只证明 world programmability，不证明 agent performance。

### 6.2 Known-policy measurement-validity controls

目标：证明 profile 能恢复已知政策，建立 construct validity。

政策：

1. `assay_all`；
2. `start_then_discard`；
3. `measure_then_threshold`。

正式矩阵：

- 5 worlds；
- 2 information arms；
- 3 policies；
- 6 vessels/cell；
- 30 campaigns；
- 180 closed lifecycles；
- provider calls：0。

预期结构必须在运行前冻结：

- assay/discard fraction；
- evidence-acquisition ordering；
- continued-investment ordering；
- instrument-use ordering；
- operation/resource-use ordering；
- threshold policy 的条件分流；
- exact replay/test–retest 判据。

`measure_then_threshold` 的阈值必须只使用独立 qualification worlds，不能从正式 5 worlds 调参。

### 6.3 Discarded-state latent terminal audit

目标：将 36 次 discard 从醒目的行为计数升级为终端选择质量分析。

设计：

- 重放到原 discard 前的唯一状态；
- 保持全部 prefix actions、observations、noise 和资源完全相同；
- 只将 terminal discard 替换为 final assay；
- 不调用 agent/provider；
- 36 evaluator-only shadow assays。

主要输出：

- continuous latent terminal score；
- latent-score distribution by arm/cell；
- discard regret；
- false-discard rate；
- assay commitment precision；
- nominal information 与 terminal selection 的描述性关系；
- threshold/censoring sensitivity。

禁止主张：

- 当前任务中 assay quota 稀缺；
- discard 已证明节省现实实验成本；
- shadow branch 是 agent 实际选择；
- 基于 10 cells 得到一般模型排名。

主文或补充材料的进入规则必须在读取 shadow scores 前冻结；无论结果如何，完整报告都必须发布。

## 7. 论文与六幅主图的最终结构

### 7.1 章节职责

1. Introduction：为什么 experimental agency 需要可控测量装置；
2. Apparatus：世界、操作、仪器、资源、失败、身份和 replay；
3. Programmability validation：base world 到 single-component fork；
4. Measurement validity：known policies 能否被稳定恢复；
5. Compiled controls：endpoint 压缩了哪些认知信息；
6. Autonomous systems：complete-system policies 与 assay/discard；
7. Process profiles：发现、保持、回撤、恢复与 fresh trajectories；
8. Discussion：与真实 SDL 互补，以及 Work II 的规律适应边界。

### 7.2 六幅主图

1. **ChemWorld apparatus and controlled world forks**
2. **Known policies validate the experimental-agency profile**
3. **Lifecycle completion does not specify terminal policy**
4. **Compiled controls separate outcome, prediction, calibration and claims**
5. **Primitive-control agents expose complete experimental lifecycles**
6. **Fresh trajectories reveal process structure omitted by endpoints**

### 7.3 必修编辑修正

- `independently configured` 改为 `distinct complete agent systems` 或等价表述；
- 首次写 120 closed lifecycles 时明确 84 assays + 36 discards；
- 图按首次引用顺序编号；
- 2/8 best/raw-terminal discordance 是 endpoint diagnostic；
- 6/8 mixed 是 threshold-sensitive supporting classification；
- 删除 Methods 10.7 中“6/8 是 primary conclusion”的残留；
- complete system、model、scaffold、transport 的边界全文一致；
- 不把 G0 写成 LLM vs BO 竞赛；
- 不把 15 个已注册任务写成 15 个正式 agent 结果；
- 不把 world-fork certificate 写成规律适应实验；
- 不把虚拟实验写成真实化学部署。

## 8. 推荐启动波次

### Wave 0：认领与冻结，目标 0–1 天

并行启动：

- M01–M05；
- F01–F04、F09–F10；
- V01–V03；
- L01–L02；
- S01–S03、S07–S09；
- P01；
- D01–D02、D06；
- Q01。

### Wave 1：实现与占位稿，目标 1–4 天

并行启动：

- F05；
- V04–V06；
- L03–L04；
- S04–S06；
- P02–P07；
- archive upload；
- Q02–Q04。

### Wave 2：资格验证与正式无 LLM 执行，目标 4–6 天

- F06–F07；
- V07–V09；
- L05–L06；
- task-local independent review。

### Wave 3：数据、主文和主图集成，目标 6–9 天

- D03–D05；
- S10；
- P08–P09；
- Q05；
- M06。

### Wave 4：发布与审稿，目标 9–12 天

- D07–D09；
- Q06–Q07；
- final claim audit；
- arXiv upload verification。

外部 archive 和作者 metadata 决定最终 `publication_ready` 日期，但不应阻塞内部代码、实验、论文和图表完成。

## 9. 每日协调模板

coordinator 每日只更新一次主状态表，并报告：

- 新认领；
- 24 小时无心跳的 claims；
- hot-file reservations；
- formal freeze decisions；
- completed deliverables；
- failed validations；
- blockers 与解除责任人；
- 下一集成窗口；
- 当前预计完成时间。

worker heartbeat 只更新自己的 claim 文件：

```text
status:
completed_since_last_heartbeat:
current_validation:
files_touched:
blocked_by:
next_24h:
handoff_eta:
```

## 10. 第一篇完成定义

Work I 只有在下列条件全部满足后才能标记 `RELEASED`：

- [ ] world component contract 与 fork lineage 已版本化；
- [ ] 24/24 world-fork traces 与 exact replay 通过；
- [ ] 180/180 known-policy lifecycles 达到冻结终态；
- [ ] measurement profile 恢复预声明的三类政策差异；
- [ ] 36/36 discard shadow audit 完成并完整发布；
- [ ] 原有 G0、Codex、DeepSeek 和 fresh-session 结果未被重复计算或选择性覆盖；
- [ ] 论文中心仍是 experimental-agency measurement apparatus；
- [ ] Work II 的规律学习结论没有被提前消费；
- [ ] 六幅主图、caption、正文和 derived data 完全一致；
- [ ] evidence DAG 无 stale binding；
- [ ] full tests 0 failures；
- [ ] clean wheel 与 independent checkout 通过；
- [ ] final numeric/citation/statistical-language/claim audit 通过；
- [ ] 17.7 GB G0 archive 公开可访问且 hash/byte count 匹配；
- [ ] 作者、单位和 corresponding metadata 完整；
- [ ] PDF、ZIP、TAR.GZ 可独立编译和逐成员验证；
- [ ] GitHub release/tag、arXiv upload 与下载核验完成。

如果只缺外部 archive 或作者 metadata，状态应为 `INTERNALLY_COMPLETE / EXTERNAL_RELEASE_BLOCKED`，不能回写为科学或代码未完成。
