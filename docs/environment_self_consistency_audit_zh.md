# ChemWorld 环境自洽性审计

更新日期：2026-07-09

本文档描述 ChemWorld 当前环境自洽性检查方法。这里的“自洽”不是指所有物理模型都已经达到真实预测级别，而是指同一个虚拟世界内部的声明、机制、状态、动作、观测、谱图、评分、日志和回放彼此一致。

## 审计目标

ChemWorld 的正式交互入口是：

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=0)
```

环境自洽性审计要回答五个问题：

1. `TaskSpec -> Scenario -> Runtime -> Observation -> Scoring -> Verify` 是否全链路一致。
2. typed ledger 和 physical constitution 是否能在每一步后保持非负、守恒和可回放。
3. HPLC、GC、UV-vis、final assay 的 raw spectra、processed estimates 和 task metrics 是否语义对齐。
4. trajectory 中的 hash、maturity、kernel、state patch 和 world event 是否能被 replay verifier 重新计算。
5. agent 多轮交互时看到的反馈是否稳定、可解释、可复现。

## 当前检查工具

新增脚本：

```powershell
.\.venv\Scripts\python.exe scripts\audit_environment_consistency.py --tasks all --seeds 0 1 2
```

默认输出：

```text
runs/audit/environment_consistency_report.json
runs/audit/environment_consistency_report.csv
runs/audit/trajectories/*.jsonl
```

每条审计记录包含：

| 字段 | 含义 |
| --- | --- |
| `task_id` | 被检查的正式 benchmark task |
| `seed` | 随机种子 |
| `scenario_id` | task 绑定的 scenario |
| `task_contract_hash` | task contract hash |
| `mechanism_hash` | 编译后 mechanism 的 hash |
| `score_contract_hash` | task scoring contract hash |
| `profile_hash` | runtime profile hash |
| `observation_contract_hash` | observation contract hash |
| `maturity` | 当前 task 的最低物理成熟度 |
| `invalid_count` | precondition failure 数量 |
| `verify_status` | replay verifier 是否通过 |
| `spectra_metric_consistency` | raw spectra 与 processed metrics 的一致性状态 |
| `warnings` | 不阻断运行但需要关注的自洽性风险 |

脚本还会运行一个小型 agent-facing probe：在 `reaction-to-purification` 上使用固定 seeds 和多轮谱图反馈，记录 first score、best score、best-so-far AUC、invalid action 和谱图决策特征。

## 最新全量审计结果

运行命令：

```powershell
.\.venv\Scripts\python.exe scripts\audit_environment_consistency.py --tasks all --seeds 0 1 2 --output-dir runs\audit
```

本次覆盖 14 个正式 task，共 42 条 task/seed 审计记录。

| 指标 | 结果 |
| --- | ---: |
| `row_count` | 42 |
| `covered_task_count` | 14 |
| `hash_coverage_complete` | true |
| `verify_failures` | 0 |
| `spectra_failures` | 0 |
| `spectra_warnings` | 0 |
| `invalid_steps` | 0 |
| `constitution_failures` | 0 |

覆盖的正式任务：

- `electrochemical-conversion`
- `flow-reaction-optimization`
- `low-budget-characterization`
- `partition-discovery`
- `public-private-generalization`
- `purity-yield-tradeoff`
- `reaction-mechanism-explanation`
- `reaction-optimization-standard`
- `reaction-safety-constrained`
- `reaction-to-assay`
- `reaction-to-crystallization`
- `reaction-to-distillation`
- `reaction-to-purification`
- `tool-agent-planning`

每条记录均包含并通过非空检查：

- `task_contract_hash`
- `mechanism_hash`
- `score_contract_hash`
- `profile_hash`
- `observation_contract_hash`

agent-facing probe 结果：

| Seed | First score | Best score | Best round | Best-so-far AUC | Invalid count |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0.371 | 0.426 | 3 | 0.416 | 0 |
| 1 | 0.282 | 0.345 | 6 | 0.329 | 0 |
| 2 | 0.335 | 0.387 | 3 | 0.378 | 0 |

当前 warning：无。

本轮修复：`reaction-to-purification` 的 final assay raw HPLC 过去使用全局 reaction
species amounts 生成谱图，因此 processed purity 较高时仍可能出现 `reactant_public` 主导峰。
现在 downstream task 在存在 selected phase 时，会使用 selected product phase 的 public
species calibration 生成 HPLC/GC/UV-vis/final assay raw signals。这样 processed purity、
recovery 与 raw spectra 指向同一个被测样品。

## 自洽性维度

### 结构自洽

检查 task、scenario、world law、mechanism、runtime profile 是否互相指向同一套世界规则。

当前已具备：

- 所有正式 task 通过 `gym.make("ChemWorld", task_id=...)` 进入同一环境。
- `task_info()` 暴露 `world_law_id`、`scenario_id`、`mechanism_hash`、`runtime_profile_hash`、`scoring_contract_hash` 和 `observation_contract_hash`。
- replay verifier 会检查 mechanism、runtime profile、scoring contract 和 observation contract hash。

当前风险：

- `reaction-to-purification` 的 allowed operations 已收紧为反应 + downstream
  extraction / separation / purification 操作；审计脚本仍保留
  `task_policy_warning` 规则，以便后续任务切片再次误暴露 flow、电化学、结晶或蒸馏操作时能够立刻报警。

### 物理自洽

检查每一步 transition 后是否满足 physical constitution。

当前已具备：

- 非负 amount、volume、temperature、pressure、cost、risk、sample ledger。
- typed phase/vessel/equipment/process ledger。
- material conservation、phase mass balance、vessel bounds、equipment attachment。
- metadata 禁止保存 primary structured state。

审计标准：

- 每步 `constitution.check_state(state)` 必须通过。
- `constraint_flags["constitution_failed"]` 不应出现。
- 非法动作只应影响 process penalty，不应破坏 material ledger。

### 观测自洽

检查 agent 得到的 observation 是否与 instrument contract 一致。

当前已具备：

- observation 包含 `raw_signal`、`processed_estimate`、`uncertainty`、`observed_mask`。
- failed precondition 返回非信息性 observation。
- HPLC、GC、UV-vis、final assay 均有 plot-ready raw signal。

审计标准：

- raw spectra 中只能出现 public aggregate species label，例如 `target_public`、`reactant_public`、`impurity_public`。
- raw spectra 不得泄漏 hidden species name、rate constant、hidden theta。
- observed mask 中未观测字段不得被当作有效测量值。

### 谱图与指标自洽

检查 raw spectra 与 processed metrics 是否方向一致。

当前已具备：

- HPLC/GC peak table 包含 retention time、peak width、area、estimated concentration、assignment 和 group。
- UV-vis 包含 wavelength 和 absorbance。
- final assay 返回 HPLC、GC、UV-vis、IR、NMR 和 calibrated mass-balance packet。

当前状态：

- `reaction-to-purification` 的 final assay HPLC 已不再由全局未反应物主导。
- 审计脚本仍保留 `semantic_alignment_warning` 规则；如果后续新增任务或仪器再次出现
  high-purity / reactant-dominant 冲突，会继续报警。

后续建议：

- 明确 final assay processed purity 与 HPLC public peak table 的校准关系。
- 对 crystallization、distillation、flow、electrochemistry 的专属谱图继续增加方向性测试。

### 评测自洽

检查 online reward、final assay score、leaderboard score 和 replay verify 是否一致。

当前已具备：

- `leaderboard_score` 只在合法 final assay 后出现。
- `verify_records()` 会重放 action sequence 并比较 observation、reward、terminated/truncated、kernel metadata、state patch summary 和 constitution checks。
- tampered mechanism hash、contract hash、runtime metadata 和 state patch 会被测试覆盖。

审计标准：

- final assay 后 `info["leaderboard_score"]` 必须等于 scoring contract 对当前 observation 的重新计算结果。
- 审计脚本生成的每条 JSONL trajectory 必须通过 `verify_records()`。

### 文档自洽

检查中文文档、课程材料和项目叙事是否没有乱码、没有过度宣称、没有与 maturity metadata 冲突。

当前约束：

- proxy kernel 必须明确标记为 proxy。
- task maturity 必须进入 task info、trajectory、baseline report 和 docs。
- 中文文档必须 UTF-8 可读，不应出现常见 mojibake 标记，例如 U+951B、U+9359 或替换字符 U+FFFD。

## 验收命令

```powershell
.\.venv\Scripts\python.exe scripts\audit_environment_consistency.py --tasks all --seeds 0 1 2
.\.venv\Scripts\python.exe -m pytest tests\test_environment_self_consistency.py
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

## 当前判断

ChemWorld 当前已经具备较强的结构自洽和 replay 自洽基础。主要短板不在“能不能执行”，而在更高层的语义一致性：

- task slice 权限需要持续由测试锁住，避免后续新增操作时再次误导 agent；
- raw spectra 与 processed metrics 需要更明确的校准关系；
- 多轮 agent probe 应进入正式 benchmark protocol，而不只是临时实验；
- proxy/lite/reference-validated 的边界要继续在 docs、trajectory 和 leaderboard 中保持显式。

这套审计的目标不是让所有 warning 立刻消失，而是让 ChemWorld 的每个层次都能被重复检查、被记录、被解释。
