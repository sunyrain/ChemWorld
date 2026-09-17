# Experiment 1 PA-P parametric repair note v1.0.2

状态：**FROZEN BEFORE DEVELOPMENT REQUALIFICATION**  
父版本：PA v1.0.1；只失效并重跑 `PA-W01..W05 × parametric`。

## 问题与诊断

v1.0.1 的五个 Worlds 均通过 Q1–Q5、Q7、Q8；W01/W02/W04/W05 只因 Q6 失败。
失败来自把五点 qualification grid 的两个几何端点都强制当作三实验 Participant
反证设计：高有机相比例端进入分配饱和区，A/M allocation gap 被压缩到 0.05 以下。
这不是 private physics 缺陷，也不授权移动 false prior 或降低阈值。

## v1.0.2 唯一科学修改

保留五个 Worlds、K* truth oracle、A/M band、五点 qualification grid、0.05 gap、SNR 2、
三实验预算和所有 runtime/noise 语义。Participant 反证设计冻结为三个可合法选择的非饱和坐标：

```text
low_ratio + reference + mid_high_ratio
```

Q6 要求这三个坐标中至少两个同时满足 allocation gap `>=0.05` 和 SNR `>=2`。三个坐标覆盖
低、中、高三个不同相体积区域；不会用重复实验冒充 unique experiment。Q5 仍要求 public K*
fit 落在 aligned band 且不落在 misspecified band。

## Denominator、停止规则与输出

- 5 Worlds × 5 phase points × 3 keyed-noise replicates = 75 primary executions；
- 每次 primary execution 必须 tolerance-zero exact replay；
- 运行前冻结 contract 和新 noise namespace；
- scientific failure 完成全部五 Worlds 并保留；platform failure 从本 block unit 0 重跑；
- Participant/provider calls 固定为 0。

本修复不改变 PA-E、PA-S 或任何 World private truth，因此二者的 v1.0.1 development evidence
保持历史有效，但仍需后续独立 confirmation。
