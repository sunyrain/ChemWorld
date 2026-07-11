# 科学状态与证据

ChemWorld 的环境、任务合同、轨迹回放和本地评测链可以用于研究开发。完整 benchmark 仍未通过
经验有效性、跨方法比较、隐藏世界泛化和独立复现的联合门禁。

## 当前结论

!!! info "可用，但不可过度解释"
    当前版本可以支持 Agent 开发、课程、协议研究和诊断实验。它尚不支持正式 leaderboard、SOTA
    排名、RL/LLM 优劣结论或现实化学发现主张。

## 三种状态不要混淆

| 状态 | 含义 | 当前情况 |
| --- | --- | --- |
| 软件就绪 | API、操作、任务、账本、回放和验证器按合同工作 | 已建立 |
| 诊断证据 | 运行能暴露方法差异、失败模式和评价缺陷 | 已建立一部分 |
| 科学验证 | 预注册比较、全部方法家族、隐藏泛化与独立复现共同通过 | 未完成 |

## 2026-07 vNext 经典诊断

最新冻结运行比较 `structured_gp_bo` 与 `random`：

- 4 个研究核心任务；
- 每个任务 20 个配对 seeds；
- 每个 seed-method 40 个完整实验；
- 共 160 个结果和 6,400 个完整实验；
- 160 条轨迹均通过独立 digest 检查、回放和指标重算；
- 无作业失败，资源账本全部闭合。

目标指标结果如下。效应为 structured GP 减 random；区间为配对 bootstrap 区间。

| 任务 | 主指标 | 平均效应 | 95% 区间 | SESOI | 目标规则 |
| --- | --- | ---: | ---: | ---: | --- |
| 分配发现 | organic product fraction | +0.0566 | [0.0505, 0.0631] | 0.0292 | 通过 |
| 反应—结晶 | crystal yield | +0.1455 | [0.1310, 0.1606] | 0.038827 | 通过 |
| 反应—蒸馏 | distillate purity | +0.1319 | [0.1224, 0.1419] | 0.0200 | 通过 |
| 连续流优化 | flow conversion | +0.0302 | [0.0278, 0.0327] | 0.0200 | 通过 |

四项任务的目标方向、SESOI 和 Holm 校正均通过。但风险诊断改变了结论：

| 任务 | random 风险超限率 | structured GP 风险超限率 | 差值 |
| --- | ---: | ---: | ---: |
| 分配发现 | 16.6% | 6.8% | −9.9 pp |
| 反应—结晶 | 21.0% | 49.6% | +28.6 pp |
| 反应—蒸馏 | 22.3% | 56.4% | +34.1 pp |
| 连续流优化 | 18.6% | 36.9% | +18.3 pp |

原冻结规则只预注册了任务目标的方向、效应阈值和多重比较，没有预注册安全与成本非劣界限。
因此客观表述是：**结构化 GP 在这一批运行中提高了任务目标，同时在三项任务中观察到更高的风险
预算超限率。** 这批结果是发现评价缺陷的诊断证据，不是完整方法胜负结论。

## 任务层级

| 层级 | 任务 | 当前用途 |
| --- | --- | --- |
| 软件回归 core | assay、purification、partition | API、回放和发布链路检查 |
| 研究核心候选 | partition、crystallization、distillation、flow | 新约束协议下重新确认 |
| 探索任务 | electrochemical、equilibrium | 继续校准可辨识主指标与机理族 |
| 其余注册任务 | 教学与能力切片 | 不进入研究主排名 |

`core` 是软件套件标签，不等于科学结论。任务被注册、无 proxy 路由或通过单元测试，也不自动获得
benchmark 有效性。

## 已建立的基础

- 版本化 task、scenario、mechanism、observation 和 scoring 合同；
- 事务式操作执行、失败回滚与 constitution 检查；
- 显式物理化学 provider，正式运行路由不依赖旧通用 fallback；
- campaign、experiment、operation 三层资源账本；
- final objective、任务主指标、在线 shaping、安全和成本分层评测；
- 轨迹 SHA-256、确定性 replay、score/replay 绑定和失败关闭；
- 类型化材料表示和可区分的经典 acquisition 实现；
- RL、LLM、机理扰动、reference search 和私有评测的控制协议骨架。

## 尚未关闭的门禁

1. 预注册逐任务安全与成本非劣界限，并在未使用的新 seed cohort 上复跑经典主比较。
2. 完成 full-budget PPO、SAC 训练与评测，保留 checkpoint、训练步数和计算摘要。
3. 完成两个冻结 live-LLM 角色的配对运行，记录失败、重试、token、费用、谱图证据与回放。
4. 校准机理族扰动强度，冻结不重叠的 Train/Dev/Bench 世界分配。
5. 完成独立 reference portfolio 搜索，避免用被评方法自己的最好值充当 oracle。
6. 完成 salted private evaluation，只发布签名聚合结果。
7. 从干净 wheel 由独立执行者复现全部主结果。

## 支持与不支持的主张

| 主张 | 状态 |
| --- | --- |
| 提供预算受限、部分可观测、可回放的虚拟实验环境 | 支持 |
| 能统一记录不同 Agent 的交互与资源使用 | 支持软件能力 |
| 最新运行显示 structured GP 的目标收益 | 支持，限四任务诊断切片 |
| structured GP 在完整约束下优于 random | 不支持 |
| safe BO、PPO、SAC 或 live LLM 已完成正式比较 | 不支持 |
| 已验证跨机理或私有世界泛化 | 不支持 |
| 数值可预测真实反应、设备或危险 | 不支持 |
| ChemWorld 是已发布的 SOTA benchmark | 不支持 |

运行自己的比较前请阅读[评测协议](benchmark_protocol.md)、[安全与成本](safety_cost.md)和
[适用范围与限制](limitations.md)。
