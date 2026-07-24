# 确认性基准任务：设计、预注册与执行状态

> **Showcase Worlds 展示平台广度；Confirmatory Benchmark Tasks 承担确认性结论。两者不再统称为“旗舰”。**

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
| Semantic protocol audit | passed，RC24 25/25 |
| A1 physical validity | passed，RC24 81/81 设计检查 |
| A2 controlled identifiability | pending |
| A3 online attainability | pending |
| Participant-Agent Gates B–E | pending |
| Private confirmation | sealed |
| Publication ready | `false` |

25 项语义检查和 81 项设计检查是两份审计中的检查项，不代表 106 份独立科学证据。当前已经具备可执行、
可预注册的协议，但尚无新的 A2/A3 确认性结果。

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

正式 RC24 冻结为：

- A2、A3 和 private confirmation：每个任务/家族各 180 个独立 world-seed cluster；
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
- action schedule；
- 相同的 observation-noise key，即 common random numbers；
- checkpoint 前后的 metadata 结构。

两臂唯一允许的差别是是否施加隐藏物理规律变化。Evaluator pseudo-checkpoint 没有 runtime side effect，
Agent 看不到 reset 或 instance 标识。

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

## 单一预注册入口

启动 A2/A3 前，唯一控制文件是：

`configs/benchmark/mechanism-adaptation-preregistration-v0.3.0-rc24.json`

它绑定 source commit、protocol/plan/relation/scorer hash、cohort namespace、样本量、reference-policy
版本、阈值、checkpoint、bootstrap、分层规则、失败处理、排除、停止规则和 private unseal 条件。
任何绑定项变化都必须产生新的 RC，不能回写解释已经采集的结果。

## 可审计入口

- 协议：`configs/benchmark/mechanism_adaptation_v0.3.0.json`
- Gate A 计划：`configs/benchmark/mechanism_adaptation_gate_a_v0.3.0.json`
- 预注册：`configs/benchmark/mechanism-adaptation-preregistration-v0.3.0-rc24.json`
- 样本量审计：`mechanism-adaptation-sample-size-audit-v0.3.0-rc24.json`
- 诊断关系图：`mechanism-adaptation-diagnostic-relation-graph-v0.3.0-rc24.json`
- 统一语义审计：`confirmatory-task-semantics-audit-rc24.json`
- 当前状态真源：`configs/current.json`
