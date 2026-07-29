# 研究发现

!!! warning "Pre-v0.5 诊断结果"
    早期 classical、Safe-GP 与 SAC 数字早于 v0.5 candidate backend，只用于说明协议和失败模式，
    不能作为当前 15 个任务上的方法排名。

> **ChemWorld 已经形成有价值的环境控制、失败案例和诊断证据，但尚未完成正式 benchmark release。**

!!! warning "证据时态"
    下文 RC28 数字是在其冻结源码上的正式历史结果。当前源码已因静态 S0 和任务合同工作发生变化，
    evidence DAG 当前将 10 个相关绑定标为 stale；当前 `benchmark_ready=false`。2026-07-27 的旧
    静态 S0 双任务结果已撤回，不再是当前证据，也不能用于论文数字或模型排名。
    当前 benchmark readiness 需要 Gate A 重新认证。

## 新发现：两个确认性任务的替代正式实验已完成

电化学替代协议已绑定 `nominal-prior-latent-v2` 材料家族、
`electrochemical-s0-balanced-efficiency-v2` 评分与匿名材料身份。反应–结晶现有独立的
`reaction-crystallization-latent-materials-v1`：催化剂和溶剂进入反应动力学，溶剂还进入溶解度、
成核、生长和杂质夹杂。两个正式 campaign 均完成 10 个独立世界、每世界 20 轮、配对盲验证、完整
经典基线和精确 replay。

Codex 在电化学和结晶上的均值分别为 0.7150 和 0.5355。电化学相对最佳 information-matched
基线的描述性差为 +0.0991，但相对最佳 privileged calibration 基线的区间跨 0；结晶低于 LHS
的 0.5708。因此当前不能声称结晶优于经典基线。比较没有预注册 superiority 阈值或多重比较方案。

## 新发现：正确匿名材料属性呈正向但不确定的中期信号

S0 v1.1 在 v1.0 opaque 条件上只增加匿名、正确、族级的名义材料属性，并保持 world seed、观测
噪声、预算、模型和盲测端点配对。负责人要求先看五世界结果，因此目前每任务只完成 seed 0–4：

- 电化学 nominal 0.7873 vs opaque 0.6939，配对差 +0.0935，95% 区间
  [−0.0062, +0.2232]，4 胜 1 负；
- 结晶 nominal 0.5507 vs opaque 0.5173，配对差 +0.0334，95% 区间
  [−0.0307, +0.0929]，3 胜 2 负。

全部 10 个单元精确 replay，账本为 380 次物理实验、210 次成功订阅调用、5 次自动重试和 0 方法
失败。两个点估计都偏正，但区间均跨 0；冻结的每任务 97.5% 规则预览也为 `inconclusive`。这不是
十世界确认性结果，不能写成“已证明材料属性提升性能”，也不能把结晶 0.5507 写成 0.6+。完整
信息价值论断仍缺 seed 5–9。

## 设计发现：15 个任务都需要真实可执行的完整实验

完成性审计发现三个纯化任务曾被错误映射为通用反应配方，蒸发与蒸馏条件也曾共享强度坐标。修正后，
三个纯化任务使用 16 个独立控制和 22 个编译操作；蒸馏使用 13 个控制，两个阶段的温度和时间相互独立。
矩阵生成器实际执行 415 个完整案例，覆盖中点、每个坐标低/高干预和全部离散类别。当前 15/15 通过，
62 个声明指标全部有可执行评估端点；这只证明设计可执行，不构成其余 13 个任务的正式性能证据。

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

## 发现三：历史四动作在线证书失败；校准后的 RC28 Gate A 通过

当前 material、mechanism 与 constitutive-law counterfactual 均由隐藏世界执行。源码绑定的 RC21
正式结果在预算 4 下给出：controlled matched certificate 为 239/240（99.58%）并通过；独立
online-policy-feasible certificate 为 230/240（95.83%），但反应 `rate_law_family` 仅识别
23/30，其 Wilson 下界为 0.5907，因而历史 RC21 Gate A 仍为 false。同一 family 在受控证书中为 30/30；
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
checkpoint。RC24 将 A3 明确为冻结 reference diagnostic policy 的 online attainability；
reference certificate 使用关系闭合和 campaign 内 pre-change cross-fitting，changed 与 never
分开定义分母，并在 `k={1,2,4,8}` 报告时序检测。A2/A3/private 每个任务/family 冻结 180 个独立
world cluster。确认性任务语义审计 25/25、物理设计审计 83/83 通过后，正式结论仍必须来自新的
RC28 未触碰 cohort；RC21/RC22-d/RC23 不能升级为 v0.3 确证证据。

RC28 随后按校准协议在未触碰正式 cohort 上完成执行。A2 生成 4,896/4,896 receipts，并在五实验
主预算通过：active oracle 与 fixed decoder top-1 均为 98.26%（95% CI 97.45–98.82），所有
task/family 交集通过。A3 生成 2,016/2,016 receipts；到 `k=8`，冻结 reference policy 的参照充分率、
changed 检测召回率、AUROC、条件 no-change FPR、条件归因率和端到端成功率分别为 99.17%、
99.35%、0.9990、2.80%、98.03% 和 96.57%。冻结源码上的联合决策为 `gate_a_pass=true`、
`benchmark_ready=true`，该版本 Gate A 总状态为 true；当前源码绑定 stale。

该新结果解决的是环境在线可达性问题，不是 participant Agent 能力问题。Gate B–E、
Private-E/Private-A、跨方法 provider 结果和发表证据仍未完成。

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
