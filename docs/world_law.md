# 世界律与版本

世界律是所有任务共享的底层规则：物质怎样流动、反应怎样推进、设备怎样约束操作、仪器能看到什么，
以及风险、成本和评分如何计算。当前版本是：

```text
chemworld-physical-chemistry-v0.4
```

任务是同一世界律上的能力切片，不会为单个任务暗中更换物理规则。世界律 ID 会写入 task
contract、scenario、trajectory 与 replay；改变状态转移、操作成本、观测可见性、评分或正式
provider 路由时必须提升版本，旧轨迹不会被静默解释为新版本结果。

## v0.4 改变了什么

v0.4 将八个经过合同与证据审查的 provider 接入统一运行时：

- `mix`、`wash`：稳定性门控、活度修正、显式夹带与逐组分守恒的 LLE；
- `dry`：有限容量竞争吸附与 spent-sorbent 物料账；
- `concentrate`：受加热功率、真空、冷凝回收与目标回收率约束的差分蒸发；
- `transfer`：源容器 heel、管线 hold-up 与交付物流的显式账本；
- `distill`：泡点、设备容量、热负荷、VLE/Fenske 与可用 FUG 诊断共同约束的蒸馏；
- reaction、spectroscopy、crystallization 的三个诊断 provider 只提供证据，不会抬高运行时
  成熟度。

上述操作每项只有一个声明的正式 runtime route。旧 `chemworld_separation_proxy`、旧 LLE 双路由
和旧 distillation route 已从 provider registry 移除；底层解析或参考函数仍可作为新 provider
的验证组件，但不能被 runtime 隐式调用。

## 为什么世界律必须可审计

世界律共同冻结：ontology、compiled mechanism、typed ledgers、transaction rollback、operation
schema、instrument observation、cost/risk、maturity、provider provenance 与 replay policy。
下游操作产生的 spent sorbent、condensate、vent、source heel 和 line hold-up 都保存在 typed phase
ledger 中，不以“损失系数”隐藏物料去向。

执行 `python scripts/audit_vnext_runtime_integration.py` 可同时验证 provider route、任务声明和真实
事务执行。系统结构见[架构](architecture.md)，证据含义见[模型成熟度](model_maturity.md)。
