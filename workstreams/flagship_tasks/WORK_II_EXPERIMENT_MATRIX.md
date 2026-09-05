# Work II 实验矩阵与贡献路线

更新：2026-09-05。任务状态由 [WORK_II_TODOLIST.md](WORK_II_TODOLIST.md) 管理。
本文是可审核的设计与规模建议，**未冻结、未执行，不授权provider或正式生产**。
已有块按原protocol/note和 [当前绑定](../../configs/current.json) 解释，不按新指标改写旧主结果。

## 1. 当前证据处置

| 证据 | 当前口径 | 论文角色与处置 |
| --- | --- | --- |
| Work I | 64 reference units、1,786 recipes、52 generated，含8 identity-new | 保持冻结的软件模型资格；不声称一般流程图编译或湿实验效度 |
| C2双模型 | 各135 scheduled；DeepSeek/GPT完成121/126，laws135/129，blind可评分121/126 | 主文：预测、显式规律与incumbent推荐；保留任务差异和原缺失规则 |
| A-P matched evidence | 每模型5 worlds、15 sessions、30 turns | 反证后条件性数值响应；缺少turn-matched no-packet控制 |
| B2及low reasoning | 三配置各15 sessions，错误组expression均0/5；存在精确alias | 补充测量诊断；不重复追求结构识别正结果 |
| B3双模型 | 各30 scheduled；DeepSeek17完成/13 schema失败，GPT30完成；joint0/30与5/30；固定机会分母gain成功均0/18 | 主文短述受限函数形式识别；不外推一般因果图恢复 |
| W2-50/64 | DeepSeek45 scheduled、42 rankings；law Top-1 0/45，participant11/45，follow-law12/42 | 主文核心动机；显式law不等于内部推理，尚未随机干预 |
| W2-61 | 每模型180 slots、45 strata；autonomy-minus-none regret -0.0913/+0.1102，两区间跨零；yoked完成10/42与24/26 | development系统策略估计；保留失败，不称纯取证或因果中介效应 |
| W2-55 | 135同域prediction states可用full schema拟合；连续law/action分析 | 表示容量诊断，不是未见条件规律恢复 |
| W2-51/52/53 | 原五条件无participant效果；16个完成unit-version的rank/action复核 | 补充评价诊断；关闭旧oracle扩网格路线 |
| private、组合迁移、独立后端 | 未形成对应当前结果 | 不宣称已验证，不恢复旧累计C1–C4门禁 |

experiments均指虚拟化学实验。worlds、sessions、调用、truth/replay不是可互换分母。
同世界重复或大量queries不能包装为大样本泛化。

## 2. 必做与条件扩展

| 块 | 问题与对照 | 主读出 | 决策 |
| --- | --- | --- | --- |
| M0 测量/执行面 | 精简typed提交；participant/truth/blind共用世界描述；正确计算和错误字段控制 | 真实路径一致性、提交负担、可评分率、失败分类 | 新数据前必做 |
| M1 表示×决策器 | 原始Agent law / 同公开证据拟合law × 自由选择 / 确定性执行器 | regret、近最优率、因子对比、成本 | 核心新增，定位可修复条件 |
| M2 取证价值 | Agent选择 / 固定LHS或预先固定简单主动设计；同预算、证据格式和下游决策器 | 每单位实验成本的未见决策损失 | 仅当主张acquisition因果价值时必做 |
| M3 知识迁移 | none / raw evidence / Agent law / fitted artifact；fresh receiver与新条件 | 零查询决策质量；预算扩展时的实验节省 | spotlight方法路线的优先扩展 |
| M4 外部复核 | 一个独立求解器或参考数据上的相同决策问题 | 效应方向、适用域与成本 | 高价值加分，近期暂缓 |

M0不是科学结果。M1完成且不确定性可解释后，优先选择M3；M2只有在取证主张必要时启动。
近期不铺满所有loci×模型×任务；追加模型、旧oracle网格、PASS图和重复checkpoint不属必做。

M0交付应包含：同一world描述在participant/truth/blind的真实执行路径一致；
合法law和合法candidate只需一次最小提交，不重复要求runner可推导的status字段；
公开开发fixture上的reference计算、候选效用与exact replay一致；失败可分类且保留。
所有拟合开发只用公开证据。以公开开发fixture确定可学习范围和成本，不能根据正式world
的Agent表现或私有候选标签挑选正式任务、拟合器或样本。科学字段错误仍算失败。

## 3. M1：最小可辨别干预

### 问题与单位

固定公开证据和完整ActionPlans，干预可观察的artifact及决策规则。
估计属于agent system，不直接识别内部belief或心理因果中介。

建议用electrochemical-conversion与reaction-to-crystallization开发。它们是候选，须在M0
确认公开证据、预算和决策机会；prospective执行开始后不能换world或按结果选任务。
旧partition exponent-crossover路线不恢复；使用该任务的新实验须有不同问题和独立note。

规划：2 tasks × 5 worlds × 2 models × 2独立模型重复 = 40来源状态。
仍只有10个独立task–world clusters；模型重复描述采样变异。
每world由事前固定、无需私有真值的12次实验形成公开证据包，两模型和重复共享同一包。
来源Agent提交law后再揭示terminal候选。合法函数类、拟合器和处理失败规则事前固定。

### 四条件

| 条件 | 显式artifact | 终端选择 |
| --- | --- | --- |
| L-A | 来源Agent生成law | fresh同配置Agent选择candidate ID |
| L-X | 同一条law | 统一确定性执行器计算候选效用并选择 |
| F-A | 仅用同一公开证据拟合的law | 与L-A相同协议的fresh Agent |
| F-X | 同一拟合law | 与L-X相同执行器 |

自由选择条件接收同一证据、计划和预算，只有artifact变化。算法条件不得读私有规律、
候选truth或标签。来源law先封存，不因选择结果改写。执行器/自由选择对比是决策规则替换，
包含计算方式差异，不能称裸模型“是否使用law”的中介效应。

主对比建议F-X相对L-X的regret差，衡量固定执行器下表示的决策价值。
L-X相对L-A衡量固定artifact下规则替换；其他因子对比与交互为secondary并控制多重比较。
最终主对比必须在数据前确定。私有真值只用于离线计分和特权参考，直接评价8个候选，
不以全局拟合排序相关性替代真实决策参考；特权参考不是公平学习baseline。

原始law与拟合law共用输入变量、输出效用、合法函数类和容量上限；额外模型容量属于另一项干预。
与拟合器共享公开证据的简单检索/最近邻决策和随机选择提供解释基线，默认无需provider；
其固定实现与计数在note中纳入，不能看到M1结果后才选择最弱对手。

结果解释事前分开：L-X优于L-A说明规则替换有价值；F-X优于L-X说明固定规则下artifact有价值；
F-X改善而F-A不改善提示自由选择限制知识部署；预测误差下降而regret不下降则限定表示收益。
这些模式都须带逐world差异和区间，不按单个p值选择故事，也不等同内部心理机制。

### 指标、成本与判定

- Primary：同world候选的效用损失；同时报告原量纲差和事前尺度的normalized regret。
  尺度及范围退化规则在M0固定，不使用事后极小max-min范围制造巨大归一化损失。
- Secondary：epsilon-optimal率、约束违反、候选效用预测误差、Agent/执行器一致率。
  epsilon按实际效用或噪声分辨率事前固定，近似并列不强行计错。
- 分别记录公开实验、样品/仪器/时间、provider input/output/cache、CPU与wall time。
  新方法要与同公开证据的简单拟合、检索或经典优化控制比较。
- scheduled主分析同时呈现可用性与损失；非法law/缺失选择按冻结规则入分母，
  完成者和适当界限分析仅作敏感性。
- task-stratified world-cluster差异和区间为主，展示逐world值。重复模型调用不增加独立n。
  负结果和不显著结果仍完整保留，不触发追加seed、更换任务或重跑至正。
- exposed cohort只用于开发；正式块另冻结world identities，参数未见与拓扑未见分别命名。

### 规划分母（不是冻结合同）

| 项目 | 数量 |
| --- | ---: |
| 独立task–world clusters | 10 |
| 来源law生成sessions | 40 |
| 四条件评价单位 | 160 |
| 其中fresh Agent终端sessions | 80 |
| 其中provider-free执行器选择 | 80 |
| 新provider sessions合计 | 120 |
| 公开证据虚拟实验 | 10 × 12 = 120 |
| evaluator候选truth | 10 × 8 = 80 |
| 对应物理路径exact replay | 120 + 80 = 200 |
| 简单最近邻与均匀随机基线的world级决策汇总 | 10 × 2 = 20；模型/重复共享 |

共200个新虚拟物理主执行及200个replay，160个条件评价不能再加算成160次物理实验。
两项解释基线复用同一证据和候选truth，不增加provider或物理执行。
重试不是新样本。token/货币上限与ETA待M0真实路径成本校准，不沿用历史小时数或虚构费用。

## 4. M2与M3条件扩展

M2规划：2 tasks × 5 worlds × 2 models × 2 repeats × 2策略 = 80 campaign slots，
每个至多12次实验，合计960个虚拟实验机会。不同策略使用同一下游推断/决策器，
receiver轮次和证据格式匹配，区分取证与额外思考/上下文/转写失败。
增加经典策略必须在启动前重新核定矩阵。

M3先做零追加实验的portability：2 target tasks × 5 fresh target worlds × 2 models ×
2 repeats × 4信息条件 = 160 fresh recipient sessions。来源artifact在target揭示前封存。
target参数/初态如何变化事先写清；同任务换对话是context portability，同族新参数是
within-family transfer，真正新连接才是compositional transfer，不能混称。
none控制提示脚手架；raw evidence与artifact同时匹配字数和完整语义通常不可兼得，
需报告所估计的信息部署/压缩策略和成本。

声称节省实验还需另行固定0/1/2/4测量预算或同一4步学习曲线：
160 × 4 = 640为最大追加机会。零查询版本只支持初始决策迁移，不支持未经测量的实验节省。
可共享M1来源artifact，不共享未声明target观测、不把来源状态计作新独立样本。

## 5. Spotlight贡献空间

这是研究判断，不能估计或保证录用概率。2027 reviewer guide于2026-09-05为404；
[2026 reviewer guide](https://iclr.cc/Conferences/2026/ReviewerGuide)仅用于理解既往重视
新知识、科学严谨与社区价值的原则，不当作2027规则。

| 层次 | 已有基础 | 所需增量 |
| --- | --- | --- |
| 有界可信经验论文 | 双模型描述性差异、完整失败处理 | 收紧故事、统一证据层级 |
| 有竞争力的机制/方法论文 | law/action缺口明确，原因未干预 | M1定位可修复环节；公开证据可学的方法及消融 |
| spotlight空间较大 | 尚未形成此证据组合 | M1给出稳健实质改善或强可解释边界；M3离开原对话仍有用；任务/模型复核及成本 |
| 化学外部效度更强 | 内部模型与部分物化参考能力 | M4独立后端/参考数据复核 |

“预测误差不等于决策损失”已有成熟研究：
[Smart Predict, then Optimize](https://arxiv.org/abs/1710.08005)、
[Decision-Focused Learning](https://doi.org/10.1609/aaai.v33i01.33011658)。
拟合器加argmax、标准regret界或增加模型数本身不足以构成新贡献。
ChemWorld的机会是自主实验、错误初始描述、知识压缩、操作约束与新条件决策的结合：
提出可复用的测量/干预方法，证明其有效条件和失败边界，并超过简单公开数据baseline。
不强制产出正结果，更不通过删除失败来制造方法优势。

## 6. 时间与停止规则

2026-09-05核实官方[CFP](https://iclr.cc/Conferences/2027/CallForPapers)和
[Author Guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines)：
摘要9月18日、全文9月25日23:59 AoE；北京时间为9月19日和26日19:59，review正文9页。

建议排期（不是执行承诺）：
- 9月5–8日：本轮收束；M0接口、可识别性与成本准备。
- 9月9–15日：若已授权且稳定，优先M1；测量仍不可靠则继续开发。
- 9月16–20日：按M1完成状态选择M3独立扩展，M2/M4默认不抢占主块。
- 9月21–25日：集中写作、图表、匿名复现和一次集成验收；用户实际提交。

M1不支持预期改善时保留负结果并收窄稿件。不能因日期更换world、降低epsilon、
放宽科学字段、补样本至显著或升级development evidence。投稿版本由已完成证据决定。
