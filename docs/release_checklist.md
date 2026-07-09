# 发布检查表

本检查表用于判断 ChemWorld 文档站、包和 benchmark contract 是否可以发布。

## 代码 Gate

```bash
python -m ruff check .
python -m mypy src/chemworld
python -m pytest
```

任何 release candidate 都应记录命令输出、Python 版本、依赖版本和 commit。

## 环境自洽性 Gate

```bash
python scripts/audit_environment_consistency.py --tasks all --seeds 0 1 2
```

必须确认：

- 注册任务均可 reset/step；
- smoke trajectory 不触发未知异常；
- replay 结果稳定；
- spectra 与 instrument contract 一致；
- constitution check 无失败。

## 文档 Gate

```bash
python -m mkdocs build --strict
```

首页应指向当前架构、任务注册表、评测协议、baseline、release artifact 和 maturity
说明。发布到 `gh-pages` 前，`site/` 目录必须来自同一 commit 的构建结果。

## Benchmark 合同

- `task_id`、`world_law_id`、maturity 和 metrics 已冻结。
- 任务卡与 registry 一致。
- action schema 和 observation schema 可被 agent 作者理解。
- 无效操作、约束 flags、termination/truncation 规则清楚。
- 三项 pre-release core task 的 golden trajectory fixture 通过测试，并且任何 fixture 更新都经过人工 diff 审查。
- 三项 pre-release core task 的 scoring contract audit 通过，且能拒绝篡改后的公开 score、错误 scoring hash、以及非 final assay 暴露的 leaderboard score。
- Replay verifier 能拒绝篡改后的 mechanism hash、task/profile/scoring/observation hash、reward、observation、transaction status、world events 和 state patch summary。

## Baseline 产物

- 至少一个简单 baseline。
- 至少一个可解释强 baseline 或 recipe。
- score table、trajectory bundle、manifest 和失败分析齐全。

## 隐藏评测

隐藏评测 split 不应泄露 hidden scenario 或 oracle state。提交包不得读取测试集答案。

## 数据与伦理

公开数据应说明生成方式、成熟度、限制和安全边界。不要把虚拟环境输出包装成真实实验
结论。

## 论文产物

论文 artifact 应包含 README、环境说明、任务卡、baseline 结果、轨迹、图表和 manifest。
