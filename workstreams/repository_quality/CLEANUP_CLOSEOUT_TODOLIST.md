# ChemWorld 控制债清理与收束 TODO

状态：**ACTIVE / DEVELOPMENT CLEANUP / RELEASE FREEZE NOT AUTHORIZED**

更新时间：**2026-08-13**

执行约束：**main、单 executor、开发优先、一次冻结；不干扰运行中实验**

本文件是仓库级工程清理的唯一当前入口。科学任务分别由
`workstreams/arxiv_v1/FIRST_PAPER_TODOLIST.md` 和
`workstreams/flagship_tasks/WORK_II_TODOLIST.md` 管理。历史清理 claims、审计快照和旧质量 TODO
只存在于 Git 历史，不构成当前 gate。

## 1. 清理目标

只追求四个结果：

1. 每个执行语义只有一个权威来源；
2. 开发态不被 release hash、readiness、preflight 或历史证据阻塞；
3. 测试证明真实生产路径，不用自写 `passed=true` 的 fixture 冒充语义 E2E；
4. 平台缺陷只影响最小污染单元，完整原始结果优先重判或续跑。

不做：

- 新增 audit、claim、lease、review queue、手工 SHA 清单或另一份清理报告；
- 为让结果更有利而重跑、改阈值、改分母或覆盖失败；
- 在开发阶段刷新全局 evidence graph 或 release certificate；
- 在 provider 实验运行时修改其 runner、配置、manifest、authorization、note 或测试；
- 为追求整齐而一次性重写所有研究模块。

## 2. 分类与完成标准

控制分类：

| 类别 | 含义 | 默认处置 |
|---|---|---|
| K0 | 科学不变量、安全、失败保全 | 保留并集中到唯一边界 |
| K1 | 原子写、断点、窄重试、资源关闭 | 收窄到真实故障边界 |
| K2 | release provenance、hash、freeze audit | 移到最终 release-freeze，只运行一次 |
| K3 | 重复 validator/status、伪 E2E、自证 guard | 合并或删除 |
| K4 | 无事故依据、owner、期限或生产测试的防御 | 删除或拒绝新增 |

一项清理只有同时满足以下条件才算完成：

- 已找到全部当前 writer、reader 和命令入口；
- 明确保留的唯一权威及兼容读取边界；
- 删除后控制面、状态副本或测试数量净减少；
- 不改变冻结科学问题、实验输入、物理语义、分母、阈值和停止规则；
- 聚焦测试及 `git diff --check` 通过；
- 没有刷新历史 hash 或生成新的替代审计包。

## 3. 已完成批次

### CD-01：删除无消费者的基线型包边界控制 — DONE

删除：

- `scripts/check_package_import_boundaries.py`；
- `scripts/check_package_research_boundary.py`；
- 两个对应测试；
- 两个现状 baseline。

理由：仓库没有 CI 或 pre-commit 消费者；两套 guard 仅由自身测试、baseline 和审计说明支持，并把
既有反向依赖固化为允许例外。真正目标是消除包→研究路径依赖，不是永久维护一套不断漂移的现状基线。

### CD-02：删除历史清理控制面 — DONE

删除 repository-quality 下的旧 `claims/`、历史质量 TODO、只读审计快照、CI 设计稿、文档表面盘点、
大文件清单和包边界审计。Git history 是这些材料的归档。当前树只保留本清单。

### CD-03：删除 W2-26 自动规模启动器 — DONE

删除 `scripts/auto_launch_work_ii_w226.py`。该脚本无当前消费者或测试，却会在依赖刚解析时自行生成
unlimited-spend authorization 并启动完整 27-cell provider 矩阵。今后只允许：

```text
production materializer
  -> exact runtime config
  -> production-runner provider-free semantic canary
  -> inspect actual summary
  -> explicit human handoff
  -> separately authorized provider launch
```

### CD-04：删除封闭自证式 Work I audit 回路 — DONE

删除 historical-report-alignment 与 manuscript-language-lock 两套脚本、测试、四份生成报告及两份仅为
这些文件声明历史所有权的 claim。它们没有
`configs/current.json`、evidence pipeline、稿件入口或生产消费者，每套只形成“生成 audit → 测试 audit
自哈希”的封闭回路。历史内容由 Git 保存；当前稿件和 current registry 继续由各自现行入口治理。

### CD-05：删除零消费者的旧 serious-benchmark diagnostics — DONE

删除 `audit_benchmark_validity_power.py`、`audit_campaign_budget_curve.py` 和
`audit_serious_generalization.py`。三者无当前入口、测试或 registry 消费者，只向 ignored `runs/`
生成 `diagnostic_only / paper_claim_allowed=false` 的旧报告。底层可复用 metrics 未删除。

### CD-06：删除旧 first-arXiv remaining-matrix 自证对 — DONE

删除 `audit_arxiv_v1_remaining_experiments.py` 及其两条专属测试。该入口硬编码旧 G0/G2 v0.5
分母，只被自身测试引用，不属于当前 first-paper TODO、registry 或 evidence pipeline。历史矩阵仍可从 Git
恢复；现行论文工作不再暴露第二个“剩余实验”权威。

### CD-07：收束 Work I claims 到两个显式 legacy reader — DONE

`workstreams/arxiv_v1/claims/` 从 68 份收束为 2 份：仅保留 policy-validity 代码实际读取的
`W1-V06--codex.md` 与 `W1-V08--codex-1.md`。其余 66 份协作 claim、README 和模板移回 Git 历史，
不再作为当前 owner、gate、任务队列或状态副本。

### CD-08：删除旧 Work I integration queue 闭环 — DONE

删除旧 14-task integration queue、专属 audit、三条自测和说明页。该闭环只从历史 Git baseline 读取
claims 并验证旧 owner/order/hot-file reservations，没有 current consumer，且与当前 main + 单 executor
协作契约冲突。

### CD-09：删除 W2-26 synthetic summary 假 E2E — DONE

删除 resource-calibration 测试中约 300 行的临时 cell runner 及其 27-cell 假执行。它复制 production
summary、provider receipt taxonomy、qualification 和 denominator 字段，并自行写入
`qualification.passed=true`；因此主线修正真实 terminal/provider 语义后，该 fixture 立即漂移并错误阻塞
清理提交。manifest/authorization、terminal-path resume、reservation 和 write-once 继续由较小的独立测试
覆盖。真实 config→campaign runner→raw→validator canary 仍单独列为 CD-P0-02，不能再由 synthetic summary
替代。

### CD-10：补齐 W2-26 最小 production-path semantic canary — DONE

新增一条 provider-free scripted-participant canary。测试只在 participant factory 边界注入确定性动作，仍由
production materializer 生成任务配置，并穿过真实 campaign runner、ChemWorld 环境、trajectory writer、
exact replay、execution audit、qualification validator 和 summary writer。测试不 monkeypatch analyzer/validator，
也不手写 `qualification.passed` 或最终 summary；因此 operation-count、环境动作、回放或资格语义再次漂移时，
会在真实生产路径上失败。该 canary 不替代 provider contract canary 或科学资格实验。

### CD-11：删除 W2-27 对旧 W2-26 v0.1 readiness 的重复重建 — DONE

W2-27 的 canonical readiness 已校验完整九任务 W2-26 execution manifest、summary 和 task resource cards，
但 authorizer 与 triplet executor 仍额外调用旧三代表任务 v0.1 readiness；旧 manifest 又绑定了一份已变化的
experiment-note Markdown hash，导致真实执行语义未变时仍可阻断 qualification。现已删除这两个入口对旧 builder
和 `missing_pattern_rounds` 的依赖，统一消费 canonical W2-27 readiness，并要求 manifest/summary 成对显式传入；
release audit 同样不再猜测不存在的默认版本。没有刷新旧 manifest，也没有新增 gate。

### CD-12：删除已完成的 A-S 一次性 closeout supervisor — DONE

删除 `scripts/supervise_work_ii_as_closeout.py` 及其 8 条专属 mock 测试。该 supervisor 的跨仓库集成任务已经
完成，canonical A-S summary、Q2 package 和两份 D1 config 均已 durable 落盘；当前树中除自测外没有调用者，
release roster、current registry 和 Work II 执行入口均不读取它。继续保留反而会重新生成旧 v0.1 W2-26
manifest/readiness，并用宽泛 `except Exception` 把编程错误包装成 `fail_closed`。历史执行方法由 Git 保存，
现行 canonical integration 工具和产物未删除。

### CD-13：删除已完成且不可重入的 A-S integration bridge — DONE

删除 `scripts/integrate_work_ii_as_development_result.py` 及其 7 条专属测试。该桥接器的 write-once 目标
已经全部存在，因此在当前仓库中再次调用只会拒绝覆盖；除自己的测试外没有 current consumer。W2-26 和 A-S
qualification runner 直接读取已生成的 canonical summary/package/D1，不依赖桥接脚本。四份 canonical 产物、
生产 validator 与源 qualification runner 均保留，历史跨仓库搬运流程由 Git 保存。

### CD-14：删除已完成的 A-P/W2-39 双模式 closeout builder — DONE

删除 `scripts/build_work_ii_ap_development_results.py` 及其 3 条专属测试。该脚本先生成旧 diagnosis 报告，
后又扩展为 W2-39 platform-requalification builder；W2-39 已终态通过，两个 tracked 报告均无下游代码消费者。
只读重建确认新版 W2-39 JSON 可由它绑定的四个 preserved run 全对象精确重建；旧 diagnosis 则因后来增加
typed taxonomy 字段和路径渲染变化不再精确重建。因此保留两份 immutable 历史报告及原始 runs，不刷新旧报告，
删除会跨两代 schema 重写历史形状的一次性 builder。当前 W2-38 readiness/executor 未删除。

### CD-15：删除 Work II runtime-semantics impact 自证审计环 — DONE

删除 builder、独立 validator、两个 CLI、两份专属测试及 13,442 行 tracked 报告，共 7 个文件。该审计递归扫描
46 份 Work II JSON 及其 hash bindings，再对生成报告做自哈希复核；终态仍是 `pending_requalification`
（18 affected、22 unknown、6 unaffected），没有闭合资格或成为执行输入。整套环未进入 current registry、
current formal execution surface、release test roster、Work II TODO 或任何生产入口；仅历史 v0.1 preflight 记录
过两个模块路径。真实 destructive measurement、catalyst charge、transaction、replay 和 runner 语义测试保留。

### CD-16：删除零引用 S0 multiseed audit CLI 包装 — DONE

删除 `scripts/audit_static_optimization_s0_multiseed.py`。该 46 行入口没有调用者、专属测试、tracked 输出、
current registry 或文档入口，只把 `aggregate_static_optimization_runs` 的结果写成 JSON。底层可复用聚合函数、
多 seed 行为测试及当前 baseline 聚合入口均保留。

### CD-17：删除已退役的 G2 付费 smoke 启动器 — DONE

删除 `scripts/run_g2_smoke.py` 与 `scripts/run_g2_codex_document_smoke.py`。两者都没有代码、测试、文档、
current registry 或任务清单消费者，也没有 tracked smoke 产物；再次调用只会分别发起 WellAU 或 Codex 的
单世界付费 development run。G2 已有冻结正式结果，这两个旧入口既不能验证当前 Work II campaign 语义，
也不应继续充当隐形 provider 启动面。底层 `LiveLLMAgent`、文档工作区、provider 客户端、runner 及其行为测试
全部保留；未来需要 provider canary 时，应从当前 production runner 的最小真实路径显式构造并单独授权。

### CD-18：移除 current release 对 development evaluator shakedown 的依赖 — DONE

删除两条一次性 shakedown 生成入口。blind 入口用合成 incumbent recommendation 验证装置，held-out 入口则
独立重跑五个 development truth blocks；两者的报告均明确 `formal_result=false`，不应成为未来 v0.2 release
的 freshness/hash gate。当前 v0.2 evidence graph 不再读取、校验或连边这两份报告，evaluator 合同由保留的
production plan→execute→validate、exact replay 和 formal orchestration 测试覆盖。该批次先把两份 shakedown
移出当时的 v0.2 graph；后续 CD-20 已将整个 preregistration/evidence-graph 闭环退役。历史内容只由 Git
保存，不因当前 builder 变化重生成；源码身份统一由 clean-release tested commit 负责。

### CD-19：删除 clean-release 的精确 pytest 数量门 — DONE

删除 `EXPECTED_WORK_II_RELEASE_TEST_COUNT=267`、独立 `--collect-only` 全量预跑及 receipt 中的 `collected`、
`test_file_count` 和 collection stdout/stderr hashes。原实现把同一固定 roster 执行两遍，并让合理的测试
增删在全部测试通过时仍因数量不等于 267 而阻断 release。现在仍在独立 clean checkout 中精确执行固定
`WORK_II_RELEASE_TEST_FILES` roster，任何命令失败都会终止；receipt 记录实际 passed 数，并严格要求
`passed>0`、`skipped=0`、`failed=0` 与完整 roster 相符。未刷新既有 receipt。

验证：`tests/test_work_ii_release.py` 10/10 通过；内存 receipt 探针确认任意正通过数均可接受，而 0
通过、skip 或 roster 漂移仍被拒绝。同期 preregistration 的 2 个失败来自历史 formal binding SHA
清单漂移，未通过刷新旧证据规避，列入后续控制债清理。

### CD-20：退役 preregistration readiness / evidence graph 闭环 — DONE

消费者审计确认：zero-call preregistration readiness、narrative draft、pre-run evidence graph、四个
`--check` subprocess、旧 clean-release receipt 与各自测试主要互相读取；真正 formal executor 不依赖
readiness 或 graph，而是在执行入口直接校验 formal manifest/source bindings、方法资格 receipt、费用与
最终用户授权 receipt。该闭环会在每次 development 改动后重新比较几十个源码 SHA，并把正常变化变成
`internal_errors`。现已整链退役 12 个 builder/module/test/config/report 文件，并从 clean-release receipt
删除 graph、四重 check 和审计脚本自哈希。旧文件不刷新、不迁移，历史由 Git 保存。

clean release 仍保留独立 clone、固定 Work II 测试 roster、wheel 构建、隔离安装 smoke、clean-before/
after 与 exact tested commit；formal execution 仍保留所有科学分母、C2 admission、方法资格、费用上限、
失败/恢复语义和显式用户授权。同步删除 submission venue route gate：投稿路径与编辑审批不改变冻结科学
问题、cohort、分析或失败规则，不再作为 provider/formal execution 的第二权威。

验证：`tests/test_work_ii_release.py` 6/6；`tests/test_work_ii_formal_runner.py` +
`tests/test_work_ii_cost.py` 23/23；qualification 20/20、private execution/report 8/8、当前 v0.2
resource-calibration 路径 11/11；Ruff、compileall、离线 wheel 构建与悬空引用扫描通过。另删除一条只读取
stale launch brief 文案的测试；它不再为已退役报告充当保留门。未生成或刷新任何旧证据。

### CD-21：删除 formal preflight 的第二套源码 SHA 权威 — DONE

formal preflight 原先递归枚举整个 `src/chemworld`、四个 runtime config tree、约三十个脚本/入口、
`pyproject.toml` 与 `uv.lock`，生成逐文件 `source_bindings`；build/check/final execution 又逐项复核。
但最终授权已经要求 clean worktree，clean-release receipt 已在独立 clone 中执行固定测试 roster、构建并
隔离安装 wheel，并把当前 material tree 唯一绑定到 exact tested commit。两套机制证明同一源码身份，
前者会把任意 development 修改扩散成数百项 stale SHA。

现已删除 preflight 的递归源码枚举、`source_bindings` 输出和 execution-time 第二次逐文件复核。formal
manifest 仍逐内容绑定 design、analysis、每个 task campaign config、C2 admission receipt/outcome-blind
selection，并直接重验 Gate A 科学证据；clean release 仍绑定 `configs`、`scripts`、`src/chemworld`、
依赖锁与构建元数据。`tests` 不再属于 runtime material tree：测试仍必须在独立 checkout 中真实通过，
但单独增删测试不会使未改变的 runtime implementation stale。

### CD-22：退役 W2-26 v0.1 协议壳与重复测试 — DONE

当前 v0.2 校准只从 2,569 行的 `work_ii_resource_calibration.py` 借用 task-resource card 的公式绑定、
校验和 cap materialization；其余 v0.1 readiness、三代表任务选择、Q2 generation、authorization、summary
与自哈希协议没有 current 消费者。旧 v0.1 manifest 只被一份同样过期的 readiness 报告引用，两者也不在
current registry、W2-27 或 C2 execution path。现已把 369 行共享契约抽成命名准确的
`work_ii_task_resources.py`，让 v0.2 直接拥有三臂执行常量并直接导入 campaign closeout 契约；删除旧模块、
旧 manifest 和旧 readiness 输出。历史 formal preflight 中的旧路径保持为不可改写快照，由 Git 归档。

同时将混合 v0.1/v0.2 的 1,681 行 calibration 测试收束为约 340 行当前行为测试：保留精确九任务/分母、
production materialization、typed resource constructor、旧 metadata 拒绝、授权/未知价格、task identity
防篡改和逐 task resume；task-card 漂移、provider/platform taxonomy、W2-27 qualification 与 C2 admission
继续由独立行为测试覆盖。当前 method-qualification CLI 的默认输出名同步改为 v0.2，避免继续生成 schema
为 v0.2、文件名却为 v0.1 的新副本。聚焦测试 39/39，下游 qualification/C2 33/33 通过。

### CD-23：退役 A-E prior qualification v0.1 执行孤岛 — DONE

删除 `work_ii_ae_prior_qualification.py`、其薄 CLI 和 12 条专属自测。三者只互相引用：旧模块把自己的
plan/report/hash 协议完整复制在一个 72 KB 文件中，没有 current registry、当前 formal cohort、v0.2/v0.3
qualification 或生产入口消费者；唯一外部命中是历史 formal preflight 的不可改写文件清单快照。当前
A-E 资格由 v0.2 cohort/qualification 与 v0.3 shards 路径承担，保留的 v0.2 测试覆盖精确分母、release
context、篡改拒绝、唯一 claim 和完整 1,200-cell disk validator，formal cohort 测试继续覆盖下游消费。
因此本批删除的是自成闭环的旧协议测试，不删除当前科学不变量、真实 validator 或篡改测试，也不刷新历史
preflight 来抹掉旧路径。

### CD-24：退役 v0.1 analysis power/resource audit 权威层 — DONE

删除 484 行 audit、2 条专属测试、655 行机器报告和将其称为 source of truth 的草稿。该工具默认读取
v0.1 analysis/design，并把校准前资源上限累计成 `6,840` operations、`324M` accepted input tokens 等旧
planning 数值；当前 W2-26 task cards、v0.2 formal builder 和 production runner 已直接校验 task config、
resource cap、checkpoint、provider timeout、并发、recipe diversity、世界分母与失败保留规则，继续保留旧
audit 只会制造第二套过期权威。

本批没有把陈旧 design SHA 刷成新值。v0.2 analysis 只按路径选择 design；formal manifest 仍分别完整绑定
design 和 analysis，本地及执行时继续重验两者。二者之间改为校验可解释的字段关系：5 tasks、25 clusters、
75 cells、三臂、每 cell 一次 provider repeat、失败结果保留、`0/2/4/6/8` checkpoints、primary hypothesis、
implementation denominator、自由度与 alpha。v0.1 legacy preflight 仍保留其原始整文件 SHA 兼容。静态 power
近似只作为历史设计依据由 Git 保存，不再成为每次开发修改都要重跑的 execution gate；实际 confirmatory
实现仍保留 bounded error、symmetric adverse bounds、25-cluster/75-cell denominator 与 H4 非 confirmatory
的行为测试。

### CD-25：收束真实实验状态并登记 private-seal 不可满足门 — DONE

W2-26 不再沿用“缺 A-S config”的过期 blocker：A-S Q2/D1 已存在，真实 r9 状态是 7/9 triplets、21/27
cells 后在第 8 个 A-S partition 遭遇三臂同步 provider outage；两次 attempt 均 invalidated，第 9 个未启动，
且没有全块 terminal summary。该状态只写入 Work II TODO，不制造新的 status JSON/hash，也不把 partial 拼成
成功。W2-37 则已有唯一机器 summary，精确完成 `10,240/10,240` primary 和同数 exact replay、两候选均
`5/5` worlds 通过；TODO 已据此关闭，仍明确 D1 不等于 participant/formal 授权。

在文档待提交期间新启动的 W2-27 也已自然终结并由仓库 validator 复核：3/3 arms 各 8/8 terminal、
每臂 1 次 provider attempt、0 provider/infrastructure failures，exact replay 各 48 steps 且 0 mismatches，
receipt validation 为 0 errors。状态源仍是 ignored run receipt；TODO 只记录摘要和边界，不复制 receipt 或
新增 hash gate。它关闭 development method qualification，但 `formal_execution_authorized=false`，也不能用来
填补 W2-26 缺失的第 8/9 task triplets。

同时确认 v0.2 private gate 当前没有可满足 witness：外部 seal 对 v0.1 design 的完整 validator 为 0 errors，
对 v0.2 唯一错误为 design identity mismatch；两版 design 却绑定同一 complete-seal commitment。修改 seal
identity 会改变 commitment，保留旧 identity 又不匹配 v0.2。因此本轮不刷新 hash、不放宽 validator、不生成
或暴露 private identities，也不把 formal-design audit 整组删除。后续须由用户/协议 owner 显式选择：将 seal
迁移为独立 cohort identity 的兼容契约，或在 release freeze 前授权重新封存并更新 v0.2 commitment。

### CD-26：退役 W2-27 重复 readiness 投影层 — DONE

W2-27 在 selected-card receipt、materialized runtime config、local manifest、费用授权和 terminal receipt 已经
形成直接 fail-closed 链后，仍保留两套 readiness builder/validator、一个 105 行零调用 CLI，以及只为 readiness
展示路径而穿透 authorizer/runner 的 `--resource-calibration-manifest` 参数。旧 full-calibration readiness 又把完整
九任务状态和历史报告绑定复制成第二事实源；local readiness 则再次序列化同一 selected card、执行分母、blockers
和 self-hash。两者都不贡献独立执行决策。

现已整组删除 1,143 行：authorizer 和 triplet runner 直接由 selected-card receipt 重建 runtime config，校验
W2-27 local manifest，再校验费用、attempt/journal、authorization、terminal receipt 与 missing-only resume。
保留了设计切片漂移、selected evidence 篡改、资源卡 identity、费用、三臂终态、replay 和 crash-resume 负向测试；
同时删除 journal validator 将历史 runner SHA 与当前工作树 runner 文件反复比较的时变 gate：runner path 与
SHA 仍作为执行时事实受 journal self-hash 保护，但当前 release 资格只由 tested commit/release envelope 负责。
76 项 qualification/local gate/formal/release/cost 测试、真实 terminal receipt 探针与 Ruff 通过。未删除
W2-26 自身 manifest，也未把 r10 partial 结果升级为 qualification evidence。

维护窗口前确认 W2-26 r10 自然终结：前 8/9 triplets、24/27 cells terminal；最后 A-S crystallization 三臂在
同步 provider error 后分别停于 9/12、1/12、1/12，整 triplet invalidated，无 root summary。控制器连续两次
观测均不存在后才修改仓库；所有失败轨迹保留，未自动续跑。

### CD-27：修复 D1 不可达 release 边界并删除 W2-26 虚构 source gate — DONE

D1 evaluator 原先允许选择 `release`，却只检查一组全局 protected-material dirty paths，不消费 canonical
release manifest，并固定写出 `release_eligible=false`；因此即使 evaluator 成功，也不存在能进入 terminal C2
admission 的 D1 witness。现已把默认模式改为 development：development 直接写入廉价、不可发布的 execution
envelope；release 则必须显式传入并通过同一 `prepare_execution_context` release manifest 校验，再写入 tested
commit、freeze id、manifest SHA 与 execution-surface SHA。缺少 release manifest 会在生产者边界直接拒绝，不再以
clean worktree 冒充冻结身份，也不再另造 C2 whole-tree source binding。

同时删除 C2 对 W2-26 terminal summary 中 `c2_source_binding` 的要求。该字段从未出现在 v0.2 producer schema、
builder、validator 或真实输出中；W2-26 的职责是九张 task resource cards、分母、失败保留与 provider accounting，
source identity 已由五份 release execution envelopes 的共同 tested commit/freeze id 负责。保留 exact nine-card
校验，不给历史或 development calibration 追补新 hash。D1/C2 聚焦测试 27/27 与 Ruff 通过；运行中的 A-E v0.3
只加载 qualification/shard/supervisor 模块且产物位于仓库外，本批未修改其 import surface、合同或执行文件。

### CD-28：退役 C2 中间 receipt 的第二套源码身份 — DONE

C2 outcome-blind selection 和 task-admission receipt 原先都嵌入 `tested_commit + material_tree`，递归覆盖 configs、
scripts、package source、tests、lockfile 与 build metadata，并在重建时比较当前 HEAD/工作树。terminal C2 admission
又独立要求 Q1/Q2/D1 与 A-E 的 release execution envelopes 全部通过校验并共享一个 freeze id 和 tested commit；
因此中间 source binding 不贡献新的科学判定，只会让无关测试或开发修改使尚未进入 final admission 的 selection/
receipt stale。

现已整组删除 source-binding builder、validator、dirty-tree projection、路径清单、两个 durable 字段及专属 mock，
净删约 240 行。由于持久结构发生变化，outcome-blind selection 升为 v0.3、task-admission receipt 升为 v0.2，旧对象
只由 Git 保存，不原地伪装成新 schema。继续保留 protected selection protocol 的 path/file/embedded hashes、stage
report bindings/self-hashes、逐阶段确定性重建、roster/slot outcome-blind 检查，以及 final admission 的五份 release
envelope 同 cohort 校验。C2 owning tests 26/26、formal runner + A-S downstream tests 47/47 与 Ruff 通过。

### CD-29：窄化 development readiness，移除时变 HEAD/clean 副本 — DONE

`work_ii_development_readiness` 仍拥有真实的 provider 前决策：历史 trajectory 重验、方向 query 稳定性、精确
config/schedule、seed-0 扩展 pilot 以及 terminal seed-0 continuation 保留。因此本批没有把 readiness 整组删除。
但旧 receipt 同时要求 build 时 clean worktree、记录生成时 source commit，并在消费时与当前 HEAD 比较；provider
入口已经用 canonical release manifest 和 config execution envelope 重验 exact HEAD、execution surface、freeze、
provider authorization，这两项只会让正常维护追溯性地使 readiness stale。

现已删除 `clean_committed_worktree`、receipt `source_commit` 与 current-HEAD comparison，schema 从 v0.6 升为
v0.7；仓库没有 current v0.6 durable receipt 需要重写。保留 trajectory/config/schedule/pilot/continuation bindings、
self-hash、zero-provider、release freeze 与所有科学/恢复 checks。readiness owning tests 11/11、provider 入口对缺
readiness/缺 release manifest 的 pre-output 拒绝 2/2 与 Ruff 通过。

### CD-30：收束 private authorization 的三重 source/clean 权威 — DONE

private authorization 已绑定并重验 clean-release receipt；后者拥有 independent checkout、tested commit、最小
material tree、current clean state、material drift 与 ancestry 校验。旧 authorization 仍额外执行 dirty-tree check、
复制当前 `source_commit` 和 `source_tree_clean_at_authorization=true`，消费时再次比较，再把同一 commit 复制进
private execution manifest。这些字段不贡献用户授权、费用或科学决策，只增加正常维护导致 authorization stale 的
入口。

现已保留 clean-release receipt 的 path/file/self-hash binding 作为唯一 source owner，删除 authorization 的重复
dirty/HEAD/clean 字段及 manifest 透传；authorization/manifest schema 均升为 v0.2。用户三项显式确认、provider
contract、pricing provenance、75→150 attempt caps、currency ceiling、write-once store 与 resume/tamper 语义均保留。
private execution 5/5、clean-release 文件授权后篡改拒绝与 Ruff 通过。

### CD-31：删除 five-seed provider launcher 的第二个 clean-tree gate — DONE

five-seed provider 入口原先先独立调用 `git_worktree_dirty`，随后立即调用 canonical
`validate_release_d1_config`；后者已经通过 release manifest 校验 current clean state、exact HEAD、execution
surface hash、config envelope 与 provider authorization。同一调用栈的前置 dirty probe 不增加不变量，只产生第二
条错误路径和三处测试 mock。

现已删除 launcher-local dirty gate 与 mock；执行开始/终态报告中的 `source_commit` 继续作为历史事实保留。
release manifest/config、qualification evidence、zero-provider readiness、credential、三臂 schedule 与 pre-output
ordering 均未削弱。缺 readiness、缺 manifest 与 development context 的聚焦入口测试 3/3、Ruff 通过。

### CD-32：删除局部离线 evaluator 的全仓 clean-tree gate — DONE

`evaluate_work_ii_catalyst_deactivation_paired_provider_campaigns.py` 对两份已完成 participant campaign 做固定
配方的 counterfactual replay；它已经逐文件绑定两份 task config、participant summary、trajectory 与 action plan，
拒绝覆盖输出，并在结果中记录运行时 `source_commit`。旧入口仍额外要求整个仓库 clean，导致无关测试、文档或
其他 workstream 的改动都能阻止这一局部 development evaluator，却不能提高配方配对、物理重放或结果身份的
可信度。

现已删除 evaluator-local `git_worktree_dirty` blocker；保留 config/file/action-plan/trajectory/self hashes、精确
配对检查、不可覆盖输出、失败明细与 source commit 历史记录。该脚本没有 current registry 或活跃 provider
runner 消费者，仅由 campaign-runner 行为测试导入其纯分析函数；因此本批不改 A-E 或 W2-26 活跃导入面，也不
刷新任何历史结果。聚焦 paired-analysis owning test 1/1、Ruff 与 skill validator 通过；同文件全测 42/43，唯一
失败是既有 qualification CLI 已先要求 manifest、旧测试仍期待 authorization 错误优先级，已作为独立测试债保留，
没有通过调换生产入口的 fail-closed 顺序来迎合旧断言。

### CD-33：修复 qualification 缺授权测试的前置条件 — DONE

qualification production 入口现在按 manifest → user authorization → per-attempt authorization → cost ledger 的顺序
fail closed；旧测试没有提供 manifest，却断言第二层 authorization 错误，因而只是在验证错误消息顺序漂移。现仅在
测试输入中补一个非空 manifest 路径，使执行仍在任何文件读取、输出创建或 provider 调用前因缺 user authorization
拒绝；未调换或放宽活跃 campaign runner 的四层入口校验。

### CD-34：退役 W2-26 readiness 自投影层 — DONE

W2-26 的 readiness builder/validator 只把 manifest resolved coverage、可选 terminal summary、blockers 与两个
eligibility boolean 重新序列化，再加一层 self-hash。它没有独立决策：authorization builder 已直接对九任务
manifest 做 full validation；execute 会重验 authorization 及其 manifest binding；terminal summary validator 已
拥有精确 9 triplets / 27 cells / 252 experiments、全部失败、provider accounting 与 replay 语义。仓库内也没有
current consumer 调用该 runner 的 `--preflight` 或 `--check`。

在确认 W2-26 等待控制器与 runner 均已自然退出、r12 输出目录从未创建后，现已整组删除 readiness schema、
self-hash、builder、validator、两个 CLI mode、`--summary` 投影输入与 execute 前的 status 翻译，共净删 160 行。
保留 `--summary-template` 作为无 provider 的 manifest/summary contract 检查，保留 direct manifest validation、
write-once authorization、user/provider/pricing/cost/attempt contracts、triplet restart hard cap、terminal summary、
所有失败与 exact replay。新增 CLI 测试证明 summary-template 直接生成零 provider 的精确分母 summary，以及
incomplete manifest 在 authorization 输出创建前被拒绝；W2-26 及下游聚焦测试 51/51、Ruff 通过。

## 4. 当前优先队列

| ID | 状态 | 控制债 | 处置 | 完成标准 |
|---|---|---|---|---|
| CD-P0-01 | DONE | W2-26 production runner 曾保留历史 operation-count fallback | 已删除旧 `electrolyze=4..5` 权威；W2-26 config 缺字段立即失败，普通历史/development config 不再套用任务特定规则 | production runner 根因回归测试通过；真实 semantic canary 仍与 CD-P0-02 合并执行 |
| CD-P0-02 | DONE | W2-26 缺少最小 production-path semantic canary | 已删除自写 `qualification.passed=true` 的 27-cell synthetic runner，并以一条 scripted-participant 真实 runner canary 覆盖 materializer→environment→trajectory→replay→validator→summary | production materializer 和 runner 生成真实 raw/summary；未 monkeypatch analyzer/validator/summary builder，也未手写 pass 字段 |
| CD-P0-03 | TODO | 平台修复后全块重跑规则可能宽于科学污染边界 | 对未来 block 分开记录 `scientific_disposition` 与 `governance_override`；当前冻结 block 仍服从现行 note | validator-only 缺陷默认可重判；扩大重跑必须逐级给出污染证据 |
| CD-P0-04 | DONE | readiness/manifest/authorization/status 多处复制 pass 状态 | 已删除 W2-27 两套 readiness、preregistration/evidence-graph 闭环与 C2 selection/receipt 的重复 material-tree source authority；最终执行只消费 direct manifest/evidence/authorization receipts 与统一 release envelope | execution-time source/scientific validation 保留；旁路状态闭环、自证明 pass 和中间 whole-tree hash 已删除 |
| CD-P0-05 | BLOCKED / OWNER DECISION | v0.2 private seal 同时要求 v0.1 complete-seal commitment 与 v0.2 design identity，逻辑上不可同时满足 | 不刷新 hash、不弱化 identity validator；选择独立 cohort compatibility migration 或显式 reseal/update commitment | 存在一份不暴露 identities、可通过 v0.2 完整 validator 的 seal witness，且迁移由用户/协议 owner 明确授权 |
| CD-P1-01 | DONE | development 与 release provenance 曾有交叉入口；旧 v0.1 authorization 测试仅因 experiment-note Markdown hash 变化而失败 | W2-27 开发授权/执行现只校验显式的当前九任务 execution manifest + summary 对；旧 prose binding 不再参与入口，release audit 也必须显式选择冻结证据 | 改说明文档/测试不再使 development qualification stale；runner/evaluator/config 由真实语义 canary 和当前 manifest/summary 捕获；未刷新旧 manifest 来换绿灯 |
| CD-P1-02 | DONE | `scripts/evidence_pipeline.py --check` 曾被脚本文档描述为普遍当前门 | 已限定为 release/current-artifact integration；明确不是功能开发、聚焦测试或 development experiment 前置 | 开发契约只要求 focused tests；release/current artifact 仍保留一次性 pipeline |
| CD-P1-03 | TODO | pytest `fast and current` 仍接近全套测试 | release 已删除 collect-only 双跑和精确 267 数量门；下一步只建立小于 60 秒的开发 smoke 命令，不增加逐测试 marker audit | smoke 覆盖 import、事务、无效动作回滚、replay、task registry、package resource |
| CD-P1-04 | DOING | 大量测试只验证 hash、自哈希 summary、字段存在或 fixture 自己写入的 pass | 已删除 W2-26 synthetic schema copy、v0.1 protocol、A-E prior v0.1、旧 power/resource audit、A-S/A-P/impact-audit 及 preregistration/graph 闭环专属测试，并保留真实路径 canary、typed constructor、tamper、科学不变量与 formal execution tests；继续按消费者和故障历史逐文件去重 | 每批删除测试后说明保留的独立行为测试；不删除篡改测试、科学不变量与真实 semantic canary |
| CD-P1-05 | DOING | 宽泛 `except Exception` 可能把编程错误伪装成科学/provider failure | 已随退役 A-S supervisor、runtime-impact audit 和旧 G2 smoke 删除不再有消费者的宽泛边界；其余只在仍活跃公共执行边界按事故证据收窄，不做机械全局替换 | `KeyError/TypeError` 等编程错误保持可见；合法恢复路径测试通过 |
| CD-P2-01 | DOING | current status 同时散落于 registry、TODO、README 和报告 | 已将 W2-26 partial/provider-blocked 与 W2-37 terminal 状态收束至 Work II TODO，并链接唯一机器 summary；`configs/current.json` 只管理稳定 current/release artifact | 不再新增同步 checker；其余活跃实验也从一个机器源派生或链接 |
| CD-P2-02 | TODO | 大型 script 同时承担 plan、execution、validation、rendering | 只在仍活跃文件上按职责拆分，CLI 保持薄层 | 不复制 schema/hash；现有输出保持兼容或有显式迁移 |
| CD-P2-03 | TODO | tracked 大型明细和多个版本副本增加 checkout 与选择歧义 | 只迁移无 current/immutable 消费者的 superseded payload | current registry 和冻结 replay 零断链；历史从 Git/release asset 恢复 |

## 5. 必须保留的控制

以下不是本轮删除目标：

- 冻结实验的 question、coverage、world/arm/seed、分母、阈值、停止规则；
- raw trajectory、exact replay、失败结果和资源账本；
- provider 凭据隔离、显式费用授权和不可覆写输出；
- 原子写、可靠 checkpoint、窄范围 transient retry；
- release-freeze 时最小执行面的 source binding；
- `configs/current.json` 对稳定 current artifact 的解析职责；
- 能证明真实篡改、泄漏、物理错误或执行语义漂移的负向测试。

## 6. 执行顺序

1. 先等待活跃 provider block 自然终结；
2. 每批只选择一个 authority group；
3. 做 writer/reader/reference 审计；
4. 删除或合并控制，再补最小真实路径缺口；
5. 只跑受影响的聚焦测试；
6. 功能面稳定后跑一次 integrated acceptance；
7. 用户授权 release-freeze 后才重建一次 provenance/evidence。

## 7. 停止条件

出现以下情况必须停下并请求用户决定：

- 需要停止或替换运行中 provider 进程；
- 删除对象仍被 current registry、冻结 artifact 或 legacy replay 读取；
- 清理会改变冻结科学语义；
- 无法证明重复测试由更强测试覆盖；
- 需要付费调用、刷新正式证据或扩大为全矩阵重跑。
