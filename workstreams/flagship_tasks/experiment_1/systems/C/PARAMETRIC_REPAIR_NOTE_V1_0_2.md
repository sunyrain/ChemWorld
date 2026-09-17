# Experiment 1 C-P parametric repair note v1.0.2

状态：**FROZEN BEFORE DEVELOPMENT REQUALIFICATION**  
父版本：C v1.0.1；只失效并重跑 `C-W01..W05 × parametric`。

## 问题与诊断

v1.0.1 在全部 Worlds 中都观测到强、抗噪声且有行为后果的 cooling response；W01/W02/W05
仅因固定绝对 crystal-yield crossing `0.15` 不在 310/290/270 K 三点区间内而 Q5 失败。
与此同时 aligned prior center 由 solubility multiplier 的手写温度公式产生，并未对应实际可执行
PBM 的 crossing。这使 prior claim 和 discriminator 测量的对象不一致。

## v1.0.2 科学问题

参数 prior 改为同一固定 upstream/solvent/seed context 下的局部冷却响应幅度：

```text
ΔY40 = crystal_yield(270 K) - crystal_yield(310 K)
```

每个 World 的 aligned center 使用 v1.0.1 已完成 denominator 的 effect estimate 作为 authoring
calibration，数值在 v1.0.2 contract 中逐 World冻结；该旧 evidence 只用于 authoring，不进入
v1.0.2 denominator。Aligned 与 misspecified 使用相同相对半宽 15%；misspecified center 固定为
aligned center 的 45%，仍表示可信的弱 cooling response，而不是不科学的反向结晶。

Qualification 继续执行 310/290/270 K，每点三次新 keyed-noise replicate。Q5 要求新 observed
ΔY40 落入 aligned band、不落入 misspecified band，且两 prior center 的绝对间隔不低于 0.12。
Q6 仍为三个 unique batches；单次实验不能估计 ΔY40。Q7 要求 ΔY40 >= 0.20；Q8 要求端点
contrast SNR >= 2。

## Frozen authoring centers

| World | aligned ΔY40 center |
| --- | ---: |
| C-W01 | 0.5339489033 |
| C-W02 | 0.4382618864 |
| C-W03 | 0.6810095541 |
| C-W04 | 0.5522700926 |
| C-W05 | 0.3422120114 |

## Denominator 与边界

- 5 Worlds × 3 temperatures × 3 replicates = 45 primary executions + 45 exact replays；
- five Worlds、private truth、PBM、public contract、固定 context 和 scoring 不变；
- Participant/provider calls 为 0；
- 本版本不修 C-S；C-S 必须另行 v1.1 structural redesign。
