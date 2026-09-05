# Work II 故事 — When Does Experimental Knowledge Improve Scientific Decisions?

更新：2026-09-05。作者侧论证入口；任务和执行状态在
[Work II TODO](../workstreams/flagship_tasks/WORK_II_TODOLIST.md)，新实验设计在
[实验矩阵](../workstreams/flagship_tasks/WORK_II_EXPERIMENT_MATRIX.md)。
已有结果通过[结果索引](../workstreams/flagship_tasks/WORK_II_PAPER_RESULTS_ZH.md)和
[当前绑定](../configs/current.json)进入。计划中的干预与迁移不得写成已完成结果。

## 1. 一个中心问题

> 实验获得的知识，何时足以支持一个从未执行过的科学决策？
> 显式知识的表示和使用，能否被干预以减少决策损失？

ChemWorld的作用是提供可控的世界、真实可执行的操作与完整证据。
第一篇已建立有限组件域内的世界/仪器能力；Work II检验完整Agent系统的实验知识和决策。
对外不把八种已注册构造模式写成一般流程图编译，也不把同模型自洽性写成实验室预测效度。

当前论文工作标题为 **When Does Experimental Knowledge Improve Scientific Decisions?**。
当前回答是受限经验事实：预测、提交的规律与行为决策具有不同质量，端点和格式正确性
不能单独确认知识的决策价值。表示/决策器干预已完成两个world的开发canary，
正式跨world复核与新条件迁移仍待执行；开发点结果尚未并入当前论文Results。

## 2. 现有证据的三条主结果

### R1：数值改善和显式规律保真不同

C2有两个模型各135个scheduled cells，DeepSeek/GPT完成121/126个。
两者都有平均预测改善；注册selective-correction gates均未通过。
laws可评价数为135/129，law MAE为0.2371/0.1753，compression loss为0.0686/0.0142。
这是两配置的描述性差异；缺失规律和失败保留，不当作模型排名或随机law-quality干预。
同域schema-capacity control支持存在提交时的信息损失，不证明已恢复可迁移真实机制。

### R2：提交的规律和实际选择不同

DeepSeek纵向队列有45 scheduled cells和42条可评分terminal rankings。
重执行最后可用law得到0/45 Top-1，参与者得到11/45，follow-law为12/42。
显式artifact不能替代实际行为读出；它也不是内部推理的直接观测。
C2推荐主要为已见incumbent，因此零增益属于利用既有方案的边界，不能充当未见行动失败证明。
W2-50有11/42 Top-1；没有同协议baseline时不判断其相对随机或无实验是否更好。

### R3：目前的信息策略比较受到系统可用性限制

W2-61两模型各180个四条件slots。all-scheduled autonomy-minus-none regret：
DeepSeek -0.0913、GPT +0.1102，区间均跨零，负值有利于autonomy。
DeepSeek/GPT donor-eligible为42/26，yoked完成10/42与24/26。
失败计入主分析保留了系统策略含义；不能把该差异解释为纯实验选择、纯知识内容或内部中介。
这构成新实验需要精简界面和固定信息交付的直接理由。

## 3. 支持证据如何放置

- A-P matched evidence：反证后出现数值纠错，作为条件性响应；没有turn-matched no-packet组，
  不归因于纯packet效应。
- B3：对受限函数形式实施可识别控制。两模型各30 scheduled，joint recovery0/30与5/30；
  DeepSeek13个schema failures必须与科学判断分开报告，两模型固定机会gain成功均0/18。
- B2、low reasoning：表面有精确alias，作为可识别性/表达诊断。后续B3已解决另一个测量问题，
  不恢复B2重复试验，不称Agent“无法识别”不可识别的结构。
- W2-51/52/53：完整排序与动作效用指标不等价，作为补充评价诊断。它们不与R1–R3并列成
  同一种Agent能力断裂；原未启动participant分母保持未启动。
- 先验端点三种形态、早期开发与资格失败：保留在结果索引和补充材料，压缩主文篇幅。

## 4. 三个必须消除的解释跳跃

1. best-minus-first和后半程出现最优说明持续搜索，随机或非自适应搜索也可改善；
   反馈的增量价值需要同预算策略对照。
2. H3是两组pre–final误差改善差，受初始headroom影响；结合初始预测和具体受反证关系解释。
   不显著不能推出没有纠错能力，也不将先验描述直接等同内部世界模型。
3. 全局MAE、精确family/exponent标签与真实决策损失不等价。评价应检查目标是否可识别、
   是否影响决策、预测是否覆盖同一决策条件，以及选择是否真的使用可用知识。

## 5. Spotlight空间：从经验缺口到可检验的修复条件

“预测好不等于决策好”有明确既有研究基础，包括
[Smart Predict, then Optimize](https://arxiv.org/abs/1710.08005)与
[Decision-Focused Learning](https://doi.org/10.1609/aaai.v33i01.33011658)。
一个拟合器加argmax或标准regret界不自动构成新方法，增加模型数也不能替代新知识。

建议贡献增量依次为：
1. M0建立低干扰、决策对齐的测量表面。
2. M1固定证据，交叉替换表示与决策规则，定位可修复或不可修复的条件；与简单公开数据控制比较。
3. M3在fresh context和事先定义的新条件中验证artifact是否仍有用，报告成本及失败边界。
4. 余力用于M2取证因果价值或M4独立后端，而不继续扩旧oracle网格。

有竞争力的结果应说明某一简洁干预为什么有效、适用于什么条件，并跨任务/完整模型系统复核。
方法可简单，但改善需有实际效用、合理不确定性和同信息/预算baseline。
如果只有描述性差异，按可信经验论文收束；如果M1或M3为负，保留负结果，不能为了spotlight换世界或加样本至正。
这里不提供录用概率，也不把spotlight当成强制正结果门禁。

## 6. 主文结构与显示项

现有稿件围绕问题、设计、R1、R2、R3和测量限制组织；历史分支在补充材料保留。
六张共享图已重构，字号与布局按实际论文宽度调整，caption与两份稿件同步：
- 系统图：可观察的artifact/决策与可干预变量。
- C2：预测/规律误差及每模型完整分母。
- 未见行动：实际选择、law-implied选择与逐world损失。
- 信息策略：条件完成率、all-scheduled regret与不确定性。
- B3/诊断：受限可识别性和接口负担；rank-gate历史放补充。

预测图展示同尺度前后均值；B2保留15条配对线；B3直接标出30与18的不同分母。
C2规律图使用同一批可评价样本作两端比较；决策图将3个缺失排名单独标记，
信息策略同时呈现完成数、failure-aware regret和world-cluster区间。历史排序诊断回到补充。
[图表显示计划](prior_discovery_display_items.md)保留每张图的数据角色和解释边界。

M1正式复核完成后，其2×2干预和逐world效应才有资格成为新的主结果图；M3图也等待实际数据。
绝不以预期实验图替换现有证据或在摘要写尚未估计的修复收益。

## 7. 开发canary带来的具体判断

[本轮对照表](../workstreams/flagship_tasks/reports/work-ii-m0-m1-development-20260905.md)
显示两类局部现象：DeepSeek电化学由Agent选择换成共享执行器，regret从0.0242降到0.0074；
GPT结晶由Agent规律换成公开数据拟合规律，固定执行器下从0.1345降到0，fresh Agent也选到最优。
F-A与F-X在全部四个task-model状态一致，不能预设“给了好law，Agent仍一定不会用”。
两world、一次模型重复不足以估计稳定性，0/12接口失败也不是历史协议的随机比较。

Spotlight路线现在有可检验的起点，但仍欠：独立world上的实质改善与边界、
相对于强公开数据baseline的新增知识，以及M3新条件迁移。不能把二次拟合+argmax包装为新算法。
优先做M1正式复核与M3；M2/M4依论文实际主张取舍。运行成本已实测，下一轮不用再修复旧audit链。
