# 研究发现与证据

!!! warning "Pre-v0.5 diagnostic"
    本页的经典优化、Safe-GP 与早期 SAC 数值来自后端 v0.5 候选冻结前，只用于解释协议和失败模式，不能作为当前 15 任务的算法排名。当前后端事实见[任务与版本](tasks.md)。

> **ChemWorld 已经产生了有价值的失败与控制结果，但完整 benchmark 仍未达到正式发布状态。**

这一页按“发现”组织证据，而不是按算法或代码模块罗列功能。每项结果都说明证据等级、支持什么，
以及不能被升级成什么结论。

!!! info "一句话状态"
    World Engine、任务合同、资源账本、回放和评价控制可以运行；完整跨方法矩阵、机制适应、私有泛化
    与独立复现仍未共同完成。当前是 benchmark candidate，不支持 SOTA 或现实迁移主张。

## 五个证据等级

| 等级 | 含义 | 当前例子 |
| --- | --- | --- |
| **Implemented** | 代码路径和接口存在 | Agent API、provider route、轨迹 schema |
| **Control-validated** | 环境行为经过可执行控制 | 回放、守恒、机理干预与信息遮蔽 |
| **Agent-demonstrated** | Agent 在开发实验中显示可解释行为 | 经典方法与单任务 RL 诊断 |
| **Confirmatory** | 冻结方法在未见 cohort 上按预注册规则检验 | Safe-GP 四任务确认切片 |
| **Externally bridged** | 独立 backend、真实数据或物理系统支持 | 当前尚无 |

通过低等级证据不会自动获得更高等级。例如 Provider 可达不等于 Agent 会适应，软件测试全绿也不
等于方法结论成立。

## Finding 1：目标改善可能掩盖风险退化

**Evidence level：Agent-demonstrated**

无约束 structured GP 在分配、结晶、蒸馏和连续流四项任务上提高了主指标，却在连续流、结晶和
蒸馏上增加操作风险预算超限。目标—安全—成本联合规则因此失败。

**支持的结论**：只报告产率或目标分数会误判一部分实验策略；风险需要独立终点。

**不支持的结论**：不能据此证明某一种安全算法普遍优越，也不能把虚拟风险解释成现实安全限值。

## Finding 2：严格规则会保留“方向正确但效应不足”的失败

**Evidence level：Confirmatory（有限四任务切片）**

Safe-GP 在 Dev worlds 上完成修复和选择，随后冻结实现，在 20 个未触碰配对世界上运行四任务、
三方法、每次 40 个完整实验；240 条轨迹通过独立回放。

| 任务 | Safe-GP − random 主指标效应 | 区间 | SESOI | safety / cost | 联合规则 |
| --- | ---: | ---: | ---: | --- | --- |
| 分配发现 | +0.036579 | [0.026105, 0.047188] | 0.0292 | 通过 / 通过 | 通过 |
| 反应—结晶 | +0.102475 | [0.082343, 0.122691] | 0.038827 | 通过 / 通过 | 通过 |
| 反应—蒸馏 | +0.049918 | [0.034127, 0.066079] | 0.0200 | 通过 / 通过 | 通过 |
| 连续流优化 | +0.018752 | [0.013144, 0.023698] | 0.0200 | 通过 / 通过 | **失败** |

四项目标方向为正，安全和成本规则通过；但连续流效应没有达到预注册最小实质效应，完整联合结论
保持失败。随后五世界 Dev 诊断也没有找到通过降低风险置信系数修复结果的依据。

**支持的结论**：确认协议能够阻止研究者在看见“接近阈值”的结果后升级主张。

**不支持的结论**：Safe-GP 尚未通过完整四任务优越性规则，这一切片也不是跨所有 Agent Track 的
benchmark 排名。

## Finding 3：候选机制在预算内可识别，但这仍不是 Agent 能力结果

**Evidence level：Control-validated**

反应任务使用速率律与网络拓扑族；分配、电化学和平衡使用各自 Provider 消费的构成律族。既有 5 个
世界 × 5 个 recipe 控制说明 9/9 任务—模式组合满足：

- 干预确定且使用 opaque 公共标识；
- 固定探针下具有局部响应分离且不超过非灾难上限；
- 过程物料衡算在容差内；
- 精确干预上下文缺失或篡改时，回放失败关闭。

这些控制本身不等于在相同动作、测量和实验预算下可以识别候选 family。机制 v0.2.1 修复了原电化学
solvent 目标不可达问题；新的四 seed 设计审计确认 reaction catalyst、electrochemical solvent 和
`electrolyte_profile` 反事实均具有决策相关性。反应速率律单元被显式绑定为“上游目标生成路径的
pivot-normalized catalyst-activity-order stress”，并证明只有 `target_formation` 速率律改变，
结晶和其它构成参数保持不变。动作—干预设计审计全部通过。

当前源码绑定的 RC21 在全新平衡 held-out cohort 上完成了两张独立证书：预算 4 的 controlled matched
oracle 为 239/240（99.58%）并通过；在线策略可行 oracle 总体为 230/240（95.83%），但反应
`rate_law_family` 仅为 23/30，Wilson 下界 0.5907，未满足逐 family 规则。该 family 在受控证书中为
30/30，反应 material family 在两份证书中均为 29/30，因此 Gate A 整体仍为 false。

非控制性的 RC22-d 开发诊断使用相互独立的 fit、policy-selection validation 与 trial namespace，
检查全部 11 个合规四动作集合。所有集合均未通过按 world 聚类的 validation，最佳最弱 family 为
16/24；所选集合的实际开发结果为 rate-law 20/20、no-change 20/20、topology 18/20、material
mapping 12/20，电化学四类均为 20/20。该结果没有启动或替代正式 RC22。它表明当前固定四动作、
单 reference/单 likelihood decoder 尚不能稳定合并时间与跨动作关系证据；阻断项不是 rate-law
物理任务本身，也不能仅靠重复同一固定周期或补齐材料配对来消除。

一个后续的 4 worlds/family 非证书筛查也否决了朴素的 myopic posterior-EIG 加一步 reference
acquisition 策略：反应任务仅为 10/16（rate-law 3/4、topology 4/4、material 1/4、no-change
2/4），电化学为 16/16，并出现重复局部高信息动作。该低功效结果不控制任何 gate，实验实现未保留，
也未触发正式 RC；它只约束下一版方法必须联合规划 reference coverage、时间证据与跨动作关系，并先
通过独立 selection validation。

**支持的结论**：ChemWorld 能执行和回放预注册隐藏规律变化；在冻结候选 family、公共动作、测量
和四次 post-change 实验预算下，受控 oracle 能完成机制诊断。当前固定策略在线 oracle 总体准确率
较高，但尚不能对所有 change-time 同时稳定区分 rate-law、topology 与 material mapping。

**不支持的结论**：Gate A 是环境可识别性证书，不是被评 Agent 的能力结果。该反应单元也不是
“结晶速率律发现”或精确动力学参数辨识。尚不能声称 Agent 会识别这些变化、恢复性能、迁移到未见
family，或适应现实机理；这些结论仍由 Gate B–E 和正式配对 provider 矩阵控制。

## Finding 4：现有 RL 结果首先暴露了动作与训练合同问题

**Evidence level：Pre-v0.5 agent-demonstrated engineering diagnostic**

后端 v0.5 前的早期 SAC 链完成了精确 100,000 Train 步、checkpoint 保存、开发评测与回放。但旧开发轨迹大量集中
在加料、测量和终止，开发评测中的 `run_flow` 计数为 0；因此 80k 与 100k checkpoint 的分数差首先
反映动作覆盖、奖励与行为完成合同问题，而不是关于训练尺度的一般发现。

当前 remediation 已将核心流程完成、零效果 Action、重复 terminate、奖励来源和行为学习 gate 纳入
显式合同。下一步需要在这些合同冻结后重新进行 pooled multi-seed Dev 选择和未见 world 评测。

**支持的结论**：训练、评测和 replay 工程链可以连通；行为审计能够拒绝“有分数但没完成核心流程”
的策略。

**不支持的结论**：不支持 RL 排名、最佳 checkpoint 或“训练越久越好/越差”的一般结论。

## Finding 5：LLM 是否使用证据，需要因果消融

**Evidence level：Control-validated protocol**

LLM Harness 已具备逐操作决策、跨实验记忆、按需谱图、token/费用/重试账本，以及 assigned/masked
信息条件。系统只保留公开 evidence、hypothesis、uncertainty、spectrum interpretation 和简短
rationale，不请求或保存私有逐字思维链。

当前没有真实 provider 轨迹。Fake client、stub 和 replay 只能证明协议工作，不能证明模型使用了
谱图、形成了正确机理或优于其它方法。

**支持的结论**：可以冻结并审计 LLM 的信息条件、工具调用和资源。

**不支持的结论**：真实 LLM 排名、模型优劣和实验记忆价值仍需配对正式矩阵。

## 发布前还差什么

1. 冻结统一风险与行为合同后重跑完整经典方法矩阵。
2. 完成多 seed PPO/SAC 训练、Dev 选择和冻结 Bench 评测。
3. 完成真实 LLM × 信息条件 × scaffold 的配对运行。
4. 运行 Agent change detection、机制识别、recovery 和跨 family 迁移实验。
5. 完成独立 reference portfolio、私有评测和 exploit matrix。
6. 在干净安装上完成独立复现并归档完整 trajectory archive。
7. 通过独立 backend 或真实数据建立第一项 Externally bridged 证据。

## 哪些说法目前站得住

| 说法 | 状态 |
| --- | --- |
| ChemWorld 提供预算受限、部分可观测、可回放的虚拟实验合同 | 支持 |
| 六任务拥有可执行、局部可分离并可回放的机理/构成律控制 | 支持 Control-validated 层 |
| 冻结候选 family 在预算 4 下可识别 | controlled 条件下支持；online Gate A 因 reaction material family 失败，不支持完整环境级闭合 |
| Safe-GP 在确认切片中满足四任务 safety/cost 规则 | 支持有限切片 |
| Safe-GP 通过完整四任务优越性规则 | 不支持 |
| 100,000 步 SAC 工程链可执行 | 支持工程诊断，不支持排名 |
| RL 或真实 LLM 已完成正式排名 | 不支持 |
| Agent 已证明能适应未见机理或真实实验 | 不支持 |
| ChemWorld 已达到正式 SOTA benchmark 状态 | 不支持 |

协议细节见[公平评测协议](benchmark_protocol.md)，现实验证路线见
[从虚拟世界到真实实验](real_world_bridge.md)。
