# 预发布限制声明

本页是 ChemWorld-Bench 公开预发布阶段的正式边界声明。任何 benchmark、论文、课程或
leaderboard 叙述都应遵守这里的表述。

## 一句话边界

ChemWorld-Bench 是一个面向 agent、optimizer 和学生的虚拟物理化学交互环境。它不是
真实反应预测软件，不是 DFT 或分子动力学 wrapper，不是商业流程模拟器，也不是实验机器人
控制系统。

## 当前适用范围

当前版本支持受控虚拟任务：

- 在同一个 `world_law_id=chemworld-physical-chemistry-v0.2` 下运行任务切片；
- 使用半机理或轻量物理模型生成 hidden scenario；
- 通过 Gymnasium API、CLI、trajectory、replay verifier 和 baseline report 评测 agent；
- 比较有限预算实验设计、仪器观测使用、局部 world model 学习、约束处理和可复现提交。

可以声明：

- 这是一个可交互、可复现、可评测的虚拟化学实验 benchmark；
- task、scenario、mechanism、scoring 和 trajectory 带有版本化合同和 hash；
- agent 只能通过公开 observation、instrument result、cost/risk signal 和日志学习；
- 预发布核心任务已经有 frozen task contract、golden trajectory、baseline report、
  replay verifier 和本地 release gate。

不可声明：

- ChemWorld 能预测真实反应产率、选择性、纯度、谱图或工艺表现；
- 当前参数可以直接指导真实实验；
- proxy/lite 模块等同于工业验证的热力学、动力学、传递或设备模型；
- leaderboard 分数代表真实实验室成功概率；
- 当前 LLM/tool agent baseline 代表真实最强化学智能体能力。

## 任务成熟度

每个任务必须携带 `physics_maturity` 和 `kernel_maturity`。预发布核心任务当前边界是：

| Task | Maturity | 边界 |
| --- | --- | --- |
| `reaction-to-assay` | `lite` | 有半机理反应网络、物料/能量约束和合成仪器观测；不是真实反应预测器。 |
| `reaction-to-purification` | `proxy` | 萃取/洗涤使用专业候选模型；干燥、浓缩和转移仍为有界 proxy。 |
| `partition-discovery` | `lite` | 相接触使用专业候选 extraction train，但分配参数仍为 benchmark 校准值，不等同于真实溶剂体系热力学。 |

所有图表、论文 artifact、baseline table 和课程报告都应显示 maturity，而不能只展示最高分。

## 已知 proxy/lite 表面

当前仍需明确标注的低成熟度表面包括：

- reaction kinetics：局部反应网络与速率律，未系统对齐真实机理数据库；
- downstream separation：萃取/洗涤已接入活度修正 extraction train、TPD-style diagnostic、夹带和物料守恒；干燥、浓缩、转移仍为可解释 proxy；
- aqueous chemistry：D4C 已提供 pH observation 和 Ksp precipitation hooks，但不是完整 electrolyte speciation solver；
- Gibbs equilibrium：D4D 已提供 fixed-TP ideal-mixture solver diagnostics，但不是数据库驱动的 multiphase Gibbs minimizer；
- crystallization 与 flow：运行时已接入专业候选 PBM/PFR；distillation 有 reference-validated shortcut slice，electrochemistry 含多个专业候选子模块；它们仍不应作为工业高保真流程模型宣传；
- spectroscopy/instruments：生成合成 HPLC/GC/UV-vis/final assay 信号，用于 agent 观测与教学，不是真实仪器谱图预测；
- safety/cost：是 benchmark 约束信号，不是法律、工业或实验室安全合规结论。

## 数据和安全边界

- 公开 trajectory 是虚拟数据，不能伪装成真实实验数据；
- 学生或 human pilot 日志用于研究前必须匿名化，并分离教学评分与科研使用；
- 任何真实实验、真实机器人、外部数据库或危险化学流程接入，都需要独立安全审查和领域专家审核；
- benchmark 输出不能作为真实实验操作建议。

## 预发布验收口径

预发布目标不是“完成通用 chemical world model”，而是提供一个小而可信的 benchmark 核心。
当前 release gate 是：

```powershell
.\.venv\Scripts\python.exe scripts\run_release_gate.py
```

该 gate 覆盖 lint、type check、全量测试、文档构建、环境自洽性审计和 baseline smoke。只有通过
该 gate，并在 artifact 中包含任务合同、baseline report、dataset card、replay manifest、
release checklist 和本限制声明时，才能发布预发布 benchmark claim。
