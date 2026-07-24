# ChemWorld RC25 确认性实验计划与执行 TODO

状态：`superseded before formal execution by RC26`

> RC25 未消费任何正式 A2、A3 或 private seed。正式执行必须使用
> `RC26_FORMAL_EXECUTION_AMENDMENT_ZH.md` 及 RC26 默认配置；不得再运行本文中的
> RC25 输出路径。
适用协议：`chemworld-world-model-mechanism-adaptation-2026-07-24-redesign-rc25`  
控制文件：`configs/benchmark/mechanism-adaptation-preregistration-v0.3.0-rc25.json`  
原则：本文只安排执行，不修改 RC25 的世界、阈值、统计定义、cohort 或 scorer。

## 1. 实验目标与评估对象

实验按以下层级推进：

| 阶段 | 评估对象 | 核心问题 | 当前状态 |
| --- | --- | --- | --- |
| A1 | 物理世界与干预 | 隐藏干预是否只改变声明的物理规律 | 已通过，81/81 |
| A2 | controlled oracle/decoder | 在相同动作、测量和预算下，候选 family 是否可区分 | 待执行 |
| A3 | frozen reference diagnostic policy | 不知道变化时点和真值时，是否存在合规在线策略可建立参照、检测变化并归因 | 待执行 |
| Gate B | participant Agent | Agent 是否能检测变化且控制 no-change 假阳性 | 待正式 runner |
| Gate C | participant Agent | 反馈是否改变行为，以及这种改变是否提高任务效用 | 待正式 runner |
| Gate D | participant Agent | Agent 是否能在变化后恢复性能并优于 frozen policy | 待正式 runner |
| Gate E | participant Agent | Agent 能否自主完成完整实验生命周期 | 待正式 runner |
| Private confirmation | 冻结环境、方法与统计管线 | 公开阶段结论能否在未触碰 cohort 上复现 | sealed |

关键解释边界：

- A2/A3 是环境证书，不评价 DeepSeek、Claude 或其他参赛 Agent。
- participant Agent 从 Gate B 开始评价。
- A3 失败表示“当前冻结 reference policy 未证明 benchmark 在线可达”，不能解释成某个参赛 Agent 失败。
- Agent Gate B–E 失败不能反向推翻已通过的物理有效性或 controlled identifiability。

## 2. 冻结规模与计算单元

### A2

- 两个任务。
- 每个任务四个 truth，包括 `no_change`。
- 每个 task/truth 180 个独立 world-seed cluster。
- 共 1,440 个 task × truth × world cluster。
- controlled budget checkpoints：2、4；主 checkpoint 为 4。
- 六个 canonical actions 是 witness set，实际证书依据 relation closure。
- predictive fit 每个 task/candidate/action 使用 12 个 development samples。
- 8 个本地 worker，不调用外部 LLM provider。

### A3

- 两个任务，每个任务三个 changed family 加一个 `never`。
- 每个 task/truth 180 个独立 world-seed cluster，共 1,440 个在线 trial。
- `truth_change_time={never,6,8,10}`；数字表示已完成的旧世界实验数。
- 每个 changed family 在 6、8、10 三个时点各 60 个 cluster。
- post-change checkpoints：`k={1,2,4,8}`。
- 每个 trial 最多运行到第 18 个实验；总实验调用上界约 25,920，按平衡时点估计约 23,040。
- 8 个本地 worker，不调用外部 LLM provider。

### Participant-Agent development matrix

当前公开 development matrix 为：

- 900 个 paired cells；
- 1,800 个 changed/no-change campaign arms；
- 2 tasks × 3 changed families × 3 changepoints × 5 public world seeds ×
  5 provider repeats × 2 label modes × 2 arms。

provider repeats 是同一物理 cluster 内的技术重复，不能当作 1,800 个独立统计样本。

## 3. 总体执行顺序

```text
RC25 source/preregistration check
  → A3 standalone certificate
  → A2 controlled certificate + Gate A composition
  → immutable public A2/A3 decision
  → freeze participant-Agent methods and formal B–E runner
  → Gate B–E development/shakedown
  → public participant-Agent confirmation
  → unseal private confirmation
  → evidence DAG / manuscript tables
```

A3 先于 A2 仅是当前 CLI 组合方式所需的操作顺序，不代表先查看 A3
结果再调整 A2。两者的策略、阈值、seed namespace 和 scorer 均已冻结；无论
A3 是否通过，都必须继续完成 A2，禁止 optional stopping。A3 完成后只生成
schema、hash、单元完整性和资源状态 receipt，不生成或查看 family/metric
摘要；A2 也完成后才一次性解封联合决策表。

## 4. Phase 0：正式运行前锁定

### 0.1 代码、协议和证据

- [x] `P0-01` RC25 protocol 已冻结。
- [x] `P0-02` preregistration 已生成并绑定 implementation commit。
- [x] `P0-03` 设计审计 81/81 通过。
- [x] `P0-04` 确认性任务语义审计 25/25 通过。
- [x] `P0-05` 样本量审计通过，选择 180 independent clusters/family。
- [x] `P0-06` evidence DAG 33 节点、0 stale。
- [ ] `P0-07` 在正式运行机器上确认 `git status --short` 为空。
- [ ] `P0-08` 运行 preregistration `--check`，保存 stdout 和 exit code。
- [ ] `P0-09` 运行 evidence DAG `--check`，保存 stdout 和 exit code。
- [ ] `P0-10` 记录 HEAD、Python 版本、依赖快照、CPU、内存、磁盘剩余量和时区。
- [ ] `P0-11` 确认 A3 和 Gate A 正式输出路径均不存在，避免覆盖不可变结果。
- [ ] `P0-12` 确认 private seed material 仍 sealed，运行人员未查看。

建议检查命令：

```powershell
git status --short
git rev-parse HEAD
$env:PYTHONPATH = "src;."
.\.venv\Scripts\python.exe scripts\build_mechanism_adaptation_preregistration.py --check
.\.venv\Scripts\python.exe scripts\evidence_pipeline.py --check
```

正式运行前只执行 RC25 相关定向测试，不运行全仓测试。任何 smoke test 必须使用
development namespace，不能消费 A2、A3 或 private seeds。

### 0.2 运行目录与日志

- [ ] `P0-13` 创建 `runs/mechanism-adaptation-v0.3.0-rc25-formal/logs/`。
- [ ] `P0-14` 为 A2 和 A3 分别记录启动时间、结束时间、wall time、peak memory、exit code。
- [ ] `P0-15` 日志不得包含 provider key、private salt 或隐藏真值映射。
- [ ] `P0-16` 设置磁盘预警；运行中只清理可重建的临时缓存，不删除轨迹或报告。

### 0.3 新增运行资格护栏

- [x] `P0-17` 在冻结 commit 上运行一套覆盖 A2/A3 全部生产代码路径的正式 release qualification suite；继续不做无关的全仓测试。
- [ ] `P0-18` 从 clean detached checkout 或构建 wheel 安装后运行一次端到端集成测试，并保存环境锁定文件与不可变 release tag。
- [x] `P0-19` 将 trial 唯一键固定为 `task × truth × world_cluster × changepoint × arm`，验证写一次 receipt、基础设施失败 attempt ledger 和 missing-only resume。
- [x] `P0-20` 将 decision script、bootstrap、table generator、censoring、failure/exclusion aggregation 和 pass/fail state machine 纳入 preregistration hash。
- [x] `P0-21` 仅使用 development sentinel namespace 完成端到端 dry run，验证最终表格可从 trial manifest 重建。

RC25 已将原型能力收束到生产路径并删除临时 prototype：

- release qualification 在冻结 commit 上完成 112 项定向测试，未运行全仓测试；
- write-once receipt、attempt ledger、missing-only resume 和结构完整 manifest 已进入正式 runner；
- keyed noise 按语义坐标配对，策略分叉后仅比较共同坐标，pre-change 坐标必须完全一致；
- metric-embargo receipt 只公开 hash、schema、单元完整性与资源状态，不提前公开 A2/A3 科学指标；
- Participant-Agent 决策输入采用 `chemworld-compact-decision-context-0.2`；开发哨兵约 520/1500 tokens，未传原始谱图数组和审计元数据。

以上仍为 `formal_result=false` 的运行资格证据，不是 A2/A3 科学结果，也不允许据此解封 private cohort。

## 5. Phase 1：执行 A3 online attainability

正式输出：

```text
workstreams/flagship_tasks/reports/
mechanism-adaptation-online-attainability-certificate-v0.9-rc25.json
```

执行命令：

```powershell
$env:PYTHONPATH = "src;."
$a3Report = "workstreams/flagship_tasks/reports/mechanism-adaptation-online-attainability-certificate-v0.9-rc25.json"
$a3Log = "runs/mechanism-adaptation-v0.3.0-rc25-formal/logs/a3-online-attainability.log"

& .\.venv\Scripts\python.exe scripts\run_mechanism_adaptation.py `
  --stage online-attainability-certificate `
  --online-attainability-output $a3Report 2>&1 |
  Tee-Object -FilePath $a3Log

$a3ExitCode = $LASTEXITCODE
```

TODO：

- [ ] `A3-01` 启动完整 1,440-trial A3，不抽样、不提前查看中间 family 结果。
- [ ] `A3-02` 持续记录 task/candidate/job 进展；不因为某个 family 暂时失败而停止。
- [ ] `A3-03` 区分 exit code 1 的“完整负结果”和异常退出；先检查报告是否完整。
- [ ] `A3-04` 核对 `protocol_sha256`、`gate_a_plan_sha256` 和 execution binding。
- [ ] `A3-05` 核对 certification subject 为 `frozen_reference_diagnostic_policy`。
- [ ] `A3-06` 核对 policy 未收到 phase/reset、change-time support、prefix 或 reference certificate。
- [ ] `A3-07` 核对 changed 与 never trial 成对使用相同 world seed、reset 和噪声流。
- [ ] `A3-08` 核对 relation closure，而不是 canonical recipe-ID completion，控制 reference pass。
- [ ] `A3-09` 核对 predictive adequacy 仅使用 campaign 内 pre-change LOO cross-fitting。
- [ ] `A3-10` 核对 `k={1,2,4,8}` 的 AUROC、Brier、recall、FPR 和右删失 delay 均存在。
- [ ] `A3-11` 核对 task-level、family-level、macro 和 supplemental pooled-micro 表。
- [ ] `A3-12` 对输出计算 SHA-256，复制到只读归档；不重跑以挑选更好结果。
- [ ] `A3-13` 核对 keyed/counter-based noise key、noise provenance，以及策略分叉后共同操作的噪声一致性；相同 seed 本身不算通过。
- [ ] `A3-14` 从 immutable trial manifest 核对恢复后 0 重复、0 遗漏；基础设施失败和科学失败采用不同 reason code。

A3 pass 必须同时满足：

- reference acquisition Wilson lower bound；
- changed recall cluster-bootstrap lower bound；
- never horizon-FPR upper bound；
- AUROC lower bound；
- integrated/mean Brier；
- conditional attribution；
- end-to-end success；
- overall、每个任务和每个 changed family 的交集规则。

## 6. Phase 2：执行 A2 并组合 Gate A

正式输出：

```text
workstreams/flagship_tasks/reports/
mechanism-adaptation-gate-a-v0.3.0-rc25.json
```

执行命令：

```powershell
$env:PYTHONPATH = "src;."
$a3Report = "workstreams/flagship_tasks/reports/mechanism-adaptation-online-attainability-certificate-v0.9-rc25.json"
$gateAReport = "workstreams/flagship_tasks/reports/mechanism-adaptation-gate-a-v0.3.0-rc25.json"
$gateALog = "runs/mechanism-adaptation-v0.3.0-rc25-formal/logs/a2-controlled-and-gate-a.log"

& .\.venv\Scripts\python.exe scripts\run_mechanism_adaptation.py `
  --stage gate-a `
  --online-attainability-certificate $a3Report `
  --output $gateAReport 2>&1 |
  Tee-Object -FilePath $gateALog

$gateAExitCode = $LASTEXITCODE
```

TODO：

- [ ] `A2-01` 即使 A3 为 failed，也按固定矩阵完整执行 A2。
- [ ] `A2-02` 确认 A2 使用 namespace `3800000000`，不与 development/A3/private 重叠。
- [ ] `A2-03` 确认 fit、action selection 和 held-out certification seed 分离。
- [ ] `A2-04` 检查 budget 2、4 的 active oracle 曲线；只让 budget 4 控制 A2。
- [ ] `A2-05` 单独报告 fixed decoder，但不得让 decoder 替代 active-oracle gate。
- [ ] `A2-06` 检查两个任务和所有 family 的 recall 与 Wilson interval。
- [ ] `A2-07` 检查 nuisance integration、matched pre/post action 和 measurement contract。
- [ ] `A2-08` 检查 A1、A2、A3 三证书均被 hash-bound 引用，没有嵌入重复大轨迹。
- [ ] `A2-09` 对正式 Gate A 报告计算 SHA-256 并复制到只读归档。
- [ ] `A2-10` 核对 fit、action selection 和 certification 单元均有不可变 manifest，可确定性恢复且不重复消费正式单元。

Gate A 的解释：

| A2 | A3 | Gate A | 允许的结论 |
| --- | --- | --- | --- |
| pass | pass | pass | 环境在 controlled 与冻结在线 reference policy 下均可识别 |
| fail | 任意 | fail | 给定动作/测量/预算下 controlled identifiability 未建立 |
| pass | fail | fail | controlled 信息存在，但冻结在线 reference policy 未证明可达 |
| fail | fail | fail | 两层证据均不足，必须分别报告原因 |

负结果不得通过改阈值、删 family、换 seed、增加预算或重跑择优来“修复”。

## 7. Phase 3：冻结公开 A2/A3 决策

- [ ] `PUB-01` 使用独立审阅脚本验证两个正式 JSON 可解析、hash 和 schema 正确。
- [ ] `PUB-02` 输出每个 task/family/checkpoint 的完整结果表和置信区间。
- [ ] `PUB-03` 输出 changed 与 never 的独立分母及无定义项说明。
- [ ] `PUB-04` 输出 reference failure、detection failure、attribution failure 的分解。
- [ ] `PUB-05` 输出 wall time、worker、异常和资源使用，不只报告科学指标。
- [ ] `PUB-06` 生成一个 immutable public A2/A3 decision artifact。
- [ ] `PUB-07` 以 result-only commit 保存正式报告；不得同时修改 protocol/scorer。
- [ ] `PUB-08` 将 evidence DAG 的 pending 路径切换到正式报告路径并刷新 current registry。
- [ ] `PUB-09` 再次运行 preregistration check 和 evidence DAG check。
- [ ] `PUB-10` 在公开决策提交后才允许满足 private unseal 的第一项条件。
- [ ] `PUB-11` 按预注册 go/no-go 分支执行：A2 fail 停止正式 B–D；A2 pass/A3 fail 时 B–D 仅为探索性；两者通过后才允许正式 B–E 和机制 private confirmation。
- [ ] `PUB-12` 分开报告 `benchmark_ready`、`evidence_complete` 和 `publication_ready`；participant Agent 表现正负是结果，不是 publication readiness 的必要条件。

## 8. Phase 4：补齐并冻结 Participant-Agent Gates B–E runner

当前 `campaign` 和 `pilot-report` 入口属于 development，明确记录
`formal_result=false`。在完成以下 TODO 前，不得把它们称作正式 Gate B–E。

### 8.1 共用 runner 与方法冻结

- [ ] `AG-00` 建立独立的 participant-Agent preregistration/manifest。
- [ ] `AG-01` 冻结 method roster、模型版本、prompt、tool scaffold 和 memory policy。
- [ ] `AG-02` 单轮基线、当前 operation-level Agent 和未来 deep-agent scaffold 分轨报告。
- [ ] `AG-03` 冻结 provider temperature、max tokens、重试、timeout 和 provider-seed 策略。
- [ ] `AG-04` 冻结每个方法的 billing ceiling；不得因某方法更贵而中途减少其样本。
- [ ] `AG-05` 实现 formal campaign materializer；不能继续只使用 public seeds 0–4。
- [ ] `AG-06` 明确 formal participant-Agent cohort 与 A2、A3、private namespaces 的关系。
- [ ] `AG-07` 将 provider repeat 固定为 cluster 内技术重复，cluster bootstrap 以 world 为单位。
- [ ] `AG-08` 实现 reason-coded provider failure、invalid action、incomplete campaign 和 exclusion ledger。
- [ ] `AG-09` 实现不可变 campaign index、trajectory hash、prompt hash 和 provider receipt。
- [ ] `AG-10` 在 development seeds 上完成 runner shakedown，确认后冻结，不查看 formal/private 结果。
- [ ] `AG-11` 冻结 backend × scaffold 二维矩阵：固定 backend 比较 direct/ReAct/planning/stateful scaffold；固定 scaffold 比较 backend。
- [ ] `AG-12` 同时报等物理实验预算下的性能，以及 calls/tokens/cost/wall-time/retry/sub-agent 使用与性能的 Pareto 关系。
- [ ] `AG-13` 对 Gate B–E 独立完成 world-cluster 样本量审计，不把 provider repeat 当作独立样本。

### 8.1.1 Participant-Agent prompt 决策上下文资格

本节不影响 A2/A3；它约束 Gate B–E 的 LLM 输入。直接采用新的分层表示，
不把旧冗余表示作为正式 A/B 条件。

- [x] `AG-P01` 每轮默认 prompt 只包含任务目标、当前实验/预算、最新可见指标、活动约束、测量摘要、历史最佳、最近两次实验和合法动作签名。
- [x] `AG-P02` 原始谱图数组、replicate curves、重复 observation views、完整历史、constitution checks、Git/provider/ledger 元数据不得进入默认决策上下文。
- [ ] `AG-P03` 完整谱图、动作 schema 和历史实验只能通过 public ID 按需请求；请求和返回均进入轨迹。
- [x] `AG-P04` 默认提示采用硬 token 上限；开发原型为保守估算 1,500 tokens，正式值和 provider tokenizer 校准须在 participant preregistration 中冻结。
- [x] `AG-P05` 超限必须显式失败或按固定优先级缩减可选摘要；不得静默删除当前指标、活动约束、合法动作必需参数或输出契约。
- [x] `AG-P06` 输出仅要求 action、expected effect、diagnostic target、expected information gain、预声明 belief-update rule、Gate B 所需的 `p(change)`/family belief、uncertainty 和可选 detail request。
- [x] `AG-P07` 不要求模型每步重复 evidence/rationale/diagnostic rationale/information-value/spectrum-interpretation 等语义重叠字段。
- [x] `AG-P08` 机制概率必须与可检查的预声明更新规则共同输出；不把叙述性“手调概率”视作严格 Bayesian update。
- [x] `AG-P09` trajectory 继续保留完整公开 observation、原始谱图、prompt hash 和 provider receipt；prompt 精简不得降低审计与复现能力。
- [ ] `AG-P10` 正式执行前记录每步 provider-reported prompt tokens、压缩层级和 on-demand retrieval；不得用日志 JSON 字节数冒充实际模型输入量。

### 8.2 Gate B：变化检测

- [ ] `B-01` changed/no-change twin 使用完全相同前缀和 common random numbers。
- [ ] `B-02` pseudo-checkpoint 不产生 agent-visible event 或 metadata change。
- [ ] `B-03` 收集 `k={1,2,4,8}` 的 `p(change)`，而不是只保留最终值。
- [ ] `B-04` 记录首次 `p(change)>=0.5` 的检测事件，未检测按 k=8 右删失。
- [ ] `B-05` changed 报 recall/AUROC/Brier/delay，never 报 horizon FPR/no-false-alarm。
- [ ] `B-06` 按 task、changed family、label mode 和 interface 分层。
- [ ] `B-07` task/family/macro 采用交集通过；pooled micro 只作补充。

### 8.3 Gate C：反馈敏感性与效用

- [ ] `C-01` 局部配对测试固定完全相同 history prefix，只替换最后反馈。
- [ ] `C-02` 条件至少包括 true、permuted、delayed、critical-measurement-deleted。
- [ ] `C-03` 局部指标包括 belief shift、change probability、下一行动和 action-distribution divergence。
- [ ] `C-04` 完整 campaign 使用相同 world/prompt/model/provider 配置和预算。
- [ ] `C-05` 分开报告“反馈是否改变行为”和“反馈是否提高最终效用”。
- [ ] `C-06` between-condition effect 必须超过 within-provider-repeat noise。
- [ ] `C-07` 不把负 feedback effect 直接解释成“错误反馈更好”，先检查 provider 噪声和前缀配对。

### 8.4 Gate D：适应与恢复

- [ ] `D-01` adaptive participant policy 运行 shifted world。
- [ ] `D-02` frozen-policy baseline 运行同一 shifted world。
- [ ] `D-03` IID action replay 分别运行 IID world 与 shifted world，估计 open-loop world effect。
- [ ] `D-04` diagnosis oracle 在相同预算下运行，提供恢复上界。
- [ ] `D-05` 计算 normalized recovery、cumulative regret 和 checkpoint recovery curve。
- [ ] `D-06` 要求 adaptive policy 优于 frozen policy，且 recovery lower CI ≥ 0.50。
- [ ] `D-07` 区分不会更新、更新慢、识别后不能恢复三类失败。
- [ ] `D-08` 预先冻结 normalized-recovery 的最小 oracle gap；分母低于阈值的 cell 标为 non-informative 并完整报告，不得事后删除。

### 8.5 Gate E：程序自治

- [ ] `E-01` autonomous run 中不进行系统强制 closeout。
- [ ] `E-02` terminate/assay/lifecycle 失败计入 protocol failure。
- [ ] `E-03` 另行生成 assisted scientific score，保留之前动作的科学价值。
- [ ] `E-04` assisted history 不得进入后续 autonomous 上下文。
- [ ] `E-05` 报 protocol-failure rate 及其上置信界；要求上界 ≤ 0.05。
- [ ] `E-06` 同时报 autonomous score 与 assisted scientific score。

## 9. Phase 5：Private confirmation

当前仓库只有 private cohort 的冻结规则和 namespace，尚无独立正式
private-confirmation CLI stage。以下事项完成前保持 sealed：

- [ ] `PRV-01` public A2/A3 decision artifact 已不可变提交。
- [ ] `PRV-02` participant-Agent method roster、runner、统计代码和 exclusion policy 已冻结。
- [ ] `PRV-03` 新增并审计专用 private runner；不得复用 `formal_result=false` 的 pilot。
- [ ] `PRV-04` 在解封前提交 private seed commitment/hash，不提交明文 seed。
- [ ] `PRV-05` 确认 private namespace 从未用于开发、阈值选择或错误排查。
- [ ] `PRV-06` 一次性运行固定矩阵；禁止根据 interim result 停止或补样本。
- [ ] `PRV-07` private failure 只能形成负结果，不能反向修改 RC25 阈值或 scorer。
- [ ] `PRV-08` 将 private 结果与 public 结果并列报告，标明是否复现。
- [ ] `PRV-09` 在解封前将 namespace 不可变拆为 Private-E（环境 A2/A3 复现）和 Private-A（participant-Agent 矩阵复现），任一子集不得用于另一子集的调试。

## 10. 最终报告必须包含的表

- [ ] `REP-01` A1/A2/A3/Gate B–E 状态机总表。
- [ ] `REP-02` A2：task × family × budget 的 top-1、recall 和 Wilson CI。
- [ ] `REP-03` A3：reference、detection、attribution、end-to-end 分解。
- [ ] `REP-04` A3：`k={1,2,4,8}` 的 AUROC、Brier、recall、FPR 和 delay。
- [ ] `REP-05` changed 与 never 分母、样本量、cluster 数和 provider repeats。
- [ ] `REP-06` Gate B 的 Agent 时序检测与校准。
- [ ] `REP-07` Gate C 的局部行为反应和完整 campaign utility，二者分开。
- [ ] `REP-08` Gate D 的 adaptive/frozen/replay/oracle 恢复曲线。
- [ ] `REP-09` Gate E 的 autonomous 与 assisted 双分数及 protocol failures。
- [ ] `REP-10` 每个 task、family、label mode、interface、method 的分层结果。
- [ ] `REP-11` provider failures、exclusions、invalid actions、右删失和缺失数据。
- [ ] `REP-12` token、费用、wall time、worker 和完整 provenance。
- [ ] `REP-13` macro 与 task/family intersection 为主，pooled micro 明确标为 supplemental。
- [ ] `REP-14` publication readiness 单独判断，不由文件齐全或某个 pooled 指标自动推出。

## 11. 近期执行优先级

### 现在立即做

1. 审阅开发哨兵，只把成熟部分整合到正式 runner 设计。
2. 完成 `P0-17` 至 `P0-21`；整合运行路径需要新 source binding 时创建 RC25，不得让 RC25 preregistration 静默漂移。
3. 完成 `P0-07` 至 `P0-16`，确认正式机器、sealed material 和输出路径。
4. 所有运行资格项通过后，才运行完整 A3；只查看 metric-embargo structural receipt。
5. 无论 A3 科学结果如何，立即运行完整 A2，之后联合解封并固化 public Gate A decision。

### A2/A3 之后做

1. 完成 participant-Agent formal runner 与独立 preregistration。
2. 在 development seeds 上完成 Gate B–E shakedown。
3. 冻结模型、prompt、scaffold、provider 和费用上限。
4. 执行正式 participant-Agent matrix。

### 暂时不要做

- 不改 RC25 阈值、family、预算或 changepoint。
- 不用 A2/A3/private seeds 做 smoke test。
- 不把 DeepSeek pilot 或 public development matrix 写成正式 Agent 结果。
- 不在 A2 或 A3 中途因暂时失败而停止。
- 不在 public A2/A3 decision 固化前解封 private cohort。
- 不因生命周期 assistance 而把 assisted success 记为 autonomous success。

## 12. 完成定义

本计划完成需要同时满足：

1. A2 和 A3 按固定矩阵完整执行并形成不可变 public decision；
2. participant-Agent formal runner、方法和统计协议单独冻结；
3. Gate B–E 按配对设计完整执行；
4. private confirmation 在解封条件满足后一次性执行；
5. 所有报告均能从 trajectory、receipt、hash 和 preregistration 重建；
6. `benchmark_ready` 只表示 A1–A3 通过且 runner、统计和 replay 已验证；
7. `evidence_complete` 表示 Gate B–E 及 public/private 结果均按冻结协议执行和报告，不要求 participant Agent 得到正结果；
8. `publication_ready` 表示证据完整、论文声明与实际正/负结果匹配、private confirmation 已报告，不以某个 Agent performance gate 必须通过为条件。
