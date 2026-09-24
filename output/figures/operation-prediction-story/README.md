# Figure 3：讨论收束与论文整合方案

2026-09-24。本文汇总本轮 Figure 3 的科学解释、数据口径和写作决定，作为此次论文整合的工作说明。
沿用已完成的数据矩阵，不新增实验。英文正文、图注和跨段落修改稿已在下方备好；
论文源文件、正式图件、PPT 和 PDF 尚未按此方案替换。准备工作与出版物更新分别记录。

## 1. 收束为两个相连的问题

**第一层保留双目标设计：不同研究委托是否产生预期的操作—预测分工？**
Optimization 优先寻找高分操作方案；Discovery 优先建立并检验解释性、预测性描述。
实验允许两种目标下的 agent 自主选择操作、测量、对照和重复，不强制规定探索或利用算法。
Discovery 也可能找到 Optimization 没有访问到的更优区域，这属于设计允许的结果。

**第二层检验实际产出：操作表现更好的会话，其预测是否也更好？**
先看实测推荐复测分，再看相同测试条件的预测 MAE，不以任务标签预设胜者。
最后用原 agent 的公开解释和封存预测，定位一个具体的判断适用范围问题。

两层复用同一批配对，不能写成两份独立实验支持。案例也取自该批会话，不增加样本数。

建议中文表述：

> 两种研究目标没有形成稳定的“优化者更会操作、发现者更会预测”的分工。
> 在这些匹配研究中，较好的操作结果也并不总是伴随较好的预测；
> 有效方案不能单独验证实验判断对新条件的适用性。

建议 Results 小节标题：

> Research objectives yield different patterns of operational and predictive performance

Discovery / Optimization 是委托目标，不是能力等级，也不是被严格规定的探索算法与优化算法。
两种会话都可以探索和改进操作；发现导向的研究也可能找到另一会话没有访问到的更优区域。
因此，不能将 Optimization 标签等同于“操作更好”，也不能把 Discovery 当作较弱的操作基线。

“更好的预测”在配对分析中仅指较低的测试 MAE。它不等于达到某个科学可接受的准确性标准。
“更好的操作”仅指推荐方案获得更高的独立复测分，不等于找到全局最优或具有普遍更强的优化能力。

“理解”仅讨论一个可检验方面：原 agent 能否利用自己的实验，对条件改变后的结果作出可靠预测，
并合理限定判断的适用范围。正文优先使用 prediction / generalization / applicability，
不用“没有理解化学”或把写得完整的机制报告等同于已验证的知识。

## 2. 问题、测量与证据强度

| 问题 | 使用的数据和比较 | 可以写出的结论 | 不能由此推出 |
|---|---|---|---|
| 实际操作表现更好的会话是否也预测得更好？ | 原有匹配对内，以独立复测分排序，再比较同一 score 的 12 题 MAE | EC 16/30 排序一致、14/30 不一致；RX 为 21/30 和 9/30 | 二者零相关、统计独立、存在普遍权衡，或高操作分导致预测失败 |
| 改变研究委托产生什么结果？ | 原有 discovery / optimization 配对，保留全部四类结果及原始差值 | EC 中优化委托更常得到高复测分；RX 不呈现相同结果 | “优化”必然胜过“探索”，或隔离了选实验与解释实验的因果作用 |
| 一次研究是否形成了操作改进？ | 全部批次的原始得分、操作变化、封存推荐及独立复测 | 选定案例形成了最终复测为 0.756 的操作方案，保留中途下降和零分 | 每一步都改善、best-so-far 上升证明学习、已达到最优 |
| 同一原 agent 的哪些预测失准？ | 全部 12 个封存预测、区间和参考值，并定位公开预测理由 | 选定案例在若干新材料/操作条件下大幅低估，参考结果超出给定区间 | 所有预测都差、总体校准已被 12 题精确估计、模型没有任何知识 |
| 操作改善过程中预测是否持续停滞？ | 需要同一研究过程的阶段性预测记录；本组没有该读出 | 当前不能回答 | 把终态预测画成随实验步数的曲线，或将独立的 12/24 会话当作连续过程 |

前三十对、后三十对分别来自两个系统的五个世界。信息臂、预算、locus 和预测题复用世界；
它们不是新的独立世界重复。重新按实际成绩定向是事后描述性整理，并没有新增对照实验。

## 3. 数据矩阵及准确分母

[完整、机器生成的数据矩阵](DATA_MATRIX.md)包含原实验覆盖、两张联合结果表、逐世界/预算/信息臂/locus
分层、原委托均值，以及选定会话的全部批次和全部预测题。

| 范围 | 原始会话 | 原有匹配对 | 高复测分会话也有更低 MAE | 高复测分会话有更高 MAE |
|---|---:|---:|---:|---:|
| 电化学 EC：5 世界 × 3 信息臂 × 2 预算 × 2 目标，E locus | 60 | 30 | 16 | 14 |
| 反应系统 RX：5 世界 × 3 信息臂 × 2 loci × 2 目标，12 批次 | 60 | 30 | 21 | 9 |
| EC 两会话均无记录恢复的敏感性子集 | 34 | 17 | 10 | 7 |

双目标设计本身的完整结果须在主图保留：

| 操作复测分较高者 | 预测 MAE 较低者 | EC | RX | 描述性解释 |
|---|---|---:|---:|---|
| Optimization | Discovery | 13/30 | 5/30 | 与预期的目标分工一致 |
| Optimization | Optimization | 13/30 | 4/30 | Optimization 两方面同时占优 |
| Discovery | Discovery | 3/30 | 17/30 | Discovery 两方面同时占优 |
| Discovery | Optimization | 1/30 | 4/30 | 与预期分工相反 |

“与预期分工一致”是本轮解释，不追认成原实验预注册的主要终点，也不是已经证实的因果机制。
EC 的 26 次 Optimization 操作获胜分成 13 次预测也更好、13 次预测更差；
RX 的 17 次 Discovery 联合占优必须正面报告。RX 不只充当“优化失败”的脚注。

每一匹配对固定 world、arm、budget、locus，仅研究委托不同。以 h、l 表示实际复测分较高/较低的会话：

- `retest_gap_higher_minus_lower = R_h − R_l`，由于定向规则总为正，不能再称作“优化带来的收益”。
- `mae_gap_higher_minus_lower = E_h − E_l`；小于零为排序一致，大于零为排序不一致。
- 分类依据严格正负号，没有显著性或最小效应阈值；全部原始量值和未舍入差值保存在 CSV 中。
  接近零的差值不能因被计数就获得科学显著性的含义。

各项数量不能混写：

| EC 数量 | 含义 |
|---|---|
| 26/30 | Optimization 委托的复测分高于 Discovery |
| 14/30（原分析） | Optimization 委托的预测 MAE 低于 Discovery |
| 13/30 | Optimization 复测分更高，但预测 MAE 也更高 |
| 13/26 | 仅在 Optimization 复测获胜的 26 对中，有 13 对预测更差 |
| 14/30（本次整理） | 无论哪个目标获胜，实际复测分较高者预测更差；等于原来的 13 + 1 |
| 16/30 | 实际复测分较高者预测也更好；等于原来的 13 + 3 |

两项 14/30 数值相同但问题不同。新的 EC 不一致逐世界计数为 **3、2、3、1、5 / 各 6 对**；
旧的 Optimization 获胜且预测更差计数为 **3、2、3、1、4 / 各 6 对**。
W05 的额外一对是 Discovery 操作更好但预测更差，必须保留。

恢复口径也已查清：旧 CSV 的 `no_source_restart` 实际来自两个会话均没有 `recovered` 标记。
EC 的该标记包括后测恢复，并非只标记来源实验重启。因此新表使用 `both_without_recorded_recovery`，
称为“无记录恢复子集”；不改旧冻结记录，不把剩下 17 对当作新的独立样本。

## 4. 原始会话说明的是判断的适用范围

选定案例使用第一电化学世界、12 批次、Opaque 的原始目标配对；进一步解释其中 Optimization 会话的预测。
两条研究路径均由原 agent 自主完成，后测保留各自完整上下文，不存在换模型读报告。
这是回顾性选取的说明性案例，不能当作总体发生率、随机抽样或最具代表性样本。

| 会话 | 日志可见的实验分配 | 推荐复测分 | Score MAE |
|---|---|---:|---:|
| Discovery | 第 1–4 批比较溶剂，第 5–7 批在 S0 下比较电位，第 8–10 批比较电解质，第 11–12 批延长反应并改变电流上限 | 0.717587 | 0.088394 |
| Optimization | 前期比较材料组合，第 5–6 批检查交叉组合，第 7–8 批在 S2/E2 下比较电位，第 9–12 批继续调整 S2/E2 的电流、时长和电位 | 0.756122 | 0.229397 |

这是一对实际发生的路径差异，不是所有会话都采用了某种策略的证据，也不能隔离研究委托的内部作用机制。
两条路径均包含探索和操作改进。Discovery 第 11、12 批含分段电解及中途测量，图示若汇总为总时长，
不能将其伪画成一次连续操作。已核对两条公开轨迹的 86 和 84 条操作及 24 批结果。

证据顺序为：

1. 保留全部 12 批结果及操作。第 3 批 S2/E2 得分 0.675，后续局部改进得到第 12 批 0.749；
   第 8 批零分、第 11 批回落同样保留。封存推荐为第 12 批，独立复测为 0.756。
2. 使用该 agent 原始 Q 理由：它因交叉组合实验的低活性，将若干材料组合判为低活性。
   这是后续公开解释，不标为实验当时的内心思考或经过验证的内部认知原因。
3. 展示全部 12 题及原始 80% 区间。完整 score MAE 为 0.229397，覆盖为 5/12。
   +0.8 V、100 mA、7,200 s 下的四个材料组合可作放大比较：S0/E0 预测 0.570、参考 0.572；
   S0/E1、S0/E3、S2/E0 分别预测 0.100、0.090、0.070，参考为 0.628、0.543、0.494，
   后三项均超出给定区间。正确预测必须与错误预测同时展示。

可写：“该会话取得了有复测支持的操作结果，但对部分新条件的低活性判断没有得到参考结果支持。”
不能写：“只改变电位就推翻其全部机理”，因为来源与测试同时涉及电位、电流、投料量和体积变化；
也不能写它已有充分判别证据，或已证明其内部推理失败。

以另一会话 MAE 较低作辅助比较即可。绝对失准应由具体误差、预测区间和科学含义说明，
不能定义成“只要不如 Discovery 就是不准确”。

## 5. 可直接用于整合的英文稿

以下 Results 和 caption 对应第 6 节的四面板方案；它们是替换稿，不是当前 PDF 已采用的正文。
读者可见的文本不写内部运行编号、文件名或 hash。

### Results 替换段落

**Research objectives yield different patterns of operational and predictive performance**

We asked whether different research objectives produced the expected specialization in operating performance and prediction. Discovery commissions prioritized developing and testing an explanatory, predictive account; optimization commissions prioritized finding a high-scoring procedure. Both allowed autonomous experimentation. Independent campaigns were matched within world, information condition, budget and prior locus, with recommendation retests and predictions evaluated separately.

The observed outcomes did not follow a uniform division of labour (Fig. 3a,b). Optimization commissions produced higher recommendation retest scores in 26 of 30 electrochemical pairs: thirteen also had lower score-prediction MAE, whereas thirteen had higher MAE. In reaction processing, discovery commissions performed better on both endpoints in seventeen of thirty pairs. Without presuming either commission superior, the higher-retest campaign had worse predictions in fourteen electrochemical and nine reaction-processing pairs. These are descriptive orderings within five reused worlds per system, not evidence of statistical independence or a causal trade-off between the endpoints.

A selected 12-batch electrochemical pair connects these outcomes to the original research process (Fig. 3c). The discovery campaign compared materials and operating conditions before extending duration and increasing the current cap. The optimization campaign refined a promising solvent–electrolyte combination, raising its observed score from 0.675 in batch 3 to 0.749 in batch 12. Independent recommendation retests were 0.718 and 0.756 for discovery and optimization, respectively, whereas score-prediction MAEs were 0.088 and 0.229.

The optimization agent's public prediction rationale assigned low activity to several combinations because cross-pair experiments had performed poorly. For one previously tested combination under new conditions, it predicted 0.070 with an 80% interval of 0–0.240, against a reference score of 0.494 (Fig. 3d). Another material combination was accurately predicted, at 0.570 versus 0.572. All twelve forecasts are retained. The failed transfer involved several changes in conditions and does not isolate a single causal factor or establish that the acquired evidence was sufficient. It shows why a useful operating result does not, by itself, validate the applicability of an experimental judgment. We next examine which outcomes improve under larger research envelopes.

### Figure 3 caption 替换稿

**Research objectives, operating outcomes and predictive judgments.** a,b, Joint outcomes of matched discovery and optimization campaigns in electrochemistry (a) and reaction processing (b). Each point is one pair. The horizontal axis is recommendation retest score under optimization minus discovery; the vertical axis is discovery score-prediction MAE minus optimization MAE. Positive values favour optimization on the respective endpoint. All four outcome categories and their counts are retained; neither goal is presumed superior. Each system contains thirty pairs from five worlds. c, All twelve observed batch scores from a selected matched pair of independent electrochemical campaigns, with sealed recommendations independently retested. Both campaigns have twelve-batch budgets; the curves are not a 12-to-24 continuation. Selected annotations describe recorded operations, not contemporaneous thoughts. d, All twelve original score forecasts from the optimization campaign, their nominal 80% prediction intervals and the withheld reference observations. The public Q rationale is author-condensed and labelled as subsequent to research; it is not a recorded internal reasoning trace. This pair is retrospectively selected for illustration. Matching fixes world, information arm, budget and prior locus. Direction counts use strict signs without a minimum-effect or significance threshold; pairs and questions share worlds. Electrochemical prediction references are single seeded observations, whereas reaction-processing point errors use five-observation means.

### 需要同步的一句话修改

| 稿件位置 | 建议替换文本 / 要点 |
|---|---|
| Abstract 中当前仅列 EC 26/30、14/30 的句子 | **Research objectives produced system-dependent outcomes, and higher recommendation scores did not consistently coincide with lower prediction errors.** |
| Introduction 最后一段的首句 | **Across six chemical system families, we examine how research objectives, resources and supplied information relate to operating outcomes and the applicability of experimental judgments.** 后续保留资源与先验的正面结果及 EQ/C 主线。 |
| Discussion 对 Figure 3 的概括 | **The goal comparison does not establish an intrinsic advantage of discovery or optimization. It shows that assigned objectives, delivered procedures and predictive generalization are distinct aspects of an autonomous research process.** |
| 转入 Figure 4 | 使用上方 Results 末句；不预设此前失败必定是数据不足，也不声称资源增加不能改善预测。 |

### Methods 补充说明

The comparison oriented by observed retest performance is a post hoc re-expression of the original goal pairs, not an additional experiment. Within each pair, we identify the campaign with the higher recommendation retest score and compare its score-prediction MAE with that of its counterpart. All pairs and exact effect magnitudes are retained; no minimum-effect threshold is applied. The electrochemical illustration is retrospectively selected and does not estimate the prevalence of its expressed prediction rule. The sensitivity subset excludes any recorded campaign recovery, including assessment-only recovery, rather than source restarts alone.

## 6. 主图、附录与全文分工

本次收束采用一个明确的四面板安排，保留已有成对差值信息；不重新设计整篇论文的所有图。

| 面板 | 主文保留的内容 | 阅读目的 |
|---|---|---|
| a | EC 全部 30 对的有符号操作/预测差值，四种结果及计数 | 双目标没有形成固定分工，且需看差值大小 |
| b | RX 全部 30 对的同类比较；单独坐标尺度 | Discovery 的 17 次联合占优与系统差异是主要结果 |
| c | 同一 12 批次配对的两条真实得分轨迹、少量操作注释及各自独立复测 | 解释两种委托下实际发生的研究路径；Discovery 也可改进操作 |
| d | 被解释的 Optimization 会话全部 12 题预测、区间和参考值；一条简短公开 Q 理由 | 从有用方案连接到具体的适用范围错误，保留正确预测 |

a/b 的坐标仍按指定目标作差，以完整保留设计；横轴明确写成目标间的复测差值，不称“优化能力提升”。
右下象限是 Optimization 操作更好、Discovery 预测更好；左上象限则是相反分工。
右上与左下分别是 Optimization 和 Discovery 同时占优。实际表现排序的 16/14、21/9 是这些象限的汇总，
用正文一句话报告，不另画一组重复柱形图。差值接近零的点保留，不借颜色暗示显著性。

c 只画紧凑的实际得分/操作注释，不再复制 Figure 2 的仪器和完整流程示意。
保留全部低分与回落；若画 best-so-far，必须与原始点并列，且不以其必然单调作为学习证据。
d 的放大关注点为 Q04/Q06/Q08/Q10 四个材料条件，但十二题全部展示，正确的 Q04 不隐藏。
Q 理由压缩为一句并注明阶段，不额外制作大块“思考过程”文字或虚构即时心理活动。

附录承接原世界均值柱图、全部四类结果的数值表、world/arm/budget/locus 分层、无记录恢复敏感性、
案例完整操作顺序和原始公开文本。RX 六响应 macro MAE 的 6/30 属于另一指标，单独保留，
不与本图 score MAE 的 8/30 混用。现有净化补充结果也继续保留。

全文顺序不扩张：

| 内容 | 主要问题 | 与 Figure 3 的边界 |
|---|---|---|
| Figure 1 | 怎样控制世界、信息和评价？ | 提供仪器与研究协议 |
| Figure 2 | 原 agent 实际怎样完成连续研究？ | 保留原结晶流程案例，不再承担目标比较 |
| Figure 3 | 研究委托对应什么实际产出，操作结果能否验证后续判断？ | 双目标群体结果 + EC 原始配对及预测 |
| Figure 4 | 增加资源改善哪些结果？ | 独立 12/24 会话比较；承认 EC 和 PA 的预测收益 |
| Figure 5 / EQ | 哪些关系被推广到失效的条件？ | 更系统的适用范围证据 |
| Figure 6 / C | 哪些仍然稳定的关系被无依据地改变？ | 补足相反方向的错误及成功响应 |

Figure 3 负责建立分别测量操作与预测的必要性；EQ/C 负责深化“判断应在何处保留、何处改变”。
本文不把两目标设计写成普遍探索—利用权衡，也不把错误预测归结为一个共同内部原因。

## 7. 收束时保留的边界与有限实施步骤

不采用“模型越优化越不懂”“探索天然更懂规律”“预测没有显著变化所以等效”“14/30 证明零相关”
或“一个案例解释所有会话”。也不声称高分即接近最优、终态预测代表全过程预测、
K2 回顾等于先前已掌握的知识。当前为一个 agent 配置、有限世界和相关读出的描述性结果。

已经完成：数据矩阵、分母口径、两目标解释、案例证据核对、上方英文替换稿与图注方案。
剩余实施限定为三个步骤：

1. 按第 6 节重排 Figure 3，保留全部点和原始数值；完成一次图件视觉检查。
2. 一次性替换 Results/图注，并同步摘要、引言、Methods、Discussion 与补充材料引用。
3. 重建并检查完整英文 PDF，确认图号、正文引用、排版和主附录分工后结束本轮整合。

这些步骤不要求新增实验、阶段性预测补测、追加模型、额外 baseline 或全矩阵机制评分。
没有必要为了写出更强的结论不断扩张证据。当前六面板图件与旧四面板正文图注的错配，
在同一次替换中解决；不能将本工作说明的完成称为稿件或 PDF 已更新。

## 8. 文件与复现

- [可读数据矩阵](DATA_MATRIX.md)：原始覆盖、全部分层、12 批操作和 12 题预测。
- [60 对实际表现矩阵](performance-pairs.csv)：原始目标、两方端点、实际高分会话、未舍入差值、恢复标记。
- [12 批实验](case-batches.csv)及[12 题预测](case-queries.csv)：全部保留，包括低分、正确预测和区间未覆盖。
- [原始目标配对表](all-60-pairs.csv)、[原始均值与计数](summary.json)：沿用旧定义，未覆写。
- [整理脚本](../../../paper/tools/analyze_operation_prediction_relationship.py)。
- 案例 [Discovery 公开报告](../../../workstreams/flagship_tasks/reports/work-ii-ec-pa-five-world-en-20260919/EC-W01-B12-discovery-E-Opaque/REPORT.md)与[完整操作](../../../workstreams/flagship_tasks/reports/work-ii-ec-pa-five-world-en-20260919/EC-W01-B12-discovery-E-Opaque/public-trajectory.json)。
- 案例 [Optimization 公开报告](../../../workstreams/flagship_tasks/reports/work-ii-ec-pa-five-world-en-20260919/EC-W01-B12-optimization-E-Opaque/REPORT.md)与[完整操作](../../../workstreams/flagship_tasks/reports/work-ii-ec-pa-five-world-en-20260919/EC-W01-B12-optimization-E-Opaque/public-trajectory.json)。

从仓库根目录运行：

```powershell
uv run --no-sync python paper/tools/analyze_operation_prediction_relationship.py
```

配对数值来自已保留的 `paper/figures/integrated-results/campaign_metrics.csv`，并逐项对照原配对 CSV。
案例原始运行和公开报告从 `configs/current.json` 的 `work_ii.w2_132_ec_pa_english_matrix` 解析；
完整重建需要该绑定的本地运行目录。导出仅含操作设置、分数和预测结果，不含原始 provider 数据或私有种子。
已导出的 CSV 和本文可独立阅读。

已有图件由 `paper/tools/render_operation_prediction_story.py` 构建，仍是原来的委托对比；
本次脚本不会调用它，也不改动既有论文配图。
