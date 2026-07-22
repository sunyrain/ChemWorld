# 世界律与版本

世界律是所有任务共享的底层规则：物质怎样流动、反应怎样推进、设备怎样约束操作、仪器能看到什么，
以及风险、成本和评分如何计算。当前版本是：

```text
chemworld-physical-chemistry-v0.5
```

任务是同一世界律上的能力切片，不会为单个任务暗中更换物理规则。世界律 ID 会写入 task
contract、scenario、trajectory 与 replay；改变状态转移、操作成本、观测可见性、评分或正式
provider 路由时必须提升版本，旧轨迹不会被静默解释为新版本结果。

## v0.5 candidate 冻结的正式运行路径

v0.5 的正式运行时已经把下列窄域 provider 接入统一事务：

- `mix`、`wash`：稳定性门控、活度修正、显式夹带与逐组分守恒的 LLE；
- `dry`：有限容量竞争吸附与 spent-sorbent 物料账；
- `concentrate`：受加热功率、真空、冷凝回收与目标回收率约束的差分蒸发；
- `transfer`：源容器 heel、管线 hold-up 与交付物流的显式账本；
- `distill`：泡点、设备容量、热负荷、VLE/Fenske 与可用 FUG 诊断共同约束的蒸馏；
- `heat`、`wait`：共享质量作用量/Arrhenius 网络与动态 batch 热量模型；
- `measure`：UV/Vis、HPLC、GC、pH 与 final assay 的验证合成仪器合同；
- `cool_crystallize`：van't Hoff 溶解度、成核/生长、CSD 与粒径矩闭合的紧凑 PBM；
- `run_flow`：共享反应网络、单相几何 PFR、分布传热与 Darcy–Weisbach 压降；
- `electrolyze`：Nernst/Butler–Volmer、传质极限、双电层、Faraday 账和水相平衡。

旧 reaction/reactor/instrument `lite` 路径、`chemworld_separation_proxy`、旧 LLE/蒸馏双路由、
旧 `pfr`/geometry 别名和只做离线诊断的结晶 route 均已从正式可达图移除。底层解析或参考函数仍可
作为验证组件，但不能被 runtime 隐式调用，也不能仅凭存在就抬高任务成熟度。

## 为什么世界律必须可审计

世界律共同冻结：ontology、compiled mechanism、typed ledgers、transaction rollback、operation
schema、instrument observation、cost/risk、maturity、provider provenance 与 replay policy。
下游操作产生的 spent sorbent、condensate、vent、source heel 和 line hold-up 都保存在 typed phase
ledger 中，不以“损失系数”隐藏物料去向。

backend v0.5 candidate 已把 provider route、任务声明、真实事务、任务合同与核心证据绑定为固定
候选后端。用户可通过[任务目录](tasks.md)查看当前 task hash，通过[模型成熟度](model_maturity.md)
理解证据含义，通过[架构](architecture.md)理解系统结构；维护者审计命令不属于公开使用流程。
