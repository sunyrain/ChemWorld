# DEV-EXPLORE-03：社区发布能力探索

状态：DONE；以下设计在执行前写入，结果在末尾追加，development evidence。执行者 Codex /root，单 executor。沿用前两块原始结果，不重跑或覆盖；不修改运行时、冻结证据或论文，不发布、不调用付费模型。

问题：当前开发版能否被仓库外的新用户安装、运行、验证和扩展？哪些科学语义、接口、文档、应用和社区流程阻碍可分享发布？

固定覆盖：

1. 构建 wheel 和 sdist 各一次；wheel 独立目标目录安装（复用锁定环境依赖），在仓库外核对导入及资源路径、包清单和 CLI。此检查不冒充全新 OS/依赖环境安装。
2. 安装包 CLI 的 help、tasks list、tasks show、random seed=0 reaction-to-assay run、verify(tolerance=0)、evaluate、未知 task 错误七个命令；三份现有示例：agent-facing API、RL vector wrapper、manual event sequence。输出全部到仓库外。
3. 固定 16 个 pytest 文件：test_env、test_tasks_and_wrappers、test_cli、test_cli_verify、test_wheel_smoke、test_flow_coupling、test_electrochemical_autonomous_open、test_electrochem_equilibrium_coupling、test_phase_equilibrium、test_separation_chain_coupling、test_environment_self_consistency、test_task_lab、test_experiment_explorer、test_experiment_codex_mcp、test_score_replay、test_latent_terminal_replay；另运行 Experiment Explorer 的 JS replay tests。记录收集/通过/失败/跳过数，不将单元测试数计作独立科学实验。
4. Gym 标准 checker：reaction-to-assay 的原始环境和 RLObservationWrapper 各一次；保留 warning 和异常。四类补充路径（flow-reaction-optimization、electrochemical-conversion、equilibrium-characterization、reaction-to-purification）各 seeds 0/1/2，用公开 task recipe 的固定 0.5 向量，各执行一份完整配方；不根据结果调参。保存全部动作、终检/失败、资源和零容差回放，共 12 路径。
5. 本机 Task Lab HTTP：正常 status、student 页面和 session 创建，外来 Origin/Host 的 status/session 请求，错误 JSON，静态路径越界；只使用合成输入且不启动 provider/Agent job。检查持久会话、请求限制和错误契约的源码。若可用，真实浏览器查看 Student Lab 和 Explorer，不把 DOM 测试冒充视觉验收。
6. 只读检查许可、贡献、安全、版本/迁移、CI、引用、文档导航/中英文一致性、模型卡、扩展合同及公共发布入口；可联网读取公开仓库元数据，不下载私有数据。尝试 docs strict build 一次，缺依赖如实列为未验证。

测量：每个命令退出状态和耗时、测试分母、包体积/文件范围、导入路径、接口响应、每路径操作/终检/事务/回放、运行时警告；记录本机配置和探针输出。单项超时 600 s，进度至少每 30 s（阶段、完成量；未知分母用日志字节/存活计数）。任何失败保留，不修复后悄悄替换。

通过规则：包实际从安装目录加载；支持的命令/示例和测试成功；结构化错误无未处理 traceback；HTTP 非本机 Origin/Host 不得产生会话状态变化；路径终检、资源与回放分别判断，不能互相替代。潜在模型局限只在实测或源码支持的范围内分类，不声称真实实验外部效度。

输出：仓库外 `D:/Projects/ChemWorld-local-research/20261009-explore03/` 的脚本、原始日志、机器摘要、轨迹和安装包；本文件追加结果。研究日志保存恢复入口。完整改良清单保存于本 experiments 目录，含优先级、证据、影响、修复建议、验收标准及未验证范围。

停止：固定覆盖各尝试一次，失败不扩张重试；完成可读摘要和分阶段改良清单即结束本块。新增假设需另立短块设计。

## 实际结果（2026-10-09）

固定覆盖已执行；下列均为当前开发工作树证据。用户明确首发服务对象为**研究者与 Agent 开发者**。未修改运行时、未重跑不利结果、未调用 provider、未发布。

| 覆盖 | 实际分母与结果 |
| --- | --- |
| 构建/安装 | wheel、sdist 各构建一次成功；wheel 安装至仓库外成功，导入路径及配置路径均在 installed 下；Windows / Python 3.12.10，复用仓库锁定依赖 |
| 7 个 CLI 命令 | 6 个正常命令退出 0；未知 task 按预期应拒绝，但输出未处理 traceback 并退出 1，未满足本块错误体验规则 |
| 3 个示例 | Agent API、RL vector 成功；manual event 在首步前访问 reset info 的 world_id，KeyError 失败 |
| 16 文件 / 205 pytest | 204 通过、1 失败、0 skip、0 error；失败是 serious readiness 的 4/6 与预期 6/6 不一致 |
| JS 与 docs | Explorer 15/15 JS tests 通过；本地 mkdocs strict build 通过 |
| 2 个 Gym checker | 原始环境 reset observation 等价检查失败；RLObservationWrapper 在 step info 等价检查失败。不能据此断言物理回放不确定 |
| 12 补充路径 | 4 类 × 3 seeds；138/138 动作 committed，12/12 终检，12/12 tolerance=0 回放，0 执行异常 |
| 9 HTTP 请求 | 正常 status/student/session 为 200/200/201；外来 Origin 和 Host 各自读 status 为 200、创建 session 为 201；畸形 JSON 为 400、越界路径为 403 |
| 浏览器 | 创建 Edge tab 不可用，浏览器列表为空；没有真实 UI 验收。临时本机服务已停止 |

机器摘要：`D:/Projects/ChemWorld-local-research/20261009-explore03/analysis.json`。17 个命令作业中 14 个退出 0、3 个非零；物理路径、命令、测试不能混为独立实验分母。构建约 80.9 s，定向 pytest 约 31.5 s；这不是隔离性能 benchmark。

### 新发现

- wheel 2,845,444 bytes / 752 条目；sdist 388,009,104 bytes / 4,432 条目，包含 2,562 个 paper/workstreams 条目，且带入用户未跟踪图件目录中的 18 个文件及本机 cache 小文件。没有向外发布此包；不要直接把开发仓库默认 sdist 当社区发行包。
- wheel 携带全部 312 个 configs 文件，不含 apps；开发仓库的 Task Lab / Explorer 启动命令不能视为 wheel 功能。路径清单没有 api.md、key2.md、.env；这不是完整秘密扫描或信息隔离证明。
- readiness 的具体差异来自结晶和水相平衡新增运行时泛化轴没有完全进入设计合同；这是当前合同维护问题，不需要重建历史证据链才能继续开发。
- 原始 Gym observation 的未观测值为 NaN，而标准 checker 比较不使用 equal_nan；可解释 reset 检查冲突。wrapped step info 的失败根因尚未逐字段定位；不能把它与物理不确定性混同。
- Task Lab 缺少 Host/Origin 写入边界，外来 Origin 的 text/plain JSON 请求实际创建了 session。只验证了服务端行为，未用浏览器或 provider 验证攻击链。Explorer 相应边界已有通过的测试。
- 公开仓库 main 已是 0.4.0，并已有 packaged Student Lab、CI、docs workflow、release workflow 和 CITATION；可见 tags 为 v0.2.0/v0.3.0。开发库仍为包 0.2.0，并在 README 指向旧冻结快照。需要区分发行版本、主线开发和科学证据版本，而非把所有功能都列为缺失。
- 公开仓库最近同一 main commit 的 CI 和 Documentation workflow 标为 failure，另一个 Pages build/deployment 成功。job step 细节不可用，失败原因未确立；不能从状态猜测是源码还是基础设施问题。元数据保存在 public-release-status.json / public-ci-jobs.json。
- 模型文档具有成熟度和适用域说明，但操作页列出独立 cool、仪器页列出 quick_assay/phase_probe 等抽象名称，与当前公开 measure IDs 不一致。world-authoring 旧冻结 fork 文档与当前 composition/开发规则需更明确分流。
- 文档账本每次 append 会读取、解析、校验并重写已有全量记录；源码提示长程 I/O 可能按总条数平方增长，本块未做规模基准，不报告已测瓶颈。

### 探针自身的失败与恢复

第一次包装检查在构建成功后将 uv 生成的 dist/.gitignore 当成 tar，产生 tarfile.ReadError。初始脚本保留为 run_checks.initial.py；仅修正探针的文件扩展名过滤，并通过 --continue 使用同一构建产物继续未执行命令。构建没有重跑，物理实验没有发生结果替换。该问题计作探索工具缺陷，不归咎于 ChemWorld。

### 未验证边界

未进行全新依赖安装、Linux/macOS、本地 Python 3.11/3.13+、大规模并发/长时内存、真实浏览器/辅助技术、真实 provider、LLM 上下文压缩后恢复或当前远端公开版的完整运行时测试。已公开 frozen evidence 也没有在本块重新资格认证。完整改良清单见 `COMMUNITY_RELEASE_IMPROVEMENT_PLAN.md`。
