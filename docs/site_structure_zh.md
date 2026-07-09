# 站点层级规划

当前文档已经通过 `mkdocs.yml` 分组改善了阅读入口，但文件仍集中在 `docs/`
根目录。短期不建议立刻批量搬迁，因为仓库中仍有未提交文档改动；更稳的路线是先固定
导航信息架构，再分批迁移文件路径。

## 目标结构

```text
docs/
├── index.md
├── en/
│   └── index.md
├── status/
│   ├── current_progress.md
│   ├── roadmap.md
│   ├── release_checklist.md
│   └── site_audit_zh.md
├── concepts/
│   ├── chemworld_overview_zh.md
│   ├── architecture.md
│   ├── technical_architecture_zh.md
│   ├── world_law.md
│   ├── physchem_core_design.md
│   └── world_model_learning.md
├── benchmark/
│   ├── tasks/
│   │   ├── task_taxonomy.md
│   │   ├── tasks.md
│   │   ├── task_cards.md
│   │   └── scenario_generation.md
│   ├── runtime/
│   │   ├── campaign_model.md
│   │   ├── operations.md
│   │   ├── wrappers.md
│   │   └── backends.md
│   ├── schemas/
│   │   ├── action_schema.md
│   │   └── mechanism_schema.md
│   ├── instruments/
│   │   ├── instrument_contracts.md
│   │   └── spectroscopy.md
│   └── protocol/
│       ├── benchmark_protocol.md
│       ├── submission.md
│       └── safety_cost.md
├── evaluation/
│   ├── baseline_reference.md
│   ├── dataset_layer.md
│   ├── local_eval_machine.md
│   ├── leaderboard_project_blueprint.md
│   ├── paper_artifact.md
│   └── ethics_and_data.md
├── tutorials/
│   ├── tutorial_curriculum_zh.md
│   ├── demos.md
│   ├── api_reference.md
│   └── reaction_separation_tasks.md
├── audits/
│   ├── environment_self_consistency_audit_zh.md
│   ├── physchem_maturity_audit.md
│   ├── sota_agent_environment_gap_audit.md
│   ├── codex55_medium_behavior_report.md
│   └── code_review_audit.md
└── development/
    ├── project_management.md
    ├── reference_repos.md
    ├── professional_todo.md
    └── professional_deepening_todo.md
```

## 迁移顺序

1. 先保持现有文件路径，用 `mkdocs.yml` 固定中文导航、搜索语言和中英文入口。
2. 在一次独立 PR 中移动 `status/`、`concepts/`、`development/` 三组低耦合文档。
3. 再移动 `benchmark/`、`evaluation/`、`tutorials/`、`audits/`，同步更新所有相对链接。
4. 每一批迁移后运行 `python -m mkdocs build --strict`，确保没有断链。
5. 如果站点已经对外发布，再引入 `mkdocs-redirects` 或静态跳转页保留旧 URL。

## 命名规则

- 中文页面文件名继续使用英文 slug，保证 URL 稳定且便于引用。
- 一级目录按读者任务划分，而不是按作者或历史来源划分。
- `en/` 先保留英文首页，后续若要完整双语化，可逐页扩展为镜像结构。
- 评测合同、任务卡、schema 和提交协议属于稳定 public contract，应优先避免频繁改 URL。
