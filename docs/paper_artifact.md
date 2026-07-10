# 论文与发布产物

公开 benchmark 产物必须让第三方从任务合同重建结果，而不是只展示一次 demo。

## 推荐结构

```text
artifact/
├── README.md
├── environment.md
├── limitations.md
├── tasks/                  # task/scenario/world-law contracts
├── schemas/                # action/recipe/trajectory schemas
├── baseline_report/        # per-task raw results and summaries
├── trajectories/           # replayable public examples
├── dataset_examples/       # dataset + provenance card
├── manifests/              # release, replay and solver provenance
└── scripts/                # exact reproduction commands
```

## 生成

```bash
chemworld artifact create --preset core --output-dir runs/core_artifact
chemworld artifact create --preset serious --output-dir runs/serious_artifact
```

`serious` 对应 `chemworld-serious-v1`。正式产物必须使 readiness manifest 显示六个任务全部
`benchmark_ready=true`，并携带与当前合同一致的多 seed 校准、threshold 与 replay 证据。

## 必备证据

- commit、依赖、命令和 solver provenance；
- task/scenario/world-law/mechanism/scoring/observation hashes；
- maturity 与 proxy policy；
- 每个 task 的原始 seed 结果、汇总统计和失败分析；
- replay manifest、trajectory digest 和 verified result；
- 数据集 provenance card；
- 适用范围与限制。

LLM/Codex 结果只保存模型元数据、prompt 摘要、动作、验证结果、观测摘要和简短决策依据，
不保存完整 chain-of-thought。论文引用必须同时给出 task id、seed suite、agent、commit 与
dependency/provenance manifest。
