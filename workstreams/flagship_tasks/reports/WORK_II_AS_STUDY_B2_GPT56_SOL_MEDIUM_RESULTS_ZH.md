# Work II A-S Study B2：phase-process matched evidence 结果

## 结论先行

B2 完成了 15/15 fresh two-turn sessions、30/30 provider turns、5/5 matched worlds，0 failures、0 participant 物理实验。直接给出预先验证可区分 linear 与 1.75-power response 的 phase-process evidence 后，misindexed 的平均 prediction update gain 高于 aligned，但世界方向混合；同时 misindexed 仍未在公开 summary 中恢复注册的 1.75 law。

- opaque/aligned/misindexed 的平均 gain 为 **0.2138/0.2017/0.2931**。
- 注册主对比为 **0.0915**，4/5 worlds 为正，exact one-sided sign-flip **p=0.062**，95% 描述区间 [0.0076, 0.1753]。
- misindexed 的 exact 1.75-law recovery 为 **0/5**；明确拒绝 supplied linear partition form 为 **0/5**；5/5 转向经验饱和/endpoint 模型。

因此 B2 没有支持一个单一的 seeking/updating 二分答案。更精确的收束是：**取得 law-level phase-process evidence 后，misindexed 数值预测确实能比 aligned 多更新一些，但这种优势不稳定，也没有转化为正确结构规律。** 纯 evidence-seeking bottleneck 与纯 stubborn belief updating 都过强；当前证据支持 acquisition、numerical revision 与 structural identification 三层分离。

## 1. 完整性与资源

- sessions：15/15；same thread：15/15；provider turns：30/30。
- pre/post scoring terms：360/360，即每阶段 15×24；全部一次完成，无 infrastructure predecessor、无 turn.failed。
- provider-free truth：80/80；participant 物理实验：0；正式 wall time：6.6 min。
- provider reported usage：input 539,172，cached input 63,488，output 56,964，reasoning output 40,550 tokens。

## 2. 三臂 prediction 更新

| Arm | pre error | post error | absolute gain | relative reduction |
|---|---:|---:|---:|---:|
| opaque | 0.2224 | 0.0086 | 0.2138 | 96.1% |
| aligned_nominal | 0.2102 | 0.0086 | 0.2017 | 95.8% |
| misindexed_nominal | 0.3013 | 0.0081 | 0.2931 | 97.3% |

三个 arms 的 post error 都降到约 0.005–0.010，说明 phase-process packet 足以驱动强烈的 endpoint calibration。主对比的正均值来自 misindexed 更大的可改善空间与三个位点的额外 gain，但两个 worlds 为负，不能升级为稳定选择性纠错。

| World seed | opaque gain | aligned gain | misindexed gain | primary contrast |
|---:|---:|---:|---:|---:|
| 110564668 | 0.1881 | 0.1938 | 0.3091 | 0.1153 |
| 241120479 | 0.2134 | 0.1646 | 0.2658 | 0.1011 |
| 527268922 | 0.2248 | 0.1929 | 0.3493 | 0.1564 |
| 650846081 | 0.2313 | 0.2102 | 0.3178 | 0.1075 |
| 946166808 | 0.2112 | 0.2468 | 0.2238 | -0.0230 |

## 3. Metric-level 结果

| Metric | aligned gain | misindexed gain | primary contrast | positive worlds |
|---|---:|---:|---:|---:|
| product_in_organic | 0.0677 | 0.1842 | 0.1165 | 4/5 |
| product_in_aqueous | 0.1723 | 0.3073 | 0.1351 | 4/5 |
| phase_ratio | 0.3651 | 0.3879 | 0.0228 | 3/5 |

三个注册 metric 都进入主分母；没有只依赖接近常数的 endpoint channel。即便如此，结构恢复仍未出现，说明问题已经不能再归因于原 Study B 的 fixed-process evidence 缺口。

## 4. 公开结构表述审计

| Arm | exact 1.75 law | power-compatible wording | explicit linear rejection | empirical saturation model |
|---|---:|---:|---:|---:|
| opaque | 0/5 | 0/5 | 0/5 | 1/5 |
| aligned_nominal | 0/5 | 0/5 | 0/5 | 3/5 |
| misindexed_nominal | 0/5 | 0/5 | 0/5 | 3/5 |

Aligned 也只有部分 worlds 使用 power-compatible 语言，且有 world 明确否定 supplied power model；misindexed 则 0/5 恢复 exact exponent。模型从证据中学到了低误差的局部映射，但没有把该映射压缩成注册的 constitutive law。

## 5. 对原 Study B 与 Paper 2 的处置

- 原 Study B 的 A-P electrochemical 15 sessions 不含 `world_interventions`，继续作为当前 evidence-seeking 证据。
- 原 Study B 的 A-S partition 15 sessions 读取了受 evaluator 缺陷影响的 truth source；该分支保留为历史平台缺陷记录，但退出当前科学结论。
- 本 B2 是当前 A-S matched-evidence 入口：它修复了 evidence-level mismatch，却得到 mixed predictive contrast 与 0/5 exact law recovery。
- Paper 2 因此不再写“只需更好的 evidence 即可恢复结构 law”，也不写“模型完全拒绝更新”。当前结论是 numerical correction 与 structural law formation 分离。

## 6. 解释边界

这是单一 GPT-5.6-sol / medium agent--tool 配置、五个 public worlds 的小样本机制 follow-up。它只与完全匹配的 DeepSeek B2 分母共同支持该 block 的跨配置复现，不支持 model superiority、private transfer 或普遍 LLM 主张；canary 不进入分析。结果不需要补跑或按方向筛选。
