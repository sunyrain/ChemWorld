# ChemWorld 工作清单

最后更新：2026-07-11

本文件是 ChemWorld 的长期维护清单。当前唯一主线是先完成并冻结一个完整、可信、可复现的
benchmark backend；在 benchmark 冻结前，不把训练环境、三层架构或更多展示功能作为阻塞项。
本文件不加入 MkDocs 导航，也不作为面向使用者的发布文档。

## 维护规则

- 开始任何任务前必须先 claim；未在远端 `claims/active/` 登记的任务不得实施。完整流程见
  [`claims/README.md`](claims/README.md)。
- claim 必须声明 owner、branch、scope、owned paths 和过期时间；路径不得与其它 active claim
  重叠。扩大范围、阻塞交接或完成任务时都必须先更新 claim 状态。
- `[ ]` 表示尚未完成，`[x]` 表示已经有可复核证据并满足验收标准。
- 不能因为“代码已经存在”就标记完成；必须同时记录测试、报告或冻结产物。
- 修改 task、scenario、mechanism、observation、scoring 或 replay 合同时，必须更新对应版本和
  hash，并重新执行冻结流程。
- 正式 benchmark 冻结后，只允许兼容性修复；任何会改变轨迹或得分的修改进入下一个版本。
- 发布门禁保持本地执行，不依赖 CI 或 GitHub Actions。

## 当前工程基线快照

以下项目说明管线和历史候选证据已经存在，不表示 scientific benchmark 已经最终冻结。

- [x] 15 个注册任务可以完成环境一致性审计。
- [x] 6 个 serious task 均通过机器合同审查，`contract_ready_count = 6`。
- [x] 6 个 serious task 已完成机器经验验证，`benchmark_ready_count = 6`。
- [x] serious 正式评测已完成 6 tasks × 6 agents × 5 seeds，共 180 次运行，artifact replay 通过。
- [x] 2026-07-10 本地发布检查通过：Ruff、mypy、全量测试、MkDocs
  strict、wheel smoke、11 个参考验证测试、runtime boundary、15 tasks × 3 seeds 环境审计和
  baseline smoke。
- [x] 已生成 serious baseline、bootstrap 95% CI、响应面、近似 oracle、难度校准、失败检查和
  可重放 release bundle；正式结果只逐任务报告，不发布跨任务总分。

历史候选发布包位于 `benchmark/releases/chemworld-serious-v1/`；临时运行证据位于
`runs/benchmark_freeze/release_v1/`。该候选包已被 2026-07-11 科学有效性审计判定为 stale，不能再
作为当前 `main` 的不可变冻结发布。

World Law v0.4 backend candidate 位于 `benchmark/releases/chemworld-serious-vnext/`。WF-110 已
接入 8 个 adapter，移除正式 runtime fallback/proxy 路由，重建 task/scenario/core golden 与集成
证据。该包明确不含新 baseline 结论，`benchmark_claim_allowed=false`；v0.4 readiness 保持
`candidate`，等待后续有效性和功效工作流。

## 2026-07-11 科学有效性审计

当前有效机器证据位于：

- `workstreams/benchmark_v1/reports/campaign-budget-curve-pilot5.json`；
- `workstreams/benchmark_v1/reports/validity-power-electro-structured40-pilot5.json`。

它们确认旧随机采样最大值不是 oracle，8–12 个完整实验不足以支撑多数主动学习任务，且类别
物料不能按连续数字距离编码。现有结果仍是 diagnostic-only：六任务均未稳定达到 0.05 SESOI，
尚缺 20 paired seeds、轴级 OOD/私评、资源匹配、RL、真实 LLM 和冻结论文证据链。

## 下一阶段互不重叠认领队列

每项必须单独 claim、单独门禁和单独关闭；不得用一次大提交同时修改环境、评测和论文结论。

1. [x] `benchmark-v1-release-integrity`：让 frozen checker 校验 task hash、commit、dirty tree、全部
   evidence digest 和轨迹索引；旧包失配时必须失败。
2. [x] `wf-110-vnext-runtime-integration`：统一接入已通过 intake 的 runtime additions/replacements，
   删除被替代路由，升级 World Law，并重冻结 task/scenario/golden，不在此任务内跑论文结论。
3. `benchmark-v1-validity-power`：修复 oracle 定义、任务地板/天花板与策略不分辨问题，使用 paired
   seeds 和功效分析确定正式 seed 数。
4. `benchmark-v1-generalization-security`：实现每任务轴级 interpolation/extrapolation/composition/
   noise、私评、语义重映射、metamorphic invariance 和 exploit matrix。
5. `benchmark-v1-method-protocol`：冻结统一 method adapter、实验调用/墙钟/token/费用资源账本、
   checkpoint 与 prompt/model provenance。
6. `benchmark-v1-classic-active-learning`：运行 random/LHS/greedy、GP-EI/PI/UCB、RF-EI、safe BO
   等传统优化与主动学习，不修改任务。
7. `benchmark-v1-rl`：建设独立 Train world-family、向量环境和 PPO/SAC 等训练基线，只在冻结
   Bench worlds 上评测。
8. `benchmark-v1-llm`：运行至少两类真实 LLM，固定 prompt、temperature、最大轮数、token/
   monetary budget 和结构化 decision summary；stub 仅保留为协议回归。
9. `benchmark-v1-statistics-figures`：汇总 paired effect、bootstrap CI、rank stability、regret、
   sample efficiency、constraint violation 与 resource frontier，图表只能从冻结摘要生成。
10. `paper-aaai-chemworld`：在前述结果冻结后撰写 AAAI LaTeX、生成 PDF、执行匿名性/引用/图表/
    页数检查；论文不得反向修改 benchmark 以美化结论。

## Phase 1：完成并冻结 Benchmark Backend

### 1.1 固定 v1 的研究主张和任务边界

- [ ] 冻结 v1 benchmark 的核心主张：评估部分可观测、实验有成本条件下的主动探索、实验
  决策和证据更新能力；不主张真实化学产率预测或工业装置设计。
- [ ] 默认以当前 6 个 serious task 为 v1 候选集；若某任务无法通过可辨识性或有效性审查，
  将其降级为 exploratory，而不是为了数量强行进入正式套件。
- [ ] 为每个正式任务写出唯一 primary claim、primary metric、secondary diagnostics 和明确的
  非主张范围。
- [ ] 决定正式结果只逐任务报告还是同时发布聚合分数。默认逐任务报告；如保留聚合分数，必须
  固定归一化、权重和缺失任务处理规则。
- [ ] 明确 benchmark 与 smoke/teaching/exploratory 任务的发布边界，避免用户把 15 个注册任务
  全部理解为正式榜单任务。

验收标准：`SERIOUS_TASK_IDS`、任务卡、benchmark protocol、README 和发布产物对正式任务范围
及能力主张完全一致。

### 1.2 六个 serious task 的逐任务有效性审查

- [ ] `partition-discovery`：证明不同接触、相体积与测量选择能够提供不同信息量；确认重复无效
  操作不会获得异常高分，且 informed strategy 显著优于 random。
- [ ] `reaction-to-crystallization`：验证反应质量、收率、纯度与 CSD 的真实权衡；确认终点测量
  不能被单一固定配方轻易饱和。
- [ ] `reaction-to-distillation`：优先调查当前 smoke 低分；验证反应条件和馏分切割确实需要联合
  决策，并排除整体地板效应。
- [ ] `flow-reaction-optimization`：优先调查当前 smoke 低分；验证停留时间、热边界、压降和安全
  风险形成可探索但非退化的响应面。
- [ ] `electrochemical-conversion`：检查当前 scripted 与 LLM stub 同分现象；确认电压/电流、传质
  与能效控制能够区分策略，而非由固定流程决定结果。
- [ ] `equilibrium-characterization`：检查当前 scripted 与 LLM stub 同分现象；证明多轮选择测量和
  干预会提高平衡参数识别质量。
- [x] 停止把随机配方最大值称为 oracle；已建立逐 seed best-known diagnostic reference，正式
  regret 仍需在冻结前绑定独立、可更新的 reference 协议。
- [ ] 对每个任务建立最低合理策略和随机下界，用于发现地板、奖励泄漏和协议捷径。

验收标准：每个任务均有独立有效性报告，至少包含响应面/状态切片、策略排序、失败案例和是否
接受进入正式套件的结论。

### 1.3 完整 Baseline 与统计校准

- [ ] 跑完整 serious baseline：`random`、`lhs`、`scripted_chemistry`、`gp_bo`、`safe_gp_bo`、
  `tool_using_llm_stub`；将不可复现或依赖外部在线服务的 agent 与官方冻结基线分开。
- [ ] 检查每个 baseline 是否真正适配任务动作空间；不允许多个“不同”baseline 实际退化为同一
  固定配方或相同行为序列。
- [x] 已用 10-seed paired pilot 和 0.05 SESOI 完成功效初估，暂定正式起点为每任务 20 seeds；
  冻结前用最终任务合同复核。
- [x] 机器报告已包含均值、配对标准差、paired bootstrap 置信区间、符号翻转检验、功效估计和
  逐 seed 紧凑指标。
- [ ] 校准任务 budget、threshold、噪声和惩罚，排除 random 也高分、所有策略都低分、所有强策略
  同分等地板/天花板情况。
- [x] 已修复 `budget_override` 未贯通 runner/suite 的协议错误，并验证 BO 在校准预算下执行
  4–8 次 acquisition；但尚未观察到达到 0.05 SESOI 的稳定自适应收益。
- [x] 已增加显式完整实验数和 4/8/12/20/40 在线前缀审计；40-experiment pilot 证明五个任务
  存在正向学习信号，但 0/6 达到 0.05 SESOI，且电化学 GP 显著为负。下一步按任务校准预算，
  并单独审计电化学搜索表示/安全目标，不能再用统一 `dimension + 2` 作为正式预算。
- [x] 已实现连续坐标 + material one-hot 的结构化 GP 探针；电化学 40-experiment 配对效应从
  -0.076 翻转为 +0.032，但尚未达到 SESOI。冻结前须扩展到 20 seeds，并审计全部任务的类别
  坐标与耦合坐标。
- [ ] 固定每个任务的 baseline reference table，并将冻结结果绑定 commit、合同 hash、solver
  provenance 和 trajectory digest。

验收标准：不同能力层级的策略在大多数正式任务上形成稳定、可解释的排序，置信区间和异常任务
均被公开说明。

### 1.4 泛化、稳健性和反作弊

- [ ] 将当前“两个 generalization axes 的文字声明”变成机器可执行的参数切片和报告。
- [ ] 对每个任务分别测试 public-test 内 seed 泛化、参数区间外推、组合变化和 observation noise
  扰动。
- [ ] 建立真正的 maintainer-side private-eval 配置；无私有 salt 时继续明确失败或标记为
  placeholder，绝不产生正式榜单声明。
- [ ] 检查 public/private 排名相关性和性能下降，而不只报告一个平均 gap。
- [ ] 增加策略不变性测试：物料代号重映射、无关字段重排、等价动作序列和观测格式轻微变化不应
  显著改变结果。
- [ ] 增加 simulator exploit 审计：重复 final assay、无成本测量、非法动作刷 reward、提前
  terminate、预算边界、浮点异常和回放差异均不能获利。
- [ ] 使用仅公开 observation 的独立 agent harness 运行正式候选，确认无法通过 Python 对象、
  debug info、文件路径或异常消息读取 hidden state。
- [ ] 对 action、observation 和任务文本做泄漏扫描，确保参数名、物种名、谱峰 assignment 或
  scenario id 不直接编码最优答案。

验收标准：正式报告包含泛化矩阵、反作弊结果和已知失败边界；private-eval 产物可验证但不能反推
私有参数。

### 1.5 Backend 科学与数值可信度

- [ ] 为每个 serious task 建立“运行时实际调用模块”到 model card、参考验证和适用域的可追踪
  映射，防止存在专业模块却未真正接入 runtime。
- [ ] 对反应、结晶、蒸馏、连续流、电化学、相平衡和水相平衡分别冻结守恒、极限行为、单调性、
  数值收敛和失败策略。
- [ ] 对当前 skipped 的 11 个 optional reference backend 测试作出发布决定：要么在正式验证
  环境安装并通过，要么明确它们不属于 v1 证据，不能让 skip 被解释为通过。
- [ ] 审查 `lite` 与 `professional_candidate` 的命名和证据是否匹配；v1 不以“professional”
  为必要条件，但每个限制必须准确公开。
- [ ] 审核合成 HPLC、GC、UV-vis、IR、NMR、MS 和 pH observation：观测必须与 hidden state
  因果耦合、噪声可复现、成本有效、不可直接泄漏真值。
- [ ] 为谱图增加任务级可辨识性检查：不同关键状态应产生可区分观测，同一状态的噪声分布应稳定，
  仪器选择应影响决策价值。
- [ ] 检查安全与成本不是纯展示字段：改变策略时必须实际改变 episode 结果或正式诊断指标。
- [ ] 对所有正式任务执行多平台或至少 Python 3.11/3.12 的数值重放一致性检查，并冻结允许误差。

验收标准：每个正式任务都有完整的 backend evidence card；不存在未声明 proxy、未接入专业模块、
非确定性回放或无效仪器信号。

### 1.6 评分、回放与发布证据链

- [ ] 冻结 primary score 与在线 reward 的分离规则；正式排名只依赖 final-assay 或 evaluator 可
  重算字段。
- [ ] 审计所有 primary/secondary metric 的方向、范围、单位、缺失值和异常值处理。
- [ ] 验证 trajectory 从初始状态完整重放，而不是隐式依赖运行结束后的内存状态。
- [ ] 验证 result、leaderboard 和 paper artifact 均从轨迹重算，手工修改 JSON 会被拒绝。
- [ ] 增加旧合同轨迹在新版本上的明确兼容/拒绝测试，避免静默漂移。
- [ ] 冻结 task、scenario、mechanism、world-law、observation、scoring、solver 和 runtime profile
  的版本与 hash 清单。
- [ ] 定义正式 benchmark release bundle：wheel、公开任务合同、seed suite、baseline 报告、
  golden trajectories、验证命令、限制说明和签名私评格式。

验收标准：从干净 wheel 安装开始，第三方能够复现公开分数、验证轨迹并检测任何合同或结果篡改。

### 1.7 冻结前最终门禁

- [ ] 将“6 个任务均有完整经验验证”变成 readiness 的机器条件，不能只手工把 status 改为
  `validated`。
- [ ] `benchmark_ready_count == 正式 serious task 数量`。
- [ ] 完整 local release gate 通过，且报告对应冻结 commit，而不是脏工作区或旧 commit。
- [ ] 完整 serious baseline 和 paper artifact 在冻结 commit 上重新生成并 replay verified。
- [ ] 文档、JSON、YAML 和生成报告统一 UTF-8；在 Windows 和静态站点中检查中文无乱码。
- [ ] 清理或忽略临时 audit、pytest cache、实验 runs、密钥文件和本地 site 输出；确保发布包不含
  `deepseek_api.md` 或任何私密信息。
- [ ] 发布候选版本并打不可变 tag；记录后续变更只能进入下一个 benchmark contract version。

验收标准：形成一个可引用的冻结版本，完整说明任务、数据划分、评分、基线、验证、限制和复现
方式；此时 Phase 1 才算完成。

## Phase 2：Benchmark 冻结后的三层系统

以下内容暂不阻塞 Phase 1，只维护设计边界。

### 2.1 ChemWorld-Bench

- [ ] 将冻结 benchmark 保持为只评测、版本化、可回放的独立层。
- [ ] 公共测试与维护者私评使用相同协议、不同隐藏世界族。
- [ ] 后续训练功能不得修改冻结任务的转移、观测或评分语义。

### 2.2 ChemWorld-Train

- [ ] 设计程序化 world generator，而不是复制冻结测试 seed。
- [ ] 支持大量并行 `reset/step`、课程难度和可验证 reward。
- [ ] 在机制拓扑、参数、传感器、噪声、资源和失败模式上产生训练多样性。
- [ ] 建立 train/dev/OOD world-family split，防止在 Bench 上训练。
- [ ] 支持非 LLM RL、LLM trajectory learning 和混合 Agent。

### 2.3 ChemWorld-Bridge

- [ ] 定义与真实 HTE 数据、外部优化 benchmark、数字孪生和真实设备之间的抽象操作协议。
- [ ] 建立 data-replay backend，测试 ChemWorld 训练是否迁移到外部数据分布。
- [ ] 以策略排序一致性和训练前后迁移提升作为外部有效性证据，不要求精确复现真实产率。

### 2.4 三层共同约束

- [ ] 共用 typed action、observation、trajectory、provenance 和 verifier 协议。
- [ ] Train 可持续扩展，Bench 必须冻结，Bridge 负责外部证据；三者不得共享隐藏测试世界。
- [ ] 物料同时支持中性代号和真实语义 skin，用配对实验分离预训练知识与主动探索能力。
- [ ] Agent 记录结构化 hypothesis/evidence/uncertainty/decision summary，不要求或保存完整私有
  chain-of-thought。

## 后续讨论队列

以下问题需要讨论后再改变实现：

1. v1 是否默认尝试冻结全部 6 个 serious task，还是先冻结通过有效性审查的子集？当前建议是
   全部进入审查，但允许不合格任务降级。
2. 正式 benchmark 的核心能力名称采用“experimental intelligence”“active scientific
   exploration”还是更窄的“closed-loop chemical experimentation”？
3. 是否完全取消跨任务总分，只发布逐任务结果和能力画像？
4. public-test 是否允许持续公开比较，private-eval 由本地维护者运行还是未来提供服务端？
5. 谱图在 v1 中应只是观测通道，还是必须至少有一个任务把“选择并解释谱图”作为核心决策？
6. 正式任务使用中性物料代号、真实名称，还是同时发布 paired semantic skins？
7. Phase 1 完成后，优先建设程序化 Train generator，还是先建设真实数据 replay Bridge？

## 常用检查命令

```powershell
.\.venv\Scripts\python.exe -m chemworld.cli tasks readiness
.\.venv\Scripts\python.exe scripts/run_serious_task_suite.py --smoke
.\.venv\Scripts\python.exe scripts/run_serious_task_suite.py
.\.venv\Scripts\python.exe scripts/run_release_gate.py
```
