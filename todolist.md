# ChemWorld 基座强化专项 Todo

最后更新：2026-07-13

## 专项范围

- 当前阶段只处理 backend、公共合同、状态转移、物理化学 provider、仪器观测、漏洞和成熟度证据。
- 暂停新增算法榜单、LLM 正式矩阵、H1–H4 主实验、Train/Bridge、实体设备、论文和最终发布。
- 现有 `benchmark-vnext-reference-portfolio-substrate` active claim 可继续完成，但不阻塞本专项。
- 所有实现继续遵守 `claims/README.md`：先 claim、单一 Task ID、精确 `owned_paths`、独立提交并推送 `main`。
- 一个任务超过约两天时，用 `原-task-id--slice-序号-名称` 拆分；共享文件最后由 integration slice 顺序合并。
- 旧冻结协议只作为历史 provenance，不是兼容性硬约束。若旧 action、reward、task、score、physics 或 replay 合同妨碍更好的基座，可直接建立新版本并重跑。
- 重建时不修改或伪装旧结果；保留旧 artifact 的版本/commit 标识，新报告明确写出 supersedes 关系即可。

## 当前诊断

- 三个共享正式运行时模块 `reaction_kinetics`、`reactors`、`spectroscopy_instruments` 已完成有界 `reference_validated` 升级并接入正式 runtime；完整工业反应器平台仍不在当前主张范围内。
- 当前 15 个注册任务的必需路径均至少为 `reference_validated`，`proxy_allowed=false`，runtime reachability 中 `lite_upgrade_targets={}`。
- LLE/wash、冷却结晶、连续流和蒸馏正式 provider 已完成动态耦合；干燥、浓缩、转移、电化学和平衡已有窄域参考实现。
- backend v0.5 candidate 已冻结；旧经典、Safe-GP、SAC 与 LLM 结果均绑定升级前后端，只能作为历史诊断，不能用于 v0.5 排名。
- 成熟度不能靠修改标签升级。每个升级都必须有适用域、模型卡、解析或独立参考、容差、失败域、运行时 provenance 和回放证据。
- RL 条件混合动作、奖励泄漏、flow quick-close 和核心 `run_flow` 漏洞已修复；冻结 backend 上 5 seeds × 20 Dev episodes 门禁已通过，但仍不构成 Bench 排名。

## 统一完成要求

- 协议声明 schema/version、单位、适用域、seed、容差、异常值、失败语义和主张边界。
- 测试至少覆盖参考点、趋势、守恒、边界、非法输入、确定性、回放和一个反作弊案例。
- provider 必须返回诊断与 ledger；求解失败、超出适用域、NaN/Inf 和不收敛必须 fail closed。
- 不允许隐藏 fallback、静默 clip、元数据影子状态、重复计费或由 observation 反向修改真实状态。
- 控制报告至少包含 `source_commit`、dirty-tree、protocol hash、检查项、限制、剩余门禁和 `benchmark_claim_allowed=false`。
- 只有最终成熟度集成任务可以修改 `src/chemworld/tasks.py` 的正式等级和 model IDs。
- 共享运行时或成熟度变更必须运行完整 pytest、ruff、mypy、strict docs、release gate 和 clean-wheel smoke test。

## P0：先修 Bug、漏洞和合同错误

- [x] **`foundation-runtime-reachability-audit` — 正式运行时可达性与残留路径审计**
  - 默认 owned_paths：`configs/foundation/runtime_reachability_vnext.json`、`scripts/audit_runtime_reachability_vnext.py`、`tests/test_runtime_reachability_vnext.py`、`workstreams/world_foundation/reports/runtime-reachability-vnext.json`。
  - 依赖：无，可立即认领。
  - [x] 枚举 15 tasks × allowed operations × service × kernel × provider × model ID × maturity。
  - [x] 检查声明的高等级 provider 是否真的改变状态、诊断、ledger 和 replay provenance。
  - [x] 检查旧 `lite`、legacy、proxy、fallback、重复 dispatcher 和不可达专业模块。
  - [x] 检查 operation registry、domain service registry、task maturity 和实际 runtime reachability 一致。
  - [x] 对每个不一致生成精确 fix slice，不在审计任务中顺手改共享运行时。
  - 结果：15 tasks、28 operations、20 providers 对齐；无 orphan/reference 误路由或禁用 runtime model；六个 `lite` providers 精确归入三个共享升级模块。动态耦合的剩余证据由 P2 任务完成。
  - 验收：15 个任务全部有机器可读 reachability 图；任何未声明路径、孤儿 provider 或隐式 fallback 都令报告失败。

- [x] **`foundation-state-transition-invariants` — 28 类操作状态语义与事务漏洞审计**
  - 默认 owned_paths：`configs/foundation/state_transition_invariants_vnext.json`、`scripts/audit_state_transition_invariants.py`、`tests/test_state_transition_invariants.py`、`workstreams/world_foundation/reports/state-transition-invariants.json`。
  - 依赖：runtime reachability audit 的 operation 清单。
  - [x] 为每个 operation 声明 additive、replace、configure、observe 或 terminal 语义。
  - [x] 验证加热、等待、流动、电解、加料、加溶剂、萃取、洗涤、分相、转移和测量不会错误叠加或重置。
  - [x] 验证失败操作原子回滚；失败显式消耗一次 attempt 且只允许固定 process cost/risk 惩罚，不提交物料、相态、设备、热、时间、样品或 observation 历史。
  - [x] 验证重复测量、终止后操作、重复 final assay、零量/负量和预算边界 fail closed。
  - [x] 验证真实状态只存在于 typed state，不由 metadata、缓存 observation 或 UI 状态覆盖。
  - [x] 对发现的缺陷建立独立 `foundation-state-fix--zero-effect-actions` slice。
  - 结果：28/28 正向、重复、同 seed 回放、失败原子性、守恒和 typed-state 控制通过；负量全部拒绝，15 个零效果字段已由 `foundation-state-fix--zero-effect-actions` 统一收口并与条件 action schema 对齐。
  - 验收：28/28 operation 均有状态差分、守恒、事务和重复调用证据。

- [x] **`foundation-rl-contract-remediation` — 49 维动作与 quick-close 漏洞修复**
  - 默认 owned_paths：`src/chemworld/rl/hybrid_actions.py`、`src/chemworld/rl/rewards.py`、`src/chemworld/rl/environment.py`、`src/chemworld/rl/training.py`、`src/chemworld/rl/evaluation.py`、`src/chemworld/wrappers.py`、`tests/test_rl_foundation_contract.py`、`configs/foundation/rl_contract_vnext.json`、`workstreams/world_foundation/reports/rl-contract-vnext.json`。
  - 依赖：可拆为 action、reward、integration 三个互斥 slice；integration 最后执行。
  - [x] 用 categorical operation + conditional parameters 替代正式 49 维全局连续合同；SB3 的 49 维 `Box` 仅保留为明确标注的兼容 latent，不再冒充语义 action space。
  - [x] 无关参数不执行、不进入损失、不改变 digest；affordance mask 在训练、评估和回放中一致。
    - [x] 无关参数不执行、不进入 trajectory digest，训练与冻结回放使用同一 public affordance mask。
    - [x] PPO 使用原生 masked categorical operation + conditional Gaussian parameter distribution；未选字段不计入 log-prob 或 entropy，policy distribution hash 写入 checkpoint 并在加载前验证。
  - [x] 删除可支配策略的完成实验 `+1` 与 measurement bonus，隔离 training shaping 与冻结 endpoint，并禁止 final-assay 后自动重置产生的 affordance 奖励。
  - [x] quick-close、只加料、只测量和未执行核心物理操作不得获得行为完成；campaign 每次实验结束后独立重置行为账本。
  - [x] 旧 checkpoint 和旧 action/reward hash 标记为 incompatible diagnostic；v0.2 manifest 与周期 checkpoint sidecar 在加载模型前做精确 hash 校验。
  - [x] 使用 5 个训练 seeds × 20 Dev episodes 验证 flow 实验实际包含 `set_flow_rate`、`run_flow` 和 final assay。
    - 冻结 v0.5 backend 上预注册 seed 106 的 25,600 checkpoint 未通过，51,200 首次通过，102,400 也通过；严格选择最早通过的 51,200。
    - 原配置扩展 seeds 107–110 后 5/5 seeds 全部通过：episode completion=1.0、behavior-complete experiment rate=1.0、quick-close=0、invalid action=0、runtime/observation domain failure=0。
  - [x] 修复审计遗漏：首次 `terminate` 后不再继续暴露 `terminate` affordance；重复终止原子回滚且记录 precondition failure，不再允许零效果 committed 循环。
  - 控制报告：`workstreams/world_foundation/reports/rl-contract-vnext.json`；native hybrid distribution、冻结 backend 绑定、CUDA/CPU 基础设施选择与五种子学习门禁均已闭环。该结果仅为 Dev gate，`benchmark_claim_allowed=false`。
  - 验收：策略不再收敛为“加料—终止—测量”；所有通过的 flow 实验执行核心操作，完整 RL 与回放测试通过。

- [x] **`foundation-public-boundary-security` — 公共边界、泄漏与回放安全收口**
  - 默认 owned_paths：`configs/foundation/public_boundary_security_vnext.json`、`scripts/audit_public_boundary_security_vnext.py`、`tests/test_public_boundary_security_vnext.py`、`workstreams/world_foundation/reports/public-boundary-security-vnext.json`。
  - 依赖：runtime reachability 和 state invariants。
  - [x] 将五类 semantic invariance 和现有 exploit probes 绑定正式 public harness。
  - [x] 扫描 hidden state、private seed、debug、异常、路径、task text、provider 参数和 model identity 泄漏。
  - [x] 覆盖 NaN/Inf、超大 payload、未知字段、非法枚举、重复 assay、预算竞争、轨迹截断和 digest 篡改。
  - [x] 验证 observation/schema/JSON 顺序和材料代号变化不改变物理与评分。
  - [x] Windows、clean wheel 和独立进程均 fail closed。
  - 验收：任何泄漏、越权观察或 replay 差异都阻止 backend freeze。

- [x] **`foundation-maturity-truth-gate` — 成熟度、防伪标签和证据门禁**
  - 默认 owned_paths：`configs/foundation/maturity_truth_vnext.json`、`scripts/audit_maturity_truth_vnext.py`、`tests/test_maturity_truth_vnext.py`、`workstreams/world_foundation/reports/maturity-truth-vnext.json`。
  - 依赖：runtime reachability。
  - [x] 验证任务成熟度严格取实际必需模块的最低等级。
  - [x] `reference_validated` 必须绑定解析/文献/独立实现、适用域和数值容差。
  - [x] `professional_candidate` 必须额外具备诊断、守恒、provenance、失败域和跨参考案例。
  - [x] model card、adapter manifest、task card、runtime provenance 和公开文档必须同源。
  - [x] 禁止仅因存在高级模块就提升未使用它的任务。
  - 验收：篡改等级、model ID、证据路径或 runtime route 时测试失败。

## P1：升级三个共享 `lite` 模块

- [ ] **`foundation-reaction-kinetics-reference` — 反应网络与速率律升级**
  - 默认 owned_paths：`src/chemworld/physchem/reaction_network.py`、`src/chemworld/physchem/reaction_network_specs.py`、`src/chemworld/physchem/reaction_rate_contracts.py`、`src/chemworld/physchem/reaction_rate_laws.py`、`src/chemworld/physchem/reaction_reference_cases.py`、`src/chemworld/physchem/reaction_sensitivity.py`、`src/chemworld/physchem/reaction_network_cards.py`、`src/chemworld/physchem/reaction_adapter_manifest.py`、`tests/test_reaction_kinetics_reference.py`、`workstreams/world_foundation/reports/reaction-kinetics-reference.json`。
  - 依赖：runtime reachability；允许用新版本替代旧反应合同并重建受影响证据。
  - [ ] 统一浓度、活度、速率常数、反应级数和 Arrhenius 单位合同。
  - [ ] 支持并验证可逆、平行/竞争、连续反应、产物抑制和催化剂失活的有界机制族。
  - [ ] 从 stoichiometric matrix 自动检查元素/物料守恒和不可生成物种。
  - [ ] 处理 stiff/non-stiff、非负性、事件终止、Jacobian/容差和不收敛诊断。
  - [ ] 与闭式解、独立 SciPy 求解和可选专业参考后端在声明域内比较。
  - [ ] 证明机制变化会改变合理温度、时间、催化剂或测量策略，而非只改变第三位小数。
  - 验收：满足 `reference_validated` 的证据门禁；若任一必要条件缺失，保持 `lite` 并记录原因。

- [x] **`foundation-reactor-reference` — Batch/Semibatch/CSTR 反应器升级**
  - 默认 owned_paths：`src/chemworld/physchem/reactor_shared.py`、`src/chemworld/physchem/reactor_solvers.py`、`src/chemworld/physchem/batch_reactors.py`、`src/chemworld/physchem/semibatch_reactors.py`、`src/chemworld/physchem/cstr_reactors.py`、`src/chemworld/physchem/reactors.py`、`src/chemworld/physchem/reactor_cards.py`、`tests/test_reactor_reference.py`、`workstreams/world_foundation/reports/reactor-reference.json`。
  - 依赖：reaction kinetics 的稳定公共接口；接口冻结前只做独立 solver/reference slice。
  - [x] 统一 batch、semibatch、CSTR 的质量、体积、能量和时间状态。
  - [x] 加入或验证投料速率、热交换、热容、反应热、环境损失、体积变化和声明域内的压力边界。
  - [x] 区分 configure、heat、wait 和 reaction advance，避免重复积分或重新实验。
  - [x] 验证绝热、恒温、一阶 batch、稳态 CSTR 和能量闭合参考案例。
  - [x] 对 runaway、无稳态、负浓度、积分失败和超适用域提供明确诊断。
  - [x] 证明温度—时间—选择性—风险存在非退化权衡，不形成机械升温偏置。
  - 验收：声明域内达到 `reference_validated`；所有热/质 ledger 与 World state 一致。

- [x] **`foundation-instruments-reference` — 合成仪器与谱图观测升级**
  - 默认 owned_paths：`src/chemworld/physchem/spectroscopy.py`、`src/chemworld/physchem/spectroscopy_identifiability.py`、`src/chemworld/physchem/spectroscopy_cards.py`、`src/chemworld/physchem/spectroscopy_adapter_manifest.py`、`src/chemworld/physchem/chromatography_methods.py`、`src/chemworld/physchem/chromatography_method_cards.py`、`src/chemworld/world/instruments.py`、`src/chemworld/world/spectra.py`、`src/chemworld/world/observation_kernel.py`、`tests/test_instruments_reference.py`、`workstreams/world_foundation/reports/instruments-reference.json`。
  - 依赖：runtime reachability 和 public-boundary schema。
  - [x] 每种公开 instrument 明确输入状态、输出单位、校准、LOD/LOQ、饱和、噪声、漂移和缺失值。
  - [x] UV/Vis 对 Beer–Lambert、HPLC/GC 对 retention/plate-count、pH 对 charge balance 建立参考案例。
  - [x] raw signal、processed estimate、uncertainty、peaks 和 assignments 分层，不泄露真实组分或 hidden state。
  - [x] 相同状态/seed 可复现；不同浓度、组成和仪器设置产生可辨识但非直接答案的变化。
  - [x] 历史谱图按需读取，测量成本/失败计入 ledger，遮蔽只移除谱图证据。
  - [x] 明确“不预测真实样品谱图”的适用边界。
  - 验收：有界 synthetic-observation contract 达到 `reference_validated`，并通过 identifiability 与泄漏门禁。

## P2：复核高等级 provider 的正式耦合

- [x] **`foundation-separation-chain-coupling` — LLE、wash、dry、concentrate、transfer**
  - 默认 owned_paths：`src/chemworld/world/phase_kernel.py`、`src/chemworld/world/separation_kernel.py`、`src/chemworld/physchem/extraction_units.py`、`src/chemworld/physchem/phase_equilibrium_adapter_manifest.py`、`src/chemworld/physchem/separations.py`、`src/chemworld/physchem/drying_units.py`、`src/chemworld/physchem/drying_adapter_manifest.py`、`src/chemworld/physchem/concentration_units.py`、`src/chemworld/physchem/concentration_adapter_manifest.py`、`src/chemworld/physchem/transfer_units.py`、`src/chemworld/physchem/transfer_adapter_manifest.py`、`tests/test_separation_chain_coupling.py`、`workstreams/world_foundation/reports/separation-chain-coupling.json`。
  - 依赖：state invariants、instrument contract。
  - [x] 验证 extractant identity、phase ratio、温度/组成、混合、静置、夹带和重复萃取真实影响分配。
  - [x] 验证 wash 回收率/纯度权衡、干燥剂容量、真空浓缩能耗/挥发损失和 transfer holdup。
  - [x] 每一步保持组分、相体积、溶剂、能量、成本和风险 ledger 闭合。
  - [x] 不允许旧 generic proxy、别名或 metadata 路径绕过专业 provider。
  - 验收：partition 与 purification 相关任务通过端到端参考轨迹和扰动敏感性测试。

- [x] **`foundation-crystallization-coupling` — 结晶与固液分离**
  - 默认 owned_paths：`src/chemworld/world/crystallization.py`、`src/chemworld/physchem/crystallization_units.py`、`src/chemworld/physchem/crystallization_validation.py`、`src/chemworld/physchem/crystallization_cards.py`、`src/chemworld/physchem/crystallization_adapter_manifest.py`、`tests/test_crystallization_coupling.py`、`workstreams/world_foundation/reports/crystallization-coupling.json`。
  - 依赖：reaction/reactor 和 instrument contracts。
  - [x] 验证溶解度、过饱和、成核/生长、晶种、冷却轨迹、杂质包埋、CSD 和过滤收率耦合。
  - [x] 处理无成核、过快冷却、晶种无效、耗尽和 solver 不收敛。
  - [x] 质量、晶体数/尺寸矩和液相组成闭合。
  - 验收：专业候选 provider 在正式 runtime 可达，决策扰动改变产率—纯度—时间权衡。

- [x] **`foundation-distillation-coupling` — 蒸馏、回流和切割**
  - 默认 owned_paths：`src/chemworld/world/distillation.py`、`src/chemworld/physchem/distillation_units.py`、`src/chemworld/physchem/distillation_adapter_manifest.py`、`tests/test_distillation_coupling.py`、`workstreams/world_foundation/reports/distillation-coupling.json`。
  - 依赖：state invariants 和 property/energy contracts。
  - [x] 验证 VLE、bubble gate、相对挥发度、回流、设备/热负荷、釜残和 fraction collection。
  - [x] 验证能量不足、未沸腾、错误切割、过量收集和重复收集 fail closed。
  - [x] 每个 fraction 与釜残满足组分、总量和能量 ledger。
  - 验收：正式任务只走 duty-limited provider，并形成可解释纯度—回收—能耗前沿。

- [x] **`foundation-flow-coupling` — 几何 PFR、传热、压降与控制状态**
  - 默认 owned_paths：`src/chemworld/world/continuous_flow.py`、`src/chemworld/physchem/pfr_reactors.py`、`src/chemworld/physchem/heat_transfer_units.py`、`src/chemworld/physchem/transport.py`、`tests/test_flow_coupling.py`、`workstreams/world_foundation/reports/flow-coupling.json`。
  - 依赖：reaction kinetics、RL contract 和 state invariants。
  - [x] 验证 flow rate、residence time、geometry、temperature boundary、heat transfer、pressure drop 和 conversion 一致。
  - [x] 明确 `set_flow_rate` 是配置、`run_flow` 是新实验推进；重复运行累计资源但不重复加料状态。
  - [x] 处理零流量、压降超限、热边界失败、solver 不收敛和设备容量。
  - [x] 报告轴向诊断、能量/压降 ledger 和核心操作覆盖。
  - 验收：专业候选 PFR 是唯一正式路径，flow 不再允许未运行反应器的伪完成。

- [x] **`foundation-electrochem-equilibrium-coupling` — 电化学与水相平衡**
  - 默认 owned_paths：`src/chemworld/world/electrochemistry.py`、`src/chemworld/physchem/electrochemistry.py`、`src/chemworld/physchem/electrochem_transport.py`、`src/chemworld/physchem/electrochem_double_layer.py`、`src/chemworld/physchem/equilibrium_chemistry.py`、`src/chemworld/physchem/equilibrium.py`、`tests/test_electrochem_equilibrium_coupling.py`、`workstreams/world_foundation/reports/electrochem-equilibrium-coupling.json`。
  - 依赖：reaction/reactor 和 instrument contracts。
  - [x] 电化学验证 Nernst、Butler–Volmer、传质限制、双电层、Faradaic charge 和 electrical work。
  - [x] 平衡验证弱酸碱 charge/mass balance、pH、Ksp hooks、温度/离子强度适用域和不收敛。
  - [x] 明确 set potential/configure 与 electrolyze/advance 的状态区别。
  - [x] 检查 equilibrium task 的 reaction 路径并绑定升级后模块。
  - 验收：两任务不再被无关或旧 `lite` 路径拉低，且端点、风险和测量信号非退化。

## P3：成熟度集成与基座冻结

- [ ] **`foundation-lite-elimination-integration` — 全 15 任务成熟度重算**
  - 默认 owned_paths：`src/chemworld/tasks.py`、`src/chemworld/physchem/maturity.py`、`docs/model_maturity.md`、`docs/tasks.md`、`docs/task_cards.md`、`tests/test_task_maturity_integration.py`、`workstreams/world_foundation/reports/task-maturity-vnext.json`。
  - 依赖：P0 全部通过，三个共享模块和相关耦合报告完成。
  - [ ] 只根据实际 runtime reachability 和已通过证据更新 module level/model IDs。
  - [ ] 逐任务重算最低等级、proxy_allowed、适用域和限制。
  - [ ] 目标是 15 个任务不再因共享旧 `lite` 模块降级；未达标项必须保留 `lite` 并给出精确缺口，不得强行清零。
  - [ ] 生成 before/after manifest 和任务—模块—证据矩阵。
  - [ ] 确认 `proxy_allowed_task_ids=[]` 且不存在旧正式 fallback。
  - 验收：代码、模型卡、任务卡、文档、轨迹 provenance 和机器报告完全一致。

- [ ] **`foundation-backend-v05-freeze` — 基座候选冻结与全量回归**
  - 默认 owned_paths：`configs/foundation/backend_v0.5.json`、`scripts/audit_backend_v05.py`、`tests/test_backend_v05_freeze.py`、`workstreams/world_foundation/reports/backend-v0.5.json`、`docs/backends.md`、`docs/world_law.md`、`docs/limitations.md`。
  - 依赖：lite elimination integration、所有缺陷 fix slices。
  - [ ] 运行 15 tasks 的合法最小轨迹、扰动轨迹、失败轨迹和 replay。
  - [ ] 运行守恒、单位、确定性、provider provenance、漏洞、资源账本和 semantic invariance 总门禁。
  - [ ] 运行完整 pytest、ruff、mypy、strict MkDocs、release gate 和 clean-wheel smoke test。
  - [ ] 冻结 backend contract/hash，但不运行正式算法排名，不写论文结论。
  - 验收：生成 `candidate_backend_only` v0.5 报告；任何失败都保留并阻止冻结。

## 建议执行顺序

- [ ] 第一批并行：runtime reachability、state invariants、RL contract 三个 slice、public boundary、maturity truth。
- [ ] 第二批并行：reaction kinetics、reactor、instruments；只有稳定接口才能进入 domain coupling。
- [ ] 第三批并行：separation、crystallization、distillation、flow、electrochem/equilibrium。
- [ ] 第四批顺序执行：lite elimination integration → backend v0.5 freeze。

## 已完成且继续保留

- [x] 15 个零时长、零洗液、零转移、零晶种和零电流 no-op 入口已 fail closed；正的最小有效量由 operation-specific schema 与 validator 共用。
- [x] Agent 公共字段 schema 已修复可选 operation 键与 choice 容器的类型漂移；全量 `mypy src` 恢复通过。
- [x] World Law v0.4、8 个正式 provider 与 domain service registry。
- [x] 旧正式 proxy/fallback 路由清理，当前 15 tasks 均 `proxy_allowed=false`。
- [x] LLE/wash、结晶、连续流、蒸馏专业候选实现。
- [x] 干燥、真空浓缩、转移和电化学窄域参考实现。
- [x] 机理/构成律 family、world-family axes、守恒和 replay provenance 控制。
- [x] 历史谱图按需访问、学生端状态动画和核心 operation semantics 修复。
- [x] 基础 public harness、exploit、semantic invariance 和 release integrity 控制。

## 本地总门禁

- [ ] `.\.venv\Scripts\python.exe scripts\manage_claims.py check`
- [ ] `.\.venv\Scripts\python.exe -m pytest`
- [ ] `.\.venv\Scripts\python.exe -m ruff check .`
- [ ] `.\.venv\Scripts\python.exe -m mypy src`
- [ ] `.\.venv\Scripts\python.exe -m mkdocs build --strict`
- [ ] `.\.venv\Scripts\python.exe scripts\run_release_gate.py`
