# ChemWorld v0.5 基座完整性与正式实验 Todo

最后更新：2026-07-13

## 目标与边界

本阶段只做两件事：证明当前 backend v0.5 候选基座足够完整、稳定且可辨识；在该基座冻结后，运行可复现、可统计解释的正式方法比较。论文写作、榜单宣传和最终发布必须等待本文件的正式证据门禁通过。

当前固定点如下：15 个注册任务的必需运行路径至少达到有界 `reference_validated`，28 类操作已有事务语义，20 个 provider 已接入正式 runtime，`proxy_allowed=false`，且没有待升级的 `lite` 正式路径。三个共享模块 `reaction_kinetics`、`reactors`、`spectroscopy_instruments` 已完成升级；完整测试曾达到 1261 passed、14 skipped，backend v0.5 release gate 12/12 通过。这些结果证明“候选基座可运行”，但尚未证明“正式 benchmark 结论成立”。

现阶段不得作正式 benchmark 主张，原因包括：旧经典方法、Safe-GP、SAC、LLM 结果绑定旧 backend；PPO 仅通过 Dev 学习门禁；reference portfolio 只有控制层和运行计划；现有 runner 不能统一执行经典、RL、真实 LLM 与世界扰动；`300–319` 已实际运行并被查看，却仍被协议称为 fresh confirmatory seeds；`reference_regret_vnext.json` 仍使用更早的 `20–39`，协议之间不一致。

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

- [ ] **`benchmark-v05-evidence-quarantine` — 污染 cohort 与旧证据隔离**
  - 默认 owned_paths：`configs/benchmark/evidence_quarantine_v0.5.json`、`scripts/audit_evidence_quarantine.py`、`tests/test_evidence_quarantine.py`、`workstreams/benchmark_v1/reports/evidence-quarantine-v0.5.json`。
  - 依赖：无，必须最先完成。
  - [ ] 枚举仓库、`runs/`、报告、文档和 git 历史中所有用过或被查看过的 Train/Dev/Bench/reference seeds 与 world cells。
  - [ ] 将 `20–39`、`300–319` 及其派生结果标记为 `diagnostic_only`；解释 `primary-0.3` 绑定旧 `lite` maturity/backend 的事实，禁止重命名为 v0.5 正式结果。
  - [ ] 建立机器可读 denylist，正式 runner 在检测到污染 seed、旧 backend、旧 evaluator 或旧协议时直接拒绝启动。
  - [ ] 检查文档不再把 `300–319` 称为 fresh/confirmatory；保留其诊断价值但移除正式措辞。
  - 验收：扫描覆盖所有保留 artifact；任一正式配置引用 denylist 即测试失败；报告明确 `benchmark_claim_allowed=false`。

- [ ] **`foundation-v05-contract-coherence` — task/world/score/reference/method 协议一致性收口**
  - 默认 owned_paths：`configs/foundation/contract_coherence_v0.5.json`、`scripts/audit_contract_coherence_v0.5.py`、`tests/test_contract_coherence_v0.5.py`、`workstreams/world_foundation/reports/contract-coherence-v0.5.json`。
  - 依赖：`benchmark-v05-evidence-quarantine`。
  - [ ] 从注册任务生成唯一合同图：task → operation → provider → observation → primary metric → risk/cost → world axes → evaluator → replay schema。
  - [ ] 检查六个严肃任务、四个 core 角色与两个 exploratory 角色在所有协议中同源；消除 `20–39` 与 `300–319`、方法别名、`greedy`/`greedy_local` 等漂移。
  - [ ] 检查单位、方向、预算、失败、终止、测量和 final assay 语义不存在重复真相源。
  - [ ] 对 protocol/model/checkpoint/backend hash 建立兼容矩阵，拒绝“schema 相同但语义不同”的 artifact。
  - 验收：所有正式配置可由同一 manifest 解析；不存在未注册 task/method/provider、悬空依赖或不一致 seed grid。

- [ ] **`foundation-v05-composed-runtime-stress` — 完整基座组合压力与回放测试**
  - 默认 owned_paths：`configs/foundation/composed_runtime_stress_v0.5.json`、`scripts/run_composed_runtime_stress.py`、`tests/test_composed_runtime_stress.py`、`workstreams/world_foundation/reports/composed-runtime-stress-v0.5.json`。
  - 依赖：合同一致性完成；不得修改 provider 实现，发现缺陷另开 fix slice。
  - [ ] 覆盖 15 tasks × 28 operations × 所有必需 provider 的可达组合，包含标称点、边界、近边界、非法输入、重复调用和强制求解失败。
  - [ ] 对反应—反应器—传热—相平衡—分离—仪器的组合链验证质量/能量/电荷守恒、非负性、单调趋势和 ledger 一致性。
  - [ ] 对同 seed 同动作逐字节回放；对进程重启、批量/单次执行和 Windows/干净环境比较确定性及声明容差。
  - [ ] 统计每个 task/world cell 的 solver failure、domain failure、NaN/Inf、回滚和超时率，不以重试掩盖失败。
  - 验收：所有声明域内 cell 通过，声明域外均显式 fail closed；正式 core task 不存在 fallback、proxy、`lite` 或静默 clip 路径。

- [ ] **`foundation-v05-observation-identifiability` — 谱图与公共观测可辨识性/泄漏验证**
  - 默认 owned_paths：`configs/foundation/observation_identifiability_v0.5.json`、`scripts/audit_observation_identifiability_v0.5.py`、`tests/test_observation_identifiability_v0.5.py`、`workstreams/world_foundation/reports/observation-identifiability-v0.5.json`。
  - 依赖：组合压力测试的稳定观测链。
  - [ ] 验证 UV/Vis、IR、NMR、HPLC/GC、pH 等公开信号随相关状态变化，噪声/漂移/LOD/LOQ 下仍有合理但非完美的辨识能力。
  - [ ] 建立 `assigned`、`unassigned`、`masked` 三种条件；除谱图字段外，配对观测必须完全相同。
  - [ ] 用无答案泄漏的简单 probe 检查观测对任务主指标/机制族有信息，同时不能直接恢复 hidden state、private seed、provider 参数或模型身份。
  - [ ] 验证历史谱图只在 agent 主动请求后返回，访问、失败和成本进入 ledger；不预先塞入全部历史。
  - 验收：每种仪器均有灵敏度、特异性、退化区和泄漏报告；assigned/masked 配对能被精确回放。

- [ ] **`foundation-v05-task-validity-power` — 主指标、风险和预算的动态范围/统计功效验证**
  - 默认 owned_paths：`configs/foundation/task_validity_power_v0.5.json`、`scripts/run_task_validity_power_v0.5.py`、`tests/test_task_validity_power_v0.5.py`、`workstreams/world_foundation/reports/task-validity-power-v0.5.json`。
  - 依赖：组合压力和观测可辨识性完成。
  - [ ] 对四个 core task 绘制冻结 response surface，验证主指标方向、非平凡最优区、局部结构、机制变化和可达到的 SESOI。
  - [ ] 验证风险阈值既非永不触发也非几乎必触发；成本指标对真实操作/测量变化敏感且不重复计费。
  - [ ] 用与正式方法无关的 policy probes 检查随机、局部、信息利用、风险盲四类行为可被指标区分。
  - [ ] 预估 20 paired seeds 对主效应、安全/成本非劣与谱图消融的功效；不足时在解封 Bench 前调整样本量，而不是事后改门槛。
  - 验收：每个 core task 都有可辨识目标、安全—性能或成本—性能权衡和预注册 SESOI；否则降级为 exploratory。

- [ ] **`foundation-v05-portable-release` — 可移植环境、依赖锁与 backend 语义冻结**
  - 默认 owned_paths：`configs/foundation/portable_release_v0.5.json`、依赖锁文件、`scripts/build_portable_release_v0.5.py`、`tests/test_portable_release_v0.5.py`、`workstreams/world_foundation/reports/portable-release-v0.5.json`。
  - 依赖：以上 P0 任务全部完成。
  - [ ] 固定 Python 与关键数值/ML 依赖，构建 clean wheel；记录 CPU/GPU、BLAS、CUDA 和求解器版本。
  - [ ] 将 backend semantic hash 与 docs/site commit 分离，避免只改文档就令正式轨迹失效，也避免语义改动逃逸版本更新。
  - [ ] 在 Windows 与一个独立 Linux 干净环境本地运行 golden/replay；数值差异必须落在预注册容差内。
  - [ ] 重跑完整 pytest、ruff、mypy、strict docs、release gate、clean-wheel smoke 和 P0 控制报告。
  - 验收：生成唯一 `backend-v0.5-formal-candidate` manifest；任一门禁失败则不得进入 P1。

## P1：冻结新的正式协议与未见数据边界

- [ ] **`benchmark-v05-formal-protocol-0.4` — 新 cohort 与主张边界预注册**
  - 默认 owned_paths：新版本 `configs/benchmark/*_v0.4.json`、`scripts/audit_formal_protocol_v0.4.py`、`tests/test_formal_protocol_v0.4.py`、`workstreams/benchmark_v1/reports/formal-protocol-v0.4.json`。
  - 依赖：P0 全部通过。
  - [ ] 由污染清单之外生成新的 Train/Dev/reference-search/Bench namespaces；实际 Bench base seeds 与 world parameters 只写入受控私有 manifest，公开协议只提交 commitment/hash。
  - [ ] 四个 core task 用于正式结论；electrochemical/equilibrium 保持 exploratory，除非 P0 validity gate 单独证明可升级。
  - [ ] 冻结 40 次完整实验预算、4/8/12/20/40 checkpoints、world axes、失败策略、停止规则和禁止 Bench 微调规则。
  - [ ] 明确 primary、secondary、ablation 和 exploratory estimands；任何协议变更都必须升级版本并废弃变更后的旧 cohort。
  - 验收：协议审计可证明所有 split 不相交、Bench 未被运行/查看、旧 0.1–0.3 全部为 diagnostic。

- [ ] **`benchmark-v05-interaction-strata` — recipe 与 operation 级公平比较合同**
  - 默认 owned_paths：`configs/benchmark/interaction_strata_v0.4.json`、`src/chemworld/eval/interaction_strata.py`、`tests/test_interaction_strata.py`、`workstreams/benchmark_v1/reports/interaction-strata-v0.4.json`。
  - 依赖：formal protocol 0.4。
  - [ ] 建立 recipe-level track：random、LHS、greedy、GP/RF/Safe-GP，只在完整实验之间更新。
  - [ ] 建立 operation-level track：operation-random、observation-blind、rule-based、RL、LLM，可在实验内适应并按需读谱。
  - [ ] 不把两个 track 的差异冒充算法优劣；另外给出 system-level comparison，完整披露能力差异和 harness assistance。
  - [ ] 冻结实验、操作、测量、模型调用和训练计算的并列预算/资源账本，不做单一资源标量化。
  - 验收：每个方法声明 decision scope、可见观测、谱图能力、适应层级和自动化帮助；缺失声明无法注册。

- [ ] **`benchmark-v05-statistical-analysis-plan` — 正式统计与失败处理方案**
  - 默认 owned_paths：`configs/benchmark/statistical_analysis_plan_v0.4.json`、`src/chemworld/eval/formal_statistics.py`、`tests/test_formal_statistics.py`、`workstreams/benchmark_v1/reports/statistical-analysis-plan-v0.4.json`。
  - 依赖：task validity/power 与 interaction strata。
  - [ ] 冻结 paired estimand、bootstrap/随机化检验、置信区间、Holm 多重比较、SESOI 和安全/成本非劣界限。
  - [ ] 主结论要求目标改善、达到 SESOI、安全非劣、成本非劣和全部回放同时成立；不以总分替代联合规则。
  - [ ] 失败运行保留在分母，并分别报告 invalid action、provider/model failure、runtime failure、budget overrun 和 incomplete accounting。
  - [ ] 冻结 family champion 选择规则，只允许 Dev 选型；Bench 不做超参数、提示词或 checkpoint 选择。
  - 验收：用纯合成 null/positive/unsafe/cost-regressing fixtures 证明 false positive、功效和失败处理符合协议。

- [ ] **`benchmark-v05-reference-plan-0.4` — 独立 reference portfolio 重建计划**
  - 默认 owned_paths：`configs/benchmark/reference_portfolio_v0.4.json`、`configs/benchmark/reference_regret_v0.4.json`、`tests/test_reference_portfolio_v0.4.py`、`workstreams/benchmark_v1/reports/reference-plan-v0.4.json`。
  - 依赖：formal protocol 与统计方案冻结。
  - [ ] 绑定新 reference-search split、新 seed namespace、backend/evaluator hash 和四个 core task，彻底移除旧 `20–39`。
  - [ ] reference builder 身份不得与任一被评方法重合；其训练、搜索、轨迹和随机数流独立。
  - [ ] 每个 task × seed × metric 至少四个独立 source runs；冻结 best-known estimate 与不确定区间，明确“不是 oracle、允许被方法超过”。
  - [ ] 在任何方法 Bench 评分前冻结完整 manifest；后续更新 reference 必须新版本并重算所有方法。
  - 验收：run plan 可枚举精确 cell/run 数和预计资源；仍保持 `formal_results_present=false`。

## P2：统一正式执行基础设施

- [ ] **`benchmark-v05-cell-runner` — 可恢复、幂等的单 cell 执行器**
  - 默认 owned_paths：`src/chemworld/eval/formal_runner.py`、`scripts/run_formal_cell.py`、`tests/test_formal_runner.py`、`workstreams/benchmark_v1/reports/formal-runner-controls-v0.4.json`。
  - 依赖：P1 协议冻结。
  - [ ] 统一 task × method × seed × world × spectrum-condition cell，支持 classic、RL checkpoint 和 live LLM adapter factory。
  - [ ] 每个 cell 原子写入 manifest、trajectory、result、failure artifact 和完成标记；中断后只重跑未完成/校验失败 cell。
  - [ ] 同一 cell 重复启动必须返回相同 identity 或拒绝覆盖；不得把半成品当成功，不得自动补动作或 final assay。
  - [ ] 每个输出绑定全部协议/代码/checkpoint/prompt/reference hashes，并立即独立回放验证。
  - 验收：故障注入覆盖进程中断、磁盘不完整、API 超时、坏 JSON、重复 cell、digest 篡改和预算超限。

- [ ] **`benchmark-v05-matrix-orchestrator` — manifest 驱动的并行矩阵编排**
  - 默认 owned_paths：`src/chemworld/eval/formal_matrix.py`、`scripts/run_formal_matrix.py`、`tests/test_formal_matrix.py`、`workstreams/benchmark_v1/reports/formal-matrix-controls-v0.4.json`。
  - 依赖：cell runner。
  - [ ] 由冻结 manifest 展开预期 cell，不在 CLI 手写 tasks/seeds；启动前输出 cell 数、CPU/GPU/API 队列和费用上限。
  - [ ] CPU 方法使用进程级并行；GPU 训练/推理按设备独占或声明配额；LLM 使用速率限制与可恢复队列。
  - [ ] 进度实时展示 queued/running/succeeded/failed/replay-verified，以及每个任务、方法和预算检查点；不得显示隐藏状态或私有 seed。
  - [ ] 聚合前检查完整笛卡尔积、成对条件、失败分母和资源账本；缺一 cell 就只产出 incomplete 报告。
  - 验收：小型 smoke matrix 可停止、恢复、并行和复算，结果与串行执行等价。

- [ ] **`benchmark-v05-resource-accounting` — 方法资源与 API 成本 fail-closed**
  - 默认 owned_paths：`src/chemworld/eval/resource_accounting_v0_4.py`、`tests/test_resource_accounting_v0_4.py`、`workstreams/benchmark_v1/reports/resource-accounting-v0.4.json`。
  - 依赖：cell runner；可与 orchestrator 并行。
  - [ ] 区分环境操作、完整实验、测量、决策、provider requests/retries、tokens、金额、训练步数、CPU/GPU 与 wall time。
  - [ ] DeepSeek usage 缺失、价格版本不匹配或失败请求无法计费时，保留轨迹但标记 accounting failure；不得估成零。
  - [ ] RL checkpoint 记录训练总资源并与多个评估 cell 分开报告；classic 方法记录拟合/采集优化时间。
  - [ ] 防止重复计费、缓存命中误算、重试漏算、并行 wall time 相加冒充 elapsed time。
  - 验收：合成账单和实际 smoke run 对账精确；所有 required ledger 字段非缺失且量纲正确。

- [ ] **`benchmark-v05-preflight-gate` — 正式运行总门禁**
  - 默认 owned_paths：`scripts/run_formal_preflight.py`、`tests/test_formal_preflight.py`、`workstreams/benchmark_v1/reports/formal-preflight-v0.4.json`。
  - 依赖：P2 其他任务全部完成。
  - [ ] 同时检查 clean source/wheel、backend manifest、协议 hashes、seed denylist/split、reference 状态、method registration、checkpoint/prompt、预算和磁盘/算力/API 配额。
  - [ ] 生成唯一 run manifest 和不可变 run ID；正式 runner 只接受已签发 manifest。
  - [ ] 任何缺失或不一致都返回非零并列出准确修复项，不允许 `--force` 绕过。
  - 验收：全方法 × 两个交互 track × assigned/masked × 小 seed 的 smoke grid 100% 轨迹回放通过；报告仍为非正式。

## P3：开发、验证并封存方法

- [ ] **`benchmark-v05-classic-adapters` — 经典与主动学习基线封存**
  - 默认 owned_paths：各 classic adapter、对应测试、`configs/methods/classic_v0.4/`、`workstreams/benchmark_v1/reports/classic-dev-v0.4.json`。
  - 依赖：P2 preflight。
  - [ ] 注册 random、LHS、greedy local、typed structured GP-EI/PI/UCB、RF-EI、Safe-GP；材料类别必须 one-hot/typed，禁止数字代号产生伪距离。
  - [ ] 在 Train/Dev 检查采集函数确实进入优化阶段、Safe-GP 约束被激活、预算曲线非退化和确定性回放。
  - [ ] 只用 Dev 选择预注册 family champion；冻结代码、超参数和 method hash。
  - 验收：每种方法的能力、失败域、复杂度和资源 ledger 完整；不使用 Bench/reference 反馈。

- [ ] **`benchmark-v05-rl-adapters` — PPO/SAC 正式适配、训练与 checkpoint 封存**
  - 默认 owned_paths：各 RL formal adapter、对应测试、`configs/methods/rl_v0.4/`、checkpoint manifests、`workstreams/benchmark_v1/reports/rl-dev-v0.4.json`。
  - 依赖：P2 preflight；PPO 旧 5-seed gate 仅作起点。
  - [ ] PPO 使用原生 masked categorical + conditional parameters；SAC 若继续采用连续 latent，必须明确其可比性限制并通过相同 public affordance/action decoder。
  - [ ] 在 Train worlds 训练多个预注册 seeds，在 Dev worlds 选择 checkpoint；验证四个 core task 的行为完成，不只验证 flow。
  - [ ] 记录学习曲线、训练步数、GPU/CPU、失败率、quick-close、观察盲控制和 checkpoint/backend/action/reward hash。
  - [ ] Bench 前冻结每个任务或共享策略的选择规则；禁止 Bench 微调和事后选 seed。
  - 验收：至少预注册数量的独立训练 seeds 均完成；checkpoint 可由干净环境加载并逐 cell 评估。

- [ ] **`benchmark-v05-live-llm-adapters` — 真实 LLM 双角色开发与提示冻结**
  - 默认 owned_paths：live LLM formal adapter、对应测试、`configs/methods/llm_v0.4/`、prompt manifests、`workstreams/benchmark_v1/reports/live-llm-dev-v0.4.json`。
  - 依赖：P2 preflight 与 resource accounting。
  - [ ] 运行时核实 DeepSeek 可用 model IDs、thinking/JSON 能力、访问日期和价格；配置错误或模型替换必须新版本，不能静默 fallback。
  - [ ] 两个角色均通过官方 adapter 多轮调用，在实验内和实验间适应，能主动请求当前/历史谱图；Task Lab 只作 UI，不作正式 launcher。
  - [ ] prompt 只描述工具、任务和公共合同，不加入“默认升温”等强倾向规则；保留结构化决策审计，不索取私有思维链。
  - [ ] 在 Train/Dev 完成 assigned/unassigned/masked 配对、API 失败/重试和成本对账；冻结 prompt、request 参数、model snapshot/access date。
  - 验收：真实多轮轨迹可回放执行，所有调用/失败/tokens/费用可核对；未证明性能提升也允许封存，但不能缺失证据。

- [ ] **`benchmark-v05-method-freeze` — 方法清单与 Bench 解封**
  - 默认 owned_paths：`configs/benchmark/method_freeze_v0.4.json`、`scripts/audit_method_freeze_v0.4.py`、`tests/test_method_freeze_v0.4.py`、`workstreams/benchmark_v1/reports/method-freeze-v0.4.json`。
  - 依赖：所有计划进入正式比较的方法完成 P3；未完成方法必须明确退出，不拖着空实现进入矩阵。
  - [ ] 固定方法 IDs、family、interaction stratum、hyperparameters、checkpoint/prompt hashes、Dev 选择依据和资源上限。
  - [ ] 核实 reference builder 与所有 evaluated method 身份、代码和随机数流独立。
  - [ ] 锁定 run count/预计算力/API 费用，并由 preflight 签发 Bench manifest。
  - 验收：解封后任何实现或协议修改都自动使 run manifest 失效并要求新 cohort。

## P4：先生成 reference，再运行基础正式矩阵

- [ ] **`benchmark-v05-reference-evidence` — 生成并冻结独立 reference portfolio**
  - 默认 owned_paths：reference-search 专用 runner/config、`runs/benchmark-v0.5/reference-v0.4/` manifests、`workstreams/benchmark_v1/reports/reference-evidence-v0.4.json`。
  - 依赖：method freeze；必须早于被评方法 Bench 评分。
  - [ ] 执行完整 reference plan；每个 source run 都使用冻结 backend、独立 builder seed、完整预算和资源账本。
  - [ ] 逐轨迹回放，冻结每个 task × seed × metric 的 best-known estimate、区间和来源 digests。
  - [ ] 检查 cell 完整、无 evaluated-method identity/trajectory 重叠、无缺失/重复/nonfinite 值，并独立复算 manifest。
  - 验收：完整 reference manifest 在方法评分前生成并只读；失败则不得开始下一任务。

- [ ] **`benchmark-v05-formal-base-matrix` — 四个 core task 的基础正式比较**
  - 默认 owned_paths：`runs/benchmark-v0.5/base-v0.4/` manifests、`workstreams/benchmark_v1/reports/formal-base-v0.4.json`、对应图表数据。
  - 依赖：reference evidence 冻结、Bench manifest 已签发。
  - [ ] 在同一配对 Bench base cells 上运行全部已封存方法；严格按 interaction strata 分析。
  - [ ] 每个 cell 完成即时回放、资源对账和失败分类；不因方法失败补 seed、改 prompt、换 checkpoint 或重跑到成功。
  - [ ] 按 task 报告主指标、联合安全/成本规则、anytime 曲线、完成率和资源前沿；保留负结果。
  - [ ] 用预注册统计代码一次性生成结果，不在看完结果后改 SESOI、排除规则或主比较。
  - 验收：预期笛卡尔积完整或明确标记 incomplete；只有同时满足联合规则的方法比较可作正式结论。

- [ ] **`benchmark-v05-base-reproduction` — 基础矩阵独立 clean-wheel 复核**
  - 默认 owned_paths：`workstreams/benchmark_v1/reports/formal-base-reproduction-v0.4.json`、复核 manifests。
  - 依赖：formal base matrix 完成。
  - [ ] 在独立干净环境复算所有结果 digests、统计表和图；抽取预注册比例的轨迹从动作日志重放。
  - [ ] 核实失败分母、资源账本、成对 cell 和 reference 绑定，没有手工补文件或绝对路径依赖。
  - 验收：复核报告与原报告在声明容差内一致；不一致时 P4 失败并回到新的协议版本。

## P5：在基础结果通过后做机制与信息消融

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

先串行完成 P0 的证据隔离与合同一致性，再并行推进组合压力、观测可辨识性和任务有效性，最后由 portable release 集成收口。P1 的交互合同、统计方案和 reference plan 可在 formal protocol 0.4 建立后并行。P2 的 orchestrator 与 resource accounting 可并行，但必须由 preflight 统一验收。P3 三类方法可并行开发，method freeze 最后收口。P4 必须严格按“reference evidence → base matrix → reproduction”串行；P5 的三个实验可在 P4 通过后并行；P6 最后串行审计和发布。
