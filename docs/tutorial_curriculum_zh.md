# ChemWorld 教程课程地图

更新日期：2026-07-08

这套教程面向本科高年级、研究生入门、AI4Science workshop 或课题组 onboarding。它不是把 Python 语法重新包装成小游戏，而是让学生和 agent 在同一个 `ChemWorld` 物理化学世界中完成实验设计、观测、建模、优化、解释和提交。

## 课程结构

教程分为三层：

| 层级 | Notebook | 目标 |
| --- | --- | --- |
| 核心闭环 | Day 1-7 | 会调用环境、记录轨迹、理解 ontology/constitution/instrument、建立局部模型、提交可复现实验 artifact。 |
| Benchmark 强化 | Day 8-12 | 会使用 validator、BO、安全优化、public/private generalization、submission bundle 和 demo-day 报告。 |
| Year 2 扩展 | Day 13 + project blueprint | 把同一世界扩展到结晶、蒸馏、连续流、电化学和课程 leaderboard。 |

所有 notebook 都围绕同一个正式 Gym 入口：

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-optimization-standard", seed=0)
```

## 每日路线

| 天数 | 文件 | 学习重点 | 学生产出 |
| --- | --- | --- | --- |
| 1 | `day_01_enter_virtual_lab.ipynb` | 进入虚拟实验室，完成第一条实验轨迹。 | 轨迹表、第一张实验图、初始机制假设。 |
| 2 | `day_02_ontology_and_constitution.ipynb` | ontology、单位、物理宪法、动作前置条件。 | 一个被 constitution 拦截的错误动作和修正版本。 |
| 3 | `day_03_observation_and_instruments.ipynb` | HPLC、GC、UV-vis、final assay、非全知观测。 | 仪器成本/噪声/信息量比较。 |
| 4 | `day_04_mechanism_scans.ipynb` | 温度、时间、催化剂、溶剂、风险扫描。 | 机制解释图和下一轮实验建议。 |
| 5 | `day_05_surrogate_modeling.ipynb` | 用轨迹训练局部 surrogate model。 | 简单预测模型、不确定性或误差分析。 |
| 6 | `day_06_baselines_and_leaderboard.ipynb` | random、LHS、scripted、BO、安全 BO 与指标。 | baseline 对比表。 |
| 7 | `day_07_capstone_artifact.ipynb` | 复现实验、评测、验证和机制解释。 | 小型 submission artifact。 |
| 8 | `day_08_gpt_planner_and_validation.ipynb` | GPT-style proposal、validator、动作修复。 | 一组可执行的 agent 操作计划。 |
| 9 | `day_09_bayesian_optimization.ipynb` | BO / safe BO 收敛、风险、样本效率。 | BO 轨迹和 acquisition 阶段分析。 |
| 10 | `day_10_public_leaderboard_challenge.ipynb` | public-test 提交演练和 JSONL 轨迹验证。 | public leaderboard 结果。 |
| 11 | `day_11_private_generalization.ipynb` | public/private gap 与过拟合诊断。 | 泛化分析报告。 |
| 12 | `day_12_demo_day_artifact.ipynb` | Demo Day：性能、机制、可复现性和报告。 | 最终展示材料。 |
| 13 | `day_13_year2_process_modules.ipynb` | 结晶、蒸馏、连续流、电化学过程模块。 | 一个跨过程 task 的最小闭环结果。 |
| 项目 | `project_leaderboard_blueprint.ipynb` | 教师端/学生端评测组织、榜单设计、项目制提交。 | 课程 leaderboard 方案。 |

## 教学节奏

推荐每天 3 小时：

| 时间 | 活动 |
| --- | --- |
| 0:00-0:25 | 今日化工问题、任务目标和评价方式。 |
| 0:25-0:55 | 最小代码演示，强调可复现 seed、action schema 和观测限制。 |
| 0:55-1:45 | 学生使用 Python/GPT/agent 推进实验。 |
| 1:45-2:30 | 小组 debug、策略比较、机制解释。 |
| 2:30-3:00 | 保存轨迹、更新榜单、写当日反思。 |

## 评分建议

不要只看最高分。建议课程评分分成五项：

| 项目 | 权重 | 证据 |
| --- | --- | --- |
| 实验闭环能力 | 25% | 能独立运行 task、保存 JSONL、通过 verify。 |
| 建模与优化 | 25% | surrogate/BO/heuristic 是否真正使用历史数据。 |
| 安全与成本意识 | 15% | 是否解释并控制 risk、cost、invalid operation。 |
| 机制解释 | 20% | 是否能把结果联系到温度、时间、催化剂、溶剂、副反应、分离损失等机制。 |
| 可复现 artifact | 15% | manifest、trajectory、results、explanation 是否完整。 |

## 教师端准备

课前建议执行：

```bash
python -m pip install -e ".[dev,notebooks]"
python -m ipykernel install --user --name chemworld --display-name "Python (ChemWorld)"
python -m pytest
python -m mkdocs build --strict
```

如果使用本机评测机，请把学生提交集中到 `local_eval_server/teacher_server/submissions_inbox/`，由教师端统一执行 validate、verify、evaluate、summarize 和 leaderboard export。

## 当前状态

当前仓库已保存执行输出的教程包括 Day 1-13 和 project leaderboard blueprint。Notebook 中不再使用自定义 HTML checkpoint 组件；每日交付要求以普通 Markdown 呈现，方便阅读、打印和二次编辑。
