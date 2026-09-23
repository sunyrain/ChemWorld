# NCS 主图概念预览 · 20 张

基于 `paper/venues/ncs/article.md`，5 张主图 × 每图 4 个独立生成方案。使用内置 image_gen；修订亦使用 image_gen。原稿和原图未替换。

打开 [index.html](index.html) 进行放大比较、选择和导出选择记录。编号如 F1-B、F4-D。所有 PNG 与画廊同目录，支持离线浏览。

## 四个方向

- A：统计网格、清晰比较、低装饰。
- B：科学装置与图谱、化学语境、实验与证据相连。
- C：编辑式叙事、主结论突出、纵向／不对称布局。
- D：技术结构、镜像／分层／证据矩阵。

## 优先参考

| 主图 | 优先参考 | 选择理由 |
|---|---|---|
| Figure 1：可控世界与自主研究流程 | B | 装置图谱最能建立 ChemWorld 的化学语境；A 更适合精简后的方法总览。 |
| Figure 2：任务表现不等于预测知识 | D | 镜像结构清楚区分两类收益；B 的实验装置视觉更鲜明。 |
| Figure 3：增加预算的收益具有选择性 | C | 纵向结构最便于递进阅读；D 适合突出覆盖率与不确定性。 |
| Figure 4：先验效果随条件和响应反转 | D | 具体案例与总体结果结合；C 更有主结论的视觉力度。 |
| Figure 5：同一批证据，不同的利用效果 | B | 证据分流结构清晰；A 和 D 更适合作为精确统计图的重绘基础。 |

## 使用边界

这些是供选视觉方向的生成式栅格预览，不是定量图终稿。虽然提示使用已核实的数字且已进行一轮视觉与文字修订，图中仍可能存在刻度、比例、字间距与术语问题。最终投稿图应从正式分析数据重新绘制坐标、点、线、柱和文本。不要从生成图反推数值，也不要直接替换论文图。

- 12／24 批为独立会话与不同资源包，不是同一轨迹续跑。
- EQ 的 9／3 指题目分组；5／5 才是世界数。该分组是探索性分析。
- C 的反应量对比是各自的预测误差；不是回收率或纯度本身升降。
- 公共观测均值基线只用同一会话的数据，不增加实验，也不访问私有规律。
- 六类装置是本轮研究覆盖的体系；不能据此把平台的九类支持范围改写为六类。
- 原论文中不同系统、不同响应的成功与失败均应保留，不把这组图解读为普遍失败证明。

## 各候选的精绘注意事项

### F1-A

[打开图片](fig01-A.png) · Swiss workflow

方法图参考。顶端任务生成、资源和评分的具体边界仍需与正式方法段逐项对齐。

### F1-B

[打开图片](fig01-B.png) · Scientific atlas

推荐构图。装置是系统示意，不代表真实湿实验验证；六类是本轮研究覆盖的体系。

### F1-C

[打开图片](fig01-C.png) · Editorial synthesis

循环与后测已分开。最终精绘可将 Opaque 的模糊文档换为清晰的中性编号，避免暗示观测质量下降。

### F1-D

[打开图片](fig01-D.png) · Technical architecture

架构构图参考；少数字样仍需改：Evolution-only → Evaluator-only，three states → three arms，exams → arms。删去未定义的硬件与时间措辞。

### F2-A

[打开图片](fig02-A.png) · Swiss outcome bars

读数以明确的计数为准；右上预测曲线仅为概念插图，不是经验拟合曲线。

### F2-B

[打开图片](fig02-B.png) · Scientific paired pathways

体系插图与双读出适合保留。精绘时应把 Optimization & discovery 改为 Optimization versus discovery，并补齐配对分母说明。

### F2-C

[打开图片](fig02-C.png) · Editorial discordance

大数字布局。条形长度为生成预览，最终按计数精确重绘；计数不能作为独立类别相加。

### F2-D

[打开图片](fig02-D.png) · Mirrored evidence ledger

推荐结构。两侧均为正向计数，不是正负效应大小；精绘时删除底部过强的普遍化概括。

### F3-A

[打开图片](fig03-A.png) · Swiss slopes

简洁统计版。线连接两个预算组的均值，不代表同一次会话继续运行。

### F3-B

[打开图片](fig03-B.png) · Scientific response atlas

区间宽度与 MAE 已区分。装置与小图比例适合选样；柱高和刻度须数据重绘。

### F3-C

[打开图片](fig03-C.png) · Editorial budget ladder

推荐叙事。每条线表达各自响应的变化，不可跨行比较斜率大小；两个预算为独立会话。

### F3-D

[打开图片](fig03-D.png) · Precision and coverage

突出覆盖率。PA 超过名义覆盖率不能直接等同于完美校准；应与区间宽度并读。

### F4-A

[打开图片](fig04-A.png) · Swiss regime reversal

精确统计构图。EQ 上方两图刻度不同，最终必须保留清楚的轴说明。

### F4-B

[打开图片](fig04-B.png) · Scientific regime atlas

仅选图谱／布局；上部共享横轴仍有原点错位，必须拆成独立原点后数据重绘。晶格插图仅示意，不是推断出的真实结构。

### F4-C

[打开图片](fig04-C.png) · Editorial five-world reversal

反转叙事清楚。下部数值是预测 MAE，不是回收率或纯度本身；结晶对比限定为 12 批。

### F4-D

[打开图片](fig04-D.png) · Selected-case diagnostic

推荐案例构图。区间为该次预测的报告区间；9／3 是题目数，5／5 是世界数。最终修复英文词间距。

### F5-A

[打开图片](fig05-A.png) · Swiss same-data benchmarks

可作为定量精绘基础。各响应使用独立刻度，不能把跨响应 MAE 直接相加或比较绝对大小。

### F5-B

[打开图片](fig05-B.png) · Scientific evidence fork

推荐构图。基线只用同一会话的实验观测；笔记、瓶子和神经网络为概念示意。

### F5-C

[打开图片](fig05-C.png) · Editorial purity puzzle

无依据的区间线已去掉。335／360 是预测条目，不是 360 个独立世界；约 0.985 不是精确总体均值。

### F5-D

[打开图片](fig05-D.png) · Technical response map

结构适合精绘；所有哑铃应水平、端点按数据定位，不赋予纵向位置含义。请将纯度 24 批 Agent 读数统一为 0.03679。

## 文件

- `fig01-A.png` 至 `fig05-D.png`：20 张候选。
- `index.html`：离线选图画廊。
- `deliverables.json`：设计提示、图片来源和已执行修订。
- `prompts.json`：最初的 20 个设计提示。
- `generation-log.json`：初版与修订计划；未执行条目不代表已完成修改。
- `ncs-concepts-20.zip`：图片、画廊、说明及提示的打包副本。

2026-09-21。所有文件是视觉探索产物，不产生新实验结果。

