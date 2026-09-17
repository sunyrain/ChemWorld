# ChemWorld 实验 1：七体系、35 Worlds 与 21 格先验资格化设计规范（v1.0）

> **版本定位**：这是“实验设计规范 v1.0”，用于统一后续 world authoring、prior generation、qualification 与正式执行。  
> **v1.0 不等于“35 个 World 已经全部跑完资格化”**；尚未完成的物理 fork 或资格化运行必须在状态栏中显式标记为 `development / pending`，不得把未运行结果写成已通过。  
> 从本版开始，不再以 v0.x 继续扩展概念框架；后续修改按 `v1.1 / v1.2 ...` 记录。

## v1.0 冻结的核心原则

1. 七个主体系固定为 **EC / RX / PA / FL / P / C / D**。
2. 每个体系开发 5 个底层 private Worlds，共 **35 个真实隐藏世界**。
3. World 是完整、合理、内部自洽的真实物理实例；**不是噪声 seed，也不是错配方式**。
4. 三类先验层固定为 **实体层 / 参数层 / 结构层**。
5. 三个先验臂固定为 **Opaque / Aligned / Misindexed(Misspecified)**。
6. 三层先验以 21 个 `体系 × 先验层` 为目标设计空间，但每一格必须逐格资格化；不为矩阵整齐性伪造不可辨识任务。
7. 发现/优化不再自动乘二。只有当“改变科学委托”本身是明确研究问题时，才预注册同世界任务配对。
8. 正式 Participant 运行前，World、prior、预算、qualification gate 与执行 manifest 必须冻结。
9. `Aligned` 已经给出的知识不能再被记为“从零发现”；正式分析必须区分初始已知与实验新增认识。
10. private truth 必须由可执行 simulator law 决定；任务层最优点、结构标签等尽量由底层参数自动推导，而不是与底层参数双重手填。

---



## v1.0 状态说明

本文件中的 21 格具有三种实现状态：

- **A：已有资产**——当前仓库已有高度一致的 private law / prior / qualification 资产，但仍需在新 5-world protocol 下重新冻结；
- **B：可直接开发**——底层物理与公开实验空间基本存在，主要缺正式 prior generator 或 qualification block；
- **C：需新增 private-physics family**——必须先新增真实 simulator fork，不能只靠 prompt 声称存在另一机制。

因此，本版可以直接作为开发和资格化的 **1.0 设计规范**。后续资格化运行结果作为 v1.x 的状态更新写入，不再为了“还没跑完”把科学设计本身停留在 v0.x。


---

# 0. 最终对象与层级

## 0.1 七个体系

| 代码 | 体系 | 当前建议主任务 | 主导性质 |
|---|---|---|---|
| EC | 电化学有效转化 | 在电荷、能耗和选择性约束下建立有效转化方案 | 工程优化为主，同时可形成电化学响应知识 |
| RX | 反应—热过程 | 解释目标生成、竞争转化和真实温度历史 | 规律/机制辨识为主 |
| PA | 相间分配 | 建立可预测两相物料去向的关系 | 规律发现为主 |
| FL | 连续流 | 识别满足反应表现、热、压力和设备约束的运行窗口 | 可行域/操作窗口发现 |
| P | 反应—萃取—纯化 | 在纯度和资源约束下交付尽可能多的目标产物 | 顺序工艺优化 |
| C | 反应—路径依赖结晶 | 在纯度和粒径要求下交付新增晶体 | 路径依赖工艺优化 |
| D | 反应—分段蒸馏 | 选择切段、保存和停止策略，回收合格馏分 | 顺序工艺优化 |

> 本实验暂不把 **有界水相平衡 EQ** 与 **有限预算表征 BC** 纳入七体系主矩阵。它们可保留为后续独立任务或支持实验，但不与 PA 混成一个模糊“平衡/表征”体系。

## 0.2 35 个底层 World

每个体系构造 5 个真实隐藏规律实例：

\[
7\ \text{systems}\times5\ \text{worlds}=35\ \text{private worlds}.
\]

World 是一套完整、科学合理、内部自洽的隐藏物理世界。它固定：

- 真实 mechanism family；
- 真实隐藏参数；
- 真实材料—性质关系；
- 初始状态；
- 仪器映射与噪声合同；
- 安全、资源与成本参数；
- 可执行操作语义。

**World 不因 Opaque / Aligned / Misindexed 改变，也不因“发现/优化”任务措辞改变。**

## 0.3 三层先验干预

| 先验层 | 操纵对象 | 典型错误 |
|---|---|---|
| 实体层 | 材料身份与性质档案的对应关系 | `material-M1` 被赋予 `M3` 的性质档案 |
| 参数层 | 已给定关系中的局部定量参数、窗口、阈值或系数 | 最优温度、电位窗口、分配强度、停留时间等发生可信偏移 |
| 结构层 | 函数形式、过程依赖、机制 family 或拓扑 | 平台型 vs 峰型、单一路径 vs 竞争路径、历史无关 vs 路径依赖 |

三层先验是三种独立信息干预。它们不是三个任务，也不是三个不同 World。

## 0.4 三个先验臂

每个已资格化的 `任务 × World × 先验层` 都运行：

| Arm | 含义 | 固定不变 |
|---|---|---|
| Opaque | 不提供该层实例级规律提示 | World、公共科学背景、操作/仪器合同、资源、任务目标 |
| Aligned | 提供该层与真实 World 一致、但非 oracle 的有限先验 | 同上 |
| Misindexed / Misspecified | 提供格式、精度、语气和置信度与 Aligned 匹配，但内容错误的先验 | 同上 |

---

# 1. World 与 seed、先验错配的关系

World 可以由 deterministic seed 生成，但 **seed 只是生成钥匙，World 才是生成后的真实隐藏规律实例**。

例如 `EC-W3` 可以由固定 seed 编译出：某套真实材料响应、电子转移动力学、欧姆损失、副反应强度和观测噪声映射。这个 World 随后被所有相关 O/A/M 会话共享。

“实体错配方式”不是 World。一个 World 可以冻结一套实体错配置换；如果研究者未来想把不同错配方式本身作为实验变量，那应当显式增加一维 `misindex_pattern`，不能把它冒充为五个 Worlds。

---

---

# 1. World 与 seed、先验错配的关系

World 可以由 deterministic seed 生成，但 **seed 只是生成钥匙，World 才是生成后的真实隐藏规律实例**。

例如 `EC-W3` 可以由固定 seed 编译出：某套真实材料响应、电子转移动力学、欧姆损失、副反应强度和观测噪声映射。这个 World 随后被所有相关 O/A/M 会话共享。

“实体错配方式”不是 World。一个 World 可以冻结一套实体错配置换；如果研究者未来想把不同错配方式本身作为实验变量，那应当显式增加一维 `misindex_pattern`，不能把它冒充为五个 Worlds。

---

---

# 2. 三层先验从“强制全交叉”改为“目标全覆盖 + 逐格资格化”

## 2.1 目标全覆盖是什么意思

我们的设计目标仍然是让七个体系尽可能都支持：

\[
\text{实体层} + \text{参数层} + \text{结构层}.
\]

也就是形成 21 个 `system × prior-locus` 设计单元。

但 **不能为了得到整齐的 21 格而硬造一个不科学、不可辨识或没有行为后果的先验干预**。

因此每一格必须先开发、再资格化：

\[
\text{候选干预}\rightarrow\text{World qualification}\rightarrow\text{正式进入矩阵或返回重设计}.
\]

如果某一格暂时不合格，优先调整 World 参数、实验支持域或 false hypothesis；只有确认该体系天然不适合该层后，才把它登记为 N/A，而不是用一个弱代理硬填。

## 2.2 资格化的共同七项要求

| 资格项 | 必须证明什么 | 失败时怎么办 |
|---|---|---|
| Q1 世界自洽 | 质量/电荷/状态传播、操作和观测语义内部一致，可重放 | 修世界；不能进入正式实验 |
| Q2 任务可达 | 在公开合法操作和预算内，至少存在合理完成任务/获得有效信息的路径 | 调整任务、预算或 World 参数 |
| Q3 先验对称 | A/M 在字段、长度、精度、措辞、置信度上匹配，只在目标内容上不同 | 重写先验模板 |
| Q4 可辨识 | A 与 M 对应的 competing hypotheses 在公开实验空间中产生可区分结果 | 调整参数、支持域或机制 family |
| Q5 预算内可反证 | 存在至少一组合法实验，使 Agent 在给定预算内有机会获得公开反证 | 增加合理测量机会或重设计 World |
| Q6 有行为后果 | 错误先验在至少部分合理策略下会改变实验选择、操作窗口或任务结果 | 调整干预强度；否则干预科学价值不足 |
| Q7 噪声稳健 | 区分度不是单个 noise seed 的偶然结果；在预定噪声重复下仍成立 | 调整信号/噪声或不纳入正式块 |

> **“物理上能跑”不等于“是一个合格 benchmark World”。** 资格化的核心是：World 自洽、任务成立、错误先验可信、且公开实验真的能够区分相关假设。

---

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

---

# 4. 五个 World 的角色：不是五种错配，而是五套真实规律

每个体系仍建议开发 5 个 Worlds，但角色用于覆盖真实规律分布，而不是定义 5 种错误先验。

| World | 真实世界设计角色 | 说明 |
|---|---|---|
| W1 | 中央参考 | 参数居中、关系清楚、最容易检查 world authoring 是否正确 |
| W2 | 定量偏移 | mechanism family 可保持不变，但关键定量窗口明显移动 |
| W3 | 机制替代 | 使用另一种真实 mechanism family，避免结构答案永远相同 |
| W4 | 强耦合 | 多因素耦合更强、决策更难，但仍需保持可辨识 |
| W5 | 边界稳健 | 位于较窄窗口、较低信号或边界区域，用于测试稳健性，但不得不可识别 |

正式数值由每个体系独立 authoring。`V*`、最优温度、最佳停留时间等任务层结论应尽量由底层物理参数通过 simulator sweep 自动推导，而不是与底层参数同时人工指定。

---

---

# 5. 七体系的主任务与三层先验设计目标

| 体系 | 主任务 | 实体层候选 | 参数层候选 | 结构层候选 |
|---|---|---|---|---|
| EC 电化学 | 受约束有效转化 | 材料/介质与响应 dossier 的映射 | 有效工作电位/电流窗口 | 平台型 vs 峰型；动力学主导 vs 传质/欧姆耦合型 |
| RX 反应—热过程 | 反应/热历史辨识 | 催化剂或反应介质 dossier | 有效温度/停留时间/失活窗口 | 串联 vs 并联竞争；可逆/不可逆；热耦合拓扑 |
| PA 相间分配 | 两相物料去向规律发现 | 萃取剂/溶剂 dossier | 分配强度、有效分配系数或相比例响应 | 线性/幂律/饱和/缔合型 constitutive law |
| FL 连续流 | 运行窗口识别 | 催化/介质/装置材料 dossier | 有效停留时间、温度或流量窗口 | 动力学控制 vs 传质/热边界控制；单调 vs 饱和/抑制 |
| P 纯化 | 受约束目标产物交付 | 萃取剂/洗涤介质 dossier | 分配/洗涤净收益/损失系数 | 独立分配 vs 组成耦合；单调洗涤收益 vs 非单调损失 |
| C 结晶 | 受约束新增晶体交付 | 溶剂/晶种 dossier | 成核温度、过饱和阈值、有效冷却窗口 | 历史无关 vs 路径依赖；自发成核 vs seed-mediated pathway |
| D 蒸馏 | 分段切馏与回收 | 组分/溶剂挥发性质 dossier | 有效相对挥发度、切段窗口 | 固定相对挥发度 vs 组成依赖 VLE；近理想 vs 非理想分馏 |

这张表是 **authoring target**，不是“21 格已经全部实现”的声明。每格状态应明确记录为：`qualified / development / N/A`。

---

---

# 6. 发现/优化不再自动乘二：改为预注册任务配对

## 6.1 原则

同一体系默认只有一个主任务。所有来源在任务结束后都可以提交任务相关的科学解释和预测，因此“要求解释机制”本身不构成第二个独立来源任务。

只有当研究问题明确是：

> **把同一个真实世界委托成“理解规律”还是“完成工程目标”，是否会改变 Agent 的实验选择和知识形成？**

才增加第二种任务委托，并形成同一 World 的配对会话。

## 6.2 当前预注册候选

| 体系 | 主任务 | 配对第二任务 | 当前建议 |
|---|---|---|---|
| RX | 反应—热过程辨识 | 在热/安全/资源约束下形成可靠合成方案 | **强烈建议预注册** |
| C | 合格晶体交付 | 辨识组成、播种和热历史对晶体群的作用 | **强烈建议预注册** |
| EC | 受约束有效转化 | 纯规律辨识式电化学响应研究 | 可作为第三候选，但先做独立 qualification |
| PA / FL / P / D | 各自主任务 | 暂不默认第二任务 | 若未来有独立科学问题再新增 |

任务配对必须满足：

- 使用同一个 private World；
- 相同工具、操作合同、初态和资源上限；
- 只改变任务委托/主要目标，不共享实验轨迹；
- 两个委托在该 World 上都必须独立有意义且可完成；
- 执行顺序随机化或平衡；
- 不允许因为某一主任务结果不好，事后给它补第二任务。

---

---

# 7. 实验数量：从固定 450 改成“资格化后按实际矩阵计数”

## 7.1 主任务理论上限

若七体系 × 五 Worlds × 三层先验全部通过资格化，并且每个体系只运行一个主任务，则：

\[
7\times5\times3\ \text{prior loci}\times3\ \text{arms}
=\boxed{315\ \text{source sessions}}.
\]

这是 **目标全覆盖的上限矩阵**，不是在资格化之前就必须完成的固定样本量。

## 7.2 配对任务增量

一个体系若在全部 5 Worlds、全部 3 先验层上增加一个第二任务，则新增：

\[
5\times3\times3=45\ \text{sessions}.
\]

因此：

- 主任务全覆盖：315；
- RX + C 两个预注册任务配对若均全覆盖：`315 + 45 + 45 = 405`；
- 若 EC 未来也通过第二任务资格并全覆盖：`405 + 45 = 450`。

但正式计数应采用一般式：

\[
S = 3\times\sum_{u\in U_{qualified}} 1,
\]

其中每个 `u` 是一个已经资格化的 `task × world × prior-locus` 单元。这样不会为了凑整齐数字，把不成立的实验强行加入正式分母。

---

---

# 8. 35 个 World 的开发与冻结流程

每个体系按以下顺序开发：

```text
科学原型与公共背景
        ↓
定义底层 mechanism family
        ↓
定义 private physical parameters
        ↓
编译 5 个真实 Worlds
        ↓
Simulator sweep / replay
        ↓
自动推导 observable truth
        ↓
为实体/参数/结构三层分别构造 A/M candidate prior
        ↓
逐格 qualification
        ↓
通过：进入正式矩阵
失败：调整 World / hypothesis / 支持域后重新资格
        ↓
冻结 world_id、truth hash、prior package 和 public contract
```

开发阶段可以修改 World；一旦进入正式块，不能根据 Agent 表现改变 World、干预强度或 qualification 阈值。

---

---

# 9. 每个 World 的 machine-readable 最小合同

建议最终每个 World 固定以下字段：

```yaml
world_id: EC-W03
system_id: EC
world_role: strong_coupling
truth_hash: ...

private_truth:
  mechanism_family: ...
  mechanism_parameters: ...
  material_realized_properties: ...
  initial_state: ...
  observation_noise_model: ...
  safety_and_resource_parameters: ...

public_contract:
  common_scientific_background: ...
  operations: ...
  instruments: ...
  legal_domains: ...
  budgets: ...

prior_loci:
  entity:
    status: qualified|development|N/A
    target_object: ...
    aligned_package: ...
    misindexed_package: ...
    qualification_record: ...
  parametric:
    status: qualified|development|N/A
    target_parameter: ...
    aligned_package: ...
    misspecified_package: ...
    qualification_record: ...
  structural:
    status: qualified|development|N/A
    true_family: ...
    false_family: ...
    aligned_package: ...
    misspecified_package: ...
    qualification_record: ...

tasks:
  primary:
    task_id: ...
    status: qualified
  paired_optional:
    task_id: ...
    status: preregistered|development|N/A
```

---

---

# 11. 21 格总览与逐格 Qualification Specification

| 体系 | 实体层 | 参数层 | 结构层 | 当前状态概览 |
|---|---|---|---|---|
| **EC 电化学** | 电解液 dossier 映射 | 电位–电流 local window | 高电流 transport limitation 是否存在 | A / A / A |
| **RX 反应–热过程** | 催化剂 dossier 映射 | 温度–时间 local relation | 催化剂失活 vs 稳定催化剂 | A / A / A |
| **PA 相间分配** | 萃取剂 dossier 映射 | 有效分配强度 / `K*` | linear vs power constitutive law | A / B / A |
| **FL 连续流** | 催化剂 dossier 映射 | 温度–停留时间 local window | 不可逆 vs reversible target pathway | B / B / A |
| **P 反应–萃取–纯化** | 萃取剂 dossier 映射 | reference separation factor | 常数独立分配 vs composition-coupled separation | B / B / C |
| **C 反应–结晶** | 结晶溶剂 dossier 映射 | 成核/冷却 local threshold | seed-mediated nucleation–growth 是否存在 | A / B / A |
| **D 反应–蒸馏** | 催化剂 dossier 映射（v1.0 首选） | effective relative volatility / cut window | constant-α vs composition-dependent VLE | A / B / C |

> v1.0 为了避免“为了体系名字好看而引入未经验证的材料属性”，D 的实体层先选当前仓库已有审计基础的 **上游催化剂 dossier**。未来如果真正实现匿名挥发性材料 dossier，可再版本升级为 D-specific entity locus。

---

# 12. EC：电化学有效转化

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

# 13. RX：反应–热过程

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

# 14. PA：相间分配

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

# 15. FL：连续流

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

# 16. P：反应–萃取–纯化

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

# 17. C：反应–结晶

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

# 18. D：反应–蒸馏

## D-E：实体层——上游催化剂 dossier 映射

**科学对象**  
反应–蒸馏任务中，upstream catalyst nominal activity profile 与 ID 的映射。

**为什么 v1.0 先选 catalyst**  
当前仓库已经对 `reaction-to-distillation` 提供 generic reaction catalyst / solvent dossier 和 A-E qualification 资产；但还没有一个经过同等审计的“匿名 volatility dossier”。为了不凭空制造实体知识，v1.0 先选已有科学合同。

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

# 19. 21 格进入正式 benchmark 的最终判定表

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

---

# 20. 实施顺序

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

---

# 21. v1.0 最终结论

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