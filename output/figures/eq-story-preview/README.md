# EQ 图：从实验事实进入预测失效

**设计状态：本版已被用户否定为仍然难读。** 后续候选改为[单一预测对照图与独立表格](../eq-simple-preview/README.md)；本目录保留设计过程及原有数值，不作为推荐展示入口。

2026-09-23。用户指出原图虽然展示了误差、覆盖率与五世界预测，但读者仍不清楚它在解释什么。本目录提供一版独立讨论预览；没有替换正在整合的稿件、PPT 或现有图件，没有产生新实验数据。

## 核心判断

旧图按指标排序，缺少“研究中观察到了什么、盲测改变了什么”的入口。读者先看到抽象 MAE，再面对五套微小坐标轴，需要自行理解灰条、参考线和预测点之间的关系。上排是三响应宏观指标，下排却是最稀单题的解离分数，范围切换也没有充分突出。

建议围绕一个论点组织：**在这组 EQ 自主研究中，先验信息的预测优势依赖测试条件；已观察到的平台在极稀条件下不再成立，而不同先验臂给出了不同的外推。**

## 三个面板

1. **a：先让读者看见实验对象。** 用世界 2 的 36 个真实终态观测，展示名义浓度与解离分数。另绘最稀三题的评价器参考均值；明确其未提供给 agent。只画实测点，不拟造连续真实响应曲线或转折位置。世界 2 是说明性案例，不代表额外的总体统计。
2. **b：展示所有世界的具体预测。** 将五个小坐标轴合为一个共享百分比坐标轴，每世界三行。保留全部十五个最稀题预测、原 80% 区间、各会话来源观测范围和对应世界的参考均值。世界 3 MisIndexed 的混合解释反例保留。
3. **c：用紧凑数值表支持总体结论。** 保留三臂在两类题目上的原始平均 MAE 与覆盖率，直接说明 Aligned 在其余九题较 Opaque 的平均误差低约 54%，在最稀三题则约为 8.7 倍；两种方向均发生于全部五世界。原逐世界误差/覆盖率散点图可留在补充材料，不必占据主图首屏。

灰色来源条、黑色参考线和彩色预测有不同的信息地位。颜色仅代表先验臂，不能同时当作正确/错误编码。a/b 的百分比是解离分数；c 的 MAE 是三个响应的宏观汇总，不可混成同一指标。

## 解释边界

- 15/15 会话、180/180 来源批次均没有达到最稀三题的名义浓度。这表明存在观测覆盖缺口，不能宣称仅凭当前图已经排除了任务困难或证据不足。
- 先验条件包含自主取证与最终解释的全流程影响；该图不证明内部锚定或某个推理步骤的因果机制。
- 其余九题包含边界条件，不能统称为“分布内/插值”。分组为既有事后分析。
- 五个世界共享底层结构。覆盖率的多个响应、问题和观测不等于独立世界。每臂稀释组三响应共 225 个覆盖判断，其余九题共 675 个。
- Q 在 K1 之后，保留原研究上下文。不能将 Q 才明确的低浓度外推倒记为 K1 已经完成的机制发现。

## 预览、数据与重建

- [PNG](eq-evidence-to-prediction.png)
- [可编辑 SVG](eq-evidence-to-prediction.svg)
- [逐会话预测](predictions.csv)
- [检查及汇总数值](summary.json)
- [绘图脚本](../../../paper/tools/render_eq_story_preview.py)
- [原自主过程摘要](../../../workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921/EQ_AUTONOMOUS_PROCESS.json)
- [原世界分组分析](../../../workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921/STORY_WORLD_ANALYSIS.json)

```powershell
uv run --no-sync python paper/tools/render_eq_story_preview.py
```

脚本检查 15 场/180 批覆盖、六组汇总与逐世界均值一致，以及五世界改善/恶化方向；不调用模型或模拟器。

## 英文图注草稿

**Observed equilibrium plateaus and predictions under strong dilution.**
a, Final-assay dissociation from all 36 source batches in a selected matched world (World 2), plotted against nominal recipe concentration. Black diamonds show the original evaluator reference means for the three most dilute test recipes; these references were withheld from the agents. No continuous response curve is fitted. None of the 180 source batches across all fifteen campaigns reaches these three test concentrations.
b, All fifteen original-session predictions at the most dilute recipe, with their 80% prediction intervals. Grey segments show each campaign's observed source-response range; black vertical lines mark the world-specific evaluator reference mean. The MisIndexed World 3 departure from the plateau is retained.
c, Original mean macro MAE and interval coverage over five worlds per arm. Unlike a and b, these aggregate all three response targets. Relative to Opaque, Aligned has lower MAE on the other nine queries and higher MAE on the dilute three in each world. The concentration grouping is exploratory; the other nine queries are not all interpolation. These contrasts describe the complete autonomous research and prediction process and do not identify an internal causal reasoning mechanism.
