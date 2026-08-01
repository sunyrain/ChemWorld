# G2 已知／未知／错配三臂资源设计实验

状态：离线、逐操作、精确回放的设计标定；不使用外部模型调用。

## 候选设计

| 设计 | batch | hard operations | 诊断上限 | 两阶段 | 生命周期 | 错配操纵 | 错配恢复 | 平均利用率 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| diagnostic-k6-one-stage | 6 | 42 | 6 | 否 | 通过 | 100% | 100% | 100% |

## 推荐

推荐设计：`diagnostic-k6-one-stage`。

选择原则不是最高单次分数，而是用最小资源同时证明：完整生命周期、正确信息的行为影响、错配信息的初始操纵，以及后期基于实验结果的纠错。

## 三臂定义

- 未知：只有匿名 action codes。
- 已知：正确匿名 nominal properties。
- 错配：Agent 不知情地交换 solvent-S1 与 solvent-S3 的整行属性；物理世界不变。

## 评价建议

主评价使用 paired-world best final score 与 operation-normalized incumbent AUC；同时把 first material choice、late material choice、lifecycle completion、invalid/resource rejection 和账本利用率作为共同必要的行为证据。只看最终最高分会遗漏错配先验是否真正影响过 Agent，也无法区分恢复与偶然命中。
