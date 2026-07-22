# Campaign、Experiment 与 Operation

ChemWorld 用三个尺度描述实验。把它们分清，才能正确计算预算，也能避免把“在同一只反应器里继续
操作”误写成一次新实验。

```text
Campaign  一次完整研究运行
└── Experiment  从新鲜初态到一次合法终检
    └── Operation  投料、控制、测量或分离动作
```

## Campaign：这一轮研究

Campaign 绑定一个 Task、一个 Scenario、一个 Agent、一个 seed 与总预算；它就是规范 benchmark cell
`Task × Scenario × Agent × Seed` 的实际执行。主动学习或 BO 可以在同一个 Campaign 中完成
多次 Experiment，并使用前一次终检结果选择下一套 recipe。

## Experiment：一只新反应器中的完整流程

Experiment 从明确初始化的样品或过程状态开始，以合法 `final_assay`、显式终止、失败或预算截断结束。
只有合法 `final_assay` 形成可比较的正式结果；失败和未完成运行仍保留在自主性统计中。多次加热、追加
物料或中间测量仍属于同一个 Experiment；只有 campaign 模式下完成当前生命周期并换到 fresh vessel，
才开始下一次实验。

## Operation：状态真正发生变化的一步

`add_reagent`、`heat`、`measure`、`separate_phase` 和 `distill` 都是 Operation。每一步会经过 Action
schema 与前置条件检查，并返回实际时间、体积、样品、风险、成本和状态事务摘要。

## 两种 Episode 模式

| 模式 | `final_assay` 之后发生什么 | 适合什么任务 |
| --- | --- | --- |
| `single_experiment` | episode 结束 | 单条流程、控制与规划 |
| `campaign` | 保存结果，预算允许时开始新 Experiment | BO、主动学习、隐藏规律发现 |

## Final Assay 为什么特殊

合法终检会写入 `leaderboard_score`、Experiment 条件摘要和 campaign 进度。没有 final assay 的中间
reward 只用于学习与诊断，不能当作正式实验结果。

运行时负责校验和记录终止/终检语义，但不会在自主评测中替 Agent 选择 closeout。若协议允许辅助收尾，
必须将程序自治与此前实验选择产生的科学结果分开报告。

## Replay 需要记录什么

轨迹会保存 task metadata、seed、Action 序列、Experiment index、合同 hash 和必要随机流信息，
确保同一 Campaign 可以被重建。完整信任链见[验证结果可信度](release_integrity.md)。
