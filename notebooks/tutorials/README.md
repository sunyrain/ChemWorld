# ChemWorld-Bench 十二天核心教程与 Year 2 扩展

请按顺序打开 notebook，并选择 `Python (ChemWorld)` 内核。

```bash
python -m pip install -e ".[dev,notebooks]"
python -m ipykernel install --user --name chemworld --display-name "Python (ChemWorld)"
```

## 课程主线

这套教程的目标不是教一个个孤立小游戏，而是让学生和 agent 在同一个 `ChemWorld` 物理化学世界中逐步学习：

- 如何调用虚拟实验环境；
- 如何理解 ontology、constitution、operation 和 instrument；
- 如何在部分可观测、有成本、有风险的条件下设计实验；
- 如何用轨迹数据建立局部 world model；
- 如何比较 random、LHS、BO、safe BO、GPT-style planner 和 human-in-loop 策略；
- 如何形成可复现 submission bundle 和 leaderboard 结果。

## 十二天核心安排与扩展

| 天数 | Notebook | 重点 |
| --- | --- | --- |
| 1 | `day_01_enter_virtual_lab.ipynb` | 进入虚拟实验室，完成第一条闭环实验轨迹 |
| 2 | `day_02_ontology_and_constitution.ipynb` | ontology、单位、物理宪法和动作前置条件 |
| 3 | `day_03_observation_and_instruments.ipynb` | 仪器观测、噪声、成本和非全知观测 |
| 4 | `day_04_mechanism_scans.ipynb` | 温度、时间、催化剂/溶剂和安全风险扫描 |
| 5 | `day_05_surrogate_modeling.ipynb` | 用实验轨迹训练局部 surrogate model |
| 6 | `day_06_baselines_and_leaderboard.ipynb` | random、LHS、scripted、BO、safe BO 和指标 |
| 7 | `day_07_capstone_artifact.ipynb` | 复现实验、评测、验证和机制解释 |
| 8 | `day_08_gpt_planner_and_validation.ipynb` | GPT-style proposal、validator 修复和实验执行 |
| 9 | `day_09_bayesian_optimization.ipynb` | BO / safe BO 收敛、风险和样本效率 |
| 10 | `day_10_public_leaderboard_challenge.ipynb` | public-test 提交演练和 JSONL 轨迹验证 |
| 11 | `day_11_private_generalization.ipynb` | public/private 泛化差距与过拟合诊断 |
| 12 | `day_12_demo_day_artifact.ipynb` | Demo Day：性能、机制、可复现性和报告 |
| 13 | `day_13_year2_process_modules.ipynb` | 结晶、蒸馏、连续流、电化学过程模块 |
| 项目 | `project_leaderboard_blueprint.ipynb` | 课程 leaderboard、项目赛道和提交协议设计 |

## Year 2 扩展建议

当前代码已经加入四类 Year 2 过程模块：

- 结晶：`reaction-to-crystallization`
- 蒸馏：`reaction-to-distillation`
- 连续流：`flow-reaction-optimization`
- 电化学：`electrochemical-conversion`

可以在十二天课程后增加 3-5 个项目日：

| 扩展日 | 主题 | 推荐任务 |
| --- | --- | --- |
| 13 | 结晶中的纯度/收率权衡 | `reaction-to-crystallization` |
| 14 | 蒸馏中的能耗/安全/回收权衡 | `reaction-to-distillation` |
| 15 | 连续流与批式反应策略比较 | `flow-reaction-optimization` |
| 16 | 电化学选择性与能效优化 | `electrochemical-conversion` |
| 17 | 跨过程 project leaderboard | 自选 task + submission bundle |

## 使用提示

- 缺失观测在 JSONL 中是 `null`，在 Gym array 中通常表示为 `NaN`。
- `observed_mask` 和 `observed_keys` 用于区分真实观测值和未观测字段。
- `final_assay` 是正式 leaderboard score 来源。
- 在 single-experiment task 中，`final_assay` 结束 episode。
- 在 campaign task 中，`final_assay` 结束当前 experiment，但 campaign 会继续到预算耗尽。
- 任何非法动作都会返回明确的 precondition failure，不应该被学生或 agent 静默忽略。

所有教程都应围绕同一个 `ChemWorld` 环境展开。新增过程任务只是同一世界规律下的 task slice，不是单独小游戏。
