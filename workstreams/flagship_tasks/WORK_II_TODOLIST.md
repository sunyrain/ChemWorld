# Work II TODO — 先验、规律发现、偏差排除与迁移

最后更新：2026-08-08
工作边界：第二篇研究在固定世界规律下，无先验、正确先验和错误先验如何影响 agent 的实验发现、错误先验排除、规律总结和 held-out 迁移。它不把“运行中规律变化”作为主要情境，也不重复第一篇的装置可观测性主张。

当前执行冻结：

- 单 executor：`Codex /root`，在 `main` 工作；不建立 review queue、review status 或额外审核包；
- task 认领后进入 `DOING`，满足验收标准即直接标记 `DONE`；
- 当前唯一 participant backend 为 WellAU 提供的 `gpt-5.6-sol`，`reasoning_effort=medium`；
- 当前 participant execution unit 冻结为：每个 `task × prior arm × world seed` cell 只允许一个
  长驻 Codex process/session identity。它继承第一篇 complete-agent 的 operation-level 语义：
  agent 在同一上下文内通过 host-owned `chemworld_lab` MCP 逐次提交 `step(action)`，读取每个公开
  outcome 后再选择下一 operation；禁止把 experiment、snapshot 或 autonomous decision 拆成互不关联的
  standalone API 问答或本地 history 重建；
- 当前 primary participant method 不采用“模型一次生成 complete-experiment plan、deterministic executor
  一次执行到底”的 Static S0 粒度。Static S0 可保留为 calibration/reference control，但不能替代
  operation-level discovery、measurement、termination 和 resource-allocation 行为；
- 每个 Work II cell 同时绑定一个 Codex session 和一个 ChemWorld discovery campaign。campaign 内可包含
  多个 complete experiments/lifecycles；每个 experiment 从新 vessel/batch 开始，以 committed
  `final_assay` 或允许的 discard 关闭。不同 experiments 共享同一 hidden law、agent context 和
  `CampaignResourceLedger`，但 final assay 后下一 batch 的物理状态重新初始化；
- discovery campaign 内所有 participant experiments 共享一张资源卡；operation attempts、vessel starts、
  final assays、non-final instrument uses、stocks、process time、sample、cost 和 risk 均跨 experiment
  累积，不得每个 experiment 重新发放。held-out/blind evaluator 使用独立 sealed campaign 和资源账本，
  不消耗 participant 资源，也不进入 participant process-profile 分母；
- 第一篇冻结的 19 个 process coordinates 作为 evaluator-side operation/campaign profile 复用，不是
  agent belief state，也不要求模型报告。Work II 的 belief snapshot 只记录 prior reliability、预测、
  uncertainty、evidence references、law summary 和 next intent，并在同一个 Codex process 内通过结构化
  MCP checkpoint 提交，不启动额外 provider session；
- 旧的 Direct Responses + 本地 history 重建实现及其报告已归档到
  `workstreams/flagship_tasks/archive/work-ii/direct_responses_reconstructed_history/`，仅作为历史
  transport/schema qualification，不再授权当前方法或科学结果；
- 涉及多 seeds 的实验，默认完成上限为每个适用独立 cell **5 个 world seeds**；未得到用户明确审核扩展前，达到 5 seeds 即视为该实验完成；
- 任何多 seed/provider 执行前必须先完成 mock/deterministic preflight 和更小的真实 provider pilot；
- 初始参考任务范围固定为五项：`electrochemical-conversion`、`reaction-to-crystallization`、
  `reaction-to-distillation`、`partition-discovery` 和 `reaction-safety-constrained`。代码审计确认
  `flow-reaction-optimization` 当前的 catalyst/solvent 类别不产生可识别的类别特异反应规律，主要只进入
  成本/稀释或共享催化剂物种，因此不适合本轮 ID↔property-bundle prior manipulation；它保留为后续
  process-law 扩展候选。五任务是首轮最低广度而非最终上限；pilot 通过后可从 15-task registry 继续加入
  prior-identifiable 任务，但不能把正式范围缩回两项。

### Work II execution semantics and denominators

- **Provider attempt**：同一 session 内一次 provider 技术尝试；失败重试不产生新的科学样本。
- **Session turn/tool loop**：同一 Codex process 内的 observation、reasoning 和 MCP tool interaction；
  session/tool turns 不是独立实验或独立统计样本。
- **Operation attempt**：一次进入 ChemWorld resource preflight 的 `step(action)`；即使 validation、resource
  preflight 或 transaction 失败，也按冻结规则记录 attempt 和相应 reporting debit。
- **Committed operation**：`transaction_status=committed` 的 operation；只有实际 committed outcome 扣除
  对应物理 stock、sample、process time、cost 和 risk，resource-rejected candidate state 不进入物理状态。
- **Complete experiment/lifecycle**：一个新 batch 从首个 vessel-starting operation 开始，经任意次
  process/measurement decisions，到 committed `final_assay` 或允许的 discard 关闭。`terminate` 是 agent
  可在中途选择的 process operation，通常使 final assay 可达；它本身不等同于 final assay。
- **Discovery campaign**：同一 cell 内的多个 complete experiments，共享 fixed world、Codex context 和
  campaign resource ledger。下一 batch 重置物理初态，但保留公开历史、信念、世界规律和剩余资源。
- **Formal cell**：`task × prior arm × world seed × participant method/session`；每个 cell 产生一条纵向
  discovery trajectory 和一个 campaign-level process profile。
- **Independent analysis unit**：独立 world seed/world cluster。operations、experiments、snapshots、held-out
  queries、blind replicates 和 provider repeats 均为 cell 内嵌套观测，不得冒充独立样本。
- 第一篇 19-coordinate producer 的固定六-lifecycle aggregation 不能原样套用；Work II 必须用 discovery
  campaign 实际冻结的 planned experiment count 重建 profile，并将 participant trajectory 与 evaluator
  held-out/blind trajectory严格分离。

## 0. Proposed manuscript architecture (planning draft)

This is an architecture proposal, not a protocol freeze and not an authorization to start
primary data collection. The formal gates below remain the source of truth once the scientific
question, methods and preregistration are frozen.

### Working title and one-sentence thesis

Working title: **Controlled Experiments on Scientific Prior Use, Revision and Transfer in AI
Agents**.

The paper should test one scientific dissociation rather than rank agents:

> An agent may reach a useful endpoint by following a prior-shaped heuristic without discovering
> the governing law. Process-complete experiments should distinguish no-prior discovery,
> correct-prior confirmation and wrong-prior rejection, then test whether the agent can summarize
> the recovered law and transfer it to held-out conditions.

### Claim hierarchy

1. **Primary claim — endpoint success is not law discovery.** Under a fixed hidden law, endpoint
   optimization, predictive law recovery and calibrated uncertainty are separate estimands.
2. **Prior-condition claim — prior quality changes discovery strategy.** No prior, correct prior
   and wrong prior should produce distinct evidence acquisition, exploration and calibration
   profiles under the same public contract.
3. **Bias-resistance claim — wrong priors can be rejected.** A scientifically adaptive agent must
   reduce confidence in an incorrect prior when observations contradict it, rather than preserve
   the prior through selective measurement or post-hoc explanation.
4. **Summary-and-transfer claim — recovered laws are reusable objects.** A law summary must make
   counterfactual predictions on held-out conditions and transfer across mechanism-held-out or
   world-held-out instances; verbal self-report alone is insufficient.
5. **Profile claim — method and resource dependence.** Backend, scaffold, evidence budget, calls,
   tokens, time, invalid actions and safety behavior are reported as separate profiles, not as a
   single intelligence score.

### Evidence architecture

The manuscript should maintain four visibly separate evidence layers:

- **Environment qualification:** current Gate A proves that fixed hidden laws, public observations
  and instrument mappings are internally coherent. It is not evidence that an agent discovered a
  law.
- **Matched prior conditions:** the same fixed world cohort is entered with no prior, a correct
  prior or an intentionally wrong/biased prior; public contract, budget and safety surface stay
  matched.
- **Process-level discovery:** each trajectory records experiment selection, evidence acquisition,
  predictive revision, uncertainty/calibration, prior rejection, law summary and endpoint outcome.
- **Summary and confirmation:** the law summary is evaluated on held-out conditions after public
  execution; private sealed worlds test transfer once with the same preregistered estimands.

### Manuscript chapter skeleton

1. **Introduction — the prior problem.** Explain why a correct endpoint can arise from a wrong
   scientific model, and state the distinction between discovery, confirmation and bias rejection.
2. **Conceptual framework.** Define prior quality, fixed hidden law, evidence, belief/calibration,
   experiment choice, law summary, counterfactual prediction and transfer.
3. **Fixed-law world cohort.** Describe matched no-prior, correct-prior and wrong-prior conditions
   across at least two mechanism families, with development/formal/private splits.
4. **Participant methods and estimands.** Freeze backend × scaffold, context/tools, evidence and
   resource budgets, provider accounting, analysis units and censoring rules.
5. **Results I — discovery under prior conditions.** Compare experiment selection, information gain,
   learning curves and endpoint outcomes for no, correct and wrong priors.
6. **Results II — rejecting biased priors.** Test contradictory evidence, posterior/calibration
   movement, counterfactual prediction and whether the agent stops defending the wrong prior.
7. **Results III — law summaries and transfer.** Evaluate compressed law summaries on held-out
   conditions and mechanism/world-held-out instances, with private sealed confirmation.
8. **Results IV — resource and safety profile.** Report measurement cost, calls, tokens, wall time,
   invalid actions, risk debits and stopping behavior as bounded operational consequences.
9. **Discussion.** State when evidence supports law discovery, when it only supports local policy
   repair, and when prior bias remains unresolved.
10. **Methods, data and appendix.** Provide the frozen prior matrix, trajectory schema, statistical
    models, robustness analyses, failure/censoring audit and reproducibility package.

### Main display plan

- **Figure 1 — From prior to law.** A causal diagram contrasting no-prior discovery, correct-prior
  confirmation and wrong-prior rejection under one fixed public contract and hidden law.
- **Figure 2 — Fixed-law cohort and prior matrix.** Mechanism families, matched world identities,
  prior conditions, development/formal/private splits and the backend × scaffold matrix.
- **Figure 3 — Experimental discovery process.** Chosen measurements, information gain, predictive
  law recovery and calibration trajectories, with endpoint success shown as a separate channel.
- **Figure 4 — Bias rejection and law transfer.** Wrong-prior confidence collapse, counterfactual
  prediction improvement, law-summary quality and mechanism/world-held-out transfer.
- **Figure 5 (optional or supplement) — Operational profile.** Resource, safety and stopping
  consequences; include only if the denominator and interpretation are independently strong.

Core tables should map claims to estimands, list the frozen cell matrix and report failure,
right-censoring and resource denominators. Raw provider payloads and private identities remain
outside the reader-facing package.

### Execution phases and stop conditions

- **P0 — Architecture and claim freeze:** W2-01 through W2-05.
- **P1 — Method qualification:** W2-06 through W2-10; no scientific arm selection by outcome.
- **P2 — Preregistration freeze:** W2-08 and W2-11, including power, budgets and sealed commitment.
- **P3 — Public formal matrix:** W2-12, with blind progress only and no live arm changes.
- **P4 — Private sealed confirmation:** W2-13, one execution after public analysis code is frozen.
- **P5 — Analysis and release:** W2-14 and W2-15; stop if the primary dissociation and transfer
  boundary are answered, even if optional bridging is deferred.

The paper must not begin formal data collection until P0--P2 are complete. Historical Gate A
numbers remain pilot/environment context until W2-02 rebinds them to the current source. A law
is fixed within each formal world; prior condition, not mid-run law drift, is the primary causal
factor.

### Reviewer-driven convergence: candidate confirmatory design

This design is a candidate for preregistration, not yet a frozen matrix.

**Primary causal manipulation.** Hold the executable world, recipe space, public task contract,
noise identity, evidence schedule, measurement surface and reward fixed. Change only the mapping
between anonymous material identities and an agent-facing nominal-property dossier:

- `opaque`: anonymous identifiers with no task-specific dossier;
- `aligned_nominal`: nominal property bundles are assigned to the material identities for which
  they are directionally useful in the fixed world;
- `misindexed_nominal`: the exact same property-bundle multiset is permuted across anonymous
  identities while fields, values, token budget and wording are preserved.

The dossier is explicitly described as incomplete nominal information, not ground truth;
experimental evidence is authoritative. Prior strength, information volume and confidence wording
must be matched between aligned and misindexed conditions. Because pretrained agents always have
implicit priors, `opaque` means no additional task-specific explicit prior, not literally no prior.
Recovering the anonymous-ID-to-dossier mapping alone is not sufficient for a law-discovery claim:
formal success additionally requires an executable law summary, held-out predictions across
unobserved conditions and transfer beyond the exact diagnostic points.

**Primary free-discovery trajectory.** The primary experiment must not give the participant a
protocol-owned discriminating experiment. Mechanism/prior identifiability is qualified before the
participant run without disclosing the diagnostic condition. Each formal cell should use one
operation-level Codex session across a resource-shared discovery campaign:

1. a pre-evidence prediction, confidence and prior-reliability checkpoint committed inside the
   active session;
2. participant-owned operation-level exploration from the first physical action, including
   experiment selection, measurement, continuation, termination and final assay;
3. fixed checkpoint locations after preregistered complete-experiment counts, with all checkpoints
   remaining inside the same Codex process rather than separate provider requests;
4. a final executable law summary, held-out predictions and agent-committed recommendation;
5. independent sealed held-out/blind execution with no feedback to the participant session.

The primary estimand is the total effect of prior condition on evidence seeking, experiment choice,
belief revision, law recovery and action. Failure to seek disconfirming evidence is therefore a
scientific outcome, not a nuisance to be repaired by injecting the key experiment. The exact number
of complete experiments and checkpoint positions remain provisional until resource and provider
qualification; a planning horizon must not be frozen merely because it appeared in a review.

**Optional matched-evidence mechanism probe.** A separate secondary cloned-world probe may present
identical contradictory evidence to all three prior arms to distinguish “did not seek the evidence”
from “saw the evidence but did not update.” It must use its own sessions and resources, remain outside
the primary free-discovery trajectory, and never enter the participant process-profile or primary
endpoint denominator. The smallest real provider pilot does not require this optional probe.

**Scientific-decision interface.** The primary participant inherits the first paper's complete-agent
interface: one long-lived Codex process uses the host-owned ChemWorld MCP to decide each operation
after observing the previous public outcome. The deterministic host owns validation, transaction,
resource and hidden-world semantics, but not participant operation selection. High-level
complete-experiment planners remain calibration controls only.

**Candidate chemical scope.** The initial cohort uses five heterogeneous reference tasks:
electrochemical conversion, reaction-to-crystallization, reaction-to-distillation,
partition discovery and safety-constrained reaction. Each must expose an identifiable matched
opaque/aligned/misindexed prior contract. Formal inclusion depends on current Gate A
requalification and prior-identifiability checks; tasks are not selected by participant
performance, and any invalid task must be replaced from the remaining reference registry rather
than shrinking the paper to two tasks. Continuous-flow optimization remains a later process-law
candidate because its current categorical material IDs do not carry a distinct causal kinetic
mapping suitable for this prior manipulation.

**Calibration controls, not a leaderboard.** A bounded semantics-free block may include random or
space-filling search, GP-BO with categorical IDs and GP-BO with the public property vector. The
property-aware control is required if semantic dossiers are supplied to an LLM. These controls
calibrate black-box search and informative-feature value; they do not define the paper's main
competition.

**Participant scope.** The only current participant backend is WellAU `gpt-5.6-sol` at medium
reasoning. Direct and compact stateful-scientific scaffolds may form a matched secondary axis; the
stateful memory is a small typed belief/evidence/next-intent object, not unconstrained free text.
No second model or provider enters the current completion scope.

### Claim ownership map

- **Work I owns:** composable-world construction, task/instrument contract validity, transaction
  semantics, public/private observation boundaries, resource ledgers, controlled world forks and
  exact environment/action-trace replay.
- **Work II owns:** prior manipulation, experiment selection, evidence interpretation, selective
  rejection of wrong priors, typed law summaries, knowledge-to-action translation and held-out
  transfer.
- **Shared boundary:** Work II may reuse only currently bound Work I qualification evidence; agent
  outcomes never qualify the environment, and Work I fork results never count as participant law
  discovery.

### Candidate hypothesis hierarchy

- **H1 — Prior utility (secondary):** aligned nominal information improves early predictive
  accuracy, evidence efficiency or blind-validated outcome relative to opaque identifiers.
- **H2 — Prior vulnerability (secondary):** misindexed nominal information harms prediction,
  experiment selection or blind-validated outcome relative to opaque identifiers.
- **H3 — Selective evidence-driven correction (primary):** evidence acquired during free discovery
  improves the misindexed condition and closes its predictive gap to the aligned condition without
  producing a comparable loss in the aligned condition; failure to acquire relevant disconfirming
  evidence remains a distinct observable failure mode.
- **H4 — Knowledge-to-action translation (key secondary):** epistemic correction predicts the next
  participant-owned operations, subsequent evidence-aligned experiments and blind-validated
  performance.

For a held-out prediction quality `Q_k` measured at snapshot `k`, define the aligned--misindexed
gap `G_k = Q_aligned,k - Q_misindexed,k`. A candidate primary contrast is
`C_prior = G_pre - G_post`, with guardrails requiring `Q_misindexed,post > Q_misindexed,pre`
and no material aligned-condition degradation beyond a preregistered tolerance. Exact scoring,
snapshot locations and tolerance remain unfrozen.

Prior benefit `B`, prior harm `H` and correction/recovery `R` may be reported as a descriptive
phenotype vector, but must not be collapsed into one ranking score. Epistemic, behavioral and
outcome channels remain separate so that the analysis can distinguish:

- understands and acts;
- understands but cannot translate knowledge into action;
- acts successfully without an accurate law model;
- neither understands nor acts effectively.

## 1. 旗舰科学问题

候选中心问题：

> **在固定的隐藏规律下，agent 能否从实验中发现规律、摒弃错误先验，并将总结出的规律迁移到未见条件？**

正式研究必须同时测量并区分：

- prior condition（无先验、正确先验、错误/带偏差先验）；
- experiment selection 与 information gain；
- law discovery 与 predictive calibration；
- wrong-prior rejection 与 bias resistance；
- law summary / representation quality；
- held-out transfer；
- endpoint outcome、resource efficiency 和 safety behavior。

当前已有的是历史环境 Gate A 证书和大量执行代码；当前证据绑定为 `historical_gate_a_pass_current_binding_stale`，participant-agent 正式 Gates/Outcomes 尚未执行。不得把历史 Gate A 写成当前 agent 规律学习结果。

详细历史计划参见：[`RC28_PARTICIPANT_FORMAL_EXPERIMENT_PLAN_AND_TODO_ZH.md`](RC28_PARTICIPANT_FORMAL_EXPERIMENT_PLAN_AND_TODO_ZH.md)。本文件是面向第二篇论文的主控清单；若两者冲突，以后续冻结的 Work II preregistration 为准。

## 2. 认领与状态规则

- 每项任务只能勾选一个认领状态和一个执行状态。
- 认领后填写负责人并进入 `DOING`；验收标准满足后直接进入 `DONE`，不设 review 阶段。
- `阻塞` 必须记录阻塞证据、解除条件和下一次检查日期。
- 开始正式 primary matrix 前，必须完成 Registered Report/常规投稿路线决策。
- 正式协议冻结后，不得因模型表现、成本或结果方向更换 world、seed、agent、阈值或主终点。
- provider repeats 是嵌套技术重复，不得冒充独立 world clusters。
- 默认 seed completion contract 为每个适用独立 cell 5 个 world seeds；超过 5 必须取得用户明确审核授权。
- provider/model 冻结为 WellAU `gpt-5.6-sol` medium；其他 backend、reasoning effort 或 provider 不在当前范围。

### 工作流负责人

- [x] 当前单一负责人：`Codex /root`
- [x] 世界/先验设计、Agent/scaffold、统计/预注册、执行与论文发布均由同一负责人协调；无独立 reviewer 角色。

## 3. 当前基线状态

- [x] mechanism-family 与 material-law interventions 已实现；
- [x] 历史 Gate A 环境实验已完成：A2 4,896 trials、A3 2,016 trials；
- [x] 历史 A2 top-1 accuracy 为 0.9826；
- [x] 历史 A3 detection sensitivity 为 0.9935、AUROC 为 0.9990、end-to-end success 为 0.9657；
- [x] 历史 experiment-level adaptation、belief metrics、change detection、attribution 和 recovery 的代码骨架已存在；
  它们需要重绑定为固定规律下的 prior/discovery/bias-rejection/law-summary protocol，不能直接当作当前结果；
- [ ] 当前 source/protocol binding 尚未重新资格验证；
- [ ] participant methods 尚未冻结；
- [ ] participant formal Outcomes 尚未执行；
- [ ] private sealed confirmation 尚未执行；
- [ ] Work II publication claim 尚未形成。

## 4. 硬门禁

以下门禁必须顺序满足：

1. `G0 — Current environment binding`：当前代码下重新确认环境可识别性；
2. `G1 — Scientific question freeze`：冻结主假设、主终点和 claim boundary；
3. `G2 — Participant method freeze`：冻结 backend、scaffold、context、tools、retry 和预算；
4. `G3 — Power and preregistration`：冻结 world clusters、重复、分析和停止规则；
5. `G4 — Public formal execution`：一次性执行公开正式矩阵；
6. `G5 — Private sealed confirmation`：公开矩阵完成后执行一次 private replication；
7. `G6 — Publication release`：证据、代码、数据、论文和主张完全绑定。

任何后续 Gate 不得反向修改已完成 Gate 的世界、指标或阈值。

## 5. 任务总览

| ID | 优先级 | 任务 | 当前状态 | 关键依赖 |
| --- | --- | --- | --- | --- |
| W2-01 | P0 | 冻结 Work II 与 Work I 的边界 | DONE | Work I scope |
| W2-02 | P0 | 重新建立当前 Gate A 证据绑定 | DOING | 干净提交 |
| W2-03 | P0 | 冻结中心假设与 claim hierarchy | DOING | W2-01、W2-02 |
| W2-04 | P0 | 冻结先验条件与固定规律 world cohort | DOING | W2-03 |
| W2-05 | P0 | 冻结 estimands、指标和判定规则 | DOING | W2-03、W2-04 |
| W2-06 | P0 | 冻结 participant backend × scaffold 矩阵 | DOING | W2-03 |
| W2-07 | P0 | 功效、资源和成本审计 | 未开始 | W2-04、W2-05、W2-06 |
| W2-08 | P0 | Registered Report/常规投稿路线决策 | 未开始 | W2-03–W2-07 |
| W2-09 | P0 | 完成 manifest-driven formal runner | DOING | W2-04–W2-07 |
| W2-10 | P0 | provider/scaffold shakedown 与方法资格验证 | DOING | W2-09 |
| W2-11 | P0 | 冻结 preregistration 与不可变执行包 | 未开始 | W2-08、W2-10 |
| W2-12 | P0 | 执行 public formal matrix | 未开始 | W2-11 |
| W2-13 | P0 | 执行 private sealed confirmation | 未开始 | W2-12 |
| W2-14 | P0 | 分析、稳健性、替代解释排除 | 未开始 | W2-12、W2-13 |
| W2-15 | P0 | 第二篇论文、数据与发布包 | 未开始 | W2-14 |
| W2-16 | P1 | 物理或高保真桥接 | 未开始，可选增强 | W2-12 |

## 6. 详细任务卡

### W2-01 — 冻结 Work II 与 Work I 的边界

- 认领：
  - [ ] 未认领
  - [x] 已认领；负责人：`Codex /root`
- 状态：
  - [ ] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [x] 完成
- 优先级：P0
- 验收标准：
  - [x] Work I 只负责 apparatus、measurement validity 和 autonomous policy observability；
  - [x] Work II 独占 prior sensitivity、law discovery、wrong-prior rejection、law summary 和 transfer；
  - [x] Work I 的 world-fork certificate 不使用 participant adaptation 结果；
  - [x] Work II 可以引用 Work I 装置，但不重复 G0/G2 作为中心发现；
  - [x] 形成一页 claim ownership map。
- 备注：`Claim: Codex /root — W2-01 — DONE`；claim ownership map 已写入本文件。

### W2-02 — 重新建立当前 Gate A 证据绑定

- 认领：
  - [ ] 未认领
  - [x] 已认领；负责人：`Codex /root`
- 状态：
  - [ ] 未开始
  - [x] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 目标：把历史 Gate A 与当前 source/protocol binding 分开，并在当前代码上重新资格验证。
- 验收标准：
  - [ ] current design audit、semantics audit、release qualification 全部通过；
  - [ ] A1 physical validity 在当前 source 上通过；
  - [ ] A2/A3 当前证书重新生成或由不可变兼容性证明合法继承；
  - [ ] `gate_a_evidence_current=true`；
  - [ ] 历史证书仍保留且不会被覆盖；
  - [ ] 环境资格验证与 participant performance 继续严格分离。
- 备注：`Claim: Codex /root — W2-02 — DOING`

### W2-03 — 冻结中心假设与 claim hierarchy

- 认领：
  - [ ] 未认领
  - [x] 已认领；负责人：`Codex /root`
- 状态：
  - [ ] 未开始
  - [x] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 候选主假设：endpoint optimization、规律发现和错误先验排除可以系统解耦；只有经过证据校准的规律总结才能支持 held-out transfer。
- 验收标准：
  - [ ] 唯一 primary scientific question 已写成可证伪形式；
  - [ ] 唯一主终点或严格层级化主终点确定；
  - [ ] H3 selective evidence-driven correction 作为候选唯一 primary hypothesis 被接受、修订或明确否决；
  - [ ] H1 prior utility、H2 prior vulnerability 和 H4 knowledge-to-action translation 的 confirmatory/exploratory 层级冻结；
  - [ ] prior condition、discovery、bias rejection、law summary、transfer 的主次层级冻结；
  - [ ] 明确何种结果支持“从实验发现并迁移规律”，何种结果只支持 endpoint heuristic；
  - [ ] 明确何种结果只支持 agent-specific 或 world-specific 结论；
  - [ ] 不把 LLM vs BO 排名设为主比赛。
- 备注：`Claim: Codex /root — W2-03 — DOING`

### W2-04 — 冻结先验条件与固定规律 world cohort

- 认领：
  - [ ] 未认领
  - [x] 已认领；负责人：`Codex /root`
- 状态：
  - [ ] 未开始
  - [x] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 最低设计要求：
  - `opaque`：无额外 task-specific dossier；
  - `aligned_nominal`：方向上有用但明确不等同于真值的 nominal dossier；
  - `misindexed_nominal`：同一 property-bundle multiset 在匿名材料 ID 间置换；
  - 固定世界规律，不在单次 run 中改变 hidden law；
  - 至少两个 mechanism families；
  - 随机选择且与开发 worlds 隔离的 formal world cohort。
- 验收标准：
  - [ ] 每个固定规律具有明确状态转移、可观测后果和自洽性检查；
  - [ ] public prior、真实 hidden law 和 instrument mapping 分别控制；
  - [ ] 三种 prior condition 在 world、预算、契约和安全边界上匹配；
  - [ ] aligned/misindexed 的字段、数值集合、措辞、token 预算和 dossier 置信强度匹配；
  - [ ] evaluator-side prior-identifiability checks 的证据设计在 participant outcomes 前冻结，但不得把关键
    discriminating experiment 直接注入 primary free-discovery trajectory；
  - [ ] 若增加 matched-evidence mechanism probe，其 cloned world、evidence packet、session、resource
    card 和 secondary estimand 必须独立冻结，不得与 primary campaign 混账；
  - [ ] electrochemical 与 crystallization 是否作为两类正式机制由 Gate A 和 prior-identifiability 决定，而非按 agent 结果挑选；
  - [ ] prior identity、world identity 和 split 均有不可变哈希；
  - [ ] qualification worlds、public formal worlds、private worlds 不重叠；
  - [ ] 不以开发结果选择正式 worlds。
- 备注：`Claim: Codex /root — W2-04 — DOING`

### W2-05 — 冻结 estimands、指标和判定规则

- 认领：
  - [ ] 未认领
  - [x] 已认领；负责人：`Codex /root`
- 状态：
  - [ ] 未开始
  - [x] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 必须分层报告：
  - O1 discovery：learning curve、law-recovery error、information gain、counterfactual prediction；
  - O2 prior calibration：prior-to-posterior movement、Brier、credible coverage 和 uncertainty；
  - O3 bias rejection：错误先验置信度下降、选择性测量、错误归因和 prior persistence；
  - O4 law summary：结构/参数摘要的可执行性、压缩稳定性和反事实预测一致性；
  - O5 transfer：机制内、机制外和 world-held-out 的预测与控制；
  - O6 autonomy/resource/safety：completion、invalid actions、measurements、risk、calls、tokens、cost、time。
  - O7 blind outcome：最终推荐的独立 blind validation、validated learning-curve AUC、incumbent 与 recommendation gap。
- 验收标准：
  - [ ] endpoint optimization 与 law discovery、prior rejection 和 transfer 指标代数独立或明确建模依赖；
  - [ ] continuous estimands 优先于阈值分类；
  - [ ] no-prior、correct-prior 和 wrong-prior 分母分离；
  - [ ] primary correction contrast 基于 participant 自主获得的证据和固定 checkpoints，同时要求 misindexed
    改善和 aligned 不发生超容差退化；不得仅凭 gap closure 或被注入的 diagnostic evidence 判定成功；
  - [ ] 仅恢复材料 ID 与 dossier 的对应关系不得计为规律发现；必须通过连续条件反事实预测、typed law summary 和 transfer 验证；
  - [ ] prior benefit/harm/recovery 只作为分立 phenotype vector 报告，不合成排行榜分数；
  - [ ] epistemic、behavioral 和 outcome 三层的联合与解耦规则冻结；
  - [ ] right censoring、missingness、provider failure 和 multiplicity 规则冻结；
  - [ ] analysis unit 为独立 world/cell cluster，provider repeats 嵌套；
  - [ ] 明确“law summary 声明”、反事实预测与后续 operation-level 行为证据的联合成功规则；
  - [ ] 明确区分“未主动寻找反证”和“看到相同反证后仍不更新”，后者只有在可选 matched-evidence probe
    中作为 secondary mechanism contrast 报告。
- 备注：`Claim: Codex /root — W2-05 — DOING`

### W2-06 — 冻结 participant backend × session/scaffold 矩阵

- 认领：
  - [ ] 未认领
  - [x] 已认领；负责人：`Codex /root`
- 状态：
  - [ ] 未开始
  - [x] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 目标：先冻结一个可审计的持久 session execution unit，再决定是否引入第二 scaffold axis；避免把
  model、session、scaffold 和 transport 完全捆绑。
- 当前最低方法：WellAU `gpt-5.6-sol` medium；一个 cell 一个长驻 operation-level Codex process，
  通过 host-owned ChemWorld MCP 控制同一 discovery campaign 的多个 complete experiments；同一 session
  内维护 typed belief、evidence references、law summary 和 next intent；当前不加入第二 backend。
- 验收标准：
  - [ ] session start、operation tool loop、checkpoint、interrupt/finalize 和 receipt 使用同一可审计 contract；
  - [ ] 每个 cell 恰有一个 session identity，所有 operations、complete experiments 和 belief checkpoints 均绑定该 identity；
  - [ ] agent 每次读取前一 public outcome 后选择一个 operation；host 只负责 validation、transaction、resource 和 hidden-world 执行；
  - [ ] `terminate`、`final_assay`、discard、budget exhaustion 和 right-censoring 的 lifecycle 语义与第一篇 complete-agent 路径一致；
  - [ ] 一个 cell 内多个 complete experiments 共享同一 campaign resource card/ledger，不允许逐 experiment 重置资源；
  - [ ] belief snapshot 通过同一 session 内的结构化 MCP checkpoint 提交，不产生额外 standalone provider session；
  - [ ] stateful memory 限定为 typed belief、diagnostic focus、evidence references 和 next intent，不使用巨型自由文本状态；
  - [ ] context、memory、retry、temperature/thinking、timeout 和 failure semantics 冻结；
  - [ ] provider attempt、MCP tool call、operation attempt、committed operation、complete experiment、cell 和 blind evaluator 分母分开报告；
  - [ ] classical/reference policies 只承担校准或机制对照角色；若 LLM 获得 property dossier，则至少包含 ID-only 与 property-aware 两类公平对照；
  - [ ] 不根据 pilot 胜负删除正式方法臂。
- 备注：`Claim: Codex /root — W2-06 — DOING`。旧 Direct Responses 多调用方法已归档；当前
  session-based method 尚未完成资格验证。未提交的 high-level complete-experiment-plan prototype
  不代表当前方法，必须替换为 operation-level complete-agent runner 或归档后才能启动真实 pilot。

### W2-07 — 功效、资源和成本审计

- 认领：
  - [ ] 未认领
  - [x] 已认领；负责人：`Codex /root`
- 状态：
  - [ ] 未开始
  - [x] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 验收标准：
  - [ ] 以独立 world clusters 进行功效分析；
  - [ ] formal power 使用 world-level paired contrasts；rounds、prediction snapshots 和多个 endpoints 不作为独立样本；
  - [ ] 对 world、mechanism、agent、session 和交互方差作预期分解；
  - [ ] 冻结 worlds、replicates、provider repeats 和最大 provider calls；
  - [ ] discovery campaign 的 complete-experiment 上限、checkpoint 位置和 optional matched-evidence probe 是否进入 secondary matrix 在 pilot 后、formal outcomes 前冻结；
  - [ ] 冻结一张跨 discovery experiments 共享的 task-pattern-specific CampaignResourceCard，包括 operation、vessel、assay、instrument、stock、process-time、quench/transfer 和 closeout 余量；
  - [ ] 冻结 token、货币、wall time、并发和失败重试预算；
  - [ ] 明确早停仅针对基础设施/安全，不针对结果方向；
  - [ ] 输出完整资源上界和预计运行 ETA。
- 备注：`Claim: Codex /root — W2-09 — DOING`；已建立 prior-pilot manifest runner、
  machine-readable execution index 和外置 progress probe；formal trajectory/prefix/law-summary
  runner 尚未完成。

### W2-08 — Registered Report/常规投稿路线决策

- 认领：
  - [ ] 未认领
  - [x] 已认领；负责人：`Codex /root`
- 状态：
  - [ ] 未开始
  - [x] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 硬约束：在路线决定前不得开始正式 primary data collection。
- 验收标准：
  - [ ] 决定是否申请 Nature Registered Report Stage 1；
  - [ ] 若申请，确认已有数据只作为 pilot/environment qualification；
  - [ ] 若不申请，冻结常规投稿目标和对应 evidence threshold；
  - [ ] 记录决策日期、负责人和不可逆后果；
  - [ ] 投稿路线不根据 formal outcomes 事后改变主假设。
- 备注：`Claim: Codex /root — W2-10 — DOING`；Stage A mock contract preflight 已通过
  15/15 cells、0 failures。Stage B 真实 WellAU 三臂小探针已通过 3/3 cells、0 failures、
  3 calls/3 attempts/0 retries；共 12,630 tokens，cache hit 为 0，progress heartbeat 正常。
  该结果仅资格验证 direct Responses transport、prior delivery 和完整实验执行，不是 prior
  效应证据，且已随 Direct Responses 实现归档，不资格验证当前 operation-level session method。
  下一步是 operation-level deterministic/mock preflight 和一个任务 × 三臂 × seed 0 的真实 session
  probe；此前不得启动五任务 breadth。

### W2-09 — 完成 manifest-driven formal runner

- 认领：
  - [ ] 未认领
  - [x] 已认领；负责人：`Codex /root`
- 状态：
  - [ ] 未开始
  - [x] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 代码交付物：
  - [ ] 基于第一篇 `InteractiveCodexExperimentAgent`/ChemWorld MCP 的 persistent operation-level participant runner；
  - [ ] immutable matrix/schedule manifest（五任务、三臂、session、operation、experiment、checkpoint、held-out/blind denominators）；
  - [ ] session-aware resume 与 right-censoring state machine；
  - [ ] provider/session/scaffold receipts；
  - [x] typed prior/evidence/belief/law-summary schema 与可执行 law-summary validator；
  - [ ] 同一 session 内的 pre-evidence、preregistered experiment checkpoints 和 final snapshot MCP contract；
  - [ ] 从首个 physical operation 开始的 free-discovery state machine；主实验不注入 protocol-owned discriminating experiment；
  - [ ] optional matched-evidence mechanism probe 的独立 cloned-world/session/resource contract，默认不进入最小 pilot；
  - [ ] operation-level `step(action)`、public outcome、termination/final-assay 和 multi-experiment campaign 的统一接口；
  - [ ] discovery campaign 共享 resource card/ledger、跨 experiment resource snapshot 和 lifecycle reserve；
  - [ ] 第一篇 19-coordinate contract 的 Work II adapter，排除 evaluator-owned held-out/blind operations；
  - [ ] exact replay、resource replay 和 hidden-boundary audits；
  - [ ] public/private split enforcement；
  - [ ] formal report generator。
- 验收标准：
  - [x] 不依赖 notebook 或人工逐单元操作；
  - [x] 中断后不覆盖、不替换、不重复计数；
  - [ ] private identities 不进入 agent prompt；
  - [ ] 每个估计量可追溯到 immutable trajectory records；
  - [ ] fail-closed tests 覆盖 provider failure、partial action 和 ledger mismatch。
- 备注：typed prior/evidence/belief/law-summary schema 与 held-out query validator 保留。旧
  Direct Responses runner、配置、tests 和 mock/real/breadth 报告均已归档；其 15/15 breadth
  只证明旧架构的 transport/schema/executor/recovery 可运行，不是当前 session method 的资格证据。
  当前未提交的 `CodexSessionClient + complete-experiment plan` prototype 关闭 MCP、按 plan 一次执行到底，
  不能观察 operation-level measurement/termination，也尚未共享 campaign resource ledger；它不得运行
  provider 或进入当前方法。新 operation-level runner 必须先通过 deterministic session preflight，再
  运行一个任务 × 三臂 × seed 0 的真实 session probe；在此之前不得启动五任务 breadth 或多 seed 数据。

### W2-10 — provider/scaffold shakedown 与方法资格验证

- 认领：
  - [ ] 未认领
  - [x] 已认领；负责人：`Codex /root`
- 状态：
  - [ ] 未开始
  - [x] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 目标：只排除接口、资源和生命周期失败，不检验或筛选科学结果。
- 验收标准：
  - [ ] 当前 persistent-session 方法完成独立 qualification cells；
  - [ ] schema-valid operation rate、committed-operation rate、lifecycle completion、receipts、cost/resource accounting 和 replay 达标；
  - [ ] 同一 session 内多个 complete experiments、共享资源、prediction checkpoints、typed law summary 和 final recommendation 全部闭环；
  - [ ] 中途 measurement、continue、`terminate`、final assay、资源拒绝和 right-censoring 均有 fail-closed qualification；
  - [ ] qualification worlds 不进入正式矩阵；
  - [ ] 失败修复只允许修改实现，不允许修改正式科学 estimands；
  - [ ] 形成当前 session method 的冻结 hash 和资格验证报告。
- 备注：旧 Direct Responses 方法及其 3/3、15/15 development qualification 已归档，不再视为
  当前方法通过。当前待验证方法为 WellAU `gpt-5.6-sol` medium、one persistent Codex session
  per cell、operation-level ChemWorld MCP、multi-experiment shared-resource discovery campaign、
  sealed held-out/blind evaluator。WellAU pricing catalog仍不可验证，货币成本不得记为零。

### W2-11 — 冻结 preregistration 与不可变执行包

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 依赖：W2-08、W2-10
- 验收标准：
  - [ ] 协议、world cohort、methods、schedule、metrics、power、stopping 和 analysis 全部冻结；
  - [ ] preregistration 文档与 machine-readable manifest 一致；
  - [ ] 干净 wheel、独立 checkout 和预运行 evidence graph 通过；
  - [ ] private matrix 密封，只公开 commitment hash；
  - [ ] 正式运行命令、预算和故障升级流程签字确认。
- 备注：`TBD`

### W2-12 — 执行 public formal matrix

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 验收标准：
  - [ ] 从冻结提交和不可变执行包启动；
  - [ ] 全部 cell 按预注册状态机达到 completed/right-censored/failed 终态；
  - [ ] 不根据 live outcomes 增删 cells 或更换模型；
  - [ ] provider、token、cost、resource 和 wall-time 账本完整；
  - [ ] 每个 completed trajectory exact replay；
  - [ ] 运行期间只发布盲化进度，不发布 arm contrasts。
- 备注：`TBD`

### W2-13 — 执行 private sealed confirmation

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 依赖：W2-12
- 验收标准：
  - [ ] public methods 和 analysis code 已冻结；
  - [ ] private world commitment 与预先公开哈希一致；
  - [ ] 只执行一次，不因结果 rerun；
  - [ ] public/private transfer 使用同一预注册指标；
  - [ ] 完整记录任何基础设施删失和未启动单元。
- 备注：`TBD`

### W2-14 — 分析、稳健性和替代解释排除

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 验收标准：
  - [ ] 主分析严格按 preregistration 执行；
  - [ ] optimization 与 law learning 的解耦由联合结果而非单一分数判断；
  - [ ] 报告 world/mechanism/agent/session 方差与交互；
  - [ ] 检查先验坚持、证据修正、错误归因、规律总结和表面 endpoint 恢复等行为类型；
  - [ ] 检查 process metrics 是否预测 law-summary quality 与 held-out transfer；
  - [ ] 区分无先验学习、正确先验确认和错误先验排除，禁止把正确先验下的高分解释为发现能力；
  - [ ] 检查错误先验是否通过选择性测量、解释重写或策略补丁被隐性保留；
  - [ ] 分析 understands+acts、understands-but-cannot-act、acts-without-understanding 和 neither 四类 phenotype；
  - [ ] black-box/random/BO 结果只校准 semantics-free search，不得改写成主 leaderboard；
  - [ ] 分析 scaffold/model matched contrasts，避免 complete-system 差异冒充 model effect；
  - [ ] threshold、missingness、censoring 和 multiplicity 敏感性完整；
  - [ ] 所有探索性分析明确标记且不覆盖主结果。
- 备注：`TBD`

### W2-15 — 第二篇论文、数据与发布包

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 验收标准：
  - [ ] 标题、摘要和第一张图直接呈现先验条件下的规律发现与偏差排除问题；
  - [ ] 环境 Gate A、agent Outcomes 和 private confirmation 严格分层；
  - [ ] 主图围绕 prior → experiment → evidence → law summary → transfer 的能力链；
  - [ ] 不将负结果改写为平台失败，也不扩大未被证据支持的主张；
  - [ ] 全部代码、协议、轨迹、派生数据、图表和统计表可独立重建；
  - [ ] 证据图、clean wheel、independent checkout 和 final claim audit 通过；
  - [ ] 数据归档、作者信息和投稿包完整。
- 备注：`TBD`

### W2-16 — 物理或高保真桥接（可选增强）

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P1
- 目标：检验虚拟世界中的 process/discovery profile 是否预测受控现实或高保真系统中的行为。
- 验收标准：
  - [ ] 选择低风险、低成本、可重复的窄域体系；
  - [ ] 优先评估真实历史实验数据的 sequential oracle，以相同 opaque/aligned/misindexed 条件复现 prior phenotype；
  - [ ] wet-lab 仅在软件 phenotype、分析代码和安全边界冻结后作为可选窄域确认；
  - [ ] 虚拟与物理接口共享 typed lifecycle semantics；
  - [ ] 先 shadow mode，再进入经批准的有限闭环；
  - [ ] 安全、审批、废物和设备边界明确；
  - [ ] 迁移结果独立报告，不把小规模现实桥接泛化为全面现实有效性。
- 备注：是否进入 Work II 主文须在 formal results 前冻结：`TBD`

## 2026-08-08 persistent-campaign pilot checkpoint

- [x] `electrochemical-conversion × opaque/aligned_nominal/misindexed_nominal × world_seed=0`
  使用 WellAU `gpt-5.6-sol` medium 完成真实 operation-level pilot。
- [x] 每个 cell 恰有一个长驻 Codex process/session；4 个 complete experiments、24 个
  participant-owned operations 和 4 个 typed belief checkpoints 均在该 session 内完成。
- [x] 三臂共 12/12 experiments、72/72 committed operations、0 resource rejection、72/72 exact
  replay；共享 campaign ledger 和 paired keyed-noise namespace 通过。运行后边界审计发现公开
  resource card 的 `card_id/metadata` 泄漏 `prior_arm/world_seed`，因此 prior-arm blinding 未通过。
- [x] 已将 cumulative input 与 uncached input 分开：总 input 4,457,978，其中 cache hit
  4,004,864、uncached 453,114、output 23,781；高 cache 不等于重复输出。
- [x] 单 world 数值轨迹已保留为 shakedown 观察，但不得用于 prior confirmation/rejection 或
  arm-effect 解释；五 seed 中性 resource-card 重跑才是第一个可解释的 blinded contrast。
- [ ] 本 pilot 尚未执行 evaluator-owned held-out queries 和 blind recommendation replicates，
  因此不能把 checkpoint law summary 解释为已验证的 transfer。
- [x] 多 seed 前已补齐：arm/seed-neutral public resource card、独立 heartbeat、task-pattern-specific
  process-time hard cap、`electrolyze` repeat cap 和 fail-closed cell qualification。sealed evaluator
  ledger 与 prediction/law scoring 在 participant trajectories 完成后独立执行，不反馈 participant。
- 证据摘要：`workstreams/flagship_tasks/reports/work-ii-seed0-persistent-campaign-pilot.{json,md}`。

五 seed 扩展（2026-08-08）：

- [x] task-pattern-specific process-time hard cap、`electrolyze` repeat limit 和独立 heartbeat
  已实现并通过 focused preflight；sealed evaluator ledger/prediction scoring 可在 participant
  trajectories 完成后独立执行，不要求重跑 participant session。
- [x] 已冻结 `world_seed=0..4 × 三 prior arms` 共 15 cells；每 cell 一个 session、4 experiments、
  4 checkpoints，状态：`DOING`。
- [ ] 15/15 cells 完成并形成五 world paired descriptive report。

## 7. 完成定义

Work II 只有在以下条件全部满足时才标记完成：

- [ ] 当前 Gate A 证据绑定有效；
- [ ] 至少两个机制家族和无/正确/错误先验进入随机 formal world cohort，且每个 formal world 内规律固定；
- [ ] participant backend × scaffold 至少有一条可识别 matched axis；
- [ ] optimization、discovery、prior rejection、law summary 和 transfer 均有预注册指标；
- [ ] public formal matrix 与 private sealed confirmation 均达到终态；
- [ ] 能明确判断 agent 是依据证据发现并总结规律，还是只取得 endpoint 或维持先验偏差；
- [ ] 所有结论与 world/agent/sample scope 一致；
- [ ] 第二篇不依赖第一篇的阈值敏感 supporting result；
- [ ] 论文、代码、轨迹、数据和发布包可公开重建。
