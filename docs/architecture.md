# 系统架构

ChemWorld 把任务、物理模型、观测与评测组织为一个版本化虚拟世界。任务只是同一世界律的
不同切片，因此操作语义、守恒规则和轨迹合同不会因任务而暗中改变。

## 分层结构

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
          ├── observation + instruments
          ├── reward + final scoring
          └── trajectory + replay hashes
          │
          ▼
World + Physchem + Foundation
  mechanisms · reactors · phases · equipment · ledgers · model cards
```

| 包 | 对外职责 |
| --- | --- |
| `chemworld.envs` | Gymnasium 注册、reset/step 编排和稳定 observation space。 |
| `chemworld.tasks` | 任务目标、预算、操作、仪器、成熟度和冻结合同。 |
| `chemworld.runtime` | 事务、操作路由、领域服务、回滚和记录。 |
| `chemworld.world` | 世界律、场景、操作卡、观测和评分合同。 |
| `chemworld.physchem` | 物性、平衡、反应器、分离、传递、仪器和安全模型。 |
| `chemworld.foundation` | ontology、typed state、单位、constitution 和协议接口。 |
| `chemworld.eval` / `data` | 运行、验证、指标、leaderboard、trajectory 和 dataset。 |

## 公共交互合同

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

## 一次 step 如何执行

1. action 被 canonicalize，并通过 schema、task 权限、payload 与前置条件校验；
2. operation kernel 选择任务所需的领域服务；
3. 服务调用版本化物理模型，生成 world event 与 state patch；
4. transaction manager 在临时状态上应用 patch；
5. physical constitution 检查物料、相、容器、设备、热量和过程账；
6. 检查通过才提交，否则回滚并返回可审计失败原因；
7. 独立 observation 与 scoring 服务生成可见结果、reward 和 final score；
8. recorder 写入操作、诊断、合同 hash、状态差异和成熟度。

这一事务边界保证失败动作不会留下半更新状态，也让 replay 可以逐步比较。

## 状态与单一事实源

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

## 领域服务与物理模块

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

## World、Scenario、Task、Campaign

```text
World Law  共享且版本化的物理/交互规则
Scenario   hidden parameters、初态、机制和随机种子
Task       目标、预算、允许操作/仪器、指标和可见策略
Campaign   agent 在 task/split/seeds 上的一次评测
Experiment campaign 中的一条完整实验流程
Operation  单步实验动作
```

`single_experiment` 任务在合法 final assay 后结束 episode；`campaign` 任务可以在预算内完成
多次 experiment，适合 BO、LHS 或 world-model learner。

## 观测、轨迹与回放

仪器输出分为 `raw_signal`、`processed_estimate` 和 `uncertainty`。trajectory 还记录任务、
世界律、场景、机制、runtime profile、observation/scoring contract、maturity、操作前置条件、
constitution checks 和状态差异摘要。

`chemworld verify` 在同一合同下重新执行 trajectory，并拒绝 hash 漂移、非法动作、状态不一致
或分数篡改。评测层读取环境结果，不修改环境语义。

## 扩展原则

新增能力时应选择正确扩展点：

- 新任务：注册 task/scenario，不复制环境；
- 新操作：扩展 action schema、operation card、kernel 和服务；
- 新物理：增加 model card、独立 kernel、适用域与参考测试；
- 新仪器：增加 instrument contract、可见边界和 raw/processed/uncertainty 输出；
- 新 backend：保持相同输入输出合同，并公开 backend id 与 maturity。

任何会改变可观察物理或评分的修改都必须提升相应合同/世界律版本并重建冻结轨迹。
