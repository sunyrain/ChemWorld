# Benchmark 协议

本协议定义 ChemWorld 任务的划分、运行、评分、验证和发布规则。任务必须保持逐任务报告，
不能用一个总分掩盖不同物理域、成熟度或失败模式。

## 套件

- `core`：三个紧凑任务，用于 API、回放和发布链路回归；
- `serious`：六个已通过结构合同与回放门禁、但仍在经验有效性审查中的候选研究任务；
- 显式 `--tasks`：用户自选任务，不自动获得正式套件声明。

```bash
chemworld baselines report --preset core
chemworld baselines report --preset serious
chemworld tasks readiness
```

正式套件的准入和冻结规则见[严肃任务设计](task_design.md)与
[Benchmark v1](benchmark_release.md)。

## 数据划分

- `public-dev`：接口调试、教学和 smoke；
- `public-test`：冻结任务与 seeds，用于可复现比较；
- `private-eval`：维护者控制的隐藏参数与 seeds，用于泛化评测。

所有 split 共享同一版本化世界律。私有参数、salt、隐藏物种量和机理参数不得进入公开
observation、trajectory 或 agent trace。

## 评测单位

`single_experiment` 任务以一条完整实验流程为单位；`campaign` 任务以固定总预算内的多条
experiment 为单位。报告至少包含：

- final-assay 分数与 best-so-far AUC；
- primary/secondary task metrics；
- invalid action、precondition、safety 与 cost；
- instrument 使用和 sample efficiency；
- task/scenario/mechanism/runtime/scoring/observation hashes；
- maturity、agent manifest 和 solver provenance。

## Baseline 与统计

正式比较由仓库中的 `configs/benchmark/publication_protocol_v0.1.json` 预注册，并由
`scripts/audit_publication_protocol.py` 失败关闭校验。当前协议固定六个 serious task、
20 个配对 seeds 和每个 task-seed-method 40 次完整实验；不允许按中间结果提前停止或改变方法。
0.05 的归一化 total-score 或任务主指标差异定义为最小实际重要差异（SESOI）。
报告逐任务配对效应、paired bootstrap 置信区间、符号翻转检验、标准差和逐 seed 结果，不发布
掩盖领域差异的跨任务总分；同一指标族跨六任务采用 Holm 校正。smoke override 只能验证管线，
不能用于性能声明。

确认性主比较是 typed categorical encoding 的 `structured_gp_bo` 对 `random`。`lhs` 是非自适应
空间填充对照，原始 `gp_bo` 是表示消融，`structured_safe_gp_bo` 是安全约束次要方法。stub、
replay trace 和脚本轨迹只做协议回归，不作为科学 baseline。每次运行同时记录墙钟、进程 CPU、
步骤数和完整实验数；正式 runner 会拒绝实验数不足、脏工作树或回放失败的结果。

```powershell
python scripts/audit_publication_protocol.py
python scripts/run_publication_protocol.py --stage confirmatory
python scripts/run_publication_protocol.py --stage full
```

随机配方探针的最大值只能称为 sampled recipe ceiling，不能称为 oracle，也不能直接用于 regret。
诊断阶段可报告“逐 seed 观测到的 best-known reference”，但未来方法允许超过它；正式 regret
必须绑定独立、可更新且逐 seed 的 reference 协议。

正式 evidence gate 还要求所有 baseline 无非法动作、每个 campaign 完成多轮实验、GP 进入
acquisition、成功阈值非饱和，并且 total score 与 primary metric 都能区分策略。
对以主动探索为主张的任务，还必须证明增加实验机会后至少一种可信自适应策略在部分任务上产生
达到 SESOI 的稳定收益；仅仅“进入 acquisition 阶段”不构成有效性证据。

实验预算必须用在线轨迹的预算—收益曲线校准，不能仅用搜索维度加常数。先导 40-experiment
diagnostic 表明部分 7–10 维任务在 8–12 个实验时仍处于冷启动，直到约 20–40 个实验才出现
正向 GP 相对收益；因此 40 次完整实验被固定为发表候选协议的统一学习预算。先导结果本身仍不
构成论文结果。

物料选择必须作为类别变量编码；数字 ID 只是序列化标识，不代表材料间具有欧氏顺序。连续过程
变量与 material one-hot/embedding 应分别进入 surrogate，正式比较必须披露该表示。

## 当前发表候选证据

2026-07-11 的正式经典方法矩阵在干净提交上运行 6 tasks × 5 methods × 20 paired seeds，得到
600 条 replay-verified 结果，每条 40 次完整实验。结构化 GP 相对 random 的 total score 在六项
任务均为正且 Holm 校正后显著，4/6 达到 0.05 SESOI；但任务主指标只有结晶和蒸馏达到 SESOI，
分配和流动方向为正但较小，电化学和平衡未显示主指标改善。

因此当前版本仍是 publication candidate，不是 validated benchmark。尤其不能把电化学复合总分
提升解释成 selectivity 提升；也不能报告安全 BO 优势。早期汇总器曾误读风险字段；修正后正式
矩阵存在非零连续风险，但 600 条结果没有一次 safety violation，安全约束从未激活。泛化、轴级
OOD、真实 LLM 和独立复现门禁仍未关闭。机器摘要可用以下命令从本地正式结果重建：

```powershell
python scripts/build_publication_evidence.py `
  --run-dir runs/publication/protocol-v0.1/full
python scripts/audit_agent_interactions.py `
  --results runs/publication/protocol-v0.1/full/baseline_results.json
```

## 方法交互审计

最终分数不能说明 Agent 是否真正使用了交互通道。正式报告同时区分：实验间 recipe 更新、实验内
动作调整、intermediate instrument 使用、谱图消费、约束激活、无效动作和资源消耗。当前五个正式
经典方法均为 recipe-level：random/LHS 不更新，三个 GP 方法根据已完成实验的 final score 更新；
没有方法把公开谱图作为特征，也没有方法在同一次实验中根据中间测量改变后续操作。

GP-PI、GP-UCB、RF-EI 和 greedy 已有实现，但现有正式协议没有保留其多 seed artifact。历史
DeepSeek pilot 展示了多轮操作、谱图读取和 schema 失败，但原始运行已不在本地证据目录，因此只能
作为工程诊断，不能作为论文或 leaderboard 结果。未来正式方法矩阵必须把轨迹、模型/prompt、
token/费用、修复次数、谱图依据、实验设计比较和 replay 状态一起保留。

当前 exploit 探针已覆盖未知操作、提前 final assay、提前 terminate、非有限数值、重复 final assay
和 action key 重排；六任务全部拒绝得分捷径，且 key 重排不改变轨迹。但这只关闭基础协议捷径，
不等于关闭完整反作弊门禁。当前每任务声明两个 generalization axis，却没有任何一个轴同时提供
interpolation、extrapolation、composition 和 observation-noise 的独立控制；material code remap、
observation field reorder 与等价动作序列接口也不可执行。因此 seed OOD 或整体 private-salt shift
只能报告为分布诊断，不能冒充轴级泛化证据。

20-seed public OOD（seeds 100–119）和 salted private-eval（seeds 200–219）已按相同 40-experiment
预算运行。结晶、蒸馏、流动、分配在两种 shift 下均保持 total score 与任务主指标的正 bootstrap
区间；电化学的 selectivity 区间仍跨零，平衡任务的 total 与主指标区间均跨零。因此两种 shift
都只有 4/6 任务通过。私有 salt 原值只存在于运行进程中，发布摘要仅保留 SHA-256。

## Verified Result Chain

```text
trajectory JSONL
  -> schema validation
  -> deterministic replay
  -> metric recomputation
  -> trajectory SHA-256 binding
  -> verified result JSON
  -> per-task leaderboard
```

`chemworld evaluate` 默认执行 replay。leaderboard 会校验 digest 并从轨迹重算指标；直接修改
result JSON、合同 hash、reward 或 observation 会被拒绝。

## 反作弊规则

提交不得读取 hidden scenario、`env.unwrapped._state`、私有 salt、隐藏 seed 表或 oracle state；
不得修改环境代码、写出评测目录或访问未授权网络。LLM trace 只保存 reasoning summary 和
decision evidence，不保存或要求完整 chain-of-thought。

提交格式和命令见[提交与验证](submission.md)，结果证据链见[结果完整性](release_integrity.md)。
