# 前瞻混合对照撤回标准条件饱和解释，但预测仍拆分未识别的时速响应

`repeat-03/PA-W01-B12-discovery-E-MisIndexed`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-03__PA-W01-B12-discovery-E-MisIndexed.json)

## 问题与先验

错配资料提示S2/X0，前七批形成以该组合为中心的稀疏交叉。实测S3X0与S2X3高于资料偏好的S2X0，v2承认边际排序未决定实测配对排序。

## 预期与实验

v2/cursor70明确预告弱5s100rpm低于强600s1000rpm，若一致才考虑饱和或未解决；后续先重复基线并保留水相，再变X体积，最后弱/强混合。

## 实际证据

基线有机0.269/0.282，弱0.272、强0.391；低/高X量0.167/0.487。D约低与基线1.9—2.0、高1.34，恒D不足；保留水相HPLC0.694→终检0.748仅支持近似闭合。

## 修订

v3明确标准120s500rpm未饱和，并保留强端平台未知及时间转速混杂。这是预期—实验—修订真实闭环。K1把材料差异解释为配对作用，但此稀疏设计本身不能证明不可加交互。

## 后续采用

Q延续混合增强方向，同时给出未独立测过的时间/速度组合点值；未测S0X3仍借资料得到D2 Q06。Q承认源实验额外reagent而查询没有的差异。K2准确指出这些是无真值反馈的建模假设，提出同容器递增混合但未执行。

## 未解决问题及解释限制

不能把事后K2的反思当作已经完成新检验，也不能把弱与强差异误写为时长的独立因果效应。局部平台否定与迁移模型未识别可以在同一研究并存。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 70, 'last_event_id': 'runner-operation-0070'}

> a very weak mix (5 s, 100 rpm) is predicted to give less organic transfer than an intense mix (600 s, 1000 rpm).

事件：runner-operation-0107, runner-operation-0117

v3 / cursor {'event_count': 120, 'last_event_id': 'runner-operation-0120'}

> equilibration was not saturated at 120 s/500 rpm in this scope

K2

> These are prospective modeling assumptions made without truth feedback, not contemporaneously validated campaign findings.
