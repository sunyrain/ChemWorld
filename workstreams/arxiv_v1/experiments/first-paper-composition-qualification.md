# 第一篇组合资格实验说明

状态：**FROZEN BEFORE DATA GENERATION**
冻结日期：**2026-08-04**
执行者：**Codex `/root`**

预启动修订（2026-08-04，尚未生成正式数据）：原表按轴数粗估了部分 pairwise covering rows；将冻结设计
用既定生成算法物化后，实际行数要求组合总分母为 52，而非 42。下表和通过规则据此修正；pattern、seed、
连续 bounds、workflow 数和通过/失败规则均未改变。预执行还发现三个 authoring level 使用了评分器不接受
的 objective 标签、纯 phase 流程未先建立材料、电化学两阶段流程缺少既有 pH gate 且未改变第二 setpoint；
在正式数据生成前将 objective levels 收敛为公开支持的 `balanced` / `yield`，并仅修正上述 workflow 动作使其
满足现有运行时合同。资格数据仍未启动，所有 52 个 case 将从第一项开始执行。

本说明覆盖 C01--C08 与 D01--D04 的一次正式资格批次。它只限定虚拟仪器、声明组件及其接口；不做
agent 排名、机理解释、任意任务穷举或真实实验室外推。旧 cross-world 协议的 owner、租约、源提交和
手工 manifest 不沿用；可复用的 runner 代码必须重新绑定本说明和当前 `main`。

## 问题与独立单位

问题：在冻结的 v1 组件词汇和兼容域内，参考任务、覆盖生成组合和冻结未见组合能否保持声明的单位、
物质/电荷/能量适用守恒、事务原子性、资源对账、观测边界、生命周期和精确重放语义？模块级模型是否
在声明适用域内满足零输入、边界、方向性、守恒和已有参考对照，而不把模拟器自洽性写成现实预测？

独立计数单位分开报告：

- 参考资格：64 个注册 `task_id × world_seed` 单元；
- 组合资格：52 个生成 composition case；
- 冻结未见资格：其中 8 个反应--蒸馏 case，亦为 U05 的共同批次；
- 模块资格：8 个物理组件，每个 4 个预设探针，共 32 个模块探针；
- 接口资格：7 条注册跨组件路径。

配方、操作、测量、负向探针和 replay 是上述单元内的重复检查，不作为独立样本。只报告确定性计数，
不做显著性检验、bootstrap 或把操作数当作样本量。

## 覆盖设计

### 参考任务与运行时语义

当前 15 个注册任务及公开 seeds 共 64 个单元。每个单元固定执行当前 task-recipe 空间的中点、每个连续
坐标的低/高边界和每个离散类别；当前冻结分母为 1786 条有效配方执行。每条配方必须闭合到一次已提交
final assay，并在临时目录内精确 replay。每个单元另运行 3 个负向探针：未知操作、fresh-reset 上的
测量前置条件失败和 solvent stock 资源耗尽，共 192 个探针。

C01 的 15 任务结构基由 live task registry 与 `configs/current.json` 中当前 `task_design` 绑定交叉检查；
只汇总组件、接口、操作、仪器、资源、终止和评价覆盖，不读取或重画模型成绩。

### 覆盖生成组合

全部 suite 使用 pairwise discrete strength 2、ordered interaction depth 2；除无连续轴的
`phase-observation` 外使用 seeded Latin hypercube。生成数取 pairwise rows、LHS samples 和 workflow
templates 的最大值，不做笛卡尔积，也不声称穷举。

| Pattern | Seed | 二值离散轴 | 连续轴与 bounds | Workflows | Cases |
| --- | ---: | --- | --- | ---: | ---: |
| phase-observation | 101 | phase profile；instrument profile；objective | 无 | 1 | 6 |
| reaction-thermal-observation | 102 | reaction family；thermal range；instrument profile | heat temperature 350--390 K；duration 600--1800 s | 2 | 6 |
| phase-separation-observation | 103 | phase profile；instrument profile；objective | phase volume 0.010--0.020 L；extractant volume 0.010--0.025 L；mix 60--300 s；settle 120--600 s | 2 | 6 |
| reaction-crystallization-observation | 104 | reaction family；thermal range；seed-mass range | reaction temperature 350--390 K；reaction time 600--1800 s；seed 0.002--0.010 g；cooling temperature 275--305 K；cooling time 900--3600 s | 2 | 6 |
| reaction-distillation-observation | 105 | 见下方冻结未见批次 | 见下方冻结未见批次 | 2 | 8 |
| reaction-continuous-flow-observation | 106 | reaction family；flow-rate range；residence-time range；instrument profile | flow 0.5--5.0 mL/min；residence 60--600 s；temperature 330--390 K | 2 | 6 |
| reaction-electrochemistry-observation | 107 | reaction family；potential range；current range；instrument profile | potential 0.5--1.8 V；current 25--150 mA；electrolysis 300--1800 s | 2 | 7 |
| reaction-phase-separation-observation | 108 | reaction family；phase profile；instrument profile；objective | reaction temperature 350--390 K；reaction time 600--1800 s；phase volume 0.010--0.020 L；extractant volume 0.010--0.025 L；mix 60--300 s；settle 120--600 s；wash 0.003--0.010 L；concentrate 300--900 s；transfer 0.65--0.95 | 2 | 7 |

每个二值 level 必须落在组件已声明域内；两个 instrument profile 都必须包含该 suite 两条 workflow 实际
使用的仪器和 final assay。实现阶段只可把本表展开为机器配置，不得改变 pattern、seed、轴数、bounds、
workflow 数或 case 分母。有连续轴的 suite 将 LHS sample count 固定为表中 `Cases` 数，因此 pairwise
rows 少于该数时不改变正式分母。

### C03/U05 冻结未见批次

共同 batch 为 seed 105 的 `reaction + thermal + distillation + observation` suite，base task 资源冻结为
16 次操作、14400 s、0.001 L 样品、4 次仪器使用和 1 次 final assay。六个二值离散轴为：

- reaction family：`declared-family-a` / `declared-family-b`；
- fraction count：2 / 4；
- instrument profile：`[hplc, gc, final_assay]` /
  `[hplc, gc, uvvis, final_assay]`，同时绑定 observation 与 task；
- thermal temperature range：`[340, 400]` / `[345, 405]` K；
- distillation temperature range：`[315, 400]` / `[320, 405]` K；
- reflux-ratio range：`[0.5, 3.5]` / `[0.8, 4.0]`。

LHS 样本数为 8，连续轴为 reaction temperature 350--390 K、reaction time 600--1800 s、evaporation
temperature 325--345 K、evaporation time 300--900 s、distillation temperature 350--390 K、distillation
time 900--2400 s、reflux ratio 1.0--3.0 和 collected transfer fraction 0.65--0.95。真实六轴设计的
pairwise rows 为 7，故由 8 个 LHS samples 决定正式 batch 为 8 个 case。

两条有序流程均从加 solvent/reagent 开始，经 reaction heat 与 quench 后完成 evaporation、distillation、
fraction collection、显式 termination 和 final assay；workflow A 在蒸馏前后分别使用 HPLC/GC，workflow B
只在收集馏分后使用 HPLC。每个 case 先运行其物化确定性流程。U05 的完整 agent 主案例固定为生成顺序
第一项，执行前不得按可读结果更换；agent 运行不属于本 C/D 资格批次，待 E02 单独 claim 后执行。

### 无效组合与模块/接口探针

C07 固定 7 个 compile-time mutants：缺失 observation、crystallization 缺 thermal、phase 与
crystallization 冲突所有权、thermal range 使用 L 单位、distillation fraction count 为 0、操作表面缺
terminate、预算低于最短生命周期。它们必须分别以 missing dependency、conflicting owner、unit mismatch、
invalid parameter、lifecycle hole 或 resource impossibility 拒绝，且不得构造环境。运行时负向语义由上述
192 个探针覆盖。

D01/D02 对 reaction、thermal、phase、separation、crystallization、distillation、continuous flow 和
electrochemistry 各运行零输入、合法低/高边界、一个模型卡声明的方向性 pair 和守恒/不变量探针。已有
数值参考 fixture 的模块报告误差与既有 tolerance；没有数值参考的模块必须标记
`conceptual_or_synthetic`，只接受方向性与不变量结论，不得冒充外部效度。

D03 固定 7 条路径：reaction--thermal、reaction--phase--separation、phase--separation、
reaction--crystallization、reaction--distillation、reaction--continuous-flow 和
reaction--electrochemistry。逐条检查 material identity、单位、数量非负、适用的 charge/energy/phase
balance、state identity 与事件传播。D04 在报告中逐模块保留 model-card domain、maturity 和
`virtual_instrument_qualification_only` 边界。

## 测量与通过规则

每个执行 case 记录：构造/兼容判定、物化动作与 schema 判定、事务状态、公开观测、资源 preflight 与
outcome delta、适用守恒、终止/评价、replay verdict、耗时、轨迹记录字节数和全部失败。C08 只作描述：
按组件数、workflow stages 和 trace length 汇总构造成功率、执行时间与记录体积；任何异常、非有限测量
或 case timeout 计为失败，但不设置性能 superiority 主张。

总体 `PASS` 必须同时满足：

- 64/64 参考单元通过，1786/1786 有效配方闭合并精确 replay；
- 192/192 负向探针以预设类别拒绝并保持声明的原子/资源语义；
- 52/52 生成 composition 编译、执行、闭合、资源对账并精确 replay；
- C03 的 8/8 case 无核心运行时补丁，且 composition ID 不属于 15 个参考 task ID；
- 7/7 compile-time mutants 按预设诊断 fail closed；
- 32/32 模块探针和 7/7 接口路径通过各自适用规则；
- public/private leakage、missing receipt 和 unclassified failure 均为 0。

任何一个分母内失败都使总体状态为 `FAILED`。执行器仍须完成所有可安全继续的预设 case，保留全部失败；
不得删除失败、替换结果或改覆盖设计。若发现并修复平台缺陷，受影响的正式批次从第一个 case 重新运行，
旧失败报告保留为历史结果。

## 第一次正式尝试后的 receipt 缺陷处理

2026-08-04 的第一次正式执行完成了全部冻结分母，运行时数值门均通过；随后按冻结说明逐字段抽查时发现，
正式 JSON 只保留了若干聚合布尔值，未完整保存每个 case 的 composition request、资源
preflight/outcome、终止后拒绝、模块误差/容差和分项接口 receipts。该结果因此不进入 current binding，
也不用于将 C01--C08 或 D01--D04 标为完成。旧输出由 Git 历史保留为 receipt-contract 缺陷尝试。

修复只补全已经冻结的测量与 fail-closed 完整性 gate，不改变 64、1786、192、52、8、7、32、7
的分母，不改变 pattern、seed、bounds、workflow 或通过/失败规则。修复提交后，整个联合资格批次从第一个
reference case 开始重新执行；不得复用第一次尝试中的成功子项替代重跑结果。

## 预期输出

- `workstreams/arxiv_v1/reports/first-paper-composition-qualification-v1.json`：完整机器报告、精确分母、
  task/pattern/module/interface 矩阵、case receipts 与全部失败；
- `workstreams/arxiv_v1/reports/first-paper-composition-qualification-v1.md`：面向协作者的简洁汇总；
- 成功生成后在 `configs/current.json` 增加唯一 current binding。

Raw provider responses、临时 trajectory 文件、缓存、重复 manifest 和手工 hash inventory 不进入 Git。
