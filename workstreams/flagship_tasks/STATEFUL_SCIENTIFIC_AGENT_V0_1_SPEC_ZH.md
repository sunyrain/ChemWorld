# Stateful Scientific Agent v0.1 原始规格

> 2026-07-25 development 更新：当前代码候选为 `v0.4-dev`，本文件保留为原始设计记录，
> 不再代表可冻结 schema。v0.4 将 persistent state 收紧为最多两个计划项、两个证据项和
> 1,400 字符；逐候选预测不再重复持久化，而由每步共享的 `expected_effect` 与
> `belief_update_rule` 承担。完整 state 留在轨迹，下一轮只接收确定性决策投影。
> 最坏合法 prompt fixture 已通过且没有运行时截断；Flash-Stateful S2 仍出现真实的
> lifecycle-autonomy failure，见 `RC28_PARTICIPANT_EXECUTION_QUALIFICATION_RESULTS_ZH.md`。
> 采纳专家意见后，该继承式 operation-level 实现只保留为 Autonomous Procedure Track 的
> 历史开发候选。Scientific Adaptation Track 已改用组合式 experiment-level interface，见
> `src/chemworld/agents/scientific_adaptation.py`；以下 schema 不再控制科学主实验。

状态：`historical operation-level candidate; Autonomous Procedure Track only`

适用实验：独立的 operation-level Autonomous Procedure development，不进入科学主实验的
四方法 `2×2` core matrix。

## 1. 设计目标

`stateful_scientific_agent_v0.1` 只增加持久、可审计的科学认知结构，不增加任何隐藏物理
知识。它与 Direct Reactive 共享同一个 backend、公共 observation、历史适配器、工具、动作
空间、实验预算和 lifecycle contract。

> Scaffold 提供认知结构，不提供科学答案。

正式对比回答：

> 当基础模型和公共信息相同，模型自维护的计划、证据账本、预测和机制信念是否改善实验决策？

## 2. Direct 与 Stateful 的精确差异

| 能力 | Direct Reactive | Stateful Scientific |
| --- | --- | --- |
| compact current observation | 相同 | 相同 |
| 最近 4 次决策 | 相同 | 相同 |
| 最近 4 个实验摘要 | 相同 | 相同 |
| public spectrum/schema/history retrieval | 相同 | 相同 |
| candidate definitions | 相同 | 相同 |
| physical experiment budget | 相同 | 相同 |
| provider calls per logical decision | 1 | 1 |
| 自写 campaign plan | 无 | 有 |
| 自写 scientific notebook | 无 | 有 |
| 自写 predictions by hypothesis | 无持久状态 | 有 |
| 自写 mechanism belief state | 仅当前 decision 输出 | 跨轮持久 |
| replan trigger | 无持久状态 | 有 |
| lifecycle/budget public facts | 相同 | 相同 |

Direct 已经能读取共享的短历史，不是 stateless strawman。Stateful 的增量仅是模型自己生成并
在后续 prompt 中重新读取的结构化科学状态。

## 3. 一次调用合同

第一轮 core matrix 中，Direct 与 Stateful 每个 logical decision 都最多发起一次 billable
provider request。基础设施 retry 遵循同一 provider policy，并单独记账。

Stateful 在一次结构化响应中同时返回：

1. 下一 public operation；
2. 当前科学状态的完整新版本；
3. 当前 mechanism distribution；
4. observation 前声明的可检验预测或对上轮预测的结算；
5. 可选的 public detail request。

Harness 只做 schema、类型、大小、引用完整性和 public-action validation，不修复科学内容。
无效科学状态与无效 action 一样进入正式 failure ledger。

该调用合同使第一轮 scaffold effect 不被“Stateful 获得更多隐藏 LLM 调用”混淆。若后续研究
多调用 deep-agent loop，必须作为新的 method cell 和资源合同单独预注册。

## 4. Candidate state schema

候选响应结构：

```json
{
  "action": {
    "operation": "public operation",
    "parameters": {}
  },
  "scientific_state": {
    "current_question": "one falsifiable question",
    "campaign_plan": [
      {
        "step": "short planned experiment",
        "purpose": "what it distinguishes",
        "status": "pending|active|completed|abandoned"
      }
    ],
    "mechanism_distribution": {
      "public_candidate_label": 0.0
    },
    "predictions_by_hypothesis": {
      "public_candidate_label": {
        "observable": "public observable name",
        "direction_or_range": "model-generated prediction",
        "falsifier": "public result that would reduce support"
      }
    },
    "evidence_ledger": [
      {
        "evidence_id": "public observation or spectrum ID",
        "supports": ["public candidate labels"],
        "contradicts": ["public candidate labels"],
        "interpretation": "model-generated concise interpretation"
      }
    ],
    "replan_trigger": "public future condition",
    "uncertainty": 0.0
  },
  "expected_effect": "short public expectation",
  "diagnostic_target": "what this action distinguishes",
  "expected_information_gain": 0.0,
  "belief_update_rule": {
    "if_supported": "model-generated update",
    "if_not_supported": "model-generated update"
  },
  "request_historical_spectrum_id": null,
  "request_action_schema_id": null,
  "request_experiment_summary_id": null
}
```

正式 schema 可以在 development 中收紧，但不能在 formal result 后修改。

## 5. State origin 与 leakage ledger

每个 state field 必须带有可追溯来源类别：

- `public_environment_fact`：当前预算、lifecycle state、合法 action signature；
- `public_observation_reference`：Agent 引用的 measurement/experiment/spectrum ID；
- `agent_generated`：plan、interpretation、prediction、belief、replan trigger；
- `deterministic_harness_bookkeeping`：schema version、state hash、长度和时间索引。

Harness 不得写入 `agent_generated` 内容。Stateful prompt 中所有持久科学文本必须逐字来源于
该 Agent 的既往合法响应，或由预注册的确定性截断器处理后保留来源 hash。

显式禁止进入 state 或 prompt：

- hidden truth、hidden intervention parameters；
- changepoint、changepoint support 或 phase/reset indicator；
- A2/A3 posterior、reference certificate 或 Gate A pass detail；
- diagnostic relation graph、oracle predictives、likelihood 或 information ranking；
- candidate-world rollout、未来 observation distribution；
- family-specific 最优 action；
- private seed、provider secret 或 evaluator-only metric。

任何禁止字段出现都属于 leakage failure，使对应 development run 无效；若在 formal code path
发现，则停止并按预注册的 infrastructure-invalidated 分支处理，不能继续产生性能结论。

## 6. State 大小与压缩

Development 候选上限：

- environment view：2,050 estimated tokens，与 Direct 相同；
- 整个 decision prompt：4,150 estimated tokens；
- Agent memory segment：1,350 estimated tokens；
- `scientific_state`：最多 1,400 个 JSON 字符；
- campaign plan：最多 2 个条目；
- evidence ledger：最多 2 个条目；
- belief distribution：必须覆盖且仅覆盖公开候选，非负并归一化；
- 禁止原始 spectrum arrays、replicate curves 和重复 observation views。

超过上限时不得让 LLM 额外调用“记忆压缩”。第一轮使用确定性、版本化压缩：

1. 保留 active plan；
2. 保留每个 candidate 最新 active prediction；
3. 按 evidence ID 去重；
4. 优先保留模型标记为高诊断价值且仍未结算的证据；
5. 其余条目进入只供审计、不再进入 prompt 的完整 trajectory。

压缩器必须输出 before/after hash 和被移除 public IDs，不能改写信念或科学解释。

## 7. 状态转换

每个 logical decision：

```text
load validated prior scientific_state
  → build shared compact public context
  → attach bounded state
  → one provider request
  → parse action + complete next state
  → validate public references and schema
  → persist state hash
  → execute public action
  → append public outcome to next context
```

Stateful 不能在看到 observation 后回写“此前预测”。prediction ledger 必须区分：

- `declared_before_observation`；
- `resolved_after_observation`；
- `abandoned_before_observation`。

所有时间戳使用 public campaign/experiment/operation index，不暴露隐藏 phase。

## 8. Lifecycle autonomy

Stateful 可以自己计划：

- 新建 experiment；
- 选择操作和 measurement；
- 结束 experiment；
- 请求 final assay；
- 结束 campaign。

Harness 只拒绝非法动作，不提供替代动作，不自动 closeout，不自动选择 assay。格式、terminate、
assay 或生命周期失败进入 Gate E autonomous protocol-failure 统计。Assisted scientific score
在隔离副本中产生，assisted history 不回流 autonomous state。

## 9. Export、restore 与因果分叉

`export_prompt_state()` 必须包含：

- 共享 direct-history state；
- 完整 bounded scientific state；
- task contract hash；
- prompt/scaffold/schema hashes；
- pending public detail requests；
- state-origin ledger hash。

不得包含 provider usage、request ID、private reasoning、hidden environment state 或 evaluator
diagnostics。`restore_prompt_state()` 必须 fail closed：

- schema/hash 不匹配则拒绝；
- public task contract 不匹配则拒绝；
- state 超限或引用未知 public ID 则拒绝。

Gate C identical-prefix fork 从同一个导出状态恢复，只改变最后一条公开 feedback。

## 10. 方法哈希与资源记录

每个正式 cell 绑定：

- backend model ID 与 provider configuration；
- compact observation adapter hash；
- Direct/Stateful prompt hash；
- state schema、compressor 和 lifecycle policy hash；
- candidate-label mode 与 order policy；
- token、call、attempt、timeout、wall-time 和美元上限；
- source commit 与 dependency lock；
- deterministic mock-provider replay hash。

每个 trajectory 记录：

- provider-reported input/output tokens；
- prompt estimated tokens；
- state token estimate；
- state before/after hashes；
- retrieval requests；
- retries/failures；
- billed cost 与 wall time。

## 11. Development 验收

只用 public development seeds，全部满足后才允许冻结：

- [ ] `S-01` Pro/Flash 均可运行同一 Stateful scaffold。
- [ ] `S-02` Direct/Stateful 共享完全相同的 compact public context adapter。
- [ ] `S-03` 每 logical decision 最多一次 provider request。
- [ ] `S-04` state export/restore 逐位 replay。
- [ ] `S-05` identical-prefix fork 只改变指定 feedback。
- [ ] `S-06` Gate A/private leakage audit 为 0。
- [ ] `S-07` prompt/state/token/cost ledger 完整。
- [ ] `S-08` invalid action 与 invalid state 不被 harness 修复。
- [ ] `S-09` autonomous 与 assisted history 完全隔离。
- [ ] `S-10` deterministic state compression 可重放。
- [ ] `S-11` provider failure receipt 与 missing-only resume 可重放。
- [ ] `S-12` 所有 formal/private namespaces 未触碰。

## 12. 冻结边界

完成 development 后只能冻结或放弃该 method，不能在看到 formal results 后修改：

- state 字段；
- prompt；
- memory limit；
- compression；
- provider calls；
- tool availability；
- lifecycle manager；
- belief validation；
- retry/failure policy。

如果候选 Stateful 在 development 中无法满足 leakage、replay 或资源合同，应报告方法未成熟并
推迟正式 participant matrix；不得通过嵌入 Gate A oracle knowledge 来获得可运行性。
