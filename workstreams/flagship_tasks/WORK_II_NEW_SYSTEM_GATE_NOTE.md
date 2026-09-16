# W2-117：未完成新任务资格的五体系首轮 gate 实测

日期：2026-09-16。身份：development。一次固定覆盖，单 executor；不调用模型、不启动正式来源，不修改平台物理语义。这里的“新体系”指近期 P/C/D 与 EC 自主试跑之外、尚未完成 W2-115 定制任务资格的 RX/EQ/BC/PA/FL，不声称平台从未运行过它们。

问题：现有真实入口能否承接这五张卡的三臂资料和预算内多批取证；公开测量是否有足够的可控响应及成对世界差异？这是一轮必要条件筛查，不代替完整 G-S/G-R 或 Agent 能力评估。

## 固定覆盖与资源

1. 每体系 O/A/M 各一次环境构造及 reset，共 **15 个资料入口检查**。使用现有 `material_information` 入口；M 仅交换 solvent 描述 0/1，其余不变。失败原样保留，不另换任务 ID；有三臂时比较公开操作/仪器/预算权限。不将旧 nominal dossier 自动认作新卡科学上正确的 Aligned 先验。
2. **8 个独立多批参考 campaign、30 个计划化学批次**：五体系各一个基础世界；EQ/PA/FL 各增加一个受控规律变化世界。RX/BC 当前不在机制家族干预注册表，标为接口缺口，不捏造变体。所有参考是事前固定的可公开执行操作序列，不访问隐藏参数选点，世界变化只由评价端设置。
3. 采用 task 默认操作上限 RX36/EQ24/BC18/PA48/FL60；每个 campaign 共用物料/仪器/容器账本，不能按批刷新。RX/EQ/PA/FL 各4批、BC2批；非终检次数分别8/8/4/8/4，终检与容器数等于计划批数。每批物料上界乘批数：试剂0.04mol、溶剂0.08L、催化剂0.005mol、相液/萃取剂各0.06L；过程时间每批7200s。stock limits 是资格参考预算，不冻结正式 Agent 预算。
4. 所有世界使用同一个预定公开开发实例序号；具体初始化、观测种子及完整执行参数留在 ignored run plan。基础和变化世界同初始化、同 keyed noise 配置；每条件一次，无噪声重复、搜索、provider 重试。

| 卡 | 固定批次（按列出顺序） | 每批操作/仪器 | 变化世界 |
| --- | --- | --- | --- |
| RX | (335K,30s)、(385K,30s)、(335K,300s)、(385K,300s) | 溶剂0.028L/索引2、试剂0.010mol、催化剂0.00025mol/索引1；heat→HPLC→同长wait→UV→terminate→final，共9步 | 不运行未注册变体 |
| EQ | (0.020L,0.002mol)、(0.060L,0.002mol)、(0.020L,0.010mol)、(0.060L,0.010mol) | 溶剂索引0、试剂；pH→UV→terminate→final，共6步 | equilibrium.acid-base-constants / extrapolation / severity=1 |
| BC | (345K,120s)、(385K,120s) | 与RX同投料和9步，heat后wait60s；两批共18步 | 不运行未注册变体 |
| PA | (extractant1,0.006L)、(extractant3,0.006L)、(extractant1,0.024L)、(extractant3,0.024L) | 溶剂0.025L/索引1→水相0.018L→萃取剂→mix240s/750rpm→settle360s→HPLC→选organic→HPLC→terminate→final，共10步 | partition.distribution-coefficient / extrapolation / severity=1 |
| FL | (0.6mL/min,300s,340K)、(0.6,300,390)、(1.8,1200,340)、(1.8,1200,390) | 溶剂0.026L/索引2、试剂0.010mol、催化剂0.00022mol/索引1→配置→run_flow(2倍停留时间)→HPLC→terminate→final，共8步 | flow.reaction-kinetics / extrapolation / severity=1 |

FL 的流量/停留时间组合改变设备几何；不宣称固定反应器独立调两旋钮，不把名义 throughput 当产品量。RX/BC 的 UV 与 HPLC 是付费观测，终检单独扣费。所有后测仅由机器分析记录，不回流给参考策略。

## 事前判定、分母与停止

- **I 入口兼容**：15次逐项记录构造/reset成功与错误。体系级 I 要求三臂均能构造，O无实例dossier、A/M有且不同、操作/仪器/预算一致。它只验证旧适配器兼容，不验证先验内容真伪。
- **R 多批运行**：8 campaigns 各自全部计划动作 committed、预定终检数完成、无提前截断；报告终检完成/30及campaign完整/8。失败批次后不继续消耗该campaign，其他独立campaign仍运行。
- **L 资源**：逐事件公开账本操作/容器/仪器/stock累计单调；末态计数与全部记录重算一致，stock增量由committed加料重算，且不超该card。终检后的新批必须继承已有消耗。8个campaign独立判定。
- **X 重放**：每个已产生轨迹的campaign执行一次 `verify_records(tolerance=0)`，传入同世界干预；完整轨迹/失败前缀分开报告。重放属于验证开销，不算新独立科学批次。
- **S1 公开响应筛查**：用终检带噪公开值和公开 final-assay noise_std。预定相邻配对 RX/EQ/PA/FL 为(批1,2)和(批3,4)，BC为(批1,2)。只在预定主通道中寻找一个两次重复对比都超过 `3*sqrt(sigma1²+sigma2²)` 的通道（BC仅一对）；阈值同时至少0.02（归一化pH至少0.01）。RX/BC通道yield/conversion/byproduct_signal；EQ为pH_normalized/acid_dissociation_fraction/precipitation_signal；PA为product_in_organic/product_in_aqueous；FL为flow_conversion/yield。每体系基础世界一次判定，共5。另报告所有因子对比的连续差异，不以噪声异常改点。此筛查非多重比较校正检验，不证明结构可辨识；EQ浓度效应弱可合理失败。
- **S2 成对世界筛查**：EQ/PA/FL各一次；同一主通道至少2/4相同操作条件的世界间差异越过上述阈值，且相关campaign运行/资源/重放通过。仅证明该预定范围的世界响应可分，不等于有限数据识别唯一机理或验证M反证。
- 体系级“基础筛查通过”=基础世界R/L/X/S1全部通过（分母5）；“现有入口与基础筛查同时通过”另计I的合取。S2分母3；RX/BC为未接入，不混入3。完整G-S/G-R仍须任务相关留出预测/可达性、先验内容核验及自由报告K1/Q/K2真实链；G-J未测、G-F开发不适用。
- FL额外连续报告四点的flow_conversion/yield/risk；以conversion≥0.50、yield≥0.10、risk≤0.35作本轮示例可行判定，必须出现可行与不可行两类才称“窗口边界已覆盖”。这不是正式任务阈值。PA含量指标与质量守恒真值不能混为一谈；本轮不声称通过完整质量守恒资格。
- 每campaign失败一次即终态，不换点/阈值/初始化/预算。任何平台语义修复另立后续开发块，保留本轮。脚本分析/计数缺陷只重算已有记录，不重跑物理。

输出：ignored `runs/development/work-ii-new-system-gates-20260916/` 内保留启动前plan、轨迹、资源与重放；生成 `reports/work-ii-new-system-gates-20260916.json` 和 `.md`，含全部失败与确切分母。运行每分钟内输出stage、完成/8、操作活性、吞吐与ETA。预计纯模拟和重放为分钟级至几十分钟，实际报告计时；零模型调用，不能据此外推Astra来源耗时。
