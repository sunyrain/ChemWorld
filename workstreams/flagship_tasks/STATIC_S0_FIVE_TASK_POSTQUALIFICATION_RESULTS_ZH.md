# S0 五任务 post-qualification 20×5 结果

日期：2026-07-30
状态：**development-only；完整执行与审计已完成，不是正式 benchmark 排名**

## 1. 这轮回答什么

本轮在同一份中性 Participant prompt、同一模型和同一预算下比较五个静态科学优化任务：

1. `electrochemical-conversion`
2. `reaction-to-crystallization`
3. `reaction-to-distillation`
4. `partition-discovery`
5. `flow-reaction-optimization`

每个任务使用 world seed 0–4。Participant 为 Codex subscription
`gpt-5.6-sol`、medium reasoning，每个任务×世界完成 20 轮自主探索，再对最终推荐和
incumbent 各做 3 次配对盲验证。经典对照为 random、LHS、greedy、Structured GP-EI 和
Structured RF-EI，算法 seed 固定为 0。

这轮用于验证升级后的五任务合同能否支撑完整比较，并观察一个共享、无任务特定隐藏指导的
Participant 策略在任务间如何变化。它没有预注册 superiority 检验，因此方法差异只作描述。

## 2. 完成性与账本

| 项目 | 结果 |
| --- | ---: |
| 结果单元 | 150 / 150 |
| Participant 单元 | 25 |
| 经典基线单元 | 125 |
| Participant 探索实验 | 500 |
| Participant 盲验证实验 | 150 |
| 基线探索实验 | 2,500 |
| 基线盲验证实验 | 750 |
| 物理实验总数 | 3,900 |
| Participant provider 调用 | 526 |
| 精确 replay | 全部通过 |
| 源码绑定 | `74cfcdaa0d9780de2d21424ef8c329079554f8b5`，clean |

计划调用数为 525。电化学 world 1 的首次最终综合使用了未知机制标签，20 轮探索本身完整；
续跑复用该探索前缀，只增加一次最终综合调用，并保留原失败 lineage。续跑结果和全部其他单元
均通过事后审计。

## 3. 盲测结果

分数只在同一任务内比较。下表为五个独立世界的均值 ± 样本标准差。

| 任务 | Codex | 最佳经典方法 | 最佳经典均值 | Codex − 最佳方法均值 | 逐世界对当世最佳基线胜/平/负 | 阈值 |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| 电化学转换 | **0.7454 ± 0.0522** | Structured RF-EI | 0.6622 | +0.0832 | 3 / 0 / 2 | 0.58 |
| 反应—结晶 | 0.5206 ± 0.0681 | Structured RF-EI | **0.6071** | −0.0866 | 1 / 0 / 4 | 0.55 |
| 反应—蒸馏 | **0.4795 ± 0.0264** | Structured GP-EI | 0.4192 | +0.0603 | 4 / 0 / 1 | 0.29 |
| 分配规律 | 0.5426 ± 0.0870 | Structured GP-EI | **0.5511** | −0.0085 | 1 / 0 / 4 | 0.58 |
| 连续流优化 | 0.1627 ± 0.0131 | Structured GP-EI | **0.2145** | −0.0518 | 0 / 0 / 5 | 0.18 |

## 4. 主要判断

### 电化学旧低分已经被当前合同替代

当前五世界 Participant 均值为 `0.7454`，世界分数为
`0.6621 / 0.7566 / 0.7359 / 0.7718 / 0.8005`。这与已撤回的
`0.3902` 不属于同一有效证据合同；网站和论文材料不得再把旧值作为当前结果。

### 结晶不是 0.6+ 的 Participant 任务

当前 Participant 均值为 `0.5206`，低于五种经典方法中的全部方法；Structured RF-EI
为 `0.6071`。world 1 的 Participant 最佳探索仅 `0.4551`，说明主要问题是搜索而非
盲测噪声或最终推荐误选。旧 `0.4829` 已撤回，但不能因此把新结果描述成 `0.6+`。

### 新蒸馏任务已经从“设计合格”进入完整比较

13D 联合反应—热分离任务在五个世界中全部超过 `0.29` 阈值。Participant 对逐世界最佳
经典基线为四胜一负，唯一一次差值仅 `−0.0022`。新增反应阶段 HPLC、后馏分 GC、安全
审计化以及两个独立无序 nominal 编码后，任务仍可解且对 LLM Participant 有区分度。

### 分配任务实现通过，但预注册性能门失败

Participant、GP-EI 和 greedy 均接近，但最佳方法跨世界均值只有 `0.5511`，没有任何方法
达到 `0.58`。不能事后降低阈值；应报告为任务合同、执行和回放合格，但当前五世界性能资格
未通过。world 4 的所有方法都明显更难，是下一轮诊断重点。

### 连续流暴露共享自然语言搜索策略的能力缺口

Participant 五个世界均低于当世最佳经典基线，均值 `0.1627`，接近 random/LHS，低于
Structured GP-EI 的 `0.2145`。最终推荐大多复用已测试 incumbent，低分主要来自探索没有
利用连续空间局部几何，而不是 closeout 误选。下一版 Participant 应考虑允许通用数值搜索
工具，而不是加入任务特定答案。

## 5. 可以与不可以说什么

可以说：

- 升级后的五任务 campaign 架构完成了 150 个单元和 3,900 次物理实验的可审计比较；
- 同一共享 Codex 策略在任务间高度异质，电化学和蒸馏强，结晶和连续流弱；
- 新蒸馏任务已具备五世界 development comparison；
- partition 的当前性能门失败被完整保留。

不可以说：

- Codex 在 ChemWorld 上整体优于经典优化器；
- 五任务绝对分数可直接横向平均；
- 这轮 development-only 结果替代既有两任务正式三臂结论；
- 仿真结果已经证明现实化学或工业流程性能。

## 6. 证据入口

- 机器可读摘要：
  `workstreams/flagship_tasks/reports/static-s0-five-task-postqualification-campaign-summary.json`
- 冻结 campaign 计划：
  `configs/benchmark/static_s0_five_task_campaign_20x5_v0.1_dev.json`
- 共享 Participant 方法：
  `configs/methods/llm_v1.5/participant_methods_s0_codex_subscription_sol_five_task_20x5_v15.json`
- 完整本地报告：
  `runs/dev/static-s0-five-task-campaign-20x5-v0.1/campaign_report.json`
