# 物理化学成熟度审计

本页用于说明 ChemWorld 中各物理化学模块的可信度边界。它的核心价值是防止把 proxy
环境误表述为真实预测系统。

## 成熟度层级

- `proxy`：用于交互语义和教学，参数或关系主要是可控近似。
- `lite`：有基本物理约束和合理趋势，但未经过系统参考校准。
- `reference-validated`：针对明确范围做过文献、实验或外部工具校准。
- `professional-candidate`：具备进入更专业工程/科研验证的候选质量，但仍需限定适用域。

## 当前审计

当前 ChemWorld 的优势在于统一世界律、交互协议、任务注册、ledger 和 evaluation
contract。物理准确性仍处于渐进提升阶段。

已相对成形的部分：

- action/operation 语义；
- phase 与 separation 的交互结构；
- safety/cost flags；
- virtual spectroscopy 接口；
- typed ledger 和 replay。

仍需深化的部分：

- 真实物性；
- 反应动力学；
- 副反应和降解；
- 相平衡；
- 单元操作；
- 仪器噪声校准。

## 策略

任何任务、图表或论文 claim 都必须携带 maturity。禁止只展示高分而不说明该任务处于
proxy、lite 还是 reference-validated。

## 机器可读元数据

任务卡应包含：

```yaml
maturity: lite
world_law_id: chemworld-physical-chemistry
validated_against: null
known_limits:
  - proxy kinetics
  - simplified phase behavior
```

## 参考阅读说明

RMG-Py、IDAES、teqp、thermopack 等项目可作为长期校准参考，但不应让当前轻量环境突然
变成重依赖。参考 backend 应分层接入。

## 立即修正

- 文档和站点中文化。
- 明确 release checklist 中的 maturity gate。
- 在 task cards 中持续标注 maturity。
- 把“真实预测”类表述替换为“虚拟交互 / benchmark / research environment”。
