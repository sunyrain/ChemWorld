# Experiment 1 P qualification readiness specification v1.0.1

状态：**FROZEN FOR FAIL-CLOSED DEVELOPMENT AUDIT**

Participant：**未授权**

Formal benchmark：**未授权**

## 1. Scope

本版本审计 `P-W01..W05 × entity/parametric/structural` 在当前仓库状态下是否已经具备
进入正式 qualification denominator 的前置条件。它不补写 private physics，不把普通 seed
冒充五个 World，也不把环境 smoke test 冒充先验可辨识性证据。

每个 seed 运行一次 `reaction-to-purification` 公开任务 smoke test，用于验证任务合同、机制与
评分 hash、轨迹校验、公开泄漏和基本工作流可执行性。由于下述前置资产尚未冻结，15 个 atomic
unit 均应 fail closed；smoke run 只证明环境可执行，不会把任一 unit 判为 qualified。

## 2. Frozen blockers

### P-E

- 当前 partition dossier 只审计并绑定 `partition-discovery`；
- 尚无 `reaction-to-purification` 专属 extractant dossier、固定 misindex permutation 和
  两个 feed-composition anchors；
- 因此 prior symmetry 与可辨识性不能声明通过。

### P-P

- 尚无标准 upstream composition 下的 `S* = K_product / K_impurity` truth oracle；
- aligned/misspecified 等宽 band generator 和 low/high phase-ratio holdout 尚未冻结；
- 因此 prior symmetry、预算内反证和 noise robustness 不能声明通过。

### P-S

- 当前 runtime 有 activity-corrected extraction，但没有注册为同一公开合同下可切换的
  constant-K private family；
- prompt 中描述两种 family 不能替代 executable private-physics fork；
- 因此结构层不得运行伪对照实验，直接保留 prerequisite failure。

## 3. Five-World rule

Seeds `0..4` 的 purification partition multipliers 当前均为 nominal `1.0`。本审计只把它们用作
五个环境 smoke seeds，不把它们认证为五套不同 private truth。`P-W01..W05` 的正式 World
manifest 必须在修复阶段另行冻结，并由底层参数/定律推导 observable behavior。

## 4. Gate interpretation

- Q1：失败；五个 distinct executable private Worlds 尚未冻结；
- Q2：由 smoke test 判断公开任务是否可执行；
- Q3：由 hash coverage、轨迹校验和 public-leakage audit 判断；
- Q4：失败；目标 prior generator/family 尚未冻结；
- Q5–Q8：失败；不得在缺少 Q1/Q4 前提时由推测代替实验资格证据。

Provider calls 固定为 0。该结果是当前状态的正式 development audit，可在后续 repair 版本中被
新证据取代，但不得删除或回写为 PASS。
