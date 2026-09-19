# Work II RX-P K1–Q–K2 任务协议 v1.1

状态：**信息边界纠正后重新冻结，尚未执行**

后续状态（2026-09-19）：本文件保留为RX-W01单世界设计历史；已由[五世界RX-P profile v1.2](WORK_II_RX_P_K1_Q_K2_PROFILE_V1_2.md)替代用于W2-131新执行，不得与v1.2来源混用。

冻结日期：2026-09-19

任务编号：W2-130

继承协议：[Work II 通用 K1–Q–K2 封存后测协议 v1.1](WORK_II_CANONICAL_K1_Q_K2_PROTOCOL_V1_1.md)

性质：RX-P 任务专用附录；固定任务单位、来源资源、十二道预测题、指标、参考与评分，不单独重写通用 K1/Q/K2 提示

替代关系：本版本替代[RX-P 任务协议 v1.0](WORK_II_RX_P_K1_Q_K2_PROFILE_V1_0.md)作为后续新运行的唯一 RX-P 附录。v1.0 保留为设计历史，不得用于启动来源。

## 1. 适用范围和历史边界

本协议用于 `reaction-safety-constrained` 任务中 `RX-W01 × P` 的后续前瞻开发块。P 层问题是局部温度—时间响应规律；比较臂为 Opaque、Aligned、MisIndexed，研究目标为机理探索与安全约束优化。六个来源必须相互独立，但使用相同世界、公共任务合同、资源、模型设置和本文件的十二道 Q。

本文件不授权自动启动六个来源、其他 RX worlds、其他先验层或正式 Participant。现有 `RX-W01 × P × Opaque` 双目标 canary 继续按其实际三问 K2、旧十二题和修复链解释；但它收到过 P 层的近似参考区域，按本版本应重标为 `ContextOnly`，不是严格 `P-Opaque`。不得用本协议替换旧题，也不得把旧 canary 与以后新跑的 A/M 合并为完整三臂效应。若要形成六格可比块，六格都须在本协议下 fresh 执行。

### 1.1 本次纠正：按目标层定义 Opaque

三臂必须按被干预的目标层 `L` 定义，而不是按整个任务是否包含任何公共背景来定义：

```text
Opaque(L):
  preserve public operations, legal ranges, instruments, scoring and information outside L;
  provide no instance-specific knowledge at L.
```

对于 `RX-P`，`L` 是温度—时间局部响应。公共任务可以告诉所有来源：存在 `target_temperature_K` 和 `reaction_duration_s` 两个控制量、它们的物理含义和合法范围、仪器与评分合同，以及不由 P 层目标结果挑选的共同非 P 配方。它不能把从目标世界、资格化结果或历史标定得到的 P 层工作点包装成“普通上下文”交给 Opaque。

| 信息 | Strict P-Opaque | Aligned / MisIndexed |
| --- | --- | --- |
| 控制量名称、单位、合法范围、实际温度是过程遥测而非恒定釜温 | 允许 | 相同 |
| 公共安全、资源、仪器、评分合同 | 允许 | 相同 |
| 不依赖 P 层结果选择的共同非 P 材料/尺度上下文 | 允许 | 相同 |
| `420 K / 3300 s` 之类实例参考中心及其容差 | **禁止** | 可作为两臂完全匹配的 P 层资料共同提供 |
| 温度或时间的方向、窗口、斜率、方程、局部最优或可行性暗示 | **禁止** | A/M 以同 schema、同锚点、同置信度提供，只允许目标关系方向不同 |
| private seed、truth family、机理标签、隐藏参数或运行结果 | **禁止** | 同样禁止 |

因此，未来 runner 不得直接复用当前 `build_public_priors(...)["opaque"]` 中带 `approximate_reference_region` 的对象。Strict P-Opaque 的序列化 payload 必须删除参考中心、容差和任何由目标 P 世界标定出的提示；不能只把 `model` 设为 `null` 就称为 Opaque。若以后确需研究“只有工作点、没有方向规律”的帮助，可另设 `ContextOnly` 诊断，但它不属于主 O/A/M 三臂，也不进入三臂效应。

### 1.2 历史归类与跨层审计记录

本次纠正不追溯改写既有轨迹，只修正名称和未来矩阵：

| 既有块 | 实际信息边界 | 本版本解释 |
| --- | --- | --- |
| EC-E 六场核心 | E-Opaque 隐藏目标材料描述；P 控制量属于 E 层之外的公共操作信息 | strict E-Opaque，未发现本类泄漏 |
| EC-P 两场补充中的所谓 Opaque | 收到完整 P 层参考配方 | `ContextOnly` 历史补充，不是 strict P-Opaque，也不能支撑 P 三臂结论 |
| RX-P 双目标 canary 中的所谓 Opaque | 收到 `420 K / 3300 s` 近似参考区域及容差 | `ContextOnly` 历史 canary，不是 strict P-Opaque |
| RX-S v1.1 设计 | Opaque 为 `None`；A/M 才收到格式对称、方向竞争的结构主张 | strict S-Opaque；未发现同类目标层泄漏 |

2026-09-19 的只读可见面检查进一步确认：RX-S 基线与结构变体的 evaluator-private mechanism/intervention hashes 不同，但 agent 可见 task contract 和 Opaque material payload 完全相同；`tests/test_experiment_1_rx_qualification.py` 为 `4 passed`。这只是信息边界审计，不是 Participant 结果或正式 RX-S 执行。后续实现仍须增加显式回归断言：`RX-S Opaque` 无 `initial_world_model`，且隐藏结构变化不改变公共 payload。

### 1.3 Q 中出现 420 K 不构成来源先验

本文件第5节的 Q 在来源任务交付和 K1 都封存后才一次性给出，并且六个来源收到完全相同的查询且不获得结果反馈。因此 Q01/Q02/Q05/Q06 中出现 `420 K`、`3300 s` 是共同盲测设计，不是来源阶段的 P 层先验。禁止泄漏的是来源开始前送入 Strict P-Opaque 的实例参考区域；不能据此删除共同 Q，也不能把 Q 条件提前透露给来源。

## 2. 从通用协议继承的部分

以下内容直接继承 v1.1，不在本文件另造变体：

- 封存顺序：来源任务交付 → K1 → Q → K2 → 参考真值/评分；
- K1 的逐字固定提示；
- Q 的逐字固定外层提示；
- K2 的逐字七问；
- K1/K2 `report`、Q `rationale` 和其他自由文本统一使用英文；
- K1、Q、K2 不补做物理实验、无真值回流、互不覆盖；
- 后测计算器政策、原失败保留和有限平台修复规则。

RX 来源阶段的最终推荐理由和结束摘要也使用英文。来源提示仍可用英文；语言统一只影响交付形式，不改变科学标准。

## 3. 研究单位和来源资源

| 字段 | 冻结值 |
| --- | --- |
| task | `reaction-safety-constrained` |
| world | `RX-W01` |
| prior locus | `P` |
| arms | `Opaque`, `Aligned`, `MisIndexed` |
| goals | `mechanism_discovery`, `safety_constrained_optimization` |
| source sessions | 6 个独立持久会话；每臂每目标各 1 |
| source experiments | 每会话 12 个独立完整批次 |
| non-final measurements | 每会话最多 12 次，按需分配 |
| final assays | 每会话最多 12 次；每个合法终止批次一次 |
| operation limit | 每会话 360 次尝试 |
| process time | 每会话 144000 s；quench 的隐含 120 s 照实记账 |
| public safety limit | `safety_risk <= 0.35` |
| model policy | 同一比较块使用同一模型和 reasoning effort；在运行 note 冻结 |
| posttest calculator | 只开放公共数值计算器，K1/Q/K2 各阶段上限 128；无实验室、网络、仓库或隐藏真值 |

来源允许自主选择溶剂、催化剂、用量、温度、时间、搅拌、分段热历史、等待、测量和 quench。两个目标资源相同且不共享来源数据：

- `mechanism_discovery`：主要目标是形成并检验能够解释和预测目标生成、竞争转化、催化剂作用/失活、实际热历史、时间及终止操作的机理；公开 safe score 为次要读出。
- `safety_constrained_optimization`：主要目标是在公开安全限制内寻找较高 safe score 的操作；机理和测量由 Agent 自主决定。

来源结束时必须从自己完成的批次中封存一项操作建议。探索任务的建议只是次要读出，不用推荐得分替代机理评价。

## 4. Q 的科学设计原则

十二题不是随机点，也不是从旧资格包顺序截取。它们按六个事前配对组成：

| 查询 | evaluator-only 设计角色 | 主要诊断问题 |
| --- | --- | --- |
| Q01–Q02 | 共同评测中心、quench 配对 | 在预注册评测中心能否作出预测，并把反应结果与终止操作作用分开 |
| Q03–Q04 | 温度轴配对 | 时间、配方和终止方式相同，只改变目标温度；是否学到温度方向和非线性 |
| Q05–Q06 | 时间轴配对 | 温度、配方和终止方式相同，只改变反应时间；是否学到生成—损失竞争 |
| Q07–Q08 | 热历史顺序配对 | 总阶段时间和温度组成相同，只反转先后顺序；是否学到路径依赖、失活或产物继续反应 |
| Q09–Q10 | 高温短时 quench 配对 | quench 作用能否从中心迁移到另一热暴露条件 |
| Q11–Q12 | 边界外推 | 低温长时和高温长时；是否扩大不确定性并避免把局部关系无界推广 |

`design role` 不进入发给受评 Agent 的查询 JSON，只用于事后分层评价。所有非目标配方变量固定在各臂共同、且不依赖 P 层结果选择的评测值，避免把温度—时间规律与材料或尺度变化混杂：

| 变量 | 固定值 |
| --- | ---: |
| solvent | 2 |
| solvent volume | 0.005 L |
| reagent amount | 0.003 mol |
| catalyst | 1 |
| catalyst amount | 0.000525 mol |
| stirring speed | 400 rpm |

这里的 `target_temperature_K` 是公开边界控制，不是恒定釜温；Agent 应自行考虑实际温度轨迹。Q07/Q08 的两个 `heat` 动作属于同一批次的连续热历史，不在两阶段之间测量或重置世界。

查询允许与某来源自主做过的条件偶然重合，因为它们在来源开始前冻结。事后另标记每个来源对各题的 exact overlap、近域和外推距离，但不据此换题。所有臂和两个目标使用相同顺序、相同动作及相同参考种子。

## 5. 发给 Agent 的完整十二题 JSON

下面 JSON 紧接通用协议 v1.1 的固定 Q 外层提示一次性发送，不附加第4节的设计角色：

```json
[
  {
    "query_id": "Q01",
    "actions": [
      {"operation": "add_solvent", "solvent": 2, "volume_L": 0.005},
      {"operation": "add_reagent", "amount_mol": 0.003},
      {"operation": "add_catalyst", "catalyst": 1, "catalyst_amount_mol": 0.000525},
      {"operation": "heat", "target_temperature_K": 420, "duration_s": 3300, "stirring_speed_rpm": 400},
      {"operation": "terminate"},
      {"operation": "measure", "instrument": "final_assay"}
    ]
  },
  {
    "query_id": "Q02",
    "actions": [
      {"operation": "add_solvent", "solvent": 2, "volume_L": 0.005},
      {"operation": "add_reagent", "amount_mol": 0.003},
      {"operation": "add_catalyst", "catalyst": 1, "catalyst_amount_mol": 0.000525},
      {"operation": "heat", "target_temperature_K": 420, "duration_s": 3300, "stirring_speed_rpm": 400},
      {"operation": "quench"},
      {"operation": "terminate"},
      {"operation": "measure", "instrument": "final_assay"}
    ]
  },
  {
    "query_id": "Q03",
    "actions": [
      {"operation": "add_solvent", "solvent": 2, "volume_L": 0.005},
      {"operation": "add_reagent", "amount_mol": 0.003},
      {"operation": "add_catalyst", "catalyst": 1, "catalyst_amount_mol": 0.000525},
      {"operation": "heat", "target_temperature_K": 390, "duration_s": 3300, "stirring_speed_rpm": 400},
      {"operation": "terminate"},
      {"operation": "measure", "instrument": "final_assay"}
    ]
  },
  {
    "query_id": "Q04",
    "actions": [
      {"operation": "add_solvent", "solvent": 2, "volume_L": 0.005},
      {"operation": "add_reagent", "amount_mol": 0.003},
      {"operation": "add_catalyst", "catalyst": 1, "catalyst_amount_mol": 0.000525},
      {"operation": "heat", "target_temperature_K": 450, "duration_s": 3300, "stirring_speed_rpm": 400},
      {"operation": "terminate"},
      {"operation": "measure", "instrument": "final_assay"}
    ]
  },
  {
    "query_id": "Q05",
    "actions": [
      {"operation": "add_solvent", "solvent": 2, "volume_L": 0.005},
      {"operation": "add_reagent", "amount_mol": 0.003},
      {"operation": "add_catalyst", "catalyst": 1, "catalyst_amount_mol": 0.000525},
      {"operation": "heat", "target_temperature_K": 420, "duration_s": 1500, "stirring_speed_rpm": 400},
      {"operation": "terminate"},
      {"operation": "measure", "instrument": "final_assay"}
    ]
  },
  {
    "query_id": "Q06",
    "actions": [
      {"operation": "add_solvent", "solvent": 2, "volume_L": 0.005},
      {"operation": "add_reagent", "amount_mol": 0.003},
      {"operation": "add_catalyst", "catalyst": 1, "catalyst_amount_mol": 0.000525},
      {"operation": "heat", "target_temperature_K": 420, "duration_s": 5100, "stirring_speed_rpm": 400},
      {"operation": "terminate"},
      {"operation": "measure", "instrument": "final_assay"}
    ]
  },
  {
    "query_id": "Q07",
    "actions": [
      {"operation": "add_solvent", "solvent": 2, "volume_L": 0.005},
      {"operation": "add_reagent", "amount_mol": 0.003},
      {"operation": "add_catalyst", "catalyst": 1, "catalyst_amount_mol": 0.000525},
      {"operation": "heat", "target_temperature_K": 390, "duration_s": 1800, "stirring_speed_rpm": 400},
      {"operation": "heat", "target_temperature_K": 450, "duration_s": 1800, "stirring_speed_rpm": 400},
      {"operation": "terminate"},
      {"operation": "measure", "instrument": "final_assay"}
    ]
  },
  {
    "query_id": "Q08",
    "actions": [
      {"operation": "add_solvent", "solvent": 2, "volume_L": 0.005},
      {"operation": "add_reagent", "amount_mol": 0.003},
      {"operation": "add_catalyst", "catalyst": 1, "catalyst_amount_mol": 0.000525},
      {"operation": "heat", "target_temperature_K": 450, "duration_s": 1800, "stirring_speed_rpm": 400},
      {"operation": "heat", "target_temperature_K": 390, "duration_s": 1800, "stirring_speed_rpm": 400},
      {"operation": "terminate"},
      {"operation": "measure", "instrument": "final_assay"}
    ]
  },
  {
    "query_id": "Q09",
    "actions": [
      {"operation": "add_solvent", "solvent": 2, "volume_L": 0.005},
      {"operation": "add_reagent", "amount_mol": 0.003},
      {"operation": "add_catalyst", "catalyst": 1, "catalyst_amount_mol": 0.000525},
      {"operation": "heat", "target_temperature_K": 440, "duration_s": 1500, "stirring_speed_rpm": 400},
      {"operation": "terminate"},
      {"operation": "measure", "instrument": "final_assay"}
    ]
  },
  {
    "query_id": "Q10",
    "actions": [
      {"operation": "add_solvent", "solvent": 2, "volume_L": 0.005},
      {"operation": "add_reagent", "amount_mol": 0.003},
      {"operation": "add_catalyst", "catalyst": 1, "catalyst_amount_mol": 0.000525},
      {"operation": "heat", "target_temperature_K": 440, "duration_s": 1500, "stirring_speed_rpm": 400},
      {"operation": "quench"},
      {"operation": "terminate"},
      {"operation": "measure", "instrument": "final_assay"}
    ]
  },
  {
    "query_id": "Q11",
    "actions": [
      {"operation": "add_solvent", "solvent": 2, "volume_L": 0.005},
      {"operation": "add_reagent", "amount_mol": 0.003},
      {"operation": "add_catalyst", "catalyst": 1, "catalyst_amount_mol": 0.000525},
      {"operation": "heat", "target_temperature_K": 370, "duration_s": 5700, "stirring_speed_rpm": 400},
      {"operation": "terminate"},
      {"operation": "measure", "instrument": "final_assay"}
    ]
  },
  {
    "query_id": "Q12",
    "actions": [
      {"operation": "add_solvent", "solvent": 2, "volume_L": 0.005},
      {"operation": "add_reagent", "amount_mol": 0.003},
      {"operation": "add_catalyst", "catalyst": 1, "catalyst_amount_mol": 0.000525},
      {"operation": "heat", "target_temperature_K": 460, "duration_s": 6300, "stirring_speed_rpm": 400},
      {"operation": "terminate"},
      {"operation": "measure", "instrument": "final_assay"}
    ]
  }
]
```

任何字段或顺序变化都需要新版本；不能依据来源实验或预测表现换题。runner 物化为独立 JSON 后，必须在来源启动前把其路径和 SHA-256 写入运行 note，并核对与本节逐字段一致。

## 6. 预测指标与输出合同

每题对以下六个 `[0,1]` 指标提交点估计和 80% 预测区间：

1. `yield`
2. `conversion`
3. `selectivity`
4. `byproduct_signal`
5. `safety_risk`
6. `score`

每题结构为：

```json
{
  "query_id": "Q01",
  "metrics": {
    "yield": {"estimate": 0.0, "lower80": 0.0, "upper80": 0.0},
    "conversion": {"estimate": 0.0, "lower80": 0.0, "upper80": 0.0},
    "selectivity": {"estimate": 0.0, "lower80": 0.0, "upper80": 0.0},
    "byproduct_signal": {"estimate": 0.0, "lower80": 0.0, "upper80": 0.0},
    "safety_risk": {"estimate": 0.0, "lower80": 0.0, "upper80": 0.0},
    "score": {"estimate": 0.0, "lower80": 0.0, "upper80": 0.0}
  },
  "rationale": "English rationale and uncertainty statement"
}
```

十二个 `query_id` 必须各出现一次；所有数值有限且满足 `0 <= lower80 <= estimate <= upper80 <= 1`。不得用总体 rationale 替代逐题英文依据。格式不合规与科学误差分开记录，不由评审代填数值或翻译。

## 7. 参考真值、噪声与评分

参考执行只在每个来源的 K2 封存后由隔离评价器运行；不反馈给受评会话。每个查询运行 5 个独立观测重复。重复种子由下式确定，避免人工挑种子：

```text
seed(query_id, replicate_id) =
  uint64_be(SHA256("rx-p-q-v1|RX-W01|" + query_id + "|r" + two_digit_replicate)[0:8])
  mod 2147483647
```

其中 `replicate_id = 01, 02, 03, 04, 05`。相同查询、臂和目标共享同一组参考执行，不为六个来源重复生成真值；参考重复不是六个独立世界。

点预测以五个独立观测的均值为该查询的参考中心，逐指标报告 MAE。80%区间对五个独立观测逐一评分，报告：

- empirical coverage；
- 平均区间宽度 `U-L`；
- 80% interval score：

```text
IS80(L, U; y) = (U - L) + 10(L - y) * I[y < L] + 10(y - U) * I[y > U]
```

分数越低越好。不能只用覆盖率，因为任意加宽区间会提高覆盖；也不能只用 MAE，因为接近零或饱和区会使常数预测显得良好。

评价按第4节六个设计配对分别报告，并另报十二题总体值。指标角色分开：

- 主要科学终点：`yield`、`byproduct_signal`、`safety_risk`；
- 支持性机理终点：`conversion`、`selectivity`；
- 次级决策终点：`score`。

`score` 是派生效用，不能和其组成信息等权重复计入未经校准的总分。默认不发布六指标平均总分；若以后需要主标量，必须在新版本中事前给出权重与理由。

配对差也单独评分：Q02−Q01、Q04−Q03、Q06−Q05、Q08−Q07、Q10−Q09。点预测必须从各题已封存点估计机械相减，不能另问 Agent 或事后重新提交。配对差用于检验方向和效应量，不增加独立题数。

## 8. 运行前验收与失败边界

在任何 provider 来源启动前，只做不读取目标世界结果的静态验收：

- Strict P-Opaque payload 不含 `approximate_reference_region`、实例参考中心/容差、方向、窗口、斜率、方程、最优或可行性暗示；`model: null` 本身不足以通过；
- A/M 的 P 层 payload 具有相同 schema、参考上下文、锚点、置信度和字段集合，只允许预注册的目标关系方向不同；
- `ContextOnly`（若另做）使用独立名称和独立分析，不进入 O/A/M 主矩阵；
- 十二个 ID 唯一、顺序固定；
- 所有动作满足公共字段范围和资源合同；
- Q07/Q08 为同一批次两段 heat，其他查询为单段 heat；
- 只有 Q02/Q10 含 quench；
- 每题恰有一次 terminate 和其后一次 final_assay；
- 六指标、英文输出和计算器预算进入实际模型提示；
- O/A/M 与两个目标引用同一查询文件哈希；
- 查询、参考生成器和评分器不能被受评 Agent 访问。

动态参考结果不得在来源前生成或读取。若 K2 后的某条参考执行出现平台、合法性或 replay 失败，保留失败并按通用协议处理；不能根据已看到的科学结果换点。若确认本协议动作本身不可执行，整个尚未见真值的受影响块停止，并通过新版本修订，不把部分可用题事后拼成十二题。

## 9. 本协议能回答和不能回答的问题

本设计可以分别观察：共同评测中心预测、局部温度斜率、局部时间斜率、热历史顺序、quench 因果对照、边界外推和区间校准。相同题用于两个来源目标，可以检验机理探索是否比优化更倾向于获得可迁移的预测知识；相同题用于三臂，可以检验没有实例 P 先验、正确 P 资料或错配 P 资料怎样影响学习与修订。

单个 `RX-W01` 仍不能证明跨世界普遍规律；六个来源各一次也不能估计稳定的平均模型效应。查询固定参考配方，因此不能评价材料、催化剂或尺度迁移。K1/K2 的语言质量、Q 的预测表现、来源操作得分和推荐复测必须分开报告。
