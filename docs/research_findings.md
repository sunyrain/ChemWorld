# 研究发现

!!! warning "Pre-v0.5 诊断结果"
    早期 classical、Safe-GP 与 SAC 数字早于 v0.5 candidate backend，只用于说明协议和失败模式，
    不能作为当前 15 个任务上的方法排名。

> **ChemWorld 已经形成有价值的环境控制、失败案例和诊断证据，但尚未完成正式 benchmark release。**

## 证据等级

| 等级 | 含义 |
| --- | --- |
| 已实现 | 存在可执行代码路径和公开接口 |
| 控制验证 | 可执行对照证明环境行为符合合同 |
| Agent 演示 | Agent 在开发实验中表现出可解释行为 |
| 确证结果 | 冻结方法在未触碰 cohort 上完成评估 |
| 外部桥接 | 独立 backend、真实数据或物理证据提供支持 |

## 发现一：目标提升可能掩盖风险退化

早期无约束 structured GP 在部分任务上提高目标值，同时增加操作风险超限。因此，最终 outcome 不能替代
风险、成本和协议有效性的独立报告。

## 发现二：严格判据应保留有信息量的失败

早期 Safe-GP 确证在四个任务上改善目标并满足安全/成本规则，但 flow effect 低于预注册实用阈值，
所以整体主张仍然失败。ChemWorld 将这种边界失败保留为结果，而不是事后放宽阈值。

## 发现三：受控可识别性通过，固定四动作在线证书仍未通过

当前 material、mechanism 与 constitutive-law counterfactual 均由隐藏世界执行。源码绑定的 RC21
正式结果在预算 4 下给出：controlled matched certificate 为 239/240（99.58%）并通过；独立
online-policy-feasible certificate 为 230/240（95.83%），但反应 `rate_law_family` 仅识别
23/30，其 Wilson 下界为 0.5907，因而 Gate A 仍为 false。同一 family 在受控证书中为 30/30；
反应 material family 在受控与在线证书中均为 29/30。

该 rate-law family 绑定的是上游目标生成路径的 pivot-normalized catalyst-activity-order stress，
不是结晶成核或生长速率律；设计审计证明只有 `target_formation` 的速率律改变，结晶构成参数不变。
RC22-d 又以独立 fit、policy-selection validation 和开发 trial namespace 检查了所有 11 个合规
四动作集合。所有集合都未通过按 world 聚类的 selection validation；最佳集合的最弱 family 仅为
16/24。所选集合在 20 worlds/family 的非控制性开发 trial 中得到：rate-law 20/20、no-change
20/20、topology 18/20、material mapping 12/20；电化学四类均为 20/20。该开发结果不控制 Gate A，
也没有触发 RC22 正式运行。它说明当前阻断来自固定四动作、单 reference/单 likelihood 在线 decoder
不能同时稳定利用时间与跨动作关系证据，而不是反应 rate-law 物理任务不可识别。

使用 RC21 原始 fit/trial seed、相同固定策略和相同公开观测合同的非控制性预算延长又给出了
`k={1,2,4,8}` 曲线。反应任务总体分别为 53/120、77/120、111/120 和 112/120；rate-law 分别为
0/30、10/30、23/30 和 23/30。k=4 精确复现 RC21，k=8 只把 no-change 从 29/30 提高到 30/30，
rate-law 的 Wilson 下界仍为 0.5907。该开发诊断复用了正式 seed，不能成为新的确证结果；它排除了
“只要把同一固定周期从四步延长到八步就能闭环”的解释，说明额外轮次没有提供新的辨识关系。

随后一个未进入证书、仅 4 worlds/family 的小规模开发筛查又否决了朴素的 “myopic posterior-EIG
与一步 reference acquisition” 策略：它虽然产生了不同动作路径，但经常重复同一个局部高信息动作；
反应任务仅识别 10/16（rate-law 3/4、topology 4/4、material 1/4、no-change 2/4），而电化学为
16/16。该低功效筛查不能估计正式通过率，相关实现也未保留；它只说明未来自适应方法必须显式联合
规划 reference coverage、时间证据与跨动作关系，并在独立 selection validation 通过后才能预注册。

RC21 还暴露了一个更基础的协议问题：`change_time=1` 虽然在实现上表示先执行一个旧世界实验，
但该实验通常落在 rate-law 的弱信号枢轴附近，不能形成足以解释“从什么变成什么”的响应基线。
因此 v0.3 不再把静态世界识别、早期无校准非平稳性和有基线的在线变化归因混在同一个 Gate。
静态轨只识别当前世界；`change_time={0,1,2,4}` 被保留为非控制性压力轨；控制 Gate A3 的校准轨
使用 `truth_change_time={never,6,8,10}`。`τ=6` 唯一表示前六个完整实验属于旧世界，第七个实验
开始才可能变化；Agent 不知道最早变化位置、候选时间、reference certificate 或 evaluator
checkpoint。RC23 reference certificate 同时要求通用关系覆盖和 held-out 旧世界预测充分性，并将
reference failure 保留在端到端成功率分母中。Development、A2、A3 与 private confirmation 使用
四个不重叠 cohort。RC23 旗舰语义审计 18/18、物理设计审计 81/81 通过，但 A2/A3 仍需新的未触碰
cohort；RC21/RC22-d 不能升级为 v0.3 确证证据。

这些结果只支持环境级可识别性诊断，不证明被评 Agent 已具备机制发现能力，也不代表发现了结晶动力学
或精确速率参数。

## 发现四：当前 RL 证据诊断的是合同，不是排名

早期 100,000-step SAC 管线能够端到端运行，但行为覆盖和核心 flow operation 仍不足。当前结果用于发现
action、reward、checkpoint 和资源计量问题，不构成正式多 seed 排名。

## 发现五：LLM 的反馈利用需要因果消融

operation-level 交互、跨实验记忆、光谱披露和资源计量已经实现，但解释文本本身不能证明反馈改变了决策。
正式证据仍需要局部配对反馈反应测试和完整 campaign 因果消融。

**当前状态：benchmark candidate。** 尚不支持 SOTA、完整 RL/LLM 排名、Agent 机制适应或真实世界迁移主张。
机器可读状态以 [`configs/current.json`](https://github.com/sunyrain/ChemWorld/blob/main/configs/current.json)
和[证据与当前状态](benchmark_release.md)为准。
