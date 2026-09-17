# EC qualification v1.0.2 — structural platform recovery 1

状态：**FROZEN PLATFORM RECOVERY；科学合同不变。**

## 1. 触发原因

第一次 structural attempt 写入：

`runs/development/experiment-1-ec-v1.0.2-6069d66/structural/`

`EC-W01` 的 18/18 次物理执行已经完成，但分析阶段在 legacy
`_model_qualification` 中抛出：

```text
ValueError: max() iterable argument is empty
```

原因是 v1.0.2 已冻结的 noisy-validation groups 为
`(0,0)/(0,1)/(0,2)`，legacy analyzer 却硬编码要求 validation 中存在中心点
`(1,1)`，用于计算 prior-model baseline match。该错误发生在 gate 计算之前，属于
analyzer implementation failure，不是任何 Q1–Q8 科学失败。

## 2. 唯一允许的修复

在 v1.0.2 独立 adapter 中计算相同的 baseline-match 语义：

- 两个模型仍在冻结中心点 `(1,1)` 对齐；
- 对齐后直接比较两个 model prediction；
- 要求绝对差 `<= 1e-12`；
- 不再要求 `(1,1)` 同时是 noisy-validation group。

原算法在 validation 包含 `(1,1)` 时比较两个模型相对同一 observed value 的绝对误差；
两模型在中心点预测相同，因此直接 prediction comparison 是更直接、等价的 prior baseline
symmetry check，不引入新证据、不改变阈值。

## 3. 不变量

以下项目全部保持 v1.0.2 冻结值：

- 五个 World 及 seeds；
- private truth；
- main 3×3 grid；
- noisy-validation groups `(0,0)/(0,1)/(0,2)` 与三次 repeats；
- effect floor `0.03`、noise multiplier `6.0`、minimum disagreement fraction `0.4`；
- Q1–Q8 gate 名称与含义；
- Participant budget；
- 90 次 scientific denominator；
- provider call count `0`；
- Participant 与 formal benchmark 均未授权。

## 4. Recovery boundary

- 第一次 attempt 永久保留为 platform-failed evidence，不进入科学 denominator；
- 修复必须先通过 unit test，并用第一次 attempt 的 W01 rows 作只读 diagnostic；
- 正式 recovery 从 `EC-W01`、execution 0 开始，在新的 write-once root 完整重跑 90 次；
- 不复用第一次 attempt 的 18 次执行作为 qualification result。

第一次 W01 rows 的只读 diagnostic 在修复后得到全部 model checks 通过，仅证明 analyzer
可处理冻结设计，不构成 qualification 结果。
