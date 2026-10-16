# ChemWorld：自主研究如何塑造科学认识

本目录是用户已授权的独立研究稿。2026-10-16 依照新的叙事要求扩展全文：以跨体系比较建立问题广度，以五模型路径展示证据获取与外推的多样性，以同期记录解释认识形成和使用，以匹配研究机会比较检验开展研究的贡献。四节框架和题目保留，摘要压缩为 171 个英文词，不放阶段性效应数字；正文恢复正向先验收益、研究目标与操作/预测差异、准确外推的不同路径及预算比较。第一篇冻结稿和 NCS 源稿及 PDF 不在本次修改范围。

## 阅读入口

- [英文阅读版](../../../output/pdf/chemworld-nature-en.pdf)
- [英文单栏行号版](../../../output/pdf/chemworld-nature-en-review.pdf)
- [中文对照版](../../../output/pdf/chemworld-nature-zh.pdf)
- [完整补充材料](../../../output/pdf/chemworld-nature-supplement.pdf)
- [可复核证据包 ZIP](../../../output/paper/chemworld-review-evidence.zip)及[数据说明与源表](evidence/README.md)
- [新增跨体系与五模型 ImageGen 数据预览](figures/preview-20261016/README.md)及[生成提示与修改记录](figures/preview-20261016/prompts.json)
- [沿用的七张框架/过程/对照预览](figures/preview-20261015/README.md)及[原始生成记录](figures/preview-20261015/prompts.json)

正文：[英文](article.md)、[中文](article_zh.md)。方法：[英文](methods.md)、[中文](methods_zh.md)。扩展图说明：[英文](extended_data.md)、[中文](extended_data_zh.md)。补充材料由脚本从保留结果生成；`tex/` 由 Markdown 构建，不手工编辑。

## 行文框架

题目：**How autonomous research shapes scientific understanding / 自主研究如何塑造科学认识**。

中心问题是实验自主性怎样转化为科学认识的拓展。正文按研究过程推进，不把全部结果解释为自我确认，也不将纠错策略成功设为收束条件。

| 结果小节 | 段落承担的工作 | 主要证据 |
| --- | --- | --- |
| 使自主科学探索成为可检验的研究对象 | 解释自主选择、公开观测、同期判断、后续使用和独立世界参照怎样连接 | 化学接口；300 场广度研究；当前 90 场过程记录；另行 30 场机会比较 |
| 科学探索的自主组织与适应 | 研究目标与先验进入探索；不同研究者获得不同证据；反馈进入下一实验 | EC/RX 各 30 对目标比较与完整 EC 案例；反应先验正向收益；结晶初始选材与覆盖；五模型 75 场、Astra 与 Sol/Opaque 两条准确路径；平衡研究 A |
| 科学认识在实验中的形成与演变 | 局部关系、前瞻检验、失败后修订、执行证据资格及关系推广 | 92 个结构窗口；修正版结晶低投料、插值、播种案例 B/C；平衡研究 A 连续记录，其他案例进入补充 |
| 自主探索中科学进展的性质与条件 | 分别考察先验、资源、研究机会的贡献，以及关系在新条件下的使用 | 两代 EQ 先验比较分开报告；五模型先验响应；12/24 批独立资源比较；研究机会总体/区域/响应结果；42 场源观测参照 |

第二、第三节描写持续交互的两个方向，而不是研究只经过一次的流水线。图 2 展示跨体系目标与先验比较，图 3 展示五模型证据路径。“平衡研究 A”（W01 Research 第一重复）从第二节的预期与实验，延续到第三节的外推，再连接第四节的同期比较；图 4 集中展示该连续轨迹。结晶图 5 展示有依据的局部改进、失败后的合理撤回和未执行高播种的不同理解；图 6 承担研究机会比较。讨论以正确性、证据支持、实际用途三者的联系收束，不把局部反转或自我确认当作全文唯一发现。

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

`process_cases.json` 是上一版选定案例的历史记录，并不定义本轮主例。`figures/preview/` 是上一版图稿预览，`figures/` 上层的数据参考图也不属于当前插图；当前稿嵌入 `figures/preview-20261015/` 的七张 PNG 和 `figures/preview-20261016/` 的两张新增数据预览。

## 构建与验证

```powershell
uv run --no-sync python paper/tools/build_nature_review_evidence.py
uv run --no-sync python paper/tools/build_nature_evidence.py
uv run --no-sync python paper/tools/build_nature_manuscripts.py
```

第一条生成可复核证据包并检查均值、公共输入一致性、窗口筛选和 182 条引文；第二条生成补充表，保留全部失败、过程窗口和 34 张历史表；均不产生新模型/模拟器实验，也不重新生成图片。第三条使用 Pandoc、XeLaTeX、共享文献库及既有独立模板，输出英文阅读版、英文行号版、中文对照和完整补充材料。本轮仅执行第三条，沿用已验证的证据和补充表；构建与视觉检查位于仓库外 `ChemWorld-local-research/manuscript-nature-20261016/`。

当前九图均由内置 ImageGen 生成：主图 1 为总框架图，主图 2–6 与扩展图 1–3 为数据预览。本轮新增跨体系目标/先验比较和五模型证据路径两图，保留既有连续轨迹、正向检验、研究机会与响应参照。关键数值与分母按保留证据输入；生成的点位、点数与几何形状仅用于临时预览，精确结果以正文、补充表和证据包为准。该阅读稿继续使用已获授权的独立布局，没有给第一篇增加期刊要求。正式数据图、作者声明和持久公开归档仍按后续定稿阶段处理。

当前正文（不含摘要、图注和方法）由 2,637 扩至 3,983 个英文词；摘要由 189 缩至 171 词。2026-10-16 四份导出为英文阅读版 **17 页**、英文行号版 **31 页**、中文对照 **15 页**、完整补充材料 **29 页**。英文正文与六张主图占 **9 页**，上一轮为 6 页；中文正文与六主图占 8 页。上一轮四份完整 PDF 为 13/25/11/29 页。

证据包和补充数值保持上一轮已验证状态：182 条当前过程窗口引文、1,044 条点误差/覆盖/区间分数、261 个非缺失分组单元及九个缺失单元，均未因本次叙事修改而重算或替换。本轮定向检查已确认 21 条参考文献的中英文顺序相同、每语言九张图片绑定有效，以及 34 张历史表原单元格不变。

本轮四份 PDF 共 **92 页**已逐页渲染、联系表检查，并放大核对标题摘要、新增图和历史数值表；未见文字溢出、缺字、未解析引用或图注截断。图号 1–6 与中英文引用顺序核对通过，构建脚本 Ruff 和 diff 检查通过。新图为内置 ImageGen 生成且提示词完整保存。未新增科学实验、重写结果或改动第一篇冻结稿/NCS；生成的 TeX/PDF 均来自当前 Markdown。
