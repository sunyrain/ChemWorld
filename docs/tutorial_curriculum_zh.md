# ChemWorld 教程课程地图

更新日期：2026-07-08

ChemWorld-Bench 的教程不是 Python 语法课，也不是一串互不相关的小游戏。它训练的是同一套 `ChemWorld` 物理化学世界中的闭环实验能力：提出假设、设计操作、读取仪器观测、建立局部 world model、优化下一轮实验、解释机理并提交可复现 artifact。

正式入口保持一致：

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-optimization-standard", seed=0)
```

建议从 Day 1 开始就使用 agent-facing 方法：

```python
print(env.unwrapped.task_prompt()["text"])
env.unwrapped.available_actions()
env.unwrapped.validate_action({"operation": "heat", "duration_s": 10.0})
env.unwrapped.observation_view("lab_report")
```

这些方法把 task card、动作合法性、仪器观测和 campaign 进度变成学生/GPT/BO/RL 都能读取的公开接口。

## 课程总目标

学生完成 Day 1-12 后，应能独立完成：

1. 根据 task card 识别目标、预算、可用操作、仪器和约束。
2. 使用统一 operation language 执行虚拟实验并保存 JSONL trajectory。
3. 理解 ontology、physical constitution、partial observation、measurement cost 和 safety cost。
4. 从有限实验中建立局部 surrogate/world model。
5. 使用 human strategy、GPT-style planner、random/LHS/BO/safe BO 等方法比较闭环决策效率。
6. 诊断 public/private generalization gap，避免只在公开世界刷分。
7. 提交包含 trajectory、manifest、results 和 explanation 的可复现项目包。

## 难度坡度

| 阶段 | Notebook | 难度 | 主要能力 | 典型交付 |
| --- | --- | --- | --- | --- |
| A. 进入世界 | Day 1-3 | 入门 | 环境调用、状态账本、仪器观测、非全知测量 | 一条可回放轨迹、一张仪器/实验图、一段机制假设 |
| B. 认识规律 | Day 4-6 | 进阶 | 机制扫描、局部 surrogate、baseline 和 leaderboard 指标 | 机制扫描图、局部模型误差表、baseline 对比表 |
| C. 形成项目 | Day 7-9 | 进阶到挑战 | 可复现 artifact、GPT-style planner、BO/safe BO | submission bundle、可执行 recipe、BO 轨迹分析 |
| D. 接近科研评测 | Day 10-12 | 挑战 | public/private split、泛化诊断、最终展示 | public 结果、private gap 分析、Demo Day 报告 |
| E. 研究延展 | Day 13 + project blueprint | 研究延展 | 结晶、蒸馏、连续流、电化学和课程 leaderboard 设计 | 一个跨过程 task 的最小闭环设计 |

## 每日路线

| 天数 | 文件 | 只解决什么 | 不要求什么 | 本日交付 |
| --- | --- | --- | --- | --- |
| Day 1 | `day_01_enter_virtual_lab.ipynb` | 第一次进入 `ChemWorld`，完成一条从动作到观测的实验轨迹 | 不要求优化，也不要求懂完整机理 | 轨迹表或 JSONL、第一张实验图、下一轮假设 |
| Day 2 | `day_02_ontology_and_constitution.ipynb` | 理解物质、相、容器、操作和 physical constitution | 不要求写新 simulator | 一个被 constitution 拦截的错误动作和修复版 |
| Day 3 | `day_03_observation_and_instruments.ipynb` | 比较 HPLC、GC、UV-vis、FinalAssay 的成本、噪声和信息量 | 不要求一次测完所有真值 | 仪器选择理由、一张 raw signal 或谱图、观测不确定性说明 |
| Day 4 | `day_04_mechanism_scans.ipynb` | 扫描温度、时间、催化剂、溶剂、浓度，形成化工直觉 | 不要求训练复杂模型 | 机制解释图、风险-性能权衡、下一轮实验建议 |
| Day 5 | `day_05_surrogate_modeling.ipynb` | 从轨迹训练局部 surrogate，理解误差和不确定性 | 不要求模型全局准确 | 预测模型、误差分析、候选条件排序 |
| Day 6 | `day_06_baselines_and_leaderboard.ipynb` | 比较 random、LHS、scripted、BO、safe BO 的样本效率与安全性 | 不要求只追最高分 | baseline 对比表、sample efficiency 和 safety cost 解释 |
| Day 7 | `day_07_capstone_artifact.ipynb` | 把前 6 天成果整理成可复现小项目 | 不要求做完私有榜 | manifest、trajectory、results、explanation 的小型提交包 |
| Day 8 | `day_08_gpt_planner_and_validation.ipynb` | 把 GPT-style proposal 变成可验证、可执行的 recipe | 不依赖在线 GPT API | 原始 plan、validator 反馈、修复后的操作序列 |
| Day 9 | `day_09_bayesian_optimization.ipynb` | 理解 BO 和 safe BO 如何利用历史数据闭环选点 | 不要求手写完整 GP 库 | BO 初始点、acquisition 阶段、best-score 曲线 |
| Day 10 | `day_10_public_leaderboard_challenge.ipynb` | 在 public-test 上组织一次标准提交 | 不鼓励手工刷榜 | public 结果 JSON、验证日志、策略说明 |
| Day 11 | `day_11_private_generalization.ipynb` | 诊断 public/private gap 和过拟合 | 不追求泄露 private 参数 | 泛化差距表、失败分析、下一版策略 |
| Day 12 | `day_12_demo_day_artifact.ipynb` | 形成最终展示：性能、机理、风险、复现性并重 | 不只展示最高分 | Demo Day 报告骨架、项目摘要、可复现证据 |
| Day 13 | `day_13_year2_process_modules.ipynb` | 理解同一 world law 下如何扩展到结晶、蒸馏、连续流、电化学 | 不要求所有模块达到专业库精度 | 一个跨过程 task 的最小闭环和后续开发计划 |
| 项目 | `project_leaderboard_blueprint.ipynb` | 设计本机教师端/学生端 leaderboard 与项目制提交 | 不做云端账号系统 | 课程评测机流程、榜单指标、提交协议 |

## 每天的 3 小时节奏

| 时间 | 活动 | 必须留下的证据 |
| --- | --- | --- |
| 0:00-0:30 | 明确今天的化工问题、task card、预算和评分指标 | 一句任务目标和当前限制 |
| 0:30-1:00 | 跑通最小代码或最小实验 | 第一条 observation 或 validator 结果 |
| 1:00-1:30 | 完成核心实验、扫描、模型或 baseline | 轨迹表、模型表或指标表 |
| 1:30-2:00 | 验证、修复、对比或 debug | verify/validator/对比结果 |
| 2:00-2:30 | 可视化、解释或选择下一轮实验 | 图、谱图、候选表或解释草稿 |
| 2:30-3:00 | 保存 artifact 并写反思 | JSONL、manifest、结果摘要和下一步计划 |

如果课堂只有 90 分钟，建议现场完成前三段，把后三段作为课后提交。

## 分层任务设计

每个 notebook 现在都用同一种分层方式组织：

| 层级 | 面向对象 | 完成标准 |
| --- | --- | --- |
| 基础任务 | 所有学生 | 能运行、能保存、能解释一个最小闭环 |
| 进阶任务 | 已经跑通基础任务的学生 | 能比较多个条件、多个仪器或多个策略 |
| 挑战任务 | 项目组长、研究型学生或 agent 组 | 能形成策略改进、泛化诊断或可复现提交 |
| 反思问题 | 所有人 | 能把数值结果翻译成化工意义和下一步实验 |

## 每日最小工作量

每个 notebook 都新增了 `三小时实验工单（必须自己完成）` 和 `学生工作区`。学生不能只运行已保存输出；每一天至少要留下：

- 一组自己新增的实验、扫描、baseline、模型或提交结果。
- 一张表：记录 action、observation、score/risk/cost、instrument 或 metric。
- 至少一张图或谱图：用于解释趋势、噪声、风险或泛化差距。
- 一条验证证据：validator、verify、leaderboard row、模型误差或 sanity assertion。
- 一段文字结论：机制解释、失败分析、下一轮实验设计。

建议教师把“新增实验数量”和“解释质量”作为课堂检查点。示例阈值：Day 4 至少 20 个机制扫描实验，Day 5 至少 30 条建模样本，Day 6 至少 5 类 baseline 各 3 个 seed，Day 9 至少让 BO 进入 3 次 acquisition 决策。

## 评分建议

不要只看最高分。建议课程评分分成五项：

| 项目 | 权重 | 证据 |
| --- | --- | --- |
| 实验闭环能力 | 25% | 能独立运行 task、保存 JSONL、通过 verify |
| 建模与优化 | 25% | surrogate、BO 或 heuristic 是否真正使用历史数据 |
| 安全与成本意识 | 15% | 是否解释并控制 risk、cost、invalid operation |
| 机理解释 | 20% | 是否能把结果联系到温度、时间、催化剂、溶剂、副反应、分离损失等机制 |
| 可复现 artifact | 15% | manifest、trajectory、results、explanation 是否完整 |

## 教师端准备

课前建议执行：

```bash
python -m pip install -e ".[dev,notebooks]"
python -m ipykernel install --user --name chemworld --display-name "Python (ChemWorld)"
python -m pytest
python -m mkdocs build --strict
```

如果使用本机评测机，把学生提交集中到 `local_eval_server/teacher_server/submissions_inbox/`，由教师端统一执行 validate、verify、evaluate、summarize 和 leaderboard export。
