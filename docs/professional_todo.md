# 专业化 TODO

本页概括 ChemWorld 从 research benchmark 走向更专业物理化学环境的长期路线。根目录
`TODO_PROFESSIONAL.md` 可作为更细的开发任务源；发布站点保留中文化摘要。

## 规则

- 不把 qualitative proxy 伪装成真实物理模型。
- 每个专业模块必须有 maturity、参考来源和验证范围。
- 先接小而可审计的专业 slice，再考虑重型 backend。
- 默认安装保持轻量，optional backend 作为验证层存在。
- 任何专业化提升都不能破坏 Gym API、trajectory replay 和 task cards。

## 模块队列

| 专业方向 | 参考目标 | 首个加固目标 |
| --- | --- | --- |
| 物性 | `chemicals`、`thermo`、DIPPR/Perry | 蒸气压、热容、液体体积、输运性质 |
| 反应动力学 | `Cantera`、`RMG-Py` | 热化学、详细平衡、ODE 验证 |
| 反应器 | IDAES、Cantera examples | CSTR、batch、热释放、multiple steady states |
| 相平衡 | teqp、thermopack、phasepy | cubic EOS、activity model、flash/VLE |
| 分离 | IDAES、shortcut distillation | FUG、蒸馏、萃取、结晶 |
| 仪器 | 分析化学参考 | UV-vis、HPLC/GC、IR/NMR 的 benchmark kernel |
| 电化学 | Nernst/Butler-Volmer 基础 | equilibrium potential、energy efficiency |

## 第一批 Professional Queue

优先处理对任务质量影响最大、实现边界清楚、验证成本低的 slice：

- curated vapor-pressure path；
- ideal-gas heat capacity；
- Rackett liquid volume；
- compact transport reporting；
- reference-validated reaction ODE；
- shortcut distillation；
- UV-vis calibration；
- HPLC/GC retention summary；
- cubic EOS report；
- Gibbs minimization 小场景。

## 完成度条

当前不是“已完成专业化”，而是“已有若干可审计专业 slice”。发布时应使用谨慎表述：

```text
foundation/lite with selected reference-validated slices
```

## 当前实现

已经存在的实现方向包括：

- 物性报告 API：蒸气压、热容、密度/摩尔体积、输运性质。
- 反应网络：反应 spec、ODE、热化学、敏感性 hook。
- 反应器：CSTR、batch、热释放和局部验证。
- 相平衡：cubic EOS、Raoult-style VLE、UNIQUAC 入口。
- 分离：shortcut distillation 和 ledger 集成。
- 仪器：UV-vis、HPLC/GC、虚拟谱图接口。
- 电化学：equilibrium potential、measured cell potential、能效摘要。
- 参考 backend：可选校验，不作为默认依赖。

## 发布表述

推荐写法：

> ChemWorld 是一个可控虚拟化学交互 benchmark，包含若干经过参考阅读或局部校准的
> 物理化学 slice；它不是完整流程模拟器、数据库驱动 speciation solver 或真实实验
> 控制系统。
