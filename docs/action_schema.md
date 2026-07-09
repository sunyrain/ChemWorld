# Action 与 Recipe 协议

ChemWorld 的 action schema 定义 agent 与虚拟化学世界交互时可以提交的操作。schema
既服务 Gymnasium `env.step(action)`，也服务 recipe、trajectory replay 和提交包校验。

## 基本形状

每个 action 是一个 JSON-like dictionary，至少包含：

```python
{"operation": "heat"}
```

不同 `operation` 会要求不同参数。例如：

```python
{"operation": "add_solvent", "volume_L": 0.03, "solvent": 1}
{"operation": "heat", "temperature_K": 350.0, "duration_s": 1200.0, "stirring_rpm": 800.0}
{"operation": "measure", "instrument": "final_assay"}
```

字段名保持英文，因为它们是稳定 API，不随站点语言变化。

## Recipe 配方序列

Recipe 是 action 的有序列表，可用于 baseline、notebook、回放和教学任务：

```python
recipe = [
    {"operation": "add_solvent", "volume_L": 0.03, "solvent": 1},
    {"operation": "add_reagent", "amount_mol": 0.012},
    {"operation": "heat", "temperature_K": 350.0, "duration_s": 1200.0},
    {"operation": "measure", "instrument": "final_assay"},
]
```

Recipe 本身不保证合法；环境会在 step 时根据任务阶段、物料状态、预算和安全约束返回
`constraint_flags`。

## 约束信号

常见约束包括：

- `precondition_failed`：当前状态不满足操作前置条件。
- `unsafe`：操作触发环境安全边界。
- `unsafe_by_task_limit`：超过该任务声明的安全限制。
- `high_cost`：成本超过任务阈值。
- `low_selectivity`：当前路线选择性不足。
- `constitution_failed`：typed ledger 或物理守恒检查失败。

这些 flags 是 agent 学习的重要反馈，不应被当成普通日志忽略。

## 设计边界

Action schema 关注可交互性和可评测性，不直接等同真实实验室 SOP。真实机器人控制、
设备驱动和安全审批应在更高成熟度的 backend 或 adapter 中处理。
