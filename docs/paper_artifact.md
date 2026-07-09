# Benchmark 论文产物

本页定义 ChemWorld 作为论文或公开 benchmark 发布时应包含的 artifact。目标是让读者能够复现核心结论，而不是只能看到一次性的 demo。

## 推荐目录

```text
paper_artifact/
├── README.md
├── environment.md
├── limitations.md
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
├── manifests/
│   ├── replay_manifest.json
│   ├── release_manifest.json
│   ├── solver_provenance_manifest.json
│   └── release_checklist.json
└── scripts/
    └── reproduce_public_artifact.ps1
```

## AAAI Preset Artifact

AAAI 投稿 preset 使用 6 个冻结任务、官方 baseline 集合和 solver/provenance manifest：

```powershell
chemworld artifact create --preset aaai --output-dir runs/aaai_2027/artifact
python scripts/run_aaai_experiments.py --smoke
```

AAAI artifact 额外要求：

- `manifests/solver_provenance_manifest.json`：记录 commit、依赖版本、solver tolerance、private salt policy 和任务 maturity；
- `baseline_report/`：按 6 个任务分别聚合，不合并成一个误导性总榜；
- `trajectories/`：包含 replay verifier 可重放的 public trajectory；
- `agent_trace`：Codex/LLM 轨迹只保存 reasoning summary 和 decision evidence，不保存完整 chain-of-thought；
- `task_cards`、`scenario_cards`、`mechanism_hash` 和 `scoring_contract_hash` 必须随结果一起发布。

论文正文引用结果时应同时给出 `task_id + seed suite + agent + commit hash + dependency/provenance manifest`。

## 必备内容

- 环境版本、commit、依赖版本和构建命令；
- 任务合同、任务成熟度、公开/隐藏 split 规则和 contract hash；
- baseline agent 的实现说明和运行命令；
- 每个任务的 metrics、预算、安全约束和失败处理规则；
- trajectory 示例、dataset card、replay manifest 和可复现实验脚本；
- 已知限制：哪些模块是 proxy，哪些是 lite，哪些经过 reference validation。

## 本地生成

```powershell
chemworld artifact create `
  --output-dir runs/paper_artifact `
  --tasks reaction-to-assay reaction-to-purification partition-discovery `
  --agents scripted_chemistry `
  --seeds 0
```

正式论文 artifact 应把 `--agents` 和 `--seeds` 扩展为冻结的官方 baseline suite。

## 发布原则

论文中的 benchmark claim 必须携带 `world_law_id`、任务版本和 maturity metadata。如果某个物理模块仍处于 proxy/lite 层级，应在正文或附录中明确说明，避免把虚拟训练环境误读为真实反应预测系统。
