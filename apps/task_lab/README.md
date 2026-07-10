# ChemWorld Task Lab

Task Lab 提供两个彼此独立的本地产品界面：

- **Agent Observatory**：运行并观察 DeepSeek 或经典主动学习算法的逐轮探索过程；
- **Student Lab**：由学生手动提交实验操作，获得即时验证、数字反应器反馈和学习记录。

## 启动界面

在仓库根目录运行：

```powershell
python -m apps.task_lab.server --port 8876
```

即使当前 `python` 不是项目虚拟环境，该命令也会在 Windows 上自动转交给
`.venv\Scripts\python.exe`。如果项目尚未安装依赖，请先运行：

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

启动后可访问：

- 产品入口：<http://127.0.0.1:8876/>
- Agent Observatory：<http://127.0.0.1:8876/agent/>
- Student Lab：<http://127.0.0.1:8876/student/>

服务默认只监听 `127.0.0.1`。不要将带有模型凭据的本地服务直接暴露到公网。

## 配置 DeepSeek

不要把 key 写进 Python、前端或运行结果。仓库根目录的 `deepseek_api.md` 已被
`.gitignore` 排除。PowerShell 中可以将它只读入当前终端的环境变量：

```powershell
$env:DEEPSEEK_API_KEY = (Get-Content .\deepseek_api.md -Raw).Trim()
$env:DEEPSEEK_MODEL = "deepseek-v4-pro"
```

默认 API 地址是 `https://api.deepseek.com`，可用 `DEEPSEEK_BASE_URL` 覆盖。API key
只由本地 Python 进程读取，不会进入浏览器、prompt artifact、trajectory 或评分文件。

## 命令行评测

快速运行两个代表任务。默认采用多轮自适应决策，并启用模型侧强化推理：

```powershell
python -m apps.task_lab.run_evaluation --max-steps 18
```

运行全部 15 个任务：

```powershell
python -m apps.task_lab.run_evaluation --all-tasks --mode adaptive --max-steps 24
```

指定任务或续跑已有目录：

```powershell
python -m apps.task_lab.run_evaluation --tasks reaction-to-assay partition-discovery
python -m apps.task_lab.run_evaluation --tasks partition-discovery --resume `
  --output-dir runs/task_lab/my_evaluation
```

两种运行模式的含义：

- `adaptive`（默认）：每一步都把最新公开实验报告、原始谱图曲线、公开峰表和合法动作发送给模型，
  执行“观测—谱图解读—假设—动作”的多轮循环；
- `plan`：一次生成完整操作计划，仅保留为低成本基线对照，不作为主交互模式。

`--thinking` 默认开启模型侧强化推理，`--reasoning-effort high|max` 控制推理强度，默认使用
`max`；`--no-thinking` 可关闭。无论是否开启，系统都不会保存或展示
模型的隐藏逐字思维链，而是要求模型返回可审计的结构化记录：公开证据、谱图解读、当前假设、
不确定性和动作依据。

## 谱图消融与实验设计审计

Agent 评测默认使用 `unassigned`：模型获得原始曲线和未指认峰中心/面积，但看不到
target、reactant 或 byproduct 标签。可用同一任务执行三档消融：

```powershell
python -m apps.task_lab.run_evaluation --tasks reaction-to-assay `
  --spectrum-disclosure raw --max-steps 18
python -m apps.task_lab.run_evaluation --tasks reaction-to-assay `
  --spectrum-disclosure unassigned --max-steps 18
python -m apps.task_lab.run_evaluation --tasks reaction-to-assay `
  --spectrum-disclosure assigned --max-steps 18
```

- `raw`：只提供降采样原始曲线，不提供峰表；
- `unassigned`：提供峰中心、面积和检出状态，但删除物种/峰组指认；
- `assigned`：提供已指认峰表，适合教学和上限对照，不作为严肃 Agent 默认档。

每个 campaign 结果还会写入 `experiment_design_audit`。审计直接从真实 action 序列复算每轮条件，
并把相对最近历史条件的变化分成 baseline、replication、controlled single factor 和
multi-factor change。多因素变化对 BO 是正常设计，但不能被 Agent 叙述为无混杂的单因素因果证据。

## 多轮实验与扩展预算

官方任务的预算和 episode 语义保持冻结。需要研究“上一轮学到的经验能否用于下一轮”时，使用
扩展研究档位：

```powershell
python -m apps.task_lab.run_evaluation --tasks reaction-to-assay `
  --mode adaptive --max-steps 36 --budget-multiplier 2 --campaign-override
```

- `--budget-multiplier` 可取 `1` 到 `4`，扩大环境总操作预算；
- `--campaign-override` 让原本的单实验任务在合法终检后重置实验状态，并保留公开的历史实验记忆；
- 每次终检会保存条件、仪器、谱图结论、终检指标和分数，供后续决策比较；
- 每次终检还会实时显示实际条件差异与实验设计分类；
- 剩余不足 6 步时不会开始一轮注定无法完成的反应配方。

只要启用预算放大或 campaign override，结果就标记为 `extended-research`：分数写入
`research_score`，`official_score` 保持 `null`，不会混入官方榜单。

## 经典主动学习

经典算法不需要 API key，适用于支持标准反应配方的任务：

```powershell
python -m apps.task_lab.run_evaluation --agent gp_bo `
  --tasks reaction-optimization-standard --max-steps 72
python -m apps.task_lab.run_evaluation --agent rf_ei `
  --tasks reaction-optimization-standard --max-steps 72
python -m apps.task_lab.run_evaluation --agent safe_gp_bo `
  --tasks reaction-safety-constrained --max-steps 72
```

| Agent | 代理模型 | 选点规则 |
| --- | --- | --- |
| `random_recipe` | 无 | 随机完整配方对照 |
| `latin_hypercube` | 无 | 空间填充初始设计 |
| `greedy_local` | 局部历史最优 | 邻域扰动 |
| `gp_pi` | Matérn Gaussian Process | Probability of Improvement |
| `gp_ucb` | Matérn Gaussian Process | Upper Confidence Bound |
| `gp_bo` | Matérn Gaussian Process | Expected Improvement |
| `rf_ei` | Random Forest ensemble | 基于树间方差的 Expected Improvement |
| `safe_gp_bo` | 分数 GP + 风险 GP | 采用公开任务安全上限的约束 Expected Improvement |

GP、RF 和安全约束代理先完成 4 个随机初始配方，从第 5 个配方起拟合代理模型；随机、LHS 与
局部搜索按各自规则直接选点。面板会实时显示训练配方数、
初始设计/采集阶段、采集函数值、历史最优值和下一配方。经典基线只学习配方到 final assay
的响应；谱图仍会展示用于审计，但不会被伪装成算法输入。

80 次多 seed 对照结果、V4 Pro 谱图审计和失败案例见
[`docs/discovery_benchmark.md`](../../docs/discovery_benchmark.md)。

## 材料名称

内部动作和轨迹继续使用稳定数字值，但界面会显示 Water、Ethanol、Acetonitrile、Toluene 以及
Catalyst A–D。语义事件也可直接提交 `"solvent": "ethanol"`。当前真实溶剂名称只代表材料身份；
任务中的速率影响仍是校准类别效应，匿名催化剂不能解释为现实催化剂。完整原则见
[`docs/material_identity.md`](../../docs/material_identity.md)。

## 结果文件

输出默认写入 `runs/task_lab/<timestamp>/`：

```text
evaluation_summary.json
reaction-to-assay/
  agent_plan.json
  trajectory.jsonl
  evaluation_result.json
equilibrium-characterization/
  ...
```

官方档位的 `official_score` 和扩展档位的 `research_score` 都只来自合法 final assay；
`total_score` 还会反映安全、成本、非法动作和
样本效率。没有完成 final assay 时，`official_score` 保持 `null`，不会用中间 reward 冒充
正式得分。每个 `evaluation_result.json` 都包含轨迹回放验证状态。

## 学生端反馈

Student Lab 不需要 API key。学生从当前合法操作中选择动作并填写参数，界面会即时更新：

- 动作验证和可执行参数范围；
- 已用预算、剩余预算和实验轮次；
- 公开指标、安全风险、成本和最佳得分；
- 数字反应器状态、学习曲线，以及 HPLC、GC、UV-Vis、IR、NMR 多通道谱图；
- 谱图坐标、公开峰指认和仪器摘要；
- 可下载的完整实验记录。

非法动作在执行前被拒绝，不消耗预算，也不改变环境状态。
