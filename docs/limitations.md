# 适用范围与限制

ChemWorld-Bench 面向部分可观测、预算受限的闭环实验决策研究。它不是现实产率预测器、分子模拟
器、商业流程模拟器、实验机器人控制软件或安全决策系统。

## 当前可以声明

- task、scenario、mechanism、provider、scoring 与 trajectory 有版本化合同和摘要；
- Agent 只能通过公开 observation、instrument result、cost/risk 与历史轨迹作决策；
- v0.4 runtime 已接入 LLE、干燥、浓缩、转移、结晶、蒸馏、流动和电化学窄域 provider，旧正式
  proxy/fallback route 已移除；
- 经典方法正式矩阵可回放，结构化 GP 在分配、结晶、蒸馏和流动任务上显示跨公开新 seed 与
  salted private shift 一致的正向证据；
- 基础 exploit 检查通过，private salt 原值不进入报告或版本库。

## 当前不可声明

- 输出能够预测或指导真实反应、分离、谱图、装置设计或危险实验；
- `reference_validated`、`professional_candidate` 或 provider 接入等于工业、法规或实验室验证；
- 六个 serious task 已全部通过科学有效性验证；
- 当前安全风险信号足以评价 safe BO 或真实安全决策；
- seed shift 等同于独立的参数外推、组成变化或观测噪声泛化；
- 已完成 RL、真实 LLM、SOTA 排名、第三方复现或发表级 release；
- leaderboard 分数代表现实实验成功概率。

## 模型与观测限制

- reaction kinetics 是局部机制和速率律，不是数据库级真实反应预测；
- 分配系数、设备参数和物性切片为 benchmark 校准值，使用真实物料名不会自动提高真实性；
- 合成 HPLC、GC、UV–vis、IR、NMR、MS 与 final assay 是状态耦合观测，不是真实谱图预测；
- 水相平衡、电化学、结晶、流动和蒸馏只覆盖各模型卡声明的窄域；
- cost/risk 是虚拟任务约束，不是采购报价、职业健康或安全合规结论；
- 当前 world-family 缺少可独立控制的完整 OOD 轴，不能把不同 seed 的稳定性扩大解释为机制泛化；
- 电化学与平衡任务的主指标尚未显示稳定的自适应收益；正式经典矩阵存在非零连续风险，但安全
  阈值从未被触发，不能辨识安全约束方法。
- 当前正式方法只从完整实验的 final score 更新，不使用中间谱图或进行实验内闭环调整；历史
  DeepSeek 与扩展经典方法结果缺少保留的正式 artifact。

## 发布状态

当前公开状态是 `candidate_backend_only`，不是 `validated benchmark`。冻结 v0.1 方法证据不会因
后续任务整改而被覆盖；任何会改变环境、观测、评分或风险信号的修订都进入新合同和新协议。

在正式发布前，项目仍需完成任务接受/降级决策、独立 world-family 轴、语义不变性、公开接口
harness、扩展 exploit、资源对齐的方法矩阵和第三方干净安装复现。达到这些门禁后，发布包才会
获得可引用 tag 和明确的 benchmark claim。
