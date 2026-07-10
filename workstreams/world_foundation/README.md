# 世界基座并行工作包

本目录把 `world_foundation_todolist.md` 拆成可独立认领的模块。目标是让多人并行实现物理模型，
而不是多人同时编辑共享 registry 和 task contract。

认领任一模块前，必须先按 [`claims/README.md`](../../claims/README.md) 创建并推送 active claim。
模块编号不是 claim；远端 claim 文件才是有效所有权记录。

## 并行规则

1. `00` 集成负责人先冻结输入/输出、model card、diagnostic 和 provider protocol。
2. `10`–`100` 模块团队只修改自己文件中列出的 owned paths；通过直接模块导入和 fixture 验证。
3. 模块团队不得修改 `src/chemworld/tasks.py`、`world/parameters.py`、runtime registry/dispatch、
   `physchem/__init__.py`、golden trajectory、正式 docs 或 benchmark evidence。
4. 每个模块提交独立 adapter proposal；`110` 集成负责人统一接入 runtime、提升 World Law 并重冻。
5. 跨模块依赖只允许经过 `00` 冻结的 protocol；不得直接导入另一团队的内部类。
6. 一个模块未完成时，其他模块使用 contract fixture/stub，不等待其实现。

## 模块目录

| ID | 模块 | 可立即并行 | 主要解锁 |
| --- | --- | --- | --- |
| 00 | [合同与集成边界](00_contracts.md) | 首先短周期冻结 | 全部团队 |
| 10 | [反应动力学与反应器](10_reaction_core.md) | 是 | 14 个反应声明任务 |
| 20 | [仪器与谱图](20_instruments.md) | 是 | 全部 15 个任务 |
| 30 | [Dry/Concentrate/Transfer](30_downstream.md) | 是 | 3 个 proxy 任务 |
| 40 | [相平衡与萃取](40_phase_equilibrium.md) | 是 | partition/purification |
| 50 | [结晶](50_crystallization.md) | 是 | crystallization |
| 60 | [蒸馏](60_distillation.md) | 是 | distillation |
| 70 | [连续流](70_flow.md) | 是 | flow |
| 80 | [电化学](80_electrochemistry.md) | 是 | electrochemical |
| 90 | [水相与平衡化学](90_equilibrium.md) | 是 | equilibrium |
| 100 | [物性、设备、安全与成本](100_foundation_services.md) | 是 | 所有工艺模块 |
| 110 | [Runtime 接入与下一版冻结](110_release_integration.md) | 模块交付后 | World Law vNext |

## 15 个任务的集成矩阵

`I` 表示任务集成时必须使用该模块；模块开发阶段不允许直接修改该任务合同。

| Task | 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 | 90 | 100 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| reaction-optimization-standard | I | I |  |  |  |  |  |  |  | I |
| reaction-safety-constrained | I | I |  |  |  |  |  |  |  | I |
| reaction-mechanism-explanation | I | I |  |  |  |  |  |  |  | I |
| reaction-to-assay | I | I |  |  |  |  |  |  |  | I |
| reaction-to-purification | I | I | I | I |  |  |  |  |  | I |
| partition-discovery |  | I |  | I |  |  |  |  |  | I |
| purity-yield-tradeoff | I | I | I | I |  |  |  |  |  | I |
| public-private-generalization | I | I |  |  |  |  |  |  |  | I |
| low-budget-characterization | I | I |  |  |  |  |  |  |  | I |
| tool-agent-planning | I | I | I | I |  |  |  |  |  | I |
| reaction-to-crystallization | I | I |  |  | I |  |  |  |  | I |
| reaction-to-distillation | I | I |  |  |  | I |  |  |  | I |
| flow-reaction-optimization | I | I |  |  |  |  | I |  |  | I |
| electrochemical-conversion | I | I |  |  |  |  |  | I |  | I |
| equilibrium-characterization |  | I |  |  |  |  |  |  | I | I |

## 统一交付格式

每个模块 PR 必须包含：model card、typed API、适用域、失败模式、守恒/极限测试、独立参考对照、
性能与确定性报告、adapter proposal，以及“未修改共享文件”的确认。达到这些条件只表示模块可
进入集成审查，不会自动改变任务成熟度。
