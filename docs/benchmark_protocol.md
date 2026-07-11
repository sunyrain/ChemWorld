# Benchmark 协议

本协议定义 ChemWorld 任务的划分、运行、评分、验证和发布规则。任务必须保持逐任务报告，
不能用一个总分掩盖不同物理域、成熟度或失败模式。

## 套件

- `core`：三个紧凑任务，用于 API、回放和发布链路回归；
- `serious`：六个已通过结构合同与回放门禁、但仍在经验有效性审查中的候选研究任务；
- 显式 `--tasks`：用户自选任务，不自动获得正式套件声明。

```bash
chemworld baselines report --preset core
chemworld baselines report --preset serious
chemworld tasks readiness
```

正式套件的准入和冻结规则见[严肃任务设计](task_design.md)与
[Benchmark v1](benchmark_release.md)。

## 数据划分

- `public-dev`：接口调试、教学和 smoke；
- `public-test`：冻结任务与 seeds，用于可复现比较；
- `private-eval`：维护者控制的隐藏参数与 seeds，用于泛化评测。

所有 split 共享同一版本化世界律。私有参数、salt、隐藏物种量和机理参数不得进入公开
observation、trajectory 或 agent trace。

## 评测单位

`single_experiment` 任务以一条完整实验流程为单位；`campaign` 任务以固定总预算内的多条
experiment 为单位。报告至少包含：

- final-assay 分数与 best-so-far AUC；
- primary/secondary task metrics；
- invalid action、precondition、safety 与 cost；
- instrument 使用和 sample efficiency；
- task/scenario/mechanism/runtime/scoring/observation hashes；
- maturity、agent manifest 和 solver provenance。

## Baseline 与统计

正式比较必须使用相同 task-seed 对。当前 v0.4 先导功效分析把 0.05 total-score 差异定义为
最小实际重要差异（SESOI），据此暂定每任务 20 个配对 seeds；冻结前仍须用扩展 pilot 复核。
报告逐任务配对效应、paired bootstrap 置信区间、符号翻转检验、标准差和逐 seed 结果，不发布
掩盖领域差异的跨任务总分。smoke override 只能验证管线，不能用于性能声明。

随机配方探针的最大值只能称为 sampled recipe ceiling，不能称为 oracle，也不能直接用于 regret。
诊断阶段可报告“逐 seed 观测到的 best-known reference”，但未来方法允许超过它；正式 regret
必须绑定独立、可更新且逐 seed 的 reference 协议。

正式 evidence gate 还要求所有 baseline 无非法动作、每个 campaign 完成多轮实验、GP 进入
acquisition、成功阈值非饱和，并且 total score 与 primary metric 都能区分策略。
对以主动探索为主张的任务，还必须证明增加实验机会后至少一种可信自适应策略在部分任务上产生
达到 SESOI 的稳定收益；仅仅“进入 acquisition 阶段”不构成有效性证据。

## Verified Result Chain

```text
trajectory JSONL
  -> schema validation
  -> deterministic replay
  -> metric recomputation
  -> trajectory SHA-256 binding
  -> verified result JSON
  -> per-task leaderboard
```

`chemworld evaluate` 默认执行 replay。leaderboard 会校验 digest 并从轨迹重算指标；直接修改
result JSON、合同 hash、reward 或 observation 会被拒绝。

## 反作弊规则

提交不得读取 hidden scenario、`env.unwrapped._state`、私有 salt、隐藏 seed 表或 oracle state；
不得修改环境代码、写出评测目录或访问未授权网络。LLM trace 只保存 reasoning summary 和
decision evidence，不保存或要求完整 chain-of-thought。

提交格式和命令见[提交与验证](submission.md)，结果证据链见[结果完整性](release_integrity.md)。
