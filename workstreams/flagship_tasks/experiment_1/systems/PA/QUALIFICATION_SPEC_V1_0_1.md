# Experiment 1 PA qualification specification v1.0.1

状态：**FROZEN FOR PROVIDER-FREE DEVELOPMENT QUALIFICATION**

Participant：**未授权**

Formal benchmark：**未授权**

## 1. Scope and corrected observation contract

本版本冻结 `PA-W01..W05 × entity/parametric/structural` 的第一次 Experiment 1
continuous qualification。15 个 atomic units 独立判定，不要求全部通过。

共同任务为 `partition-discovery`。所有执行显式绑定
`partition-s0-extraction-efficiency-v3`，科学 endpoint 固定为**分相前、settle 后的第一条
HPLC**：`product_in_organic / product_in_aqueous / phase_ratio`。分相后的 HPLC 和 final assay
只用于轨迹闭合，不作为两相分配判别数据。

这项绑定修复了历史小范围 PA gate 的解释边界：默认 scoring contract 的同名通道不能被
直接当作已核定的两相数据，历史结果不进入本版本 denominator。

## 2. Five executable private Worlds

仓库审计显示：seeds `0..4` 的 PA 相关 domain parameters 都是相同的 `1.0/1.0/1.0`，
因此本版本不把五个 seed 冒充五个 World。五个 World 通过已经注册并可 replay 的
`partition.distribution-coefficient` 和 `partition.phase-volume-ratio` world axes 实例化：

| World | seed | executable intervention | runtime multiplier（约） | role |
| --- | ---: | --- | --- | --- |
| PA-W01 | 0 | none | coefficient 1.000; phase volume 1.000 | central reference |
| PA-W02 | 1 | distribution coefficient, extrapolation +0.75 | coefficient 1.522 | strong partition |
| PA-W03 | 2 | distribution coefficient, extrapolation −0.75 | coefficient 0.657 | weak partition |
| PA-W04 | 3 | phase-volume ratio, extrapolation +0.80 | phase volume 1.565 | organic-volume boundary |
| PA-W05 | 4 | coefficient +0.45 and phase volume −0.80 | coefficient 1.286; phase volume 0.639 | coupled boundary |

三个 prior loci 在同一 World 中必须共享相同 axis manifest 和 canonical truth hash。
parent constitutive family 均为 `linear_response`；`power_response` 只在 PA-S 中作为成对
可执行 child fork，prior Arm 不选择 physics。

guidance v0.3 中包含 mixed linear/power truth 和手写 `K*` 的表格是 authoring proposal，
不作为本次已实现 truth。未来如要将 mixed family 设为五个 benchmark Worlds，必须新版本、
重新冻结并重跑三个 loci。

## 3. PA-E — extractant dossier mapping

- target：四个匿名 extractant 的 marginal dossier/action mapping；
- aligned：当前 audited nominal partition dossier；
- misspecified：只交换 `X0 ↔ X3`，permutation `[3,1,2,0]`，solvent dossier 不变；
- anchors：solvent `S0` 与 `S2`；targets：extractant `X0` 与 `X3`；
- 每个条件三次独立 noise replicate；每 World 12 次，五 World 共 60 次；
- process：solvent 0.020 L、aqueous addition 0.015 L、extractant 0.019 L、
  900 s / 1200 rpm mix、900 s settle；
- aligned marginal product-distribution ordering 必须与公开两相 organic allocation ordering
  一致；至少一个 anchor 的 mean gap `>=0.05` 且 SNR `>=2`；
- Participant 最小反证预算为 `2 extractants × 2 anchors = 4` 个 unique experiments。

分类器只读取公开 marginal dossier 与公开 HPLC，不读取 hidden 4×4 pair table。

## 4. PA-P — reference effective partition strength `K*`

- reference pair：`S0 × X1`；
- `K*` 定义为 frozen five-point phase-ratio design 上，用公开 ideal allocation equation
  对 private noiseless runtime allocation 拟合得到的 effective coefficient；
- aligned：`K* ±10%`；
- misspecified：相同相对宽度，false-center factor 按 Worlds 固定为
  `[1.35, 0.70, 1.45, 0.65, 1.30]`；
- five-point design 覆盖 extractant 0.008–0.030 L 与 total aqueous 0.026–0.045 L；
- 每点三次 independent noise replicate；每 World 15 次，五 World 共 75 次；
- public fit 必须落在 aligned band 且不落在 false band；
- low/high ratio 两端都必须形成 `>=0.05` allocation counterexample；至少两个点 SNR `>=2`；
- Participant 最小反证预算为三个 phase ratios。

`K*` 是 reference effective response parameter，不等同于公开 raw pair table 或最优流程。

## 5. PA-S — linear vs power constitutive law

每个 World 在完整 `4 solvents × 4 extractants` pair design 上成对执行：

- parent：`linear_response`，exponent 1.0；
- child：registered `partition_power_response_stress_v1`，exponent 1.75；
- 每 pair 两个 laws，共 32 次；五 World 共 160 次；
- categorical/volume/process actions 和 HPLC noise 在 law pair 内完全相同；
- organic 与 aqueous 两个 endpoint 均需至少 8/16 pairs 达到 paired gap `>=0.09`；
- 公共 `log(product_in_organic/product_in_aqueous)` 的 cross-pair slope 必须偏离 1.0
  至少 0.20，用于排除只调整单一 coefficient multiplier 的 false-family refit；
- 预注册四个低/高 coefficient pairs 构成 Participant 四实验 falsification budget。

## 6. Common Q1–Q8 and stop rules

1. Q1：固定 denominator、distinct truth binding、outcome classification、exact replay；
2. Q2：V3 分相前两相 endpoint 公开、有限且 observed；
3. Q3：public contract 不变且无 private intervention/seed 泄漏；
4. Q4：A/M 除目标 mapping/band/family 外 schema、宽度与模板对称；
5. Q5：冻结 public evidence 可区分 aligned 与 misspecified；
6. Q6：预注册 Participant budget 内存在反证路径；
7. Q7：差异作用于 registered two-phase endpoint；
8. Q8：效应通过冻结 noise gate并 exact replay；structural 使用 paired noise。

Provider calls 固定为 0。Scientific failure 完成 denominator、保留并继续；platform failure
停止受影响 block，修复后从 unit 0 重跑并保留旧 attempt。同一 campaign 不因结果修改 World、
pair、ratio、threshold 或 gate。Participant 与 formal benchmark 始终未授权。
