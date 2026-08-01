# ChemWorld 自主逐操作实验与资源合同草案

状态：`design draft; development only; not preregistered`

审计基准：`main@0005e239a26c276a95ea8ce291ab559caf00857d`

用途：在现有 experiment-recipe 世界之后，建立第一套真正由 Agent 自主选择操作、测量、
实验终止与跨实验资源分配的评测。本文不把“LLM 是否胜过 BO”设为主问题。

---

## 1. 结论

下一阶段不应简单地把当前任务的 operation limit 从 18 调大，也不应只在 prompt 中告诉
Agent“最多使用若干次仪器”。正确的最小设计是：

> **给每个 Agent 完全相同的实验室禀赋，而不是强迫它们产生相同的实际用量；让 Agent
> 自己决定将有限的原料、反应容器、操作机会和表征机会分配给哪些实验与哪些阶段。**

具体需要同时完成三件事：

1. 新增跨 fresh-vessel 持续存在、由运行时强制执行的 `CampaignResourceCard`；
2. 保留物理、安全和设备前置条件，但为 autonomous track 去掉预先规定科研流程的
   workflow gates；
3. 把当前实验的完整、紧凑、可验证操作账本在每次决策前返回给 Agent。

“原料份数”和“仪器操作次数”都应该使用，但它们是不同资源轴，不能合成一个人为总成本。
份数用于定义公平禀赋，实际动作仍可使用连续物理量，从而不把自主操作重新离散成固定 recipe。

---

## 2. 当前实现审计：已经有什么，缺什么

| 层级 | 当前已有 | 当前缺口 |
| --- | --- | --- |
| 单个实验物理账本 | `time_s`、`cost`、`risk`、`sample_consumed_L` | fresh vessel 后会随物理状态重置，不是 campaign 库存 |
| 物料动作 | 加 reagent、solvent、catalyst、phase、extractant、seed 等均记录实际物理量 | 没有跨实验的总库存和逐资源 hard cap |
| 仪器 | HPLC、GC、UV-vis、pH meter、final assay；有成本和破坏性取样 | 没有跨实验的逐仪器使用次数上限 |
| 正式 method 账本 | 操作数、完整实验数、模型调用、tokens、费用、CPU/GPU、wall time | 没有 vessel-start、abandon、原料库存、逐仪器次数 |
| 生命周期 | Agent 自己 `terminate`，随后自己 `measure(final_assay)`；正式 runner 不修复 | 只有 final assay 才会得到 fresh vessel；缺少显式丢弃失败 batch 的动作 |
| Agent 记忆 | adapter 内部保存 `_current_experiment_operations` | 构建每轮 prompt 时没有传入该完整账本；通常只给最近两次决策 |

最后一点会直接混淆自主性结果。一个真实实验员可以查看当前 batch 的实验记录；向 Agent
公开它自己刚刚执行过的操作、结果和资源变化不是人类脚手架，而是实验环境的必要可观测状态。

### 2.1 当前两个 flagship task 还不适合作为“自由测量”任务

现有 `electrochemical-conversion` 的 validator 规定：

- 第一次 electrolysis 后必须依次完成 pH meter 和 UV-vis；
- 然后必须修改 setpoint 并完成第二次 electrolysis；
- 第二次 electrolysis 后必须完成 UV-vis，才能 terminate。

现有 `reaction-to-crystallization` 的 validator 规定：

- 第一次 seed 前必须在当前 process time 做非终局 assay；
- cooling 后、filter 前必须再次在当前 process time 做 assay；
- filter 后才能 terminate。

这些规则非常适合冻结 recipe、校准环境和保证任务可达，但它们把测量位置写进了任务脚本。
如果在不修改任务的情况下添加“仪器次数”，Agent 并没有真正决定是否测量和把测量机会花在哪里。

因此原任务应原样保留以保证旧结果可复现；自主实验应新增 task variants，而不是偷偷改旧任务。

### 2.2 我们以前确实做过 G2-like：三代证据必须分开

仓库历史不是“从未做过逐操作”，而是已经形成了三代 operation-level 试验：

| 代际 | 任务与规模 | 生命周期帮助 | 结果 | 能说明什么 |
| --- | --- | --- | --- | --- |
| DeepSeek mechanism diagnostics v0.1 | 两个旗舰任务，10 个 live-LLM campaigns、40 个完整实验、455 条 operation records | 最后两槽 guardrail；7 次覆盖落在 4 个实验 | 36/40 个实验未用 guardrail；450 model calls | operation-level 闭环早已可运行，也产生过反馈置换、机制识别和优化—认知解耦结果 |
| mechanism-adaptation pilot v0.2.1 | 结晶任务，changed/no-change 两个 campaigns、28 个完整实验、333 条 records | 9 次覆盖落在 6 个实验 | 22/28 个实验完全由 Agent 自行 closeout；6 个 assisted | Agent 不是从来不会完成逐操作实验，但该 pilot 不是严格自主结果 |
| RC28 strict qualification | Direct 与 Stateful 各 4 条 phase trajectories、各 72 次决策 | 完全关闭 | 两者均 0/4 complete；Direct 38 次 HPLC，Stateful 39 次加 reagent | 去掉 guardrail 后暴露 late/no terminate、missing final assay、测量循环和加料循环 |

第一代完整报告已在工作树清理时删除，但仍可由 Git 对象恢复：

```text
git show aa2db760:workstreams/flagship_tasks/reports/deepseek-mechanism-diagnostics-v0.1.json
git show aa2db760:workstreams/flagship_tasks/reports/deepseek-mechanism-diagnostics-v0.1.md
```

第二代的 compact report 仍在
`workstreams/flagship_tasks/reports/mechanism-adaptation-agent-pilot-v0.2.1.json`，但其引用的四条原始
JSONL 和 provider receipt archive 当前不在工作区；因此 22/28 只能作为已绑定的历史汇总，不能重新
统计逐动作细节。第三代的原始轨迹仍在 `runs/mechanism-adaptation-v0.3.0-rc28/`，权威说明见
`workstreams/flagship_tasks/RC28_PARTICIPANT_EXECUTION_QUALIFICATION_RESULTS_ZH.md`。

这三代合起来给出的正确判断是：

> 旧系统已经实现了“一次选择一个 primitive operation”的控制循环；真正缺失的是无强制收尾、
> 跨 batch 持久资源、自由测量合同和足够完整的当前实验账本。RC28 的 0/4 是旧严格合同下的
> lifecycle failure，不是对重新设计后的 G2 能力上限。

### 2.3 我们以前的“资源账本”到底是什么

旧设计有三本账，但没有一本是实验室 campaign endowment：

1. `ProcessLedger`：当前 vessel 内的 `time/cost/risk/sample/energy`；final assay 后创建 fresh
   vessel 时重置。
2. `MethodResourceLedger`：runner 外部累计 operation、完整实验、model calls、tokens、provider
   USD、CPU/GPU 和 wall time，并在超限时 fail closed。
3. 已从当前树删除的 resource-accounting v0.4：把 complete experiments、operations、
   measurements、decisions、provider requests/retries、tokens、USD、fit/acquisition、RL steps、
   CPU/GPU/wall time 作为 15 个并列轴审计，并明确禁止把它们标量化。

仪器合同虽然声明了 latency，但当前 runtime 没有把它并入 `ProcessLedger.time_s`。因此第一阶段只能
把 process time 与 instrument latency 分别报告，不能把现有 `time_s` 称为完整实验周转时间。

历史 mechanism runner 的物理执行预算则是：

```text
reference recipe length + closeout headroom
crystallization: 12 + 6 = 18 actions / experiment
electrochemistry: 11 + 6 = 17 actions / experiment
phase limit = per-experiment limit × planned experiments
```

随后 wrapper 在每个实验最后两槽强制选择 `terminate` 和 `final_assay`。这不是资源分配账本，
而是“每个实验预分相同操作槽 + 生命周期保险”。它没有原料总库存、vessel token、逐仪器 quota，
也不能让 Agent 把一个实验省下的操作重新分配给另一个实验。

还有一个对 G0 很关键的实现事实：当前 static-optimization 正式脚本每一轮新建一个
`experiment_horizon=1` session。Agent history 虽然保留，环境和任何 env-owned campaign 状态都会
重置。要做真正 resource-matched 的 G0，必须把全部 `K` 轮放进同一个 session；仅给
`ChemWorldEnv` 添加账本仍然不够。

---

## 3. `CampaignResourceCard`：共同禀赋，多本账

建议新增以下公共且可强制执行的 campaign 资源合同：

```json
{
  "schema_version": "chemworld-campaign-resource-card-0.1",
  "card_id": "electrochem-k6-reference-balanced",
  "reference_equivalent": {
    "recipe_space_version": "chemworld-task-recipe-space-1.2",
    "unit_vector": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    "count": 6
  },
  "hard_limits": {
    "environment_action_attempts": 84,
    "vessel_starts": 6,
    "stocks": {
      "reagent_mol": 0.099,
      "solvent_total_L": 0.150
    },
    "instrument_uses": {
      "diagnostic_total": 18,
      "per_instrument": {
        "uvvis": null,
        "ph_meter": null
      },
      "final_assay": 6
    }
  },
  "report_only": {
    "sample_consumed_L": true,
    "process_time_s": true,
    "instrument_latency_s": true,
    "physical_environment_cost": true,
    "peak_and_accumulated_risk": true
  },
  "debit_semantics": "committed_physical_resources_only",
  "card_sha256": "<canonical payload hash>"
}
```

上例只是电化学 formal-balanced card 的候选值，正式值需在 deterministic qualification 后冻结。
model calls、tokens、provider cost、wall/CPU/GPU time 不放进物理 card；它们继续由
`MethodResourceLedger` 独立记账。

### 3.1 为什么不用单一“总资源分”

一个 HPLC、1 mmol reagent、一次失败操作和 10 分钟 process time 之间没有无争议的换算率。
强行标量化会把结论变成任意权重的产物。正式报告应：

- 用 hard caps 保证同一 task 内各方法拥有相同的资源可行域；
- 分别报告各资源的实际使用量；
- 报告 performance–resource 曲线和 Pareto 前沿；
- 不把不同 task 的物理库存直接横向比较。

### 3.2 “份数”的正确含义

定义每个 task 的一个带版本和 hash 的公开 reference batch，例如 midpoint recipe 的物理消耗。
`K=6` 份表示 Agent 拥有完成六个 reference batches 所需的总库存，但 Agent 不必做六个相同实验：

- 可以把更多 reagent 用在少数 batch；
- 可以把一个 batch 的 reagent 分多次加入；
- 可以提前丢弃失败 batch；
- 可以保留未用资源；
- 不能突破总库存。

运行时仍按 `mol`、`L`、`g` 连续扣减，而不是把动作参数量化成固定格点。这样既能公平控制资源，
也不会把高自由度操作重新变成参数表。

为了避免用极小加料反复试探，可同时使用：

- 每次提交给环境的 action attempt 都消耗一个 operation slot；
- 公共 action schema 规定最小有意义的物理加料量；
- 库存按实际 committed 物理量扣减。

第一轮工程资格测试可以先使用 `max-envelope card`：物料为 `K × 合法 recipe 上界`，保证任意
G0 参数计划都可执行；它主要测试 operation、instrument 和 lifecycle 分配。正式资源分配实验再使用
`reference-balanced card`：物料为 `K × reference batch`，此时 G0 和 G2 都必须真正管理库存。
这两个 card 不能在看过 formal 结果后互相替换。

### 3.3 资源扣减语义

必须在协议中逐条冻结：

- 每次实际进入 `env.step` 的 action attempt，包括 schema invalid、物理 precondition failure、
  transaction rollback 和 resource-overrun proposal，都消耗 operation slot；
- provider request/retry 单独进入 method ledger；若 provider 最终失败且没有 action 进入环境，
  不伪造物理操作，也不扣 operation slot；若系统显式提交 `model_failure` 事件，则该事件必须按
  协议记为一次失败的 environment attempt；
- 只有 committed material action 扣减物理库存；
- 超过剩余库存的动作在 transaction 前 fail closed，状态不改变；
- 只有 committed measurement 扣减仪器 token、样品体积和仪器成本；
- final assay 使用独立 token，不与 diagnostic measurement 共用同一本账；
- final assay 仍消耗一个 operation slot，仍必须由 Agent 主动选择；
- 不自动 repair、terminate、assay 或补充原料；
- campaign 截止时未关闭的 batch 记为 right-censored protocol failure。

final assay token 独立并不是 lifecycle assistance。它避免“为了研究诊断资源分配而设置的
scarcity”在数学上顺带剥夺 closeout 机会；Agent 仍可能忘记或拒绝执行 final assay。

### 3.4 两本累计账与一次原子扣减

不要把新账本塞进 `WorldState.ledger`。正确结构是：

```text
WorldState / ProcessLedger
  └─ 当前 vessel 的物理状态；fresh vessel 时重置

CampaignResourceLedger
  └─ operation attempts、vessels、stocks、instrument tokens；
     final assay 或 discard 后不重置，只有显式 campaign reset 才清零

MethodResourceLedger
  └─ decisions、provider attempts、tokens、USD、CPU/GPU、wall time
```

每一步使用同一个事务顺序：

1. canonicalize action 并运行 schema/物理 validator；
2. 由纯函数 `resource_request(pre_state, action)` 计算请求量；
3. 先检查 campaign remaining；不足时产生公开的
   `campaign_resource_available=false` precondition failure；
4. 环境照常记录这次 attempt，因此 operation slot 已消耗；
5. 只有底层 transaction committed 后才扣 material/instrument；初始 vessel 在 campaign reset 时
   记作第 1 个 start，后续 vessel 只在 committed final-assay/discard rollover 时增加；
6. 从实际 pre/post state 更新 sample、time、cost、risk 等 report-only totals；
7. 写入 `resource_before/request/delta/after/result/reason`，并用这些 receipts 重放最终账本。

同一物料类别使用共享池：选择不同 solvent 或 catalyst identity 不会凭空获得一套新库存；
identity-level 用量另行报告。可用参数上界应动态收窄为
`min(physical_bound, campaign_remaining)`，仪器 token 为零时从公开 choices 中移除，但越界提案
仍必须 fail closed，不能由 harness 自动改写。

---

## 4. 新增 autonomous task variants

### 4.1 A0：`reaction-to-assay-autonomous`

用途：只做 controller、账本和生命周期资格验证，不作为主科学结论。

保留：

- 容器容量、温压、安全和样品充分性；
- `terminate -> final_assay` 生命周期；
- 空 vessel、实际物料、热反应、quench 和测量语义。

允许 Agent 自己决定：

- 加料次序与次数；
- 是否使用 catalyst；
- heat/wait/quench 的时点和次数；
- 是否及何时做 HPLC；
- 何时 terminate 和 final assay。

当前 midpoint reference 为 8 次操作：
`add_solvent -> add_reagent -> add_catalyst -> heat -> quench -> HPLC -> terminate -> final_assay`。

### 4.2 A1：`electrochemical-campaign-autonomous`

这是第一主任务，因为它天然具有“操作—测量—再操作”的闭环。

保留物理约束：

- 有 volume/material 后才能配置和运行电化学单元；
- 电解前必须有合法 setpoint；
- 电压、电流、时间、容量、安全与样品量边界；
- final assay 只在 terminate 后可用。

去掉科研脚本约束：

- 不强制恰好两段 electrolysis；
- 不强制第一次后 pH+UV-vis、第二次后 UV-vis；
- 不强制第二 setpoint 必须达到人为规定的最小变化；
- 完成至少一次有效 electrolysis 后即可由 Agent 决定继续、测量或终止。

这样 pH 和 UV-vis token 才是 Agent 可以真实分配的信息资源。

当前 midpoint reference 为 11 次操作，每 batch 消耗：

- solvent 25 mL；
- reagent 16.5 mmol；
- pH meter 1 次、UV-vis 2 次；
- electrolysis process time 2,490 s；
- final assay 1 次。

### 4.3 A2：`reaction-crystallization-autonomous`

这是第二主任务，因为它包含反应、表征、结晶和分离的长依赖链。

保留物理约束：

- 有产物/物料才能结晶；
- cooling 后才能过滤实际形成的 crystals；
- filter 后才能按当前任务定义进入终局；
- 容量、温度、时间、seed 和样品约束。

去掉科研脚本约束：

- seed 前不强制 HPLC；
- filter 前不强制 HPLC；
- HPLC 变成可选择的诊断，而不是解锁下一操作的钥匙。

是否允许 unseeded crystallization 应在 physics qualification 后一次性冻结。若当前 kernel 对
unseeded 路径尚不可靠，第一版可以保留“seed 或明确 nucleation setup”这一物理条件，但不能
规定必须在固定位置先测 HPLC。

当前 midpoint reference 为 12 次操作，每 batch 消耗：

- solvent 25 mL；
- reagent 16.5 mmol；
- catalyst 0.315 mmol；
- seed 8 mg；
- HPLC 2 次；
- heat+cool process time 11,550 s；
- final assay 1 次。

### 4.4 新增显式 `discard_batch`

当前 campaign 只有成功 final assay 后才产生 fresh vessel。对真正自主的实验 campaign，这会使
Agent 无法放弃已经污染、耗尽或明显无价值的 batch。

建议新增 `discard_batch`：

- 只能作用于当前尚未 final-assayed/discarded 的 open batch；允许在 `terminate` 后放弃无法 assay
  或已无价值的 batch；
- 消耗一个 operation slot；当前 vessel 的 start token 已在该 vessel 创建时扣过，不重复扣；
- 已投入的原料、样品、时间和成本不返还；
- 不产生 final score；
- 记录 `abandoned=true`、原因和废弃资源；
- 只有仍有 vessel token 且至少有一个 operation slot 时才创建 fresh vessel；否则 campaign 结束。

vessel 语义固定为：campaign 初始 vessel 计作第 1 个 start；每次成功 final assay 或
`discard_batch` 后创建下一 vessel 时再加 1。达到 `K` 后不得创建“phantom fresh vessel”。
同时报告 `vessels_started`、`completed_batches`、`discarded_batches` 和
`unused_fresh_vessels`，避免把从未加入物料的空 vessel 误算成科学实验。

它不是给 Agent 修复错误，而是把真实实验中的“止损/丢批”变成可测的自主决策。

---

## 5. 必须公开的当前实验账本

每轮操作前的 public state 至少包含：

```text
current_experiment:
  vessel_index
  experiment_action_count
  terminated
  minimum_actions_to_final_assay
  discard_available
  complete compact operation ledger:
    operation
    committed / rolled_back
    compact parameters
    observed result summary
    resource request / delta
  current physical summary
  latest measurement

campaign_resources:
  immutable card id / hash
  operations used / remaining
  vessels started / remaining
  each stock used / remaining
  each instrument used / remaining
  final assay tokens remaining
  cumulative sample, time, cost, max risk
```

账本是环境事实，不能由模型自己从最近两轮对话猜测。为了控制 token：

- 当前 batch 的全部操作以一行一个 compact event 保留；
- 完成 batch 只保留 terminal summary 和关键 measurement summaries；
- raw spectra 使用 catalog/on-demand retrieval，不在每轮重复；
- 不删掉 action order、commit status 和 resource deltas。

`minimum_actions_to_final_assay` 只是当前状态的可达性事实，例如未 terminate 时通常至少还需两步、
terminate 后至少还需一次 final assay；它不会替 Agent 预留槽位或自动选择动作。
Agent 自写的 plan、belief 和 evidence ledger 应与这本环境事实账分开，防止把模型记忆误当成真实
实验状态。

---

## 6. 实验臂：比较行动权，而不是制造弱基线

### G0：`compiled_recipe_anchor`

- 每个 batch 前由 Agent 或经典 optimizer 选择 recipe 参数；
- 现有 compiler 执行固定操作序列；
- `K` 个 batch 必须在同一个 persistent session 中执行，不能每轮重置环境账本；
- 必须经过同一个 `CampaignResourceCard`，真实扣减每一步资源；
- 用途是连接已经完成的参数选择结果，不代表自主操作。

旧 formal G0 数值可以作为背景，但不能直接作为资源匹配的因果对照；需要在新 world cohort 和新
resource wrapper 下重跑 matched anchor。

### G2：`closed_loop_primitive`

- 每次只选择一个操作；
- 每步得到更新后的物理状态、测量结果和资源账本；
- Agent 自己拥有 planner、notebook、belief state、retry 和 lifecycle manager；
- harness 不替 Agent 选择任何科学或 lifecycle action。

第一阶段直接跳过 G1。G0→G2 应准确表述为 **experimental-control transfer**：
同时把 recipe structure、操作顺序、测量时机、实验内适应和 lifecycle 的控制权交给 Agent。
它是系统级行动权对照，不是“反馈价值”的单因素因果估计，也不以 G2 必须胜过 G0 为前提。

实验中反馈的因果价值在 G2 内部另做配对 intervention：只在 Agent 自己选择测量以后，从同一个
state prefix 分支为 true / masked / delayed / permuted observation，比较下一步 action、
belief update 与 terminal outcome。这样无需为了一个不自然的 open-loop G1 接口增加主实验臂。

### 非学习型控制

- `validated_state_machine`：证明任务和资源 card 可达，要求 100% lifecycle completion；
- `valid_random`：从当前 affordance 中采样，并使用公开的随机 closeout policy；
- 可选 `myopic_measurement_policy`：简单阈值策略，用于检查资源 scarcity 是否真的影响决策。

不建议为了“公平”强行训练一个 BO 逐操作。BO 的自然接口仍是 G0，经典 sequential controller
则通过 state machine、valid random 或后续 RL 表示。

---

## 7. 两种资源实验：主禀赋与资源扰动

### 7.1 主实验：相同 balanced endowment

所有方法在同一 task×world 上得到完全相同的资源 card。实际使用量由方法自己决定。

候选 formal card（`K=6`）：

| 任务 | vessels | operation attempts | material stock | nonfinal instruments | final assays |
| --- | ---: | ---: | --- | ---: | ---: |
| A1 electrochem | 6 | 84 | 6 reference equivalents | 18 | 6 |
| A2 crystallization | 6 | 90 | 6 reference equivalents | 12 | 6 |

operation limit 等于 `6 × reference operations + 18`，即平均每个 vessel 有 3 次额外操作。
这允许额外测量、分次加料和错误恢复，但无法无限循环。**84/90 是整个 campaign 的全局池，
不是每个实验各自获得 14/15 步**：Agent 可以给一个难实验 20 步、另一个实验 8 步，只要总账不超限。
这正是相对于旧 17/18 steps-per-experiment 设计的关键变化。

对应物理库存：

| 任务 | reagent | solvent | catalyst | seed |
| --- | ---: | ---: | ---: | ---: |
| A1 electrochem | 99 mmol | 150 mL | 0 | 0 |
| A2 crystallization | 99 mmol | 150 mL | 1.89 mmol | 48 mg |

这些是按当前 midpoint reference 得到的初始候选值，不是不可修改的最终协议。qualification
应检查整个合法 action range 后再冻结，以免 reference card 与真实容量/安全域冲突。

在 provider qualification 中先用不制造结构性失败的 `max-envelope card`：

| 任务（K=4） | reagent | solvent | catalyst | seed | diagnostics | final |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A1 electrochem | 120 mmol | 100 mL | 0 | 0 | 12 | 4 |
| A2 crystallization | 120 mmol | 100 mL | 2.20 mmol | 60 mg | 8 | 4 |

它按合法 G0 recipe 上界给物料，只验证 controller、账本和 lifecycle；P1 通过后再切换到上面的
reference-balanced card 研究真实分配。

这个资源层并非凭空假设。把 RC28 四条独立 strict trajectories 仅作为压力回放相加：

| 旧 controller | committed reagent | committed solvent | HPLC |
| --- | ---: | ---: | ---: |
| Direct | 225 mmol | 160 mL | 38 |
| Stateful | 1,110 mmol | 260 mL | 19 |

而 proposed K=4 reference card 只有 66 mmol reagent、100 mL solvent 和 8 个 HPLC tokens。
新账本会在循环行为真正发生时阻止继续消耗，而不是等到第 18 步才发现没有 closeout；越界提案仍
消耗 operation attempt 并保留为可解释的 procedural failure。

### 7.2 配对资源扰动：观察 Agent 如何重新分配

只改变一本账，其余资源保持不变：

- `instrument-scarce`：nonfinal instrument tokens 减半；final assay 不变；
- `material-scarce`：reagent/solvent/catalyst/seed 总库存减半；仪器、vessel、operation 不变。

主要比较同一 model、同一 world、同一 observation-noise coordinate 下：

- 是否减少测量、减少 started vessels 或缩短实验；
- 是否把资源集中到少数高价值 batch；
- 是否保留 closeout 资源；
- 最终 score 和 cognition 是否以不同方式退化；
- 是否出现资源替代，例如 material scarcity 下增加早期诊断。

不要把 scarcity 与模型或 prompt 同时改变。

---

## 8. 结果端点

### 8.1 两个共同主端点

1. **Procedural autonomy**
   - completed final assays / started vessels；
   - protocol-failure rate；
   - time/operations to first completed experiment。
2. **Scientific campaign utility**
   - 固定 resource card 结束时的 best final-assay score；
   - incumbent score 对 operation、material 和 measurement resource clocks 的 AUC。

二者必须并列。高分但大多数 batch 无法关闭，与低分但程序完整，是不同失败。

### 8.2 资源行为

- 各 stock 的投入、剩余和废弃；
- 各 instrument 的使用次数、阶段位置和跨 batch 分布；
- measurement/process action ratio；
- repeated-action run length；
- sample、process time、environment cost、maximum risk；
- score–resource Pareto；
- scarcity elasticity。

### 8.3 反馈使用与适应

- measurement 后下一操作是否改变；
- setpoint/recipe 的 within-experiment adaptation 次数和幅度；
- 在相同 prompt-state prefix 上，对 true、masked、delayed 或 permuted feedback 的下一动作差异；
- feedback intervention 对局部动作和 terminal utility 分开报告。

反馈干预只在 Agent 自己选择测量后建立 paired branch；不得用系统强制测量制造“反馈使用”。

### 8.4 优化与认知分开

继续保留：

- 每次操作前的 expected effect、diagnostic target、belief-update rule 和 uncertainty；
- 预注册 counterfactual query 的方向准确率和 Brier；
- 结构/机制标签与 unsupported-claim rate；
- 预测改善是否与 terminal optimization 改善一致。

不要构造一个“科学智能总分”。自主操作的价值之一正是观察优化、程序能力和认知是否解耦。

### 8.5 计算资源

独立报告 calls、tokens、provider cost 和 wall time。G2 天然比 G0 调用更多；不应为了匹配
LLM calls 而剥夺 G2 的逐操作反馈，也不应把计算成本与物理实验成本混成一个权重。

---

## 9. 统计与矩阵

独立统计单位是 frozen world cluster，不是 operation、experiment 或 provider call。

- 所有方法在同一 world 上配对；
- observation noise 使用 keyed coordinate；
- provider repeats 是测量模型随机性的重复，不当作独立样本；
- task 分层报告；
- 以 world-cluster bootstrap 或 paired randomization interval 为主；
- 不用 pooled operation count 虚增样本量。

### 9.1 P0：离线和 deterministic qualification

- resource conservation 和 fail-closed 单元测试；
- state machine 在每个 task×resource card 100% 完成；
- G0 midpoint recipe 在 card 内可执行；
- G0 的全部 `K` 个 batch 在同一个 session 内执行，resource ledger 不随每轮 optimizer query 重置；
- `discard_batch`、final assay、新 fresh vessel 和库存不重置测试；
- invalid/precondition/rollback 只扣 operation attempt，不扣物料或 instrument token；
- prompt 中完整当前实验 ledger 的最坏长度测试；
- replay 逐位重建所有资源，并与 method/provider ledger 分账 reconcile。

### 9.2 P1：最小 provider qualification

使用 development worlds：

- A0 reaction-to-assay；
- A1 electrochem；
- A2 crystallization；
- 每个 2 worlds × 2 provider repeats；
- 只运行 G2。

候选 `K=4 max-envelope` qualification card：

| 任务 | vessels | operations | material | diagnostics | final assays |
| --- | ---: | ---: | ---: | ---: | ---: |
| A0 assay | 4 | 40 | 4 × legal recipe maxima | 4 | 4 |
| A1 electrochem | 4 | 56 | 4 × legal recipe maxima | 12 | 4 |
| A2 crystallization | 4 | 60 | 4 × legal recipe maxima | 8 | 4 |

P1 的目标不是挑选“结果好看”的模型，而是确认：

- provider/prompt/resource infrastructure 正常；
- Agent 能看到准确 ledger；
- 至少有可评分的完整 trajectory；
- 失败可以明确归为 Agent、resource、environment 或 provider。

### 9.3 P2：arXiv 最小主矩阵

```text
2 main tasks × 5 untouched worlds × 2 controllers (matched G0 / strict G2)
× 2 provider repeats = 40 method cells
```

其中强制新增的 live-G2 部分是 20 cells。若 G0 使用确定性经典 optimizer，则其 repeat 由算法种子
而非 provider repeat 定义；不要伪装成 LLM cell。另运行 state-machine 和 valid-random 的所有
task×world cells。若冻结前的方差审计表明关键 paired contrast 的 CI 预期过宽，则按只依赖方差、
不依赖效应方向的规则把所有 arms 一致扩到 10 worlds。

### 9.4 P3：资源扰动

优先只对 G2 做小型配对子矩阵：

```text
2 tasks × 5 worlds × 2 scarcity conditions × 2 repeats
= 40 additional G2 cells
```

balanced cell 来自 P2；scarcity 只新增 material-scarce 与 instrument-scarce。该实验回答资源分配
行为，不用于扩大“G2 胜过 G0”的样本量。

---

## 10. 旧实验能复用什么

### 10.1 可以复用

固定 recipe/参数选择结果可用于：

- 选择 A1/A2 两个主任务；
- 校准 score range、任务异质性和 world difficulty；
- 定义 reference batch 与 G0 matched anchor；
- 延续优化—认知解耦、先验影响等已有观察；
- 使用现有 recipe compiler、baseline 和 evidence pipeline。

旧逐操作 Direct/Stateful 实验可用于：

- 定义 lifecycle failure taxonomy；
- 证明 strict runner 没有自动 closeout；
- 估计重复测量/重复加料的 failure mode；
- 说明为什么必须公开完整 current-experiment ledger；
- 设计 operation 和 instrument caps。

具体历史诊断：

- 2026-07-21 G2-like mechanism diagnostics：两个任务、10 个 live campaigns、40 个完整实验；
  36 个实验没有 guardrail，4 个实验由 7 次 lifecycle actions 协助；
- 该轮已经提出可延续的科学现象：静态排名与变化后排名弱相关、真反馈优势未稳定出现、机制识别
  与结果恢复分离、声明信息价值明显高估；但反馈 arms 是独立 provider samples 而非 prefix-paired
  branches，且带 guardrail，旧数值只能生成新假设；
- v0.2.1：28 个完整结晶实验中 22 个自主 closeout、6 个 assisted，证明 operation-level
  controller 并非从未完成过实验；
- Direct：4 trajectories、72 decisions、38 次 HPLC、0/4 complete；
- Stateful：4 trajectories、72 decisions、39 次 add_reagent、19 次 HPLC、0/4 complete；
- Direct 的两个 no-change trajectory 到第 18 步才 terminate，没有第 19 步执行 final assay；
- 两类方法均未得到可解释的完整 scientific campaign。

`runs/golden/` 中的 scripted trajectories 可直接作为 resource wrapper、terminate→final-assay、
fresh-vessel 和 replay 的 deterministic positive controls；它们不读取反馈，不能作为学习型
Agent baseline。Task Lab adaptive 可以复用交互和光谱检索设计，但因为存在 action repair、失败
fallback 和 automatic closeout，不能列为 strict G2 结果。

### 10.2 不能直接复用

- 旧 G0 final scores 不能当作新 G2 的 resource-matched control；
- 旧 operation trajectories 不能当作“LLM 不能自主实验”的证据；
- 旧 formal seeds 不应用于新的 confirmatory autonomous claim；
- 不能把旧 workflow-gated task 的 measurement behavior 解释成自由资源分配；
- 不能在加入完整 ledger、resource card 和新 task contract 后做无条件 before/after 性能比较。
- v0.2.1 原始 JSONL 当前缺失，在恢复 archive 前不能重新做逐操作或资源统计；
- RC28 Gate A 是环境/oracle 可达性证书，不是 LLM G2 performance；
- 后来的 Scientific Adaptation 是 complete-experiment planner + mechanical executor，不是 G2。

旧结果应在论文中标为 motivating diagnostic 或 background evidence；新的 matched cells 才是主比较。

---

## 11. 实现顺序与 go/no-go

### R0：先修合同

1. 新增 campaign-persistent resource ledger；
2. 把 resource card 和 remaining resources 加入 public view；
3. 把 `_current_experiment_operations` 作为完整 compact ledger 传入每轮 prompt；
4. 新增 `discard_batch`；
5. 新增 A0/A1/A2 autonomous task variants，旧 tasks 不变；
6. 把 G0 的 `K` 轮改为一个 persistent `StaticOptimizationExperimentSession`，并以实际
   `env.step` 数而不是 optimizer decision 数记录 lab operation attempts；
7. 让 G0 compiler 与 G2 controller 经过同一个 resource gate；
8. 所有资源与轨迹进入 write-once receipt 和 replay。

### R1：资格条件

正式 provider pilot 前必须满足：

- deterministic state machine completion = 100%；
- 资源守恒、跨 vessel 持久与 replay 全部通过；
- resource-overrun proposal fail closed；
- final assay 绝不由 harness 自动选择；
- Agent public state 中不存在 hidden truth；
- current-experiment ledger 不因 prompt 压缩丢失 action order 和 resource delta；
- G0/G2 在同一 task 内拿到完全相同的物理资源 card 和 autonomous task contract；
- `lab operation attempts`、`Agent decisions` 与 `provider attempts` 三者可独立 reconcile；
- 第 `K` 个 vessel 后不创建 phantom fresh vessel，discard 不返还任何物理资源。

### R2：冻结顺序

```text
task physics and autonomous gates
-> resource cards
-> public state and memory contract
-> persistent G0 / strict G2 adapters
-> metrics and failure taxonomy
-> development worlds
-> variance-only sample-size rule
-> untouched formal worlds
```

在看到 formal performance 后不得修改任务 gate、库存、instrument quota、closeout 规则或 prompt ledger。

---

## 12. 第一阶段论文中这一实验应呈现什么

核心图不应只是三根“平均 score”柱子。建议至少包含：

1. 同一个 chemical world 和 resource ledger 上，G0 recipe compiler 与 G2 closed-loop controller
   的行动权边界图；
2. 同一资源 card 下，一条完整 G2 trajectory 的操作、测量、资源和 belief 时间线；
3. G0/G2 的 lifecycle completion 与 best final score 并列图；
4. score 对 operation/material/instrument 三种 resource clocks 的曲线；
5. balanced→scarce 时资源重新分配的 paired arrows；
6. self-chosen measurement 后 true/masked/delayed/permuted paired branches 的 action divergence；
7. optimization、procedural autonomy、prediction/cognition 的分离散点图。

这一实验最终回答的不是“Agent 是否比 BO 强”，而是：

> 当实验不再被压缩为一个参数向量，并且有限实验资源必须由 Agent 自己在操作、测量和
> 多个 batch 之间分配时，它实际上如何进行实验；它在哪些层面表现出自主性、适应性、浪费、
> 先验依赖，以及优化与理解的分离。
