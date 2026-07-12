# 打包并提交结果

ChemWorld 不接收一个手写分数，而是接收一个可以复现的文件夹。评测端会检查 manifest、回放轨迹，
再重新计算结果。

## 提交包里有什么

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

| 内容 | 作用 |
| --- | --- |
| `manifest.json` | 说明 Agent、任务、seed、源码版本和复现命令 |
| `trajectories/` | 保存每一步 Action 与公开观测，是评分的事实来源 |
| `results/` | 本地 evaluator 生成的结果，便于自查 |
| `explanations/` | 可选的假设、失败分析与下一轮建议 |
| `dependency_notes.md` | 记录 Python、平台和关键依赖 |

## 生成一个示例包

```bash
chemworld submission example runs/example_submission \
  --task-id reaction-to-purification \
  --agent tool_using_llm_stub \
  --seeds 0
```

生成后先浏览 `README.md` 与 `manifest.json`，确认命令、task ID 和 seeds 与实际运行一致。

## 在提交前自检

```bash
chemworld submission validate runs/example_submission
chemworld submission summarize runs/example_submission
chemworld verify --constitution \
  --submission runs/example_submission/trajectories/tool_using_llm_stub_reaction-to-purification_seed0.jsonl
```

验证器会检查：

- manifest 使用 `chemworld-submission-bundle-0.1`，并给出可复现命令与非空 seeds；
- `README.md`、依赖说明、trajectory 和对应 result 都存在；
- 每条 trajectory 满足 schema，并能通过 constitution 与 replay；
- result 含有 `total_score`；
- 如果提交 explanation，它包含 `hypothesis`、`learned_mechanism` 和 `failure_analysis`。

## 评测端如何处理

```text
接收文件夹
  → validate 结构与 manifest
  → verify 轨迹和状态守恒
  → replay 并重新 evaluate
  → summarize 逐任务结果
  → 汇总到 leaderboard 或课程报告
```

`results/*.json` 不是可信分数来源。正式结果始终从 trajectory replay 重新计算。

## Manifest 核心字段

| 字段 | 含义 |
| --- | --- |
| `schema_version` | 当前提交协议版本 |
| `agent_name` / `agent_family` | 方法名称与家族 |
| `platform_version` / `commit_hash` | 生成结果的软件身份 |
| `dependency_file` | 包内依赖说明 |
| `command` | 可复现实验命令 |
| `task_id` / `seeds` | 任务与世界实例 |
| `llm_metadata` | 如适用，记录模型、参数、日期、缓存与费用 |

!!! note "本地提交包的边界"
    这是可复现文件协议，不是云端防作弊系统。Private eval 的 salt、seeds 和最终 runner 由评测端
    持有；公开包只能证明格式、轨迹与回放链自洽。

需要模拟教师端完整流程时，继续阅读[运行本地评测机](local_eval_machine.md)。
