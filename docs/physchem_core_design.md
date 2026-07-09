# 物理化学核心设计

本页给出 PhysChem 核心层的中文发布版设计说明。更细的逐项实现记录应进入开发文档；
站点主线只保留模块边界、当前能力和成熟度限制。

## 参考阅读

本地参考仓库只作为设计参照，不直接复制实现。主要参照方向包括：

- RMG-Py：反应网络、热化学和机理生成；
- Cantera：反应器、热化学和动力学接口；
- IDAES：过程系统工程和单元操作结构；
- teqp / thermopack / phasepy：热力学、EOS、相平衡；
- chemicals / thermo / fluids：物性和输运性质相关公式。

## 当前范围

当前实现覆盖 foundation/lite 主线，并包含若干 reference-validated slice。核心目标是让
ChemWorld 的任务不只是字符串游戏，而是有可审计的物理化学骨架。

## 物性核心

物性层提供蒸气压、热容、密度、摩尔体积、输运性质和 EOS 相关报告。设计重点是：

- API 可序列化；
- provenance 可追踪；
- 单位明确；
- 超出适用域时给出 warning 或 failure；
- 与 separation、reactor、instrument 共享同一报告面。

该层仍不是完整数据库；当前只覆盖 curated compounds 和 compact correlations。

## 反应网络核心

反应网络层包含 `ReactionSpec`、stoichiometry、可逆性、反应热、速率表达、ODE 入口和
局部 analytical validation。它支持 mechanism library 和 scenario generation，但不是
完整 RMG/Cantera 替代品。

重点边界：

- mechanism 是任务可执行合同；
- reaction kernel 不直接决定 task reward；
- 反应热、Gibbs、平衡和动力学应逐步接入 model card；
- 隐藏机制只通过观测和评分影响 agent。

## Mechanism 与 Scenario Library

机制库负责把反应、species role、可见参数和隐藏参数组织成可复现实验场景。Scenario
card 应说明采样范围、hidden/public boundary 和 maturity。

## 光谱与仪器耦合

虚拟仪器层生成 UV-vis、HPLC/GC、IR/NMR 等 benchmark-oriented signals。目标不是数据库
级谱图预测，而是让 agent 在有限测量预算下进行合理规划。

仪器输出应携带：

- signal type；
- noise；
- unit；
- cost；
- calibration metadata；
- visibility boundary。

## 电化学

当前电化学 slice 关注 equilibrium potential、measured cell potential、overpotential、
resistance、selectivity 和 energy efficiency。它适合 benchmark，不是完整电池或电化学
反应器模拟器。

## 可选参考 Backend 验证

参考 backend 用于局部公式级比较或 smoke validation，不应成为默认环境的硬依赖。引入
任何外部 backend 都需要说明 license、安装方式、适用范围和容忍度。

## 反应器模型核心

反应器层提供 CSTR、batch、热释放和局部稳定性/多稳态分析入口。设计上分离：

- mechanism；
- reactor equations；
- numerical integration；
- task observation；
- scoring。

这能避免任务层和数值积分层互相污染。

## 密度与摩尔体积

密度和摩尔体积用于 flash、distillation、separation 和 reactor volume 相关任务。当前
以报告型 API 为主，返回估计值、单位、适用范围和 warning。

## 输运性质

输运性质包括 viscosity、diffusivity、thermal conductivity 和 heat-transfer 相关
correlation。当前只覆盖小范围 benchmark slice，不是高压气体或复杂多相流通用后端。

## EOS 核心

EOS 层以 compact cubic EOS 为主，提供根选择、残余性质、volume translation 和 model
card。它适合训练 agent 理解相行为趋势，但不替代专业热力学软件。

## 相平衡核心

相平衡层覆盖 Raoult-style VLE、activity coefficient 入口、UNIQUAC slice 和 flash/VLE
报告。未来 extraction、evaporation 和 distillation 任务会依赖这一层。

## 平衡化学核心

平衡化学层提供小规模 reaction equilibrium 和 Gibbs minimization slice。当前适合隐藏
equilibrium scenario 和 analytical checks，不是数据库驱动的 aqueous speciation solver。

## 分离单元操作核心

分离层支持 extraction、shortcut distillation、phase split 和 ledger 集成。目标是让
downstream processing 可以进入 benchmark，而不是在反应结束后直接给最终分数。

## 传递与换热核心

传递/换热层提供小范围 pipe flow、heat-transfer correlation 和 metadata。当前覆盖
单相或简化两相场景，boiling、condensation、复杂设备几何仍不在默认范围。

## 边界

当前 PhysChem 核心是真实工程模型的“可审计轻量骨架”，不是完整商业流程模拟器。所有
使用它的任务都应声明 maturity 和适用范围。

## 验证规则

核心层应在以下情况快速失败：

- 单位或参数缺失；
- 输入超出适用范围；
- ledger 守恒失败；
- phase 或 species role 不一致；
- optional backend 结果超出容忍度。

这给 transition kernels 更清晰的合同：无效化学状态应被早发现、早解释，而不是在后续
评分阶段才表现为神秘异常。
