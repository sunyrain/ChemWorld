# DeepSeek 旗舰任务机制诊断（探索性）

- 状态：`exploratory_complete`
- 协议：`chemworld-deepseek-flagship-mechanism-diagnostics-2026-07-21`
- 协议 SHA-256：`900c1e51cda19082bd8ebbb5b79224b043c4ecf02767a636e973c6391ada2991`
- 定位：Agent 能力测试环境；不训练、不微调、不更新模型权重。
- 声明边界：单种子探索性诊断，不构成正式排行榜或可发表的确认性结论。

## 完整性审计

- 覆盖是否完整：`True`
- 预期单元：22；观测单元：22
- 缺失单元：0；未完成阶段：0

## 核心发现

- 排名迁移很弱：IID/切换排名 Spearman = 0.0896，共 6 对反转。DeepSeek 的 IID/适应排名为 6/6。
- 没有观察到正的证据依赖：平均 `J_true - J_permuted` = -0.1518。负值不能证明错误反馈有益，但说明本轮没有稳定的真实反馈优势。
- 真反馈下机制识别 0/2，在两个切换实验内恢复 0/2；模型虽报告变化概率上升，最终仍倾向 no_change。
- 名称—规律反事实识别 0/2；两项最佳得分都提高，但真值概率都很低，属于结果与机制理解分离。
- 信息价值明显高估：加权声明值 0.2471，下一步实际熵下降 0.0079，绝对校准误差 0.2439。
- 独立 campaign 分类：`{"accidental_optimizer": 5, "genuine_experimental": 1, "joint_failure": 4}`。

## 实验一：IID 排名与未见机制切换排名

该实验检验静态任务得分能否代表机制变化后的适应能力。Spearman 排名相关为 0.0896，排名反转 6 对。

| 方法 | IID | 切换后 | IID 排名 | 适应排名 | 排名变化 |
| --- | --- | --- | --- | --- | --- |
| greedy_local | 0.6043 | 0.4510 | 1 | 4 | -3 |
| random_recipe | 0.6043 | 0.4510 | 2 | 5 | -3 |
| structured_gp_bo | 0.5900 | 0.5895 | 3 | 2 | 1 |
| structured_gp_ucb | 0.5900 | 0.6187 | 4 | 1 | 3 |
| rule_based | 0.5015 | 0.5099 | 5 | 3 | 2 |
| deepseek_v4_flash | 0.4335 | 0.2288 | 6 | 6 | 0 |

解释：这里比较的是同一公开种子、两个旗舰任务上的描述性均值；它能发现排序错位，但不能估计跨种子显著性。

## 实验二：反馈置换与证据依赖

环境状态和真实评分始终不变，只修改 Agent 可见的测量反馈。证据依赖定义为 `J_true - J_permuted`；正值表示真实反馈对结果有帮助。

| 任务 | 真实 | 跨实验置换 | 延迟 | 关键测量删除 | 证据依赖 |
| --- | --- | --- | --- | --- | --- |
| electrochemical-conversion | 0.2570 | 0.5176 | 0.7578 | 0.2778 | -0.2606 |
| reaction-to-crystallization | 0.3973 | 0.4404 | 0.0028 | 0.3967 | -0.0431 |

跨任务平均证据依赖：-0.1518。由于各条件是独立采样调用而非确定性轨迹克隆，差值同时包含模型采样噪声。

## 实验三：名称—规律反事实

材料名称、说明、动作编码、成本与风险保持不变，仅交换隐藏材料效应行；因此该实验测试模型是否依赖观测到的物理化学反馈，而不是记住名称先验。

| 任务 | IID 最佳 | 反事实最佳 | 得分变化 | 机制识别 | 真值概率 |
| --- | --- | --- | --- | --- | --- |
| reaction-to-crystallization | 0.5231 | 0.5785 | 0.0555 | False | 0.1000 |
| electrochemical-conversion | 0.3866 | 0.7629 | 0.3763 | False | 0.1000 |

## 实验四：结果与机制理解解耦

分类规则：相对结果达到本 campaign IID 最佳值的 90% 且正确识别为 genuine_experimental；高结果但未识别为 accidental_optimizer；低结果但正确识别为 theoretical_explainer；两者皆低为 joint_failure。

类型计数：`{"accidental_optimizer": 5, "genuine_experimental": 1, "joint_failure": 4}`

| 实验 | 任务 | 反馈 | 最终目标 | 机制识别 | 真值概率 | 变化检测 | Brier | 恢复实验 | 分类 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ranking_shift | reaction-to-crystallization | true_feedback | 0.3973 | False | 0.1500 | True | 1.0350 | None | joint_failure |
| ranking_shift | electrochemical-conversion | true_feedback | 0.2570 | False | 0.3000 | True | 0.8600 | None | joint_failure |
| feedback_ablation | reaction-to-crystallization | permuted_feedback | 0.4404 | False | 0.2500 | False | 0.7500 | 1 | accidental_optimizer |
| feedback_ablation | reaction-to-crystallization | delayed_feedback | 0.0028 | False | 0.2500 | True | 0.7500 | 1 | accidental_optimizer |
| feedback_ablation | reaction-to-crystallization | critical_measurement_deleted | 0.3967 | False | 0.2000 | True | 0.8750 | 1 | accidental_optimizer |
| feedback_ablation | electrochemical-conversion | permuted_feedback | 0.5176 | False | 0.3000 | False | 0.7800 | None | joint_failure |
| feedback_ablation | electrochemical-conversion | delayed_feedback | 0.7578 | True | 0.5000 | True | 0.3800 | 2 | genuine_experimental |
| feedback_ablation | electrochemical-conversion | critical_measurement_deleted | 0.2778 | True | 0.4000 | True | 0.5400 | None | joint_failure |
| material_law_swap | reaction-to-crystallization | true_feedback | 0.5785 | False | 0.1000 | False | 1.1750 | 1 | accidental_optimizer |
| material_law_swap | electrochemical-conversion | true_feedback | 0.7629 | False | 0.1000 | False | 1.3400 | 1 | accidental_optimizer |

信息价值校准使用模型声明的预期信息增益与下一步归一化熵下降比较；它衡量公开概率报告的一致性，不等同于访问或评判私有思维链。
这里的高/低结果是相对各 campaign 的 IID 基线定义，不代表绝对分数高/低；因此绝对分数很低的轨迹仍可能被标为 accidental_optimizer。

## 综合判断

这组结果支持 ChemWorld 作为“反馈驱动的物理化学 world-model Agent 评测环境”的故事：静态优化排名不能代表机制切换后的表现，任务还能把变化检测、机制识别、结果恢复和信息价值校准彼此拆开。

它不支持把当前 DeepSeek 控制器称为已具备可靠机制发现能力。真反馈下两个机制切换都未被正确识别，材料反事实也未识别；多个相对高结果被归为 accidental_optimizer。唯一 genuine_experimental 出现在电化学延迟反馈条件，属于单种子、采样型孤立结果。

负 Evidence Reliance 与严重的信息价值高估表明：当前控制器尚未展示稳定、可校准的反馈使用。下一步确认性研究应冻结协议后增加种子、使用确定性或配对重放设计，并为信息增益策略加入真正的专用基线。

## 资源与可复现性

- DeepSeek 独立活动 campaign：10
- 模型调用：450
- 计费响应后决策失败：10
- Provider 重试：2
- 生命周期收尾覆盖：7
- 输入 / 输出 token：3984857 / 180916
- 估算费用（USD）：0.499251
- 私有推理保留：否；报告只保留公开决策、概率诊断、请求回执和环境轨迹。

## 限制

- 仅使用一个公开种子，属于探索性诊断，不是正式方法排名。
- DeepSeek 响应由 provider 采样；不同反馈条件不是确定性轨迹克隆。
- PPO 旧 failed-smoke checkpoint 与当前 observation contract 不兼容，已在评估前排除。
- UCB 基线是乐观探索策略，不是专用 Bayesian information-gain 基线。
- 切换后只有两个实验，恢复时间是右删失诊断，不能估计长期样本效率。
- 材料规律交换是 benchmark 环境干预，不是对真实命名化学材料的断言。
- 生命周期护栏只覆盖每实验最后两个动作槽；被强制收尾的动作不是 Agent 的自由决策。
