# ChemWorld 双稿工作入口

用户于 2026-09-21 决定同步准备 ICLR 与 **Nature Computational Science Article**。
这里维护两个完整写作版本，共用已完成证据；NCS 的文章类型已确定，不再按 Resource 组织。
当前是供作者讨论和继续修订的首版全文，不是已提交或已录用稿。

| 项目 | ICLR 2027 | Nature Computational Science |
|---|---|---|
| 英文正文 | [manuscript.md](iclr2027/manuscript.md) | [article.md](ncs/article.md) |
| 阅读 PDF | [ICLR PDF](../../output/pdf/chemworld-iclr2027.pdf) | [NCS Article PDF](../../output/pdf/chemworld-ncs-article.pdf) |
| 工作标题 | ChemWorld: Task Success Does Not Ensure Scientific Generalization | Controlled chemical worlds reveal limits of generalization in autonomous scientific research |
| 核心读者问题 | 怎样评价 agent 是否从实验中获得可泛化的知识？ | 自主研究何时应维持已观察规律，何时应改变它？ |
| 主要贡献组织 | 可控环境与评价协议；目标、预算、先验干预；agent 行为发现 | 计算实验工具；跨任务现象；规律适用范围的互补失效与科学解释 |
| 主文结构 | Introduction → instrument/protocol → task success → budget → priors → response regimes → related work/limits | 无标题引言 → Results 五小节 → Discussion → Methods |
| 当前篇幅 | 正文 7 页，摘要 198 词，4 幅主图 | 正文约 1,980 词，摘要 143 词，5 幅主图 |
| 作者处理 | 匿名，PDF 正文与元数据检查作者身份信息 | 保留现有六位作者顺序、单位、共同贡献及通讯信息 |

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
- 所有发现和待检验解释仍在[发现目录](../../workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921/FINDINGS_AND_HYPOTHESES_ZH.md)中讨论；它不是可直接全部搬入摘要的结果集。

只有第一篇平台资格验证保留其原冻结地位。当前 agent 开发证据不会因为进入
两份稿件而自动升级为正式验证。旧的 ICLR prior-discovery 导出不覆盖；
原 integrated review PDF 保留为此前讨论版，不作为这两个投稿版的构建入口。

## 图表对应关系

| 证据内容 | ICLR | NCS Article |
|---|---|---|
| 平台控制与推荐/K1/Q/K2 时序 | Fig. 1 | Fig. 1 |
| EC/RX 目标配对 | Fig. 2 | Fig. 2 |
| 12/24 预算变化 | 附录 A.7 | Fig. 3 |
| EQ 浓度区间反转 + C 响应分化 | Fig. 3 | Fig. 4 |
| C 与同源均值基线比较 | Fig. 4 | Fig. 5 |
| 完整先验概览 | 附录 A.6 | 补充材料 A.6 |
| 所有指标、参考对象、失败与探索性分组 | 共享附录 A–C | 共享补充材料 A–C |

NCS 目前使用 5 个主文展示项，给后续真正有增量的分析保留 1 个位置，不用无关图填满。

## 下一轮修订重点

以下是写作和研究优先级，不是阻止继续编辑的 gate，也不授权新的模型实验。

1. **先做现有结果的过程解释。** 从已保留的轨迹中统一抽取“提出的规律—所用证据—承认的边界—实际预测”，覆盖成功与失败，并记录等价机制表达。先完成跨世界的可核对分析，再讨论是否需要独立复核或额外模型判分。当前两稿均未声称已有全体机理评分。
2. **补强比较而非扩充体系数量。** 当前同源均值/最近邻只定位 C 的选择性错误，不是强经典系统辨识基线。评估哪些公共模型比较能够公平复用已有数据，明确拟合信息与调参规则；需要新数据的比较另行设计，不从现有结果中挑一个有利方案冒充预设基线。
3. **检验主解释的稳健性。** EQ 的三个稀释问题是事后分组。后续有资源时，优先独立世界/查询验证、同证据条件下的推断比较或新的 agent 配置，而不是立即铺开剩余三个体系。现在不能据此声称已证明“先验导致锚定”或“报告压缩损失”。
4. **分别打磨定位。** ICLR 应明确相对现有 scientific-agent benchmark 的评价增量；NCS 应强化计算方法及它揭示的新科学问题。两版均需针对近期相关工作继续补全比较。当前九条参考文献足以建立首稿背景，尚不是投稿前完成的文献覆盖。
5. **完成交付材料。** ICLR 需整理匿名代码/数据包并确认与既有摘要注册内容一致；NCS 需最终归档数据/代码、完成作者贡献、基金及利益冲突等由作者确定的声明。现稿不编造这些信息或公开可用性。两条投递路径的选择与实际提交留待作者决定。

## 构建

```powershell
uv run --no-sync python paper/tools/render_venue_results.py
uv run --no-sync python paper/tools/build_venue_manuscripts.py
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
