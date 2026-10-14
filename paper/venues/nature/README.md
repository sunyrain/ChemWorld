# ChemWorld：自主科研如何将实验经历转化为科学认识

这是按用户授权新建的 Nature 正刊风格独立版本。NCS 源稿、图和现有 PDF 未被覆盖。2026-10-14，用户进一步要求全部图使用 ImageGen，当前 4 张主图和 3 张扩展图因此均为**临时视觉预览**，不可作为投稿定量图。

## 阅读入口

- [英文双栏阅读版](../../../output/pdf/chemworld-nature-en.pdf)：14 页，开篇引用摘要、正文、参考文献、方法和扩展数据。
- [英文单栏行号版](../../../output/pdf/chemworld-nature-en-review.pdf)：26 页，12 pt、双倍行距，供逐段讨论。
- [中文对照阅读版](../../../output/pdf/chemworld-nature-zh.pdf)：12 页，同步正文、方法和扩展图说明；参考文献与图内标签保持英文。
- [完整补充材料](../../../output/pdf/chemworld-nature-supplement.pdf)：21 页，90 场逐场数值与记录清单、9 场结构化主例、全部不完整链、90 个淬灭配对处置、34 张保留结果表及执行过程关系。
- [全部七张 ImageGen 图](figures/preview/README.md)与[实际使用的提示词](figures/preview/prompts.json)。

正文编辑入口为 [article.md](article.md) 和 [article_zh.md](article_zh.md)；方法为 [methods.md](methods.md) 和 [methods_zh.md](methods_zh.md)；扩展数据为 [extended_data.md](extended_data.md) 和 [extended_data_zh.md](extended_data_zh.md)。`tex/` 是从这些源稿生成的完整 XeLaTeX 文件，不另行手改。

四份 PDF 已逐页渲染并检查；脚本 Ruff、图源、引用顺序和保留表格一致性检查通过。当前文件用于阅读与讨论，投稿前事项见文末。

## 中心论证与结果组织

中心问题是：实验自主性如何转化为可靠、可迁移的科学认识。当前稿件以同一平衡研究中的完整轨迹承担中心：先提出并实际检验组分映射猜想，合理修订局部解释，随后又将该实验作为收缩极稀预测的依据。结晶的已述高纯度与后续预测提供互补过程。局部发现与后续使用的分化可以出现在同一段研究中；不预设自我确认机制，也不要求以改进策略成功收束。

2026-10-14 按新主线与对照审稿意见重写标题、摘要、结果连接与讨论。补充材料新增全部 90 场记录可用性清单、9 场结构化主例和 14 条按笔记版本/封存阶段核对的短引文，数据源为 [process_cases.json](process_cases.json)。该表不等于全队列统一机制编码，独立研究者复核尚未完成。

## Recovery 口径核对与结论调整

审稿意见指出的分母问题确实存在，而且不能解释成简单的新旧队列差异：

- [模块内部回收](../../../src/chemworld/runtime/crystallization_services.py)以分离前目标物为分母。
- [完整流程观测覆盖](../../../src/chemworld/runtime/observation_services.py:394)以 `initial_reactant_amount` 为分母；[该量定义](../../../src/chemworld/runtime/species.py:192)来自所跟踪的初始试剂投料。
- [TruthCapture](../../../scripts/run_work_ii_c_pilot.py:251)从同一观测内核捕获最终取样前响应；[推荐复测、参考读取与评分](../../../scripts/run_work_ii_c_formal.py:968)沿此路径。不是直接读取结晶模块内部阶段回收率。
- 两期执行提交 `68dce156` 与 `69337c7d` 中均核实了相同覆盖公式；保存的源指令及 Q 提示却定义为分离前目标物归一化。完整公式和各接口角色已写入中英文方法及补充材料。

原数值不变，但回收误差与质量/回收联合计数改作受协议不一致影响的诊断值，退出中心科学迁移论证；新增颗粒/纯度/细粉合格数 O/A/M 为 10/15、9/15、14/15。高纯度观察、公开识别与后续低估的同研究者对照保留。记录本路径在原指令下形成，不能声称这一问题对 Agent 选择没有影响。若今后要证明定义一致的回收预测或优化能力，需要先统一接口，再另开受影响的固定实验块；本轮未改运行时或重跑。

| 正文推进 | 实验与结果 | 图文位置 |
| --- | --- | --- |
| 自主取证及可核对的研究时序 | 旧 300 场提供广度；新 90 场、284 版笔记提供同期过程，二者分别计数 | 开篇与图 1 |
| 真实反馈支持检验、修订和工作关系 | 平衡组分映射检验；结晶种量拯救预期撤回；体积窗口的前瞻检验、重复与复测 | 图 2 |
| 局部修订与外推使用可以分化 | 接续同一 EQ W04/M/R1 会话的极稀预测；45 场完整定量覆盖；同世界重复及正确外推对照 | 图 3 |
| 操作成功、公开认识和新条件判断需分别考察 | C W04/M 三次会话均推荐成功、识别高纯度，却下调新配方纯度；45 场各响应误差 | 图 4 |
| 证据地位可与实际执行不一致 | C W04/A/R3 的 2 g 请求、0.05 g 成功投料与持续阴性记述；C W02/A/R2 正确识别拒绝的对照 | 扩展数据图 1 |
| 公开原则与最终选择可能不同 | 边界回收选择与保留余量的两个说明案例，非策略试验 | 扩展数据图 2 |
| 世界效果与认识形成原因分别解释 | 原 18 条推荐跨五世界的有无淬灭对照，90 对全部保留，75 对完整 | 扩展数据图 3 |

原研究包含 240 场 Sol 跨体系研究与 60 场其他模型平衡研究；五模型平衡共 75 场，其中 15 场 Sol 已计入 240，不重复累加。24 场较早笔记案例也不混入旧 300 或新 90。新 90 分为前期 48 与扩展 42，84 条链完整、86 个 Q 有效。模型采样 seed 不可控，不称为受控 seed 重复。参考、推荐复测和固定配方干预不增加研究者人数。

读数区分实际执行、当时公开表述、后续预测和评价者真值。笔记不是内部认知直接读数；时间顺序和公开理由不证明笔记的因果作用。没有将旧稿 8.7 倍外推误差比写成本次重复幅度；当前 Aligned/Opaque 比约 1.34。错配臂较晚执行，结晶只交换 S1/S3 描述，不能把 14/15 操作成功解释为错误知识的因果收益。

## 证据来源

- [证据族与补实验判断](../../../workstreams/flagship_tasks/reports/research-extension-20261014/EVIDENCE_FAMILIES.md)：六族定位、主例原文与边界。
- [90 场定量分析](../../../workstreams/flagship_tasks/reports/research-extension-20261014/ANALYSIS.md)和[机器摘要](../../../workstreams/flagship_tasks/reports/research-extension-20261014/process_analysis.json)。
- [新增 42 场逐场精读](../../../workstreams/flagship_tasks/reports/research-extension-20261014/CASE_READINGS.md)、[前期 48 场精读](../../../workstreams/flagship_tasks/reports/research-formation-20261013/CLOSE_READING.md)。
- [淬灭全部处置](../../../workstreams/flagship_tasks/reports/research-extension-20261014/QUENCH.md)。
- [旧研究矩阵](../../../workstreams/flagship_tasks/WORK_II_EXPERIMENT_MATRIX.md)、[NCS 保留补充材料](../ncs/supplementary_en.md)。新补充材料逐字保留其中 34 张表的单元格，不改变原分母或结果。
- [当前产物路由](../../../configs/current.json)继续约束既有生成证据；本目录为新稿件入口，不更改冻结绑定。

## 预览图与真实数据

稿件只嵌入 `figures/preview/` 中的七张 ImageGen PNG，使用内置工具生成，并以该身份标注。部分生成图将分布简化为均值，另一些仍带示意散点；这些散点、误差线位置、示意时间线及文字概括不可用于定量解读，也不是原笔记逐字引文。ImageGen 对图 1 的反馈时序、扩展图 2 的主体与纵轴做过定向修正。准确数字由正文和补充表承载。

`figures/` 上一层的七组 PDF/PNG 是从保留结果脚本生成的数据参考，不是当前插图。选定版式后需用真实数据重建正式矢量图，不能将预览图片直接升级为证据图。

## 排版与重建

采用独立的标题、带引用开篇摘要、四主图、Methods 和 Extended Data 结构。双栏版是受 Nature 阅读布局启发的作者稿，不是官方出版排版，没有期刊标志、卷期或 DOI。单栏行号版用于内部审阅，并非已经具备投稿全部声明的文件。

官方参考：[Nature formatting guide](https://www.nature.com/nature/for-authors/formatting-guide)、[initial submission](https://www.nature.com/nature/for-authors/initial-submission)。本稿开篇英文摘要 195 词，正文不含开篇摘要和图注约 2,540 词，方法约 2,576 词；四张组合图的实际占页仍须按最终图稿判断。引用采用顺序上标，超过五名作者以首位加 et al. 表示。作者顺序、单位、共同贡献及通讯信息读取保留 NCS 元数据，资助沿用用户确认原文。

```powershell
uv run --no-sync python paper/tools/build_nature_evidence.py
uv run --no-sync python paper/tools/build_nature_manuscripts.py
```

第一个命令只读取保留 JSON 与旧表，生成数据参考图及补充材料；不会重新调用 ImageGen，不覆盖七张预览。第二个命令使用 Pandoc、XeLaTeX 和本目录独立模板，生成四份 PDF 与对应 TeX；参考文献读取共享 BibTeX。两者均不调用模型或模拟器开展新实验。构建日志和视觉检查页图位于仓库外 `ChemWorld-local-research/manuscript-nature-20261014/`。

## 收稿前仍需落实

目前不需要为了这条限定明确的主线默认追加覆盖矩阵。最终主例仍应由另一位研究者独立核对，保留解释分歧；当前不能声称编码一致性已验证。若要报告机制发生率、先验的独立因果作用或跨模型同期形成规律，则先补相应编码或针对性实验，而非直接扩大当前表述。

投稿前还需作者确认贡献与利益冲突声明、确定完整研究的公开数据/代码归档及永久入口，并将 ImageGen 预览重制为证据准确的正式图。上述项目不被当前排版完成所替代；稿件没有虚构相关声明，也没有将开发证据自动提升为正式资格结果。
