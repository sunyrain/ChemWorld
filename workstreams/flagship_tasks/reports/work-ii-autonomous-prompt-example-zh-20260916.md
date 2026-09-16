# 旧自主实验的复用与实际提示：电化学参数错误先验实例

日期：2026-09-16。性质：既有记录只读核查、提示还原与中文译文；不是新实验或新正式分析。

## 阅读范围与来源

本例取自 W2-62 GPT-5.6-sol / medium C2 队列：电化学参数层、注册顺序第一个世界的错误先验会话。
选择规则是第一注册世界及指定先验条件，没有按成功或失败筛选。该例完成10个批次、90次已提交操作、5次模型快照；
保留4次MCP工具失败，不能把“完成”写成“零接口错误”。

当前入口是 [C2评价报告](work-ii-w2-62-codex-c2-current-composite-evaluation-v0.1.json)，
执行范围见 [W2-62实验说明](../WORK_II_W262_CODEX_C2_FULL_REPLICATION_EXPERIMENT_NOTE.md)。
本例是该历史development队列中的完成会话，不提升为新协议的正式证据。

原运行器已经清理临时提示文件。此次从记录的源码版本取出系统提示，利用保存的配置、首步之前的决策上下文和公共合同重建初始提示。
初始提示14034字节，与原receipt中的指纹完全相同；任务合同8086字节、材料/先验资料3407字节、检查点合同12744字节，均与历史记录一致。
这里只初始化环境以读取初始合法操作，未执行物理step、调用provider或生成新实验结果。

下面“系统提示”是全文中文翻译；任务资料是保持原字段、数值和信息边界的中文展开。
文末附完整英文系统提示和未删字段的公共JSON，便于核对。JSON仅调整缩进；它们是研究者提供的输入，不是原始provider响应。
这不是完整对话转录，也不声称重新保存了当时每一次动态tools/list和工具返回。

同一会话的后续过程见[逐步输入输出中文译读与分析](work-ii-autonomous-transcript-zh-20260916.md)：覆盖90次操作、5次模型快照、全部480项预测及最终推荐，并标明记录缺失与事后分析的边界。

## 哪些旧内容可以复用

| 旧内容 | 可以支持的工作 | 解释边界 |
| --- | --- | --- |
| 自主操作、实际公开测量、资源与错误记录 | 检查探索覆盖、取得何种证据、实验顺序、停止和预算使用 | 使用当时公开信息与当时物理语义；不能用修复后的世界替换旧观测 |
| 每步decision_audit与五个模型快照 | 将预期、观察、公开假设/预测变化与后续行动对照 | 自述是显式报告，需与预测和行为核对；不能等同内部信念 |
| 已提交可执行规律及预测 | 重新分析旧接口下的预测误差与表达一致性 | 受限表达和已展示查询不构成开放建模及未见问题预测证据 |
| 旧实验数据交给新的建模Agent | 若另行设计，可作为固定证据再推断实验 | 这是新的接收者实验，不能追认原Agent已经自主形成该模型 |
| 近期完整流程开发轨迹 | 过程诊断、平台与任务设计校准 | 单批开发结果、历史合同缺陷和服务中断保留各自身份 |

可以先复用全部计划会话及失败做回顾性过程分析；不能因为本例可读，就只分析这一类成功轨迹。
按当前评价报告的135个计划会话核对，本地135/135有非空summary，135/135有非空trajectory；这只说明文件保留，尚未逐会话验证新增过程诊断所需字段的完整性。
新增加的分类规则和统计属于事后分析，应标明；本次只核对一个例子，没有完成整个队列的失效分类。
独立“实验→规律→预测”研究仍自行确定任务、取证和预算；旧资料不成为强制来源。

## 系统提示：全文中文翻译

你是 Work II ChemWorld 发现研究中唯一负责操作层决策的科学 Agent。
一个 Codex 进程控制整个研究过程，跨越多个新批次；这些批次共享一个固定的隐藏世界、一种公开先验条件和一本研究资源账。
调用一次 `material_information`。
在第一次物理操作之前，以及每一个要求的检查点，调用 `belief_snapshot_status`，然后严格通过分阶段的 `tools/list` 协议使用 `commit_belief_snapshot`：
先提交 `action=begin`，再按顺序提交公布的每一页预测与规律，最后提交 `action=finalize`。
每一个物理操作都通过 `step` 提交，并在决定下一个操作之前使用其公开结果。
每次 `step` 调用都必须包含工具schema要求的、有长度边界的 `decision_audit`：预期效果、诊断目标、预期信息增益、
明确写出获得支持与未获支持时如何更新判断、不确定性，以及本次调整所依据的公开信息来源。
这些内容是简洁的科学理由，不能提交私有思维链。

这是一项实验执行任务，不是编程或检查仓库的任务。
不要使用shell、文件、状态或资源枚举工具，也不要检查仓库。
你的第一个动作必须是 `chemworld_lab.material_information`；之后根据需要，只使用
`chemworld_lab.belief_snapshot_status`、`chemworld_lab.commit_belief_snapshot`、`chemworld_lab.step`、
`chemworld_lab.status`、`chemworld_lab.history` 和 `chemworld_lab.inspect_artifact`。
不要创建笔记或运行命令。调用非实验室工具属于无效调用，并会浪费本会话的provider预算。

`experiment_ended` 结果只代表当前批次结束。
当 `campaign_ended=false` 时，保留科学研究上下文，使用返回的 `next_state` 继续下一个新批次。
当 `campaign_ended=true` 时，如最终检查点待提交，先提交它，然后恰好调用一次 `chemworld_lab.commit_final_recommendation`。
仅根据参与者可见的研究证据，从 `campaign_closeout.completed_experiment_indices` 中选出恰好一个已完成批次，
提交其从1开始的 `lifecycle_experiment_index`，供评价器执行盲重放；盲重放结果不会返回给你。
只有在工具确认提交后，才返回恰好一个包含 `status` 与 `summary` 的JSON对象，不要附加其他文字或Markdown代码围栏：

```json
{"status":"campaign_complete","summary":"..."}
```

宿主程序绝不会替你选择、修正、终止、终检或替换操作。
失败以及因资源不足被拒绝的尝试仍保留在轨迹中。
保留足够的操作额度、库存、过程时间和终检能力，以便结束所有计划批次。
19项过程坐标由评价器推导，不要自行报告。不要提供私有思维链。

配方覆盖是研究资格的硬性要求，不是可选建议。
阅读初始提示中的 `recipe_coverage_contract`，同时满足 `target_complete_experiments`、
`minimum_unique_recipes` 和 `maximum_exact_repeats`。
只有当从批次开始到终检的、按顺序提交且成功执行的实验动作对象完全相同，包括操作名称和每一个参数，两个已完成实验才算相同配方。
被拒绝或回滚的尝试不定义配方身份。
根据公开结果自行追踪已完成配方，在消耗重复额度之前规划所需多样性；不要假定宿主会修复重复过多的研究过程。

译者说明：上面的省略号是原提示最终summary字段的示例占位符，不代表本译文省略了系统指令。
原提示同时写了泛指的“不要使用status工具”和明确允许的 `chemworld_lab.status`，此处保留原措辞。

## 初始任务包：中文展开

初始指令为：自主运行完整的多实验发现研究。提交必需的类型化模型检查点；依据公开结果选择每一步操作；
保留共享资源账；结束每一个计划批次；将配方覆盖合同作为硬性资格要求。

### 任务与可操作对象

任务为电化学转化，目标为综合表现 `balanced`，采用开放自主工作流 `autonomous_open_v1`。
在有限的溶剂和电解质选项中，识别有效平衡、传质、双电层、动力学与欧姆行为的耦合，优化电位、电流上限和持续时间，
实现有选择性、电荷与能量利用率较高的转化。
公开的 `current_mA` 是非负电源电流幅度上限，不是对实际有符号反应电流的直接指定；后者与反应方向遵循Butler–Volmer关系。
pH诊断是归一化的有效质子活度指标，不是对真实非水溶剂pH的字面主张。

可选匿名溶剂为 `solvent-S0`、`solvent-S1`、`solvent-S2`、`solvent-S3`，操作编号分别为0、1、2、3。
电解质为 `electrolyte-E0`、`electrolyte-E1`、`electrolyte-E2`、`electrolyte-E3`，操作编号分别为0、1、2、3。
试剂为匿名限量试剂 `limiting_reagent`。
这些编号不对应现实物质或商业配方，也不揭示世界特定的材料残差；本例不提供材料名义性质表。

允许的操作是加试剂、加溶剂、设定电位/电流上限/电解质、电解、测量、终止和明确弃批。
具体合法动作及参数范围随当前状态返回，不能把操作名单理解为任何时刻都可执行。
初始状态为第1步、批次尚未开始、成本/风险/分数均为0、无已有测量；初始可加试剂0至0.04 mol，或加0至0.08 L的四种溶剂之一。
终检须先显式 `terminate`，再执行 `measure`，仪器指定为 `final_assay`；宿主不自动收尾。

### 评分与观测

任务声明的安全限额为0.65。综合评分的分量权重如下，其他门槛与结算仍以原评分合同为准：

| 指标 | 权重 |
| --- | --- |
| 选择性产物产率 `selective_product_yield` | 0.30 |
| 电化学选择性 `electrochemical_selectivity` | 0.15 |
| 能量效率 `energy_efficiency` | 0.15 |
| 法拉第效率 `faradaic_efficiency` | 0.12 |
| 电化学转化率 `electrochemical_conversion` | 0.10 |
| 传质效率 `transport_efficiency` | 0.10 |
| 欧姆效率 `ohmic_efficiency` | 0.08 |

原合同另声明选择性产物产率的乘性门控参数0.02；不能把上表加权和当作完整评分实现。
本例公开的仪器返回字段如下，保留历史接口，即使它与现实仪器名称的直觉对应不同：

| 仪器 | 合同列出的观测 |
| --- | --- |
| `ph_meter` | 归一化pH、沉淀信号 |
| `uvvis` | 能量效率、法拉第效率、传质效率、欧姆效率 |
| `final_assay` | 选择性产物产率、电化学转化率/选择性、能量效率、归一化pH、沉淀信号、法拉第效率、传质效率、欧姆效率 |

观测是仪器限定的部分观测。物种标签使用 `reactant_public`、`target_public`、`impurity_public`、`degradation_public`；
隐藏机理到物种的映射不公开。本例不能追溯改称已经获得后来新增的完整观测映射合同。

### 多批预算与覆盖要求

| 项目 | 当时限额 |
| --- | --- |
| 完整实验目标 / 容器启动 / 终检 | 各10 |
| 全研究操作尝试 | 110 |
| 非终检仪器使用 | 30 |
| 电解操作次数 | 20 |
| 模拟过程时间 | 51750 s |
| 试剂总库存 | 0.345 mol |
| 溶剂总库存 | 0.2875 L |
| 最少不同配方 | 8 |
| 额外完全重复次数上限 | 2 |

所有批次共用额度，新批次不刷新预算。“额外重复”按完成总数减不同配方数计算，所以某配方出现3次会用掉2次额外重复。
初始任务同时保留平台默认 `official_budget=48` 和本研究覆盖后的 `budget=110`；本会话实际动作限额是110，不能误读为48。
收尾合同保留20次收尾操作和6750 s过程时间，允许用于弃批、终检、淬灭、终止、转移这类收尾操作；
这一通用类别列表不代表电化学任务开放了全部这些操作。
另有公开的生命周期建议：起始时完成所有终检至少保留60次操作，因此当前可用于额外探索的建议余量为50次。
该建议与资源卡中的强制保护额度是两个概念。

### 初始科学资料：Agent看到的内容

以下为先验资料的中文译文；“错误先验组”是研究者标签，不向Agent展示。

> 所提供模型可能可靠，也可能发生偏移。实验结果具有最终依据地位。
>
> 这是一个不完整的局部过程模型。相对于探测阶段和所述参考条件，**较高受控电位一侧，应当比低电位一侧更可靠地维持综合表现。**
>
> 该判断的置信度为0.7。在声明适用范围之外，以实验结果为准。

| 参考条件 | 数值 |
| --- | --- |
| 试剂量 | 0.004 mol |
| 溶剂编号 | 1 |
| 电解质编号 | 2 |
| 探测电位 | 1.18 V |
| 探测电流上限 | 70 mA |
| 探测持续时间 | 630 s |
| 受控阶段持续时间 | 3540 s |
| 归一化坐标中心 | 0.5 |

目标控制变量为受控电位和受控电流；相对参考变量为探测电位和探测电流。
这份参考资料不是强制固定所有自主实验的配方，评价查询使用参考条件与Agent的实际取证选择也不是一回事。

### 检查点、预测与规律提交

在实验开始前、完成第2、4、7、10个实验后提交快照，阶段标识分别为 `pre_evidence`、`after_experiment_2`、
`after_experiment_4`、`after_experiment_7`、`final`。这些只是检查点ID，不表示宿主安排了某种科学实验阶段。

每份快照要求提供：资料是否可用、可靠性概率、怀疑有误的字段及理由；每个查询各指标的均值、区间上下界及置信度；
可执行规律摘要、证据引用、适用范围、限制、下一实验意图与整体置信度。
允许被标记的先验字段为受控电位和受控电流。证据目录是10个批次的终检引用；引用应与实际已经获得的证据对应。

可执行规律的输入限于9个字段：电解质编号、溶剂编号、试剂量、探测电位/电流/时间、受控电位/电流/时间。
输出是6个指标：选择性产物产率、电化学选择性、法拉第效率、能量效率、安全风险和综合分数。
规律使用截距及数值项，支持线性、二次、三次、两变量交互、类别项和类别条件下的一/二/三次项；
连接函数限于identity或logistic，并声明输出上下界。初始规律可以只有截距、没有数值项。
因此这里允许调整受限表达式，但没有开放任意程序、微分方程求解器或自由机理实现。

每个检查点有16个预测查询，每个查询预测上述全部6个指标。查询条件可见、答案隐藏，不会向Agent反馈评价真值。
所有查询共同使用上表中的试剂、溶剂、电解质、探测阶段和受控时长，改变的受控电位/电流如下。
下面仅将浮点显示舍入为便于阅读的十进制，文末JSON保留原始数值。

| 查询ID | 受控电位/V | 受控电流上限/mA |
| --- | --- | --- |
| p05-i05 | 1.200 | 71.0 |
| p00-i01 | 0.895 | 29.4 |
| p00-i09 | 0.895 | 110.6 |
| p09-i00 | 1.412 | 19.5 |
| p09-i10 | 1.412 | 120.5 |
| p10-i05 | 1.465 | 71.0 |
| p00-i05 | 0.895 | 71.0 |
| p04-i01 | 1.107 | 29.4 |
| p04-i09 | 1.107 | 110.6 |
| p02-i03 | 1.001 | 49.2 |
| p02-i07 | 1.001 | 90.8 |
| p07-i02 | 1.306 | 39.3 |
| p07-i07 | 1.306 | 90.8 |
| p09-i03 | 1.412 | 49.2 |
| p00-i03 | 0.895 | 49.2 |
| p00-i07 | 0.895 | 90.8 |

提交顺序为begin→四页预测→三页规律→finalize；半成品不算已提交快照，宿主不自动修补数据，待提交检查点会阻止继续物理操作。
四页预测依次包括：

- 第一页：p00-i01、p00-i09、p05-i05、p09-i00。
- 第二页：p00-i05、p04-i01、p09-i10、p10-i05。
- 第三页：p02-i03、p02-i07、p04-i09、p07-i02。
- 第四页：p00-i03、p00-i07、p07-i07、p09-i03。

三页规律依次覆盖：产率/选择性、法拉第效率/能量效率、安全风险/综合分数。

### 工具与上下文边界

`material_information` 返回上面的材料目录与先验；`belief_snapshot_status` 提供当前检查点和分阶段提交要求；
`commit_belief_snapshot` 提交快照；`step` 执行动作；`status` 获取当前有界状态；`history` 返回有界、非权威历史缓存；
`inspect_artifact` 读取公开表征片段；最终通过 `commit_final_recommendation` 选定一个已完成批次。
本例没有末尾新候选ActionPlan包，不能和另一个纵向开放行动实验混淆。

初始JSON中存在“agent/可写目录、可选记忆”的通用元数据，但该会话系统提示明确禁止创建笔记和使用文件工具；
研究者不能因为通用元数据写了可写，就宣称本例开放了持久笔记与编程。
参与者没有权威完整轨迹文件，完整轨迹由评价器保存。此处“完整提示”也不意味着Agent在每一步都重新收到全部历史数据。

## 该会话实际怎样行动：既有记录摘读

所有批次实际保持试剂0.004 mol、溶剂1且体积0.025 L、电解质2、探测阶段1.18 V/70 mA/630 s、
一次UV–Vis测量，以及受控阶段3540 s；每批最后显式终止并终检。受控电位与电流上限变化如下。
得分从已保存的公开操作结果读取并与批次摘要核对，不是重新执行物理环境得到的值。

| 批次 | 受控电位/V | 受控电流上限/mA | 公开得分 |
| --- | --- | --- | --- |
| 1 | 1.5 | 90 | 0.174446 |
| 2 | 0.6 | 90 | 0.631292 |
| 3 | 0.2 | 90 | 0.560596 |
| 4 | 0.6 | 150 | 0.706515 |
| 5 | 0.6 | 250 | 0.748720 |
| 6 | 0.6 | 350 | 0.705582 |
| 7 | 0.6 | 220 | 0.772431 |
| 8 | 0.6 | 200 | 0.767910 |
| 9 | 0.6 | 220 | 0.767533 |
| 10 | 0.6 | 220 | 0.770918 |

公开的先验可靠性报告依次为0.70、0.25、0.18、0.12、0.10。
第二批后的明确表述是：“在固定电流下，较低受控电位显著优于较高电位配方，因此提供的方向判断在所测试条件中未获支持。”
这里“显著优于”是Agent原话的中文意思，不是研究者报告统计显著性。
最终表述为：“实验排除了在所测参考条件中高受控电位简单占优的解释，支持0.6 V附近、配合中等电流上限的非线性最优区域。”
它最终推荐第7批，并用第9、10批完全重复了这一配方。

这些记录支持一个明确的个案结论：Agent取得了相反方向的公开证据，报告了修订，并改变了后续搜索行为。
这不是“始终困在高电位区域”或“看到反证仍维持原方向判断”的例子。
不能仅凭它得出整个队列普遍纠错成功，也不能用置信度变化替代留出预测评分或完整机理识别。

原系统提示已经强制要求每步说明诊断目标、预期信息增益和条件更新规则。因此它检验的是带这种研究指导的Agent；
不能把它事后命名为完全没有研究程序提示的自然自主基线。

## 原文附件与复现边界

以下附研究者输入的系统原文、完整初始JSON、材料/先验JSON和检查点JSON。字段、查询和数值未删减；
提供JSON并不意味着当时模型可直接读这些文件，其中两份资料实际通过实验室工具取得。
动态工具schema的说明上文已给出，逐次传输文本未保存在本报告中。

### 系统提示原文

```text
You are the sole operation-level scientific agent in a Work II
ChemWorld discovery campaign. One Codex process controls the full campaign across multiple fresh
batches that share one fixed hidden world, one public prior condition, and one campaign resource
ledger. Call material_information once. Before the first physical operation and at every required
checkpoint, call belief_snapshot_status, then use commit_belief_snapshot only through its staged
tools/list protocol: action=begin,
then every published prediction page and law page in order, then action=finalize. Submit every
physical operation through step and use
its public outcome before deciding the next operation. Every step call must include the bounded
decision_audit requested by the tool schema: expected effect, diagnostic target, expected
information gain, explicit supported/not-supported belief updates, uncertainty, and the public
adaptation source. This is a concise scientific rationale, never private chain-of-thought.

This is an experiment execution task, not a coding or repository-inspection task. Do not use shell,
file, status, or resource-listing tools and do not inspect the repository. Your first action must be
chemworld_lab.material_information; thereafter use only chemworld_lab.belief_snapshot_status,
chemworld_lab.commit_belief_snapshot, chemworld_lab.step, chemworld_lab.status,
chemworld_lab.history, and chemworld_lab.inspect_artifact
as needed. Do not create notes or run commands. A non-lab tool call is invalid and wastes the cell's
provider budget.

An experiment_ended outcome closes only the current batch. When campaign_ended=false, preserve your
scientific context and continue into the next fresh batch using the returned next_state. When
campaign_ended=true, commit the final checkpoint if it is due, then call
chemworld_lab.commit_final_recommendation exactly once. Select exactly one completed batch's 1-based
lifecycle_experiment_index from campaign_closeout.completed_experiment_indices for evaluator-owned
blind replay using only participant-visible campaign evidence; no blind outcome will be returned.
Only after the tool confirms the commitment, return exactly one JSON object with status and summary,
with no prose or Markdown fence: {"status":"campaign_complete","summary":"..."}.
The host never chooses, repairs, terminates, assays, or replaces your operations. Failed and
resource-rejected attempts remain part of the trajectory. Keep enough operation, stock,
process-time, and assay capacity to close all planned batches. The 19 process coordinates are
evaluator-derived; do not report them yourself. Do not provide private chain-of-thought.

Recipe coverage is a hard campaign qualification obligation, not optional advice. Read the
recipe_coverage_contract in the initial prompt and satisfy its target_complete_experiments,
minimum_unique_recipes, and maximum_exact_repeats simultaneously. Two completed experiments are
the same recipe only when their ordered committed lab action objects are exactly equal, including
operation names and every submitted action parameter; rejected or rolled-back attempts do not
define recipe identity. Track completed recipes yourself from public outcomes, plan the required
diversity before spending repeat allowance, and never assume the host will repair a repeat-heavy
campaign.
```

### 初始提示JSON

```json
{
  "belief_checkpoint_contract": {
    "byte_count": 12744,
    "contents_in_prompt": false,
    "relative_path": "../reference/belief_checkpoint_contract.json",
    "sha256": "2fde67f772dabb2d6575e80651c1fa65df8b4aa3410112944b3b90ca076b3bf2",
    "submission_protocol": [
      "action=begin",
      "append every host-published prediction page in order",
      "append every host-published law page in order",
      "action=finalize"
    ],
    "submit_with": "chemworld_lab.commit_belief_snapshot"
  },
  "initial_public_state": {
    "active_constraint_flags": {},
    "campaign_resources": {
      "campaign_terminal": false,
      "current_experiment": {
        "experiment_index": 1,
        "experiment_index_base": 1,
        "vessel_started": false
      },
      "ledger_sha256": "14d3a507bc201a0954119ace7166282ad956f7a28bf1ff050fe1e679d6d77514",
      "lifecycle_reserve": {
        "current_batch": {
          "minimum_operations_to_explicit_discard": 2,
          "minimum_operations_to_final_assay": 6,
          "open": false
        },
        "discretionary_attempts_before_final_assay_floor": 50,
        "future_unstarted_batches": 9,
        "minimum_fresh_batch_operations": {
          "to_explicit_discard": 2,
          "to_final_assay": 6
        },
        "minimum_future_batch_operation_reserve": {
          "for_explicit_discards": 18,
          "for_final_assays": 54
        },
        "policy": "advisory_only_agent_controlled_no_hidden_allocation",
        "recommended_remaining_attempt_floor": {
          "to_close_all_planned_batches_with_discards_allowed": 20,
          "to_final_assay_all_planned_batches": 60
        },
        "remaining_operation_attempts": 110,
        "schema_version": "chemworld-campaign-lifecycle-reserve-0.1"
      },
      "schema_version": "chemworld-public-campaign-resource-state-0.1",
      "state": {
        "closed_batches": 0,
        "discarded_batches": 0,
        "final_assays": 0,
        "instrument_uses": {},
        "nonfinal_instrument_uses": 0,
        "operation_attempts": 0,
        "operation_committed_counts": {},
        "protected_closeout_reserve": {
          "allowed_operation_classes": [
            "discard_batch",
            "final_assay",
            "quench",
            "terminate",
            "transfer"
          ],
          "consumption_by_operation_class": {},
          "operation_attempts_consumed": 0,
          "outstanding_batches": 10,
          "planned_batches": 10,
          "policy": "protected_closeout_reserve_enforced",
          "process_time_consumed_s": 0.0,
          "protected_process_time_s": 6750.0,
          "required_operation_attempts": 20
        },
        "remaining": {
          "final_assays": 10,
          "nonfinal_instrument_uses": 30,
          "operation_attempts": 110,
          "operation_repeats": {
            "electrolyze": 20
          },
          "per_instrument": {},
          "process_time_s": 51750.0,
          "stocks": {
            "reagent_mol": 0.345,
            "solvent_L": 0.2875
          },
          "vessel_starts": 10
        },
        "report_only": {
          "accumulated_risk": 0.0,
          "peak_risk": 0.0,
          "physical_cost": 0.0,
          "process_time_s": 0.0,
          "protected_reserve_consumed_s": 0.0,
          "reserve_consumption_by_operation_class": {},
          "sample_consumed_L": 0.0
        },
        "stocks_used": {},
        "vessel_starts": 0
      }
    },
    "campaign_state": {
      "best_score": null,
      "budget": 110,
      "campaign_id": "episode-4cf98906b0ff4575a383907a8a446621",
      "closed_batch_count": 0,
      "completed_batches": [],
      "completed_experiment_count": 0,
      "discarded_batches": [],
      "done": false,
      "episode_mode": "campaign",
      "experiment_index": 1,
      "experiment_index_base": 1,
      "experiment_summaries": [],
      "final_assay_count": 0,
      "last_terminal_summary": null,
      "operation_count": 0,
      "remaining_budget": 110,
      "scenario_id": "electrochemical-conversion",
      "task_id": "electrochemical-conversion"
    },
    "characterization_artifact": null,
    "latest_measurement": {
      "available": false
    },
    "legal_actions": [
      {
        "amount_mol": {
          "range": [
            0.0,
            0.04
          ],
          "unit": "mol"
        },
        "operation": "add_reagent"
      },
      {
        "operation": "add_solvent",
        "solvent": {
          "choice_labels": {
            "0": "solvent-S0",
            "1": "solvent-S1",
            "2": "solvent-S2",
            "3": "solvent-S3"
          },
          "choices": [
            0,
            1,
            2,
            3
          ],
          "unit": "categorical"
        },
        "volume_L": {
          "range": [
            0.0,
            0.08
          ],
          "unit": "L"
        }
      }
    ],
    "recipe_coverage_contract": {
      "maximum_exact_repeats": 2,
      "minimum_unique_recipes": 8,
      "recipe_identity_semantics": {
        "exact_repeat_count": "target completed experiments minus the number of distinct recipes",
        "identity_basis": "exact equality of the ordered committed lab action objects from batch start through the final assay, including operation names and every submitted action parameter",
        "rejected_or_rolled_back_attempts_included": false,
        "unit": "completed_experiment"
      },
      "target_complete_experiments": 10
    },
    "remaining_operations": 110,
    "schema_version": "chemworld-interactive-codex-experiment-0.6",
    "stage": "experiment_setup",
    "step": 1,
    "uncertainty": {},
    "visible_metrics": {
      "cost": 0.0,
      "safety_risk": 0.0,
      "score": 0.0
    }
  },
  "instruction": "Run the complete multi-experiment discovery campaign autonomously. Commit the required typed belief checkpoints, choose every operation after its public outcome, preserve the shared resource ledger, close every planned batch, and satisfy the recipe_coverage_contract as a hard qualification obligation.",
  "material_information": {
    "byte_count": 3407,
    "contents_in_prompt": false,
    "relative_path": "../reference/material_information.json",
    "sha256": "58f2b62738d60705b9a1b0482d4e35ce723276bb9d1e650681666d31029f9e04"
  },
  "mcp_step_example": {
    "action": {
      "operation": "one currently legal operation"
    },
    "expected_step": 1,
    "submit_with": "chemworld_lab.step"
  },
  "recipe_coverage_contract": {
    "maximum_exact_repeats": 2,
    "minimum_unique_recipes": 8,
    "recipe_identity_semantics": {
      "exact_repeat_count": "target completed experiments minus the number of distinct recipes",
      "identity_basis": "exact equality of the ordered committed lab action objects from batch start through the final assay, including operation names and every submitted action parameter",
      "rejected_or_rolled_back_attempts_included": false,
      "unit": "completed_experiment"
    },
    "target_complete_experiments": 10
  },
  "schema_version": "chemworld-interactive-codex-experiment-0.6",
  "session_scope": "campaign",
  "task": {
    "allowed_instruments": [
      "final_assay",
      "ph_meter",
      "uvvis"
    ],
    "allowed_operations": [
      "add_reagent",
      "add_solvent",
      "discard_batch",
      "electrolyze",
      "measure",
      "set_potential",
      "terminate"
    ],
    "budget": 110,
    "campaign_resources": {
      "campaign_terminal": false,
      "campaign_terminal_reason": null,
      "card": {
        "card_id": "work-ii-electrochemical-a-p-k10-two-repeat",
        "card_sha256": "67c9cac1de56157e1716e65b7fc96e727971659702b38f4d04c6f8a0f3ef68da",
        "hard_limits": {
          "final_assays": 10,
          "nonfinal_instrument_uses": 30,
          "operation_attempts": 110,
          "operation_repeats": {
            "electrolyze": 20
          },
          "per_instrument": {},
          "process_time_s": 51750.0,
          "stocks": {
            "reagent_mol": 0.345,
            "solvent_L": 0.2875
          },
          "vessel_starts": 10
        },
        "metadata": {
          "closeout_policy": {
            "allowed_operation_classes": [
              "discard_batch",
              "final_assay",
              "quench",
              "terminate",
              "transfer"
            ],
            "automatic_action_repair": false,
            "automatic_closeout": false,
            "discard_path_operations_per_batch": 1,
            "discard_path_total_operation_reserve": 10,
            "final_assay_path_operations_per_batch": 2,
            "final_assay_path_total_operation_reserve": 20,
            "planned_batches": 10,
            "policy": "protected_closeout_reserve_enforced",
            "resource_status": "w2_26_runtime_envelope"
          },
          "pilot_id": "work-ii-electrochemical-matched-prior-d1",
          "process_time_policy": {
            "formula": "8 unique probe+controlled electrolysis maxima + 2 exact-repeat probe+controlled maxima; no quench/transfer stage",
            "implicit_stage_reserve_s": 0.0,
            "pattern_id": "electrochemical-a-p-k10-two-repeat",
            "protected_reserve_fraction": 0.15,
            "protected_reserve_s": 6750.0,
            "quench_transfer_allowance_s": 0.0,
            "repeat_allowance_s": 9000.0,
            "required_stage_max_s": 36000.0,
            "resource_status": "w2_26_runtime_envelope"
          },
          "recipe_coverage_contract": {
            "maximum_exact_repeats": 2,
            "minimum_unique_recipes": 8,
            "recipe_identity_semantics": {
              "exact_repeat_count": "target completed experiments minus the number of distinct recipes",
              "identity_basis": "exact equality of the ordered committed lab action objects from batch start through the final assay, including operation names and every submitted action parameter",
              "rejected_or_rolled_back_attempts_included": false,
              "unit": "completed_experiment"
            },
            "target_complete_experiments": 10
          },
          "scope": "one_task_prior_world_cell",
          "task_id": "electrochemical-conversion"
        },
        "schema_version": "chemworld-campaign-resource-card-0.1"
      },
      "current_experiment": {
        "experiment_index": 0,
        "vessel_started": false
      },
      "last_event_id": null,
      "latest_receipt": null,
      "ledger_sha256": "14d3a507bc201a0954119ace7166282ad956f7a28bf1ff050fe1e679d6d77514",
      "lifecycle_reserve": {
        "current_batch": {
          "minimum_operations_to_explicit_discard": 2,
          "minimum_operations_to_final_assay": 6,
          "open": false
        },
        "discretionary_attempts_before_final_assay_floor": 50,
        "future_unstarted_batches": 9,
        "minimum_fresh_batch_operations": {
          "to_explicit_discard": 2,
          "to_final_assay": 6
        },
        "minimum_future_batch_operation_reserve": {
          "for_explicit_discards": 18,
          "for_final_assays": 54
        },
        "policy": "advisory_only_agent_controlled_no_hidden_allocation",
        "recommended_remaining_attempt_floor": {
          "to_close_all_planned_batches_with_discards_allowed": 20,
          "to_final_assay_all_planned_batches": 60
        },
        "remaining_operation_attempts": 110,
        "schema_version": "chemworld-campaign-lifecycle-reserve-0.1"
      },
      "schema_version": "chemworld-public-campaign-resource-state-0.1",
      "state": {
        "closed_batches": 0,
        "discarded_batches": 0,
        "final_assays": 0,
        "instrument_uses": {},
        "nonfinal_instrument_uses": 0,
        "operation_attempts": 0,
        "operation_committed_counts": {},
        "protected_closeout_reserve": {
          "allowed_operation_classes": [
            "discard_batch",
            "final_assay",
            "quench",
            "terminate",
            "transfer"
          ],
          "consumption_by_operation_class": {},
          "operation_attempts_consumed": 0,
          "outstanding_batches": 10,
          "planned_batches": 10,
          "policy": "protected_closeout_reserve_enforced",
          "process_time_consumed_s": 0.0,
          "protected_process_time_s": 6750.0,
          "required_operation_attempts": 20
        },
        "remaining": {
          "final_assays": 10,
          "nonfinal_instrument_uses": 30,
          "operation_attempts": 110,
          "operation_repeats": {
            "electrolyze": 20
          },
          "per_instrument": {},
          "process_time_s": 51750.0,
          "stocks": {
            "reagent_mol": 0.345,
            "solvent_L": 0.2875
          },
          "vessel_starts": 10
        },
        "report_only": {
          "accumulated_risk": 0.0,
          "peak_risk": 0.0,
          "physical_cost": 0.0,
          "process_time_s": 0.0,
          "protected_reserve_consumed_s": 0.0,
          "reserve_consumption_by_operation_class": {},
          "sample_consumed_L": 0.0
        },
        "stocks_used": {},
        "vessel_starts": 0
      }
    },
    "contract_profile": "extended-research",
    "description": "Select a bounded solvent medium and electrolyte profile, identify coupled effective equilibrium, transport, double-layer, kinetic, and ohmic behavior (the pH diagnostic is a normalized effective proton-activity index, not a literal non-aqueous pH claim), and optimize potential, current, and duration for selective, charge- and energy-efficient conversion. The public current_mA control is a nonnegative power-supply magnitude cap; the signed electrochemical current and reaction direction follow Butler-Volmer.",
    "electrochemical_workflow_mode": "autonomous_open_v1",
    "env_id": "ChemWorld",
    "episode_mode": "campaign",
    "experiment_lifecycle": {
      "automatic_closeout": false,
      "explicit_terminate_required": true,
      "final_assay_action_template": "{\"operation\":\"measure\",\"instrument\":\"final_assay\"}",
      "final_assay_after_terminate": true,
      "final_assay_required": true,
      "planned_complete_experiments": 10,
      "schema_version": "chemworld-public-experiment-lifecycle-0.1",
      "terminate_action_template": "{\"operation\":\"terminate\"}"
    },
    "method_budget_contract": {
      "checkpoint_complete_experiments": [
        2,
        4,
        7,
        10
      ],
      "complete_experiment_limit": 10,
      "operation_limit": 110
    },
    "objective": "balanced",
    "observation_contract": {
      "contract_hash": "ae2bd704eef7c7a8198d33575d9769de3851fa2de837ac52469a2a6e2fa88678",
      "instrument_observable_keys": {
        "final_assay": [
          "selective_product_yield",
          "electrochemical_conversion",
          "electrochemical_selectivity",
          "energy_efficiency",
          "pH_normalized",
          "precipitation_signal",
          "faradaic_efficiency",
          "transport_efficiency",
          "ohmic_efficiency"
        ],
        "ph_meter": [
          "pH_normalized",
          "precipitation_signal"
        ],
        "uvvis": [
          "energy_efficiency",
          "faradaic_efficiency",
          "transport_efficiency",
          "ohmic_efficiency"
        ]
      },
      "mapping_visibility_policy": "hidden mechanism-to-species mapping is not public",
      "public_species_label_policy": [
        "reactant_public",
        "target_public",
        "impurity_public",
        "degradation_public"
      ],
      "required_observation_keys": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "transport_efficiency",
        "ohmic_efficiency",
        "energy_efficiency",
        "pH_normalized",
        "precipitation_signal",
        "safety_risk",
        "electrochemical_conversion"
      ],
      "score_family": "electrochemistry",
      "success_metrics": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "score",
        "faradaic_efficiency",
        "transport_efficiency",
        "ohmic_efficiency",
        "energy_efficiency",
        "pH_normalized",
        "precipitation_signal",
        "safety_risk"
      ]
    },
    "observation_contract_hash": "ae2bd704eef7c7a8198d33575d9769de3851fa2de837ac52469a2a6e2fa88678",
    "observation_policy": "partial-instrument-observation",
    "official_budget": 48,
    "safety_limit": 0.65,
    "schema_version": "chemworld-public-interactive-task-contract-0.1",
    "scoring_contract": {
      "component_weights": {
        "electrochemical_conversion": 0.1,
        "electrochemical_selectivity": 0.15,
        "energy_efficiency": 0.15,
        "faradaic_efficiency": 0.12,
        "ohmic_efficiency": 0.08,
        "selective_product_yield": 0.3,
        "transport_efficiency": 0.1
      },
      "contract_hash": "b5603757998437e3537a07c1916c36dbff3266b48bb5bf46dad8a952d1f9842b",
      "contract_id": "electrochemical-s0-balanced-efficiency-v2",
      "multiplicative_gates": {
        "selective_product_yield": 0.02
      },
      "objective": "balanced",
      "score_family": "electrochemistry",
      "success_metrics": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "score",
        "faradaic_efficiency",
        "transport_efficiency",
        "ohmic_efficiency",
        "energy_efficiency",
        "pH_normalized",
        "precipitation_signal",
        "safety_risk"
      ]
    },
    "scoring_contract_hash": "b5603757998437e3537a07c1916c36dbff3266b48bb5bf46dad8a952d1f9842b",
    "success_metrics": [
      "selective_product_yield",
      "electrochemical_selectivity",
      "score",
      "faradaic_efficiency",
      "transport_efficiency",
      "ohmic_efficiency",
      "energy_efficiency",
      "pH_normalized",
      "precipitation_signal",
      "safety_risk"
    ],
    "task_contract_hash": "c93f5daf6e0c8643f7e8899e0d71086fd912853be17e39bb1879f7b880d9f43b",
    "task_id": "electrochemical-conversion",
    "termination_policy": "budget-with-workflow-gated-final-assay"
  },
  "task_contract_reference": {
    "byte_count": 8086,
    "contents_in_prompt": true,
    "relative_path": "../reference/task_contract.json",
    "sha256": "1fd6aaa769867a9dae24c222df1d364c2138786b0e9ae69ba389d594cfc04afe"
  },
  "terminal_action_readout": null,
  "workspace": {
    "authoritative_trajectory_available": false,
    "material_reference": "chemworld_lab.material_information",
    "mcp_server": "chemworld_lab (required, bounded, host-owned)",
    "public_history": "bounded non-authoritative cache",
    "task_contract_reference": "../reference/task_contract.json",
    "transport": "host-owned STDIO MCP; no shell command is required",
    "writable_root": "agent/ (current working directory; optional memory)"
  }
}
```

### 材料与先验JSON

```json
{
  "initial_world_model": {
    "availability": "supplied_incomplete_model",
    "context_contract": {
      "coordinate_center": 0.5,
      "reference_context": {
        "controlled_duration_s": 3540.0,
        "electrolyte_profile": 2,
        "probe_current_mA": 70.0,
        "probe_duration_s": 630.0,
        "probe_potential_V": 1.18,
        "reagent_amount_mol": 0.004,
        "solvent": 1
      },
      "relative_to": [
        "probe_potential_V",
        "probe_current_mA"
      ],
      "target_controls": [
        "controlled_potential_V",
        "controlled_current_mA"
      ]
    },
    "interpretation": "The supplied model may be reliable or shifted. Experimental evidence is authoritative.",
    "locus": "parametric",
    "model": {
      "claim": {
        "directional_axis": "controlled_potential_V",
        "expected_relation": "Relative to the probe and stated reference context, the higher-controlled-potential side should retain balanced performance more reliably than the lower-controlled-potential side."
      },
      "confidence": 0.7,
      "scope_limit": "This is an incomplete local process model. Experimental evidence is authoritative outside the stated context."
    },
    "schema_version": "chemworld-work-ii-initial-world-model-0.2"
  },
  "material_catalog": {
    "catalog_version": "chemworld-public-electrochemical-materials-1.0",
    "electrolyte_profiles": [
      {
        "anonymous_material_id": "electrolyte-E0",
        "display_name": "electrolyte-E0",
        "identity_kind": "anonymous_benchmark_electrolyte_formulation",
        "index": 0,
        "reference_status": "no_real_material_identity_claimed"
      },
      {
        "anonymous_material_id": "electrolyte-E1",
        "display_name": "electrolyte-E1",
        "identity_kind": "anonymous_benchmark_electrolyte_formulation",
        "index": 1,
        "reference_status": "no_real_material_identity_claimed"
      },
      {
        "anonymous_material_id": "electrolyte-E2",
        "display_name": "electrolyte-E2",
        "identity_kind": "anonymous_benchmark_electrolyte_formulation",
        "index": 2,
        "reference_status": "no_real_material_identity_claimed"
      },
      {
        "anonymous_material_id": "electrolyte-E3",
        "display_name": "electrolyte-E3",
        "identity_kind": "anonymous_benchmark_electrolyte_formulation",
        "index": 3,
        "reference_status": "no_real_material_identity_claimed"
      }
    ],
    "interpretation_policy": "The solvent and electrolyte IDs are benchmark-only labels. They do not identify real substances or formulations, and their action indices reveal no hidden world-specific material residuals.",
    "presentation": "anonymous_material_ids",
    "reagent": {
      "canonical_id": "limiting_reagent",
      "display_name": "Anonymous limiting reagent",
      "identity_kind": "mechanism_role",
      "reference_status": "mechanism_specific_not_a_real_identity"
    },
    "solvents": [
      {
        "anonymous_material_id": "solvent-S0",
        "display_name": "solvent-S0",
        "identity_kind": "anonymous_benchmark_solvent_medium",
        "index": 0,
        "reference_status": "no_real_material_identity_claimed"
      },
      {
        "anonymous_material_id": "solvent-S1",
        "display_name": "solvent-S1",
        "identity_kind": "anonymous_benchmark_solvent_medium",
        "index": 1,
        "reference_status": "no_real_material_identity_claimed"
      },
      {
        "anonymous_material_id": "solvent-S2",
        "display_name": "solvent-S2",
        "identity_kind": "anonymous_benchmark_solvent_medium",
        "index": 2,
        "reference_status": "no_real_material_identity_claimed"
      },
      {
        "anonymous_material_id": "solvent-S3",
        "display_name": "solvent-S3",
        "identity_kind": "anonymous_benchmark_solvent_medium",
        "index": 3,
        "reference_status": "no_real_material_identity_claimed"
      }
    ]
  },
  "material_information": {
    "availability": "opaque_identifiers_only",
    "dossier": null,
    "interpretation": "No task-specific nominal property dossier is supplied. Experimental evidence is authoritative."
  },
  "schema_version": "chemworld-env-owned-material-information-reference-0.1"
}
```

### 检查点合同JSON

```json
{
  "allowed_feature_ids": [
    "electrolyte_profile",
    "solvent",
    "reagent_amount_mol",
    "probe_potential_V",
    "probe_current_mA",
    "probe_duration_s",
    "controlled_potential_V",
    "controlled_current_mA",
    "controlled_duration_s"
  ],
  "allowed_metric_ids": [
    "selective_product_yield",
    "electrochemical_selectivity",
    "faradaic_efficiency",
    "energy_efficiency",
    "safety_risk",
    "score"
  ],
  "allowed_prior_fields": [
    "controlled_potential_V",
    "controlled_current_mA"
  ],
  "checkpoint_complete_experiments": [
    0,
    2,
    4,
    7,
    10
  ],
  "evidence_catalog": [
    "experiment-1-final-assay",
    "experiment-2-final-assay",
    "experiment-3-final-assay",
    "experiment-4-final-assay",
    "experiment-5-final-assay",
    "experiment-6-final-assay",
    "experiment-7-final-assay",
    "experiment-8-final-assay",
    "experiment-9-final-assay",
    "experiment-10-final-assay"
  ],
  "held_out_queries": [
    {
      "feature_values": {
        "controlled_current_mA": 71.0,
        "controlled_duration_s": 3540.0,
        "controlled_potential_V": 1.2,
        "electrolyte_profile": 2,
        "probe_current_mA": 70.0,
        "probe_duration_s": 630.0,
        "probe_potential_V": 1.18,
        "reagent_amount_mol": 0.004,
        "solvent": 1
      },
      "metric_ids": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "energy_efficiency",
        "safety_risk",
        "score"
      ],
      "query_id": "p05-i05"
    },
    {
      "feature_values": {
        "controlled_current_mA": 29.4,
        "controlled_duration_s": 3540.0,
        "controlled_potential_V": 0.8949999999999999,
        "electrolyte_profile": 2,
        "probe_current_mA": 70.0,
        "probe_duration_s": 630.0,
        "probe_potential_V": 1.18,
        "reagent_amount_mol": 0.004,
        "solvent": 1
      },
      "metric_ids": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "energy_efficiency",
        "safety_risk",
        "score"
      ],
      "query_id": "p00-i01"
    },
    {
      "feature_values": {
        "controlled_current_mA": 110.6,
        "controlled_duration_s": 3540.0,
        "controlled_potential_V": 0.8949999999999999,
        "electrolyte_profile": 2,
        "probe_current_mA": 70.0,
        "probe_duration_s": 630.0,
        "probe_potential_V": 1.18,
        "reagent_amount_mol": 0.004,
        "solvent": 1
      },
      "metric_ids": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "energy_efficiency",
        "safety_risk",
        "score"
      ],
      "query_id": "p00-i09"
    },
    {
      "feature_values": {
        "controlled_current_mA": 19.5,
        "controlled_duration_s": 3540.0,
        "controlled_potential_V": 1.412,
        "electrolyte_profile": 2,
        "probe_current_mA": 70.0,
        "probe_duration_s": 630.0,
        "probe_potential_V": 1.18,
        "reagent_amount_mol": 0.004,
        "solvent": 1
      },
      "metric_ids": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "energy_efficiency",
        "safety_risk",
        "score"
      ],
      "query_id": "p09-i00"
    },
    {
      "feature_values": {
        "controlled_current_mA": 120.5,
        "controlled_duration_s": 3540.0,
        "controlled_potential_V": 1.412,
        "electrolyte_profile": 2,
        "probe_current_mA": 70.0,
        "probe_duration_s": 630.0,
        "probe_potential_V": 1.18,
        "reagent_amount_mol": 0.004,
        "solvent": 1
      },
      "metric_ids": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "energy_efficiency",
        "safety_risk",
        "score"
      ],
      "query_id": "p09-i10"
    },
    {
      "feature_values": {
        "controlled_current_mA": 71.0,
        "controlled_duration_s": 3540.0,
        "controlled_potential_V": 1.4649999999999999,
        "electrolyte_profile": 2,
        "probe_current_mA": 70.0,
        "probe_duration_s": 630.0,
        "probe_potential_V": 1.18,
        "reagent_amount_mol": 0.004,
        "solvent": 1
      },
      "metric_ids": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "energy_efficiency",
        "safety_risk",
        "score"
      ],
      "query_id": "p10-i05"
    },
    {
      "feature_values": {
        "controlled_current_mA": 71.0,
        "controlled_duration_s": 3540.0,
        "controlled_potential_V": 0.8949999999999999,
        "electrolyte_profile": 2,
        "probe_current_mA": 70.0,
        "probe_duration_s": 630.0,
        "probe_potential_V": 1.18,
        "reagent_amount_mol": 0.004,
        "solvent": 1
      },
      "metric_ids": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "energy_efficiency",
        "safety_risk",
        "score"
      ],
      "query_id": "p00-i05"
    },
    {
      "feature_values": {
        "controlled_current_mA": 29.4,
        "controlled_duration_s": 3540.0,
        "controlled_potential_V": 1.107,
        "electrolyte_profile": 2,
        "probe_current_mA": 70.0,
        "probe_duration_s": 630.0,
        "probe_potential_V": 1.18,
        "reagent_amount_mol": 0.004,
        "solvent": 1
      },
      "metric_ids": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "energy_efficiency",
        "safety_risk",
        "score"
      ],
      "query_id": "p04-i01"
    },
    {
      "feature_values": {
        "controlled_current_mA": 110.6,
        "controlled_duration_s": 3540.0,
        "controlled_potential_V": 1.107,
        "electrolyte_profile": 2,
        "probe_current_mA": 70.0,
        "probe_duration_s": 630.0,
        "probe_potential_V": 1.18,
        "reagent_amount_mol": 0.004,
        "solvent": 1
      },
      "metric_ids": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "energy_efficiency",
        "safety_risk",
        "score"
      ],
      "query_id": "p04-i09"
    },
    {
      "feature_values": {
        "controlled_current_mA": 49.2,
        "controlled_duration_s": 3540.0,
        "controlled_potential_V": 1.001,
        "electrolyte_profile": 2,
        "probe_current_mA": 70.0,
        "probe_duration_s": 630.0,
        "probe_potential_V": 1.18,
        "reagent_amount_mol": 0.004,
        "solvent": 1
      },
      "metric_ids": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "energy_efficiency",
        "safety_risk",
        "score"
      ],
      "query_id": "p02-i03"
    },
    {
      "feature_values": {
        "controlled_current_mA": 90.8,
        "controlled_duration_s": 3540.0,
        "controlled_potential_V": 1.001,
        "electrolyte_profile": 2,
        "probe_current_mA": 70.0,
        "probe_duration_s": 630.0,
        "probe_potential_V": 1.18,
        "reagent_amount_mol": 0.004,
        "solvent": 1
      },
      "metric_ids": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "energy_efficiency",
        "safety_risk",
        "score"
      ],
      "query_id": "p02-i07"
    },
    {
      "feature_values": {
        "controlled_current_mA": 39.3,
        "controlled_duration_s": 3540.0,
        "controlled_potential_V": 1.3059999999999998,
        "electrolyte_profile": 2,
        "probe_current_mA": 70.0,
        "probe_duration_s": 630.0,
        "probe_potential_V": 1.18,
        "reagent_amount_mol": 0.004,
        "solvent": 1
      },
      "metric_ids": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "energy_efficiency",
        "safety_risk",
        "score"
      ],
      "query_id": "p07-i02"
    },
    {
      "feature_values": {
        "controlled_current_mA": 90.8,
        "controlled_duration_s": 3540.0,
        "controlled_potential_V": 1.3059999999999998,
        "electrolyte_profile": 2,
        "probe_current_mA": 70.0,
        "probe_duration_s": 630.0,
        "probe_potential_V": 1.18,
        "reagent_amount_mol": 0.004,
        "solvent": 1
      },
      "metric_ids": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "energy_efficiency",
        "safety_risk",
        "score"
      ],
      "query_id": "p07-i07"
    },
    {
      "feature_values": {
        "controlled_current_mA": 49.2,
        "controlled_duration_s": 3540.0,
        "controlled_potential_V": 1.412,
        "electrolyte_profile": 2,
        "probe_current_mA": 70.0,
        "probe_duration_s": 630.0,
        "probe_potential_V": 1.18,
        "reagent_amount_mol": 0.004,
        "solvent": 1
      },
      "metric_ids": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "energy_efficiency",
        "safety_risk",
        "score"
      ],
      "query_id": "p09-i03"
    },
    {
      "feature_values": {
        "controlled_current_mA": 49.2,
        "controlled_duration_s": 3540.0,
        "controlled_potential_V": 0.8949999999999999,
        "electrolyte_profile": 2,
        "probe_current_mA": 70.0,
        "probe_duration_s": 630.0,
        "probe_potential_V": 1.18,
        "reagent_amount_mol": 0.004,
        "solvent": 1
      },
      "metric_ids": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "energy_efficiency",
        "safety_risk",
        "score"
      ],
      "query_id": "p00-i03"
    },
    {
      "feature_values": {
        "controlled_current_mA": 90.8,
        "controlled_duration_s": 3540.0,
        "controlled_potential_V": 0.8949999999999999,
        "electrolyte_profile": 2,
        "probe_current_mA": 70.0,
        "probe_duration_s": 630.0,
        "probe_potential_V": 1.18,
        "reagent_amount_mol": 0.004,
        "solvent": 1
      },
      "metric_ids": [
        "selective_product_yield",
        "electrochemical_selectivity",
        "faradaic_efficiency",
        "energy_efficiency",
        "safety_risk",
        "score"
      ],
      "query_id": "p00-i07"
    }
  ],
  "nominal_information_available": true,
  "physical_experiment_selection_authority": "participant",
  "query_metric_contract": {
    "p00-i01": [
      "selective_product_yield",
      "electrochemical_selectivity",
      "faradaic_efficiency",
      "energy_efficiency",
      "safety_risk",
      "score"
    ],
    "p00-i03": [
      "selective_product_yield",
      "electrochemical_selectivity",
      "faradaic_efficiency",
      "energy_efficiency",
      "safety_risk",
      "score"
    ],
    "p00-i05": [
      "selective_product_yield",
      "electrochemical_selectivity",
      "faradaic_efficiency",
      "energy_efficiency",
      "safety_risk",
      "score"
    ],
    "p00-i07": [
      "selective_product_yield",
      "electrochemical_selectivity",
      "faradaic_efficiency",
      "energy_efficiency",
      "safety_risk",
      "score"
    ],
    "p00-i09": [
      "selective_product_yield",
      "electrochemical_selectivity",
      "faradaic_efficiency",
      "energy_efficiency",
      "safety_risk",
      "score"
    ],
    "p02-i03": [
      "selective_product_yield",
      "electrochemical_selectivity",
      "faradaic_efficiency",
      "energy_efficiency",
      "safety_risk",
      "score"
    ],
    "p02-i07": [
      "selective_product_yield",
      "electrochemical_selectivity",
      "faradaic_efficiency",
      "energy_efficiency",
      "safety_risk",
      "score"
    ],
    "p04-i01": [
      "selective_product_yield",
      "electrochemical_selectivity",
      "faradaic_efficiency",
      "energy_efficiency",
      "safety_risk",
      "score"
    ],
    "p04-i09": [
      "selective_product_yield",
      "electrochemical_selectivity",
      "faradaic_efficiency",
      "energy_efficiency",
      "safety_risk",
      "score"
    ],
    "p05-i05": [
      "selective_product_yield",
      "electrochemical_selectivity",
      "faradaic_efficiency",
      "energy_efficiency",
      "safety_risk",
      "score"
    ],
    "p07-i02": [
      "selective_product_yield",
      "electrochemical_selectivity",
      "faradaic_efficiency",
      "energy_efficiency",
      "safety_risk",
      "score"
    ],
    "p07-i07": [
      "selective_product_yield",
      "electrochemical_selectivity",
      "faradaic_efficiency",
      "energy_efficiency",
      "safety_risk",
      "score"
    ],
    "p09-i00": [
      "selective_product_yield",
      "electrochemical_selectivity",
      "faradaic_efficiency",
      "energy_efficiency",
      "safety_risk",
      "score"
    ],
    "p09-i03": [
      "selective_product_yield",
      "electrochemical_selectivity",
      "faradaic_efficiency",
      "energy_efficiency",
      "safety_risk",
      "score"
    ],
    "p09-i10": [
      "selective_product_yield",
      "electrochemical_selectivity",
      "faradaic_efficiency",
      "energy_efficiency",
      "safety_risk",
      "score"
    ],
    "p10-i05": [
      "selective_product_yield",
      "electrochemical_selectivity",
      "faradaic_efficiency",
      "energy_efficiency",
      "safety_risk",
      "score"
    ]
  },
  "schema_version": "chemworld-work-ii-campaign-checkpoint-contract-0.1",
  "snapshot_stages": [
    "pre_evidence",
    "after_experiment_2",
    "after_experiment_4",
    "after_experiment_7",
    "final"
  ],
  "snapshot_submission_protocol": {
    "finalize_requires_exact_full_snapshot": true,
    "law_pages": [
      {
        "metric_ids": [
          "selective_product_yield",
          "electrochemical_selectivity"
        ],
        "page_id": "laws-001"
      },
      {
        "metric_ids": [
          "faradaic_efficiency",
          "energy_efficiency"
        ],
        "page_id": "laws-002"
      },
      {
        "metric_ids": [
          "safety_risk",
          "score"
        ],
        "page_id": "laws-003"
      }
    ],
    "partial_draft_counts_as_checkpoint": false,
    "participant_payload_auto_repair": false,
    "prediction_pages": [
      {
        "page_id": "predictions-001",
        "query_metric_contract": {
          "p00-i01": [
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score"
          ],
          "p00-i09": [
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score"
          ],
          "p05-i05": [
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score"
          ],
          "p09-i00": [
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score"
          ]
        }
      },
      {
        "page_id": "predictions-002",
        "query_metric_contract": {
          "p00-i05": [
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score"
          ],
          "p04-i01": [
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score"
          ],
          "p09-i10": [
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score"
          ],
          "p10-i05": [
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score"
          ]
        }
      },
      {
        "page_id": "predictions-003",
        "query_metric_contract": {
          "p02-i03": [
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score"
          ],
          "p02-i07": [
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score"
          ],
          "p04-i09": [
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score"
          ],
          "p07-i02": [
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score"
          ]
        }
      },
      {
        "page_id": "predictions-004",
        "query_metric_contract": {
          "p00-i03": [
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score"
          ],
          "p00-i07": [
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score"
          ],
          "p07-i07": [
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score"
          ],
          "p09-i03": [
            "selective_product_yield",
            "electrochemical_selectivity",
            "faradaic_efficiency",
            "energy_efficiency",
            "safety_risk",
            "score"
          ]
        }
      }
    ],
    "protocol": "staged_pages_v1",
    "submission_order": [
      "predictions-001",
      "predictions-002",
      "predictions-003",
      "predictions-004",
      "laws-001",
      "laws-002",
      "laws-003"
    ]
  },
  "stage_labels_are_checkpoint_ids_only": true
}
```


来源定位：历史源码提交 `5437b5e85233fd18effa88039a23bb82b074f0a0`；本例为公共测试世界，不含私有种子。
本地会话记录：[summary](../../../runs/development/work-ii-w2-62-codex-c2-full-replication-v0.1-20260902/cells/A_P--electrochemical-conversion--seed973419928--misindexed_nominal/summary.json)、[trajectory](../../../runs/development/work-ii-w2-62-codex-c2-full-replication-v0.1-20260902/cells/A_P--electrochemical-conversion--seed973419928--misindexed_nominal/trajectory.jsonl)。
