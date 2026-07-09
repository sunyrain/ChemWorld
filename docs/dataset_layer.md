# 数据集层

ChemWorld 的数据集层用于把交互轨迹、任务元数据和评测结果整理成可复现的研究产物。
它不是单纯的日志目录，而是连接 agent 训练、离线分析、leaderboard 和论文 artifact 的
公共接口。

## 数据对象

- `trajectory`：一次 episode 的完整 step 序列，包括 action、observation、reward、
  termination、truncation 和 `info`。
- `task_info`：任务注册表输出的任务卡信息，包括 `task_id`、`world_law_id`、
  `maturity`、预算、指标和约束。
- `scenario`：环境初始化时采样出的隐藏条件和可见条件。
- `record`：运行时的 typed ledger、transaction record、instrument record 和
  replay metadata。
- `score`：评测器输出的 task-specific metrics、constraint flags、cost 和 safety
  汇总。

## 目录约定

```text
artifacts/
├── trajectories/
├── scores/
├── task_cards/
├── reports/
└── manifests/
```

`manifest` 应记录代码版本、任务版本、seed、配置、依赖版本和生成时间。公开数据集应
优先发布 manifest 和压缩后的 trajectory bundle，而不是散落的临时日志。

## 与 Minari 风格的关系

长期目标是接近 Minari 一类离线 RL 数据集的可复用程度：trajectory 可被重复加载，
observation/action schema 可被机器检查，episode metadata 可被索引，且 evaluation
split 与 training split 明确隔离。

当前阶段仍是轻量实现：先保证轨迹字段稳定、replay 可核验、任务成熟度可追踪，再引入
更重的数据集打包工具。

## 质量闸门

- 每条轨迹必须带 `task_id`、`world_law_id`、`seed` 和 `task_maturity`。
- 每个数据包必须能追溯到生成它的命令和 git commit。
- 公开 benchmark claim 必须说明使用的是哪一批任务、哪一组 seeds、哪一个 scoring
  protocol。
- 隐藏评测数据不得泄露 hidden scenario、oracle intermediate state 或最终答案。
