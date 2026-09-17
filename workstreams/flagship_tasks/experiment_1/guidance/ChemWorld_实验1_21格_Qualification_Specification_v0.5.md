# ChemWorld 实验 1：21 个“体系 × 先验层” Qualification Specification（v0.5）

> **目标**：把 v0.4 的“目标全覆盖、逐格资格化”真正落到 21 个可开发单元上。  
> 本文只回答一件事：**某个体系中的实体层 / 参数层 / 结构层先验，是否有资格进入正式 Opaque / Aligned / Misspecified 三臂 benchmark？**  
> 本文不定义 Agent 下游评分，不讨论知识报告、部署或模型排名。

---

# 0. 先读这一页：这里的 qualification 到底在验证什么

对任意一个 `体系 × World × 先验层`，顺序必须是：

```text
先有一个科学合理的 private World
        ↓
从 World truth 派生一个有限但正确的 Aligned prior
        ↓
构造格式、精度、措辞、置信度匹配的错误 prior
        ↓
证明两种 prior 对应的假设在公开实验空间中可以区分
        ↓
证明预算内至少存在一组公开实验可以反驳错误 prior
        ↓
证明这种差异不是单个 noise seed 的偶然结果
        ↓
才允许进入正式 O / A / M Participant 实验
```

因此：

- **World 不是错误的。** World 永远是 simulator 的真实物理。
- **Aligned / Misspecified 只是 Agent 收到的信息不同。**
- **qualification 不要求 Agent 实际找到判别实验。** 它只证明“公开条件下存在可找到的反证”，避免把不可辨识题目甩给 Agent。
- **qualification 必须在 Participant 正式结果之前完成。** 不能因为某个 World 上 Agent 表现不好再换 World。

---

# 1. 本文依据与“已实现 / 建议新增”的边界

本文优先继承当前仓库已经存在的设计资产：

- `docs/world-authoring-contract.md`：private physics fork 与 public contract invariance；
- `docs/mechanism_schema.md`：hidden mechanism / constitutive family；
- `docs/world_law.md`：当前反应、相分配、结晶、蒸馏、连续流、电化学执行路径；
- `docs/world-capability-map.md`：公开操作、参数轴、仪器；
- `src/chemworld/materials.py`：电化学、反应、分配、结晶材料 dossier；
- `src/chemworld/eval/work_ii_ae_prior_qualification_v03.py`：实体层先验资格化模板；
- `src/chemworld/eval/work_ii_matched_prior_qualification.py` 与 `work_ii_electrochemical_matched_prior_qualification.py`：参数层 local-prior 资格化模板；
- `src/chemworld/eval/work_ii_structural_candidate_qualification.py`：电化学 transport 与结晶 seed-effect 结构候选；
- `src/chemworld/eval/work_ii_catalyst_deactivation_q0.py`：反应热过程 catalyst deactivation topology；
- `src/chemworld/eval/work_ii_static_topology_q0.py`：连续流 reversible-pathway topology；
- `src/chemworld/eval/work_ii_constitutive_structural_qualification.py`：相间分配 power-law constitutive family。

状态标记：

| 标记 | 含义 |
|---|---|
| **A：已有资产** | 当前代码中已有与该设计高度一致的 prior / fork / qualification 资产；仍需按新 5-world protocol 重新冻结 |
| **B：可直接开发** | 当前底层 physics 与公开动作已经支持，主要缺 prior schema / qualification block |
| **C：需新增 private-physics family** | 当前世界律没有我们想测试的那对 competing families；必须先实现和验证 world fork，不能只写进 prompt |

> “A”不等于已经获得新实验的正式发表级资格，只表示已有可复用工程与设计资产。

---

# 2. 三类 qualification 的共同硬门

## 2.1 所有 21 格都必须通过的硬门

1. **世界自洽**：质量、电荷、能量、phase / crystal / fraction ledger 闭合；运行和 exact replay 通过。
2. **public contract 匹配**：O/A/M 的 operation、instrument、resource、noise policy、task objective 完全一致。
3. **先验不泄漏 arm 身份**：不得出现 `aligned / misspecified / oracle / world seed / hidden mechanism` 等提示。
4. **A/M 对称**：相同 schema、字段、上下文、置信度和近似文本长度，只允许目标科学 claim 不同。
5. **可辨识**：A 与 M 在公开可执行实验空间存在可测差异。
6. **预算内可反证**：Participant 总预算中存在现实可承受的判别实验，不要求穷举全空间。
7. **有任务相关后果**：错误 prior 必须至少在一部分合理策略下改变实验选择、预测、可行域或工艺行为。
8. **噪声稳健**：区分不能依赖一个幸运 noise seed。

## 2.2 三类先验分别采用的推荐开发门槛

这些不是新正式阈值，而是**优先复用当前仓库已使用过的资格化逻辑**；新单元正式运行前仍需独立校准并冻结。

### 实体层模板

继承当前 A-E v0.3 的思想：

- 2 个预注册 anchor recipe；
- 4 个候选材料；
- 每个 anchor × material 做独立噪声重复；
- 至少一个任务相关公开 endpoint 在错配的两材料间具有：
  - absolute separation ≥ **0.05**；
  - signal-to-noise ratio ≥ **2.0**；
- A/M dossier 不能读取 world seed、真实 residual、hidden outcome。

正式 Participant 不需要重复这个大资格化面；它只需要在自身预算内**存在**可验证错配的实验。

### 参数层模板

优先采用 current matched-local-prior 逻辑，而不是手工固定 `+25 K / +0.20 V / ×1.35`：

1. provider-free 扫描真实 response surface；
2. 在 reference context 附近拟合一个有限 local model；
3. Aligned 给真实 local direction / window；
4. Misspecified 通过“反射 / 合理位移”构造，使两者在 reference point 附近难以靠一个点区分，但在低侧和高侧均出现反证区；
5. 推荐保留当前模板中的：
   - aligned normalized MAE ≤ **0.20**；
   - A/M 在 held-out 上有足够 disagreement（当前模板约 **25%**）；
   - false prior 相对 aligned 至少有明确 blind-error margin；
   - 低侧和高侧都存在反证区域。

### 结构层模板

两类结构门都可使用：

**关系结构型**（如 EC transport、C seed × cooling）：

- 3 × 3 预注册 intervention grid；
- 对关键 validation points 做独立噪声重复；
- 核心 effect ≥ `max(0.03, 6 × observed_sigma)`；
- A/M held-out disagreement fraction ≥ **0.40**；
- 同时存在低区和高区 counterexample；
- aligned model 的 blind error 必须小于 misspecified model。

**真实 law/topology fork 型**（如 RX deactivation、FL reversible topology）：

- parent/child 只改变一个注册 private-physics target；
- 同 action plan、同 noise key 成对执行；
- 至少两个公开 metric 出现 ≥ `max(0.05, 3σ)` 的 paired effect；
- 支持点不能全部集中在一个局部格子；
- 必须有与结构差异一致的 accumulation / interaction signature。

---

# 3. 21 格总览

| 体系 | 实体层 | 参数层 | 结构层 | 当前状态概览 |
|---|---|---|---|---|
| **EC 电化学** | 电解液 dossier 映射 | 电位–电流 local window | 高电流 transport limitation 是否存在 | A / A / A |
| **RX 反应–热过程** | 催化剂 dossier 映射 | 温度–时间 local relation | 催化剂失活 vs 稳定催化剂 | A / A / A |
| **PA 相间分配** | 萃取剂 dossier 映射 | 有效分配强度 / `K*` | linear vs power constitutive law | A / B / A |
| **FL 连续流** | 催化剂 dossier 映射 | 温度–停留时间 local window | 不可逆 vs reversible target pathway | B / B / A |
| **P 反应–萃取–纯化** | 萃取剂 dossier 映射 | reference separation factor | 常数独立分配 vs composition-coupled separation | B / B / C |
| **C 反应–结晶** | 结晶溶剂 dossier 映射 | 成核/冷却 local threshold | seed-mediated nucleation–growth 是否存在 | A / B / A |
| **D 反应–蒸馏** | 催化剂 dossier 映射（v0.5 首选） | effective relative volatility / cut window | constant-α vs composition-dependent VLE | A / B / C |

> v0.5 为了避免“为了体系名字好看而引入未经验证的材料属性”，D 的实体层先选当前仓库已有审计基础的 **上游催化剂 dossier**。未来如果真正实现匿名挥发性材料 dossier，可再版本升级为 D-specific entity locus。

---

# 4. EC：电化学有效转化

## EC-E：实体层——电解液配置 dossier 映射

**科学对象**  
四个匿名 `electrolyte-E0..E3` 的 nominal physicochemical dossier 与 action ID 的映射。

**Private truth**  
每个 World 固定：

- 4 个 nominal electrolyte profile；
- world-specific bounded residual；
- 真实 conductivity / diffusivity / diffusion-layer / capacitance / acid-base / precipitation / standard-potential shift 对电化学运行的实际作用。

World residual 可以让 nominal dossier 不完美，但不能让“错配行”系统性比正确行更接近 realized truth。

**Aligned**  
给 `E0..E3` 正确的 nominal dossier。当前仓库已有字段包括 conductivity、diffusivity、diffusion-layer thickness、double-layer capacitance、acid concentration、supporting electrolyte、precipitating salt、pKa、Ksp、standard-potential shift 等。

**Misindexed**  
只对 `electrolyte_profile` 做预注册两行交换，例如 `E0 ↔ E2`；所有字段整行交换，不单独篡改某一个数值。Solvent dossier 在三臂保持相同信息状态。

**最小公开判别实验**  
选被交换的两种 electrolyte，在完全相同的 solvent / reagent / duration 下，各做：

1. 一个中等 current anchor；
2. 一个高 current anchor；

并测 UV / final assay（必要时 pH diagnostic）。高 current anchor 应放大 conductivity / diffusion / ohmic 差异。

**为什么预算内可反证**  
只需 4 个完整 recipe（2 electrolyte × 2 anchors）就有机会检验 dossier 的关键排序；正式 Agent 不需要恢复完整 10 维物性。

**E0 pass**  
沿用实体层模板：两 anchor 上被交换材料的任务相关 endpoint separation 均达到 effect + SNR 门；世界 residual 不得反转正确 mapping。

**状态**：**A**。当前 S0 / A-E 资格化已有高度一致资产。

---

## EC-P：参数层——电位–电流局部工作关系

**科学对象**  
在固定 electrolyte / solvent / reagent / duration reference context 下，`controlled_potential` 与 `controlled_current` 对 balanced electrochemical performance 的局部方向或窗口。

**Private truth**  
由真实 EC World 的 Butler–Volmer、transport、ohmic、selectivity-decay 等参数执行后产生完整 response surface。**不手填 V* 作为独立真值**；V* / preferred direction 从 surface 自动推导。

**Aligned**  
给一个不完整的 local process model，例如：

- “在当前 context 下，更高 potential 更可能改善综合表现”；或
- “更低 current 更可能避开 transport loss”；

只给局部方向 / 窗口，不给 hidden constants 和全局 optimum。

**Misspecified**  
相同 schema / confidence / context，给反方向或经过 reference center 反射的 local relation。

**最小公开判别实验**  
4 点设计：

- reference 附近两个 potential × 两个 current；
- 至少一个点落在 A 偏好侧，一个点落在 M 偏好侧。

测 selective product yield、Faradaic efficiency、energy efficiency、risk / score。

**为什么预算内可反证**  
当前已有 K=4 参数先验 pilot；4 个完整实验就能覆盖 A/M 两侧，不需要全网格搜索。

**E0 pass**  
provider-free surface 先证明 aligned local model 足够准确；A/M 在 held-out 上产生足够 disagreement，且低侧、高侧都有反证区域。

**状态**：**A**。当前 `work_ii_electrochemical_matched_prior_qualification.py` 可直接借鉴。

---

## EC-S：结构层——高电流 transport limitation 是否存在

**科学对象**  
不是“最佳电流是多少”，而是：**固定 potential 时，把 current 从中区继续提高，是否出现可测的 transport / Faradaic efficiency 损失和 diminishing product gain。**

**Private truth**  
当前 World 的 electrochemical physics 自动决定 seed-current interaction 与 transport limitation signature。

**Aligned**  
> 在固定 potential 下，从中等 current 继续升高，目标产物的边际收益递减，同时 transport / Faradaic efficiency 明显下降。

**Misspecified**  
> 在固定 potential 下，从中等 current 继续升高仍持续带来目标产物收益，transport / Faradaic efficiency 近似稳定。

两条 prior 不给任何具体 optimum。

**公开判别实验**  
使用当前已实现的 3 × 3 grid：

- potential：低 / 中 / 高；
- current：低 / 中 / 高；

并在中等 potential 下对三档 current 做独立噪声重复。

**为什么预算内可反证**  
Agent 实际不需要跑完整 9 点；只要在同一 potential 下比较中电流与高电流，测 transport / Faradaic / yield，就可能出现直接反证。9 点 grid 是 E0 资格化而非 Participant 必做。

**E0 pass**  
直接继承现有 structural-candidate 逻辑：关键效应 ≥ `max(0.03,6σ)`；held-out disagreement ≥ 40%；低/高 current 两侧都有 counterexample；aligned model blind error 更低。

**状态**：**A**。已有 `electrochemical_transport` structural candidate。

---

# 5. RX：反应–热过程

## RX-E：实体层——催化剂 dossier 映射

**科学对象**  
四个匿名 `catalyst-C0..C3` 的参考活性 profile 与 action ID 的映射。

**Private truth**  
每个 World 固定 4 个 catalyst 的 nominal reference-panel activity 与 world-specific catalytic residual；实际反应网络、温度效应和失活机制仍然隐藏。

**Aligned**  
正确映射 catalyst dossier，字段使用当前 generic reaction prior：reference-panel activity geomean / floor / ceiling / log variability。

**Misindexed**  
只交换一对 catalyst 行；不改 solvent dossier，不改温度/时间 prior。

**最小公开判别实验**  
被交换的两种 catalyst，在固定 solvent、温度、时间、投料下做两个 anchor：

1. 较短反应时间；
2. 较长但仍安全的反应时间；

quench 后用 HPLC / final assay 看 conversion、yield、selectivity、byproduct。

**为什么预算内可反证**  
4 个 reaction batches 即可直接测试两 catalyst 的相对活性与长期表现，不要求识别整个反应网络。

**E0 pass**  
沿用 A-E physical gate：两个 anchor 均有足够 endpoint separation 与 SNR，且 world residual 不使错配变成更准确的资料。

**状态**：**A**。`reaction-safety-constrained` 已在现有 A-E qualification 范围内。

---

## RX-P：参数层——温度–时间局部响应

**科学对象**  
固定 catalyst / solvent / reagent context 下，temperature 与 reaction duration 的 local safe-performance relation。

**Private truth**  
由真实 reaction network、Arrhenius kinetics、thermal history、deactivation / side reaction 等共同形成 response surface。

**Aligned**  
给 reference region 附近真实的 directional claim，例如“更高温度更可能改善 balanced performance”或“更长时间更可能恶化安全/选择性”。

**Misspecified**  
保持 reference region、schema、confidence 不变，只反转 target axis 的 local direction。

**公开判别实验**  
2 × 2：

- 两档温度；
- 两档时间；

覆盖 A/M 两侧；测 yield / selectivity / safety risk / score。

**为什么预算内可反证**  
4 个 batch 就可以构成最小 local response test；当前仓库已经有更大的 121 点 provider-free surface 用来做 E0。

**E0 pass**  
复用 matched-prior template：aligned local surface fit 合格、A/M disagreement 足够、低温/高温或短时/长时两侧都有 blind counterexample。

**状态**：**A**。

---

## RX-S：结构层——催化剂失活 vs 稳定催化剂

**科学对象**  
是否存在一个真正的 catalyst deactivation pathway，而不是只把“长时间效果差”解释成某个 rate constant 偏小。

**Private truth**  
两类真实 topology：

- `deactivating_baseline`：存在 catalyst deactivation reaction；
- `stable_catalyst`：该 deactivation pathway 被移除。

parent / child 只改变这一 private reaction topology。

**Aligned**  
如果 World 为 deactivating：声明“催化活性会随温度/时间积累性衰减，长时效果不是简单线性累积”；stable World 则给相反关系。

**Misspecified**  
给相反 topology claim。

**公开判别实验**  
优先 3 维小设计：

- 低 / 高温；
- 短 / 长时间；
- 低 / 高 catalyst dose。

Participant 最小版可只跑 4 个角点；E0 可使用现有 3 × 3 × 3 paired-law screen。

**为什么预算内可反证**  
失活是“随时间累积且受温度 / catalyst loading 调制”的结构 signature；只要有早/晚两个时间点和至少两种 catalyst dose，就能与稳定催化剂产生不同预测。

**E0 pass**  
沿用现有 Q0：至少两个 direct metrics 解析 topology；支持点跨多个 grid 区域和至少两种 catalyst dose；存在 duration-accumulation signature；pair execution 与 noise 完全匹配。

**状态**：**A**。已有 `work_ii_catalyst_deactivation_q0.py`。

---

# 6. PA：相间分配

## PA-E：实体层——萃取剂 dossier 映射

**科学对象**  
四个匿名 extractant 的 marginal partition / selectivity profile 与 action ID 映射。

**Private truth**  
真实 World 固定 solvent × extractant pair interaction table、world-level coefficient transform、phase-volume response 与 mixing response；公开 dossier 只给 extractant 在 reference partner panel 上的边际摘要。

**Aligned**  
正确映射 extractant dossier：product distribution、impurity distribution、selectivity geomean / ceiling / variability。

**Misindexed**  
只交换两个 extractant dossier 行；solvent info 保持同状态。

**最小公开判别实验**  
固定一个预注册 solvent、aqueous / organic volume、mix / settle 条件，对被交换的两个 extractant 分别做 partition；HPLC / final assay 同时读 organic 与 aqueous product amount。

为了避免 pair-specific residual 偶然抵消，建议再使用第二个 solvent anchor。

**为什么预算内可反证**  
2 extractant × 2 solvent anchors = 4 个实验即可测试边际 profile 是否可信；不要求试完 16 个 pair。

**E0 pass**  
两 anchors 上至少一个 gating endpoint 满足 separation + SNR；正确 dossier 在独立 World 上能识别 H0 vs swap，不能用 hidden pair table 直接做 classifier 输入。

**状态**：**A**。当前 partition dossier 与 A-E qualification 已覆盖。

---

## PA-P：参数层——参考 pair 的有效分配强度 `K*`

**科学对象**  
固定 solvent / extractant pair 与充分 mix / settle 条件下，product 的 reference effective distribution strength（推荐在 log-space 表示）。

**Private truth**  
从真实 World 的 partition constitutive law 自动计算 reference `K*`；不直接把 private raw table 全部暴露。

**Aligned**  
给 `log K*` 的近似区间，或等价地给“在 reference phase ratio 下 product 更偏 organic / 更偏 aqueous”的定量范围。

**Misspecified**  
给相同宽度、相同精度但在 log-space 反射/平移后的 plausible 区间；不得跨出当前 simulator 支持域。

**公开判别实验**  
同一 pair 下改变 phase ratio / extractant volume，建议 3 个相隔较开的 ratio；保证 mix / settle 足够接近平衡；同时测两相 product amount。

**为什么预算内可反证**  
一个常数 `K*` 能从少量质量守恒分配实验估计；3 个 phase ratios 足以防止单点噪声或体积误差伪装成正确 prior。

**E0 pass**  
provider-free 先生成 reference surface；Aligned band 对 held-out phase ratios 预测误差合格，M 在低/高 ratio 均有反证点，且错误区间不是只在一个极端点失败。

**状态**：**B**。底层 law 和公开操作已存在，需新增 matched parametric prior contract。

---

## PA-S：结构层——linear vs power partition constitutive law

**科学对象**  
base distribution coefficient 进入实际 constitutive law 时，是近线性关系还是 power response。

**Private truth**  
当前已注册：

- baseline：`partition_coefficient_exponent = 1.0`；
- altered：power response，当前 stress 可到 exponent ≈ 1.75。

**Aligned**  
给真实 law family：`linear_response` 或 `power_response`，可给近似 exponent family，但不提供 private pair table。

**Misspecified**  
给另一 family。

**公开判别实验**  
**不能再只用一个 nominal pair。** 这是历史 under-identification 的关键教训。

建议公开最小判别集：

- 选至少 4 个 solvent–extractant pair；
- 事前保证其 nominal base coefficient 覆盖 `<1`、`≈1`、`>1` 的区域；
- process 条件保持一致并接近平衡；
- 测 organic / aqueous amount 与 phase ratio。

`K^1` 与 `K^1.75` 在 `K≈1` 可近似 alias，但在低 / 高 K pair 上会明显分开。

**为什么预算内可反证**  
4–6 个 carefully chosen pair 即可覆盖 family divergence，不需要 16 pair × 全过程网格。

**E0 pass**  
除了 paired-law effect，还必须证明：

- false family 在允许参数调整后仍不能同时解释低-K 与高-K holdout；
- 至少两个 resolved metrics；
- 资格化不读取 Participant 不可见的 hidden coefficient table。

**状态**：**A**。已有 registered constitutive transform 与结构资格化资产，但新 Participant protocol 必须重新做 public identifiability。

---

# 7. FL：连续流

## FL-E：实体层——催化剂 dossier 映射

**科学对象**  
四个匿名 catalyst 对 flow reaction kinetics 的 reference activity profile。

**Private truth**  
连续流 World 使用共享 reaction network；不同 catalyst 有 nominal activity + world residual，真实 outlet behavior 还受 residence time、temperature、heat transfer、pressure drop 影响。

**Aligned**  
复用 generic reaction catalyst dossier：reference-panel activity geomean / range / variability。

**Misindexed**  
固定两 catalyst 行交换。

**公开判别实验**  
同一个 reactor configuration / temperature / residence time 下比较被交换的两 catalyst；再在第二个 residence-time anchor 重复；出口用 UV / final assay 测 conversion / yield / selectivity。

**为什么预算内可反证**  
2 catalyst × 2 residence anchors = 4 个 flow runs；足以检验“哪个 catalyst 在 reference kinetics 上更活跃”。

**E0 pass**  
实体层 separation + SNR gate；必须同时确认差异不是因为两个 run 实际几何/flow contract 不一致。

**状态**：**B**。底层 catalyst / reaction 已存在，但 `materials.py` 当前未把 FL 纳入 audited nominal prior task，需要新增 task-specific dossier contract。

---

## FL-P：参数层——温度–停留时间 local operating relation

**科学对象**  
固定 catalyst / feed context 下，temperature 与 residence time 对 outlet conversion / yield / risk 的局部可行窗口。

**Private truth**  
由 PFR reaction network + heat transfer + pressure-drop / geometry contract 产生。注意当前接口中 `flow rate` 与 `residence time` 会共同定义设备几何，不能把它们当固定 reactor 上两个完全独立旋钮。

**Aligned**  
给“更长 residence time / 更高温度是否改善当前局部表现”的有限 directional prior，或给一个近似可行窗口。

**Misspecified**  
在同 reference context 下反转一个 target axis 的 local relation。

**公开判别实验**  
2 × 2：两档 temperature × 两档 residence time；测 outlet conversion / yield / safety，必要时同时记录 pressure / feasibility status。

**为什么预算内可反证**  
4 个 run 可形成最小 local surface，不要求 Agent 枚举 flow-rate × geometry 全域。

**E0 pass**  
参数层 matched-prior 模板；另外加一条 FL 特异 gate：A/M 差异不能只是由接口自动改变设备体积造成的 bookkeeping artefact，必须在公开配置语义下可解释。

**状态**：**B**。

---

## FL-S：结构层——不可逆 vs reversible target pathway

**科学对象**  
连续流出口随 residence time 增长，是持续向 product 累积，还是因为 target pathway 可逆而逐渐受 equilibrium-like back reaction 限制。

**Private truth**  
当前已有真实 topology fork：

- baseline target pathway；
- 增加一个 reverse reaction 的 `reversible_target_pathway`。

**Aligned**  
给“target pathway 在当前支持域内可视作不可逆”或“存在可逆 back reaction，长 residence time 的净收益会饱和 / 回退”。

**Misspecified**  
给相反 topology。

**公开判别实验**  
当前 Q0 已给出合适设计：

- 3 temperatures × 3 residence times；
- UV 测 yield / selectivity / flow_conversion。

Participant 最小判别可只选：低/高温各做短/长 residence time 共 4 个 run。

**为什么预算内可反证**  
可逆 topology 的差异会随 residence time 积累，因此“短 vs 长”本身就是结构 signature，而不是只比较一个 endpoint。

**E0 pass**  
至少两个 direct metric 超过 `max(0.05,3σ)`；支持点空间分离；存在 duration accumulation signature；pair action/noise 完全匹配。

**状态**：**A**。当前 `work_ii_static_topology_q0.py` 已覆盖 flow task。

---

# 8. P：反应–萃取–纯化

## P-E：实体层——萃取剂 dossier 映射

**科学对象**  
四个 extractant 对 product / impurity separation 的 nominal profile。

**Private truth**  
完整 P World 中真实 feed composition 来自上游 reaction；后续 extraction / wash 使用 activity-corrected distribution、phase volume、entrainment、loss 等真实状态。

**Aligned**  
建议复用 PA 的 extractant marginal dossier，但必须新增 `reaction-to-purification` task binding；信息只描述 reference panel 的 product/impurity distribution 与 selectivity，不给整个最佳流程。

**Misindexed**  
固定两 extractant dossier 行交换。

**公开判别实验**  
为了保证 feed 可重复：

1. 使用预注册的标准 upstream reaction prefix；
2. quench 后分成独立 batches；
3. 比较被交换的两 extractant；
4. HPLC 测 organic / aqueous product 与 impurity。

第二 anchor 用另一种预注册 upstream composition（例如较高 impurity load）。

**为什么预算内可反证**  
虽然每次测试需要完整 upstream prefix，但 P 本身是高预算多阶段任务；4 个 reference batches 足以测试实体 prior，不需要完成全套深度纯化。

**E0 pass**  
两个 feed anchors 上的 extractant contrast 均可测；上游 prefix 的变异不能大到淹没 dossier 差异；物料守恒与相选择语义通过。

**状态**：**B**。底层 separation physics 可用，需把 partition dossier 正式接入 P task 并重新资格化。

---

## P-P：参数层——reference separation factor `S*`

**科学对象**  
固定 upstream composition + extractant 条件下，product 相对 impurity 的有效分离因子：

```text
S* ≈ K_product / K_impurity
```

它是 local process parameter，不是整个 extraction train 的 oracle optimum。

**Private truth**  
由当前 activity-corrected extraction / wash runtime 在 reference composition 自动计算 `S*`。

**Aligned**  
给 `log S*` 近似 band，或者“单次 extraction 在当前相比例下预计具有中等 / 高 selectivity”的定量范围。

**Misspecified**  
给相同宽度但 log-space 反射后的 band；不改变 entity dossier。

**公开判别实验**  
固定 upstream feed，改变 organic/aqueous ratio 两档；对每档做一次 extraction，测两相 product / impurity。若预算允许，再做一个小 wash 作为 holdout。

**为什么预算内可反证**  
2–3 个 stage-level experiments 就能估计 local selectivity；Participant 不需要先完成最终交付流程才能发现 parameter prior 有误。

**E0 pass**  
A 对未见相比例预测优于 M；低/high ratio 两侧均有反证；结果不能主要由 entrainment 或 sample loss 解释。

**状态**：**B**。

---

## P-S：结构层——常数独立分配 vs composition-coupled separation

**科学对象**  
决定 product / impurity 去向的 effective distribution law 是否近似“固定 K、组分独立”，还是会随 feed composition / activity / impurity load 发生系统性改变。

**Private truth（建议新增）**  
两套真正可执行的 downstream constitutive families：

- **P-S1**：composition-independent effective distribution（在限定支持域内 K 近似常数）；
- **P-S2**：activity-corrected / composition-coupled distribution（当前更接近 runtime 的复杂模型）。

两 family 必须通过 world-authoring contract 注册为 single private-physics target fork。

**Aligned**  
给真实 family 的有限说明：“分配倾向在当前支持域内近似不随 impurity load 改变”或“高 impurity load 会系统改变 product/impurity selectivity”。

**Misspecified**  
给相反 family。

**公开判别实验**  
需要显式改变 feed composition：

- 低 impurity upstream prefix；
- 高 impurity upstream prefix；
- 两者使用完全相同 extraction conditions；
- HPLC 读取两相 product / impurity。

可再加一档 wash volume 形成 interaction check。

**为什么预算内可反证**  
核心不是做更多 extraction stages，而是比较**相同 extraction 在两种 feed composition 下 apparent K / selectivity 是否保持**。4 个 batch 可形成最小设计。

**E0 pass**  
false constant-K family 即使重新拟合一个 K，也不能同时解释低/high impurity holdout；至少两个 composition anchors 出现超噪声 interaction；行为上会改变 extractant / wash 决策。

**状态**：**C**。当前 runtime 有 activity-corrected extraction，但尚缺一个正式注册、公共合同不变的 constant-K 对照 private family。

---

# 9. C：反应–结晶

## C-E：实体层——结晶溶剂 dossier 映射

**科学对象**  
四个匿名 solvent 的 nominal reaction + crystallization profile。

**Private truth**  
每个 World 固定 solvent nominal profile + residual；真实作用包括 relative solubility、nucleation tendency、crystal growth、impurity occlusion，并与真实 reaction feed / thermal history 耦合。

**Aligned**  
正确 solvent dossier 映射。

**Misindexed**  
固定两 solvent 行交换；catalyst info 保持同状态。

**公开判别实验**  
对被交换的两 solvent，使用完全相同 upstream reaction 与标准 seeded cooling schedule；final assay + particle-size measurement（如果该 task card 开放）比较 crystal yield / purity / CSD / fines。

第二 anchor 可改变 cooling severity，但不改变 solvent pair。

**为什么预算内可反证**  
2 solvent × 2 cooling anchors = 4 个完整 crystallization batches；足以检验 dossier 中溶解度/成核/生长倾向的主要方向。

**E0 pass**  
复用实体层 A-E 资格逻辑；当前仓库已经为 crystallization solvent 定义专门 descriptor whitelist。

**状态**：**A**。

---

## C-P：参数层——成核/冷却局部阈值

**科学对象**  
在固定 composition / seed policy 下，一个可实验解释的 local threshold，例如：

- 明显成核开始出现的 cooling region；或
- 在 reference seed mass 下，CSD 开始显著恶化的 cooling severity。

这里不直接泄露 PBM 内部 nucleation coefficient。

**Private truth**  
从 current PBM 对 reference context 的 sweep 自动导出 `T_nuc*` / effective cooling threshold。

**Aligned**  
给一个近似 threshold band，例如“在 reference seed mass 下，显著成核通常在某一温区以下出现”。

**Misspecified**  
给等宽但偏移后的 threshold band；保持 seed / solvent / structural claim 不变。

**公开判别实验**  
固定 seed mass，选择 3 个 crystallization temperatures：

- A band 上方；
- A/M 中间；
- M band 下方；

保持 cooling duration 统一，测 yield、particle size / CSD / fines。

**为什么预算内可反证**  
3 个 batch 可形成阈值 bracket；不需要恢复完整 nucleation/growth kinetic constants。

**E0 pass**  
阈值两侧至少一个公开 metric 有稳定 crossing；A band 对 held-out 温度的预测优于 M，且差异不由 seed mass 或 upstream composition 变化造成。

**状态**：**B**。PBM 已实现，需新增 parametric prior generator / qualification。

---

## C-S：结构层——seed-mediated nucleation–growth 是否存在

**科学对象**  
seed mass 是否只是“无关背景变量”，还是会实质改变 CSD / fines，并且 seed effect 与 cooling severity 发生 interaction。

**Private truth**  
当前 crystallization PBM 产生真实 seed × cooling response。

**Aligned**  
> 在固定 cooling 下，改变 seed mass 会改变 crystal-size quality / fines，且 seed effect 随 cooling severity 改变。

**Misspecified**  
> 在固定 cooling 下，seed mass 对 crystal-size quality / fines 近似无影响，主要由 cooling severity 决定。

**公开判别实验**  
当前已有完整设计：

- seed mass：0.001 / 0.008 / 0.015 g；
- crystallization temperature：310 / 290 / 270 K；
- 3 × 3 主 grid；
- 中等 cooling 下三 seed levels 做 noise validation。

**为什么预算内可反证**  
Participant 最小版只需固定 cooling 做 low/high seed，再换一个更强 cooling 条件复测，即可观察 seed effect 及 interaction。

**E0 pass**  
直接使用当前 structural candidate gate：axis effects、seed×cooling topology signature、noise gate、held-out disagreement、aligned blind advantage。

**状态**：**A**。

> 注意：这格测试的是 **“seed-mediated mechanistic relationship”**，不是声称当前 World 已经实现两个不同 PBM topology fork。若未来要研究“历史无关 vs 真路径依赖”两个 world family，需要另开版本并注册 private-physics fork。

---

# 10. D：反应–蒸馏

## D-E：实体层——上游催化剂 dossier 映射（v0.5）

**科学对象**  
反应–蒸馏任务中，upstream catalyst nominal activity profile 与 ID 的映射。

**为什么 v0.5 先选 catalyst**  
当前仓库已经对 `reaction-to-distillation` 提供 generic reaction catalyst / solvent dossier 和 A-E qualification 资产；但还没有一个经过同等审计的“匿名 volatility dossier”。为了不凭空制造实体知识，v0.5 先选已有科学合同。

**Private truth**  
catalyst 的 nominal activity + world residual 决定 upstream feed composition；下游 distillation 使用该真实 feed。

**Aligned**  
正确 catalyst dossier。

**Misindexed**  
固定两 catalyst 行交换。

**公开判别实验**  
两 catalyst × 两个 reaction-duration anchors；在进入 distillation 前 quench / HPLC 测 conversion / yield / selectivity。必要时用相同 distillation micro-cut 作支持，但实体 qualification 的主反证应先来自 upstream feed。

**为什么预算内可反证**  
4 个 reaction prefixes 即可检验 catalyst 信息；不必每个都完成全蒸馏流程。

**E0 pass**  
沿用 A-E reaction-to-distillation catalyst gate。

**状态**：**A**。

---

## D-P：参数层——reference effective relative volatility / cut window

**科学对象**  
固定 reference feed composition / pressure / reflux context 下的 effective relative volatility `α*`，或等价的 first-cut enrichment window。

**Private truth**  
从当前 distillation engine 在 reference feed 下计算，不直接提供 Fenske 内部所有参数。

**Aligned**  
给 `α*` 的近似 band，或“在当前 reference composition 下，轻组分相对目标组分的 enrichment strength 属于某范围”。

**Misspecified**  
给等宽但 log-space 反射后的 band；不改 catalyst/entity prior。

**公开判别实验**  
使用预注册 upstream feed：

1. 固定 reflux，做一个小 early cut；
2. 做一个 later cut 或第二 reflux setting；
3. GC 测各 fraction composition / purity。

由 enrichment 反推 effective α / cut response。

**为什么预算内可反证**  
2–3 个短切段已能明显区分高 α 与低 α 的 prior；不要求 Agent 完成全 recovery optimization 才知道参数先验错了。

**E0 pass**  
A 对 unseen cut/reflux 的 composition 预测优于 M；反证不能仅由 upstream feed 漂移引起；两侧 cut 区域均有支持。

**状态**：**B**。current VLE / Fenske runtime 已存在，需新增 public local-prior contract。

---

## D-S：结构层——constant-relative-volatility vs composition-dependent VLE

**科学对象**  
随着 pot composition 改变，effective relative volatility 是否近似常数，还是存在显著 composition dependence / non-ideal VLE。

**Private truth（建议新增）**  

- **D-S1**：当前支持域内 constant-α / near-ideal shortcut family；
- **D-S2**：composition-dependent gamma-phi / non-ideal VLE family。

> 当前正式 distillation provider 的 model card 明确更接近 constant-relative-volatility shortcut，并没有把任意 azeotropic / composition-dependent behavior 作为同一正式任务的可切换 family。因此 D-S2 必须真正实现后才能进入 benchmark。

**Aligned**  
给真实 family 的有限 claim：“在当前 composition range 内 α 近似稳定”或“α 会随 pot composition 系统变化，早段与后段分馏能力不同”。

**Misspecified**  
给相反 family。

**公开判别实验**  
必须产生不同 pot composition：

- 固定同一 upstream feed；
- early fraction + later fraction 分开保存；
- GC 测两个切段与残液 composition；
- 或使用两种预注册 feed composition，保持 column / reflux settings 一致。

若 α 恒定，两个 composition region 估计出的 α 应近似一致；non-ideal family 会呈系统性偏移。

**为什么预算内可反证**  
3–4 个分段/组成点即可检测 α 是否随 composition 漂移；关键是**独立保存 cut**，避免累计混合把结构 signal 抹掉。

**E0 pass**  
constant-α family 即使重新拟合单一 α，也不能同时解释 early + late holdout；composition-dependent family 必须改善 blind composition prediction，且差异明显超过 GC noise。

**状态**：**C**。需要新增并注册 D-specific VLE private family；在此之前该格只能 `development`，不能通过 prompt 假装存在。

---

# 11. 21 格进入正式 benchmark 的最终判定表

每个 `system × locus` 不是一次性“整体通过”，而是首先对 **W1–W5 分别资格化**。

推荐 registry：

| 字段 | 含义 |
|---|---|
| `system_id` | EC / RX / PA / FL / P / C / D |
| `world_id` | W1..W5 |
| `prior_locus` | entity / parametric / structural |
| `candidate_truth_id` | 被测 private truth / law / relation ID |
| `aligned_prior_id` | A prior frozen hash |
| `misspecified_prior_id` | M prior frozen hash |
| `public_discriminator_id` | 资格化判别实验设计 |
| `world_self_consistent` | Q1 |
| `prior_schema_matched` | Q3 |
| `identifiable` | Q4 |
| `falsifiable_within_budget` | Q5 |
| `behaviorally_relevant` | Q6 |
| `noise_robust` | Q7 |
| `status` | qualified / development / N/A |
| `evidence_bundle_sha256` | 资格化证据绑定 |

### 五世界规则

- **单个 World 失败时**：正式 Participant 运行前，可以在 development 阶段重新 author 该 World；旧失败保留在开发记录。
- **正式块开始后**：不得因为 Participant 表现差替换 World。
- 一个 `system × locus` 只有在预注册的 5 个 Worlds 全部达到该 locus 的资格门后，才称 **5-world qualified**。
- 若反复开发后确认某 World / locus 天然无法可辨识，可以在正式冻结前将该格登记为 `N/A`；不能拿一个弱代理填满矩阵。

---

# 12. 建议的实际开发顺序

## Phase 1：优先复用已有 qualification 资产

1. EC-E / EC-P / EC-S
2. RX-E / RX-P / RX-S
3. PA-E / PA-S
4. C-E / C-S
5. FL-S
6. D-E

这些单元已有较直接的 dossier / matched-prior / structural-Q0 代码资产。

## Phase 2：只需新增 prior generator 与 E0 block

1. PA-P
2. FL-E / FL-P
3. P-E / P-P
4. C-P
5. D-P

## Phase 3：真正新增 private-physics family

1. P-S：constant-K vs composition-coupled extraction / wash law
2. D-S：constant-α vs composition-dependent VLE

这两个不能先写 prompt 再说“结构层已完成”；必须从 world-authoring contract 开始实现、审计、replay、public-contract invariance 和 divergence qualification。

---

# 13. 当前最重要的设计结论

这 21 格不应该被看作 21 个“随便想一个错误先验”的 prompt 模板，而应该看作 21 个**受控科学干预**：

```text
Entity：谁的属性属于谁？
        ↓
必须有材料表型实验能验证

Parametric：同一模型下，局部定量关系往哪边走？
        ↓
必须有低侧 + 高侧实验能反证

Structural：到底是哪一种关系 / 机制结构？
        ↓
必须有 discriminative intervention，且另一结构不能靠重新调参数把差异完全吃掉
```

因此实验 1 的开发目标不是“把 21 格写满”，而是：

> **让每一个进入正式矩阵的格子，都同时满足：真实、匹配、可辨识、可反证、有后果。**

只有这样，后面 Opaque / Aligned / Misspecified 的任何差异才有清晰科学解释。
