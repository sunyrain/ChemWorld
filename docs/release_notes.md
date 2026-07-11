# 发布说明

## World Law v0.4 backend candidate

本次更新提升到 `chemworld-physical-chemistry-v0.4` 与 `chemworld-task-contract-0.6`。它是后端
候选版本，不是新的冻结 leaderboard release。

- 八个 adapter proposal 已按原始 hash-bound provider contract 集成；
- `dry`、`concentrate`、`transfer` 不再走 `chemworld_separation_proxy`；
- `mix`/`wash` 使用唯一 stability-aware LLE route；
- `distill` 使用唯一 duty-limited route；
- 诊断 provider 与 runtime maturity 隔离；
- spent sorbent、condensate、vent、source heel 和 line hold-up 进入 typed phase ledger；
- 15 个任务均为 `lite`、`proxy_allowed=false`，但 v0.4 的经验状态保持 `candidate`；
- 新 candidate bundle 与历史 `chemworld-serious-v1` 分目录保存，旧证据不被改写。

`scripts/audit_vnext_runtime_integration.py` 验证七类集成条件并实际执行 purification 与
distillation 事务。`scripts/build_vnext_backend_candidate.py` 生成带 SHA-256 的 task、scenario、
World Law、runtime route、readiness、integration 与 golden 摘要。

## ChemWorld-Bench 0.2.0 / serious v1

历史 v1 使用 World Law v0.3 与 task contract 0.5。其证据包只适用于对应合同。当前严格 frozen
checker 会拒绝把该旧包作为 v0.4 发布证据；candidate 模式只能验证其结构，不能授权新版本声明。
