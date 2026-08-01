# G2 资源账本与真实 Codex qualification 状态

更新时间：2026-08-01

> 当前权威状态已更新至 v0.4。完整结果、指标和 roadmap 见
> `workstreams/G2_CODEX_SOL_MEDIUM_MCP_5X2_V04_RESULTS_ZH.md`。
> 本文后续的 2026-07-31 quota 与旧 qualification 内容仅作历史记录。

## 当前结论（2026-08-01）

G0 保持 baseline。G2 的原生 Codex STDIO MCP、逐操作 affordance、campaign 资源账本、batch 生命周期、provider receipt 和 exact replay 已闭环。

真实 `gpt-5.6-sol / medium` 状态：

- seed 3 nominal K6 v0.4 qualification：59 operations，6/6 final assay，通过。
- 5 world × 2 material-information v0.4 matrix：10/10 cells，60/60 final assay，通过。
- 815 operations，164 次非终点表征与 60 次 final assay（共 224 个 `measure` 操作），0 invalid/resource rejection。
- 所有资源账本、物理配对、provider session 和 exact replay 通过。
- audit v0.3 哈希：`bc7495315745272c95fb326b7b50fb509081ad70323354899a233abac6c7b4a9`；原始轨迹、资源账本和 provider receipts 未改变。
- 新增发现—保留—恢复审计：opaque/nominal 平均在线保留率为 52%/72%，平均终点/最佳为 67%/94%，平均最佳发现进度为 32%/80%。该结果说明发现速度与保留/终局优化可能解耦，仍仅作 n=5 开发性观察。

## 历史记录（2026-07-31）

## 已实现的 G2 修复

1. `discard_batch` 仅在 autonomous campaign G2 中暴露，必须带 `reason`，消耗 operation attempt，已消耗物料/风险/成本不返还。
2. campaign ledger 记录 `discarded_batches`、`closed_batches`，并绑定 preflight、outcome、snapshot、integrity replay、hash 和 public state。
3. agent-facing `available_actions`、`action_schema`、`validate_action` 现在使用同一份资源规则：
   - stock 剩余量收窄加料 bounds；
   - stock 耗尽隐藏对应加料操作；
   - non-final instrument quota 和 per-instrument quota 收窄测量 choices；
   - final assay quota、operation attempts、vessel starts 用尽时 fail closed；
   - 账本预览不写入事件，真正扣账仍只发生在 `env.step` preflight/outcome。
4. public campaign resource state 新增 `lifecycle_reserve`：公开当前 batch 最低 closeout 操作数、未来 batch 的 final-assay/discard reserve 和 advisory floor。它不做隐式预留，仍由 Agent 自主决定。
5. Codex session receipt 对 provider `error`/`turn.failed` 只保留 hash 和 byte count，不保留错误正文，便于审计而不泄露 provider 文本。
6. 失败 run 的 `accepted_operation_count` 绑定 durable trajectory，而不是只读空的异常路径内存 history。
7. qualification token envelope 改为按 primitive-operation capacity 估计。Codex 的 `input_tokens` 是多轮累计值并包含 cache hit，不能按 batch 数简单线性估计。

## 真实 run 证据

### opaque K=1

目录：

`runs/development/g2-autonomous-electrochemical-seed0-opaque-k1-qualification-v4/`

- 14 operations，1 batch，1 final assay。
- provider session audit 通过，usage complete，lab tool integrity 通过。
- exact deterministic replay 通过。

### opaque K=2

目录：

`runs/development/g2-autonomous-electrochemical-seed0-opaque-k2-qualification-v2/`

- 23 operations，2 batches，2 final assays，0 discard。
- `closed_batch_count=2`，`right_censored_open_experiment=false`。
- 2 个 Codex session 均 completed，final payload、usage、integrity 全通过。
- exact deterministic replay 通过。
- provider input tokens：862,283；output tokens：7,609。

### opaque K=6

首轮目录：

`runs/development/g2-autonomous-electrochemical-seed0-opaque-k6-qualification-v1/`

前两批已完成（18 operations），第三个 session 在提交首个 operation 前收到 provider `turn.failed`，没有 tool event、没有 accepted action，lab tool integrity 仍通过。

第二轮目录：

`runs/development/g2-autonomous-electrochemical-seed0-opaque-k6-qualification-v2/`

首个 provider turn 即同样失败，说明不是 batch 状态或 session 收尾竞态。

最小 Codex CLI 探针返回账户级错误：

`You've hit your usage limit ... try again at Aug 5th, 2026 12:29 PM.`

该错误发生在 provider 外部状态，当前不能通过仓库代码修复。恢复后应从新的 K=6 output root 重跑，不要复用 v1/v2 目录。

## 验证结果

G2 相关离线回归：

```text
68 passed
```

覆盖 campaign resources、resource integration、interactive Codex、Codex IPC、G2 matrix、campaign audit。

全仓库 pytest 当前仍有既有 baseline/G0 与旧 golden 失败；本轮不修改 G0，也不把这些失败重新解释为 G2 资源账本失败。

## 恢复后的执行顺序

1. provider quota 恢复后，使用新的目录重跑 opaque K=6。
2. 确认 6 个 batch 的 vessel start、close、final assay/discard、provider receipts、usage 和 exact replay。
3. 再做 nominal K=1/K=2/K=6 qualification。
4. 最后才考虑完整 5×2 matrix；G0 仍只作为 baseline。

## 三臂已知／未知／错配设计（2026-07-31）

三臂资源设计已单独冻结，见：

- `workstreams/G2_TRIARM_TEST_DESIGN_FREEZE_ZH.md`
- `configs/benchmark/g2_autonomous_electrochemical_material_3x3_v0.1_dev.json`
- `scripts/run_g2_autonomous_material_triarm.py`

离线标定已经比较 lean-k4、diagnostic-k6、adaptive-k6、diagnostic-k8 和 rich-control；默认正式 envelope 为 `lean-k4-one-stage`。真实 Codex 三臂 runner 已支持按 world seed 分阶段执行，并在每个 cell 之后绑定 trajectory、resource ledger、provider receipts、exact replay 和三臂 paired analysis。真实 provider 运行仍需等待账户 quota 恢复。
