# Experiment 1 Authority Map

## 原则

Experiment 1 需要一个单一**权威入口**，但不把科学语义、机器输入和实验结果强行合并成一个文件。不同层各自回答不同问题，并通过路径与 digest 绑定。

## 权威层级

| 问题 | 当前权威源 | 权限边界 |
| --- | --- | --- |
| 如何协作、开发和冻结 | `AGENTS.md` | 仓库级工作规则，不替代科学规范 |
| Experiment 1 当前入口和状态 | `workstreams/flagship_tasks/experiment_1/README.md` | 导航和状态，不新增 Gate |
| qualification 的科学执行语义 | `workstreams/flagship_tasks/EXPERIMENT_1_MINIMUM_EXECUTION_SPEC_V1_0_1.md` | 冻结用于 development qualification；不是 benchmark release |
| 体系级问题、单位和停止规则 | `workstreams/flagship_tasks/experiment_1/systems/<SYSTEM>/` | 仅覆盖文件声明的体系与版本 |
| 精确机器输入 | `configs/benchmark/experiment_1_*` | 路径、digest、World、预算、阈值或 fail-closed audit 的机器合同 |
| 已发生的 raw evidence | 服务器 `runs/development/experiment-1-*` | 结果事实；不是设计授权，不纳入 Git |
| 体系级可读结果 | `workstreams/flagship_tasks/experiment_1/results/<SYSTEM>/` | 对应 system registry 的可读解释 |
| 105-unit 结果事实 | `workstreams/flagship_tasks/experiment_1/results/EXPERIMENT_1_QUALIFICATION_REGISTRY.json` | 当前七体系机器总账；结果不等于执行授权 |
| Participant 候选边界 | `workstreams/flagship_tasks/experiment_1/results/EXPERIMENT_1_PARTICIPANT_READINESS.md` | 只定义候选和 blocker；不授权运行 |
| 七体系设计背景 | `workstreams/flagship_tasks/experiment_1/guidance/` | 非 normative；不能直接授权执行 |
| 旧 Work II 文档、代码和结果 | `WORK_II_*`、旧 configs/reports/modules | provenance、复现或当前显式依赖；不能推导新的 Experiment 1 设计 |

## 冲突处理

1. 当前结果事实以绑定的 registry 和 evidence 为准，可读报告必须与其一致；
2. 精确执行参数以对应机器合同为准，但机器合同不能越过执行规范授权新的科学范围；
3. guidance 或旧 Work II 内容与当前执行规范冲突时，不进入当前设计；
4. 历史结果不能自动升级为当前 qualification PASS；
5. “五个 Worlds”不是五个噪声 seeds，“15/15 完成”也不是“15/15 qualified”。

## 冻结文件规则

EC v1.0.1 合同绑定以下现有路径和 SHA-256：

- `workstreams/flagship_tasks/EXPERIMENT_1_MINIMUM_EXECUTION_SPEC_V1_0_1.md`；
- `workstreams/flagship_tasks/EXPERIMENT_1_EC_QUALIFICATION_V1_0_1_NOTE.md`；
- `configs/benchmark/work_ii_campaign_pilot.json`；
- 两份合同列明的历史 source reports。

这些文件不能为了目录整齐而移动、重命名或静默修改。未来修订必须使用新版本文件、新合同和新的 evidence namespace，不能覆盖 v1.0.1。

## 尚未冻结的范围

当前没有一个已批准的全七体系 benchmark release manifest。现有五份设计文档仍是 guidance。
P/D 的正式 five-World private truth、完整 prior generator 与目标 structural private family 尚未
冻结；所有体系的 Participant 模型、样本量、正式执行 manifest 和发布版本也仍未授权。
