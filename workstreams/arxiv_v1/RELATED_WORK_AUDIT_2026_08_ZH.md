# ChemWorld 第一版 arXiv：相关工作公允审计与生态位边界

状态：working evidence audit，2026-08-02

主文稿：`paper/experimental_intelligence_v1_manuscript.md`

证据范围：优先使用论文原文、出版商页面和正式会议页面；预印本明确标为 preprint。
本文档比较的是各系统**实际回答的研究问题**，不是用一个总分判断谁“更先进”。

## 1. 审计后的定位

ChemWorld 不应再声称：

- 首个交互式科学发现环境；
- 首个虚拟化学实验室；
- 首个隐藏规律或主动机制发现 benchmark；
- 首个测量科学 Agent 过程而非终点的工作；
- 首个在未知物理系统中自由选择实验并恢复规律的 Agent；
- 首个长程或端到端自主科学发现系统；
- 最完整、近乎无限或可以生成任意物理规律的化学世界；
- 比真实自主实验室、机器人系统或主动学习算法“更强”。

截至 2026-08-02，最有价值且可守的定位是：

> **ChemWorld 是研究化学实验智能的受控测量装置：Agent 在有状态、部分可观测的
> 化学/化工过程中自主选择逐步操作和表征，承担材料、仪器、失败与生命周期后果；
> 研究者则可以在保持其他身份不变时干预先验信息或物理世界，并通过不可覆盖轨迹、
> 资源账本与精确重放测量发现、保留、回撤和恢复。**

这里，world 的可变性是实验控制能力，不是论文必须证明的最终对象；环境规模是基础设施，
不是故事本身。故事的对象是 **experimenting agent 的可测行为**。

## 2. 哪些近期工作已经占据了哪些主张

### 2.1 化学工具 Agent 与真实自主实验室

#### Coscientist

Boiko 等人在 Nature 2023 展示了由 GPT-4 驱动的多模块系统，可检索网页和仪器文档、
执行代码、调用液体处理器与云实验室，并完成钯催化偶联优化。

- 它比 ChemWorld 强的地方：真实硬件与云实验室执行；从自然语言目标到现实实验的端到端展示；
  更直接的现实化学有效性。
- 它没有回答的问题：如何在相同隐藏物理系统中反复克隆条件，仅改变先验或模型轨迹；
  如何以发现、保留、回撤、恢复等冻结指标估计 Agent 的实验行为。
- 与 ChemWorld 的关系：互补，不是同一个 benchmark。Coscientist 证明 Agent 可以接入实验室；
  ChemWorld 研究接入后表现出的实验智能是否稳定、如何受信息和物理后果影响。

来源：<https://doi.org/10.1038/s41586-023-06792-0>。

#### ChemCrow

Bran 等人在 Nature Machine Intelligence 2024 将 GPT-4 与 18 个化学工具结合，覆盖合成、
药物发现和材料设计，并连接机器人合成。

- 它比 ChemWorld 强的地方：工具广度、真实合成与专家评价、跨多类化学知识任务。
- 它没有回答的问题：工具调用成功是否对应稳定的实验学习；中间证据是否改变后续物理操作；
  在严格配对的信息干预下，成功与理解能否分离。
- 原论文自己指出：任务数量有限，闭源模型单次结果的可重复性困难。
- 与 ChemWorld 的关系：ChemCrow 的核心对象是化学 Agent 与工具增强；ChemWorld 的核心对象是
  对 Agent 实验行为做可重复干预和测量。

来源：<https://doi.org/10.1038/s42256-024-00832-8>。

#### A-Lab、移动机器人和近期机器人化学压力测试

A-Lab 在 Nature 2023 展示无机粉末固相合成的自主实验室；移动机器人工作在 Nature 2024
展示机器人跨合成与表征平台执行探索化学。A-Lab GPSS（2026 preprint）进一步在 glovebox
中完成 352 个 air-sensitive lithium-halide spinel 样品的长程 campaign，并从 proposal traces
区分面向异常局部追问的 abductive strategy 与扩展未探索空间的 inductive strategy。2026-07-25
的机器人压力测试预印本把 45 个机器人
workstations 暴露为技能，在 4,608 次 trials 中直接评估物理可执行性和反馈后重规划；只有
3.3% trials 产生专家认可的可执行 workflow，最佳系统为 28.1%，且五轮反馈主要引发局部调整，
没有 workflow-level replanning 或分析方法重设计。

- 它们比 ChemWorld 强的地方：真实物理执行、硬件异质性、操作安全、部署有效性和
  sim-to-real/real-world evidence。
- 它们的规模限制是物理实验成本与硬件可用性带来的设计约束，而不是研究缺陷。
- ChemWorld 的互补价值：低成本克隆同一物理身份、严格配对信息条件、大量独立轨迹、
  保存失败后果和精确反事实重放。
- 重要主张边界：2026 机器人压力测试已经使用“make scientific agency measurable”这一思想；
  A-Lab GPSS 已经分析 Agent 的实验提议策略。ChemWorld 不能把这两件事本身写成首创。

来源：
<https://doi.org/10.1038/s41586-023-06734-w>、
<https://doi.org/10.1038/s41586-024-08173-7>、
<https://arxiv.org/abs/2604.11957>、
<https://arxiv.org/abs/2607.23045>。

#### ORGANA 与 ChemAgents

ORGANA（Matter 2025）由自然语言目标生成长程计划，以视觉反馈执行溶解度、pH、重结晶和电化学
任务，并行完成 19 步 quinone characterization workflow。ChemAgents（JACS 2025）用分层多
Agent 与文献、protocol、model 和 automated-lab 资源完成六类递增复杂度任务，并迁移到第七个
机器人有机化学实验室执行光催化反应。

- 它们比 ChemWorld 强的地方：真实机器人感知与动作、多任务化学覆盖、并行调度、人与系统交互
  评价，以及跨实验室适配。
- ChemWorld 的差异：不是证明通用编排可以驱动多个现实流程，而是对相同隐藏化学身份进行
  受控干预，问证据使用、发现后保留和失败后恢复是否跨 fresh trajectories 稳定。
- 主张边界：long-horizon chemical operations、multi-agent laboratory orchestration 和跨任务
  真实执行都已有强先例，不能作为第一版的独占标题。

来源：<https://doi.org/10.1016/j.matt.2024.10.015>、
<https://doi.org/10.1021/jacs.4c17738>。

#### AutoLabs

AutoLabs 已于 2026 年在 Scientific Reports 正式发表。它把自然语言实验说明转换为高通量液体
处理器 protocol，通过多 Agent、计算工具与自纠错提高程序准确性，并在五类 benchmark 实验、
20 种配置上做系统消融；复杂多板合成上最强配置的步骤 F1 超过 0.89。

- 它比 ChemWorld 强的地方：protocol generation 的系统架构消融和面向硬件的定量正确性。
- 相对边界：它主要测“能否把已给定目标和步骤编译成正确 protocol”，不是 Agent 在未知
  化学过程中自主选择实验、表征并从后果中更新策略。
- 公允限制：其实证只覆盖 Big Kahuna 的平台约束和硬件文件生成，原文也明确将其解释为该平台
  的 case study；这不是对其 protocol-generation 贡献的否定。

来源：<https://doi.org/10.1038/s41598-026-45593-z>。

#### RoboChem-Flex

RoboChem-Flex（Nature Synthesis 2026）以约 5,000 美元的基础配置、开源 Python 控制、模块化
硬件和 Bayesian optimization 支持 fully closed-loop 或 human-in-the-loop 反应优化，并在
光催化、生物催化、热交叉偶联和不对称催化等六个 case studies 中展示单目标、多目标与迁移学习。

- 它比 ChemWorld 强的地方：真实反应、在线 NMR/UHPLC-MS/Raman 兼容、可扩展验证、低成本
  开放硬件以及跨反应类型的闭环部署证据。
- 相对边界：其研究问题是如何低成本、可靠地优化真实反应；不是在克隆的物理身份中随机化
  Agent 先验、复现实验策略表型。固定 workflow 和 BO 主导的条件选择也不同于 G2 的逐操作自主权。
- 公允表述：真实系统受化学与硬件约束不是“局限”或“缺陷”；它回答的是 ChemWorld 当前
  完全不能回答的现实有效性问题。

来源：<https://doi.org/10.1038/s44160-026-01053-0>。

#### Co-Scientist 与 Robin

Co-Scientist（Nature 2026）以多 Agent tournament、批判和演化过程扩展 test-time compute，
生成并排序生物医学假设，在专家参与下完成三类湿实验验证。Robin（Nature 2026）把文献检索、
假设生成、实验建议与新实验数据的自主分析连成连续反馈环，识别并验证候选治疗药物；其湿实验
由研究者按 human-generated protocol 执行，再把数据交还 Agent。

- 它们比 ChemWorld 强的地方：大规模文献综合、生物医学假设新颖性、真实湿实验验证、专业数据
  分析，以及对有意义科学结论的直接证据。
- ChemWorld 的差异：Agent 直接控制样品从加料到终点检测的 primitive lifecycle；研究者可克隆
  同一物理身份并干预先验条件，以新轨迹估计行为差异。Co-Scientist/Robin 的核心对象是高质量
  假设及分析，不是固定物理身份下的实验操作表型。
- 公允表述：不能把 ChemWorld 当前的 synthetic-world 结果写成比这两项工作的现实发现“更深”；
  也不能把它们写成完全自主湿实验室，因为实验执行仍有人类和专家在环。

来源：<https://doi.org/10.1038/s41586-026-10644-y>、
<https://doi.org/10.1038/s41586-026-10652-y>。

#### 可学习仪器 Agent 与 X-ray scientist

Vriza 等人（npj Computational Materials 2026）让多 Agent 编排 X-ray nanoprobe 与材料机器人，
并把人类操作指导写入可检索长期记忆。Chen 等人（Nature Machine Intelligence 2026）让 Agent
在六圆衍射仪的虚拟 beamline 中逐步选择命令、读取 detector/scan 结果并适应异常，随后把相同
工作流部署到真实同步辐射 beamline；首次现实演示为安全起见由人类原样转发 Agent 命令。

- 它们比 ChemWorld 强的地方：真实仪器、视觉/多模态反馈、设施级安全约束、sim-to-real 和
  对真实异常的适应。X-ray scientist 也直接证明了“Agent 自主逐步操作仪器”不能作为独占主张。
- ChemWorld 的差异：它把动作自由度用于可复制的实验行为测量，可固定物理身份并改变信息条件；
  上述工作的主要 estimand 是特定仪器任务能否正确完成和人类指导能否改善操作。
- 公允表述：它们的任务专一性来自设施目标和安全边界，不应被贬低为“粗浅实现”。

来源：<https://doi.org/10.1038/s41524-026-02005-0>、
<https://doi.org/10.1038/s42256-026-01261-5>。

### 2.2 虚拟化学实验室、优化与过程控制

#### ChemGymRL

ChemGymRL 提供互联的虚拟反应、萃取、蒸馏等 benches，并允许 RL Agent 进行细粒度操作。
它是 ChemWorld 在“可操作虚拟化学实验室”主张上的最直接先例。

- 它比 ChemWorld 强的地方：成熟的 RL 训练定位、互联 bench 表达、像素/连续控制方向和
  已发表的数字化学环境先例。
- ChemWorld 的新增问题：在相同化学世界中干预 Agent 所获信息；显式允许 Agent 购买表征；
  将材料、仪器、容器、失败与 provider session 分账；将轨迹作为受试对象并做 fresh-trajectory
  replication。
- 安全表述：不能写“first interactive virtual chemistry lab”；可以写 ChemWorld 将
  chemistry-native primitive control 与 controlled behavioral experiments 组合起来。

来源：<https://doi.org/10.1039/D3DD00183K>。

#### Summit、Olympus 与 PC-Gym

Summit 和 Olympus 已系统化 in-silico 反应优化、实验规划与算法比较；PC-Gym 提供含非线性、
扰动和约束的化工过程控制环境，并与 NMPC 比较。

- 它们比 ChemWorld 强的地方：优化/控制基线成熟、算法覆盖更完整、评价目标清晰。
- ChemWorld 不应以 BO 胜负作为主要创新；其增量是让一次“实验”成为有生命周期的行动链，
  并测量 Agent 对信息、表征和失败的响应，而不是只评价 objective regret 或 tracking reward。

来源：<https://doi.org/10.1002/cmtd.202000051>、
<https://arxiv.org/abs/2010.04153>、<https://arxiv.org/abs/2410.22093>。

#### MADE

MADE（ICML 2026）是当前与“可扩展、预算受限、闭环材料发现环境”最直接重叠的工作。Agent 或
算法依次提出材料组成与晶体结构，获得形成能 oracle 反馈，并在凸包发现目标下迭代；框架可组合
生成模型、过滤器与 planner，并在三元、四元和五元体系上比较固定与自适应 pipeline。

- 它比 ChemWorld 强的地方：跨化学体系复杂度的系统算法比较、晶体结构生成生态、稳定材料
  发现指标，以及 end-to-end discovery pipeline 的模块化消融。
- 它占据的主张：ChemWorld 不能再声称首次提供“budget-constrained closed-loop materials
  discovery environment”，也不能只凭 world 数量或 closed loop 区分自己。
- ChemWorld 的差异：MADE 的基本交互单元是“提出候选结构—查询形成能 oracle”；ChemWorld
  的基本单元是带中间状态、表征选择、终止、失败和共享实体资源的实验生命周期。第一版还把
  prior condition 与物理身份分开干预，并在同一世界重复 fresh trajectories。

来源：<https://openreview.net/forum?id=nrXxVDYMMF>、<https://arxiv.org/abs/2601.20996>。

### 2.3 交互式科学发现环境

#### ScienceWorld 与 DiscoveryWorld

DiscoveryWorld（NeurIPS 2024）已有 24 个长程、虚构、多模态科学任务，要求形成假设、设计和
执行实验、分析结果并采取行动，同时用任务完成、过程 report card 和解释知识评价 Agent。
ScienceWorld 更早在文本环境中评价基础科学实验与概念推理。

- 它们比 ChemWorld 强的地方：跨学科发现任务、多模态/空间行动、完整科学循环和更成熟的
  general discovery benchmark 定位。
- ChemWorld 的差异：连续的材料—相—设备—热—过程状态；有类型化学操作和合成仪器包；
  campaign-wide 物理资源；物理、观测和 prior 的严格配对；每一步状态转换精确重放。
- 不能写“首次完整科学发现循环”或“首次虚构科学世界”。

来源：<https://aclanthology.org/2022.emnlp-main.775/>、
<https://proceedings.neurips.cc/paper_files/paper/2024/hash/13836f251823945316ae067350a5c366-Abstract-Datasets_and_Benchmarks_Track.html>。

#### BoxingGym 与 SciGym

BoxingGym 用 10 个生成概率环境评价实验设计和模型发现，并以 expected information gain 与
预测/解释质量评分。SciGym 在 350 个 SBML systems-biology 模型上提供迭代扰动 dry lab。

- 它们比 ChemWorld 强的地方：BoxingGym 的信息论实验设计评价和 SciGym 的动态系统规模。
- 相对边界：它们的主要交互是对生成模型或生物系统提出查询/扰动；ChemWorld 把加料、处理、
  测量、终止和检测组织为带资源后果的化学实验生命周期。

来源：<https://arxiv.org/abs/2501.01540>、<https://arxiv.org/abs/2507.02083>。

### 2.4 2025—2026 主动规律发现与因果机制恢复

#### SciExplorer

SciExplorer（Physical Review X 2026）给 Agent 一个最小的通用工具集，让其在事先未知的机械、
波动和量子多体模型中自由选择数值实验、编写分析代码和形成假设，并评价运动方程或 Hamiltonian
恢复。论文每个系统运行五个独立尝试，也系统报告复杂或非典型模型中的提前收敛、符号/尺度错误和
先验知识依赖。

- 它比 ChemWorld 强的地方：跨物理域的未知系统自由探索、显式规律恢复、标准符号回归比较，
  以及对噪声、工具和模型配置的消融。
- 它占据的主张：ChemWorld 不能声称首次让 LLM Agent 在未知物理世界中自主选择实验、分析并
  恢复规律；“没有 domain-specific blueprint”也不是独占点。
- ChemWorld 的差异：基本行动不是选择数值初始条件后分析轨迹，而是构造有状态化学样品并承担
  库存、容器、仪器、失败和终止后果；第一版的因果设计还配对干预 prior 与物理身份，并以 fresh
  trajectories 测量策略是否复现。

来源：<https://doi.org/10.1103/xnqc-q6nt>。

#### NewtonBench、DiscoverPhysics 与 ActiveSciBench-Chem

NewtonBench（ICLR 2026）包含 12 个物理域、324 个反事实规律任务，要求 Agent 主动探测复杂
模型系统；DiscoverPhysics（2026 preprint）包含 22 个偏离现实的 N-body 世界，同时评价
held-out trajectory prediction 和规律解释；LLM-AutoSciLab/ActiveSciBench-Chem（2026 preprint）
在 57 个酶动力学任务上联合假设生成、主动实验和符号机制恢复。

- 它们比 ChemWorld 强的地方：规律发现任务数量、held-out law evaluation、显式可执行规律输出、
  多模型比较和机制恢复样本效率。当前 ChemWorld 不能声称在这些方面领先。
- ChemWorld 的差异：这些工作主要让 Agent 选择初始条件、变量或 assay query；ChemWorld 的
  G2 Agent 必须自己构造并推进一个有状态实验，选择何时表征、何时继续处理、何时终止和检测，
  并承担共享库存及容器机会成本。
- 世界变化在 ChemWorld 里是控制变量；第一版不把 law discovery 规模当作主结果。

来源：<https://arxiv.org/abs/2510.07172>、
<https://arxiv.org/abs/2605.26087>、<https://arxiv.org/abs/2605.24043>。

#### CausaLab 与 ReplaySCM

CausaLab（2026 preprint）在随机 SCM 中允许观测和干预，并明确分开任务预测与图/结构方程恢复；
ReplaySCM 用 1,300 个 Boolean-SCM worlds 和受限 DSL 评价训练及 held-out intervention replay。

- 它们比 ChemWorld 强的地方：明确的结构真值、机制可识别性分析、可执行机制输出和大规模
  causal generalization。
- ChemWorld 的差异：机制不是离散 SCM 答题层，而嵌在连续、守恒、有生命周期和资源约束的
  化学过程里；第一版同时观察声明知识与实际实验控制是否一致。
- 不能写“首次证明 prediction 不等于 understanding”或“首次 executable mechanism replay”。

来源：<https://arxiv.org/abs/2605.26029>、<https://arxiv.org/abs/2605.08197>。

### 2.5 过程级科学 Agent 评价：概念上最接近的工作

#### AI Agent Behavioral Science

Chen 等人的 2026 年综述已经把 AI agent behavioral science 明确定义为：通过系统观察、干预
设计和理论解释研究 Agent 在情境中的行动、适应与交互。因此 ChemWorld 不能把“对 Agent 做
行为科学”这层一般思想写成首创。

- 它比 ChemWorld 强的地方：跨 individual、multi-agent 和 human-agent settings 的概念整合，
  以及对公平、安全、可解释性和治理问题的广泛连接。
- ChemWorld 的实证增量：为实验化学这一具体行为域提供可执行、可干预、可重放的 apparatus，
  并报告真实运行轨迹，而不是提出一个新的通用行为科学范式。
- 最安全的表述：ChemWorld 是这一范式在 experimenting scientific agents 上的领域化实现，
  其创新落在实验装置和可识别研究设计的组合，不落在“behavioral science”这个词本身。

来源：<https://doi.org/10.1057/s41599-026-07316-7>。

#### AHOIS

AHOIS（2026 preprint）在真实 multimode-fibre optical platform 上把 hypothesis、Socratic
physics criticism、hardware abstraction、system-integrity monitoring 与 quantitative inference
组成闭环。它不仅操作仪器，还提出并验证 random-interference encoding hypothesis、调整稀疏
测量、区分多种失败来源，并对 Socratic critic 做消融。

- 它比 ChemWorld 强的地方：真实高维物理平台、假设级认识论自治、显式反例/证伪标准、机制
  解释质量消融和实质性发现结果。当前 ChemWorld 的 synthetic assays 与低 mechanism F1 不能
  被描述为比它“更深的科学理解”。
- ChemWorld 的差异：固定同一化学世界及材料身份、随机化式先验条件、实体资源收据、状态重放和
  fresh-trajectory replication；AHOIS 的主要因果比较是组件消融，不是跨克隆世界的行为表型复现。
- 正确关系：AHOIS 占据“epistemic autonomy on real instruments”；ChemWorld 占据“controlled
  reproducibility of experimental behavior in executable chemistry”。

来源：<https://arxiv.org/abs/2606.26722>。

#### Qiushi Discovery Engine

Qiushi（2026 preprint）在真实光学平台上以 nonlinear research phases、Meta-Trace memory 和
双层架构维持长程研究。其开放研究报告 145.9M tokens、3,242 次 LLM calls、1,242 次 tool calls、
163 条研究笔记和 44 个脚本，并声称提出及实验证实一种此前未报告的 optical bilinear interaction
机制。

- 它比 ChemWorld 强的地方：真实平台、开放式研究目标、轨迹长度、研究记忆、从假设到机制证据的
  端到端闭环，以及实质性新发现。
- 它占据的主张：ChemWorld 不能声称首个 end-to-end autonomous discovery、首个长程研究轨迹，
  或首个 Agent 自主提出并验证非平凡机制。
- ChemWorld 的差异：Qiushi 以一条大型发现轨迹证明“能做到什么”；ChemWorld 以多个固定身份、
  配对信息干预和 fresh trajectories 问“观察到的实验策略是否由干预造成、是否可重复”。这是
  discovery demonstration 与 controlled measurement apparatus 的区别，不是优劣排序。

来源：<https://arxiv.org/abs/2604.27092>。

#### Corral

Ríos-García 等人的 Corral（2026 preprint）在八个科学环境、超过 25,000 次 Agent runs 上，
同时分解 base model/scaffold 与认识论行为。其结果表明 base model 解释的方差远高于 scaffold；
68% traces 忽略证据，反驳驱动的信念修正只出现在 26%，而结果评价无法揭示这些失败。

- 它比 ChemWorld 强的地方：跨八环境、跨模型/脚手架的大样本过程分析；更直接、系统的
  epistemic-reasoning taxonomy。
- ChemWorld 的差异：评价信号来自外显的化学操作、表征购买、库存消耗、物理失败和随后实验，
  而不主要依赖自然语言 reasoning trace 的认识论编码；还可以通过 nominal/opaque/misindexed
  条件对 prior 进行随机化式干预，并在固定物理世界中重复新轨迹。
- 正确关系：Corral 强化而不是威胁 ChemWorld 的动机。两者共同反对只看 endpoint；ChemWorld
  提供 chemistry-grounded controlled apparatus，Corral 提供跨环境认识论诊断。

来源：<https://arxiv.org/abs/2604.18805>。

#### ScienceBoard 与 SciAgentArena

ScienceBoard（ICLR 2026）用 169 个多模态真实科学 workflow 任务评价 computer-use agents；
SciAgentArena（2026 preprint）以约 200 个真实科研情境和 stepwise verification 评价多领域 Agent。

- 它们比 ChemWorld 强的地方：专业软件、视觉界面、多领域真实工作流和更广的任务真实性。
- ChemWorld 的差异：不是完成已有软件 workflow，而是在隐藏化学过程中用实验行动生产证据；
  evaluator 拥有逐步物理真值、资源后果和可重复的干预身份。

来源：<https://openreview.net/forum?id=bJvwJahJeF>、
<https://arxiv.org/abs/2606.12736>。

### 2.6 具身实验室模拟、数字孪生与失败诊断

#### LabUtopia 与 MATTERIX

LabUtopia（NeurIPS 2025）以高保真多物理模拟、程序生成实验室场景、30 个任务和 200+ assets
评价科学具身 Agent。MATTERIX（Nature Computational Science 2026）模拟机器人操作、粉末和
液体、设备、热传递与基础反应动力学，并展示 sim-to-real workflow transfer。

- 它们比 ChemWorld 强的地方：视觉、几何、接触、移动操作、设备数字孪生和 sim-to-real。
- ChemWorld 的差异：抽象掉运动控制，以稳定化学操作语义把计算预算用于大量 agent-world
  受控实验；研究问题是证据如何改变实验策略，不是机器人能否可靠拿起、倾倒和运输器皿。
- 它们可以成为 ChemWorld 的未来 front-end，不应被写成被我们替代的工作。

来源：<https://arxiv.org/abs/2505.22634>、
<https://doi.org/10.1038/s43588-025-00924-4>。

#### Labimus 与 ADePT

Labimus（2026 preprint）重建 30+ 个有功能对应的有机化学工作站资产，引入粒子粉末物理、闭环
仪器读数、六类原子操作和七步固体称量流程，并区分“任务做完”与“达到实验精度”。ADePT
（Communications Chemistry 2026 Perspective）则用 adaptability/learning、dexterity、
perception 和 task complexity 四维描述实验室机器人自主性。

- 它们比 ChemWorld 强的地方：精细具身操作、粉末动力学、精度容差、视觉/接触问题和机器人
  自主性评价语言。
- ChemWorld 的边界：当前显式抽象 dexterity 与 perception；它测的是 Agent 为何选择某个
  化学操作、证据如何改变后续行动，以及这种策略能否在控制身份后重复。
- 结论：具身仿真与 ChemWorld 不争同一块“蛋糕”，但它们使我们不能把逐步 laboratory
  operation 或 task-completion/validity dissociation 当作独占主张。

来源：<https://arxiv.org/abs/2606.31037>、
<https://doi.org/10.1038/s42004-026-01932-9>。

#### LabOSBench 与 LabRobFail

LabOSBench（2026 preprint）以八个 web 仪器模拟器和 96 个 subtasks 评价 sample loading、对准、
调参、采集和结果检查。LabRobFail（2026 preprint）注入控制、物理与语义失败，发布 20,000+
轨迹、70+ 场景并评价失败检测、定位、分类和修复。

- 它们比 ChemWorld 强的地方：GUI/视觉仪器控制，以及机器人失败的规模、类型和诊断粒度。
- ChemWorld 的差异：失败是实验策略本身的后果之一，并与材料、信息、测量和后续实验选择共同
  进入轨迹；它不解决视觉故障诊断或精密仪器 GUI 控制。

来源：<https://arxiv.org/abs/2606.16802>、<https://arxiv.org/abs/2607.23704>。

## 3. 能力矩阵：不是谁赢，而是谁在测什么

符号：✓ 为核心能力；△ 为部分覆盖或不是主要评价对象；— 为原论文的主要系统不覆盖。

| 工作族 | 化学状态过程 | Agent 自选多步实验 | 主动表征 | 物理资源/失败后果 | 受控 prior/物理身份干预 | 轨迹行为评价 | 固定世界 fresh replication | 真实硬件/具身 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Summit / Olympus / PC-Gym | ✓ | △ | — | △ | △ | △ | — | — |
| ChemGymRL | ✓ | ✓ | △ | △ | — | △ | — | — |
| MADE | 计算材料 | 候选结构提议 | oracle query | 查询预算 | 系统条件 | △ | — | — |
| Coscientist / ChemCrow | ✓ | ✓ | ✓ | △ | — | △ | — | ✓ |
| Co-Scientist / Robin | 数据与假设 | protocol proposal | 数据分析 | 人类执行成本 | expert-in-loop | ✓ | — | ✓ |
| A-Lab GPSS / robot chemistry | ✓ | ✓ | ✓ | ✓ | — | ✓ | — | ✓ |
| ORGANA / ChemAgents | ✓ | ✓ | ✓ | ✓ | — | △ | — | ✓ |
| AutoLabs | protocol 表示 | protocol compilation | — | 硬件约束 | — | ✓ | — | hardware-ready |
| RoboChem-Flex | ✓ | 优化闭环 | ✓ | ✓ | — | △ | — | ✓ |
| X-ray / teachable instrument agents | 仪器状态 | ✓ | ✓ | ✓ | — | ✓ | — | ✓ |
| DiscoveryWorld | △ | ✓ | ✓ | △ | △ | ✓ | — | — |
| BoxingGym / SciGym | △ | △ | ✓ | 预算 | ✓ | △ | — | — |
| SciExplorer | 数值物理模型 | ✓ | ✓ | 查询/计算成本 | 系统条件 | ✓ | 独立尝试 | — |
| NewtonBench / DiscoverPhysics | — | △ | ✓ | 查询预算 | ✓ | △ | — | — |
| ActiveSciBench-Chem | 动力学 | △ | assay query | 查询预算 | ✓ | △ | — | — |
| CausaLab / ReplaySCM | 抽象 SCM | △ | 干预 | 查询预算 | ✓ | ✓ | — | — |
| Corral | 依赖底层环境 | 依赖底层环境 | 依赖底层环境 | △ | △ | ✓ | — | — |
| AHOIS | 真实光学系统 | ✓ | ✓ | △ | critic ablation | ✓ | — | ✓ |
| Qiushi | 真实光学系统 | ✓ | ✓ | 真实平台成本 | — | ✓ | 单一长程研究 | ✓ |
| LabUtopia / MATTERIX / Labimus | ✓ | ✓ | △ | ✓ | 场景变化 | △ | — | △/✓ |
| LabOSBench / LabRobFail | △ | workflow | ✓ | ✓ | failure injection | ✓ | — | △ |
| **ChemWorld 当前版本** | **✓** | **✓** | **✓** | **✓** | **✓** | **✓** | **✓** | **—** |

最后一行的“全 ✓”不能被解释为全面优于其他工作。ChemWorld 把运动学、视觉、真实仪器误差和
现实化学开放性抽象掉，才换得这一组合的可控性和重复性。

## 4. 真正的独占生态位

在截至 2026-08-02 审计的工作中，没有单一系统同时把下面五件事作为同一研究设计的一部分：

1. chemistry-native、有状态、部分可观测的材料—过程运行时；
2. Agent 自主决定加料、过程控制、表征、终止和终点检测；
3. campaign-wide 材料、仪器、容器、操作和 provider 资源账本；
4. 对 Agent 先验和物理身份的配对干预；
5. 以不可覆盖轨迹、精确重放和 fixed-world fresh replication 测量发现、保留、回撤与恢复。

因此可守的独占生态位不是“比机器人更像实验室”，也不是“比规律发现 benchmark 有更多规律”，
更不是“首先提出 Agent 行为科学”，而是下面这一组能力的交集：

> **controlled experimental science of experimenting agents, grounded in executable chemistry**

中文可以写为：

> **以可执行化学世界为实验装置，对正在做实验的 Agent 开展受控、可重复的行为科学。**

这个定位允许三类工作同时成立：

- 真实实验室负责回答“能否安全、可靠地作用于现实”；
- 规律发现 benchmark 负责回答“能否恢复可泛化的机制”；
- ChemWorld 负责回答“Agent 如何通过实际实验行动使用证据，以及这种行为是否稳定”。

## 5. 必须主动承认的 ChemWorld 弱点

1. 当前 15 个任务中只有电化学和结晶具有正式 Agent 结果；G2 正式复现只覆盖电化学、两个
   有目的选择的 worlds 和一个模型配置。
2. 五类 instrument packet 是 state-coupled synthetic signals，不是真实样品谱图预测器。
3. 没有视觉、机器人运动控制、真实仪器 API、湿实验或 sim-to-real 证据。
4. 当前规律与任务组合仍是有界枚举，不能支持“近乎无限世界”的经验性主张。
5. native Codex provider sampling seed 不可冻结；fresh replicate 是独立 session，不是可重放
   的模型随机数。
6. G2 v0.5 是 selected-world descriptive replication，不是一般世界中的 prior effect 检验。
7. 过程指标虽然在 fresh run 前冻结，但 discovery/retention/recovery 仍是我们定义的 operational
   measures；需要报告敏感性和完整轨迹，避免把它们过度心理化。

这些限制应当写进正文。承认它们反而保护真正的贡献：当前结果已经足以证明这种实验装置能够
区分 endpoint、prior response、prediction 和 trajectory stability，但还不足以建立普适的
“AI 科学家心理学”。

## 6. 论文中建议使用的 related-work 结论句

> Existing systems establish complementary capabilities: chemistry agents and
> self-driving laboratories demonstrate tool use and physical execution;
> interactive discovery benchmarks test hypothesis formation and law recovery;
> embodied simulators test perception and manipulation; and recent process-level
> evaluations show that successful outcomes need not be supported by scientific
> reasoning. ChemWorld occupies a different intersection. It uses a stateful
> chemical runtime as controlled apparatus for intervening on an experimenting
> agent and measuring how evidence, prior information, resources and physical
> consequences shape its subsequent actions.

不建议使用的结论句：

> Unlike all prior work, ChemWorld is the first complete autonomous virtual
> chemistry laboratory and can generate unlimited physical worlds.

后一句同时违反现有证据、相关工作事实和当前仓库能力边界。

## 7. 截止日期与更新规则

- 检索截止：2026-08-02，Asia/Shanghai。
- 2026 年工作均需在正文中标明 peer-reviewed 或 preprint 状态。
- arXiv 提交前重新检索 `scientific agent benchmark`、`virtual chemistry laboratory`、
  `autonomous chemical experimentation`、`experimental intelligence`、`robotic chemistry agent`
  和所有直接竞品标题。
- 新工作若覆盖上述五项交集中的四项以上，必须更新能力矩阵和主张边界，而不能只追加引用。
