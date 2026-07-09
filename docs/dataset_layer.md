# 数据集层

ChemWorld 的数据集层把交互轨迹、任务合同、agent-facing 视图、agent 行为摘要和 replay metadata 整理成可复现的研究产物。它不是单纯的日志目录，而是连接 offline analysis、leaderboard 审核、教学回放和论文 artifact 的公共接口。

## 当前数据对象

| 对象 | 用途 |
| --- | --- |
| trajectory JSONL | 每一步 action、observation、reward、termination、info、contract hash 和 replay metadata |
| agent view | 每一步公开给 agent 的 `rl_vector`、`tool_json` 和 `lab_report` 视图 |
| agent trace | agent 的 prompt 摘要、selected action、validator result、observation summary、memory note 和 hypothesis note |
| dataset export | 把 trajectory 转成 JSONL copy 或 Parquet/表格友好的 flattened records |
| dataset card | 记录 task、seeds、world law version、env version、hash、privacy status 和 replay verification |

## 导出命令

```bash
chemworld datasets export \
  --submission runs/example_submission/trajectories/tool_stub.jsonl \
  --format jsonl \
  --output runs/example_dataset.jsonl

chemworld datasets export \
  --submission runs/example_submission/trajectories/tool_stub.jsonl \
  --format parquet \
  --output runs/example_dataset.parquet

chemworld datasets card --dataset runs/example_dataset.jsonl
```

Parquet 导出需要本地安装 `pyarrow` 或 `fastparquet`。如果只需要审阅和回放，JSONL 足够；如果要做批量统计、offline model 训练或表格分析，优先使用 Parquet。

## Agent Trace 合同

trajectory 原始记录保留完整 `agent_trace` 列表。flattened dataset 额外提供这些列，便于表格分析：

| 字段 | 含义 |
| --- | --- |
| `agent_trace_step_count` | 当前记录中累计的 agent trace 条数 |
| `agent_trace_prompt_summary` | 最新一步 prompt/public context 摘要 |
| `agent_trace_selected_action` | 最新一步 agent 选择的 action |
| `agent_trace_validation_result` | validator、constraint flag、precondition 和错误信息摘要 |
| `agent_trace_observation_summary` | 最新一步 public observation/reward/leaderboard 摘要 |
| `agent_trace_reasoning_summary` | agent 自述的简短策略理由，不保存完整 chain-of-thought |
| `agent_trace_hypothesis_note` | agent 当前机制假设或下一轮解释线索 |
| `agent_trace_memory_note` | agent 从历史 public observation 形成的短记忆 |

这些字段只来自 public observation、task prompt、validator result 和 agent 自己的公开行为摘要，不允许读取 hidden ledgers、rate constants、private scenario 参数或 debug truth。

## 示例

运行：

```bash
python examples/demo_dataset_agent_trace_export.py
```

该示例会：

1. 使用 `ToolUsingLLMStubAgent` 跑通 `reaction-to-assay`；
2. 写出 trajectory JSONL；
3. 导出 dataset JSONL；
4. 如果本地有 Parquet backend，则导出 Parquet；
5. 打印最终 lab report 和 agent trace 摘要字段。

## Dataset Card

`dataset_card()` 会扫描数据集并输出：

- task ids、seeds、env version、world law version；
- task/runtime/mechanism/scoring/observation contract hash；
- replay verification summary；
- agent manifest summary；
- privacy/anonymization status；
- known limitations。

公开发布数据集前，应检查 dataset card 中的 privacy 字段，尤其是 human pilot trajectory、explanation 文本和 agent metadata。

## 质量门槛

- 每条 trajectory 必须通过 schema validation。
- 每个公开 dataset 应能追溯到 task id、scenario id、mechanism hash、seed、commit hash 和生成命令。
- `agent_view` 与 `agent_trace` 必须是 public-facing；不能泄露 hidden species id、hidden amounts、rate constants 或 private-eval 参数。
- replay verification 不通过的数据集不能作为 benchmark artifact 发布。
