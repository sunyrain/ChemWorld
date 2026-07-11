# 结果可信链

ChemWorld 的可信链从源代码、合同和轨迹延伸到统计结果。软件门禁、科学证据和发布授权是三个
不同层级；通过前者不会自动获得后者。

## 信任链

```text
source commit + clean tracked tree
  -> isolated wheel smoke
  -> versioned task/scenario/mechanism/evaluation contracts
  -> trajectory JSONL
  -> schema + constitution + deterministic replay
  -> verified result + trajectory SHA-256 + score/replay binding
  -> task-level paired statistics
  -> signed private aggregate / public release artifact
```

任何一环失败，结果都不能进入正式排名。

## Evaluation Result 0.3

`chemworld-evaluation-result-0.3` 至少包含：

- 完整任务和评测指标；
- `verified=true` 与 replay report；
- `evaluation_threshold`；
- `trajectory_path` 与 `trajectory_sha256`；
- `score_replay` 绑定，包括指标版本、源记录数和 layered evaluation；
- 任务风险语义、完整实验数和资源账本。

验证器重新计算轨迹摘要、回放状态、指标和 score binding。修改轨迹、result JSON、threshold、合同
或评测字段都会失败。运行包中的绝对路径不作为唯一身份；可搬移审计器通过包内相对结构重新绑定
轨迹，再比较 SHA-256。

## 资源完整性

每种方法都必须声明并记录适用资源：完整实验、操作、测量、墙钟、CPU/GPU、训练步数、模型请求、
输入/输出 token 和费用。LLM 的失败请求、重试和结构修复计入调用；RL 的训练步数和 checkpoint
必须与无学习评测分开。

## Private Eval

私有评测使用维护者持有的高熵 secret 生成 salted worlds，并签署只包含允许公开字段的聚合 envelope。
验证同时检查 schema、result count、secret hash 和 HMAC。secret、salt 原值、隐藏 seeds、逐条私有
轨迹和可逆参数不得进入仓库或网页。

## 第三方代码

本地评测机采用 `trusted-local-subprocess`，具备路径边界、环境白名单和超时，但不提供操作系统级
隔离。它只适合可信代码、课程和协议开发。未知第三方提交必须在无网络、只读挂载、低权限且限制
CPU、内存、PID 和时间的容器或沙箱中运行。

## 本地质量门禁

```bash
python -m pip install -e ".[dev,docs,physchem-ref]"
python scripts/run_release_gate.py
```

门禁覆盖 lint、typing、测试、文档、wheel 资源、runtime integration、回放和参考切片。它证明
当前 checkout 的工程完整性，不证明方法有效性或 benchmark 已发布。

严格冻结发布还需核验 source commit、clean tree、task contract、完整 trajectory archive、统计摘要、
私有签名和独立复现。候选 bundle 或历史换行兼容只能证明文件没有损坏，不能提升科学状态。
