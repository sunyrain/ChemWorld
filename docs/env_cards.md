# 阅读环境卡

环境卡描述整个 ChemWorld Gym 环境：如何 reset、一次 step 返回什么、Agent 可以调用哪些辅助接口，
以及当前模型成熟度意味着什么。任务卡讲“这道题”，环境卡讲“这间实验室”。

## 创建环境

`ChemWorld` 是统一的 Gymnasium 环境入口。不同任务通过 `task_id` 选择，但它们共享同
一个物理化学世界律和运行时服务。

```python
env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=1)
```

环境卡用于说明任务能力、输入输出、成熟度和审计入口。它是 agent 作者理解 benchmark
合同的第一层机器可读/人类可读文档。

## Reset 后先看哪些信息

`reset()` 返回的 `info` 应包含：

- `task_id`
- `world_law_id`
- `task_maturity`
- 可见 scenario 信息
- budget 和 step limit
- 允许操作列表
- scoring metadata

隐藏 scenario 不应在公开 `info` 中泄露。

## 一次 Step 返回什么

`step(action)` 返回：

```python
obs, reward, terminated, truncated, info
```

其中 `info["constraint_flags"]` 是诊断 agent 行为的关键字段。无效动作应产生可解释
flag，而不是让状态静默损坏。

## Agent 推荐入口

`ChemWorldEnv` 现在直接暴露 agent-facing 方法：

- `task_prompt()`：返回任务说明、目标、预算、可用工具、成功指标和隐藏信息政策。
- `available_actions()`：返回当前 state 下合法操作及其 schema/preconditions。
- `action_schema(operation)`：查看单个 operation 的 payload、单位和推荐范围。
- `validate_action(action)`：只校验不执行，适合 LLM/tool planner 预检查。
- `observation_view("rl" | "tool_json" | "lab_report")`：面向 RL、工具 agent 和学生的三种公开观测视图。
- `campaign_state()`：返回 campaign/experiment 进度、remaining budget、best score 和 final assay count。

这些接口是 public observation view，不允许泄露 hidden state、hidden species amounts、rate constants 或 private eval 参数。

## 渲染与界面

当前 rendering 合同是结构化文本、实验状态、谱图 packet 和 campaign 进度数据。可视化层
应从这些公开字段派生，不能读取 hidden ledger。

## 自查与诊断

环境自洽性检查应覆盖注册任务、reset/step、replay、spectra、constitution 和 smoke
trajectory。检查结果应进入 release checklist。

## 环境自一致性证据

发布候选应说明注册任务、reset/step、replay、spectra、constitution 与 smoke trajectory 的检查状态，
并把失败项保留在发布说明中。使用者可通过[验证安装与结果](validation.md)检查自己的轨迹和提交包。

## 如何理解成熟度

环境卡必须明确哪些模块是 proxy/lite/reference-validated。没有成熟度标注的 task 不应
进入正式 benchmark claim。
