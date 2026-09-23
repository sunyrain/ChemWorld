# EQ 图与表分开：第二版讨论预览

**状态：2026-09-23 用户已批准，并已替换中英文 NCS 正文。** 正文使用[发布图件](../../../paper/figures/venue-results/eq_predictions_reference.README.md)、独立表1及[补充表F1](../../../paper/venues/ncs/eq_prediction_details.md)。以下保留本版设计和原始生成入口。

2026-09-23。回应用户对嵌入表格、难读 a/b 和突兀黑色符号的意见。主图只保留一个比较任务：在每个世界的同一最稀配方下，三种先验臂的点预测与盲测参考相差多少。

- [单图 PNG](eq-predictions-vs-reference.png) / [可编辑 SVG](eq-predictions-vs-reference.svg)
- [独立结果表](TABLE.md)：三臂、两类题目的宏观误差与覆盖率
- [完整预测区间表](PREDICTION_INTERVALS.md)：原十五场预测及 80% 区间、各自来源范围
- [精确预测数据](predictions-with-intervals.csv) / [精确分组数据](regime-summary.csv)
- [绘图与表格生成脚本](../../../paper/tools/render_eq_simple_preview.py)

浅灰柱表示原五次参考观测的均值；三种颜色仅表示先验臂。底部浅灰带是 180 个来源观测的合并范围，不是误差带，也不是每个世界各自的范围。全部参考均未提供给 agent。主图只显示单题解离分数的点预测；区间单独保留，没有删除或改分。

原 a 的对数浓度图和 b 的十五行区间图不再作为本版主图。既有文件保留，但它们不是这个方案的首屏。世界 3 MisIndexed 的偏离平台预测仍完整展示。先验优势反转的宏观结论由独立表格支撑，不能只凭单题图推断全部十二题的结果，也不能从图中归因内部锚定。

本目录最初只提供独立设计候选；后续按用户授权完成正文替换，英文配图PPT同步为同数据的可编辑柱图，中文沿用本目录批准图件。未产生新的模型或模拟器数据。

## 图注草稿

**Original predictions and withheld outcomes at the most dilute equilibrium test.** Bars show the original reference mean and the three agents' point predictions for the same recipe within each of five worlds (nominal concentration 13.3 µM). The pale horizontal band marks the pooled minimum-to-maximum dissociation range of all 180 final-assay source observations from the fifteen campaigns; it is not an uncertainty interval or a world-specific source range. The reference mean uses the original five evaluator observations and was withheld from the agents. Complete agent-issued 80% prediction intervals and campaign-specific source ranges are reported separately. The MisIndexed World 3 counterexample is retained. This single-response, single-query comparison is distinct from the three-response regime aggregates in the accompanying table.

## 重建

```powershell
uv run --no-sync python paper/tools/render_eq_simple_preview.py
```

输入为保留的 `EQ_AUTONOMOUS_PROCESS.json` 与 `STORY_WORLD_ANALYSIS.json`。脚本检查十五场、一百八十批、共享参考值和分组均值；无模型/模拟器调用。
