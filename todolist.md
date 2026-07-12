# ChemWorld 执行清单

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

## 2. 小团队快速迭代补充说明

### 2.1 认领、拆分与状态

- [ ] 任何人都可以自行认领任意未被占用的任务；本文件不预设固定岗位、团队或长期负责人。
- [ ] 每次优先认领一个可在约 0.5–2 个工作日内形成独立验收物的最小切片，完成后再认领下一项。
- [ ] 如果一个 Task ID 过大，可创建 `原-task-id--slice-序号-简短名称`；claim notes 必须写明父 Task ID、输入、输出和不处理的内容。
- [ ] 同一父任务的多个 slice 必须拥有互不重叠的文件；需要修改共享文件的部分统一留给该父任务的 integration slice。
- [ ] 父任务只有在所有子检查项、所有 slice 和最终集成验收都完成后才能勾选 `[x]`。
- [ ] `[ ]` 只表示尚未完成；是否已认领必须以 `claims/active/` 为准，不能仅凭本文件判断。
- [ ] active claim 表示有人正在实现，不表示方案已被接受；completed claim 表示交付通过当时门禁，不自动形成论文结论。
- [ ] 依赖尚未完成时，只能实现与最终输入无关的纯模块、schema 草案和单元测试；不得冻结数值、运行正式实验或伪造上游摘要。
- [ ] 阻塞时在 claim notes 和报告中记录具体缺失输入、尝试过的替代方案和可继续工作的边界，不降低验收条件。
- [ ] 快速迭代仍然必须先推送 claim；“只改几行”不是跳过认领和测试的理由。

### 2.2 文件边界与交接

- [ ] 每项任务列出的“默认 owned_paths”是推荐的冲突隔离边界；认领时必须根据实际文件写成精确路径。
- [ ] 新功能优先放入任务独占的新模块、新配置、新测试和新报告，避免多人同时编辑中央 registry、runner 或大型测试文件。
- [ ] `src/chemworld/wrappers.py`、RL environment/training/evaluation、task registry、正式协议、发布摘要和 golden trajectory 属于共享集成面，只能由明确的 integration/release claim 修改。
- [ ] 上游任务交付机器可读 config/report；下游任务通过 schema version 和 SHA-256 引用，不复制粘贴数值，也不直接修改上游报告。
- [ ] 生产者必须在报告中列出稳定输出字段；消费者只依赖这些字段，不解析日志文本、终端输出或文件名猜测状态。
- [ ] 需要扩展上游 schema 时，先在本任务独占文件中提交提案和失败测试，再由上游或 integration claim 合并。
- [ ] 合并时只做必要改动，不顺手格式化无关目录、不移动他人文件、不重写已有证据。
- [ ] 如果两个任务最终必须修改同一文件，先完成各自独立模块，再顺序执行一个单独 integration claim；不得并行抢改。

### 2.3 每个交付包必须包含什么

- [ ] **协议/config**：声明 schema version、任务范围、输入、输出、seed、预算、阈值、单位、缺失/异常语义和冻结状态。
- [ ] **实现**：公共 API 有类型、文档和确定性边界；不读取未声明的全局状态、私有路径或开发者缓存。
- [ ] **测试**：至少包含成功、边界、非法输入、确定性/回放、篡改拒绝和一个该任务特有的反作弊案例。
- [ ] **审计脚本**：从配置和原始产物重新计算控制结论；不得只检查报告中的布尔值。
- [ ] **机器报告**：至少包含 `schema_version`、`protocol_id/hash`、`source_commit`、`source_tree_dirty`、检查项、限制、剩余门禁和 `benchmark_claim_allowed`。
- [ ] **人类摘要**：在 completed claim 的 summary 中说明完成了什么、没有完成什么、负结果和下一依赖；不得使用“全面完成”代替具体证据。
- [ ] **公开文档**：只有用户接口、安装、运行方式或公开限制改变时才更新；研究路线和内部诊断继续留在本文件或 workstreams。
- [ ] **大文件清单**：checkpoint、轨迹和数据集必须有大小、digest、生成命令和保留策略；禁止无说明提交临时缓存。

### 2.4 证据等级不得混用

- [ ] **Control-ready**：schema、单元测试、确定性和最小控制探针通过；只说明基础设施可用。
- [ ] **Diagnostic**：可在 Dev 或少量 seed 上发现问题和选择后续设计；不得进入正式排名或论文主结论。
- [ ] **Frozen confirmatory**：协议、seeds、endpoint、SESOI 和统计计划在运行前冻结，完整保留失败，才可支持预注册比较。
- [ ] **Independent reproduction**：未参与实现者从 clean wheel 重建摘要，才可解锁发布级复现主张。
- [ ] **Bridge evidence**：使用独立数据/backend/设备和相同适应预算比较 pretrained 与 scratch，才可讨论 V3/V4。
- [ ] 报告必须显式写出当前等级；下游不得把 control-ready 或 diagnostic 结果重命名为 formal evidence。

### 2.5 关键术语的执行含义

- [ ] **Freeze**：协议内容、hash、seeds、预算、endpoint 和统计计划不可再因结果修改；任何变更生成新版本。
- [ ] **Primary endpoint**：每任务唯一预注册主终点；total score、训练 return 或解释质量不能临时替代。
- [ ] **SESOI**：最小有科学意义的效应，不等同于 `p < 0.05`；必须给出单位、方向和来源。
- [ ] **Paired seeds**：方法在同一隐藏世界/干预上配对，seed 分配在运行前冻结，失败对仍保留。
- [ ] **Replay verified**：从原始 action/observation/ledger 重新执行或重算，与摘要在容差内一致；只校验文件 hash 不够。
- [ ] **Fail closed**：缺配置、缺字段、hash 不符、NaN/Inf、越权观察或资源账本不完整时拒绝形成结果，而不是填默认值继续。
- [ ] **Train/Dev/Bench**：Train 用于学习，Dev 只用于预注册选择，Bench 只用于冻结后评价；三者 world family 和 seed 不重叠。
- [ ] **Core operation coverage**：策略实际执行决定任务物理结果的操作；仅合法地加料、终止、测量不算完成任务能力。
- [ ] **Transfer-vs-scratch**：相同架构、相同外部实验预算和相同选择规则下比较预训练与从零学习。
- [ ] **Bridge**：验证适应策略和方法排序能否迁移，不要求 Core 数值逐点预测真实化学。

### 2.6 快速自检与交接顺序

- [ ] 先运行新增测试，再运行受影响模块测试；不要一开始只跑全库测试掩盖局部失败原因。
- [ ] 控制报告通过后，检查其是否仍标记 `benchmark_claim_allowed=false`；正式主张必须等待 confirmatory task。
- [ ] 提交前运行 `git diff --check`、claim check、ruff，并确认 `git status` 没有密钥、缓存和无关文件。
- [ ] 共享运行时、协议集成、正式实验、发布任务再运行完整 pytest、mypy、strict docs 和 release gate。
- [ ] 推送 completed claim 后，在下一个认领的 notes 中引用上游 completed claim、commit 和 report hash，形成可追踪交接链。

## 3. 核心主张与硬边界

- [ ] Core 只主张 V0 软件有效性、V1 结构有效性和 V2 因果有效性。
- [ ] 独立 backend/Dataset Bridge 只在证据通过后主张 V3 行为有效性。
- [ ] 实体 Bridge 只在预注册迁移实验通过后主张 V4 迁移有效性。
- [ ] 不主张 V5 命名化学体系的通用数值预测有效性。
- [ ] 不使用“通用数字孪生”“真实产率预测器”或“零样本 sim-to-real”表述。
- [ ] H1–H4 均作为待检验假设，不提前写成结论。
- [ ] 旧 `publication_protocol_v0.1` 及其结果保持不可变；整改必须进入新协议版本。
- [ ] 默认正式任务为 provisional core-4：partition、crystallization、distillation、flow。
- [ ] electrochemistry 和 equilibrium 在通过独立 G1/G2 前保持 exploratory。

## 4. P0：冻结科学问题、任务集和关键合同

- [ ] **`benchmark-vnext-scientific-positioning` — 冻结科学定位**
  - 默认 owned_paths：`workstreams/benchmark_v1/protocols/scientific-positioning-vnext.md`、`configs/benchmark/scientific_positioning_vnext.json`、`tests/test_scientific_positioning.py`。
  - 依赖：无。
  - [ ] 将 H1 固定世界高估、H2 知识与实验智能分离、H3 显式适应有益、H4 虚拟训练迁移写成可反驳假设。
  - [ ] 为每个假设指定 primary endpoint、SESOI、失败条件和允许的主张。
  - [ ] 固定 V0–V5、Core/Benchmark/Bridge 和禁用表述。
  - [ ] 明确 H1–H3 属于核心 benchmark，H4 属于 Bridge。
  - [ ] 机器测试拒绝缺少终点、SESOI 或 claim boundary 的协议。
  - 验收：定位协议可由后续配置引用；不得包含预设实验结论。

- [ ] **`benchmark-vnext-core4-sesoi-freeze` — 冻结 core-4 任务有效性**
  - 默认 owned_paths：`configs/benchmark/core4_task_validity_vnext.json`、`scripts/audit_core4_task_validity.py`、`tests/test_core4_task_validity.py`、`workstreams/benchmark_v1/reports/core4-task-validity-freeze.json`。
  - 依赖：`benchmark-vnext-scientific-positioning`。
  - [ ] 分任务冻结 primary metric、单位、方向、absolute SESOI、风险阈值和成本阈值。
  - [ ] 给出最低合理策略、legal-random、强策略的预期可识别排序。
  - [ ] 冻结 confirmatory seeds，不使用已有诊断结果调阈值。
  - [ ] 明确 flow 的 core-candidate 升级/降级规则。
  - [ ] 保持 electrochemistry/equilibrium exploratory，不为六任务叙事降低阈值。
  - 验收：core-4 每项均有独立有效性卡；阈值来源和冻结时间可审计。

- [ ] **`benchmark-vnext-rl-hybrid-action-contract` — 混合动作合同**
  - 默认 owned_paths：`src/chemworld/rl/hybrid_actions.py`、`tests/test_rl_hybrid_actions.py`、`configs/benchmark/rl_hybrid_action_vnext.json`、`workstreams/benchmark_v1/reports/rl-hybrid-action-controls.json`。
  - 依赖：现有 typed public action contract。
  - [ ] 定义 categorical operation head。
  - [ ] 为每个 operation 定义 conditional parameter heads、类型、单位和边界。
  - [ ] 无关参数不得执行、不得进入损失、不得影响动作 digest。
  - [ ] 公共 affordance mask 在训练、评估和回放中语义一致。
  - [ ] 覆盖 operation/parameter 编解码 round-trip、非法 mask、NaN/Inf 和稳定序列化。
  - [ ] 明确 PPO、混合动作算法和 process-control SAC 分别使用的动作子合同。
  - 验收：不再把 28 个操作和 21 个全局参数当作一个 49 维连续控制量。

- [ ] **`benchmark-vnext-rl-reward-contract` — 训练奖励与防捷径合同**
  - 默认 owned_paths：`src/chemworld/rl/rewards.py`、`tests/test_rl_rewards.py`、`configs/benchmark/rl_reward_vnext.json`、`workstreams/benchmark_v1/reports/rl-reward-controls.json`。
  - 依赖：`benchmark-vnext-core4-sesoi-freeze`。
  - [ ] 删除或重构可支配策略的“完成实验 +1”奖励。
  - [ ] training shaping 与冻结评测 endpoint 完全分离。
  - [ ] 固定可比的完整实验、operation、measurement 和资源预算。
  - [ ] 添加 quick-close、重复测量、非法动作刷分、无核心操作完成和 reward scaling sensitivity 探针。
  - [ ] 证明 shaping 不改变冻结评测器，不通过 shaping return 选择最终主张。
  - [ ] flow 策略未执行 `run_flow` 时不得通过行为有效性门禁。
  - 验收：legal-random、捷径策略和任务合理策略形成可解释的训练/评测差异。

- [ ] **`benchmark-vnext-rl-contract-integration` — RL 共享运行时集成**
  - 集成约束：等待动作和奖励独立模块完成后再认领；其他认领不得同时修改这些共享文件。
  - 默认 owned_paths：`src/chemworld/rl/environment.py`、`src/chemworld/rl/training.py`、`src/chemworld/rl/evaluation.py`、`src/chemworld/wrappers.py`、`tests/test_rl_contract_integration.py`。
  - 依赖：hybrid action 和 reward 两项控制报告通过。
  - [ ] 移除正式训练对旧 `ContinuousEventActionWrapper` 的依赖；旧接口只保留显式 legacy 路径。
  - [ ] 训练 manifest 绑定动作/奖励合同 hash。
  - [ ] 冻结评估禁用 training shaping。
  - [ ] checkpoint、replay buffer、资源账本和轨迹验证保持兼容。
  - [ ] 旧 100k checkpoint 标记为 incompatible/diagnostic，不可进入正式排名。
  - 验收：完整 RL 测试、完整 `pytest`、ruff、mypy 全部通过。

- [ ] **`benchmark-vnext-mechanism-adaptation-protocol` — 机制适应协议**
  - 默认 owned_paths：`configs/benchmark/mechanism_adaptation_vnext.json`、`scripts/audit_mechanism_adaptation_protocol.py`、`tests/test_mechanism_adaptation_protocol.py`、`workstreams/benchmark_v1/reports/mechanism-adaptation-protocol.json`。
  - 依赖：scientific positioning、core-4 SESOI、已有 mechanism-family controls。
  - [ ] 冻结 core-4 的 mechanism-family Train/Dev/Bench 分配。
  - [ ] 将 seed、参数插值/外推、composition、noise 与 rate-law/topology/constitutive-law shift 分开。
  - [ ] 定义 stationary、episode-boundary shift 和 within-campaign change point。
  - [ ] 定义 detection delay、adaptation regret、experiments-to-recovery、transfer-vs-scratch、风险和成本。
  - [ ] 机制分类准确率只能作诊断，不能替代决策终点。
  - [ ] 冻结 severity，确保非灾难、可辨识且会改变合理行动。
  - 验收：协议可在不泄露 family identity 的情况下生成确定性世界分配。

- [ ] **`benchmark-vnext-prior-disclosure-protocol` — 材料先验与谱图干预协议**
  - 默认 owned_paths：`configs/benchmark/prior_disclosure_vnext.json`、`src/chemworld/agents/prior_disclosure.py`、`tests/test_prior_disclosure.py`、`workstreams/benchmark_v1/reports/prior-disclosure-controls.json`。
  - 依赖：scientific positioning、现有 live-LLM 谱图边界。
  - [ ] 同一隐藏世界支持 Opaque、Descriptor、Named/Retrieval 和 diagnostic-only Oracle。
  - [ ] Descriptor 带不确定性，不泄露隐藏 provider 参数。
  - [ ] 加入 material-label permutation 和 semantic-prior conflict。
  - [ ] 加入 assigned/masked/peak-permuted spectra 与 memory retained/deleted 配对条件。
  - [ ] 所有配对条件保持非干预公共状态一致。
  - [ ] Oracle 永不进入正式排行榜。
  - 验收：测试证明披露条件只改变指定信息，不改变 world law、预算或评分。

- [ ] **`benchmark-vnext-security-freeze-integration` — 安全与不变性正式绑定**
  - 默认 owned_paths：`configs/benchmark/security_freeze_vnext.json`、`scripts/audit_security_freeze.py`、`tests/test_security_freeze.py`、`workstreams/benchmark_v1/reports/security-freeze-controls.json`。
  - 依赖：core-4 SESOI、已有 public harness/exploit/semantic-invariance controls。
  - [ ] 将 12 组已通过的 semantic invariance 绑定冻结 public harness。
  - [ ] 绑定隐藏状态、debug、异常、路径、任务文本和私有 seed 泄漏扫描。
  - [ ] 绑定无成本测量、预算边界、非法刷分、NaN/Inf、重复 assay、提前结束和 replay 篡改探针。
  - [ ] Windows 和 clean-wheel 环境均 fail closed。
  - 验收：任何 probe 失败均阻止正式方法运行和 release。

## 5. P1：最小可识别方法矩阵

- [ ] **`benchmark-vnext-reference-portfolio-substrate` — 独立参考组合底座（已被 knitua 认领）**
  - 当前 owned_paths：`src/chemworld/eval/reference_portfolio.py`、`scripts/build_reference_portfolio.py`、`tests/test_reference_portfolio.py`、`configs/benchmark/reference_portfolio_vnext.json`、`workstreams/benchmark_v1/reports/reference-portfolio-controls.json`。
  - 依赖：已有 score/replay 和 reference-regret protocol；本任务仅交付 control-ready substrate。
  - [ ] 其他认领者不得修改该 active claim 的五个 owned paths。
  - [ ] 完成 candidate substrate、失败关闭、回放验证和非正式主张边界。
  - 验收：以该 claim 的完成报告为准；当前仍不能称 oracle。

- [ ] **`benchmark-vnext-reference-portfolio-search` — 正式 best-known/reference 搜索**
  - 默认 owned_paths：`configs/benchmark/reference_portfolio_search_vnext.json`、`scripts/run_reference_portfolio_search.py`、`tests/test_reference_portfolio_search.py`、`workstreams/benchmark_v1/trajectories/reference_portfolio_search/`、`workstreams/benchmark_v1/reports/reference-portfolio-search.json`；不得覆盖 substrate 文件。
  - 依赖：reference substrate、core-4 freeze、score/replay。
  - [ ] 预注册搜索方法、预算、seeds 和停止条件。
  - [ ] 搜索轨迹通过统一 replay evaluator。
  - [ ] 报告 coverage 和不确定性，不把有限搜索最大值命名为真实 oracle。
  - 验收：reference 只用于 regret 分母和覆盖诊断，不泄露给 agent。

- [ ] **`benchmark-vnext-classic-confirmatory` — 经典方法正式矩阵**
  - 默认 owned_paths：`configs/benchmark/classic_confirmatory_vnext.json`、`scripts/run_classic_confirmatory.py`、`tests/test_classic_confirmatory.py`、`workstreams/benchmark_v1/trajectories/classic_confirmatory/`、`workstreams/benchmark_v1/reports/classic-confirmatory.json`。
  - 依赖：全部 P0 门禁、reference protocol。
  - [ ] 运行 random、LHS、greedy、typed GP-EI、typed constrained GP；扩展方法只作 secondary。
  - [ ] 每任务使用相同完整实验预算、paired seeds 和公共 observation。
  - [ ] 验证方法行为不退化为同一候选序列。
  - [ ] 报告 primary、risk、cost、regret 和资源前沿，不只报告 total score。
  - [ ] 保留 Safe-GP 在 flow 未达 SESOI 的负结果。
  - 验收：所有轨迹 replay 通过；统计计划在看结果前冻结。

- [ ] **`benchmark-vnext-procedure-rl-baselines` — Procedure Execution RL**
  - 默认 owned_paths：`src/chemworld/rl/procedure_baselines.py`、`tests/test_rl_procedure_baselines.py`、`configs/benchmark/rl_procedure_vnext.json`、`workstreams/benchmark_v1/artifacts/procedure_rl/`、`workstreams/benchmark_v1/reports/rl-procedure-baselines.json`。
  - 依赖：RL contract integration、mechanism adaptation protocol。
  - [ ] 实现 legal-random、recurrent PPO 和一个 parameterized hybrid-action 方法。
  - [ ] history/recurrent state 只接收公共 observation。
  - [ ] 先在单任务多 seed 上超过 legal-random，再扩 core-4。
  - [ ] operation coverage 必须包含任务核心操作。
  - [ ] checkpoint 只用 pooled Dev 选择；Bench 在冻结前不可访问。
  - 验收：多 seed、重放、资源账本和 adaptation endpoint 全部报告。

- [ ] **`benchmark-vnext-flow-control-baselines` — Process Control 基线**
  - 默认 owned_paths：`src/chemworld/control/__init__.py`、`src/chemworld/control/baselines.py`、`tests/test_flow_control_baselines.py`、`configs/benchmark/flow_control_vnext.json`、`workstreams/benchmark_v1/reports/flow-control-baselines.json`。
  - 依赖：独立 process-control 子合同、RL integration。
  - [ ] 实现规则/PID 下界、system identification + MPC 和 SAC。
  - [ ] 三者使用相同状态、执行器、延迟、噪声、风险和控制周期。
  - [ ] SAC 只用于连续控制参数，不负责离散实验流程。
  - [ ] 报告 tracking/endpoint、constraint、energy/resource、adaptation 和计算成本。
  - 验收：不得与 campaign design 方法通过一个无解释总分直接排名。

- [ ] **`benchmark-vnext-context-model-baseline` — 显式上下文/world-model 基线**
  - 默认 owned_paths：`src/chemworld/adaptation/__init__.py`、`src/chemworld/adaptation/context_model.py`、`tests/test_context_model_baseline.py`、`configs/benchmark/context_model_vnext.json`、`workstreams/benchmark_v1/reports/context-model-baseline.json`。
  - 依赖：mechanism adaptation protocol。
  - [ ] 只选择一个可审计的 context encoder 或 latent world-model + planning 代表。
  - [ ] 输出 belief/context、不确定性和用于选择实验的公开摘要。
  - [ ] 与同架构无记忆、随机 context 和错误 context 做配对。
  - [ ] 评估 H3 的 adaptation regret 和 experiments-to-recovery。
  - 验收：先证明能力轴，再决定是否扩展 Dreamer/TD-MPC/PEARL/VariBAD 等方法。

- [ ] **`benchmark-vnext-live-llm-confirmatory` — 真实 LLM 冻结矩阵**
  - 默认 owned_paths：`configs/benchmark/live_llm_confirmatory_vnext.json`、`scripts/run_live_llm_confirmatory.py`、`tests/test_live_llm_confirmatory.py`、`workstreams/benchmark_v1/trajectories/live_llm_confirmatory/`、`workstreams/benchmark_v1/reports/live-llm-confirmatory.json`。
  - 依赖：prior disclosure、method protocol、P0 security。
  - [ ] 只通过官方 operation-level adapter 调用，不使用 Task Lab 代替正式 runner。
  - [ ] 运行冻结模型角色、paired seeds 和 core tasks。
  - [ ] 保留 API 失败、重试、非法输出、token、费用、墙钟和模型版本。
  - [ ] 不保存私有思维链；只保存结构化假设、证据引用、行动理由和置信度。
  - [ ] masked/assigned 条件必须保持非谱图证据一致。
  - 验收：轨迹 replay、provider usage 和费用 reconciliation 全部通过。

- [ ] **`benchmark-vnext-llm-causal-ablation` — LLM 证据使用因果实验**
  - 隔离约束：不得与 live confirmatory 任务共用输出路径。
  - 默认 owned_paths：`configs/benchmark/llm_causal_ablation_vnext.json`、`scripts/run_llm_causal_ablation.py`、`tests/test_llm_causal_ablation.py`、`workstreams/benchmark_v1/reports/llm-causal-ablation.json`。
  - 依赖：live-LLM confirmatory、prior disclosure。
  - [ ] 在相同公共状态比较谱图可见/遮蔽/峰置换。
  - [ ] 比较记忆保留/删除和语义一致/冲突。
  - [ ] 测量行动变化、后续结果、change-detection delay 和锚定恢复。
  - [ ] `adaptation_source` 和自然语言解释只能作诊断，不能作为因果使用证据。
  - 验收：预注册配对统计支持或反驳 H2；不做型号数量竞赛。

- [ ] **`benchmark-vnext-method-matrix-integration` — 跨方法公平性集成**
  - 默认 owned_paths：`configs/benchmark/method_matrix_vnext.json`、`scripts/run_method_matrix_vnext.py`、`tests/test_method_matrix_vnext.py`、`workstreams/benchmark_v1/reports/method-matrix-vnext.json`。
  - 依赖：classic、procedure RL、flow control、context model、live LLM 各自产出。
  - [ ] 检查任务合同、seeds、实验预算、公共 observation 和资源账本一致。
  - [ ] campaign、procedure、process-control 分轨报告。
  - [ ] 只在相同交互层级内做算法归因。
  - [ ] 失败方法和缺失单元显式进入矩阵。
  - 验收：任何合同 hash 不一致均拒绝汇总。

## 6. P2：机制适应主实验与统计

- [ ] **`benchmark-vnext-h1-fixed-vs-shift` — H1 固定世界与机制变化**
  - 默认 owned_paths：`configs/benchmark/h1_fixed_vs_shift_vnext.json`、`scripts/run_h1_fixed_vs_shift.py`、`tests/test_h1_fixed_vs_shift.py`、`workstreams/benchmark_v1/reports/h1-fixed-vs-shift.json`。
  - 依赖：method matrix integration。
  - [ ] 比较 IID、参数 shift、机制 shift 下的 primary/risk/cost 排名。
  - [ ] 报告 rank correlation、rank inversion 和安全性变化。
  - [ ] 不预设必须发生排名反转。
  - 验收：paired bootstrap、Holm 和 SESOI 同时报告。

- [ ] **`benchmark-vnext-h2-prior-anchoring` — H2 先验与实验智能**
  - 默认 owned_paths：`configs/benchmark/h2_prior_anchoring_vnext.json`、`scripts/run_h2_prior_anchoring.py`、`tests/test_h2_prior_anchoring.py`、`workstreams/benchmark_v1/reports/h2-prior-anchoring.json`。
  - 依赖：LLM causal ablation，可加入非 LLM 对照。
  - [ ] 比较 Opaque/Descriptor/Named-Retrieval。
  - [ ] 比较 congruent、label-permuted 和 semantic-conflict worlds。
  - [ ] 报告初始样本效率、证据更新、锚定恢复和行动质量。
  - 验收：将化学知识收益与证据驱动适应分开。

- [ ] **`benchmark-vnext-h3-adaptation` — H3 显式世界模型适应**
  - 默认 owned_paths：`configs/benchmark/h3_adaptation_vnext.json`、`scripts/run_h3_adaptation.py`、`tests/test_h3_adaptation.py`、`workstreams/benchmark_v1/reports/h3-adaptation.json`。
  - 依赖：context model、procedure/control baselines。
  - [ ] 比较显式适应、无记忆、model-free 和经典局部模型。
  - [ ] 报告 change-detection delay、adaptation regret、恢复实验数、风险和成本。
  - [ ] 报告任务和机制族异质性。
  - 验收：结论必须来自冻结 endpoint，不使用解释文本代替行为结果。

- [ ] **`benchmark-vnext-statistics-figures` — 冻结统计与图形**
  - 默认 owned_paths：`scripts/build_vnext_figures.py`、`tests/test_vnext_figures.py`、`paper/figure_specs_vnext.json`、`paper/figures_vnext/`、`paper/source_data_vnext/`。
  - 依赖：H1–H3 冻结摘要。
  - [ ] paired bootstrap、Holm、SESOI、rank stability 和预算曲线齐全。
  - [ ] 图只读取签名摘要，不读取临时轨迹或手工数值。
  - [ ] 每张图有 source data、生成命令和 digest。
  - [ ] 负结果和未通过门禁以同等可见度展示。
  - 验收：从干净环境可确定性重建全部图。

## 7. P3：Train / Bench / Bridge

- [ ] **`chemworld-train-generator` — Train 世界生成器**
  - 默认 owned_paths：`src/chemworld/train/__init__.py`、`src/chemworld/train/generator.py`、`tests/test_train_generator.py`、`configs/benchmark/train_generator_vnext.json`、`workstreams/benchmark_v1/reports/train-generator-controls.json`。
  - 依赖：mechanism adaptation protocol 冻结 world-family schema；冻结前只能实现生成器接口和隔离测试。
  - [ ] 程序化生成机制族、难度课程和向量化 reset/step。
  - [ ] Train/Dev 不包含冻结 Bench worlds。
  - [ ] 生成分布、seed 空间和 curriculum 可审计。
  - 验收：训练吞吐、确定性和隔离测试通过。

- [ ] **`benchmark-vnext-dataset-bridge` — DatasetOracle Bridge**
  - 默认 owned_paths：`src/chemworld/bridge/__init__.py`、`src/chemworld/bridge/dataset_oracle.py`、`tests/test_dataset_oracle_bridge.py`、`configs/benchmark/dataset_bridge_vnext.json`、`workstreams/benchmark_v1/reports/dataset-bridge-controls.json`。
  - 依赖：scientific positioning 和稳定公共 action/observation/trajectory 合同。
  - [ ] 选择一个授权清晰、任务同构的 partition 或 flow 数据集。
  - [ ] 实现 Train/Calibration/Test 隔离、缺失值 fail-closed 和不确定性。
  - [ ] 禁止 agent 查询 held-out 真值。
  - [ ] 比较 virtual-pretrained 与同架构 scratch 的少样本适应。
  - 验收：报告 transfer advantage、实验节省和失败模式，不要求数值完美相关。

- [ ] **`benchmark-vnext-independent-backend` — 独立高保真后端**
  - 默认 owned_paths：`src/chemworld/bridge/independent_backend.py`、`tests/test_independent_backend.py`、`configs/benchmark/independent_backend_vnext.json`、`workstreams/benchmark_v1/reports/independent-backend-controls.json`。
  - 依赖：Dataset Bridge 至少完成 `chemworld.bridge` 包边界；不得修改其 `__init__.py`。
  - [ ] 为 partition 或 flow 实现训练期不可见、代码和参数来源独立的 backend。
  - [ ] 保持公共 action/observation/trajectory 合同。
  - [ ] 不针对某个方法调后端。
  - [ ] 报告跨后端排名、适应收益和 core-specific failure。
  - 验收：形成 V3 行为有效性证据或明确失败。

- [ ] **`benchmark-vnext-h4-transfer` — H4 虚拟预训练迁移**
  - 默认 owned_paths：`configs/benchmark/h4_transfer_vnext.json`、`scripts/run_h4_transfer.py`、`tests/test_h4_transfer.py`、`workstreams/benchmark_v1/reports/h4-transfer.json`。
  - 依赖：Train generator、Dataset Bridge 或 independent backend。
  - [ ] 冻结相同架构、相同现实/外部数据预算和 checkpoint 选择规则。
  - [ ] 比较 virtual-pretrained、scratch、BO/Safe-BO 和固定 DOE。
  - [ ] 报告 k-shot transfer curve、adaptation regret、实验节省、安全和不确定性。
  - 验收：无显著迁移收益时明确反驳 H4，不更换主终点。

- [ ] **`benchmark-vnext-physical-partition-bridge` — 实体 partition 工程闭环**
  - 默认 owned_paths：`src/chemworld/bridge/physical_partition.py`、`tests/test_physical_partition_bridge.py`、`configs/benchmark/physical_partition_bridge_vnext.json`、`workstreams/benchmark_v1/reports/physical-partition-bridge.json`。
  - 依赖：H4 在 Dataset/independent backend 上完成；不阻塞 Core release。
  - [ ] LLM/Agent 只输出结构化意图。
  - [ ] schema validation、硬安全约束、人工批准和确定性执行层独立。
  - [ ] 冻结真实实验预算、失败记录和人工干预账本。
  - 验收：只主张适应成本和实验节省，不把 Core 风险分数解释为现实安全。

- [ ] **`benchmark-vnext-physical-flow-bridge` — 实体 flow 旗舰桥接**
  - 默认 owned_paths：`src/chemworld/bridge/physical_flow.py`、`tests/test_physical_flow_bridge.py`、`configs/benchmark/physical_flow_bridge_vnext.json`、`workstreams/benchmark_v1/reports/physical-flow-bridge.json`。
  - 依赖：partition 工程链和独立 flow backend。
  - [ ] 先 shadow mode，再 supervised closed loop，再评估窄域 autonomous loop。
  - [ ] 设备 adapter 与 LLM 决策隔离。
  - [ ] MPC、SAC、BO 和 virtual-pretrained 使用相同真实预算。
  - 验收：外部实验室可独立重复；否则只作工程示范。

## 8. P4：独立复现、发布与论文

- [ ] **`benchmark-vnext-independent-reproduction` — 第三方干净复现**
  - 默认 owned_paths：`configs/benchmark/independent_reproduction_vnext.json`、`scripts/run_independent_reproduction.py`、`tests/test_independent_reproduction.py`、`workstreams/benchmark_v1/reports/independent-reproduction.json`。
  - 依赖：目标方法、冻结摘要和 release candidate 全部完成；不得以开发工作区代替安装包。
  - 独立性约束：认领者不应是目标实现和正式运行的主要作者。
  - [ ] 从 clean wheel 和公开命令重建指定 seeds。
  - [ ] 对比协议 hash、trajectory digest、摘要和数值容差。
  - [ ] 不访问开发者缓存、API key、私有路径或未发布数据。
  - 验收：复现报告和全部失败公开保留。

- [ ] **`benchmark-vnext-private-evaluation` — 私有 Bench 评测**
  - 默认 owned_paths：`configs/benchmark/private_evaluation_vnext.json`、`scripts/run_private_evaluation.py`、`tests/test_private_evaluation.py`、`workstreams/benchmark_v1/reports/private-evaluation-summary.json`；私有实例置于仓库外。
  - [ ] 私有 worlds/salts 与实现者隔离。
  - [ ] 使用同一公开合同和冻结 evaluator。
  - [ ] 检查提交包的资源、依赖、超时和泄漏。
  - 验收：私评摘要可公开，私有实例不泄露。

- [ ] **`benchmark-vnext-release` — 发布候选**
  - 默认 owned_paths：`configs/benchmark/release_vnext.json`、`scripts/run_release_vnext.py`、`tests/test_release_vnext.py`、`workstreams/benchmark_v1/reports/release-vnext.json`；需要更新公开文档时在 claim 中逐项追加。
  - 集成约束：只在上游证据冻结且没有重叠 active claim 时认领。
  - [ ] wheel、公开合同、seed suite、报告、golden trajectory 和验证命令齐全。
  - [ ] 本地完整门禁通过，不依赖 CI/GitHub Actions。
  - [ ] 用户文档只包含发布级内容和真实限制。
  - [ ] 打不可变 tag，记录 source/evidence digests。
  - 验收：clean install、replay、docs strict build 和 release gate 全通过。

- [ ] **`paper-chemworld-final` — 论文与 PDF**
  - 默认 owned_paths：`paper/main.tex`、`paper/main.pdf`、`paper/references.bib`、`paper/claims.json`、`paper/manuscript-audit.json`、`paper/README.md`；冻结 figures/source data 只读引用。
  - 依赖：不得在 H1–H3 和复现冻结前认领。
  - [ ] 标题跟随结果，不预设 Nature 叙事。
  - [ ] 主文只写主张矩阵允许的结论。
  - [ ] Methods、Extended Data、source data、代码/数据可用性和 limitations 完整。
  - [ ] H4 未完成时只写 V0–V3 范围；实体 bridge 不得用模拟结果替代。
  - [ ] LaTeX 无错误渲染 PDF，图表从冻结 source data 生成。
  - 验收：论文、PDF、release tag 和证据 commit 一致。

## 9. 建议的并行批次

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

## 10. 已完成且不得重复认领

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

## 11. 本地总门禁

- [ ] `.\.venv\Scripts\python.exe scripts\manage_claims.py check`
- [ ] `.\.venv\Scripts\python.exe scripts\audit_publication_protocol.py`
- [ ] `.\.venv\Scripts\python.exe scripts\audit_publication_generalization_security.py`
- [ ] `.\.venv\Scripts\python.exe scripts\run_release_gate.py`
- [ ] `.\.venv\Scripts\python.exe -m pytest`
- [ ] `.\.venv\Scripts\python.exe -m ruff check .`
- [ ] `.\.venv\Scripts\python.exe -m mypy src`
- [ ] `.\.venv\Scripts\python.exe -m mkdocs build --strict`
