# Work II evidence-to-action oracle v0.3 资格收口

状态：**SCIENTIFICALLY REJECTED / 不得进入 participant 或 formal**
日期：2026-08-24

v0.3 在五个全新 electrochemical worlds 上 `5/5` 通过，Spearman 依次为
`0.976190, 0.976190, 0.976190, 0.904762, 0.928571`。第六个完整单元、首个
crystallization world `seed468887863` 完成 `96/96` grid truth、`16/16` registered truth
和 `112/112` exact replay；candidate opportunity gate 通过，但 oracle `rho=0.595238`，
低于冻结门槛 `0.80`。该单元 typed-law design rank 为 `8`，蒸馏最大绝对误差仅
`2.33e-15`，因此失败来自 KNN4 局部预测，不再来自 typed-law 蒸馏。

stop rule 自动生效，后续 `9` 个 clusters 均未启动。v0.3 合计完成 `672/672` truth/replay，
fit/candidate overlap 为 `0`，candidate outcomes read 为 `0`，provider calls 为 `0`，没有换
seed、降阈值或删除失败 world。

将新失败加入 construction 后，统一的固定 ExtraTrees 候选在全部 `25` 个 exposed worlds 上
回放为 `25/25`、最低 `rho=0.833333`、中位数 `0.952381`。这只授权开发最后一个 v0.4
候选，不构成资格或 participant 证据。

机器收口：`work-ii-evidence-to-action-oracle-v0.3-qualification-closeout.json`。
