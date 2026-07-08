# ChemWorld-Bench 技术架构文档

更新日期：2026-07-08

## 1. 平台定位

ChemWorld-Bench 是一个面向 AI4Science、化工教育和闭环实验决策研究的虚拟物理化学 benchmark。它不是一组彼此独立的小游戏，也不声称预测真实反应体系；它的正式定位是：

> 在同一个共享物理化学世界规律下，提供多个可复现、可评测、可提交的实验任务切片，用于研究 agent、人类学习者、贝叶斯优化器和混合系统如何在有限预算下进行实验设计、观测、建模、优化和解释。

正式 Gymnasium 入口统一为：

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-optimization-standard", seed=0)
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(action)
```

## 2. 当前核心架构

当前代码主干位于 `src/chemworld/`：

```text
chemworld
├── foundation          # ontology、constitution、state、ledger、units、world law
├── world               # 专业 world-law 层：ontology、scenario、instrument、operation、recipe、kernel、scoring
├── core                # 事件调度层：调用 world kernel，维护 state ledger 和 operation record
├── envs                # ChemWorld Gymnasium 环境
├── tasks               # task registry 和 task card
├── schemas             # action、recipe、trajectory、manifest、task、scenario schema
├── agents              # random、LHS、greedy、BO、safe BO、scripted、LLM stub
├── eval                # runner、metrics、leaderboard、verify、suite
├── data                # logging、submission、dataset export、validation、anonymize
├── wrappers            # action mask、safety/cost、NaN observation wrappers
└── cli                 # run/evaluate/verify/tasks/scenarios/datasets/render
```

## 3. WorldLaw：统一物理化学世界

`WorldLawSpec` 是所有 task 的共同底座。它记录：

- ontology registry；
- physical constitution；
- operation registry；
- instrument registry；
- transition kernel registry；
- observation kernel registry；
- module versions；
- backend spec；
- scenario generators；
- constitution rules。

当前所有内置 task 共享：

```text
world_law_id = chemworld-physical-chemistry
```

这保证新增 task 不会变成独立小游戏，而是同一个物理化学世界下的不同 scenario/task slice。

## 4. Scenario：隐藏世界实例

Scenario 是 hidden parameter 和 initial state 的正式契约。每个 scenario 声明：

- `scenario_id`；
- `world_law_id`；
- `family`；
- `split`；
- `difficulty`；
- `hidden_parameter_seed`；
- `initial_state_seed`；
- `initial_state_id`；
- `parameter_profile`；
- `allowed_module_tags`；
- `expected_qualitative_behavior`。

CLI 支持：

```bash
chemworld scenarios list
chemworld scenarios show reaction-to-purification
```

public/private split 共享机制族，但不共享具体 hidden parameters。

## 5. Task：世界切片而不是独立环境

Task 只定义评测切片：

- 使用哪个 scenario；
- 允许哪些 operations；
- 允许哪些 instruments；
- 预算是多少；
- 是 single experiment 还是 campaign；
- 目标函数和成功指标是什么；
- safety limit 是多少。

当前任务包括：

- `reaction-optimization-standard`
- `reaction-safety-constrained`
- `reaction-mechanism-explanation`
- `reaction-to-assay`
- `reaction-to-purification`
- `reaction-to-crystallization`
- `reaction-to-distillation`
- `flow-reaction-optimization`
- `electrochemical-conversion`
- `partition-discovery`
- `purity-yield-tradeoff`
- `public-private-generalization`
- `low-budget-characterization`
- `tool-agent-planning`

## 6. Campaign / Experiment / Operation

当前日志模型已经正式区分三层：

```text
Campaign
  └── Experiment
        └── Operation
```

每条 trajectory JSONL 记录包含：

- `campaign_id`
- `experiment_index`
- `operation_id`
- `scenario_id`
- `initial_state_id`

在 campaign task 中，`final_assay` 结束当前 experiment，但不结束整个 campaign；在 single-experiment task 中，`final_assay` 终止 episode。

## 7. Action Schema 与 Recipe Compiler

动作语言统一为：

```json
{
  "operation": "add_solvent",
  "volume_L": 0.02,
  "solvent": 1
}
```

高层 recipe 可以编译为 operation sequence：

```json
{
  "steps": [
    {"operation": "add_solvent", "volume_L": 0.02, "solvent": 1},
    {"operation": "add_reagent", "amount_mol": 0.01}
  ]
}
```

验证分三层：

1. schema validation；
2. task policy；
3. constitution preconditions。

CLI 支持：

```bash
chemworld validate-action --task reaction-to-purification --action action.json
chemworld validate-recipe --task reaction-to-purification --recipe recipe.json
```

## 8. Instrument Contract

每个 instrument 都有正式 contract：

- observable keys；
- raw signal schema；
- processed estimate schema；
- uncertainty model；
- noise model；
- cost；
- latency；
- sample consumption；
- destructive flag；
- requires terminated；
- calibration profile。

当前 instruments：

- `uvvis`
- `gc`
- `hplc`
- `final_assay`

默认 observation 不泄露 hidden species amounts、rate constants 或 partition coefficients。`final_assay` 是 leaderboard score 的正式来源。

## 9. Safety / Cost Channel

ChemWorld 保持 Gymnasium 五元组不变，同时在 `info` 中提供安全成本：

```python
info["cost"]
info["cost_components"]
info["constraint_budget_remaining"]
```

cost components 包括：

- safety risk；
- high cost；
- precondition failure；
- constitution failure。

安全任务使用 task-level `safety_limit`，不再依赖硬编码全局阈值。

## 10. Dataset Layer

数据导出命令：

```bash
chemworld datasets export --submission runs/example.jsonl --format jsonl
chemworld datasets export --submission runs/example.jsonl --format parquet
chemworld datasets card --dataset datasets/chemworld_dataset.jsonl
```

JSONL 始终可用；Parquet 需要本地安装 `pyarrow` 或 `fastparquet`。

Dataset card 包含：

- dataset id；
- task ids；
- world law versions；
- env versions；
- commit hash；
- seeds；
- agent manifests；
- license；
- privacy/anonymization status；
- known limitations。

## 11. 当前实现状态

已完成：

- 单一正式 Gym 环境 `ChemWorld`；
- 共享 `WorldLawSpec`；
- scenario registry；
- task registry；
- campaign/experiment/operation 日志字段；
- action/recipe schema；
- instrument contracts；
- safety/cost channel；
- dataset export/card；
- render ansi；
- task-aware wrappers；
- BO 默认 `n_initial=4`；
- reaction + separation 任务族；
- crystallization、distillation、continuous-flow、electrochemistry Year 2 过程模块基础版；
- `chemworld baselines report` 官方基线报告生成器；
- `chemworld private-eval sign` 本机私有评测签名 artifact；
- `chemworld artifact create` release artifact 目录生成器；
- 本地教师端/学生端评测框架；
- 12 天中文 notebook 教程。

仍需继续推进：

- 继续把 crystallization、continuous-flow、electrochemistry 的过程 proxy 拆成更独立的 world kernel，并把 distillation 从当前 VLE shortcut slice 推进到 Underwood/Gilliland 与 MESH 级严格塔模型；
- 继续把 HPLC/GC/IR/NMR 从合成信号推进到带公开校准案例的 instrument kernels；UV-vis 已有 Beer-Lambert 校准切片；
- 用完整 task/agent/seed 矩阵重新运行并冻结官方 reference baseline table；
- 将本机 signed private-eval artifact 升级为远端 maintainer-side registry；
- 增加 Minari 风格 dataset metadata；
- 继续提高 crystallization、distillation、continuous flow、electrochemistry 的物理保真度与 baseline 标定。

## 12. 验收命令

```bash
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy src\chemworld
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m mkdocs build --strict
```
