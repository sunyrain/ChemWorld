# Experiment 1 Legacy and Dependency Index

状态：**只读分类索引；本轮不移动、不删除 legacy 资产。**

“文件名包含 `WORK_II`”不等于“不再使用”。当前 EC v1.0.1 垂直切片明确复用了历史实现和冻结 source assets，因此必须按真实引用分类。

## CURRENT_DEPENDENCY

以下旧命名资产仍被 EC v1.0.1 的合同或运行链直接使用，不能移动或改名：

### 配置与 source assets

- `configs/benchmark/work_ii_campaign_pilot.json`：机器合同绑定的 campaign config；
- `workstreams/flagship_tasks/reports/work-ii-electrochemical-matched-prior-qualification-20260811.json`：parametric reference source；
- `workstreams/flagship_tasks/reports/work-ii-mechanism-oracle-electrochemical-classified-v0.2-20260811.json`：parametric noise source。

### Python evaluator / runner 依赖

- `src/chemworld/eval/work_ii_ae_prior_qualification_v02.py`；
- `src/chemworld/eval/work_ii_electrochemical_matched_prior_qualification.py`；
- `src/chemworld/eval/work_ii_structural_candidate_qualification.py`；
- `scripts/run_work_ii_mechanism_oracle_qualification.py`；
- `scripts/run_work_ii_q1_response_surface.py`；
- `scripts/run_work_ii_structural_candidate_qualification.py`。

这些依赖的名称可以在未来版本中逐步解除，但不能在已完成的 v1.0.1 evidence chain 中原地替换。

## CURRENT_PORTFOLIO_NAVIGATION

- `workstreams/flagship_tasks/WORK_II_TODOLIST.md`：仍管理 Work II/Experiment 1 的组合级执行状态；
- `workstreams/flagship_tasks/WORK_II_EXPERIMENT_MATRIX.md`：保留更广的 Paper 2 问题与历史矩阵，并已把当前 Experiment 1 执行语义让位给 v1.0.1 最小规范。

它们不是 EC 机器合同，也不能覆盖当前 Experiment 1 authority map。

## HISTORICAL_REPRODUCTION

其余旧 `WORK_II_*` notes、configs、reports 和 run namespaces 默认属于历史设计、复现、bug/recovery 或论文 provenance。除非依赖审计证明安全，本轮保持原路径与原文，不批量增加 banner，也不重写其中的历史原则。

## DEAD/UNREFERENCED_CANDIDATE

本轮不宣称任何资产已经可以删除。仅凭 `rg` 未发现引用不足以证明 Python 动态入口、外部论文链接或未跟踪 evidence 不再依赖它。删除候选必须在后续独立任务中具备：

1. 静态引用与 import 审计；
2. CLI/动态加载审计；
3. 论文与报告链接审计；
4. 历史 replay 验证；
5. 人工批准。

## 后续迁移规则

- 优先添加 archive index、deprecation notice 或 redirect/stub；
- 已被机器合同绑定的路径永不在原版本中迁移；
- 只有新版本执行链完成去耦后，旧实现才可降级为纯 historical reproduction；
- 大规模 legacy migration 必须等 EC 三个 locus 全部通过并经过单独审阅后再决定。
