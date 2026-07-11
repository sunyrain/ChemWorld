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

## 2026-07 vNext 约束确认候选

最新冻结运行比较 `structured_gp_bo` 与 `random`：

- 4 个研究核心任务；
- 每个任务 20 个配对 seeds；
- 每个 seed-method 40 个完整实验；
- 共 160 个结果和 6,400 个完整实验；
- 160 条轨迹均通过独立 digest 检查、回放和指标重算；
- 无作业失败，资源账本全部闭合。

协议 0.3 在运行前冻结新 seeds 300–319、任务 SESOI、5 个百分点安全非劣界限、5% 相对成本非劣
界限，以及 8 个约束比较的 Bonferroni 同时上界。它没有复用已观察的 seeds 20–39。

目标指标结果如下。效应为 structured GP 减 random；区间为配对 bootstrap 区间。

| 任务 | 主指标 | 平均效应 | 95% 区间 | SESOI | 目标规则 |
| --- | --- | ---: | ---: | ---: | --- |
| 分配发现 | organic product fraction | +0.0484 | [0.0417, 0.0551] | 0.0292 | 通过 |
| 反应—结晶 | crystal yield | +0.1503 | [0.1326, 0.1694] | 0.038827 | 通过 |
| 反应—蒸馏 | distillate purity | +0.1331 | [0.1252, 0.1413] | 0.0200 | 通过 |
| 连续流优化 | flow conversion | +0.0310 | [0.0271, 0.0349] | 0.0200 | 通过 |

四项任务的目标方向、SESOI 和 Holm 校正均通过。但风险诊断改变了结论：

| 任务 | random 风险超限率 | structured GP 风险超限率 | 差值 |
| --- | ---: | ---: | ---: |
| 分配发现 | 14.9% | 7.6% | −7.3 pp |
| 反应—结晶 | 21.1% | 48.4% | +27.3 pp |
| 反应—蒸馏 | 20.1% | 59.1% | +39.0 pp |
| 连续流优化 | 19.3% | 35.3% | +16.0 pp |

四项成本非劣规则全部通过；分配任务通过安全非劣，另外三项失败，其 simultaneous upper bounds
分别为 33.8、43.9 和 21.1 个百分点，均高于 5 个百分点界限。因此客观结论是：**结构化 GP 在
新 cohort 中稳定提高任务目标，但完整受约束主比较失败。** 该结果拒绝方法优越性主张，同时为
开发真正风险感知的策略提供了明确目标。

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

1. 只在 Train/Dev worlds 开发真正风险感知的策略；当前 Bench cohort 不再用于调参。
2. 完成 full-budget PPO、SAC 训练与评测，保留 checkpoint、训练步数和计算摘要。
3. 完成两个冻结 live-LLM 角色的配对运行，记录失败、重试、token、费用、谱图证据与回放。
4. 校准机理族扰动强度，冻结不重叠的 Train/Dev/Bench 世界分配。
5. 完成独立 reference portfolio 搜索，避免用被评方法自己的最好值充当 oracle。
6. 完成 salted private evaluation，只发布签名聚合结果。
7. 若风险感知方法形成新主比较，冻结另一个未触碰 cohort，并由独立执行者复现。

## 支持与不支持的主张

| 主张 | 状态 |
| --- | --- |
| 提供预算受限、部分可观测、可回放的虚拟实验环境 | 支持 |
| 能统一记录不同 Agent 的交互与资源使用 | 支持软件能力 |
| 最新运行显示 structured GP 的目标收益 | 支持，限四任务 0.3 切片 |
| structured GP 在完整约束下优于 random | 不支持 |
| safe BO、PPO、SAC 或 live LLM 已完成正式比较 | 不支持 |
| 已验证跨机理或私有世界泛化 | 不支持 |
| 数值可预测真实反应、设备或危险 | 不支持 |
| ChemWorld 是已发布的 SOTA benchmark | 不支持 |

运行自己的比较前请阅读[评测协议](benchmark_protocol.md)、[安全与成本](safety_cost.md)和
[适用范围与限制](limitations.md)。
