# 隐藏机理与世界族

Mechanism contract 决定一个世界内部真正遵守的反应、相行为、设备参数和观测映射。Agent 看不到
这些隐藏参数，只能通过实验推断；运行时则用它们执行操作，并把摘要绑定进 replay 身份。

## 一个 Mechanism 包含什么

一个 mechanism 可包含：

- species identity、角色与守恒组成；
- reaction steps、stoichiometry 和 rate-law family；
- thermodynamic、phase 或 partition constitutive family；
- crystallization、distillation、flow 或 electrochemical 参数；
- instrument mapping、noise 和披露策略；
- safety/cost 参数与适用域；
- model provenance、maturity 和版本摘要。

隐藏字段不向 Agent 公开，但必须足以初始化 ledger、执行 operation、生成观测并确定性 replay。

## 怎样编译并绑定身份

Compiler 将声明式 mechanism 转为 runtime kernels、初始 ledger 和 instrument models。canonical
内容生成 SHA-256；scenario、trajectory 和 verified result 都绑定该 digest。编译失败、未知模型、
单位不一致或守恒不成立时必须 fail closed。

## 怎样构造不同世界族

同一任务可以在保持公共 action/observation schema 不变的前提下改变隐藏机理族，例如：

- 结晶前反应、蒸馏前反应和连续流反应的速率律或网络拓扑；
- 分配任务的活度修正构成律指数；
- 电化学任务的标准电位、传递系数与过电位—选择性响应；
- 平衡任务的活度系数比与电荷平衡响应。

每个干预产生独立 opaque digest。公开轨迹只披露版本与 hash；维护者回放需要另行提供精确干预
上下文，缺失或篡改时失败关闭。正式泛化实验按机理族划分 Train、Dev 和 Bench，而不是只换随机
seed。

## 当前已经验证了什么

六个研究任务都已有实际 provider 消费的机理或构成律族。控制审计使用 5 个世界和 5 个固定探针配方，
共检查 9 个任务—模式组合。全部组合满足确定性、固定探针下的局部响应分离、90 分位响应不过强和
质量守恒要求。这些阈值只证明干预可执行且不会被固定探针完全淹没，不证明候选 family 在相同动作、
测量和实验预算下可识别，也不应解释为真实化学常数或物理精度验证。冻结候选版已将电化学
`solvent` 与 `electrolyte_profile` 都变为公开可选的反事实坐标，并移除了 Agent 可见消息中的世界/机理
身份字段。RC20 动作—干预设计审计与控制匹配可识别性证书已通过；在线策略可行证书总体达到
227/240，但反应催化剂映射反事实仅识别 22/30，未满足逐 family 规则，因此 Gate A 整体仍为 false。

## Agent 能看到什么

Agent 可以获得任务目标、合法操作、公开材料标签、测量结果和必要约束；不能获得隐藏 species amount、
rate constant、partition coefficient、机理族标签、私有扰动幅度或 debug truth。解释模型可提出假设，
但评价只依据其公开证据和后续决策，不把接近隐藏答案的文字当作唯一得分。

## 回放如何发现机理漂移

Replay 使用相同 world law、mechanism、scenario、seed、精确干预上下文和 action sequence。结果漂移时，验证器会检查
随机流、浮点容忍、transaction、instrument noise、合同 hash 和 runtime provider。机理可执行并不
代表 Agent 已学会识别它；正式机制适应主张还需要不重叠的 family 分配、Agent 识别指标和未见
family 迁移评测。

模型成熟度见[模型成熟度](model_maturity.md)，整体分层见[系统架构](architecture.md)。
