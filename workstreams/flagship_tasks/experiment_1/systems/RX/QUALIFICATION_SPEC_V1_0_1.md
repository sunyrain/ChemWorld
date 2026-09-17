# Experiment 1 RX qualification specification v1.0.1

状态：**FROZEN FOR PROVIDER-FREE DEVELOPMENT QUALIFICATION**

Participant：**未授权**
Formal benchmark：**未授权**

## 1. Scope

本版本冻结 `RX-W01..W05 × entity/parametric/structural` 的第一次 Experiment 1
continuous qualification。目标是得到 15 个独立 atomic-unit 结论，不要求全部通过。

共同任务为 `reaction-safety-constrained`，world split 为 `public-test`，objective 为
`safe`。五个 World 使用 seeds `0..4`，W00 canary 使用 seed `900001` 且不进入科学
denominator。

## 2. Private truth manifest

本版本只冻结仓库当前能够一致执行的 truth compiler：

```text
load_chemworld_parameters(public-test, seed)
+ DefaultScenarioGenerator(reaction-safety)
+ deactivating_baseline parent topology
```

五个 World 都属于 `deactivating_baseline` parent family，但其 kinetic、catalyst/solvent
residual、thermal 和 safety 参数由不同 seed 生成并固定。canonical truth hash 覆盖 RX
相关参数和 compiled parent mechanism hash，三个 prior loci 必须逐 World 共享该 hash。

guidance v0.3 中 `W1/W5 stable、W2–W4 deactivating` 是尚未实现为跨三个 loci 一致
truth 的 authoring proposal。本版本不把它冒充已实现 benchmark truth。Structural
qualification 会执行 stable child fork 以检查两种 topology 是否可区分，但 prior Arm
绝不选择 physics。

## 3. RX-E — catalyst dossier mapping

- target：四个匿名 catalyst 的 dossier/action mapping；
- aligned：当前 generic reaction nominal dossier；
- misspecified：只交换 `C1 ↔ C2`，permutation `[0,2,1,3]`；
- 两个 frozen nuisance anchors、四个 catalyst、每点三次独立 noise replicate；
- 每 World 24 次，五 World 共 120 次；
- endpoint vector：`yield / selectivity / conversion / byproduct_signal`；
- 两个 anchor 都必须满足 mean-support separation `>=0.05`、single endpoint
  separation `>=0.03`、support SNR `>=2.0`；
- Participant 最小反证预算固定为 4 个 unique batches。

World residual 如果使 nominal mapping 反转，或任一 anchor 不可辨识，该 unit 按冻结 gate
记录 `failed`，不在本 campaign 改 pair 或换 seed。

## 4. RX-P — temperature/duration local response

- target：固定 catalyst/solvent/reagent context 下的 temperature–duration local relation；
- 每 World 使用 11×11 surface，共 121 个 primary executions；
- 每个 primary execution 必须有独立 evaluator 的 tolerance-zero exact replay；
- reference context 来自已追踪的历史 authoring summary；
- validation noise scale 来自已追踪的 mechanism-oracle authoring summary；
- 旧 summary 和缺失的旧 raw reports不进入本次 qualification denominator；
- aligned/misspecified 只反转一个 local directional claim，schema/context/confidence 对称；
- Participant 最小反证预算固定为 4 个 batches，且低/高侧均需 counterexample support。

五 World共 605 primary + 605 exact replay evaluations。

## 5. RX-S — catalyst deactivation topology

每个 World 执行同一 3×3×3 temperature/duration/catalyst-dose design，成对比较：

- parent：`deactivating_baseline`；
- child：移除唯一 `catalyst_deactivation` reaction 的 `stable_catalyst` fork。

每个 grid cell 两个 laws，共 54 次；五 World 共 270 次。paired action plans 和 HPLC
observation noise 必须完全匹配，所有轨迹 exact replay。

Frozen scientific gates继承已存在的 Q0 语义：

- 至少两个 direct metrics 解析 topology；
- supporting cells 位于两个分离 grid region；
- support 跨至少两档 catalyst dose；
- 至少一个 product metric 有 duration-accumulation signature；
- compiled child 恰好移除一个 deactivation reaction，且 mechanism binding deterministic。

Participant 最小反证预算固定为 4 个角点。历史 seed-0 Q0 的 scientific fail 只作为
authoring warning，不进入本次新 denominator，也不降低任何 gate。

## 6. Common Q1–Q8 semantics

1. `Q1_world_integrity`：固定 denominator、truth binding、outcome classification 与 exact replay；
2. `Q2_task_accessibility`：公开任务接口可执行并能取得注册 endpoint；
3. `Q3_public_contract_invariance`：无 private truth/mechanism/seed 泄漏；
4. `Q4_prior_symmetry`：A/M 除目标 claim/mapping 外 schema、文本模板、action/noise 对称；
5. `Q5_identifiability`：公开证据在冻结阈值下区分 A/M；
6. `Q6_budgeted_falsifiability`：四次 Participant 预算内存在预注册反证路径；
7. `Q7_behavioral_relevance`：差异影响已注册 endpoint，而非装饰性文本；
8. `Q8_noise_robustness`：效应超过冻结 noise gate 并有 exact replay/paired noise 支持。

每个 World×locus 独立判定。只有五个 World 全部 qualified 才称该 locus
`five_world_qualified`；某格失败不阻止完成同 block 或继续下一体系。

## 7. Execution and stop rules

- provider calls：0；
- raw output：write-once；
- platform failure：停止受影响 block，保留 attempt，修复后从 unit 0 重新开始；
- scientific failure：完成冻结 denominator、保留失败、继续 campaign；
- 同一 campaign 不因结果修改 World、pair、grid、threshold 或 gate；
- Participant 和 formal benchmark execution 始终为 `false`。
