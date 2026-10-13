# 48 场同期记录逐场精读

W2-250 事后逐场精读。全部145版源笔记全文阅读；K1/Q/K2按相关判断及预测对照，重点案例扩展全文核对。单一分析者解释性记录，不是盲法双人编码或私有思维读数。

下文引文逐字核对到指定源笔记版本；相邻解释由分析者撰写。数字从保留导出生成。
EQ 的极稀误差为 Q03/Q08/Q09 九个指标预测的 MAE；C 的复测为无噪真实结果。
R1/R2/R3 是三次新会话，固定环境映射，无可控模型 RNG seed。缺测不填零。
所有完整缺失原因见 [定量分析](ANALYSIS.md)；[综合解释](CLOSE_READING.md)。

## C-W01-Aligned

### repeat-01

始终淬灭；从S2优越改为直接结晶均产生细粉，控制缓降只保留粗种晶。预期混合流程改善被最后一批否定。该运行有清楚的预期—检验—撤回链，但将原因归于操作类别仍不能排除共同热史。Q纯度均值降到0.924，源期均值约0.986。

> The operation class, not simply nominal solvent

出处：[笔记 v6](repeat-01/C-W01-Aligned-notebook.md#revision-6)；[K1/Q/K2](repeat-01/C-W01-Aligned-reports.md)；[批次与预测原始科学导出](repeat-01/C-W01-Aligned.json)。

数值核对：淬灭批次 12/12；推荐复测回收 0.00000、细粉 0.00000，仅质量合格；纯度预测 MAE 0.06045；质量分类 5/12 正确。

### repeat-02

始终淬灭，固定C1/S2，低装料可达细粉要求但公共回收很小。明确没有达到0.10目标，推荐后复测回收为零。局部阈值结论不等于发现有效工艺；Q仍低估纯度且热对比方向错误。

> supported loading threshold in tested S2 recipes

出处：[笔记 v3](repeat-02/C-W01-Aligned-notebook.md#revision-3)；[K1/Q/K2](repeat-02/C-W01-Aligned-reports.md)；[批次与预测原始科学导出](repeat-02/C-W01-Aligned.json)。

数值核对：淬灭批次 12/12；推荐复测回收 0.00000、细粉 0.00000，仅质量合格；纯度预测 MAE 0.07045；质量分类 9/12 正确。

### repeat-03

不淬灭，S2先提供稳健合格域；S0从直接降温失败，到二段仍失败，再三段合格且回收更高，最终推荐真实回收0.584、细粉0.463。明确稳健性与样本最高值的取舍；但后测质量分类仅3/12正确，操作成功没有保证迁移。

> supported with boundary risk

出处：[笔记 v3](repeat-03/C-W01-Aligned-notebook.md#revision-3)；[K1/Q/K2](repeat-03/C-W01-Aligned-reports.md)；[批次与预测原始科学导出](repeat-03/C-W01-Aligned.json)。

数值核对：淬灭批次 0/12；推荐复测回收 0.58400、细粉 0.46312，质量及回收目标均达到；纯度预测 MAE 0.00811；质量分类 3/12 正确。

## C-W01-Opaque

### repeat-01

始终淬灭；逐步否定长停留、循环、加种与中度稀释。最后极稀批细粉合格但公共回收约0.003，模型坦承目标失败；复测无噪回收为零。质量合格不能替代有效回收，源期已有正确区分。

> not a satisfactory recovery optimum

出处：[笔记 v5](repeat-01/C-W01-Opaque-notebook.md#revision-5)；[K1/Q/K2](repeat-01/C-W01-Opaque-reports.md)；[批次与预测原始科学导出](repeat-01/C-W01-Opaque.json)。

数值核对：淬灭批次 12/12；推荐复测回收 0.00000、细粉 0.00000，仅质量合格；纯度预测 MAE 0.01514；质量分类 5/12 正确。

### repeat-02

全程不淬灭；筛选后固定S2，跨催化剂保持合格，再降低终温提升回收。推荐真实回收0.509、细粉0.263。笔记称五个S2批但实际列了六个，逐批记录优先；热循环后测方向仍预测错误。

> colder endpoints increased observed recovery

出处：[笔记 v3](repeat-02/C-W01-Opaque-notebook.md#revision-3)；[K1/Q/K2](repeat-02/C-W01-Opaque-reports.md)；[批次与预测原始科学导出](repeat-02/C-W01-Opaque.json)。

数值核对：淬灭批次 0/12；推荐复测回收 0.50946、细粉 0.26340，质量及回收目标均达到；纯度预测 MAE 0.01494；质量分类 5/12 正确。

### repeat-03

不淬灭，先否定高种量与强回热，再发现S2降温序列有效。末批加倍冷停留只提高公共回收约0.003，小于噪声，模型正确称效应未决，却仍选择更复杂的批12，未执行上一版优先简单批11的规则。两批无噪回收相同，判断与选择存在具体不一致。

> prefer the simpler batch 11 process

出处：[笔记 v5](repeat-03/C-W01-Opaque-notebook.md#revision-5)；[K1/Q/K2](repeat-03/C-W01-Opaque-reports.md)；[批次与预测原始科学导出](repeat-03/C-W01-Opaque.json)。

数值核对：淬灭批次 0/12；推荐复测回收 0.53839、细粉 0.28229，质量及回收目标均达到；纯度预测 MAE 0.01529；质量分类 5/12 正确。

## C-W03-Aligned

### repeat-01

始终淬灭；批11降装料后细粉0.591，事前预测继续降料可合格；批12实际升到0.846，立即撤回单调关系，只留下未建立的内点最优。是真实反向结果与公开修订，未获得合格工艺。

> narrowed, non-monotonic

出处：[笔记 v5](repeat-01/C-W03-Aligned-notebook.md#revision-5)；[K1/Q/K2](repeat-01/C-W03-Aligned-reports.md)；[批次与预测原始科学导出](repeat-01/C-W03-Aligned.json)。

数值核对：淬灭批次 12/12；推荐复测回收 0.49177、细粉 0.59725，质量不合格；纯度预测 MAE 0.02652；质量分类 9/12 正确。

### repeat-02

前五批淬灭且细粉近1，六批起取消淬灭并同时改变种量/降温序列，细粉约0.21并保持后续合格。K2自提单因素淬灭挑战，正确承认混杂。Q却把所有含淬灭的新配方判失败，质量分类6/12，纯度预测均值0.902；局部关系被使用，但迁移范围仍失准。

> Avoiding the rapid quench and using a staged, seeded cool

出处：[笔记 v3](repeat-02/C-W03-Aligned-notebook.md#revision-3)；[K1/Q/K2](repeat-02/C-W03-Aligned-reports.md)；[批次与预测原始科学导出](repeat-02/C-W03-Aligned.json)。

数值核对：淬灭批次 5/12；推荐复测回收 0.38450、细粉 0.15406，质量及回收目标均达到；纯度预测 MAE 0.08319；质量分类 6/12 正确。

### repeat-03

不淬灭，发现0.055 L S2合格而0.05/0.04 L细粉近1，再用四个0.055 L批次确认局部区域，并否定加长老化必增益。得到有边界的经验关系；配置ramp_rate并不证明直接cool_crystallize按该速率执行，因果表述须按实际动作。Q回热方向仍错。

> the feasible loading window is sharp

出处：[笔记 v4](repeat-03/C-W03-Aligned-notebook.md#revision-4)；[K1/Q/K2](repeat-03/C-W03-Aligned-reports.md)；[批次与预测原始科学导出](repeat-03/C-W03-Aligned.json)。

数值核对：淬灭批次 0/12；推荐复测回收 0.50268、细粉 0.38264，质量及回收目标均达到；纯度预测 MAE 0.03569；质量分类 8/12 正确。

## C-W03-Opaque

### repeat-01

始终淬灭；跨催化剂、溶剂及热史均有细粉失败，先后否定慢冷、回热、温停、去种。最终诚实标记推荐不合格；Q承认新配方差别，采用的热循环方向正确。不能由操作失败推定完全没有形成有效判断。

> explicitly not a specification-compliant process

出处：[笔记 v4](repeat-01/C-W03-Opaque-notebook.md#revision-4)；[K1/Q/K2](repeat-01/C-W03-Opaque-reports.md)；[批次与预测原始科学导出](repeat-01/C-W03-Opaque.json)。

数值核对：淬灭批次 12/12；推荐复测回收 0.50923、细粉 0.99995，质量不合格；纯度预测 MAE 0.00939；质量分类 8/12 正确。

### repeat-02

全程不淬灭；固定热史换溶剂找到S2，逐步降温并复验种量方案。明确加种收益不超过波动，推荐工艺复测合格；热对比方向也正确，但不代表全部机理已识别。

> unresolved seed effect

出处：[笔记 v3](repeat-02/C-W03-Opaque-notebook.md#revision-3)；[K1/Q/K2](repeat-02/C-W03-Opaque-reports.md)；[批次与预测原始科学导出](repeat-02/C-W03-Opaque.json)。

数值核对：淬灭批次 0/12；推荐复测回收 0.52042、细粉 0.24128，质量及回收目标均达到；纯度预测 MAE 0.02235；质量分类 9/12 正确。

### repeat-03

不淬灭，早期高种量失败后切入S1/C0，300到250 K降温序列保持合格且回收提升，末批复验。形成有范围的工艺关系；Q热循环采用有利熟化解释，方向与参考相反。

> S1 batches 5–12 consistently met

出处：[笔记 v3](repeat-03/C-W03-Opaque-notebook.md#revision-3)；[K1/Q/K2](repeat-03/C-W03-Opaque-reports.md)；[批次与预测原始科学导出](repeat-03/C-W03-Opaque.json)。

数值核对：淬灭批次 0/12；推荐复测回收 0.49205、细粉 0.43056，质量及回收目标均达到；纯度预测 MAE 0.03235；质量分类 4/12 正确。

## C-W05-Aligned

### repeat-01

不淬灭；从S2先验出发，经材料对比转向S1/C0，再检验预加种、延长高温段及降低终温。明确撤回S2最高回收的泛化，推荐真实回收0.539、细粉0.257；有前瞻预测及后续实验支持的正向案例。

> rejected as general prior

出处：[笔记 v5](repeat-01/C-W05-Aligned-notebook.md#revision-5)；[K1/Q/K2](repeat-01/C-W05-Aligned-reports.md)；[批次与预测原始科学导出](repeat-01/C-W05-Aligned.json)。

数值核对：淬灭批次 0/12；推荐复测回收 0.53882、细粉 0.25713，质量及回收目标均达到；纯度预测 MAE 0.01246；质量分类 8/12 正确。

### repeat-02

不淬灭，经共同工艺比较把S2最高回收先验改为S1更好，进一步选C0及冷端。识别370/380 K反应回收近乎并列而未强排；推荐复测成功，Q却采用回热改善细粉的错误方向。

> rejected for recovery ranking

出处：[笔记 v2](repeat-02/C-W05-Aligned-notebook.md#revision-2)；[K1/Q/K2](repeat-02/C-W05-Aligned-reports.md)；[批次与预测原始科学导出](repeat-02/C-W05-Aligned.json)。

数值核对：淬灭批次 0/12；推荐复测回收 0.55096、细粉 0.42345，质量及回收目标均达到；纯度预测 MAE 0.02060；质量分类 9/12 正确。

### repeat-03

不淬灭，辨识S1高回收但边界敏感，也知道S2为稳健备选。最终选择公共细粉0.4919的S1；无噪复测0.50493略超限。模型并未宣称稳健成功，而是明确承担了样本最高值选择的边界风险。

> The fines margin is narrow

出处：[笔记 v3](repeat-03/C-W05-Aligned-notebook.md#revision-3)；[K1/Q/K2](repeat-03/C-W05-Aligned-reports.md)；[批次与预测原始科学导出](repeat-03/C-W05-Aligned.json)。

数值核对：淬灭批次 0/12；推荐复测回收 0.47799、细粉 0.50493，质量不合格；纯度预测 MAE 0.06445；质量分类 10/12 正确。

## C-W05-Opaque

### repeat-01

始终淬灭；加种、慢冷、回热、重悬与减种都未合格，公开记录失败且不虚报机制。其纯度后测接近参考、热方向正确，展示工艺搜索失败与部分预测准确并存。

> explicitly noting its fines failure

出处：[笔记 v4](repeat-01/C-W05-Opaque-notebook.md#revision-4)；[K1/Q/K2](repeat-01/C-W05-Opaque-reports.md)；[批次与预测原始科学导出](repeat-01/C-W05-Opaque.json)。

数值核对：淬灭批次 12/12；推荐复测回收 0.53846、细粉 1.00000，质量不合格；纯度预测 MAE 0.00534；质量分类 11/12 正确。

### repeat-02

始终淬灭，多种形貌处理均失败，低料提高回收但细粉仍近1；推荐明确不合格。Q把所有新配方判不合格，符合7/12，热方向错。纯度预测却很准确，不能合并成整体认知好或坏。

> No completed batch is quality-feasible

出处：[笔记 v3](repeat-02/C-W05-Opaque-notebook.md#revision-3)；[K1/Q/K2](repeat-02/C-W05-Opaque-reports.md)；[批次与预测原始科学导出](repeat-02/C-W05-Opaque.json)。

数值核对：淬灭批次 12/12；推荐复测回收 0.63335、细粉 0.99949，质量不合格；纯度预测 MAE 0.00543；质量分类 7/12 正确。

### repeat-03

不淬灭，S1形成300–260 K可行范围；更低温/二段虽有略高样本值，但未超噪声。主动选较简单且细粉余量更大的260 K批次，复测成功。与C-W01/O第三次的决策偏离形成有意义对照。

> retaining materially more fines margin

出处：[笔记 v3](repeat-03/C-W05-Opaque-notebook.md#revision-3)；[K1/Q/K2](repeat-03/C-W05-Opaque-reports.md)；[批次与预测原始科学导出](repeat-03/C-W05-Opaque.json)。

数值核对：淬灭批次 0/12；推荐复测回收 0.46269、细粉 0.43026，质量及回收目标均达到；纯度预测 MAE 0.01443；质量分类 6/12 正确。

## EQ-W01-Aligned

### repeat-01

先写档案精确稀释预期，再执行锚点；观测ΔpH约0.00444、Δ解离率约0.01230，与局部先验相容。明确未确定全局机制；Q08仍由弱对数趋势给出0.1232、上界0.18，遗漏参考值约0.716。局部验证与远端预测之间存在实质断点。

> supported locally, not established globally

出处：[笔记 v2](repeat-01/EQ-W01-Aligned-notebook.md#revision-2)；[K1/Q/K2](repeat-01/EQ-W01-Aligned-reports.md)；[批次与预测原始科学导出](repeat-01/EQ-W01-Aligned.json)。

数值核对：最低名义浓度 0.0185185 M；极稀三题 MAE 0.19140。

### repeat-02

重复锚点并记录局部稀释与高浓度平台的差别；Q改用高浓度底值加弱酸项，Q08解离率0.746接近参考0.716。源笔记的有界认识与后测新增的函数延伸分开；K2指出预测区间排除了仍可能成立的平台。

> the dilute local relationship should not be extrapolated

出处：[笔记 v2](repeat-02/EQ-W01-Aligned-notebook.md#revision-2)；[K1/Q/K2](repeat-02/EQ-W01-Aligned-reports.md)；[批次与预测原始科学导出](repeat-02/EQ-W01-Aligned.json)。

数值核对：最低名义浓度 0.0185185 M；极稀三题 MAE 0.04234。

### repeat-03

对锚点采取部分支持：pH有序而解离率不单调，明确跨仪器混杂；总体回归和有效pKa均保留范围。K1即服务失败，因此源笔记充分但没有完整后测链。

> Dissociation fractions at these three points were non-monotone

出处：[笔记 v2](repeat-03/EQ-W01-Aligned-notebook.md#revision-2)；[K1/Q/K2](repeat-03/EQ-W01-Aligned-reports.md)；[批次与预测原始科学导出](repeat-03/EQ-W01-Aligned.json)。

数值核对：最低名义浓度 0.0185185 M；极稀三题 MAE 缺测。
缺失阶段：K1, Q, K2, EQS。

## EQ-W01-Opaque

### repeat-01

预先固定4×3矩阵，未在中途写修订；最终撤回强方向规律，只保留0.0625–2 M近平台与多种解释。Q沿微弱对数斜率外推，Q08解离率0.0923。应区分合理的局部描述和失准的远端数值，不能写成源期已宣称普遍平台。

> not supported as originally directional

出处：[笔记 v2](repeat-01/EQ-W01-Opaque-notebook.md#revision-2)；[K1/Q/K2](repeat-01/EQ-W01-Opaque-reports.md)；[批次与预测原始科学导出](repeat-01/EQ-W01-Opaque.json)。

数值核对：最低名义浓度 0.0625 M；极稀三题 MAE 0.20238。

### repeat-02

六批试剂实验未见预期效应后，明确提出component 0替代假说，后续确实转测组分与分段稀释；最终未识别作用坐标。Q采用平台与水样稀释极限的折中，区间较宽。体现主动改变检验对象，并未形成唯一机制。

> Selectable component 0 may be the missing

出处：[笔记 v2](repeat-02/EQ-W01-Opaque-notebook.md#revision-2)；[K1/Q/K2](repeat-02/EQ-W01-Opaque-reports.md)；[批次与预测原始科学导出](repeat-02/EQ-W01-Opaque.json)。

数值核对：最低名义浓度 0.1 M；极稀三题 MAE 0.09224。

### repeat-03

浓度矩阵后明确撤回简单浓度律，修正把两种仪器当重复测量的初始设想。源研究及K1保留；Q服务失败，不能给它分配预测表现，也不能用另两次结果补齐。

> not supported as a simple concentration law

出处：[笔记 v2](repeat-03/EQ-W01-Opaque-notebook.md#revision-2)；[K1/Q/K2](repeat-03/EQ-W01-Opaque-reports.md)；[批次与预测原始科学导出](repeat-03/EQ-W01-Opaque.json)。

数值核对：最低名义浓度 0.0625 M；极稀三题 MAE 缺测。
缺失阶段：Q, K2, EQS。

## EQ-W02-Aligned

### repeat-01

锚点单对同向，但浓端重复的pH差异本身较大，故没有把数值相近当精确确认。Q用有效pKa和局部弱趋势延伸，Q08解离率0.112、上界0.20；范围警觉仍未传到足够宽的预测分布。

> unresolved, directionally compatible only

出处：[笔记 v2](repeat-01/EQ-W02-Aligned-notebook.md#revision-2)；[K1/Q/K2](repeat-01/EQ-W02-Aligned-reports.md)；[批次与预测原始科学导出](repeat-01/EQ-W02-Aligned.json)。

数值核对：最低名义浓度 0.0185185 M；极稀三题 MAE 0.16909。

### repeat-02

中期观察稀释方向，后期重复锚点后仍承认散布与范围。Q继续小幅外推，Q08为0.119、上界0.229。比第三次同条件更差，差异主要出现在后测采用的函数形式，而不是有没有获得局部验证。

> supported locally, with substantial scatter

出处：[笔记 v3](repeat-02/EQ-W02-Aligned-notebook.md#revision-3)；[K1/Q/K2](repeat-02/EQ-W02-Aligned-reports.md)；[批次与预测原始科学导出](repeat-02/EQ-W02-Aligned.json)。

数值核对：最低名义浓度 0.0185185 M；极稀三题 MAE 0.16609。

### repeat-03

重复锚点支持方向而非先验精确幅度，跨全范围拒绝强单调律；Q采用溶解上限加弱酸方程，最低三题误差显著小于前两次。K2指出其区间排除了K1仍保留的缓冲解释；正确答案也可能伴随依据不足的排他性。

> point magnitude not confirmed

出处：[笔记 v3](repeat-03/EQ-W02-Aligned-notebook.md#revision-3)；[K1/Q/K2](repeat-03/EQ-W02-Aligned-reports.md)；[批次与预测原始科学导出](repeat-03/EQ-W02-Aligned.json)。

数值核对：最低名义浓度 0.0185185 M；极稀三题 MAE 0.01350。

## EQ-W02-Opaque

### repeat-01

八批后否定强弱酸浓度预期，安排重复、等浓度与分段稀释，最终保留局部平台。Q中心仍接近平台，但区间包含多种稀释极限；最低三题点误差较大、区间覆盖完整，展示点预测与不确定性表现可以分离。

> not supported over the tested range

出处：[笔记 v2](repeat-01/EQ-W02-Opaque-notebook.md#revision-2)；[K1/Q/K2](repeat-01/EQ-W02-Opaque-reports.md)；[批次与预测原始科学导出](repeat-01/EQ-W02-Opaque.json)。

数值核对：最低名义浓度 0.1 M；极稀三题 MAE 0.17576。

### repeat-02

研究期与K1保留近平台、缓冲、溶解度钳制等竞争解释。Q才将后者具体化为约0.00268 M溶解上限和Ka约1.4e-5，Q08解离率0.6269接近参考0.6546。K2承认将一个候选解释用得过强；准确外推与证据唯一性是两件事。

> effective near-constant mapping

出处：[笔记 v3](repeat-02/EQ-W02-Opaque-notebook.md#revision-3)；[K1/Q/K2](repeat-02/EQ-W02-Opaque-reports.md)；[批次与预测原始科学导出](repeat-02/EQ-W02-Opaque.json)。

数值核对：最低名义浓度 0.05 M；极稀三题 MAE 0.01501。

### repeat-03

源期用线性描述近平台并保留不可识别性；Q引入有效Ka稀释延伸，Q08约0.63。K2明确称该外推模型在K1后引入。它是依据研究数据与理论构造的成功预测候选，不能回写成实验中已经验证了稀释规律。

> near-flat empirical response in this scope

出处：[笔记 v3](repeat-03/EQ-W02-Opaque-notebook.md#revision-3)；[K1/Q/K2](repeat-03/EQ-W02-Opaque-reports.md)；[批次与预测原始科学导出](repeat-03/EQ-W02-Opaque.json)。

数值核对：最低名义浓度 0.0625 M；极稀三题 MAE 0.01451。

## EQ-W03-Aligned

### repeat-01

六批后提出高浓度沉淀上升的预期，后续高浓度观测未支持，最终搁置阈值主张。保留锚点而不认定绝对pKa已识别；Q仍作微弱对数外推，最低三题区间覆盖为零。

> supported only at the archival anchor

出处：[笔记 v3](repeat-01/EQ-W03-Aligned-notebook.md#revision-3)；[K1/Q/K2](repeat-01/EQ-W03-Aligned-reports.md)；[批次与预测原始科学导出](repeat-01/EQ-W03-Aligned.json)。

数值核对：最低名义浓度 0.0185185 M；极稀三题 MAE 0.16287。

### repeat-02

全程矩阵后得到有效pKa约5.02及局部锚点相容；Q将很弱的pH对数斜率与Henderson关系结合，Q08解离率0.1089。与同轮Opaque的0.5637相比，二者均未测极稀区却采用不同延伸。

> supported only as an effective weak-acid description

出处：[笔记 v2](repeat-02/EQ-W03-Aligned-notebook.md#revision-2)；[K1/Q/K2](repeat-02/EQ-W03-Aligned-reports.md)；[批次与预测原始科学导出](repeat-02/EQ-W03-Aligned.json)。

数值核对：最低名义浓度 0.0185185 M；极稀三题 MAE 0.15325。

### repeat-03

中途预期固定体积浓度系列应有序，结束时承认斜率弱、重复差异可大于系列变化；Q继续弱斜率延伸，极稀预测仍失准。三次Aligned均是局部有界描述配合偏平台的远端预测。

> effective pKa relationship supported; concentration trend weak

出处：[笔记 v3](repeat-03/EQ-W03-Aligned-notebook.md#revision-3)；[K1/Q/K2](repeat-03/EQ-W03-Aligned-reports.md)；[批次与预测原始科学导出](repeat-03/EQ-W03-Aligned.json)。

数值核对：最低名义浓度 0.0138889 M；极稀三题 MAE 0.15504。

## EQ-W03-Opaque

### repeat-01

局部浓度规律不成立；等浓度比较和分段稀释提供线索，但明确组间与仪器混杂。Q采用平台与温和稀释的折中，未得到真实的大幅解离变化。与后两次低误差形成同世界路径对照。

> suggestive, sensor-confounded

出处：[笔记 v2](repeat-01/EQ-W03-Opaque-notebook.md#revision-2)；[K1/Q/K2](repeat-01/EQ-W03-Opaque-reports.md)；[批次与预测原始科学导出](repeat-01/EQ-W03-Opaque.json)。

数值核对：最低名义浓度 0.025 M；极稀三题 MAE 0.14145。

### repeat-02

八批加载实验后提出体积作为独立坐标，后续固定量变体积仍未发现效应，最终收回为平台。Q再用溶解上限及总量饱和沉淀模型外推，误差很小。研究中的假说淘汰与后测的模型补充具有不同时间位置。

> liquid volume/dilution as an independent simulator variable

出处：[笔记 v2](repeat-02/EQ-W03-Opaque-notebook.md#revision-2)；[K1/Q/K2](repeat-02/EQ-W03-Opaque-reports.md)；[批次与预测原始科学导出](repeat-02/EQ-W03-Opaque.json)。

数值核对：最低名义浓度 0.0833333 M；极稀三题 MAE 0.01273。

### repeat-03

4×3矩阵拒绝原方向预期，保留水相局部不变。Q解释为可能的溶解度平台，给出约0.563的极稀解离率，接近参考0.580；明确缓冲等价解释未排除。不能将预测成功自动判为机制已发现。

> most defensible model is an approximately invariant acidic state

出处：[笔记 v2](repeat-03/EQ-W03-Opaque-notebook.md#revision-2)；[K1/Q/K2](repeat-03/EQ-W03-Opaque-reports.md)；[批次与预测原始科学导出](repeat-03/EQ-W03-Opaque.json)。

数值核对：最低名义浓度 0.05 M；极稀三题 MAE 0.01158。

## EQ-W04-Aligned

### repeat-01

锚点两指标均反向，模型明确记下而非忽略；因信噪比不足保留为未决，同时pKa中心与先验相容。Q仍用近平台回归，最低三题覆盖为零。不能把先验外推失败解释为未承认反例。

> point estimates oppose the archival dilution direction

出处：[笔记 v3](repeat-01/EQ-W04-Aligned-notebook.md#revision-3)；[K1/Q/K2](repeat-01/EQ-W04-Aligned-reports.md)；[批次与预测原始科学导出](repeat-01/EQ-W04-Aligned.json)。

数值核对：最低名义浓度 0.0185185 M；极稀三题 MAE 0.14272。

### repeat-02

锚点pH同向而解离率反向，扩容后pH又反转，故缩小先验支持。Q仍仅给温和稀释趋势，Q08上界0.145而参考约0.517。明确承认局部未决与远端过窄分布并存。

> archival weak-acid dilution direction is not robustly resolved

出处：[笔记 v2](repeat-02/EQ-W04-Aligned-notebook.md#revision-2)；[K1/Q/K2](repeat-02/EQ-W04-Aligned-reports.md)；[批次与预测原始科学导出](repeat-02/EQ-W04-Aligned.json)。

数值核对：最低名义浓度 0.0138889 M；极稀三题 MAE 0.14012。

### repeat-03

锚点方向与幅度接近先验，明确pKa只是有效观测关系；沉淀未见阈值。Q服务失败，只能分析源期与K1，不能将其源期局部支持外推为预测成功。

> effective observational relation

出处：[笔记 v2](repeat-03/EQ-W04-Aligned-notebook.md#revision-2)；[K1/Q/K2](repeat-03/EQ-W04-Aligned-reports.md)；[批次与预测原始科学导出](repeat-03/EQ-W04-Aligned.json)。

数值核对：最低名义浓度 0.00925926 M；极稀三题 MAE 缺测。
缺失阶段：Q, K2, EQS。

## EQ-W04-Opaque

### repeat-01

五批后公开否定强单调律，继续重复、等浓度和分段稀释。Q采用有效pKa稀释模型并保留缓冲候选，Q08为0.49接近参考0.517；三次Opaque中这次最佳，不能据单次定义固定能力。

> H1's strong monotonic form is rejected

出处：[笔记 v2](repeat-01/EQ-W04-Opaque-notebook.md#revision-2)；[K1/Q/K2](repeat-01/EQ-W04-Opaque-reports.md)；[批次与预测原始科学导出](repeat-01/EQ-W04-Opaque.json)。

数值核对：最低名义浓度 0.0625 M；极稀三题 MAE 0.04810。

### repeat-02

因子矩阵结束后记录不同通道斜率甚至方向不一，不将描述系数当强机理。Q接近平台但给出宽区间，点误差大于第一轮；其经验中心和理论延伸选择发生了变化。

> concentration dependence weak and channel-specific

出处：[笔记 v2](repeat-02/EQ-W04-Opaque-notebook.md#revision-2)；[K1/Q/K2](repeat-02/EQ-W04-Opaque-reports.md)；[批次与预测原始科学导出](repeat-02/EQ-W04-Opaque.json)。

数值核对：最低名义浓度 0.0625 M；极稀三题 MAE 0.14143。

### repeat-03

六批后提出平台替代和分段稀释检验；后续pH方向相反且仪器混杂，保持限定。Q对平台与稀释极限折中，Q08为0.18，尚未达到第一轮模型外推准确度。

> supported only as a bounded effective description

出处：[笔记 v3](repeat-03/EQ-W04-Opaque-notebook.md#revision-3)；[K1/Q/K2](repeat-03/EQ-W04-Opaque-reports.md)；[批次与预测原始科学导出](repeat-03/EQ-W04-Opaque.json)。

数值核对：最低名义浓度 0.0625 M；极稀三题 MAE 0.11121。

## EQ-W05-Aligned

### repeat-01

知道档案变化量小于单次噪声，锚点同向但不宣称校准；最终有效pKa与局部平台并存。Q中心延续平台，区间比后两次宽，最低三题覆盖约0.644。

> should not be treated as calibrated by this campaign

出处：[笔记 v3](repeat-01/EQ-W05-Aligned-notebook.md#revision-3)；[K1/Q/K2](repeat-01/EQ-W05-Aligned-reports.md)；[批次与预测原始科学导出](repeat-01/EQ-W05-Aligned.json)。

数值核对：最低名义浓度 0.0185185 M；极稀三题 MAE 0.12640。

### repeat-02

六批后发现前后读数同时变状态与仪器，明确决定先稀释再测量；批次7–12实际改变了测量顺序。获得的是测量设计上的修正，最终稀释幅度仍未决；Q仍采用弱趋势，不能称测量改进已经带来外推提升。

> Switch remaining intermediate measurements to the final composition

出处：[笔记 v2](repeat-02/EQ-W05-Aligned-notebook.md#revision-2)；[K1/Q/K2](repeat-02/EQ-W05-Aligned-reports.md)；[批次与预测原始科学导出](repeat-02/EQ-W05-Aligned.json)。

数值核对：最低名义浓度 0.0166583 M；极稀三题 MAE 0.13206。

### repeat-03

中途承认加载扫描不支持传统浓度律；最后加入component探针仍无沉淀阈值，有效pKa保留为通道恒等描述。Q按档案方向小幅延伸，极稀区继续偏低。

> supported only as a bounded effective identity

出处：[笔记 v3](repeat-03/EQ-W05-Aligned-notebook.md#revision-3)；[K1/Q/K2](repeat-03/EQ-W05-Aligned-reports.md)；[批次与预测原始科学导出](repeat-03/EQ-W05-Aligned.json)。

数值核对：最低名义浓度 0.00925926 M；极稀三题 MAE 0.12764。

## EQ-W05-Opaque

### repeat-01

源研究拒绝强浓度律并保留局部平台；Q采用自行设定约1e-4 M的转折尺度走向水样极限，Q08解离率0.89高于参考0.448。展示脱离平台的延伸也可以过头，不是离开平台就必然更好。

> not supported over tested aqueous slice

出处：[笔记 v2](repeat-01/EQ-W05-Opaque-notebook.md#revision-2)；[K1/Q/K2](repeat-01/EQ-W05-Opaque-reports.md)；[批次与预测原始科学导出](repeat-01/EQ-W05-Opaque.json)。

数值核对：最低名义浓度 0.0625 M；极稀三题 MAE 0.14630。

### repeat-02

八批后搁置平方根浓度律，后续分段稀释和重复未区分机制。Q采用向稀释极限的谨慎折中，最低三题覆盖完整。K2服务失败，不能补写它对自己预测的反思。

> empirical plateau, not a microscopic mechanism

出处：[笔记 v3](repeat-02/EQ-W05-Opaque-notebook.md#revision-3)；[K1/Q/K2](repeat-02/EQ-W05-Opaque-reports.md)；[批次与预测原始科学导出](repeat-02/EQ-W05-Opaque.json)。

数值核对：最低名义浓度 0.0714286 M；极稀三题 MAE 0.08730。
缺失阶段：K2, EQS。

### repeat-03

两体积网格产生不一致斜率，源期只保留平台。Q坚持不以未观测机理替换经验中心，解离率0.065、上界0.20，遗漏真实稀释变化。与第一轮过度走向水极限构成两侧失准。

> no solvent, temperature, time, or identity generalization is justified

出处：[笔记 v2](repeat-03/EQ-W05-Opaque-notebook.md#revision-2)；[K1/Q/K2](repeat-03/EQ-W05-Opaque-reports.md)；[批次与预测原始科学导出](repeat-03/EQ-W05-Opaque.json)。

数值核对：最低名义浓度 0.05 M；极稀三题 MAE 0.13473。
