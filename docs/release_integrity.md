# 结果与发布完整性

本页定义 ChemWorld 从安装包、轨迹到榜单的可信链。它是正式 benchmark 协议的一部分，
不是可选的运维建议。

## 信任链

```text
source commit
  -> non-editable wheel smoke
  -> versioned task/scenario/mechanism/scoring contracts
  -> trajectory JSONL
  -> replay verifier
  -> verified result + trajectory SHA-256
  -> metric recomputation
  -> leaderboard
  -> signed private-eval envelope / paper artifact
```

任一箭头无法验证时，产物不得用于正式排名或论文主结果。

## Wheel 资源合同

机制和场景 YAML 会被打包到 `chemworld/resources/configs`。源码 checkout 可以使用仓库根目录
`configs/`，非 editable 安装优先使用 wheel 内资源。`scripts/smoke_test_wheel.py` 会在临时目录
构建 wheel、安装到隔离 target，并从仓库外创建和 reset 环境，以防 editable install 掩盖资源遗漏。

## Evaluation Result 0.2

`chemworld-evaluation-result-0.2` 至少包含：

- 完整 `EvaluationResult` 指标；
- `verified=true` 与 replay report；
- `evaluation_threshold`；
- 绝对 `trajectory_path`；
- `trajectory_sha256`。

`chemworld evaluate` 只在 replay 通过后生成该产物。榜单再次检查 trajectory digest、执行 replay，
并用记录的 threshold 重算所有指标。这样既防止轨迹被替换，也防止只修改 result JSON 中的分数。

## Private Eval 签名

`chemworld-private-eval-signed-0.2` 使用 HMAC-SHA256 签署除 `signature` 外的完整 envelope，包括：

- schema version；
- generation time；
- ChemWorld version 与 commit；
- signing-secret hash；
- result count；
- verified results 和 run log。

验证时同时检查 schema、result count、secret hash 和 HMAC。签名密钥必须是维护者持有的高熵密钥，
不得使用可猜测口令，也不得提交到仓库。

## 学生代码威胁模型

仓库自带 local evaluator 是 `trusted-local-subprocess`：它有路径边界、环境白名单、响应超时和
公开信息清理，但没有操作系统级文件、网络或进程隔离。因此：

- 可用于 demo、课程中教师审阅过的 agent 和协议开发；
- 不得直接运行未知第三方代码；
- 正式第三方评测必须在无网络、只读挂载、低权限、有限 CPU/内存/PID 的容器中运行；
- `allowed_network=false` 是声明，不是安全控制。

## Release Gate

```bash
python -m pip install -e ".[dev,docs,physchem-ref]"
python scripts/run_release_gate.py
```

门禁覆盖 lint、typing、全量测试、文档、wheel smoke、外部参考后端、runtime boundary、
环境自洽审计和 baseline smoke。默认开发门禁允许一个结构完整但明确不能用于发布声明的 candidate
bundle，并在 summary 中记录 `release_claim_ready=false`。正式发布必须显式运行：

```bash
python scripts/run_release_gate.py --require-frozen-benchmark
```

严格 frozen 检查会重新核验公开 manifest、内嵌证据 SHA-256、当前 task contract hash、source
commit、clean tree、release status 和完整 trajectory archive。任何失败都阻止 release claim；
`validated=true` 或 readiness 计数本身不构成冻结证据。
