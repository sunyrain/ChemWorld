# Year 1-2 验收审计

更新日期：2026-07-08

本文用于回答一个具体问题：当前仓库是否已经完成“目前 Year 1-2 的内容，并全面完善文档和教程”。结论基于当前工作树、测试结果、CLI 行为、已保存 notebook 输出和文档站构建结果。

## 验收结论

当前 Year 1-2 范围已经闭环：

- Year 1 benchmark 底座可安装、可运行、可提交、可验证、可导出数据、可生成 paper artifact。
- Year 2 过程模块已经以同一个 `ChemWorld` 世界规律下的 task slice 形式接入，包括结晶、蒸馏、连续流和电化学。
- 教程体系已覆盖 Day 1-13 和 project leaderboard blueprint，所有 notebook 均保存执行输出且无错误输出。
- 文档站包含 world law、scenario、campaign、schema、instrument、safety/cost、dataset、local eval machine、tutorial curriculum、architecture 和 Year 1-2 completion 页面。
- 本机教师端/学生端评测机 demo 可执行，能生成 leaderboard。

这不等价于真实反应预测软件、远端托管 leaderboard、机器人实验平台或高保真单元操作模拟器。这些属于 Year 3+ 或正式 1.0 发布前工作。

## 要求与证据

| 要求 | 当前证据 | 状态 |
| --- | --- | --- |
| 单一正式 Gym 入口 | `gym.make("ChemWorld", task_id=...)` 在测试和 notebooks 中使用；`chemworld tasks list` 中所有 task 的 `env_id` 为 `ChemWorld`。 | 通过 |
| 统一世界规律 | `chemworld.world.world_law_spec()` 暴露 ontology、constitution、operations、instruments、transition modules、observation modules；所有 built-in task 共享 `world_law_id = chemworld-physical-chemistry`。 | 通过 |
| Year 1 reaction/separation benchmark | `reaction-optimization-standard`、`reaction-safety-constrained`、`reaction-to-assay`、`reaction-to-purification`、`partition-discovery`、`purity-yield-tradeoff` 等 task 已注册并有测试覆盖。 | 通过 |
| Year 2 过程模块 | `reaction-to-crystallization`、`reaction-to-distillation`、`flow-reaction-optimization`、`electrochemical-conversion` 已注册；对应 operation、instrument observation、metrics 和 scripted smoke path 已覆盖。 | 通过 |
| world 层接管底座 | `chemworld.world` 已接管 ontology、parameter generation、instrument registry、operation registry、recipe compiler、reaction ODE、thermal risk、phase partition、downstream truth、observation helper 和 scoring helper；测试禁止 `world` 反向导入 `core.batch_reactor`。 | 通过 |
| campaign/experiment/operation 日志 | trajectory JSONL 包含 `campaign_id`、`experiment_index`、`operation_id`、scenario 和 observation metadata；`verify --constitution` 可重放。 | 通过 |
| action/schema/validator | runtime schema 与静态 schema 一致；validator 覆盖 task policy、instrument policy、constitution preconditions 和 payload bounds；CLI 支持 `validate-action` 与 `validate-recipe`。 | 通过 |
| observation/instrument contract | HPLC、GC、UV-vis、final assay 有 observable keys、cost、noise、sample consumption、raw signal、processed estimate、uncertainty。 | 通过 |
| safety/cost channel | Gym `info` 暴露 `cost`、`cost_components`、`constraint_budget_remaining`，metrics 使用同一 safety/cost 信息。 | 通过 |
| dataset / submission / artifact | CLI 支持 dataset export、submission validation、baseline report、private-eval signing、paper artifact creation。 | 通过 |
| 本机评测机 | `local_eval_server/teacher_side/eval_machine.py` 可运行 demo，教师端持有环境，学生端只返回 action。 | 通过 |
| 教程完整性 | `notebooks/tutorials/` 包含 Day 1-13 和 `project_leaderboard_blueprint.ipynb`；已保存执行输出，无 error output，无旧 HTML checkpoint 组件。 | 通过 |
| 文档完整性 | `mkdocs build --strict` 通过；新增 `tutorial_curriculum_zh.md` 串联课程、评分和评测机流程。 | 通过 |

## 已执行的验收命令

质量门禁：

```bash
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy src\chemworld
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

结果：

- `ruff`: all checks passed。
- `mypy`: no issues in `src\chemworld`。
- `pytest`: 70 passed。
- `mkdocs build --strict`: documentation built successfully。

代表性 CLI 链路：

```bash
.\.venv\Scripts\python.exe -m chemworld.cli tasks list
.\.venv\Scripts\python.exe -m chemworld.cli scenarios list
.\.venv\Scripts\python.exe -m chemworld.cli run --task reaction-to-assay --agent scripted_chemistry --output runs\audit\reaction_to_assay.jsonl
.\.venv\Scripts\python.exe -m chemworld.cli verify --constitution --submission runs\audit\reaction_to_assay.jsonl
.\.venv\Scripts\python.exe -m chemworld.cli evaluate --submission runs\audit\reaction_to_assay.jsonl --output runs\audit\reaction_to_assay.results.json
.\.venv\Scripts\python.exe -m chemworld.cli datasets export --submission runs\audit\reaction_to_assay.jsonl --format jsonl --output runs\audit\reaction_to_assay.dataset.jsonl
.\.venv\Scripts\python.exe -m chemworld.cli render --task reaction-to-assay --actions runs\audit\render_action.json
.\.venv\Scripts\python.exe -m chemworld.cli baselines report --tasks reaction-to-assay reaction-to-crystallization --agents random scripted_chemistry --seeds 0 --output-dir runs\audit\baseline_report
.\.venv\Scripts\python.exe -m chemworld.cli artifact create --output-dir runs\audit\paper_artifact --tasks reaction-to-assay reaction-to-crystallization --agents random scripted_chemistry --seeds 0
.\.venv\Scripts\python.exe -m chemworld.cli private-eval verify --artifact runs\audit\private_eval_signature.json --salt audit-local-secret
```

代表性结果：

- `run`: 生成 11 步 trajectory 和 manifest。
- `verify --constitution`: `verified=true`、`constitution_passed=true`、`max_abs_error=0.0`。
- `datasets export`: 生成 11 条 JSONL dataset records。
- `render`: 输出 ANSI 环境摘要。
- `baselines report`: 生成 task-specific report 和 leaderboard rows。
- `artifact create`: 生成 paper artifact summary、task cards、schema snapshot、baseline report 和 dataset example。
- `private-eval verify`: `signature_valid=true`。

本机评测机：

```bash
.\.venv\Scripts\python.exe local_eval_server\teacher_side\eval_machine.py --workspace runs\audit\local_eval_machine demo --tasks reaction-to-assay --seeds 0
```

结果：生成 `team_alpha_scripted` leaderboard，`result_count=1`。

Notebook 审计：

- Day 1-13：所有 code cell 均有 execution count。
- Project leaderboard blueprint：所有 code cell 均有 execution count。
- 所有教程 notebook：error output 数量为 0。
- 未发现 `display_student_checkpoint` 或 `student-checkpoint` 残留。

## 当前边界

以下项目不属于“目前 Year 1-2 完成”的验收阻塞项，但需要在后续阶段继续推进：

- 用完整 task/agent/seed 矩阵冻结正式 reference baseline table。
- 将本机 hidden-salt private eval 升级为远端 maintainer-side registry。
- 将 crystallization、distillation、continuous-flow、electrochemistry 的过程 proxy 提升为更高保真 world kernel。
- 增加真实数据校准、专家机制评分或外部化学工具链。
- 用 Docker 或等价沙箱替换本机评测机中的模拟隔离。
