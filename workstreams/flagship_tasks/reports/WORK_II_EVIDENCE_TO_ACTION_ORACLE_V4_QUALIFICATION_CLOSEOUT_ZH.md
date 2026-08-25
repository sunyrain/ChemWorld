# Work II evidence-to-action oracle v0.4 资格收口

状态：**SCIENTIFICALLY REJECTED / 当前 96-grid oracle 路线关闭 / 不得进入 participant 或 formal**
日期：2026-08-24

v0.4 将局部 KNN4 升级为固定的 ExtraTrees：每个指标独立使用 `512` 棵树、
`min_samples_leaf=1`、`max_features=1.0`、不 bootstrap、`random_state=20260824`。拟合只读取
每个 world 的 `96` 个 disjoint-grid outcomes 与八个候选的公开 feature locations，不读取任何
候选 outcome、rank、checkpoint outcome、prior 或 provider 输出。ExtraTrees 的候选预测再通过
standardized minimum-norm least squares 精确蒸馏进既有 conditional-cubic typed-law schema。

在所有 `25` 个已暴露 construction worlds 上，固定 ExtraTrees 回放为 `25/25` 通过，最低
`rho=0.833333`、中位数 `0.952381`。这些结果只用于选定开发候选，不属于新资格证据。

全新 v0.4 qualification 按冻结顺序完成前五个 electrochemical worlds，Spearman 依次为
`0.880952, 0.850315, 0.952381, 0.976190, 0.785714`；前四个通过。第五个完整单元
`electrochemical-conversion / seed241995082` 完成 `96/96` grid truth、`16/16` registered truth
及 `112/112` exact replay；candidate opportunity gate 通过，raw score range 为 `0.546144`，
八个候选中有 `6` 个 raw regret 至少为 `0.05`。但是 oracle `rho=0.785714`，低于冻结门槛
`0.80`，且 Top-1 不一致。

该失败单元的 candidate design rank 为 `8`，typed-law 蒸馏最大绝对误差仅
`2.13e-14`；全部五个已完成单元的 rank 均为 `8`，最大蒸馏误差为 `9.95e-14`。因此失败不是
typed-law 无法表达树模型，而是当前 `96-grid -> 8 candidates` 设计下，ExtraTrees 在全新 world
上的候选排序外推仍不稳定。

预设 stop rule 已自动生效：计划 `15` 个 clusters，完成 `5`、通过 `4`、科学失败 `1`、未启动
`10`。合计完成 grid truth/replay `480/480`、registered truth/replay `80/80`，即总 truth/replay
`560/560`；fit/candidate overlap 为 `0`，candidate outcomes read 为 `0`，provider calls 为
`0`。没有换 seed、降低门槛、删除失败 world 或触碰五个 formal reserved seeds。

原始 W2-51 的 `reaction-to-crystallization / seed836245547 / rho=0.738095` 仍是独立、不可回写的
终局失败。v0.2、v0.3 与 v0.4 也是三个独立开发资格，各自失败记录并存。v0.4 是当前 96-grid
设计预先声明的最后一次 oracle-development iteration；不建立 v0.5，不恢复 participant cohort，
不授权 formal execution。若未来继续，必须提出新的 grid coverage / candidate-domain 设计问题，
另写 experiment note 并使用全新 prospective worlds。

机器收口：`work-ii-evidence-to-action-oracle-v0.4-qualification-closeout.json`。
