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
- 当前已完成 safe BO、PPO、SAC、live LLM 或 SOTA 排名；
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

最新经典诊断显示，目标改善可以伴随更高风险预算超限率。这证明只看 objective 会产生错误结论，
也说明“风险字段存在”不等于评价系统已完成：安全和成本非劣界限必须在新数据前预注册，并进入
联合决策规则。

现有经典方法主要根据完整实验的 final assay 更新下一配方。它们不使用谱图特征，也不在同一次
实验内根据中间测量调整动作，因此应称为 recipe-level active learning，而不是闭环实验室控制。

## 发布边界

当前状态是 `benchmark_candidate`。正式发布仍需：新 cohort 上的约束确认、完整 RL/LLM 矩阵、
机理族 Train/Dev/Bench、独立 reference search、salted private evaluation、第三方复现和干净 wheel
验证。任何环境、观测、评分或约束变化都会提升合同版本并触发新运行；历史证据不会被静默改写。
