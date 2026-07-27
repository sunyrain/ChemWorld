# RC28 之后的 Participant-Agent 科学适应实验计划与 TODO

> 2026-07-25 已完成 S0 最坏 prompt qualification、Flash-Direct S1 和
> Flash-Stateful v0.4 S2，见
> `RC28_PARTICIPANT_EXECUTION_QUALIFICATION_RESULTS_ZH.md`。生命周期计数与 prompt
> envelope 阻断均已修复；两种 operation-level scaffold 在干净的 autonomous
> `1 pre + 1 post` pair 中仍为 0/4 completion。该结果只归入 O4 Procedural autonomy，
> 不再用于判定 Agent 是否具备科学适应能力。S3、Pro 与正式矩阵保持未启动。

状态：`Gate A frozen; r4 two-task real-provider pilot completed with 3 method failures; formal execution blocked`

适用环境：`mechanism-adaptation-v0.3.0-rc28-gate-a-passed`

本计划组织 Participant Outcomes O1–O5、独立 Autonomous Procedure Track 与最终 private
confirmation。RC28 的 A1/A2/A3
已经完成并冻结；不得因 Agent 结果、成本或开发便利修改 Gate A 的世界、动作、预算、阈值、
cohort、scorer 或公开联合决策。

新的 experiment-level development candidate 位于：

- `src/chemworld/agents/scientific_adaptation.py`；
- `src/chemworld/eval/scientific_adaptation_execution.py`；
- `src/chemworld/eval/participant_outcomes.py`。

旧 `StatefulScientificMechanismAgent` 与 0/4 smoke 保留为 Autonomous Procedure Track 的开发
证据，不再继续膨胀为科学主接口。

## 1. 正式研究问题

正式实验回答的是：

> 在相同的物理实验预算、可见状态和反馈接口下，不同 Agent scaffold 与不同 backend
> 能否建立旧世界参照，检测和归因隐藏规律变化，并通过后续实验恢复任务表现？

它不再回答“环境是否可识别”。该问题已经由 A1/A2/A3 回答。

正式科学主实验按五类 Outcomes 报告，其中 O4 由独立 Track 产生：

| Outcome | 主要问题 | 估计量角色 |
| --- | --- | --- |
| O1 Detection | Agent 是否检测并归因真实变化 | AUROC/Brier/recall/FPR/delay 与 family attribution |
| O2 Feedback use | 实验反馈是否因果改变判断和下一实验 | identical-prefix response 与小型 campaign utility subset |
| O3 Adaptation/recovery | Agent 是否在变化后恢复任务表现 | **post-change adaptation regret AUC（唯一主终点）** |
| O4 Autonomy | Agent 是否能自主完成 operation-level 生命周期 | protocol-failure rate 与 assisted scientific score |
| O5 Resource efficiency | 获得结果使用了多少资源 | experiments/measurements/risk/calls/tokens/cost/time |

Agent 的负结果是正式结果，不反向推翻 `benchmark_ready=true`，也不得通过事后换模型、换
seed、加轮次或改阈值“修复”。

## 2. 专家建议的采纳结论

| 建议 | 判断 | 落地方式 |
| --- | --- | --- |
| A3 认证 reference policy，不认证参赛 Agent | 已满足 | A3 保持冻结；参赛 Agent 从 O1–O5 开始 |
| changed 与 never 分母分离 | 已满足 | participant runner 复用同一统计语义 |
| `k={1,2,4,8}` 的时序定义与右删失 | 已满足环境侧 | O1/O3 原样复用，不只看终点 |
| reference 用 campaign 内 pre-change cross-fit | 已满足 A3 | Participant 不能读取 A3 reference certificate |
| relation closure 而非 recipe-ID checklist | 已满足 | 不再修改 Gate A |
| 明确 receipts 与独立 clusters | 新增完成 | 见 `RC28_GATE_A_POSTRUN_SANITY_AUDIT_ZH.md` |
| 审计 oracle/decoder 98.26% 重合 | 新增完成 | decoder 降格为辅助一致性检查 |
| 正交比较 backend 与 scaffold | 必须新增 | 使用四方法 `2×2` 因子矩阵；C1 为唯一主假设 |
| 主接口改为 experiment-level plan | 已新增开发候选 | Agent 选完整实验，deterministic executor 只执行 |
| Gate B–E 改称 Outcomes | 已新增兼容层 | 旧 artifact 可映射到 O1–O4，O5 独立报告 |
| bounded evidence summary | 已新增开发候选 | 真实 evidence ID、去重、条数与 JSON 长度上限 |
| Private-E/Private-A 保持 sealed replication | 保留 | public 方法冻结和执行完成后一次性运行 |
| 不先把 benchmark 称为“困难” | 采纳 | 等 participant 结果后再描述经验难度 |

## 3. 当前方法为什么还不能正式运行

当前 development freeze 同时包含：

- `live_llm_a`：`deepseek-v4-pro`、thinking on、deliberative controller；
- `live_llm_b`：`deepseek-v4-flash`、thinking off、direct controller。

该比较同时改变 backend、inference configuration 和 scaffold，不能识别任何单一因素。
现有 `campaign`/`pilot-report` 入口也明确写入 `formal_result=false`，且它们实现的是
operation-level controller。experiment-level scientific adaptation 已有独立 development candidate，
但尚未接入 manifest-driven formal runner，也尚未完成 provider shakedown 和成本冻结。

ReAct 与 planning-memory 是可选中间架构，不再是第一轮正式实验的启动条件。它们的边界
容易因规划频率、反思次数、记忆长度和内部 retry 发生漂移；如果 stateful 方法产生明确增益，
更适合通过删除 notebook、belief state、plan 或 lifecycle manager 的预注册消融解释增益来源。

因此当前正确状态是：

```text
Gate A: passed and frozen
Scientific Adaptation development interface: implemented
Participant methods: not frozen
Manifest-driven formal Outcome runner: incomplete
Formal participant execution: prohibited
```

## 4. 正式四方法 `2×2` 因子矩阵

第一轮只比较两个 backend 与两个 scaffold：

| Method | Backend | Scaffold | 作用 |
| --- | --- | --- | --- |
| M1 | `deepseek-v4-pro` | direct reactive | 强 backend 的反应式基线 |
| M2 | `deepseek-v4-pro` | stateful scientific | Pro 上的 scaffold simple effect |
| M3 | `deepseek-v4-flash` | direct reactive | Flash 上的反应式基线 |
| M4 | `deepseek-v4-flash` | stateful scientific | Flash 上的 scaffold simple effect |

该设计一次性估计：

```text
C1 = Stateful - Direct                    # scaffold 主效应
C2 = Pro - Flash                          # backend 主效应
C3 = (Pro_Stateful - Pro_Direct)
     - (Flash_Stateful - Flash_Direct)    # backend × scaffold 交互
```

其中只把 `C1` 冻结为主假设；`C2` 是确认性次假设；`C3` 是探索性或经多重校正的次假设。
两个 scaffold simple effects 和两个 backend simple effects用于解释异质性，不替换 C1。

新增的 M3 是最轻量的一格，却能防止以下不完整解释：

- 只知道 scaffold 在 Pro 上有效，却不知道 Flash 能否使用它；
- 只知道 backend 在 stateful 下不同，却不知道 direct baseline 中是否同样不同；
- 无法判断弱模型还是强模型更受益于结构化科学状态。

“Agent 更强”不得通过不可见人工帮助、自动动作修复或 harness 代替科学选择实现。

### 4.1 Direct Reactive 的公平合同

Direct 与 Stateful 必须共享：

- 同一 compact observation adapter；
- 相同候选机制名称与公共定义；
- 相同谱图/动作 schema/历史 retrieval 工具；
- 相同可见实验历史与原始公开反馈；
- 相同物理实验预算、measurement cost 和 lifecycle rules；
- 相同 model-specific provider 参数，除了 scaffold 必需的调用组织差异。

Scientific Adaptation Track 中 Direct 每个 experiment 只进行一次决策调用，输出完整实验计划，
不维护显式持久科学状态；但不能故意给它更脏的 prompt、更少的公共信息或更差的实验 schema。
否则观察到的不是 scaffold effect，而是输入质量差异。

这里的 Direct 不是 history-blind：它读取与 Stateful 完全相同的压缩实验历史和 evidence
catalog。`direct` 的准确含义是没有额外的 Agent 自写持久 scientific state；正式报告不得把它
描述成“没有历史”的弱化基线。

### 4.2 Stateful Scientific 的允许能力

Stateful 只比 Direct 多获得一份 bounded Agent-authored state：

Harness 只提供字段和状态机，不填写其中的科学内容。允许的结构示例：

```json
{
  "belief": {},
  "unresolved_question": "...",
  "next_experiment_plan": {
    "intent": "...",
    "controlled_variables": [],
    "varied_variable": "..."
  },
  "evidence_summary": [
    {
      "evidence_id": "exact-public-id",
      "observation": "...",
      "interpretation": "...",
      "reliability": "high"
    }
  ]
}
```

每条 evidence 必须引用共享公共历史中的真实 ID；重复 ID、越界条数和超长状态均 fail closed。
`closeout_intent` 不属于该 state，因为 Scientific Adaptation Track 的 closeout 是 executor 的
机械职责。

严禁向 stateful scaffold 提供：

- hidden truth、实际 changepoint 或 changepoint support；
- Gate A reference certificate、posterior 或 oracle likelihood；
- diagnostic relation graph 中的真实机制 signature；
- 候选世界 rollout 或未来观测理论分布；
- family-specific 固定最优动作；
- 任何由 harness 代写的机制判断或实验结论。

核心边界是：

> Scaffold 提供认知结构，不提供科学答案。

必须增加 leakage audit，证明 Stateful 与 Direct 接收同一公共环境信息，新增字段只来源于
Agent 自身先前输出和公开 observation。

### 4.3 中间 scaffold 与单轮基线的位置

Explicit ReAct 和 planning + memory 不进入第一轮 core matrix，也不阻断正式启动。若 core
matrix 出现稳定 scaffold effect，优先做 stateful component ablation；只有在有明确科学问题时
才新增中间 scaffold。

单轮/open-loop recipe proposer 可以作为补充描述性基线，用于和材料发现中的一次性提案系统
比较，但不替代 direct 基线，也不控制 O1–O5。若加入，必须在正式冻结前实现，
且不得在看到 formal 结果后追加。

## 5. Experiment-level 决策接口

每个物理实验前只调用一次 Agent。Direct 与 Stateful 共享的公共部分包含：

- 任务目标、公共 candidate definitions 和剩余物理实验预算；
- task-aware unit-vector recipe space、维度和 categorical coordinates；
- 固定位置的可选 diagnostic measurement slots；
- 相同的压缩实验历史、terminal summaries 与 public evidence catalog；
- 固定机械 closeout：`terminate` 后 `final_assay`。

Agent 输出 `experiment_intent`、严格位于 `[0,1]` 且长度匹配任务的 `search_vector`、显式选择的
`requested_measurement_slots`、diagnostic target、mechanism distribution、expected effect、
belief update rule 和 uncertainty。只有 Stateful 返回 bounded `scientific_state`。

deterministic executor 只负责把向量交给现有 task recipe compiler、删除未选择的 diagnostic
slots、执行固定合法顺序和机械 closeout。越界向量、未知 measurement slot 或非法 state 一律
拒绝，不 clipping、不修复、不补充诊断测量，也不更新机制判断。

默认禁止进入模型决策上下文：完整 raw arrays、同一 observation 的多份表示、constitution
checks、Git/provider/ledger 元数据、Gate A relation graph、reference certificate、oracle
signature、hidden truth 和 candidate-world likelihood。

正式冻结必须约束唯一 interface version、两种 scaffold 相同的 public-context hash/token cap、
Stateful 额外 memory cap、per-experiment/campaign token ceiling、provider-reported usage 和
on-demand retrieval 预算。模型输出不接受冗长 rationale 或未声明字段。

## 6. 两条独立 Track

### 6.1 Scientific Adaptation Track

主 campaign 使用 experiment-level interface，并在同一组冻结 world clusters 跨 method 配对：

- 两个 Confirmatory Tasks；
- 每个任务三个 changed families 加一个 `never` truth；
- changed 与 never twins 共用相同初始世界、pre-change prefix、reset 语义与可对齐噪声坐标；
- changepoint 从 `{6,8,10}` 冻结分配；
- post-change checkpoints 为 `k={1,2,4,8}`；
- 所有方法具有相同物理实验预算；
- provider repeats 是同一物理 cluster 内的技术重复，不增加独立样本数。

同一条 scientific trajectory 同时产生 O1、O3 和 O5 所需结果。O2 local-prefix fork 复用冻结
公共前缀，完整 feedback utility 只运行预注册小型 subset。

### 6.2 O2 Feedback use 的两层设计

局部 identical-prefix test 冻结完全相同的历史前缀，只替换最后一次反馈为 true 或 permuted，
比较 belief JS divergence、true-family probability shift、下一实验 disagreement 与参数距离。
delayed 和 critical-measurement-deleted 只作为解释性条件。

完整 campaign utility test 只在少量代表性 world clusters 上运行 true vs permuted。它是机制
验证，不复制主矩阵；局部行为敏感性和长期效用分别报告。

### 6.3 Autonomous Procedure Track

旧 operation-level Direct/Stateful controller 独立测量 O4：非法动作、terminate、final assay、
生命周期完成率和 assisted scientific score。当前 Flash Direct/Stateful 的 0/4 归入本 Track；
它不能阻断 Scientific Adaptation Track，也不能作为“没有科学适应能力”的证据。

## 7. 统计单位、候选规模与样本量审计

唯一独立统计单位保持：

```text
independent unit = task × world_cluster
```

truth twins、changepoint arms、feedback conditions、methods 和 provider repeats 都是 cluster 内
配对或嵌套观测。主置信区间使用 world-cluster bootstrap；provider repeat 只估计技术噪声。

现有每任务 60 个 clusters、四 method cells、三个 provider repeats 的 5,760-arm 数量只保留为
power/cost audit 上界，不是批准预算。冻结前必须模拟 adaptation regret AUC 的 CI 稳定性、C1
最小可检测效应、C2/C3 次级覆盖率、provider/world 方差、失败率和总成本。不得根据 formal
interim results 增补样本或减少昂贵方法的重复。

## 8. Outcome 估计量与报告规则

Participant 主实验只冻结一个 primary endpoint：

```text
post-change adaptation regret AUC at k={1,2,4,8}  # 越低越好
```

reference 是同一 shifted world 上冻结的 diagnosis-oracle policy。C1 在该终点上是唯一主假设；
C2 是确认性次假设；C3 是探索性或经多重校正的次假设。其他 Outcome 指标只用于解释恢复
机制，不能替换不利的主终点。

### O1 Detection

- changed：`Recall(k)`、`AUROC(k)`、`Brier(k)` 和 detection delay；
- never：对应 pseudo-checkpoint 后窗口 FPR 与 horizon FPR；
- family attribution：top-1、true-family probability 与 confusion matrix；
- changed-only recall 和 never FPR 分母分离报告。

### O2 Feedback use

- local sensitivity 与 small full-campaign utility 是两个独立 estimands；
- paired history prefix 是因果比较的必要条件；
- between-condition effect 与 within-provider-repeat noise 并列报告；
- 负效应不能直接解释为“错误反馈更好”。

### O3 Adaptation and recovery

- 比较 adaptive participant、frozen policy、IID action replay、diagnosis oracle；
- 主报告 post-change adaptation regret AUC；
- 同时报 raw task regret、task-normalized regret、best-so-far recovery curve 和
  adaptive-frozen paired difference；
- normalized recovery 仅为 secondary；低 oracle-headroom cell 标为 non-informative，保留原始分数；
- 区分“不更新”“更新慢”“识别后仍不能恢复”。

### O4 Procedural autonomy

- 只在独立 Autonomous Procedure Track 中禁止 harness 强制 closeout；
- terminate、final assay 或生命周期失败计入 protocol failure；
- assisted scientific score 单独生成，且 assisted history 不进入后续 autonomous context。

### O5 Resource efficiency

统一报告 experiment count、measurement count、risk、provider calls、tokens、cost 和 wall time。

O1–O5 可以得到负结果；`evidence_complete` 取决于是否按冻结协议完整执行和报告，不要求 Agent
通过性能阈值。participant performance 不控制 release readiness。

## 9. Provider、失败与成本合同

正式 freeze 必须记录：

- 精确 model ID、provider endpoint、access date 与模型版本语义；
- temperature/provider seed 支持、thinking/reasoning 配置；
- 每 decision 与每 campaign 的 max tokens、attempts、timeout、backoff；
- 每 method 的 calls、input/output tokens、cache usage、美元成本和 wall time 上限；
- invalid action、schema error、provider timeout、rate limit、refusal 和 infrastructure failure 的
  reason codes；
- infrastructure failure 的 missing-only resume；
- 科学失败、invalid plan、invalid action 和 lifecycle failure 不得被自动重试成成功；
- Scientific Adaptation Track 只允许冻结 recipe compiler 的机械 closeout；Autonomous Procedure
  Track 的自动动作修复和自动 closeout 均为 false。

执行调度还必须冻结：

- 四个 method cells 在每个 world/repeat 内按公开 scheduler seed 的哈希顺序交错运行；
- 不允许先完整跑完一个 backend 或 scaffold 再运行另一个；
- 每个 cell 的 prompt state、provider conversation 和 retrieval archive 完全隔离；
- 同一 backend 的 Direct/Stateful 使用相同 thinking、temperature、max output tokens、
  timeout、attempt 和 provider-seed policy；
- provider 不提供可控 seed 时，以 repeat index 作为嵌套技术重复标签，不伪称确定性配对；
- 记录 provider model ID、system fingerprint、访问时间和服务异常；运行期间模型别名发生
  可检测变化时 fail closed，不把跨版本结果合并成同一 cell。

在用户批准总成本上限前，不启动正式 provider matrix。

## 10. 执行阶段与临时 TODO

### Phase P：Gate A 收束

- [x] `P-01` 固化 A2/A3 联合公开决策。
- [x] `P-02` 核对 receipt、trial 与独立 cluster 口径。
- [x] `P-03` 审计 active oracle/fixed decoder 的错误重合与调用链。
- [x] `P-04` 明确 fixed decoder 是非控制性辅助检查。
- [ ] `P-05` 在论文提交前决定是否运行 detached full-suite/wheel/replay attestation。

### Phase M：方法实现

- [x] `M-01` 新增组合式 experiment-level Direct development scaffold。
- [x] `M-02` 新增 bounded Stateful scientific memory development scaffold。
- [x] `M-03` 统一 Direct/Stateful 的 public context、experiment schema 与 validator。
- [x] `M-04` 实现 belief/question/next-plan/evidence-summary 的 bounded validation。
- [x] `M-05` 测试 public-context hash 相同且 scientific state 不进入共享历史。
- [ ] `M-06` 核验并冻结已有 spectrum-ID retrieval；补齐按 ID 请求 schema/history 的公开工具。
- [x] `M-07` 实现 evidence ID、去重、条数、字符上限与无效响应原子拒绝。
- [x] `M-08` 为两种 scaffold × 两个 backend cells 增加 deterministic mock-provider、receipt、hash binding、硬 prompt 预算与 resume tests；r4 双任务 `6 pre + 2 post` 共 128/128 experiments 通过。
- [ ] `M-09` 将 ReAct/planning-memory 明确标为 deferred supplemental，而非 formal blocker。

### Phase R：正式 runner

- [ ] `R-01` 新增 manifest-driven formal Outcomes stage；不复用 `formal_result=false` pilot 输出。
- [ ] `R-02` materialize 完整 formal cohort，而不是 public seeds 0–4。
- [ ] `R-03` 实现跨 method 的 common-world pairing 和 keyed observation noise。
- [ ] `R-04` 实现 write-once campaign receipts、attempt ledger 与 missing-only resume。
- [ ] `R-05` 实现 O1 时序表、右删失与 calibration。
- [ ] `R-06` 实现 O2 identical-prefix fork 和小型 utility subset。
- [ ] `R-07` 实现 O3 regret AUC 与 frozen/replay/oracle comparators。
- [ ] `R-08` 保留 O4 autonomous/assisted 独立 runner 且隔离 history。
- [ ] `R-09` 实现 reason-coded failure/exclusion/resource ledger。
- [ ] `R-10` 从 receipts 重建所有表并逐位 replay。
- [ ] `R-11` 实现四 method cells 的哈希交错调度和完全隔离的 prompt/provider state。

### Phase D：只使用 development cohort

- [x] `D-01` r3 v7 四方法最小 shakedown 8/8 cells、16/16 experiments 完成。
- [x] `D-02` Pro/Flash 使用同一 Stateful schema；r3 v7 两个 backend 均通过最小运行资格。
- [x] `D-03` v7 核对 provider prompt tokens；Direct/Stateful 最大 2,322/2,898，低于 3,600/4,150 cap。
- [x] `D-03a` r4 双任务扩大时域 mock 16/16 cells、128/128 experiments 完成；Direct/Stateful 单一历史表示最大 5,434/6,157，低于独立冻结 cap 6,250/7,100；resume 不改变 terminal receipts。
- [x] `D-03b` 按 r4 输入与 v7 真实输出完成 128-call 成本预审：均值情景 USD 0.285703，全部打满 output cap 的保守情景 USD 0.577598；用户批准 development stop cap USD 0.75。
- [x] `D-03c` r4 双任务真实 provider pilot 产生 16/16 terminal cells：13 completed、3 method failures、115/128 experiments、118 calls、121 attempts、USD 0.4027606358；零 infrastructure failure，resume 不改变 receipts。
- [x] `D-03d` WellAU `gpt-5.6-sol` high 单 backend development pilot 产生 8/8 terminal cells：6 completed、2 Stateful method failures、59/64 experiments、61 calls/attempts、354,357 provider-reported tokens；零 infrastructure failure。定价不可验证，`accounting_complete=false`、USD cost unknown；resume/hash/prompt/key-leak 审计通过。
- [ ] `D-04` 补齐 provider/world 方差与 wall-time 分解；首轮真实 calls/tokens/cost/failure 已记录，但一个 pair/task 不足以估计独立方差。
- [ ] `D-05` 围绕 C1 主假设完成 power audit，并审计 C2/C3 次级覆盖率和总成本。
- [ ] `D-06` 冻结 oracle minimum gap、exclusions 和所有 aggregation。
- [ ] `D-07` 删除仅为调试添加的 Agent 可见字段；确认 phase/reset/changepoint 不泄露。
- [ ] `D-08` 冻结 O2 prefix bank 与 full-campaign representative subset。

### Phase F：一次性方法预注册

- [ ] `F-01` 冻结四个 `2×2` method cells、C1 主假设及 C2/C3 次级角色。
- [ ] `F-02` 冻结 prompt、tools、memory、provider config 与每 method 资源上限。
- [ ] `F-03` 冻结 formal/public/private namespaces、样本量和 provider repeats。
- [ ] `F-04` 冻结 regret AUC 主终点与 O1–O5 secondary estimands。
- [ ] `F-05` 冻结 invalid/incomplete/provider failure 和 exclusion 处理。
- [ ] `F-06` 生成单一 hash-bound Participant-Agent preregistration manifest。
- [ ] `F-07` clean detached qualification；只允许修复 infrastructure bug，不得查看 formal metrics。
- [ ] `F-08` 用户批准不可突破的总 provider 成本上限。
- [ ] `F-09` 冻结 C2/C3 和 simple effects 的 multiple-comparison policy。

### Phase X：正式 public execution

- [ ] `X-01` 一次性 materialize 全矩阵并记录 expected unit count。
- [ ] `X-02` 先完成 Scientific Adaptation 主 trajectories，再完成 O2 prefix forks 和 O4 独立 Track。
- [ ] `X-03` 不查看 interim task/family/method 排名，不做 optional stopping。
- [ ] `X-04` 只按 missing-only 规则恢复基础设施失败。
- [ ] `X-05` 完整性达到 100% 后一次性解封正式表。
- [ ] `X-06` result-only commit；不得同时修改方法、scorer 或协议。

### Phase V：private confirmation

- [ ] `V-01` Private-E 在未触碰 namespace 上一次性复现环境证书。
- [ ] `V-02` Private-A 使用完全冻结的 participant matrix 一次性复现。
- [ ] `V-03` Private-E 不用于修改 participant 方法，Private-A 不用于修改阈值。
- [ ] `V-04` public/private 结果并列报告；private failure 保留为负结果。

## 11. 正式启动的 go/no-go

只有以下条件全部为 true，才允许启动正式 provider matrix：

```text
gate_a_pass == true
method_roster_frozen == true
backend_scaffold_axes_unconfounded == true
formal_runner_complete == true
compact_prompt_contract_verified == true
development_only_shakedown_passed == true
world_cluster_power_audit_passed == true
cost_ceiling_approved == true
participant_preregistration_hash_bound == true
Private-A remains sealed == true
```

当前只有 `gate_a_pass` 已正式冻结。r4 已为 `backend_scaffold_axes_unconfounded`、
`compact_prompt_contract_verified` 和 `development_only_shakedown_passed` 提供 mock 加真实 provider
证据；额外 WellAU 单 backend pilot 又产生两个 bounded-state method failures，但不改变 frozen formal
roster。现有 contract failures、replay 缺口与尚未 hash-bound 的 preregistration 使其仍不能升级为
formal go。下一步不是消耗 formal seeds，而是依次完成剩余 Phase M、R、D 和 F。

真正阻断第一轮 provider matrix 的只有：

1. experiment-level interface 尚未接入统一 formal manifest runner；
2. 双任务扩大时域真实 provider pilots 已完成，但 DeepSeek 三个和 WellAU 两个 method failures 的 contract sensitivity、失败处理冻结与 replay qualification 尚未完成；
3. 围绕 C1 主假设的 power/cost audit 尚未通过；
4. participant preregistration 尚未冻结并 hash-bound。

ReAct、planning-memory 和完整五方法梯度均不在该列表。

`api.md` 中旧凭据已轮换。r4 真实 pilot 只将新 key 注入执行进程环境；进程结束后环境变量已移除，
17 个实验 artifact 文件的通用 key pattern 命中为 0。后续外部调用仍必须采用相同的进程级注入，
不得把 key 写入 manifest、receipt 或日志。
WellAU pilot 同样只使用进程级 key 注入；9 个真实 artifact 文件的精确 key 与通用 key pattern 命中
均为 0。其认证模型目录未提供定价，因此 354,357 实验 tokens 加 329-token 兼容探针只能报告 usage，
不能伪造 USD 成本。本轮 Process-scope 注入已在 `finally` 中清理；工作站预存的同值 User-scope
`WELLAU_API_KEY` 不是本轮创建，按主任务要求保留，不计为 runner 进程残留。

## 12. 最终论文表格

至少生成：

1. Gate A 环境证书与 compact readiness；
2. receipt、trial、independent cluster、provider repeat 四种计数；
3. backend × scaffold 方法与资源合同；
4. O1 的 task/family/time calibration 表；
5. O2 的 local response 与 small campaign utility 两张表；
6. O3 的 regret AUC 与 adaptive/frozen/replay/oracle recovery curves；
7. O4 的 autonomous/assisted 与 protocol failure 表；
8. C1 主结果、C2/C3 次结果、cluster CI 与 simple effects；
9. calls/tokens/cost/wall-time–performance Pareto；
10. public 与 Private-E/Private-A replication；
11. 所有 negative、incomplete、invalid 和 infrastructure outcomes。

在 participant 结果出来前，项目可以声称环境在线可达，但不能声称任务对通用 Agent 很难、
DeepSeek 缺少机制发现能力，或某种 deep-agent scaffold 优于单轮基线。
