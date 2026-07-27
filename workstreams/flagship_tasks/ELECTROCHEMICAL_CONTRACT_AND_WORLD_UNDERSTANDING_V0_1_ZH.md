# 电化学任务合同与世界认识评估 v0.1

日期：2026-07-26
状态：开发完成，付费实验前等待负责人确认

## 1. 这次修正的不是一个符号，而是四套冲突定义

旧实现同时存在四个互不一致的来源：

1. mechanism YAML 声明负电位窗口、Arrhenius 速率、五个物种和四条路径；
2. scenario card 使用另一个任务 ID，仍声明负电位与 2 A；
3. 独立 electrochemical scenario 模块维护另一套隐藏参数，但没有接入任务运行时；
4. 实际任务运行时使用正电位、Nernst、Butler-Volmer、传质、双电层、欧姆损失和 Faraday 账本。

旧 YAML 中的 `D` 和 `Coupled` 从未被任务运行时推进；`IsoRed` 接收了全部非目标产物，
却被名字和别名暗示成一个具体异构体。这使“声明机理”和“实际世界”无法比较。

现在的唯一合同是
`src/chemworld/physchem/electrochemical_task_contract.py`。运行时初始化时必须验证：

- task：`electrochemical-conversion`；
- mechanism：`electrochemical_conversion`；
- species：`Ox / Red / SideRed`；
- pathway：`Ox <=> Red` 和 `Ox => SideRed`；
- electron number：`n = 2`；
- standard potential base：`E0 = 1.05 V`，再叠加世界与介质偏移；
- forward-current sign：`-1`；
- generic reaction ODE 不得执行这两条路径，必须由专用电化学 runtime 执行。

如果 YAML、scenario card 或 runtime 任一层漂移，环境构造直接失败，不再静默运行。

## 2. 物种、化学式与守恒到底表示什么

当前三个物种不是现实分子的身份声明，而是三个集总库存池：

| ID | 精确含义 | 不代表什么 |
|---|---|---|
| `Ox` | 可被目标还原的氧化态库存池 | 某个已知的 `C6H10O5` 分子 |
| `Red` | 目标还原库存池 | 已确认结构的目标化合物 |
| `SideRed` | 正向还原过程中形成的非目标库存池 | “一定是异构体”、过还原物或二聚体 |

三者的 `formula: C6H10O5` 只用于元素库存闭合。它的严格语义是：

> 每转移 1 mol 集总物种，C/H/O 元素库存按同一基准单位守恒。

它不是字面分子式。电子由 Faraday charge ledger 维护；质子、支持电解质、沉淀盐和溶剂
属于电解质边界状态，不进入这三个 redox species 的化学计量账本。代码和 YAML 都记录了
这三条语义，不能再把相同 formula 解读成“已经定义了真实分子”。

旧 `D`、`Coupled` 已删除，原因不是简化偏好，而是运行时没有独立状态方程、速率或产物流
推进它们。保留它们会制造不可执行的假机理。

如果以后要改成真实化学，应选择明确半反应。例如对苯醌/氢醌体系必须声明：

`C6H4O2 + 2 H+ + 2 e- <=> C6H6O2`

此时必须同步追踪 `H+`、水/缓冲体系、分子电荷和真实副反应物种；不能只把 `Ox/Red`
改名，或只替换 formula。当前 benchmark 明确不声称达到这一级真实化学身份。

## 3. 反向电化学分支的修正

运行时的 Butler-Volmer 模型允许电流反向。旧实现会在 `Red -> Ox` 时仍应用“正向产品
选择性”，从而把一部分被氧化的 `Red` 记入副产物池。这与声明路径不一致。

现在：

- `Ox -> Red` 时，目标产物和 `SideRed` 按正向选择性分流；
- `Red -> Ox` 时，只闭合主 redox couple，不生成 `SideRed`；
- 正反向都检查物料、charge 和 energy residual；
- runtime provenance 明确记录 current setpoint 是非负幅值上限，真实有符号电流由
  Butler-Volmer 决定。

## 4. 为什么归一化向量不能继续面向科学模型

9 维 `[0,1]` 向量适合 LHS、随机搜索和 BO 的内部计算，但不适合科学 Agent。旧接口不告诉
模型“第 3 维是 probe potential”，也不展示向量最终解码成的物理步骤。因此模型无法把证据
写成可审计的“电位、电流、时间、介质”关系。

新电化学 S0 接口要求模型直接提交：

- `electrolyte_profile`、`solvent`；
- `reagent_amount_mol`；
- `probe_potential_V / probe_current_mA / probe_duration_s`；
- `controlled_potential_V / controlled_current_mA / controlled_duration_s`。

执行器内部仍确定性编码成单位向量，以复用现有 baseline 和 recipe compiler；该向量不再进入
模型 prompt。历史中展示命名参数和实际执行 controls。这样模型与 baseline 使用同一个物理
搜索域，但模型不再被迫用无物理意义的坐标说话。

## 5. “认识世界”比较什么

不比较模型是否猜中 `Ox`、`SideRed` 或某个私有类名，而比较可实验区分的因果等价类。

最终综合必须给出结构化 claim：cause、effect、方向/非单调性、机制标签、适用范围、证据 ID
和 confidence。隐藏 reference graph 对电位、电流、时间、电解质、溶剂和投料量与公开响应的
关系评分：

其中电位、电流和时间明确指主 controlled electrolysis 阶段，claim vocabulary 使用
`controlled_potential_V`、`controlled_current_mA` 和 `controlled_duration_s`，不再使用会混淆
probe/controlled 阶段的泛化字段名。

- structural edge precision / recall / F1；
- directional accuracy；
- mechanism-tag precision / recall / F1；
- unsupported claim rate；
- confidence Brier score。

这只是 **Declared** 层。它能回答“模型公开声明的世界图是否接近模拟器的可观测结构”，
不能单独证明模型真的会用这个认识。

完整结论仍需三层：

1. **Declared**：结构化 claim 与隐藏 reference graph 的一致性；
2. **Predictive**：对冻结、未执行干预的结果预言是否正确；
3. **Actionable**：最终推荐在独立 observation seeds 上是否超过 incumbent。

当前 v0.3 已同时实现 Declared、Predictive 和 Actionable。Predictive 在最终综合上下文中给出
三个由探索历史确定、尚未执行、只改变一个因素的问题：改变 controlled potential、controlled
current 和 electrolyte profile。模型只预测固定指标的 `increase`、`decrease` 或
`no_material_change`，并给出 confidence；统一方向阈值为 0.01。问题集合在模型回答前确定，验证
结果不返回模型，不能在看到回答或模拟结果后再选择问题。

预测指标的来源也显式冻结：除 `leaderboard_score` 来自 terminal summary 外，其余指标一律取
`closeout-final-assay` 的 processed estimate。三个诊断槽仍作为标准化完整 assay 执行，但不会
因同一字段在多个仪器中出现而改变评分来源。

每个问题做 2 次配对重复。每次重复分别运行 reference 和 intervention，并强制两臂使用相同
observation seed 与 noise namespace，共 `3 × 2 × 2 = 12` 次本地模拟。Predictive 不增加模型
调用，单独报告 directional accuracy、confidence Brier score、nontrivial actual-effect rate 和
逐 query/metric 审计行，不与 Declared 或 Actionable 混成一个总分。

## 6. 付费实验前冻结清单

- [x] mechanism、scenario、runtime、S0 搜索域对齐；
- [x] 删除未执行物种和假 Arrhenius；
- [x] `runtime_owned` 在 generic ODE 中 fail closed；
- [x] 正向副产物与反向 redox accounting 对齐；
- [x] 模型侧改为命名物理参数，单位向量仅内部可见；
- [x] 最终综合要求 evidence-grounded structured claims；
- [x] Declared scorer 与隐藏 reference graph；
- [x] 三次 incumbent + 三次 recommendation 的 paired blind validation 草案；
- [x] 冻结 Predictive held-out intervention、指标、方向阈值、配对重复和零反馈设计；
- [x] 冻结候选 method config：`gpt-5.6-sol`、`high`、输出上限 8000、最多 3 attempts；
- [x] 八轮 mock prompt preflight：decision 最大 6268/7500，Predictive final 8579/9000；
- [x] 计算单 seed / 五 seed 的调用量与 token 上界；
- [ ] 负责人确认协议 hash 后，才允许读取 key 并执行付费实验。

资源口径如下：

- 每 seed：8 次实验决策 + 1 次最终综合 = 9 次成功 provider calls；
- 每 seed：8 次 exploration + 12 次 Predictive paired validation + 3 次 incumbent validation
  + 3 次 recommendation validation = 26 次本地物理模拟；这些 validation 不调用模型；
- 五 seed：45 次成功 provider calls，130 次本地物理模拟；
- 最坏 retry 上界：每 call 最多 3 attempts，即五 seed 最多 135 个 HTTP attempts；
- 按冻结 prompt cap 和 `max_tokens` 计算的极端 token 包络：每 seed 最多约 69k input
  estimate + 72k output allocation，五 seed约 705k；若每次都用满三次 attempt，则请求包络约
  2.115M tokens。它是保护性上界，不是预计消耗；
- 旧 r3 的 16 calls 共报告 84,210 tokens，约 5,263 tokens/call；不能直接当作新协议成本，
  因为新协议多一次 final synthesis 且输出 structured claims；
- WellAU 当前没有可核实单价，仓库只能报告 token 和 calls，不能给出可信 USD 预算。开始前如
  不能取得供应商价格，应把“成本上限”写成 calls/tokens 上限，而不是伪造美元数。

## 7. 当前本地验证

- 新增合同、物种、反向分支、命名参数和 world-understanding 测试均通过；
- 电化学两轮 mock、一次最终综合、incumbent/recommendation 各一次盲验证端到端完成；
- 完整八轮 mock + 最终综合 + 12 次 Predictive 配对模拟 + 六次盲验证完成，9 次 mock model
  calls、26 次本地模拟；
- exploration、Predictive 与 Actionable 三类收据均可独立回放；query、plan、result、score 和
  配对 seed/namespace 的篡改会导致审计失败；
- mock 全程未读取 API key，未调用外部 provider；
- 仓库仍有一个既有的无关失败：`mechanism_preregistration.py` 中的 `LEGACY_*` 名称触发
  `test_runtime_does_not_use_legacy_species_constants`，不是本次修改引入。
