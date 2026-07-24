# 旗舰世界与任务

> **任务不是功能清单，而是不同实验推理能力的压力测试。**

首页只突出四个研究核心世界；探索任务、教学切片和软件回归任务仍然保留，但不与旗舰任务共享同一
视觉层级，也不因为“能运行”就自动进入正式排名。

这里的四个世界是 **research showcase worlds**。当前机制适应确认协议中的 formal flagship
execution tasks 是 `reaction-to-crystallization` 与 `electrochemical-conversion`。展示层与确认性
实验层是两个正交集合，详细状态见[旗舰实验与冻结状态](flagship_experiments.md)。

## 能力地图

```text
发现隐藏规律
  ├── Partition Discovery
  └── Equilibrium Characterization

规划多阶段过程
  ├── Reaction to Crystallization
  └── Reaction to Distillation

识别与控制动态系统
  ├── Flow Reaction Optimization
  └── Electrochemical Conversion
```

## Partition Discovery

**科学问题**：Agent 能否用有限测量学习未知液液分配规律，而不是穷举配方？

| 维度 | 内容 |
| --- | --- |
| 最困难的决策 | 直接追求回收率，还是先做能区分分配假设的测量 |
| 可执行操作 | 选择相、萃取剂、比例、混合、静置、分相与测量 |
| 可获得观测 | 相探针、终检、成本、样品消耗和公开约束 |
| 隐藏变化轴 | 分配构成律、活度修正与世界参数 |
| 主要评价 | 信息效率、最终回收、风险、成本与实验预算 |
| 适合方法 | BO、Safe-BO、主动学习、world model、LLM planner |
| 当前证据 | 环境与构成律控制可运行；正式适应矩阵未闭合 |
| Bridge 潜力 | 低风险、低成本，适合作为首批数据或物理桥接候选 |

## Reaction to Crystallization

**科学问题**：Agent 能否把反应、晶种、冷却、生长和过滤连接成一条稳定流程？

| 维度 | 内容 |
| --- | --- |
| 最困难的决策 | 何时结束反应、怎样安排晶种与冷却，而不牺牲回收和粒度 |
| 可执行操作 | 反应操作、冷却、加晶种、结晶、过滤与终检 |
| 可获得观测 | 过程、谱图、晶体与终检摘要，以及成本和风险 |
| 隐藏变化轴 | 反应速率族、结晶与传递条件 |
| 主要评价 | 目标结果、纯度、回收率、粒度代理、风险与成本 |
| 适合方法 | 长程规划、层级 RL、world model、operation-level LLM |
| 当前证据 | Provider 与守恒控制可运行；完整跨方法结果未形成 |
| Bridge 潜力 | 适合第二阶段窄域数据与设备验证，需要更强校准和安全边界 |

## Reaction to Distillation

**科学问题**：Agent 能否从反应结果出发，规划切割策略并管理纯度、回收、能耗和风险？

| 维度 | 内容 |
| --- | --- |
| 最困难的决策 | 何时结束反应、如何设置蒸馏条件与产品切割 |
| 可执行操作 | 反应、终止、浓缩、蒸馏、切割和终检 |
| 可获得观测 | 温度、过程摘要、产品指标、能耗与约束 |
| 隐藏变化轴 | 反应族、VLE 与设备能力边界 |
| 主要评价 | 纯度、回收、能耗、风险、成本与流程完成度 |
| 适合方法 | 多阶段规划、Safe-BO、层级 RL、模型预测控制 |
| 当前证据 | runtime route 与局部参考验证具备；正式适应结果未形成 |
| Bridge 潜力 | 工业意义强，但设备与安全复杂，不适合作为首个物理闭环 |

## Flow Reaction Optimization

**科学问题**：Agent 能否在隐藏动力学、传热与设备边界下快速辨识并控制连续过程？

| 维度 | 内容 |
| --- | --- |
| 最困难的决策 | 在流量、停留时间、温度、测量与风险之间寻找动态策略 |
| 可执行操作 | 配置流动条件、运行反应、测量、调整和终检 |
| 可获得观测 | 转化、选择性、过程与安全摘要 |
| 隐藏变化轴 | 速率律、网络拓扑、传热与过程参数 |
| 主要评价 | 转化或选择性、适应速度、风险、成本和资源 |
| 适合方法 | SAC/TD3、MPC、system identification、world-model control |
| 当前证据 | 动态 Provider 与单 seed RL 工程链可运行；稳定策略排名未建立 |
| Bridge 潜力 | 连续反馈与硬件接口清晰，是重要候选，但需先完成 shadow-mode 验证 |

## 其它世界承担什么角色

| 类别 | 任务 | 用途 |
| --- | --- | --- |
| 探索世界 | `electrochemical-conversion`、`equilibrium-characterization` | 主指标与适应协议仍在发展 |
| 教学与能力切片 | mechanism explanation、low-budget characterization、tool planning 等 | 课程、接口和诊断 |
| 软件回归 | assay、purification、partition 等稳定切片 | API、状态账本、回放和发布链检查 |

物理成熟度属于每张任务卡的证据字段，不是任务的第一句价值描述。backend v0.5 candidate 冻结后，
15 个注册任务的最弱必需路径均为 `reference_validated`，且 `proxy_allowed=false`。这一等级仍只适用于
各模型卡的窄域，不会被包装为真实化学或工业验证。

完整 15 任务目录、Task ID 与合同字段见[完整任务目录](tasks.md)和[任务卡](task_cards.md)。
