# 事前指定相量和弱混合试验后建立局部关系，Q又采用未标定的长混合平衡假设

`repeat-02/PA-W04-B12-discovery-E-Opaque`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-02__PA-W04-B12-discovery-E-Opaque.json)

## 问题与先验

无物性资料；v1提出类别配对、相量和混合三项可检验假设，计划重复，但最终12批均为不同配方。前8批有交替保留水相/有机相，支持测量通道对应被保留的物料，而非把移除相读数近零当本征不存在。

## 预期与实验

v2/cursor80识别第一批体积与X0同时不同，先要求补一个标准S0/X0，再预言S0/X1相量增加会提高有机份额，1 s/100 rpm弱混合会低于标准300 s/800 rpm。第9批补X0；第10、11批相率0.134/0.413对应有机份额0.487/0.803；第12批弱混合0.646低于标准0.786。前后顺序明确，支持预期参与组织后续实验。

## 实际证据

第10、11批均采用溶剂/萃取剂等体积，表观分配系数约5.99；标准S0/X1二者比例不同，系数约4.44。v3正确将其限制为窄组成范围的相分配关系，没有宣称全局常数。S0四X标准份额0.659/0.786/0.700/0.812支持类别差异；跨S仅零散配对，不能分离交互与主效应。

## 修订

v3将类别和局部相量方向标为支持，混合也得到单次受控对照支持；但混合时间与转速共同变化，且无真正重复。正文所称‘标准强混合可能在平台’并未被更强条件检验。最终报告保留组成依赖、过程差异及质量闭合不完美等解释。

## 后续采用

Q采用S0/X0约3.2、S0/X3约6.8固定亲和度，并把900–1200 s强混合视为达到平衡，只对较弱混合小幅折扣；未测S2/X0和S2/X3也使用近似S0迁移。K2主动指出这些假定与报告保留意见的张力，且Q以名义相量替代此前要求的实测相率。D1选水相，说明最终行动没有把多数源实验有机相较多泛化为一律留有机相。

## 未解决问题及解释限制

这是有事前测试、形成局部关系、并意识到迁移边界的正向案例，同时展示边界知识未完全约束数值模型。K2提出同一容器先弱后强混合来区分传质与批次差异，尚未执行；不能因提出诊断实验就记为完成因果识别。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 80, 'last_event_id': 'runner-operation-0080'}

> A standardized S0/X0 batch is still needed because batch 1 used different volumes.

事件：runner-operation-0087

v3 / cursor {'event_count': 120, 'last_event_id': 'runner-operation-0120'}

> Scope is narrow:

事件：runner-operation-0097, runner-operation-0107

Q

> The 900–1200 s vigorous mixes were treated as effectively equilibrated

K2

> There are genuine tensions between the sealed report and predictions.
