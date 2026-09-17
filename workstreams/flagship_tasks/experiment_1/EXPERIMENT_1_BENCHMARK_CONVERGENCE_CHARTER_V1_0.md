# Experiment 1 Benchmark Convergence Charter v1.0

状态：**FROZEN FOR PROVIDER-FREE BENCHMARK DEVELOPMENT**  
基线：Git commit `a5b11d2e0a5cc6971f19799fbe9513c582c2eded`（2026-09-18）  
Participant/provider execution：**禁止**

## 1. 目标与优先级

本 campaign 的目标不是把 105 个原子单元机械地调成 PASS，而是让每个单元获得科学诚实、
可审计的当前状态，并只把科学合理、可辨识、预算内可反证、有任务后果、抗噪声且不送分的
单元交给 Participant。

优先级固定为：

```text
科学合理性 > 可辨识性 > 任务相关性 > challenge quality
> 可复现性 > qualification coverage > PASS 数量
```

本轮只允许 provider-free authoring、development qualification、confirmation qualification
和 release-manifest authoring。不得运行 Participant Agent，不得调用外部 LLM/provider，不得按
结果降低 Q1–Q8 或下游评分阈值。

## 2. 状态与历史保留

当前状态集合为：

- `qualified-development`：冻结 development denominator 通过；尚未通过 confirmation；
- `qualified-confirmed`：同版本的五个 Worlds 在隔离 confirmation 中全部通过；
- `failed`：冻结科学设计执行完成但至少一个必要 Gate 失败；
- `development`：正在 authoring，尚无完整冻结 denominator；
- `readiness-blocked`：缺少 executable prerequisite，不能称为科学失败；
- `N/A`：有明确科学理由证明该 locus 不适用；
- `superseded`：旧版本因 truth/prior/runtime 变化失效，但历史证据永久保留。

旧 registry、旧 truth/prior hash、旧失败和 `runs/development/` evidence 不得覆盖。当前
baseline 的内容寻址记录见 `results/EXPERIMENT_1_BASELINE_A5B11D2.json`。

## 3. Failure hierarchy 与执行顺序

1. 局部 prior/discriminator repair：`PA-P`、`C-P`、`RX-E`；
2. locus-level structural redesign：`RX-S`、`C-S`；
3. system-level contract redesign：`FL-E/P/S`；
4. 首次正式 build：`P-E/P/S`、`D-E/P/S`；
5. 全局 diversity、prior-symmetry 和 challenge audit；
6. 隔离 confirmation；
7. Participant release manifest（不启动 Participant）。

局部 repair 优先修改 prior/discriminator 和公开诊断设计，不修改 simulator physics。结构或
runtime 问题不得逐 World 调参直到变绿。

## 4. 失效与重跑规则

| 改变对象 | 最小失效范围 |
| --- | --- |
| 一个 World 的 private truth | 该 World 的 entity/parametric/structural 三个 locus |
| 一个 locus 的 prior/discriminator | 该体系该 locus 的全部 W01–W05 |
| 一个 system 的 public/runtime contract | 该体系 5 Worlds × 3 loci |
| shared runtime/instrument/noise semantics | 所有实际受影响体系和 locus |

被失效的旧 PASS 必须成为 `superseded`，不能 carry forward。平台缺陷修复后，受影响冻结 block
从 unit 0 重跑；平台恢复不计科学 redesign iteration。

## 5. Redesign discipline

一个 `system × locus` 最多允许两次 scientific redesign iteration。Baseline 为 Round 0。
一次 iteration 必须先冻结新版本、问题、覆盖、测量、Gate、预算与 stop rule，再完成整个受影响
denominator。每轮在 repair ledger 中记录 diagnosis、changed object、scientific reason、affected
units、rerun scope 和 result。

两轮后仍系统性失败时，保留 `failed`/`development`；只有真正科学不适用时才可使用 `N/A`。
更换核心科学问题必须显式升级设计版本，不得伪装成 patch。

P/D 的 readiness audit 不计 redesign iteration；其第一次完整 executable contract 计 Round 1。

## 6. Authoring、development 与 confirmation 隔离

- Authoring/calibration 可以比较候选，但不得使用最终 confirmation 坐标和噪声；
- Development qualification 可以暴露结果并触发下一版本 redesign；
- 一个 block 宣布冻结后不得再修改；confirmation 使用未参与 redesign 的坐标、新 keyed noise、
  独立 replay 和相同的 Q1–Q8；
- Confirmation one-shot 失败后，该 confirmation set 退休。若返回开发，消耗一次 redesign
  iteration，下一次必须使用新的隐藏 set；
- 五个 Worlds 全部 confirmation PASS 后，locus 才能称为 `five-world participant-ready`。

具体隔离、commitment 与 challenge 规则见
`EXPERIMENT_1_CONFIRMATION_PROTOCOL_V1_0.md`。

## 7. Challenge quality

候选 participant-ready locus 必须同时满足：

- 默认 recipe 和单次最常见实验不能稳定直接揭示 A/M；
- false prior 位于冻结的 plausible envelope；
- A/M schema、字段、数值精度、语气、置信度和近似长度匹配；
- 至少需要一次有信息价值的实验选择；
- 最小可靠反证成本高于 trivial lower bound，且不超过 Participant budget；
- 错误 prior 在至少一个预注册策略区产生正的 behavioral regret/consequence。

Challenge audit 失败不能通过降低 qualification 难度修复。

## 8. 停止条件与最终输出

Campaign 完成条件是 105/105 均有可审计当前状态，不是 105/105 PASS。最终必须生成：

1. 支持 development/confirmation/supersession 的 105-unit registry；
2. `EXPERIMENT_1_BENCHMARK_CONVERGENCE_REPORT.md`；
3. `EXPERIMENT_1_PARTICIPANT_RELEASE_MANIFEST.md`。

Release manifest 只能列出 `qualified-confirmed` 单元，并必须以
`Participant execution was not started.` 结尾。
