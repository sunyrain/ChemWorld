# Work II oracle gate 与动作目标对齐分析

## 结论

冻结的完整排序门槛与真正的动作目标并不等价。96-grid 的 W2-51 已完成单元中，
`7/8` 通过 `rho>=0.80`，但仅
`1/8` 选中真实第一名；反过来，320-grid
在首个全新 prospective world 上虽因 `rho=0.714286` 被合法拒绝，却选中了真实第一名，
其动作 regret 为零。W2-51/W2-52 的终态不改变，但这一分离应成为论文的核心结果，
而不是继续解释成 grid 仍不够大。

## Programme 收束

- W2-51 与 W2-52 均按完整固定分母形成终态结果，工作包状态为 `completed`；完成不等于科学门槛通过。
- 两项历史 `rho>=0.80` stop rule 原样保留，但不再是当前 ICLR 写稿、图表或其他独立实验的前置阻断。
- 原 225-session cohort 仍不获 participant 授权；不能用本分析把未执行的五条件因果对比写成已完成。
- 若未来新建 action-aligned prospective control，failure-aware normalized regret、距最优 `<=0.01`
  与 near-tie-aware ordering 是决策指标，complete-ranking Spearman 仅作辅助诊断；新 control 不复用这 16 个已暴露单元。

## 固定分母结果

| 证据组 | 单元版本 | rank gate 通过 | Top-1 | 距最优 <=0.01 | 平均 normalized regret | rank过但Top-1错 | rank不过但Top-1对 |
|---|---:|---:|---:|---:|---:|---:|---:|
| W2-51 96-grid fresh formal preparation | 8 | 7 | 1 | 3 | 0.0411 | 6 | 0 |
| W2-52 320-grid exposed construction | 7 | 7 | 4 | 6 | 0.0052 | 3 | 0 |
| W2-52 320-grid fresh prospective | 1 | 0 | 1 | 1 | 0.0000 | 0 | 1 |

320-grid 在 7/7 exposed construction 单元上通过，并修复四个已知 96-grid 失败；这只证明
对已暴露 world 的覆盖改善。首个全新 world 随即出现低完整排序相关但零动作损失，说明
主要问题已从‘是否能拟合已知失败’转为‘oracle 定义是否与研究的动作 estimand 对齐’。

## 边界

- 本分析复算 `16/16` 固定单元版本，未删除失败，未产生新 truth、provider call 或物理实验。
- 7 个 construction 单元不能估计泛化；1 个 prospective 单元也不能估计成功率。
- 不回溯修改 `rho>=0.80`、stop rule 或 W2-51/W2-52 disposition，不据此启动原 225-session cohort。
- 投稿主张应是‘完整排序泛化与动作充分性分离’，不是‘320-grid oracle 已经泛化成功’。
