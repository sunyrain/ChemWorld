# ChemWorld：自主科学中的反绎探索

当前整合稿题目为 **Abductive inquiry in autonomous science / 自主科学中的反绎探索**。以爱因斯坦 1905 年狭义相对论论文的解释张力与演绎展开起手，将反绎、可检验推论、经验评价与修订共同组成的探索过程作为主线。它不是“爱因斯坦测试”，也不把全部探索动作重新标为反绎。

本轮按两份审稿意见，以解释的形成、实际检验、修订及后续使用重组证据；摘要 160 英文词，不加入阶段性效应数字。NCS 原稿、原图和第一篇冻结产物保持原状。新增的是保留记录的事后解释历史分析与修正版结晶分布计算，没有新增模型或模拟器实验，也不改变历史证据地位。

## 阅读入口

- [英文阅读版](../../../output/pdf/chemworld-nature-en.pdf)
- [英文单栏行号版](../../../output/pdf/chemworld-nature-en-review.pdf)
- [中文对照版](../../../output/pdf/chemworld-nature-zh.pdf)
- [完整补充材料](../../../output/pdf/chemworld-nature-supplement.pdf)
- [重要历史版本：How autonomous research shapes scientific understanding / 自主研究如何塑造科学认识](../../../output/pdf/archive/nature-inquiry-20261016/README.md)（原版中英文PDF、行号版及补充材料）
- [可复核证据包](../../../output/paper/chemworld-review-evidence.zip)及[数据说明](evidence/README.md)
- [当前十图来源与状态](figures/integrated-20261016/README.md)、[新框架图提示词](figures/integrated-20261016/prompts.json)

正文：[英文](article.md)、[中文](article_zh.md)。方法：[英文](methods.md)、[中文](methods_zh.md)。扩展图：[英文](extended_data.md)、[中文](extended_data_zh.md)。`tex/` 来自 Markdown，不手工编辑。

## 行文框架

共同问题：**自主研究者如何从与世界的交互中形成、检验并发展解释，使其成为能够指导研究、也能够被研究修订的科学认识？**

| 结果小节 | 推进的问题 | 实验与图 |
| --- | --- | --- |
| 使反绎探索成为可检验的研究过程 | 怎样连接自主证据选择、公开判断与独立世界参照 | 300 场广度、当前 90 场过程、另行 30 场机会比较；图 1 |
| 从意外观测到解释性假说 | 一个候选解释怎样从差异观测中提出、形成条件性预期并进入检验 | 平衡研究 A 全部笔记与十二次测定，保留终点未决与未执行提议；图 2 |
| 实验何时能够约束解释 | 检验意图是否成为真实判别；观测改变了什么判断 | 同物种投料语义核查、低投料局部支持、插值撤回；图 3；七项选定判断不是全队列反绎频率 |
| 从局部证据走向外推的不同路径 | 观察到变化、猜想外推与未决解释的后续使用各有何依据 | 五模型 75 场、Astra/Sol 两路径、同期平衡外推；图 4；先验矩阵移至扩展图 2 |
| 自主探索如何改变科学判断 | 开展研究的后果及同一经历对不同响应判断的作用 | 30 场研究机会、42 场修正版结晶源参照和重算分布；图 5、扩展图 4 |

讨论以解释的提出、证据支持和后续使用的联系收束。解释形成可取得局部进展，也可留下机制和外推未决；不把发现与误解设为整场研究的互斥标签，不强制统一为自我确认或以纠错策略获胜作结。受控比较检验各自的科学问题，不被称为反绎的独立因果效应。

科学史依据为 Einstein (1905), DOI 10.1002/andp.19053221004；反绎采用 Douven 对 Peirce 的解释性假说形成/采纳论述（Stanford Encyclopedia of Philosophy，2025 修订）。两项来源已核对；开篇不宣称磁体—导体例子是相对论的唯一来源，也不将历史人物的方法直接作为智能体实验测量。

## 当前证据和历史材料

| 材料 | 当前用途与分母 |
| --- | --- |
| 历史广度研究 | Sol 240 场与其他模型平衡 60 场，共 300；五模型平衡 75 场中的 Sol 15 场已计入，不再累加 |
| 原平衡过程研究 | 45 场，39 完整链、41 有效 Q；34 窗口在 30 场中 |
| 修正版结晶过程研究 | 45 场，41 完整链、42 有效 Q、510/540 源批次；58 窗口在 35 场中 |
| 当前过程合计 | 90 场，80 完整链、83 有效 Q；92 窗口在 65 场中，另 25 场无完整可观察窗口 |
| 研究机会比较 | 另行 30 场，29 完整链与有效 Q，180/180 源批次；Research 14/15、NoResearch 15/15 有效预测 |
| 源观测参照 | 修正版结晶 42/45 有效会话、504 题；同溶剂参照 186/504 题回退 |
| 淬灭对照 | 历史十八份推荐 × 五世界，90 对/180 轨迹、75 完整对；物理操作作用，不是判断形成原因 |
| 旧结晶 45 场 | 回收描述与执行量不一致；保留为历史，不与修正版合并 |
| 早期笔记案例 | 6+18=24 场，单独保留，不混入上述当前过程分母 |

当前回收量统一为扣除晶种的固相目标产物摩尔量/跟踪的初始试剂投料摩尔量，截断至 [0,1]。内部结晶阶段量采用分离前目标产物为分母，两者不可互换。旧分数不修改；本次整合的是已经完整重跑的修正版，不是给旧分数重新贴标签。

核心比较在五个固定世界内先平均有效会话，再对世界等权。研究机会总体 MAE 为 0.035632 对 0.132086，极稀为 0.103677 对 0.061467；一份缺失预测及敏感性分析均保留。模型采样 seed 不可控，不称受控 seed 重复。研究机会是完整组合效应，不分离笔记、反馈或自主选择的独立作用。

机会比较全部采用 **Opaque**，十五对科学公共输入在仅去除 campaign ID 后一致。极稀点预测误差增量的 **85.2%** 来自解离分数；三项平均点误差的方向不代表每个会话、每道题或区间分数都恶化。证据包包含 1,044 条有效逐题逐响应记录、270 个计划会话/题组/响应单元（保留九个空单元），以及 90 个世界/题组/响应汇总。

当前 90 场共 268 版笔记、178 对相邻修订，全部包含新最终测定；92 对还满足后续有已提交研究动作的条件，另外 86 对无此后续动作。入选规则先于语义匹配，但条件化于继续研究；83 匹配、7 部分匹配、2 无明确计划只描述所选即时计划。证据包保留全部相邻对、全文及执行锚点，终点修订不被判为没有学习。

全部内部科学复查已按用户分工由本工作流程完成，性质为单分析者复查；不声称第二研究者独立一致性，也不再将外部人员待定列为本轮实验完成的阻塞项。

新增[解释历史](evidence/explanation_histories.json)沿五场既有案例追踪七项相关判断，涵盖终点修订，不把92个行动窗口改称反绎次数。主例执行版本中 `add_reagent` 与 `add_component(0)` 都加入同一单一进料，未实现智能体设想的酸身份对照；局部平台仍有测量支持，但不能据此声称机制判别成功。源版本与推导保留在证据包，核心判断同步进入双语正文、图2–3及方法。

新增[修正版分布](evidence/corrected_c_distribution_summary.json)与源/逐题/逐会话CSV：42份有效预测对应504次源测定和504题，纯度源均值0.986443、目标题目均值0.984628、预测均值0.947403，463/504低于参考；五世界等权有符号误差−0.037537。合并分布保留重复目标，不视作独立条件。没有沿用旧结晶的偏差数值。

## 证据定位

当前产物先经 [configs/current.json](../../../configs/current.json) 的 `work_ii.w2_257_inquiry_completion` 解析。

- [最新综合报告](../../../workstreams/flagship_tasks/reports/inquiry-completion-20261015/REPORT.md)
- [机会比较与逐次统计](../../../workstreams/flagship_tasks/reports/inquiry-completion-20261015/OPPORTUNITY.md)、[机器摘要及全部会话](../../../workstreams/flagship_tasks/reports/inquiry-completion-20261015/opportunity_comparison.json)
- [路径与源参照](../../../workstreams/flagship_tasks/reports/inquiry-completion-20261015/RETROSPECTIVE.md)、[路径数据](../../../workstreams/flagship_tasks/reports/inquiry-completion-20261015/research_paths.json)、[逐题参照](../../../workstreams/flagship_tasks/reports/inquiry-completion-20261015/source_references.json)
- [修正版结晶精读](../../../workstreams/flagship_tasks/reports/c-recovery-aligned-20261014/REVIEW.md)、[58 窗口完整编码](../../../workstreams/flagship_tasks/reports/c-recovery-aligned-20261014/semantic_analysis.json)
- [原过程编码](../../../workstreams/flagship_tasks/reports/inquiry-trajectories-20261014/semantic_analysis.json)：当前仅采用其中 34 个 EQ 窗口，71 个旧 C 窗口保留为历史
- [原过程逐场分析](../../../workstreams/flagship_tasks/reports/research-extension-20261014/analysis.json)：当前保留其 EQ 子集；[淬灭记录](../../../workstreams/flagship_tasks/reports/research-extension-20261014/QUENCH.md)
- [历史广度补充材料](../ncs/supplementary_en.md)：34 张表的原单元格完整保留

主例定位（只用于证据记录，不写入面向读者的正文）：

| 正文案例 | 记录位置 |
| --- | --- |
| 弱酸预期、组分测试、极稀外推 | opportunity `sessions/repeat-01/EQ-W01-Research.json`，v1 游标 0、v2 游标 30、第 8–12 批、Q08 |
| 同平台不同外推 | opportunity `sessions/repeat-01/EQ-W02-Research.json` 与 `repeat-02/EQ-W02-Research.json` |
| 低投料检验 | corrected C，repeat-01/C-W05-Aligned，v5 后第 12 批 |
| 0.065 L 插值及撤回 | corrected C，repeat-02/C-W05-Aligned，v3 及后续 |
| 正确识别未执行高播种 | corrected C，repeat-02/C-W02-Aligned，v4 |
| 将拒绝请求记为高播种实验 | corrected C，repeat-03/C-W03-Aligned |
| 440 K 热史解释及冷却拒绝 | corrected C，repeat-02/C-W04-Aligned |
| 310 K 近阈值重复 | corrected C，repeat-03/C-W01-MisIndexed |

`process_cases.json` 保留此前案例来源，不定义当前主例。当前插图来源以 [整合图源表](figures/integrated-20261016/README.md) 为准；此前 preview 目录仅保留其生成记录。

## 构建与验证

```powershell
uv run --no-sync python paper/tools/build_nature_manuscripts.py
```

本轮先用 `build_nature_review_evidence.py` 重建原有可复核记录并调用新的 `build_abductive_evidence.py`，核对解释引文、执行语义和修正版分布；用 `plot_abductive_evidence.py` 生成六张数据图，再由 `build_nature_evidence.py` 同步补充材料。日常仅改文字时不需要重复数据分析。

五主图、五扩展图中，主图4和扩展图1–2逐字节复用NCS原生定量PDF；图1保留ImageGen概念图；其余六张均为保留数据直接绘制的矢量图。旧ImageGen数据预览仍保留生成记录，但不再出现在当前稿件。三份供体及34张历史数值表均未修改。

英文正文 **4,132词**（不含摘要、标题、图注及方法），摘要 **160词**。英文阅读版 **19页**、行号版 **34页**、中文对照版 **17页**、补充材料 **30页**；英文与中文正文及五主图分别占 **9页、8页**，其后为参考文献、方法和扩展图。

四份共 **100页** 已渲染检查；更新后的主图另行放大核对，研究机会图位于讨论之前。23条双语引用顺序、每语言十图源、五主图顺序、三份供体文件、34张历史表通过定向验证。新计算与原有源参照逐会话/逐响应及等权世界MAE一致；182条既有窗口引文和新增主例锚点核对通过，全部缺失仍保留。五项Python脚本Ruff、证据ZIP完整性及diff检查通过。当前状态为可审阅稿，案例是单分析者事后解释，不宣称全队列反绎能力或独立复核。
