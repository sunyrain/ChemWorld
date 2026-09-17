# ChemWorld Experiment 1

状态：**当前权威导航入口；不是新的科学规范，也不授权 Participant。**

本目录给 Experiment 1 提供单一导航入口。现有冻结文件继续保留在原路径，因为 EC v1.0.1 机器合同同时绑定文件路径和 SHA-256。本次导航清理不移动、不复制成第二份权威，也不改变科学语义。

## 从这里开始

1. 阅读 [`AUTHORITY.md`](AUTHORITY.md)，确认不同问题应以哪一类文件为准；
2. 当前 development qualification 的科学执行语义见 [`EXPERIMENT_1_MINIMUM_EXECUTION_SPEC_V1_0_1.md`](../EXPERIMENT_1_MINIMUM_EXECUTION_SPEC_V1_0_1.md)；
3. EC 本轮问题、单位和停止规则见 [`EXPERIMENT_1_EC_QUALIFICATION_V1_0_1_NOTE.md`](../EXPERIMENT_1_EC_QUALIFICATION_V1_0_1_NOTE.md)；
4. 精确机器输入见 [`experiment_1_ec_qualification_v1.0.1.json`](../../../configs/benchmark/experiment_1_ec_qualification_v1.0.1.json)；
5. 已完成结果见 [`experiment-1-ec-qualification-v1.0.1-20260917.md`](../reports/experiment-1-ec-qualification-v1.0.1-20260917.md)；
6. 科学设计背景稿见 [`guidance/README.md`](guidance/README.md)，但不得据此直接开跑；
7. 旧 Work II 资产与当前依赖边界见 [`LEGACY_INDEX.md`](LEGACY_INDEX.md)。

## 当前状态

- `EC-W00` canary 已通过；
- `EC-W01..W05 × entity/parametric/structural` 的 15/15 原子单元均已完成；
- 11/15 `qualified`，4/15 `failed`；
- `EC-P` 为 5/5 `five_world_qualified`；
- `EC-E` 和 `EC-S` 各为 3/5，失败集中在 W01/W04；
- 0 Participant/provider calls；
- EC 整体、Participant development 和正式 benchmark execution 均未获授权。

“执行完成”不等于“Gate 全部通过”。通过单元不能抵消失败单元。

## 当前执行链

```text
minimum execution spec（科学执行语义）
        ↓
EC qualification note（本轮问题与停止规则）
        ↓
machine contract（路径、hash、World、预算、阈值）
        ↓
runner / evaluator / exact replay
        ↓
machine registry + human-readable report
```

服务器上的 development evidence 根目录为：

```text
runs/development/experiment-1-ec-v1.0.1-941110e/
```

`runs/` 是未纳入 Git 的 development evidence；可读报告和代码保存在仓库中。不要用缺少本地 `runs/` 目录解释为服务器证据丢失。

## 当前下一道门

Authority/navigation cleanup 已于 2026-09-17 获得人工接受。下一项科学工作是审阅 [`systems/EC/QUALIFICATION_REPAIR_NOTE_V1_0_2.md`](systems/EC/QUALIFICATION_REPAIR_NOTE_V1_0_2.md) 中针对以下四个失败原子单元提出的 repair design：

- `EC-W01:entity`；
- `EC-W04:entity`；
- `EC-W01:structural`；
- `EC-W04:structural`。

该 repair note 当前仍是 candidate，不授权执行。在 repair note 和新 manifest 冻结前，不得重跑受影响 block；在 EC 三个 locus 全部 five-world qualified 前，不得启动 EC Participant。
