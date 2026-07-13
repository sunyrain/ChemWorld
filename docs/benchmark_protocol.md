# 设计一场公平评测

!!! warning "旧数值只作诊断"
    本页引用的经典优化、Safe-GP 与 SAC 数值均为 pre-v0.5 diagnostic。它们展示如何冻结规则和解释失败，不是当前后端上的正式排名。

这一页回答的是：**怎样比较两个 Agent，才不会把更多预算、更多信息或更高风险误写成算法进步。**
协议覆盖任务选择、数据划分、资源、统计、回放与发布。ChemWorld 逐任务报告结果，不用一个跨物理
域的总分掩盖指标单位和失败模式的差异。

!!! tip "第一次做评测时，先固定五件事"
    任务、完整实验预算、Agent 可见信息、Train/Dev/Bench 划分，以及失败如何计入结果。

## 先选择评测范围

- `core`：API、轨迹、回放和发布链路的紧凑回归套件；
- `serious`：六个研究候选任务，不自动构成已验证 benchmark；
- 显式任务列表：用户自选实验，不继承套件级主张。

```bash
chemworld tasks list
chemworld tasks readiness
chemworld baselines report --preset core
```

## 把开发数据与最终评测分开

| Split | 用途 | 是否用于选模型 |
| --- | --- | --- |
| `public-dev` | 调试接口、训练与开发 | 可以 |
| `public-test` | 冻结的公开诊断和回归 | 不应反复调参 |
| `private-eval` | 隐藏世界和泛化评测 | 不可以 |

所有 split 共享同一世界律和公共操作语义。私有 salt、机理参数、隐藏物种量和评测 seeds 不进入
observation、Agent trace 或公开结果。正式训练方法必须在 Train 上学习、在 Dev 上选择，并只在
Bench/Private 上执行一次冻结评测。

## 明确你在数什么

```text
Campaign  一次 task × world × seed × method 运行
└── Experiment  一条从初态到合法终检的实验流程
    └── Operation  单步操作、测量或控制动作
```

方法预算以**完整实验数**为主，操作数、测量数、墙钟、CPU/GPU、模型请求、token、费用和训练
环境步数作为并列资源记录。提前结束、失败请求、JSON 修复和重试都计入账本。

## 不要只看最终分数

每条运行分别产生四类证据：

1. **任务目标**：逐任务主指标、best-so-far 和预算—收益曲线；
2. **约束**：逐实验最大 operational risk、风险预算超限、成本和非法动作；
3. **资源**：完整实验、操作、测量、计算、模型调用和费用；
4. **有效性**：策略是否真的更新、是否使用观测、是否完成预算、结果是否可回放。

在线 reward 只用于学习和诊断，不是主终点。正式结果从轨迹终检记录重算。

## 在看结果前写下决策规则

目标改善不是充分条件。未来确认协议必须在看见新 cohort 结果前逐任务冻结：

- 主指标方向和最小有意义效应（SESOI）；
- 安全非劣界限；
- 成本或资源非劣界限；
- 配对 seeds、实验预算和停止规则；
- bootstrap 样本数、显著性水平和 Holm 校正族；
- 缺失、失败、超时和非有限值的处理方式。

完整主比较只在目标、约束、资源、公平性和回放门禁同时通过时成立。任何一层缺失都必须保留为
失败或“不可判定”，不能只报告成功运行。

## 经典优化方法怎么比较

候选方法覆盖随机、空间填充、局部搜索、类型化 GP/RF acquisition 和风险约束方法。物料是类别
变量；数字 action 值只是序列化 ID，不能作为连续距离直接输入 surrogate。

0.2 冻结诊断使用 seeds 20–39，objective-only 规则通过但暴露三任务风险退化。0.3 随后在运行前
冻结 seeds 300–319、5 个百分点安全非劣界限、5% 相对成本非劣界限和 Bonferroni 同时上界。
0.3 的四任务 objective 与 cost 规则通过，但三任务 safety 规则失败，因此完整主比较失败。
这两个 cohort 都已消费，并且绑定 pre-v0.5 backend；它们只能解释协议为何改变，不能用于当前排名。
后续正式 preflight 会拒绝仓库公开配置、历史结果或文档中已经暴露的任何 seed，而不是只维护一组
手工排除范围。

Safe-GP 随后仅在 Dev seeds 1100–1119 上修复和选择。确认协议 0.1 在看见结果前冻结实现文件摘要、
recipe space 0.2、峰值风险标签、seeds 500–519、四任务 SESOI 和相同的安全/成本非劣规则。240 条
确认轨迹及独立回放显示四任务 safety/cost 全部通过，但连续流平均效应 0.018752 未达到 SESOI
0.020000，故联合规则失败。seeds 500–519 同样已消费；任何方法修改都必须再次使用未触碰 seeds。

这些历史 cohort 的冻结清单、运行清单和审计报告应随研究工件保存；公开结果只引用工件摘要、协议版本和摘要哈希，不要求使用者执行仓库维护脚本。

## RL 还要记录训练过程

RL 结果至少保留：算法与库版本、网络和观测封装、训练 world 分配、随机种子、环境步数、计算设备、
checkpoint 摘要、Dev 选择规则和无学习评测轨迹。PPO/SAC 等方法不能只运行未训练策略或短 smoke
后进入方法排名。

Pre-v0.5 SAC 开发证据只有连续流任务的单模型 seed。它精确完成 100,000 步并通过开发回放门禁，但
80k checkpoint 的开发结果高于 100k。正式协议必须在多个训练 seed 上汇总 checkpoint 选择，不能
默认使用训练步数最大的模型。

## LLM 还要记录调用与信息条件

正式 LLM 角色采用 operation-level adaptive 交互：每个逻辑决策读取最新公开观测、可用动作、
测量和谱图证据，再返回结构化 evidence、spectrum interpretation、hypothesis、uncertainty 与
rationale。系统不请求、保存或展示私有逐字思维链。

每个操作只允许一个最终逻辑决策；provider 请求和 JSON 修复可重试，但所有尝试、失败、token 和
费用都计入资源账本。正式运行冻结 provider、model ID、prompt hash、请求参数和价格快照。stub、
replay trace 或手写计划只能验证管线，不能冒充在线模型结果。

## 证明 Agent 真的使用了谱图或反馈

若主张 Agent 使用了表征反馈，必须执行配对消融：

- `raw`：只给原始曲线；
- `unassigned`：给曲线和未指认峰；
- `assigned`：给教学用指认峰，作为信息上限；
- masked：不提供该表征通道。

同时区分实验间 recipe 更新与实验内操作调整。只根据 final assay 选择下一配方的方法属于
recipe-level active learning，不能描述为实验内闭环控制。

## 最终报告应该包含什么

- 逐任务使用配对效应和确定性 bootstrap 区间；
- 多任务同一假设族使用 Holm 校正；
- 报告 SESOI、约束差值、资源差值和全部失败；
- 不将不同单位的任务主指标平均成一个“总能力分”；
- 同时发布逐 seed 结果、预算—收益曲线和方法资源前沿；
- 参考 regret 只使用独立搜索并冻结的逐 cell reference，不使用被评方法自身最好值。

## 从轨迹走到可信结果

```text
trajectory JSONL
  -> schema and constitution validation
  -> deterministic replay
  -> metric and constraint recomputation
  -> trajectory SHA-256 + score binding
  -> verified result
  -> paired task-level statistics
  -> signed/private or public release artifact
```

## 隔离第三方代码并准备发布

Agent 不得读取 hidden state、私有 salt、评测 seed 表、oracle 参数或评测输出目录，不得修改环境代码
或访问未授权网络。正式第三方代码必须运行在无网络、只读挂载、低权限和资源受限的独立沙箱中；
本地 trusted subprocess 只适合可信代码。

完整发布还要求 salted private evaluation、独立复现、干净 wheel 安装和所有协议/轨迹摘要固定。
提交格式见[提交与验证](submission.md)，当前证据见[科学状态](benchmark_release.md)。
