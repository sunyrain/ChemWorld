# ChemWorld：自主研究如何塑造科学认识

本目录是用户已授权的独立研究稿。2026-10-15 在总纲四节框架下落实审稿意见，使研究机会的总体收益、区域反转与局部认识的后续使用成为中心发现；连续案例、逐响应/逐会话结果及过程窗口筛选依据同步展开。第一篇冻结稿和 NCS 源稿及 PDF 不在本次修改范围。

## 阅读入口

- [英文阅读版](../../../output/pdf/chemworld-nature-en.pdf)
- [英文单栏行号版](../../../output/pdf/chemworld-nature-en-review.pdf)
- [中文对照版](../../../output/pdf/chemworld-nature-zh.pdf)
- [完整补充材料](../../../output/pdf/chemworld-nature-supplement.pdf)
- [可复核证据包 ZIP](../../../output/paper/chemworld-review-evidence.zip)及[数据说明与源表](evidence/README.md)
- [本轮 ImageGen 框架图与六张数据预览](figures/preview-20261015/README.md)与[完整提示词及修改记录](figures/preview-20261015/prompts.json)

正文：[英文](article.md)、[中文](article_zh.md)。方法：[英文](methods.md)、[中文](methods_zh.md)。扩展图说明：[英文](extended_data.md)、[中文](extended_data_zh.md)。补充材料由脚本从保留结果生成；`tex/` 由 Markdown 构建，不手工编辑。

## 行文框架

题目：**How autonomous research shapes scientific understanding / 自主研究如何塑造科学认识**。

中心问题是实验自主性怎样转化为科学认识的拓展。正文按研究过程推进，不把全部结果解释为自我确认，也不将纠错策略成功设为收束条件。

| 结果小节 | 段落承担的工作 | 主要证据 |
| --- | --- | --- |
| 使自主科学探索成为可检验的研究对象 | 解释自主选择、公开观测、同期判断、后续使用和独立世界参照怎样连接 | 化学接口；300 场广度研究；当前 90 场过程记录；另行 30 场机会比较 |
| 科学探索的自主组织与适应 | 从目标与信息进入起始选择，接着追踪反馈怎样改变下一实验 | 150 场路径提取；50 个世界内对照；结晶初始选材；平衡弱酸预期转向组分检验 |
| 科学认识在实验中的形成与演变 | 局部关系、前瞻检验、失败后修订、执行证据资格及关系推广 | 92 个结构窗口；修正版结晶低投料、插值、播种案例 B/C；平衡研究 A 连续记录，其他案例进入补充 |
| 自主探索中科学进展的性质与条件 | 研究大幅改善总体预测，却损害特定区域；检查获得的关系如何发挥作用 | 研究机会总体收益与极稀损失、响应贡献及会话差异；42 场源观测参照；历史电化学与平衡先验比较 |

第二、第三节描写持续交互的两个方向，而不是研究只经过一次的流水线。“平衡研究 A”（W01 Research 第一重复）从第二节的预期与实验，延续到第三节的外推，再连接第四节的同期比较。图 2 集中展示这条连续轨迹，结晶图 3 突出有依据的局部改进、失败后的合理撤回，以及对未执行高播种的两种理解。

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

`process_cases.json` 是上一版选定案例的历史记录，并不定义本轮主例。`figures/preview/` 是上一版图稿预览，`figures/` 上层的数据参考图也不属于当前插图；当前稿只嵌入 `figures/preview-20261015/` 的七张 PNG。

## 构建与验证

```powershell
uv run --no-sync python paper/tools/build_nature_review_evidence.py
uv run --no-sync python paper/tools/build_nature_evidence.py
uv run --no-sync python paper/tools/build_nature_manuscripts.py
```

第一条生成可复核证据包并检查均值、公共输入一致性、窗口筛选和 182 条引文；第二条生成补充表，保留全部失败、过程窗口和 34 张历史表；均不产生新模型/模拟器实验，也不重新生成图片。第三条使用 Pandoc、XeLaTeX、共享文献库及既有独立模板，输出英文阅读版、英文行号版、中文对照和完整补充材料。构建与视觉检查位于仓库外 `ChemWorld-local-research/manuscript-nature-20261015/`。

当前七图均由内置 ImageGen 生成并逐张检查：主图 1 为总框架图，主图 2–4 与扩展图 1–3 为数据预览。本轮重做主图 2–4 和扩展图 1，突出连续轨迹、正向检验、区域反转、响应贡献、逐会话结果及窗口入选过程。关键数值与分母按保留证据输入；生成的点位、点数与几何形状仅用于临时预览，精确结果以正文、补充表和证据包为准。该阅读稿继续使用已获授权的独立布局，没有给第一篇增加期刊要求。正式数据图、作者声明和持久公开归档仍按后续定稿阶段处理。

2026-10-15 本轮导出：英文阅读版 **13 页**（正文与四张主图 6 页、参考文献 1 页、方法及数据说明 4 页，数据说明与首张扩展图共页，另两张扩展图各一页），英文行号版 **25 页**，中文对照 **11 页**，完整补充材料 **29 页**。相较上一轮 13/25/12/25 页，正文未缩减，补充材料新增四页；中文减少一页来自方法尾部与扩展图的连续排版。

验证已完成：四份 PDF 共 **78 页**渲染检查；20 条参考文献中英文顺序一致；每语言 7 张图片绑定有效；182 条当前过程窗口引文及主例预测原句核对；34 张历史数值表原单元格保留；三份构建脚本 Ruff 通过。另从五个参考观测逐题复算 1,044 条点误差、覆盖和区间分数，以及 261 个非缺失分组单元；九个缺失单元保留。证据包含 11 份公共材料，通过 ZIP 完整性检查，不包含私有世界参数、凭证或原始提供商传输记录。所有生成物由稿件源重建，未修改实验结果。
