# WF-00 合同与集成边界

目标：冻结所有并行团队共同使用的最小协议，不实现具体物理模型。

独占范围：maturity/evidence schema、provider protocol、adapter manifest schema、模型可达性审计。

禁止范围：不得改变 v0.3 状态转移、task score 或正式轨迹。

交付：

- model input/output、units、domain check、diagnostics、failure 和 provenance protocol；
- operation → service → kernel → model 可达性报告格式；
- 每个模块可独立使用的 fixture/stub；
- shared-file ownership 检查；
- 交给 `WF-110` 的 adapter manifest schema。

验收：`WF-10`–`WF-100` 团队只依赖这里的 protocol 就能运行模块测试；protocol 冻结后，兼容性修改必须进入新的开发周期。

## 当前认领：WF-00 runtime contracts

状态：`active`。本轮只新增只读合同与审计，不改变 v0.3 的状态转移、observation 或 scoring。

首批交付：

- `ModelProviderContract` 与 `PhysicalModelProvider`，统一 input/output、units、适用域、diagnostic、failure 和 provenance；
- `ContractModelProviderStub`，让模块团队在 runtime 集成前验证合同形状和失败路径；
- 每个 operation 的 service/kernel/model route；无物理模型的 ledger operation 必须写明原因；
- task maturity 声明与实际可达模型的差异报告；
- reference-only provider 与 runtime provider 的机器隔离检查。

运行：

```powershell
.\.venv\Scripts\python.exe scripts\audit_model_reachability.py
```

默认命令要求结构合同和共享路径所有权完整，并将现有声明漂移作为 warning 输出。`--strict-alignment` 只能在后续 WF-110 清理 task maturity 并重冻结受影响任务后升级为强制门禁。本地发布门禁采用默认的非严格模式。

模块团队交接 adapter 时使用 `ModelAdapterManifest`。最小字段包括：

```json
{
  "schema_version": "chemworld-model-adapter-manifest-0.1",
  "adapter_id": "wf-20-example-adapter",
  "adapter_version": "0.1",
  "owner_workstream": "wf-20-instruments",
  "provider_contract": "由 ModelProviderContract.to_dict() 生成",
  "owned_paths": ["模块 claim 内的实现文件"],
  "integration_operations": ["measure"],
  "target_world_law": "chemworld-physical-chemistry-vnext",
  "status": "proposal",
  "replaces_model_ids": []
}
```

manifest hash 绑定所有字段，读取时会拒绝手工篡改。共享 runtime、task、World Law、golden 与 benchmark evidence 只能由 `wf-00-*`、`wf-110-*` 或 `release-*` active claim 认领。
