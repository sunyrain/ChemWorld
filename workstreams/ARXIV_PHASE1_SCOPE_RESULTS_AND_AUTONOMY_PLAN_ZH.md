# 已被取代的第一阶段 arXiv 计划

本文件保留旧的 static-S0/G0–G2 规划历史。当前权威计划为：

- `workstreams/arxiv_v1/EXPERIMENTAL_INTELLIGENCE_V1_MASTER_PLAN_ZH.md`；
- `workstreams/arxiv_v1/reports/experimental-intelligence-experiment-ledger-v0.1.json`；
- `paper/experimental_intelligence_v1_manuscript.md`。

旧40-cell matched G0/G2 矩阵已不再是第一版 arXiv 的必做前置实验。

---

# ChemWorld 第一阶段 arXiv：范围、证据与逐操作实验计划

状态：`working synthesis; not a publication claim`

审计基准：`main@0005e239a26c276a95ea8ce291ab559caf00857d`

用途：收束第一阶段 arXiv 的中心问题，区分已经完成的实验、开发证据和待执行实验，并冻结
逐操作自主实验的设计原则。本文不提升任何已有证据的等级。

---

## 1. 结论先行

第一阶段论文不应以“LLM 是否优于 BO”为中心，也不应把当前临时的固定 recipe executor 写成
ChemWorld 的本体。

最稳固且最贴近项目真实价值的中心命题是：

> **现有化学 AI 评测通常把实验压缩成一次参数选择；ChemWorld 将实验恢复为一个有状态的行动—
> 测量过程，使实验程序、主动表征、证据使用、生命周期、资源约束、认知更新和最终优化可以在同一
> 化学/化工世界中被分别测量。**

英文工作表述：

> **ChemWorld turns an experiment from a vector-valued query into a stateful policy over chemical
> operations and measurements, making experimental agency measurable.**

建议标题：

> **ChemWorld: From Recipe Optimization to Experimental Agency in Executable Chemical Worlds**

这篇论文的贡献顺序应为：

1. **世界与运行时**：统一的、有状态的、部分可观测的化学过程世界；
2. **实验语言**：逐操作动作、主动测量、事务提交/回滚、成本/风险/样品账本和可回放轨迹；
3. **评测方法**：把程序完成、优化、预测、认知更新和先验影响拆成不同端点；
4. **行为证据**：现有固定流程实验已经显示出任务异质性、优化—认知分离以及先验对行动的强影响；
5. **自主实验结果**：用新的严格逐操作矩阵检验 agent 在没有固定流程时如何实验，而不是要求它必须
   战胜经典优化器。

世界实例、机制变化和反事实干预是 ChemWorld 的重要能力，但不是第一阶段论文必须押注的唯一中心
命题。它们在本稿中承担“可控实验条件”的角色，而不是把论文写成“规律分布理论”。

---

## 2. 为什么这个故事成立

当前相关工作大致解决了四类相邻问题：

- [Summit](https://doi.org/10.1002/cmtd.202000051)、
  [Olympus](https://arxiv.org/abs/2010.04153) 等把化学实验抽象为可查询的优化目标；
- [ChemGymRL](https://doi.org/10.1039/D3DD00183K) 已经证明虚拟化学 bench 和细粒度 RL 操作
  并非空白；
- [ScienceWorld](https://aclanthology.org/2022.emnlp-main.775/)、
  [DiscoveryWorld](https://proceedings.neurips.cc/paper_files/paper/2024/hash/13836f251823945316ae067350a5c366-Abstract-Datasets_and_Benchmarks_Track.html)
  等已经建立交互式科学发现环境；
- [Coscientist](https://doi.org/10.1038/s41586-023-06792-0)、
  [ChemCrow](https://doi.org/10.1038/s42256-024-00832-8)、
  [LabUtopia](https://arxiv.org/abs/2505.22634) 和
  [MATTERIX](https://doi.org/10.1038/s43588-025-00924-4) 等研究真实或具身实验执行。

ChemWorld 不需要与这些工作争夺“第一个虚拟实验室”或“第一个实验 agent”。当前更可守的交集是：

> 一个统一的化学/化工因果运行时，同时包含有状态材料过程、多步操作、可选仪器、部分观测、
> 失败与资源账本、跨实验 campaign、稳定任务合同和轨迹回放；同一底层世界既能支持经典
> recipe 优化，也能支持 agent 自主逐操作实验。

因此，与现实机器人实验室的关系应写成互补而非替代：

- 机器人实验室主要测量现实设备可执行性、硬件编排和部署就绪度；
- ChemWorld 主要隔离并大规模测量实验决策、证据使用和科学行为；
- 未来可以把机器人/仪器前端接到 ChemWorld 的操作语义上，但第一阶段不做 sim-to-real 主张。

第一阶段避免绝对使用：

- “最完整的虚拟化学实验室”；
- “可以近乎无限生成任意物理规律”；
- “首个交互式化学世界”；
- “可以执行任意现实化学实验”。

更准确的当前表述是：

> ChemWorld 是一个覆盖有限但异质物理机制的高自由度、任务约束下的逐操作化学过程环境。

---

## 3. 当前系统本体：已经实现什么

### 3.1 交互内核

当前底层已经是逐操作环境，而不是 recipe 表格：

- 每个环境 `step` 执行一个 operation；
- action 先经过 schema、任务权限和状态前置条件校验；
- operation 在事务中改变物料、相、设备、热状态、过程状态和资源账本；
- 无效或物理上未定义的 action 被记录为失败事务，不会静默变成另一个动作；
- 测量是 agent 主动选择的 operation；
- `terminate` 后仍需 agent 主动执行 `measure(final_assay)` 才形成完整实验；
- campaign 模式在合法 final assay 后创建 fresh vessel，继续同一隐藏世界中的下一实验。

关键实现：

- `src/chemworld/envs/chemworld_env.py`
- `src/chemworld/runtime/engine.py`
- `src/chemworld/runtime/transactions.py`
- `src/chemworld/operation_validator.py`
- `src/chemworld/agent_interface.py`

### 3.2 操作、仪器和观测规模

当前注册：

- **28 类 operation**；
- **5 类仪器**：HPLC、GC、UV-vis、pH meter、final assay；
- **37 个公开标量观测键**；
- **15 个任务合同**；
- 反应、液液分离、结晶、蒸馏、连续流、电化学和平衡表征等物理域。

28 类 operation 包括：

- 反应：加试剂、加溶剂、加催化剂、加热、等待、取样、淬灭；
- 分离：加相、加萃取剂、混合、静置、分相、洗涤、干燥、浓缩、转移；
- 结晶：加晶种、冷却结晶、过滤；
- 蒸馏：蒸发、蒸馏、收集馏分；
- 连续流：设定流量、运行流动反应；
- 电化学：设定电位/电流、电解；
- 生命周期与表征：终止、测量。

操作注册和字段合同见 `src/chemworld/world/operations.py`。

### 3.3 主动表征的当前真实边界

Agent 可以决定：

- 是否测量；
- 使用哪一种当前允许的仪器；
- 何时测量；
- 如何根据 raw signal、processed estimate、uncertainty 和 observed mask 决定下一操作；
- 是否按公开 spectrum ID 读取历史表征。

当前测量是同步 operation。系统还没有实现真实仪器队列、审批、异步等待、轮询或延迟返回。
因此论文应写“agent actively chooses measurements and receives measurement outcomes”，不应写成已经
完成真实异步实验申请系统。

### 3.4 世界能力的当前真实边界

当前版本具有有限但异质的机制库、连续参数变化、初始条件变化、观测噪声、材料映射和受控机制
变换，可以产生大量可回放实例。

但当前还不是：

- 开放式化学物种生成器；
- 任意反应拓扑或任意物理定律的组合语法；
- 任意现实反应预测器；
- 工业级通用数字孪生。

第一阶段应把“可扩展架构”和“当前已实现覆盖”分开写。

---

## 4. 当前结果审计：已完成的实验矩阵

### 4.1 环境和任务设计资格

| 项目 | 当前记录 | 证据性质 |
| --- | ---: | --- |
| 注册任务 | 15 | 环境覆盖 |
| complete-experiment 设计 | 15/15 可执行 | 设计资格 |
| midpoint/boundary/categorical cases | 415 | 确定性执行审计 |
| 声明成功指标 | 62 | 任务合同 |
| 已绑定到 evaluator 的指标 | 62/62 | 端点资格 |
| dead recipe coordinate | 0 | adapter 资格 |
| 有正式多世界 participant 结果的任务 | 2 | 科学结果 |

证据入口：`workstreams/flagship_tasks/reports/task-design-matrix-v1.json`。

这个矩阵证明任务和端点可执行，不证明 15 个任务上的 agent 性能。

### 4.2 正式 S0 v1.0：固定流程、无材料 dossier

共同合同：

- 任务：electrochemical conversion、reaction-to-crystallization；
- 独立 worlds：每任务 10；
- 每 world 20 次探索实验；
- 每次 agent 决策选择一套完整实验参数；
- 执行器将参数编译为固定操作序列；
- 结束后另做 final recommendation、3 个 predictive checks 和成对盲验证；
- LLM：`gpt-5.6-sol`，medium reasoning；
- 推断单位：world，而不是调用或算法 seed。

规模：

| 组成 | 单元/实验 |
| --- | ---: |
| Participant cells | 20 |
| Participant physical experiments | 760 |
| Participant provider calls | 420 |
| Classic baseline cells | 1,050 |
| Classic baseline physical experiments | 27,300 |
| v1.0 总 physical experiments | 28,060 |

主结果：

| 任务 | Participant | 最强信息匹配基线 | 配对差及 95% world interval |
| --- | ---: | ---: | ---: |
| Electrochemical | 0.7150 | Structured RF-EI 0.6159 | +0.0991 `[+0.0103,+0.1748]` |
| Crystallization | 0.5355 | LHS 0.5708 | −0.0353 `[−0.0650,−0.0085]` |

电化学中最强 privileged descriptor calibration 为 0.6441；Participant 与它的配对区间跨 0。
这些算法比较没有预注册 superiority margin 或 multiplicity plan，只能作为正式描述性结果。

从本地 raw campaign 重新调用汇总 builder 后，重建对象与 tracked summary 完全一致；canonical
SHA-256 为 `70b79e126953c4ac61b3d44e4b825909b604123de90ac6f2a628244d81a8cac3`。

证据入口：

- `workstreams/flagship_tasks/reports/static-s0-v1.0-formal-campaign-summary.json`
- `configs/benchmark/scientific_optimization_s0_v1.0_freeze_manifest.json`

### 4.3 正式 S0 v1.2：Opaque / Nominal / Misindexed 三臂

矩阵：

```text
2 tasks × 3 information arms × 10 paired worlds = 60 participant cells
```

规模：

- 1,200 exploration experiments；
- 720 predictive physical experiments；
- 360 blind-validation experiments；
- 合计 2,280 physical experiments；
- 1,260 provider calls；
- 5 次 provider retry；
- 0 method failure；
- 60/60 cells 通过记录中的 exact replay。

注意：Opaque 臂复用 v1.0 participant 结果。正式 active corpus 的唯一实验数应按
`27,300 baselines + 2,280 tri-arm participant = 29,580` 计算，不能把 v1.0 opaque 再加一次。

正确信息结果：

| 任务 | Opaque | Nominal | 配对差 | familywise 97.5% interval |
| --- | ---: | ---: | ---: | ---: |
| Electrochemical | 0.7150 | 0.7874 | +0.0724 | `[+0.0074,+0.1546]` |
| Crystallization | 0.5355 | 0.5615 | +0.0260 | `[−0.0130,+0.0630]` |

错误先验结果：

| 任务 | Misindexed | Misindexed − Nominal | 早期操纵 | 差分动作纠偏 | 恢复到 Opaque | 联合恢复 |
| --- | ---: | ---: | --- | --- | --- | --- |
| Electrochemical | 0.6853 | −0.1020 | 通过 | 通过 | 未通过 | 未通过 |
| Crystallization | 0.5845 | +0.0229 | 通过 | 未通过 | 通过 | 未通过 |

更细的行为证据：

- 电化学错误先验将 first misleading action rate 从 Opaque 的 0.0 提高到 0.7；
- 结晶错误先验将 first misleading action rate 从 0.0 提高到 1.0；
- 电化学的 misleading-action share 从早期 0.54 降到后期 0.24，但性能恢复未成立；
- 结晶从早期 0.86 降到后期 0.50，差分纠偏仍未成立；
- 结晶在错误先验下得分更高，不能解释为发现了先验错误。

证据入口：

- `workstreams/flagship_tasks/reports/static-s0-v1.2-three-arm-information-campaign-summary.json`
- `configs/benchmark/scientific_optimization_s0_v1.1_nominal_information_freeze_manifest.json`
- `configs/benchmark/scientific_optimization_s0_v1.2_misindexed_information_freeze_manifest.json`

从本地 raw campaign 重新构建的三臂对象也与 tracked summary 完全一致；canonical SHA-256 为
`becff70ecbc33aa4c151fcdf16a7a100e2a5b032acb97a38aad4c1eddaa2e516`。

### 4.4 优化和认知的现有分离信号

| 指标 | Electrochemical | Crystallization |
| --- | ---: | ---: |
| Final recommendation score | 0.7150 | 0.5355 |
| Held-out directional accuracy | 0.744 | 0.478 |
| Held-out Brier | 0.186 | 0.298 |
| Declared directional accuracy | 0.680 | 0.850 |
| Structural edge F1 | 0.389 | 0.275 |
| Mechanism-tag F1 | 0.190 | 0.144 |
| Unsupported claim rate | 0.611 | 0.714 |
| Final recommendation gain over incumbent | 0 in 10/10 worlds | 0 in 10/10 worlds |

这组结果不能证明普遍规律，但已经给出一个很有价值的现象：

- 更高的优化分数不自动等于更可靠的解释；
- 自信的声明不自动转化为 held-out prediction；
- 正确信息、受先验影响、后期改动作和最终性能恢复是不同变量；
- 最终重新描述一个已测试条件不等于合成了新方法。

第一阶段应把它写成“ChemWorld 可以分解测量这些维度”的示范，而不是把两任务结果上升为普遍
心理学定律。

Predictive query 的物理结果在 final synthesis 前没有反馈，但 query 定义本身已经可见；因此论文
应称其为 outcome-held-out predictive checks，不应写成连 query 都完全未见的独立外部测试。

### 4.5 五任务 development campaign

矩阵：

```text
5 tasks × 5 worlds × (1 participant + 5 classic methods) = 150 cells
```

规模：

- 3,900 physical experiments；
- 526 provider calls；
- 150/150 cells 完成；
- 记录中全部 exact replay；
- 明确为 development-only。

| 任务 | Participant | 最佳 classic | 差值 |
| --- | ---: | ---: | ---: |
| Electrochemical | 0.7454 | RF-EI 0.6622 | +0.0832 |
| Crystallization | 0.5206 | RF-EI 0.6071 | −0.0866 |
| Distillation | 0.4795 | GP-EI 0.4192 | +0.0603 |
| Partition | 0.5426 | GP-EI 0.5511 | −0.0085 |
| Flow | 0.1627 | GP-EI 0.2145 | −0.0518 |

它支持“同一 scaffold 的表现具有任务异质性”，不支持五任务 superiority 或跨任务平均总分。

证据入口：

- `workstreams/flagship_tasks/reports/static-s0-five-task-postqualification-campaign-summary.json`

### 4.6 历史环境 attainability

RC28 Gate A 历史结果记录：

- A2：4,896 trials，5-experiment budget top-1 accuracy 0.9826；
- A3：2,016 trials，8 个 post-change experiments 时 end-to-end success 0.9657；
- 这是 reference 环境证书，不是 participant-agent 结果；
- 当前 source binding 已 stale；
- Participant Gates B–E 未执行。

这一块最多放在环境资格或 Supplementary，不应成为第一阶段 agent 主结果。

### 4.7 当前严格逐操作 agent 证据

现有真正 strict closed-loop primitive 结果非常窄，而且是负结果：

| 方法 | 轨迹 | 决策 | 关键行为 | 完整实验 |
| --- | ---: | ---: | --- | ---: |
| Flash Direct | 4 | 72 | 38 次 HPLC；2 次 terminate 均在最后一步；0 final assay | 0/4 |
| Flash Stateful | 4 | 72 | 39 次 add_reagent；19 次 HPLC；0 terminate/final assay | 0/4 |

这些运行没有 harness action repair、automatic terminate 或 automatic final assay。它们证明 strict
逐操作闭环可执行，并暴露了 lifecycle failure；不能证明通用 LLM 缺乏科学实验能力。

一个重要混杂是：当前 prompt 没有给模型完整、紧凑的当前实验 operation ledger，只保留很短的
recent decision context。重复加料和重复 HPLC 首先可能是 controller memory failure。

证据入口：

- `workstreams/flagship_tasks/RC28_PARTICIPANT_EXECUTION_QUALIFICATION_RESULTS_ZH.md`
- `src/chemworld/agents/live_llm.py`
- `src/chemworld/agents/prompt_context.py`

### 4.8 Scientific Adaptation development

当前 experiment-level scientific adaptation r4 跨 provider/scaffold 开发运行还包括：

- 2 tasks；
- changed/no-change twins；
- 24 planned method/provider cells；
- 192 planned physical experiments；
- 19 cells completed，5 method failures；
- 174/192 physical experiments 完成并 replay。

这些结果适合审计 schema sensitivity、provider accounting 和 failure handling，不适合比较 provider
或 scaffold 的科学因果效应。它们仍然采用 experiment-level executor，也不是逐操作自主结果。

---

## 5. 证据状态和发布阻断

### 5.1 当前 evidence DAG 不通过

在上述审计基准上执行：

```text
.venv\Scripts\python.exe scripts/evidence_pipeline.py --check
```

返回失败。`configs/current.json` 记录 10 个 stale 节点，但按当前源码实际重算为 **17 个**：

- runtime affordance；
- runtime reachability；
- state transition invariants；
- maturity truth；
- mechanism diagnostic relation graph；
- backend candidate；
- mechanism preregistration；
- task design matrix；
- mechanism confirmatory task semantics；
- five-task postqualification summary；
- mechanism design audit；
- mechanism release qualification；
- mechanism A2/A3 structural receipts；
- mechanism preflight；
- mechanism public Gate A decision；
- pre-arXiv claim-evidence ledger。

因此 `configs/current.json` 当前不是一个与 HEAD 闭合的一致证据面。正式数值可以是历史冻结结果，
但必须明确绑定到产生它们的 source commit；不能用当前 HEAD 的状态替历史结果背书。

Formal S0 v1.0 和 v1.2 summaries 不在这 17 个 stale 节点中，并且已从本地 raw 结果精确重建。
因此当前主要数值本身的证据强度高于环境/current registry 的一致性状态；两类问题必须分开报告。

### 5.2 本次聚焦测试

本次在现有 `.venv` 中完成：

- agent interface；
- agent interaction contract；
- invalid action atomicity；
- task design；
- runtime reachability；
- runtime domain affordance；
- runtime boundary；
- RL public action adapter；
- RL observation contract；
- score replay。

合计 **83 tests passed**。

`current and not slow` 大子集在 5 分钟限制内未完成，也未在超时前给出失败。因此这次审计不能替代
完整 detached test/wheel/replay attestation。

### 5.3 原始数据没有进入 Git

`runs/` 被 `.gitignore` 排除。当前本机共有约 **17,714 个文件、32.3 GiB**，其中主要 active
campaign 大致包含：

- v1.0 classic baselines：约 15.5 GB；
- 三个 participant arms：每臂约 472 MB；
- five-task development：约 1.3 GB；
- RC28 mechanism runs：约 258 MB。

Git 中目前主要保存 compact summaries、freeze manifests 和 hashes，而不是完整轨迹。arXiv 前至少
需要发布：

1. 逐 cell derived table；
2. trajectory/receipt hash manifest；
3. 小型可直接 replay 的公开 subset；
4. 完整 archive 的持久化下载地址和数据卡；
5. 生成全部论文图表的单一脚本。

`benchmark/releases/chemworld-serious-v1` 当前为空，`benchmark/` 下没有 tracked release 文件；
因此现在的公开 clone 不能独立复现 formal results。

### 5.4 不同正式臂来自不同 source commit

v1.0 baselines、opaque、nominal 和 misindexed 绑定到不同历史 commit。发布前有两种可接受路线：

- **Archive-first**：为每个 arm 发布精确 source snapshot/wheel/container 和原始 manifest；
- **Release-candidate recertification**：在一个冻结 release candidate 上重新 replay 全部旧轨迹，
  证明分数、观测和账本一致。

推荐第二种，因为读者最终只需一个公开 release tag。

---

## 6. 逐操作实验：应当比较什么

第一阶段正式矩阵只区分两种控制粒度。

### G0：`experiment_recipe`

Agent 一次选择完整实验参数，compiler 执行预定义操作序列。

作用：

- 经典 BO/LHS 的自然接口；
- 当前 S0 结果的接口；
- 低 agency calibration。

它不是 ChemWorld 的全部能力，也不能被描述为逐操作自主实验。

### G2：`closed_loop_primitive`

Agent 每次只选择一个 operation；环境执行后返回公开结果，再由 agent 决定下一 operation。

作用：

- 测量实验内反馈、主动表征和在线程序调整；
- 是项目核心的高 agency 接口。

官方 runner 已支持 strict policy：

- one decision per operation；
- no automatic action repair；
- no automatic terminate；
- no automatic final assay；
- failed/invalid actions retained。

### 两组对照的可解释性

- G0 → G2 是 experimental-control transfer：recipe structure、操作顺序、测量时机、实验内适应和
  lifecycle 同时移交给 Agent；
- 它是系统级行动权对照，不是反馈价值的单因素因果估计；
- 反馈价值在 G2 内部以 self-chosen measurement 后的 identical-prefix
  true/masked/delayed/permuted branches 单独估计；
- BO/LHS 只在 G0 中作为 calibration，不与 G2 做“同算法层级”的胜负归因。

---

## 7. 逐操作协议

### 7.1 Agent 输入

每个 operation 前提供：

- 任务目标和成功标准；
- 当前 campaign/experiment 资源；
- 当前有效操作和 operation-specific schema；
- 当前已公开观测、uncertainty 和 mask；
- 当前实验的完整紧凑 operation ledger；
- 已完成实验的压缩 memory；
- 可用历史 spectrum catalog。

不得提供：

- hidden species amounts；
- rate constants 或真实 mechanism identity；
- world seed/private salt；
- evaluator truth；
- 固定 recipe、必经 phase 或 harness 建议的下一操作。

`available_actions()` 是公开 affordance 和安全 interlock，不是人类写好的实验流程。

### 7.2 Agent 输出

每次只接受一个 flat typed action：

```json
{
  "operation": "measure",
  "instrument": "hplc"
}
```

同时记录简短、可评分的决策审计：

```json
{
  "decision_role": "probe",
  "target_observable": "selectivity",
  "direction_or_range": "increase",
  "confidence": 0.65,
  "expected_effect": "...",
  "belief_update_rule": {
    "if_supported": "...",
    "if_not_supported": "..."
  }
}
```

不请求或保存私有逐字 chain-of-thought。

### 7.3 失败和预算

- 主公平轴是 **operation count**；
- invalid action 占一个 operation；
- provider/schema/normalization failure 不转换为有效动作；
- 不自动重问模型来获得一个“成功版本”，基础设施 retry 单独记账；
- `terminate` 和 `final_assay` 必须由 agent 自主选择；
- 没有 final assay 的实验是 incomplete，不从 hidden state 补算分数；
- time、sample、measurement cost、risk、model calls、tokens、USD cost 和 wall time 分轴报告。

完成实验数本身是结果，不能预先给逐操作 agent 自动补足相同的 completed-experiment count。

### 7.4 Agent 自有过程记忆

正式运行前必须增加完整、紧凑的 current-experiment ledger，例如：

- 已执行 operation 顺序；
- 每步 transaction status；
- 当前物料/阶段的公开摘要；
- 已用测量及其公开结果 ID；
- terminate/final-assay 状态；
- 剩余 operation budget。

这不是固定流程 scaffold。它只保存 agent 自己刚刚做过什么，不替 agent 决定下一步。

---

## 8. 逐操作指标

不要把所有指标压成一个总分。

### A. Lifecycle autonomy

- `P(at least one completed experiment)`；
- completed experiments per operation budget；
- operations to first valid final assay；
- terminate 后成功 final assay 的比例；
- premature termination / budget exhaustion。

### B. Procedural validity

- valid / invalid / rollback rate；
- repeated identical operation without new evidence；
- repeated measurement without intervening state change；
- failure 后恢复率；
- operation diversity 和 route diversity。

### C. Scientific utility

- final score conditional on autonomous completion；
- best-so-far by completed experiment；
- best-so-far by operation；
- operation-normalized utility AUC；
- risk、cost 和 sample consumption。

端到端 utility 可以把 incomplete 记为 0，但必须同时单独报告 completion，避免“低分”和“没有做完”
被混成一个数字。

### D. Feedback use

- measurement 后下一控制动作改变率；
- self-chosen measurement 后 true / masked / delayed / permuted identical-prefix action divergence；
- assigned / unassigned / masked spectrum 对后续操作的影响；
- true / permuted feedback 的 identical-prefix next-action sensitivity。

### E. Cognition

- 预声明方向预测 accuracy；
- Brier/calibration；
- 结果与 belief update rule 的一致性；
- unsupported claim rate；
- probe / exploit / verify 资源分配；
- cognition metrics 与 optimization utility 的逐 task、逐 world 关系。

论文核心不是预设二者必须正相关或负相关，而是：

> ChemWorld 允许我们观察“优化成功但认知不可靠”“认知判断改善但性能未恢复”等不同表型。

---

## 9. 第一阶段最小可发表矩阵

### 9.1 Qualification：不产生科学主张

| 任务 | 条件 | 预算/重复 | 目的 |
| --- | --- | --- | --- |
| reaction-to-assay | strict G2 + state machine | 18 ops × 3 repeats | 最短 lifecycle |
| electrochemical seed 0 | strict G2 + state machine | 48 ops × 3 repeats | 单 stage 过程 |
| crystallization seed 0 | strict G2 + state machine | 72 ops × 3 repeats | 多 stage 过程 |
| purification seed 0 | strict G2 + state machine | 90 ops × 1–3 repeats | 22-step stress |

进入主矩阵的工程门槛：

- lifecycle assistance = 0；
- prompt 包含完整 current-experiment ledger；
- runner/receipt/replay 通过；
- failure reasons 完整；
- 至少 state-machine positive control 能稳定完成；
- LLM completion 可以低，但必须足以估计，或明确接受 lifecycle-negative paper。

### 9.2 主矩阵

```text
2 tasks
× 5 paired worlds
× 2 controller conditions (matched G0 / strict G2)
× 2 provider repeats
= 40 method campaign cells
```

任务：

- electrochemical conversion；
- reaction-to-crystallization。

主信息条件：

- opaque material；
- assigned spectra；
- 相同任务/世界/公开信息；
- keyed paired observation noise；
- operation-count budget；
- 同一基础模型、相同 provider 配置；
- 每个 granularity 条件单独记录调用和 token。

校准方法：

- LHS；
- 一个最强 information-matched typed surrogate；
- valid-action random；
- deterministic state machine。

LHS/BO 只回答 recipe-search calibration。valid-random/state-machine 才是 G2 的同层 procedural controls。

### 9.3 主问题和估计量

主问题不是“G2 是否一定比 G0 高分”，而是：

1. 移除固定流程后，agent 的生命周期和程序完成能力发生什么变化？
2. 在相同 primitive action space 下，读取中间反馈是否改变动作、测量和端到端效用？
3. 优化、程序完成、预测和认知更新是否给出相同的 agent 排序？

推荐主端点：

```text
operation-normalized end-to-end utility AUC
```

联合报告：

- autonomous completion；
- conditional final score；
- feedback-use 指标；
- prediction/calibration；
- resource vector。

统计单位是 task × world；provider repeat 是嵌套技术重复。

### 9.4 可选连接实验：先验 × 高 agency

现有三臂结果已经证明先验显著改变 recipe-level 早期动作。若预算允许，最有价值的扩展不是再加
更多 BO，而是：

```text
electrochemical
× 3 prior arms (opaque/nominal/misindexed)
× G2
× 5 worlds
× 2 repeats
= 30 cells
```

它直接回答：

> 当 agent 可以自主选择测量和程序时，高 agency 是否改变错误先验的锁定、证据获取和纠偏？

这会把现有最有意思的结果与项目真正的逐操作本体接起来。它是优先扩展，不是首轮 40-cell 矩阵的
启动前提。

---

## 10. 论文图表

### Figure 1：实验不再是一行参数

展示：

```text
hidden chemical world
→ public operation affordances
→ stateful transaction
→ optional measurement
→ evidence-dependent next action
→ terminate + final assay
→ fresh experiment in same campaign
```

同时把 recipe compiler 画成进入同一 runtime 的一个低 agency adapter。

### Figure 2：平台覆盖和资格

- 15 tasks × physical domains；
- 28 operations × task permissions；
- 5 instruments；
- 415 execution cases；
- 62 bound endpoints；
- transaction/replay/partial-observation contract。

### Figure 3：固定流程 pilot 揭示任务异质性

- electrochemical 与 crystallization 的 Participant/classic paired result；
- five-task development 只作 task heterogeneity 补充；
- 不画成 SOTA leaderboard。

### Figure 4：先验改变行为，但恢复不是一个数字

- opaque/nominal/misindexed scores；
- early/late misleading-action share；
- manipulation / action correction / performance recovery 三组件；
- 两任务失败组件不同。

### Figure 5：从 recipe 到真正实验自主性

- G0/G2；
- completion、procedural validity、utility AUC、feedback use；
- 失败保留在图中；
- 资源前沿而不是单一总分。

### Figure 6 或 Extended Data：优化—认知表型

- final utility vs prediction accuracy；
- calibration；
- unsupported claims；
- belief-update consistency；
- 按 task/world 展示，不只给模型平均。

---

## 11. 论文结构

1. **Introduction**：参数建议不等于做实验；现实 lab 很重要但难以大规模隔离科学决策。
2. **ChemWorld**：世界、运行时、任务合同和公开边界。
3. **An experiment as a policy**：operation、measurement、transaction、campaign、replay。
4. **Environment qualification**：15 tasks、415 cases、62 endpoints、模型适用域。
5. **Controlled behavioral probes**：两任务 S0 和三臂先验。
6. **Autonomous procedure study**：G0/G2 主矩阵。
7. **Experimental agency profiles**：lifecycle、utility、feedback、cognition、resource。
8. **Limitations**：有限机制库、合成仪器、无现实迁移、模型/任务样本有限。
9. **Methods and release**：冻结、统计单位、失败、replay、data package。

---

## 12. Claim ledger

### 第一阶段可以声称

- ChemWorld 实现了有状态、逐操作、部分可观测、可回放的虚拟化学过程交互。
- Agent 可以主动选择表征，并根据公开结果继续实验。
- 15 个任务的 complete-experiment adapters 和 62 个评价端点通过记录中的设计资格。
- 当前正式固定流程结果在两个任务、三种先验信息条件和 10 个配对 worlds 上完成。
- 正确信息对电化学有正价值，对结晶不确定。
- 错误先验显著改变两任务的早期行为，但两任务都未通过联合恢复规则。
- 现有结果显示任务依赖的优化、预测和声明可靠性差异。
- 严格逐操作 runner 已实现；当前开发 agent 暴露 lifecycle failure。

### 当前不能声称

- ChemWorld 已覆盖任意化学和任意物理规律。
- 当前正式 S0 是逐操作 agent 结果。
- LLM 普遍优于 BO，或 BO 普遍优于 LLM。
- Participant 已学到正确机制或合成了新方法。
- 错误先验下分数不降等于 agent 发现并纠正错误。
- agent 已完成正式的在线机制变化检测和恢复。
- 当前结果迁移到现实化学、机器人实验室或工业数字孪生。
- 当前 HEAD、报告和论文已经形成可发布的一致证据链。

---

## 13. Roadmap 和 go/no-go

### P0：证据闭合

- 冻结 arXiv release candidate；
- 修复 evidence DAG 的 current fingerprint/freshness；
- 重新生成 runtime、task matrix 和 maturity reports；
- 在单一 release candidate 上 recertify 正式旧轨迹；
- 把 historical/development/formal/withdrawn 分层写入一个 registry；
- 生成 derived-data single source of truth；
- 完成 clean wheel、full tests、replay 和独立 checkout。
- 修复当前 manuscript 未纳入 v1.2、引用 stale 15-task attestation、存在乱码且缺图/参考文献的问题。

退出条件：

```text
evidence_pipeline --check == pass
paper numbers generated from one frozen derived table
all cited formal artifacts have current or explicit archival bindings
```

### P1：逐操作 controller 基础

- 完整 current-experiment operation ledger；
- campaign-persistent material/instrument/vessel/operation resource contract；
- G0 全部 batch 使用同一个 persistent session，并与 G2 通过同一 resource gate；
- `discard_batch` 和 strict G2 controller；
- machine-scorable prediction audit；
- decision-scope/consumed-information/scaffold-authority manifest；
- no-repair/no-closeout tests。

退出条件：

```text
state-machine completes all qualification tasks
strict G2 receipts replay
no hidden/fixed recipe information enters G2
G0/G2 resource cards and autonomous task contracts match
```

### P2：逐操作 qualification

- 运行 9.1 小矩阵；
- 报告 completion 和 failure taxonomy；
- 不因低 completion 修改正式指标；
- 只修复真实 infrastructure bug。

退出条件：

```text
all cells terminal and replayable
method failure is distinguishable from infrastructure failure
formal sample size and cost are estimable
```

### P3：40-cell 主矩阵

- 冻结 worlds、model、provider repeats、operation budgets 和统计规则；
- 哈希交错执行 G0/G2；
- 不看 interim 排名；
- 失败进入分母；
- 一次性生成主表。

退出条件不是“G2 获胜”，而是：

```text
100% terminal receipts
primary and secondary estimands reconstruct from trajectories
negative outcomes retained
```

### P4：数据与论文

- 发布 derived tables、trajectory subset、hash index、data card 和 archive；
- 重写 manuscript，不在当前 narrow S0 稿上简单追加一节；
- 所有图从冻结 derived table 生成；
- 在摘要中明确 recipe-level pilot 与 operation-level main study 的层级；
- arXiv 发布后再决定是否扩展 prior × G2、更多任务或 provider。

---

## 14. 最终判断

当前项目已经具备一篇有价值的环境论文所需的大部分“骨骼”：有状态物理世界、逐操作语言、主动
表征、事务和失败、任务合同、回放，以及一批能显示 agent 行为异质性的正式结果。

现在最缺的不是再增加一个固定 recipe leaderboard，而是两件事：

1. 把当前分散且 source binding 不一致的证据收成一个可发布工件；
2. 用严格 G0/G2 矩阵把“世界支持逐操作”升级为“我们实际测量了逐操作 experimental agency”。

一旦这两件事完成，第一阶段 arXiv 的故事将是完整的：

> **ChemWorld 提供了一个可执行的化学/化工世界，使“agent 如何做实验”本身成为可复现的研究对象；
> 现有实验表明，优化、认知、先验响应和程序自主性不是同一个能力维度。**
