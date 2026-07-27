# 研究发现与证据

!!! warning "Pre-v0.5 diagnostic"
    本页的经典优化、Safe-GP 与早期 SAC 数值来自后端 v0.5 候选冻结前，只用于解释协议和失败模式，不能作为当前 15 任务的算法排名。当前后端事实见[任务与版本](tasks.md)。

> **ChemWorld 已经产生了有价值的失败与控制结果，但完整 benchmark 仍未达到正式发布状态。**

!!! success "当前静态 S0 正式证据"
    两个确认性任务的五 seed `gpt-5.6-sol high` 静态优化已经完成并逐实验 replay。电化学盲最终均值
    为 0.3902（95% world-cluster CI [0.1732, 0.6072]），反应–结晶为 0.4829
    （[0.4326, 0.5332]）；相对最强经典校准家族逐 world 分别为 2 胜 3 负和 0 胜 5 负。十次
    final synthesis 中 0 次产生正增益。固定世界 S0 是当前主线；世界变化实验已经延期。

!!! info "15 任务设计证据"
    15 个完整实验适配器均通过坐标干预检查和端到端中点执行，死坐标与未解决正式化 blocker 均为 0。
    三个纯化任务现覆盖完整后处理，蒸发与蒸馏控制也已拆分。该证据只支持设计可执行性；其余 13 个
    任务没有本轮正式模型性能结果。

!!! warning "RC28 当前绑定"
    RC28 Gate A 的 4,896 条 A2 与 2,016 条 A3 receipts 仍是冻结源码上的历史正式结果。当前 source
    fingerprint 已变化，相关 evidence nodes 标记为 stale；在重新认证前，当前
    `benchmark_ready=false`。

这一页按“发现”组织证据，而不是按算法或代码模块罗列功能。每项结果都说明证据等级、支持什么，
以及不能被升级成什么结论。

!!! info "一句话状态"
    World Engine、任务合同、资源账本、回放和评价控制可以运行；完整跨方法矩阵、机制适应、私有泛化
    与独立复现仍未共同完成。当前是 benchmark candidate，不支持 SOTA 或现实迁移主张。

## 五个证据等级

| 等级 | 含义 | 当前例子 |
| --- | --- | --- |
| **Implemented** | 代码路径和接口存在 | Agent API、provider route、轨迹 schema |
| **Control-validated** | 环境行为经过可执行控制 | 回放、守恒、15 任务设计 smoke、机理干预与信息遮蔽 |
| **Agent-demonstrated** | Agent 在开发实验中显示可解释行为 | 经典方法与单任务 RL 诊断 |
| **Confirmatory** | 冻结方法在未见 cohort 上按预注册规则检验 | 两个确认性任务的五 seed 静态 S0 |
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
30/30，反应 material family 在两份证书中均为 29/30，因此 RC21 未通过 Gate A。

非控制性的 RC22-d 开发诊断使用相互独立的 fit、policy-selection validation 与 trial namespace，
检查全部 11 个合规四动作集合。所有集合均未通过按 world 聚类的 validation，最佳最弱 family 为
16/24；所选集合的实际开发结果为 rate-law 20/20、no-change 20/20、topology 18/20、material
mapping 12/20，电化学四类均为 20/20。该结果没有启动或替代正式 RC22。它表明当前固定四动作、
单 reference/单 likelihood decoder 尚不能稳定合并时间与跨动作关系证据；阻断项不是 rate-law
物理任务本身，也不能仅靠重复同一固定周期或补齐材料配对来消除。

进一步复核确认，RC21 还把“旧世界参考是否充分”和“有参考后能否归因变化”混入同一在线证书。
`change_time=1` 虽然有一个旧世界实验，但通常只有枢轴附近的弱信号，不能支持“从什么变成什么”的
关系判断。v0.3 因此把静态当前世界识别、`change_time={0,1,2,4}` 的无校准压力轨、以及控制 Gate A3
的校准在线轨分开。RC24 校准轨的真值支持是 `never/6/8/10`，并冻结 `τ` 为“已完成的旧世界实验数”；
策略只看到总 horizon，不看到前缀、时间支持或证书状态。A3 认证冻结 reference policy 的 online
attainability，不认证参赛 Agent。Reference certificate 要求关系闭合、campaign 内 pre-change
cross-fitting 和参考新鲜度；changed 与 never 使用不同分母。Development、A2、A3 与 private
confirmation cohort 互不重叠。确认性任务语义审计 25/25、物理设计审计 83/83 已通过；新增两项
检查证明每个任务的 primary controlled budget 能在调度前闭合全部声明关系。该重构不改变
RC21 历史结果。RC28 随后在新的 untouched cohort 上完成正式 A2/A3。

RC28 保留上述 A3 科学设计、阈值和 cohort 规模；A2 保留 `k={2,4}` 诊断点并新增最小可行
`k=5` primary certificate，同时硬化执行语义：正式 trial 使用 write-once receipt
与 missing-only resume；changed/never 在共同语义坐标上使用 keyed observation noise；A3 指标在 A2
完成前保持 embargo；Private confirmation 拆为环境证书复现 Private-E 与 participant-Agent 复现
Private-A。A2 的 2/4/5 次配对诊断预算不再与 A3 的六次旧世界参照前缀混为同一个预算条件。

RC28 正式运行完成 A2 4,896/4,896 和 A3 2,016/2,016 receipts，冻结源码上的联合公开决策为
`gate_a_pass=true`、`benchmark_ready=true`，该冻结版本 Gate A 整体因此通过。A2 主预算 `k=5` 下 active oracle 与 fixed decoder
top-1 均为 98.26%（95% CI 97.45–98.82），所有 task/family 交集通过。A3 在 `k=8` 的 reference
sufficiency、changed recall、AUROC、条件归因和端到端成功率分别为 99.17%、99.35%、0.9990、
98.03% 和 96.57%；条件 no-change FPR 为 2.80%，未条件化 horizon FPR 为 3.33%。完整分任务、
分 family 和 `k={1,2,4,8}` 表见 [确认性基准任务](flagship_experiments.md)。

运行后审计确认，fixed decoder 未复制 active-oracle prediction，但反应–结晶在 `k=5`
时二者选择同一个五动作 batch，因而该任务共享 paired contrast；电化学 batch 不同。
fixed decoder 不控制 Gate A，只作为辅助一致性检查。A2 的 4,896 receipts 对应 360 个
held-out certificate clusters 加 24 个独立 fit clusters，而不是 4,896 个独立 worlds；
A3 的 certificate 使用另外 360 个 clusters。

使用 RC21 原始 fit/trial seed 和同一固定策略的非控制性 `k={1,2,4,8}` 延长曲线进一步得到：
反应总体为 53/120、77/120、111/120、112/120，rate-law 为 0/30、10/30、23/30、23/30。
k=4 精确复现 RC21；k=8 仅把 no-change 从 29/30 提高到 30/30，rate-law Wilson 下界仍为
0.5907。由于复用了正式 seed，这不是新的确证结果；它只排除“把相同固定周期延长到八步即可解决”
的解释。

一个后续的 4 worlds/family 非证书筛查也否决了朴素的 myopic posterior-EIG 加一步 reference
acquisition 策略：反应任务仅为 10/16（rate-law 3/4、topology 4/4、material 1/4、no-change
2/4），电化学为 16/16，并出现重复局部高信息动作。该低功效结果不控制任何 gate，实验实现未保留，
也未触发正式 RC；它只约束下一版方法必须联合规划 reference coverage、时间证据与跨动作关系，并先
通过独立 selection validation。

**支持的结论**：ChemWorld 能执行和回放预注册隐藏规律变化；在冻结候选 family、公共动作、测量
和五次 controlled 诊断预算下，受控 oracle 与固定 decoder 均能完成机制家族诊断。冻结 reference
policy 能在未知变化时点与真值时先建立旧世界参照，再以较低 no-change 假阳性率检测变化并归因
family。A1/A2/A3 环境前置证书已经通过。

**不支持的结论**：Gate A 是环境可识别性证书，不是被评 Agent 的能力结果。该反应单元也不是
“结晶速率律发现”或精确动力学参数辨识。仍不能声称 DeepSeek 或其他 participant Agent 会识别
这些变化、恢复性能、迁移到未见 family，或适应现实机理；这些结论仍由尚未冻结和执行的 Gate B–E
及正式配对 provider 矩阵控制。

Gate B–E 的正式实验已形成单一实施计划，但尚未冻结方法、runner、power 和成本合同。主设计是
Pro/Flash × direct reactive/stateful scientific 的四方法 `2×2` 因子矩阵，预注册 backend、
scaffold 和交互效应；当前 `live_llm_a/live_llm_b` 的混合差异只能作为 development pilot。
ReAct 与 planning-memory 不阻断第一轮正式实验。

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
信息条件。默认输入已切换到 `chemworld-compact-decision-context-0.3`：只传当前任务、生命周期、
预算、标量指标、处理后的测量摘要、约束、短期记忆和合法动作参数签名。上限不再固定为 1,500，
而由 50 个最坏合法 fixture 加 15% 余量得到：Direct/Stateful 共享 2,050-token environment view，
总 prompt cap 分别为 3,600 和 4,150。原始谱图数组、replicate 曲线、重复 observation view、constitution checks 与
Git/provider/ledger 元数据仍保留在审计轨迹中，但不进入默认决策 prompt。输出要求可检验的
expected effect、diagnostic target、information-gain forecast 和条件式 belief-update rule，不请求或
保存私有逐字思维链。

当前已有 Flash Direct/Stateful 的 development execution-qualification 轨迹；两者在同一
`1 pre + 1 post` pair 中均为 0/4 autonomous completion。它们证明 provider、prompt envelope 和
失败归因链可以运行，但不能证明模型使用了谱图、形成了正确机理或优于其它方法。

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
