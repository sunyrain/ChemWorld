# ChemWorld 实验 1：35 个底层 World 的 Private Truth 设计（工作版 v0.3）

> **目标**：把上一版“10 个任务—导向单元 × 3 个先验层 × 5 个 world × 3 个 arms = 450 sessions”的研究设计，继续下沉到可以直接交给开发者实现的 **35 个底层物理世界**。
>
> 本文只负责 **world authoring / prior generation**，不定义下游评分指标。
>
> **重要边界**：本文中的经典化学体系是“科学锚点”，用于选择合理的机制 family、变量和参数范围；下面给出的数值是 **benchmark 内部的合成/校准参数**，不是对真实具名化学体系的定量复现，也不能作为真实实验常数引用。

---

# 0. 这版设计最终要得到什么

## 0.1 底层世界数量

只构建：

\[
7\ \text{体系}\times 5\ \text{worlds}=\boxed{35\ \text{private worlds}}
\]

每个 world 固定一套：

- 真实机制 family；
- 真实隐藏参数；
- 真实材料—性质映射；
- 初始状态；
- 仪器映射与噪声合同；
- 安全/资源参数；
- 可执行操作合同。

然后从同一个 world 派生不同实验会话。

## 0.2 450 sessions 如何从 35 worlds 展开

当前任务导向：

- 双重导向：电化学、反应—热安全、结晶，各有“发现 + 优化”两个任务；
- 发现导向：相平衡/分配；
- 优化导向：连续流、萃取/纯化、蒸馏。

因此共有 10 个“体系 × 导向”任务单元。

每个任务单元：

\[
3\ \text{先验层}\times5\ \text{worlds}\times3\ \text{arms}=45\ \text{sessions}
\]

总计：

\[
10\times45=\boxed{450\ \text{sessions}}
\]

**双重导向任务不新建 world**。例如 `EC-W03` 同时用于电化学发现任务和优化任务；真实物理完全相同，只改变公开任务目标。

---

# 1. 与当前 ChemWorld 仓库的关系

## 1.1 当前仓库已经提供的关键能力

最新版仓库已经具备以下基础：

- 反应、热过程、相行为、分离、结晶、蒸馏、连续流、电化学等可执行模块；
- hidden mechanism 可以包含 reaction network、rate-law family、partition law、crystallization、distillation、flow、电化学参数；
- world-specific hidden parameter seed 与 deterministic replay；
- 4 类有限材料候选是当前多个任务的成熟设计习惯；
- 电化学、反应/安全、分配、结晶、蒸馏已经存在不同程度的静态材料 dossier；
- `Opaque / nominal / misindexed` 材料资料接口已经存在；
- 当前 `domain_parameters` 已直接支持 partition、crystallization、distillation、flow、电化学若干倍率型世界变化；
- 当前 mechanism-family 层已经支持：
  - 反应 rate-law family；
  - reaction topology；
  - partition constitutive law；
  - electrochemical constitutive response；
  - equilibrium activity response。

## 1.2 本文新增的设计，不应假装已经全部实现

为了让 7 个体系都拥有“实体 / 参数 / 结构”三层扰动，本文提出若干**新增 authoring contract**：

1. 连续流需要独立的材料 dossier，以及“动力学控制 vs 热/传质边界控制”的结构 family；
2. 反应—萃取—纯化需要 extractant dossier 和组成耦合 partition family；
3. 结晶需要直接作用于结晶过程的 structural family，而不仅是上游 reaction topology；
4. 蒸馏需要显式的 `constant-relative-volatility` vs `activity-corrected VLE` 结构 fork，以及更适合蒸馏的材料 dossier；
5. 反应—热安全的现有 generic reaction dossier 建议增加高温稳定/失活相关字段。

这些都应该先在 development mode 实现和资格化，再进入正式 freeze。

---

# 2. 35 个 world 的共同 private-truth schema

建议每个底层 world 都编译成下面的统一逻辑对象。

```yaml
world_id: EC-W03
system_id: electrochemistry
scientific_anchor: quinone_hydroquinone_pcet
initial_state_profile: fixed-system-reference-v1

private_truth:
  mechanism_family: bounded_peak_decay
  mechanism_parameters: {...}
  material_family_id: ...
  material_realized_residuals: {...}
  observation_model: {...}
  safety_and_cost: {...}

public_contract:
  operations: [...]
  instruments: [...]
  legal_domains: {...}
  budgets: {...}

prior_generation:
  entity:
    target_field: electrolyte_profile
    nominal_dossier_id: ...
    misindex_permutation: [2, 0, 3, 1]
  parametric:
    target_parameter: effective_window_center_V
    scope: reference_material_pair_and_standard_charge
  structural:
    true_family: bounded_peak_decay
    false_family: monotonic_transport_plateau
```

### 硬规则

1. `private_truth` 不因 O/A/M 改变；
2. discovery/optimization 共用同一 `private_truth`；
3. 同 world 的 O/A/M 使用相同 public operation/instrument contract；
4. 同 world 的三个先验层之间，不要求能做因果横向比较；它们是三个不同的信息干预实验；
5. noise 建议使用 **keyed deterministic noise**：同一个 world、同一个合法实验坐标，在不同 arms 中返回配对噪声，而不是因为会话顺序不同产生不同随机扰动。

---

# 3. 五个 worlds 的统一构造原则

5 个 world 不能只是 `seed=0..4` 的无解释随机样本。建议每个体系都预先承担五种覆盖角色：

| World | 设计角色 | 目的 |
|---|---|---|
| W1 | 中央参考 world | 参数居中、可辨识性清楚，作为最容易解释的参照 |
| W2 | 参数偏移 world | mechanism family 不一定改变，但关键定量窗口明显移动 |
| W3 | 结构替代 world | 使用另一种真实 mechanism family，防止结构答案永远相同 |
| W4 | 强耦合/困难 world | 两个过程耦合更强，但仍必须可辨识 |
| W5 | 边界稳健 world | 位于较难操作区或低信号区，但不能低到不可识别 |

这五个角色是设计原则，不要求七个体系的数值形式完全一样。

## 3.1 什么应该跨 world 变化

优先改变：

- 私有机制 family（至少两个 family 在五个 world 中出现）；
- 关键 kinetic / equilibrium / transport 参数；
- 材料 world residual；
- 安全/成本中的少量 private nuisance parameters。

## 3.2 什么原则上不要跨 world 随意变化

第一版建议保持：

- public action schema；
- public instrument schema；
- 候选材料数量；
- 预算结构；
- 初始投料的名义量级；
- 任务目标定义；
- 评分方向。

这样 world shift 主要来自**真实规律变化**，而不是题面变化。

---

# 4. 三类 prior 的统一生成规则

# 4.1 实体层先验：统一采用 4 个候选 + 固定无固定点错配

每个体系实体层只选择 **一个主材料类别** 作为 target，避免同时错配多个对象导致解释困难。

默认候选数：

\[
\boxed{4\ \text{candidate materials}}
\]

统一错配置换：

```text
真实索引: 0  1  2  3
错配来源: 2  0  3  1
```

即：

```text
M0 ← profile(M2)
M1 ← profile(M0)
M2 ← profile(M3)
M3 ← profile(M1)
```

这是一个 derangement，没有任何材料保留自己的 profile。

### Opaque

只显示：

- `material-M0 ... material-M3`；
- 合法操作角色；
- 不提供目标性质 dossier。

### Aligned

显示 nominal dossier 的**正确索引关系**。

注意：Aligned 不显示 world-specific residual，因此它是“正确方向的有限先验”，不是 oracle truth。

### Misindexed

保持：

- 相同 4 条 profile；
- 相同字段；
- 相同有效位数；
- 相同描述长度和置信度；

只改变 `material_id ↔ profile` 映射。

## 4.1.1 nominal profile 与 realized truth 的关系

建议：

\[
p_{realized}=p_{nominal}\times r_{world}
\]

其中 `r_world` 是 campaign 内固定的隐藏 correlated residual。

第一版推荐把大多数 residual 控制在约 `0.85–1.15`，个别已经成熟的仓库 family 可保留现有 contract，但正式资格时必须确认：

- Aligned 仍然统计上是有用信息；
- residual 不应把 nominal ranking 完全随机化；
- Misindexed 不能因为 residual 偶然“错配成对”。

---

# 4.2 参数层先验：给近似参数区间，而不是精确 truth

对每个体系只选一个**主参数对象**，并明确适用范围。

例如：

> “在参考材料 M1、标准投料、标准几何和指定测量定义下，有效电位窗口中心约为 ……”

这样参数先验不会与实体材料差异混在一起。

### Aligned 生成

对于正值参数 `θ > 0`：

\[
A=[0.90\theta,\ 1.10\theta]
\]

对于温度中心：

\[
A=[T^*-5K,\ T^*+5K]
\]

对于电位中心：

\[
A=[V^*-0.05V,\ V^*+0.05V]
\]

### Misspecified 生成

使用与 Aligned 相同的区间宽度和文本格式，但中心系统性偏移。

五个 world 预注册交替偏移方向，避免“错误先验永远偏高”这种捷径：

| World | 正值参数 false-center 倍率 | 温度偏移 | 电位偏移 |
|---|---:|---:|---:|
| W1 | 1.35× | +25 K | +0.20 V |
| W2 | 0.70× | −25 K | −0.18 V |
| W3 | 1.45× | +30 K | +0.22 V |
| W4 | 0.65× | −30 K | −0.20 V |
| W5 | 1.30× | +20 K | +0.18 V |

如果 false-center 超出合法域，使用**关于合法域中点镜像**的预注册规则修正，而不是人工挑一个更“好”的错误值。

### Opaque

只给合法控制域和参数单位，不给局部估计。

---

# 4.3 结构层先验：给 family/topology，不给精确数值

### Aligned

给出真实 family 的简短机制陈述，但不包含 private numerical parameters。

### Misspecified

给出预注册的可信替代 family，要求：

- 同等级复杂度；
- 同样完整的语言；
- 同样数量的机制要点；
- 在实验域中可被证据推翻；
- 不是明显荒谬模型。

### Opaque

只说明：

> “当前体系的响应结构未知，请通过实验判断。”

不提供 family 标签。

---

# 5. 体系一：电化学转化（EC）

## 5.1 科学锚点

**对苯醌/氢醌型质子耦合电子转移（PCET）原型**。

正式 benchmark 仍使用匿名 `Ox / Red / solvent-Si / electrolyte-Ej`，不向 Agent 暴露具名真实反应。

当前 ChemWorld 已经具备较成熟的：Nernst、Butler–Volmer、传质极限、双电层、电阻、电荷/能量账和材料 dossier，因此这是 7 个体系中最接近直接落地的一类。

## 5.2 真实 mechanism family

注册两个结构 family：

### EC-S1：单调到传质平台

- 增加有效过电位提高目标通道；
- 最终受到 limiting current / ohmic loss 限制；
- 目标选择性在合法操作区内不出现明显下降。

### EC-S2：峰型选择性衰减

- 低驱动力不足；
- 中等过电位最优；
- 高过电位下副反应/界面竞争增强，选择性下降；
- 可同时受到传质与电阻限制。

结构层错配规则：`S1 ↔ S2`。

## 5.3 Private hidden parameters

核心 private 参数：

- `standard_potential_scale`：有效标准电位尺度；
- `exchange_current_scale`：交换电流密度倍率；
- `effective_resistance_scale`：欧姆/接触电阻倍率；
- `selectivity_decay_scale`：高过电位选择性衰减强度；
- `transfer_asymmetry_scale`：电荷转移非对称性；
- world-fixed cell geometry；
- electrolyte / solvent latent residuals。

参数层公开 target 不直接用这些 raw coefficients，而定义成更容易理解的：

> **参考材料组合下的有效最优电位窗口中心 `V*`**。

参考条件固定为：`solvent-S1 + electrolyte-E1 + standard charge`。

## 5.4 实体层 target：电解液配置

保持溶剂 dossier 不作为本轮 Entity 干预对象，主 target 固定为 4 个 `electrolyte-E0..E3`。

沿用当前仓库 `nominal-prior-latent-v2` 的核心字段：

1. 体相电导率；
2. 扩散系数；
3. 扩散层厚度；
4. 双电层电容；
5. 酸/质子活度相关信息；
6. 沉淀倾向（Ksp 相关）；
7. 标准电位偏移。

不公开：Faradaic efficiency、产品选择性、最优配方。

## 5.5 五个 EC worlds

| World | 真结构 | `V*` (V，参考条件) | E0 倍率 | j0 倍率 | 电阻倍率 | 选择性衰减倍率 | 转移非对称倍率 | 角色 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| EC-W1 | S1 平台型 | 0.90 | 0.92 | 1.25 | 0.85 | 1.10 | 0.95 | 中央参考 |
| EC-W2 | S2 峰型 | 1.05 | 1.00 | 0.90 | 1.00 | 2.00 | 1.05 | 参数偏移 |
| EC-W3 | S2 峰型 | 1.20 | 1.08 | 0.75 | 1.20 | 3.20 | 1.20 | 强副反应 |
| EC-W4 | S2 峰型 | 0.95 | 0.96 | 1.40 | 1.35 | 4.00 | 1.35 | 强耦合/高阻 |
| EC-W5 | S1 平台型 | 1.30 | 1.12 | 0.65 | 0.75 | 1.05 | 0.85 | 边界/传质主导 |

> 这些是 benchmark-scale 设计值；正式实现时 `V*` 应通过 provider-free truth sweep 由 private law 计算并冻结，而不是手写后再强迫 simulator 与之匹配。

## 5.6 三层先验生成

### Entity

- O：只给 E0–E3；
- A：正确 electrolyte nominal dossier；
- M：使用 `[2,0,3,1]` 错配。

### Parametric

target：参考条件的 `V*`。

- A：`V* ± 0.05 V`；
- M：按 W1–W5 预注册电位偏移生成相同宽度区间；
- O：只给合法电位域。

### Structural

- A：陈述当前是真实 `S1` 或 `S2`；
- M：陈述另一 family；
- O：不说明响应是平台还是峰型。

## 5.7 实现状态

**高**。当前代码已支持大部分参数、材料 prior 和 electrochemical constitutive stress。主要工作是把两个 structural family 的公共描述和 truth qualification 固定成正式合同。

---

# 6. 体系二：反应—热过程与安全（RS）

## 6.1 科学锚点

使用**乙酸酐水解/酸促进放热反应**作为过程安全科学锚点，但正式 world 仍使用匿名 `A → P / S` 网络。

这里不声称复制真实乙酸酐水解的全部动力学；锚点只是为了保持：

- 明显放热；
- 温度对速率强影响；
- “继续升温/延时”可能带来风险；
- 目标反应、竞争通道和催化/促进剂稳定性之间存在权衡。

## 6.2 真实 reaction skeleton

所有 5 world 共享：

```text
A  --kP(T,C)-->  P        目标路径
A  --kS(T,C)-->  S        竞争副反应
C  --kD(T)---->  C*       可选失活路径
```

两个结构 family：

### RS-S1：稳定促进剂

- `kD ≈ 0`；
- 目标/副反应都受 Arrhenius 控制；
- 主要挑战是温度—时间—选择性权衡。

### RS-S2：温度依赖失活

- 催化/促进剂存在显著失活；
- 高温虽然短期加速反应，但持续时间过长会降低后期有效速率并提高副反应/热风险。

结构错配：`S1 ↔ S2`。

## 6.3 Private hidden parameters

- `kP_ref_s-1`：参考温度下目标路径有效速率；
- `kS_ref_s-1`：参考温度下副反应速率；
- `Ea_P`, `Ea_S`；
- `k_deactivation_ref`；
- `ΔH_rxn`；
- `UA` / heat-loss strength；
- world-specific catalyst/solvent residual；
- safety response parameters。

参数层公开 target 定义为：

> **参考 Catalyst-C1 / Solvent-S1 / 标准投料下的推荐安全生产温度中心 `T*`**。

`T*` 由 truth sweep 计算，不等于某个单独 kinetic constant。

## 6.4 实体层 target：催化/促进剂

4 个 `catalyst-C0..C3`。

### 第一版建议 dossier 字段

1. 参考反应面板平均活性；
2. 目标选择性倾向；
3. 高温活性保持；
4. 失活抗性；
5. 热风险放大倾向。

当前仓库已有 `reference_panel_activity_geomean / floor / ceiling / variability`；后 3 个热安全字段属于建议新增，需要通过真实 private generator 派生，不能手工写成与 runtime 无关的装饰信息。

### 推荐 nominal profile（相对值）

| Catalyst | 活性 | 选择性 | 高温保持 | 失活抗性 | 热风险倾向 |
|---|---:|---:|---:|---:|---:|
| C0 | 1.25 | 0.90 | 0.70 | 0.75 | 1.15 |
| C1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| C2 | 0.85 | 1.20 | 1.20 | 1.25 | 0.90 |
| C3 | 1.15 | 1.10 | 0.85 | 0.90 | 1.05 |

没有一个 catalyst 在所有维度绝对占优。

## 6.5 五个 RS worlds

参考温度用于定义 `k_ref`：350 K。

| World | 真结构 | `T*` (K) | kP_ref (s⁻¹) | kS_ref (s⁻¹) | Ea_P (kJ/mol) | Ea_S (kJ/mol) | kD_ref (s⁻¹) | ΔH (kJ/mol) | UA (W/K) | 角色 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| RS-W1 | S1 稳定 | 360 | 0.012 | 0.0020 | 48 | 60 | 0 | −65 | 12 | 中央参考 |
| RS-W2 | S2 失活 | 350 | 0.010 | 0.0030 | 52 | 55 | 2e−4 | −80 | 8 | 参数偏移 |
| RS-W3 | S2 失活 | 370 | 0.016 | 0.0040 | 45 | 48 | 5e−4 | −55 | 16 | 快反应/强竞争 |
| RS-W4 | S2 失活 | 345 | 0.009 | 0.0015 | 56 | 65 | 8e−4 | −90 | 6 | 强热耦合 |
| RS-W5 | S1 稳定 | 355 | 0.014 | 0.0050 | 50 | 46 | 0 | −70 | 10 | 副反应边界 |

## 6.6 三层先验

### Entity

target：Catalyst C0–C3；A 正确、M `[2,0,3,1]` 错配。

### Parametric

target：`T*`。

- A：`T* ± 5 K`；
- M：W1..W5 分别 `+25 / −25 / +30 / −30 / +20 K`，区间宽度仍为 ±5 K；
- O：只给合法温度范围和安全警告。

### Structural

- A：稳定促进剂 vs 高温失活 family；
- M：另一 family；
- O：只说明可能存在目标/副反应，不声明是否存在失活。

## 6.7 实现状态

**高—中**。反应网络、Arrhenius、catalyst deactivation、reaction material prior 已存在；需要把高温稳定/失活 dossier 与 runtime 真正绑定。

---

# 7. 体系三：相平衡与分配（PT）

## 7.1 科学锚点

**苯甲酸在水/有机相中的分配及有机相缔合**。

这是非常适合发现导向 benchmark 的原型：理想 Nernst 分配可近似线性，而溶质在有机相缔合时会产生非线性/幂律表现。

正式 world 使用匿名 `solute-P / impurity-I / solvent-S / extractant-X`。

## 7.2 两个真实 constitutive families

### PT-S1：常数 Nernst 分配

在工作域中：

\[
D_P\approx K_P,\qquad D_I\approx K_I
\]

主要变化来自材料 pair 和 phase ratio。

### PT-S2：缔合/幂律分配

有效分配随浓度/组成出现幂律响应：

\[
D_{eff}\propto D_0\,c^{n-1},\qquad n>1
\]

结构错配：`S1 ↔ S2`。

## 7.3 Private parameters

- `K_product_ref`；
- `K_impurity_ref`；
- `partition_exponent n`；
- `phase_volume_multiplier`；
- `mixing/equilibration efficiency`；
- solvent × extractant pair interaction table；
- world residual。

参数层公开 target：

> **参考 `solvent-S1 × extractant-X1`、1:1 相比下的目标产物分配强度 `K_P*`**。

## 7.4 实体层 target：萃取剂

4 个 `extractant-X0..X3`。

沿用当前仓库 partition dossier 的 5 个核心字段：

1. 参考 partner panel 中产品分配几何均值；
2. 杂质分配几何均值；
3. 选择性几何均值；
4. 选择性上限；
5. 选择性 log-variability。

不公开真实 pair-interaction table。

## 7.5 五个 PT worlds

| World | 真结构 | K_P* | K_I* | exponent n | phase-volume mult. | equilibration efficiency | 角色 |
|---|---|---:|---:|---:|---:|---:|---|
| PT-W1 | S1 常数 | 2.2 | 1.0 | 1.00 | 0.90 | 0.85 | 中央参考 |
| PT-W2 | S2 幂律 | 3.5 | 0.8 | 1.50 | 1.05 | 0.90 | 参数偏移 |
| PT-W3 | S2 幂律 | 5.0 | 0.6 | 1.75 | 1.10 | 0.75 | 结构标准例 |
| PT-W4 | S1 常数 | 7.0 | 1.4 | 1.00 | 0.95 | 0.95 | 高分配/低选择性 |
| PT-W5 | S2 幂律 | 4.2 | 0.4 | 2.00 | 1.20 | 0.80 | 边界/强非线性 |

## 7.6 三层先验

### Entity

A 正确 extractant dossier；M 固定错配；O 只给 X0–X3。

### Parametric

target：`K_P*`。

- A：`0.90–1.10 × K_P*`；
- M：按 `[1.35, 0.70, 1.45, 0.65, 1.30] × K_P*` 作为 false center；
- O：不提供分配强度估计。

### Structural

- A：Nernst 常数分配或幂律缔合 family；
- M：另一 family；
- O：不说明 family。

## 7.7 实现状态

**高**。当前 partition material dossier、power-law constitutive stress 和 phase kernel 与该设计最接近。

---

# 8. 体系四：连续流反应（FL）

## 8.1 科学锚点

**乙酸乙酯与 NaOH 皂化的管式/PFR 原型**。

科学锚点提供：

- 二阶反应动力学；
- residence time 对 conversion 的直接影响；
- 温度与 kinetic rate 的耦合；
- flow rate 同时影响 throughput、residence time、pressure drop 和换热。

正式 benchmark 继续使用匿名 `feed-A / feed-B / carrier-medium-Mi`。

## 8.2 两个 structural families

### FL-S1：动力学主导 PFR

- 轴向温度变化较弱；
- conversion 主要由 reaction kinetics + residence time 决定；
- 简化的理想 PFR 关系在工作域内成立。

### FL-S2：热边界/输运耦合 PFR

- wall heat transfer 与 axial temperature profile 对 rate 明显；
- 相同 nominal residence time 在不同 flow/thermal 条件下不能用一个简单速率式解释；
- 可能出现“更慢流速不一定更优”的 throughput/risk 代价。

> 当前仓库的 flow provider 已经有 geometry、pressure drop、thermal boundary，但“FL-S1 vs FL-S2”尚需正式注册成可 fork 的 structural family。

## 8.3 Private parameters

- `k_ref`；
- `Ea`；
- `residence_time_multiplier`；
- `wall_UA_multiplier`；
- `hydraulic_resistance_multiplier`；
- geometry-fixed nuisance parameters；
- medium-specific transport residuals。

参数层公开 target：

> **参考温度/标准 feed 下的推荐 residence-time center `τ*`**。

## 8.4 实体层 target：载体/溶剂介质

新增 4 个 `medium-M0..M3`，建议 dossier：

1. 相对黏度；
2. 相对扩散能力；
3. 相对热容；
4. 相对换热能力；
5. 对参考反应的活度/反应速率影响。

### 推荐 nominal profile

| Medium | 黏度 | 扩散 | 热容 | 换热 | 反应活度 |
|---|---:|---:|---:|---:|---:|
| M0 | 0.80 | 1.20 | 0.95 | 1.10 | 0.95 |
| M1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| M2 | 1.30 | 0.85 | 1.20 | 0.90 | 1.10 |
| M3 | 1.60 | 0.70 | 1.05 | 0.80 | 0.90 |

没有单一 medium 在流动、热与反应三方面同时占优。

## 8.5 五个 FL worlds

| World | 真结构 | τ* (s) | k_ref (L mol⁻¹ s⁻¹) | Ea (kJ/mol) | residence mult. | UA mult. | hydraulic mult. | 角色 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| FL-W1 | S1 动力学主导 | 80 | 0.020 | 42 | 0.85 | 1.30 | 0.90 | 中央参考 |
| FL-W2 | S2 热耦合 | 130 | 0.030 | 48 | 1.15 | 0.55 | 1.20 | 参数偏移 |
| FL-W3 | S1 动力学主导 | 100 | 0.015 | 38 | 1.00 | 1.00 | 0.80 | 结构对照 |
| FL-W4 | S2 热耦合 | 150 | 0.025 | 55 | 1.25 | 0.45 | 1.40 | 强耦合 |
| FL-W5 | S2 热耦合 | 110 | 0.018 | 45 | 0.90 | 0.70 | 1.10 | 边界/压降 |

## 8.6 三层先验

### Entity

A 正确 medium dossier；M 固定错配；O 只给 M0–M3。

### Parametric

target：`τ*`。

- A：`0.90–1.10 × τ*`；
- M：乘 `[1.35,0.70,1.45,0.65,1.30]`；
- O：只给可行 flow / residence-time 域。

### Structural

- A：动力学主导 vs 热/输运耦合；
- M：另一 family；
- O：不提供 regime 假设。

## 8.7 实现状态

**中**。flow physics 已存在；需要新增：

- flow 专属 material dossier；
- `FL-S1 / FL-S2` structural fork；
- 对 `τ*` 的 provider-free truth sweep 和可辨识性 qualification。

---

# 9. 体系五：反应—萃取—纯化（PU）

## 9.1 科学锚点

**苯甲酸 + 乙醇酯化生成苯甲酸乙酯，随后水洗/萃取/干燥/浓缩的 work-up 原型**。

正式 world 只保留其一般科学结构：

```text
反应生成目标 P + 残余反应物/副产物 I
        ↓
两相分配
        ↓
选相 / 洗涤 / 再萃取
        ↓
干燥 / 浓缩 / 转移
        ↓
最终纯度与回收
```

## 9.2 两个 structural families

### PU-S1：近独立常数分配

- 产品与杂质具有近似固定 distribution coefficient；
- 多级萃取可以用独立分配近似；
- 洗涤主要体现常规 diminishing return。

### PU-S2：组成耦合/复杂化分配

- 杂质浓度、酸碱状态或配位/缔合改变产品的有效分配；
- 洗涤对产品 loss 和 impurity removal 的净收益随组成变化；
- 相同 solvent ratio 在不同阶段不能用固定 K 解释。

结构错配：`S1 ↔ S2`。

## 9.3 Private parameters

- `K_product_ref`；
- `K_impurity_ref`；
- `composition_coupling_strength`；
- `entrainment_fraction`；
- `wash_product_loss_fraction`；
- `transfer_hold_up_fraction`；
- `phase_disengagement_rate`；
- reaction-stage nuisance parameters。

参数层 target：

> **参考组成和 1:1 phase ratio 下的 product/impurity separation factor `S* = K_P/K_I`**。

## 9.4 实体层 target：萃取剂

新增 4 个 `extractant-X0..X3` dossier：

1. 产品亲和性；
2. 杂质亲和性；
3. 名义选择性；
4. 夹带倾向；
5. 相分离/脱层倾向；
6. 相对成本。

### 推荐 nominal profile

| Extractant | 产品亲和 | 杂质亲和 | 选择性 | 夹带倾向 | 脱层能力 | 成本 |
|---|---:|---:|---:|---:|---:|---:|
| X0 | 1.30 | 1.00 | 1.30 | 1.20 | 0.80 | 0.70 |
| X1 | 1.00 | 0.50 | 2.00 | 0.80 | 1.20 | 1.00 |
| X2 | 1.60 | 1.20 | 1.33 | 0.70 | 1.00 | 1.40 |
| X3 | 0.80 | 0.25 | 3.20 | 0.50 | 1.30 | 1.20 |

X3 高选择性但产品亲和较低；X2 产品抓取强但杂质共萃明显，避免单一绝对最佳材料。

## 9.5 五个 PU worlds

| World | 真结构 | K_P | K_I | S*=K_P/K_I | 耦合强度 | 夹带 | wash 产品损失 | transfer hold-up | 角色 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| PU-W1 | S1 独立 | 4.0 | 0.60 | 6.67 | 0.00 | 0.02 | 0.03 | 0.01 | 中央参考 |
| PU-W2 | S1 独立 | 7.0 | 1.50 | 4.67 | 0.00 | 0.04 | 0.02 | 0.02 | 高抓取/共萃 |
| PU-W3 | S2 耦合 | 3.5 | 2.00 | 1.75 | 0.35 | 0.06 | 0.06 | 0.03 | 低选择性困难 |
| PU-W4 | S2 耦合 | 6.0 | 0.80 | 7.50 | 0.60 | 0.08 | 0.08 | 0.05 | 强耦合/洗涤代价 |
| PU-W5 | S1 独立 | 2.5 | 0.40 | 6.25 | 0.00 | 0.12 | 0.04 | 0.06 | 边界/高物料损失 |

## 9.6 三层先验

### Entity

A 正确 extractant dossier；M `[2,0,3,1]`；O 只给 X0–X3。

### Parametric

target：`S*`。

- A：`0.90–1.10 × S*`；
- M：使用 world-specific false-center multiplier；
- O：不给 separation factor。

### Structural

- A：独立分配 vs 组成耦合；
- M：另一 family；
- O：只说明可能存在组成效应，不给结论。

## 9.7 实现状态

**中**。多阶段 work-up 和 extraction 已有 runtime 基础，但需要新增：

- purification 专属 extractant dossier；
- composition-coupled extraction structural fork；
- `S*` 的标准参考组成合同；
- 5 worlds 的完整物料守恒 qualification。

---

# 10. 体系六：反应—结晶（CR）

## 10.1 科学锚点

**阿司匹林合成后的冷却结晶/重结晶原型**。

这里只用它作为“反应后形成溶液 → 冷却/播种 → 成核/生长 → 过滤”的经典结构，不声称当前 simulator 逐分子复现真实阿司匹林结晶。

当前 ChemWorld 已经具备：

- van’t Hoff 型溶解度；
- seed mass；
- primary nucleation；
- crystal growth；
- impurity occlusion；
- crystal-size distribution；
- temperature/supersaturation history；
- filtration recovery。

## 10.2 两个 crystallization structural families

### CR-S1：晶种—生长主导

- 自发初生成核相对弱；
- 及时播种后，晶体数目主要由 seed population 决定；
- 合理慢冷有利于 growth，细粉较少。

### CR-S2：初生成核主导

- supersaturation 超阈值后 primary nucleation 强；
- seed 对最终 particle number 的控制有限；
- 快速冷却或过深过饱和容易形成 fines。

结构层错配：`S1 ↔ S2`。

> 两类都可以存在路径依赖；我们不把一个 family 粗暴定义成“完全无路径依赖”，因为当前真实 crystallization runtime 本身就是历史依赖过程。

## 10.3 Private parameters

- `reference_solubility_mol_L`；
- solvent-specific solubility multiplier；
- nucleation multiplier；
- growth multiplier；
- impurity occlusion multiplier；
- seed effectiveness multiplier；
- cooling-response nuisance parameters；
- upstream reaction composition residual。

参数层公开 target：

> **在参考溶剂/标准母液组成下达到明显 primary nucleation 的有效温度中心 `T_nuc*`**。

该值由 truth provider sweep 冻结，而不是直接把某个底层 coefficient 暴露给 Agent。

## 10.4 实体层 target：结晶溶剂

沿用当前 crystallization dossier 的 4 个 `solvent-S0..S3`。

核心字段：

1. 参考反应活性概括；
2. 相对溶解度；
3. 相对成核倾向；
4. 相对晶体生长；
5. 相对杂质包埋；
6. 可保留当前 activity floor/ceiling/variability 作为辅助字段。

## 10.5 五个 CR worlds

| World | 真结构 | T_nuc* (K) | S_ref (mol/L) | solubility mult. | nucleation mult. | growth mult. | occlusion mult. | seed effect | 角色 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| CR-W1 | S1 晶种主导 | 290 | 0.090 | 0.90 | 0.65 | 1.45 | 0.75 | 1.50 | 中央参考 |
| CR-W2 | S2 初生成核 | 295 | 0.100 | 1.05 | 1.50 | 0.85 | 1.15 | 0.75 | 参数偏移 |
| CR-W3 | S2 初生成核 | 285 | 0.085 | 0.80 | 1.80 | 0.70 | 1.35 | 0.65 | 强成核 |
| CR-W4 | S2 初生成核 | 300 | 0.095 | 1.20 | 1.30 | 1.00 | 1.50 | 0.80 | 强杂质耦合 |
| CR-W5 | S1 晶种主导 | 292 | 0.105 | 1.00 | 0.55 | 1.60 | 0.70 | 1.70 | 边界/慢成核 |

## 10.6 三层先验

### Entity

A 正确 solvent dossier；M 固定错配；O 只给 S0–S3。

### Parametric

target：`T_nuc*`。

- A：`±5 K`；
- M：W1..W5 使用统一温度偏移表；
- O：只给可行 cooling temperature range。

### Structural

- A：晶种—生长主导 vs 初生成核主导；
- M：另一 family；
- O：不声明哪一种主导。

## 10.7 实现状态

**中—高**。结晶 runtime 和材料 dossier 已成熟；主要新增点是：

- 把 seed-dominated / primary-nucleation-dominated 注册成真正 private-physics fork；
- 加入 seed-effect parameter；
- 对相同终温不同 thermal history 做 structural distinguishability qualification。

---

# 11. 体系七：反应—蒸馏（DS）

## 11.1 科学锚点

**乙酸 + 乙醇可逆酯化生成乙酸乙酯，并与蒸馏分离耦合的反应精馏原型**。

正式 benchmark 只保留：

- 可逆/选择性 reaction contribution；
- volatile product / solvent / impurity mixture；
- VLE；
- reflux / cut strategy；
- pot inventory 和 saved fractions 的不可逆演化。

## 11.2 两个 VLE structural families

### DS-S1：近常数相对挥发度

在工作组成域内：

- 主要组分的 relative volatility 变化较小；
- constant-α shortcut 能较好描述 cut enrichment。

### DS-S2：组成依赖非理想 VLE

- activity correction 使 K-value / relative volatility 随 liquid composition 改变；
- 早期馏分和后期馏分的分离能力不同；
- 固定 cut/reflux 经验不能直接外推到整个 batch。

结构错配：`S1 ↔ S2`。

## 11.3 Private parameters

- `alpha_ref`；
- `activity_nonideality_strength`；
- `reflux_efficiency`；
- `reaction_equilibrium/selectivity nuisance`；
- `energy_cost_multiplier`；
- pot/fraction inventory state；
- world-specific solvent/entrainer residuals。

参数层公开 target：

> **标准 feed composition 和参考温度下的有效 relative volatility `α*`**。

## 11.4 实体层 target：溶剂/夹带剂类别

使用 4 个 `entrainer-S0..S3`，建议 dossier：

1. 目标产物相对挥发度影响；
2. 非理想活度倾向；
3. 对上游反应的活度影响；
4. 热负荷指数；
5. 溶剂损失倾向；
6. 相对成本。

### 推荐 nominal profile

| Entrainer | 产品挥发提升 | 非理想倾向 | 反应活度 | 热负荷 | 溶剂损失 | 成本 |
|---|---:|---:|---:|---:|---:|---:|
| S0 | 1.20 | 0.80 | 0.90 | 1.00 | 1.20 | 0.70 |
| S1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| S2 | 0.85 | 1.25 | 1.15 | 1.20 | 0.80 | 1.30 |
| S3 | 1.35 | 1.40 | 0.80 | 1.40 | 1.40 | 1.10 |

## 11.5 五个 DS worlds

| World | 真结构 | α* | nonideality strength | reflux efficiency | reaction-selectivity mult. | energy mult. | 角色 |
|---|---|---:|---:|---:|---:|---:|---|
| DS-W1 | S1 常数α | 1.35 | 0.00 | 0.75 | 1.00 | 1.00 | 中央参考 |
| DS-W2 | S2 非理想 | 1.60 | 0.35 | 0.85 | 0.90 | 1.20 | 参数偏移 |
| DS-W3 | S1 常数α | 2.10 | 0.00 | 0.90 | 1.10 | 0.80 | 高分离能力 |
| DS-W4 | S2 非理想 | 2.50 | 0.55 | 0.70 | 0.80 | 1.40 | 强耦合 |
| DS-W5 | S2 非理想 | 1.25 | 0.75 | 0.80 | 1.00 | 1.10 | 边界/低α |

## 11.6 三层先验

### Entity

A 正确 entrainer dossier；M `[2,0,3,1]`；O 只给 S0–S3。

### Parametric

target：`α*`。

- A：`0.90–1.10 × α*`；
- M：按统一 world-specific false-center multiplier；
- O：不给相对挥发度估计。

### Structural

- A：常数 relative volatility vs composition-dependent activity-corrected VLE；
- M：另一 family；
- O：不声明 VLE family。

## 11.7 实现状态

**中**。distillation runtime 已有 Raoult/activity VLE 与 constant-relative-volatility shortcut 的物理基础，但需要：

- 正式注册 DS-S1/DS-S2 world fork；
- 蒸馏专属 material dossier；
- 标准 feed composition 下 α* 的 truth oracle；
- cut/fraction inventory 下的可辨识性测试。

---

# 12. 35 个 Private Worlds 总表

| ID | 体系 | 真 structural family | 参数层 target | 主要 private challenge |
|---|---|---|---|---|
| EC-W1 | 电化学 | 平台型 | V*=0.90 V | 中央参考 |
| EC-W2 | 电化学 | 峰型 | V*=1.05 V | 参数偏移 |
| EC-W3 | 电化学 | 峰型 | V*=1.20 V | 强副反应 |
| EC-W4 | 电化学 | 峰型 | V*=0.95 V | 高阻+强衰减 |
| EC-W5 | 电化学 | 平台型 | V*=1.30 V | 传质边界 |
| RS-W1 | 热安全 | 稳定促进剂 | T*=360 K | 中央参考 |
| RS-W2 | 热安全 | 失活 | T*=350 K | 失活+热反馈 |
| RS-W3 | 热安全 | 失活 | T*=370 K | 快反应+副反应 |
| RS-W4 | 热安全 | 失活 | T*=345 K | 强放热/弱散热 |
| RS-W5 | 热安全 | 稳定促进剂 | T*=355 K | 副反应边界 |
| PT-W1 | 分配 | 常数 Nernst | K*=2.2 | 中央参考 |
| PT-W2 | 分配 | 幂律 | K*=3.5 | 中等非线性 |
| PT-W3 | 分配 | 幂律 | K*=5.0 | 1.75 power 标准例 |
| PT-W4 | 分配 | 常数 Nernst | K*=7.0 | 高分配/低选择性 |
| PT-W5 | 分配 | 幂律 | K*=4.2 | 强非线性 |
| FL-W1 | 连续流 | 动力学主导 | τ*=80 s | 中央参考 |
| FL-W2 | 连续流 | 热耦合 | τ*=130 s | 热边界 |
| FL-W3 | 连续流 | 动力学主导 | τ*=100 s | 低速率 |
| FL-W4 | 连续流 | 热耦合 | τ*=150 s | 强热/压降耦合 |
| FL-W5 | 连续流 | 热耦合 | τ*=110 s | 边界流动 |
| PU-W1 | 纯化 | 独立分配 | S*=6.67 | 中央参考 |
| PU-W2 | 纯化 | 独立分配 | S*=4.67 | 高共萃 |
| PU-W3 | 纯化 | 组成耦合 | S*=1.75 | 低选择性 |
| PU-W4 | 纯化 | 组成耦合 | S*=7.50 | 强耦合+洗涤损失 |
| PU-W5 | 纯化 | 独立分配 | S*=6.25 | 高夹带/hold-up |
| CR-W1 | 结晶 | 晶种主导 | Tnuc*=290 K | 中央参考 |
| CR-W2 | 结晶 | 初生成核主导 | 295 K | 高成核 |
| CR-W3 | 结晶 | 初生成核主导 | 285 K | 强成核+慢增长 |
| CR-W4 | 结晶 | 初生成核主导 | 300 K | 杂质包埋 |
| CR-W5 | 结晶 | 晶种主导 | 292 K | 慢成核/快生长 |
| DS-W1 | 蒸馏 | 常数α | α*=1.35 | 中央参考 |
| DS-W2 | 蒸馏 | 非理想 VLE | 1.60 | 中等非理想 |
| DS-W3 | 蒸馏 | 常数α | 2.10 | 高分离能力 |
| DS-W4 | 蒸馏 | 非理想 VLE | 2.50 | 强耦合/高能耗 |
| DS-W5 | 蒸馏 | 非理想 VLE | 1.25 | 低α边界 |

---

# 13. 450-session 展开规则

## 13.1 底层 world ID 不随任务导向变化

例如：

```text
EC-W03
```

可以派生：

```text
EC-DISC-ENT-W03-O
EC-DISC-ENT-W03-A
EC-DISC-ENT-W03-M
EC-DISC-PAR-W03-O
...
EC-OPT-STR-W03-M
```

## 13.2 推荐命名

- 体系：`EC / RS / PT / FL / PU / CR / DS`
- 导向：`DISC / OPT`
- 先验层：`ENT / PAR / STR`
- world：`W01..W05`
- arm：`O / A / M`

完整：

```text
{system}-{orientation}-{locus}-{world}-{arm}
```

例如：

```text
CR-DISC-STR-W04-M
```

表示：结晶、发现导向、结构层、World 4、错误结构先验。

## 13.3 每体系 sessions

| 体系 | 导向 | sessions |
|---|---|---:|
| 电化学 | DISC + OPT | 90 |
| 反应—热安全 | DISC + OPT | 90 |
| 相平衡/分配 | DISC | 45 |
| 连续流 | OPT | 45 |
| 萃取/纯化 | OPT | 45 |
| 结晶 | DISC + OPT | 90 |
| 蒸馏 | OPT | 45 |
| **总计** | 10 task-orientations | **450** |

---

# 14. 一个非常关键的正交性规则

三个先验层不是简单把三份信息同时塞给 Agent。

## 14.1 Entity 会话

只操纵材料 dossier 映射。

参数/结构方面：三 arms 获得**完全相同的普通任务描述**，不额外泄露正确数值或 mechanism family。

## 14.2 Parametric 会话

只操纵一个预注册数值对象。

材料 dossier 在三 arms 中保持同一状态；建议使用**统一 nominal dossier**或统一 opaque dossier，不让材料信息成为 arm 差异。

结构方面，三 arms 使用相同 public formulation；参数 target 必须有明确 scope，避免依赖未说明的结构假设。

## 14.3 Structural 会话

只操纵 mechanism family 陈述。

材料 dossier 和参数 hints 在三 arms 中保持相同，不额外给 A 更精确的数字。

> 这条规则非常重要：`Entity / Parametric / Structural` 是三个独立实验层，而不是把 A arm 做成“所有方面都知道正确答案”的超级信息组。

---

# 15. 正式编码前必须完成的 qualification

每个 `system × world × locus` 都至少要过下面 8 个检查。

## Q1. 可执行

所有预注册操作都能在合法域完成；不靠异常/越界区分机制。

## Q2. 守恒与 replay

- 物料守恒；
- 能量/电荷相关 ledger 合法；
- exact replay 一致。

## Q3. 先验真实性

Aligned 不是装饰性文字：其 nominal information 与 realized world 在指定层面真正相关。

## Q4. 错配真实性

Misindexed/Misspecified 必须实际错误，而且错误方向在实验域中有后果。

## Q5. 可辨识

至少存在一组**合法、预算内、公开可见**的实验，使 A 与 M 所表达的两个候选 hypothesis 产生可区分观测。

## Q6. 不能一眼猜答案

不能只做一次默认实验或读取一个材料编号就直接知道 structural family。

## Q7. 不是同一最优配方

对于优化导向，至少部分 worlds 中错误先验对应的自然推荐策略和真实最优/近优策略应不同，否则 prior 对决策没有意义。

## Q8. 世界不按 Agent 结果筛选

world 的保留/淘汰只能依据 provider-free qualification，不能因为某个模型表现太好或太差而事后换 world。

---

# 16. 建议的开发顺序

为了降低实现风险，不建议同时写完 35 个 world 再统一调试。

## Phase A：直接利用现有能力的 15 worlds

优先：

1. 电化学 EC-W1..W5；
2. 相平衡 PT-W1..W5；
3. 反应—热安全 RS-W1..W5。

原因：

- 当前材料 prior 和机制 family 最成熟；
- 最容易验证三层先验是否真正正交；
- 可以先把统一 world schema、prior generator、misindex、parameter hint 和 structural statement 接口做对。

## Phase B：已有 runtime、需要新增先验/结构合同的 10 worlds

4. 结晶 CR-W1..W5；
5. 蒸馏 DS-W1..W5。

## Phase C：新增 authoring 较多的 10 worlds

6. 连续流 FL-W1..W5；
7. 萃取/纯化 PU-W1..W5。

---

# 17. 现在还没有冻结、但下一步必须决定的 7 件事

本文已经把 private truth 设计推进到“可以开始实现”的程度，但下面内容建议在正式 coding 之前开一次设计 review：

1. **材料 profile 的最终公开字段**：特别是 RS / FL / PU / DS 新增 dossier；
2. **参数层 target 的精确定义和 reference condition**；
3. **structural family 的 JSON schema 与 runtime switch**；
4. **5 个 world 数值是否需要在 provider sweep 后微调**；
5. **discover/optimize 两个 task contract 如何共享同一 world 但使用不同公开目标**；
6. **是否所有体系统一使用 4 个材料候选**；
7. **qualification 阈值**：信号差、可区分度、最优策略差异和安全可达性的具体数值。

这些都应在模型正式实验前冻结，并且一旦正式 block 启动，不应根据 Agent 结果再修改。

---

# 18. 当前设计最核心的逻辑

最终实验不是：

> 造 450 个随机题，让模型做优化。

而是：

```text
7 个科学体系
        ↓
每个体系 5 个预先设计且可资格化的真实规律实例
        ↓
35 个固定 private worlds
        ↓
同一 world 上分别改变
实体知识 / 参数知识 / 结构知识
        ↓
每层分别 Opaque / Aligned / Misindexed(Misspecified)
        ↓
发现型或优化型任务复用同一真实世界
```

这样 450 sessions 的差异真正来自：

1. **任务导向不同**；
2. **先验知识层级不同**；
3. **先验正确性不同**；
4. **底层真实规律不同**；

而不是来自随意更换题面、材料数、仪器或预算。

这才是后面能够把整个 Experiment 1 做成一个严谨 benchmark 的基础。
