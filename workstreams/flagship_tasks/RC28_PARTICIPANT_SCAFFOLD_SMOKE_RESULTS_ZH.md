# RC28 Participant Scaffold 小规模实验记录

> 后续 lifecycle 修复、最坏 prompt qualification 和干净的 S1/S2 结果见
> `RC28_PARTICIPANT_EXECUTION_QUALIFICATION_RESULTS_ZH.md`。本文件记录的 1,500-token
> smoke 已被后续资格结果取代，不应再用于判断当前 Direct/Stateful 方法。
> 采纳专家意见后，所有这里的 completion/lifecycle 结果只归入 O4 Autonomous Procedure，
> 不阻断 experiment-level Scientific Adaptation Track。

状态：`development smoke completed; Direct result non-confirmatory; Stateful still blocked`

日期：2026-07-25

本记录只覆盖开发命名空间中的小规模实现尝试。它不是 Gate B–E 结果，不改变已经通过并冻结的
Gate A，也不允许形成任何 publication claim。

## 1. 本轮执行范围

固定条件：

- Confirmatory Task：`reaction-to-crystallization`；
- development pair：`2c17220fd0d51bdda1bd`；
- backend：`deepseek-v4-flash`，thinking off；
- feedback：`true_feedback`；
- spectrum disclosure：`assigned`；
- scaffold：`direct_reactive` 与 `stateful_scientific`；
- 每个逻辑决策最多一次 provider call；
- prompt estimated-token hard cap：1,500；
- 开发截断：每个 changed/no-change arm 各执行 `1 pre + 1 post`；
- 所有输出均为 `formal_result=false`。

`1 pre + 1 post` 只用于验证运行链、上下文和生命周期，不能用于机制可识别性、变化检测或
scaffold 优劣结论。

## 2. 最终可用的 Direct smoke

结果目录：

`runs/development/participant_scaffold_smoke_rc28_20260725/dev_flash_direct_v15`

| 项目 | 结果 |
| --- | ---: |
| changed/no-change campaign | 2 |
| 执行 phase | 4 |
| provider calls | 72 |
| provider failures | 0 |
| input tokens | 107,722 |
| output tokens | 17,532 |
| billed cost | USD 0.0193226992 |
| 最大已发送 prompt estimate | 1,445 |
| 完整实验 | 0/4 |
| lifecycle guardrail closeout | 0 |

四个 phase 均执行到 18-operation development limit，但没有产出 final-assay-complete
experiment。它们是 procedural failures，不是低分实验。

不过，这一结果不能直接解释为“DeepSeek 不会管理生命周期”。运行后审计发现：

1. two-phase adapter 已把
   `diagnostic_actions_used_current_experiment` 和
   `diagnostic_per_experiment_action_limit` 写入 public campaign state；
2. compact prompt 白名单却没有保留这两个字段；
3. prompt 要求模型保留最后两个 closeout slots，却没有提供当前 per-experiment count。

该缺口已经修复并有定向测试，但 v15 发生在修复之前。因此 v15 的用途是证明 provider、
动作解析和 1,500-token context 可以稳定跑完整个小矩阵，并暴露 lifecycle-context
缺口；它不是有效的 Agent 性能样本。

## 3. Stateful smoke

最终停止点：

`runs/development/participant_scaffold_smoke_rc28_20260725/dev_flash_stateful_v6`

v6 在 changed/pre phase 中完成 15 次合法 provider decision：

- 15/15 响应通过 action 与 scientific-state 校验；
- 最大已发送 prompt estimate 为 1,446；
- 已计费成本约 USD 0.004587；
- 未完成实验；
- 第 16 次调用前的本地 prompt estimate 为 1,538，因超过硬上限而 fail closed；
- 超限 prompt 没有发送给 provider。

此前的 v1–v5 用于逐步验证 state schema、state projection 和预算行为。它们证明：

- 单次响应可同时产生合法 action、plan、mechanism distribution、evidence ledger、
  replan trigger 和 state hash；
- state export/restore 与篡改拒绝测试通过；
- 显式 state 并不会自动产生有效重规划；部分轨迹出现重复 `add_reagent` 或 state hash
  长时间不变；
- 较宽的 state schema 会与后期扩大的 legal-action menu 共同超过 1,500-token 上限。

当前 `stateful_scientific` 是 development candidate，不应进入正式 2×2 participant matrix。

## 4. 本轮实现和修正

### 4.1 Prompt 与动作合同

- legal action 改为扁平字段，不再诱导模型输出嵌套 `parameters`；
- 保留实际 bounds、choices 和 required fields；
- 只把当前有效动作放入 `legal_actions`；
- raw HPLC arrays、replicate signals 和重复谱图表示不进入 prompt；
- HPLC 使用峰表与 processed summary；
- 前一轮 mechanism distribution 进入最小决策记忆；
- historical best 与 recent experiment 不再重复序列化；
- prompt serialization 目标为 1,450，1,500 仍为 fail-closed hard cap；
- diagnostic → mechanism → stateful 先组合 payload，只在最外层做一次预算检查；
- lifecycle per-experiment used/limit 计数现已进入 compact current state。

### 4.2 Stateful v0.3-dev

当前持久 state 只允许：

- 一个当前科学问题；
- 最多两个计划项；
- 完整且归一化的 public candidate distribution；
- 最多两条 evidence ledger 项；
- replan trigger；
- uncertainty。

完整 state 与 hash 保存在轨迹；下一轮 prompt 在需要时只接收确定性投影：

- mechanism distribution；
- current plan step；
- latest evidence 的 supports/contradicts；
- uncertainty；
- 无 evidence 时保留 replan trigger。

每步的可证伪预测仍由共享输出中的 `expected_effect` 和 `belief_update_rule` 承担，不在
persistent state 中重复一份 prediction ledger。

### 4.3 Development-only horizon override

runner 新增 development pre/post truncation。缩短 pre phase 时：

- changed truth changepoint 与 phase reset 同步移动；
- no-change pseudo-checkpoint 同步移动；
- frozen row 不被修改；
- output 强制 `formal_result=false`；
- ordinary change-detection claim 强制关闭。

## 5. 解释边界

本轮可以支持：

1. Flash backend 能稳定消费新的 compact Direct prompt；
2. Direct 的真实 provider 链在一个完整小矩阵中达到 0 provider failure；
3. 旧的冗余上下文、动作 schema 和重复序列化确实是主要基础设施故障源；
4. Stateful schema 本身可生成、校验、持久化和恢复；
5. 当前 Stateful scaffold 尚未满足固定 1,500-token 合同；
6. lifecycle count 曾被 compact adapter 丢弃，v15 的 0/4 不能当作纯 Agent 失败。

本轮不能支持：

- Agent 是否能建立充分 pre-change reference；
- changed detection、family attribution、AUROC、Brier 或 detection delay；
- Direct 与 Stateful 的性能差异；
- DeepSeek-Pro 与 Flash 的 backend effect；
- Gate B–E 的任何通过或失败结论；
- benchmark 难度或 publication readiness。

## 6. 资源透明度

包括所有失败调试尝试在内，本目录累计：

- 366 次 provider calls；
- 约 USD 0.103238268。

正式成本审计只应采用最终冻结的 clean runs；上述总额仅用于开发支出透明度，不进入方法
比较。

## 7. 下一批最小 TODO

### P0：再次运行 provider 前必须完成

- [x] 将 lifecycle used/limit 字段纳入 compact prompt；
- [ ] 为 Stateful 的最终 response schema 再做一次静态压缩，使最坏 legal-action menu
  下也留有至少 50-token 余量；不得提高 1,500 hard cap；
- [ ] 新增从真实晚期 action menu 构造的离线 prompt-budget fixture；
- [ ] 明确 phase 中 0 complete experiment 时的
  `reference_acquisition_failed` 与 Gate B/D 不可评价状态，不能只靠下游推断；
- [ ] 对当前改动运行 targeted lint/type/test，不运行全仓测试。

### 下一次 development smoke

- [ ] 只跑 Flash-Direct 的一个 `1 pre + 1 post` changed/no-change pair，验证 lifecycle
  counter 修复是否改变 closeout；
- [ ] Direct 通过运行完整性后，再跑同一 pair 的 Stateful；
- [ ] 两者均无基础设施阻断后，扩展到 `2 pre + 2 post`；
- [ ] Flash 两个 scaffold 稳定前，不启动 Pro cells；
- [ ] 不查看或使用 formal/private cohort。

当前 go/no-go：

```text
Gate A: passed and frozen
Compact Direct runtime: development-shakedown passed
Direct Agent performance: not evaluated cleanly
Stateful schema/runtime: partially implemented, prompt-budget blocked
Formal participant methods: not frozen
Formal B–E execution: prohibited
```
