# W2-117：五体系首轮 gate 实测

固定开发块；无模型调用、无重试。完整科学资格与 Agent 后测链尚未通过。

耗时 2.06 分钟；真实多批campaign 8/8 完整，终检 30/30，记录动作 246。
共用账本 8/8，精确重放 8/8；重放不增加独立样本。

旧三臂资料入口可构造 7/15；基础筛查 0/5；入口与基础筛查合取 0/5；成对世界差异 1/3。

这些比例是固定小覆盖的工程/科学必要条件通过率，不是 Agent 成功率或全矩阵资格率。

| 体系 | 三臂入口 | 基础多批 | 账本 | 重放 | S1公开响应 | 基础合取 | S2世界差异 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RX | 未通过 | 通过 | 通过 | 通过 | 未通过 | 未通过 | 未接入 |
| EQ | 未通过 | 通过 | 通过 | 通过 | 未通过 | 未通过 | 通过 |
| BC | 未通过 | 通过 | 通过 | 通过 | 未通过 | 未通过 | 未接入 |
| PA | 通过 | 通过 | 通过 | 通过 | 未通过 | 未通过 | 未通过 |
| FL | 未通过 | 通过 | 通过 | 通过 | 未通过 | 未通过 | 未通过 |

## 每个 campaign 的终态

| 条件 | 完成批次 | 动作 | 运行秒 | 重放秒 | 失败 |
| --- | --- | --- | --- | --- | --- |
| RX-base | 4/4 | 36/36 | 19.36 | 0.89 | 无 |
| EQ-base | 4/4 | 24/24 | 8.17 | 0.42 | 无 |
| EQ-shift | 4/4 | 24/24 | 8.17 | 0.39 | 无 |
| BC-base | 2/2 | 18/18 | 6.94 | 0.42 | 无 |
| PA-base | 4/4 | 40/40 | 19.89 | 0.73 | 无 |
| PA-shift | 4/4 | 40/40 | 19.86 | 0.70 | 无 |
| FL-base | 4/4 | 32/32 | 17.48 | 1.08 | 无 |
| FL-shift | 4/4 | 32/32 | 17.39 | 1.09 | 无 |

## 入口失败（全部保留）

- RX/A：ValueError — nominal material properties require exactly one audited prior task
- RX/M：ValueError — nominal material properties require exactly one audited prior task
- EQ/A：ValueError — nominal material properties require exactly one audited prior task
- EQ/M：ValueError — nominal material properties require exactly one audited prior task
- BC/A：ValueError — nominal material properties require exactly one audited prior task
- BC/M：ValueError — nominal material properties require exactly one audited prior task
- FL/A：ValueError — nominal material properties require exactly one audited prior task
- FL/M：ValueError — nominal material properties require exactly one audited prior task

## 公开终检（顺序对应实验说明中的固定批次）

### RX-base

| 批次 | yield | conversion | byproduct_signal |
| --- | --- | --- | --- |
| 1 | 0.966964 | 1.000000 | 0.028091 |
| 2 | 0.968909 | 0.998125 | 0.023277 |
| 3 | 0.644343 | 1.000000 | 0.183601 |
| 4 | 0.651804 | 0.988824 | 0.193000 |

### EQ-base

| 批次 | pH_normalized | acid_dissociation_fraction | precipitation_signal |
| --- | --- | --- | --- |
| 1 | 0.280616 | 0.079553 | 0.155577 |
| 2 | 0.276316 | 0.083719 | 0.155192 |
| 3 | 0.277260 | 0.073050 | 0.154044 |
| 4 | 0.274994 | 0.071622 | 0.163499 |

### EQ-shift

| 批次 | pH_normalized | acid_dissociation_fraction | precipitation_signal |
| --- | --- | --- | --- |
| 1 | 0.365780 | 0.078387 | 0.155669 |
| 2 | 0.360463 | 0.080348 | 0.155432 |
| 3 | 0.362861 | 0.072813 | 0.154063 |
| 4 | 0.360374 | 0.070916 | 0.163555 |

### BC-base

| 批次 | yield | conversion | byproduct_signal |
| --- | --- | --- | --- |
| 1 | 0.869379 | 1.000000 | 0.079702 |
| 2 | 0.870398 | 0.998125 | 0.075864 |

### PA-base

| 批次 | product_in_organic | product_in_aqueous |
| --- | --- | --- |
| 1 | 0.914466 | 0.000000 |
| 2 | 0.904020 | 0.000000 |
| 3 | 0.924058 | 0.000000 |
| 4 | 0.898811 | 0.000422 |

### PA-shift

| 批次 | product_in_organic | product_in_aqueous |
| --- | --- | --- |
| 1 | 0.945030 | 0.000000 |
| 2 | 0.940849 | 0.000000 |
| 3 | 0.951954 | 0.000000 |
| 4 | 0.930149 | 0.000422 |

### FL-base

| 批次 | flow_conversion | yield |
| --- | --- | --- |
| 1 | 0.012729 | 0.000000 |
| 2 | 0.000000 | 0.005601 |
| 3 | 0.003105 | 0.000000 |
| 4 | 0.014310 | 0.030843 |

### FL-shift

| 批次 | flow_conversion | yield |
| --- | --- | --- |
| 1 | 0.014151 | 0.000183 |
| 2 | 0.003711 | 0.010529 |
| 3 | 0.008898 | 0.002847 |
| 4 | 0.034937 | 0.049529 |

## 结果诊断与下一轮设计方向

上面的计数、判定和观测表由 runner 生成；本节为保留数据的事后解释，不改变本轮通过率，也未追加物理执行。完整已购测量已补入机器报告的 `retained_measurement_diagnostics`。

| 体系 | 实际发现 | 对下一轮的影响 |
| --- | --- | --- |
| RX | 335/385K温度对比弱；但延长时间后yield分别从0.967降到0.644、从0.969降到0.652。首次HPLC的conversion已约0.998—1.000 | 时间效应明确，S1失败不等于体系没有规律。需要更早阶段、催化/投料干预和公开实际热历史，才能辨别生成与竞争转化 |
| BC | 两次首次HPLC也已接近完全转化；终检yield仅差0.001 | 当前温度探针没有体现有限测量预算的判别价值；先验证竞争解释及预算内可分的观测时机，再比较Agent测量安排 |
| EQ | 稀释的归一化pH差仅0.002—0.004，未达0.01；pKa变化世界同点差0.084—0.086，4/4越阈值 | 世界变化可测，当前稀释设计判别力不足。应检验有效参数/等价解释的留出预测；如需独立滴定控制，须明确开发，不能把新操作当成现成能力 |
| PA | 终检extractant对比差0.010/0.025，未达0.0424；世界变化最大差0.0368。分相前HPLC的organic通道约0.383—0.636，分相后约0.864—0.928；aqueous通道接近零 | 阶段和体积已有响应，但同名通道的分母、相对象及两相物料闭合尚需核定；不能将前后读数差直接解释为真实产物增加或归因给Agent |
| FL | 基础四点conversion为0—0.0143、yield为0—0.0308。仅长停留条件的温度yield差越过单对阈值；示例可行点0/4 | 既未满足“两对均通过”的规则，也未覆盖可行/不可行边界。先建立真实可行见证和出口/温度/压力观测合同，再研究窗口发现 |

PA本轮调用原生默认scoring contract；旧 `run_work_ii_partition_constitutive_q0.py` 显式使用 `PARTITION_S0_EXTRACTION_EFFICIENCY_V3`，观测服务有独立分支。**本轮不替代或推翻旧合同的资格**。新PA任务必须明确选择/修订哪条观测合同，并独立验证两相数据。这个发现是当前新卡接入不完整，不能把默认接口输出直接当作已经合格的任务数据。

三臂入口只有PA具备全部O/A/M兼容性；其余四卡的A/M均被现有静态材料入口拒绝。这表明当前适配缺口，不要求新设计沿用旧材料描述：应为定制委托制定可被公开实验检验的实例先验。构造成功也不证明Aligned内容与当前世界匹配，本轮没有测试三臂Agent行为。

下一块优先利用RX已有时间效应与EQ可测世界差异，PA先核定两相观测，FL先建立可行窗口，BC把稀缺测量安排在可分时段。五卡同步接入各自先验与公共操作/观测说明，保持自由机理报告，不给Agent限定方程模板。通过相应任务资格后再做Astra medium逐条件一次的来源试跑；本轮没有启动这部分。

## 解释边界

S1要求预定的两对对比在同一主通道均超过3倍合并仪器噪声及最小效应；BC仅一对。S2要求同通道至少2/4条件越阈值。它们不是结构可辨识性证明或正式显著性检验。
旧适配器构造失败说明当前调用路径未接入，不能推断模拟器不能支持该科学任务；旧nominal dossier可构造也不证明新卡的Aligned内容已科学验证。
G-D仅本块明确；G-S仍缺留出预测/任务可达性与先验内容核验；G-R本轮覆盖真实多批、资源和重放，未覆盖provider→自由K1→Q→K2；G-J未测，G-F不适用，G-C保留全部终态。
RX/BC未接入规律变化接口。PA本轮未独立核验两相质量守恒；FL的示例窗口阈值仅作开发诊断；EQ的confidence不作为Agent置信度。

[固定说明](../WORK_II_NEW_SYSTEM_GATE_NOTE.md) · [机器结果](work-ii-new-system-gates-20260916.json)
