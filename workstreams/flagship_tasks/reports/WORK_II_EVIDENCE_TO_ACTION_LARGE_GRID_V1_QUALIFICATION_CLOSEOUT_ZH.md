# Work II evidence-to-action large-grid v1.0 资格收口

状态：**SCIENTIFICALLY REJECTED / 不得进入 participant 或 formal**
日期：2026-08-24

large-grid v1.0 在七个已暴露 construction units 上 `7/7` 通过，并将四个历史失败分别从
`0.785714, 0.785714, 0.738095, 0.595238` 提升至
`0.904762, 0.904762, 0.928571, 0.928571`。该结果证明扩大到 `320` grid points 能修复
已知失败，但仅属于 construction，不是泛化证据。

独立 prospective qualification 的第一个全新单元
`electrochemical-conversion / seed799649867` 完成 `320/320` grid truth/replay 与
`16/16` registered truth/replay。candidate opportunity gate 通过，raw score range 为
`0.594633`，八个候选中有 `6` 个 raw regret 至少为 `0.05`；fit/candidate overlap 为 `0`，
candidate outcomes read 为 `0`。

oracle 的 Top-1 与真实 Top-1 一致，但完整八候选排序的 Spearman 仅
`rho=0.714286 < 0.80`。这两项不矛盾：Top-1 只检查第一名，Spearman 检查八项整体顺序。
candidate design rank 为 `8`，typed-law 蒸馏最大绝对误差仅 `3.55e-14`，artifact 保留全部
`320` 个 fit IDs，并在 typed law 中按 schema 上限确定性引用 `128` 个。因此本次失败不是
候选不可区分、candidate leakage、law schema 或蒸馏误差，而是 320-grid ExtraTrees 对新 world
的完整候选排序外推仍不稳定。

首个科学失败触发预设 stop rule：计划 `15` 个 clusters，完成 `1`、通过 `0`、科学失败 `1`、
未启动 `14`。总 truth/replay 为 `336/336`，provider calls 为 `0`；没有换 seed、删失败 world、
降低 `rho>=0.80` 或触碰五个 formal reserved seeds。

结论：增加 grid 是有效的 construction 修复，但没有通过新 world 资格，不能据此恢复 W2-51 或
启动 participant/formal。若继续换模型或再加 grid，`seed799649867` 已经暴露，只能作为未来
construction 诊断，不能再次充当资格；任何下一版都必须先提出与当前失败相对应的新预测设计，
再冻结另一组全新 prospective worlds，不能通过连续调参把已暴露失败“修到通过”。

机器收口：`work-ii-evidence-to-action-large-grid-v1.0-qualification-closeout.json`。
