# EQ/P：原自主研究的过程与结论核对

2026-09-22。只分析保留数据，零新模型、模拟器或评审调用。覆盖全部 15 场有效来源、五世界三臂、180 批、945 步操作和 45 个 K1/Q/K2 阶段。原始恢复与历史失败沿用来源记录，不替换来源，也不将本次分析升级为正式证据。

**核心发现：原自主研究的最终预测呈现不同的外推方式。五个 Opaque 会话都允许极稀条件离开已测平台，五个 Aligned 会话都主要延续平台或弱趋势；MisIndexed 有一个混合解释反例。这可把已有误差差异连接到公开表达的预测规则，但不能定位实验过程中哪个推理步骤导致差异。**

本报告的单位是原 agent 完成的自主研究。固定记录的新会话读出已退出验证路径，其两次结果及资源继续保留，不混入下表，也不据此否定原研究。

## 1. 范围与方法

按已发布来源索引和轨迹索引纳入全部十五场；逐步计数操作与测量，按实际加料之和计算终态配方名义浓度，不将它冒充活性溶解浓度。Q03/Q08/Q09 沿用此前按公开配方浓度选择的最稀三题，其余九题不全是插值。所有 Q 分数对原五次参考观测复算，逐场加权复现原总 MAE。

文本核对只编码两项有限问题：Q 公开解释采用何种低浓度外推；K2 选择什么下一实验。十五场均保留 K1 适用域摘录、Q 原解释、K2 对应原段落及原文件引用。这是单次作者探索性解释编码，不是词频自动归因，也不宣称完成全部 240 场的机理标注。类别允许定性偏离、混合解释和非稀释后续实验。

完整阶段证据与数值见 [机器摘要](EQ_AUTONOMOUS_PROCESS.json)。读取现有 configs/current.json 后，当前 EQ/P 队列沿用现行矩阵指定的发布索引；不从旧注册表恢复历史实验，也不按版本名挑选有利结果。

## 2. 实验实际覆盖了什么

15/15 场的终态配方名义浓度均高于三道最稀题；最低为约 0.01852 mol/L，而三题分别约为 0.0001333、0.00001333、0.0001667 mol/L。这些研究没有直接测到目标极稀区间。参数跨度大不代表已经跨过响应转折。

945/945 个决策 audit 状态都是 `not_provided`，诊断目标和预期效应字段为空。公开动作和观测可追溯，逐步的同期决策理由没有被提供。不能用这些占位字段重建认知更新，也不能把 K1/K2 的事后解释当作逐步决策记录；这不意味着原模型没有进行推理。

## 3. 全部十五场：覆盖、预测规则和 Q08 数值

Q08 是 1 μmol / 75 mL；下列解离分数、区间及参考均值均来自原自主会话。分类依据是封存 Q 的公开说明，含义仅限于可观察的外推方式。

| 来源 | 已测名义浓度范围 mol/L | Q 外推方式 | Q08 解离预测 [80%区间] | 参考均值 |
|---|---:|---|---:|---:|
| W01/Opaque | 0.05000–1.00000 | 分段弱酸外推 | 0.6990 [0.2500, 0.9000] | 0.7160 |
| W01/Aligned | 0.01852–1.00000 | 平台／弱趋势延拓 | 0.1040 [0.0440, 0.2250] | 0.7160 |
| W01/MisIndexed | 0.01852–2.00000 | 平台／弱趋势延拓 | 0.1092 [0.0772, 0.1412] | 0.7160 |
| W02/Opaque | 0.10000–0.40000 | 分段弱酸外推 | 0.6290 [0.4500, 0.8000] | 0.6546 |
| W02/Aligned | 0.01852–1.66667 | 平台／弱趋势延拓 | 0.0804 [0.0530, 0.1080] | 0.6546 |
| W02/MisIndexed | 0.01852–0.74074 | 平台／弱趋势延拓 | 0.0806 [0.0556, 0.1056] | 0.6546 |
| W03/Opaque | 0.06250–1.16667 | 分段弱酸外推 | 0.5630 [0.4300, 0.7000] | 0.5797 |
| W03/Aligned | 0.01852–1.00000 | 平台／弱趋势延拓 | 0.1100 [0.0450, 0.1900] | 0.5797 |
| W03/MisIndexed | 0.01852–2.00000 | 弱酸与平台解释混合 | 0.4600 [0.1000, 0.7500] | 0.5797 |
| W04/Opaque | 0.05000–0.80000 | 允许脱离平台（定性） | 0.5200 [0.1500, 0.8800] | 0.5173 |
| W04/Aligned | 0.01852–1.00000 | 平台／弱趋势延拓 | 0.0724 [0.0400, 0.1050] | 0.5173 |
| W04/MisIndexed | 0.01852–0.66667 | 平台／弱趋势延拓 | 0.0962 [0.0400, 0.4500] | 0.5173 |
| W05/Opaque | 0.04444–1.33333 | 分段弱酸外推 | 0.4130 [0.2000, 0.7000] | 0.4480 |
| W05/Aligned | 0.03333–0.82500 | 平台／弱趋势延拓 | 0.0790 [0.0350, 0.1300] | 0.4480 |
| W05/MisIndexed | 0.01852–0.83333 | 平台／弱趋势延拓 | 0.0681 [0.0400, 0.0960] | 0.4480 |

Opaque 的 W01/W02/W03/W05 明确使用弱酸关系连接低浓度与高浓度平台；W04 给出脱离平台的定性外推，不强行归类为同一个定量机理。Aligned 五场虽然承认极稀条件的外推风险，数值仍接近平台。MisIndexed W03 使用弱酸与背景平台的混合解释，Q08 解离预测为 0.46，构成不能省略的反例；不能写成有资料必然维持平台。

| 原自主研究分组 | Opaque MAE / 覆盖率 | Aligned MAE / 覆盖率 | MisIndexed MAE / 覆盖率 |
|---|---:|---:|---:|
| 最稀三题 | 0.01833 / 93.3% | 0.15862 / 2.2% | 0.14397 / 13.8% |
| 其余九题 | 0.01008 / 90.7% | 0.00465 / 91.3% | 0.00439 / 89.6% |

MAE 对原五次参考均值计算，三响应等权；覆盖率对全部参考观测计算。每臂稀释组为 5 世界 × 3 题 × 3 响应 × 5 观测 = 225 个覆盖判断，其余组为 675 个，这些判断不构成独立世界。分组是事后分析，五个世界共享底层结构，不能扩展为普遍化学规律。

## 4. 哪些结论已经在 K1，哪些是在 Q 才具体化

W01/Opaque 的 K1 已计算约 2.2×10⁻⁵ 的有效 Ka，以及约 0.004 mol/L 的活性池上限；同时承认缓冲、溶解限制和观测映射尚不能唯一辨别。Q 使用这个假设进一步计算低浓度解离。这一例存在可核对的 K1→Q 延续。

W02/Opaque 的 K1 则主要支持 pH 调节平台和有效 pKa≈4.85，并明确限制域外外推。Q 才给出约 0.0026 mol/L 的溶解浓度上限并使用未饱和弱酸计算。因此只能说完整原会话在作答时形成了有效外推，不能把 Q 的全部成功记为 K1 已封存的发现。

W02/Aligned 的 K1 同样得到局部有效 pKa≈4.84，且明确说不能把平坦响应外推到零加料。但 Q08 仍沿弱对数趋势给出解离分数 0.0804、区间 [0.053, 0.108]，参考约 0.6546。两臂在局部参数表述上的接近，没有带来相同的低浓度预测。这比“一个有知识、另一个没知识”更准确；尚不能证明先验通过锚定造成差异。

所引用的 K1 均明确限制适用范围；有限文本核对显示，承认范围限制与把它落实到数值预测是不同的可观察表现。不能仅凭流畅的局限性陈述判断预测已校准。

## 5. K2 提出的下一实验，保留为后测之后的判断

11/15 场在 K2 选择极稀实验：Opaque 5/5、Aligned 3/5、MisIndexed 3/5。另外四场分别选择等浓度放大、原资料附近的同容器稀释、同状态跨仪器比较和复测异常批次。这些都是假设性建议，没有执行，也没有获得盲测真值反馈。K2 已经看过 Q 的条件，因此不能把这些建议写成研究过程中主动发现并验证了关键实验，更不能说追加实验已修复错误。

| 来源 | K2 所选下一实验（未执行） |
|---|---|
| W01/Opaque | 极稀条件 |
| W01/Aligned | 极稀条件 |
| W01/MisIndexed | 极稀条件 |
| W02/Opaque | 极稀条件 |
| W02/Aligned | 极稀条件 |
| W02/MisIndexed | 极稀条件 |
| W03/Opaque | 极稀条件 |
| W03/Aligned | 等浓度放大 |
| W03/MisIndexed | 极稀条件 |
| W04/Opaque | 极稀条件 |
| W04/Aligned | 原资料附近的同容器稀释 |
| W04/MisIndexed | 同状态跨仪器比较 |
| W05/Opaque | 极稀条件 |
| W05/Aligned | 极稀条件 |
| W05/MisIndexed | 复测已有异常批次 |

## 6. 对主故事的推进与边界

可以写：在完整自主研究中，agent 形成了能描述已测平台的有效关系；跨越已测区间时，公开表达的外推规则与预测可靠性发生分化。不同先验条件影响整个研究过程，包含取证和解释；这里不要求先分离两条路径。原始操作、K1 和同上下文 Q 一起构成证据，K2 单独标为回顾。

不能写：所有有先验会话都被锚定；更广探索必然更好；Opaque 已在实验中观测到稀释转折；K1 已经包含 Q 的全部推理；K2 建议就是原实验计划；从这批记录已定位出内部认知原因。

本分析到此收束，不自动触发新实验或恢复剩余 28 次固定记录读出。本报告供稿件整合使用，未改写英文主文或重导出 PDF。

## 附：逐场阶段证据入口

以下列出原文件与 K1 原文摘录；全部 Q 原解释、K2 对应完整段落及计算分母在机器摘要中。

### EQ-W01--Opaque

[原报告](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W01--Opaque/EXPERIMENT_REPORT.md) · [结果](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W01--Opaque/RESULT.json) · [逐步 IO](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W01--Opaque/trajectory.jsonl)

> Applying this transformation separately to the 12 final assays gives apparent K_a values from approximately 1.80×10^−5 to 2.69×10^−5, with a mean of 2.16×10^−5 and an apparent pK_a of about 4.66.

> C_active ≈ C_cap ≈ 0.004 mol/L

> - The molecular identity of the acid-active species or precipitated material.
> - Whether precipitate actually formed, its amount, or its composition.
> - Whether the inferred active concentration is a solubility limit, buffer capacity, complexation limit, or calibration artifact.
> - Independent kinetic or equilibration timescales, because no waits or time series were performed.
> - Temperature dependence, pressure dependence, catalyst effects, or solvent effects.
> - Behavior below 0.050 mol/L nominal loading, where a saturation or buffering plateau might end.
> - Behavior above 1.000 mol/L or outside 0.040–0.080 L.
> - Exact separation of total-loading and volume effects beyond the single matched-concentration pair.
> - Whether repeated batches at one condition would reproduce the small observed differences.


### EQ-W01--Aligned

[原报告](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W01--Aligned/EXPERIMENT_REPORT.md) · [结果](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W01--Aligned/RESULT.json) · [逐步 IO](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W01--Aligned/trajectory.jsonl)

> The causal interpretation of g is not identified. It may represent buffering, coupled dissolution/precipitation, ionic-strength-dependent activities, or an environment-specific latent constraint. This model is intended for interpolation inside the sampled water-only domain, not extrapolation to zero loading, extreme dilution, concentrations above 1 mol L^-1, other solvents, temperatures, or times.


### EQ-W01--MisIndexed

[原报告](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W01--MisIndexed/EXPERIMENT_REPORT.md) · [结果](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W01--MisIndexed/RESULT.json) · [逐步 IO](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W01--MisIndexed/trajectory.jsonl)

> The empirical equations and pKa_eff estimate are supported only for water, nominal C_T = 0.0185–2.0 mol L^-1, reagent amounts 0.001–0.040 mol, volumes 0.018–0.080 L, and the near-ambient conditions actually used. They should not be extrapolated to zero loading, beyond 2 mol L^-1, other solvents, added catalysts, altered temperature, long equilibration times, or different pressure. In particular, the weak fitted precipitation slope must not be used to assert absence of a threshold outside this interval.


### EQ-W02--Opaque

[原报告](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W02--Opaque/EXPERIMENT_REPORT.md) · [结果](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W02--Opaque/RESULT.json) · [逐步 IO](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W02--Opaque/trajectory.jsonl)

> The present data favor a pH-coupled description over a concentration-only dissociation law, but they do not discriminate among explanations 1–4. Likewise, they do not establish whether the small variations in P are chemical or instrumental.

> **Unsupported extrapolation:** predictions at substantially different concentration, dilution, temperature, solvent, residence time, or added catalyst/base/acid are not justified. In particular, no claim is made that pKa_eff remains constant outside this narrow slice or that precipitation remains flat beyond 0.40 mol/L.


### EQ-W02--Aligned

[原报告](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W02--Aligned/EXPERIMENT_REPORT.md) · [结果](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W02--Aligned/RESULT.json) · [逐步 IO](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W02--Aligned/trajectory.jsonl)

> Using each final assay's pH and acid fraction gives apparent pKa_eff values from approximately 4.770 to 4.975, with a mean of 4.837. This is close to the supplied archival interval of 4.789–4.889. Eleven of the twelve estimates are close to that narrow neighborhood; the principal high-side values are from batches 8 and 12. I therefore retain an effective pKa near 4.84 as a useful descriptive relationship within this world.

> Interpolation inside the tested box should favor the pKa-coupled, weak-concentration-response model. I would not extrapolate the flat response to zero loading, to concentrations above 1.667 mol L^-1, to other solvents, or to materially different temperatures. A precipitation threshold, buffer exhaustion, second dissociation, activity-coefficient change, or phase transition could appear immediately outside the observed range.


### EQ-W02--MisIndexed

[原报告](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W02--MisIndexed/EXPERIMENT_REPORT.md) · [结果](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W02--MisIndexed/RESULT.json) · [逐步 IO](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W02--MisIndexed/trajectory.jsonl)

> I would not extrapolate this model to concentrations outside the tested range, other solvents, catalysts, changed temperature, long aging times, or named real chemical systems. In particular, the flat precipitation response does not rule out a threshold just outside the tested range.


### EQ-W03--Opaque

[原报告](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W03--Opaque/EXPERIMENT_REPORT.md) · [结果](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W03--Opaque/RESULT.json) · [逐步 IO](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W03--Opaque/trajectory.jsonl)

> The clearest discriminating future tests—stated only as predictions, not performed here—would be exact recipe replicates; controlled acid/base titration at fixed C_T; extension to much lower C_T; independent quantification of dissolved and solid material; and perturbation of background ionic composition. An isolated weak-acid model predicts substantial pH and α changes upon large dilution, whereas the favored clamped-background model predicts continued near-constant pH until buffer capacity or the latent setpoint regime is exceeded.


### EQ-W03--Aligned

[原报告](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W03--Aligned/EXPERIMENT_REPORT.md) · [结果](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W03--Aligned/RESULT.json) · [逐步 IO](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W03--Aligned/trajectory.jsonl)

> My interpretation is therefore that the archival dilution relationship is retained as a useful local effective relationship. It was not rejected or substantially revised. It should not, however, be extrapolated far beyond the 0.001 mol, 0.018-0.054 L neighborhood on the strength of a single paired contrast.


### EQ-W03--MisIndexed

[原报告](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W03--MisIndexed/EXPERIMENT_REPORT.md) · [结果](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W03--MisIndexed/RESULT.json) · [逐步 IO](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W03--MisIndexed/trajectory.jsonl)

> I would not extrapolate the constant-response model outside the tested range, to nonaqueous solvents, to different temperatures, or to other material identities. In particular, a true transition may exist below 0.0185 M or above 2.0 M, and the present experiments would not reveal it.


### EQ-W04--Opaque

[原报告](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W04--Opaque/EXPERIMENT_REPORT.md) · [结果](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W04--Opaque/RESULT.json) · [逐步 IO](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W04--Opaque/trajectory.jsonl)

> The most plausible microscopic story is a buffered proton reservoir coupled to a weak acid with effective pK_a near 5.2, plus either a precipitation reporter baseline or a solubility-buffered species. A precipitation-controlled proton reservoir is an attractive unified explanation, but the present measurements cannot distinguish it from independent pH buffering plus an unrelated proxy baseline. Claims outside the tested concentration, volume, solvent, temperature, and timing ranges would be extrapolations and are not warranted by these observations.


### EQ-W04--Aligned

[原报告](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W04--Aligned/EXPERIMENT_REPORT.md) · [结果](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W04--Aligned/RESULT.json) · [逐步 IO](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W04--Aligned/trajectory.jsonl)

> The final assays declared one-measurement standard deviations of 0.002 for normalized pH, 0.006 for alpha, 0.006 for precipitation signal, and 0.004 for equilibrium residual. The empirical scatter is consistent with small effects being difficult to resolve. Regression forms above are descriptive interpolation summaries, not validated structural laws, and should not be extrapolated beyond the tested domain.


### EQ-W04--MisIndexed

[原报告](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W04--MisIndexed/EXPERIMENT_REPORT.md) · [结果](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W04--MisIndexed/RESULT.json) · [逐步 IO](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W04--MisIndexed/trajectory.jsonl)

> The best current interpretation is a regulated or saturated latent aqueous state combined with a potentially important instrument/stage indexing layer. Buffering, precipitation-mediated clamping, nonideal activity, preparation history, and readout mis-indexing remain observationally equivalent to varying degrees. The data justify the empirical plateau model for interpolation, but they do not uniquely identify the underlying chemical mechanism.


### EQ-W05--Opaque

[原报告](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W05--Opaque/EXPERIMENT_REPORT.md) · [结果](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W05--Opaque/RESULT.json) · [逐步 IO](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W05--Opaque/trajectory.jsonl)

> The conclusions apply only to water, approximately ambient temperature near 297 K, anonymous reagent loadings 0.004-0.040 mol, nominal final volumes 0.030-0.090 L, and nominal final concentrations 0.0444-1.333 mol/L under the tested operation sequence. They should not be extrapolated to other solvents, catalysts, temperatures, ionic backgrounds, much lower concentration, or long equilibration times.


### EQ-W05--Aligned

[原报告](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W05--Aligned/EXPERIMENT_REPORT.md) · [结果](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W05--Aligned/RESULT.json) · [逐步 IO](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W05--Aligned/trajectory.jsonl)

> These are supported-range predictions rather than universal laws. A proportional change of reagent amount and volume that preserves L should produce little change beyond instrumental scatter. Dilution at fixed amount may produce a small increase in pH and alpha, but its magnitude is not securely estimated here. Extrapolations to other solvents, temperatures, catalysts, extreme dilution, or stronger concentration are speculative and should not be inferred from this campaign.


### EQ-W05--MisIndexed

[原报告](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W05--MisIndexed/EXPERIMENT_REPORT.md) · [结果](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W05--MisIndexed/RESULT.json) · [逐步 IO](../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/EQ-W05--MisIndexed/trajectory.jsonl)

> This says that dilution raises pH slightly, but the fitted change is small relative to batch-level variation. It is an empirical interpolation, not a chemical law and not justified outside 0.0185-0.833 M.


复算（不调用模型或模拟器）：

```powershell
uv run --no-sync python -m scripts.analyze_work_ii_eq_autonomous_process
```
