# ChemWorld 仓库清理与收束 TODO

状态：**ACTIVE / DEVELOPMENT CLEANUP / RELEASE FREEZE NOT AUTHORIZED**
更新时间：**2026-08-12**
执行方式：**单 executor；优先在 `main` 集成；不创建 claim 文件、租约、review queue 或 per-task worktree**

当前清理执行者：**Codex `/root` — 清衡**
最近完成批次：**QH-08 / PACKAGE IMPORT-LAYER NON-REGRESSION GUARD — DONE**
当前批次：**HANDOFF / MAIN-PROCESS INTEGRATION**
当前批次状态：**READY**
当前 write set：`CONTRIBUTING.md`、`SECURITY.md`、`CHANGELOG.md`、`workstreams/README.md`、
`workstreams/repository_quality/CLEANUP_CLOSEOUT_TODOLIST.md`、
`workstreams/repository_quality/REPOSITORY_LARGE_FILE_INVENTORY.md`、
`workstreams/repository_quality/DOCUMENTATION_SURFACE_AUDIT.md`、
`workstreams/repository_quality/PACKAGE_RESEARCH_BOUNDARY_AUDIT.md`、
`workstreams/repository_quality/EVIDENCE_AUTHORITY_AUDIT.md`、
`workstreams/repository_quality/QUALITY_GATE_CI_DESIGN.md`。
QH-03A 已完成的代码 write set：
`src/chemworld/eval/work_ii_structural_candidate_qualification.py`、
`work_ii_catalyst_deactivation_q0.py`、`work_ii_observation_screen.py`、
`work_ii_runtime_semantics_impact.py`、`work_ii_runtime_semantics_impact_validation.py`、
`work_ii_development_analysis.py`、`work_ii_resource_calibration.py`、`work_ii_formal.py`、
`work_ii_cost.py`、`work_ii_report.py`、`work_ii_formal_evaluators.py`、`work_ii_confirmatory.py`、
`work_ii_private.py`、`work_ii_private_execution.py`，以及这些模块已有的定向测试（仅在行为回归测试确有
缺口时修改）。
QH-03B 新增 write set：`work_ii_execution_mode.py`、`work_ii_c2_admission.py`、
`work_ii_ae_prior_qualification.py`、`work_ii_ae_prior_qualification_v02.py`，以及这些模块已有的定向测试
（仅在行为回归测试确有缺口时修改）。这些路径已由主进程提交至 `ed07969b`，共享工作区连续检查保持稳定，
因此进入最后一批静态类型收束。明确排除：其他 `scripts/`、`configs/`、
`pyproject.toml`、`uv.lock`、Work I/II 稿件、实验 note、报告、生成证据和 release artifact。主进程看到
`清衡` 或 `QH-03B` 即可识别本支线修改。

QH-04 write set：`scripts/check_tracked_secrets.py`、`tests/test_tracked_secret_guard.py` 和本清单；只检查
Git 已跟踪工作树与 index，不读取、不打印或枚举未跟踪/ignored 本地凭据内容。主进程看到 `清衡` 或
`QH-04` 即可识别本支线修改。

QH-05 已完成 write set：`scripts/check_package_research_boundary.py`、
`tests/test_package_research_boundary_guard.py`、`PACKAGE_RESEARCH_BOUNDARY_AUDIT.md` 和本清单；只把
当前 26 个已审计路径固化为 non-regression baseline，新增包→仓库研究路径依赖时 fail closed，不迁移现有
消费者、不修改 package/runtime/evidence 行为。

QH-06 write set：`README.md`、`DEVELOPMENT.md`、`CONTRIBUTING.md` 和本清单；只统一 public editable
install 与 locked contributor execution 的适用场景及命令，不修改依赖、lockfile、测试 marker 或代码。

QH-08 write set：`scripts/check_package_import_boundaries.py`、
`tests/test_package_import_boundary_guard.py`、机器基线、`PACKAGE_RESEARCH_BOUNDARY_AUDIT.md` 和本清单；
只阻止 foundation/physchem/world/runtime/envs/data 新增向上层 orchestration 包的 import，现有例外精确
基线化，不移动模块、不重写 import、不修改运行时行为。

QH-01 完成记录：新增贡献指南、安全策略和从下一版本开始维护的 changelog；完成 5 MiB 阈值大文件
清单及根目录 poster 诊断；确认文档表面为 `24` 个主导航页面、`34` 个 reference-only 页面、`0`
个未分类中文公共页面。`tests/test_public_docs.py` 为 `4/4` 通过，MkDocs strict build 通过，根目录
Markdown 本地链接检查和 `git diff --check` 通过。未移动或删除任何文件，未触碰受保护执行面。

QH-03A 完成记录：将全仓 mypy 从 `67 errors / 18 files` 收束到 `12 errors / 4 files`，本批允许的
14 个 Work II 模块均为零错误；四组定向测试分别为 `36/36`、`17/17`、`36/36`、`10/10`，合计
`99/99` 通过；全仓 Ruff 和 `git diff --check` 通过。修改仅做显式类型收窄、容器注解和变量去重，
没有改变实验问题、分母、阈值、停止规则、canonical hash 或 evidence lifecycle。

QH-03B 完成记录：消除最后 `12 errors / 4 files`，全仓 mypy 为 `378 source files / 0 errors`；
execution-mode/C2 admission 定向测试 `14/14`、A-E v0.1/v0.2 定向测试 `19/19` 通过。QH-03A/B
合计定向回归 `132/132` 通过；最终全仓 Ruff 和 `git diff --check` 通过。

QH-04 完成记录：新增 `scripts/check_tracked_secrets.py`，只通过 Git 管理面检查已跟踪/index 中的禁止
路径和高置信凭据指纹，输出仅含路径与指纹类别；不会读取、枚举或打印未跟踪/ignored 本地凭据内容。
守卫自身 `4/4` 测试、Ruff、Mypy 和当前仓库实跑均通过；当前 tracked path 未发现 `api.md`、
`key2.md`、`.env`、`runs/`、cache 或 generated site 越界。

QH-05 完成记录：新增 AST 精确扫描、26 模块机器基线和 5 个守卫测试；当前 package→repository-only
路径依赖无法继续增长，已迁移掉的条目会被报告为可删除。守卫同时纠正 QH-02 的一个文本扫描假阳性：
CLI 没有 `paper/` 路径字面量；并补获两个以根目录字面量后续拼接或作为 Git pathspec 的消费者。
QH-04/QH-05 守卫合计 `9/9` 测试通过，两个脚本的 Ruff、Mypy 和仓库实跑均通过。

QH-06 完成记录：统一 README、DEVELOPMENT 与 CONTRIBUTING 的环境口径。面向用户的 editable pip
安装继续保留；贡献者明确一次 `uv sync --extra dev`，随后所有仓库命令使用 `uv run --no-sync`。
公共文档与两类守卫合计 `13/13` 测试通过；全仓 Ruff、扩展至 380 个 Python 文件的 Mypy 和
`git diff --check` 通过。

QH-08 完成记录：新增 import-layer AST 守卫、13 模块/16 条现有向上依赖机器基线和 6 个测试。
foundation/physchem/world/runtime/envs/data 不能再新增向 orchestration 层的 import；移除既有例外时守卫
会提示收缩基线。守卫 `6/6`、Ruff、Mypy 和仓库实跑通过；未移动或改写任何现有 import。

QH-07 交付审查：主进程已重新写入以下非清衡路径，清衡没有覆盖、回退、暂存或修改它们：

- `src/chemworld/eval/work_ii_constitutive_structural_qualification.py`；
- `tests/test_work_ii_constitutive_structural_qualification.py`；
- `workstreams/flagship_tasks/WORK_II_CONSTITUTIVE_STRUCTURAL_Q1_Q2_EXPERIMENT_NOTE.md`；
- `workstreams/flagship_tasks/WORK_II_TODOLIST.md`。

主进程随后把这四个路径提交为 `3a2aa8bd`，并把稳定基线继续推进至 `7995fa49`；当前未提交修改重新
只含清衡 write set。清衡没有执行
blanket `git add`、提交、rebase、merge 或全局证据重建。全仓 Ruff、Mypy 和 `git diff --check`
通过；execution-mode、A-E、matched-prior、oracle、response-surface 与 A-S 定向门 `85/85` 通过。

本文件是仓库级技术债清理和工程收束的当前入口。它不替代
`workstreams/arxiv_v1/FIRST_PAPER_TODOLIST.md` 或
`workstreams/flagship_tasks/WORK_II_TODOLIST.md`，也不改变其中已经冻结的科学问题、实验分母、
候选选择、门槛、停止规则或证据身份。

`MAIN_QUALITY_TODOLIST.md` 记录 2026-08-03 的上一轮质量门修复，保留为历史审计；其中的
claim-driven 协作方式和当时的通过状态不再授权当前工作。现有 `claims/` 只作历史记录，不新增。

## 0. 收束目标

本轮收束只追求四个结果：

1. 建立一个安静、可复核、可持续集成的开发基线；
2. 把核心平台、研究协议、生成证据和论文发布面的边界重新变得清楚；
3. 让状态、质量门和发布门使用同一套不歧义的权威口径；
4. 在用户选择 Work I 发布或 Work II 正式冻结后，只做一次必要的证据重建和最终验收。

本轮不追求：

- 新增任务、世界、物理机制、Agent 方法或 provider campaign；
- 为了让结果更好而调整已有实验门槛、候选、分母或停止规则；
- 在开发阶段反复刷新全局 hash、readiness、evidence graph 或 release certificate；
- 把历史开发结果升级为正式结果，或把环境资格升级为 Agent 性能结论；
- 一次性重写所有大型模块，或以“清理”为名改变运行时和统计语义。

## 1. 状态词、优先级与完成规则

任务状态只使用：`TODO / DOING / BLOCKED / DONE / DEFERRED`。

| 优先级 | 含义 |
| --- | --- |
| P0 | 当前开发分支或基本质量门的直接阻塞；开始其他收束前处理 |
| P1 | 任何 Work I 发布重冻或 Work II release-freeze 前必须完成 |
| P2 | 下一轮大规模功能/实验开发前应完成；不阻塞当前最小发布闭环 |
| P3 | 发布后维护项；不得把它们变成当前冻结的前置审计跑步机 |

一项任务只有同时满足以下条件才能标记 `DONE`：

- 实际问题已消失，而不是只更新说明或改写 hash；
- 定向测试和该任务声明的验收命令通过；
- 没有覆盖、删除或隐式替换失败证据；
- 没有扩大科学主张或改变冻结实验语义；
- `git diff --check` 通过，且变更范围与任务一致；
- 若改变 reader-facing 文档或发布物，规范源和生成物按其工作流同步。

## 2. 2026-08-12 审计基线

以下数字是创建本清单时的诊断快照，不是永久验收常数。正式执行每个任务时应在安静的目标提交上
重新测量，不能因为数字后来变化而手工维护证据 hash。

### 2.1 仓库与分支状态

- 当前 checkout 为 `agent/work-ii-platform-gates`，不是协调分支 `main`；
- 审计期间 Work II 未提交路径持续增加，说明同一工作区仍有并行写入；
- 新改动集中在 execution mode、A-E prior qualification、C2 admission、A-S qualification runner、
  入口脚本、测试和两份实验 note；
- 当前脏树会按设计使 release/source-binding 与 evidence-graph 门 fail closed；开发阶段不应通过刷新
  旧证据来掩盖这一点。

### 2.2 规模与边界

- `src/chemworld`：约 377 个 Python 文件、192k 行；
- `chemworld.eval`：约 124 个 Python 模块、90.5k 行，占源码近一半；
- `scripts`：约 167 个 Python 文件、67k 行；
- `tests`：约 295 个 Python 文件、76.5k 行；
- 测试收集约 2,589 项，其中 `fast and current` 仍选中约 2,457 项；
- Git 跟踪文件的 checkout 体积约 365 MB，pack 约 257 MiB；
- 两份组合资格 JSON 各约 78 MB，另有多份 MB 级 bundle、PDF、TIFF 和历史 RC 报告；
- 跟踪路径中约有 116 个 RC 命名项和 571 个 version/vnext 命名项。

### 2.3 已验证的健康面

- 核心环境、确定性、无效动作原子性、公开观测边界、世界组合、CLI replay 和资源账本代表测试
  `67/67` 通过；
- 当前状态注册、发布工件和 evidence pipeline 代表测试 `21/21` 通过；
- wheel/package smoke `7/7` 通过；
- MkDocs strict build 通过；
- CLI 可以加载，15 个注册任务均可列出；15 个任务的当前卡片都声明
  `physics_maturity=reference_validated`、`proxy_allowed=false`。

### 2.4 当前失败或不完整面

- 活跃 Work II execution-mode 定向测试曾为 `17/18`，source-binding ancestor/material-tree 场景失败；
- Ruff 报告当前未提交 A-E 文件中的 2 个 `SIM102`；
- 创建清单时 Mypy 在 377 个源码文件中报告 17 个文件、67 个错误；QH-03A/B 已在当前 378 个源码
  文件上清零，本条只保留为原始基线；
- Work II release/admission 代表测试为 `10/12`，两个失败来自源码改变后 committed evidence graph 和
  protected material binding 不再匹配；这应在开发期保留为 fail-closed，不立即刷新旧证据；
- 没有仓库内 `.github/workflows`，质量门依赖人工执行；
- `configs/current.json` 的 `updated_at` 为 2026-08-09，未覆盖之后的 Work II 开发状态；
- Work I 清单虽为 `DONE`，但三项 qualification binding 已 stale，`publication_ready=false`；
- Work II 正式 participant/R5 尚未执行，A-E、资源校准、method qualification、A-S 和用户授权门仍未闭合。

## 3. P0：先建立安静的开发基线

| ID | 状态 | 技术债 | 风险 | 完成标准 |
| --- | --- | --- | --- | --- |
| CL-P0-01 | DONE | 主进程已把并行 Q1/Q2 写入提交为 `3a2aa8bd`，未提交树恢复为单一清衡 write set | 共享写入风险已通过显式 owner/write set 和提交边界解除 | 最终定向验收期间 `git status` 稳定；未覆盖、回退或暂存主进程修改 |
| CL-P0-02 | TODO | 当前工作在 feature branch，`main`、本地 `main` 和 `origin/main` 不同速 | 不清楚哪个提交代表下一开发基线 | 先完成或明确搁置当前 feature change；以非破坏方式集成到 `main`；记录目标提交，不 reset 用户分支 |
| CL-P0-03 | DONE | execution-mode 与相关 Work II qualification 定向测试已在当前提交后复核 | development/release 正反路径由现有测试覆盖 | execution-mode、A-E、matched-prior、oracle、response-surface、A-S 定向测试 `85/85` 通过 |
| CL-P0-04 | DONE | QH-03A 已消除当前 Ruff 失败并复跑全仓检查 | 基本提交门已闭合 | `uv run --no-sync ruff check src tests scripts` 通过；`git diff --check` 通过 |
| CL-P0-05 | DONE | QH-03A/B 已把 mypy 从 67 个错误收束至 0，并纠正旧质量状态 | 类型门已闭合；后续新增错误应 fail closed | `uv run --no-sync mypy src/chemworld` 在 378 个源码文件上零错误；132 项定向回归通过 |
| CL-P0-06 | TODO | Work II evidence graph 与 protected source bindings 因开发改动失配 | 若误刷新，会把开发源码伪装成已冻结证据 | 开发期间保留失败；功能稳定后只跑 focused acceptance；直到用户授权 release-freeze 才重建一次正式 graph/receipt |

### P0 验收顺序

1. 等待并行写入完成，确认 owner 和 write set；
2. 只检查当前变更的 Ruff、Mypy 和 focused pytest；
3. 检查 development/release mode 的正反篡改案例；
4. 集成到 `main` 后再建立下一阶段基线；
5. 不在此阶段重建 Work I qualification 或 Work II 全局 release evidence。

## 4. P1：发布或正式冻结前必须清零的技术债

### 4.1 质量门与测试反馈

| ID | 状态 | 技术债 | 处理要求 | 完成标准 |
| --- | --- | --- | --- | --- |
| CL-QA-01 | TODO | `fast and current` 覆盖约 95% 测试，不是真正快速反馈面 | 建立显式 smoke/core/full/slow/reference 分层；不能只按文件名默认把几乎所有测试标 fast | smoke 在普通开发机目标小于 60 s；core 给出稳定分母和进度；full 单独运行；现有语义覆盖不减少 |
| CL-QA-02 | TODO | slow/current/history/rl/reference 主要由 `tests/conftest.py` 文件名和 node token 推断 | 将关键 release、provider-free、network/provider、wheel、paper、reference 类测试改为显式清单或 marker；加入 roster 自检 | 每个测试恰有速度和货币状态；新增测试漏标时 fail closed；选择集数量可机器读取 |
| CL-QA-03 | TODO | 长测试在 `-q` 下数分钟无进度 | 为集成/资格测试提供阶段、completed/total、吞吐和 ETA；日志放仓库外 | 任何预计超过 60 s 的官方命令至少每分钟输出一次有效进度；可定位卡住的 unit |
| CL-QA-04 | TODO | 仓库没有自动 CI | 建立最小跨平台 CI，不调用付费 provider、不刷新正式证据 | Linux/Windows、Python 3.11/3.12 至少覆盖 import/package smoke、Ruff、Mypy、smoke/core；密钥和 private artifacts 不进入 CI |
| CL-QA-05 | DONE | README、DEVELOPMENT、CONTRIBUTING 已区分 public editable install 与 locked contributor execution | 保留用户 pip 路线；贡献者先显式 sync，后续命令全部 `uv run --no-sync` | 三个当前入口命令相容；public-doc tests 通过；不再把系统 Python 当仓库诊断证据 |
| CL-QA-06 | TODO | 缺少按变更范围选择测试的机器映射 | 为核心包、物理模块、Work I、Work II、paper/docs 建立维护成本低的测试 roster | 每个高风险目录有 focused gate；roster 与实际文件漂移时测试失败 |

### 4.2 类型、schema 与失败边界

| ID | 状态 | 技术债 | 处理要求 | 完成标准 |
| --- | --- | --- | --- | --- |
| CL-TY-01 | DONE | Work II 的 `object`/`Any | None` 数字运算入口已显式收窄 | 采用运行时结构检查和局部类型收窄，没有新增无依据 `cast` | 全仓 mypy 通过；相关 artifact/receipt 既有负向测试保持通过 |
| CL-TY-02 | DONE | `Mapping`、`dict`、`list[dict]` 与 `list[Mapping]` 的可变性错误已清零 | 输入保持只读抽象，内部构建和 validator 视图使用显式容器类型 | variance、indexed assignment、return-value 类 mypy 错误为零 |
| CL-TY-03 | DONE | report/cell/key 变量复用和错误 tuple-key 推断已消除 | 使用 `source_report`、`bound_receipt`、`region_key`、`world_key` 等领域化名称 | `no-redef`、错误 tuple key、unreachable 为零；132 项行为测试通过 |
| CL-TY-04 | TODO | evidence artifact 多用裸 `dict[str, Any]`，schema 规则分散在 builder/validator/test | 为跨模块核心 artifact 引入 TypedDict/dataclass 或集中 schema parser；保留 canonical JSON hash | builder、loader、validator 共享同一字段合同；篡改测试仍 fail closed；旧正式 artifact 只读兼容 |
| CL-TY-05 | TODO | 一些运行时错误边界依赖宽泛 `Exception` 捕获或隐式不变量 | 审核公共执行边界，只捕获已知 domain/numerical 错误；编程错误保持可见 | 未知 `KeyError/TypeError` 等不会被伪装为科学失败；已声明 domain failure 仍可重放 |

### 4.3 状态与 readiness 语义

| ID | 状态 | 技术债 | 处理要求 | 完成标准 |
| --- | --- | --- | --- | --- |
| CL-ST-01 | TODO | `benchmark_ready` 在 mechanism 子树为 true，而 README/架构用同一词表达全局 false | 将作用域写入字段名或结构：runtime/environment gate、formal benchmark、publication 分开 | 读者无需上下文即可判断每个 ready 的对象；禁止同名布尔值跨层复用 |
| CL-ST-02 | TODO | `configs/current.json` 的更新时间和部分 Work II 状态落后于活跃工作 | development 状态可更新说明，但不能把未冻结改动写成 current formal evidence | 稳定集成后更新一次；每个状态有 scope、evidence role、artifact state 和 gate state；测试校验派生关系 |
| CL-ST-03 | TODO | 状态表、README、architecture、benchmark docs 和 TODO 中存在人工复制的状态句 | 选择 `configs/current.json` 为机器真值，生成或测试关键读者状态摘要 | 修改状态时单一来源；文档漂移测试能指出具体字段；内部 hash 不进入读者 prose |
| CL-ST-04 | TODO | Work I 的任务清单 `DONE` 容易被误解为 publication-ready | 区分 implementation complete、qualification current、release built、publication ready | Work I 入口和当前状态表使用四个不同状态；三项 stale binding 在未重跑前保持 false |
| CL-ST-05 | TODO | 历史 RC、当前 candidate 和 development result 的命名/位置仍容易被按版本号误选 | 所有消费者只走 current registry 或明确 immutable receipt；禁止 glob 取“最新版本” | 静态检查找不到按版本后缀/mtime 选当前 artifact 的代码；历史文件不再出现在当前入口列表 |

### 4.4 证据与发布完整性

| ID | 状态 | 技术债 | 处理要求 | 完成标准 |
| --- | --- | --- | --- | --- |
| CL-EV-01 | TODO | Work I composition、deterministic-use-case、agent-instrument-use 三项绑定 stale | 只在运行时稳定和用户选择 Work I 收束后，从各 block 第一单元重跑 | 三项新报告全分母通过、全部失败可读、exact replay 通过，`current.json` 绑定 fresh |
| CL-EV-02 | TODO | Work II development evidence 与 release evidence 过去共用过强 clean-tree/source-hash 前置 | 完成 execution-mode 分离：development 清楚标 `development_only`，release 必须 manifest-bound | development 输出无 release/C2 权限；release 输出缺任一 commit/freeze/manifest/surface binding 即拒绝 |
| CL-EV-03 | TODO | release binding 可能包含与执行无关的测试、文档和历史报告 | 定义最小 execution-relevant surface，并单测 included/excluded 路径 | 改论文或历史报告不使 runtime qualification stale；改 evaluator/runtime/config 必须使其 stale |
| CL-EV-04 | TODO | 多个 evidence graph、manifest、readiness 和 audit 可能重复表达同一事实 | 画出当前 DAG，保留一个生成顺序和最少必要 receipt；不新建手工 SHA 清单 | 每个生成节点有唯一 producer、dependencies 和 lifecycle；无循环、无重复权威状态 |
| CL-EV-05 | TODO | 清理过程中可能误删被 frozen artifact 或 legacy replay 引用的路径 | 删除前做 current/immutable/legacy 引用审计；必要时保留兼容读取或迁移表 | current DAG 路径全部存在；正式历史结果仍可验证；不恢复历史文档为当前入口 |

### 4.5 凭据、隐私与执行安全

| ID | 状态 | 技术债 | 处理要求 | 完成标准 |
| --- | --- | --- | --- | --- |
| CL-SEC-01 | DONE | 本地凭据文件仍由 ignore 边界管理；QH-04 新增 tracked/index 守卫 | `scripts/check_tracked_secrets.py` 拒绝禁止路径和高置信凭据指纹，只输出路径和类别，不接触 untracked/ignored 内容 | 守卫 `4/4` 测试、Ruff、Mypy 和当前仓库实跑通过；`git ls-files` 不含凭据、raw provider payload、runs |
| CL-SEC-02 | TODO | 本地 student harness 不是恶意代码 OS sandbox | 文档和入口继续 fail honest；正式第三方提交必须使用独立低权限、无网络、只读和资源限制环境 | public docs 与 evaluator 配置不暗示本地 harness 是安全沙箱；正式 route 有独立隔离验收 |
| CL-SEC-03 | TODO | provider route、credential rotation、pricing 和 currency ceiling 尚未冻结 | 保持为 Work II 外部授权门，不写入通用 cleanup 默认值 | 无授权时 provider 命令 fail closed；费用、重试和停止条件由一次性正式决策文件绑定 |

## 5. P2：结构性技术债，避免下一轮继续膨胀

### 5.1 核心包与研究协议解耦

| ID | 状态 | 技术债 | 建议目标 | 完成标准 |
| --- | --- | --- | --- | --- |
| CL-AR-01 | TODO | `chemworld.eval` 约 90.5k 行，同时承载通用评测、Work I、Work II 和论文资格逻辑 | 至少拆为通用 replay/metrics/artifacts 与 `research.work_i`、`research.work_ii` 命名边界；是否独立 distribution 另行决策 | 核心 wheel 不依赖论文 TODO、workstreams 或 scripts 才能完成普通 run/verify/evaluate |
| CL-AR-02 | TODO | 安装包模块直接硬编码 `workstreams/`、`scripts/`、paper-specific 路径 | 路径绑定移入研究入口/config；核心模块接受显式 Path/contract | wheel 在仓库外能运行核心 API；研究 release 工具仍能显式解析 repo root |
| CL-AR-03 | TODO | `scripts` 有约 167 个 Python 文件、67k 行，部分与 eval builder/validator 重复 | script 只保留参数解析与 I/O，领域逻辑放可测试模块；合并只差版本号的入口 | 每类当前 workflow 有一个入口；历史入口从当前文档移除；CLI wrapper 单测覆盖参数传递 |
| CL-AR-04 | TODO | 多个超大模块：约 5.2k、4.0k、2–3k 行，计划、执行、验证、统计、Markdown 混在一起 | 按 plan/schema、execution、validation、analysis/render 分拆，先处理仍活跃的 Work II 文件 | 单模块目标以职责而非机械行数为准；核心函数可独立测试；canonical hash 输出保持不变或有显式 schema migration |
| CL-AR-05 | TODO | import 层级依赖由约定而非工具保护 | 定义 foundation → physchem/world → runtime → env/data → eval 的允许方向，列出必要例外 | 加入 import-boundary 测试；低层不反向依赖论文、provider 或具体 experiment runner |
| CL-AR-06 | TODO | task/runtime/evaluator 的 ID、版本和字段常量分散 | 建立最小公共 contract/version registry，避免双写和过期别名无限保留 | 轨迹 v0.3 alias 移除有迁移测试；旧轨迹保持只读；新 writer 不再双写弃用字段 |

### 5.2 仓库体积与证据存储

| ID | 状态 | 技术债 | 处理要求 | 完成标准 |
| --- | --- | --- | --- | --- |
| CL-RP-01 | DONE | 跟踪 checkout 约 365 MB，两份资格 JSON 各约 78 MB | 已在 `REPOSITORY_LARGE_FILE_INVENTORY.md` 按 current/immutable、historical/compatibility、generated 和 local-only 分类，并记录消费者、恢复路线与迁移门 | 5 MiB 阈值以上 3 个 tracked 文件均有保留理由、producer/consumer 和安全迁移条件；未授权删除 |
| CL-RP-02 | TODO | 完整明细、摘要和多版本副本同时进入 Git | current 代码仓只保留必要 compact summary、manifest、schema、关键公开轨迹；大 payload 移到 versioned release asset/数据仓 | clone 和常规测试不下载非必要大 payload；公开 release 仍可按 digest 获取完整证据 |
| CL-RP-03 | TODO | 多个 RC/version 文件仍留在当前树，与“Git history 是 archive”不一致 | 先验证引用，再迁出未被 current/immutable artifact 依赖的 superseded 副本 | `configs/current.json` 和 immutable release 引用零断链；当前目录不靠版本号表达历史时间线 |
| CL-RP-04 | TODO | paper 同时保存规范源、生成 TeX、PDF、source bundle、图像和多个导出版本 | 明确哪些是必须跟踪的 publication deliverable，哪些由 release job 生成/托管 | 规范源唯一；同一发布的 PDF/source/manifest 可验证；日常分支不反复提交临时构建物 |
| CL-RP-05 | TODO | 根目录存在大型会议 poster 文件，命名含空格、括号和重复版本 | 判定它们是否为当前发布资产；否则迁入明确 archival/release 位置或外部存储 | 根目录只保留代码仓入口；保留资产有来源、license/用途和版本说明 |

### 5.3 可维护性与公共项目元数据

| ID | 状态 | 技术债 | 处理要求 | 完成标准 |
| --- | --- | --- | --- | --- |
| CL-MT-01 | DONE | 缺少当前 `CONTRIBUTING.md` | 已新增贡献指南，覆盖锁定环境、工作流入口、focused validation、证据边界、长任务进度和禁入数据 | 本地链接检查通过；指南不复制密钥/私有发布流程，且明确 `uv run --no-sync` 执行口径 |
| CL-MT-02 | DONE | 缺少 `SECURITY.md` | 已新增私密报告、凭据事件、第三方代码隔离、provider 边界和现实实验安全说明 | 安全入口明确；未声称本地 harness 是安全沙箱；未读取或暴露本地凭据 |
| CL-MT-03 | TODO | 缺少 `CITATION.cff` 和清晰的发布版本说明 | 以实际公开仓库、作者和 release tag 为准生成；先核对 Work I/Work II 不同作者面 | GitHub citation 可解析；论文、软件和数据集 citation 不混淆 |
| CL-MT-04 | DONE | 缺少面向用户的变更记录/迁移说明 | 已新增从下一 release 开始维护的 `CHANGELOG.md`，不追溯伪造旧版本历史 | Unreleased 分类和 release-entry 规则已定义；明确排除实验流水账、hash 和内部运行元数据 |
| CL-MT-05 | DONE | MkDocs 中多份文档不在 nav，读者难判断是隐藏参考还是遗漏 | 已在 `DOCUMENTATION_SURFACE_AUDIT.md` 分类主导航、reference-only、locale overlay 与 internal/obsolete | `24 nav / 34 reference-only / 0 unclassified`；public-doc tests `4/4` 和 MkDocs strict build 通过 |

## 6. P3：发布后或下一大版本处理

| ID | 状态 | 技术债 | 延后理由与停止条件 |
| --- | --- | --- | --- |
| CL-P3-01 | DEFERRED | 对全部物理模块做新一轮独立参考校准 | 这是新科学/验证工作，不属于工程清理；需要独立问题、note、分母和用户授权 |
| CL-P3-02 | DEFERRED | 建立真实数据、独立 backend 或物理实验 bridge | 不能由软件质量门替代；需外部数据、安全审查和新证据计划 |
| CL-P3-03 | DEFERRED | 大规模重写 runtime/world API | 当前代表测试健康；除非有明确迁移收益，否则不为美观破坏 replay 兼容性 |
| CL-P3-04 | DEFERRED | 清除全部历史轨迹/schema 读取支持 | 必须先定义支持期限并确认公开 release 可迁移；当前只停止旧别名写入 |
| CL-P3-05 | DEFERRED | 把所有研究代码拆成多个独立仓库 | 先完成包内边界和数据外置，再根据维护负担决定物理拆仓 |

## 7. 两条允许的收束路线

P0 和 P1 工程门完成后，用户需选择一个主路线。不得同时启动两个 release freeze。

### 路线 A：优先收束 Work I

1. 冻结稳定的最小 Work I execution surface；
2. 在干净提交上从第一单元重跑三项 stale qualification；
3. 更新一次 `configs/current.json` 和相应证据 DAG；
4. 重建规范稿件对应的 arXiv TeX、PDF、source bundle 和 build manifest；
5. 跑 Work I release tests、视觉检查和 claim-boundary audit；
6. 标记 publication ready 或列出精确剩余 blocker，然后停止扩展。

### 路线 B：继续 Work II 开发，暂不冻结

1. 完成 W2-25Q、W2-26、W2-27、W2-37 的既定准入工作；
2. 保持所有输出 `development_only`，不刷新 formal release evidence；
3. 用户审核 D1/D2、失败轨迹、资源和 evaluator；
4. 等 A-E、2 A-P、2 A-S 与共同 runtime 均稳定后，再请求一次 release-freeze 授权；
5. 授权前不调用正式 participant/provider，不生成 final freeze receipt。

## 8. 集成验收矩阵

以下是收束完成时的最低验收面。执行时遵循 `uv run --no-sync ...`；任何预计超过 60 s 的命令必须
使用原生进度或 `scripts/run_with_progress.py`，并把 wrapper log 放仓库外。

| Gate | 命令或检查 | 通过条件 |
| --- | --- | --- |
| Diff hygiene | `git diff --check` | 无空白/冲突标记错误 |
| Ruff | `uv run --no-sync ruff check src tests scripts` | 0 error |
| Mypy | `uv run --no-sync mypy src/chemworld` | 0 error |
| Smoke | 新的显式 smoke roster | 目标 <60 s，0 failure，分母固定 |
| Core | 核心 runtime/world/replay/resource/public-boundary roster | 0 failure；不依赖 provider、paper 或外部网络 |
| Package | `uv run --no-sync pytest -q --no-cov tests/test_wheel_smoke.py` | 全部通过，仓库外 import/资源查找正常 |
| Registry | current-registry 和 evidence-pipeline focused tests | 路径存在、状态派生一致、当前 DAG 无断链 |
| Docs | MkDocs strict build 到仓库外临时目录 | 构建成功，无新增断链；孤儿页面有明确分类 |
| Security | tracked/staged secret-path scan | 禁入文件、raw runs、provider payload 和凭据为 0 |
| Workstream | 所选 Work I 或 Work II focused acceptance | 仅所选路线通过；另一工作流保持诚实 pending/development |
| Final status | `git status --short --branch` | release-freeze 时必须干净；普通 development closeout 可只保留已声明用户改动 |

## 9. 最终停止条件

满足以下条件后，本轮仓库清理立即停止，不继续制造新的审计层：

1. P0 全部完成；
2. P1 全部完成，或被用户明确降级到 P2/P3 且不影响所选发布路线；
3. Ruff、Mypy、smoke、core、wheel、registry、docs 和 secret-path gates 全部通过；
4. readiness 字段无跨层歧义，reader-facing 状态与 `configs/current.json` 一致；
5. 核心代码、研究协议、正式证据、开发结果和生成发布物边界清楚；
6. 大文件清单和迁移策略已确定，当前/immutable artifact 没有断链；
7. 只对所选路线执行一次 release evidence rebuild；
8. 未改变冻结科学设计，未覆盖失败结果，未把 development evidence 提升为 formal evidence；
9. 最终 handoff 记录目标提交、实际通过的命令、未完成项和下一次允许启动工作的条件。

达到停止条件后，未完成的 P2/P3 债务进入下一维护周期，不阻塞当前发布，也不继续反复生成
preflight、readiness、evidence graph、SHA inventory 或 release audit。
