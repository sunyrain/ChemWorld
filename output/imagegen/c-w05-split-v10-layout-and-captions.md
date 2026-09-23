# C-W05 示例图拆分：正文位置与图注建议

依据：远端 `origin/main` 的 `74c9303295762888594390640bf696f5645f1679`（2026-09-22，Add NCS Chinese manuscript and generated figure archive）新增的 `paper/venues/ncs/ChemWorld_NCS_中文正文_v1.md`，已读全文；同时对照本地有未提交修改的 `paper/venues/ncs/article.md`。本轮 fetch 获取远端，未合并或覆盖本地稿件。以下是图件编排建议，尚未修改正文、图号或 PDF。

## 判断

原 v9 把来源探索、预算对比、单批操作、推荐复测、盲测、事后反思和未执行提议都放在同一张竖图里。读者必须同时理解实验内操作、实验间选择和实验后的问答，两个时间层级互相挤压。拆为两张具有独立问题和完整图注的图，比简单上下裁切更合适。

最新中文稿已有六张主图，前两张分别承担研究框架与基础设施，后四张承担操作/预测、资源预算、先验区间效应和保持/修订。若本例两张均进入主文，建议形成七张主图：图1只保留基础设施的简要分层关系，详细事务、重放和资格验证结构移入 Methods 或扩展图。不要把旧图2所有内容压进图1。

## 推荐主图顺序

| 建议图号 | 科学问题与来源 | 正文位置 |
| --- | --- | --- |
| 1 | 自主研究框架；吸收简要基础设施分层 | 第一节，保留完整研究会话和双路评价 |
| 2 | 操作成功与预测知识分离；原图3 | 操作成功一节，保留 EC 主证据和 RX 边界 |
| 3 | 研究资源的总体作用；原图4 | 更多实验一节，保留 EC/PA 正面结果与 C 边界 |
| 4 | **新图 A：两种预算如何形成不同实验轨迹与推荐** | 总体预算结果之后，用具体 C 案例展示行动和观测；不替代总体结果 |
| 5 | 先验作用依赖区间和响应；原图5 | 先验信息一节，保留 EQ/P 九题/稀三题反转 |
| 6 | 错误保持与错误修订；原图6 | 最后一节，保留 EQ 与 C 纯度的互补证据 |
| 7 | **新图 B：原研究者如何预测、反思并提出后续检验** | 最后一节末尾、讨论之前，用一小段连接定量预测与公开反思 |

这是一种七图的叙事安排，不需要增加实验或添加新的总体统计结论。若之后压缩主图数量，优先把图 B 放入扩展图，而不是把两张再次合并。图 B 是选取的过程实例，图6的总体证据优先级更高。

## 图 A：实验过程

文件：[c-w05-split-a-research-v10.png](c-w05-split-a-research-v10.png)

**中文标题：不同研究预算形成不同的探索路径与操作推荐。**

保留三部分：

1. 同一世界、同一信息条件下两场独立的 12/24 批次会话，展示阶段和首次质量合格批次。
2. 各选一个真实的相邻批次决策：12 批次会话第9→10批降低冷却终点；24 批次会话第19→20批同时调整加热和冷却。
3. 两场分别选择第10与第23批配方，以及独立复测结果。

即时考虑只以带星号的示意性重构呈现；底层动作与数值来自记录。24批次不是12批次的续跑；阶段对齐不代表配对干预或相同耗时。

**建议正文引入句：**

> 一个选取的结晶配对案例展示了研究资源如何被组织为不同的探索历史（图4）。两场独立会话分别通过降低冷却终点，以及联合改变上游热处理与分段冷却形成了合格推荐。该案例中24批次会话的独立复测回收率较高、细粉比例较低，但它不代表结晶总体的预算效应，也不能把联合调整的收益归因于单一操作。

**Suggested English caption**

**Two research budgets produce different experimental paths and operating recommendations.** A retrospectively selected pair of independent crystallization campaigns shares the same world and aligned information. **a,** Phase summaries and the number of batches meeting the purity and fines constraints. **b,** Recorded observations and operations for batches 9–10 of the 12-batch campaign and batches 19–20 of the 24-batch campaign. Consideration notes are illustrative reconstructions; contemporaneous decision reasons were not logged. The latter transition changes both heating and cooling. **c,** Selected procedures and independent retests. Recovery excludes seed mass; fines are particles smaller than 20 μm. Heating temperatures are requested targets, not measured temperatures. These selected trajectories do not estimate the overall budget effect or isolate the contribution of any one process change.

## 图 B：证据使用与后测

文件：[c-w05-split-b-posttest-v10.png](c-w05-split-b-posttest-v10.png)

**中文标题：从实验经验到新干预预测：封存预测、公开反思与判别实验提议。**

保留四部分：

1. 同一前序结晶配方之后的两个新条件：低温保持，或复热再冷却。
2. 原来的两个研究会话分别预测细粉 17%→12% 与 49%→35%，并在预测封存、未获得真值反馈时回答哪项预测最不可靠。
3. 24批次会话另一个真实回答：保留第23批上游条件，将分段冷却替换为直接冷却。提议及其分支解释均未执行、未验证。
4. 单独显示复热题的无噪声评价器参考：细粉 35%→100%。此结果不是对上述未执行提议的测试，也没有作为反思的输入。

**与全文主张的关系：** 这是外推与事后证据反思的实例。它不是“结晶纯度稳定却被过度修订”的同一个现象，不能替代图6的纯度证据。也不能把 K2 的谨慎陈述写成 Q 之前的认知，或声称 agent 早已知道预测错误却拒绝修正——协议本就不允许 K2 修改封存预测。

**建议正文引入段：**

> 同一结晶案例的后测进一步展示了定量预测与公开反思之间的区别（图7）。两场研究会话都预测复热再冷却将降低细粉比例，而评价器参考给出相反方向。在没有参考反馈的回顾问答中，两者均指出该预测不可靠；24批次会话还指出，它没有充分利用第8批复热未见改善的结果，并提出一个区分上游条件与冷却作用的实验。该提议未执行，回顾也不能改变已封存预测。因此，这个实例能够定位 agent 公开承认的证据局限，不能据此认定内部错误原因已被识别或预测已得到修复。

**Suggested English caption**

**Blind predictions and retrospective reflection in the original research sessions.** **a,** Two held-out recipes share the same preceding crystallization process but end with either a 2-h low-temperature hold or 1-h reheating towards 315 K followed by 1-h recooling. Temperature diagrams show schematic targets. **b,** Both original agents predict lower fines after thermal cycling. After sealing their predictions, and without reference feedback, they identify the intervention as uncertain. Notes condense the recorded retrospective responses and are not verbatim quotations. **c,** The 24-batch agent proposes replacing staged cooling in its selected procedure with direct cooling while retaining upstream conditions. The test and its expected interpretations remain unexecuted. **d,** The noise-free evaluator reference for the reheating comparison in a gives the opposite fines direction. It does not evaluate the proposed experiment in c and was unavailable during prediction and reflection. This selected example does not estimate the prevalence or establish the cause of extrapolation failures.

## 数据来源与制作

- [12批次来源及后测](../../workstreams/flagship_tasks/reports/work-ii-c-formal-20260920-v3-auto/C-W05-B12-E-Aligned.md)
- [24批次来源及后测](../../workstreams/flagship_tasks/reports/work-ii-c-formal-20260920-v3-auto/C-W05-B24-E-Aligned.md)
- 配对题的无噪声参考：本地 `runs/formal/work-ii-c-five-world-20260920-v3-auto/qualification/W05/queries/result.json` 中第7/8题。图中取整数百分比展示。
- 制作工具：内置 imagegen。原 v9 合图保留；两张 v10 都是独立重新编排，未替换原图或修改论文。
- [图A提示词](c-w05-split-a-research-v10-prompt.txt)
- [图B提示词](c-w05-split-b-posttest-v10-prompt.txt)
