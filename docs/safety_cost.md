# 安全与成本

安全和成本是 ChemWorld 任务评分的一部分，不是事后日志。Agent 必须学会在性能、风险
和预算之间做取舍。

## 安全信号

常见字段：

- `unsafe`
- `unsafe_by_task_limit`
- `degradation_detected`
- `precondition_failed`

安全 flag 应进入 reward、score report 和 failure analysis。

## 成本信号

成本可来自试剂、溶剂、催化剂、仪器、时间、温度和操作次数。不同任务可以采用不同权重，
但必须在任务卡中声明。

## 设计原则

高分路线不应只追求目标指标。若某路线通过过高风险、过高成本或大量无效操作获得表面
高产率，应在 benchmark 中被惩罚。
