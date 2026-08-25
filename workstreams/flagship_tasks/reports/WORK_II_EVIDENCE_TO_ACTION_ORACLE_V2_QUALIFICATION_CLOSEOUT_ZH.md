# Work II evidence-to-action oracle v0.2 资格收口

状态：**SCIENTIFICALLY REJECTED / 不得进入 participant 或 formal**
日期：2026-08-24

oracle v0.2 计划覆盖 `3 tasks × 5 worlds = 15` 个全新 task-world clusters。第一个完整单元
`electrochemical-conversion / seed762707071` 完成 `96/96` grid truth、`16/16` registered
truth 和 `112/112` exact replay，candidate opportunity gate 通过，但 oracle 对八个候选的
Spearman `rho=0.785714`，低于冻结的 `0.80`。fit/candidate overlap 为 `0`，fitter 读取
candidate outcome 的次数为 `0`，provider calls 为 `0`。这是科学资格失败，不是平台失败。

按冻结 stop rule，v0.2 关闭且不得换 seed、降阈值或删除失败 world。停止过程中第二个单元
`seed712842817` 已完成 `48/96` grid truth 与 `48/48` exact replay；它永久保留为 incomplete，
没有执行 registered truth 或 oracle qualification，也不得在后续资格中复用。其余 `13` 个
task-world clusters 未启动。v0.2 合计落盘 `160` 条 truth 与 `160` 条 exact replay，零平台失败、
零 provider calls。

离线误差分解只把所有既有结果当作 exposed construction data。失败 world 上，outcome-blind
KNN4 局部预测本身为 `rho=0.904762`，蒸馏后的 conditional-cubic typed law 才降为
`0.785714`，所以失败来自蒸馏而非局部预测。候选域 exact typed distillation 在全部 `24` 个
已暴露 worlds 上回放为 `24/24`、最低 `rho=0.857143`；这只支持开发 v0.3，不构成资格证据。

机器收口：`work-ii-evidence-to-action-oracle-v0.2-qualification-closeout.json`。
