# ChemWorld 多团队执行清单

最后更新：2026-07-12

## 0. 所有成员开始工作前

- [ ] 阅读 `claims/README.md`、本文件和目标模块附近的测试。
- [ ] 执行 `git pull --ff-only origin main`。
- [ ] 执行 `.\.venv\Scripts\python.exe scripts\manage_claims.py list`，确认任务尚未被认领。
- [ ] 只认领下文一个 Task ID；不得把协议、实现、正式实验和论文写作塞进同一 claim。
- [ ] 在 claim 中列出精确 `owned_paths`；不得使用仓库根目录、`src`、`tests` 等宽泛路径。
- [ ] 将 active claim 作为独立提交先推送到 `main`，再开始修改。
- [ ] 依赖未完成时可以认领并开展不依赖最终输入的设计/单元实现，但不得冻结协议、启动正式实验或关闭任务。
- [ ] 发现需要修改未认领文件时，先更新并推送 claim；不得先改后补。
- [ ] 不提交 API key、模型私有思维链、真实设备凭证、未脱敏路径或私有 Bench 数据。

## 1. 每项任务的统一完成要求

- [ ] 实现只修改 claim 的 `owned_paths`，且与其他 active claim 不重叠。
- [ ] 新合同具有 schema/version、单位、边界、缺失值、异常值和 fail-closed 语义。
- [ ] 新随机过程声明 seed；相同合同、seed 和 action 必须得到可回放结果。
- [ ] 新评价同时区分 objective、constraint、resource、validity 和 training shaping。
- [ ] 新实验保留失败、超时、非法动作和零结果，不允许静默过滤。
- [ ] 报告包含协议 hash、代码 commit、dirty-tree 状态、轨迹摘要、资源账本和主张边界。
- [ ] 单元测试覆盖正常路径、边界、非法输入、回放篡改和至少一个反作弊案例。
- [ ] 运行任务专属测试和 `python -m ruff check`；共享运行时或发布任务还必须运行完整 `pytest`、`mypy` 和严格文档构建。
- [ ] 生成机器可读验收报告；“代码存在”或“脚本跑完”不等于科学门禁通过。
- [ ] 更新使用者可见行为对应的发布文档；内部路线、claim 和诊断不得进入公开站点。
- [ ] 执行 `.\.venv\Scripts\python.exe scripts\manage_claims.py check`。
- [ ] 使用 `manage_claims.py complete` 关闭认领，提交 completed claim、实现、测试和证据并推送 `main`。

## 2. 核心主张与硬边界

- [ ] Core 只主张 V0 软件有效性、V1 结构有效性和 V2 因果有效性。
- [ ] 独立 backend/Dataset Bridge 只在证据通过后主张 V3 行为有效性。
- [ ] 实体 Bridge 只在预注册迁移实验通过后主张 V4 迁移有效性。
- [ ] 不主张 V5 命名化学体系的通用数值预测有效性。
- [ ] 不使用“通用数字孪生”“真实产率预测器”或“零样本 sim-to-real”表述。
- [ ] H1–H4 均作为待检验假设，不提前写成结论。
- [ ] 旧 `publication_protocol_v0.1` 及其结果保持不可变；整改必须进入新协议版本。
- [ ] 默认正式任务为 provisional core-4：partition、crystallization、distillation、flow。
- [ ] electrochemistry 和 equilibrium 在通过独立 G1/G2 前保持 exploratory。

## 3. P0：冻结科学问题、任务集和关键合同

- [ ] **`benchmark-vnext-scientific-positioning` — 冻结科学定位**
  - 建议团队：核心科学/协议组。
  - 建议独占路径：`workstreams/benchmark_v1/protocols/scientific-positioning-vnext.md`、`configs/benchmark/scientific_positioning_vnext.json`、`tests/test_scientific_positioning.py`。
  - 依赖：无。
  - [ ] 将 H1 固定世界高估、H2 知识与实验智能分离、H3 显式适应有益、H4 虚拟训练迁移写成可反驳假设。
  - [ ] 为每个假设指定 primary endpoint、SESOI、失败条件和允许的主张。
  - [ ] 固定 V0–V5、Core/Benchmark/Bridge 和禁用表述。
  - [ ] 明确 H1–H3 属于核心 benchmark，H4 属于 Bridge。
  - [ ] 机器测试拒绝缺少终点、SESOI 或 claim boundary 的协议。
  - 验收：定位协议可由后续配置引用；不得包含预设实验结论。

- [ ] **`benchmark-vnext-core4-sesoi-freeze` — 冻结 core-4 任务有效性**
  - 建议团队：任务有效性组。
  - 建议独占路径：`configs/benchmark/core4_task_validity_vnext.json`、`scripts/audit_core4_task_validity.py`、`tests/test_core4_task_validity.py`、`workstreams/benchmark_v1/reports/core4-task-validity-freeze.json`。
  - 依赖：`benchmark-vnext-scientific-positioning`。
  - [ ] 分任务冻结 primary metric、单位、方向、absolute SESOI、风险阈值和成本阈值。
  - [ ] 给出最低合理策略、legal-random、强策略的预期可识别排序。
  - [ ] 冻结 confirmatory seeds，不使用已有诊断结果调阈值。
  - [ ] 明确 flow 的 core-candidate 升级/降级规则。
  - [ ] 保持 electrochemistry/equilibrium exploratory，不为六任务叙事降低阈值。
  - 验收：core-4 每项均有独立有效性卡；阈值来源和冻结时间可审计。

- [ ] **`benchmark-vnext-rl-hybrid-action-contract` — 混合动作合同**
  - 建议团队：RL 动作组。
  - 建议独占路径：`src/chemworld/rl/hybrid_actions.py`、`tests/test_rl_hybrid_actions.py`、`configs/benchmark/rl_hybrid_action_vnext.json`、`workstreams/benchmark_v1/reports/rl-hybrid-action-controls.json`。
  - 依赖：现有 typed public action contract。
  - [ ] 定义 categorical operation head。
  - [ ] 为每个 operation 定义 conditional parameter heads、类型、单位和边界。
  - [ ] 无关参数不得执行、不得进入损失、不得影响动作 digest。
  - [ ] 公共 affordance mask 在训练、评估和回放中语义一致。
  - [ ] 覆盖 operation/parameter 编解码 round-trip、非法 mask、NaN/Inf 和稳定序列化。
  - [ ] 明确 PPO、混合动作算法和 process-control SAC 分别使用的动作子合同。
  - 验收：不再把 28 个操作和 21 个全局参数当作一个 49 维连续控制量。

- [ ] **`benchmark-vnext-rl-reward-contract` — 训练奖励与防捷径合同**
  - 建议团队：RL 奖励/评测组。
  - 建议独占路径：`src/chemworld/rl/rewards.py`、`tests/test_rl_rewards.py`、`configs/benchmark/rl_reward_vnext.json`、`workstreams/benchmark_v1/reports/rl-reward-controls.json`。
  - 依赖：`benchmark-vnext-core4-sesoi-freeze`。
  - [ ] 删除或重构可支配策略的“完成实验 +1”奖励。
  - [ ] training shaping 与冻结评测 endpoint 完全分离。
  - [ ] 固定可比的完整实验、operation、measurement 和资源预算。
  - [ ] 添加 quick-close、重复测量、非法动作刷分、无核心操作完成和 reward scaling sensitivity 探针。
  - [ ] 证明 shaping 不改变冻结评测器，不通过 shaping return 选择最终主张。
  - [ ] flow 策略未执行 `run_flow` 时不得通过行为有效性门禁。
  - 验收：legal-random、捷径策略和任务合理策略形成可解释的训练/评测差异。

- [ ] **`benchmark-vnext-rl-contract-integration` — RL 共享运行时集成**
  - 建议团队：核心集成人；RL 动作组和奖励组不得同时修改这些文件。
  - 建议独占路径：`src/chemworld/rl/environment.py`、`src/chemworld/rl/training.py`、`src/chemworld/rl/evaluation.py`、`src/chemworld/wrappers.py`、`tests/test_rl_contract_integration.py`。
  - 依赖：hybrid action 和 reward 两项控制报告通过。
  - [ ] 移除正式训练对旧 `ContinuousEventActionWrapper` 的依赖；旧接口只保留显式 legacy 路径。
  - [ ] 训练 manifest 绑定动作/奖励合同 hash。
  - [ ] 冻结评估禁用 training shaping。
  - [ ] checkpoint、replay buffer、资源账本和轨迹验证保持兼容。
  - [ ] 旧 100k checkpoint 标记为 incompatible/diagnostic，不可进入正式排名。
  - 验收：完整 RL 测试、完整 `pytest`、ruff、mypy 全部通过。

- [ ] **`benchmark-vnext-mechanism-adaptation-protocol` — 机制适应协议**
  - 建议团队：世界族/因果评测组。
  - 建议独占路径：`configs/benchmark/mechanism_adaptation_vnext.json`、`scripts/audit_mechanism_adaptation_protocol.py`、`tests/test_mechanism_adaptation_protocol.py`、`workstreams/benchmark_v1/reports/mechanism-adaptation-protocol.json`。
  - 依赖：scientific positioning、core-4 SESOI、已有 mechanism-family controls。
  - [ ] 冻结 core-4 的 mechanism-family Train/Dev/Bench 分配。
  - [ ] 将 seed、参数插值/外推、composition、noise 与 rate-law/topology/constitutive-law shift 分开。
  - [ ] 定义 stationary、episode-boundary shift 和 within-campaign change point。
  - [ ] 定义 detection delay、adaptation regret、experiments-to-recovery、transfer-vs-scratch、风险和成本。
  - [ ] 机制分类准确率只能作诊断，不能替代决策终点。
  - [ ] 冻结 severity，确保非灾难、可辨识且会改变合理行动。
  - 验收：协议可在不泄露 family identity 的情况下生成确定性世界分配。

- [ ] **`benchmark-vnext-prior-disclosure-protocol` — 材料先验与谱图干预协议**
  - 建议团队：Agent 因果实验组。
  - 建议独占路径：`configs/benchmark/prior_disclosure_vnext.json`、`src/chemworld/agents/prior_disclosure.py`、`tests/test_prior_disclosure.py`、`workstreams/benchmark_v1/reports/prior-disclosure-controls.json`。
  - 依赖：scientific positioning、现有 live-LLM 谱图边界。
  - [ ] 同一隐藏世界支持 Opaque、Descriptor、Named/Retrieval 和 diagnostic-only Oracle。
  - [ ] Descriptor 带不确定性，不泄露隐藏 provider 参数。
  - [ ] 加入 material-label permutation 和 semantic-prior conflict。
  - [ ] 加入 assigned/masked/peak-permuted spectra 与 memory retained/deleted 配对条件。
  - [ ] 所有配对条件保持非干预公共状态一致。
  - [ ] Oracle 永不进入正式排行榜。
  - 验收：测试证明披露条件只改变指定信息，不改变 world law、预算或评分。

- [ ] **`benchmark-vnext-security-freeze-integration` — 安全与不变性正式绑定**
  - 建议团队：安全/评测组。
  - 建议独占路径：`configs/benchmark/security_freeze_vnext.json`、`scripts/audit_security_freeze.py`、`tests/test_security_freeze.py`、`workstreams/benchmark_v1/reports/security-freeze-controls.json`。
  - 依赖：core-4 SESOI、已有 public harness/exploit/semantic-invariance controls。
  - [ ] 将 12 组已通过的 semantic invariance 绑定冻结 public harness。
  - [ ] 绑定隐藏状态、debug、异常、路径、任务文本和私有 seed 泄漏扫描。
  - [ ] 绑定无成本测量、预算边界、非法刷分、NaN/Inf、重复 assay、提前结束和 replay 篡改探针。
  - [ ] Windows 和 clean-wheel 环境均 fail closed。
  - 验收：任何 probe 失败均阻止正式方法运行和 release。

## 4. P1：最小可识别方法矩阵

- [ ] **`benchmark-vnext-reference-portfolio-substrate` — 独立参考组合底座（已被 knitua 认领）**
  - [ ] 其他团队不得修改该 active claim 的五个 owned paths。
  - [ ] 完成 candidate substrate、失败关闭、回放验证和非正式主张边界。
  - 验收：以该 claim 的完成报告为准；当前仍不能称 oracle。

- [ ] **`benchmark-vnext-reference-portfolio-search` — 正式 best-known/reference 搜索**
  - 建议团队：独立参考搜索组。
  - 建议独占路径：新的 reference search 配置、运行脚本、轨迹目录和正式摘要；不得覆盖 substrate 文件。
  - 依赖：reference substrate、core-4 freeze、score/replay。
  - [ ] 预注册搜索方法、预算、seeds 和停止条件。
  - [ ] 搜索轨迹通过统一 replay evaluator。
  - [ ] 报告 coverage 和不确定性，不把有限搜索最大值命名为真实 oracle。
  - 验收：reference 只用于 regret 分母和覆盖诊断，不泄露给 agent。

- [ ] **`benchmark-vnext-classic-confirmatory` — 经典方法正式矩阵**
  - 建议团队：经典优化组。
  - 建议独占路径：新的 confirmatory 配置、运行脚本、轨迹目录和摘要。
  - 依赖：全部 P0 门禁、reference protocol。
  - [ ] 运行 random、LHS、greedy、typed GP-EI、typed constrained GP；扩展方法只作 secondary。
  - [ ] 每任务使用相同完整实验预算、paired seeds 和公共 observation。
  - [ ] 验证方法行为不退化为同一候选序列。
  - [ ] 报告 primary、risk、cost、regret 和资源前沿，不只报告 total score。
  - [ ] 保留 Safe-GP 在 flow 未达 SESOI 的负结果。
  - 验收：所有轨迹 replay 通过；统计计划在看结果前冻结。

- [ ] **`benchmark-vnext-procedure-rl-baselines` — Procedure Execution RL**
  - 建议团队：RL procedure 组。
  - 建议独占路径：新的 recurrent PPO/混合动作方法模块、测试、配置、checkpoint manifest 和报告。
  - 依赖：RL contract integration、mechanism adaptation protocol。
  - [ ] 实现 legal-random、recurrent PPO 和一个 parameterized hybrid-action 方法。
  - [ ] history/recurrent state 只接收公共 observation。
  - [ ] 先在单任务多 seed 上超过 legal-random，再扩 core-4。
  - [ ] operation coverage 必须包含任务核心操作。
  - [ ] checkpoint 只用 pooled Dev 选择；Bench 在冻结前不可访问。
  - 验收：多 seed、重放、资源账本和 adaptation endpoint 全部报告。

- [ ] **`benchmark-vnext-flow-control-baselines` — Process Control 基线**
  - 建议团队：控制/MPC 组。
  - 建议独占路径：`src/chemworld/control/` 下新模块、对应测试、控制协议和报告。
  - 依赖：独立 process-control 子合同、RL integration。
  - [ ] 实现规则/PID 下界、system identification + MPC 和 SAC。
  - [ ] 三者使用相同状态、执行器、延迟、噪声、风险和控制周期。
  - [ ] SAC 只用于连续控制参数，不负责离散实验流程。
  - [ ] 报告 tracking/endpoint、constraint、energy/resource、adaptation 和计算成本。
  - 验收：不得与 campaign design 方法通过一个无解释总分直接排名。

- [ ] **`benchmark-vnext-context-model-baseline` — 显式上下文/world-model 基线**
  - 建议团队：适应学习组。
  - 建议独占路径：`src/chemworld/adaptation/` 下新模块、测试、配置和报告。
  - 依赖：mechanism adaptation protocol。
  - [ ] 只选择一个可审计的 context encoder 或 latent world-model + planning 代表。
  - [ ] 输出 belief/context、不确定性和用于选择实验的公开摘要。
  - [ ] 与同架构无记忆、随机 context 和错误 context 做配对。
  - [ ] 评估 H3 的 adaptation regret 和 experiments-to-recovery。
  - 验收：先证明能力轴，再决定是否扩展 Dreamer/TD-MPC/PEARL/VariBAD 等方法。

- [ ] **`benchmark-vnext-live-llm-confirmatory` — 真实 LLM 冻结矩阵**
  - 建议团队：LLM 运行组。
  - 建议独占路径：新的 live-LLM confirmatory 配置、运行脚本、脱敏轨迹索引和报告。
  - 依赖：prior disclosure、method protocol、P0 security。
  - [ ] 只通过官方 operation-level adapter 调用，不使用 Task Lab 代替正式 runner。
  - [ ] 运行冻结模型角色、paired seeds 和 core tasks。
  - [ ] 保留 API 失败、重试、非法输出、token、费用、墙钟和模型版本。
  - [ ] 不保存私有思维链；只保存结构化假设、证据引用、行动理由和置信度。
  - [ ] masked/assigned 条件必须保持非谱图证据一致。
  - 验收：轨迹 replay、provider usage 和费用 reconciliation 全部通过。

- [ ] **`benchmark-vnext-llm-causal-ablation` — LLM 证据使用因果实验**
  - 建议团队：LLM 因果评测组；不得与 live 运行组共用输出路径。
  - 建议独占路径：新的配对干预脚本、统计配置、报告和测试。
  - 依赖：live-LLM confirmatory、prior disclosure。
  - [ ] 在相同公共状态比较谱图可见/遮蔽/峰置换。
  - [ ] 比较记忆保留/删除和语义一致/冲突。
  - [ ] 测量行动变化、后续结果、change-detection delay 和锚定恢复。
  - [ ] `adaptation_source` 和自然语言解释只能作诊断，不能作为因果使用证据。
  - 验收：预注册配对统计支持或反驳 H2；不做型号数量竞赛。

- [ ] **`benchmark-vnext-method-matrix-integration` — 跨方法公平性集成**
  - 建议团队：核心评测集成人。
  - 建议独占路径：冻结总协议、统一 runner 入口、矩阵摘要和集成测试。
  - 依赖：classic、procedure RL、flow control、context model、live LLM 各自产出。
  - [ ] 检查任务合同、seeds、实验预算、公共 observation 和资源账本一致。
  - [ ] campaign、procedure、process-control 分轨报告。
  - [ ] 只在相同交互层级内做算法归因。
  - [ ] 失败方法和缺失单元显式进入矩阵。
  - 验收：任何合同 hash 不一致均拒绝汇总。

## 5. P2：机制适应主实验与统计

- [ ] **`benchmark-vnext-h1-fixed-vs-shift` — H1 固定世界与机制变化**
  - 建议团队：主实验 A 组。
  - 依赖：method matrix integration。
  - [ ] 比较 IID、参数 shift、机制 shift 下的 primary/risk/cost 排名。
  - [ ] 报告 rank correlation、rank inversion 和安全性变化。
  - [ ] 不预设必须发生排名反转。
  - 验收：paired bootstrap、Holm 和 SESOI 同时报告。

- [ ] **`benchmark-vnext-h2-prior-anchoring` — H2 先验与实验智能**
  - 建议团队：主实验 B 组。
  - 依赖：LLM causal ablation，可加入非 LLM 对照。
  - [ ] 比较 Opaque/Descriptor/Named-Retrieval。
  - [ ] 比较 congruent、label-permuted 和 semantic-conflict worlds。
  - [ ] 报告初始样本效率、证据更新、锚定恢复和行动质量。
  - 验收：将化学知识收益与证据驱动适应分开。

- [ ] **`benchmark-vnext-h3-adaptation` — H3 显式世界模型适应**
  - 建议团队：主实验 C 组。
  - 依赖：context model、procedure/control baselines。
  - [ ] 比较显式适应、无记忆、model-free 和经典局部模型。
  - [ ] 报告 change-detection delay、adaptation regret、恢复实验数、风险和成本。
  - [ ] 报告任务和机制族异质性。
  - 验收：结论必须来自冻结 endpoint，不使用解释文本代替行为结果。

- [ ] **`benchmark-vnext-statistics-figures` — 冻结统计与图形**
  - 建议团队：统计/可视化组。
  - 建议独占路径：新统计脚本、figure specs、矢量图和 source-data 表。
  - 依赖：H1–H3 冻结摘要。
  - [ ] paired bootstrap、Holm、SESOI、rank stability 和预算曲线齐全。
  - [ ] 图只读取签名摘要，不读取临时轨迹或手工数值。
  - [ ] 每张图有 source data、生成命令和 digest。
  - [ ] 负结果和未通过门禁以同等可见度展示。
  - 验收：从干净环境可确定性重建全部图。

## 6. P3：Train / Bench / Bridge

- [ ] **`chemworld-train-generator` — Train 世界生成器**
  - 建议团队：训练环境组。
  - [ ] 程序化生成机制族、难度课程和向量化 reset/step。
  - [ ] Train/Dev 不包含冻结 Bench worlds。
  - [ ] 生成分布、seed 空间和 curriculum 可审计。
  - 验收：训练吞吐、确定性和隔离测试通过。

- [ ] **`benchmark-vnext-dataset-bridge` — DatasetOracle Bridge**
  - 建议团队：数据桥接组。
  - [ ] 选择一个授权清晰、任务同构的 partition 或 flow 数据集。
  - [ ] 实现 Train/Calibration/Test 隔离、缺失值 fail-closed 和不确定性。
  - [ ] 禁止 agent 查询 held-out 真值。
  - [ ] 比较 virtual-pretrained 与同架构 scratch 的少样本适应。
  - 验收：报告 transfer advantage、实验节省和失败模式，不要求数值完美相关。

- [ ] **`benchmark-vnext-independent-backend` — 独立高保真后端**
  - 建议团队：外部后端组。
  - [ ] 为 partition 或 flow 实现训练期不可见、代码和参数来源独立的 backend。
  - [ ] 保持公共 action/observation/trajectory 合同。
  - [ ] 不针对某个方法调后端。
  - [ ] 报告跨后端排名、适应收益和 core-specific failure。
  - 验收：形成 V3 行为有效性证据或明确失败。

- [ ] **`benchmark-vnext-h4-transfer` — H4 虚拟预训练迁移**
  - 建议团队：迁移实验组。
  - 依赖：Train generator、Dataset Bridge 或 independent backend。
  - [ ] 冻结相同架构、相同现实/外部数据预算和 checkpoint 选择规则。
  - [ ] 比较 virtual-pretrained、scratch、BO/Safe-BO 和固定 DOE。
  - [ ] 报告 k-shot transfer curve、adaptation regret、实验节省、安全和不确定性。
  - 验收：无显著迁移收益时明确反驳 H4，不更换主终点。

- [ ] **`benchmark-vnext-physical-partition-bridge` — 实体 partition 工程闭环**
  - 建议团队：外部实验组。
  - 依赖：H4 在 Dataset/independent backend 上完成；不阻塞 Core release。
  - [ ] LLM/Agent 只输出结构化意图。
  - [ ] schema validation、硬安全约束、人工批准和确定性执行层独立。
  - [ ] 冻结真实实验预算、失败记录和人工干预账本。
  - 验收：只主张适应成本和实验节省，不把 Core 风险分数解释为现实安全。

- [ ] **`benchmark-vnext-physical-flow-bridge` — 实体 flow 旗舰桥接**
  - 建议团队：外部实验/控制组。
  - 依赖：partition 工程链和独立 flow backend。
  - [ ] 先 shadow mode，再 supervised closed loop，再评估窄域 autonomous loop。
  - [ ] 设备 adapter 与 LLM 决策隔离。
  - [ ] MPC、SAC、BO 和 virtual-pretrained 使用相同真实预算。
  - 验收：外部实验室可独立重复；否则只作工程示范。

## 7. P4：独立复现、发布与论文

- [ ] **`benchmark-vnext-independent-reproduction` — 第三方干净复现**
  - 建议团队：未参与实现的复现组。
  - [ ] 从 clean wheel 和公开命令重建指定 seeds。
  - [ ] 对比协议 hash、trajectory digest、摘要和数值容差。
  - [ ] 不访问开发者缓存、API key、私有路径或未发布数据。
  - 验收：复现报告和全部失败公开保留。

- [ ] **`benchmark-vnext-private-evaluation` — 私有 Bench 评测**
  - 建议团队：独立评测组。
  - [ ] 私有 worlds/salts 与开发团队隔离。
  - [ ] 使用同一公开合同和冻结 evaluator。
  - [ ] 检查提交包的资源、依赖、超时和泄漏。
  - 验收：私评摘要可公开，私有实例不泄露。

- [ ] **`benchmark-vnext-release` — 发布候选**
  - 建议团队：发布集成人。
  - [ ] wheel、公开合同、seed suite、报告、golden trajectory 和验证命令齐全。
  - [ ] 本地完整门禁通过，不依赖 CI/GitHub Actions。
  - [ ] 用户文档只包含发布级内容和真实限制。
  - [ ] 打不可变 tag，记录 source/evidence digests。
  - 验收：clean install、replay、docs strict build 和 release gate 全通过。

- [ ] **`paper-chemworld-final` — 论文与 PDF**
  - 建议团队：论文组；不得在 H1–H3 和复现冻结前认领。
  - [ ] 标题跟随结果，不预设 Nature 叙事。
  - [ ] 主文只写主张矩阵允许的结论。
  - [ ] Methods、Extended Data、source data、代码/数据可用性和 limitations 完整。
  - [ ] H4 未完成时只写 V0–V3 范围；实体 bridge 不得用模拟结果替代。
  - [ ] LaTeX 无错误渲染 PDF，图表从冻结 source data 生成。
  - 验收：论文、PDF、release tag 和证据 commit 一致。

## 8. 建议的并行批次

- [ ] **批次 A，可立即并行认领**
  - [ ] scientific positioning。
  - [ ] core-4 SESOI freeze。
  - [ ] RL hybrid action contract。
  - [ ] RL reward contract。
  - [ ] mechanism adaptation protocol。
  - [ ] prior disclosure protocol。
  - [ ] security freeze integration。
  - [ ] reference portfolio substrate 由现认领者继续完成。

- [ ] **批次 B，P0 各自控制报告通过后并行**
  - [ ] RL contract integration。
  - [ ] reference portfolio search。
  - [ ] classic confirmatory。
  - [ ] procedure RL。
  - [ ] flow control。
  - [ ] context/world-model。
  - [ ] live LLM confirmatory。

- [ ] **批次 C，方法矩阵冻结后并行**
  - [ ] H1 fixed-vs-shift。
  - [ ] H2 prior anchoring。
  - [ ] H3 adaptation。
  - [ ] Train generator。
  - [ ] Dataset Bridge。

- [ ] **批次 D，主实验冻结后**
  - [ ] statistics/figures。
  - [ ] independent backend。
  - [ ] H4 transfer。
  - [ ] independent reproduction。
  - [ ] private evaluation。

- [ ] **批次 E，最后执行**
  - [ ] physical bridge。
  - [ ] release。
  - [ ] final paper/PDF。

## 9. 已完成且不得重复认领

- [x] World Law v0.4：8 个正式 provider 接入，旧正式 proxy/fallback 路由移除。
- [x] 六任务基础合同、守恒、单位、回放和 release integrity 候选底座。
- [x] 600 条经典方法正式旧协议运行及 public/private shift 历史证据。
- [x] 六任务 12 个 world-family 轴和四类参数/组成/噪声控制。
- [x] core-6 mechanism/constitutive-law family 控制、校准和回放绑定。
- [x] 风险—成本信号校准、实验峰值风险和三类成本账本。
- [x] 六层评价、交互能力层级、资源账本和只读 replay evaluator。
- [x] operation-level Agent 公共上下文、谱图递交、decision audit 和能力声明。
- [x] live-LLM 官方 adapter、跨实验记忆、失败保留和资源计费控制。
- [x] assigned/masked 谱图边界，非谱图证据保持一致。
- [x] semantic invariance：6 tasks × 2 seeds = 12 组配对、五类 probe 全部通过。
- [x] public harness、基础 exploit、public-boundary 和 replay-integrity 控制。
- [x] typed GP/RF acquisitions、task-aware greedy 和方法 distinctness 控制。
- [x] score/replay、primary evidence、confirmatory freeze 和 method protocol 底座。
- [x] Safe-GP 失败诊断：保留 flow 未达到预注册 SESOI 的负结果。
- [x] SAC 100k 工程记账与回放诊断。
- [x] 已确认旧 RL 49 维 Box 与完成实验 shaping 诱导 quick-close；旧 checkpoint 禁止用于正式能力结论。
- [x] reactor state、操作叠加/重置、历史谱图访问和 Task Lab 学生动画审计。
- [x] 核心 operation semantics、extractant identity coupling 和旧别名清理。
- [x] 用户文档、站点、main/gh-pages 现有发布底座。
- [x] Nature 稿件结构草案和 figure scaffold；仅为写作底座，不代表论文证据完成。

## 10. 本地总门禁

- [ ] `.\.venv\Scripts\python.exe scripts\manage_claims.py check`
- [ ] `.\.venv\Scripts\python.exe scripts\audit_publication_protocol.py`
- [ ] `.\.venv\Scripts\python.exe scripts\audit_publication_generalization_security.py`
- [ ] `.\.venv\Scripts\python.exe scripts\run_release_gate.py`
- [ ] `.\.venv\Scripts\python.exe -m pytest`
- [ ] `.\.venv\Scripts\python.exe -m ruff check .`
- [ ] `.\.venv\Scripts\python.exe -m mypy src`
- [ ] `.\.venv\Scripts\python.exe -m mkdocs build --strict`
