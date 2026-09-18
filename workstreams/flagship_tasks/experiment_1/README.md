# ChemWorld Experiment 1

状态：**当前权威导航入口；不是新的科学规范，也不授权 Participant。**

本目录给 Experiment 1 提供单一导航入口。现有冻结文件继续保留在原路径，因为 EC v1.0.1 机器合同同时绑定文件路径和 SHA-256。本次导航清理不移动、不复制成第二份权威，也不改变科学语义。

当前合作者综合审阅请首先阅读
[`COLLABORATOR_REVIEW_SNAPSHOT_2026_09_18.md`](COLLABORATOR_REVIEW_SNAPSHOT_2026_09_18.md)。
该文件只是集成快照，不替代下列分层权威文件，也不授权正式执行。

## 从这里开始

1. 阅读 [`AUTHORITY.md`](AUTHORITY.md)，确认不同问题应以哪一类文件为准；
2. convergence repair、重跑和停止规则见
   [`EXPERIMENT_1_BENCHMARK_CONVERGENCE_CHARTER_V1_0.md`](EXPERIMENT_1_BENCHMARK_CONVERGENCE_CHARTER_V1_0.md)，
   confirmation/challenge 隔离见
   [`EXPERIMENT_1_CONFIRMATION_PROTOCOL_V1_0.md`](EXPERIMENT_1_CONFIRMATION_PROTOCOL_V1_0.md)；
3. qualification 的共同科学执行语义见
   [`EXPERIMENT_1_MINIMUM_EXECUTION_SPEC_V1_0_1.md`](../EXPERIMENT_1_MINIMUM_EXECUTION_SPEC_V1_0_1.md)；
4. 当前 105-unit 机器总账见
   [`EXPERIMENT_1_CONVERGENCE_REGISTRY.json`](results/EXPERIMENT_1_CONVERGENCE_REGISTRY.json)；
5. 本轮完整可读结论见
   [`EXPERIMENT_1_BENCHMARK_CONVERGENCE_REPORT.md`](results/EXPERIMENT_1_BENCHMARK_CONVERGENCE_REPORT.md)，
   当前 challenge decision 见
   [`EXPERIMENT_1_CHALLENGE_AUDIT_V1_2.md`](results/EXPERIMENT_1_CHALLENGE_AUDIT_V1_2.md)，
   confirmation preflight 见
   [`EXPERIMENT_1_CONFIRMATION_PREFLIGHT_V1_0.json`](results/EXPERIMENT_1_CONFIRMATION_PREFLIGHT_V1_0.json)；
6. Participant release 边界见
   [`EXPERIMENT_1_PARTICIPANT_RELEASE_MANIFEST.md`](results/EXPERIMENT_1_PARTICIPANT_RELEASE_MANIFEST.md)；
7. 各体系冻结 note、机器合同与结果位于 `systems/<SYSTEM>/`、
   `configs/benchmark/experiment_1_*` 和 `results/<SYSTEM>/`；
8. 科学设计背景稿见 [`guidance/README.md`](guidance/README.md)，但不得据此直接开跑；
9. 旧 Work II 资产与当前依赖边界见 [`LEGACY_INDEX.md`](LEGACY_INDEX.md)。

## 当前状态

连续 campaign 已覆盖 `7 systems × 5 Worlds × 3 prior loci = 105` 个原子单元：

| System | Qualified-development | Failed-development | Readiness-blocked |
| --- | ---: | ---: | ---: |
| EC | 15 | 0 | 0 |
| RX | 13 | 2 | 0 |
| PA | 15 | 0 | 0 |
| FL | 0 | 15 | 0 |
| C | 10 | 5 | 0 |
| P | 0 | 0 | 15 |
| D | 0 | 0 | 15 |

总计 `53 qualified-development / 22 failed-development / 30 readiness-blocked`。
challenge v1.2 已在 10 个 five-World candidate loci 中确认 7 个可进入 process-isolated
confirmation：`EC-E / EC-P / EC-S / RX-P / PA-E / C-E / C-P`；`RX-S / PA-P / PA-S`
继续 fail-closed。confirmation 公共合同和 preflight 已冻结，覆盖 `7 × 5 = 35` 个原子单元，
但状态仍为 `ready-but-not-executed`，因此 `qualified-confirmed = 0`、Participant-ready 单元为 0。
当前 campaign 使用 0 Participant/provider calls。

P/D 的 failure 表示五个 distinct private Worlds、prior generator 或目标 private-physics
family 尚未冻结，不表示公开任务环境不可运行。其 smoke 的任务合同、轨迹校验、hash 覆盖和
public-leakage audit 均通过。

“执行完成”不等于“Gate 全部通过”。通过单元不能抵消失败单元。

## 当前执行链

```text
minimum execution spec（共同科学执行语义）
        ↓
system note + machine contract（体系级冻结）
        ↓
provider-free runner / evaluator / exact replay 或 fail-closed readiness audit
        ↓
15-row system registry
        ↓
105-row global registry + campaign report
```

服务器上的 raw development evidence 保留在 `runs/development/experiment-1-*`。`runs/` 不纳入
Git；Git 中保存冻结合同、runner/evaluator、system registry、summary 与全局 registry。不要用
本地缺少 `runs/` 解释为服务器证据丢失。

## 当前下一道门

当前 development convergence 与 challenge v1.2 已完成并保留失败地图。release 轨的下一道门是
在明确授权后，对 7 个 challenge-eligible loci 运行一次 process-isolated confirmation；不是直接跑
Participant。expansion 轨的下一步则是分别审阅并授权 C-S 的 252 次、P 的 80 次 provider-free
calibration，不能把尚未执行的 calibration 写成 qualification PASS。

所有 development PASS 仍只是 candidate；confirmation 尚未执行，当前 release manifest 明确
withheld，本入口和集成审阅分支都不提供自动授权。
