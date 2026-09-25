# 中文整稿配图

这组图依据远端 `74c9303295762888594390640bf696f5645f1679` 新增的中文稿全文制作，插入[中文正文](../../venues/ncs/archive/ChemWorld_NCS_中文正文_v1.md)。正文保留原有科学内容，替换图件占位、加入两个案例引入段并接入既有参考文献和完整补充材料。2026-09-22 重构图 3 后，此图及对应图注也已同步至英文 NCS 稿。

| 图 | 读者需要理解的问题 | 制作方式 |
| --- | --- | --- |
| 1 | 自主实验、持久状态与分离评价如何连接 | Imagegen 框架示意 |
| 2 | 更好的操作交付是否等于更准确的预测 | EC/RX 匹配差值与纯化约束散点 |
| 3 | 更多研究资源改善哪些端点 | 绝对均值和改善场数 + 按世界/信息臂逐行展示的有向配对变化；6 列共 90 个响应配对 |
| 4 | 两种预算如何形成不同实验路径与推荐 | 保留轨迹驱动的 Imagegen 案例示意 |
| 5 | 先验信息何时有用、何时反转 | EQ/P 区间分组与结晶联合响应 |
| 6 | 应保持的关系与应修订的关系如何判断 | 公开均值参考、纯度分布与概念图 |
| 7 | 原研究者如何预测、反思和提出后续实验 | 保留 Q/K2 驱动的 Imagegen 案例示意 |
| S1 | 基础设施有哪些层次、资格验证覆盖什么 | Matplotlib 矢量结构图 |
| S2 | 所有研究块的先验结果如何分布 | 既有补充材料的完整先验总览 |

## 数据和边界

- 统计图由[绘图脚本](../../tools/render_ncs_full_figures.py)从保留结果生成，同时提供矢量 PDF 和 PNG；[数值摘要](figure-data-summary.json)记录精确分母和图中统计。
- 图 3 的[独立绘图入口](../../tools/render_ncs_budget.py)去除交叉连线，统一向右为改善；另提供可编辑 SVG、[逐配对数据](figure03-research-envelope-pairs.csv)及[表示规则](figure03-research-envelope-design.json)。C 的三个响应复用相同会话，90 个配对变化不是 90 个独立研究样本。其核心数值与重绘前逐项一致；英文和中文 NCS 正文共用此图。
- 绘图输入为 `paper/figures/integrated-results/analysis.json`、`campaign_metrics.csv`、`paper/figures/venue-results/c_response_pairs.csv`，以及已有 `STORY_WORLD_ANALYSIS.json` 与结晶 `BASELINE_REANALYSIS.json`。这些是本轮之前保留的结果，不含新实验。
- 图 4/7 使用同一结晶世界、Aligned 信息下两场独立会话；24 批次不是 12 批次的续跑。两张图是回顾性案例，不能代替总体预算效应。
- 图 4 星号标注的即时考虑为示意重构，原始日志未记录即时决策理由。图 7 为原会话 Q/K2 的压缩转述；K2 未获参考反馈、不能修改封存 Q，后续实验提议未执行。评价器参考只对应已列出的盲测题。
- 图 6 的保持/修订图是概念性综合，不是额外实验或全体会话的象限频率。
- 平台资格统计与 240 场 agent 研究分开；本轮不产生新科学数据。

## 示意图制作记录

- [图 1 提示词与校正](../../../output/imagegen/ncs-full-figure1-framework-prompt.txt)
- [图 4 提示词](../../../output/imagegen/c-w05-split-a-research-v10-prompt.txt)
- [图 7 提示词](../../../output/imagegen/c-w05-split-b-posttest-v10-prompt.txt)
- [案例数据来源与完整图注说明](../../../output/imagegen/c-w05-split-v10-layout-and-captions.md)

## 重建

在仓库根目录运行：

```powershell
uv run --no-sync python paper/tools/render_ncs_full_figures.py
uv run --no-sync python paper/tools/build_ncs_chinese.py
```

构建需要 Pandoc、XeLaTeX、BibTeX、Poppler，以及模板指定的中文字体。示意图 PNG 为已保留资产；上述命令不会再次调用 Imagegen。

输出为 `output/pdf/archive/ncs/chemworld-ncs-zh-full.pdf`，包含中文正文、方法、参考文献、扩展图和既有英文完整补充材料。[构建摘要](../../venues/ncs/CHINESE_BUILD_SUMMARY.json)记录页数、缺字/引用/溢出检查；临时目录中的逐页 PNG 用于视觉复核。

图 3 重构后的最新阅读版本为[中文 PDF](../../../output/pdf/archive/ncs/chemworld-ncs-zh-budget-redesign.pdf)（29 页）及[英文 PDF](../../../output/pdf/archive/ncs/chemworld-ncs-article-budget-redesign.pdf)（24 页）。原 PDF 被阅读器占用，本次用构建脚本的 `--output` 参数保存为独立文件；默认输出路径不变。单图提供 [PNG](figure03-research-envelope.png)、[SVG](figure03-research-envelope.svg) 与[矢量 PDF](figure03-research-envelope.pdf)。
