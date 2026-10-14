# 全队列研究反馈窗口的语义分析

已编码 58/58 个预先列出的结构窗口，逐字核对 116 条指定版本引文。
标注来自单一分析者，尚未独立复核。

匹配表示选定的公开计划与实际动作相符；初始既定设计与反馈调整在解释中分别说明。
更新类型表示研究者公开作出了怎样的判断，不等于关系已被科学证实。

## 覆盖进度

| 体系 | 全部会话 | 已编码/计划窗口 | 有窗口且全部编码的会话 | 无完整观察窗口的会话 |
| --- | ---: | ---: | ---: | ---: |
| C | 45 | 58/58 | 35 | 10 |

## 完整覆盖后的描述性计数

会话列表示至少有一个该标签窗口的会话数，分母仅为具有窗口的会话；
10场无窗口会话单独保留。窗口嵌套于会话，不能作为58个独立样本。
公开更新标签允许重叠；同一会话也可有不同执行标签，因此会话列不可相加。
matched仅评估所选即时计划；不表示新发现、反馈导致行动或计划的全部内容均执行。

| 标签 | all窗口 /58 | all会话 /35 | C窗口 /58 | C会话 /35 |
| --- | ---: | ---: | ---: | ---: |
| action_link: matched | 52 | 32 | 52 | 32 |
| action_link: no_explicit_plan | 0 | 0 | 0 | 0 |
| action_link: not_executed | 0 | 0 | 0 | 0 |
| action_link: partly_matched | 6 | 6 | 6 | 6 |
| action_link: rejected | 0 | 0 | 0 | 0 |
| action_link: unclear | 0 | 0 | 0 | 0 |
| update_types: established | 58 | 35 | 58 | 35 |
| update_types: narrowed | 55 | 34 | 55 | 34 |
| update_types: restated | 0 | 0 | 0 | 0 |
| update_types: revised | 41 | 30 | 41 | 30 |
| update_types: unassessable | 0 | 0 | 0 | 0 |
| update_types: unresolved | 51 | 35 | 51 | 35 |

完整解释见[研究过程综合分析](REVIEW.md)。

## 已完成窗口

| 会话与版本 | 公开更新 | 计划执行 | 解释 |
| --- | --- | --- | --- |
| [repeat-01/C-W01-MisIndexed](sessions/repeat-01/C-W01-MisIndexed.json) v1→v2 | established, narrowed, unresolved | matched | 四种催化剂结果后把C0作为工作选择并保留小差异未决；随后C0下完成S0/S1/S3筛选。材料筛选初始已计划，具体固定C0是后版明确；不将排序当作机制识别。 |
| [repeat-01/C-W01-Opaque](sessions/repeat-01/C-W01-Opaque.json) v1→v2 | established, revised, narrowed, unresolved | matched | 前八批形成S2及混合溶剂可行关系，同时承认热史与材料混杂；第9批落实C0/S2的330K/7200s检验。这里匹配的是温度/时长检验，不据此宣布同句所有重复计划均落实。 |
| [repeat-01/C-W02-MisIndexed](sessions/repeat-01/C-W02-MisIndexed.json) v1→v2 | established, revised, unresolved | matched | 初始材料筛选后调整催化剂排序，固定C0开展溶剂与热程比较；低温过滤判断仍保留混杂。后续追加种量被拒，不能用此计划匹配推定整段所有检验成功。 |
| [repeat-01/C-W02-Opaque](sessions/repeat-01/C-W02-Opaque.json) v1→v2 | established, narrowed, unresolved | matched | 溶剂筛选后收窄慢冷解释，选择S1继续三种催化剂筛选。材料筛选原已计划，S1的具体选择和可行边界在结果后明确；重复性仍未决。 |
| [repeat-01/C-W02-Opaque](sessions/repeat-01/C-W02-Opaque.json) v2→v3 | established, narrowed, unresolved | matched | 新结果支持若干合格配方，研究者保留单次试验边界，提出370K反应与280K冷却的组合预期并在第12批执行；温度、种量和持温变化不能拆成单一机理效应。 |
| [repeat-01/C-W03-Aligned](sessions/repeat-01/C-W03-Aligned.json) v1→v2 | established, revised, narrowed, unresolved | partly_matched | 获得高纯度但粒度/回收权衡后尝试重复并调整老化；第8批试剂投料被拒，部分热处理与播种执行，不能视作成功重复原配方。同版将第2批0.20g当作证据，原逐场核对显示追加被拒，故修订标签不证明叙述真实。 |
| [repeat-01/C-W03-Opaque](sessions/repeat-01/C-W03-Opaque.json) v1→v2 | established, narrowed, unresolved | matched | 两批后保留催化剂/投料/热史混杂并提出低种量预期；随后C1跨S1/S2/S3筛选并采用0.001g及分段冷却。筛选方向初始已有，具体材料和种量选择被进一步明确。 |
| [repeat-01/C-W04-Aligned](sessions/repeat-01/C-W04-Aligned.json) v1→v2 | established, narrowed, unresolved | matched | 先对材料及粒度取得局部认识，再在S1/C1下改反应热程并保留慢冷老化；匹配的是工艺细化，不能据此宣称种量、终温和精确重复全部完成。 |
| [repeat-01/C-W04-Opaque](sessions/repeat-01/C-W04-Opaque.json) v1→v2 | established, revised, narrowed, unresolved | matched | 先认识到慢冷/种量联合变化改善但未达标，随后C0/S0下进行更低种量与分段冷却。初始微量不足后的若干动作被拒，补至0.0001g后冷却执行；并非从头完全成功的单因素检验。 |
| [repeat-01/C-W04-Opaque](sessions/repeat-01/C-W04-Opaque.json) v2→v3 | established, narrowed, unresolved | matched | 第4至7批支持所测组合工艺合格，保留催化剂小差异未决，再固定C1跨S1/S2/S3筛选。材料筛选原已计划，已有结果进入具体催化剂及冷却流程选择。 |
| [repeat-01/C-W05-Aligned](sessions/repeat-01/C-W05-Aligned.json) v1→v2 | established, narrowed, unresolved | matched | 前两批一成一败后保留混杂，固定第2批所用结晶设置比较催化剂；第3至5批执行C3/C2/C0，不能把随后第6批额外低种量试验也视作原计划的固定协议。 |
| [repeat-01/C-W05-Aligned](sessions/repeat-01/C-W05-Aligned.json) v2→v3 | established, revised, narrowed | matched | 催化剂筛选未保留原可行性，低种量组合也未改善，研究者收窄S2保证粒度的判断；随后C3下比较S1/S3，第三个后续批另改C1。不将催化剂伴随组成变化拆成独立粒度机制。 |
| [repeat-01/C-W05-Aligned](sessions/repeat-01/C-W05-Aligned.json) v3→v4 | established, revised, narrowed | matched | 其他溶剂未改善细粉后转向高种量与回热的组合预期，第10批实际完成0.05g及280→310→270K热程。明确检验的是组合补救，不能单独识别种量或回热原因。 |
| [repeat-01/C-W05-Aligned](sessions/repeat-01/C-W05-Aligned.json) v4→v5 | established, revised, narrowed | matched | 高种量热循环失败后，第11批低投料接近阈值，于是事前提出0.02mol检验并在第12批执行。固定催化剂绝对量仍改变催化剂/试剂比，后续成功不单独确证浓度机理。 |
| [repeat-01/C-W05-MisIndexed](sessions/repeat-01/C-W05-MisIndexed.json) v1→v2 | established, revised, narrowed, unresolved | partly_matched | 降低投料并回热再冷却落实，溶剂仍为原来的0.08L，并未增加。研究者收窄慢冷/播种解释，同时保留催化剂与过饱和度混杂。 |
| [repeat-01/C-W05-Opaque](sessions/repeat-01/C-W05-Opaque.json) v1→v2 | established, revised, narrowed, unresolved | matched | 单批比较后形成溶剂相关判断并承认未重复；随后C0下筛S2/S3，再于S1比较C1至C3。筛选原已计划，具体分支依照当前结果细化。 |
| [repeat-02/C-W01-Aligned](sessions/repeat-02/C-W01-Aligned.json) v1→v2 | established, revised, narrowed, unresolved | matched | 0.03L细粉失败而0.04L合格后保留C0/S2并在0.04L改变热史。边界来自单次不同体积比较，不能把尖锐边界视为已定位的机理阈值。 |
| [repeat-02/C-W01-Opaque](sessions/repeat-02/C-W01-Opaque.json) v1→v2 | established, revised, unresolved | matched | 首批高细粉且等待升温后，提出稀释/播种/分段冷却组合并于第2批执行。工具创建被拒未阻止后续合法工艺，组合改善不能拆作种量独立效应。 |
| [repeat-02/C-W01-Opaque](sessions/repeat-02/C-W01-Opaque.json) v2→v3 | established, narrowed, unresolved | matched | 筛选后固定S2/C0结晶流程，第9批350K/7200s落实降低温度延时分支；温度和时间共同改变，并未检验另一可选的减催化剂分支。 |
| [repeat-02/C-W02-Aligned](sessions/repeat-02/C-W02-Aligned.json) v1→v2 | established, revised, narrowed, unresolved | matched | 三批高细粉后降低至0.02mol，催化剂同比减半；热史和后处理也变化。局部负面证据进入下一试验，但不是独立浓度因果估计。 |
| [repeat-02/C-W02-Aligned](sessions/repeat-02/C-W02-Aligned.json) v2→v3 | established, revised, narrowed | partly_matched | 低投料/老化未改善后提出累计高种量。第7批仅首个0.05g提交，其后19次被拒，故目标高种量未实现；不能用结果拒绝高种量物理假说。 |
| [repeat-02/C-W02-Aligned](sessions/repeat-02/C-W02-Aligned.json) v3→v4 | established, revised, narrowed, unresolved | matched | 明确撤回累计种量的证据资格，再选择C0/S2并延伸至250K。第12批溶剂由0.07增至0.08L，故回收变化不能只归因于冷却终温。 |
| [repeat-02/C-W03-Aligned](sessions/repeat-02/C-W03-Aligned.json) v1→v2 | established, revised, narrowed, unresolved | matched | 对已测热史收窄充分性判断，提出局部回热并实际执行；细粉与零回收权衡提供动机，不能把跨热史结果当作纯终温效应。 |
| [repeat-02/C-W03-Aligned](sessions/repeat-02/C-W03-Aligned.json) v2→v3 | established, revised, narrowed, unresolved | matched | 回热不改善后提出多次老化并执行。该版同时把19次被拒播种描述成1g试验，是执行记述偏差；修订标签记录公开立场变化，不认可该高种量推断。 |
| [repeat-02/C-W03-MisIndexed](sessions/repeat-02/C-W03-MisIndexed.json) v1→v2 | established, narrowed, unresolved | matched | 溶剂筛选支持当前S2组合且保留混杂，随后固定S2比较催化剂；初始材料筛选被具体化，不判为新生的因果机制。 |
| [repeat-02/C-W03-MisIndexed](sessions/repeat-02/C-W03-MisIndexed.json) v2→v3 | established, revised, narrowed, unresolved | matched | 选择C3同时保留近似排序未决，第8批降低温度、第9批缩短时间，分别对应温和/缩时两个分支。 |
| [repeat-02/C-W03-Opaque](sessions/repeat-02/C-W03-Opaque.json) v1→v2 | established, revised, narrowed, unresolved | matched | 催化剂筛选后固定C1测试S1/S2/S3；局部可行性与细粉限制共同进入后续材料选择，原有筛选框架保留。 |
| [repeat-02/C-W03-Opaque](sessions/repeat-02/C-W03-Opaque.json) v2→v3 | established, narrowed, unresolved | matched | 选择有质量裕度的350K而不声称回收差异显著，下一批实际检验250K冷端，后续才重复该组合。 |
| [repeat-02/C-W04-Aligned](sessions/repeat-02/C-W04-Aligned.json) v1→v2 | established, narrowed, unresolved | matched | 高纯度和局部可行粒度后在C1/S2执行330K延时反应；保留种量/催化剂/热史混杂。 |
| [repeat-02/C-W04-Aligned](sessions/repeat-02/C-W04-Aligned.json) v2→v3 | established, revised, narrowed, unresolved | matched | 低温方向被新结果否定，前瞻提出420K/900s并执行；该温度与时长联合方向不能拆成纯温度效应。 |
| [repeat-02/C-W04-Aligned](sessions/repeat-02/C-W04-Aligned.json) v3→v4 | established, revised, unresolved | matched | 低回收被解释成440K热史断崖，随后430K边界检验实际执行。但前两批冷却均被拒，265/270K不是已完成的冷端比较；局部可用策略与错误过程解释并存。 |
| [repeat-02/C-W04-MisIndexed](sessions/repeat-02/C-W04-MisIndexed.json) v1→v2 | established, narrowed, unresolved | matched | 边界读数后给出低种量/延时冷却组合，第4批落实；保留近阈值不确定性。 |
| [repeat-02/C-W04-MisIndexed](sessions/repeat-02/C-W04-MisIndexed.json) v2→v3 | established, revised, narrowed, unresolved | matched | 收回低种量延时的强预期，转向已选375K工艺下的C2/C3比较；对精确最优点仍保持未决。 |
| [repeat-02/C-W04-Opaque](sessions/repeat-02/C-W04-Opaque.json) v1→v2 | established, revised, narrowed, unresolved | matched | 保留C1跨溶剂筛选实际发生，热史同时变化。0.5g累计播种并未全部提交，不能从该负面叙述推出高种量物理效应；计划匹配与证据误记分别编码。 |
| [repeat-02/C-W05-Aligned](sessions/repeat-02/C-W05-Aligned.json) v1→v2 | established, revised, narrowed, unresolved | matched | 局部冷端差异后收窄慢冷保证粒度的范围，固定C0进行原计划内溶剂比较。 |
| [repeat-02/C-W05-Aligned](sessions/repeat-02/C-W05-Aligned.json) v2→v3 | established, narrowed, unresolved | matched | 0.06L近阈值失败后提出0.065L插值并实际执行。另有0.20g追加播种被拒却被写成已做负例；插值检验与证据误记在同一版共存。 |
| [repeat-02/C-W05-MisIndexed](sessions/repeat-02/C-W05-MisIndexed.json) v1→v2 | established, revised, narrowed, unresolved | matched | C0可行而C3高回收高细粉后在C3延长分段冷却；明确承认反应温度也变，不能单独归因冷却。 |
| [repeat-02/C-W05-Opaque](sessions/repeat-02/C-W05-Opaque.json) v1→v2 | established, revised, narrowed, unresolved | matched | 第3批310K操作被拒，第4批合法完成较暖端冷却，第8批回热循环落实；匹配后续可选分支，不把第3批算作成功完成。 |
| [repeat-02/C-W05-Opaque](sessions/repeat-02/C-W05-Opaque.json) v2→v3 | established, revised, narrowed, unresolved | matched | 回热未改善后收回该方向，转向细分温阶，第9批完成预定路径。 |
| [repeat-02/C-W05-Opaque](sessions/repeat-02/C-W05-Opaque.json) v3→v4 | established, revised, narrowed | matched | 低投料接近阈值后提出更低投料与细分温阶组合并在末批执行；保留单次与未达标边界，非纯浓度因果效应。 |
| [repeat-03/C-W01-Aligned](sessions/repeat-03/C-W01-Aligned.json) v1→v2 | established, revised, narrowed, unresolved | matched | 保留第二批结晶方案筛催化剂；初始材料筛选继续，明确保持温度与时间的因果未决。 |
| [repeat-03/C-W01-MisIndexed](sessions/repeat-03/C-W01-MisIndexed.json) v1→v2 | established, revised, narrowed, unresolved | matched | 高种量未改善后第3批0.005g加分段深冷实际执行；跨材料/热史的旧对比未被写成孤立种量效应。 |
| [repeat-03/C-W01-MisIndexed](sessions/repeat-03/C-W01-MisIndexed.json) v2→v3 | established, revised, narrowed | matched | 零/低/高种量均高细粉后选择局部回热并执行，结论限于已测深冷流程。 |
| [repeat-03/C-W01-MisIndexed](sessions/repeat-03/C-W01-MisIndexed.json) v3→v4 | established, narrowed, unresolved | partly_matched | 310K首次近阈值合格后比较一段与三段等待，但额外端点实际为312K而非更低温，故整体计划部分匹配。 |
| [repeat-03/C-W01-MisIndexed](sessions/repeat-03/C-W01-MisIndexed.json) v4→v5 | established, revised, narrowed, unresolved | matched | 多次近阈值反复后否定单调等待效应并执行310K双等待重复；近阈值不确定性进入判断，但不能保证最终推荐达标。 |
| [repeat-03/C-W01-Opaque](sessions/repeat-03/C-W01-Opaque.json) v1→v2 | established, narrowed, unresolved | matched | 对角材料筛选后选择S2并进一步比较催化剂与末段热史；此计划进入行动不等同于已分离溶剂因果。 |
| [repeat-03/C-W02-MisIndexed](sessions/repeat-03/C-W02-MisIndexed.json) v1→v2 | established, revised, narrowed, unresolved | matched | 材料结果修改C1先验并选择C0，后续跨溶剂/种量/热史探索落实；各比较存在耦合，不以行动匹配证明解释成立。 |
| [repeat-03/C-W02-Opaque](sessions/repeat-03/C-W02-Opaque.json) v1→v2 | established, revised, narrowed, unresolved | matched | C0局部领先但细粉失败后进行固定C0的溶剂筛选，初始筛选框架被明确化。 |
| [repeat-03/C-W03-Aligned](sessions/repeat-03/C-W03-Aligned.json) v1→v2 | established, revised, narrowed, unresolved | matched | 第3批低种量多级慢冷落实，但此前1g种量由被拒追加构成，不能据此宣布高种量不支持。 |
| [repeat-03/C-W03-Aligned](sessions/repeat-03/C-W03-Aligned.json) v2→v3 | established, revised, narrowed | partly_matched | 转向S3并执行长等待/回热，额外39次播种被拒，只有0.05g提交；更大种群未实际形成。原1g误记仍留在本版。 |
| [repeat-03/C-W03-MisIndexed](sessions/repeat-03/C-W03-MisIndexed.json) v1→v2 | established, narrowed, unresolved | matched | 后续0.05g及280K落实，同时缩短反应时长；本版称B2单次冷却可达标，但B2最终细粉0.6543，显示即使保留混杂仍可能错误引用可行性。 |
| [repeat-03/C-W03-MisIndexed](sessions/repeat-03/C-W03-MisIndexed.json) v2→v3 | established, revised, narrowed, unresolved | matched | 两种冷端均可行后向265K提出预测并检验；杂质/过饱和度解释仍是解释性主张，动作本身未直接识别其因果。 |
| [repeat-03/C-W04-Aligned](sessions/repeat-03/C-W04-Aligned.json) v1→v2 | established, revised, narrowed, unresolved | matched | 筛选后选S1的可行性并以S0高回收高细粉为新检验方向，第8批实际执行热循环。 |
| [repeat-03/C-W04-Opaque](sessions/repeat-03/C-W04-Opaque.json) v1→v2 | established, revised, narrowed, unresolved | partly_matched | 冷端/催化剂比较及重复落实，播种仍0.02g，没有种量稳健性检验；机制和重复性保留未决。 |
| [repeat-03/C-W05-Aligned](sessions/repeat-03/C-W05-Aligned.json) v1→v2 | established, revised, narrowed, unresolved | matched | 选C0并依次测试反应热程和溶剂；初始筛选明确化，同时承认小排序未经重复。 |
| [repeat-03/C-W05-Aligned](sessions/repeat-03/C-W05-Aligned.json) v2→v3 | established, narrowed, unresolved | matched | 第10批265K与等待落实；已有微小改善未被当作稳健增益，后续仍是组合热史检验。 |
| [repeat-03/C-W05-MisIndexed](sessions/repeat-03/C-W05-MisIndexed.json) v1→v2 | established, revised, narrowed, unresolved | matched | 材料/热程筛选后固定C3开展溶剂比较。后段实际转到S1，不能将笔记随后围绕S2细化的全部意向记为落实。 |
| [repeat-03/C-W05-Opaque](sessions/repeat-03/C-W05-Opaque.json) v1→v2 | established, revised, narrowed, unresolved | matched | S1边界与S2可行性后第7批热循环、第8批暖端实际落实；匹配选定工艺检验，不宣称全段复制计划已完成。 |

## 未完成窗口

无；105个窗口均有逐版本引文、证据与执行时序检查。

## 无完整观察窗口的会话

- repeat-01/C-W01-Aligned：不满足连续时序覆盖，不据此判断是否学习。
- repeat-01/C-W02-Aligned：不满足连续时序覆盖，不据此判断是否学习。
- repeat-01/C-W03-MisIndexed：不满足连续时序覆盖，不据此判断是否学习。
- repeat-01/C-W04-MisIndexed：不满足连续时序覆盖，不据此判断是否学习。
- repeat-02/C-W01-MisIndexed：不满足连续时序覆盖，不据此判断是否学习。
- repeat-02/C-W02-MisIndexed：不满足连续时序覆盖，不据此判断是否学习。
- repeat-02/C-W02-Opaque：不满足连续时序覆盖，不据此判断是否学习。
- repeat-03/C-W02-Aligned：不满足连续时序覆盖，不据此判断是否学习。
- repeat-03/C-W03-Opaque：不满足连续时序覆盖，不据此判断是否学习。
- repeat-03/C-W04-MisIndexed：不满足连续时序覆盖，不据此判断是否学习。

- Codes describe public statements and selected immediate plans, not private cognition.
- Matching execution is not evidence that the statement caused the action.
- A plan may have been fixed initially; sequence alone does not establish adaptation.
- Public claims can be wrong; validation checks provenance, not scientific truth.
- No-window sessions remain unassessed for this cycle, not classified as nonlearning.
- Independent coding/adjudication remains unfinished.
