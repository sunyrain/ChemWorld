# Agent Observatory 与 Student Lab

ChemWorld Task Lab 将智能体评测和学生实验拆分为两个独立界面。二者使用相同的任务合同与世界律，
但不会混合操作流程：研究者关注模型性能和轨迹，学生关注实验决策及即时反馈。

## 启动

在仓库根目录运行：

```powershell
python -m apps.task_lab.server --port 8876
```

Windows 下即使尚未激活虚拟环境，仓库也会自动使用 `.venv\Scripts\python.exe` 重新启动。
首次使用且依赖尚未安装时，请运行：

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

| 入口 | 地址 | 是否需要模型 API |
| --- | --- | --- |
| 产品首页 | `http://127.0.0.1:8876/` | 否 |
| Agent Observatory | `http://127.0.0.1:8876/agent/` | DeepSeek 需要；经典算法不需要 |
| Student Lab | `http://127.0.0.1:8876/student/` | 否 |

!!! warning "仅在本机使用"
    服务默认绑定 `127.0.0.1`。不要将包含模型凭据的服务直接暴露到公网。

## Agent Observatory

Agent 端支持搜索和选择全部 15 个任务，也可使用快速双任务、严肃任务集或全任务预设。运行时页面
通过实时事件流展示：

- 当前任务与逐步决策依据；
- 动作是否合法、修正过程和剩余预算；
- HPLC、GC、UV-Vis、IR、NMR 原始公开曲线与峰表；
- 模型对公开峰形、主要峰组和不确定性的结构化解读；
- 公开指标、最佳分数和 final assay 状态；
- 模型调用数、token 用量和动作有效率；
- 每个任务的回放验证结果与可导出的评测汇总。

两种策略模式适用于不同目的：

- **逐步自适应（adaptive，默认）**：每一步都发送最新公开观测、谱图曲线、峰表和当前合法动作，
  要求模型先解释证据，再选择下一步；
- **整段规划（plan）**：仅作为低调用成本的基线对照，不作为产品默认模式。

界面展示的是模型主动返回的结构化决策记录，包括公开证据、谱图解读、实验假设、动作依据和
不确定性。模型侧可以开启强化推理，但隐藏逐字思维链不会写入轨迹或发送到浏览器。

### 谱图证据档位

Agent 端可选择三种可复现实验条件：

| 档位 | 模型获得的信息 | 用途 |
| --- | --- | --- |
| `raw` | 降采样原始曲线，不含峰表 | 原始信号读取下限 |
| `unassigned` | 曲线以及未指认峰中心、面积和检出状态 | 默认严肃评测 |
| `assigned` | 曲线和带物种/峰组标签的峰表 | 教学或信息上限 |

选择 `raw` 或 `unassigned` 时，prompt 中的 lab-report 峰组汇总也会同步删除，避免从另一字段泄露
target/reactant/byproduct。Student Lab 保留已指认教学视图，不受 Agent 消融设置影响。

### 实验条件差异审计

每次 final assay 后，系统从实际执行的溶剂、投料、催化剂和温度程序中建立条件签名，并选择条件
距离最近的历史实验作为参考。事件流和结果 JSON 会标记：初始基线、完全重复、单因素对照或多因素
变化，并列出真实变化字段与分数差。该指标描述设计结构，不把 BO 的多变量选点错误判为失败；但当
模型声称单因素因果结论时，多因素变化会成为可直接检查的归因风险。

### 扩展研究档位

面板中的“实验预算”可选择 1× 到 4×，“连续实验 Campaign”允许原本的单实验任务在终检后
开始下一轮。系统会把每轮公开条件、仪器、谱图结论、终检指标和分数压缩为实验记忆，下一轮
明确接收这些记录。剩余预算不足一个最小完整反应配方时，调度器停止启动新实验。

1× 且不覆盖 campaign 时使用冻结的官方任务合同。预算放大或 campaign override 都会切换为
`extended-research`，只产生 `research_score`；该分数与 `official_score` 和官方榜单严格隔离。

### 经典主动学习后端

Agent 后端可切换为：

- `random_recipe`：随机完整配方对照；
- `latin_hypercube`：空间填充初始设计；
- `greedy_local`：围绕历史最佳配方进行局部扰动；
- `gp_pi`：Matérn Gaussian Process + Probability of Improvement；
- `gp_ucb`：Matérn Gaussian Process + Upper Confidence Bound；
- `gp_bo`：Matérn Gaussian Process + Expected Improvement；
- `rf_ei`：Random Forest ensemble + Expected Improvement；
- `safe_gp_bo`：分数 GP 与风险 GP 共同约束的 Expected Improvement，并自动采用公开任务的
  更严格安全上限。

GP、RF 和安全约束代理先做 4 个初始配方，第 5 个配方起使用已完成 final assay 的实验拟合代理模型；
随机、LHS 与局部搜索按各自规则直接选点。事件流会
展示训练样本数、采集阶段、采集函数值、历史最优和选中配方。经典配方编译器只适用于兼容的
反应任务，界面会禁用不兼容任务。运行经典算法不需要模型 API key。

### 配置 DeepSeek

=== "PowerShell"

    ```powershell
    $env:DEEPSEEK_API_KEY = (Get-Content .\deepseek_api.md -Raw).Trim()
    $env:DEEPSEEK_MODEL = "deepseek-v4-pro"
    python -m apps.task_lab.server --port 8876
    ```

=== "bash"

    ```bash
    export DEEPSEEK_API_KEY="..."
    export DEEPSEEK_MODEL="deepseek-v4-pro"
    python -m apps.task_lab.server --port 8876
    ```

API key 只由本地 Python 服务读取，不进入浏览器、prompt artifact、trajectory 或
`evaluation_result.json`。

当前默认使用 V4 Pro、thinking 和 `reasoning_effort=max`。CLI 可用
`--reasoning-effort high` 降低推理强度。DeepSeek 的当前模型名称与参数以
[官方 API 文档](https://api-docs.deepseek.com/)和
[thinking mode 指南](https://api-docs.deepseek.com/guides/thinking_mode/)为准。

### 材料标签

界面把稳定数字 action 值同时显示为 Water、Ethanol、Acetonitrile、Toluene 或 Catalyst A–D。
真实溶剂名称表示身份，不表示当前任务的动力学已经由该物料的参考物性预测；Catalyst A–D 仍是
匿名 benchmark 配方。详见[材料身份与真实化学边界](material_identity.md)。

### 全任务命令行评测

```powershell
python -m apps.task_lab.run_evaluation --all-tasks --mode adaptive --max-steps 24
```

每次运行会生成 `evaluation_summary.json`，并为每个任务保存模型计划、完整轨迹和经过回放验证的
评分结果。可用 `--tasks <task-id...>` 选择部分任务，用 `--resume --output-dir <目录>` 续跑。

扩展 DeepSeek campaign：

```powershell
python -m apps.task_lab.run_evaluation --tasks reaction-to-assay --mode adaptive `
  --max-steps 36 --budget-multiplier 2 --campaign-override `
  --spectrum-disclosure unassigned
```

经典 GP-EI：

```powershell
python -m apps.task_lab.run_evaluation --agent gp_bo `
  --tasks reaction-optimization-standard --max-steps 72
```

## Student Lab

学生端先选择任务与 seed，再从当前合法操作中选择动作并填写参数。每次提交都会同步更新：

1. 动作是否合法，以及失败时的参数修正建议；
2. 已用/剩余预算和 experiment index；
3. 可见分数、产率、风险、成本或表征指标；
4. 数字反应器、仪器摘要和最佳得分学习曲线；
5. 可切换通道的 HPLC、GC、UV-Vis、IR、NMR 曲线与公开峰指认；
6. 可下载的完整操作—观测实验记录。

非法动作会在执行前被拒绝，不消耗预算，也不会改变世界状态。学生可将验证器作为实验前检查，
而不需要通过失败来猜测环境规则。

## 分数含义

`official_score` 只属于冻结合同下的合法 final assay；扩展研究终检写入 `research_score`。
`total_score` 是评测层的综合值，还会反映安全、成本、
非法动作和样本效率。没有 final assay 时，页面明确显示“未评分”，不会把中间 reward 当作正式
成绩。公开—私有泛化任务在本地只能产生占位评分；正式私有榜单结果必须由持有私有盐的评测服务生成。
