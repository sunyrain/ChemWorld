# Scientific Adaptation 跨 Provider 实验审计与阶段评价

日期：2026-07-26

状态：`development-only; formal_result=false; benchmark_claim_allowed=false`

本报告统一审计以下两轮真实 provider 实验：

- DeepSeek r4 双任务 pilot：16 个 terminal cells；
- WellAU `gpt-5.6-sol` high pilot：8 个 terminal cells；
- 合计 24 个 terminal cells、192 个计划实验，其中 174 个完成；
- 不调用 provider，不修改原始 terminal receipts，只重放已经完成的物理实验前缀。

机器可读审计产物：

`runs/development/scientific_adaptation_r4_cross_provider_postrun_audit_20260726/report.json`

## 1. 总体判断

当前实验已经证明三件事：

1. experiment-level Scientific Adaptation runner、资源记账和失败落盘是可工作的；
2. changed/twin 设计确实制造了可观察的适应问题，尤其在 electrochemical task 上；
3. 当前模型有时能察觉异常，但“察觉变化、正确归因、选择有效实验、恢复性能”尚未形成稳定闭环。

当前实验没有证明：

- Stateful 优于 Direct；
- 某个 provider 优于另一个 provider；
- 模型通过了 O1-O5 中任何正式 Participant outcome；
- 当前描述性 0.5 阈值可以替代预注册的 change-detection estimand。

最关键的结果不是单纯的平均分下降，而是能力链条发生了解耦：

- 10 个完整 changed cells 中，只有 2 个最终 top-1 指向真实变化 family；
- 这 2 个正确归因 cells 的 post-minus-pre 平均分仍分别为 `-0.0845` 和 `-0.0774`；
- 仅有的 2 个 changed 性能改善 cells，又都没有正确识别变化；
- 因此“正确解释”目前没有稳定转化为“恢复”，“偶然恢复”也不能解释为科学适应成功。

## 2. 执行与资源结果

| 指标 | 结果 |
| --- | ---: |
| Terminal cells | 24 |
| Completed / method failure | 19 / 5 |
| 完成 / 计划实验 | 174 / 192 |
| 实验完成率 | 90.625% |
| Logical calls / provider attempts | 179 / 182 |
| Provider-reported tokens | 1,167,782 |
| 已知 billed cost | USD 0.4027606358 |
| 未知成本 cells | 8 个 WellAU cells |
| Infrastructure failures | 0 |

WellAU 的 354,357 tokens 有 provider usage 记录，但认证模型目录没有可核实定价，因此总成本不能伪造为一个合计 USD 数字。

所有 174 个成功决策的 prompt estimate 均在合同上限内：Direct 最大 `5,469 / 6,250`，Stateful 最大
`6,591 / 7,100`。失败响应的 prompt estimate 没有单独保留，但 runner 在 provider call 之前强制检查 cap，能发生响应校验失败本身说明该调用已经通过 pre-call cap。

## 3. 确定性物理重放

审计器从每个 receipt 的已验证 plan 重建 `ScientificExperimentPlan`，使用原始：

- task、world seed 和 experiment index；
- changed arm 的 world interventions；
- pair-stable observation seed；
- experiment-specific observation namespace；
- 完全相同的 recipe compiler 和机械 closeout。

结果：

| 重放指标 | 结果 |
| --- | ---: |
| Replayed receipts | 24 / 24 |
| Replayed experiments | 174 / 174 |
| Exact verified receipts | 24 / 24 |
| Result mismatch fields | 0 |
| Source receipt hashes matching run reports | 全部匹配 |

比较范围包括 plan、executed steps、measurement evidence、terminal summary、score、operation count、completed flag、
peak safety risk 和 experiment/evidence IDs。5 个 method-failure cells 只重放已经完成的前缀，不推测失败后的科学结果。

这将当前证据等级从“receipt 看起来完整”提高到了“全部已完成物理结果可以由 frozen context 确定性再生”。

## 4. Scaffold 工程表现

| Scaffold | Completed cells | 完成实验 | Calls | Tokens |
| --- | ---: | ---: | ---: | ---: |
| Direct | 11 / 12 | 94 / 96 | 95 | 522,486 |
| Stateful | 8 / 12 | 80 / 96 | 84 | 645,296 |

Stateful 总 tokens 比 Direct 高约 23.5%，但完成实验更少；按完成实验计，约为 `8,066` 对 `5,558` tokens，
高约 45%。Stateful 有 4/12 method failures，Direct 为 1/12。

这不是 Stateful 科学效果较差的因果估计，因为方法、模型和完成前缀并不构成正式可交换样本。但它足以支持一个工程判断：

> 当前自由文本 persistent scientific state 是显著的协议负担，尚未显示出与成本和失败风险相匹配的收益。

不建议直接放宽 2,800 字符上限。更合理的 r5 候选是将状态压缩为固定结构：belief vector、少量 evidence IDs、一个待判别关系、
一个受控变量集合和一个 varied variable； observation/interpretation 长文本继续留在公共 receipt，不重复抄入 Agent memory。

## 5. Task 差异

| Task | Completed cells | 完成实验 | Method failures | Tokens |
| --- | ---: | ---: | ---: | ---: |
| reaction-to-crystallization | 11 / 12 | 92 / 96 | 1 | 562,900 |
| electrochemical-conversion | 8 / 12 | 82 / 96 | 4 | 604,882 |

完整 changed cells 的描述性 post-minus-pre 均值：

- reaction-to-crystallization：`-0.0143`；
- electrochemical-conversion：`-0.0838`。

5 个 method failures 中 4 个发生在 electrochemical task。该任务同时有更长的 recipe/context、更多材料类候选、明显更差的 changed
性能恢复和更高的协议失败密度。下一轮小规模方法诊断应优先围绕 electrochemical task，而不是把两个任务简单平均后增加样本量。

## 6. 描述性科学结果

以下数字只用于 development diagnosis，不是预注册 outcome。

### Changed cells

- 完整 cells：10；
- 平均 post-minus-pre score：`-0.0490`；
- 性能改善：2/10；
- 最终 `P(no_change) < 0.5`：6/10；
- 最终 top-1 指向真实 family：2/10；
- 真实 family 最终平均概率：`0.2867`。

模型经常降低 no-change 信念，但通常把质量转移给错误的变化 family。变化察觉没有稳定转化为归因，也没有稳定转化为恢复。

### No-change twins

- 完整 cells：9；
- 平均 post-minus-pre score：`+0.0598`；
- 性能改善：6/9；
- 描述性 false positive，即最终 `P(no_change) < 0.5`：3/9；
- 将失败 cells 的最后可用 belief 计入后：6/12。

Twin 的正向分数变化说明单纯比较 pre/post score 不能定义 adaptation：没有世界变化时，模型也会因正常探索找到更好的 recipe。正式 O1/O3 必须依赖 paired contrast、校准和预注册 estimand，而不是“post 比 pre 高”。

## 7. 代表性样本

### 正确归因但没有恢复

DeepSeek Pro Direct，electrochemical changed：

- 真实 family：`constitutive_law_family`；
- 最终 belief：真实 family `0.35`，为 top-1；
- post-minus-pre score：`-0.0845`。

DeepSeek Pro Stateful，reaction changed：

- 真实 family：`rate_law_family`；
- 最终 belief：真实 family `0.88`；
- post-minus-pre score：`-0.0774`。

这两个样本说明归因正确仍不足以完成 recovery。模型可能没有把机制判断转译成有效的 recipe search direction。

### 有改善但没有识别变化

WellAU Codex Direct，reaction changed：

- post-minus-pre score：`+0.0166`；
- 最终 `P(no_change)=0.82`；
- 真实 rate-law family 概率仅 `0.13`。

DeepSeek Pro Direct，reaction changed：

- post-minus-pre score：`+0.0028`；
- 四个候选最终均为 `0.25`。

这两个样本只能称为性能改善，不能称为机制适应。

### 明显的 twin 假阳性

DeepSeek Pro Stateful，reaction no-change twin：

- 世界没有变化；
- post-minus-pre score：`+0.0617`；
- 最终 `P(rate_law_family)=0.90`，`P(no_change)=0.03`。

这是当前最清楚的“探索收益被错误解释为世界变化”样本。

## 8. Method failures 与诊断改进

| 失败类型 | Cells |
| --- | ---: |
| `scientific_state` 超过 2,800 JSON 字符 | 3 |
| `belief_update_rule` 超过 700 字符 | 1 |
| `varied_variable` 为空 | 1 |

其中 4/5 属于 Stateful，4/5 位于 electrochemical task。全部是 method contract failure，不是 provider infrastructure failure，
也不允许 scientific retry。

代码现已新增 `ScientificPlanValidationError`。未来 failure receipt 会只保存：

```json
{
  "field_path": "scientific_state",
  "constraint": "max_json_characters",
  "observed": 3124,
  "limit": 2800
}
```

不会保存失败字段正文、response、prompt 或 reasoning。既有真实 receipts 没有回写。

## 9. 架构简化结论

可以立即保留的最小核心：

1. 单一 public experiment context builder；
2. 单一 plan validator；
3. deterministic recipe compiler 和 mechanical closeout；
4. write-once terminal receipt；
5. 独立 postrun replay/audit，而不是在 runner 内继续堆叠分析逻辑。

建议在新 r5 合同中评估、而不是修改 r4 的部分：

1. 用固定字段状态替代自由文本 evidence summary；
2. memory 只引用 evidence ID，不重复观察正文；
3. 将“变化检测 belief”和“下一实验计划”分离验证，避免一处超长使整个决策报废；
4. 对 Direct 与 compact-stateful 做同 backend、同 task、同 pair 的资格实验；
5. 先在 electrochemical task 上验证协议可运行性，再扩展 provider matrix。

不建议继续保留或扩大：自动修复模型输出、校验失败后的科学重试、为过关而放宽状态长度、把描述性阈值包装成 O1。

## 10. 下一阶段

下一步应是一个新的 r5 development freeze，而不是覆盖 r4：

1. 定义 compact-stateful schema 和明确的长度预算；
2. 做 mock 资格与确定性 replay；
3. 在 electrochemical task 上做极小真实 provider A/B，Direct 对 compact-stateful；
4. 只有 contract failure 明显下降且 paired signal 有改善时，才进行多 seed power/cost audit；
5. 之后再冻结 participant preregistration，进入 formal/private 阶段。

在此之前，最稳妥的项目表述是：ChemWorld 已经具备可审计、可重放的科学适应实验基础设施，并观察到真实的检测、归因与恢复困难；但尚无证据支持 Stateful 优势、provider 优势或正式 Participant outcome 结论。
