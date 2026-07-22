# ChemWorld 机制适应基准：最终判断与 v0.2 确认协议

## 一句话结论

ChemWorld 最有说服力的论文故事不是“LLM 操作虚拟实验室”，而是：

> ChemWorld 是面向 world-model Agent 的物理化学反馈环境，用受控隐藏规律变化、可诊断实验预算和可复现反事实，拆分测量反馈利用、变化检测、机制族识别、主动诊断、性能恢复与程序自主性。

环境提供训练和评估能力，但本次 DeepSeek 评测不训练、不微调、也不更新模型权重。campaign 内发生的是上下文、显式分布、记忆和行动的更新；模型权重中的世界知识是否能被有效调用，正是被测对象之一。

## 当前证据的最终解释

v0.1 的原始轨迹和报告保持不变，v0.1.1 只做严格重分析。当前证据支持以下结论：

1. ChemWorld 能构造静态优化分数无法覆盖的机制变化和物理化学反馈任务。
2. 当前 DeepSeek 控制器尚未证明具有可靠的机制发现能力。
3. 旧报告唯一的 `genuine_experimental` 只能称为 `provisional_threshold_joint_success`：它在单个轨迹上同时越过结果和机制阈值，但没有多种子重复、没有机制可识别性证书，且 campaign 历史中存在系统辅助收尾。
4. 因而当前“确认级机制发现”计数为 0；这不是把旧结果删除，而是降低解释等级。
5. 在 Gate 0 和 Gate A–E 全部通过前，任何正式输出都必须保持 `publication_ready=false`。

对应的机器可读重分析和中文报告为：

- `deepseek-mechanism-diagnostics-v0.1.1.json`
- `deepseek-mechanism-diagnostics-v0.1.1.md`

## 论文主张分层

### 当前可以主张

- 提出一个面向 world-model Agent 的受控物理化学反馈环境和任务体系。
- 说明 IID 静态表现不能替代隐藏规律变化后的适应表现。
- 提供把结果、机制理解、反馈敏感性和程序自主性拆开的评估协议。
- 展示单种子探索性轨迹中的失败模式，用于提出确认性假设。
- 明确环境不负责为被测托管模型重新训练权重。

### 当前不可以主张

- DeepSeek 已可靠发现物理化学机制。
- 两个 post-change 实验足以识别所有候选机制。
- 旧 `J_true-J_permuted` 是反馈的因果效应。
- `expected_information_gain` 已得到 Bayesian 校准。
- 系统强制收尾后的得分等同于完全自主成绩。
- 单种子混合接口排名代表方法总体优劣。

## v0.1.1 已修正的解释问题

### 1. 信息价值

旧分析把模型自报的 expected information gain 与下一步熵下降比较，并称为校准误差。新分析只使用相邻、两端均为 `model_decision` 的更新对：

- 旧 pair 数：201；
- 排除涉及 `model_failure` 的 pair：9；
- 排除跨过生命周期动作的非相邻 pair：1；
- 清洁 pair 数：191；
- 平均自报信息值：0.2524；
- 平均 declared-distribution JS 变化：0.0021。

这些指标现在称为“自报分布更新”，不再称为 EIG 校准或 Bayesian posterior 更新。

### 2. 重复的 change probability

v0.1 允许模型独立上报 `change_probability` 和 `q(no_change)`。438 个有效决策中，两者平均绝对差为 0.3138，71.23% 的差异超过 0.2。v0.2 删除独立字段，只保留一个机制分布，并由评估器计算：

`p(change) = 1 - q(no_change)`

变化发生时的机制族分布另记为 `q(family | change)`。

### 3. 生命周期覆盖

7 次 guardrail action 影响了 4/40 个实验、4/20 个阶段、4/10 个独立 campaign。7/40=17.5% 是“辅助动作数/实验数”的混合口径；实验影响率实际为 10%。v0.2 强制同时报告：

- `Autonomous score`：Agent 未自行 terminate/final assay 时记协议失败或固定惩罚；
- `Assisted scientific score`：允许系统记录后收尾，只评价此前选择的科学价值。

### 4. 排名接口和平局

recipe 级方法与 operation 级方法不是同一种决策接口，正式排名必须分层报告；跨接口结果只作描述。平局使用 average rank，严格 inversion 排除 ties。

### 5. Provider 证据

v0.1 已记录模型 ID、请求 ID、system fingerprint、thinking 和 max tokens，但未完整记录 temperature、top-p、provider seed、逐请求时间戳和请求/响应 payload hash。v0.2 把这些纳入 Gate 0。它能证明用户侧没有训练和权重更新，但不能证明托管 provider 内部永远不变。

## v0.2 的六道 Gate

| Gate | 要回答的问题 | 必须证据 | 冻结通过条件 |
| --- | --- | --- | --- |
| Gate 0 | 数据是否完整且无泄漏？ | private split commitment、哈希、三层 outcome、receipts、排除原因、replay | 所有证据齐全，私有真值和评估派生字段零 prompt 泄漏 |
| Gate A | 预算内机制是否可识别？ | 主动预算 oracle + 固定轨迹 decoder | active oracle 总体 top-1 Wilson 下界 ≥0.80，每机制族 recall 下界 ≥0.70 |
| Gate B | 检测到的真是变化吗？ | 配对 no-change twins、随机 change time | FPR ≤0.10，AUROC 置信下界 ≥0.80，并报告 Brier/延迟 |
| Gate C | 反馈是否真的改变且改善行为？ | 同前缀局部反应测试 + 配对完整 campaign | 局部反馈效应超过 provider 重复噪声，真实反馈效用差的置信方向为正 |
| Gate D | 恢复来自 Agent 适应还是世界差异？ | IID action replay、frozen policy、adaptive policy、oracle | adaptive 优于 frozen；normalized recovery 置信下界 ≥0.50 |
| Gate E | 科学决策是否程序自主？ | autonomous/assisted 双成绩和失败率 | protocol failure rate 置信上界 ≤0.05 |

Gate A 中两个系统回答不同问题：主动 oracle 证明在相同动作、测量和预算接口下“任务原则上可识别”；固定轨迹 decoder 判断 Agent 实际选择的轨迹是否包含足够诊断信息。只有 decoder 成功而 Agent 失败，更接近“推理/更新失败”；两者都失败则不能排除实验设计本身信息不足。

## 确认性实验矩阵

### 变化与预算

- pre-change：2 个实验；
- 总 horizon：14 个实验；
- change time：`never, 1, 2, 4, 6`，由独立种子随机化并对 Agent 隐藏；
- post-change checkpoint：`k ∈ {1, 2, 4, 8}`；
- 未恢复轨迹按右删失处理。

`never` 条件必须经历相同记忆保留、环境实例重建和阶段协议，只是不改变隐藏规律。由此估计 sensitivity、false-positive rate、AUROC、Brier score 和检测延迟。

### 反馈因果设计

局部反应测试固定完全相同的公开历史前缀，只改变最后一个反馈包，比较机制分布 JS 变化、下一 operation、诊断测量率和 operation-aware action distance。同条件 provider 重复给出技术噪声基线：

`Net feedback effect = between-condition distance - within-condition provider distance`

完整 campaign 再在相同 world seed、初始状态、prompt、模型设置及可用 provider seed 下重复，评价终局得分、累计 regret、机制识别和恢复时间。局部测试回答“反馈是否改变行为”，完整 campaign 回答“改变是否带来效用”，二者不得合并成一个指标。

### 恢复分解

- `world effect = IID action replay@shifted - IID action replay@IID`；
- `adaptation gain = adaptive policy@shifted - frozen policy@shifted`；
- `normalized recovery = adaptation gain / (oracle@shifted - frozen policy@shifted)`。

统计单位是 world seed 或 paired cell；provider repeats 是嵌套技术重复，不能伪装成独立科学样本。区间使用冻结种子的 hierarchical/cluster bootstrap。

## 已落地的实现

- `configs/benchmark/mechanism_adaptation_v0.2.1.json`：当前设计对齐版本；冻结数据合同、阈值、六道 Gate，以及动作—干预—观测可达性前置审计。
- `src/chemworld/agents/mechanism_adaptation_live_llm.py`：候选操作定义、semantic/anonymous 标签、随机顺序、单一机制分布、派生字段防泄漏。
- `src/chemworld/eval/mechanism_adaptation.py`：分布指标、no-change 检测、Gaussian 诊断 oracle、固定轨迹 decoder、反馈净效应、action distance、恢复分解、自主性与 Gate evaluator。
- `src/chemworld/eval/flagship_reanalysis.py`：v0.1.1 非破坏重分析和完整性核验。
- `scripts/reanalyze_flagship_mechanism_diagnostics.py`：可重复生成 v0.1.1 JSON/Markdown。
- `scripts/plan_mechanism_adaptation_matrix.py`：展开 changed/no-change twin 公共开发矩阵；当前冻结为 1,000 个配对 cell、2,000 个 campaign arm。
- 对应单元测试覆盖协议冻结、oracle/decoder、no-change twin、反馈、恢复、自主性、Agent prompt 与历史重分析。

## 尚未伪装成“已完成”的部分

新一轮多世界种子、多 provider 重复的 DeepSeek campaign 尚未运行。因此：

- 六道 Gate 当前均为 `not_evaluated`，不是 failed，也不是 passed；
- v0.2 完成的是确认性协议、实现基础和历史重分析；
- 正式论文中的 DeepSeek 能力结论必须等实际运行、盲化核验和统计分析后更新。

这是最终的 method freeze：后续如果数据不通过某个 Gate，应报告具体失败维度，而不是事后修改阈值或候选定义。
