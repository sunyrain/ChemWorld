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

## 4. 当前优先队列

| ID | 状态 | 控制债 | 处置 | 完成标准 |
|---|---|---|---|---|
| CD-P0-01 | DONE | W2-26 production runner 曾保留历史 operation-count fallback | 已删除旧 `electrolyze=4..5` 权威；W2-26 config 缺字段立即失败，普通历史/development config 不再套用任务特定规则 | production runner 根因回归测试通过；真实 semantic canary 仍与 CD-P0-02 合并执行 |
| CD-P0-02 | DOING | W2-26 缺少最小 production-path semantic canary | 已删除自写 `qualification.passed=true` 的 27-cell synthetic runner；下一步用一条真实 runner canary 覆盖 config→raw→validator | production materializer 和 runner 生成真实 raw/summary；不得 monkeypatch summary builder 或手写 pass 字段 |
| CD-P0-03 | TODO | 平台修复后全块重跑规则可能宽于科学污染边界 | 对未来 block 分开记录 `scientific_disposition` 与 `governance_override`；当前冻结 block 仍服从现行 note | validator-only 缺陷默认可重判；扩大重跑必须逐级给出污染证据 |
| CD-P0-04 | TODO | readiness/manifest/authorization/status 多处复制 pass 状态 | 找出每个字段的 writers/readers，选择 machine summary 为唯一派生权威 | 删除自证明 pass 字段或改为派生；状态副本数量净减少 |
| CD-P1-01 | DOING | development 与 release provenance 仍有交叉入口；已复现旧 v0.1 authorization 测试仅因 experiment-note Markdown hash 变化而失败 | 开发态绕开 clean-tree、全树/说明文档 hash、旧 readiness；先区分仍可执行的 current protocol 与历史 manifest，再把 prose binding 移出 development authorization | 改说明文档/测试不使 development run stale；改 runner/evaluator/config 必须被语义 canary 捕获；不刷新旧 manifest 来换绿灯 |
| CD-P1-02 | DONE | `scripts/evidence_pipeline.py --check` 曾被脚本文档描述为普遍当前门 | 已限定为 release/current-artifact integration；明确不是功能开发、聚焦测试或 development experiment 前置 | 开发契约只要求 focused tests；release/current artifact 仍保留一次性 pipeline |
| CD-P1-03 | TODO | pytest `fast and current` 仍接近全套测试 | 先建立小于 60 秒的显式 smoke roster；不增加逐测试五维 marker 审计 | smoke 覆盖 import、事务、无效动作回滚、replay、task registry、package resource |
| CD-P1-04 | DOING | 大量测试只验证 hash、自哈希 summary、字段存在或 fixture 自己写入的 pass | 首批已删除 W2-26 复制 production schema 的 27-cell synthetic test；继续按生产消费者和故障历史逐文件去重 | 每批删除测试后说明保留的独立行为测试；不删除篡改测试、科学不变量与真实 semantic canary |
| CD-P1-05 | TODO | 宽泛 `except Exception` 可能把编程错误伪装成科学/provider failure | 只审计公共执行边界，收窄为已知 domain/transient errors | `KeyError/TypeError` 等编程错误保持可见；合法恢复路径测试通过 |
| CD-P2-01 | TODO | current status 同时散落于 registry、TODO、README 和报告 | `configs/current.json` 只管理稳定 current/release artifact；活跃实验状态只在对应 TODO/summary | 不再新增同步 checker；读者状态从一个机器源派生或链接 |
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
