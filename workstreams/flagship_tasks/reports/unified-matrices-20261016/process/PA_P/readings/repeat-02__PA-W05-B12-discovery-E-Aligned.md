# 筛选把探索从边际有利S2/X2转向实测S0/X3，后续相量与混合检验形成有范围的关系

`repeat-02/PA-W05-B12-discovery-E-Aligned`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-02__PA-W05-B12-discovery-E-Aligned.json)

## 问题与先验

正确资料提示S2与X2/X3，但仅给边际信息；八个标准配对中S2/X2有机份额0.187，S0/X0为0.152，S0/X3为0.314最高。不能称资料被证伪，因为其未给配对排序；可见的是资料无法确定的关系通过选择配对而显现。

## 预期与实验

v2/cursor80明确将剩余四批用于S0/X3低高相量与弱强混合。固定总添加液体约0.10 L、改变X为0.01/0.02/0.04 L，份额0.183/0.314/0.560；混合10 s/100 rpm、300 s/600 rpm、1200 s/1200 rpm为0.267/0.314/0.399，符合总体方向但未建立平台。

## 实际证据

对应相量表观D约2.22/1.64/1.80，形成近似分配关系并限定为插值。相量改变保持溶剂/水等体积，却改变其相对X的组成；不能只归因于几何。一次保留水相S1/X1使前段0.787水相对应末端0.767，其他有机保留也大体对应，支持物料语义。

## 修订

v3从初始体积不变D及平台模型缩窄为近似关系和平台未识别。K1将S0/X3成为研究锚点描述为实验补充边际资料，且保留稀疏配对、无重复、时间速度混杂等问题。真正正向过程是未知配对观察→后续定向试验→局部定量模型，尚未识别普遍化学机理。

## 后续采用

Q以直接测过的S0/X3相量/混合序列回答Q03/04/06，选择Q06相对Q05也有S0内X0/X3对照依据，比完全未测配对的决定更有支持；但强混合与新相量的共同迁移仍未验证。未测S2/X0、S2/X3则依赖资料并给宽区间，K2指出共同混合修正超出范围。

## 未解决问题及解释限制

只有一批/配方，没有独立批间方差；相量和混合函数无法从三点唯一确定。K2提出1200 s/600 rpm缺角实验尚未执行。强混合趋向平衡是候选解释，不能等同于已经测到平衡。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 80, 'last_event_id': 'runner-operation-0080'}

> For a fixed S0–X3 pairing, increasing extractant/organic phase amount should increase phase ratio and organic inventory fraction

事件：runner-operation-0087, runner-operation-0097

v3 / cursor {'event_count': 120, 'last_event_id': 'runner-operation-0120'}

> The model should be used for bounded interpolation, not extrapolation.

Q

> X3 produced much greater organic transfer than X0 with S0, making Q06 the supported choice over Q05.
