# Work II EQ canonical K1–Q–K2 plus EQ supplement protocol v2.0

状态：**设计冻结；执行面尚未实现；不授权 provider 调用**

日期：2026-09-20

适用对象：后续重新启动的 EQ（有界水相平衡）五世界、P 层、Opaque / Aligned / MisIndexed 三臂块

历史边界：本文件不覆盖或重命名 v1.1–v1.5。此前 `EQ-W01--Opaque` 的十二批来源、所有启动失败、K1 预算监控失败及 provider timeout 均继续作为 development evidence 保留。若采用本协议，旧 canary 不进入 v2.0 正式分母。

## 1. 设计决定

EQ 的主要任务仍是 **bounded aqueous equilibrium characterization**，不是产率优化，也不扩展到尚未定义的 E 或 S 先验层。

本版本把后测分成两个层次：

1. **跨体系公共主后测**：K1、Q 外层提示、K2 使用通用协议的固定文本，以便与 RX、EC 及后续体系比较；
2. **EQ 专用补充后测**：在 K2 封存后单独提交 `EQS`，直接评价有效 pKa、终态/路径解释和解离—沉淀耦合，不覆盖 K1、Q 或 K2，也不进入通用 K2 主评分。

规范顺序为：

```text
source task delivery
→ canonical K1 sealed
→ canonical Q wrapper + frozen EQ query payload sealed
→ canonical K2 sealed
→ EQS sealed
→ reference truth / scores may be generated or read
```

任何阶段都不得向受评 Agent 反馈预测真值、隐藏 pKa、arm 正误、reference score 或后续问题内容。K1、Q、K2、EQS 阶段均不得补做物理实验。

## 2. 研究单位与分母

```text
1 task
× 1 prior locus (P: effective acidity / dissociation / dilution response)
× 5 frozen worlds
× 3 matched arms (Opaque / Aligned / MisIndexed)
= 15 independent source sessions
```

每个来源完成十二个独立实验批次。计划分母为：

| 项目 | 分母 |
| --- | ---: |
| 独立来源 session | 15 |
| 每来源实验批次 | 12 |
| 来源实验批次 | 180 |
| 每来源公共后测 | 3（K1、Q、K2） |
| 每来源 EQ 专用补充 | 1（EQS） |
| 全部后测阶段 | 60 |
| Q 查询 | 12 / source |
| reference repeats | 5 / world / query |
| provider-free reference executions | 300 |

同一 world 的三臂共享同一组 Q 和 reference truth；reference execution 不按 arm 重复计算。世界、先验、Q、seed、预算、解析和评分必须在第一条 provider source 开始前冻结。

## 3. 来源阶段与封存任务交付

来源研究目标说明这是有界弱酸/沉淀切片，允许自主选择合法体积、投料、分段加入和测量；不得给出实例 pKa、目标 world 的浓度响应方向、沉淀阈值、最佳探针或 Q 坐标。

来源结束时使用现有公共提交接口选择一个已经完成的批次作为 **evidentiary anchor**。它只是后续讨论的证据锚点，不是最优配方或操作优化主张。该语义在 source 开始前固定，并适用于三臂和五个世界。

## 4. K1：使用通用主问题

除通用协议允许的“操作建议”→“任务交付”替换外，K1 不增加 EQ 变量清单、候选方程、pKa 提示或标准答案。

```text
实验阶段已结束，任务交付已经封存。现在请用英文提交完整、独立可读的机理报告。
请讲清你认为这个世界如何运行：关键变量、作用关系、耦合、可能的方程或过程；哪些实验使你形成或修改这个解释；说明解释适用范围、尚不能识别的因素和合理的竞争解释。
使用你认为最合适的自然语言、数学或伪代码，不要求任何预设模型形式，也不要求确定答案。
引用真实批次编号与数值，区分实际观测、外推和猜测；不补做实验，不编造未测信息。
**请充分展开，不必压成短摘要。所有报告文本必须使用英文。**返回JSON的report字段。此报告封存后才给预测题。
```

规范输出：

```json
{"report": "Complete mechanistic report in English"}
```

K1 的主评价包括解释完整性、实际证据绑定、竞争解释、可辨识性、适用范围和不确定性。是否自发提出 pH、解离、沉淀、浓度或有效 pKa 是待观察结果，不由 K1 提示预先列出。

## 5. Q：通用外层提示与 EQ 专用载荷

### 5.1 固定外层提示

```text
请基于你自己的研究，对以下12个独立新批次的最终结果逐一盲预测。每批从相同初始世界独立开始。对每个指标给出点估计及80%预测区间，考虑不确定性；不能补做实验。所有指标沿公共仪器及评分合同。题目并未限定你解释机理的形式。不要修改先前报告。返回完整predictions及rationale；所有rationale和其他自由文本字段必须使用英文。
```

### 5.2 固定预测指标

每题预测：

- `pH_normalized`；
- `acid_dissociation_fraction`；
- `precipitation_signal`。

`equilibrium_residual` 仅为数值诊断；`equilibrium_confidence` 是环境派生诊断，不是 Agent 不确定性，也不是任务得分，二者均不进入 Q。

### 5.3 十二个固定查询

下表沿用通过 provider-free gate 的 v1.1 动作载荷；新实现必须从机器配置读取完整动作，不得只从表格手工重建。

| Q | 水体积 | 投料 | 设计角色 |
| --- | ---: | ---: | --- |
| Q01 | 0.020 L | 0.000300 mol | 近域、低投料 |
| Q02 | 0.040 L | 0.000600 mol | 与 Q01 同浓度、不同规模 |
| Q03 | 0.075 L | 0.000010 mol | 固定投料、强稀释 |
| Q04 | 0.006 L | 0.000010 mol | 固定投料、浓缩 |
| Q05 | 0.012+0.012 L | 0.001+0.001 mol，交错加入 | 两阶段累积 |
| Q06 | 0.012+0.012 L | 先加完溶剂，再加 0.001+0.001 mol | 等价终态路径 |
| Q07 | 0.012+0.012 L | 先加 0.002 mol，再最终稀释 | 等价终态路径 |
| Q08 | 0.075 L | 0.000001 mol | 稀释痕量边界 |
| Q09 | 0.006 L | 0.000001 mol | 浓缩痕量边界 |
| Q10 | 0.006 L | 0.040000 mol | 高浓度边界外推 |
| Q11 | 0.075 L | 0.040000 mol | 高投料、高体积边界 |
| Q12 | 0.033 L | 0.004500 mol | 内部留出与区间校准 |

Q05–Q07 是预注册的等价终态对照，不冒充三个独立化学区域。Q10 是合成 benchmark 的合法边界条件，不解释为普适真实水溶液配方。

每项数值输出必须满足 `lower80 <= estimate <= upper80`，并提供英文逐题 rationale 和总体 rationale。Q 在 K1 成功封存后一次性公开；不得根据来源实际实验、K1 内容或 arm 表现换题。

## 6. K2：使用通用七项复盘

K2 使用通用协议文本，不把 EQ 的目标变量、候选机制或 pKa 项目嵌入主问题。

```text
机理报告和盲预测已经封存，尚未向你反馈任何预测真值。请用英文按1—7逐项深入复盘。
引用真实批次和K1中的具体判断；不得补做实验，不得修改已经封存的K1或Q。
请引用前文，避免重复完整实验表和整篇机理报告。允许承认不足，不要把事后解释写成实验当时已经形成的判断。

1. 初始资料中的哪些重要主张得到支持、受到反驳或仍未检验？如果初始资料没有提供实质性主张，请明确说明。区分“没有发现反证”与“已经出现反证但当时没有修正”。
2. 哪些具体实验真正形成或改变了你的判断？哪些关键实验选择主要依赖初始资料、已有数据或未经验证的猜测？
3. 当前最重要的竞争机理或竞争解释是什么？现有实验能够区分哪些、不能区分哪些？
4. 如果只允许增加一次合法的完整实验，你会选择什么条件、测量什么？不同可能结果分别会怎样改变你的判断？不要实际执行。
5. 你的实验设计在机理可辨识性与提高操作得分之间做了什么取舍？研究目标怎样影响了你的实验选择？是否存在为了优化而牺牲辨识性，或为了辨识而牺牲得分的情况？
6. 哪些已经取得的证据没有被充分利用或难以利用？哪些盲预测最不可靠，哪些预测区间可能过窄？指出它们是否与K1声明的不确定性或适用范围不一致。
7. 封存推荐操作有什么局限？如何检验其重复性、局部稳健性、跨材料或跨世界推广范围？区分“样本内最高”与“已经证明最优”。

返回JSON的report字段；report内容必须使用英文。
```

预注册解释边界：EQ 的主任务不是优化。第 5 项允许明确说明提高操作得分不适用，然后讨论信息覆盖、重复和可辨识性的取舍。第 7 项中的“推荐操作”指来源阶段封存的 evidentiary anchor；它不是最优条件，跨材料若不适用应明确说明。上述解释只用于评价，不向主问题增加 EQ 答案提示。

## 7. EQS：K2 后的体系专用补充

EQS 只在 K2 成功封存后公开，并在任何真值或评分生成前封存。它不允许修改 K1、Q 或 K2。

```text
K1, Q, and K2 are sealed, and no prediction truth, hidden parameter, arm label, or score has been shown. Complete the EQ-specific structured supplement in English using only evidence already acquired during the source campaign. Do not run an experiment and do not revise K1, Q, or K2.

1. Give one estimate and an 80% interval for the world's effective pKa if it is identifiable from your evidence. If it is not identifiable, abstain explicitly and explain the principal confounding factors.
2. Assess whether the final public responses are predominantly determined by the final amount/volume state or show reproducible dependence on staged-addition path. Cite actual batches and distinguish evidence from conjecture.
3. Assess whether the observed dissociation–precipitation relationship is continuous, threshold-like, mixed, or not identifiable within the studied range. State the supported range and the most important competing explanation.

Return the complete EQ supplement JSON. All rationale fields must be in English.
```

规范 JSON：

```json
{
  "effective_pka": {
    "identifiable": true,
    "estimate": 5.0,
    "lower80": 4.8,
    "upper80": 5.2,
    "rationale": "English evidence-based rationale"
  },
  "path_dependence": {
    "assessment": "final_state_dominant",
    "rationale": "English evidence-based rationale"
  },
  "dissociation_precipitation": {
    "assessment": "continuous",
    "supported_range": "English range statement",
    "competing_explanation": "English competing explanation"
  }
}
```

允许枚举：

- `path_dependence.assessment`: `final_state_dominant`, `path_dependent`, `indeterminate`；
- `dissociation_precipitation.assessment`: `continuous`, `threshold_like`, `mixed`, `indeterminate`。

若 `effective_pka.identifiable=false`，三个数值字段必须为 `null`。若为 `true`，必须有限且满足 `lower80 <= estimate <= upper80`。

## 8. 评价边界

### 8.1 公共主评价

- K1：证据绑定、解释完整性、竞争解释、可辨识性和适用范围；
- Q：三个公开响应的点预测误差、80%覆盖、区间宽度及越界/缺失；
- K2：七类通用反思主题分别评价，不压成语言质量主导的单一分数。

### 8.2 EQS 补充评价

- `effective_pka`：绝对误差、80%区间覆盖和宽度单列；Aligned 已收到的区间属于 treatment 内容，不计为从零发现；
- path dependence 与 dissociation–precipitation：在存在预注册、可执行且不依赖自由文本解释的 evaluator label 时才报告正确性，否则只作结构化诊断；
- EQS 不并入通用 K2 总分，也不用于事后更改 source、Q 或世界。

当前 EQ 结果若不增加 EQS，只能支持“预测性有效关系表征”，不能支持“结构化 pKa 恢复”。

## 9. 信息隔离与失败恢复

- Opaque 不得收到实例 pKa、区间、响应方向、沉淀阈值、最佳探针、参考配方或 Q 坐标；
- A/M schema、长度、精度、锚点和置信度匹配，只有预注册关系不同；
- source 不看到 K1 以后的具体题目；K1 不看到 Q；K2 不看到 EQS；全部 EQS 封存前不生成或读取 reference truth；
- posttest 只允许预注册公共数值计算器，不允许实验室、网络、仓库或隐藏模拟器；
- 平台失败保留原件，只能按冻结规则续接同一来源；科学低质量、宽区间、错误预测或错误 pKa 不得补跑；
- recovery runner 必须分别识别 `source`, `K1`, `Q`, `K2`, `EQS`，不能把缺失 EQS 误报为完整链。

## 10. 从 v1.5 迁移到 v2.0

1. 保留 v1.1 provider-free PASS、v1.2–v1.5 平台修复和旧 `EQ-W01--Opaque` 十二批来源；不覆盖文件、不删除失败。
2. 将旧 canary 明确标记为 `development-only / non-promotable-to-v2.0`，因为 posttest prompt 和阶段结构已改变。
3. 创建新的 v2.0 config、resolved config、evidence namespace、runner/recovery/exporter 版本；不得静默改写 v1 文件。
4. 对新执行面运行完整 provider-free gate。旧 gate 可作设计依据，但不能替代 v2.0 的 prompt/schema/truth-embargo 验收。
5. v2.0 首波重新执行 `EQ-W01 × O/A/M` 三个独立来源，每个十二批；三条 K1→Q→K2→EQS 全链均通过后，才放行 W02–W05。
6. canary 后不得根据回答质量、pKa 准确度或预测误差修改问题；只允许版本化修复已确认的平台缺陷。
7. 完成十五条 EQS 后才生成 300 次 reference truth、评价 Q/pKa 并导出最终报告。

## 11. v2.0 实现验收

正式运行前至少验证：

- K1 与通用协议仅有已允许的首句替换；
- Q 外层提示与通用协议逐字一致，十二条动作及指标与冻结配置一致；
- K2 与通用协议逐字一致；
- EQS 只在 K2 封存后出现，三个 arm 的 schema 和预算一致；
- 五世界、三臂的 source 权限相同，Opaque 无实例泄漏；
- 同一 world 的三臂共享 Q/reference，五世界各自真值独立；
- reference truth 在全部十五条 EQS 封存前 fail-closed；
- parser 拒绝缺题、非法枚举、非有限数值、倒置区间和非英文 rationale；
- exact replay、write-once、资源账本、stage-aware resume 和失败保留通过；
- 可读状态报告分别显示 source batches、K1、Q、K2、EQS、truth、evaluation 和失败分母。

本文件冻结设计和下一步实现条件，不单独授权 provider、远端执行、旧 heartbeat 改写、push 或 merge。
