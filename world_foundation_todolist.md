# ChemWorld 世界基座升级清单

最后更新：2026-07-10

本文件面向负责物理化学底座强化的团队。目标不是把所有模块包装成“高保真”，而是让每个
运行时声明都具备真实调用关系、适用域、守恒、数值诊断、参考验证和可复现证据。

当前 `chemworld-serious-v1` 与 `chemworld-physical-chemistry-v0.3` 应视为冻结基线。任何改变
状态转移、观测或得分的底座升级，都进入新的 World Law 和 benchmark contract；不得静默覆盖
v1 证据。

## 当前结论

- 共 15 个注册任务：12 个整体为 `lite`，3 个整体为 `proxy`。
- 没有任务整体达到 `reference_validated`、`professional_candidate` 或 `professional`。
- 6 个 serious benchmark 任务全部为 `lite`。
- 三个共同瓶颈是 `reaction_kinetics`（14 个任务）、`reactors`（14 个任务）和
  `spectroscopy_instruments`（15 个任务），当前均为 `lite`。
- 三个 proxy 任务都被同一个 `separations` 模块限制；具体操作是 `dry`、`concentrate` 和
  `transfer`。
- 现有结晶、连续流、萃取/洗涤已是 `professional_candidate`；蒸馏、电化学和平衡化学已有
  `reference_validated` 切片。但任务成熟度按最弱必需模块聚合，因此这些局部成果尚不能提高
  整体任务等级。

这里的计数来自当前任务合同。它还暴露了一个必须优先修复的问题：
`default_kernel_maturity()` 给 14 个任务无条件登记反应动力学、反应器和合成仪器，并不一定等于
实际运行时依赖。例如 `partition-discovery` 的主要运行路径是相接触和测量，却仍被登记为依赖
反应器。团队在升级模型前，必须先把“声明依赖”改成“由 operation → service → kernel 实际调用
关系生成的依赖”。

## 全任务成熟度清单

| Task | 角色 | 整体等级 | 当前最弱模块 | 已有较强切片 |
| --- | --- | --- | --- | --- |
| `partition-discovery` | core + serious v1 | `lite` | reaction、reactor、instrument 声明；需先核实是否真实依赖 | phase equilibrium `professional_candidate` |
| `reaction-to-crystallization` | serious v1 | `lite` | reaction kinetics、reactor、instrument | crystallization `professional_candidate` |
| `reaction-to-distillation` | serious v1 | `lite` | reaction kinetics、reactor、instrument | distillation `reference_validated` |
| `flow-reaction-optimization` | serious v1 | `lite` | reaction kinetics、generic reactor、instrument | continuous flow `professional_candidate` |
| `electrochemical-conversion` | serious v1 | `lite` | reaction kinetics、reactor、instrument | electrochemistry `reference_validated` |
| `equilibrium-characterization` | serious v1 | `lite` | instrument | equilibrium chemistry `reference_validated` |
| `reaction-to-assay` | core / smoke | `lite` | reaction kinetics、reactor、instrument | Beer–Lambert 与色谱局部参考切片 |
| `reaction-optimization-standard` | registered | `lite` | reaction kinetics、reactor、instrument | — |
| `reaction-safety-constrained` | registered | `lite` | reaction kinetics、reactor、instrument；安全 screening 也需单列证据 | — |
| `reaction-mechanism-explanation` | exploratory | `lite` | reaction kinetics、reactor、instrument | — |
| `low-budget-characterization` | exploratory | `lite` | reaction kinetics、reactor、instrument | — |
| `public-private-generalization` | private-eval placeholder | `lite` | reaction kinetics、reactor、instrument | — |
| `reaction-to-purification` | core / exploratory | `proxy` | dry、concentrate、transfer | LLE 与 wash `professional_candidate` |
| `purity-yield-tradeoff` | exploratory | `proxy` | dry、concentrate、transfer | LLE 与 wash `professional_candidate` |
| `tool-agent-planning` | exploratory | `proxy` | dry、concentrate、transfer | LLE 与 wash `professional_candidate` |

## 升级目标

第一目标不是让标签变好看，而是让所有任务的成熟度声明可信。建议下一版采用两级目标：

1. 所有正式任务的必需运行时模块至少达到 `reference_validated`；
2. 对结晶、连续流、相平衡等已有较完整模型卡的模块，继续扩大适用域证据后再决定是否提升到
   `professional`，不要把“代码复杂”直接等同于专业验证。

当共同反应、反应器和仪器层达到 `reference_validated` 后，当前 12 个 lite 任务才可能整体升级；
当 downstream separation 同时移除 proxy 后，剩余三个任务才具备进入正式任务审查的资格。

## P0：先修复成熟度与运行时真相

- [ ] WF-00.1 从 `TaskRuntimeProfile`、`DomainServiceRegistry`、operation kernel 和 instrument
  contract 自动生成每个任务的实际模块依赖，不再在 `default_kernel_maturity()` 中无条件添加
  三个共同模块。
- [ ] WF-00.2 为每个 operation 记录 `service_id`、`kernel_id`、`model_id`、版本、maturity 和
  provenance；轨迹必须能证明一次操作最终调用了哪个物理模型。
- [ ] WF-00.3 检查 `partition-discovery`、`flow-reaction-optimization` 和
  `equilibrium-characterization` 的冗余依赖；没有实际参与状态转移或观测的模块不得压低任务等级。
- [ ] WF-00.4 区分“运行时模型”“诊断模型”“离线参考模型”。仅存在于 `physchem/` 但未被
  runtime 调用的专业实现，不得计入任务成熟度。
- [ ] WF-00.5 建立机器门禁：任务声明的每个 model id 必须可从至少一条允许操作到达；实际
  到达的每个 model id 又必须出现在任务声明中。
- [ ] WF-00.6 把成熟度审计生成 JSON 报告，固定 15 个任务的实际依赖图、最低等级和证据路径。

验收：删除或替换任一 kernel 后，受影响任务的成熟度和 contract hash 自动变化；虚假、缺失、
不可达或重复依赖都会令测试失败。

## P1：共同反应与反应器基座

### WF-01 反应网络、热化学与动力学

- [ ] 支持可逆、多反应、竞争/串联网络，以及统一的化学计量、元素和电荷守恒检查。
- [ ] 统一 Arrhenius、modified Arrhenius、可逆速率、活度/浓度基准和反应级数的单位合同。
- [ ] 将反应焓、热容、相态和温度依赖接入能量账；禁止把独立随机参数同时当成动力学与热力学
  真值而不满足一致性。
- [ ] 对正逆速率与平衡常数增加热力学一致性检查；不满足时明确失败或降级，不能静默继续。
- [ ] 提供 stiff/non-stiff solver 策略、事件检测、非负性、局部误差、守恒残差和失败原因。
- [ ] 建立解析算例：一级、二级、可逆、并联、串联、绝热放热和守恒极限。
- [ ] 建立独立参考对照：在相同小机制和适用域内与 Cantera 或等价后端比较时间轨迹、终态和
  热量，固定 rtol/atol。
- [ ] Scenario generator 只从声明适用域采样；将速率常数、活化能、反应焓和催化/溶剂效应的
  分布写入有版本的参数卡。

### WF-02 Batch、CSTR、PFR 与半连续反应器

- [ ] 分离理想 batch、semibatch、CSTR 和 PFR 的物料/能量方程，不再使用一个笼统
  `chemworld_reactor_lite` 标签覆盖所有行为。
- [ ] Batch/semibatch：投料曲线、体积变化、UA、夹套/盘管边界、相变与压力边界。
- [ ] CSTR：稳态/动态模式、停留时间、多个稳态、启动与冲洗过程、不可行解诊断。
- [ ] PFR：几何、停留时间分布的声明边界、压降、热边界和 reaction network 的一致耦合。
- [ ] 所有反应器返回统一 material/energy residual、solver status、iteration、warning 和
  operating-domain flags。
- [ ] 与解析解及独立参考后端对照；对零速率、无限停留时间、等温、绝热和无压降极限做测试。
- [ ] 明确高风险外推、刚性失败、热失控、干涸、负库存和超设备包络时的回滚策略。

验收：`reaction_kinetics` 与各 reactor module 可以分别达到 `reference_validated`；任务只声明
其实际使用的反应器类型。

## P1：仪器、谱图与可辨识性基座

### WF-03 合成仪器统一管线

这是覆盖全部 15 个任务的共同瓶颈，优先级与反应基座相同。

- [ ] 建立统一链路：hidden composition → sample preparation → method settings → raw signal →
  calibration/processing → public estimate；每一层均有独立 schema 和 provenance。
- [ ] 区分 evaluator truth 与 final assay。`final_assay` 不能只是无噪声 hidden-state 直读；应是
  声明精度、偏差、LOD/LOQ 和成本的参考方法，排行榜真值由 evaluator 独立重算。
- [ ] HPLC/GC：保留时间、峰宽、共洗脱、响应因子、校准、漂移、饱和、积分和 censoring。
- [ ] UV–vis：Beer–Lambert 适用域、混合吸收、光程、基线、杂散光、校准与检测限。
- [ ] pH：活度基准、温度、junction/校准误差、量程、缓冲能力与重复测量。
- [ ] IR/NMR/MS：明确哪些是真正参与任务的 observation channel；若未参与正式任务，不要用其
  独立专业模型抬高任务成熟度。
- [ ] 清理 `world/spectra.py` 中未声明的 broad proxy fallback。保留 fallback 时必须暴露模型
  maturity；正式任务应使用有物种/方法卡的可追溯信号。
- [ ] 同一 hidden state 的 replicate 分布必须稳定；不同关键状态在声明仪器下必须具有统计可辨
  识性；高成本或高信息仪器应产生可测量的决策价值差异。
- [ ] 建立 blank、standard、mixture、overlap、LOD/LOQ、饱和、漂移与错误方法的 golden cases。

验收：每个正式 task 都有 instrument identifiability report；Agent 看不到 hidden species、参数或
evaluator truth；仪器模型至少达到 `reference_validated` 的局部适用域要求。

## P1：移除剩余 downstream proxy

### WF-04 Dry、Concentrate、Transfer

- [ ] 将当前统一的 `chemworld_separation_proxy` 拆成三个独立 model id 和 operation contract。
- [ ] Dry：显式湿组分/有机相库存、干燥剂容量与选择性、接触平衡或速率、夹带/产品损失、终点
  判据和废物流。
- [ ] Concentrate：VLE/蒸气压、真空/压力、热量、蒸发速率、溶剂回收、目标物挥发损失、设备
  容量和过热风险。
- [ ] Transfer：源/目标容器、管线 hold-up、dead volume、残留、冲洗、相夹带、取样损失和严格
  物料闭合。
- [ ] 复用现有 equipment card、heat-transfer、flash/VLE 和 phase ledger；禁止另写一套旁路状态。
- [ ] 为每项操作给出零容量、无限容量、零挥发度、完全挥发、零 hold-up 和满 hold-up 极限测试。
- [ ] 与公开物性/解析计算或独立后端的小范围结果对照，并记录温压、组成和设备适用域。
- [ ] 专业 kernel 接管后，删除 runtime 中对应 fallback 路由和成熟度 proxy 声明；不得保留双重
  实现由隐式条件随机选择。

验收：`reaction-to-purification`、`purity-yield-tradeoff` 和 `tool-agent-planning` 不再包含
`proxy`；所有物流、能量、成本和风险可从 ledger 重算。

## P2：扩展已有专业候选模块

### WF-05 相平衡、萃取与洗涤

- [ ] 用有 provenance 的组分/溶剂参数替代仅为 benchmark 校准的 intrinsic distribution
  coefficient，或明确保留“匿名虚拟物系”profile。
- [ ] 增加 activity model、温度依赖、电解质/盐析、pH-dependent speciation 和多级逆流边界。
- [ ] 加强 flash、phase stability、tie-line、entrainment 和 material closure 的联合验证。
- [ ] 对单相极限、临界混溶、极高/极低 K、相反转和乳化/不收敛给出显式诊断。

### WF-06 结晶

- [ ] 扩展 secondary nucleation、agglomeration、breakage、polymorph/solvate 和 shape 边界。
- [ ] 将能量平衡、母液活度、杂质吸附/包裹和过滤洗涤与 PBM 一致耦合。
- [ ] 以矩守恒、网格收敛、粒数/质量闭合和公开 benchmark case 验证 CSD。
- [ ] 明确哪些高级过程是 v0.4 必需项，避免一次升级变成不可验证的全流程模型。

### WF-07 蒸馏

- [ ] 在现有 constant-relative-volatility shortcut 之外，增加多组分 flash 和温压依赖 VLE。
- [ ] 若任务继续模拟 column，增加 MESH/energy、reflux、stage efficiency、condenser/reboiler duty
  与基本 hydraulics；否则把任务明确限定为 batch shortcut cut optimization。
- [ ] 验证 Fenske/Underwood/Gilliland 极限、总回流/最小回流、物料与能量闭合。

### WF-08 连续流

- [ ] 保持 geometry-resolved PFR 为唯一正式路径，完成与 WF-01/WF-02 新 reaction core 的耦合。
- [ ] 扩展换热、黏度/密度温度依赖、停留时间、压降和安全包络的联合响应。
- [ ] 对 laminar/turbulent 边界、零反应、等温、绝热、短/长管和压降失败做参考验证。

### WF-09 电化学

- [ ] 将 Nernst、Butler–Volmer、Faraday ledger、传质和 controller 统一到同一个状态合同。
- [ ] 增加多物种竞争、ohmic drop、浓差、current distribution 的声明边界；迁移、对流、多孔电极
  若不实现，继续作为明确限制。
- [ ] 建立开路、平衡、低过电位、Tafel、高传质和耗尽极限对照。

### WF-10 水相与平衡化学

- [ ] 从单弱酸/顺序 Ksp hooks 扩展到多元酸碱、离子强度、活度、络合与同时沉淀的小规模系统。
- [ ] 强化 Gibbs minimization 的相出现/消失、rank deficiency、KKT residual 和初值不变性。
- [ ] 与 Reaktoro、Cantera 或解析物种分布在明确小体系中对照；不追求未验证的全元素数据库覆盖。

## P2：物性、设备、安全与成本公共层

### WF-11 物性与设备

- [ ] 建立 component identity → property package → model selection 的唯一入口；禁止服务层自行拼
  常数。
- [ ] 统一密度、热容、黏度、导热、蒸气压、相变焓和扩散系数的单位、温区、来源与外推策略。
- [ ] 将 vessel、pump、mixer、heat exchanger、column 和 electrochemical cell 的 equipment card
  真正接入 operation validation 与 runtime diagnostics。
- [ ] 安全风险必须由物理状态和设备包络产生，不得只由动作类型或温度阈值 proxy 决定。
- [ ] 成本分为资源、仪器、能耗、废物和失败成本；各项可追溯且不能重复计费。

验收：物性冲突、缺失、超域和 solver failure 均显式记录；安全/成本变化会真实影响 episode 结果，
同时不被误称为法规或工程认证。

## P3：集成、验证与下一版冻结

### WF-12 统一交付标准

每个工作包的 PR/合并请求必须同时提交：

- [ ] 版本化 model card：方程/算法、假设、单位、适用域、失败模式、reference、证据和 intended use；
- [ ] typed input/output 与 kernel/service adapter；
- [ ] 物料、元素、电荷和能量守恒测试；不适用的守恒项要解释；
- [ ] 解析极限、单调性、连续性、solver convergence 和失败回滚测试；
- [ ] 至少一个独立 reference backend 或公开 reference case；
- [ ] runtime integration test，证明任务轨迹确实调用新模块；
- [ ] 旧实现清理清单，证明没有专业实现与 proxy 同时留在正式路径；
- [ ] 性能基准和确定性重放测试；
- [ ] maturity 变更说明以及所有受影响 task/scenario/world-law/observation/scoring hashes。

### WF-13 下一版 World Law

- [ ] 在独立 runtime profile 中集成升级，不改写 `chemworld-physical-chemistry-v0.3` 的行为。
- [ ] 完成所有 operation × service × kernel 覆盖审计。
- [ ] 重跑 15 tasks × 多 seeds 的 environment consistency、golden、reference validation 和 replay。
- [ ] 对六个 serious tasks 重做 response surface、baseline、threshold 和 OOD generalization 校准。
- [ ] 若得分或最优策略发生变化，发布新的 benchmark contract；不得沿用 v1 排名或阈值。
- [ ] 清理新发布路径之外的已替代 proxy，但保留旧 wheel/tag 作为 v1 可复现载体。
- [ ] 更新用户文档，只公开真实成熟度和适用边界；本团队清单不进入发布站点导航。

## 推荐并行工作流

可直接认领的独立模块包、目录所有权和合并顺序见
[`workstreams/world_foundation/README.md`](workstreams/world_foundation/README.md)。模块团队不直接
修改 task contract、共享 registry、runtime dispatch 或冻结证据；这些文件由集成模块独占，
从而使物理团队能够并行开发而不互相覆盖。

| 工作流 | 范围 | 前置依赖 | 主要解锁任务 |
| --- | --- | --- | --- |
| A | WF-00 依赖真相与证据图 | 无 | 全部 15 个 |
| B | WF-01/WF-02 反应与反应器 | WF-00 接口 | 14 个声明依赖反应的任务 |
| C | WF-03 仪器与可辨识性 | WF-00 observation contract | 全部 15 个 |
| D | WF-04 downstream unit ops | WF-00、物性接口 | 3 个 proxy 任务 |
| E | WF-05/WF-06/WF-07 相与分离 | WF-00、WF-11 物性 | partition、crystal、distillation、purification |
| F | WF-08/WF-09/WF-10 特殊反应域 | WF-01/WF-02 | flow、electrochemical、equilibrium |
| G | WF-11 物性、设备、安全 | WF-00 | 所有工艺模块 |
| H | WF-12/WF-13 集成与冻结 | A–G 的目标切片 | 下一版正式 benchmark |

不建议等待所有专业模块全部完成后再集成。每个工作流应先交付一个范围小、证据闭合、可接入
runtime 的 reference slice，再逐步扩大适用域。

## 常用检查

```powershell
# 当前任务成熟度与实际声明
.\.venv\Scripts\python.exe -m chemworld.cli tasks list
.\.venv\Scripts\python.exe -m chemworld.cli tasks readiness

# 运行时边界和参考后端
.\.venv\Scripts\python.exe scripts\audit_runtime_boundary.py
.\.venv\Scripts\python.exe scripts\run_reference_validation.py

# 所有任务的环境一致性
.\.venv\Scripts\python.exe scripts\audit_environment_consistency.py --tasks all --seeds 0 1 2

# 下一版冻结前的完整门禁
.\.venv\Scripts\python.exe scripts\run_release_gate.py
```

## 完成定义

世界基座升级完成，不等于所有模型达到现实工业预测精度。完成指：任务实际调用关系可证明；
正式路径无未声明 proxy；每个模型在其适用域内有独立验证；状态、守恒、失败、观测和 provenance
可审计；新 World Law 下的 benchmark 难度与证据已重新冻结。
