# Benchmark 论文产物

本页定义 ChemWorld-Bench 若作为论文或公开 benchmark 发布时应包含的 artifact。目标是
让读者能复现核心结论，而不是只看到一次性的 demo。

## 推荐包结构

```text
paper_artifact/
├── README.md
├── environment.md
├── limitations.md
├── release_checklist.md
├── artifact_summary.json
├── tasks/
│   ├── task_cards.json
│   ├── task_contracts.json
│   ├── scenario_cards.json
│   └── world_law.json
├── schemas/
│   ├── action_schema.json
│   ├── recipe_schema.json
│   └── trajectory_schema.json
├── baseline_report/
│   ├── baseline_report.json
│   ├── baseline_results.json
│   ├── baseline_summary_table.json
│   └── baseline_leaderboard.json
├── trajectories/
├── dataset_examples/
│   ├── dataset_card.json
│   └── *_dataset.jsonl
├── manifests/
│   ├── replay_manifest.json
│   ├── release_manifest.json
│   └── release_checklist.json
└── scripts/
    └── reproduce_public_artifact.ps1
```

## 必备内容

- 环境版本、commit、依赖版本和构建命令。
- 任务合同、任务成熟度、隐藏/公开 split 规则和 contract hash。
- baseline agent 的实现说明和运行命令。
- 每个任务的 metrics、预算、安全约束和失败处理规则。
- trajectory 示例、dataset card、replay manifest 和可复现实验脚本。
- 已知限制：哪些模块是 proxy，哪些是 lite，哪些经过参考校准。

## 本地生成

```powershell
chemworld artifact create `
  --output-dir artifact/paper_artifact `
  --tasks reaction-to-assay reaction-to-purification partition-discovery `
  --agents scripted_chemistry `
  --seeds 0
```

该命令会运行所选 baseline，导出 example trajectory，重放验证轨迹，并生成
`manifests/replay_manifest.json`。正式论文 artifact 应把 `--agents` 和 `--seeds`
扩展为冻结的官方 baseline suite。

## 图表建议

- 任务覆盖矩阵：反应、分离、表征、安全、机理、规划等维度。
- agent performance 表：随机、规则 baseline、简单 optimizer、tool-agent。
- 约束失败分析：precondition、safety、cost、selectivity 的分布。
- world model 学习曲线：离线数据量与在线表现。

## 发布原则

论文中的 benchmark claim 必须携带 `world_law_id`、任务版本和 maturity metadata。
如果某个物理模块仍处于 proxy/lite 层级，应在主文或附录中明确说明，避免把教学环境
误读为真实反应预测系统。

`release_checklist.md` 中如果仍有 `required` 项，artifact 只能作为预发布骨架，不能
声称已经满足正式公开榜单发布条件。
