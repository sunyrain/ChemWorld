# 提交包

提交包是 ChemWorld-Bench 的本地评测单位。学生、agent 或 baseline 不直接写排行榜，
而是提交一个文件夹；教师端或维护者再执行 validate、verify、evaluate、summarize。

## 标准结构

```text
submission/
├── README.md
├── dependency_notes.md
├── manifest.json
├── trajectories/
│   └── <agent>_<task>_seed0.jsonl
├── results/
│   └── <agent>_<task>_seed0.json
└── explanations/
    └── <agent>_<task>_seed0.json
```

`explanations/` 对普通优化任务不是强制评分项，但示例包会包含它，便于检查
机制假设、失败分析和下一轮实验理由。

## 一键生成示例包

```bash
chemworld submission example runs/example_submission \
  --task-id reaction-to-purification \
  --agent tool_using_llm_stub \
  --seeds 0
```

该命令会生成：

- `manifest.json`：agent、task、seed、commit、依赖说明文件和可复现命令；
- `trajectories/*.jsonl`：由正式 runner 写出的轨迹；
- `results/*.json`：由正式 evaluator 重算的指标；
- `explanations/*.json`：结构化解释字段；
- `dependency_notes.md`：Python、平台和关键依赖版本。

## 验证

```bash
chemworld submission validate runs/example_submission
chemworld submission summarize runs/example_submission
chemworld verify --constitution \
  --submission runs/example_submission/trajectories/tool_using_llm_stub_reaction-to-purification_seed0.jsonl
```

有效提交包至少需要：

- `manifest.json` 使用 `chemworld-submission-bundle-0.1`；
- `manifest.command` 是非空列表，能够说明如何复现；
- `manifest.seeds` 是非空列表；
- `manifest.dependency_file` 指向包内存在的依赖说明文件；
- `README.md` 存在；
- `trajectories/` 至少有一个 JSONL，且每条记录满足 trajectory schema；
- `results/` 至少有一个 JSON，且包含 `total_score`；
- 每个 trajectory 有同名 result 文件；
- 如果提供 explanation JSON，必须包含 `hypothesis`、`learned_mechanism` 和
  `failure_analysis`。

## 教师端评测顺序

```text
submission bundle
  -> chemworld submission validate
  -> chemworld verify --constitution
  -> chemworld evaluate
  -> chemworld submission summarize
  -> leaderboard aggregation
```

评测端不信任提交者写入的最终分数。`results/*.json` 只是本地复现实验输出，正式榜单应
从 trajectory replay 和 evaluator 重新计算。

## Manifest 字段

`manifest.json` 的核心字段：

| 字段 | 含义 |
| --- | --- |
| `schema_version` | 当前为 `chemworld-submission-bundle-0.1` |
| `agent_name` | agent 或项目名称 |
| `agent_family` | baseline、BO、LLM replay、student project 等 |
| `platform_version` | ChemWorld 包版本 |
| `commit_hash` | 生成包时的 git commit |
| `dependency_file` | 包内依赖说明文件 |
| `command` | 可复现实验命令 |
| `task_id` | 目标 benchmark task |
| `seeds` | 运行 seeds |
| `llm_metadata` | 如适用，记录模型名、日期、temperature、缓存策略和成本 |

## 边界

当前提交包是本地文件夹协议，不是云端防作弊系统。private-eval 仍由教师端或维护者持有
hidden salt、hidden seeds 和最终 runner。公开包只能证明提交格式、轨迹、评测和回放链路
自洽。
