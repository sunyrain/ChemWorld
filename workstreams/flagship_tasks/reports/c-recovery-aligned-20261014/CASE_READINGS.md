# 修正回收定义队列：逐场笔记精读

已读 45/45 场，145 版笔记；核对 65 条逐版本引文及141 个指定执行锚点。
单分析者回溯精读，非盲且尚无独立复核。引文核对确认来源，不等于确认科学解释正确。后测指标见[完整定量报告](REPORT.md)；不宣称所有后测全文均做了独立人工审查。

## repeat-01/C-W01-Opaque

状态：completed；[笔记全文](repeat-01/C-W01-Opaque-notebook.md) / [后测](repeat-01/C-W01-Opaque-reports.md) / [执行时序](sessions/repeat-01/C-W01-Opaque.json)。

源笔记从材料筛选转向可行S2流程，再将体积变化解释为有范围的回收/细粉权衡。明确区分局部工艺选择与混杂的热历史原因；末版承认1与2 mol/L之间的边界仅为单次观察，不能当作重现性估计。中版计划反应温度/时间变化和重复，末版实际总结还包含浓度加密；计划的全部兑现需动作时序核对，不能仅据文字判定。有效Q纯度误差较小而质量分类仅3/12，说明各响应读出应分开。

v2：

> Solvent is a confound, so a general thermal-history effect remains unresolved.

## repeat-01/C-W01-Aligned

状态：failed；[笔记全文](repeat-01/C-W01-Aligned-notebook.md) / [后测](repeat-01/C-W01-Aligned-reports.md) / [执行时序](sessions/repeat-01/C-W01-Aligned.json)。

只留下事前预期，首批完成前触发服务端错误次数上限；没有后续观测—修订链。可说明它如何以名义档案选择C1/S2，并预留排序反转可能，不能评价该预期是否经此会话实验支持。失败保留，Q及推荐复测均缺失。

v1：

> Hidden fixed residuals could reverse either ranking.

## repeat-01/C-W01-MisIndexed

状态：completed；[笔记全文](repeat-01/C-W01-MisIndexed-notebook.md) / [后测](repeat-01/C-W01-MisIndexed-reports.md) / [执行时序](sessions/repeat-01/C-W01-MisIndexed.json)。

先验支持C1/S2，筛选后保留S2但将C0列为实际主选，并把C0/C1/C3微小排序保留为未决。末版区分深冷提高回收、长时程改善形貌及种量小差异的不确定性；高回收S0因细粉不合格被排除。K1明确写出总回收=上游产率×捕获率的口径分解，但只称记账关系。源最佳观测回收0.483与独立复测真值0.474属于含噪测定和真值的区别，不能误报为推荐换了批次。

v3：

> The recovery difference is comparable to single-assay uncertainty and is not evidence of a yield penalty without replication.

## repeat-01/C-W02-Opaque

状态：failed；[笔记全文](repeat-01/C-W02-Opaque-notebook.md) / [后测](repeat-01/C-W02-Opaque-reports.md) / [执行时序](sessions/repeat-01/C-W02-Opaque.json)。

中期依据共同流程的溶剂比较保留S1/S2，再筛催化剂并细化温度和种量。末批的反应温度/终点组合成功后，笔记将其限为经验配方决定而非两个温度分别最优。源期及K1/Q有效、K2服务端失败，因此不能补写末次反思。保留有效Q和推荐复测，不将整场失败解释为已观测预测无效。

v4：

> this is an empirical recipe decision, not proof that 370 K or 280 K is individually optimal.

## repeat-01/C-W02-MisIndexed

状态：completed；[笔记全文](repeat-01/C-W02-MisIndexed-notebook.md) / [后测](repeat-01/C-W02-MisIndexed-reports.md) / [执行时序](sessions/repeat-01/C-W02-MisIndexed.json)。

更新后的口径下，笔记将上游选择性列为总回收限制，后期反应条件与热程共同调整，并承认最优和细粉原因未分离。但末版称第11批总种量0.10 g，执行汇总显示该批只有0.05 g成功、另一请求被拒，第12批同样如此；这是科学表述与实际执行不一致，不能把0.10 g当作完成条件。该记录不证明错误剂量叙述导致后续选择。

v2：

> With C0, reaction selectivity rather than crystallization purity currently limits seed-excluded recovery.

v3：

> with 0.10 g total seed

执行锚点：120, 121, 131, 132。

## repeat-01/C-W03-Opaque

状态：completed；[笔记全文](repeat-01/C-W03-Opaque-notebook.md) / [后测](repeat-01/C-W03-Opaque-reports.md) / [执行时序](sessions/repeat-01/C-W03-Opaque.json)。

早期筛选后采用C1/S2及低种量分段流程，后期把更高温/更短时组合与回收改善联系；450 K/600 s的源观测几乎无回收，末版因而拒绝单调推广。笔记同时承认种量、热程和上游因素有混杂。失败条件是新的范围信息；其提出的固态/溶解度历史原因仍是候选，不能仅凭末端读数视为已识别机制。

v3：

> rejecting monotone extrapolation and suggesting a sharp upstream/solid-state or solubility-history failure.

## repeat-01/C-W03-Aligned

状态：completed；[笔记全文](repeat-01/C-W03-Aligned-notebook.md) / [后测](repeat-01/C-W03-Aligned-reports.md) / [执行时序](sessions/repeat-01/C-W03-Aligned.json)。

形成了高回收细粉过多与低细粉回收很低的工艺权衡，最终承认没有测试配方同时达到0.10回收及质量要求，没有因操作失败就丢弃本场。对增种无效的解释存在执行依据问题：第2批成功种量仅0.05 g，3次追加被拒，却在中期和末期被记成0.20 g阴性检验；温暖/延长老化的候选原因仍须和实际量变化区分。

v2：

> 0.20 g total seed in batch 2 coincided with fines=1

v3：

> No tested recipe combined recovery >=0.10 with the stated purity and fines constraints.

执行锚点：20, 21, 22, 23。

## repeat-01/C-W03-MisIndexed

状态：completed；[笔记全文](repeat-01/C-W03-MisIndexed-notebook.md) / [后测](repeat-01/C-W03-MisIndexed-reports.md) / [执行时序](sessions/repeat-01/C-W03-MisIndexed.json)。

仅有事前与源期末两版笔记，因此没有中途更新后继续实验的完整观察窗口，不能将此判作未学习。末版把S2先验限制在纯度/回收层面，承认降装料后的形貌改善仍未达到细粉阈值，并明确推荐不合格候选。降低装料还同时改变体积、催化剂与种量，不能把它独立归因于浓度。真正种量0.02/0.05 g等有成功执行记录，与将被拒大种量写成已测的案例不同。

v2：

> Recommend batch 12 only as the closest tested candidate and best basis for further work, not as specification-compliant.

## repeat-01/C-W04-Opaque

状态：completed；[笔记全文](repeat-01/C-W04-Opaque-notebook.md) / [后测](repeat-01/C-W04-Opaque-reports.md) / [执行时序](sessions/repeat-01/C-W04-Opaque.json)。

从前两批形貌不足出发，形成极小合法种量加长时分段热程的可行流程，并继续筛材料及反应温度。末版虽然将这组操作称为关键干预，却明确保留种量与停留时间各自贡献未分离；小回收优势也要求重复。所谓最低有效种量来自冷却能否执行等反馈，不等于直接测量到了通用种量阈值。实际种晶记录显示第3批两次合法微量加种合计约0.0001 g，不能把多次请求一概当成失败或越界。

v4：

> Exact causal shares of seed dose and residence time remain confounded.

## repeat-01/C-W04-Aligned

状态：completed；[笔记全文](repeat-01/C-W04-Aligned-notebook.md) / [后测](repeat-01/C-W04-Aligned-reports.md) / [执行时序](sessions/repeat-01/C-W04-Aligned.json)。

先验给S2优先，但源研究转向S1/C1的可行流程；后期高温短时组合改善回收，记录明确限制在组合条件，不当作一般动力学规律。较高回收的第10批因细粉不合格被排除，选择第9批并保留近阈值风险。第8批从0.02 g改为合法0.05 g并延长热程，不能独立把改进归于种量；末批一次追加被拒，末版没有把它写成成功的大剂量对照。

v3：

> This trend is bounded to the tested duration/temperature combinations and is not a general kinetic law.

## repeat-01/C-W02-Aligned

状态：completed；[笔记全文](repeat-01/C-W02-Aligned-notebook.md) / [后测](repeat-01/C-W02-Aligned-reports.md) / [执行时序](sessions/repeat-01/C-W02-Aligned.json)。

288步长研究探索多种种量与热程，但末版明确承认12批均无合格细粉，并把高回收第12批标为不合格推荐。只有事前和最终两版，不提供更新后继续实验的完整窗口。最终质量分类11/12与操作不达标并存；仍须结合题目类别分布解释，不能由分类正确数推定机制已经识别。推荐复测保留长流程及重放，未用更短/更有利配方替换。

v2：

> No completed batch meets purity >=0.80 and fines <=0.50.

## repeat-01/C-W04-MisIndexed

状态：completed；[笔记全文](repeat-01/C-W04-MisIndexed-notebook.md) / [后测](repeat-01/C-W04-MisIndexed-reports.md) / [执行时序](sessions/repeat-01/C-W04-MisIndexed.json)。

最终保留C1/S2并局部加密345–347.5 K反应条件，把最佳已测配方与连续最优区分。种量和热程联合变化被明确承认为混杂，不能单独建立种晶机制。只有首尾两版记录，无完整中途修订窗口；末版对最佳温度范围的表述为带边界的研究结果，后测纯度仍出现负偏差，二者分别记录而不以终分倒推源期全部无效。

v2：

> The 347.5 K result is the highest qualifying recovery observed, not a proven continuous optimum.

## repeat-01/C-W05-Opaque

状态：completed；[笔记全文](repeat-01/C-W05-Opaque-notebook.md) / [后测](repeat-01/C-W05-Opaque-reports.md) / [执行时序](sessions/repeat-01/C-W05-Opaque.json)。

源期将S1质量可行性与S2较低细粉分开，保留C0/C3小回收差异未决。降低S1体积虽增回收但越过细粉阈值，最终返回已测合格第4批，并明确没有精确重复。初始设想0.3–0.6 g种量，实际全期成功量仅0.03–0.05 g，末版按实际0.05 g描述，未把初始高剂量预期虚构为已做对照。

v3：

> Batch 4 was not exactly replicated; final-assay uncertainty is much smaller than its margins to the purity and fines limits, but broader process repeatability is unknown.

## repeat-01/C-W05-Aligned

状态：completed；[笔记全文](repeat-01/C-W05-Aligned-notebook.md) / [后测](repeat-01/C-W05-Aligned-reports.md) / [执行时序](sessions/repeat-01/C-W05-Aligned.json)。

可作为正向连续主例：合法高种量热循环未达标后，0.03 mol批次的细粉仍略高于阈值；v5在末批前提出降至0.02 mol的明确预期。核对第11/12批，除独立容器编号及试剂量外，其余提交的成功操作和参数一致；细粉从0.529降至0.387，回收分数从0.488升至0.520。v6将最后检验用于推荐，同时保留单次比较及作用机制未分离的边界。这个局部成功不自动证明跨条件预测充分可靠，也不要求另加纠错策略。

v5：

> A further reduction to 0.02 mol at unchanged solvent, catalyst, seed, and slow cool is predicted to cross the fines limit

v6：

> Scope caveat: the apparent loading trend has only one batch at each loading, so repeatability and separate catalyst/loading effects remain unresolved;

执行锚点：120, 121, 122, 123, 124, 125, 126, 127, 128, 130, 131, 132, 133, 134, 135, 136, 137, 138。

## repeat-02/C-W03-MisIndexed

状态：completed；[笔记全文](repeat-02/C-W03-MisIndexed-notebook.md) / [后测](repeat-02/C-W03-MisIndexed-reports.md) / [执行时序](sessions/repeat-02/C-W03-MisIndexed.json)。

先以共同流程筛溶剂，再筛催化剂，由C1先验转向C3/S2，并以较短反应和更低结晶终点继续优化。末版明确区分最高观测回收与真正优于邻近条件，0.001差异不足以排序，另结合粒度读数选择。与同条件第一次未找到合格配方不同，本次找到联合合格流程；这是相同世界/信息下的路径差异，不能单次定义模型的固定研究风格。

v4：

> The 0.001 recovery difference is far below the declared assay noise and is not evidence that 900 s is truly superior.

## repeat-01/C-W05-MisIndexed

状态：completed；[笔记全文](repeat-01/C-W05-MisIndexed-notebook.md) / [后测](repeat-01/C-W05-MisIndexed-reports.md) / [执行时序](sessions/repeat-01/C-W05-MisIndexed.json)。

高纯度局部关系被保留，但不同催化剂、减装料及再热路线仍未达细粉要求。最接近阈值的0.5031没有被改判为合格；研究者明确区分噪声尺度与现行判定规则，推荐仅作待确认候选。第4批3次追加被拒、成功种量0.05 g，笔记使用0.02–0.05 g实际范围，没有明确虚构0.20 g对照。

v3：

> The difference from the 0.50 limit is small relative to the declared final-assay noise scale, but the observed value is still formally noncompliant.

## repeat-02/C-W03-Aligned

状态：completed；[笔记全文](repeat-02/C-W03-Aligned-notebook.md) / [后测](repeat-02/C-W03-Aligned-reports.md) / [执行时序](sessions/repeat-02/C-W03-Aligned.json)。

中期把第10批的1 g种量当作阴性证据，实际仅0.05 g成功、19次追加被拒；因此对种量不足或饱和的排除没有所称对照支持。末批降低装料并改变终点/停留后找到合格流程，末版承认这些贡献未分离，却仍将失败的增种叙述用于解释主要限制。可以同时保留真实的局部工艺成功与不充分的原因判断，不能用前者抵消后者，也不能推断错误叙述造成了末批选择。

v3：

> increasing S3 seed from 0.05 g to 1.0 g left fines near 0.85–0.87

v4：

> the separate contributions of dilution versus colder endpoint/longer hold remain unresolved.

执行锚点：135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154。

## repeat-02/C-W03-Opaque

状态：completed；[笔记全文](repeat-02/C-W03-Opaque-notebook.md) / [后测](repeat-02/C-W03-Opaque-reports.md) / [执行时序](sessions/repeat-02/C-W03-Opaque.json)。

事前明确根据总投料回收口径优先上游形成目标物，与旧口径记录中的研究理由可以对照，但不同模型会话/时期不能作随机提示效应估计。后续围绕C1/S2提出250 K终点检验并保留小差异未决。末批同时延长停留，笔记所称confirmation不能等同于完全相同配方的精确重复；跨温度/催化剂的多次达标也应解释为已测范围支持而非独立重复性估计。

v1：

> Because crystal yield is overall reagent recovery and excludes seed, maximize upstream target formation before optimizing crystallization.

v4：

> the recovery difference is too small to claim beyond assay/process variability without further repeats.

## repeat-02/C-W05-MisIndexed

状态：failed；[笔记全文](repeat-02/C-W05-MisIndexed-notebook.md) / [后测](repeat-02/C-W05-MisIndexed-reports.md) / [执行时序](sessions/repeat-02/C-W05-MisIndexed.json)。

前五批形成C0的质量可行基准和C3高回收但细粉超标的候选，随后预告分段延长冷却并明确承认同时降反应温度会混杂解释。第6批完成后发生通道错误上限，后测全部缺失；可保留6批观测和事前计划，不能补写对第6批的后续修订或预测表现。这是中断的研究链，不是该科学预期被实验证伪。

v2：

> A lower reaction temperature is also tested, so interpretation will remain confounded unless followed by a targeted comparison.

## repeat-02/C-W04-MisIndexed

状态：completed；[笔记全文](repeat-02/C-W04-MisIndexed-notebook.md) / [后测](repeat-02/C-W04-MisIndexed-reports.md) / [执行时序](sessions/repeat-02/C-W04-MisIndexed.json)。

试剂和种量/热程调整之后，在370–375 K附近保留可行工作区间，再实际筛催化剂并重做第7批主要配方。核对第7/12批：主要制备操作及参数相同，第7批另有一次粒径测量，因此支持配方重做但并非完全相同的完整命令序列。两次细粉0.479与0.494都近阈值，末版保留温度排序与稳健性未决，并区分最高观测目标与安全余量较大的备选。

v4：

> Batch 12 repeated the batch-7 recipe and remained feasible

v4：

> Exact temperature superiority is unresolved because differences are modest and uncertainty/process variability were not independently quantified.

## repeat-02/C-W04-Aligned

状态：completed；[笔记全文](repeat-02/C-W04-Aligned-notebook.md) / [后测](repeat-02/C-W04-Aligned-reports.md) / [执行时序](sessions/repeat-02/C-W04-Aligned.json)。

中期先对420 K短时组合提出收益预期，随后440 K相关热史出现液相产率高而晶体回收极低，再在结果出现前提出430 K边界检验。末版保留420–430 K的局部可行区间，同时不声称已识别骤降原因。两次440 K试验改变了冷却终点，且反应温度/时长联动，因此是对具体热史范围的支持，不是独立温度定律。局部工艺推荐达标与后测纯度负偏差、较差质量分类可以同时成立。

v4：

> An intermediate reaction at 430 K/750 s should test the boundary.

v5：

> Mechanistic cause remains unresolved.

## repeat-02/C-W04-Opaque

状态：completed；[笔记全文](repeat-02/C-W04-Opaque-notebook.md) / [后测](repeat-02/C-W04-Opaque-reports.md) / [执行时序](sessions/repeat-02/C-W04-Opaque.json)。

前期把0.5 g增种当作未奏效，实际第4批只有0.05 g成功、9次追加被拒，所称大剂量阴性证据不存在。后期S3组合取得联合合格结果，且明确部分回收小差异尚未确认；这不补足此前缺失的种量检验。高温加种的‘必要性’也只能限定于已测配方，淬灭、温度及热程未全面独立对照，不应升级为唯一机制。

v2：

> increasing seed from 0.02 g to 0.5 g did not solve fines.

v3：

> This is a bounded empirical relationship, not an identified mechanism.

执行锚点：51, 52, 53, 54, 55, 56, 57, 58, 59, 60。

## repeat-02/C-W05-Aligned

状态：completed；[笔记全文](repeat-02/C-W05-Aligned-notebook.md) / [后测](repeat-02/C-W05-Aligned-reports.md) / [执行时序](sessions/repeat-02/C-W05-Aligned.json)。

完整的局部预期—否定—选择链：v3在第12批前预测0.065 L S2能够兼顾回收与细粉；实际第11/12批分别投入0.06/0.065 L，后者细粉0.6013未达标，v4明确撤回简单插值并选择已有合格的第4批。推荐复测联合达标，回收预测MAE约0.138。这个正向修订与另一个执行记述偏差同时存在：v3/v4称0.20 g晶种未能挽救S0/S1，但第9/10批各仅一次0.05 g成功，随后三次0.05 g均被拒。因此该高种量阴性解释并未由真实执行支持；不能由此反推它造成了溶剂选择。

v3：

> Prediction before batch 12: an intermediate 0.065 L loading with the established 270 K slow cooling should preserve most recovery gain while bringing fines below 0.50.

v4：

> The precommitted expectation that intermediate 0.065 L S2 would retain recovery while restoring fines below 0.50 was not supported

v4：

> Warmer endpoints, slower cooling, longer holds, and 0.20 g seed did not rescue S0/S1

执行锚点：121, 122, 123, 124, 138, 139, 140, 141, 150, 164。

## repeat-02/C-W05-Opaque

状态：completed；[笔记全文](repeat-02/C-W05-Opaque-notebook.md) / [后测](repeat-02/C-W05-Opaque-reports.md) / [执行时序](sessions/repeat-02/C-W05-Opaque.json)。

v1/2从匿名材料筛选和初期细粉失败出发；v3明确一次温和回温循环未支持预期，转而提出分段冷却；v4在低投料接近边界后提出进一步降低投料及细化冷却。第11→12批细粉0.533→0.228，回收0.351→0.333，最终选择唯一合格批，复测也联合达标。执行核对证实试剂0.02→0.018 mol、催化剂同比降低，并将10 K步长改为5 K、增加冷却段数；不是单变量浓度因果对照。最终笔记自述混杂与未重复，故可作有边界的前瞻检验/采用证据，不能确立浓度独立机制。回收预测MAE约0.112。

v4：

> Prediction: slightly lower loading plus finer staging should push fines below 0.50 while preserving recovery near the ~0.35 observed at 0.02 mol.

v5：

> Loading and staging are confounded between the last two batches; both may contribute, and repeatability is unknown.

执行锚点：139, 152, 141, 154, 145, 158。

## repeat-02/C-W01-MisIndexed

状态：completed；[笔记全文](repeat-02/C-W01-MisIndexed-notebook.md) / [后测](repeat-02/C-W01-MisIndexed-reports.md) / [执行时序](sessions/repeat-02/C-W01-MisIndexed.json)。

只有零操作事前笔记与145操作后的终末修订，不能从这两版建立中段判断持续影响选择的证据。最终记录把C1先验改为C0局部最优、描述较热较短联合路径，并对晶种/温度混杂和接近噪声的回收差异作出限制。推荐复测联合达标，回收预测MAE约0.069，但质量分类仅5/12、纯度平均偏差约−0.085；操作成功与新条件判断仍应分别呈现。MisIndexed并不意味着其常用S2披露也错配。

v2：

> This comparison is confounded by changing reaction conditions, so it supports the combined process rather than an isolated seed effect.

## repeat-02/C-W01-Aligned

状态：completed；[笔记全文](repeat-02/C-W01-Aligned-notebook.md) / [后测](repeat-02/C-W01-Aligned-reports.md) / [执行时序](sessions/repeat-02/C-W01-Aligned.json)。

v2在第9批后识别0.03/0.04 L的形貌边界，提出保留0.04 L并探索热史；v3说明三种复杂热史未改进并选择第8批。它没有把浓度收益无限外推，最终自述单批差异与未量化重复性。推荐复测联合达标，回收MAE约0.115，质量分类5/12；局部边界认识与查询域预测能力仍非同一结果。这里依据版本时序描述公开计划和修订，未把笔记表述当作行动的唯一原因。

v2：

> thus the usable concentration window has a sharp morphology boundary between 0.03 and 0.04 L for the tested seed/cooling schedule.

v3：

> These are numerical differences from single batches, not established causal effects; run-to-run variability is not separately quantified.

## repeat-02/C-W01-Opaque

状态：completed；[笔记全文](repeat-02/C-W01-Opaque-notebook.md) / [后测](repeat-02/C-W01-Opaque-reports.md) / [执行时序](sessions/repeat-02/C-W01-Opaque.json)。

v2在首批后识别wait期间回暖，因此不把这一步误称恒定低温停留；随后从稀释/种量/分段冷却的组合改进转入材料筛选。v3提出保持S2结晶工艺、调整上游反应，v4总结较热较短路径提升回收，同时承认温度/时间共同变化和单批限制。推荐复测联合达标，回收预测MAE约0.043、纯度平均偏差接近零，但质量分类4/12，提示响应层面表现仍需分开。没有额外晶种请求被拒；合法0.05 g上限的使用不必伴随错误高种量记述。

v2：

> The subsequent 3600 s wait warmed the slurry to 291.2 K

v4：

> These are numerical differences from single batches with simultaneous temperature/time changes, so the separate causal effects and optimum beyond the explored boundary remain unresolved.

## repeat-02/C-W02-MisIndexed

状态：completed；[笔记全文](repeat-02/C-W02-MisIndexed-notebook.md) / [后测](repeat-02/C-W02-MisIndexed-reports.md) / [执行时序](sessions/repeat-02/C-W02-MisIndexed.json)。

仅有事前与源期终末两版，缺少可直接观察的中段笔记反馈循环。终末从早期高细粉与后期热史改变概括回收—细粉折衷，将第12批0.504明确保留为不合格，并推荐第11批，不把噪声可能性当作越过阈值的理由。回热/再冷失败被限制在所测形式，未排除所有热端点。推荐复测联合达标，回收预测MAE约0.094、分类6/12；这些是局部工艺结果与后测的分别读出，不能把回顾叙述当作中段实验选择的同期原因。

v2：

> This locates the practical boundary near the batch 11 history, but assay noise and lack of replicate process variance make the exact threshold unresolved.

## repeat-02/C-W02-Opaque

状态：completed；[笔记全文](repeat-02/C-W02-Opaque-notebook.md) / [后测](repeat-02/C-W02-Opaque-reports.md) / [执行时序](sessions/repeat-02/C-W02-Opaque.json)。

事前提出材料筛选及慢冷/种量预期，直到181操作后的终末才更新，因此不可重建中段笔记—下一行动循环。最终明确所有细粉仍超标，区分最接近目标的第8批与真正合格工艺；重复回热、更强回热及降低投料被限制为所测范围的负结果。推荐复测未联合达标，回收MAE约0.092、质量分类4/12。该例说明没有得到合格配方也可以形成范围明确的负向判断；不能把整场操作失败等同为没有形成认识。

v2：

> I will recommend batch 8 as the closest quality/recovery compromise, not as a constraint-satisfying process.

## repeat-02/C-W02-Aligned

状态：completed；[笔记全文](repeat-02/C-W02-Aligned-notebook.md) / [后测](repeat-02/C-W02-Aligned-reports.md) / [执行时序](sessions/repeat-02/C-W02-Aligned.json)。

有明确的公开计划—执行失败—证据地位修订链。v3提出累计约1 g种晶；第7、9、10、11批各20次0.05 g请求中，首笔成功、19笔被拒（共76次拒绝）。v4正确依据资源摘要撤回高剂量解释，说明这些批次不能支持高种量效应。它构成同类平台拒绝被正确解释的对照，而非所有被拒请求必然形成误认。全程没有合格配方，v5仍将第12批标为细粉不合格；与第9批相比同时改变体积和冷却终点，最终也明确承认。推荐复测未联合达标，回收MAE约0.077、质量分类5/12。认识修订的价值不能由工艺是否达标单独判定。

v3：

> batch 7 will test repeated seed additions totaling about 1 g.

v4：

> Repeated identical seed additions did not create a cumulative high-dose treatment: campaign resource summaries show only 0.05 g seed used in batches 7 and 9–11. Thus their outcomes cannot support a high-dose-seed effect.

执行锚点：120, 121, 139, 170, 171, 189, 204, 205, 223, 238, 239, 257。

## repeat-03/C-W05-Aligned

状态：completed；[笔记全文](repeat-03/C-W05-Aligned-notebook.md) / [后测](repeat-03/C-W05-Aligned-reports.md) / [执行时序](sessions/repeat-03/C-W05-Aligned.json)。

v2在四批均合格后把材料筛选收窄到C0/S2并安排反应温度、溶剂和热史检验；v3提出更深冷却及生长停留；v4把较热较短与深冷/停留的组合收益用于选择第12批，同时承认混杂、未重复及细粉接近边界。推荐复测联合达标，但回收MAE约0.156，明显高于同条件第1次的约0.041。三次工艺均能达标并不意味着形成相同路线或同等外推能力。

v4：

> temperature and duration changed together and each condition lacks replication, so the precise causal law and optimum remain unresolved.

## repeat-03/C-W05-MisIndexed

状态：completed；[笔记全文](repeat-03/C-W05-MisIndexed-notebook.md) / [后测](repeat-03/C-W05-MisIndexed-reports.md) / [执行时序](sessions/repeat-03/C-W05-MisIndexed.json)。

v2由催化剂比较选择C3并安排溶剂筛选，末版从最初S2转向S1的局部可行工艺。它没有机械追逐最高点估计：第12批回收仅稍高且细粉更近边界，因此选择第10批；推荐复测联合达标。对种量效应保持未决，并明确未重复。回收预测MAE约0.182，分类7/12，局部合理的选择与较弱的新条件定量预测仍可并存。MisIndexed仅S1/S3披露交换，不能把S2初始预期也视为错配。

v3：

> Recommend batch 10 rather than batch 12: batch 10 has essentially the same recovery within measurement resolution (0.630 vs 0.633) but a more defensible fines margin (0.433 vs 0.487)

## repeat-03/C-W05-Opaque

状态：completed；[笔记全文](repeat-03/C-W05-Opaque-notebook.md) / [后测](repeat-03/C-W05-Opaque-reports.md) / [执行时序](sessions/repeat-03/C-W05-Opaque.json)。

v2在材料/形貌筛选后明确暂停广泛催化剂搜索，转向S1/S2边界优化；v3保留S1未解决细粉、S2多个终点合格的局部关系，并把更低体积末批用于推荐。它将所见趋势限制为工作关系而非精确规律，且把更大细粉裕量的第11批列为备选。第2批存在一次0.05 g成功和9次追加拒绝，但所读笔记仅声称0.05 g，不把拒绝请求记成实际0.5 g检验。推荐复测联合达标；回收预测MAE约0.164、分类10/12，不因工艺成功而推定回收迁移精确。

v2：

> Suspend broad catalyst screening unless refined crystallization loses feasibility.

v3：

> the trend is useful but not a precision law.

## repeat-03/C-W01-Aligned

状态：completed；[笔记全文](repeat-03/C-W01-Aligned-notebook.md) / [后测](repeat-03/C-W01-Aligned-reports.md) / [执行时序](sessions/repeat-03/C-W01-Aligned.json)。

v2明确把较冷/较长冷却与种量、反应条件共同改变视为组合工艺，提出沿用结晶工艺做反应筛选；末版收窄到C0/S2局部配方，描述提高浓度同时提高细粉的约束。第9与12批回收近乎相同，最终因细粉裕量选择第9批，推荐复测联合达标。它保留未正交分离和未重复的限制；回收MAE约0.133、纯度偏差约−0.090、分类5/12，不能由审慎表述或合格操作推定新条件预测可靠。

v2：

> treat this as a process-package improvement rather than a single-factor estimate.

v3：

> The ~0.0006 recovery difference between batches 9 and 12 is negligible relative to single-assay noise

## repeat-03/C-W01-Opaque

状态：completed；[笔记全文](repeat-03/C-W01-Opaque-notebook.md) / [后测](repeat-03/C-W01-Opaque-reports.md) / [执行时序](sessions/repeat-03/C-W01-Opaque.json)。

v2由对角材料筛选识别形貌差异，同时承认催化剂/溶剂共同改变，下一步转入S2催化剂及热史检验。末版选择0.03 L加细分段冷却的第12批，保留细粉接近边界和工艺组合混杂，并提出将来应固定冷却序列检验体积。推荐复测联合达标，回收MAE约0.077、分类7/12；既不能把混杂的材料筛选解释成溶剂独立因果，也不能因未完全辨识机制而否认局部可行配方。

v3：

> a future confirmation should repeat batch 12 and separately test solvent loading while holding the exact cooling schedule fixed.

## repeat-03/C-W01-MisIndexed

状态：completed；[笔记全文](repeat-03/C-W01-MisIndexed-notebook.md) / [后测](repeat-03/C-W01-MisIndexed-reports.md) / [执行时序](sessions/repeat-03/C-W01-MisIndexed.json)。

先由深冷全细粉转向直接温和冷却，再比较等待次数和端点；v5明确提出最后一批重复310 K/两次等待配方，v6据第8批细粉0.489911与第12批0.504891跨越阈值而承认边界不稳。执行核对：主要制备/热史动作一致，但第8批多一次非破坏粒径测量，因此是主要配方重做，不能称整条指令完全相同。推荐仍为观测回收更高且当时合格的第8批；无噪复测细粉0.502934，故联合未达标。回收预测MAE约0.0405，同时纯度偏差约−0.0921。此例连起前瞻重复、边界修订、按观测选择及复测未达标，不能把两次含噪终检直接解释为两次独立物理世界采样。

v5：

> use the last batch as an exact 310 K/two-hold repeat.

v6：

> showing that fines performance is borderline rather than robust.

执行锚点：95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151。

## repeat-03/C-W02-Aligned

状态：completed；[笔记全文](repeat-03/C-W02-Aligned-notebook.md) / [后测](repeat-03/C-W02-Aligned-reports.md) / [执行时序](sessions/repeat-03/C-W02-Aligned.json)。

仅两版事前/终末笔记。终末正确说明12批均未满足细粉约束，推荐第8批时保留不合格状态；但H3把0.5 g温种晶与3 g冷种晶记为无效检验。执行核对：第7批首笔0.05 g成功、9次追加拒绝，第12批首笔成功、59次追加拒绝，所以两组均只实际加入0.05 g，不能作为高剂量阴性证据。它与同世界同信息条件第2次正确撤回高剂量解释形成重复间对照；不是固定模型性格，也未识别引起差异的原因。推荐复测未联合达标，回收MAE约0.130、分类7/12。

v2：

> 0.5 g warm seeding (batch 7), and 3 g cold seeding (batch 12) all retained near-unity fines.

执行锚点：92, 93, 101, 177, 178, 236。

## repeat-03/C-W02-Opaque

状态：completed；[笔记全文](repeat-03/C-W02-Opaque-notebook.md) / [后测](repeat-03/C-W02-Opaque-reports.md) / [执行时序](sessions/repeat-03/C-W02-Opaque.json)。

v2在S0催化剂筛选后先完成计划中的溶剂比较，再围绕S2改善粒度；v3承认种量和冷却时长共同变化，并保留0.06 L高回收但细粉不合格的边界，选择第10批0.08 L方案。推荐复测联合达标，但回收预测MAE约0.196、质量分类4/12，不能以工艺成功推定后测可靠。与同条件第2次未找到合格配方并列说明路径波动；这种差异本身不证明自我确认或某项判断的因果影响。

v3：

> so the apparent concentration benefit is not recommended without further particle-control work.

## repeat-03/C-W02-MisIndexed

状态：completed；[笔记全文](repeat-03/C-W02-MisIndexed-notebook.md) / [后测](repeat-03/C-W02-MisIndexed-reports.md) / [执行时序](sessions/repeat-03/C-W02-MisIndexed.json)。

v2将名义催化剂顺序收窄到所测C0/S2区域，明确较低温/较长时长并不自动改善结果，随后提出种量/端点/溶剂检验。v3回到前期近边界配方，选择第12批，同时保留第1批较低回收但更大细粉裕量作为备选。自述第2批为近重复，未把两次细粉约0.49当成稳健概率。推荐复测联合达标，回收MAE约0.080、分类7/12。这里可说明局部工艺选择和不确定性表述，不能单凭终末归因确认种量独立机制。

v3：

> robustness at the boundary is unresolved; batch 1 offers a lower-recovery but larger observed fines margin.

## repeat-03/C-W03-Aligned

状态：completed；[笔记全文](repeat-03/C-W03-Aligned-notebook.md) / [后测](repeat-03/C-W03-Aligned-reports.md) / [执行时序](sessions/repeat-03/C-W03-Aligned.json)。

v2/v3把1 g种量写为未解决细粉的检验，但第2批只有0.05 g成功，随后19次追加被拒；这部分阴性解释缺乏执行支持。v3又提出S3更多晶种/热史检验，第8批存在39次追加拒绝，不能将意向2 g视作真实给料。最终第9批S3/C1的联合深冷及长等待配方达标，v4正确保留端点/停留未分离，并据其他催化剂在该工作程序中未达标作局部选择。推荐复测联合达标，回收MAE约0.035、纯度偏差约−0.0045；较好的数值预测与一项错误高种量证据记述也可并存，不应由分数反推证据解释全部正确。

v2：

> Raising seed charge from 0.05 g to 1.0 g plus a long low-temperature hold did not solve fines

v4：

> The effect is associated with the combined deeper cooling plus long hold; those factors were not separated.

执行锚点：24, 25, 43。

## repeat-03/C-W03-Opaque

状态：completed；[笔记全文](repeat-03/C-W03-Opaque-notebook.md) / [后测](repeat-03/C-W03-Opaque-reports.md) / [执行时序](sessions/repeat-03/C-W03-Opaque.json)。

只有事前与末版两次记录，无法直接追踪中段判断更新进入下一行动。末版明确所有细粉约0.99–1.00、没有合格批，推荐第1批时仍保留不合格标签，并将因素不敏感限定为所测范围，拒绝声称零效应。执行有第2批9次和第5批39次种量追加被拒；笔记笼统写repeated seed addition，未给出高累计量，也未明确识别拒绝，因此既不能当作已成功高剂量检验，也不能标为正确核对拒绝的反例。推荐复测未联合达标；回收MAE约0.145、纯度偏差接近零、分类8/12。

v2：

> measurement uncertainty plus recipe confounding prevent claiming zero effect.

## repeat-03/C-W04-MisIndexed

状态：failed；[笔记全文](repeat-03/C-W04-MisIndexed-notebook.md) / [后测](repeat-03/C-W04-MisIndexed-reports.md) / [执行时序](sessions/repeat-03/C-W04-MisIndexed.json)。

只留下零操作时点的初始假说；源阶段随后因max_provider_error_events达到既定上限中断，没有完成源批次，K1/Q/K2及推荐复测均缺失。它是必须保留的技术性不完整链，不能根据没有后续修订判作未学习，也不能把缺失预测或复测填成科学失败。未补跑替换。

v1：

> This may fail if fixed-world residuals reverse the dossier ranking.

## repeat-03/C-W04-Aligned

状态：completed；[笔记全文](repeat-03/C-W04-Aligned-notebook.md) / [后测](repeat-03/C-W04-Aligned-reports.md) / [执行时序](sessions/repeat-03/C-W04-Aligned.json)。

v2由纯S0高回收但细粉失败、S1合格的折衷提出热循环及S1改进；v3总结20% S0/80% S1混合溶剂配方两次合格，且30%配方也合格但优势未决。第10/12批的主要制备、配比和热控动作相同，第10批多一次非破坏粒径测量，不能声称整条操作记录完全相同。两批回收约0.501/0.495、细粉约0.451/0.441，推荐第10批并明确小差异不是本质更优；复测联合达标。回收预测MAE约0.035、分类9/12。它提供局部混合配方、重复和适用范围的正向材料，但只有三版笔记，没有单独的事前混合比例预测，不能补写成对该混合比例预期的完整前瞻验证。

v3：

> the small yield difference is within assay-scale variability and is not evidence that batch 10 is intrinsically better.

执行锚点：112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149。

## repeat-03/C-W03-MisIndexed

状态：completed；[笔记全文](repeat-03/C-W03-MisIndexed-notebook.md) / [后测](repeat-03/C-W03-MisIndexed-reports.md) / [执行时序](sessions/repeat-03/C-W03-MisIndexed.json)。

v2从额外冷阶段改善回收但恶化细粉的观察收窄到单冷阶段；v3在275/270 K两批均合格后事前提出265 K末批检验，若超标则退回已有配方。v4因末批回收0.571、细粉0.424而选择第12批，并保留端点排名未决，推荐复测联合达标。关于杂质/过饱和控制的表述仍是解释，未由这些复合条件独立识别。回收预测MAE约0.126、纯度偏差约−0.080、分类10/12；前瞻性局部检验与不同响应的迁移误差应分开。

v3：

> If fines exceed 0.50, prefer B10/B11 rather than the colder endpoint.

v4：

> exact endpoint ranking remains unresolved within assay/process variability.

## repeat-03/C-W04-Opaque

状态：completed；[笔记全文](repeat-03/C-W04-Opaque-notebook.md) / [后测](repeat-03/C-W04-Opaque-reports.md) / [执行时序](sessions/repeat-03/C-W04-Opaque.json)。

v2在285 K近边界失败与290 K合格后，事前提出288–290 K窗口并安排稍低终点、催化剂及热史检验；v3据几批合格结果保留有范围的工作窗口，并承认温度排序和重复差异未决。单次差值大于一个仪器噪声尺度不等于已完成显著性或重复性检验，不能提升为精确温度阈值。最终选择第8批，推荐复测联合达标；回收预测MAE约0.115、纯度偏差约−0.008、分类9/12。末批较低温/较长时长的负结果明确不隔离温度效应。

v2：

> Prediction: 288–290 K should remain near the fines limit and may maximize qualified recovery.

v3：

> Exact temperature ranking is unresolved because recovery differences are on the order of the reported assay noise
