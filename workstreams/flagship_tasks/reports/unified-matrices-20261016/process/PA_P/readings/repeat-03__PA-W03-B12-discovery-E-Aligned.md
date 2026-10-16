# 中途安排强化检验后限定混合结论，未测材料比较保留不确定

`repeat-03/PA-W03-B12-discovery-E-Aligned`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-03__PA-W03-B12-discovery-E-Aligned.json)

## 问题与先验

边际资料引向S2/X3，但初始对角筛选不能唯一识别配对交互。标准S2/X3多次测量形成局部锚点，相量和混合成为后段问题。

## 预期与实验

v2/cursor90追述短混合前的预测时，弱混合批9实际上已经完成，不能算同期事前承诺；同版要求检验中等与强混合，确实先于批10/11。

## 实际证据

标准S2/X3有机0.282/0.269/0.312；高X量0.486、低X量0.147。弱混合0.251、中等0.279、强混合0.387，因此强化条件高于标准散布，但时间与转速共同变化。最后保留水相后有机库存降至0.0039，最终回收为0，不能把HPLC库存直接替换为终态回收。

## 修订

v3保留混合强度相关的局部增量，同时明确尚未证明平台或排除更剧烈混合的分离问题。K1区分配对依赖与交互未识别，避免用边际排名充当完整规律。

## 后续采用

Q的D2仍为uncertain，未测S0/X3与S2/X0依靠边际外推。定量部分把名义萃取剂量/总加液当核心相量预测因子；K2指出这与初始相液和实际体积的限制存在张力。K2提出重复强混合并比较300/3600s静置，属于尚未执行的后续检验。

## 未解决问题及解释限制

体积、混合均有真实局部证据，但全配对外推、名义相量近似及独立时间/转速效应尚不充分。宽区间及不确定决策不能被忽略，也不能把所有未直接采样的点预测一概判为错误。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 90, 'last_event_id': 'runner-operation-0090'}

> Test intermediate and vigorous conditions before claiming an effect.

事件：runner-operation-0097, runner-operation-0107

v3 / cursor {'event_count': 120, 'last_event_id': 'runner-operation-0120'}

> no evidence establishes a plateau or rules out very-vigorous separation problems.

Q

> I treated extractant volume divided by total liquid added as the central phase-ratio predictor

K2

> The Q05-versus-Q06 decision was appropriately left uncertain.
