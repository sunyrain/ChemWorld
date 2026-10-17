# 自主研究如何塑造科学理解

**How autonomous research shapes scientific understanding**。沿用重要历史版的爱因斯坦1905年简短开篇与四节结构，围绕自主研究如何形成和使用科学认识组织全文。反绎保留为解释性假设形成的辅助视角，不再承担结果分类或能力评价。2026-10-17依据审稿意见整合四矩阵、新300场结果与完整过程精读；没有新增实验，也未改变旧队列的证据地位。

## 阅读入口

- [中文PDF（本轮修订版）](../../../output/pdf/chemworld-nature-zh-revised.pdf)
- [英文PDF](../../../output/pdf/chemworld-nature-en.pdf)
- [英文单栏行号版](../../../output/pdf/chemworld-nature-en-review.pdf)
- [完整补充材料](../../../output/pdf/chemworld-nature-supplement.pdf)
- [可复核证据包](../../../output/paper/chemworld-review-evidence.zip) · [证据说明](evidence/README.md)
- [重要历史版本](../../../output/pdf/archive/nature-inquiry-20261016/README.md)

源稿：[英文](article.md)、[中文](article_zh.md)；方法：[英文](methods.md)、[中文](methods_zh.md)；扩展图：[英文](extended_data.md)、[中文](extended_data_zh.md)。`tex/`与`supplementary.md`由构建脚本生成，不手工修改。

本轮导出时，WPS占用旧中文PDF并阻止覆盖，因此最新中文稿另存为上方修订版。原`chemworld-nature-zh.pdf`仍是前版；中英文源稿与修订版内容已同步。关闭该WPS文档后，常规构建即可恢复标准输出路径。

## 论证与证据

| 小节 | 主要解释工作 | 核心材料 |
| --- | --- | --- |
| 使自主科学探索成为可检验的研究对象 | 实验自由、持续状态与独立参照使证据选择和判断形成可核对 | 四矩阵450场设计，300新增/150保留，完整失败分母 |
| 科学探索的自主组织与适应 | 目标和信息进入路径，形成的判断又改变下一行动 | 新EC/RX矩阵；纯化双条件决策及库存耗尽；电化学极性认识与反向检验 |
| 科学认识在实验中的形成与演变 | 前瞻预期如何进入实际检验、局部关系和后续用途 | 反应等待—淬灭完整轨迹；两条匹配世界历史；跨体系支持移至扩展图 |
| 自主探索中科学进展的性质与条件 | 操作、点准确性、适用范围和不确定性可以分化 | 新结晶机会比较与同队列源观测参考、保留平衡机会、按响应的信息收益 |

关键修订：新结晶研究使纯度和粒径判断明显改善，细粉区间评分仍恶化；同批十五场研究的源观测均值参考又在纯度、粒径上全部优于智能体，回收上则十四场由智能体更好。由此区分获取证据的收益与使用证据的质量，旧队列诊断继续独立保留。三组核心过程展开为完整轨迹，接口歧义只作有明确边界的支持证据。发现与误解可发生在同场不同判断上，不预设统一自我确认机制或纠错成功结局。[新增派生分析](inquiry_revision_analysis.md) · [七条核心历史索引](evidence/core_history_index.json)。

## 矩阵与分母

| 矩阵 | 新增 | 保留 | 合计 |
| --- | ---: | ---: | ---: |
| 目标与信息：EC90、RX90 | 180 | 0 | 180 |
| 过程：PA45、P45；EQ45、修正C45 | 90 | 90 | 180 |
| 机会：新C30、保留EQ30 | 30 | 30 | 60 |
| 匹配化学机制世界 | 0 | 30 | 30 |
| 设计合计 | 300 | 150 | 450 |

新300场全部终态：288完整链、298有效预测、3,379/3,420源终检、898/900有效封存阶段。十场纯化材料耗尽缺41次终检，两场反应预测缺失/无效；四场服务中断技术补跑完成，中断尝试仍保留。精读覆盖300/300场、873版笔记、31,922条操作、1,363处核对引文。899份非空封存内容中含一份无效预测，不能与898有效阶段混淆。模型采样seed不可控。

保留150场协议、时期、失败均独立报告；历史广度300场和早期案例不并入450设计。原34张历史数值表不变。旧结晶回收口径不一致的结果仍为历史诊断，当前结晶使用统一初始投料、扣除晶种的回收定义。没有将阅读覆盖率作为反绎成功率，也不宣称独立人类第二编码。

来源由[当前绑定](../../../configs/current.json)解析，主入口为`work_ii.w2_267_unified_matrices`，保留`w2_257_inquiry_completion`和`w2_263_abductive_completion`等独立块。[新定量报告](../../../workstreams/flagship_tasks/reports/unified-matrices-20261016/REPORT.md) · [完整过程解释](../../../workstreams/flagship_tasks/reports/unified-matrices-20261016/PROCESS_REVIEW.md) · [新补充表](unified_matrices_analysis.md)。

## 图稿与构建

五张主图、八张扩展图全部是已标注的ImageGen临时预览。此次重做全部五张主图：[图件与完整提示词](figures/imagegen-inquiry-focus-20261017/README.md)。扩展图沿用[前次预览](figures/imagegen-preview-20261016/README.md)及[最近更新](figures/imagegen-preview-20261017/README.md)，历史模型路径和四案例图移入扩展图7、8。数字来自保留证据；几何和曲线不作精确数据或统计区间使用，五世界精确比较另存补充表。[旧原生定量图](figures/integrated-20261016/README.md)仍对应旧队列，不替代新表。

```powershell
uv run --no-sync python -X utf8 paper/tools/build_nature_review_evidence.py
uv run --no-sync python -X utf8 paper/tools/build_nature_evidence.py
uv run --no-sync python -X utf8 paper/tools/build_nature_manuscripts.py
```

第一步重建派生分析及ZIP，直接纳入已保留的新300场公开科学记录与逐场精读，不重新执行研究。第二步生成完整补充材料并保留34张历史表；第三步生成四份PDF。正式投稿前仍需数据绘制的最终图、永久公开存档与作者定稿。NCS、第一篇冻结稿及重要历史归档保持不变。

2026-10-17交付检查：英文23页、中文修订版20页、英文行号版41页、补充材料41页，共125页已渲染并检查。英文正文含主图8页，中文6页；各版总页数另含方法、参考文献和扩展图。摘要155词，五主图、八扩展图；26处图源及全部图注、双语引用、34张不变历史表、85行精确世界比较、15场/179条合格源测定参照、七条核心历史和十四条支持案例链接、证据ZIP完整性、五脚本Ruff与diff检查通过。修复扩展图6/7合并及图注缺失、补充材料长路径溢出；没有新增实验或独立第二评分者声明。
