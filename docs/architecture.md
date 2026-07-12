# 系统如何工作

可以把 ChemWorld 想成一座分层实验室：世界层决定隐藏规律，交互层接收 Action 并返回公开观测，
评价层再把轨迹变成可以复查的结果。三层分别版本化，Agent 不需要读取内部状态，评分规则也不会
反过来修改环境。

## 先看全景

| 层 | 负责什么 | 不负责什么 |
| --- | --- | --- |
| World | 机理、物性、设备、场景、仪器与隐藏参数 | 方法排名和论文结论 |
| Interaction | Gym API、动作验证、campaign、公开观测和资源使用 | 读取 hidden truth |
| Evaluation | replay、任务主指标、约束、资源、公平性与统计 | 改变运行时物理 |

这种分离让 ChemWorld 同时成为测试环境和训练环境：Agent 可在公开 Train worlds 上训练，但 Bench
worlds、评价合同和私有参数保持不可见。只要 World 或 Evaluation 合同改变，就生成新版本证据，
不会用新评分解释旧轨迹。

## 代码与职责怎样分层

```text
Agent / Optimizer / CLI
          │
          ▼
Gymnasium API ── Task + Scenario contracts
          │
          ▼
Transactional Runtime
  validation → operation kernel → domain service → constitution → commit
          │
          ├── public observation + instruments
          ├── online learning reward
          └── trajectory + replay hashes
          │
          ▼
World + Physchem + Foundation
  mechanisms · reactors · phases · equipment · ledgers · model cards

Verified Evaluation
  replay · task objective · constraints · resources · paired statistics
```

| 包 | 对外职责 |
| --- | --- |
| `chemworld.envs` | Gymnasium 注册、reset/step 编排和稳定 observation space。 |
| `chemworld.tasks` | 可执行任务目标、预算、操作、仪器、成熟度和冻结合同。 |
| `chemworld.task_design` | 严肃任务的研究问题、指标对齐、泛化轴、证据与 readiness 审查。 |
| `chemworld.runtime` | 事务、操作路由、领域服务、回滚和记录。 |
| `chemworld.world` | 世界律、场景、操作卡、观测和评分合同。 |
| `chemworld.physchem` | 物性、平衡、反应器、分离、传递、仪器和安全模型。 |
| `chemworld.foundation` | ontology、typed state、单位、constitution 和协议接口。 |
| `chemworld.eval` / `data` | 运行、验证、分层指标、资源账本、trajectory 和 dataset。 |

## Agent 实际接触的接口

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=1)
observation, info = env.reset(seed=1)
observation, reward, terminated, truncated, info = env.step(action)
```

Agent 只依赖任务允许的 action、observation 和 `info`。hidden mechanism parameters、真实物种
账本以及私有评测条件不会通过公共观测泄漏。未观测值使用 `NaN`/`null` 与显式 mask，而不是
伪造为零。

## 一次 `env.step()` 发生了什么

1. action 被 canonicalize，并通过 schema、task 权限、payload 与前置条件校验；
2. operation kernel 选择任务所需的领域服务；
3. 服务调用版本化物理模型，生成 world event 与 state patch；
4. transaction manager 在临时状态上应用 patch；
5. physical constitution 检查物料、相、容器、设备、热量和过程账；
6. 检查通过才提交，否则回滚并返回可审计失败原因；
7. 独立 observation 与 scoring 服务生成可见结果、reward 和 final score；
8. recorder 写入操作、诊断、合同 hash、状态差异和成熟度。

这一事务边界保证失败动作不会留下半更新状态，也让 replay 可以逐步比较。

## 状态存在哪里

`WorldState` 使用 typed ledgers：

| Ledger | 记录内容 |
| --- | --- |
| Species | 物种 identity、组成、角色和公开标签。 |
| Phase | 各相组分量、体积、相型、选择与容器归属。 |
| Vessel | 容量、温度、压力和相引用。 |
| Equipment | 反应器、柱、结晶器、电化学池和仪器配置/诊断。 |
| Thermal | 外部热、反应热、热损失和能量闭合。 |
| Process | 时间、成本、风险、样品消耗和过程指标。 |

主物料状态由 phase/species ledger 管理；metadata 只保存非主状态的诊断与 provenance。
constitution 会审计聚合视图与单一事实源是否一致。

## Operation 怎样到达物理模块

Runtime 按能力拆分服务，而不是把所有逻辑放进 `env.step()`：

- 反应与热：共享 compiled mechanism 的 batch/CSTR/PFR 推进、热账和风险投影；
- 相与分离：相 ledger、活度修正萃取、TPD-style 诊断、洗涤和有界降级单元；
- 结晶：溶解度曲线、显式晶种、粒度群体平衡、固/液相和过滤；
- 蒸馏：VLE shortcut、馏分、能量和回收率；
- 连续流：几何解析 PFR、停留时间、压降、Reynolds 数和求解诊断；
- 电化学：电位/电流、传质、动力学、控制、双电层和能耗；
- 仪器：采样、成本、可见信号、处理结果与不确定度；
- 评分：严格根据任务 scoring contract 生成在线 reward 和最终榜单分数。

每个模块通过 model card 声明单位、适用域、失败模式、provenance 和成熟度。详见
[物理化学模型](physchem_core_design.md)和[模型成熟度](model_maturity.md)。

## 隐藏机理怎样形成不同世界

固定 seed 只能改变同一世界实例中的随机量，不足以证明 Agent 能适应不同机理。ChemWorld 将可干预
世界参数组织为机理族，例如分配本构关系、反应速率律、结晶动力学、蒸馏分离行为和流动拓扑。
每个干预都产生新的 mechanism hash，并保持公共任务语义不变。

正式训练/泛化实验需要在机理族层面冻结不重叠的 Train、Dev 和 Bench cells，同时校准扰动强度：
过弱的 shift 无法辨识泛化，过强的 shift 会把任务变成不可解。当前六个研究任务共有 9 种实际
可执行的机理/构成律模式，均通过 5 世界 × 5 配方的可辨识性、非灾难性和守恒校准。多 seed Agent
识别与迁移证据仍未完成。

## 结果怎样被评价

Evaluation 从只读轨迹产生独立结果层：终点目标、任务主指标、在线 shaping、风险/成本约束、
方法资源、有效性和交互能力。在线 reward 不能替代任务主指标，目标改善也不能覆盖约束退化。
完整主比较采用逐任务联合规则，不生成跨物理域混合总分。

交互能力分为 recipe-search、operation-open-loop 和 operation-closed-loop。跨层结果只能解释完整
系统能力；若要归因到算法，必须在同一交互层和信息合同下比较。评价还记录实际 adaptation source、
脚手架是否代办动作、外部模型调用、token、费用、训练步数和计算时间，这些诊断不被压进端点总分。

结果通过 trajectory digest 与 score/replay payload 绑定。评测器重新加载轨迹、执行 replay、重算
指标和约束，再生成 verified result；方法自报的 score 不进入可信链。

## 四个容易混淆的概念

```text
World Law  共享且版本化的物理/交互规则
Scenario   hidden parameters、初态、机制和随机种子
Task       目标、预算、允许操作/仪器、指标和可见策略
Campaign   agent 在 task/split/seeds 上的一次评测
Experiment campaign 中的一条完整实验流程
Operation  单步实验动作
```

`TaskSpec` 只描述环境能够执行什么；研究设计卡描述任务是否足以支撑科学比较。两者分离可避免
“已注册”被误解为“已验证”。准入检查覆盖指标实现、成熟度、seed 深度、决策预算、baseline、
泛化轴、证据和反作弊边界。

`single_experiment` 任务在合法 final assay 后结束 episode；`campaign` 任务可以在预算内完成
多次 experiment，适合 BO、LHS 或 world-model learner。

## 公开观测怎样变成可回放轨迹

仪器输出分为 `raw_signal`、`processed_estimate` 和 `uncertainty`。trajectory 还记录任务、
世界律、场景、机制、runtime profile、observation/scoring contract、maturity、操作前置条件、
constitution checks 和状态差异摘要。

`chemworld verify` 在同一合同下重新执行 trajectory，并拒绝 hash 漂移、非法动作、状态不一致
或分数篡改。评测层读取环境结果，不修改环境语义。

## 扩展系统时遵守什么

新增能力时应选择正确扩展点：

- 新任务：注册 task/scenario，不复制环境；
- 新操作：扩展 action schema、operation card、kernel 和服务；
- 新物理：增加 model card、独立 kernel、适用域与参考测试；
- 新仪器：增加 instrument contract、可见边界和 raw/processed/uncertainty 输出；
- 新 backend：保持相同输入输出合同，并公开 backend id 与 maturity。

任何会改变可观察物理或评分的修改都必须提升相应合同/世界律版本并重建冻结轨迹。
