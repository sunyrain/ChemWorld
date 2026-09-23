# ChemWorld NCS：严格学术风格配图预览

打开 `index.html`，每个 Figure 有 A–D 四版，共 20 张 imagegen 生成图。图中文字为英文。可选择每图一个版本，导出 JSON；可切换精确数据底图并下载 SVG。

## 交付内容

- `fig01-A.png` 至 `fig05-D.png`：最终 20 张生成预览。
- `reference/`：相同 20 个版式的 PNG 和可编辑 SVG，直接从既有分析数据绘制。
- `prompts.json`：内置 image_gen 的 20 次初始生成及 5 次修订提示词。
- `generation-records.json`：最终输出与来源对应关系。
- `render_reference.py`：底图绘图脚本；在本仓库内通过 `uv run --no-sync python output/imagegen/ncs-rigorous-20260922/render_reference.py` 运行。
- `build_gallery.py`：打包和文件验证脚本，不编辑生成图像。

## 使用界限

这些是选版预览，不是已经验证的投稿定量图。数据面板、逐场比较、配对线、图例和分母均以源数据底图为依据，imagegen 生成仍可能改变局部点位、刻度间距、重叠标记或字形。正式投稿应从数据生成最终矢量图，不能把生成位图直接作为数值证据。没有运行新实验，也没有替换任何稿件或论文原图。

已检查 20 张生成图的风格和整体构成；修正 Figure 2A 的 W01 图例、Figure 2D 的填充标签、Figure 5A 的 12 次预算图例、Figure 5B 横向排版、Figure 5D 脚注。Figure 5A 修订后 MisIndexed 图例仍有一个多余圆点，属于预览层排版瑕疵；SVG 中没有这个问题。高密度面板的单个标记不保证由 imagegen 完整复现。

## 图的组织

1. 平台、三臂、自主实验及封存后测的流程。
2. EC / RX 优化表现与预测能力的配对关系。
3. EC / PA / C 的 12 与 24 次预算比较。
4. EQ 查询条件变化及 C 响应间权衡。
5. C 四响应与同场公开观测均值基线的比较。

## 科学内容来源

- `paper/venues/ncs/article.md`
- `paper/figures/integrated-results/analysis.json`
- `paper/figures/integrated-results/campaign_metrics.csv`
- `workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921/STORY_WORLD_ANALYSIS.json`
- `workstreams/flagship_tasks/reports/work-ii-c-formal-20260920-v3-auto/BASELINE_REANALYSIS.json`

底图脚本验证 EC / RX 各 30 个目标配对、每个预算面板 15 个配对、C 基线胜出数 26 / 0 / 4 / 21。所有展示均来自已有证据；没有新增因果结论或显著性标记。
