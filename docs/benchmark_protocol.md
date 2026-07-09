# Benchmark 协议

本协议定义 ChemWorld 任务如何划分、提交、评分和发布。

## 数据划分

- `train`：公开任务和公开 scenario，用于开发 agent；
- `validation`：公开但固定的检查集，用于调参和报告；
- `private_eval`：隐藏 scenario 或隐藏任务切片，用于 leaderboard。

所有 split 共享同一个 `world_law_id`，但隐藏参数和评测 seed 不应泄露。

## AAAI Preset Protocol

AAAI preset 是面向投稿实验的冻结协议：

- 任务集合由 `AAAI_TASK_IDS` 给出；
- baseline agent 集合由 `AAAI_BASELINE_AGENTS` 给出；
- 自动报告入口是 `chemworld baselines report --preset aaai`；
- artifact 入口是 `chemworld artifact create --preset aaai`；
- 快速烟测入口是 `python scripts/run_aaai_experiments.py --smoke`。

AAAI 结果必须按任务分别报告，不使用单一总分覆盖所有任务。每条结果至少记录：

- task id；
- seed；
- scenario id；
- mechanism hash；
- scoring contract hash；
- observation contract hash；
- runtime profile hash；
- maturity label；
- agent manifest；
- solver/provenance manifest。

`equilibrium-characterization` 是 AAAI 任务集中新增的平衡表征任务。它只暴露 pH-meter、UV-vis 和 final assay 等 public observation，不泄露 hidden pKa、Ksp 或 hidden species amounts。

## Seed Suite

正式报告必须声明使用哪一组 seed：

```bash
chemworld seeds show
```

规则：

- `public-dev` seeds 可用于教学、调试和 smoke test；
- `public-test` seeds 公开且冻结，用于 baseline 表和外部复现实验；
- `private-eval` hidden seeds 和 salt 由维护者控制；
- 显式 `--seeds` 是 smoke/debug override，不能冒充完整官方结果。

## 提交要求

提交包应包含 agent 入口、依赖、配置和 manifest。评测端负责创建环境、运行 episode、保存 trajectory 并计算分数。

提交包不得：

- 读取 hidden scenario；
- 根据文件名或 seed 表作弊；
- 写入评测目录以外的位置；
- 访问未授权网络资源；
- 修改环境代码。

## 指标

指标应按任务声明，常见维度包括：

- yield；
- purity；
- selectivity；
- information gain；
- mechanism accuracy；
- safety penalty；
- cost penalty；
- invalid-action penalty；
- sample efficiency。

总分可以是加权组合，但每个子指标都应单独报告，便于诊断。

## Replay Verifier

`chemworld.eval.verify_records(records)` 是提交轨迹进入评测前的 replay gate。它会用：

```text
task_id + seed + scenario/mechanism/task/profile/scoring hash + action sequence
```

重新创建环境并逐步执行 action，然后比较 reward、public observation、terminated/truncated、contract hashes、kernel metadata、affected ledgers、world events、state patch summary 和 transaction status。
