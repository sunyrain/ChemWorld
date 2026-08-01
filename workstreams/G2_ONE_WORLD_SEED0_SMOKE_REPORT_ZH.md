# G2 单世界单 seed 试运行报告

> 状态：development-only；不是正式 benchmark 结果，也不支持模型优劣或总体能力结论。
>
> 运行单元：`reaction-to-assay / public-dev / world_seed=0 / agent_seed=0`
>
> Agent：现有 direct operation-level `LiveLLMAgent`
>
> Provider：WellAU `gpt-5.6-sol`, reasoning effort `high`

## 1. 一句话结论

这次现有 G2 v1 在一个严重但可恢复的接口失败之后，**无 repair、无自动 terminate、
无自动 final assay 地完成了 1/1 个实验闭环**：前 8 步均因模型输出缺少
`action.operation` 而失败，第 9 步起连续 9 个动作全部合法，并在第 16、17 步自行
`terminate → final_assay`。

因此结果不是简单的“G2 能/不能做实验”，而是三个同时成立的结论：

1. 当前 ChemWorld 的严格逐操作闭环对该模型是可达的；
2. 现阶段最大损耗首先来自 Agent/provider 动作合同，而不是化学操作本身；
3. Agent 在获得 HPLC 结果后确实改变了后续动作，但其物料投入更大；终点成本又受到
   前 8 次接口失败的验证惩罚污染，尚不能解释成纯粹的化学资源策略。

## 2. 冻结配置

| 项目 | 冻结值 |
|---|---:|
| task | `reaction-to-assay` |
| world | `ChemWorld:public-dev:public:seed-0` |
| world seed / Agent seed | `0 / 0` |
| episode mode | `single_experiment` |
| operation limit | 18 |
| complete-experiment limit | 1 |
| provider attempts limit | 36（每个逻辑决策最多 2 attempts） |
| input/output token limit | 216,000 / 72,000 |
| wall-time limit | 3,600 s |
| automatic action repair | false |
| automatic terminate | false |
| automatic final assay | false |
| invalid actions retained | true |
| full current-experiment ledger in prompt | false（现有 v1 的已知缺口） |

环境的 deterministic scripted positive control 在同一 world/seed、同核心物理和评分
合同下可用 11 步完成实验，且当前代码 replay/constitution audit 均通过。因此，本次
结果不是环境不可达造成的。它与 G2 的 `contract_profile` 和来源 commit 不同，故只作为
可执行正控，不是完全同运行合同的基线。

## 3. 主结果

| 指标 | 结果 |
|---|---:|
| 完整实验 | 1/1 |
| 总 operation | 17/18 |
| 合法、已执行 operation | 9 |
| 非法/失败 operation | 8 |
| 总体动作合同通过率 | 9/17 = 52.9% |
| 第 9 步之后动作合同通过率 | 9/9 = 100% |
| terminate / final assay | step 16 / step 17 |
| final leaderboard score | 0.265839 |
| 注册任务阈值 | 0.55（注册表：`src/chemworld/tasks.py`） |
| replay | 17/17，`max_abs_error=0` |
| `--constitution` audit | fail：step 1–8 的 `action_schema_valid` 前置条件失败 |
| 物理状态 constitution checks | 17/17 steps 全部通过 |

最准确的状态描述是：

- **生命周期完成：是；**
- **轨迹可精确 replay：是；**
- **全轨迹动作合同/constitution audit clean：否；**
- **物理状态 constitution checks：通过；**
- **达到注册标量阈值：否。**

## 4. 逐阶段轨迹

| 阶段 | 步骤 | 实际行为 | 判读 |
|---|---:|---|---|
| 动作合同失败 | 1–8 | 8 次 `model_failure` | provider 返回可解析 JSON，但缺少 `action.operation`；无物料、温度或反应进程变化，但每步写入 `delta_cost=0.01`、`delta_risk=0.08` 的 validation penalty |
| 合同恢复 | 9 | `add_catalyst(1, 1 mmol)` | 首个合格动作；没有 harness repair |
| 投料 | 10–11 | `add_solvent(0, 40 mL)`；`add_reagent(20 mmol)` | 连续合法 |
| 反应 | 12 | `heat(340 K, 1800 s, 600 rpm)` | 安全，但 cost/low-selectivity flag 激活 |
| 取样 | 13 | `sample(1 mL)` | 决策文本已明确提到保留 closeout budget |
| 表征 | 14 | `measure(hplc)` | 得到 conversion 0.9735、yield 0.4579、selectivity 0.4843、byproduct 0.2670 |
| 反馈后动作 | 15 | `quench` | Agent 明确引用上述观测并据此停止反应；`adaptation_source=spectrum` |
| 自主收尾 | 16–17 | `terminate → measure(final_assay)` | 没有脚手架代替收尾；余 1 个 operation slot |

这里有两类不同的适应：

- step 1–8 到 step 9 是**动作合同恢复**。当前日志没有保留被拒绝的原始结构化 payload，
  因而不能判断它是稳定学习、随机波动，还是某种 provider 输出格式切换。
- step 14 到 step 15 是可审计的**观测条件化**：Agent 的下一步理由直接使用 HPLC 返回
  的 yield/selectivity/byproduct 数值，并选择 quench。

## 5. 科学结果与 G0 positive control

下表中的 G0 是仓库已有 deterministic scripted positive control，不是优化基线，也不能
用于模型优劣结论；它的作用只是给出同一 world/seed、同核心物理和评分合同的可执行
参照。两条轨迹的 `contract_profile` 和来源 commit 不同。

| 终点指标 | G2 本次 | G0 positive control | G2 相对变化 |
|---|---:|---:|---:|
| yield | 0.4547 | 0.3942 | +15.3% |
| selectivity | 0.4565 | 0.4043 | +12.9% |
| conversion | 0.9663 | 1.0000 | -3.4% |
| byproduct signal | 0.2593 | 0.3758 | -31.0% |
| safety risk | 0.0890 | 0.1056 | -15.7% |
| normalized cost | 1.0000 | 0.5721 | +74.8% |
| leaderboard score | 0.2658 | 0.2860 | -7.0% |

这条轨迹提供了一个很有价值、但目前只能称为 case observation 的现象：

> G2 得到了更高 yield/selectivity、更低 byproduct/risk，却伴随更高材料投入和饱和的
> 终点成本，最终得到更低 scalar score。

这正适合作为后续研究“化学结果、资源策略与标量优化目标如何解耦”的候选现象；单个
world/seed 还不能把它上升为统计结论。尤其是终点 cost 同时混入了 8 次接口验证惩罚，
不能用本条轨迹把 score 差异单独归因于 Agent 的化学资源选择。

## 6. 资源审计

### 6.1 物理资源

| 资源 | G2 本次 | G0 positive control |
|---|---:|---:|
| solvent | 40 mL | 28 mL |
| reagent | 20 mmol | 10 mmol |
| catalyst | 1.00 mmol | 0.25 mmol |
| explicit sample | 1 mL | 0 |
| HPLC | 1 | 1 |
| UV-Vis | 0 | 1 |
| final assay | 1 | 1 |
| total operation slots | 17 | 11 |
| valid chemistry/lifecycle operations | 9 | 11 |

这个结果直接证明：**仅用 operation 次数不能等价控制实验资源。** G2 和 G0 都只进行
一次 reagent/catalyst addition，但实际 mol 数分别相差 2 倍和 4 倍；反过来，G2 使用
更少的仪器表征。这里的物料数量比较不依赖终点 normalized cost；后者还受到接口失败
惩罚影响。后续正式资源合同至少必须把以下账本分开：

- 原料/溶剂/催化剂用量或离散份数；
- 仪器调用次数与样品消耗；
- 加热时间/温度、搅拌时间等过程资源；
- operation slots；
- 模型调用、token、延迟和货币成本。

### 6.2 模型与计算资源

| 指标 | 结果 |
|---|---:|
| logical decisions | 17 |
| provider attempts | 18 |
| provider attempts succeeded / failed | 17 / 1 |
| input tokens | 91,582 |
| output tokens | 7,802 |
| total reported tokens | 99,384 |
| decision wall time | 1,245.9 s |
| total run wall time | 1,247.7 s |
| billed USD | unknown |

前 8 个动作合同失败消耗了：

- 46,979 tokens，占总 token 的 47.3%；
- 612.5 s，占 decision wall time 的 49.2%；
- 8 个 operation slots。

WellAU 没有可验证的冻结价格表，因此 `accounting_complete=false`、
`monetary_accounting_complete=false`；报告中的数值 0 只是旧 schema 的占位，不代表
实际 billed USD 为 0。

## 7. 最值得保留的行为发现

### 7.1 接口错误会污染科学认知

前 8 步真正失败的是 `action_schema_valid`，但公开 constraint flags 同时出现了
`low_selectivity`。第 9–12 步 Agent 将这一 validator 状态解释为化学证据：

- 先加催化剂以“改善反应路径”；
- 再加溶剂以“降低副反应”；
- 在尚未获得真实实验表征前就围绕 low selectivity 展开化学推理。

这表明当前接口把**控制器/序列化错误**和**世界中的物理化学反馈**混在了同一认知通道。
同时，每次非法动作还更新 validation penalty ledger，而物理状态 constitution checks
本身全部通过。它可能诱发错误机制解释和不必要的资源消耗。后续必须把
`interface_validation_feedback` 与 `world_constraint_feedback` 分离。

### 7.2 合法阶段并非固定脚本回放

HPLC 之后，Agent 明确引用观测到的 yield、selectivity 和 byproduct，并选择 quench；
随后主动保留 `terminate + final_assay` 空间。这至少证明了该单轨迹中存在：

- 中间表征消费；
- 观测条件化动作；
- lifecycle headroom 管理。

但当前任务很短，且完整当前实验 ledger 仍未进入 prompt，不能据此推断复杂 G2 任务也会
稳定完成。

### 7.3 信息价值声明有部分结构，但未校准

Agent 给 HPLC 的 expected information gain 为 0.86，给 quench 和 terminate 分别为
0.12 和 0.05，说明它在语言声明上区分了“认知动作”和“执行/收尾动作”。但 compulsory
final assay 又被赋值 0.96，说明该数值还不是经过校准的信息价值估计，暂时只能作为行为
trace，不能直接当作认知指标。

## 8. 下一轮之前必须修的 P0

1. **冻结结构化动作合同。** 优先验证 provider 是否支持严格 JSON Schema；这属于生成
   接口约束，不是运行后 action repair。
2. **保留失败 payload 的安全证据。** 至少保存脱敏后的结构化 payload、schema error path
   和 hash；不保存 private reasoning。否则无法解释前 8 次究竟错在哪里。
3. **分离错误语义。** interface/schema failure 不能复用 low-selectivity 等物理 constraint
   flag，也不能被当作化学观测。
4. **把完整当前实验 ledger 送入每一步 prompt。** 当前 v1 虽内部保存 ledger，但 prompt
   只含压缩的最近决策和完成实验摘要。
5. **实现多账本资源卡。** 物料份数、仪器调用、样品量、过程资源、operation 和 compute
   必须独立扣账并逐步回执。

完成 P0 后，建议顺序是：

1. 在同一 public-dev world 上做 G2-v2 development qualification，确认 action-contract
   pass rate 和 constitution；
2. 再进入 low-budget campaign，观察跨实验资源分配；
3. 最后才上 crystallization/electrochemistry，避免重新把接口失败与科学难度混在一起。

正式结果必须换成冻结代码、干净 worktree、多 world/seed 和预注册重复；当前 provider
接口也没有可控 sampling seed，因此本轨迹可 replay，但不能保证重新调用模型时 bitwise
复现。

## 9. 证据与可复现入口

- launcher：`scripts/run_g2_smoke.py`
- frozen config：
  `runs/development/g2-reaction-to-assay-w0-a0-wellau-sol-high-v1/run_config.json`
- full trajectory：
  `runs/development/g2-reaction-to-assay-w0-a0-wellau-sol-high-v1/trajectory.jsonl`
- machine summary：
  `runs/development/g2-reaction-to-assay-w0-a0-wellau-sol-high-v1/run_summary.json`
- trajectory SHA-256：
  `5ee68e301e4f528a64a4807dad61c48705a1210db9b693b625f7554376d6e63b`
- source commit：`0005e239a26c276a95ea8ce291ab559caf00857d`
- source worktree：dirty；因此只能作为 development evidence

验证结果：

```text
trajectory replay: verified=true, checked_steps=17, max_abs_error=0
CLI --constitution audit: false, failures=steps 1..8 at action_schema_valid
physical-state constitution checks: passed at all 17 steps
G0 positive control: replay verified, CLI --constitution audit passed
focused tests: 52 passed
ruff + git diff --check: passed
```

上述 replay/constitution 是 post-run CLI 复核结果，未回写
`run_summary.json`；阈值 0.55 来自任务注册表，而不是本次 summary 的内嵌字段。
