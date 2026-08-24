# Work II W2-51 evidence-to-action 正式收口

状态：**TERMINAL / SCIENTIFICALLY REJECTED BEFORE PROVIDER**  
日期：2026-08-24

## 1. 结论

W2-51 没有进入 provider participant cohort。正式 provider-free preparation 在第 8 个
task-world cluster 触发预设 oracle rank gate：`reaction-to-crystallization / seed836245547`
的候选排序 Spearman `rho=0.738095`，低于冻结阈值 `0.80`。该 cluster 的 candidate
opportunity gate 通过，oracle fit 与 candidate 的重叠为 `0`，因此这不是候选过平、结果泄露、
执行污染或平台失败，而是 fresh formal world 上的 oracle-law 科学资格失败。

按实验说明，oracle gate 失败拒绝 oracle 对照设计；不得查看结果后更换 formal world、放宽阈值、
替换 seed 或补跑获取更有利结果。W2-51 因而以
`scientifically_rejected_before_provider` 终止。

## 2. 冻结问题与设计

计划问题是：自主实验能否因果性地改善未见完整 ActionPlan 的预测与终端选择，以及价值在
evidence、learned law 和 action 之间何处损失。冻结设计为：

- `3` 个任务 × `5` 个 fresh formal worlds × `3` 个 priors × `5` 个 information conditions；
- 计划 `225` 个 fresh participant sessions；
- `45` 个 autonomous donors 各执行 `12` 轮，计划 `540` 次 participant experiments；
- 五条件为 no evidence、yoked evidence、autonomous exploration、learned-law-only 和
  oracle-law；
- 每个 task-world 的 provider-free preparation 固定执行 `8` 个 candidate truth、`8` 个
  checkpoint truth 和 `96` 个 disjoint oracle-grid truth，共 `112` 条，并逐条 exact replay；
- oracle 对 8 个候选的 Spearman 排序相关必须达到 `rho>=0.80`。

只有全部 `15/15` formal task-world clusters 通过 candidate 与 oracle 门控，participant
operational canary 才具备科学执行资格。

## 3. 正式执行与精确分母

第一次正式 preparation 因长 truth helper 未在 60 秒内提供内部 liveness 而停止；它没有形成
完整 cluster，作为 platform-invalid 历史尝试原样保留且没有复用。加入每 30 秒 liveness 后，
科学问题、coverage、seeds、阈值和 stop rules 全部不变，并从第一个 cluster 在新输出根重启。

正式 restart 的终态为：

| 项目 | 结果 |
|---|---:|
| 计划 task-world clusters | 15 |
| 完成全部 truth 与 replay 的 clusters | 8 |
| candidate gates | 8/8 passed |
| oracle gates | 7/8 passed |
| 因科学门控未启动 clusters | 7 |
| provider-free truth | 896/1,680 |
| exact replay | 896/1,680 |
| evaluator provider calls | 0 |
| participant sessions | 0/225 |
| participant provider calls | 0 |
| participant experiments | 0/540 |
| outcome-based replacements | 0 |
| formal-world replacements | 0 |

已通过的七个 clusters 包含 electrochemical `5/5` 和 crystallization 前两个 formal worlds；
对应 oracle `rho=0.8095--0.9762`。第八个 crystallization formal world 完成 `112/112`
truth 与 exact replay 后，oracle `rho=0.738095`、Top-1 disagreement、fit/candidate overlap `0`，
从而触发冻结门控。其余两个 crystallization worlds 与五个 reaction-safety worlds 均标记为
`not_started_due_to_provider_free_gate_failure`，不构成缺失 participant outcome。

## 4. 科学解释

该结果说明，development worlds 上 `15/15` 通过的 32-global + 64-neighborhood oracle-law
构造没有在 fresh formal crystallization worlds 中保持足够稳健的候选排序正确性。它否定的是
当前五条件设计里的 oracle 对照资格，而不是 participant agent 的探索能力：没有 participant
session 被调用，因此 autonomous-minus-no-evidence、yoked-minus-no-evidence、
autonomous-minus-yoked、learned-law-minus-no-evidence 和 oracle-minus-learned-law 五个预设
对比均未估计。

W2-50 仍然提供多任务未见完整 ActionPlan 终端排序的有界描述性证据，但它没有 no-evidence 或
pre-exploration control。W2-51 原本要补上的 causal evidence-to-action 对照现已正式关闭，不能把
W2-50 的终端结果事后升级为因果 action-transfer 结论。

## 5. 证据与可复现入口

- 机器收口：`work-ii-evidence-to-action-formal-closeout-v0.1.json`
- 冻结实验说明：`../WORK_II_EVIDENCE_TO_ACTION_CAUSAL_DECOMPOSITION_EXPERIMENT_NOTE.md`
- 正式执行器：`../../../scripts/run_work_ii_evidence_to_action_formal.py`
- retained formal output：`runs/formal/w2-51-e2a-20260824-restart1`
- platform-invalid predecessor：`runs/formal/w2-51-e2a-20260824`

内部 source binding、commit、run identifiers 和派生 artifact 路径仅属于证据记录，不进入读者正文。
