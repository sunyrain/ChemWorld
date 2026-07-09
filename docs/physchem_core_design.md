# 物理化学核心设计

本页描述 ChemWorld `physchem` 层的当前稳定结构。更细的任务记录放在 `TODO.md`
和开发审计文档中；站点主线只保留模块边界、当前能力和成熟度限制。

## 设计目标

`physchem` 层不是外部专业软件的复制品，也不是简单 proxy 集合。它的目标是提供一套
可审计、可序列化、可测试的轻量物理化学核心，使 ChemWorld 的交互任务具备明确的
物理合同。

核心原则：

- 所有模型必须声明单位、适用范围、失败边界和 maturity label；
- 计算结果应返回 report 或 ledger，而不是只返回一个裸数值；
- 数值内核、任务评分、观测生成和文档声明必须一致；
- 参考库只用于设计对照和验证思路，不直接复制实现。

## 参考方向

本地参考仓库只作为设计对照。当前主要参考方向包括：

- RMG-Py：反应网络、热化学和机理生成；
- Cantera：反应器、热化学、动力学和化学平衡接口；
- IDAES：过程系统工程和单元操作结构；
- teqp / thermopack / phasepy：热力学、EOS、相平衡；
- chemicals / thermo / fluids：物性和输运性质相关公式。

## 当前范围

当前实现覆盖 foundation/lite 主线，并包含若干 reference-validated slice。它足以支撑
虚拟实验 benchmark 的可解释交互，但不是完整商业流程模拟器或数据库驱动的真实反应预测器。

## 物性核心

物性层提供蒸气压、热容、密度、摩尔体积、输运性质、EOS 相关报告和 curated
component 数据。

设计重点：

- API 可序列化；
- provenance 可追踪；
- 单位明确；
- 超出适用域时返回 warning 或 failure；
- separation、reactor、instrument 共享同一报告格式。

当前边界：还不是完整物性数据库；只覆盖 curated compounds、compact correlations 和
benchmark 所需的局部物性。

## 反应网络核心

反应网络层包含 `ReactionSpec`、stoichiometry、可逆性、反应热、速率表达、ODE
入口和局部 analytical validation。

重点边界：

- mechanism 是任务可执行合同；
- reaction kernel 不直接决定 task reward；
- 反应热、Gibbs、平衡和动力学逐步通过 model card 接入；
- 隐藏机理只通过观测和评分影响 agent。

## Mechanism 与 Scenario Library

机制库负责把反应、species role、可见参数和隐藏参数组织成可复现实验场景。Scenario
card 应说明采样范围、hidden/public boundary、maturity 和适用任务。

后续专业化应继续把固定物种名迁移到 mechanism spec 和 compiled mechanism，而不是写入
通用 runtime 或 scoring。

## 光谱与仪器耦合

虚拟仪器层生成 UV-vis、HPLC/GC、IR、NMR 等 benchmark-oriented signals。目标不是
数据库级谱图预测，而是让 agent 在有限测量预算下进行合理规划。

仪器输出应携带：

- signal type；
- noise；
- unit；
- cost；
- calibration metadata；
- visibility boundary。

## 电化学核心

当前电化学 slice 关注 equilibrium potential、measured cell potential、
overpotential、resistance、selectivity 和 energy efficiency。它适合 benchmark
交互，不是完整电池、电解槽或电化学反应器模拟器。

## 可选参考 Backend 验证

参考 backend 用于局部公式级比较或 smoke validation，不应成为默认环境的硬依赖。
引入任何外部 backend 都必须说明 license、安装方式、适用范围和容忍度。

## 反应器模型核心

反应器层提供 batch、CSTR、PFR、半批式、热释放和局部稳定性分析入口。设计上分离：

- mechanism；
- reactor equations；
- numerical integration；
- task observation；
- scoring。

这样可以避免任务层和数值积分层互相污染。

## 密度与摩尔体积

密度和摩尔体积用于 flash、distillation、separation 和 reactor volume 相关任务。
当前以报告型 API 为主，返回估计值、单位、适用范围和 warning。

## 输运性质

输运性质包括 viscosity、diffusivity、thermal conductivity、pressure drop 和
heat-transfer correlations。当前只覆盖小范围 benchmark slice，不是高压气体或复杂
多相流通用后端。

## EOS 核心

EOS 层以 compact cubic EOS 为主，提供根选择、残余性质、volume translation 和 model
card。它适合训练 agent 理解相行为趋势，但不替代专业热力学软件。

## 相平衡核心

相平衡层覆盖 Raoult-style VLE、activity coefficient 入口、UNIQUAC slice、
flash/VLE 报告和 LLE 诊断。

### LLE 相稳定性与相分配

当前 LLE 切片已从单纯分配系数 proxy 推进到可审计的 `reference_validated` 诊断层：

- `lle_phase_stability_diagnostic()` 生成 TPD-style phase-stability report；
- 初始化策略显式记录为 `initialization_policy`；
- organic / aqueous trial composition 由 partition coefficient、phase volume 和 feed
  composition 生成；
- `liquid_liquid_split()` 在保持组分物料守恒的同时返回 `stability_diagnostic`；
- `liquid_liquid_extraction()` 把最新一级 split diagnostic 写入 separation ledger
  metadata；
- runtime `partition_split()` 复用同一诊断，并把 `lle_phase_status`、
  `lle_minimum_tpd_like` 和 `lle_partition_log_spread` 写入 phase metadata。

边界：这不是严格 LLE flash、tie-line tracing 或全局 Gibbs minimization。它适合
extraction / partition-discovery benchmark，让 agent 看到稳定、可解释、可回放的相分配
规律。严谨 electrolyte LLE、密度耦合体积预测和参数估计仍属于后续 P3 深化。

## 平衡化学核心

平衡化学层提供小规模 reaction equilibrium、acid-base、precipitation 和 fixed-TP
ideal Gibbs minimization slice。当前适合隐藏 equilibrium scenario 和 analytical
checks，不是数据库驱动的 aqueous speciation solver。

### Gibbs Minimization 诊断

`solve_gibbs_minimization()` 当前保留 SLSQP fixed-TP ideal-mixture 求解器，同时新增
`GibbsMinimizationDiagnostic` 和 `diagnose_gibbs_minimization()`：

- 检查 element residual、charge residual 和 bound violation；
- 计算 constraint matrix rank 和 composition degrees of freedom；
- 对自由物种计算 KKT-style stationarity residual；
- 标记 pure condensed phase 的线性项和边界退化风险；
- 将 diagnostic 写入 result 和 metadata，便于 trajectory、model card 和审计脚本读取。

已验证的小算例包括：

- A/B 理想异构化，平衡比满足 `n_B / n_A = exp[-Delta G0 / RT]`；
- H2/O2/H2O 小化学计量体系，元素约束守恒并偏向低 Gibbs 产物；
- Na+/Cl-/NaCl(s) 相限制与电荷平衡案例。

边界：这些诊断是对当前 SLSQP 结果的局部一致性检查，不证明任意非理想、多相、数据库生成体系的全局最优性。

## 分离单元操作核心

分离层支持 extraction、shortcut distillation、phase split、dry/concentrate 和 ledger
集成。目标是让 downstream processing 进入 benchmark，而不是在反应结束后直接给最终分数。

当前边界：部分 dry/concentrate 操作仍是 benchmark proxy；后续需要逐步补充设备、能量和相平衡细节。

## 传递与换热核心

传递和换热层提供小范围 pipe flow、pressure drop、heat-transfer correlation 和 metadata。
当前覆盖单相或简化两相场景，boiling、condensation、复杂设备几何仍不在默认范围。

## 边界

当前 `physchem` 核心是真实工程模型的可审计轻量骨架，不是完整商业流程模拟器。所有使用
它的任务都必须声明 maturity 和适用范围。

## 验证规则

核心层应在以下情况下快速失败：

- 单位或参数缺失；
- 输入超出适用范围；
- ledger 守恒失败；
- phase 或 species role 不一致；
- optional backend 结果超出容忍度。

这给 transition kernels 更清晰的合同：无效化学状态应被早发现、早解释，而不是在后续评分阶段才表现为异常。
