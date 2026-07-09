# 物理化学核心设计

本页描述 ChemWorld `physchem` 层的当前稳定结构。更细的开发任务记录放在仓库根目录 `TODO.md` 中；站点文档只保留模块边界、当前能力、成熟度和限制。

## 设计目标

`physchem` 层不是外部专业软件的复制品，也不是松散的 proxy 集合。它的目标是提供一套可审计、可序列化、可测试的轻量物理化学核心，让 ChemWorld 的交互任务具备明确的物理合同。

核心原则：

- 所有模型必须声明单位、适用范围、失败边界和 maturity label。
- 计算结果尽量返回 report 或 ledger，而不是只返回一个裸数值。
- 数值内核、任务评分、观测生成和文档声明必须一致。
- 参考库只用于设计对照和验证思路，不直接复制实现。

## 当前范围

当前实现覆盖 foundation/lite 主线，并包含若干 `reference_validated` slice。它足以支撑虚拟实验 benchmark 的可解释交互，但不是完整商业流程模拟器、真实反应预测软件或数据驱动性质数据库。

已稳定接入的核心方向包括：

- 物性报告、蒸气压、热容、密度、摩尔体积和基础输运性质；
- 反应网络、Arrhenius / mass-action / 可逆动力学、第三体、Lindemann/Troe falloff 和有限差分敏感性；
- NASA7 物种热化学、反应焓、反应 Gibbs 自由能、平衡常数和可逆速率 detailed balance；
- batch reactor、反应热、简化传热和运行报告；
- LLE 诊断、分配、萃取、shortcut distillation、dry/concentrate 等分离切片；
- UV-vis、HPLC/GC、IR、NMR 等 benchmark-oriented 虚拟谱图；
- acid-base、Ksp、reaction equilibrium 和小规模 Gibbs minimization diagnostic；
- electrochemistry、flow、crystallization 等面向任务的轻量交互切片。

## 反应网络核心

反应网络层包含 `SpeciesSpec`、`ReactionSpec`、`RateLawSpec`、化学计量矩阵、元素守恒检查、ODE 积分入口和局部 analytical validation。

设计边界：

- mechanism 是任务可执行合同，不是隐藏在 runtime 里的硬编码分支；
- reaction kernel 不直接决定 task reward；
- 反应热、Gibbs 自由能、平衡和动力学通过 model card 与测试接入；
- 隐藏机理只通过观测和评分影响 agent，不应泄漏到 public observation。

当前 `reference_validated` 子切片包括：

- 不可逆/可逆一阶 batch ODE 与解析解对比；
- Arrhenius rate 与可选 Cantera backend 对照；
- NASA7 Gibbs 自由能驱动的 `K_eq(T)`、浓度标准态换算、`k_reverse = k_forward / K_c` detailed balance；
- 第三体 collision efficiency、Lindemann 低压/高压极限、Troe broadening 和 bath-gas-sensitive ODE；
- 反应网络有限差分敏感性报告。

仍未完成的专业化方向包括 chemically activated pressure dependence、表面覆盖、反应器能量方程与大型刚性网络求解策略。

## 热化学核心

热化学层提供 NASA7 物种 Cp/H/S/G、Cantera-style YAML thermo 解析、连续性诊断、反应热化学和 `K = exp(-Delta G/RT)`。

当前完成的关键能力：

- 物种标准态 Cp/H/S/G 计算；
- 反应 `Delta H`、`Delta S`、`Delta G` 和平衡常数；
- 由反应 Gibbs 自由能生成可逆 Arrhenius 的 detailed-balance reverse rate；
- 在反应网络 ODE 中验证平衡组成趋向。

边界：这不是完整 NASA9/Shomate/group-additivity 数据库，也没有自动热化学估算。缺少物种热化学时，相关计算应 fail fast。

## 物性核心

物性层提供蒸气压、热容、密度、摩尔体积、输运性质、EOS 相关报告和 curated component 数据。

设计重点：

- API 可序列化；
- provenance 可追踪；
- 单位明确；
- 超出适用域时返回 warning 或 failure；
- separation、reactor、instrument 共享同一报告风格。

边界：当前不是完整物性数据库；只覆盖 curated compounds、compact correlations 和 benchmark 所需的局部物性。

## 相平衡与分离

相平衡层覆盖 Raoult-style VLE、activity coefficient 入口、UNIQUAC slice、flash/VLE 报告和 LLE 诊断。

当前 LLE 切片已从单纯分配系数 proxy 推进到可审计诊断层：

- `lle_phase_stability_diagnostic()` 生成 TPD-style phase-stability report；
- 初始化策略显式记录为 `initialization_policy`；
- organic / aqueous trial composition 由 partition coefficient、phase volume 和 feed composition 生成；
- `liquid_liquid_split()` 在保持组分物料守恒的同时返回 `stability_diagnostic`；
- runtime `partition_split()` 复用同一诊断，并将 `lle_phase_status`、`lle_minimum_tpd_like` 和 `lle_partition_log_spread` 写入 phase metadata。

边界：这不是严格 LLE flash、tie-line tracing 或全局 Gibbs minimization。它适合 extraction / partition-discovery benchmark，让 agent 看到稳定、可解释、可回放的相分配规律。

## 平衡化学核心

平衡化学层提供小规模 reaction equilibrium、acid-base、precipitation 和 fixed-TP ideal Gibbs minimization slice。它适合隐藏 equilibrium scenario 和 analytical checks，不是数据库驱动的 aqueous speciation solver。

当前 Gibbs minimization diagnostic 包括：

- element residual、charge residual 和 bound violation；
- constraint matrix rank 和 composition degrees of freedom；
- 自由物种的 KKT-style stationarity residual；
- pure condensed phase 的线性项和边界退化风险；
- result 和 metadata 中可读取的 diagnostic 信息。

已验证的小算例包括 A/B 理想异构化、H2/O2/H2O 小化学计量体系、Na+/Cl-/NaCl(s) 相限制案例。

## 仪器与谱图

虚拟仪器层生成 UV-vis、HPLC/GC、IR、NMR 等 benchmark-oriented signals。目标不是数据库级谱图预测，而是让 agent 在有限测量预算下进行合理规划。

仪器输出应携带：

- signal type；
- noise；
- unit；
- cost；
- calibration metadata；
- visibility boundary。

所有 public observation 与 lab report 必须从可见观测派生，不得读取 hidden rate constants、hidden species amount 或 hidden mechanism parameters。

## 电化学与流动切片

当前电化学 slice 关注 equilibrium potential、measured cell potential、overpotential、resistance、selectivity 和 energy efficiency。它适合 `electrochemical-conversion` benchmark 交互，不是完整电池、电解槽或电化学反应器模拟器。

当前 flow slice 提供小范围 flow setup、residence-time style observation 和轻量运行报告。后续 P3 会逐步补足 limiting current、potentiostatic/galvanostatic controllers、double-layer transient 和 electrochemical scenario cards。

## 成熟度与验证

所有模型卡必须说明 maturity：

- `proxy`：只用于交互占位或定性趋势；
- `lite`：有基本物理结构和单元测试；
- `reference_validated`：有解析解、文献公式或可选 reference backend 对照；
- `professional-candidate`：结构接近专业后端，但仍需更广泛验证。

当前文档不会把任何 lightweight slice 描述成完整专业模拟器。任务、artifact 和论文写作中也必须保留这一边界。

## 验证规则

核心层应在以下情况快速失败：

- 单位或参数缺失；
- 输入超出适用范围；
- ledger 守恒失败；
- phase、species role 或 mechanism contract 不一致；
- optional backend 结果超出容忍度。

这给 transition kernels 更清晰的合同：无效化学状态应被早发现、早解释，而不是在后续评分阶段才表现为异常。
