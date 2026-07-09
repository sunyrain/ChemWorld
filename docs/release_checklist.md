# 发布检查表

本页定义 ChemWorld-Bench 公开预发布前必须满足的检查项。它不是长期专业物理模型路线图；P3 的专业深化可以继续排队，但不阻塞当前 benchmark 预发布。

当前发布目标是：外部研究者能够安装包、读取任务合同、运行 `ChemWorld` 环境、提交 agent、复现实验轨迹、理解成熟度边界，并引用当前预发布 artifact。

## 发布判定

| 项目 | 要求 | 状态说明 |
| --- | --- | --- |
| 代码门禁 | lint、type check、tests、docs、环境审计全部通过 | 必须通过 |
| Benchmark 合同 | task、scenario、world law、scoring、trajectory、submission contract 已冻结 | 必须通过 |
| 公开边界 | public observation 不泄露 hidden mechanism、hidden seed、rate constants 或 oracle state | 必须通过 |
| 数据产物 | 至少包含 baseline report、示例 submission、trajectory、dataset card 和 paper artifact skeleton | 必须通过 |
| 文档站 | 首页、任务、agent 接口、评测协议、发布限制、notebook 示例均可访问 | 必须通过 |
| 私有评测 | private-eval 只发布规则和维护者流程，不公开 hidden salt / hidden seeds | 必须通过 |
| 已知限制 | proxy/lite/reference_validated/professional-candidate 边界明确 | 必须通过 |

## 本地 Release Gate

正式 release candidate 使用一个入口命令：

```powershell
.\.venv\Scripts\python.exe scripts\run_release_gate.py
```

该命令会顺序运行：

1. `python -m ruff check .`
2. `python -m mypy src/chemworld`
3. `python -m pytest`
4. `python -m mkdocs build --strict`
5. `python scripts/audit_environment_consistency.py --tasks all --seeds 0 1 2`
6. `python -m chemworld.cli baselines report --tasks reaction-to-assay --agents scripted_chemistry --seeds 0`

输出摘要写入 `runs/release_gate/release_gate_summary.json`。每个 release candidate 必须记录：

- Git commit hash；
- Python 版本；
- 依赖锁定文件或 dependency manifest；
- gate 命令和运行日期；
- 是否使用 `CHEMWORLD_PRIVATE_EVAL_SALT`；
- 任何跳过项及原因。

## 环境自洽性 Gate

```powershell
.\.venv\Scripts\python.exe scripts\audit_environment_consistency.py --tasks all --seeds 0 1 2
```

必须确认：

- 所有正式 task 可以 reset/step；
- task、scenario、mechanism、profile、scoring 和 observation hash 可追踪；
- action mask、validator、allowed operations 和 allowed instruments 一致；
- typed ledgers 满足物料非负、phase totals、vessel/equipment 引用闭合；
- public observation、tool JSON、lab report 和 trajectory 不泄露 hidden truth；
- HPLC、GC、UV-vis、final assay 的 raw signal、processed estimate 和 score 语义一致；
- replay verifier 能重放脚本生成的 trajectory；
- 篡改 reward、observation、hash、transaction status、world events 或 state patch summary 会被拒绝。

## 文档 Gate

```powershell
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

站点发布前必须检查：

- 首页说明正式入口是 `gym.make("ChemWorld", task_id=...)`；
- 左侧导航围绕预发布 benchmark 组织，而不是历史开发日志；
- 中英文切换只使用 Material 右上角语言切换；
- `tasks.md`、`task_cards.md`、`benchmark_protocol.md`、`agent_interface.md`、`submission.md`、`dataset_layer.md`、`paper_artifact.md` 和本页互相一致；
- `docs/en/index.md` 作为英文入口存在，但当前中文站点是主发布入口；
- `notebooks/tutorials/` 和 `notebooks/end_to_end/` 的用途区分清楚；
- 中文 Markdown 和 notebook 无明显乱码字符；乱码扫描器的命中列表必须为空。

部署站点使用：

```powershell
.\.venv\Scripts\python.exe -m mkdocs gh-deploy --force
```

`site/` 目录只作为本地构建产物，不应手工编辑。

## Benchmark 合同

预发布核心任务：

| Task | 用途 | 发布要求 |
| --- | --- | --- |
| `reaction-to-assay` | 从投料到 final assay 的完整单实验闭环 | golden trajectory、scoring audit、端到端 notebook |
| `reaction-to-purification` | 反应、相系统、后处理、纯化和最终检测 | golden trajectory、spectra-metric audit、端到端 notebook |
| `partition-discovery` | campaign 多轮实验下学习分配规律 | campaign semantics、agent-facing probe、端到端 notebook |

冻结项：

- `task_id`；
- `world_law_id`；
- task maturity；
- allowed operations；
- allowed instruments；
- budget 和 termination policy；
- success metrics；
- scoring contract hash；
- trajectory schema；
- submission bundle schema。

如果修改以上任一项，必须更新：

- task card；
- benchmark protocol；
- golden trajectory fixture；
- scoring contract audit；
- baseline report；
- paper artifact；
- release checklist。

## Baseline 和 Agent 产物

发布包至少包含：

- `random` 或等价随机 baseline；
- `scripted_chemistry` 可解释 baseline；
- 一个 BO 或 safe-BO 类传统优化 baseline；
- `ToolUsingLLMStubAgent` 或 `LLMReplayAgent` 的可复现 trace；
- baseline summary table；
- invalid-action rate、precondition failure、final assay count、best-so-far AUC；
- 每个核心 task 的 trajectory 示例；
- 失败分析或限制说明。

LLM 相关结果必须声明：

- 模型名或 replay/stub 类型；
- prompt/template 版本；
- temperature 或 deterministic policy；
- 调用日期；
- 是否使用缓存；
- 是否访问外部网络或工具；
- 是否读取 hidden/private 信息。

## Submission Bundle

一个有效提交包至少包含：

```text
submission/
├── manifest.json
├── trajectories/
│   └── *.jsonl
├── results/
│   └── *.json
└── explanations/        # optional
    └── *.json
```

验证命令：

```powershell
chemworld submission validate path\to\submission
chemworld submission summarize path\to\submission
chemworld verify --constitution --submission path\to\submission\trajectories\run.jsonl
```

提交包不得：

- 读取 hidden scenario、private salt 或 oracle state；
- 修改 ChemWorld 源码；
- 写入评测目录以外的位置；
- 访问未授权网络资源；
- 根据文件名、seed 表或本地缓存作弊；
- 在 manifest 中省略依赖、命令或 agent 描述。

## Paper Artifact

生成入口：

```powershell
chemworld artifact create `
  --output-dir artifact/paper_artifact `
  --tasks reaction-to-assay reaction-to-purification partition-discovery `
  --agents scripted_chemistry `
  --seeds 0
```

正式 artifact 应包含：

- `README.md`；
- environment card；
- task cards；
- world law snapshot；
- schemas；
- baseline report；
- example trajectories；
- dataset examples；
- release manifest；
- replay manifest；
- release checklist；
- limitations；
- reproduction script。

`paper_artifact.md` 定义完整目录结构。本页只定义是否可发布。

## Private-Eval 政策

当前 private-eval 是维护者控制的隐藏评测流程，不是公开可反推的本地测试集。

规则：

- public-dev 用于教学、调试和开发；
- public-test 用于公开 baseline 和外部复现；
- private-eval 使用相同 `world_law_id` 和 mechanism family，但 hidden parameters、hidden seeds 和 salt 不公开；
- 没有 `CHEMWORLD_PRIVATE_EVAL_SALT` 时，private-eval 只能作为 placeholder，不得报告为正式隐藏榜单结果；
- private-eval 结果必须由维护者在干净环境中运行，并记录 commit、dependency manifest、date 和 evaluator manifest；
- 任何 private-eval 输出只发布 aggregate score、rank、confidence interval 和 violation summary，不发布 hidden task internals。

## 已知限制

发布时必须明确说明：

- ChemWorld 当前是 virtual chemical world model gym，不是真实反应预测器；
- 当前物理模块存在 proxy/lite/reference_validated/professional-candidate 混合成熟度；
- 当前不连接真实机器人、真实实验仪器、DFT 或分子动力学后端；
- private-eval 仍是维护者运行的本机隐藏评测流程，尚不是云端防作弊系统；
- LLM baseline 以 deterministic stub / replay 为主，不代表在线 SOTA LLM 的充分能力；
- P3 专业物理化学深化仍在路线图中，未完成项不应被宣传为正式 professional backend。

## Citation 和复用说明

预发布引用建议：

```bibtex
@misc{chemworldbench2026,
  title = {ChemWorld-Bench: A Virtual Chemical World Model Gym for Closed-Loop Experimental Decision Making},
  author = {ChemWorld-Bench Contributors},
  year = {2026},
  note = {Pre-release benchmark artifact},
  url = {https://github.com/sunyrain/ChemWorld}
}
```

复现实验时应报告：

- ChemWorld commit；
- task id；
- world law id；
- task maturity；
- scenario split；
- seed suite；
- scoring contract hash；
- agent manifest；
- dependency manifest；
- release gate summary。

## 停止发布条件

出现以下任一情况，不应发布 release candidate：

- release gate 失败；
- environment self-consistency audit 有 failure；
- public observation 泄露 hidden truth；
- replay verifier 不能重放官方示例 trajectory；
- baseline report 无法生成；
- task card 与 task registry 不一致；
- notebook 或 docs 出现明显乱码；
- private-eval salt、hidden seeds 或 hidden parameters 被提交到公开仓库；
- P3 未完成模块被描述为 fully professional model；
- site build 不是来自当前 main commit。
