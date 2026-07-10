# 物理化学核心设计

本页描述 ChemWorld `physchem` 层的发布能力、模型合同、成熟度和限制。

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

## 数据基础与单位治理

三个数据基础设施切片共同提供模型输入的 identity → dimension → provenance 闭环：

- `ComponentIdentityRegistry` 以版本化不可变记录保存 canonical id、aliases、CAS、InChI、
  InChIKey、formula、charge、formula-checked molecular weight 和 provenance；identifier、alias、
  CAS、InChI 或 InChIKey 的任何跨组件碰撞都会拒绝构造，canonical JSON 使用 SHA-256 固化；
- `foundation.dimensions` 为 amount、mass、volume、temperature、pressure、energy、molar
  thermodynamics、transport、electrochemistry、NMR/MS/chromatography detector response、cost 和
  risk 提供语义维度与整数指数向量；field contract 可把“维度兼容”进一步收紧到允许单位集；
- `audit_component_data_conflicts()` 按显式 source priority 解析多来源字段，数值一致性使用
  `atol + rtol*|selected|`，结构化值使用 exact equality；required uncertainty、undefined source、
  warning/hard-fail finding、resolution 和 source citation 全部进入可摘要、可验 digest 的报告；
- `DatasetProvenanceCard` 将 registry digest、source records、policy、resolution 和 finding 固化；
  通用 trajectory `dataset_card()` 的 schema 0.3 也记录源 trajectory、commit、agent manifest、
  protocol hashes 和 replay verification。

这些能力标记为 `professional_candidate`：它们提供严格的 benchmark 数据治理合同，但不是广域
化学结构数据库、任意单位表达式解析器或自动决定科学权威性的数据库融合系统。

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

固定 TP 闪蒸切片通过 `tp_flash_with_energy_balance()` 迭代 liquid composition 与 gamma-phi
K 值，使用 Rachford-Rice 求相分率，并显式返回逐组分液/汽相数量、进料/产品焓、热负荷、
收敛状态和物料/能量残差。activity、vapor fugacity、liquid-reference fugacity 与 Poynting
factor 都是可审计输入。该模型标为 `professional_candidate`：它适合受控 benchmark，但不包含
自动物性数据库、EOS 相稳定性、临界区治理、反应闪蒸或未知温度的绝热闪蒸。

当前 LLE 切片已从单纯分配系数 proxy 推进到可审计诊断层：

- `lle_phase_stability_diagnostic()` 生成 TPD-style phase-stability report；
- 初始化策略显式记录为 `initialization_policy`；
- organic / aqueous trial composition 由 partition coefficient、phase volume 和 feed composition 生成；
- `liquid_liquid_split()` 在保持组分物料守恒的同时返回 `stability_diagnostic`；
- runtime `partition_split()` 复用同一诊断，并将 `lle_phase_status`、`lle_minimum_tpd_like` 和 `lle_partition_log_spread` 写入 phase metadata。

专业候选 extraction train 在此诊断层之外增加可执行的工艺序列：

- `DistributionCoefficientModelSpec` 保存 intrinsic partition coefficient 与 provenance；
- 每级通过 `D_i = K_i^0 gamma_i^aq / gamma_i^org` 迭代 composition-corrected distribution ratio；
- extraction stage 使用新鲜 organic contact，wash stage 使用新鲜 aqueous contact；
- stage efficiency 对平衡相分配做显式 approach-to-equilibrium，entrainment 同时记录夹带组分和水相体积；
- 最终报告 target recovery、solute-basis purity、impurity rejection、逐级收敛和全流程组分守恒。

该模型不预测 bulk solvent amount、密度、互溶度、乳化或速率控制传质，因此仍是
`professional_candidate`，不是严格 electrolyte LLE flowsheet。

冷却结晶专业候选切片由 `SolubilityCurveSpec`、`CrystallizationKineticsSpec` 和
`cooling_crystallization()` 组成：

- van't Hoff 曲线提供带温区和 provenance 的 `C*(T)`；
- 线性 cooling ramp 逐步报告 `S=C/C*`、relative supersaturation、primary nucleation 与 growth rate；
- 每个时间步形成 size cohort，成核/生长都受可用过饱和目标物上限约束；
- seed mass 作为外加目标物进入总账，避免把晶种“免费”计入 recovery；
- impurity occlusion 随新结晶量和 supersaturation 变化；
- CSD 报告 number-basis D10/D50/D90、mean、standard deviation、CV、fines fraction 与 cohort count。

该紧凑 PBM 不含 secondary nucleation、agglomeration、breakage、polymorph、shape、CFD 或
heat-balance coupling。World Law v0.2 已将其接入 Gym crystallization task，并重新冻结 task
contract 与 golden trajectories；它仍只在上述适用域内标为 `professional_candidate`。

## 设备换热与相变

`equipment_heat_transfer()` 将设备几何、污垢、集总显热和相变账合为一个可审计报告：

- `HeatTransferEquipmentSpec` 区分 jacket、coil、shell，jacket coverage 与几何修正均显式；
- `FoulingEvolutionSpec` 用渐近热阻记录 elapsed-time degradation，并通过
  `1/U_fouled = 1/U_clean + R_f(t)` 更新 U；
- 无相变时使用固定 utility 的 lumped-capacitance 解析解；
- boiling/condensation 在 `T_sat` 处分段消耗/释放潜热，phase inventory 用尽后才继续显热；
- 输出清洁/有效 U、UA、平均 duty、显热、潜热、相变量、最终温度和 energy residual；
- 若调用方提供饱和边界但 `mode=none`，跨越边界只产生 warning，不会隐式生成相变。

该切片不包含 critical heat flux、film boiling、流型换热系数、分布参数壁温或 CFD，因此标记为
`professional_candidate`。

两相压降同时保留两种明确分层的模型：

- `homogeneous_two_phase_pressure_drop()` 是平滑、轻量的 rollout proxy；
- `lockhart_martinelli_pressure_drop()` 是水平光滑圆管的 reference-validated separated-flow slice。

后者使用两相表观速度分别计算 Re 和原始 Lockhart-Martinelli 摩阻，按 laminar/turbulent 组合选取
Chisholm `C=5/12/10/20`，再报告 `X`、`phi_l^2` 和 frictional pressure drop。它与
`fluids.two_phase.Lockhart_Martinelli` 做 `rtol=1e-12` 对照。倾斜管直接失败；近单相端点、微通道和
低气液密度比会产生适用域 warning；static head、acceleration、roughness、dryout 和 critical flow
不在该 slice 内。

## 安全包络与失控指标

`assess_safety_envelope()` 将设备阈值与瞬时过程状态分离：

- envelope card 声明 temperature warning/maximum、pressure warning、relief set、MAWP、
  relief capacity 和 risk/event cost；
- `RunawayStateInput` 声明 heat generation/removal、removal slope、activation energy、
  process heat capacity、remaining exotherm、pressure rate 和 vapor generation；
- 计算 `dT/dt`、Arrhenius `dQ_gen/dT`、Semenov slope margin、adiabatic rise、MTSR、
  relief load ratio 与到 temperature/relief limit 的局部预测时间；
- 输出 `normal/warning/relief_required/emergency_shutdown`、逐项 severity、risk、cost 和 flags；
- `constraint_flags()` 可被 Gym adapter 转成 `unsafe`、relief、shutdown、risk 和 cost。

这是可解释的 process-safety screening slice，不是 relief-device sizing、vent-network solve、HAZOP、
LOPA 或真实装置保护层认证。

## 设备卡与约束

`EquipmentCardSpec` 使用 `chemworld-equipment-card-0.1` schema，把设备额定参数、provenance 与
unit-bearing scalar constraints 分开保存。标准工厂覆盖 vessel、pump、mixer、condenser、heat
exchanger 和 column。`evaluate_equipment_constraints()` 对每项返回 operating value、limit、
min/max relation、margin、normalized margin、utilization、severity 和 violated；只有 hard violation
令 `feasible=false`，warning 仍保留为规划信号。

当前卡适合 Gym action validation、scenario generation 和 trajectory audit，不执行 ASME stress、
pump curve interpolation、coupled P-T derating、compressor map 或完整 column hydraulics。

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

色谱方法层在原有虚拟 chromatogram 之上增加 `EmpiricalChromatographyAnalyteSpec`：HPLC 使用
local `log10(k)` mobile-phase/temperature slopes，GC 使用 signed retention enthalpy 的 van't Hoff
温度关系；`gc_linear_retention_index()` 用相邻 n-alkane 的 logarithmic adjusted retention 做插值；
detector calibration 返回 slope、intercept、standard error、residual standard deviation、R²、LOD
和 LOQ；tailing factor 被分类为 symmetric/fronting/tailing/severe 并写入 warning。

这些系数必须带 method/analyte provenance，不能被解释成全局 retention database 或 ab initio
retention prediction。

NMR 专业候选切片使用 provenance-tagged `ProtonNMRSignalSpec` 与 `ProtonNMRMethodSpec`：

- shift anchor 经 expected/observed reference ppm 修正；
- d/t/q/quint 用 Pascal intensity，dd 用 sequential doublet splitting，J 通过场强转换成 ppm；
- integral 按 species amount × proton count × response factor 计算并归一化；
- solvent residual、line-width overlap、`Delta nu/J < 10`、exchangeable proton 和 unresolved
  multiplet 都进入显式 warning。

它是 first-order 1H stick/assignment layer，不包括 quantum shift prediction、dynamic exchange、
relaxation、NOE、shimming、phase/baseline processing 或 2D NMR。

MS 专业候选切片对 H/C/N/O/F/Si/P/S/Cl/Br 的自然丰度做 repeated convolution，将同一 nominal
shift 的 isobar 合并为 probability-weighted exact-mass center，并报告 abundance、base-peak intensity
和 m/z。fragment 由 provenance-tagged formula、charge、relative intensity、assignment 与 neutral loss
显式声明；detector response 同时给 mean、RSD 和 standard deviation。Cl/Br/C 的解析 isotope pattern
构成回归基准。

该模型不自动加入 proton/electron/adduct mass correction，也不预测 fragmentation、ion-source
competition、metastable ions、high-resolution lineshape 或 library match。

## 电化学与流动切片

当前电化学 slice 关注 equilibrium potential、measured cell potential、overpotential、resistance、selectivity 和 energy efficiency。它适合 `electrochemical-conversion` benchmark 交互，不是完整电池、电解槽或电化学反应器模拟器。

World Law v0.2 的 flow runtime 使用共享 compiled mechanism 的几何解析 PFR：由流量与停留时间
确定反应器体积，显式声明管长、管径、粗糙度、流体性质和轴向热边界，并输出 Reynolds 数、
Darcy 压降、能量账、物料残差和求解器诊断。该切片不包含多相流、轴向弥散、径向梯度、
复杂换热网络或 CFD，因此标为 `professional_candidate`。电化学层同时提供 limiting current、
potentiostatic/galvanostatic controllers、double-layer transient 和 electrochemical scenario cards。

电化学传质专业候选切片使用 `DiffusionLayerSpec`：

- `i_lim = n F A D C_bulk / delta`；
- 请求电流低于平台时 bulk concentration 按恒流线性下降；
- 达到平台后或初始即超限时，按 `dC/dt = -(AD/(delta V))C` 指数下降；
- 报告 surface/bulk concentration、initial/final i_lim、transition time、signed useful current、
  applied/useful/side charge、depletion 和 current efficiency。

该解析 slice 不包含 migration、convection、porous electrode、multiple reactants 或动态 diffusion layer。

电化学 controller 使用 versioned `ElectrochemicalControlRecipe`：segment 明确声明
potentiostatic/galvanostatic 与 ramp/hold。执行器分别维护 potential/current state，对 ramp 应用
range 与 slew clipping，对 hold 的突变标记 sample-slew warning；输出逐点 trace、逐段 operation log、
final state 和 clipping count。canonical recipe+limits+initial state 与完整 execution 分别计算 SHA-256，
`verify_electrochemical_control_replay()` 通过重新执行做逐字段比对。

该组件是 deterministic setpoint engine，不包含 PID、noisy feedback、hardware latency 或 plant response。

double-layer slice 使用 `R_s-(R_ct || C_dl)` Randles RC：potential step 下电流从 `DeltaE/R_s`
衰减到 `DeltaE/(R_s+R_ct)`；current step 下 capacitive current 指数衰减、Faradaic current 互补上升。
每个 trace point 同时报告 terminal/interfacial potential 和三类 current，解析积分满足
`Q_total = Q_F + Q_C`。少于 5 time constants 与 startup capacitive dominance 都进入 observation warning。

该模型不含 Warburg/CPE、nonlinear Butler-Volmer、adsorption、porous electrode 或 aging。

电化学 scenario card 使用公开/私有双视图：公开视图包含 redox metadata、electrode area/gap/volume、
electrolyte window、cathodic/anodic side-reaction onset、qualitative behavior 和 hidden parameter 的
distribution family；range endpoints 与生成值仅存在私有视图。`public-dev/public-test/private-eval`
使用 schema/scenario/split/seed/salt 的稳定 hash seed，private-eval 强制 salt，公开实例只携带不泄密的
hidden-parameter digest。生成实例可直接构造 reaction、electrolyte resistance、diffusion layer 和
double-layer model bundle。

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
