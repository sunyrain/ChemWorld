# 旗舰实验：设计、证据与冻结状态

> **旗舰实验不是“环境能运行”的同义词。它们是具有明确对照、盲化、统计单位和失效边界的确认性评测。**

## 两种容易混淆的“旗舰”

网站首页展示四个 **research showcase worlds**：分配发现、反应–结晶、反应–蒸馏和流动反应优化。
它们用于解释 ChemWorld 覆盖的实验推理类型。

当前进入机制适应正式协议的 **flagship execution tasks** 只有两个：

| 正式任务 | 主要隐藏变化 | 诊断观测 |
| --- | --- | --- |
| Reaction to Crystallization | 反应 rate-law、网络 topology、催化剂映射 | HPLC、终检与任务分数 |
| Electrochemical Conversion | 构成律、solvent 映射、electrolyte 映射 | UV-Vis、终检与任务分数 |

因此，首页出现某个世界不代表该世界已经完成在线变化识别确证。反过来，电化学虽然不是首页四张展示卡
之一，却是当前机制适应协议的正式执行任务。

## 当前冻结状态

| 层级 | 回答的问题 | 当前状态 |
| --- | --- | --- |
| 旗舰语义审计 | 对照、分母、盲化、cohort 与阈值是否自洽 | RC23，18/18 通过 |
| A1 物理有效性 | 隐藏干预是否真实、单轴且可观测 | RC23，81/81 设计检查通过 |
| A2 受控可识别性 | 信息充分时，候选机制是否可区分 | 新 cohort 待执行 |
| A3 在线变化识别 | Agent/策略能否先建参照，再检测并归因变化 | 新 cohort 待执行 |
| Gate B 变化检测 | 误报、召回、校准与检测延迟是否达标 | 待正式结果 |
| Gate C 反馈因果性 | 反馈是否改变行为并改善结果 | 待正式 provider 矩阵 |
| Gate D 恢复 | 收益是否来自适应而非世界本身更容易 | 待正式结果 |
| Gate E 自治性 | 科学决策质量与流程自治是否同时成立 | 待正式结果 |

当前 `publication_ready=false`。设计审计通过不能替代 A2/A3，更不能证明某个完整 Agent 已经通过。

## A3 的正确时间语义

正式支持为：

```text
truth change time ∈ {never, 6, 8, 10}
total horizon = 18
```

`τ=6` 被唯一解释为：前六个完整实验使用旧世界，第七个实验开始才可能使用新世界。`never` 是一等
真值状态；评估器可以为配对和计分设置伪 checkpoint，但隐藏规律始终不变。

策略只知道总 horizon，以及世界可能保持不变或在未指定时刻改变。以下信息不会进入 Agent 上下文：

- 最少稳定前缀长度；
- changepoint 候选集合；
- 是否已经通过 reference certificate；
- evaluator pseudo-checkpoint；
- 当前是否处于 post-change checkpoint。

## 旧世界参照不是动作清单

Reference certificate 由两个独立部分组成：

1. **结构充分性**：六动作设计、rate-law 的 low/pivot/high 关系、topology 关系，以及材料映射关系均
   被同背景实验覆盖。
2. **预测充分性**：开发 cohort 上拟合的旧世界预测模型，必须在 A3 cohort 的 held-out pre-change
   公共观测上满足冻结的标准化预测误差阈值；参考还必须足够新鲜。

要求对所有候选变化家族通用，不能在看到真值以后选择 family-specific 准入规则。

## 条件能力与端到端能力同时报告

令：

- `R`：成功建立合格旧世界参照；
- `D`：在冻结阈值下正确判断是否变化；
- `A`：变化家族归因正确。

正式报告同时给出：

```text
P(R)
P(D | R)
P(A | D, R)
P(R ∧ D ∧ A)
```

Reference acquisition failure 不进入条件归因率的分母，但仍作为失败保留在端到端成功率中。这样不会
出现“只在少量成功建立参照的 campaign 上看起来很准”的选择性报告。

## 运行前已冻结的 A3 标准

主要标准包括：

- reference acquisition rate 的 95% Wilson 下界不低于 0.80；
- changed detection recall 的 95% 世界种子聚类 bootstrap 下界不低于 0.80；
- no-change false-positive rate 的 95% 世界种子聚类 bootstrap 上界不高于 0.10；
- change-detection AUROC 的世界种子聚类 bootstrap 下界不低于 0.80；
- change-probability Brier score 不高于 0.20；
- `P(A | D,R)` 的世界种子聚类 bootstrap 下界不低于 0.80；
- 端到端成功率的世界种子聚类 bootstrap 下界不低于 0.70。

这些阈值在查看 A2/A3 结果前冻结。Development、A2、A3 与 private confirmation 使用四个互不重叠的
seed namespace。

## 其它旗舰实验是否有同类问题

统一语义审计覆盖完整能力链：

| 实验 | 已冻结的关键控制 |
| --- | --- |
| Gate 0 完整性 | 私有 split、prompt/response hash、三层 outcome、泄漏与回放检查 |
| Gate B 检测 | changed/no-change 配对、FPR、AUROC、Brier、检测延迟 |
| Gate C 反馈 | 局部测试使用完全相同历史前缀，只替换最后反馈；完整 campaign 配对 world/state/prompt |
| Gate D 恢复 | old-policy open-loop、frozen no-update、adaptive 与 diagnosis oracle 分开 |
| Gate E 自治 | autonomous score 与 assisted scientific score 强制同时报告 |

这次复核没有发现 Gate C–E 存在与旧 A3 相同的基础语义错误。它们仍是**设计已冻结、经验结果待执行**，
而不是已经通过。

## 可审计入口

- 协议：`configs/benchmark/mechanism_adaptation_v0.3.0.json`
- Gate A 计划：`configs/benchmark/mechanism_adaptation_gate_a_v0.3.0.json`
- 诊断关系图：`mechanism-adaptation-diagnostic-relation-graph-v0.3.0-rc23.json`
- 统一语义审计：`flagship-experiment-semantics-audit-rc23.json`
- 当前状态真源：`configs/current.json`
