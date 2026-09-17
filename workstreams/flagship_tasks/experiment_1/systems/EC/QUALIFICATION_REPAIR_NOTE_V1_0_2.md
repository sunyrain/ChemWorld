# Experiment 1 EC qualification repair note v1.0.2

状态：**已批准并冻结用于 v1.0.2 continuous development qualification；不授权 Participant。**

日期：2026-09-17。父协议为 `Experiment 1 EC qualification v1.0.1`。本 note 只处理 v1.0.1 已完成 qualification 中的四个科学失败单元：

- `EC-W01:entity`；
- `EC-W04:entity`；
- `EC-W01:structural`；
- `EC-W04:structural`。

本 note 不运行 Participant，不调用 provider，不改变 simulator physics，不降低 Gate，也不把旧 development evidence 重新标记为 PASS。

## 1. 问题

能否在保持 EC-W01..W05 private Worlds、任务、公开操作域、Participant 预算和 v1.0.1 科学阈值不变的条件下，修复：

1. Entity 错配实例在部分 World 的两-anchor 可辨识覆盖不足；
2. Structural noisy validation 固定在中电位，导致部分 World 的高电流侧 A/M 反证覆盖不足？

目标是产生一个新的、事前冻结的 v1.0.2 repair contract，并重新 qualification 受影响的完整 locus blocks。旧失败必须保留。

## 2. v1.0.1 诊断事实

### 2.1 Entity

统一 `E0 ↔ E2` transposition 下：

| World | 失败位置 | absolute separation | SNR | 失败 Gate |
| --- | --- | ---: | ---: | --- |
| EC-W01 | anchor 1 | 0.032703 | 3.751 | Q5 |
| EC-W04 | anchor 0 | 0.008602 | 1.187 | Q5、Q8 |

两个 World 均无 platform/physical failure，private mapping audit 通过，A/M schema 与文本模板对称。问题是被固定交换的材料对没有在两个预注册 anchor 上都产生足够公开 endpoint separation。

### 2.2 Structural

EC-W01 和 EC-W04 均有强、稳健的 high-current efficiency-loss topology：

| World | topology effect | frozen threshold | topology passed | A/M disagreement | high-side support |
| --- | ---: | ---: | --- | ---: | ---: |
| EC-W01 | 0.838658 | 0.097880 | yes | 2/9 | 0 |
| EC-W04 | 0.811844 | 0.089557 | yes | 2/9 | 0 |

因此失败不表示 World 没有 transport limitation。当前 noisy validation 只在中电位 `1.05 V` 扫低/中/高 current；在该切片上，低侧可反证，但 W01/W04 的高侧 A/M model difference 没有超过冻结的 effect/noise gate，导致 Q5 和 Q6 失败。

## 3. 不变项

v1.0.2 repair 必须保持：

- EC-W00 和 EC-W01..W05 的 world seeds、private truth 和 realized truth digests；
- `electrochemical-conversion` 任务、public-test split、材料 family、scoring contract；
- Opaque / Aligned / Misspecified 的可见性边界；
- Q1–Q8 的含义；
- Entity absolute separation `>= 0.05`、SNR `>= 2.0`；
- Structural effect `>= max(0.03, 6 × observed_sigma)`；
- Structural A/M held-out disagreement fraction `>= 0.40`；
- Structural 低侧和高侧都必须存在 counterexample；
- aligned blind error 小于 misspecified blind error；
- Participant 每个 locus 至多 4 个独特实验的反证预算；
- exact replay、零 provider calls、失败不平均抵消、禁止覆盖旧 attempt。

任何实现若改变 simulator、共同 World、公开 action contract、共同噪声政策或 Gate，均超出本 note；EC-P carry-forward 将自动失效。

## 4. Entity repair：冻结 world-balanced transposition schedule

### 4.1 Proposed intervention

用五个不同的、预注册两行交换替代所有 World 共用的 `E0 ↔ E2`。每个 World 仍只交换两条完整 dossier 行，不改字段、精度、语气、置信度或真实材料：

| World | transposition | machine permutation | 旧 evidence 上两 anchor 的 separation / SNR |
| --- | --- | --- | --- |
| EC-W01 | `E0 ↔ E3` | `[3, 1, 2, 0]` | `0.066692 / 3.294`; `0.080689 / 10.574` |
| EC-W02 | `E0 ↔ E2` | `[2, 1, 0, 3]` | `0.610318 / 47.650`; `0.128195 / 8.548` |
| EC-W03 | `E1 ↔ E3` | `[0, 3, 2, 1]` | `0.625006 / 58.908`; `0.173089 / 9.686` |
| EC-W04 | `E2 ↔ E3` | `[0, 1, 3, 2]` | `0.550430 / 90.851`; `0.130273 / 11.648` |
| EC-W05 | `E1 ↔ E2` | `[0, 2, 1, 3]` | `0.669828 / 79.897`; `0.085935 / 6.008` |

这五种 transposition 不重复；四个类别在五个 World 中分别被交换 2、2、3、3 次，避免一个类别或一种错误模式垄断 campaign。

### 4.2 Disclosure and anti-overfitting rule

该 schedule 是使用 v1.0.1 provider-free development evidence 提出的结果知情 redesign，必须透明披露；因此表中旧数值只能证明“值得冻结并重新测试”，不能计作 v1.0.2 qualification。

一旦 v1.0.2 manifest 冻结：

- 不得按新结果重新选择 pair；
- 两个 anchor recipes 保持不变；
- 每个 anchor × 四材料仍做三次独立 keyed-noise 重复；
- 使用新的 observation namespace；
- 五个 World 的 entity block 必须从 W01 开始全部重跑，即使 W02/W03/W05 在 v1.0.1 已通过。

新 qualification 仍要求被交换两材料在两个 anchor 上均达到 separation 和 SNR 门，并再次验证 realized truth 没有反转 aligned mapping。

## 5. Structural repair：把 noisy validation 固定到低电位切片

### 5.1 Proposed diagnostic coverage

保留现有结构假设 family、prior 文本语义、3×3 主网格和三个 current levels，只把 EC structural noisy-validation groups 从：

```text
(potential_index=1, current_index=0/1/2) = 1.05 V × 15/91/190 mA
```

改为：

```text
(potential_index=0, current_index=0/1/2) = 0.75 V × 15/91/190 mA
```

每个 validation point 仍做三次独立重复。该切片是所有五个 World 共用的固定公开设计，不做 per-world 查询选择。

### 5.2 Scientific justification

结构先验声称的是固定电位下，电流跨过中等区间后是否出现 transport/Faradaic efficiency 的非线性恶化。低电位切片仍直接检验同一个 mechanistic relation，同时在五个 World 的现有主网格模型中都提供低侧与高侧 A/M divergence。

使用旧主网格和旧 noise estimate 的只读预检显示，在 `0.75 V` 下五个 World 均预计有：

- 4/9 model-metric comparisons 超过原 effect/noise gate；
- disagreement fraction `4/9 = 0.444... >= 0.40`；
- low-current support = 2；
- high-current support = 2。

这只是 query-design diagnostic。新 noisy validation 尚未发生，aligned/misspecified blind error 和 Q8 必须由 v1.0.2 独立 evidence 决定，不能预先宣称 PASS。

### 5.3 Budgeted falsifiability

Participant 在同一个 `0.75 V` 下测试低/中/高 current 只需三个独特实验，小于冻结的四实验预算。Qualification 的完整 3×3 网格和重复不计入 Participant 预算。

结构 query set 是 block-level 共同设计，因此 W01–W05 的 structural block 必须全部重跑；不能只挑 W01/W04 重跑并与旧 W02/W03/W05 混成同一新 block。

## 6. Requalification scope and evidence composition

### 必须新跑

1. v1.0.2 EC-W00 canary；
2. Entity W01–W05：`5 × 2 anchors × 4 materials × 3 repeats = 120` 次计划执行；
3. Structural W01–W05：`5 × (9 main-grid + 9 noisy-validation) = 90` 次计划执行；
4. 上述 210 次正式 repair qualification execution 的 exact replay。

### 不自动重跑

EC-P parametric block 不在本次科学修复范围。它只能在以下兼容性审计全部通过时原样 carry forward：

- World seed 和每个 World 的 truth digest 与 v1.0.1 一致；
- simulator、task/public contract、parametric evaluator、fit/held-out grid、阈值和 noise policy 未改变；
- v1.0.1 parametric reports、summary 和 registry rows 的文件 hash/self-hash 均有效；
- 新实现没有改变 parametric 代码路径。

Carry-forward 不得复制或重新标记旧结果。v1.0.2 应输出一个 composite manifest，显式绑定：

- v1.0.1 的五条 parametric registry rows；
- v1.0.2 新生成的五条 entity rows；
- v1.0.2 新生成的五条 structural rows。

如果任一兼容性检查失败，EC-P 必须在最终 EC 决策前重跑，不能靠人工声明保留。

## 7. Stop rules

- W00 失败：停止，不启动 W01–W05；
- platform failure：停止受影响 block，修复后从该 block 第一个 World 重跑；
- scientific Gate failure：完成已冻结 block 分母并保留失败，不调 pair、不换 validation potential、不降阈值；
- 任一 entity/structural World 失败：对应 locus 仍为 `failed`；
- 只有 composite registry 中三个 locus 均为 5/5 `five_world_qualified`，EC 才可进入另行预注册的 Participant development；
- 本 note 和未来 manifest 本身都不自动授权 Participant。

## 8. Proposed machine artifacts（尚未创建）

本 note 已在 continuous campaign 启动时获得人工接受，下一步允许创建：

- `configs/benchmark/experiment_1_ec_qualification_repair_v1.0.2.json`；
- 新版本 repair evaluator/runner/summary adapter；
- path-sensitive carry-forward compatibility audit；
- `runs/development/experiment-1-ec-v1.0.2-repair-<commit>/`；
- 10-row repair delta registry、15-row composite registry 和人类可读结果。

manifest 必须在执行前冻结 repair mappings、query groups、noise namespaces、denominators、stop rules 和所有 source bindings。

## 9. 冻结决定

项目负责人在 2026-09-17 启动 continuous development qualification campaign，接受：

1. 接受五个 World 使用五种预注册、近似平衡的两行 transposition；
2. 接受 Structural noisy validation 从中电位统一移动到低电位，hypothesis family 与 Gate 不变；
3. 接受 entity/structural 各自五个 World 整块重跑，而不是只重跑四个失败单元；
4. 接受 EC-P 仅在机器兼容性审计通过时通过 composite manifest carry forward。

上述四项现已冻结。实现必须逐项编码进 v1.0.2 machine manifest；任何偏离都需要新版本 note，不能在运行中静默修改。
