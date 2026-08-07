# Work II TODO — 规律冲突、证据响应与科学适应

最后更新：2026-08-07
工作边界：第二篇研究智能体在世界规律与训练先验冲突时，能否通过实验检测变化、修正信念、恢复控制并迁移到 held-out conditions。它不重复第一篇的装置可观测性主张，也不把单纯 endpoint optimization 当作规律学习。

## 0. Proposed manuscript architecture (planning draft)

This is an architecture proposal, not a protocol freeze and not an authorization to start
primary data collection. The formal gates below remain the source of truth once the scientific
question, methods and preregistration are frozen.

### Working title and one-sentence thesis

Working title: **Optimizing Without Learning the Law: Detecting, Attributing and Adapting to
Hidden-Law Shifts with AI Agents**.

The paper should test one dissociation rather than rank agents:

> An agent may optimize an endpoint while failing to detect, attribute or update on a change in
> the governing law; process-complete experiments can distinguish these cases and quantify the
> recovery and held-out-transfer consequences.

### Claim hierarchy

1. **Primary claim — optimization is not law learning.** Endpoint success and governing-law
   detection/belief update are separate estimands; a high endpoint score alone cannot establish
   scientific adaptation.
2. **Secondary claim — evidence-conditioned adaptation.** When a law shift is detectable, the
   agent should attribute its family, revise its belief/action state and recover control on
   subsequent experiments. The chain is evaluated as detection → attribution → belief/action
   change → recovery, not collapsed into one intelligence score.
3. **Transfer claim — held-out generalization.** Adaptation must survive mechanism-held-out and
   world-held-out conditions, with a private sealed confirmation after the public matrix.
4. **Profile claim — method dependence.** Backend, scaffold and their interaction are reported
   separately through a matched matrix; no complete-system contrast is presented as a pure model
   effect.
5. **Exploratory profile — resources and safety.** Calls, tokens, time, measurements, invalid
   actions and risk debits characterize the cost of adaptation, but do not define the primary
   scientific result.

### Evidence architecture

The manuscript should maintain four visibly separate evidence layers:

- **Environment qualification:** current Gate A proves that the intervention is identifiable,
  internally coherent and observable under the declared public contract. It is not a participant
  performance result.
- **Matched participant outcomes:** the frozen backend × scaffold matrix produces trajectories with
  identical public contracts, budgets, context and failure semantics.
- **Process-level adaptation:** each trajectory records change detection, mechanism attribution,
  belief/calibration movement, evidence-conditioned action change, recovery and endpoint outcome.
- **Transfer and confirmation:** mechanism-held-out transfer is analyzed after public execution;
  private sealed worlds are run once with the same preregistered estimands.

### Manuscript chapter skeleton

1. **Introduction — the dissociation problem.** Explain why endpoint optimization, change
   detection and law learning are often conflated, and state the primary claim and boundaries.
2. **Conceptual framework.** Define public prior, hidden law, intervention families, observation,
   belief state, action change, recovery and held-out transfer; give the causal/evidence chain.
3. **World cohort and controlled interventions.** Describe no-change controls, parameter shifts,
   relation changes and sign/order reversals across at least two mechanism families, with strict
   development/formal/private splits.
4. **Participant methods and estimands.** Freeze backend × scaffold, context/tools, retries,
   budgets, provider accounting, analysis units and censoring rules; separate primary and
   exploratory estimands.
5. **Results I — detection and attribution.** Report whether agents notice a law shift and identify
   its family before interpreting endpoint changes; include calibration and delay.
6. **Results II — belief and action revision.** Test identical-prefix responses, belief/action
   changes after evidence and whether changes are directionally consistent with the hidden law.
7. **Results III — recovery and held-out transfer.** Quantify post-change regret, recovery time,
   terminal recovery and mechanism/world-held-out transfer; use the private sealed result as a
   confirmation layer rather than a second exploratory benchmark.
8. **Results IV — resource and safety profile.** Report measurements, calls, tokens, wall time,
   invalid actions, risk debits and completion as bounded operational consequences.
9. **Discussion.** State exactly what supports law-sensitive adaptation, what remains agent- or
   world-specific, and why endpoint-only success is insufficient. Keep physical/high-fidelity
   bridging optional and separate.
10. **Methods, data and appendix.** Provide the frozen matrix, trajectory schema, statistical
    models, robustness analyses, failure/censoring audit and reproducibility package.

### Main display plan

- **Figure 1 — What counts as law learning?** A causal timeline showing intervention, evidence,
  detection, attribution, belief/action update, recovery and endpoint; explicitly contrast an
  endpoint-only success path with an evidence-conditioned adaptation path.
- **Figure 2 — Frozen world cohort.** Intervention taxonomy, matched no-change controls,
  mechanism families, development/formal/private splits and the backend × scaffold matrix.
- **Figure 3 — Process readouts.** Detection/calibration, attribution confusion, identical-prefix
  response and evidence-conditioned action change, with world-cluster uncertainty.
- **Figure 4 — Adaptation and transfer.** Post-change regret/recovery trajectories and
  mechanism-held-out/world-held-out transfer, aligned to the same primary estimands.
- **Figure 5 (optional or supplement) — Operational profile.** Resource and safety consequences;
  include only if the denominator and interpretation are strong enough to stand independently.

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
numbers remain pilot/environment context until W2-02 rebinds them to the current source.

## 1. 旗舰科学问题

候选中心结论：

> **AI agents can optimize experiments without learning their governing laws.**

正式研究必须同时测量并区分：

- endpoint optimization；
- change detection；
- mechanism/family attribution；
- belief update and calibration；
- evidence-conditioned action change；
- adaptation/recovery；
- held-out transfer；
- resource efficiency and safety behavior。

当前已有的是历史环境 Gate A 证书和大量执行代码；当前证据绑定为 `historical_gate_a_pass_current_binding_stale`，participant-agent 正式 Gates/Outcomes 尚未执行。不得把历史 Gate A 写成当前 agent 规律学习结果。

详细历史计划参见：[`RC28_PARTICIPANT_FORMAL_EXPERIMENT_PLAN_AND_TODO_ZH.md`](RC28_PARTICIPANT_FORMAL_EXPERIMENT_PLAN_AND_TODO_ZH.md)。本文件是面向第二篇论文的主控清单；若两者冲突，以后续冻结的 Work II preregistration 为准。

## 2. 认领与状态规则

- 每项任务只能勾选一个认领状态和一个执行状态。
- 认领后填写负责人；多人协作时指定一名最终负责人。
- `阻塞` 必须记录阻塞证据、解除条件和下一次检查日期。
- 开始正式 primary matrix 前，必须完成 Registered Report/常规投稿路线决策。
- 正式协议冻结后，不得因模型表现、成本或结果方向更换 world、seed、agent、阈值或主终点。
- provider repeats 是嵌套技术重复，不得冒充独立 world clusters。

### 工作流负责人

- [ ] 总负责人已认领；负责人：`TBD`
- [ ] 世界与规律设计负责人已认领；负责人：`TBD`
- [ ] Agent/scaffold 负责人已认领；负责人：`TBD`
- [ ] 统计与预注册负责人已认领；负责人：`TBD`
- [ ] 正式执行负责人已认领；负责人：`TBD`
- [ ] 论文与发布负责人已认领；负责人：`TBD`

## 3. 当前基线状态

- [x] mechanism-family 与 material-law interventions 已实现；
- [x] 历史 Gate A 环境实验已完成：A2 4,896 trials、A3 2,016 trials；
- [x] 历史 A2 top-1 accuracy 为 0.9826；
- [x] 历史 A3 detection sensitivity 为 0.9935、AUROC 为 0.9990、end-to-end success 为 0.9657；
- [x] experiment-level adaptation、belief metrics、change detection、attribution 和 recovery 的主要代码骨架已存在；
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
| W2-01 | P0 | 冻结 Work II 与 Work I 的边界 | 未开始 | Work I scope |
| W2-02 | P0 | 重新建立当前 Gate A 证据绑定 | 未开始 | 干净提交 |
| W2-03 | P0 | 冻结中心假设与 claim hierarchy | 未开始 | W2-01、W2-02 |
| W2-04 | P0 | 冻结规律干预分类与 world cohort | 未开始 | W2-03 |
| W2-05 | P0 | 冻结 estimands、指标和判定规则 | 未开始 | W2-03、W2-04 |
| W2-06 | P0 | 冻结 participant backend × scaffold 矩阵 | 未开始 | W2-03 |
| W2-07 | P0 | 功效、资源和成本审计 | 未开始 | W2-04、W2-05、W2-06 |
| W2-08 | P0 | Registered Report/常规投稿路线决策 | 未开始 | W2-03–W2-07 |
| W2-09 | P0 | 完成 manifest-driven formal runner | 未开始 | W2-04–W2-07 |
| W2-10 | P0 | provider/scaffold shakedown 与方法资格验证 | 未开始 | W2-09 |
| W2-11 | P0 | 冻结 preregistration 与不可变执行包 | 未开始 | W2-08、W2-10 |
| W2-12 | P0 | 执行 public formal matrix | 未开始 | W2-11 |
| W2-13 | P0 | 执行 private sealed confirmation | 未开始 | W2-12 |
| W2-14 | P0 | 分析、稳健性、替代解释排除 | 未开始 | W2-12、W2-13 |
| W2-15 | P0 | 第二篇论文、数据与发布包 | 未开始 | W2-14 |
| W2-16 | P1 | 物理或高保真桥接 | 未开始，可选增强 | W2-12 |

## 6. 详细任务卡

### W2-01 — 冻结 Work II 与 Work I 的边界

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
  - [ ] Work I 只负责 apparatus、measurement validity 和 autonomous policy observability；
  - [ ] Work II 独占 law conflict、belief revision、mechanism attribution、recovery 和 transfer；
  - [ ] Work I 的 world-fork certificate 不使用 participant adaptation 结果；
  - [ ] Work II 可以引用 Work I 装置，但不重复 G0/G2 作为中心发现；
  - [ ] 形成一页 claim ownership map。
- 备注：`TBD`

### W2-02 — 重新建立当前 Gate A 证据绑定

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
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
- 备注：`TBD`

### W2-03 — 冻结中心假设与 claim hierarchy

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 候选主假设：优化表现与规律识别/适应可以系统解耦。
- 验收标准：
  - [ ] 唯一 primary scientific question 已写成可证伪形式；
  - [ ] 唯一主终点或严格层级化主终点确定；
  - [ ] detection、attribution、belief update、recovery、transfer 的主次层级冻结；
  - [ ] 明确何种结果支持“optimize without learning laws”；
  - [ ] 明确何种结果只支持 agent-specific 或 world-specific 结论；
  - [ ] 不把 LLM vs BO 排名设为主比赛。
- 备注：`TBD`

### W2-04 — 冻结规律干预分类与 world cohort

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 最低设计要求：
  - no-change / prior-aligned；
  - parameter-shifted；
  - relation-changed；
  - sign/order-reversed；
  - 至少两个 mechanism families；
  - 随机选择且与开发 worlds 隔离的 formal world cohort。
- 验收标准：
  - [ ] 每类 intervention 具有明确状态转移、可观测后果和自洽性检查；
  - [ ] public prior、真实 hidden law 和 instrument mapping 分别控制；
  - [ ] no-change controls 与 changed worlds 匹配；
  - [ ] world identity、intervention identity 和 split 均有不可变哈希；
  - [ ] qualification worlds、public formal worlds、private worlds 不重叠；
  - [ ] 不以开发结果选择正式 worlds。
- 备注：`TBD`

### W2-05 — 冻结 estimands、指标和判定规则

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 必须分层报告：
  - O1 detection：AUROC、Brier、sensitivity、FPR、delay；
  - O2 feedback use：identical-prefix response、belief/action change；
  - O3 adaptation：post-change regret AUC、recovery time、terminal recovery；
  - O4 autonomy：protocol completion、invalid actions、assay/discard；
  - O5 resource efficiency：experiments、measurements、risk、calls、tokens、cost、time；
  - held-out transfer：机制内/机制外预测与控制。
- 验收标准：
  - [ ] endpoint optimization 与 law-learning 指标代数独立或明确建模依赖；
  - [ ] continuous estimands 优先于阈值分类；
  - [ ] changed 与 never-change 分母分离；
  - [ ] right censoring、missingness、provider failure 和 multiplicity 规则冻结；
  - [ ] analysis unit 为独立 world/cell cluster，provider repeats 嵌套；
  - [ ] 明确“belief 声明”与“行为证据”的联合成功规则。
- 备注：`TBD`

### W2-06 — 冻结 participant backend × scaffold 矩阵

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 目标：至少引入一条可识别的 matched axis，避免再次把 model、scaffold 和 transport 完全捆绑。
- 推荐最低矩阵：2 backends × 2 scaffolds。
- 验收标准：
  - [ ] 两个 backend 使用同一 provider-independent action/result schema；
  - [ ] direct-reactive 与 stateful-scientific scaffold 的工具权限和资源预算匹配；
  - [ ] context、memory、retry、temperature/thinking、timeout 和 failure semantics 冻结；
  - [ ] model effect、scaffold effect、interaction 和 complete-system profile 分开报告；
  - [ ] classical/reference policies 只承担校准或机制对照角色；
  - [ ] 不根据 pilot 胜负删除正式方法臂。
- 备注：`TBD`

### W2-07 — 功效、资源和成本审计

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
  - [ ] 以独立 world clusters 进行功效分析；
  - [ ] 对 world、mechanism、agent、session 和交互方差作预期分解；
  - [ ] 冻结 worlds、replicates、provider repeats 和最大 provider calls；
  - [ ] 冻结 token、货币、wall time、并发和失败重试预算；
  - [ ] 明确早停仅针对基础设施/安全，不针对结果方向；
  - [ ] 输出完整资源上界和预计运行 ETA。
- 备注：`TBD`

### W2-08 — Registered Report/常规投稿路线决策

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
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
- 备注：`TBD`

### W2-09 — 完成 manifest-driven formal runner

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 代码交付物：
  - [ ] experiment-level participant runner；
  - [ ] immutable matrix/schedule manifests；
  - [ ] resume 与 right-censoring state machine；
  - [ ] provider/scaffold receipts；
  - [ ] belief/action/feedback trajectory schema；
  - [ ] exact replay、resource replay 和 hidden-boundary audits；
  - [ ] public/private split enforcement；
  - [ ] formal report generator。
- 验收标准：
  - [ ] 不依赖 notebook 或人工逐单元操作；
  - [ ] 中断后不覆盖、不替换、不重复计数；
  - [ ] private identities 不进入 agent prompt；
  - [ ] 每个估计量可追溯到 immutable trajectory records；
  - [ ] fail-closed tests 覆盖 provider failure、partial action 和 ledger mismatch。
- 备注：`TBD`

### W2-10 — provider/scaffold shakedown 与方法资格验证

- 认领：
  - [x] 未认领
  - [ ] 已认领；负责人：`TBD`
- 状态：
  - [x] 未开始
  - [ ] 进行中
  - [ ] 阻塞
  - [ ] 完成
- 优先级：P0
- 目标：只排除接口、资源和生命周期失败，不检验或筛选科学结果。
- 验收标准：
  - [ ] 每个正式方法完成独立 qualification cells；
  - [ ] schema-valid action rate、completion、receipts、cost accounting 和 replay 达标；
  - [ ] qualification worlds 不进入正式矩阵；
  - [ ] 失败修复只允许修改实现，不允许修改正式科学 estimands；
  - [ ] 形成方法冻结 hash 和资格验证报告。
- 备注：`TBD`

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
  - [ ] 检查先验坚持、证据修正、错误归因和表面恢复等行为类型；
  - [ ] 检查 process metrics 是否预测 held-out transfer；
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
  - [ ] 标题、摘要和第一张图直接呈现规律冲突下的科学适应问题；
  - [ ] 环境 Gate A、agent Outcomes 和 private confirmation 严格分层；
  - [ ] 主图围绕 detection → attribution → adaptation → transfer 的能力链；
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
- 目标：检验虚拟世界中的 process/adaptation profile 是否预测受控现实或高保真系统中的行为。
- 验收标准：
  - [ ] 选择低风险、低成本、可重复的窄域体系；
  - [ ] 虚拟与物理接口共享 typed lifecycle semantics；
  - [ ] 先 shadow mode，再进入经批准的有限闭环；
  - [ ] 安全、审批、废物和设备边界明确；
  - [ ] 迁移结果独立报告，不把小规模现实桥接泛化为全面现实有效性。
- 备注：是否进入 Work II 主文须在 formal results 前冻结：`TBD`

## 7. 完成定义

Work II 只有在以下条件全部满足时才标记完成：

- [ ] 当前 Gate A 证据绑定有效；
- [ ] 至少两个机制家族和多类规律冲突进入随机 formal world cohort；
- [ ] participant backend × scaffold 至少有一条可识别 matched axis；
- [ ] optimization、belief、attribution、adaptation 和 transfer 均有预注册指标；
- [ ] public formal matrix 与 private sealed confirmation 均达到终态；
- [ ] 能明确判断 agent 是依据证据修正规律模型，还是只取得 endpoint；
- [ ] 所有结论与 world/agent/sample scope 一致；
- [ ] 第二篇不依赖第一篇的阈值敏感 supporting result；
- [ ] 论文、代码、轨迹、数据和发布包可公开重建。
