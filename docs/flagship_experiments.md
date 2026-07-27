# 确认性基准任务：设计、预注册与执行状态

> **Showcase Worlds 展示平台广度；Confirmatory Benchmark Tasks 承担确认性结论。两者不再统称为“旗舰”。**

!!! warning "当前源码绑定"
    RC28 Gate A 在其冻结源码上正式通过，但 2026-07-27 的静态 S0 与任务合同更新改变了当前源码指纹。
    旧 RC28 数字仍是历史正式结果，当前绑定标记为 stale，`benchmark_ready=false`，必须重新认证后才能
    对当前源码恢复环境 Gate A 主张。

## 2026-07-27 静态 S0 正式结果

两个确认性任务现已在同一静态科学优化范式下完成 `gpt-5.6-sol high` 五 world seed 正式实验。每个
seed 有 20 个完整探索实验、一次独立最终综合、三个冻结 Predictive 干预、incumbent 与 recommendation
各三个配对盲验证；所有物理实验均已 replay。

| 任务 | LLM 盲最终 mean，95% CI | 最佳经典校准 mean | 配对差 LLM − 经典，95% CI | World 胜负 | Predictive |
| --- | ---: | ---: | ---: | ---: | ---: |
| Electrochemical Conversion | 0.3902 [0.1732, 0.6072] | RF-EI 0.4798 | -0.0896 [-0.2896, 0.1104] | 2 胜 / 3 负 | 29/45（64.4%） |
| Reaction to Crystallization | 0.4829 [0.4326, 0.5332] | GP-EI 0.5324 | -0.0495 [-0.0933, -0.0056] | 0 胜 / 5 负 | 20/45（44.4%） |

统计单位是 world seed；经典算法的五个 algorithm seed 先在每个 world 内取均值。表中区间是五个
world cluster 上的双侧 95% Student-t 描述性区间。“最佳经典校准”从六个候选算法家族中按总体
盲均值选择，因此这些区间不是预注册优越性检验。

![静态 S0 逐 world 盲最终分](assets/images/static-s0-blind-scores-v0.1.png)

两个任务的十个最佳探索点都出现在第 11 次实验以后：20 轮预算提供了实际搜索机会。第 8 轮到第
20 轮的 LLM best-so-far 均值，电化学从 0.3749 增至 0.4297，反应–结晶从 0.4311 增至 0.4911。

![静态 S0 优化曲线](assets/images/static-s0-optimization-curves-v0.1.png)

模型能进行静态闭环优化，但跨世界稳定性和世界理解均未超过结构化优化基线。十次最终提交全部为
`tested`：8/10 相对配对 incumbent 为零增益，2/10 为轻微负增益，0/10 为正增益。独立 final
synthesis 因而提供了清晰提交与解释接口，但尚未证明能产生更好的实验条件。

S0 是当前研究主线：它测量固定但未知系统中的闭环科学优化。下文 RC28 是冻结源码上的历史环境
可识别性证书，不是当前 Participant 实验路线。隐藏 changepoint、机制替换与世界变化实验已经延期；
只有建立现实漂移场景和独立问题定义后才会重新设计。

## 15 任务优化设计状态

两个确认性任务以外的 13 个任务不要求本轮昂贵模型实验，但其优化设计不能只是任务注册表。当前
15 个任务都已有版本化完整实验适配器、物理坐标、固定测量槽、final-assay 反馈和安全/成本边界。
生成器对每个坐标执行低/高干预检查，并在 world seed 0 实际运行中点配方：15/15 通过，死坐标为 0，
未解决正式化 blocker 为 0。

三个纯化任务使用 16 个独立控制和 22 个编译操作，覆盖反应、萃取、分相、洗涤、干燥、浓缩与转移；
蒸馏使用 13 个控制，蒸发/蒸馏的温度和时间已经相互独立。这些是可执行设计证据，不是其余 13 个任务
的正式算法排名。

## 两个正交集合

网站首页展示四个 **Showcase Worlds**：分配发现、反应–结晶、反应–蒸馏和流动反应优化。它们说明
ChemWorld 能支持哪些实验推理和物理化学反馈。

机制适应协议当前只有两个 **Confirmatory Benchmark Tasks**：

| 确认性任务 | 隐藏变化家族 | 可主动改变的诊断坐标 | 主要观测 |
| --- | --- | --- | --- |
| Reaction to Crystallization | rate law、反应 topology、催化剂映射 | 催化剂剂量、温度/时间、催化剂选择 | HPLC、终检、任务分数 |
| Electrochemical Conversion | 构成律、solvent 映射、electrolyte-profile 映射 | 电压、电流、时间、solvent、electrolyte profile | UV-Vis、终检、任务分数 |

Showcase 卡片不是确认性证据；确认性任务也不必出现在首页四张卡片中。代码中的部分 `flagship`
标识符是兼容性名称，不再是论文或网站的科学分类。

## 当前状态机

| 状态 | 当前值 |
| --- | --- |
| Environment design candidate | passed |
| Semantic protocol audit | 历史 RC28 passed，25/25；当前绑定 stale |
| A1 physical validity | 历史 RC28 passed，83/83 设计检查；当前绑定 stale |
| A2 controlled identifiability | 历史 RC28 **passed**，4,896/4,896 receipts；当前源码绑定 stale |
| A3 online attainability | 历史 RC28 **passed**，2,016/2,016 receipts；当前源码绑定 stale |
| Static S0 Participant Agent | 两个确认性任务五 seed 正式实验与 replay 已完成 |
| Mechanism-adaptation Participant Gates B–E | 延期研究扩展；Flash Direct/Stateful S1/S2 均为 0/4 autonomous completion，正式矩阵未启动 |
| Private-E environment confirmation | eligible，尚未执行 |
| Private-A participant-Agent confirmation | sealed，等待 participant freeze |
| Benchmark ready | `false`，等待当前源码 Gate A 重新认证 |
| Evidence complete | `false` |
| Publication ready | `false` |

25 项语义检查和 83 项设计检查是两份审计中的检查项，不代表 108 份独立科学证据。RC28 在冻结源码上
完成正式 A2/A3，并于同一联合决策中解封结果：`gate_a_pass=true`、`benchmark_ready=true`。这只表示该版本环境的
物理有效性、预算内可识别性和在线可达性前置条件已通过；它不表示 DeepSeek 或其他 participant Agent
已经通过 Gate B–E，也不使 `evidence_complete` 或 `publication_ready` 自动变为 true。

## RC28 正式 Gate A 结果

### A2：预算内受控可识别性

每个预算包含 1,440 个 task × truth × world-cluster 单元。冻结的主预算是 `k=5`：

| 预算 | Active oracle top-1（95% CI） | Fixed decoder top-1（95% CI） | family 交集 |
| --- | --- | --- | --- |
| 2 | 93.75%（92.38–94.89） | 94.44%（93.14–95.51） | fail |
| 4 | 98.47%（97.70–98.99） | 95.35%（94.13–96.32） | decoder fail |
| **5（primary）** | **98.26%（97.45–98.82）** | **98.26%（97.45–98.82）** | **pass** |

`k=4` 的 active oracle 在该 cohort 上已经能得到高准确率，但电化学五动作关系并集不能在四动作内形成
完整结构见证，而且 fixed decoder 的 family 交集仍未通过。因此正式证书仍正确绑定 `k=5`，不能事后
把较好的 `k=4` oracle 结果改成主门槛。

运行后重合审计表明，`k=5` 的 25 个 oracle/decoder 错误完全重合。原因不是 prediction
字段复制：电化学的两个五动作 batch 不同；但反应–结晶的 information maximum 恰好等于固定
前五动作，所以该任务 720 条 trial 共用同一 paired contrast。fixed decoder 从一开始就
`controls_gate=false`，这里应解释为辅助一致性检查，而不是第二个完全独立的 A2 复现证书。

在 `k=5`，电化学的 constitutive、solvent mapping、electrolyte-profile mapping 和 no-change
召回率均为 100%。反应–结晶的 rate-law、topology、material mapping 和 no-change 召回率分别为
98.33%、98.89%、88.89% 和 100%；最弱的 material mapping 95% 下界仍为 83.46%，高于冻结的
70% family 下界。

### A3：在线参照、检测与归因

冻结 reference policy 不接收变化时点、最短稳定前缀、真值或 reference certificate。总体适应曲线为：

| post-change k | 检测 recall | AUROC | 条件 FPR | mean Brier | 条件归因 | 端到端成功 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 83.10% | 0.9703 | 0.84% | 0.0641 | 88.65% | 73.06% |
| 2 | 93.46% | 0.9965 | 1.12% | 0.0446 | 95.50% | 88.52% |
| 4 | 98.88% | 0.9987 | 1.96% | 0.0331 | 97.54% | 95.65% |
| **8** | **99.35%** | **0.9990** | **2.80%** | **0.0263** | **98.03%** | **96.57%** |

这里的 FPR 是在 reference sufficient 条件下计算；未条件化的 no-change horizon FPR 为 3.33%。
总体 reference sufficient rate 为 99.17%，检测到事件的平均延迟为 1.233 个 post-change 实验。
`k=8` 时电化学和反应–结晶的端到端成功率分别为 98.33% 和 94.81%；六个 changed family 均单独
通过，最弱的是反应–结晶 material mapping（93.33% 端到端成功）。

这些数字认证的是冻结 reference diagnostic policy 所证明的 benchmark attainability，而不是
participant Agent 的能力。后者必须使用独立冻结的方法、prompt、runner、样本量和 provider 成本契约
进入 Gate B–E。

## A1、A2、A3 分别认证什么

| 层级 | 认证对象 | 作用 |
| --- | --- | --- |
| A1 | 物理世界与隐藏干预 | 变化是否真实、单轴、可达且会进入公开观测 |
| A2 | 受控 oracle/decoder | 在充分控制和相同预算下，候选家族是否可区分 |
| A3 | 冻结的 reference diagnostic policy | 在不知道变化时点和真值时，是否存在合规在线策略能建立参照、检测变化并识别家族 |
| Gate B–E | 实际被测 Agent | 检测、反馈利用、适应恢复和程序自治能力 |

因此 DeepSeek、Claude 或任何参赛 Agent 的失败不会使 A3 重新定义，也不会把环境自动判成不可识别。
A3 的正式名称是 **Online attainability certificate**；参赛 Agent 从 Gate B 开始评分。

## 校准后的在线变化语义

```text
truth change time ∈ {never, 6, 8, 10}
total experiment horizon = 18
relative checkpoints k ∈ {1, 2, 4, 8}
```

`τ=6` 只表示前六个完整实验使用旧世界，第七个实验才可能进入新世界。策略只知道总 horizon，以及
世界可能保持不变或在未指定时刻变化。最短稳定前缀、候选变化时点、真值、reference certificate、
pseudo-checkpoint 和当前相对 checkpoint 均不进入策略上下文。

`never` 是一等真值。它的 pseudo-checkpoint 只存在于 evaluator，不触发新的环境事件，也不改变
instance ID、metadata、reset 规则或随机数流。

## A3 的参照不是六个动作 ID 清单

冻结的六动作 recipe 是可复现的 **canonical witness set**，不是唯一合格答案。Reference certificate
依据的是 **relation closure**：

- varied fields 和 controlled background 是否满足关系定义；
- rate-law 或构成律的 low/pivot/high 是否形成；
- topology 与材料映射所需的同背景对照是否闭合；
- 可观察 signature 的拟合信息是否非饱和；
- 参照是否仍在冻结的 age limit 内。

未来策略可以使用不同的连续剂量或扫描点，只要同样闭合声明关系并通过预测充分性检查，就不会因为没有
调用 `design-00` 到 `design-05` 而失败。

## 预测充分性不再由全局模型循环认证

Development cohort 只冻结：

- 特征编码；
- 预测模型族；
- action selection 规则；
- 误差阈值。

每个 A3 campaign 使用自己的 pre-change 观测估计 nuisance reference 参数，并执行
leave-one-experiment-out cross-fitting。被留出的旧世界观测不能参与自身参数估计；post-change 观测和
真实 family 标签完全禁止进入 reference fit。报告同时保留标准化平方误差、预测 log score 和 95%
prediction-interval coverage。

## Changed 与 never 使用不同分母

令 `R` 为参照充分，`D_change` 为变化报警，`A` 为变化家族归因正确。

Changed campaigns 报告：

```text
P(R | changed)
P(D_change | R, changed)
P(A | D_change, R, changed)
P(R ∧ D_change ∧ A | changed)
```

No-change campaigns 报告：

```text
P(R | never)
P(no false alarm | R, never)
FPR_horizon = P(八个实验窗口内曾经报警 | never)
```

`never` 没有可归因的变化家族，因此不会进入 `P(A|D,R)` 的分母。Reference failure 只从条件归因分母
排除，在 changed 端到端成功率中仍按失败保留。

## 时序检测指标

在 `k={1,2,4,8}` 分别报告：

- Recall(k)；
- AUROC(k)；
- Brier(k)；
- 与相同 pseudo-checkpoint 窗口配对的 no-change FPR(k)。

主 Brier 指标先对 changed/never 两类等权，再对四个 checkpoint 等权求均值。检测事件冻结为：

```text
T_D = min{k : p(change) >= 0.5}
```

到 `k=8` 仍未检测的 changed campaign 按右删失记录，不赋值为 8、无穷大，也不从数据中删除。FPR
使用 horizon 内“曾经越阈”的事件，不能用终点 posterior 回落来抹去早期误报。

## 样本量与独立性

正式 RC28 沿用 RC27 的世界、cohort 与统计设计并冻结为：

- A2、A3、Private-E 和 Private-A：每个任务/家族各 180 个独立 world-seed cluster；
- 每个 changed family 在 `τ={6,8,10}` 上严格平衡为每个时点 60 个 cluster；
- 每个任务有 180 个 `never` cluster；
- provider repeat 为每个配对 cell 5 次，但只作为嵌套技术重复，不作为独立样本；
- cluster bootstrap 单位是 `task_id + world_seed`。

功效审计显示，30 个 cluster 在真实 reference 成功率 0.90 时，通过 Wilson 下界 0.80 的概率仅约
0.18。180 个 cluster 将该概率提高到约 0.964；在真实 recall=0.90 和 FPR=0.05 时，通过冻结
cluster-bootstrap 规则的概率分别约为 0.978 和 0.808。真实 reference 成功率仅 0.85 时功效仍有限，
该限制在审计中明确保留。

## 严格配对的 no-change 对照

同一 changed/never twin 共享：

- 初始状态和 world seed；
- pre/post session 边界与 reset 规则；
- 完全相同的 pre-change action schedule；
- 每个共同语义坐标上的相同 observation-noise key，即 common random numbers；
- checkpoint 前后的 metadata 结构。

两臂唯一允许的差别是是否施加隐藏物理规律变化。Evaluator pseudo-checkpoint 没有 runtime side effect，
Agent 看不到 reset 或 instance 标识。自适应策略在 post-change 后可能选择不同动作，因此不要求两臂
拥有完全相同的后续噪声坐标集合；只要求所有共同坐标的噪声 key 一致。

## RC28 的关系预算证书、执行硬化与 Agent 上下文

RC27 的正式执行暴露出一个此前设计审计未覆盖的矛盾：电化学任务要同时闭合 constitutive
low/pivot/high、solvent pair 与 electrolyte-profile pair，最少需要 5 个不同动作，primary
budget=4 不可行。RC28 保留 A2 的 `k=2`、`k=4` 诊断点，并新增最小可行的 `k=5` 作为 primary
certificate；A3 的 `k={1,2,4,8}`、online horizon=8 与 reference policy 不变。83 项设计审计
现在为每个任务生成关系并集最小覆盖 witness，并在任何 formal scheduler 前验证预算可行性。

RC28 同时保留 RC25–RC27 的执行硬化：A3 的 576 个 predictive-fit 单元与 1,440 个在线 trial
合计为 2,016 个 receipts；A2 在三个 checkpoint 下合计为 4,896 个 receipts。receipt 是执行
与恢复单元，不是独立样本：A2 的三个预算复用同一组 360 个 held-out task × world clusters，
A3 使用另外 360 个 confirmatory clusters，两者无交集。除此之外：

- 每个 `task × truth × world cluster × changepoint × arm` 只允许一个 write-once terminal receipt；
- 基础设施失败进入独立 attempt ledger，恢复时只补缺失 trial，不重跑已完成单元；
- A3 先运行时只公开结构完整性 receipt；A2 完成后才一次性发布联合 A2/A3 决策和科学表；
- 观测噪声由实验号、操作、仪器和 replicate 的语义坐标派生，不再依赖分支路径消耗了多少 RNG；
- Private confirmation 拆成环境复现 Private-E 与 Agent 矩阵复现 Private-A。

Participant-Agent 的默认决策 prompt 使用 `chemworld-compact-decision-context-0.3`。50 个最坏合法
fixture 给出的 development cap 为：共享 environment view 2,050，Direct 总 prompt 3,600，
Stateful v0.4 总 prompt 4,150 estimated tokens。它只包含当前决策所需的任务、生命周期、预算、
指标、测量摘要、约束、短期记忆和动作参数签名；完整谱图数组、replicate 曲线、重复 observation view、constitution checks 与
Git/provider/ledger 元数据只进入审计轨迹。历史谱图可通过公开 `spectrum_id` 按需获取。

## 分层通过规则

A3 最终采用交集规则：

1. overall 通过；
2. Reaction to Crystallization 单独通过；
3. Electrochemical Conversion 单独通过；
4. 每个 changed family 单独通过；
5. macro-average 通过。

Pooled micro-average 仅作补充，不能用一个容易任务掩盖另一个任务，也不能用容易 family 掩盖局部
不可识别性。

## Gate B–E 的证据边界

当前设计审计未发现 Gate C–E 存在旧 A3 的前置条件混淆，但它们的**经验有效性仍待正式执行**：

- Gate B 评价参赛 Agent 的时序检测与校准；
- Gate C 仍需验证相同前缀的反馈局部配对和完整 campaign 的 provider 噪声；
- Gate D 仍需验证 frozen-policy、adaptive-policy 与 oracle 的严格冻结；
- Gate E 仍需确认 assisted history 不污染后续 autonomous 实验。

语义审计通过不等于这些 Gate 已通过。

第一轮正式实验采用四方法 `2×2` 因子设计：Pro/Flash 两个 backend 分别运行 direct reactive
与 stateful scientific 两种 scaffold。该设计同时估计 backend、scaffold 和交互效应，只需新增
一个 stateful scientific scaffold；ReAct 与 planning-memory 延后为有针对性的消融或补充，
不阻断第一轮。当前 `live_llm_a/live_llm_b` 同时改变 backend、thinking 和 controller，只能
保留为 development pilot，不能直接形成正式模型或 scaffold 效应。完整实施顺序和临时 TODO
已收束到仓库内的 RC28 Participant 正式实验主计划。

## 单一预注册入口

启动 A2/A3 前，唯一控制文件是：

`configs/benchmark/mechanism-adaptation-preregistration-v0.3.0-rc28.json`

它绑定 source commit、protocol/plan/relation/scorer hash、cohort namespace、样本量、reference-policy
版本、阈值、checkpoint、bootstrap、分层规则、失败处理、排除、停止规则和 private unseal 条件。
任何绑定项变化都必须产生新的 RC，不能回写解释已经采集的结果。

## 可审计入口

- 协议：`configs/benchmark/mechanism_adaptation_v0.3.0_rc28.json`
- Gate A 计划：`configs/benchmark/mechanism_adaptation_gate_a_v0.3.0_rc28.json`
- 预注册：`configs/benchmark/mechanism-adaptation-preregistration-v0.3.0-rc28.json`
- 样本量审计：`mechanism-adaptation-sample-size-audit-v0.3.0-rc28.json`
- 诊断关系图：`mechanism-adaptation-diagnostic-relation-graph-v0.3.0-rc28.json`
- 统一语义审计：`confirmatory-task-semantics-audit-rc28.json`
- 发布资格：`mechanism-adaptation-release-qualification-v0.1-rc28.json`
- A2 结构回执：`mechanism-adaptation-a2-structural-receipt-v0.1-rc28.json`
- A3 结构回执：`mechanism-adaptation-a3-structural-receipt-v0.1-rc28.json`
- 联合公开决策：`mechanism-adaptation-public-decision-v0.1-rc28.json`
- Participant-Agent 预注册候选：`configs/benchmark/mechanism_adaptation_participant_preregistration_rc28.json`
- Gate A 运行后审计：`RC28_GATE_A_POSTRUN_SANITY_AUDIT_ZH.md`
- Participant 正式实验计划：`RC28_PARTICIPANT_FORMAL_EXPERIMENT_PLAN_AND_TODO_ZH.md`
- Stateful Scientific 实现规格：`STATEFUL_SCIENTIFIC_AGENT_V0_1_SPEC_ZH.md`
- 当前状态真源：`configs/current.json`
