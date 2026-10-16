# ChemWorld：自主科学中的反绎探索

当前整合稿题目为 **Abductive inquiry in autonomous science / 自主科学中的反绎探索**。以爱因斯坦 1905 年狭义相对论论文的解释张力与演绎展开起手，将反绎、可检验推论、经验评价与修订共同组成的探索过程作为主线。它不是“爱因斯坦测试”，也不把全部探索动作重新标为反绎。

本轮整合 NCS 的跨体系与五模型证据、新版同期过程记录及研究机会比较；摘要 162 英文词，不加入阶段性效应数字。NCS 原稿、原图和第一篇冻结产物保持原状，当前稿在本目录持续更新。无新增科学实验、重编码或证据地位提升。

## 阅读入口

- [英文阅读版](../../../output/pdf/chemworld-nature-en.pdf)
- [英文单栏行号版](../../../output/pdf/chemworld-nature-en-review.pdf)
- [中文对照版](../../../output/pdf/chemworld-nature-zh.pdf)
- [完整补充材料](../../../output/pdf/chemworld-nature-supplement.pdf)
- [可复核证据包](../../../output/paper/chemworld-review-evidence.zip)及[数据说明](evidence/README.md)
- [当前十图来源与状态](figures/integrated-20261016/README.md)、[新框架图提示词](figures/integrated-20261016/prompts.json)

正文：[英文](article.md)、[中文](article_zh.md)。方法：[英文](methods.md)、[中文](methods_zh.md)。扩展图：[英文](extended_data.md)、[中文](extended_data_zh.md)。`tex/` 来自 Markdown，不手工编辑。

## 行文框架

共同问题：**自主研究者如何从与世界的交互中形成、检验并发展解释，使其成为能够指导研究、也能够被研究修订的科学认识？**

| 结果小节 | 推进的问题 | 实验与图 |
| --- | --- | --- |
| 以可编程世界研究科学推断 | 怎样连接研究者自主获得的证据、公开判断、后续使用和独立世界参照 | 300 场广度、当前 90 场过程、另行 30 场机会比较；图 1 |
| 研究目标与先验知识组织科学探索 | 什么进入研究选择，操作成果能够说明多少认识进展 | EC/RX 各 30 配对、完整 EC 轨迹、反应先验收益、结晶材料选择、独立预算比较；图 2 |
| 解释在猜想、检验与修订中发展 | 观测怎样引出候选解释、相关检验、局部支持与撤回 | 平衡研究 A、低投料检验、插值失败、播种证据资格；图 3–4；92 窗口是记录分母而非反绎成功数 |
| 从局部证据走向外推的不同路径 | 观测变化、合理猜想与局部关系的外推各建立什么 | 五模型 75 场、Astra/Sol 两路径、同期平衡外推、历史及重复先验结果；图 5–6 |
| 研究改变科学认识的适用范围 | 开展研究对判断有何贡献，已获关系能否进入新预测 | 30 场研究机会、42 场修正版结晶源参照；图 7、扩展图 2 |

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

本轮仅重新编译稿件，沿用已验证的数值表和证据包；补充材料的组织说明与其生成脚本同步更新，不重算数据。后续确需重建证据包和表时，分别使用 `build_nature_review_evidence.py` 和 `build_nature_evidence.py`，无需在每次文字修改后执行。

七张主图、三张扩展图中，主图 2、5、6 直接复用 NCS 原生定量 PDF；图 1 是新生成的反绎框架概念图；其余六张为明确标注的 ImageGen 数据预览。精确数值仍以正文、补充表及证据包为准。三张定量供体文件逐字节复用，供体本身未修改。当前 PDF 页眉和首页说明区分两类图，不再称所有插图均为概念预览。

最终英文正文为 **4,160 词**（不含摘要、标题、图注及方法），摘要 **162 词**。四份 PDF 分别为英文阅读版 **18 页**、英文行号版 **33 页**、中文对照版 **17 页**、补充材料 **29 页**；中英文阅读版的正文及七主图均占 **10 页**，其后为参考文献、方法和扩展图。

全部 **97 页**已渲染并检查联系表，放大核对首页、定量图、过程图与图注；研究机会图位于讨论之前。编译日志无溢出、缺字或未解析引用。23 条中英文参考文献顺序一致，每语言十张有效图源、七个依序主图号、三份与供体逐字节一致的定量图，以及 34 张未改历史表均通过定向核对；两项构建脚本 Ruff 通过。原始平衡主例笔记另行核对了候选酸投料解释及其事前判别预期。构建和渲染记录保留在仓库外 `ChemWorld-local-research/manuscript-nature-20261016/qa-final-abduction/`。

本轮未重算或更换 182 条既有引文、1,044 条预测记录及任何实验失败。反绎框架不提升既有证据地位，方法保留单分析者解释范围；正式定稿仍需将六张数据预览换为精确数据图，并完成作者声明与持久公开归档。
