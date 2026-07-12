# 计算后端与 Provider

任务和 Action 定义“要做什么”，Provider 负责“这一步怎样改变世界”。这种分离让公共接口保持稳定，
同时允许物理实现逐步升级并留下明确来源。

## 三种 Provider 角色

| 角色 | 是否改变运行时状态 | 用途 |
| --- | --- | --- |
| runtime provider | 是 | 正式执行 Operation |
| diagnostic provider | 否 | 生成可审计诊断，不提高任务成熟度 |
| reference provider | 否 | 与独立实现或专业软件做局部对照 |

World Law v0.4 使用单一 provider registry，每个正式 Operation 只有一个声明的 runtime route，
当前 registry 不提供静默 `runtime_fallback`。

每个 Provider 应说明 model ID、输入输出单位、适用域、失败策略、诊断、provenance 与目标 Operation。
RMG-Py、IDAES、PhasePy、teqp 等专业软件可以作为参考或校准边界，但不会在默认安装中被隐式调用。

## 查看实际路由

```bash
python scripts/audit_model_reachability.py --strict-alignment
python scripts/audit_vnext_runtime_integration.py
```

第一条检查任务声明能否到达实际 Provider，第二条确认模型路径真的进入运行时事务。当前后端服务于
可控、可复现的 Agent 训练与评测，不等同商业流程模拟器。
