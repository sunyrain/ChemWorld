# Benchmark 协议

本协议定义 ChemWorld 任务的划分、运行、评分、验证和发布规则。任务必须保持逐任务报告，
不能用一个总分掩盖不同物理域、成熟度或失败模式。

## 套件

- `core`：三个紧凑任务，用于 API、回放和发布链路回归；
- `serious`：六个无 proxy 的严肃任务候选，用于开始难度校准和研究评测；
- 显式 `--tasks`：用户自选任务，不自动获得正式套件声明。

```bash
chemworld baselines report --preset core
chemworld baselines report --preset serious
chemworld tasks readiness
```

严肃候选的准入和提升规则见[严肃任务设计](task_design.md)。

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

每个严肃任务至少运行 random、可解释 scripted baseline、优化 baseline 和安全感知 baseline。
正式比较使用任务冻结 seeds，报告逐任务均值、标准误或 bootstrap confidence interval。smoke
override 只能验证管线，不能用于性能声明。

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
