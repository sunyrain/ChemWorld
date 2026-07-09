# ChemWorld 教程 Notebook

这套 notebook 面向本科高年级、研究生入门、AI4Science workshop 或课题组 onboarding。目标不是再讲一遍 Python 语法，而是让学习者在同一个 `ChemWorld` 物理化学世界中完成实验设计、观测、建模、优化、解释和提交。

## 环境准备

请在项目根目录执行：

```bash
python -m pip install -e ".[dev,notebooks]"
python -m ipykernel install --user --name chemworld --display-name "Python (ChemWorld)"
```

打开 notebook 后选择 `Python (ChemWorld)` 内核。

## 推荐学习方式

每个 notebook 都按 3 小时工作块设计，并在开头给出：

- 学习路径定位：难度、先修、今天只解决什么、本日交付。
- 课堂时间盒：每 30 分钟都要留下一个可检查证据。
- 本日任务梯度：基础任务、进阶任务、挑战任务和反思问题。
- 三小时实验工单：列出当天最低实验数量、图表、验证和文字交付。
- 学生工作区：留给学生新增代码和记录，不再只浏览已执行输出。
- 检查点：不用调用可视化 helper，直接在 markdown 里写清楚今天应提交什么。

如果课堂只有 90 分钟，建议现场完成前 3 个时间盒，把后 3 个作为课后提交。

可以用下面的命令检查教程是否仍然满足非平凡工作量要求：

```bash
python scripts/audit_tutorial_workload.py --output-dir runs/tutorial_audit
python -m pytest tests/test_tutorial_notebooks.py
```

该审计会检查 Day 1-12 是否包含 30 分钟时间盒、三小时实验工单、学生工作区、最低实验数量或提交数量、图表/验证/解释证据，以及是否残留乱码或旧式 checkpoint helper。

## 难度路线

| 阶段 | Notebook | 难度 | 学习重点 |
| --- | --- | --- | --- |
| 进入世界 | Day 1-3 | 入门 | 环境调用、物理宪法、仪器观测、局部证据 |
| 认识规律 | Day 4-6 | 进阶 | 机制扫描、surrogate、baseline 和 leaderboard |
| 形成项目 | Day 7-9 | 进阶到挑战 | 可复现 artifact、GPT-style planner、BO/safe BO |
| 科研评测 | Day 10-12 | 挑战 | public/private split、泛化诊断、最终展示 |
| 研究延展 | Day 13 + project blueprint | 延展 | 过程模块扩展和课程 leaderboard 设计 |

## Notebook 清单

| 天数 | 文件 | 本日交付 |
| --- | --- | --- |
| Day 1 | `day_01_enter_virtual_lab.ipynb` | 第一条闭环实验轨迹、第一张实验图、下一轮假设 |
| Day 2 | `day_02_ontology_and_constitution.ipynb` | ontology/constitution 理解、非法动作与修复动作 |
| Day 3 | `day_03_observation_and_instruments.ipynb` | 仪器成本/噪声/信息量对比，HPLC/UV-vis raw signal 图 |
| Day 4 | `day_04_mechanism_scans.ipynb` | 温度、时间、催化剂、溶剂和安全风险扫描 |
| Day 5 | `day_05_surrogate_modeling.ipynb` | 局部 surrogate model、误差分析、候选推荐 |
| Day 6 | `day_06_baselines_and_leaderboard.ipynb` | random、LHS、scripted、BO、safe BO 指标对比 |
| Day 7 | `day_07_capstone_artifact.ipynb` | trajectory、evaluation、verification、explanation 小型提交包 |
| Day 8 | `day_08_gpt_planner_and_validation.ipynb` | GPT-style plan、validator 修复、可执行 recipe |
| Day 9 | `day_09_bayesian_optimization.ipynb` | BO / safe BO 的收敛、风险和样本效率分析 |
| Day 10 | `day_10_public_leaderboard_challenge.ipynb` | public-test 提交演练、manifest、结果 JSON |
| Day 11 | `day_11_private_generalization.ipynb` | public/private gap 和过拟合诊断 |
| Day 12 | `day_12_demo_day_artifact.ipynb` | Demo Day 展示材料和最终科学闭环 |
| Day 13 | `day_13_year2_process_modules.ipynb` | 结晶、蒸馏、连续流、电化学过程模块 |
| 项目 | `project_leaderboard_blueprint.ipynb` | 课程 leaderboard、教师端/学生端评测、项目提交协议 |

## 教师建议

- 每 30 分钟要求一个小证据：表格、图、JSONL、验证结果、解释文本或下一轮实验建议。
- 把“自己新增的实验/模型/提交”作为硬要求；只点击运行演示单元不算完成。
- 不只奖励最高分；同时评价安全、样本效率、可复现性、机理解释和日志质量。
- 鼓励学生使用 GPT 或其他助手，但必须经过 action schema、validator、verify 和最终轨迹记录约束。
- 谱图、色谱和 raw signal 位于 `info["raw_signal"]` 或 trajectory `raw_signal`，适合用来训练仪器观测和机制解释。
