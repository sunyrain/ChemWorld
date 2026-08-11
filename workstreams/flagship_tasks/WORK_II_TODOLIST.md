# Work II TODO — Experimental Intelligence

最后更新：2026-08-11

当前状态：实验架构与 A-E 核心设计已经冻结；正式 participant outcomes 尚未执行。当前只允许设计、确定性
诊断和已明确授权的资格实验，不得直接启动 public/private formal matrix。

## 1. 研究目标与边界

中心问题：

> 在固定隐藏规律、公开契约和资源预算下，agent 能否通过自主实验修正其初始世界模型，并依次把证据转化为
> 预测、可执行规律、行动和可迁移知识；若不能，能力链在哪一环断裂？

能力链：

`initial model → experiment selection → evidence → prediction/update → executable law → action → transfer`

- Work I 负责可组合世界、测量有效性、资源账本、事务语义和 exact replay。
- Work II 负责初始世界模型干预、错误先验修正、规律总结、knowledge-to-action 和 transfer。
- 规律在每个 world 内固定；不把运行中物理规律变化作为主问题。
- 当前 participant method 只有 WellAU `gpt-5.6-sol`、medium reasoning、Codex harness + ChemWorld MCP。
  结果只能表述为这个完整 agent system 的能力，不能外推为裸模型或跨模型排名。

## 2. 冻结执行语义

- 一个 formal cell 是 `task × world seed × initial-model arm × participant method`。
- 每个 cell 只使用一个长驻 Codex process/session；模型读取上一公开 outcome 后逐 operation 决策。
- 每个 free-discovery cell 包含 4 个 complete experiments，checkpoint 位于实验前、实验 1 后、实验 2 后和最终。
- 4 个 experiments 共享同一 hidden law、session context 和 CampaignResourceLedger；新 batch 重置物理状态，
  但资源、历史和剩余预算不重置。
- complete experiment 从新 batch 的首个 vessel-starting operation 开始，以 committed `final_assay` 或
  允许的 discard 关闭；`terminate` 本身不等于 final assay。
- 独立统计单位是 `task × world seed` cluster。operations、experiments、checkpoints、queries、blind
  replicates 和 provider retries 均为嵌套观测。
- 三个 arm 为 `opaque / aligned / misspecified`。同一 cluster 内 world、noise、resource、safety、公开契约
  和信息预算匹配，只改变一个 agent-facing initial-model locus。
- 科学或方法失败保留且不替换；只有尚未形成 scientific trajectory 的纯基础设施缺失可 resume 一次。
- 每个适用 task block 到 5 个 world seeds 即停止；超过 5 seeds 必须重新取得用户审核。
- 长任务每 30 秒输出 liveness；用户可见进展至少包含当前 block、completed/total、throughput 和 ETA。

## 3. 实验矩阵

### 3.1 Study A — prior-conditioned free discovery

| Block | 操纵层级与任务 | 独立 clusters | Participant sessions | Complete experiments | 状态 |
|---|---|---:|---:|---:|---|
| A-E public | entity/ontology；electrochemical、crystallization、distillation、partition、reaction safety | 25 | 75 | 300 | 设计已冻结，执行未授权 |
| A-E private | 与 public 同任务的 sealed world-held-out replication | 25 | 75 | 300 | commitment 已冻结，public 分析后一次执行 |
| A-S | structural/mechanistic；计划 2 tasks × 5 worlds | 10 | 30 | 120 | 候选阶段 |
| A-P | parametric；计划 2 tasks × 5 worlds | 10 | 30 | 120 | electrochemical 环境门控与单-world D1 通过；第二任务及 5-world freeze 待定 |

A-E 是唯一 primary confirmatory block。A-S/A-P 是 additive registered secondary blocks，不改变 A-E 的
H3、alpha、worlds、failure rules 或正式分母。

Primary H3：

[
C_{prior} =
(E_{misspecified,pre}-E_{misspecified,final})
-
(E_{aligned,pre}-E_{aligned,final})
]

成功要求同时满足：

- `C_prior > 0` 的预注册单侧检验；
- misspecified arm 自身预测误差改善；
- aligned arm 不劣于冻结容差 `-0.05`；
- 失败、缺失和 right-censoring 按预注册规则进入分母。

### 3.2 Study B — matched-evidence falsification

- 目的：区分“没有主动寻找反证”和“看到同样反证后仍不更新”。
- 规模：2 loci × 1 prespecified task × 5 worlds = 10 clusters；三臂共 30 fresh sessions。
- 每个 session 提交 pre-evidence prediction/confidence，读取相同 contradictory evidence packet，再提交
  post-evidence prediction/confidence 和一个 action/recommendation。
- B 不属于 participant-owned free discovery，不进入 Study A 的 experiment-selection 或 resource-efficiency
  分母。
- 状态：candidate；若未在 A-E outcomes 被查看前冻结，只能作为 exploratory evidence。

### 3.3 Study C — prediction → law → action evaluator

- 不新增 participant session，不调用 provider。
- 对 Study A terminal outputs 计算 held-out prediction error、typed executable-law error、
  `L_prediction→law`、`L_law→action` 和 blind recommendation gain。
- A-E public 每 cluster 4 个共享 truth queries，共 100 truth executions；completed cells 最多 450 blind replays。
- private block使用同一 evaluator contract，但 evaluator trajectory 与 participant ledger 严格分离。

### 3.4 Study D — context-reset artifact-only transfer

- 目的：检验 agent 产生的规律能否作为独立知识对象进入新组合世界。
- 规模：2 source-pair→target composition families × 5 linked targets = 10 clusters。
- 四个 artifact arms：none、token-matched raw evidence、prose law、executable law。
- 共 40 fresh target sessions，暂定 160 complete experiments。
- target agent 使用全新 Codex process/context，只能读取被分配的 artifact。
- A-E private 是 within-family replication，不得改称 compositional transfer。
- 状态：candidate；constructor、artifact budget、contamination audit 和 evaluator 均未冻结。

## 4. Claim ladder

| Claim package | 必需证据 | 允许的最高表述 |
|---|---|---|
| C1 | A-E public + A-E private + C | entity-level explicit-prior correction |
| C2 | C1 + terminal A-S + A-P，且每 locus 两个 task | general initial-world-model effects |
| C3 | C2 + B | acquisition failure 与 updating failure 的机制区分 |
| C4 | C3 + D | context-reset compositional transfer of executable laws |

缺少后续 block 时自动收窄标题、摘要和结论，不为维持大标题而补做未资格验证的矩阵。

## 5. 试验规模与 ETA

### 5.1 实测基线

当前最可靠的 WellAU 实测基线来自三个完整五-seed development blocks：

- 45 scheduled cells、176/180 complete experiments；
- task wall-time sum 为 11,850.3 s，即 3.29 h；
- 15 个三臂 world triplets，平均 13.2 min/triplet；
- electrochemical 8.9 min/triplet、crystallization 20.4 min/triplet、distillation 10.2 min/triplet；
- 当前全局并发冻结为 3 cells，即同时执行同一个 world 的三臂；cell 内不并发。

ETA 场景采用：

- 理想：10 min/triplet，无 resume；
- 正常：16 min/triplet，包含常规 evaluator、写盘和少量恢复余量；
- 不乐观：30 min/triplet，包含慢任务和局部基础设施恢复；
- hard cap：按 method resource contract 计算，不代表预期耗时。

### 5.2 分 block provider 执行时间

| Block | Sessions | Triplet-equivalent waves | 理想 | 正常 | 不乐观 | Hard cap |
|---|---:|---:|---:|---:|---:|---:|
| A-E public | 75 | 25 | 4.2 h | 6.7 h | 12.5 h | initial 47.5 h；全 resume 95 h |
| A-E private | 75 | 25 | 4.2 h | 6.7 h | 12.5 h | 单独预算，不能借用 public ceiling |
| A-S + A-P | 60 | 20 | 3.3 h | 5.3 h | 10.0 h | 待各 task qualification 后冻结 |
| B | 30 | 10 short waves | 0.7 h | 1.5 h | 4.0 h | 待 evidence-session contract 冻结 |
| D | 40 | 14 waves | 2.3 h | 3.7–5.0 h | 7–10 h | 待 composition runner 冻结 |
| C evaluator | 0 | local execution | <0.5 h | 0.5–1 h | 1–2 h | 0 provider calls |

这些是 provider execution wall time，不包含 intervention 设计、资格门控、public/private 中间分析冻结和论文整合。

### 5.3 累计规模

| 最高 claim | Sessions | Complete experiments | 理想执行时间 | 正常执行时间 | 不乐观执行时间 |
|---|---:|---:|---:|---:|---:|
| C1 | 150 | 600 | 8–9 h | 13–17 h | 25–36 h |
| C2 | 210 | 840 | 12–13 h | 18–23 h | 35–50 h |
| C3 | 240 | 840 | 13–14 h | 20–25 h | 38–55 h |
| C4 | 280 | 1,000 | 15–17 h | 24–32 h | 45–65 h |

按45-cell WellAU开发块的实测 token 均值线性估算：

| Claim | Cumulative input | Uncached input | Output |
|---|---:|---:|---:|
| C1 | 约 198 M | 约 22 M | 约 1.36 M |
| C2 | 约 277 M | 约 31 M | 约 1.90 M |
| C3 | 不高于约 317 M；B 应明显更短 | 不高于约 35 M | 不高于约 2.17 M |
| C4 | 约 370 M | 约 41 M | 约 2.53 M |

A-E public 的现有 accepted-cell hard cap 为 324 M input、43.2 M uncached input 和 3.24 M output；
若所有 cell 都耗尽唯一基础设施 resume，provider-attempt hard cap 翻倍。其他 blocks 必须独立冻结预算，不能用
线性估算替代正式 ceiling。货币 ETA 暂不填写，直到 WellAU cache-hit/cache-miss/output 单价和用户批准的
currency ceiling 可验证。

### 5.4 Calendar ETA

在用户及时完成 route、预算和执行授权，且不出现平台级缺陷时：

| 目标 | 理想日历时间 | 正常日历时间 | 不乐观 |
|---|---:|---:|---:|
| C1 可分析结果 | 2–3 working days | 3–5 working days | 1–2 weeks |
| C2 initial-world-model 结果 | 5–7 working days | 7–10 working days | 2–3 weeks |
| C3 机制归因结果 | 7–9 working days | 9–12 working days | 3–4 weeks |
| C4 完整 transfer 结果 | 9–12 working days | 12–18 working days | 3–5 weeks |

C1 之后每一级都包含新增实现和独立资格，不应把纯 provider runtime 当作完整项目 ETA。

## 6. 当前状态

### 已完成

- Work I / Work II claim boundary、current Gate A binding 和 five-task A-E world cohort；
- A-E primary H3、analysis unit、failure/censoring 和 evaluator contracts；
- persistent Codex session + operation-level MCP runner、shared campaign ledger、exact/resource replay；
- A-E 75-cell manifest preflight、held-out truth compiler、blind evaluator 和 formal dataset builder；
- agent-facing `initial_world_model` 输入与 hidden arm identity 防泄露；
- parametric/structural environment diagnostic builders 和 machine-readable summaries。
- electrochemical parametric seed-1 D1：3/3 persistent participant sessions、12/12 experiments、
  4/4 shared truth queries 和 18/18 paired blind replays 完成且 exact replay；未重跑 participant 轨迹。

### Intervention screening

| Candidate | Result | Decision |
|---|---|---|
| electrochemical parametric v1, seed 0 | repaired 20/20 exact replay；gap `0.0055333 < 0.10` | 不接纳 |
| distillation structural v1, seed 0 | 4/4 exact replay；gap `0.0303474 < 0.10` | 不接纳，不调用 provider |
| electrochemical parametric v2, seed 1 | 20/20、0 failures、exact replay；gap `0.5849161 ≥ 0.10` | environment-qualified |
| electrochemical parametric D1, seed 1 | 3/3 cells、12/12 experiments、4/4 truth、18/18 blind exact replay | 单-world D1 通过；等待用户审核后才可冻结 5-world block |

未通过的 diagnostic 只说明 intervention 不可识别，不能解释为 agent 缺乏相应推理能力。

### 当前 blockers

1. W2-17：冻结两个 structural candidates 和第二个 parametric task，并完成 environment-only screens；
   electrochemical parametric 5-world 扩展等待本次 D1 的用户审核。
2. W2-10：当前 WellAU persistent-session method 的独立三臂真实资格收据尚未完成。
3. W2-07：正式价格来源、currency ceiling 和 qualified expected ETA 尚未签字。
4. W2-08：正式数据采集路线尚未由用户锁定。
5. W2-11：以上输入完成后生成最终 preregistration freeze receipt。

在这五项完成前，W2-12 public formal execution 保持关闭。

## 7. 下一执行顺序

### P0 — 先完成 C1 launch gates

- [ ] 冻结并运行 current A-E method qualification triplet；只按 harness/lifecycle/replay 资格，不按科学效果。
- [ ] 用户冻结 submission route、qualification/formal currency ceilings 和 failure-escalation signoff。
- [ ] 生成 W2-11 final freeze receipt，确认 public 75 cells、150 provider-attempt hard cap 和执行命令。
- [ ] 执行 A-E public：25 seed triplets；只报告 blinded progress。
- [ ] 生成 public analysis 并冻结 hash。
- [ ] 解封并一次性执行 A-E private；不得因结果方向重跑。
- [ ] 完成 Study C evaluator 和 C1 分析。

### P1 — 并行准备 C2，但不抢跑 provider

- [ ] Structural roster：优先筛选 reaction-to-crystallization 与 reaction-safety-constrained。
- [x] Electrochemical parametric：environment gate 与单-world D1 participant/evaluator pilot 已完成；不自动扩展。
- [ ] Parametric roster：筛选 flow-reaction temperature/residence-time
  或 flow-rate operating-window law。
- [ ] 新 checkpoint 写通用字段 `initial_model_available` 与 `challenged_model_fields`；历史 entity 轨迹只读兼容。
- [ ] 每个通过环境门控的 task 先执行一个三臂 D1 pilot，再冻结 5-world block。

### P2 — 条件性扩展

- [ ] 只有要区分 evidence seeking 与 belief updating 时才执行 B。
- [ ] 只有要保留 “transferable laws” 主张时才实现并执行 D。
- [ ] Observation-model locus 当前 DEFERRED，不扩成第四个完整矩阵。

## 8. Task tracker

| Work package | 状态 | 说明 |
|---|---|---|
| W2-01–06 | DONE | scope、questions、A-E cohort、estimands、participant contract |
| W2-07 | DOING | power/resource 已完成；价格、currency、qualified ETA 待定 |
| W2-08 | DOING | route 等待用户锁定 |
| W2-09 | DONE | manifest-driven runner 与 evaluators |
| W2-10 | DOING | current-method real qualification 待完成 |
| W2-11 | DOING | 等待 W2-07/08/10 后 final freeze |
| W2-12 | NOT STARTED | A-E public 75-cell formal matrix |
| W2-13 | NOT STARTED | A-E private 75-cell one-shot confirmation |
| W2-14 | NOT STARTED | confirmatory analysis、robustness、failure audit |
| W2-15 | DOING | manuscript skeleton/figures 已有；formal results 待补 |
| W2-17 | DOING | non-entity intervention qualification |
| W2-18 | CONDITIONAL | A-S/A-P registered extensions |
| W2-19 | CONDITIONAL | matched-evidence probe |
| W2-20 | CONDITIONAL | artifact-only compositional transfer |

## 9. 不可违反的规则

- 不根据 agent outcome 选择、删除或新增 task/world/arm。
- qualification 修复平台缺陷后，受影响 qualification block 从第一单元重新开始；正式 scientific trajectory
  一旦形成则永不替换。
- provider retry 不产生新科学样本；失败、right-censored 和 unscorable cells 全部报告。
- participant trajectory 与 evaluator truth/blind trajectory 分开，资源和分母不混用。
- endpoint success 不等于 law discovery；文字总结不等于 executable law。
- 一项 locus 只有一个 task 达到终态时，只能作为 task-specific case study。
- private within-family replication 不能支持 compositional transfer。
- C4 未完成时，标题和摘要不得声称 transferable laws。
- raw provider payload、credentials、`runs/` 和 private world identities 不进入 Git。

## 10. 当前证据入口

- Formal design：`configs/benchmark/work_ii_formal_design_v0.1.json`
- Analysis plan：`configs/benchmark/work_ii_analysis_plan_v0.1.json`
- Power/resource audit：`workstreams/flagship_tasks/reports/work-ii-analysis-power-audit.json`
- Formal preflight：`workstreams/flagship_tasks/reports/work-ii-formal-matrix-runner-preflight-v0.1.json`
- Current-method readiness：`workstreams/flagship_tasks/reports/work-ii-method-qualification-readiness-v0.1.json`
- WellAU development timing：`workstreams/flagship_tasks/reports/work-ii-three-task-five-seed-campaign.md`
- Parametric v2 diagnostic：
  `workstreams/flagship_tasks/reports/work-ii-parametric-initial-model-diagnostic-seed1-v2-20260811.json`
- Parametric v2 D1 participant/evaluator report：
  `workstreams/flagship_tasks/reports/work-ii-parametric-initial-model-pilot-evaluation-20260811.json`
- Structural v1 diagnostic：
  `workstreams/flagship_tasks/reports/work-ii-structural-initial-model-diagnostic-20260811.json`

Git history保存本文件过去的详细任务卡和运行日志；不再在当前主控页重复维护历史版本。
