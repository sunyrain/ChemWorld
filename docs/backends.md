# 计算后端与 Provider

任务和 Action 定义“要做什么”，Provider 负责“这一步怎样改变世界”。这种分离让公共接口保持稳定，
同时允许物理实现逐步升级并留下明确来源。

## Provider 角色

| 角色 | 是否改变运行时状态 | 用途 |
| --- | --- | --- |
| runtime provider | 是 | 正式执行 Operation |
| diagnostic provider | 否 | 可用于独立审计，不提高任务成熟度；当前正式 registry 未注册此角色。 |
| reference provider | 否 | 与独立实现或专业软件做局部对照 |

World Law v0.4 使用单一 provider registry。当前有 20 个 runtime/reference provider、28 条完整
Operation 路由，不提供静默 `runtime_fallback`；一个 Operation 可以显式组合多个必需模型，例如
连续流同时依赖反应网络与几何 PFR，但同一模型不会通过别名或旧 proxy 重复执行。

每个 Provider 应说明 model ID、输入输出单位、适用域、失败策略、诊断、provenance 与目标 Operation。
RMG-Py、IDAES、PhasePy、teqp 等专业软件可以作为参考或校准边界，但不会在默认安装中被隐式调用。

## 理解实际路由

每张任务卡公开 task contract hash、整体成熟度和 `proxy_allowed`；轨迹进一步记录正式 provider 与
机制 provenance。用户不需要运行维护者审计脚本来判断当前状态：backend v0.5 candidate 的固定结论
是 15 个任务均为 `reference_validated` 且 `proxy_allowed=false`。它服务于可控、可复现的 Agent
训练与评测，不等同商业流程模拟器。

`v0.5` 是对当前 v0.4 World Law 实现、任务
合同和证据字节的候选冻结标签；它不提升 World Law ID，也不包含算法排名。任何状态转移、观测、
评分或正式 provider 变化都会使合同哈希失配并阻止复用该冻结。
