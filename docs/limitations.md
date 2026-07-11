# 适用范围与限制

ChemWorld-Bench 面向预算受限、部分可观测的闭环实验决策研究。它不是现实产率预测器、分子模拟器、
商业流程模拟器、实验机器人控制软件或安全决策系统。

## 可以声明

- task、scenario、mechanism、provider、observation、scoring 与 trajectory 有版本化合同；
- Agent 通过公开操作、测量、成本、风险和历史记录与环境交互；
- 正式 runtime route 使用显式 provider，不依赖旧的通用 proxy/fallback；
- 轨迹可以执行 digest 校验、确定性 replay、指标重算和 score 绑定；
- 经典、RL 和 LLM 方法可使用统一的实验与资源账本；
- 最新四任务经典诊断完整重放，并观察到目标收益与风险变化同时存在。

## 不可以声明

- 输出能预测或指导真实反应、分离、谱图、装置设计或危险实验；
- `reference_validated` 或 `professional_candidate` 等于工业、法规或实验验证；
- 无 proxy route 等于全部物理模块已达到专业精度；
- 四任务目标改善证明 structured GP 在完整约束下优于 random；
- Safe-GP 的一次边界确认等于已证明完整方法优越性，或 PPO、SAC、live LLM 已完成正式排名；
- public seeds 上的结果证明跨机理或私有世界泛化；
- 当前候选包是正式发表级 benchmark release。

## 模型边界

- reaction kinetics 是局部虚拟机制和速率律，不是数据库级反应预测；
- 物性、分配、设备和材料效应是版本化 benchmark 参数，真实名称不自动带来现实精度；
- HPLC、GC、UV–vis、IR、NMR、MS 与 final assay 是状态耦合的合成观测，不预测真实样品谱图；
- 平衡、电化学、结晶、流动和蒸馏只在各模型卡的窄适用域内解释；
- cost/risk 是虚拟任务约束，不是采购报价、职业健康或法规指标；
- 整体任务成熟度按最弱必需模块聚合，当前注册任务仍为 `lite`；
- 电化学和平衡任务尚未证明主指标对自适应探索具有稳定可辨识性。

## 评价边界

0.3 经典比较在新数据前预注册了安全和成本非劣界限。普通 GP 的目标与成本通过但三项安全失败。
随后 Safe-GP 在另一未触碰 cohort 上使四项 safety/cost 全部通过，说明峰值风险标签与约束
acquisition 修复了已观察到的安全退化；但连续流目标效应 0.018752 未达到 SESOI 0.020000，完整
比较仍被正确拒绝。项目仍缺少四任务联合通过、跨机理/私有世界验证和独立外部复现。

现有经典方法主要根据完整实验的 final assay 更新下一配方。它们不使用谱图特征，也不在同一次
实验内根据中间测量调整动作，因此应称为 recipe-level active learning，而不是闭环实验室控制。

## 发布边界

当前状态是 `benchmark_candidate`。正式发布仍需：改进策略后的新未触碰 cohort 联合通过、完整 RL/LLM 矩阵、
机理族 Train/Dev/Bench、独立 reference search、salted private evaluation、第三方复现和干净 wheel
验证。任何环境、观测、评分或约束变化都会提升合同版本并触发新运行；历史证据不会被静默改写。
