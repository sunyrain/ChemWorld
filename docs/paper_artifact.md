# Benchmark 论文产物

本页定义 ChemWorld-Bench 若作为论文或公开 benchmark 发布时应包含的 artifact。目标是
让读者能复现核心结论，而不是只看到一次性的 demo。

## 推荐包结构

```text
paper_artifact/
├── README.md
├── environment.md
├── task_cards/
├── baseline_results/
├── trajectories/
├── figures/
├── tables/
└── manifests/
```

## 必备内容

- 环境版本、commit、依赖版本和构建命令。
- 任务列表、任务成熟度、隐藏/公开 split 规则。
- baseline agent 的实现说明和运行命令。
- 每个任务的 metrics、预算、安全约束和失败处理规则。
- trajectory bundle 或可复现实验脚本。
- 已知限制：哪些模块是 proxy，哪些是 lite，哪些经过参考校准。

## 图表建议

- 任务覆盖矩阵：反应、分离、表征、安全、机理、规划等维度。
- agent performance 表：随机、规则 baseline、简单 optimizer、tool-agent。
- 约束失败分析：precondition、safety、cost、selectivity 的分布。
- world model 学习曲线：离线数据量与在线表现。

## 发布原则

论文中的 benchmark claim 必须携带 `world_law_id`、任务版本和 maturity metadata。
如果某个物理模块仍处于 proxy/lite 层级，应在主文或附录中明确说明，避免把教学环境
误读为真实反应预测系统。
