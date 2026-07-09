# Codex 5.5 Medium 行为报告

本文档描述 2026-07-09 本地评测中 `gpt-5.5`、medium reasoning 子代理在 ChemWorld 复杂任务上的实际行为。它是一份实测报告，不是 OpenAI 官方产品能力声明。

## 评测对象

子代理被要求作为 ChemWorld 探索型 planner 运行。它直接在本地仓库中使用 Python、Gymnasium 和 ChemWorld 包，并且只在下面目录写入临时产物：

```text
runs/codex55_medium_probe/
```

生成文件包括：

| 文件 | 含义 |
| --- | --- |
| `probe_trials.py` | 子代理写出的评测脚本 |
| `trial_results.json` | 每个 trial 的动作序列、观测和指标 |
| `trial_summary.csv` | 扁平化汇总表 |
| `best_by_task.json` | 每个任务的最佳单次 trial |

本轮共运行 78 个 trial：

| Task | Recipe families | Seeds |
| --- | ---: | ---: |
| `reaction-to-purification` | 5 | 0, 1, 2 |
| `purity-yield-tradeoff` | 5 | 0, 1, 2 |
| `reaction-to-distillation` | 4 | 0, 1, 2 |
| `reaction-to-crystallization` | 4 | 0, 1, 2 |
| `flow-reaction-optimization` | 4 | 0, 1, 2 |
| `electrochemical-conversion` | 4 | 0, 1, 2 |

运行时 `debug_truth=False`，所以 Gym observation 没有直接暴露 hidden state。可是子代理拥有本地仓库读取权限，能够阅读 task、operation、scoring 和源码。因此，这次结果应被理解为：

```text
developer-side recipe-planning probe
```

它不是严格黑盒 leaderboard submission。

## 它实际做了什么

这次子代理不是在做在线强化学习，也不是在做贝叶斯优化或 surrogate-model fitting。它表现出来的行为更接近一个会写代码的实验规划者：

1. 阅读已注册 task id 和允许的 operation language。
2. 为每个 task 设计一组有化工直觉的 recipe families。
3. 在多个 seed 上执行这些 recipe。
4. 记录 score、task metrics、cost、risk、precondition flags、constitution flags 和异常行为。
5. 对每个 task 选出最佳单次 trial。

脚本中确实包含 HPLC、UV-vis 等中间测量，但没有根据测量结果进行实时分支决策。也就是说，这些测量主要用于让流程更像真实实验，并检查 observation 字段；它们还不是一个真正的闭环自适应策略。

## 典型策略模式

### 反应前段

多数流程先执行：

```text
add_solvent -> add_reagent -> add_catalyst -> heat -> wait -> measure -> wait -> measure -> quench
```

子代理主要调节：

- reagent amount；
- catalyst id 和 catalyst amount；
- temperature；
- heating time；
- 是否加入 HPLC 或 UV-vis 中间测量。

这说明它能够把 task affordance 翻译成合理的实验操作，但这些操作是预先脚本化的，不是实时学习出来的。

### 萃取和纯化

在 purification 任务中，它尝试了 balanced、conservative、aggressive、heavy purification 和 minimal downstream 等路径。典型后处理为：

```text
add_phase -> add_extractant -> mix -> settle -> separate_phase -> wash -> dry -> concentrate -> transfer -> final_assay
```

观察到的环境响应：

- 更重的 downstream processing 会提高 purity。
- recovery 仍然偏低，因此总分被明显限制。
- 高 purity recipe 往往带来较高 process cost。

### 结晶

在 crystallization 任务中，它调节 seed mass、cooling temperature 和 cooling duration：

```text
seed_crystals -> cool_crystallize -> filter_crystals -> final_assay
```

观察到的环境响应：

- 更深的冷却和更强的 seeding 往往得到更高 crystallization score。
- 最佳 trial 同时具有较好的 crystal purity 和 crystal yield。
- 这个任务最能体现子代理的过程直觉。

### 蒸馏

在 distillation 任务中，它比较了 gentle、scripted、heavy 和 aggressive upstream reaction，再接：

```text
evaporate -> distill -> collect_fraction -> final_assay
```

观察到的环境响应：

- aggressive reaction 加中等 reflux 的路径最好。
- distillate recovery 较高，但 distillate purity 仍然有限。
- 高分路径通常成本较高，因此该任务能暴露 yield、purity、cost 的 trade-off。

### 连续流

在 flow 任务中，它调节 residence time、flow rate、temperature 和 catalyst loading：

```text
set_flow_rate -> run_flow -> final_assay
```

观察到的环境响应：

- long residence time 明显优于 fast/hot flow。
- 最佳 flow score 仍然偏低，说明当前 flow task 的优化信号可能还不够强，或者 recipe 空间仍未覆盖真正高分区域。

### 电化学

在 electrochemistry 任务中，它比较 scripted、gentle、aggressive 和 efficiency variants：

```text
set_potential -> electrolyze -> final_assay
```

其中一个 recipe 显式设置了欧姆降相关字段：

```text
electrolyte_conductivity_S_m
electrode_gap_m
electrode_area_m2
contact_resistance_ohm
```

观察到的环境响应：

- scripted electrochemical recipe 仍然最强。
- selectivity 和 energy efficiency 比较稳定。
- 环境能响应最近加入的 ohmic-drop model。

## 最佳单次结果

下面是每个 task 的最佳单次 trial。注意，这不是官方 leaderboard mean。

| Task | Best recipe | Seed | Score | 主要现象 |
| --- | --- | ---: | ---: | --- |
| `electrochemical-conversion` | `scripted_electro` | 2 | 0.5565 | 高 selectivity、高 energy efficiency、低 risk |
| `reaction-to-crystallization` | `crystallization_heavy` | 2 | 0.5493 | crystal purity 和 crystal yield 都较好 |
| `reaction-to-purification` | `purification_heavy` | 0 | 0.3657 | purity 高，但 recovery 偏低 |
| `purity-yield-tradeoff` | `purity_first` | 1 | 0.3515 | purity 不错，但 cost 高、recovery 有限 |
| `reaction-to-distillation` | `aggressive_reaction_distill` | 1 | 0.2605 | recovery 较好，但 distillate purity 偏低 |
| `flow-reaction-optimization` | `flow_long_residence` | 0 | 0.1637 | long residence 改善 conversion |

## 与官方 baseline 的关系

本轮子代理的最佳单次 trial 在所有复杂 task 上都超过了当前官方 baseline mean：

| Task | 当前最佳官方 baseline mean | Codex 5.5 medium best trial |
| --- | ---: | ---: |
| `electrochemical-conversion` | 0.5334 | 0.5565 |
| `reaction-to-crystallization` | 0.3360 | 0.5493 |
| `reaction-to-purification` | 0.2253 | 0.3657 |
| `purity-yield-tradeoff` | 0.2887 | 0.3515 |
| `reaction-to-distillation` | 0.0763 | 0.2605 |
| `flow-reaction-optimization` | 0.0561 | 0.1637 |

这不能直接解释为“Codex 5.5 medium 已经领先官方 baseline”。原因是：

- 官方 baseline 报告的是固定 agent 在多个 seed 上的均值。
- 子代理报告的是多个手工设计 recipe families 中的最佳单次 trial。
- 子代理可以读取源码和任务实现，因此不是严格 blind agent。

更准确的说法是：它证明当前环境已经能被一个强代码代理用化工直觉探索出比 naive baseline 更好的 recipe，但还没有构成正式黑盒 LLM leaderboard 结果。

## 它擅长什么

本轮观察到的优势：

- 能理解 task id、operation 名称和流程约束。
- 能把任务类型映射到合理的反应、分离、结晶、蒸馏、流动和电化学 recipe。
- 能生成多样的 recipe variants。
- 能主动检查 precondition、risk、cost 和 score。
- 能避免明显非法 action。
- 能输出可复查的本地产物。

## 它没有做什么

这次没有观察到：

- 严格 hidden-state-free 的竞赛式盲优化。
- 每一步根据 observation 实时改变下一步动作。
- surrogate model 训练。
- uncertainty-aware active learning。
- 严格统计意义上的 leaderboard evaluation。
- 可迁移的通用 task policy learning。

因此它更像一个强的 developer-side experimental planner，而不是一个封闭自治 benchmark agent。

## 暴露出的环境问题

本轮 78 个 trial 没有出现 invalid action、precondition failure 或 constitution failure。但它暴露了几个 benchmark 设计问题：

1. campaign task 中，final assay 返回 `leaderboard_score`、`experiment_ended=True`，但保持 `terminated=False`。该语义现在由 `campaign_model.md`、`info["experiment_summaries"]`、`info["last_terminal_summary"]` 和 `info["next_experiment_ready"]` 明确约束。
2. `info["cost"]` 是 safe-RL 风格的 constraint signal，而 observation 或 assay 中的 `cost` 是过程指标。两个 cost 的命名需要进一步区分。
3. purification、crystallization、flow 等复杂过程仍依赖 proxy-maturity modules，高分不能被解释成高保真物理模拟成功。
4. best-trial result 适合调试和 agent probing，但正式 leaderboard 应使用 mean-over-seeds、置信区间和固定评测预算。

## 如何复现

运行：

```powershell
.\.venv\Scripts\python.exe runs\codex55_medium_probe\probe_trials.py
```

主要输出：

```text
runs/codex55_medium_probe/trial_results.json
runs/codex55_medium_probe/trial_summary.csv
runs/codex55_medium_probe/best_by_task.json
```

## 建议使用的标签

在论文、报告和 leaderboard 注释里，建议标注为：

```text
Codex 5.5 medium developer-side recipe-planning probe
```

不建议标注为：

```text
black-box LLM leaderboard agent
```

前者准确说明了它是一个有仓库访问权限、能写代码、能运行实验的规划型 probe。后者会夸大这次评测的黑盒性和自治程度。
