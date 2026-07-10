# 闭环发现测试

本页记录 2026-07-10 的可复现实验。它回答两个问题：经典主动学习在同一冻结任务上是否真的
利用了后续实验机会，以及 DeepSeek V4 Pro 是否能读取公开谱图并据此进行多轮实验修正。

!!! important "结论边界"
    这里的“发现”是对 ChemWorld 隐藏参数面的 benchmark-local 发现，不是新反应、新催化剂或
    现实实验结论。任务中的催化剂和反应物仍是匿名对象。

## 经典算法：80 次完整运行

测试包含 8 个算法、2 个 72-step campaign 任务、每个组合 5 个 seed，共 80 次运行。所有运行
非法动作数均为 0。

### 标准反应优化

| 算法 | 5-seed 平均最佳分数 | 标准差 | 平均 total score | 平均 best-score AUC |
| --- | ---: | ---: | ---: | ---: |
| GP + Expected Improvement | 0.4251 | 0.0871 | 0.3812 | 0.2770 |
| Safety GP + constrained EI | 0.3950 | 0.0690 | 0.3528 | 0.2546 |
| Greedy local | 0.3846 | 0.0676 | 0.3432 | 0.2468 |
| GP + Upper Confidence Bound | 0.3796 | 0.0753 | 0.3448 | 0.2695 |
| Random Forest + EI | 0.3635 | 0.0612 | 0.3266 | 0.2469 |
| GP + Probability of Improvement | 0.3257 | 0.0589 | 0.2951 | 0.2318 |
| Latin hypercube | 0.3058 | 0.0431 | 0.2756 | 0.2143 |
| Random recipe | 0.2883 | 0.0943 | 0.2635 | 0.2214 |

GP-EI 在本组 seed 上取得最高均值；GP-UCB 的最终最佳值较低，但 AUC 接近 GP-EI，说明它更早
获得有效条件。单个 seed 的排名仍有波动，因此不应以一次运行宣布算法胜负。

### 安全约束反应优化

下表的违规数是每个算法 5 次运行、共 360 个操作中的总数。

| 算法 | 平均最佳分数 | 平均 safety-aware score | 安全违规 | 平均风险 |
| --- | ---: | ---: | ---: | ---: |
| Greedy local | 0.2391 | 0.0448 | 42 | 0.1982 |
| Safety GP + constrained EI | 0.2031 | 0.0365 | 24 | 0.1851 |
| GP + Probability of Improvement | 0.2337 | 0.0310 | **21** | 0.1990 |
| GP + Upper Confidence Bound | 0.2059 | 0.0287 | 36 | **0.1833** |
| Random Forest + EI | 0.2089 | 0.0276 | 39 | 0.2062 |
| Random recipe | 0.2238 | 0.0000 | 51 | — |
| Latin hypercube | 0.2084 | 0.0000 | 39 | — |
| GP + Expected Improvement | 0.2000 | 0.0000 | 27 | — |

这里没有单一“安全冠军”：Greedy local 的安全感知得分最高，但违规较多；GP-PI 违规最少；
GP-UCB 平均风险最低；Safety GP 在得分、风险和违规之间提供了较均衡的折中。后续正式比较应扩大
seed 数，并把置信区间和 Pareto 前沿作为主要结论。

## DeepSeek V4 Pro 多轮发现

配置为 `deepseek-v4-pro`、thinking 开启、`reasoning_effort=max`，在
`reaction-to-assay` 上使用 2× 扩展预算和连续 experiment campaign。36 步内完成 5 次合法
final assay，0 个非法动作，结果经轨迹回放验证。

| 实验 | 主要条件变化 | final assay |
| --- | --- | ---: |
| 0 | Ethanol、Catalyst A 0.001 mol；350 K 后再升至 370 K | 0.4136 |
| 1 | 改用 Catalyst B；实际仅执行 350 K 单段加热 | 0.3541 |
| 2 | 回到 Catalyst A；改为 360 K、1800 s 单段加热 | 0.4964 |
| 3 | 在实验 2 基础上把时间增至 3600 s | 0.4529 |
| 4 | 在实验 2 基础上把 Catalyst A 增至 0.0015 mol | **0.5321** |

实验 2→3 和 2→4 是清晰的单因素检验：延长时间使分数下降，提高匿名 Catalyst A 的用量则进一步
提高分数。实验 1 的文字意图是只比较催化剂，但实际还改变了加热程序，因此不能把下降完全归因于
Catalyst B；报告保留这一偏差，而不把模型叙述当成实验事实。

新增的 trajectory-derived 实验设计审计对该历史轨迹给出：4 次历史比较中 3 次单因素变化、
1 次多因素变化，单因素比较率 75%。它自动识别实验 1 同时改变了 `catalyst_charge` 和
`thermal_program`，而不依赖模型自然语言解释。多因素变化本身适用于 BO 或因子设计；这里的问题是
模型将其叙述为单因素催化剂证据。

第一次 HPLC 的原始峰面积对应 target 约 88.9%、reactant 约 3.9%、byproduct 约 7.2%；模型记录为
约 89%、3.9%、7.1%，并正确读取 target 约 2.64 min、byproduct 约 3.22 min。说明谱图曲线和峰表
确实进入了下一轮决策，而不是仅在网页中装饰展示。

该运行使用 34 次模型调用和 642,566 tokens。与较早的 V4 Flash 扩展运行相比，最佳分数从
0.5221 提高到 0.5321；由于执行轮数和 runner 配置不完全相同，这只能视为工程观察，不能视为
受控模型基准。

## 失败案例与防护

另一条 equilibrium 试跑反复产生不属于公开动作 schema 的字段，最终没有形成完整评测。该失败
推动了两项防护：thinking 模式给予足够的输出预算，且连续三次修复后仍非法时停止决策循环；若已有
有效实验状态，runner 只执行合法收尾。未来若要进一步提高动作可靠性，优先方向是把每个 operation
变成严格工具 schema，而不是继续堆叠自然语言提示。

## 未指认谱图 Pilot

在相同任务、seed 0 和 36-step 扩展预算下，新增一次 V4 Pro/max `unassigned` 运行。模型只获得
原始曲线和无物种标签的峰中心/面积：

| 运行 | 最佳 research score | Total | 实验 | 调用 | Tokens | 条件差异审计 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| V4 Pro/max · unassigned | 0.4127 | 0.3250 | 4 | 34 | 616,275 | 3/3 单因素变化 |
| 较早 V4 Pro/max · assigned | 0.5321 | 0.4448 | 5 | 34 | 642,566 | 3 单因素、1 多因素 |
| GP-EI · raw | 0.3879 | 0.3506 | 6 | 0 | 0 | 5/5 多因素变化 |

这不是严格的 assignment 因果效应：两个 DeepSeek 运行在第一次看到谱图之前就选择了不同的初始
配方，且 API 随机性没有重复采样。因此当前只能说“去掉峰标签后表现下降，值得正式消融”，不能说
峰标签必然导致 0.1194 的分数差。

更重要的失败模式是：尽管峰表已经删除 assignment，模型仍把 2.64 min 峰称为 product、把
3.22 min 峰称为 byproduct。它可以结合公开 yield/selectivity/byproduct 指标作这种推断，但该标签
不是仪器包直接提供的证据。后续应要求模型区分 supplied assignment、inferred assignment 和
unknown，并单独评分归属依据。

## 如何复现

经典算法不需要 API key：

```powershell
python -m apps.task_lab.run_evaluation --agent gp_ucb `
  --tasks reaction-optimization-standard --max-steps 72
```

DeepSeek 扩展 campaign：

```powershell
python -m apps.task_lab.run_evaluation --tasks reaction-to-assay `
  --model deepseek-v4-pro --reasoning-effort max --mode adaptive `
  --max-steps 36 --budget-multiplier 2 --campaign-override `
  --spectrum-disclosure unassigned
```

扩展运行写入 `research_score`，不会进入冻结的 `official_score`。
