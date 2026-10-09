# R20 / R34 / R35：公开边界、批次语义与未完成结果

开发块，Codex /root。不引入托管沙箱、任意样品身份或新结果系统；复用现有 public payload 校验、campaign IDs、logger/exporter 和 dataset_card。

固定覆盖：seed 0 四类记录——R02 的 10 步零晶体路径（含 filter 预期失败）正常终检；reaction-to-assay 的两步加料后停止（没有终检）；一个 operation budget=2 的两步加料截断；一个带资源卡的 campaign 两步加料、明确弃批、下一批加溶剂后停止（4 步）。总 18 动作、4 campaign、5 个记录到的批次，预期 1 终检负结果/1 弃批/1 截断未终检/2 开放未终检。导出 JSONL 与 Parquet（如锁定环境未装 backend 则记录缺失而不自行安装），检查原始 null/mask/成本/失败/分母，四条轨迹 zero-tolerance replay。笔记自由与 host 事实权限不混淆。

边界：全部 15 注册任务的 seed 0 task_info/prompt/schema 及 public view；各一条固定 0.5 task recipe，另在开始时提交一次未知 operation 作为错误边界。逐步验证公开 payload 不含 evaluator truth/隐藏物种/定律/参数或 traceback；记录所有失败与各路径终态，不把意料外科学失败藏掉。用同一执行进程记录实际读取的仓库 runtime JSON/YAML/CSV 等路径，交 LYJ 打包清单；这不等于验证 wheel/sdist，也不声明本地包拥有者无法读私有代码或文件。

不运行历史全局安全审计或刷新其 hash 绑定，只跑当前接口定向测试。输出 `D:/Projects/ChemWorld-local-research/20261009-r20-r34-r35/`。

## 结果与失败保留

- 结果块通过：4 个 campaign、5 个有操作记录的批次、18 次动作，其中 17 次提交和 1 次预期拒绝。保留 1 个终检负结果、1 个弃批、1 个预算截断未终检、2 个开放未终检；负结果是终检数的子集，不重复计入批次总数。4/4 轨迹零容差回放通过。
- JSONL 导出保留全部 18 次动作；缺失晶体统计仍为 null、对应 mask=false，未终检的 leaderboard_score 仍为 null，拒绝原因、测量成本与实际取样消耗保留。共享扁平化层也验证这些字段。dataset_card 增加逐批结束类型、操作提交/拒绝分母及当前执行语义标识。
- campaign 弃批后换到新釜：操作的 experiment_index 为 `[0, 0, 0, 1]`，弃批摘要为 `batch-0001`；跨两批累计溶剂消耗 0.05 L、vessel starts=2，弃批不退还已消耗库存。logger 的 environment_outcome 保留终态摘要、弃批与右删失标记。
- 首轮边界 runner 调用 action_schema 时漏传 operation，15/15 单元在执行操作前失败；`attempt-01/summary.json` 原样保留。该轮结果/导出块已通过，数据在 `attempt-01/outcomes/`，没有为取得更好结果重跑。修正 runner 后只重新执行完整边界块，结果为 `attempt-02/summary.json`。
- 修正后的边界块 15/15 通过：181 次动作，包含 15 次预期未知操作拒绝；736 个公开 payload 未检出 evaluator truth、隐藏物种/定律/参数或 traceback；15 次终检和 15/15 零容差回放。范围为上述固定任务、seed 和路径，不作为任意恶意代码的隔离证明。
- Parquet 实际导出调用返回明确的可选 backend 缺失诊断；锁定环境无 pyarrow/fastparquet，未安装新依赖。**没有验证 Parquet 文件导出成功**；LYJ 若承诺该可选功能，应在安装矩阵中验证。

相关定向检查先后为 39 passed 和 36 passed；修改的 datasets/logging 通过 mypy，两个模块及新增测试通过 Ruff。最后一次跨本轮核心改动的集成回归为 **327 passed / 0 failed（40.28 s）**，覆盖热控/负结果、时钟、CLI、长历史/笔记/IPC/MCP、采样/Gym、过程状态、语义标识/回放、风险、任务设计、结果导出、资源及公开边界。12 条 Gym 提示涉及 wrapper 和动作空间归一化建议，checker 均通过。此前一次集成命令写错 CLI 测试文件名而收集失败、0 项执行；修正为 test_cli_errors.py 后才得到上述集成结果。未运行冻结报告相等性或全局 hash 审计。

## LYJ R16/R32/R37：批次和结果解释

| 字段或动作 | 当前含义 |
| --- | --- |
| campaign_id | 一次 episode 的独立标识；同一 seed 不代表同一个 campaign |
| experiment_index | 日志中的批次索引，从 0 开始；同一索引内是同釜继续 |
| lifecycle_experiment_index / batch_id | 终态摘要中从 1 开始的显示序号和 batch 标签；摘要原始 experiment_index 仍从 0 开始，不把 experiment_index_base=1 套到原始字段 |
| terminate / final_assay | 显式停止过程后完成终检；终检闭合批次，不保证化学成功，零晶体也是可记录的负结果 |
| campaign 下一批 | 当前批次终检或弃批后，资源允许时初始化新釜；共享 campaign 资源账本继续累计 |
| discard_batch | 受 campaign 模式及资源卡政策约束；保留原因和资源后果，不伪造终检、不退款 |
| 记录停止 / 预算截断 | 前者是开放未完成记录，后者单列 truncated；均不能补成成功终检或把缺失分数填成 0 |

复用 TrajectoryLogger、export_dataset 和 dataset_card 即可。outcome_counts 只统计实际记录到的批次：终检、弃批、截断未终检、开放未终检四类互斥；negative_final_assay_count 是第一类的子集。未记录任何动作的初始空釜不进入该分母。支持模型自由写 notebook，宿主事实账本由现有工具接口维护；这不等于操作系统沙箱。

## LYJ R06/R12：实际读到的运行资源

导入 ChemWorld 前安装文件读取探针，覆盖本块 15 个任务和回放；观察到以下资源：

```text
configs/mechanisms/autocatalytic_reaction.yaml
configs/mechanisms/catalyst_deactivation.yaml
configs/mechanisms/electrochemical_conversion.yaml
configs/mechanisms/parallel_series_reaction.yaml
configs/mechanisms/pfr_hotspot.yaml
configs/mechanisms/reaction_extraction.yaml
configs/mechanisms/reactive_distillation_lite.yaml
configs/mechanisms/simple_batch_reaction.yaml
configs/scenarios/mechanism_scenarios.yaml
```

这是已测路径观察到的最小集合，**不是完整打包 allowlist**。其他可选功能、声明式 schema/authoring 资源仍须按实际发行支持范围补足，并在仓库外验证真实 wheel/sdist。当前打包配置广泛纳入 configs，Ours 没有修改 LYJ 所有的 packaging 文件。私有 evaluator provenance、研究配置与原始日志不能通过 Agent 接口提供；本地安装包拥有者仍能读取其持有的代码和资源，因此不能据此宣称文件保密或托管安全沙箱。
