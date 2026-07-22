# Benchmark 设计

> **怎样判断一个 Agent 真正学会了实验，而不是只在固定世界中拿到高分？**

ChemWorld Bench 不把所有任务压成一个排行榜。它用分开的任务指标、约束、资源和适应实验回答：
方法在什么条件下有效，付出了什么代价，规律变化后能否恢复。

## 主要科学问题

固定世界（IID）性能是否能够预测 Agent 在未见机制、构成律、设备边界或独立后端上的适应？如果
不能，哪些训练世界、记忆和世界模型设计能够减少恢复所需的实验数量？

## 三个评测单位

```text
Campaign  一次 task × world × seed × method 运行
└── Experiment  从新鲜初态到合法终检的完整实验
    └── Operation  一次投料、控制、测量或分离动作
```

Campaign Track 主要比较完整实验数；Procedure 与 Control Track 还需要记录操作数、控制频率和
测量资源。

每个 Campaign 对应一个规范评测单元：

```text
Task × Scenario × Agent × Seed
```

Task 是公开且稳定的合同；World 是隐藏规律实例；Scenario 再加入初态、干预、reset、反馈条件与 seed。
这些对象不能继续用 task、environment、instance 或 episode 互相代替。

## 三种套件角色

| 套件 | 回答什么 | 当前边界 |
| --- | --- | --- |
| Core | 冻结范围内的正式方法比较 | v0.4 四任务，method freeze 尚未通过 |
| Diagnostic | 可识别性、反馈利用、反事实、适应与自治归因 | 旧 Gate A 已失效；控制匹配与在线策略证书待重跑 |
| Extended | 环境覆盖、训练、教学和方法开发 | 不自动获得正式排名主张 |

## 每个任务保留自己的结果

结晶、分配和连续流的主指标具有不同含义与单位。ChemWorld 不把它们直接平均成“总智能分”。每个
任务分别报告：

- 主指标与最小有意义效应；
- best-so-far 和预算—收益曲线；
- 完整实验成功、失败与未完成情况；
- 对应的风险、成本和资源。

## 高目标值不能抵消约束

一次比较至少保留六条轴：

| 轴 | 需要回答什么 |
| --- | --- |
| 任务目标 | 方法是否产生实质而非微小改善 |
| 风险与合法性 | 是否增加风险超限、无效或非法动作 |
| 实验与测量成本 | 改善是否来自更多、更贵的实验 |
| 适应速度 | 世界变化后多少次实验恢复 |
| 信息效率 | 哪些测量真正减少不确定性或 regret |
| 方法资源 | 训练步、GPU/CPU、token、费用和延迟 |

完整主张只在预先写下的目标、约束、资源、公平性和轨迹门禁共同成立时通过。

## 泛化不是一个单一 Split

| 变化轴 | 回答的问题 |
| --- | --- |
| 新 seed | 对实例随机性是否稳健 |
| 参数外推 | 能否离开训练范围 |
| 新 mechanism family | 能否识别因果规律变化 |
| 独立 backend | 排名是否依赖实现特有捷径 |
| 真实数据 / 物理 Bridge | 虚拟训练是否减少现实适应成本 |

这些证据不能互相替代。尤其是多 seed 稳健不等于机制迁移，模拟器间稳定也不等于现实有效。

## 适应需要自己的指标

- **Change detection**：Agent 是否发现旧模型已经失效；
- **Identification**：能否区分预注册的世界变化轴；
- **Recovery experiments**：恢复到目标水平需要多少次实验；
- **Adaptation regret**：变化后相对逐世界 reference 的累计损失；
- **Transfer advantage**：相同预算下，预训练相对从零开始的收益；
- **Constraint cost during adaptation**：恢复过程是否以更多风险换速度。

机制理解还需要分开三层证据：Agent 声明了什么（Declared）、能否预测未执行干预（Predictive）、
以及判断是否改变实验并改善结果（Actionable）。当前 v0.2.1 主要覆盖声明与行动诊断；独立预测探针
属于后续协议，不能由机制标签准确率替代。

## 反馈和评价不能混成一个 outcome

Trajectory v0.2 分别记录 `environment_outcome`、`agent_visible_observation` 和 `evaluation_outcome`。
反馈置换、延迟或删除只能改变 Agent 可见层；环境真实结果与评价真实结果保持配对固定。局部前缀测试
回答反馈是否改变行为，完整 campaign 测试回答这种改变是否改善任务结果，两者不合并成一个指标。

## 不同 Agent Track 分开报告

Campaign Design、Procedure Execution 与 Process Control 使用不同决策粒度。系统级结果可以并列，
但算法比较需固定相同 Track、公开信息和资源合同。详见[选择交互层级](agent_tracks.md)。

## Private Eval 怎样工作

评测端持有隐藏 world cells、salt 和一次性访问策略。Agent 进程只获得公开任务与独立 agent seed，
不能读取评测目录、世界标签或私有参数。对外只发布允许公开的聚合与签名摘要。

## 结果为什么可信

```text
Agent submission
  → trajectory schema 与状态守恒
  → deterministic replay
  → metric recomputation
  → constraint and resource audit
  → task-level statistics
  → verified release artifact
```

评价器不信任自报分数，也不把工程门禁通过自动升级为科学结论。

## 当前状态

World Engine、回放、资源合同和部分确认协议可运行；正式方法范围仍为 0/5 readiness slots ready。当前
四 seed action/intervention 设计审计已证明各材料反事实具有决策相关性，但旧 Gate A 因动作、主指标和
Agent 可见信息合同改变而失效。控制匹配证书与在线策略可行证书都仍待重跑。完整跨方法矩阵、真实
LLM、私有泛化和独立 Bridge
证据仍未共同闭合。当前是 benchmark candidate。

继续阅读：[公平评测协议](benchmark_protocol.md) · [研究发现与证据](benchmark_release.md) ·
[提交、回放与私有评测](submission.md)
