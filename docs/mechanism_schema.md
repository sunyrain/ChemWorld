# Mechanism 协议

Mechanism contract 把隐藏世界中的物种、反应、本构关系、设备参数和观测映射编译为可执行 runtime。
它既是 replay 身份的一部分，也是 Train/Dev/Bench 世界族的基本单位。

## 合同内容

一个 mechanism 可包含：

- species identity、角色与守恒组成；
- reaction steps、stoichiometry 和 rate-law family；
- thermodynamic、phase 或 partition constitutive family；
- crystallization、distillation、flow 或 electrochemical 参数；
- instrument mapping、noise 和披露策略；
- safety/cost 参数与适用域；
- model provenance、maturity 和版本摘要。

隐藏字段不向 Agent 公开，但必须足以初始化 ledger、执行 operation、生成观测并确定性 replay。

## 编译与身份

Compiler 将声明式 mechanism 转为 runtime kernels、初始 ledger 和 instrument models。canonical
内容生成 SHA-256；scenario、trajectory 和 verified result 都绑定该 digest。编译失败、未知模型、
单位不一致或守恒不成立时必须 fail closed。

## 机理族干预

同一任务可以在保持公共 action/observation schema 不变的前提下改变隐藏机理族，例如：

- 反应速率律或网络拓扑；
- 分配本构指数与相选择行为；
- 成核/生长动力学；
- 蒸馏相对挥发度或设备约束；
- 流动反应的速率与传递轴。

每个干预产生独立 mechanism digest，并记录父机制、干预轴和强度。正式泛化实验按机理族划分
Train、Dev 和 Bench，而不是只换随机 seed。

## Public 与 hidden 边界

Agent 可以获得任务目标、合法操作、公开材料标签、测量结果和必要约束；不能获得隐藏 species amount、
rate constant、partition coefficient、机理族标签、私有扰动幅度或 debug truth。解释模型可提出假设，
但评价只依据其公开证据和后续决策，不把接近隐藏答案的文字当作唯一得分。

## 回放与证据

Replay 使用相同 world law、mechanism、scenario、seed 和 action sequence。结果漂移时，验证器会检查
随机流、浮点容忍、transaction、instrument noise、合同 hash 和 runtime provider。机理可执行并不
代表 Agent 已学会识别它；正式机制适应主张还需要多 seed、强度校准和未见 family 评测。

模型成熟度见[模型成熟度](model_maturity.md)，整体分层见[系统架构](architecture.md)。
