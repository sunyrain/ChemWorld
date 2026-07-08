# ChemWorld 教程 Notebook

这套 notebook 面向本科高年级、研究生入门、AI4Science workshop 或课题组 onboarding。核心目标不是再教一遍 Python 语法，而是让学生在同一个 `ChemWorld` 物理化学世界里完成实验设计、观测、建模、优化、解释和提交。

## 环境准备

请在项目根目录执行：

```bash
python -m pip install -e ".[dev,notebooks]"
python -m ipykernel install --user --name chemworld --display-name "Python (ChemWorld)"
```

打开 notebook 后选择 `Python (ChemWorld)` 内核。

## 课堂使用方式

每个教程 notebook 都按 3 小时工作坊设计，并在开头提供 6 个半小时工作块：

| 时间 | 用途 |
| --- | --- |
| 0:00-0:30 | 明确问题、入口、任务合同或数据对象。 |
| 0:30-1:00 | 运行最小示例，确认工具链和观测字段。 |
| 1:00-1:30 | 完成第一轮核心实验或模型操作。 |
| 1:30-2:00 | 比较、验证、修复或解释中间结果。 |
| 2:00-2:30 | 形成策略、图表、指标或 artifact。 |
| 2:30-3:00 | 写出机制解释、失败分析和下一步计划。 |

如果课堂只有 90 分钟，可以完成前 3 个时间盒，把后 3 个作为课后提交。

## Notebook 路线

| 天数 | Notebook | 重点产出 |
| --- | --- | --- |
| 1 | `day_01_enter_virtual_lab.ipynb` | 第一条闭环实验轨迹、第一张实验图、下一轮假设。 |
| 2 | `day_02_ontology_and_constitution.ipynb` | ontology/constitution 理解、非法动作与修复动作。 |
| 3 | `day_03_observation_and_instruments.ipynb` | 仪器成本/噪声/信息量对比，HPLC/UV-vis raw signal 图。 |
| 4 | `day_04_mechanism_scans.ipynb` | 温度、时间、催化剂、溶剂和安全风险扫描。 |
| 5 | `day_05_surrogate_modeling.ipynb` | 局部 surrogate model、误差分析、候选推荐。 |
| 6 | `day_06_baselines_and_leaderboard.ipynb` | random、LHS、scripted、BO、safe BO 的指标对比。 |
| 7 | `day_07_capstone_artifact.ipynb` | trajectory、evaluation、verification、explanation 小型提交包。 |
| 8 | `day_08_gpt_planner_and_validation.ipynb` | GPT-style plan、validator 修复、可执行 recipe。 |
| 9 | `day_09_bayesian_optimization.ipynb` | BO / safe BO 的收敛、风险和样本效率分析。 |
| 10 | `day_10_public_leaderboard_challenge.ipynb` | public-test 提交演练、manifest、结果 JSON。 |
| 11 | `day_11_private_generalization.ipynb` | public/private gap 和过拟合诊断。 |
| 12 | `day_12_demo_day_artifact.ipynb` | Demo Day 展示材料和最终科学闭环。 |
| 13 | `day_13_year2_process_modules.ipynb` | 结晶、蒸馏、连续流、电化学过程模块。 |
| 项目 | `project_leaderboard_blueprint.ipynb` | 课程 leaderboard、教师端/学生端评测、项目提交协议。 |

## 教师建议

- 让学生每 30 分钟保存一个小证据：表格、图、JSONL、验证结果、解释文本或下一轮实验建议。
- 不要只奖励最高分；同时评价安全、样本效率、可复现性、机制解释和日志质量。
- 鼓励学生使用 GPT，但必须通过 action schema、validator、verify 和最终轨迹记录约束它。
- 谱图和色谱数据位于 `info["raw_signal"]` 或 trajectory `raw_signal`，适合让学生做仪器观测和机制解释练习。
