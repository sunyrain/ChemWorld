# Experiment 1 Continuous Development Qualification Campaign Plan

状态：**ACTIVE — provider-free development qualification；Participant 未授权。**

启动日期：2026-09-17。执行顺序：`EC repair → RX → PA → FL → C → P → D`。

## 1. Campaign objective

为 `7 systems × 5 Worlds × 3 prior loci = 105` 个 atomic units 建立完整、可审计的状态记录。成功标准不是 105/105 PASS，而是：

- 每个 unit 有明确的 implementation 与 qualification 状态；
- 已运行单元保留完整 denominator、所有失败、truth/prior/config/evidence binding 和 exact replay；
- 未完成单元明确记录 blocker；
- 整个 campaign 不运行 Participant、不调用外部 LLM/provider；
- 不通过降低 Gate、覆盖失败或中途换设计追求矩阵全绿。

## 2. Authority boundary

- 全局目标框架和共同 Q1–Q8 语义：`EXPERIMENT_1_MINIMUM_EXECUTION_SPEC_V1_0_1.md`；
- 当前权威导航：`experiment_1/README.md` 与 `experiment_1/AUTHORITY.md`；
- EC repair：`systems/EC/QUALIFICATION_REPAIR_NOTE_V1_0_2.md`；
- 其余六体系的五 Worlds、prior generator、诊断坐标和机器合同尚未冻结，必须在各自运行前产生 versioned system note 与 machine config；
- guidance 只用于提出候选设计，不能直接充当运行授权。

## 3. Continuous execution policy

本 campaign 不要求逐体系等待人工回复，但不能省略事前冻结：

```text
system audit
→ versioned scientific note
→ W1–W5/private-truth manifest
→ prior and qualification design
→ committed machine config
→ tests
→ provider-free execution
→ exact replay / registry / report
→ next system
```

每个 frozen block 只进行一次预注册科学尝试：

- scientific failure：完成冻结分母，记录 `failed`，不在同一 campaign 中改设计重试，继续下一 block；
- platform failure：停止受影响 block，修复后从冻结 recovery boundary 重跑，保留旧 attempt；
- implementation blocker：记录 `pending` 和 blocker，继续其他可完成单元；
- `N/A` 只在科学对象确实不适用且理由明确时使用，不能用来隐藏实现困难。

## 4. Status schema

实现与科学结果分开：

```text
implementation_readiness: A / B / C
implementation_status: proposed / authoring / implemented / frozen
qualification_status: pending / qualified / failed / N/A
participant_ready_candidate: true / false
participant_execution_authorized: false
```

`development` 不是 qualification status。一个 `system × locus` 只有五个 Worlds 全部 `qualified` 才能称 `five_world_qualified`。

## 5. Campaign start state

EC v1.0.1 已完成 15/15 atomic units：11 `qualified`、4 `failed`。失败为 `EC-W01/W04 × entity/structural`。v1.0.2 将重跑完整 entity 和 structural blocks；EC-P 只有通过机器兼容性审计才 carry forward。

其余 90 个 units 在 campaign 启动时为 `pending`，不得把历史 Work II PASS 自动升级为当前 Experiment 1 PASS。

| System | Entity readiness | Parametric readiness | Structural readiness | Start status |
| --- | --- | --- | --- | --- |
| EC | A | A | A | v1.0.2 repair active |
| RX | A | A | A | pending audit/freeze |
| PA | A | B | A | pending audit/freeze |
| FL | B | B | A | pending audit/freeze |
| C | A | B | A | pending audit/freeze |
| P | B | B | C | pending audit/freeze |
| D | A | B | C | pending audit/freeze |

A/B/C 是初始 authoring readiness，必须由真实代码与依赖 audit 复核，不是 qualification 结果。

## 6. Authoring / qualification isolation

- authoring/calibration evidence 用于选择候选 World、prior 和 diagnostic design；
- qualification config 必须在 qualification evidence 产生前提交并冻结；
- qualification 结果不能在同一版本中反向修改 World、prior、coverage、Gate 或 stop rule；
- 如未来根据失败重新设计，必须 version bump、保留旧失败并重新运行整个受影响 block；
- Participant evidence 永远不能进入 World/prior authoring。

## 7. World and structural rules

- World 不是 noise seed、prior、misindex pattern 或 prompt；
- Opaque/Aligned/Misspecified 必须共享同一个 private truth；
- structural alternate law family 可以作为 simulator 可表达的候选关系，但 Arm 不得选择不同 physics；
- 如果同一 World 的 private truth 改变，entity/parametric/structural 三个 loci 全部失效并必须重跑；
- 当前 EC v1.0.2 repair 明确不改变 private truth。

## 8. Progress and outputs

每个 system 完成后更新：

- machine-readable 105-row registry；
- per-system matrix 与 human-readable report；
- qualified/failed/pending/N/A 的准确分母；
- participant readiness candidate，但 `participant_execution_authorized` 始终为 `false`。

最终交付：

1. `EXPERIMENT_1_QUALIFICATION_REGISTRY`；
2. `EXPERIMENT_1_QUALIFICATION_CAMPAIGN_REPORT.md`；
3. `EXPERIMENT_1_PARTICIPANT_READINESS.md`。

本 campaign 不创建 Participant run，不生成论文结论，不自行发布 benchmark release。
