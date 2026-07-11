# Backend 后端

Backend 把稳定的 task/action/observation 语义连接到具体物理实现。每个正式 provider 必须声明
model ID、角色、输入输出单位、适用域、诊断、失败策略、provenance 和目标 operation。

## 当前执行模型

World Law v0.4 使用单一 provider registry。runtime route、diagnostic provider 和 reference-only
模型分开记录：

- runtime provider 改变状态；
- diagnostic provider只产生可审计证据，不能抬高任务成熟度；
- reference provider 用于独立验证，不可由正式 operation 隐式执行；
- 当前 registry 不含 `runtime_fallback`。

RMG-Py、IDAES、PhasePy、teqp 或其它专业软件可以作为校准与约定边界，但不是默认安装的隐式
替代路径。引入外部 backend 必须保持公共合同，公开版本与适用域，并通过 operation-to-model
可达性和 replay 审计。

当前 backend 的目标是提供可控、可复现、具有物理约束的 agent 训练与评测环境，不是复制商业
流程模拟器。运行 `python scripts/audit_model_reachability.py --strict-alignment` 查看任务声明与
实际 provider route，运行 `python scripts/audit_vnext_runtime_integration.py` 验证真实事务调用。
