# 自主研究如何塑造科学理解

**How autonomous research shapes scientific understanding**。沿用重要历史版的爱因斯坦1905年开篇与四节结构，以反绎、演绎和经验检验连接探索与理解。2026-10-17整合四矩阵、新300场结果与完整过程精读；没有新增实验，也未改变旧队列的证据地位。

## 阅读入口

- [中文PDF](../../../output/pdf/chemworld-nature-zh.pdf)
- [英文PDF](../../../output/pdf/chemworld-nature-en.pdf)
- [英文单栏行号版](../../../output/pdf/chemworld-nature-en-review.pdf)
- [完整补充材料](../../../output/pdf/chemworld-nature-supplement.pdf)
- [可复核证据包](../../../output/paper/chemworld-review-evidence.zip) · [证据说明](evidence/README.md)
- [重要历史版本](../../../output/pdf/archive/nature-inquiry-20261016/README.md)

源稿：[英文](article.md)、[中文](article_zh.md)；方法：[英文](methods.md)、[中文](methods_zh.md)；扩展图：[英文](extended_data.md)、[中文](extended_data_zh.md)。`tex/`与`supplementary.md`由构建脚本生成，不手工修改。

## 论证与证据

| 小节 | 主要解释工作 | 核心材料 |
| --- | --- | --- |
| 使自主科学探索成为可检验的研究对象 | 实验自由、持续状态与独立参照使证据选择和判断形成可核对 | 四矩阵450场设计，300新增/150保留，完整失败分母 |
| 科学探索的自主组织与适应 | 目标和信息进入路径，形成的判断又改变下一行动 | 重复EC/RX矩阵、纯化条件计划、资源耗尽、历史五模型路径、匹配世界前瞻检验 |
| 科学认识在实验中的形成与演变 | 候选、检验、局部关系、合理撤回、范围扩展及经历重建 | 新反应/分配/结晶连续过程，旧平衡和修正版结晶作对照 |
| 自主探索中科学进展的性质与条件 | 操作、点准确性、适用范围和不确定性可以分化 | 新结晶机会比较、保留平衡机会、按响应的信息收益、旧源均值诊断与预算 |

关键修订：新结晶研究使纯度和粒径判断明显改善，细粉区间评分仍恶化；旧“已有稳定证据未进入预测”只保留为特定队列的源观测使用诊断。反应先验收益分解为操作、风险和转化等判断，不再用总分概括。发现与误解可发生在同场不同判断上，不预设统一自我确认机制或纠错成功结局。

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

六张主图、六张扩展图全部是已标注的ImageGen临时预览。此次更新图2、5、6和扩展图2、6：[新图与提示词](figures/imagegen-preview-20261017/README.md)。其余图沿用[前次预览](figures/imagegen-preview-20261016/README.md)。数字来自保留证据；几何和曲线不作精确数据或统计区间使用。[旧原生定量图](figures/integrated-20261016/README.md)仍对应旧队列，不替代新表。

```powershell
uv run --no-sync python -X utf8 paper/tools/build_nature_review_evidence.py
uv run --no-sync python -X utf8 paper/tools/build_nature_evidence.py
uv run --no-sync python -X utf8 paper/tools/build_nature_manuscripts.py
```

第一步重建派生分析及ZIP，直接纳入已保留的新300场公开科学记录与逐场精读，不重新执行研究。第二步生成完整补充材料并保留34张历史表；第三步生成四份PDF。正式投稿前仍需数据绘制的最终图、永久公开存档与作者定稿。NCS、第一篇冻结稿及重要历史归档保持不变。

2026-10-17交付检查：英文23页、中文20页、英文行号版42页、补充材料37页，共122页已渲染并检查。页数包含各版方法、参考文献和扩展图，不等于正文篇幅。英文摘要155词；双语引用顺序、24处图源、34张历史表原样保留、主要逐世界方向、14条案例链接、证据包完整性与构建脚本Ruff检查通过。
