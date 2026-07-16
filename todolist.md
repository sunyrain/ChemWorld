# ChemWorld v0.5 基座完整性与正式实验 Todo

最后更新：2026-07-16

## 目标与边界

本阶段只做两件事：证明当前 backend v0.5 候选基座足够完整、稳定且可辨识；在该基座冻结后，运行可复现、可统计解释的正式方法比较。论文写作、榜单宣传和最终发布必须等待本文件的正式证据门禁通过。

当前固定点如下：15 个注册任务的必需运行路径至少达到有界 `reference_validated`，28 类操作已有事务语义，20 个 provider 已接入正式 runtime，`proxy_allowed=false`，且没有待升级的 `lite` 正式路径。三个共享模块 `reaction_kinetics`、`reactors`、`spectroscopy_instruments` 已完成升级；完整测试曾达到 1261 passed、14 skipped，backend v0.5 release gate 12/12 通过。随后完成的公开 affordance/runtime-domain 审计在六个 serious tasks 的 223 个边界候选上达到 0 finding，并修复了会污染 RL/LLM 评价的耦合可行域与活性相状态错误。这些结果证明“候选基座及当前公开动作边界可运行”，但尚未证明“正式 benchmark 结论成立”。

现阶段仍不得作正式 benchmark 主张：P3 的 PPO/SAC 当前合同训练、单任务真实 LLM 筛选和方法冻结尚未完成，reference evidence 尚未生成，Bench 仍封存，P4–P6 没有正式结果。旧 backend、旧 observation contract 和已暴露 cohort 的结果继续只作诊断，不得因模型文件仍在仓库中而恢复正式资格。

## 当前共享状态（2026-07-15）

| 项目 | 当前事实 | 下一门禁 |
| --- | --- | --- |
| 主线 | 核心主目录已同步并包含最新 RL 反馈；site 由独立团队维护，本任务不修改 | 新工作继续先 claim，方法 owned paths 不交叉；具体证据绑定各自 source commit 而非易漂移的“当前 main”标签 |
| 动作/运行域审计 | `fa546e5` 新增版本化公开 action schema 与确定性离线审计；六个 serious tasks 共采样 223 个公开候选，215 个被验证器接受且 215 个全部提交，schema/validator/runtime/observation 四层 0 finding。修复包括冷却速率跨字段约束、结晶 reaction/seed 前置条件、flow 有效停留时间下界、蒸馏零组分除零、所选相浓度/压力风险一致性；88 项接口/耦合回归与 150 项跨架构回归通过 | 这是新的 backend/action 语义边界，不是性能结果；报告 `runtime-domain-affordance-audit-v0.4.json` 仍声明 `benchmark_claim_allowed=false`。任何新 PPO/SAC/LLM 试点必须绑定 `fa546e5` 或其内容等价后继提交，旧 checkpoint/cell 不得恢复 |
| RL writer | `origin/main@cb23c98` 上 PPO/SAC 的 manifest 0.3、sidecar 0.2、精确 observation hash 与禁止 shape-only compatibility 均通过 4-step 行为探针；4 个定向测试通过，`formal_training_allowed=true` | writer 不再阻塞 Train/Dev，但不等于方法已封存 |
| 旧 SAC | pre-v0.4.8 运行完成 19/20 jobs、产生 99/100 checkpoints、评价 95 个，旧 eligibility 仅 13 个且结晶任务为 0；约 199 万环境步全部标记为 `quarantined_incomplete_stale_contract` | 不恢复、不进入当前 index、不形成 benchmark claim；必须按当前合同重训 |
| 当前 PPO | `89dff507` 干净 source 的 v0.4.12 preflight 已完成 4/4 任务、102,400 训练步和 16 次 exact Dev replay；4/4 任务 operational 且有学习信号，行为完整实验 50→407、trained 主指标观测 414，四任务 step-0/trained runtime/observation domain failure 均为 0，原 crystallization 3+7 缺口已在正式 evaluator 中清零 | `full_matrix_allowed=true` 只表示当前 PPO full-matrix gate 已解锁，不是方法封存或 Bench 结果；先固化正报告，再完成同合同 SAC preflight。20-run PPO 矩阵仍未启动、0 checkpoint 入选、`ppo_method_ready=false` |
| 当前 SAC | `c4497586` 干净 source 的 v0.4.12 preflight 已完成 4/4 任务、102,400 训练步和 16 次 exact Dev replay；4/4 operational、3/4 有学习信号，行为完整实验 57→155、trained 主指标观测 362，四任务 step-0/trained runtime/observation domain failure 均为 0 | `full_matrix_allowed=true` 只解锁 SAC full matrix，不是方法封存或 Bench 结果；蒸馏 trained 单任务 0 主指标观测/0 行为完整实验必须在任务级结果中保留。旧 199 万步与 v0.4.8–v0.4.10 负结果继续隔离，`sac_method_ready=false` |
| 真实 LLM | `4949403` 上 v0.4.10 严格运行 1/6：只启动 `live_llm_a/assigned`，10 operations/requests、0 retry、54,546 input + 13,599 output tokens、0.034620 USD、233.90 s；0 非法动作/前置条件失败/安全违规，完整实验、账本与 10 步零误差回放通过。第 5 步 HPLC 后模型据谱图选择加晶种，第 7 步冷却结晶成功提交；`total_score=0.366305`、`final_best=0.477341`，但单 cell 不是性能比较 | v0.4.10 已冻结为 `benchmark_claim_allowed=false` 的 source-bound 可执行性诊断，不续跑剩余 5 cells。轨迹发现通用 `decision_audit` 漏掉已存在于 agent trace 的公开谱图解读/历史请求字段；`23c9361` 已修复并隔离为 v0.4.11，64 项相关回归通过。该改动曾使旧 operation freeze 正确失配，现已由独立 v0.4.1 freeze 与测试替代。v0.4.11 无 key dry-run 通过；当前不再付费扩矩阵 |
| operation controls | v0.4.1 的 3/3 source-bound freeze、24-cell preflight 与 `ef202b7` 正式开发证据均已闭合。最终报告 288/288 cells、每 cell 40 次完整实验，`formal_operation_baselines_ready=true`；起止 commit 均为 `ef202b7` 且工作树干净，blind/rule 为 0 invalid，operation-random 的 403 次拒绝原样计账，决策审计、主指标、账本与确定性复跑全部通过，未访问 Bench/reference | 第一次启动因主 `.venv` 的 editable package 解析到可变 main，完整报告以 `source_commit_stable=false` 正确拒绝；不得使用。显式固定 worktree `PYTHONPATH` 后只重签同一 source-bound 缓存，最终有效证据为 `operation-baselines-dev-v0.4.1.json`；下一步只接入全局 method freeze |
| classic/主动学习 controls | recipe space 0.3 修复 flow residence/run-duration 耦合后，8/8 freeze 与 64-cell preflight 通过；最终 `ef202b7` 正式开发报告 768/768 cells、每 cell 40 次完整实验，`formal_classic_matrix_ready=true`。八种方法均 0 invalid，账本、确定性与 anytime 曲线通过，五种 surrogate 均实际 fit/acquisition，Safe-GP activation rate=0.8625 | Dev 仅在完整 scope 后选择 design=`lhs`、local search=`greedy_local`、Bayesian optimization=`structured_gp_ucb`、constrained optimization=`structured_safe_gp_ei`；未访问 Bench/reference。首次错误 editable 启动在 767/768 后内存失败且 source 不稳定，不构成证据；最终有效证据为 `classic-dev-v0.4.1.json` |
| RL post-affordance 执行 | v0.4.12 PPO/SAC 均在干净且已推送的 source 上完成 4/4 tasks、各 102,400 步与 16 次 exact Dev replay；PPO 4/4、SAC 3/4 learning signal，行为完整实验分别 50→407 与 57→155。公开 crystallization 的 solubility 起始温度域与最小有效 seed population 后，两算法 step-0/trained 的四任务 runtime/observation failure 全部为 0 | v0.4.10/v0.4.11 负报告保持不可变，v0.4.12 两个 `full_matrix_allowed=true` 仅解锁各自后续执行。PPO/SAC full matrix 尚未启动，必须回到各自 exact source-bound 报告/clean tree 上执行并继续由正式训练入口 fail closed；不得把 preflight 冒充方法结果 |
| 开源 VLM | 确定性谱图图像合同 0.1 已通过审计：PNG/信号/公开包/渲染合同均有摘要，历史目录强制为纯元数据，只有显式取回的历史谱图可进入图像输入；未下载或运行模型；未来推理依赖已从主环境锁隔离 | 推理依赖、模型与 processor revision 尚未封存；仅在 P4 之后先做一个 Dev 任务的学习价值试点，未通过不得扩矩阵 |
| 环境锁 | VLM 临时 extra 已完全移除，`uv.lock` 精确恢复到 VLM 前 `099028d` 的 179 包摘要；但该摘要与 P0 `be4e38f` 的 178 包 portable-release 证明不同，漂移在 VLM 任务之前已由后续 RL 依赖产生 | 不回写历史 P0 报告；待 P3 方法依赖稳定后执行 `benchmark-v05-portable-release-reattestation`，在此之前不得签发正式 Bench source/wheel manifest |
| 正式证据 | `benchmark_claim_allowed=false`，reference/Bench/P4 均未开始 | P3 全部封存并通过 method freeze 后，严格执行 reference → base matrix → independent reproduction |

执行职责固定为“核心组控制、方法组盲执行”：核心组保留协议、Bench commitment、reference、统计代码、cell 签发和最终主张；RL 组负责当前合同 Train/Dev、checkpoint/replay/resource evidence，并可在收到不可变 cell manifest 后执行正式 cell，但不得访问 Bench 参数、reference feedback、事后改指标或删除失败。执行人与控制人分离不要求不同计算机器，但要求不同 owned paths、不可变输入 hash 和独立重放验收。

## 执行制度

- 所有任务遵守 `claims/README.md`：先 claim 并推送 active claim，再修改文件；一个 Task ID 对应一个明确交付。
- 默认 `owned_paths` 是任务边界。需要扩大时先更新 claim；不要同时认领目录父路径和其中子文件。
- 共享协议、runner、正式 manifest 和公开文档由独立 integration task 最后合并。并行任务只写自己的模块、测试和报告。
- 超过约两天的任务按 `原-task-id--slice-序号-名称` 拆分；每个 slice 仍需独立 claim、测试、报告和提交。
- 历史 artifact 不删除、不回写、不改标签。新协议用 `supersedes` 明确降级旧证据，并保留旧 commit、协议 hash 和失败原因。
- 正式 Bench 种子、世界参数和 reference 结果不得用于开发、调参、提示词修改、checkpoint 选择或失败修复。任何泄漏都必须换协议版本和整套未见 cohort。
- 不要求或保存模型私有思维链。LLM 只保留结构化公开决策记录：证据、谱图解释、假设、不确定性、动作、简短理由和适应来源。
- 本地脚本或干净容器即可完成复现，不新增 GitHub Actions。

## 统一证据要求

每个控制报告必须含 schema/version、source commit、dirty-tree 状态、依赖与协议 hash、任务/方法/seed/world cell、运行命令、软硬件信息、通过项、失败项、限制和 `benchmark_claim_allowed`。正式运行还必须绑定 trajectory digest、result digest、backend semantic hash、task contract hash、method/config/checkpoint 或 prompt hash、evaluation hash 与 reference manifest hash。

所有异常默认 fail closed：缺失轨迹、缺失主指标、NaN/Inf、预算超限、provider 失败、token 或价格不可核对、checkpoint 不匹配、回放不一致、重复/缺失 cell、dirty source、自动修复动作、Bench 微调或 seed 泄漏都不能被静默丢弃或按成功运行统计。

正式结果按任务和交互层级报告，不能用一个跨任务总分掩盖失败。至少报告任务主指标、目标分、安全约束、成本、完成率、非法动作、模型/运行时失败、4/8/12/20/40 次完整实验的 anytime 曲线，以及实验数、操作数、测量数、模型调用、tokens、金额、训练步数、CPU/GPU 时间等独立资源轴。

## 阶段门禁

P0 全部通过前不得冻结新协议；P1 全部通过前不得生成正式 reference；P2 全部通过前不得训练或运行正式方法；P3 全部通过且方法封存后，才能解封新 Bench cohort；P4 只做基础正式矩阵；只有 P4 通过的方法家族代表才能进入 P5 泛化实验；P6 通过后才允许更新发布级 benchmark 结论。

## P0：修复协议错误并证明基座完整

- [x] **`benchmark-v05-evidence-quarantine` — 污染 cohort 与旧证据隔离**
  - 默认 owned_paths：`configs/benchmark/evidence_quarantine_v0.5.json`、`scripts/audit_evidence_quarantine.py`、`tests/test_evidence_quarantine.py`、`workstreams/benchmark_v1/reports/evidence-quarantine-v0.5.json`。
  - 依赖：无，必须最先完成。
  - [x] 枚举仓库、`runs/`、报告、文档和 git 历史中所有用过或被查看过的 Train/Dev/Bench/reference seeds 与 world cells。
  - [x] 将 `20–39`、`300–319` 及其派生结果标记为 `diagnostic_only`；解释 `primary-0.3` 绑定旧 `lite` maturity/backend 的事实，禁止重命名为 v0.5 正式结果。
  - [x] 建立机器可读 denylist，正式 runner 在检测到污染 seed、旧 backend、旧 evaluator 或旧协议时直接拒绝启动。
  - [x] 检查文档不再把 `300–319` 称为 fresh/confirmatory；保留其诊断价值但移除正式措辞。
  - 结果：协议 0.4 建立前的 280-seed 暴露清单作为不可变、hash-bound 冻结快照，单独证明新公共命名空间在选定时未被使用；当前累计扫描覆盖 51 份公开配置与 105 个历史配置 blob，隔离 502 个已暴露 seed 和 120 个 world-cell 身份，供以后所有 runner 拒绝复用。旧 `primary-0.3` 的 160 份结果与 160 个轨迹身份由两个冻结 manifest 摘要承诺，绑定 `lite` maturity 并统一标记为 `pre-v0.5_diagnostic_only`。干净 clone 不再依赖被忽略的 `runs/` 才能执行隔离测试；原始文件存在时会额外核对数量、seed 网格、maturity、replay 与两个摘要，主工作区 160/160 原始工件已反向验证通过。正式 guard 对暴露 seed、旧协议、非 claimable 协议、缺失 backend semantic hash 或私有 seed commitment 全部 fail closed，且没有 force override。
  - 验收：扫描覆盖所有保留 artifact；任一正式配置引用 denylist 即测试失败；报告明确 `benchmark_claim_allowed=false`。

- [x] **`foundation-v05-contract-coherence` — task/world/score/reference/method 协议一致性收口**
  - 默认 owned_paths：`configs/foundation/contract_coherence_v0.5.json`、`scripts/audit_contract_coherence_v0.5.py`、`tests/test_contract_coherence_v0_5.py`、`workstreams/world_foundation/reports/contract-coherence-v0.5.json`。
  - 依赖：`benchmark-v05-evidence-quarantine`。
  - [x] 从注册任务生成唯一合同图：task → operation → provider → observation → primary metric → risk/cost → world axes → evaluator → replay schema。
  - [x] 检查六个严肃任务、四个 core 角色与两个 exploratory 角色在所有协议中同源；消除 `20–39` 与 `300–319`、方法别名、`greedy`/`greedy_local` 等漂移。
  - [x] 检查单位、方向、预算、失败、终止、测量和 final assay 语义不存在重复真相源。
  - [x] 对 protocol/model/checkpoint/backend hash 建立兼容矩阵，拒绝“schema 相同但语义不同”的 artifact。
  - 结果：六任务合同图与 15-task runtime reachability 同源，四个 formal-core 与两个 exploratory 角色精确对齐；12 个正式方法 ID、9 个 legacy runner alias 和两个排除 stub 已分层。任务主指标、final-assay、风险/成本、资源失败、版本与成熟度控制全部通过，三份旧 seed 协议只允许从 quarantine 读取。backend semantic hash 由后续 portable-release gate 生成，在此之前仍保持 `benchmark_claim_allowed=false`。
  - 验收：所有正式配置可由同一 manifest 解析；不存在未注册 task/method/provider、悬空依赖或不一致 seed grid。

- [x] **`foundation-v05-composed-runtime-stress` — 完整基座组合压力与回放测试**
  - 默认 owned_paths：`configs/foundation/composed_runtime_stress_v0.5.json`、`scripts/run_composed_runtime_stress.py`、`tests/test_composed_runtime_stress.py`、`workstreams/world_foundation/reports/composed-runtime-stress-v0.5.json`。
  - 依赖：合同一致性完成；不得修改 provider 实现，发现缺陷另开 fix slice。
  - [x] 覆盖 15 tasks × 28 operations × 所有必需 provider 的可达组合，包含标称点、边界、近边界、非法输入、重复调用和强制求解失败。
  - [x] 对反应—反应器—传热—相平衡—分离—仪器的组合链验证质量/能量/电荷守恒、非负性、单调趋势和 ledger 一致性。
  - [x] 对同 seed 同动作逐字节回放；对进程重启、批量/单次执行和 Windows/干净环境比较确定性及声明容差。
  - [x] 统计每个 task/world cell 的 solver failure、domain failure、NaN/Inf、回滚和超时率，不以重试掩盖失败。
  - 结果：15 tasks、28 operations、20 providers 与 163 个允许的 task-operation pairs 全部可达；45 个 lower/nominal/upper profiles 共执行 381 steps，runtime/constitution/precondition/nonfinite-observed failure 均为 0，同 seed digest 全部一致。六条反应/纯化/结晶/蒸馏/流动/电化学/平衡组合链全部提交并回放。临时 clean wheel 在独立 Windows 进程中重跑完整矩阵，45 profiles 与六条链的 digest 和 source 运行逐项一致。
  - 验收：所有声明域内 cell 通过，声明域外均显式 fail closed；正式 core task 不存在 fallback、proxy、`lite` 或静默 clip 路径。

- [x] **`foundation-v05-observation-identifiability` — 谱图与公共观测可辨识性/泄漏验证**
  - 默认 owned_paths：`configs/foundation/observation_identifiability_v0.5.json`、`scripts/audit_observation_identifiability_v0.5.py`、`tests/test_observation_identifiability_v0.5.py`、`workstreams/world_foundation/reports/observation-identifiability-v0.5.json`。
  - 依赖：组合压力测试的稳定观测链。
  - [x] 验证 UV/Vis、IR、NMR、HPLC/GC、pH 等公开信号随相关状态变化，噪声/漂移/LOD/LOQ 下仍有合理但非完美的辨识能力。
  - [x] 建立 `assigned`、`unassigned`、`masked` 三种条件；除谱图字段外，配对观测必须完全相同。
  - [x] 用无答案泄漏的简单 probe 检查观测对任务主指标/机制族有信息，同时不能直接恢复 hidden state、private seed、provider 参数或模型身份。
  - [x] 验证历史谱图只在 agent 主动请求后返回，访问、失败和成本进入 ledger；不预先塞入全部历史。
  - 结果：HPLC、GC、NMR 在预注册状态对上达到 pairwise identifiability，UV/Vis 与 IR 显式呈现弱分离区；五种谱图在低信号域均正确退化，pH 对 8.4 pH 状态差可分而 0.014 pH 低对比低于 0.06 LOQ。assigned/unassigned 共享完全相同 raw curve，三条件非谱图 context hash 一致且 masked 不含信号；公开报告无 secret/hidden/private/provider 泄漏。历史 archive 只公开无信号 catalog，显式 ID 请求后才返回 packet，成功和 unknown-ID 失败均写入成本 ledger。
  - 验收：每种仪器均有灵敏度、特异性、退化区和泄漏报告；assigned/masked 配对能被精确回放。

- [x] **`foundation-v05-task-validity-power` — 主指标、风险和预算的动态范围/统计功效验证**
  - 默认 owned_paths：`configs/foundation/task_validity_power_v0.5.json`、`scripts/run_task_validity_power_v0.5.py`、`tests/test_task_validity_power_v0.5.py`、`workstreams/world_foundation/reports/task-validity-power-v0.5.json`。
  - 依赖：组合压力和观测可辨识性完成。
  - [x] 对四个 core task 绘制冻结 response surface，验证主指标方向、非平凡最优区、局部结构、机制变化和可达到的 SESOI。
  - [x] 验证风险阈值既非永不触发也非几乎必触发；成本指标对真实操作/测量变化敏感且不重复计费。
  - [x] 用与正式方法无关的 policy probes 检查随机、局部、信息利用、风险盲四类行为可被指标区分。
  - [x] 预估 20 paired seeds 对主效应、安全/成本非劣与谱图消融的功效；不足时在解封 Bench 前调整样本量，而不是事后改门槛。
  - 结果：四个 core task 各运行 5 Dev seeds × 12 recipes，主指标 spread 为 0.499275、0.734407、0.375185、0.106557，冻结 SESOI 为 0.024964、0.036720、0.020000、0.020000；主指标方向、最优区和四类非方法行为 probe 均可区分。v0.5 分位校准使四任务风险触发率均为 0.20、process-cost 触发率均为 0.10；旧协议的结晶风险 0% 触发和分配成本 100% 触发被明确 supersede。20 paired seeds 对部分目标效应足够，但在 8 个同时比较、5% 非劣 margin 下，即使零额外失败也至少需 99 pairs；结合配对成本方差，protocol 0.4 的最低建议冻结为 100 paired seeds。
  - 验收：每个 core task 都有可辨识目标、安全—性能或成本—性能权衡和预注册 SESOI；否则降级为 exploratory。

- [x] **`foundation-v05-portable-release` — 可移植环境、依赖锁与 backend 语义冻结**
  - 默认 owned_paths：`configs/foundation/portable_release_v0.5.json`、依赖锁文件、`scripts/build_portable_release_v0.5.py`、`tests/test_portable_release_v0.5.py`、`workstreams/world_foundation/reports/portable-release-v0.5.json`。
  - 依赖：以上 P0 任务全部完成。
  - [x] 固定 Python 与关键数值/ML 依赖，构建 clean wheel；记录 CPU/GPU、BLAS、CUDA 和求解器版本。
  - [x] 将 backend semantic hash 与 docs/site commit 分离，避免只改文档就令正式轨迹失效，也避免语义改动逃逸版本更新。
  - [x] 在 Windows 干净环境本地运行 golden/replay；Linux clean-wheel 复核降为非阻断的后续可选验证，不作为当前 P0/P1 门禁。
  - [x] 重跑完整 pytest、ruff、mypy、strict docs、release gate、clean-wheel smoke 和 P0 控制报告。
  - 结果：`uv.lock` 已锁定 178 个包；193 个 backend 语义文件与 docs/site 分别计算独立摘要。Windows clean wheel 在隔离目录和独立进程精确复现 45 个 profile、381 步与 6 条组合链。完整本地 release gate 12/12 通过：ruff、265 个源模块 mypy、1302 passed/14 skipped、89% coverage、strict docs、wheel smoke、reference validation、45 行环境一致性、runtime boundary、20-provider/28-route reachability、baseline smoke 与 candidate integrity 均通过。门禁还捕获并修复了 composed stress audit 对七槽参考夹具名称的越界耦合，以及长门禁期间 HEAD 漂移仍被误报成功的并发漏洞；最终门禁起止均绑定 `be4e38f`、`source_commit_stable=true`、工作树干净。按当前推进决策，Windows 是 P0 必需平台，Linux 作为透明记录的非阻断后续复核；manifest 已进入 `formal_candidate`，但正式算法结果仍须经过 P1–P6，`benchmark_claim_allowed` 继续为 false。
  - 验收：生成唯一 `backend-v0.5-formal-candidate` manifest；任一门禁失败则不得进入 P1。

## P1：冻结新的正式协议与未见数据边界

- [x] **`benchmark-v05-formal-protocol-0.4` — 新 cohort 与主张边界预注册**
  - 默认 owned_paths：新版本 `configs/benchmark/*_v0.4.json`、`scripts/audit_formal_protocol_v0.4.py`、`tests/test_formal_protocol_v0.4.py`、`workstreams/benchmark_v1/reports/formal-protocol-v0.4.json`。
  - 依赖：P0 全部通过。
  - [x] 由污染清单之外生成新的 Train/Dev/reference-search/Bench namespaces；实际 Bench base seeds 与 world parameters 只写入受控私有 manifest，公开协议只提交 commitment/hash。
  - [x] 四个 core task 用于正式结论；electrochemical/equilibrium 保持 exploratory，除非 P0 validity gate 单独证明可升级。
  - [x] 冻结 40 次完整实验预算、4/8/12/20/40 checkpoints、world axes、失败策略、停止规则和禁止 Bench 微调规则。
  - [x] 明确 primary、secondary、ablation 和 exploratory estimands；任何协议变更都必须升级版本并废弃变更后的旧 cohort。
  - 结果：Train/Dev/reference-search 分别冻结 100/20/100 个全新公开种子且与 P0 的 280 个污染种子不相交；Bench 在 Git 私有区一次性封存 100 个配对身份，每个身份绑定四个 core task、两条任务世界轴与四种干预模式（32 个世界分配），公开仓库和审计报告只保留 SHA-256 承诺 `dc7888fa…2b8f5b7`、计数和状态，不包含 seed 或世界参数。协议同时哈希绑定六项 P0 证据、portable backend 语义、任务 SESOI/风险/成本阈值，并将 0.1–0.3 全部限定为 diagnostic；14 个篡改/泄漏/重叠/版本失配测试与 30 个相邻边界测试通过。
  - 验收：协议审计可证明所有 split 不相交、Bench 未被运行/查看、旧 0.1–0.3 全部为 diagnostic。

- [x] **`benchmark-v05-interaction-strata` — recipe 与 operation 级公平比较合同**
  - 默认 owned_paths：`configs/benchmark/interaction_strata_v0.4.json`、`src/chemworld/eval/interaction_strata.py`、`tests/test_interaction_strata.py`、`workstreams/benchmark_v1/reports/interaction-strata-v0.4.json`。
  - 依赖：formal protocol 0.4。
  - [x] 建立 recipe-level track：random、LHS、greedy、GP/RF/Safe-GP，只在完整实验之间更新。
  - [x] 建立 operation-level track：operation-random、observation-blind、rule-based、RL、LLM，可在实验内适应并按需读谱。
  - [x] 不把两个 track 的差异冒充算法优劣；另外给出 system-level comparison，完整披露能力差异和 harness assistance。
  - [x] 冻结实验、操作、测量、模型调用和训练计算的并列预算/资源账本，不做单一资源标量化。
  - 结果：冻结 8 个 recipe-level 与 7 个 operation-level 方法声明，分成 recipe 设计/搜索、operation affordance controls、公共状态控制和谱图 LLM 四个比较块；跨 track 仅允许 system-level 描述且禁止合并排名。每个方法均声明观测集、谱图/历史谱图能力、适应层级、action affordance、更新边界、实现状态及 harness assistance，其中 recipe 编译器、operation mask/decoder 和 LLM JSON 校验均显式披露。完整实验、操作、测量、决策、API 请求/重试、tokens、金额、拟合/采集优化、训练步数、CPU/GPU/wall time 共 15 条资源轴并列记录，不标量化；23 个定向和相邻合同测试通过。
  - 验收：每个方法声明 decision scope、可见观测、谱图能力、适应层级和自动化帮助；缺失声明无法注册。

- [x] **`benchmark-v05-statistical-analysis-plan` — 正式统计与失败处理方案**
  - 默认 owned_paths：`configs/benchmark/statistical_analysis_plan_v0.4.json`、`src/chemworld/eval/formal_statistics.py`、`tests/test_formal_statistics.py`、`workstreams/benchmark_v1/reports/statistical-analysis-plan-v0.4.json`。
  - 依赖：task validity/power 与 interaction strata。
  - [x] 冻结 paired estimand、bootstrap/随机化检验、置信区间、Holm 多重比较、SESOI 和安全/成本非劣界限。
  - [x] 主结论要求目标改善、达到 SESOI、安全非劣、成本非劣和全部回放同时成立；不以总分替代联合规则。
  - [x] 失败运行保留在分母，并分别报告 invalid action、provider/model failure、runtime failure、budget overrun 和 incomplete accounting。
  - [x] 冻结 family champion 选择规则，只允许 Dev 选型；Bench 不做超参数、提示词或 checkpoint 选择。
  - 结果：100 个 opaque paired identities 上冻结 task-level paired percentile bootstrap（20,000）、sign-flip randomization（100,000）、四 core task 内 Holm、任务 SESOI，以及 8 个安全/成本同时比较对应的 0.99375 单侧上界和 5% 非劣 margin。首要对比限定为 masked 条件下 Dev 选出的 operation champion 对 operation-random；其他 recipe/RL/LLM 家族为独立 secondary，不挤占 P0 功效假设。成功必须同时通过正向区间、Holm、SESOI、安全/成本非劣、完整矩阵、全部 replay 和完整 accounting；失败按五类保留在 100-pair 分母。null 不通过、positive 4/4 通过、unsafe/cost-regressing 目标虽通过但联合失败、单个 failed run 仍保持 100 分母且联合失败；24 个新旧相邻统计测试通过。
  - 验收：用纯合成 null/positive/unsafe/cost-regressing fixtures 证明 false positive、功效和失败处理符合协议。

- [x] **`benchmark-v05-reference-plan-0.4` — 独立 reference portfolio 重建计划**
  - 默认 owned_paths：`configs/benchmark/reference_portfolio_v0.4.json`、`configs/benchmark/reference_regret_v0.4.json`、`tests/test_reference_portfolio_v0.4.py`、`workstreams/benchmark_v1/reports/reference-plan-v0.4.json`。
  - 依赖：formal protocol 与统计方案冻结。
  - [x] 绑定新 reference-search split、新 seed namespace、backend/evaluator hash 和四个 core task，彻底移除旧 `20–39`。
  - [x] reference builder 身份不得与任一被评方法重合；其训练、搜索、轨迹和随机数流独立。
  - [x] 每个 task × seed × metric 至少四个独立 source runs；冻结 best-known estimate 与不确定区间，明确“不是 oracle、允许被方法超过”。
  - [x] 在任何方法 Bench 评分前冻结完整 manifest；后续更新 reference 必须新版本并重算所有方法。
  - 结果：reference 目标绑定同一私有 Bench task/pair/world cell，但 builder RNG 来自全新 `12000–12099` reference-search namespace，实际 Bench seed 始终只在私有 manifest 中解析。精确计划含 4 tasks × 100 opaque pairs × 2 metrics = 800 reference cells、每 cell 四个独立 source、共 1,600 个唯一 run/RNG、64,000 次完整实验、3,200 条 source-metric 记录和最多 640,000 个 operation；独立 builder 已实现 space-filling、ensemble-surrogate、evolutionary 与 risk-aware 四种归一化搜索 profile，不导入 evaluated agent/RL/provider 命名空间。builder 源码摘要与 15 个被评方法逐项 canonical adapter 摘要均已 hash-bound，并验证身份、代码和 RNG 分离。estimate 是带 20,000 次 bootstrap 区间的 empirical best-known，不是 oracle；负 regret 保留。任何缺失 source、replay/accounting/digest 失败都会阻止方法 Bench 评分，完整 reference manifest 必须先冻结。
  - 验收：run plan 可枚举精确 cell/run 数和预计资源；仍保持 `formal_results_present=false`。

## P2：统一正式执行基础设施

- [x] **`benchmark-v05-cell-runner` — 可恢复、幂等的单 cell 执行器**
  - 默认 owned_paths：`src/chemworld/eval/formal_runner.py`、`scripts/run_formal_cell.py`、`tests/test_formal_runner.py`、`workstreams/benchmark_v1/reports/formal-runner-controls-v0.4.json`。
  - 依赖：P1 协议冻结。
  - [x] 统一 task × method × seed × world × spectrum-condition cell，支持 classic、RL checkpoint 和 live LLM adapter factory。
  - [x] 每个 cell 原子写入 manifest、trajectory、result、failure artifact 和完成标记；中断后只重跑未完成/校验失败 cell。
  - [x] 同一 cell 重复启动必须返回相同 identity 或拒绝覆盖；不得把半成品当成功，不得自动补动作或 final assay。
  - [x] 每个输出绑定全部协议/代码/checkpoint/prompt/reference hashes，并立即独立回放验证。
  - 结果：正式 cell 只能从摘要校验通过的 issued run manifest 解析，classic/RL/live-LLM 三类 adapter 分别强制绑定 method artifact、checkpoint 或 prompt/model-config hash；私有 method/world seed 与世界扰动经 commitment 校验后才进入 adapter。执行采用 OS cell 锁、隔离 staging、逐文件短名原子写入、精确 artifact 白名单与整目录发布，完成标记最后落盘；中断和磁盘错误仅留下不可聚合 staging，重复 cell 命中已校验缓存，并发重复被拒绝，已发布 digest 篡改拒绝覆盖。轨迹逐条绑定 task/method/pair/spectrum/cell/world-seed，公开 result 去除 raw seed，仅保留 opaque pair 与 commitment；真实环境轨迹即时独立 replay 通过。26 项 runner 测试和 98 项相邻协议/统计/replay 回归通过，并覆盖 API timeout、坏 JSON、nonfinite、预算越界、账本缺失、错 cell、manifest/额外文件篡改和私有值泄漏。
  - 验收：故障注入覆盖进程中断、磁盘不完整、API 超时、坏 JSON、重复 cell、digest 篡改和预算超限。

- [x] **`benchmark-v05-matrix-orchestrator` — manifest 驱动的并行矩阵编排**
  - 默认 owned_paths：`src/chemworld/eval/formal_matrix.py`、`scripts/run_formal_matrix.py`、`tests/test_formal_matrix.py`、`workstreams/benchmark_v1/reports/formal-matrix-controls-v0.4.json`。
  - 依赖：cell runner。
  - [x] 由冻结 manifest 展开预期 cell，不在 CLI 手写 tasks/seeds；启动前输出 cell 数、CPU/GPU/API 队列和费用上限。
  - [x] CPU 方法使用进程级并行；GPU 训练/推理按设备独占或声明配额；LLM 使用速率限制与可恢复队列。
  - [x] 进度实时展示 queued/running/succeeded/failed/replay-verified，以及每个任务、方法和预算检查点；不得显示隐藏状态或私有 seed。
  - [x] 聚合前检查完整笛卡尔积、成对条件、失败分母和资源账本；缺一 cell 就只产出 incomplete 报告。
  - 结果：矩阵只能由 digest 校验通过的 issued manifest 展开精确 task × method × opaque-pair × spectrum-condition 笛卡尔积，CLI 不接受手写任务或 seed。classic 使用 CPU 进程池，RL 使用带显式设备槽和配额校验的 GPU 进程池，live LLM 使用有并发、cell 启动速率和费用上限的可恢复线程队列；停止后只补缺失 cell。公开 JSONL 进度覆盖 queued/running/checkpoint/succeeded/failed/replay-verified，并拒绝私有 seed/world 字段。聚合逐 cell 复验 artifact、replay、配对 commitment、失败分母以及账本 schema、预算、checkpoint、时间、用量和在线模型溯源；缺失、额外或伪造账本均只产出 incomplete。11 项矩阵测试及 109 项 runner/协议/统计/replay 联合回归通过，串并行 semantic digest 一致。
  - 验收：小型 smoke matrix 可停止、恢复、并行和复算，结果与串行执行等价。

- [x] **`benchmark-v05-resource-accounting` — 方法资源与 API 成本 fail-closed**
  - 默认 owned_paths：`src/chemworld/eval/resource_accounting_v0_4.py`、`tests/test_resource_accounting_v0_4.py`、`workstreams/benchmark_v1/reports/resource-accounting-v0.4.json`。
  - 依赖：cell runner；可与 orchestrator 并行。
  - [x] 区分环境操作、完整实验、测量、决策、provider requests/retries、tokens、金额、训练步数、CPU/GPU 与 wall time。
  - [x] DeepSeek usage 缺失、价格版本不匹配或失败请求无法计费时，保留轨迹但标记 accounting failure；不得估成零。
  - [x] RL checkpoint 记录训练总资源并与多个评估 cell 分开报告；classic 方法记录拟合/采集优化时间。
  - [x] 防止重复计费、缓存命中误算、重试漏算、并行 wall time 相加冒充 elapsed time。
  - 结果：正式资源协议固定 15 个不做标量化的资源轴及 count/token/USD/second/environment-step 量纲。live LLM 按每次 provider attempt 的唯一 request、逻辑决策、连续 retry index、成功/失败状态、完整 usage、cache hit/miss token、可计费状态和 digest 绑定价格逐笔重算，并与累计 ledger 精确对账；缺 usage、价格版本错、失败请求不可计价、账单不符或重复 request 时保留 cell 但金额为 null 且禁止聚合，绝不按零处理。classic 的 fit/acquisition 事件计数并声明为总 CPU/wall 的组成量，防止二次相加；RL 训练按唯一 checkpoint 单列，多个评估 cell 只引用一次，评估账本出现训练步数或无关训练 artifact 均失败。method identity 已绑定 resource profile，runner 生成独立 digest-indexed `resources.json`，matrix 强制消费全部 cell 与 checkpoint 账本并使用实测 matrix elapsed，不能把并行 cell wall time 求和冒充耗时。11 项专项、51 项 runner/matrix/resource 联合和 147 项扩展回归通过，实际 ChemWorld smoke 轨迹 15 轴无缺失精确对账。
  - 验收：合成账单和实际 smoke run 对账精确；所有 required ledger 字段非缺失且量纲正确。

- [x] **`benchmark-v05-preflight-gate` — 正式运行总门禁**
  - 默认 owned_paths：`scripts/run_formal_preflight.py`、`tests/test_formal_preflight.py`、`workstreams/benchmark_v1/reports/formal-preflight-v0.4.json`。
  - 依赖：P2 其他任务全部完成。
  - [x] 同时检查 clean source/wheel、backend manifest、协议 hashes、seed denylist/split、reference 状态、method registration、checkpoint/prompt、预算和磁盘/算力/API 配额。
  - [x] 生成唯一 run manifest 和不可变 run ID；正式 runner 只接受已签发 manifest。
  - [x] 任何缺失或不一致都返回非零并列出准确修复项，不允许 `--force` 绕过。
  - 结果：preflight 只接受 clean Git commit 对应的 digest-bound wheel 与 clean-build/dependency-lock manifest，逐项复验 backend、formal/interaction/statistics/reference/method、runner、matrix 和 resource controls，并交叉绑定 cell 的 protocol/backend/evaluator/reference hashes。方法声明必须与 hash-bound interaction registration、resource profile 和 spectrum conditions 一致；RL checkpoint 与独立训练账本、LLM prompt/model config/价格版本、classic artifact 均进入 identity 或 manifest binding。私有 pair assignment 单独输入，seed 同时对照 formal protocol 中的 train/dev/reference-search 区间和额外 denylist，公开 manifest/report 只保留 commitment；private runtime 先发布，唯一随机 issuance nonce 参与 run ID，manifest 最后发布且拒绝覆盖。门禁按 cell 数校验磁盘估算，并校验 CPU、GPU device、API credential presence、并发、cell/provider rate 和费用配额；失败仅输出具体 blocker 且不签发，CLI 无 `--force`。使用 15 个正式方法 ID 的 contract adapters 覆盖两个 track 和 LLM assigned/masked，共 17 个非正式 cell，17/17 即时 replay 且资源聚合完整；14 项专项与 161 项扩展回归通过。该 smoke 只证明门禁/调度/回放管线，不是方法性能；真实 formal Bench 仍会因 P3 method freeze 和 reference evidence 未完成而正确拒绝。
  - 验收：全方法 × 两个交互 track × assigned/masked × 小 seed 的 smoke grid 100% 轨迹回放通过；报告仍为非正式。

## P3：开发、验证并封存方法

- [x] **`benchmark-v05-classic-adapters` — 经典与主动学习基线封存**
  - 默认 owned_paths：各 classic adapter、对应测试、`configs/methods/classic_v0.4.1/`、`workstreams/benchmark_v1/reports/classic-dev-v0.4.1.json`；v0.4 同名资产只作历史证据。
  - 依赖：P2 preflight。
  - [x] 注册 random、LHS、greedy local、typed structured GP-EI/PI/UCB、RF-EI、Safe-GP；材料类别必须 one-hot/typed，禁止数字代号产生伪距离。
  - [x] v0.4.1 preflight 在 Train/Dev 检查采集函数确实进入优化阶段、Safe-GP 约束被激活、预算曲线非退化和确定性回放；64/64 cells 完成、全部方法 0 invalid，Safe-GP activation rate=0.75。预检的 diagnostic leaders 不进入选择字段。
  - [x] 在当前 v0.4.1 source 上完成 4 Train + 20 Dev seeds、4 tasks、8 methods、每 cell 40 次完整实验的 768-cell 重认证；最终报告绑定干净稳定的 `ef202b7`，768/768 cells、30,720 次完整实验全部闭合，八种方法 0 invalid，完整 Dev scope 才产生 family champions。
  - 结果：v0.4.1 选择 design=`lhs`、local search=`greedy_local`、Bayesian optimization=`structured_gp_ucb`、constrained optimization=`structured_safe_gp_ei`；Safe-GP constraint activation rate=0.8625。旧 v0.4 同名结果只作历史实现证据，不进入当前方法冻结；当前证据为 `classic-dev-v0.4.1.json`。
  - 验收：每种方法的能力、失败域、复杂度和资源 ledger 完整；不使用 Bench/reference 反馈。

- [x] **`benchmark-v05-operation-baselines` — operation-level 盲控制与规则基线封存**
  - 默认 owned_paths：operation baseline adapter、`configs/methods/operation_v0.4.1/`、对应测试与 `workstreams/benchmark_v1/reports/operation-baselines-dev-v0.4.1.json`；v0.4 同名资产只作历史证据。
  - 依赖：P2 preflight 与 interaction strata。
  - [x] 实现 operation-random、observation-blind 与 rule-based，三者只使用声明的公开 affordance/观测，不读取 hidden state 或私有 Bench。
  - [x] 固定 terminal assay 活性、动态操作边界和 closeout 预算，禁止 runner 静默修复；随机负控制的非法尝试必须保留并计账，盲控制与规则基线必须为零非法操作。
  - [x] v0.4.1 冻结与 24-cell preflight：三种 method artifact/source binding 全部 ready；1 个 Train seed + 1 个 Dev seed × 4 tasks × 3 methods × 2 complete experiments 全部完成，回放、账本、决策审计、动作多样性和规则测量适应全部通过。12-process runner 固定每 worker 1 个 numeric thread 后无 OpenBLAS 资源错误；报告保持 `development_diagnostic_only`，不冒充正式矩阵。
  - [x] 在当前 v0.4.1 source 上完成 4 个 core task、4 个 Train seed、20 个 Dev seed、每 cell 40 次完整实验的 288-cell 开发重认证；最终报告绑定干净稳定的 `ef202b7`，blind/rule 零非法、random 的 403 次 rejection 原样计账，确定性回放、决策审计、主指标和资源账本全部闭合。
  - 结果：旧 v0.4 的 1,563 次 random invalid 只作历史实现证据；当前 v0.4.1 正式开发证据为 `operation-baselines-dev-v0.4.1.json`，三种方法各 96 cells，未使用 Bench/reference feedback。
  - 验收：三种方法的 freeze、source/hash-bound adapter、完整开发证据和 interaction registration 均已进入 fail-closed method-freeze 审计。

- [ ] **`benchmark-v05-rl-adapters` — PPO/SAC 正式适配、训练与 checkpoint 封存**
  - 默认 owned_paths：各 RL formal adapter、对应测试、`configs/methods/rl_v0.4/`、checkpoint manifests、`workstreams/benchmark_v1/reports/rl-dev-v0.4.json`。
  - 依赖：P2 preflight；PPO 旧 5-seed gate 仅作起点。
  - [x] PPO 使用原生 masked categorical + conditional parameters；SAC 保留连续 latent，并明确只作 system-level comparison、通过同一 public affordance/action decoder。
  - [ ] 在 Train worlds 训练多个预注册 seeds，在 Dev worlds 选择 checkpoint；验证四个 core task 的行为完成，不只验证 flow。
  - [ ] 记录学习曲线、训练步数、GPU/CPU、失败率、quick-close、观察盲控制和 checkpoint/backend/observation/action/reward hash。
  - [ ] Bench 前冻结每个任务或共享策略的选择规则；禁止 Bench 微调和事后选 seed。
  - [x] 共享训练 writer 已写出 final manifest 0.3 与周期 sidecar 0.2，并绑定精确 task-specific observation hash；PPO/SAC 4-step 探针均通过当前 reader。
  - [x] PPO 完成当前合同 step-0 versus trained preflight；门禁因并非所有任务 operational 而以负结果关闭，完整矩阵未启动。
  - [x] SAC 完成同等 current-contract step-0 versus trained preflight；仅 1/4 任务有学习信号、完整实验数下降且 runtime-domain failures 大幅增加，门禁以负结果关闭，完整矩阵未启动。
  - [x] v0.4.9 post-affordance 计划与 runner 已预注册：PPO/SAC 使用独立 writer gate、artifact/report namespace，正式入口对两者对称 fail closed；job resume 绑定 plan hash + source commit，报告前再次检查 source/clean tree。旧 v0.4.8 负结果及产物保持不可变。
  - [x] 保留 PPO v0.4.9 的零训练步基础设施失败：唯一启动任务仅产生 step-0 checkpoint，0 个训练步、0 次 Dev evaluation、0 个结果指标；错误为 Windows 子进程导入 `nvrtc64_130_0.alt.dll` 时的 `WinError 1455`，不得解释为 PPO 性能结果，也不得删除后原路径静默重跑。
  - [x] 完成 SAC v0.4.9 四任务 preflight：102,400 训练步，全部 checkpoint/合同/重复回放与 source-stability 检查通过；但 0/4 学习信号、行为完整实验 13→0、runtime-domain failures 47→428，门禁正确禁止完整矩阵。step-0 已在三任务出现 runtime failure，结合轨迹操作分布将结果定性为共享 adapter 诊断，不冒充 SAC 算法结论。
  - [x] 修复共享 RL public-schema adapter 并预注册 PPO/SAC v0.4.10：动态 choices、state-dependent bounds 与公开 cross-field constraints 进入确定性 decoder，float32 精确端点也落在公开包含/排他边界内；任务、split、seed、25,600-step 预算、超参数、Dev evaluator、SESOI 与通过门槛不变。四任务 64-step seeded walks 和所有当前可用操作的 `-1/+1` 端点均 0 validation failure。Windows PPO 保持 8 个有序 vector slots 与 subprocess 边界，但用单个 spawn worker 承载全部 slots；8-env 训练 smoke 与 DummyVecEnv 固定 seed/slot 的 4 步 observation/reward/done/info 完全一致，134 项 adapter、runner、writer、公开 schema 与 runtime 联合回归通过。
  - [x] 在 `4c34e8c` 干净 source 签发 adapter 0.2 writer gate，并先单独完成 PPO v0.4.10 `partition-discovery`；随后四任务均完成精确步数、checkpoint 合同和双重 Dev replay。Windows 单 spawned worker + 8 vector slots 全程稳定，4/4 有学习信号，但 crystallization 与 distillation 的公开 validator/runtime operational 缺口令聚合门禁 fail closed，完整矩阵未启动。
  - [x] 修复并版本化 v0.4.10 新暴露的公共前置条件：`cool_crystallize` 只在扣除 seed 后仍有正目标进料时可用；`measure` 必须满足所选仪器采样体积，终止后只允许 final assay。conditional hybrid action 合同升至 0.3；PPO/SAC v0.4.11 新 namespace/preflight/full-matrix fail-closed plan 已预注册，且阈值、split、seed、超参数和 SESOI 未修改。
  - [x] 在 `ab62d3f` 干净且已推送的 source 上重签 writer gate 并完成 PPO v0.4.11：4/4 学习信号、102,400 步和 16 次 exact replay 均通过，但 crystallization step-0 的 10 次 runtime-domain failure 令 `all_tasks_operational=false`；负结果已固化，SAC/full matrix 未启动。
  - [x] 修复并版本化 v0.4.11 剩余的两项公共结晶域：`cool_crystallize` 的起始温度必须落在 250–430 K solubility 有效域内；已有正 seed charge 必须达到固定 runtime 粒径/密度下的最小有效粒子数。conditional hybrid action 合同升至 0.4，PPO/SAC v0.4.12 preflight 与 full-matrix fail-closed plan 均已预注册，科学合同与门槛保持不变。使用 v0.4.11 step-0 checkpoint、原 Dev cohort/sampler/policy seeds 的 1,200-step 精确只读复现已把 crystallization runtime-domain failure 从 10 降至 0；PPO/SAC 计划、正式训练入口与结晶耦合定向回归通过。
  - [x] 在干净且已推送的 `89dff507` v0.4.12 source 上签发 PPO/SAC writer gate，并先完成 PPO step-0 versus trained preflight：4/4 tasks operational、4/4 learning signal、102,400 步、16 次 exact replay、行为完整实验 50→407、trained 主指标观测 414，所有 runtime/observation domain failure 为 0；`ppo_v0412_preflight_passed_full_matrix_allowed`。
  - [x] 固化并推送 PPO v0.4.12 正报告后，在 `c4497586` 干净 source 完成同合同 SAC step-0 versus trained preflight：4/4 operational、3/4 learning signal、102,400 步、16 次 exact replay、行为完整实验 57→155、trained 主指标观测 362，所有 runtime/observation domain failure 为 0；`sac_v0412_preflight_passed_full_matrix_allowed`。蒸馏 trained 的 0 主指标观测/0 行为完整实验作为任务级限制保留，聚合门禁因其他任务提供 362 次观测且总行为不降而通过。
  - [ ] 固化 SAC v0.4.12 正报告；在各自 exact source-bound preflight report 与 clean tree 上依次执行 PPO/SAC 四任务五 seed full matrix，封存 checkpoint index、资源账本和确定性重放，未完成前 `ppo_method_ready=false`、`sac_method_ready=false`。
  - [ ] 只有各自 preflight 通过后，才执行四任务五 seed Train/Dev、干净加载、确定性重放与 checkpoint index 封存。
  - 当前诊断：旧 PPO 的非 Markov 状态别名已经通过公开阶段位、reward contract 0.3 和任务级 `chemworld-rl-observation-contract-0.1` 修复；旧 checkpoint index 已 fail closed 清零。`89dff507` PPO 与 `c4497586` SAC 的 v0.4.12 preflight 均执行 4 个 task ×（step-0、25,600-step）共 8 个 checkpoint，manifest/sidecar/task observation hash、干净加载、双重复放与 source stability 全部通过；PPO 4/4、SAC 3/4 任务达到学习信号，行为完整实验分别 50→407、57→155，两算法四任务 step-0/trained runtime/observation failure 均为 0。v0.4.11 crystallization step-0 的 3 次 solubility reference temperature 越界和 7 次低有效 seed population 已由公开前置条件在 runtime dispatch 前关闭。两个 full matrix 尚未启动，P3 仍未完成。
  - 两个 preflight 与 LLM 轨迹最初定位了冷却温度上下界错误；`e626474` 修复后，离线系统审计继续发现冷却速率跨字段约束、flow 运行时长/有效停留时间、蒸馏零组分除零以及所选相浓度与压力风险错配。`fa546e5` 将公开 action schema 版本化为 `chemworld-public-action-affordance-0.1`，显式发布边界包含性和跨字段约束，并把物理合法但没有成核/没有转移的结晶程序保留为可学习的零收益负实验，而不是 runtime failure。六个 serious tasks 的 223 个候选中，215 个验证有效动作全部提交，runtime 与 observation failure 均为 0；88 项定向回归及 150 项跨模块回归通过。
  - 活性相浓度修复会改变涉及分相/下游处理的风险与分数，六个 scripted golden 已按同源新语义更新。因此所有此前 PPO/SAC checkpoint、LLM v0.4.8/v0.4.9 cells 和旧正式基线只属于旧 source-bound 诊断，不得直接恢复、续跑或与新结果拼表。下一步不是放宽门槛或重复抽 seed，而是用绑定 `fa546e5` 或内容等价后继提交的新 plan/hash，分别给 PPO/SAC 各一次有界 step-0 versus trained 门禁；仍失败的方法退出正式方法清单，不拖延 reference/Bench。
  - 验收：至少预注册数量的独立训练 seeds 均完成；checkpoint 可由干净环境加载并逐 cell 评估。

- [ ] **`benchmark-v05-live-llm-adapters` — 真实 LLM 双角色开发与提示冻结**
  - 默认 owned_paths：live LLM formal adapter、对应测试、`configs/methods/llm_v0.4/`、prompt manifests、`workstreams/benchmark_v1/reports/live-llm-dev-v0.4.json`。
  - 依赖：P2 preflight 与 resource accounting。
  - [x] 运行时核实 DeepSeek 可用 model IDs、thinking/JSON 能力、访问日期和价格；配置错误或模型替换必须新版本，不能静默 fallback。
  - [x] 两个角色均通过官方 adapter 多轮调用，在实验内和实验间适应，能主动请求当前/历史公开谱图数值包；Task Lab 只作 UI，不作正式 launcher。DeepSeek 官方 `deepseek-v4-pro` Chat API 的 user content 当前仍是字符串，网站 canvas 图像不会自动进入模型输入，不得把数值读谱描述为原生 VLM 读图。
  - [x] prompt 只描述工具、任务和公共合同，不加入“默认升温”等强倾向规则；保留结构化决策审计，不索取私有思维链。
  - [ ] 在 Train/Dev 完成 assigned/unassigned/masked 配对、API 失败/重试和成本对账；冻结 prompt、request 参数、model snapshot/access date。
  - 当前状态：v0.4.6 开发矩阵在 56/96 cells 后主动停止并判定为 `incomplete_configuration_rejected`，16 cells 成功、40 cells 方法失败，56/56 资源账本完整，累计 2,369 次 provider 调用和 10.0387 USD；该证据只用于配置诊断，不得汇总为 benchmark 结果。根因是 deliberative 角色反复耗尽墙钟时间，以及 direct 角色因重复谱图/记忆导致累计输入超限。v0.4.7 已将 provider prompt 平均载荷离线回放压缩约 57%–58%，冻结 Pro=`thinking/high, max_tokens=4000`、Flash=`thinking/off, max_tokens=1000`。新的 v0.4.8 使用独立版本、source-commit 级私有缓存、报告 schema 和 seed 派生命名空间，并将付费入口收敛为 `reaction-to-crystallization` 单任务、2 角色 × 3 谱图条件的 6-cell `candidate_screen`，矩阵费用硬上限 2.10 USD。任务、方法、谱图条件、首个 Train seed、开发计划摘要和费用上限均在 provider 调用前 fail closed，不能通过 CLI 静默缩减或扩展，也不能跨提交误续跑。候选未通过完成率、逐方法成功、回放/账本和四实验投影 token/墙钟余量时，代码禁止启动后续 pilot/Dev 矩阵。
  - v0.4.8 首个严格单 cell 诊断绑定 `7c08191` 和 prompt 0.6，`live_llm_a/assigned` 恰好只启动一次并自然生成 `stopped_resumable` 报告：1/1 完整实验、10 operations、10 provider requests、47,341 input tokens、13,421 output tokens、0 retry、0.030392 USD、246.28 s，资源对账完整且独立回放 `max_abs_error=0`。该 cell 的 `total_score=0.011736`、`crystal_yield=0`、`crystal_purity=0.018821`、1/10 非法动作且末态 safety risk 0.213 超过任务阈值 0.168；单 cell、单实验既不能比较谱图条件，也不能检验跨实验学习，禁止据此排名模型。
  - 该诊断还发现一个会污染“模型读取谱图后适应”解释的交互漏洞：第 6 步 GC 后执行加热，旧 `processed_estimate` 仍作为最近已知公开指标存在，模型却把它叙述为加热后的新 GC 结果，并在未重新测量时连续升温。`da83200` 已升级到 prompt/interaction contract 0.7：显式区分当前事件、当前是否存在新谱图包、最近历史谱图 ID/测量步和距测量的操作数；非测量步骤不再把旧 processed estimate 放入 `latest_spectra`，masked 条件也不会泄露“已提供当前谱图”的标志。相关 runner/agent/VLM 回归 74 passed、7 optional skipped，控制审计 `controls_ready=true`；这只证明合同修复，不代表模型性能改善。
  - v0.4.9 的 prompt 0.7 fresh diagnostic cell 绑定 `9ceb87c`，仍恰好只启动 `live_llm_a/assigned` 一次：完成 16 operations、17 provider requests、97,878 input tokens、30,390 output tokens、1 retry、0.063826 USD、568.69 s，资源对账和 16 步回放 `max_abs_error=0`。末态 `total_score=0.162118`、`final_best_score=0.390058`、`crystal_yield=0.310771`、`crystal_purity=0.389096`，2/16 非法动作，最大 safety risk 0.211 仍超过 0.168 限制；这些数值只能描述单次可执行性，不能证明 prompt 改善。轨迹在第 5/13 步测量后的下一决策正确标记新谱图，在随后的控制步骤把 `current_spectral_packet` 置 false、清空 raw/processed packet，并明确把 HPLC 称为历史证据；旧谱图误归因没有复现。
  - v0.4.9 同时暴露的两个非法动作来自共享可行域错误而非模型未知私有物理。`fa546e5` 已在 `e626474` 基础上完成系统审计与修复：公开 schema/验证器/runtime/观测四层在六任务 223 个候选上达到 0 finding，且跨字段约束会随 action schema 一并进入 LLM 紧凑工具视图。这也使 v0.4.9 的剩余 5 cells 彻底失去同源可比性。
  - v0.4.10 已在 `4949403`、action schema `chemworld-public-action-affordance-0.1` 和 223/215/215/0 runtime-domain 审计绑定下运行一个 fresh cell。调度器只启动 `live_llm_a/assigned`，其余 5 cells 保持未运行：10 operations、10 provider requests、54,546 input tokens、13,599 output tokens、0 retry、0.034620 USD、233.90 s；0 非法动作、0 前置条件失败、0 安全违规，资源对账与 10 步回放 `max_abs_error=0`。终点 `total_score=0.366305`、`final_best_score=0.477341`、`crystal_yield=0.475541`、终点 `crystal_purity=0.978764`。第 5 步 HPLC 后，第 6 步模型明确解释目标峰/副产物峰并选择加晶种，第 7 步 `cool_crystallize` 成功提交；后续控制步骤正确把该谱图标记为历史而非当前新谱图。该单任务、单角色、单条件、单实验只能证明新合同可执行，不能比较模型、谱图条件或跨实验学习。
  - v0.4.10 同时暴露一个只影响公开解释消费、不改变动作/分数的缺口：`agent_trace` 已保存 `spectrum_interpretation` 和 `request_historical_spectrum_id`，但通用 `DecisionAuditRecord` 丢弃二者，导致面板或其他只读 `explanation.decision_audit` 的消费者看不到明确读谱结论。`23c9361` 已令通用审计保留这两个结构化公开字段，仍不保存私有 reasoning，并把 runner/cache/report/seed namespace 隔离为 v0.4.11；相关 LLM、runner、交互和规则策略测试 64 passed。另 2 个 formal-operation 测试失败是旧 operation freeze 已精确检测 `agent_interface.py`、`interaction.py`、`operation_validator.py` source mismatch，却仍被旧测试断言为 ready，不是本修复的运行失败。
  - 下一门禁：v0.4.8–v0.4.10 缓存和报告均保持不可续跑的 source-bound 诊断。v0.4.11 已在 `23c9361` 完成无 API key dry-run，并绑定同一通过的 runtime-domain 审计；按照“先单 cell、再决定”的预算纪律，当前不再调用 provider。若以后决定继续 LLM，必须在届时的干净 v0.4.11 source 上重新签发并运行完整 6-cell candidate screen，而不是挑选性续跑成功条件；只有六条件完成率、逐方法成功、账本、回放和四实验资源投影均通过，才进入 2-experiment `live_pilot`，跨实验学习再由 4-experiment Dev 单独验证。
  - 验收：真实多轮轨迹可回放执行，所有调用/失败/tokens/费用可核对；未证明性能提升也允许封存，但不能缺失证据。

- [ ] **`benchmark-v05-portable-release-reattestation` — P3 后依赖锁与 clean-wheel 重新证明**
  - 默认 owned_paths：新版本 portable source/wheel manifest、对应审计脚本/测试、`workstreams/world_foundation/reports/portable-release-v0.5.1.json`；不得覆盖 P0 的 v0.5 历史报告。
  - 依赖：PPO/SAC/LLM 最终纳入范围及运行依赖稳定；早于 method freeze 的正式 manifest 签发。
  - [ ] 枚举 P0 后所有 `pyproject.toml`/`uv.lock` 变化，区分 RL 正式依赖、开发工具和未来 VLM 非执行计划；证明主锁不含未授权的 VLM 推理栈。
  - [ ] 由当前干净提交重建 wheel/source manifest，在隔离 Windows 环境执行 golden/replay、runtime boundary、方法 adapter clean-load 与资源 writer/reader smoke；Linux 仍为非阻断记录。
  - [ ] 比较 backend semantic hash：若后端语义未变则显式继承同一 backend identity 并只升级环境证明；若已变则必须生成新 backend candidate 和相应协议版本，不得静默沿用。
  - [ ] 将新的 dependency-lock/source/wheel 摘要接入 formal preflight；旧 `3c6845…` 环境证明保留为 P0 历史证据，但不得为当前正式运行签发 manifest。
  - 验收：当前锁、clean wheel、源码、backend/method 合同与 preflight 精确绑定；缺一项即 `formal_training_allowed` 可用于 Train/Dev 但 `formal_bench_issuance_allowed=false`。

- [ ] **`benchmark-v05-method-freeze` — 方法清单与 Bench 解封**
  - 默认 owned_paths：`configs/benchmark/method_freeze_v0.4.json`、`scripts/audit_method_freeze_v0.4.py`、`tests/test_method_freeze_v0.4.py`、`workstreams/benchmark_v1/reports/method-freeze-v0.4.json`。
  - 依赖：所有计划进入正式比较的方法完成 P3；未完成方法必须明确退出，不拖着空实现进入矩阵。
  - 当前预检：fail-closed 方法冻结审计器与 19 项 hash-bound 输入合同已经落地；历史报告为 `method_freeze_preflight_blocked`，不能在新语义边界上沿用 blocker 数量。operation v0.4.1 freeze 3/3 与 288-cell 正式开发报告已 ready；classic recipe space 0.3 freeze 8/8 与 768-cell 正式开发报告已 ready，两者均绑定稳定干净的 `ef202b7`。当前 blocker 收敛为 PPO/SAC v0.4.9 门禁与 checkpoint、LLM 完整 candidate/Dev、正式资源硬预算和 portable-release reattestation；Bench 继续封存。待 P3 最终纳入范围稳定后必须重生成方法冻结报告，不能修补旧摘要或使用 `--force`。
  - [ ] 固定方法 IDs、family、interaction stratum、hyperparameters、checkpoint/prompt hashes、Dev 选择依据和资源上限。
  - [x] 核实 reference builder 与所有 evaluated method 身份、代码和随机数流独立。
  - [ ] 锁定 run count/预计算力/API 费用，并由 preflight 签发 Bench manifest。
  - 验收：解封后任何实现或协议修改都自动使 run manifest 失效并要求新 cohort。

## P4：先生成 reference，再运行基础正式矩阵

- [ ] **`benchmark-v05-reference-evidence` — 生成并冻结独立 reference portfolio**
  - 默认 owned_paths：reference-search 专用 runner/config、`runs/benchmark-v0.5/reference-v0.4/` manifests、`workstreams/benchmark_v1/reports/reference-evidence-v0.4.json`。
  - 依赖：method freeze；必须早于被评方法 Bench 评分。
  - [ ] 执行完整 reference plan；每个 source run 都使用冻结 backend、独立 builder seed、完整预算和资源账本。
  - [ ] 逐轨迹回放，冻结每个 task × seed × metric 的 best-known estimate、区间和来源 digests。
  - [ ] 检查 cell 完整、无 evaluated-method identity/trajectory 重叠、无缺失/重复/nonfinite 值，并独立复算 manifest。
  - 控制边界：本任务由核心组持有，不向方法执行组反馈 reference 结果；RL 组不得同时承担 reference 搜索与自身 checkpoint 选择。
  - 验收：完整 reference manifest 在方法评分前生成并只读；失败则不得开始下一任务。

- [ ] **`benchmark-v05-formal-base-matrix` — 四个 core task 的基础正式比较**
  - 默认 owned_paths：`runs/benchmark-v0.5/base-v0.4/` manifests、`workstreams/benchmark_v1/reports/formal-base-v0.4.json`、对应图表数据。
  - 依赖：reference evidence 冻结、Bench manifest 已签发。
  - [ ] 在同一配对 Bench base cells 上运行全部已封存方法；严格按 interaction strata 分析。
  - [ ] 每个 cell 完成即时回放、资源对账和失败分类；不因方法失败补 seed、改 prompt、换 checkpoint 或重跑到成功。
  - [ ] 按 task 报告主指标、联合安全/成本规则、anytime 曲线、完成率和资源前沿；保留负结果。
  - [ ] 用预注册统计代码一次性生成结果，不在看完结果后改 SESOI、排除规则或主比较。
  - 执行边界：已封存方法的 cell 可交给 RL 组或其他执行者盲运行，但只能消费核心组签发的不可变 cell manifest；执行者不能查看私有 Bench 参数或 reference feedback，核心组负责 digest 重放、统计和结论。
  - 验收：预期笛卡尔积完整或明确标记 incomplete；只有同时满足联合规则的方法比较可作正式结论。

- [ ] **`benchmark-v05-base-reproduction` — 基础矩阵独立 clean-wheel 复核**
  - 默认 owned_paths：`workstreams/benchmark_v1/reports/formal-base-reproduction-v0.4.json`、复核 manifests。
  - 依赖：formal base matrix 完成。
  - [ ] 在独立干净环境复算所有结果 digests、统计表和图；抽取预注册比例的轨迹从动作日志重放。
  - [ ] 核实失败分母、资源账本、成对 cell 和 reference 绑定，没有手工补文件或绝对路径依赖。
  - 验收：复核报告与原报告在声明容差内一致；不一致时 P4 失败并回到新的协议版本。

## P5：在基础结果通过后做机制与信息消融

- [x] **`benchmark-v05-vlm-observation-contract` — 开源 VLM 谱图输入的确定性准备合同**
  - 边界：只建立未来试点所需的 provider-neutral 图像引用、固定 PNG 渲染、模态/assigned/unassigned/masked 条件、历史访问白名单、依赖锁和审计；不下载权重、不推理、不调用付费 API、不修改 site，也不进入 v0.4 基础矩阵。
  - 结果：HPLC、GC、UV/Vis、IR、NMR 和 pH 公共信号可生成固定 960 × 640 PNG；IR/NMR 使用约定的逆向横轴。轨迹只记录相对路径及图像、原始曲线、公开包和渲染合同四类 SHA-256，不保存 base64、绝对路径或私有思维链。assigned/unassigned 共享相同曲线摘要，身份字段在 unassigned 文本和图像中移除；masked 不生成图像。审计还发现并修复了“异常 catalog 携带信号时可能绕过显式历史请求”的边界漏洞，现在目录只保留 spectrum ID、仪器、状态等标量元数据。
  - 验证：新增 10 项合同/泄漏/重放/锁隔离测试，连同 11 项既有 live-LLM/历史谱图测试共 21 项通过；ruff 与 mypy 通过；独立控制报告 `contract_ready=true`、`pre_vlm_primary_lock_restored=true`、`runtime_ready_for_model_execution=false`、`benchmark_claim_allowed=false`。Pillow 只存在于本次本地合同审计环境；其余推理需求只记录在 future-Dev 配置中，不进入主 `pyproject.toml`/`uv.lock`，模型/processor revision 仍要求在试点前单独封存。
  - 后续门禁：P4 未通过前不启动 VLM 性能实验；P4 后只允许一个 Dev 任务比较 masked、numeric-unassigned、image-unassigned、image+numeric-unassigned、image-assigned。必须先证明图像输入产生可重放的决策或结果增益，再认领任何多任务矩阵。
  - 验收：同输入逐字节复现、改变信号改变摘要、历史谱图仅显式请求后出现、日志不含图像字节/绝对路径、仓库不含模型权重，全部已满足；这只证明观察合同完整，不代表 VLM 有效。

- [ ] **`benchmark-v05-spectrum-ablation` — assigned/unassigned/masked 谱图价值实验**
  - 默认 owned_paths：`runs/benchmark-v0.5/spectrum-v0.4/` manifests、`workstreams/benchmark_v1/reports/spectrum-ablation-v0.4.json`、对应图表数据。
  - 依赖：P4 通过；只运行预注册 operation-level 方法和相应盲控制。
  - [ ] 在相同 task/world/model seed 上配对三种谱图条件，确保非谱图公开字段、预算和调用策略一致。
  - [ ] 区分“读取了谱图”“决策因谱图改变”“结果因谱图改善”三个 estimand；报告历史谱图请求时点和成本。
  - [ ] 比较 observation-blind、谱图 masked、unassigned 和 assigned 条件，防止把额外 tokens/提示长度当成化学推理收益。
  - 验收：配对完整且资源差异可解释；无改善是有效结果，不得筛选任务后才汇报。

- [ ] **`benchmark-v05-world-generalization` — 世界轴与机制族泛化**
  - 默认 owned_paths：`runs/benchmark-v0.5/generalization-v0.4/` manifests、`workstreams/benchmark_v1/reports/world-generalization-v0.4.json`、对应图表数据。
  - 依赖：P4；仅每个方法家族预注册 champion 加 random/control 进入。
  - [ ] 覆盖 interpolation、extrapolation、composition、observation noise 及注册机制族，所有方法使用相同 task-axis-mode-severity-seed cell。
  - [ ] 每轴单独报告 effect shift、failure shift、安全/成本和资源；禁止跨轴标量化。
  - [ ] 验证 axis identity 对 agent 隐藏，扰动确实改变物理/观测而非只改 metadata。
  - 验收：每个注册轴都有完整 paired cells 和机制解释；未完成轴不得被“总体平均”掩盖。

- [ ] **`benchmark-v05-safety-cost-stress` — 约束激活与资源压力实验**
  - 默认 owned_paths：`runs/benchmark-v0.5/stress-v0.4/` manifests、`workstreams/benchmark_v1/reports/safety-cost-stress-v0.4.json`、对应图表数据。
  - 依赖：P4；可与 world generalization 并行但不得共用 owned paths。
  - [ ] 在预注册近阈值 cells 检验 Safe-GP、RL、LLM 与盲控制是否真正响应风险/成本信号。
  - [ ] 分别改变操作、测量、实验、token 和计算预算，绘制 Pareto/resource frontiers，不合成单一成本分。
  - [ ] 检查模型是否通过少做实验、提前终止、避免测量或失败不记账来伪造安全/低成本。
  - 验收：约束有实际激活且 ledger 闭合；所有规避路径由 replay/behavior-completion gate 捕获。

## P6：正式证据总审计与发布决策

- [ ] **`benchmark-v05-formal-evidence-audit` — 完整性、泄漏、复现和主张边界终审**
  - 默认 owned_paths：`scripts/audit_formal_evidence_v0.5.py`、`tests/test_formal_evidence_v0.5.py`、`workstreams/benchmark_v1/reports/formal-evidence-audit-v0.5.json`。
  - 依赖：计划纳入结论的 P4/P5 实验全部完成。
  - [ ] 校验所有 manifest、hash、cell、轨迹、结果、reference、失败分母、统计表、图和资源账本。
  - [ ] 重新扫描 Train/Dev/reference/Bench 泄漏、事后调参、选择性汇报、重复 seed、旧 backend 混入和 hidden-state 使用。
  - [ ] 将结论分为 supported、negative、exploratory、incomplete、invalid 五类；不给 incomplete/invalid 结果排名。
  - [ ] 独立运行 clean-wheel reproduction，并记录任何无法复现的 cell 与影响范围。
  - 验收：只有审计全通过时 `benchmark_claim_allowed=true`；否则保持 false 并输出精确 remediation tasks。

- [ ] **`benchmark-v05-release-integration` — 发布级协议、结果与用户文档整合**
  - 默认 owned_paths：正式 benchmark 文档、结果摘要、图表、release notes、网站数据与最终 release manifest。
  - 依赖：formal evidence audit 允许主张。
  - [ ] 面向使用者说明任务、交互层级、基座适用域、方法、预算、结果、失败、局限和复现命令；移除内部 claim/团队/调试信息。
  - [ ] 明确 synthetic world 不等同真实化学发现，benchmark 衡量的是多层调度、实验设计、信息获取、适应、约束与泛化能力。
  - [ ] 发布逐任务结果和资源前沿，提供机器可读 manifests/digests；不发布 API key、私有 seed、隐藏状态或私有思维链。
  - [ ] 严格构建 docs/site 并在本地核对链接、导航、图表和移动端；发布动作另按用户当时指令执行。
  - 验收：公开页面与正式 artifact 同源，所有数字可追溯到 replay-verified result；此后才进入论文撰写阶段。

## 推荐执行顺序

`fa546e5` 后的一个 v0.4.10 LLM fresh cell 已完成，v0.4.11 公开谱图审计修复也已离线就绪；当前暂停更多付费调用。operation 288-cell 与 classic 768-cell 的 v0.4.1 正式开发重认证均已通过并绑定稳定干净的 `ef202b7`，相应 P3 项已完成。RL adapter 0.2 已支撑 v0.4.12 PPO/SAC 两个四任务 gate，在原冻结门槛下关闭结晶 3+7 公共域缺口并分别获得 `full_matrix_allowed=true`。下一步固化 SAC 正报告，并在各自 exact source-bound 报告/clean tree 上执行 PPO/SAC full matrix 与 checkpoint index 封存。之后确定 LLM 是否退出或完成 candidate/Dev，执行 portable-release reattestation 与 method freeze。P4 必须严格按“reference evidence → base matrix → reproduction”串行；P5 的三个实验可在 P4 通过后并行；P6 最后串行审计和发布。
