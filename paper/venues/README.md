# ChemWorld 双稿工作入口

用户于 2026-09-21 决定同步准备 ICLR 与 **Nature Computational Science Article**。
这里维护两个完整写作版本，共用已完成证据；NCS 的文章类型已确定，不再按 Resource 组织。
当前 NCS 英文稿已完成本轮全文与图表收束；稿件尚未提交。

2026-09-23 结晶案例图已改为常规字重，a/b/c 与新 Figure 1 的 Arial 子图标记统一，图例和限制说明移入图注。英文 Figure 2 与中文 Figure 4 使用同一更新图；[可编辑单图](../../output/pptx/chemworld-figure2-typography.pptx)独立保留，原合并PPT未覆盖。两张原生曲线的全部系列数值与此前图件一致。

2026-09-23 Figure 1 已替换为用户提供的 `FIgure1_2.pptx` 第1页。当前阅读文件为[英文正文 PDF](../../output/pdf/chemworld-ncs-en-final.pdf)与[中文正文 PDF](../../output/pdf/chemworld-ncs-zh-full.pdf)，均保留前次 EQ 图、独立表1及补充表F1的更新。新图采用原生 PDF 嵌入，原PPT不改动，图注已对应新的 a/b/c 分区；见[图件来源](../figures/venue-results/figure01-user-ppt.README.md)。

2026-09-23 已按用户确认替换 EQ 主图：五世界的参考值与三臂点预测直接对照，误差/覆盖率独立为正文表1，全部十五场区间及来源范围保留于补充表F1。[英文更新 PDF](../../output/pdf/chemworld-ncs-en-eq-replacement.pdf)（32页）与[中文更新 PDF](../../output/pdf/chemworld-ncs-zh-eq-replacement.pdf)（35页）均已重建。英文保留下述流程图及 Fig. 6 优化，使用同数据的可编辑PPT柱图；中文使用批准的原预览图，其余章节保持当前中文结构，补充图引用按自身编号校正。EQ 图件来源见[替换说明](../figures/venue-results/eq_predictions_reference.README.md)。

2026-09-23 已完成 [英文完整 PDF](../../output/pdf/chemworld-ncs-en-final.pdf) 与 [配图 PPT](../../output/pptx/chemworld-figures-final.pptx) 的读者版优化。沿用指定 preserved 稿件与 v16 案例素材；真实结晶研究路径升为主文 Fig. 2（PDF 第 4 页），EQ 使用已确认的五世界柱图及独立 Table 1，Fig. 6 直接展示纯度值与逐场预测误差差值。正文六图一表，完整先验/预算统计与后测反思保留为五幅补充图，十五场 EQ 预测区间完整保留于 Table F1。全文 32 页，Methods 不变。图表位置与重建命令见[最终图表说明](../figures/final-ppt/README.md)。本轮未重建 ICLR，未运行新实验。

2026-09-22 已同步远端 [NCS 叙事指南](ncs/README.md)，并将全部十五场 EQ/P 原自主过程核对整合到 NCS 主文、Methods、两张更新主图及共享补充材料 C.4。主线保持原会话的连续研究与预测；固定记录的新会话读出已退出验证路径，余下 28 格不再排期。两个 PDF 已同步，ICLR 正文结构保持；本轮只使用保留数据。

| 项目 | ICLR 2027 | Nature Computational Science |
|---|---|---|
| 英文正文 | [manuscript.md](iclr2027/manuscript.md) | [article.md](ncs/article.md) |
| 阅读 PDF | [ICLR PDF](../../output/pdf/chemworld-iclr2027.pdf) | [NCS Article PDF](../../output/pdf/chemworld-ncs-en-final.pdf) |
| 工作标题 | ChemWorld: Task Success Does Not Ensure Scientific Generalization | Controlled chemical worlds reveal limits of generalization in autonomous scientific research |
| 核心读者问题 | 怎样评价 agent 是否从实验中获得可泛化的知识？ | 自主研究何时应维持已观察规律，何时应改变它？ |
| 主要贡献组织 | 可控环境与评价协议；目标、预算、先验干预；agent 行为发现 | 计算实验工具；跨任务现象；规律适用范围的互补失效与科学解释 |
| 主文结构 | Introduction → instrument/protocol → task success → budget → priors → response regimes → related work/limits | 无标题引言 → Results 五小节 → Discussion → Methods |
| 当前篇幅 | 正文 7 页、含附录 21 页，摘要 198 词，4 幅主图 | 正文 2,709 词、含补充材料 32 页，摘要 143 词；6 幅主图、1 张正文表、5 幅补充图 |
| 作者处理 | 匿名，PDF 正文与元数据检查作者身份信息 | 保留现有六位作者顺序、单位、共同贡献及通讯信息 |

2026-09-22 已将 NCS 图 3 的交叉连线改为按世界/先验臂排列的配对变化，统一改善方向，保留全部数据及绝对均值；[当时的中文整稿](../../output/pdf/chemworld-ncs-zh-budget-redesign.pdf)同步此图。此前英文导出均保留，当前英文版以上表为准。

PDF 均附完整协议、全指标表和新增探索性分析。篇幅自动统计见
[BUILD_SUMMARY.json](BUILD_SUMMARY.json)；正文词数排除摘要、图注和 Methods，
采用脚本的英文词边界算法，投稿系统统计可能略有不同。

## 两版共用的科学主线

1. **先把研究成功拆清楚。** 合法操作、交付合格产物、预测新条件、给出合理不确定性是相连但不同的结果。EC 的 26/30 对 14/30 是入口；P 说明质量约束不能被回收率替代。
2. **检查资源不足这一解释。** EC、PA 在较大预算下明显改善，C 的部分响应仍有问题。保留成功案例及反例，也说明 24 批是新会话、更大的资源包，不能解释成只增加十二个数据点。
3. **检查先验信息这一解释。** RX/P 有明确正面结果，其余条件并非共同排序。EQ/P 的整体劣势进一步拆成同一世界内不同浓度区间的反转。
4. **回到具体证据与适用范围。** EQ 的平台区响应在稀释区间应当改变；C 的低变异纯度在测试区间反而应当保持。二者共同提出“什么时候继续相信一个经验规律”的研究问题。
5. **把解释与因果证明分开。** 现有结果支持行为模式与选择性失效。先验锚定、信息压缩损失、采样与推断的因果分解仍是待检验解释。

ICLR 版本把这一链条用于建立评价论点。NCS Article 版本把它用于论述计算工具
揭示的科学推断问题。两版不是替换标题的同文，也不依赖虚构尚未完成的结果来区分。

## 共用证据及同步规则

当前共同分母为 **240 场 source campaigns、238 条合规链、3,597/3,600 次最终测定、
720/720 个 K1/Q/K2 阶段、165 次推荐复测，以及 15 个额外 EQ 参数补充报告**。
平台支持九个任务家族，当前匹配 agent 研究覆盖六个；二者不能混写。

- 数值来源：[统一证据入口](../CHEMWORLD_INTEGRATED_EVIDENCE.md)与其中绑定的完成结果。
- 全指标共享表：[chemworld_integrated_results_appendix.md](../chemworld_integrated_results_appendix.md)，由现有分析脚本生成，两个 PDF 直接读取同一文件。
- 共享协议：[shared_protocol.md](shared_protocol.md)。任何对方法事实的更正应同时核对两版正文的对应陈述。
- 共享探索性分析：[shared_exploratory_analysis.md](shared_exploratory_analysis.md)。EQ 稀释分组和 C 联合响应比较明确标为事后分析。
- 新图的数值：[EQ 分组](../figures/venue-results/eq_regimes.csv)和 [C 世界配对](../figures/venue-results/c_response_pairs.csv)，从已保存的完整世界分析再生成。
- 原自主过程：[十五场 EQ/P 核对](../../workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921/EQ_AUTONOMOUS_PROCESS_REVIEW_ZH.md)及其机器摘要；[原会话预测图数据](../figures/venue-results/eq_autonomous_predictions.csv)逐场与来源核对。Q 公开解释的有限回顾性分类不等于同期推理记录或全队列机理评分。
- 所有发现和待检验解释仍在[发现目录](../../workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921/FINDINGS_AND_HYPOTHESES_ZH.md)中讨论；它不是可直接全部搬入摘要的结果集。

只有第一篇平台资格验证保留其原冻结地位。当前 agent 开发证据不会因为进入
两份稿件而自动升级为正式验证。旧的 ICLR prior-discovery 导出不覆盖；
原 integrated review PDF 保留为此前讨论版，不作为这两个投稿版的构建入口。

## 图表对应关系

| 证据内容 | ICLR | NCS Article |
|---|---|---|
| 平台控制与推荐/K1/Q/K2 时序 | Fig. 1 | Fig. 1 |
| EC/RX 目标配对 | Fig. 2 | Fig. 3 |
| 12/24 预算变化 | 附录 A.7 | Fig. 4；完整六项为 Fig. S3 |
| RX 先验收益与 EQ 浓度区间反转 | Fig. 3 含 EQ 分组 | Fig. S2 与主文 Table 1 |
| EQ 原自主实验与稀释外推 | 共享附录 C.4 | Fig. 5，保留五世界十五场预测 |
| C 与同源均值基线比较 | Fig. 4 | Fig. 6 展示实际纯度与 agent-minus-mean 误差差值 |
| 完整先验概览 | 附录 A.6 | 补充材料 A.6 |
| 选定的 12/24 批结晶路径与后测反思 | 未增加案例配图 | 主文 Fig. 2；后测反思 Fig. S4 与附录 D |
| 纯化交付、C 粒度及 fines 比较 | 既有正文及共享附录 | 补充图 S5，附录 E |
| 所有指标、参考对象、失败与探索性分组 | 共享附录 A–C | 共享补充材料 A–C；案例与补充结果为 D–E；完整 EQ 区间为 F |

NCS 主文使用六幅图和一张表。真实流程案例保留主文完整一页；全量先验/预算比较、后测反思与次要响应进入补充材料，正文保留对应引用。

## 下一轮修订重点

首个回顾性问题已整理为[世界合理性与任务可学性分析](../../workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921/WORLD_VALIDITY_REVIEW_ZH.md)：区分已有资格检查能证明什么，以及 C/EQ 等关键结论还需要哪些证据，包含可直接修订的审稿回应草稿。

以下是写作和研究优先级，不是阻止继续编辑的 gate，也不授权新的模型实验。

1. **用已有过程证据收束解释。** EQ/P 全部十五场的操作、K1、Q 和 K2 已完成有限核对并进入稿件。保留成功、失败和混合解释反例；未提供的同期决策理由不补写，Q 新提出的模型不倒记到 K1。当前没有声称完成全部 240 场机理评分，也不将其设为无限扩展的前置任务。
2. **准确界定已有比较。** 同源均值/最近邻定位 C 的响应特异性错误，不充当强经典系统辨识基线。保留它在低变异纯度上占优的条件，不用基线胜负推断是否学得了机制；不因这一边界自动新增比较实验。
3. **固定研究对象和因果边界。** EQ 稀释分组与公开解释分类均为回顾性分析，五世界共享结构。完整自主研究的条件差异包含取证和解释两条路径；当前不拆成固定记录的新会话任务，不追加世界、模型或预算，也不声称已证明锚定、报告压缩或排除了证据不足。
4. **分别打磨定位。** ICLR 应明确相对现有 scientific-agent benchmark 的评价增量；NCS 应强化计算方法及它揭示的新科学问题。两版均需针对近期相关工作继续补全比较。当前九条参考文献足以建立首稿背景，尚不是投稿前完成的文献覆盖。
5. **完成交付材料。** ICLR 需整理匿名代码/数据包并确认与既有摘要注册内容一致；NCS 需最终归档数据/代码、完成作者贡献、基金及利益冲突等由作者确定的声明。现稿不编造这些信息或公开可用性。两条投递路径的选择与实际提交留待作者决定。

## 构建

```powershell
uv run --no-sync python paper/tools/render_venue_results.py
uv run --no-sync python paper/tools/build_venue_manuscripts.py
```

重建本轮 NCS 最终稿时，使用已经从最终 PPT 导出的图：

```powershell
uv run --no-sync python paper/tools/build_venue_manuscripts.py --venue ncs --output output/pdf/chemworld-ncs-en-final.pdf
```

单独构建可用 `--venue iclr2027` 或 `--venue ncs`。脚本读取保留数据、共享补充材料
及现有参考文献，不调用模型或模拟器。使用 Pandoc、BibTeX、pdfLaTeX/XeLaTeX、
Poppler；临时 TeX、日志和排版检查图保存在系统临时目录。Markdown 图片使用可直接
预览的相对路径，构建时归一到共享图目录。原 ICLR 2027 官方样式文件不作修改。

## 格式依据

- [ICLR 2027 Author Guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines)：初次投稿正文最多 **9 页**；讨论/终稿的 10 页额度不能挪用于初投。参考文献、附录及指定声明不计正文页数。现有官方样式来源见 [SOURCE.md](../iclr2027/SOURCE.md)。
- [NCS content types](https://www.nature.com/natcomputsci/content)：**Article** 摘要最多 150 词，正文最多 3,500 词，主要展示项最多 6 个；引言不单设标题，Results 可分小节，Discussion 不设小标题，Methods 单列。
- [NCS article-type editorial](https://www.nature.com/articles/s43588-023-00588-y)：文章类型应对应贡献，不能把 Article/Resource 当作降低证据要求的选择。当前 NCS PDF 是可读投稿草稿排版，并非仿制已录用期刊版式。

格式信息核对日期：2026-09-21。此次只准备稿件，未向任何会议或期刊提交。
