# Work II observation/measurement Q0：阶段分析

日期：2026-08-12

## 结论

A-O observation/measurement Q0 已通过全部 `12/12` controls，执行时间 `0.31 s`，没有
participant session 或 provider call。它确认现有观测层具备设计跨任务 observation-prior
实验所需的最小条件，但不构成 agent capability、模型排名或 formal A-O 结果。

## 主要结果

| Instrument | 高对比状态可识别 | 低信号显式退化 | replicate probe accuracy |
|---|---|---|---:|
| HPLC | yes | yes | 1.00 |
| GC | yes | yes | 1.00 |
| UV/Vis | no（符合预注册） | yes | 1.00 |
| IR | no（符合预注册） | yes | 0.75 |
| NMR | yes | yes | 1.00 |

Nearest-centroid accuracy 只是简单 public probe，不覆盖完整 identifiability 判据，因此 UV/Vis 的
`1.00` 不会推翻其在完整光谱门下的 non-identifiable 结论。

pH 高对比状态差为 `8.4 pH`，显著超过 `0.06 pH` LOQ；低对比状态差为 `0.014 pH`，低于
LOQ。assigned 与 unassigned conditions 的 raw-curve hash 完全一致，masked condition 不暴露
signal，三种条件的 non-spectral context 保持配对。public report 没有发现 forbidden evaluator
token。

历史 spectrum catalog 只暴露索引和成本，不包含 signal arrays；显式 retrieval 返回与原 packet
相同的 hash，unknown ID fail-closed，成功和失败都进入 ledger。

## 实验价值和边界

Q0 证明 observation contract 不是“所有仪器总能区分一切”的理想化接口：它同时包含可识别、
不可识别和低信号退化区域，也能在 assigned/unassigned/masked disclosure 下保持其他条件配对。
因此 A-O 可以研究 agent 是否能识别观测偏差、噪声与可观测性边界，而不是只把 instrument 当作
无误差 oracle。

Q0 尚未覆盖两个 task family 或五个 world，也没有构造 aligned/misspecified observation priors。
下一阶段先运行固定的 seed-0 screen：electrochemical controlled-current 与 crystallization seed-mass
各三个水平、每水平三个 keyed replicates，并以 evaluator truth 审计 bias。只有 seed 0 通过，才按
原设计扩展到 world seeds `0–4`。

