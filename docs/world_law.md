# 世界律

世界律定义 ChemWorld 中物质、相、反应、设备、操作、测量、安全、成本和评分必须共同遵守
的规则。任务是世界律上的不同切片，不是拥有独立隐藏规则的小游戏。

当前正式标识：

```text
chemworld-physical-chemistry-v0.3
```

## 版本语义

世界律版本会进入 task contract、scenario、trajectory、submission manifest 和 replay 检查。
下列变化必须提升版本并重建冻结轨迹：

- 状态转移、相分配、反应、仪器或安全模型改变可观察行为；
- 操作的前置条件、成本、风险或物料语义改变；
- observation visibility 或 final scoring contract 改变；
- 原 proxy 被新的专业模块替代。

只修正文案或不改变合同的内部优化不需要提升世界律版本。

## 共享合同

- ontology 与 component identity；
- mechanism schema 与 compiled reaction network；
- typed species/phase/vessel/equipment/thermal/process ledgers；
- physical constitution 与 transaction rollback；
- operation/action schema 与任务前置条件；
- instrument raw signal、processed estimate 和 uncertainty；
- safety/cost signals 与 scoring interface；
- maturity、provenance、hash 和 replay policy。

## v0.3 的运行时物理

v0.3 将三个已有专业候选模块接入正式运行时，并冻结 serious v1 的任务感知实验空间：

- 冷却结晶：van't Hoff 溶解度、晶种质量、紧凑 PBM、CSD 和物料闭合；
- 连续流：共享 compiled mechanism 的几何解析 PFR、热边界、压降和求解诊断；
- 萃取/洗涤：活度修正分配、逐级收敛、夹带和 TPD-style 稳定性诊断。

没有等价专业实现的干燥、浓缩和转移仍保持显式 proxy。世界律升级不会把局部
`professional_candidate` 误称为工业验证模型。

## 一致性规则

若任务需要特殊初态、隐藏参数或观测权限，应写入 scenario/task contract。若需要新的物理行为，
应增加带版本和模型卡的 kernel。不得在单个任务分支中悄悄改变公共操作的物料、能量或可见语义。

完整执行结构见[系统架构](architecture.md)，模型证据边界见[模型成熟度](model_maturity.md)。
