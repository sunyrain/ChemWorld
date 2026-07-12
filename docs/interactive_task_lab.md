# Agent Observatory 与 Student Lab

ChemWorld Task Lab 将智能体评测和学生实验拆分为两个独立界面。二者使用相同的任务合同与世界律，
但不会混合操作流程：研究者关注模型性能和轨迹，学生关注实验决策及即时反馈。

## 启动

在仓库根目录运行：

```powershell
python -m apps.task_lab.server --port 8876
```

若密钥保存在仓库根目录的本地 `api.md`，无需先设置环境变量：

```powershell
python -m apps.task_lab.server --port 8876 --api-key-file .\api.md
```

该文件已被 Git 忽略；密钥只进入本地服务进程内存，不会进入浏览器、轨迹或结果文件。

Windows 下即使尚未激活虚拟环境，仓库也会自动使用 `.venv\Scripts\python.exe` 重新启动。
首次使用且依赖尚未安装时，请运行：

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

| 入口 | 地址 | 是否需要模型 API |
| --- | --- | --- |
| 产品首页 | `http://127.0.0.1:8876/` | 否 |
| Agent Observatory | `http://127.0.0.1:8876/agent/` | 在线模型需要；经典算法不需要 |
| Student Lab | `http://127.0.0.1:8876/student/` | 否 |

!!! warning "仅在本机使用"
    服务默认绑定 `127.0.0.1`。不要将包含模型凭据的服务直接暴露到公网。

## Agent Observatory

Agent 端支持搜索和选择全部 15 个任务，也可使用快速双任务、严肃任务集或全任务预设。运行时页面
通过实时事件流展示：

- 当前任务与逐步决策依据；
- 动作是否合法、修正过程和剩余预算；
- HPLC、GC、UV-Vis、IR、NMR 原始公开曲线与峰表；
- 模型可读取的历史谱图目录、主动请求事件，以及该轮实际取回的谱图载荷；
- 可按任务、实验、步骤和来源回看全部历史谱图，并用前后按钮逐张比较；
- 模型对公开峰形、主要峰组和不确定性的结构化解读；
- 公开指标、最佳分数和 final assay 状态；
- 模型调用数、token 用量和动作有效率；
- 每个任务的回放验证结果与可导出的评测汇总。

两种策略模式适用于不同目的：

- **逐步自适应（adaptive，默认）**：每一步发送最新公开报告、历史谱图目录和当前合法动作。目录只含
  仪器、实验和步骤等索引；模型明确返回 `spectrum_request_id` 后，系统才在下一次调用中提供指定谱图；
- **整段规划（plan）**：仅作为低调用成本的基线对照，不作为产品默认模式。

界面展示的是模型主动返回的结构化决策记录，包括公开证据、谱图解读、实验假设、实验意图、
历史对照、动作依据和不确定性。`MEASUREMENT OUTPUT` 表示刚完成实验的输出，
`MODEL RETRIEVAL · DECISION N` 表示模型主动请求并实际收到的谱图载荷。没有请求时，历史曲线和峰表
不会自动进入模型上下文。模型侧可以开启强化推理，
但隐藏逐字思维链不会写入轨迹或发送到浏览器。

### 反应器与实验边界

一次实验内的操作共享同一个反应器状态。加料会进入当前釜并累积体积或物料量；连续 `heat`/`wait`
会从当前组成和温度继续积分，因此反应时间、转化、能耗与风险都会累计。HPLC 等中间测量读取当前实验，
同时扣除相应样品体积和仪器成本，但不会自动生成一个新的配方实验。

只有成功完成 `final_assay` 才形成一个可独立比较的已完成实验。在 `single_experiment` 模式下这会结束
episode；在 `campaign` 模式下系统记录终检结果、增加 experiment index，并以相同世界参数恢复一只
全新的初始反应器。因而，同一釜内继续升温或追加物料不能被描述为独立对照实验；溶剂和催化剂类别也
应在单次实验内保持为同一配方选择。Agent prompt 会显式收到这些状态语义。

### 谱图证据档位

Agent 端可选择三种可复现实验条件：

| 档位 | 模型获得的信息 | 用途 |
| --- | --- | --- |
| `raw` | 降采样原始曲线，不含峰表 | 原始信号读取下限 |
| `unassigned` | 曲线以及未指认峰中心、面积和检出状态 | 默认严肃评测 |
| `assigned` | 曲线和带物种/峰组标签的峰表 | 教学或信息上限 |

选择 `raw` 或 `unassigned` 时，按需取回的载荷不会包含更高档位的峰信息。未请求谱图时，prompt 中
只出现可用目录和 `retrieval_required` 标记，不包含曲线、峰表或峰组汇总。Student Lab 保留已指认
教学视图，不受 Agent 消融设置影响。

### 操作效果与有效输入

Agent 和 Student 共用一套公开操作语义。每个可执行动作会说明它属于累计投料、连续过程、配置更新、
取样扣除、库存选择还是带损失转移；执行后再返回实际的 `Δt`、`ΔV`、样品消耗、风险和成本增量。
这能区分“修改设备设定”和“真正处理当前物料”，也能区分最近一次过程指标与累计库存变化。

交互入口只接受当前运行时会原样执行的范围，避免合法输入在内核中被静默裁剪或改义。例如：

- 结晶种子、加相体积以及冷却、蒸发、蒸馏和流动反应温区使用有效运行范围；
- `add_phase` 只开放当前实现支持的 aqueous/organic 液相；
- 当前萃取模型只开放 organic 功能相，不把 extractant 名称表述成尚未实现的独立物性效应；
- 单次结晶实验只接受一次晶种投加；同一实验内溶剂和催化剂类别保持锁定。

这些约束只对交互入口做输入—运行时对齐，不改变冻结任务的世界律或评分函数。

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

### 配置在线模型

=== "本地 key 文件"

    ```powershell
    python -m apps.task_lab.server --port 8876 --api-key-file .\api.md
    ```

=== "PowerShell"

    ```powershell
    $env:DEEPSEEK_API_KEY = "<your-api-key>"
    $env:DEEPSEEK_MODEL = "<provider-model-id>"
    python -m apps.task_lab.server --port 8876
    ```

=== "bash"

    ```bash
    export DEEPSEEK_API_KEY="..."
    export DEEPSEEK_MODEL="<provider-model-id>"
    python -m apps.task_lab.server --port 8876
    ```

API key 只由本地 Python 服务读取，不进入浏览器、prompt artifact、trajectory 或
`evaluation_result.json`。

模型标识和可用推理参数可能随 provider 更新。请使用 provider 当前 API 文档列出的模型 ID；
正式比较必须把 provider、模型 ID、请求参数、prompt hash、token 来源和调用时间写入方法账本。
密钥只通过进程环境变量传入，不要保存在仓库、轨迹、prompt artifact 或提交包中。

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
4. 由公开事务增量驱动的数字实验动画、仪器摘要和最佳得分学习曲线；
5. 可切换通道的 HPLC、GC、UV-Vis、IR、NMR 曲线与公开峰指认；
6. 可从 session 操作记录重建并前后切换的历史谱图；
7. 可下载的完整操作—观测实验记录。

数字实验动画覆盖投料、升温、混合、取样/测量、分层、洗涤、结晶、过滤、蒸发、蒸馏、流动反应和
电化学过程。液位依据当前 experiment 的公开 `ΔV` 累积，测量会显示取样扣除，campaign 换釜后会
回到 fresh vessel。动画是已执行操作的状态示意，不会把未知组成、颜色或晶体形貌伪装成观测结果。

非法动作会在执行前被拒绝，不消耗预算，也不会改变世界状态。学生可将验证器作为实验前检查，
而不需要通过失败来猜测环境规则。

## 分数含义

`official_score` 只属于冻结合同下的合法 final assay；扩展研究终检写入 `research_score`。
`total_score` 是评测层的综合值，还会反映安全、成本、
非法动作和样本效率。没有 final assay 时，页面明确显示“未评分”，不会把中间 reward 当作正式
成绩。公开—私有泛化任务在本地只能产生占位评分；正式私有榜单结果必须由持有私有盐的评测服务生成。
