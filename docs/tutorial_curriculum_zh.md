# ChemWorld 教程课程地图

更新日期：2026-07-08

ChemWorld-Bench 现在已经可以作为一个科研型虚拟自驱实验课程底座使用。它的核心不是“多个小游戏”，而是同一个 `ChemWorld` 物理化学世界规律下的不同 task slice。学生、LLM agent、BO、safe BO 和人工策略都在同一个实验接口、同一套日志和同一套评测协议下工作。

## 现在能做什么

| 能力 | 怎么做 | 产出 |
| --- | --- | --- |
| 运行虚拟实验 | `gym.make("ChemWorld", task_id=..., seed=...)` 后执行事件动作。 | observation、reward、info、trajectory。 |
| 设计反应条件 | 操作 `add_solvent`、`add_reagent`、`add_catalyst`、`heat`、`terminate`、`measure`。 | 产率、选择性、转化率、风险、成本。 |
| 做后处理和分离 | 使用 `add_extractant`、`mix`、`settle`、`separate_phase`、`wash`、`dry`、`concentrate`。 | purity、recovery、phase ratio、mass balance error。 |
| 使用仪器观测 | 选择 HPLC、GC、UV-vis、final assay。 | noisy processed estimate、uncertainty、raw spectral signal。 |
| 生成谱图/色谱 | 读取 `info["raw_signal"]` 或 trajectory `raw_signal`。 | HPLC/GC 色谱、UV-vis、IR、NMR proxy spectra。 |
| 验证动作合法性 | 使用 validator、action schema、recipe compiler。 | invalid reasons、修复后的 recipe。 |
| 训练局部模型 | 从轨迹抽取特征，训练 surrogate model。 | 预测、误差、候选实验推荐。 |
| 运行 baseline | 使用 random、LHS、scripted、GP BO、RF EI、safe BO。 | baseline table、leaderboard metrics。 |
| 组织评测 | 运行 `chemworld run/evaluate/verify/suite/leaderboard`。 | JSONL、manifest、results、leaderboard。 |
| 做课程项目 | 使用 submission bundle 和本机教师端/学生端评测流程。 | 可审核项目包和排名结果。 |

## 推荐学习路径

| 阶段 | Notebook | 学生能力 |
| --- | --- | --- |
| 核心闭环 | Day 1-7 | 会调用环境、记录轨迹、理解 ontology/constitution/instrument、建立局部模型、提交可复现实验 artifact。 |
| Benchmark 强化 | Day 8-12 | 会使用 validator、BO、安全优化、public/private generalization、submission bundle 和 demo-day 报告。 |
| 过程扩展 | Day 13 + project blueprint | 会把同一世界扩展到结晶、蒸馏、连续流、电化学和课程 leaderboard。 |

所有 notebook 都围绕同一个正式 Gym 入口：

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-optimization-standard", seed=0)
```

## 每日 Notebook

| 天数 | 文件 | 学习重点 | 学生交付 |
| --- | --- | --- | --- |
| 1 | `day_01_enter_virtual_lab.ipynb` | 进入虚拟实验室，完成第一条实验轨迹。 | 轨迹表、第一张实验图、初始机制假设。 |
| 2 | `day_02_ontology_and_constitution.ipynb` | ontology、单位、物理宪法、动作前置条件。 | 一个被 constitution 拦截的错误动作和修正版本。 |
| 3 | `day_03_observation_and_instruments.ipynb` | HPLC、GC、UV-vis、final assay、虚拟谱图、非全知观测。 | 仪器成本/噪声/信息量比较和一张 raw signal 图。 |
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

## 每 30 分钟工作节奏

每个教程 notebook 的开头都已经加入 6 个时间盒。推荐每天 3 小时：

| 时间 | 活动 | 证据 |
| --- | --- | --- |
| 0:00-0:30 | 明确今天的化工问题、任务合同和评价指标。 | 写出任务目标或 task card 摘要。 |
| 0:30-1:00 | 运行最小代码或最小实验。 | 得到第一条 observation 或检查表。 |
| 1:00-1:30 | 执行核心实验、扫描、模型或 baseline。 | 生成轨迹表、模型表或指标表。 |
| 1:30-2:00 | 验证、修复、对比或 debug。 | 留下 validator/verify/对比结果。 |
| 2:00-2:30 | 可视化、解释或选择下一轮实验。 | 得到图、谱图、候选表或解释草稿。 |
| 2:30-3:00 | 保存 artifact 并写反思。 | JSONL、manifest、结果摘要和下一步计划。 |

如果课堂只有 90 分钟，建议现场完成前 3 段，后 3 段作为课后提交。

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

如果使用本机评测机，把学生提交集中到 `local_eval_server/teacher_server/submissions_inbox/`，由教师端统一执行 validate、verify、evaluate、summarize 和 leaderboard export。
