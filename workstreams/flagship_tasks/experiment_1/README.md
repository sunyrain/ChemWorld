# ChemWorld Experiment 1

状态：**当前权威导航入口；不是新的科学规范，也不授权 Participant。**

本目录给 Experiment 1 提供单一导航入口。现有冻结文件继续保留在原路径，因为 EC v1.0.1 机器合同同时绑定文件路径和 SHA-256。本次导航清理不移动、不复制成第二份权威，也不改变科学语义。

## 从这里开始

1. 阅读 [`AUTHORITY.md`](AUTHORITY.md)，确认不同问题应以哪一类文件为准；
2. qualification 的共同科学执行语义见
   [`EXPERIMENT_1_MINIMUM_EXECUTION_SPEC_V1_0_1.md`](../EXPERIMENT_1_MINIMUM_EXECUTION_SPEC_V1_0_1.md)；
3. 当前 105-unit 机器总账见
   [`EXPERIMENT_1_QUALIFICATION_REGISTRY.json`](results/EXPERIMENT_1_QUALIFICATION_REGISTRY.json)；
4. 七体系可读汇总见
   [`EXPERIMENT_1_QUALIFICATION_CAMPAIGN_REPORT.md`](results/EXPERIMENT_1_QUALIFICATION_CAMPAIGN_REPORT.md)；
5. Participant 候选范围与 repair 优先级见
   [`EXPERIMENT_1_PARTICIPANT_READINESS.md`](results/EXPERIMENT_1_PARTICIPANT_READINESS.md)；
6. 各体系冻结 note、机器合同与结果位于 `systems/<SYSTEM>/`、
   `configs/benchmark/experiment_1_*` 和 `results/<SYSTEM>/`；
7. 科学设计背景稿见 [`guidance/README.md`](guidance/README.md)，但不得据此直接开跑；
8. 旧 Work II 资产与当前依赖边界见 [`LEGACY_INDEX.md`](LEGACY_INDEX.md)。

## 当前状态

连续 campaign 已覆盖 `7 systems × 5 Worlds × 3 prior loci = 105` 个原子单元：

| System | Qualified | Failed | 结果性质 |
| --- | ---: | ---: | --- |
| EC | 15 | 0 | 完整 qualification |
| RX | 8 | 7 | 完整 qualification |
| PA | 11 | 4 | 完整 qualification |
| FL | 0 | 15 | 完整 qualification |
| C | 7 | 8 | 完整 qualification |
| P | 0 | 15 | fail-closed readiness audit；5/5 smoke 通过 |
| D | 0 | 15 | fail-closed readiness audit；5/5 smoke 通过 |

总计 `41 qualified / 64 failed / 0 pending / 0 N/A`。EC 是唯一 15/15
通过的完整体系；当前 seven-system campaign 使用 0 Participant/provider calls。

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

当前阶段从“建立失败地图”切换到“分块 repair”。任何 repair 都必须：保留旧失败、使用新版本
note/config/evidence namespace、在重跑前冻结，并只重跑受影响 block。不得降低 Q1–Q8 阈值或
用 Participant 表现反向选择 World。

虽然 EC 15/15 已通过，它仍只是 Participant-ready candidate；正式 Participant 或 benchmark
execution 需要独立 release/participant manifest，本入口不提供自动授权。
